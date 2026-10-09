# -*- coding: utf-8 -*-
"""信号富集采集：commit 活跃 / release / GHSA 安全通告 / contributor / 语言构成。

维度刷新原则（按数据变化成因二分）：
  push 依赖维度（commit/release/contrib/lang）——无 push 物理上不会变
  （发版必有 tag push、贡献者必有 commit、语言构成随代码变）：
      首轮必采；此后仅当 pushed_at 变化且到期才重采
  时间依赖维度（security）——GHSA 披露是外部事件，与仓库死活无关：到期即采
  整仓跳过：pushed_at 未变且无任何到期维度才跳过（修复旧版死仓连 security
  到期都被短路豁免的问题）；进 targets 只采到期维度（死仓只花 1 次调用）
分层（star 分层 + 国产 floor）：
  head(star>=1000)：commit/release 7 天、security 30 天、contrib 90 天、lang 一次性
  mid(star>=100)：commit/release 30 天、security 90 天、contrib/lang 一次性
  tail：仅 security 180 天；release/contrib/lang 首轮一次；死活看池 pushed_at（免费）
  国产仓 floor=mid（识别双信号：topics ∩ 国产 topic 集，或发现通道命中国产词/org），
  活跃国产仓享受 30 天 commit/release，死仓也只花 security 轮转
状态：state/enrich_state.json（断点/三振）+ state/enrich_cache_shards/ 256 分片
      （信号数据侧车，10-09 起分片，存取走 lib/enrich_store.py）
预算：--max-calls / --max-minutes / 保底线（gh.py 内置）

用法：
  python enrich.py --tier head                 # 头部增量刷新
  python enrich.py --tier all                  # 首轮铺全量（断点续采）
  python enrich.py --only commit --tier tail   # 单维度
"""
from __future__ import annotations

import argparse
import json
import logging
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import sys as _sys, pathlib as _pl
ROOT = _pl.Path(__file__).resolve().parents[1]
for _d in (ROOT, ROOT / "lib", ROOT / "config"):
    _sys.path.insert(0, str(_d))
HERE = ROOT                      # 历史引用兼容：统一指向项目根

import requests  # noqa: E402

import strategy                  # noqa: E402
from gh import Budget, BudgetOut, CoreReserveOut, GitHubClient, QuotaPatienceOut, atomic_write_json  # noqa: E402
from enrich_store import EnrichCacheStore  # noqa: E402  enrich_cache 分片存取（10-09 起）

log = logging.getLogger("enrich")
STATE = HERE / "state" / "enrich_state.json"
CACHE = HERE / "state" / "enrich_cache.json"   # 过渡期双写旧单文件（cutover 时与分片收口同步删）
THREE_STRIKES = 3
DIMS = ("commit", "release", "security", "contrib", "lang")
TIER_STAR = {"head": 1000, "mid": 100, "tail": 0}
# 每层采集的维度集合
TIER_DIMS = {
    "head": ("commit", "release", "security", "contrib", "lang"),
    "mid": ("commit", "release", "security", "contrib", "lang"),
    "tail": ("release", "security", "contrib", "lang"),   # 长尾不采 commit（死活看 pushed_at）
}
# 每层每维度刷新天数（None = 首轮采过即不再采）
REFRESH_DAYS = {
    "head": {"commit": 7, "release": 7, "security": 30, "contrib": 90, "lang": None},
    "mid":  {"commit": 30, "release": 30, "security": 90, "contrib": None, "lang": None},
    "tail": {"commit": None, "release": None, "security": 180, "contrib": None, "lang": None},
}
SEV_ORDER = {"critical": 4, "high": 3, "moderate": 2, "low": 1}


def _cn_signals():
    """国产识别信号（双信号：仓库自身 topics ∪ 发现通道命中），不改池 schema。"""
    cn = strategy.derive_sections()["cn"]
    return (set(cn["topics"]), set(cn["queries"]),
            {strategy.norm(o) for o in cn["orgs"]})


CN_TOPICS, CN_WORDS, CN_ORGS = _cn_signals()


def is_cn_item(it: dict) -> bool:
    if set(it.get("topics") or []) & CN_TOPICS:
        return True
    st = it.get("source_topic") or ""
    if it.get("source") == "keyword":
        return st in CN_WORDS
    if it.get("source") == "org":
        return st in CN_ORGS
    return False


def load_json(path: Path, default):
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return default


def _persist(cache: EnrichCacheStore) -> None:
    """落盘：分片 flush（只重写脏桶）+ 过渡期双写旧单文件（切换期保险，cutover 时去掉后者）。"""
    cache.flush()
    atomic_write_json(CACHE, cache)


def tier_of(stars: int, cn: bool = False) -> str:
    for name in ("head", "mid"):
        if stars >= TIER_STAR[name]:
            return name
    return "mid" if cn else "tail"    # 国产 floor=mid


def iso_days_ago(days: int) -> str:
    return (datetime.now(timezone.utc) - timedelta(days=days)) \
        .strftime("%Y-%m-%dT%H:%M:%SZ")


def days_since(date_str: str) -> int | None:
    if not date_str:
        return None
    try:
        d = datetime.strptime(date_str[:10], "%Y-%m-%d").replace(tzinfo=timezone.utc)
        return (datetime.now(timezone.utc) - d).days
    except ValueError:
        return None


def _needs_refresh(rec: dict, dim: str, refresh_days) -> bool:
    if refresh_days is None:
        return False
    ts = (rec.get("dims") or {}).get(dim)
    if not ts:
        return True
    try:
        done = datetime.strptime(ts, "%Y%m%d").replace(tzinfo=timezone.utc)
    except ValueError:
        return True
    return (datetime.now(timezone.utc) - done).days >= refresh_days


def due_dims(rec: dict, tier: str, pushed_changed: bool) -> list[str]:
    """到期维度：security 到期即采；push 依赖维度首轮必采、其后需 pushed_at 变化且到期。"""
    due = []
    for d in TIER_DIMS[tier]:
        rd = REFRESH_DAYS[tier][d]
        if d == "security":
            if _needs_refresh(rec, d, rd):
                due.append(d)
        elif not (rec.get("dims") or {}).get(d):
            due.append(d)
        elif pushed_changed and rd and _needs_refresh(rec, d, rd):
            due.append(d)
    return due


def collect_dims(client: GitHubClient, fn: str, cache: dict, dims: tuple,
                 pushed_changed: bool) -> dict:
    """对一个仓库执行到期的维度采集，返回信号字段（异常由调用方处理）。"""
    sig = cache.setdefault(fn, {})
    cache.touch(fn)          # 值字段是原地 update，脏桶追踪看不见——采集前显式标脏
    today = datetime.now(timezone.utc).strftime("%Y%m%d")
    if "commit" in dims:
        # 7 天必采；90 天条件采——死仓（7 天 0 提交且 pushed_at 未变）的 90 天数不会变
        c7 = client.commits_count(fn, iso_days_ago(7))
        if c7 or pushed_changed or "commit_90d" not in sig:
            sig["commit_90d"] = client.commits_count(fn, iso_days_ago(90))
        sig["commit_7d"] = c7
    if "release" in dims:
        try:
            rels = client.releases(fn)
        except requests.HTTPError as e:
            if getattr(e.response, "status_code", None) == 404:
                rels = []
            else:
                raise
        if rels:
            latest = rels[0]
            cutoff = datetime.now(timezone.utc) - timedelta(days=90)
            n90 = sum(1 for r in rels
                      if (r.get("published_at") or "")[:10] >= cutoff.strftime("%Y-%m-%d"))
            sig.update({"rel_ver": latest.get("tag_name"),
                        "rel_pub": (latest.get("published_at") or "")[:10],
                        "rel_days": days_since(latest.get("published_at") or ""),
                        "rel_n90": n90, "rel_pre": bool(latest.get("prerelease")),
                        "rel_none": False})
        else:
            sig.update({"rel_ver": None, "rel_none": True})
    if "security" in dims:
        try:
            advs = client.advisories(fn)
        except requests.HTTPError as e:
            if getattr(e.response, "status_code", None) == 404:
                advs = []
            else:
                raise
        live = [a for a in advs if a.get("withdrawn_at") is None]
        worst = max((a.get("severity") for a in live if a.get("severity") in SEV_ORDER),
                    key=lambda s: SEV_ORDER[s], default=None)
        sig.update({"sec_n": len(live),
                    "sec_worst": worst,
                    "sec_last": max(((a.get("published_at") or "")[:10] for a in live),
                                    default=None),
                    "sec_ids": [f'{a.get("ghsa_id")}({(a.get("cve_id") or "-")},{a.get("severity")})'
                                for a in live[:8]]})
    if "contrib" in dims:
        try:
            sig["contrib_n"] = client.contributors_count(fn)
        except requests.HTTPError as e:
            if getattr(e.response, "status_code", None) in (404, 409):
                sig["contrib_n"] = None
            else:
                raise
    if "lang" in dims:
        langs = client.languages(fn)
        total = sum(langs.values()) or 1
        sig["lang"] = {k: round(v * 100 / total) for k, v in
                       sorted(langs.items(), key=lambda x: -x[1])[:5]}
    sig["enriched_at"] = today
    # 字段级采集时间：enriched_at 是记录级触碰时间（多机合并取新用），
    # security-only 刷新会 bump enriched_at 而不动 commit_7d/rel_ver 等旧值——
    # 解读侧判断这些字段的新鲜度必须以 dim_ts 为准，防止陈旧值被"洗白"成今天
    tsmap = sig.setdefault("dim_ts", {})
    for d in dims:
        tsmap[d] = today
    return sig


def run(args):
    pool_path = Path(args.pool)
    if not pool_path.is_file():
        raise SystemExit(f"pool 不存在：{pool_path}（先跑 collect_intl.py / collect_cn.py）")
    pool = json.loads(pool_path.read_text(encoding="utf-8"))
    st = load_json(STATE, {"version": 1, "items": {}})
    cache = EnrichCacheStore()
    items = st["items"]

    tiers = ["head", "mid", "tail"] if args.tier == "all" else [args.tier]
    want_dims = [args.only] if args.only else None

    def pick_due() -> list:
        """到期目标：star 降序；已新鲜（无到期维度——含长尾死仓 pushed_at 未变）排除。
        跨窗重取：上一窗盖过时间戳的维度自动退出目标集（天然断点续采）。"""
        out = []
        for it in sorted(pool, key=lambda x: -(x.get("stars") or 0)):
            fn = it["full_name"]
            rec = items.get(fn) or {}
            if rec.get("status") in ("failed", "gone"):
                continue
            tier = tier_of(it.get("stars") or 0, cn=is_cn_item(it))
            if tier not in tiers:
                continue
            changed = (it.get("pushed_at") or "") != rec.get("pushed_checked")
            due = due_dims(rec, tier, changed)
            if want_dims:
                due = [d for d in due if d in want_dims]
            if due:
                out.append(fn)
        return out

    # 星层 tail、被 floor 提到 mid 的国产仓（日志口径）
    n_cn = sum(1 for it in pool
               if is_cn_item(it) and tier_of(it.get("stars") or 0) == "tail")

    client = GitHubClient(Budget(max_calls=args.max_calls, max_minutes=args.max_minutes))
    t0 = time.time()
    deadline = t0 + args.max_minutes * 60
    counts = {"done": 0, "failed": 0}
    quarantined = []
    stop_reason = None
    windows = waits = stuck_rounds = 0

    by_fn = {it["full_name"]: it for it in pool}
    targets: list = []                             # deadline 先触发时 summary 不炸
    log.info("层 %s · 维度 %s · 跨窗等待上限 %d 次 · 总时长 %s 分钟",
             tiers, want_dims or "按层", args.wait_windows, args.max_minutes)

    while True:
        if time.time() >= deadline:
            stop_reason = f"总时长达上限 {args.max_minutes} 分钟"
            break
        targets = pick_due()
        if not targets:
            break
        # 预算按窗发新的（跨窗续跑时每窗各得一份 max_calls/max_minutes，同 readme）
        client.budget = Budget(max_calls=args.max_calls, max_minutes=args.max_minutes)
        windows += 1
        done0 = counts["done"] + counts["failed"]
        log.info("第 %d 窗：到期目标 %d 项（池 %d · 国产 floor=mid 命中 %d）",
                 windows, len(targets), len(pool), n_cn)
        try:
            for i, fn in enumerate(targets):
                it = by_fn.get(fn, {})
                tier = tier_of(it.get("stars") or 0, cn=is_cn_item(it))
                rec = items.setdefault(fn, {"dims": {}, "fail_count": 0})
                changed = (it.get("pushed_at") or "") != rec.get("pushed_checked")
                dims = due_dims(rec, tier, changed)
                if want_dims:
                    dims = [d for d in dims if d in want_dims]
                if not dims:
                    continue
                try:
                    collect_dims(client, fn, cache, tuple(dims), changed)
                    today = datetime.now(timezone.utc).strftime("%Y%m%d")
                    for d in dims:                 # 只给真正采到的维度盖时间戳
                        rec["dims"][d] = today
                    rec["pushed_checked"] = it.get("pushed_at") or ""
                    rec["fail_count"] = 0
                    rec.pop("last_error", None)
                    counts["done"] += 1
                except requests.HTTPError as e:
                    code = getattr(e.response, "status_code", None)
                    if code in (404, 410):          # 仓库已删/私有：标记并隔离
                        rec.update({"status": "gone", "last_error": f"HTTP {code}"})
                        counts["failed"] += 1
                        continue
                    # 其余 HTTP 状态（409 空仓类/5xx 重试耗尽）按仓记振继续——
                    # 绝不 raise：毒仓会每晚卡死在同一位置，阻断其后全部目标
                    rec["fail_count"] += 1
                    rec["last_error"] = f"HTTP {code}"[:200]
                    if rec["fail_count"] >= THREE_STRIKES:
                        rec["status"] = "failed"
                        quarantined.append(fn)
                    counts["failed"] += 1
                    log.warning("%s HTTP %s(%d)：%s", fn, code, rec["fail_count"], str(e)[:60])
                    continue
                except (BudgetOut, QuotaPatienceOut):
                    raise                            # 预算/配额停止不算仓库失败
                except Exception as e:               # noqa: BLE001
                    rec["fail_count"] += 1
                    rec["last_error"] = str(e)[:200]
                    if rec["fail_count"] >= THREE_STRIKES:
                        rec["status"] = "failed"
                        quarantined.append(fn)
                    counts["failed"] += 1
                    log.warning("%s 失败(%d)：%s", fn, rec["fail_count"], str(e)[:80])
                    continue
                if (i + 1) % 50 == 0:
                    atomic_write_json(STATE, st)
                    _persist(cache)
                    log.info("进度 %d/%d · %s", i + 1, len(targets), counts)
            break                                  # 本窗自然扫完且无剩余到期项 → 收尾
        except CoreReserveOut as e:
            # Core 触保底线：按响应头 reset 睡到下一小时窗再续（跨窗推进的关键，
            # 否则 220 分钟预算只跑 ~50 分钟就收工——10-01 实测 4200 调/49.9 分）
            if args.wait_windows <= 0 or waits >= args.wait_windows:
                stop_reason = str(e)
                break
            reset = getattr(e, "reset", None)
            wait_sec = max(5.0, reset - time.time() + 5) if reset else 600.0
            if time.time() + wait_sec > deadline:
                stop_reason = f"{e}，等下一窗需 {wait_sec / 60:.0f} 分钟将超总时长上限"
                break
            waits += 1
            log.warning("Core 触保底线——睡 %.0f 分钟到下一小时窗再续（等待 %d/%d）",
                        wait_sec / 60, waits, args.wait_windows)
            time.sleep(wait_sec)
            continue
        except (BudgetOut, QuotaPatienceOut) as e:
            # 调用数达上限：有进展且允许跨窗 → 发新预算续跑；连续无进展收尾防空转
            progressed = (counts["done"] + counts["failed"]) > done0
            stuck_rounds = 0 if progressed else stuck_rounds + 1
            if args.wait_windows <= 0 or stuck_rounds >= 2:
                stop_reason = str(e) + ("（连续无进展，收尾防空转）"
                                        if stuck_rounds >= 2 else "")
                break
            if time.time() >= deadline:
                stop_reason = f"{e}，已达总时长上限"
                break
            log.info("本窗停止：%s（断点已存，续跑）", e)
            continue
        finally:
            atomic_write_json(STATE, st)
            _persist(cache)

    summary = {"tiers": tiers, "dims": want_dims or "per-tier", "targets": len(targets),
               "cn_floor_mid": n_cn,
               "counts": counts,
               "api_calls": client.stats_summary()["calls"],
               "elapsed_min": round((time.time() - t0) / 60, 1),
               "windows": windows, "waits": waits,
               "stop_reason": stop_reason, "quarantined": quarantined[:20]}
    atomic_write_json(HERE / "state" / "enrich_summary.json", summary)
    log.info("==== enrich 完成：%s · API %d 次 · %s 分钟 ====", counts,
             summary["api_calls"], summary["elapsed_min"])
    if stop_reason:
        log.warning("预算停止：%s（断点已存，重跑同命令续）", stop_reason)
    if quarantined:
        log.warning("三振隔离 %d 项：%s", len(quarantined), quarantined[:10])


def main():
    ap = argparse.ArgumentParser(description="信号富集：commit/release/security/contrib/lang")
    ap.add_argument("--pool", default=str(HERE / "data" / "snapshot_latest" / "pool.json"))
    ap.add_argument("--tier", choices=["head", "mid", "tail", "all"], default="head")
    ap.add_argument("--only", choices=DIMS, help="只跑单维度")
    ap.add_argument("--max-calls", type=int, default=4000)
    ap.add_argument("--max-minutes", type=float, default=90.0)
    ap.add_argument("--wait-windows", type=int, default=0,
                    help="Core 触保底线后按响应头 reset 睡到下一小时窗续跑的最多次数"
                         "（0=触线即收尾，旧行为）")
    ap.add_argument("-v", action="store_true")
    args = ap.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.v else logging.INFO,
                        format="%(asctime)s %(levelname)-6s %(name)s | %(message)s",
                        datefmt="%H:%M:%S")
    run(args)


if __name__ == "__main__":
    main()
