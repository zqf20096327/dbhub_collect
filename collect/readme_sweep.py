# -*- coding: utf-8 -*-
"""README 采集：初始化 / 周增量 / 月全量（ETag 304 免费）。

去重链路（先去重再解读）：
  拉取层 fn→sha（一仓一拉）→ 内容层 归一化 SHA（同 sha 跳过，跨仓同内容共用）
  → 解读层由 interpret.py 消费（sha 键控）
状态机：pending → done / no_readme / oversized / failed（三振隔离）
预算：--max-calls / --max-minutes / --reserve 三重停止线 + 睡等上限（gh.py 内置）

用法：
  python readme_sweep.py --mode init [--pool data/snapshot_YYYYMMDD/pool.json]
  python readme_sweep.py --mode weekly --pool ...     # 仅 pushed_at 有变化的
  python readme_sweep.py --mode monthly --pool ...    # 全量 ETag 扫描
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

from gh import (Budget, BudgetOut, GitHubClient, QuotaPatienceOut,  # noqa: E402
                atomic_write_json)

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

def run(args):
    pool_path = Path(args.pool)
    if not pool_path.is_file():
        raise SystemExit(f"pool 不存在：{pool_path}（先跑 collect_pool.py）")
    pool = json.loads(pool_path.read_text(encoding="utf-8"))
    by_fn = {it["full_name"]: it for it in pool}
    st = load_state()
    items = st.setdefault("items", {})

    # 目标集合
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
    elif args.mode == "weekly":
        # 仅 pushed_at 晚于上次检查时间的
        targets = [it["full_name"] for it in pool
                   if (it.get("pushed_at") or "") > (items.get(it["full_name"]) or {}).get("checked_pushed", "")]
    else:  # monthly
        targets = [it["full_name"] for it in pool]

    # 过滤已完成（init 下 done/oversized/no_readme 跳过；monthly 下都要 ETag 复核）
    if args.mode == "init":
        targets = [fn for fn in targets
                   if (items.get(fn) or {}).get("status") not in ("done", "oversized", "no_readme")]
    elif args.mode == "weekly":
        targets = [fn for fn in targets if (items.get(fn) or {}).get("status") != "no_readme"]

    log.info("模式 %s · 目标 %d 项（池 %d）", args.mode, len(targets), len(pool))
    READMES.mkdir(parents=True, exist_ok=True)
    client = GitHubClient(Budget(max_calls=args.max_calls, max_minutes=args.max_minutes))
    t0 = time.time()
    counts = {"done": 0, "unchanged": 0, "no_readme": 0, "failed": 0, "oversized": 0}
    stop_reason = None
    quarantined = []

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
                if getattr(e.response, "status_code", None) == 404:
                    rec.update({"status": "no_readme", "etag": None, "fail_count": 0,
                                "last_error": ""})
                    counts["no_readme"] += 1
                    continue
                raise
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
                continue
            if text is None or not text.strip():
                rec.update({"status": "no_readme", "etag": None, "fail_count": 0})
                counts["no_readme"] += 1
                continue
            fn_to_file(fn).write_text(text, encoding="utf-8")
            nsha = sha1_of(normalize(text))
            rec.update({"status": "oversized" if truncated else "done",
                        "etag": new_etag, "sha": nsha,
                        "updated": datetime.now(timezone.utc).strftime("%Y%m%d"),
                        "checked_pushed": by_fn.get(fn, {}).get("pushed_at", ""),
                        "fail_count": 0, "last_error": ""})
            counts["oversized" if truncated else "done"] += 1
            if (i + 1) % 200 == 0:
                save_state(st)
                log.info("进度 %d/%d · %s", i + 1, len(targets), counts)
    except (BudgetOut, QuotaPatienceOut) as e:
        stop_reason = str(e)
    finally:
        save_state(st)

    summary = {"mode": args.mode, "targets": len(targets), "counts": counts,
               "api_calls": client.stats_summary()["calls"],
               "elapsed_min": round((time.time() - t0) / 60, 1),
               "stop_reason": stop_reason, "quarantined": quarantined[:20]}
    atomic_write_json(HERE / "state" / "readme_summary.json", summary)
    log.info("==== %s 完成：%s · API %d 次 · %s 分钟 ====", args.mode, counts,
             summary["api_calls"], summary["elapsed_min"])
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
    ap.add_argument("--max-minutes", type=float, default=90.0)
    ap.add_argument("-v", action="store_true")
    args = ap.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.v else logging.INFO,
                        format="%(asctime)s %(levelname)-6s %(name)s | %(message)s",
                        datefmt="%H:%M:%S")
    run(args)


if __name__ == "__main__":
    main()
