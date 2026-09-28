# -*- coding: utf-8 -*-
"""信号富集采集：commit 活跃 / release / GHSA 安全通告 / contributor / 语言构成。

覆盖并超越旧管道（daily_github/v2 run_enrich + commit_activity）：
  - commit：近 7 天（必采）+ 近 90 天（条件采：仅活跃仓，死仓跳过）
  - release：最新版 / 发布日 / 近 90 天发版数 / 预发布
  - security：GHSA 数量 / 最高严重级 / 最近披露 / ID 列表
  - contributor：贡献者总数（慢变量，各层基本一次性）
  - lang：语言构成（纯一次性，永不重采）
分层增量（每维度独立时间戳，节奏按数据变化速度定）：
  head(star>=1000)：commit/release 7 天、security 30 天、contrib 90 天、lang 一次性
  mid(star>=100)：commit/release 30 天、security 90 天、contrib/lang 一次性
  tail：仅 security 180 天；release/contrib/lang 首轮一次；死活靠池 pushed_at（免费）
死仓跳过：pushed_at 未变且已采过 → 长尾整仓跳过（趋零成本）
状态：state/enrich_state.json（断点/三振）+ state/enrich_cache.json（信号数据侧车）
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
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import sys as _sys, pathlib as _pl
ROOT = _pl.Path(__file__).resolve().parents[1]
for _d in (ROOT, ROOT / "lib", ROOT / "config"):
    _sys.path.insert(0, str(_d))
HERE = ROOT                      # 历史引用兼容：统一指向项目根

import requests  # noqa: E402

from gh import Budget, BudgetOut, GitHubClient, QuotaPatienceOut, atomic_write_json  # noqa: E402

log = logging.getLogger("enrich")
STATE = HERE / "state" / "enrich_state.json"
CACHE = HERE / "state" / "enrich_cache.json"
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


def load_json(path: Path, default):
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return default


def tier_of(stars: int) -> str:
    for name in ("head", "mid"):
        if stars >= TIER_STAR[name]:
            return name
    return "tail"


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


def collect_dims(client: GitHubClient, fn: str, cache: dict, dims: tuple,
                 pushed_changed: bool) -> dict:
    """对一个仓库执行到期的维度采集，返回信号字段（异常由调用方处理）。"""
    sig = cache.setdefault(fn, {})
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
    return sig


def run(args):
    pool_path = Path(args.pool)
    if not pool_path.is_file():
        raise SystemExit(f"pool 不存在：{pool_path}（先跑 collect_pool.py）")
    pool = json.loads(pool_path.read_text(encoding="utf-8"))
    st = load_json(STATE, {"version": 1, "items": {}})
    cache = load_json(CACHE, {})
    items = st["items"]

    tiers = ["head", "mid", "tail"] if args.tier == "all" else [args.tier]
    want_dims = [args.only] if args.only else None
    # 目标：按层过滤后 star 降序；已新鲜（维度时间戳未到期 + 长尾 pushed_at 未变整仓跳过）排除
    targets = []
    for it in sorted(pool, key=lambda x: -(x.get("stars") or 0)):
        tier = tier_of(it.get("stars") or 0)
        if tier not in tiers:
            continue
        fn = it["full_name"]
        rec = items.get(fn) or {}
        if rec.get("status") == "failed" and rec.get("fail_count", 0) >= THREE_STRIKES:
            continue
        dims = want_dims or TIER_DIMS[tier]
        pushed = it.get("pushed_at") or ""
        if tier == "tail" and rec.get("dims") and rec.get("pushed_checked") == pushed:
            continue  # 长尾死仓：pushed_at 未变且采过 → 整仓跳过
        if any(_needs_refresh(rec, d, REFRESH_DAYS[tier][d]) for d in dims):
            targets.append(fn)
    log.info("层 %s · 维度 %s · 目标 %d 项（池 %d）", tiers, want_dims or "按层",
             len(targets), len(pool))

    client = GitHubClient(Budget(max_calls=args.max_calls, max_minutes=args.max_minutes))
    t0 = time.time()
    counts = {"done": 0, "failed": 0}
    quarantined = []
    stop_reason = None

    by_fn = {it["full_name"]: it for it in pool}

    try:
        for i, fn in enumerate(targets):
            rec = items.setdefault(fn, {"dims": {}, "fail_count": 0})
            it = by_fn.get(fn, {})
            tier = tier_of(it.get("stars") or 0)
            dims = want_dims or TIER_DIMS[tier]
            pushed_changed = (it.get("pushed_at") or "") != rec.get("pushed_checked")
            try:
                collect_dims(client, fn, cache, dims, pushed_changed)
                today = datetime.now(timezone.utc).strftime("%Y%m%d")
                for d in dims:
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
                raise
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
                atomic_write_json(CACHE, cache)
                log.info("进度 %d/%d · %s", i + 1, len(targets), counts)
    except BudgetOut as e:
        stop_reason = str(e)
    finally:
        atomic_write_json(STATE, st)
        atomic_write_json(CACHE, cache)

    summary = {"tiers": tiers, "dims": want_dims or "per-tier", "targets": len(targets),
               "counts": counts,
               "api_calls": client.stats_summary()["calls"],
               "elapsed_min": round((time.time() - t0) / 60, 1),
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
    ap.add_argument("-v", action="store_true")
    args = ap.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.v else logging.INFO,
                        format="%(asctime)s %(levelname)-6s %(name)s | %(message)s",
                        datefmt="%H:%M:%S")
    run(args)


if __name__ == "__main__":
    main()
