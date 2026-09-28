# -*- coding: utf-8 -*-
"""候选池采集（新策略）：probe 分级 → topic（变体+大 topic 分档拆分）→ org → 关键词 → 白名单 → 合并去重。

用法：
  python collect_pool.py                      # 全流程（当晚预算内跑多少算多少，断点续采）
  python collect_pool.py --only topic         # 只跑某阶段
  python collect_pool.py --dry-run            # 只打印将执行的查询，不联网
  python collect_pool.py --max-calls 3000     # 覆盖当晚调用预算
产物：data/snapshot_YYYYMMDD/pool.json + meta/{probe,run_summary}.json
"""
from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import sys as _sys, pathlib as _pl
ROOT = _pl.Path(__file__).resolve().parents[1]
for _d in (ROOT, ROOT / "lib", ROOT / "config"):
    _sys.path.insert(0, str(_d))
HERE = ROOT                      # 历史引用兼容：统一指向项目根
import db_profiles as dp        # noqa: E402
import strategy                 # noqa: E402
from gh import Budget, BudgetOut, GitHubClient, atomic_write_json  # noqa: E402

log = logging.getLogger("collect")
TODAY = datetime.now(timezone.utc).strftime("%Y%m%d")
STAR_MIN = dp.GLOBAL["star_min"]
PER_PAGE = dp.GLOBAL["per_page"]
CAP = dp.GLOBAL["per_page"] * dp.GLOBAL["max_pages"]      # 1000


# ---------------- 条目归一 ----------------

def slim(it: dict, source: str, source_topic: str = "") -> dict:
    owner = it.get("owner") or {}
    lic = it.get("license") or {}
    return {
        "full_name": it.get("full_name") or "",
        "html_url": it.get("html_url") or "",
        "description": it.get("description") or "",
        "topics": (it.get("topics") or [])[:20],
        "language": it.get("language") or "",
        "license": lic.get("spdx_id") or "",
        "fork": bool(it.get("fork")),
        "archived": bool(it.get("archived")),
        "created_at": (it.get("created_at") or "")[:10],
        "pushed_at": (it.get("pushed_at") or "")[:10],
        "updated_at": (it.get("updated_at") or "")[:10],
        "stars": it.get("stargazers_count") or 0,
        "forks": it.get("forks_count") or 0,
        "watchers": it.get("watchers_count") or 0,
        "open_issues": it.get("open_issues_count") or 0,
        "homepage": it.get("homepage") or "",
        "owner": owner.get("login") or "",
        "owner_type": owner.get("type") or "",
        "source": source, "source_topic": source_topic,
        "snapshot_date": TODAY,
    }


# ---------------- 大 topic 分档拆分 ----------------

STAR_BANDS = ["stars:>=1000", "stars:100..999", f"stars:{STAR_MIN}..99"]
YEAR0, YEAR1 = 2008, 2026


def _topic_of(q: str) -> str:
    return q.split()[0].split(":", 1)[1]


def collect_big_topic(client: GitHubClient, topic: str) -> list[dict]:
    """>1000 结果的 topic：star 三档；10-99 档超限再按创建年份/月拆分。"""
    base = f"topic:{topic} fork:false"
    out: dict[str, dict] = {}
    for band in STAR_BANDS:
        q = f"{base} {band}"
        total = client.search_total(q)
        if total == 0:
            continue
        if total <= CAP:
            for it in client.search_all(q):
                out.setdefault(it["full_name"], slim(it, "topic", topic))
            continue
        log.info("  topic:%s %s 共 %d > %d，按创建日期拆分", topic, band, total, CAP)
        for sub in _split_by_date(client, q):
            out.setdefault(sub["full_name"], sub)
    return list(out.values())


def _split_by_date(client: GitHubClient, q: str) -> list[dict]:
    """按创建年份线性拆；单年仍超限再按月拆（最细粒度）。"""
    parts = []
    for y in range(YEAR0, YEAR1 + 1):
        qy = f"{q} created:{y}-01-01..{y}-12-31"
        total = client.search_total(qy)
        if not total:
            continue
        if total <= CAP:
            for it in client.search_all(qy):
                parts.append(slim(it, "topic", _topic_of(q)))
        else:
            parts += _split_by_month(client, q, y)
    return parts


def _split_by_month(client: GitHubClient, q: str, year: int) -> list[dict]:
    import calendar
    parts = []
    for m in range(1, 13):
        last = calendar.monthrange(year, m)[1]
        qm = f"{q} created:{year}-{m:02d}-01..{year}-{m:02d}-{last}"
        if client.search_total(qm):
            for it in client.search_all(qm):
                parts.append(slim(it, "topic", _topic_of(q)))
    return parts


# ---------------- 各阶段 ----------------

def run(args):
    gen = strategy.derive()
    snap = HERE / "data" / f"snapshot_{args.date}"
    parts = snap / "parts"
    parts.mkdir(parents=True, exist_ok=True)
    state_p = HERE / "state" / "collect_state.json"
    state = {"date": args.date, "done": []}
    if state_p.is_file() and (imported := _load(state_p)).get("date") == args.date:
        state = imported

    only = args.only
    start = time.time()

    if args.dry_run:
        print("[dry-run] topic 查询：")
        disc = gen["DISCOVERY_TOPIC"]
        excl = " ".join(f"-topic:{t}" for t in gen["BIG_FOUR_MUTUAL_EXCLUDE"] if t != disc)
        print(f"  topic:{disc} fork:false {excl} （泛库桶互斥）")
        for t in gen["TOPICS"]:
            if t == disc:
                continue
            print(f"  topic:{t} fork:false [大topic自动分档: {' '.join(STAR_BANDS)}]")
        print("[dry-run] org 扫描：", " ".join(dict.fromkeys(gen["ORG_SCAN_LIST"])))
        print("[dry-run] 关键词检索：")
        for q in gen["KEYWORD_SEARCH_QUERIES"].values():
            print("  ", q)
        print("[dry-run] 白名单：", " ".join(gen["WHITELIST_REPOS"]))
        return

    client = GitHubClient(Budget(max_calls=args.max_calls))
    budget_stopped = None

    try:
        # ① topic
        if only in (None, "topic", "probe"):
            probe = {}
            probe_file = snap / "meta" / "probe.json"
            if probe_file.is_file():          # 断点续采：恢复已探测的量级
                probe = json.loads(probe_file.read_text(encoding="utf-8")).get("total_count") or {}
            if "probe" not in state["done"]:
                disc = gen["DISCOVERY_TOPIC"]
                excl = " ".join(f"-topic:{t}" for t in gen["BIG_FOUR_MUTUAL_EXCLUDE"] if t != disc)
                for t in gen["TOPICS"]:
                    if t in probe:
                        continue
                    q = f"topic:{disc} fork:false {excl}" if t == disc else f"topic:{t} fork:false"
                    probe[t] = client.search_total(q)
                    log.info("probe topic:%s = %d", t, probe[t])
                atomic_write_json(probe_file, {"date": args.date, "total_count": probe})
                state["done"].append("probe")
                atomic_write_json(state_p, state)

        if only in (None, "topic"):
            pool: dict[str, dict] = _load_parts(parts, "topic")
            disc = gen["DISCOVERY_TOPIC"]
            excl = " ".join(f"-topic:{t}" for t in gen["BIG_FOUR_MUTUAL_EXCLUDE"] if t != disc)
            for t in gen["TOPICS"]:
                if t in state["done"]:
                    continue
                q = f"topic:{disc} fork:false {excl}" if t == disc else f"topic:{t} fork:false"
                total = probe.get(t)
                if total is None:
                    total = client.search_total(q)
                if total == 0:
                    log.info("topic:%s = 0（known_empty 或空）", t)
                elif total <= CAP:
                    for it in client.search_all(q):
                        pool.setdefault(it["full_name"], slim(it, "topic", t))
                else:
                    pool.update({p["full_name"]: p for p in collect_big_topic(client, t)})
                atomic_write_json(parts / "topic.json", list(pool.values()))
                state["done"].append(t)
                atomic_write_json(state_p, state)
                log.info("topic:%s 完成，累计 %d", t, len(pool))

        # ② org
        if only in (None, "org"):
            pool = _load_parts(parts, "org")
            for o in dict.fromkeys(gen["ORG_SCAN_LIST"]):
                if f"org:{o}" in state["done"]:
                    continue
                for it in client.org_repos(o):
                    if (it.get("stargazers_count") or 0) >= STAR_MIN:
                        r = slim(it, "org", o)
                        pool[r["full_name"]] = r
                atomic_write_json(parts / "org.json", list(pool.values()))
                state["done"].append(f"org:{o}")
                atomic_write_json(state_p, state)
                log.info("org:%s 完成，累计 %d", o, len(pool))

        # ③ 关键词
        if only in (None, "keyword"):
            pool = _load_parts(parts, "keyword")
            for w, q in gen["KEYWORD_SEARCH_QUERIES"].items():
                if f"kw:{w}" in state["done"]:
                    continue
                for it in client.search_all(q):
                    r = slim(it, "keyword", w)
                    pool.setdefault(r["full_name"], r)
                atomic_write_json(parts / "keyword.json", list(pool.values()))
                state["done"].append(f"kw:{w}")
                atomic_write_json(state_p, state)
                log.info("keyword:%s 完成，累计 %d", w, len(pool))

        # ④ 白名单
        if only in (None, "whitelist"):
            if "whitelist" not in state["done"]:
                pool = {}
                for fn in gen["WHITELIST_REPOS"]:
                    try:
                        r = slim(client.repo(fn), "whitelist")
                        pool[r["full_name"]] = r
                    except Exception as e:      # noqa: BLE001 白名单失败不中断
                        log.warning("白名单 %s 失败：%s", fn, e)
                atomic_write_json(parts / "whitelist.json", list(pool.values()))
                state["done"].append("whitelist")
                atomic_write_json(state_p, state)

        # ⑤ 合并去重（通道优先级：whitelist > org > keyword > topic）
        if only in (None, "merge"):
            merged: dict[str, dict] = {}
            for stage in ("topic", "keyword", "org", "whitelist"):
                for it in _load_parts(parts, stage).values():
                    fn = it["full_name"]
                    if fn not in merged:
                        it.setdefault("all_sources", [])
                        merged[fn] = it
                    else:
                        srcs = merged[fn].setdefault("all_sources", [])
                        if it["source"] not in srcs and it["source"] != merged[fn]["source"]:
                            srcs.append(it["source"])
            merged_list = sorted(merged.values(),
                                 key=lambda x: -(x.get("stars") or 0))
            atomic_write_json(snap / "pool.json", merged_list)
            state["done"].append("merge")
            atomic_write_json(state_p, state)
            log.info("合并去重：%d 项 → pool.json", len(merged_list))

    except BudgetOut as e:
        budget_stopped = str(e)
        log.warning("预算先到，优雅收尾：%s", budget_stopped)

    summary = {"date": args.date, "stage": only or "full",
               "api_calls": client.stats_summary()["calls"],
               "elapsed_min": round((time.time() - start) / 60, 1),
               "budget_stopped": budget_stopped,
               "progress": state["done"]}
    atomic_write_json(snap / "meta" / "run_summary.json", summary)
    print("=" * 50)
    print(f"  完成。API {summary['api_calls']} 次 · {summary['elapsed_min']} 分钟")
    if budget_stopped:
        print(f"  预算停止：{budget_stopped}")
        print("  断点已存，重跑同命令自动续。")
    print("=" * 50)


def _load(p: Path):
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}


def _load_parts(parts: Path, stage: str) -> dict:
    p = parts / f"{stage}.json"
    if not p.is_file():
        return {}
    return {it["full_name"]: it for it in json.loads(p.read_text(encoding="utf-8"))}


def main():
    ap = argparse.ArgumentParser(description="新策略候选池采集")
    ap.add_argument("--date", default=TODAY)
    ap.add_argument("--only", choices=["probe", "topic", "org", "keyword",
                                       "whitelist", "merge"])
    ap.add_argument("--max-calls", type=int, default=4000)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("-v", action="store_true")
    args = ap.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.v else logging.INFO,
                        format="%(asctime)s %(levelname)-6s %(name)s | %(message)s",
                        datefmt="%H:%M:%S")
    run(args)


if __name__ == "__main__":
    main()
