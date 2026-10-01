# -*- coding: utf-8 -*-
"""README 采集：初始化 / 周增量 / 月全量（ETag 304 免费）。

去重链路（先去重再解读）：
  拉取层 fn→sha（一仓一拉）→ 内容层 归一化 SHA（同 sha 跳过，跨仓同内容共用）
  → 解读层由 interpret.py 消费（sha 键控）
状态机：pending → done / no_readme / oversized / failed（三振隔离）
预算：--max-calls / --max-minutes / --reserve 三重停止线 + 睡等上限（gh.py 内置）
跨窗：--wait-windows N——Core 触保底线时按失败响应的 X-RateLimit-Reset 睡到
      配额恢复再续断点，最多 N 次；--max-total-minutes 管住整次调用（含等待）的墙钟。

用法：
  python readme_sweep.py --mode init [--pool data/snapshot_YYYYMMDD/pool.json]
  python readme_sweep.py --mode weekly --pool ...     # 仅 pushed_at 有变化的
  python readme_sweep.py --mode monthly --pool ...    # 全量 ETag 扫描
  python readme_sweep.py --mode weekly --pool ... --wait-windows 10   # CI 跨窗续
产物：state/readme_state.json（原子写+轮转）+ data/readmes/{fn安全名}.md
"""
from __future__ import annotations

import argparse
import json
import logging
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import sys as _sys, pathlib as _pl
ROOT = _pl.Path(__file__).resolve().parents[1]
for _d in (ROOT, ROOT / "lib", ROOT / "config"):
    _sys.path.insert(0, str(_d))
HERE = ROOT                      # 历史引用兼容：统一指向项目根
import requests

from gh import (Budget, BudgetOut, CoreReserveOut, GitHubClient,  # noqa: E402
                QuotaPatienceOut, atomic_write_json)

log = logging.getLogger("readme")
STATE = HERE / "state" / "readme_state.json"
READMES = HERE / "data" / "readmes"
THREE_STRIKES = 3


# ---------------- 归一化 + SHA（内容级去重键） ----------------

def normalize(txt: str) -> str:
    """剥徽章/链接/HTML/URL/空白——只留语义文本。"""
    t = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", txt or "")
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
    t = re.sub(r"<[^>]+>", "", t)
    t = re.sub(r"https?://\S+", "", t)
    return re.sub(r"\s+", " ", t).strip().lower()


def sha1_of(txt: str) -> str:
    import hashlib
    return hashlib.sha1(txt.encode("utf-8", "ignore")).hexdigest()[:12]


def fn_to_file(fn: str) -> Path:
    return READMES / (fn.replace("/", "__") + ".md")


# ---------------- 状态 ----------------

def load_state() -> dict:
    if STATE.is_file():
        return json.loads(STATE.read_text(encoding="utf-8"))
    return {"version": 1, "items": {}}


def save_state(st: dict) -> None:
    atomic_write_json(STATE, st)


# ---------------- 主流程 ----------------

# 月度校准标记：本进程 UTC 日。304/200/404 校验过的仓打上，pick_targets(monthly)
# 据此排除——否则每窗从池头重新枚举，3000/窗的预算全花在对同一批仓重复发 304 条件
# 请求上，后面的仓永远轮不到（2026-10-01 首次 monthly 实发：连开 6 窗只扫到前 3000）。
CAL_DATE = datetime.now(timezone.utc).strftime("%Y%m%d")


def pick_targets(args, pool: list, items: dict) -> list:
    """按模式取待扫目标（failed=三振隔离，剔除防跨窗轮空转；monthly 排除当日已校准项）。"""
    if args.mode == "init":
        # 按 star 降序铺，先高价值；--layer1 只铺分类层对象（canon 命中者由 classify 产出）
        targets = [it["full_name"] for it in
                   sorted(pool, key=lambda x: -(x.get("stars") or 0))]
        if args.layer1:
            reg = HERE / "state" / "registry.json"
            if reg.is_file():
                layer1 = {r["fn"] for r in json.loads(reg.read_text(encoding="utf-8"))
                          ["items"] if r.get("layer") == 1}
                targets = [fn for fn in targets if fn in layer1]
            else:
                log.warning("registry.json 不存在，忽略 --layer1 全量铺")
        skip = ("done", "oversized", "no_readme", "failed")
        return [fn for fn in targets
                if (items.get(fn) or {}).get("status") not in skip]
    if args.mode == "weekly":
        # 仅 pushed_at 晚于上次检查时间的
        return [it["full_name"] for it in pool
                if (it.get("pushed_at") or "") > (items.get(it["full_name"]) or {}).get("checked_pushed", "")
                and (items.get(it["full_name"]) or {}).get("status") not in ("no_readme", "failed")]
    # monthly：全量校准但排除本 UTC 日已校验过的（跨窗推进；无此排除会每窗从头重扫）
    return [it["full_name"] for it in pool
            if (items.get(it["full_name"]) or {}).get("calibrated") != CAL_DATE]


def run(args):
    pool_path = Path(args.pool)
    if not pool_path.is_file():
        raise SystemExit(f"pool 不存在：{pool_path}（先跑 collect_pool.py）")
    pool = json.loads(pool_path.read_text(encoding="utf-8"))
    by_fn = {it["full_name"]: it for it in pool}
    st = load_state()
    items = st.setdefault("items", {})

    READMES.mkdir(parents=True, exist_ok=True)
    client = GitHubClient(Budget(max_calls=args.max_calls, max_minutes=args.max_minutes))
    reserve = client.budget.reserve_remaining
    t0 = time.time()
    deadline = t0 + args.max_total_minutes * 60 if args.max_total_minutes else None
    counts = {"done": 0, "unchanged": 0, "no_readme": 0, "failed": 0, "oversized": 0}
    stop_reason = None
    quarantined = []
    windows = waits = total_calls = 0
    stuck_rounds = 0
    targets = pick_targets(args, pool, items)
    targets0 = len(targets)
    log.info("模式 %s · 目标 %d 项（池 %d）· 跨窗等待上限 %d 次 · 总时长 %s 分钟",
             args.mode, targets0, len(pool), args.wait_windows,
             args.max_total_minutes or "∞")

    while targets:
        if deadline and time.time() >= deadline:
            stop_reason = f"总时长达上限 {args.max_total_minutes} 分钟"
            break
        # 窗口预检（/rate_limit 免费不计配额）：仅本地 PAT 场景有效——Actions
        # GITHUB_TOKEN 上探测与真实调用分属不同桶（09-30 实测探测 5000/调用头
        # 800），CI 的等待由 CoreReserveOut.reset 驱动（见下方 except 分支）
        rl = client.core_rate_limit()
        rem = (rl or {}).get("remaining")
        if rem is not None and rem <= reserve:
            if waits >= args.wait_windows:
                stop_reason = (f"Core 剩余配额触保底线（remaining={rem}），"
                               f"跨窗等待 {args.wait_windows} 次已用尽")
                break
            reset = (rl or {}).get("reset") or (time.time() + 60)
            wait_sec = max(5.0, reset - time.time() + 5)
            if deadline and time.time() + wait_sec > deadline:
                stop_reason = (f"Core 触保底线（remaining={rem}），等下一窗需 "
                               f"{wait_sec / 60:.0f} 分钟将超总时长上限")
                break
            waits += 1
            log.warning("Core 剩余 %d 触保底线——睡 %.0f 分钟到下一小时窗（等待 %d/%d）",
                        rem, wait_sec / 60, waits, args.wait_windows)
            time.sleep(wait_sec)
            targets = pick_targets(args, pool, items)
            continue
        # 本窗一轮：预算按窗发新的（跨窗续跑时每窗各得一份 max_calls/max_minutes）
        client.budget = Budget(max_calls=args.max_calls, max_minutes=args.max_minutes)
        windows += 1
        done0 = sum(counts.values())
        round_stop = None
        round_exc: Exception | None = None
        log.info("第 %d 窗：目标 %d 项 · Core 剩余 %s", windows, len(targets),
                 rem if rem is not None else "?")
        try:
            for i, fn in enumerate(targets):
                rec = items.setdefault(fn, {"status": "pending", "fail_count": 0})
                if rec.get("status") == "failed" and rec.get("fail_count", 0) >= THREE_STRIKES:
                    quarantined.append(fn)
                    continue
                etag = rec.get("etag")
                try:
                    r = client.readme_conditional(fn, etag)
                    status, text, new_etag = r[0], r[1], r[2]
                    truncated = r[3] if len(r) > 3 else False
                except requests.HTTPError as e:
                    code = getattr(e.response, "status_code", None)
                    if code == 404:
                        rec.update({"status": "no_readme", "etag": None, "fail_count": 0,
                                    "last_error": "", "calibrated": CAL_DATE})
                        counts["no_readme"] += 1
                        continue
                    # 其余 HTTP 状态按仓记振继续（毒仓不得阻断循环，与 enrich 同策略）
                    rec["fail_count"] += 1
                    rec["last_error"] = f"HTTP {code}"[:200]
                    if rec["fail_count"] >= THREE_STRIKES:
                        rec["status"] = "failed"
                        quarantined.append(fn)
                    counts["failed"] += 1
                    log.warning("%s HTTP %s(%d)", fn, code, rec["fail_count"])
                    continue
                except (BudgetOut, QuotaPatienceOut):
                    # 预算/配额停止是全局事件（由外层优雅收尾），绝不能记成该仓失败——
                    # 旧版在这里被 except Exception 吞掉，预算触线后剩余目标被逐个记
                    # 假振次，三晚后错误隔离约 2.4k 仓（2026-09-29 实发事故）
                    raise
                except Exception as e:                     # noqa: BLE001
                    rec["fail_count"] += 1
                    rec["last_error"] = str(e)[:200]
                    if rec["fail_count"] >= THREE_STRIKES:
                        rec["status"] = "failed"
                        quarantined.append(fn)
                    counts["failed"] += 1
                    log.warning("%s 失败(%d)：%s", fn, rec["fail_count"], str(e)[:80])
                    continue
                if status == 304:
                    counts["unchanged"] += 1
                    rec["checked_pushed"] = by_fn.get(fn, {}).get("pushed_at", "")
                    rec["calibrated"] = CAL_DATE
                    continue
                if text is None or not text.strip():
                    rec.update({"status": "no_readme", "etag": None, "fail_count": 0,
                                "calibrated": CAL_DATE})
                    counts["no_readme"] += 1
                    continue
                fn_to_file(fn).write_text(text, encoding="utf-8")
                nsha = sha1_of(normalize(text))
                rec.update({"status": "oversized" if truncated else "done",
                            "etag": new_etag, "sha": nsha,
                            "updated": datetime.now(timezone.utc).strftime("%Y%m%d"),
                            "checked_pushed": by_fn.get(fn, {}).get("pushed_at", ""),
                            "fail_count": 0, "last_error": "",
                            "calibrated": CAL_DATE})
                counts["oversized" if truncated else "done"] += 1
                if (i + 1) % 200 == 0:
                    save_state(st)
                    log.info("进度 %d/%d · %s", i + 1, len(targets), counts)
        except CoreReserveOut as e:
            round_stop, round_exc = str(e), e
        except QuotaPatienceOut as e:
            round_stop, round_exc = str(e), e
        except BudgetOut as e:
            round_stop, round_exc = str(e), e
        finally:
            save_state(st)
        total_calls += client.budget.calls
        progressed = sum(counts.values()) > done0
        stuck_rounds = 0 if progressed else stuck_rounds + 1
        if round_stop is None:
            # 本轮自然扫完：目标集仍在收缩才续下一轮（monthly 全量单轮即止，防空转）
            nxt = pick_targets(args, pool, items)
            if len(nxt) < len(targets):
                targets = nxt
                continue
            break
        if args.wait_windows <= 0:
            stop_reason = round_stop
            break
        if isinstance(round_exc, (CoreReserveOut, QuotaPatienceOut)):
            # 真实配额触线——睡到失败响应自带的 reset 再续。等待决策必须走
            # 这条路而非窗口预检：Actions GITHUB_TOKEN 的 /rate_limit 与真实
            # 调用分属不同桶（09-30 实测探测 5000 / 调用头 800）
            if waits >= args.wait_windows:
                stop_reason = f"{round_stop}，跨窗等待 {args.wait_windows} 次已用尽"
                break
            reset = getattr(round_exc, "reset", None)
            wait_sec = max(5.0, reset - time.time() + 5) if reset else 600.0
            if deadline and time.time() + wait_sec > deadline:
                stop_reason = (f"{round_stop}，等下一窗需 {wait_sec / 60:.0f} 分钟"
                               f"将超总时长上限")
                break
            waits += 1
            log.warning("配额触线——睡 %.0f 分钟到下一窗再续（等待 %d/%d）",
                        wait_sec / 60, waits, args.wait_windows)
            time.sleep(wait_sec)
            targets = pick_targets(args, pool, items)
            continue
        if stuck_rounds >= 2:
            stop_reason = f"{round_stop}（连续 {stuck_rounds} 轮无进展，收尾防空转）"
            break
        log.info("本窗停止：%s（断点已存，续跑）", round_stop)
        targets = pick_targets(args, pool, items)

    summary = {"mode": args.mode, "targets": targets0, "counts": counts,
               "api_calls": total_calls,
               "elapsed_min": round((time.time() - t0) / 60, 1),
               "windows": windows, "waits": waits,
               "stop_reason": stop_reason, "quarantined": quarantined[:20]}
    atomic_write_json(HERE / "state" / "readme_summary.json", summary)
    log.info("==== %s 完成：%s · API %d 次 · %s 分钟 · %d 窗/等 %d 次 ====", args.mode, counts,
             summary["api_calls"], summary["elapsed_min"], windows, waits)
    if stop_reason:
        log.warning("预算停止：%s（断点已存，重跑同命令续）", stop_reason)
    if quarantined:
        log.warning("三振隔离 %d 项（人工复核）：%s", len(quarantined), quarantined[:10])


def main():
    ap = argparse.ArgumentParser(description="README 采集（init/weekly/monthly）")
    ap.add_argument("--mode", choices=["init", "weekly", "monthly"], required=True)
    ap.add_argument("--pool", default=str(HERE / "data" / "snapshot_latest" / "pool.json"))
    ap.add_argument("--layer1", action="store_true", help="init 时只铺分类层对象")
    ap.add_argument("--max-calls", type=int, default=4000)
    ap.add_argument("--max-minutes", type=float, default=90.0,
                    help="单窗墙钟上限（跨窗续跑时每窗各一份）")
    ap.add_argument("--wait-windows", type=int, default=0,
                    help="Core 触保底线后睡到下一小时窗续跑的最多次数（0=立即收尾，"
                         "等待用 /rate_limit 的 reset 对齐）")
    ap.add_argument("--max-total-minutes", type=float, default=None,
                    help="整次调用（含跨窗等待）的墙钟上限，超时优雅收尾")
    ap.add_argument("-v", action="store_true")
    args = ap.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.v else logging.INFO,
                        format="%(asctime)s %(levelname)-6s %(name)s | %(message)s",
                        datefmt="%H:%M:%S")
    run(args)


if __name__ == "__main__":
    main()
