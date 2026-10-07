# -*- coding: utf-8 -*-
"""池采集共享核心：collect_intl.py / collect_cn.py 的公共实现。

按 section 参数化的差异点（策略单一事实源：db_profiles.GLOBAL["sections"] + orgs 的 class）：
  intl：topic/keyword 带 stars:>=10；超 1000 结果按星三档→年→月拆；新项目窗口
        stars:>=3 created:>=45天前（窗口结果并入同通道 parts，复用 source 枚举，
        下游无感知）；窗口最易腐烂（次晚自愈不成立），排在当晚最前
  cn  ：国产不设星——topic/keyword 查询不加星限定；超 1000 结果纯按创建年→月拆
        （绝不套星档：防止拆档路径隐性给国产加上 >=10）；无新项目窗口（主通道
        无星线，新仓从第 0 天起即被覆盖）
  org：class=dedicated（org 即产品）不设星线；class=cloud（云厂商超集 org，
        含大量非数据库 SDK）与国际 org 用 star_min 当范围噪音闸

截断修复（方案评审漏洞一）：任何检索查询 total>1000 一律拆分抓取——旧版只有
topic 有拆档、keyword 在 1000 处静默截断（实测 sqlite keyword 正好顶在 1000）。

产物（两脚本完全隔离；merge 带完成门控，不出半成品池）：
  data/snapshot_DATE/parts_{sec}/{topic,keyword,org,whitelist}.json
  data/snapshot_DATE/pool_{sec}.json —— section 完成标记（全部阶段跑完才写）
  data/snapshot_DATE/pool.json —— 两侧完成标记都在才写的并集（固定 intl→cn 顺序）；
  任一侧未跑/预算截断时 pool.json 不更新，下游 ls -t 回退昨池
状态：state/collect_state_{sec}.json（按日期断点续采；次日晚新日期全量重跑）
meta：meta/probe_{sec}.json（各查询量级曲线，国产召回验收观测点）+ run_summary_{sec}.json
"""
from __future__ import annotations

import argparse
import calendar
import json
import logging
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import sys as _sys, pathlib as _pl
ROOT = _pl.Path(__file__).resolve().parents[1]
for _d in (ROOT, ROOT / "lib", ROOT / "config"):
    _sys.path.insert(0, str(_d))
HERE = ROOT
import db_profiles as dp        # noqa: E402
import strategy                 # noqa: E402
from gh import Budget, BudgetOut, GitHubClient, atomic_write_json  # noqa: E402

log = logging.getLogger("collect")
CAP = dp.GLOBAL["per_page"] * dp.GLOBAL["max_pages"]      # GitHub Search 单查询 1000 硬上限
YEAR0 = 2008
YEAR1 = datetime.now(timezone.utc).year
STAGES = ("new", "topic", "keyword", "org", "whitelist", "merge")
MERGE_STAGES = ("topic", "keyword", "org", "whitelist")   # 通道优先级：whitelist > org > keyword > topic
# 仓库黑名单（GLOBAL.exclude_repos + 各库档案 exclude_repos 并集）：
# 检索查询带 -repo: 挡 search API，merge/union 过滤兜底（org 列表 API 与旧池残留）
BLACKLIST = set(dp.GLOBAL.get("exclude_repos") or []) \
    | {ex for p in dp.PROFILES for ex in (p.get("exclude_repos") or [])}
_REPO_EXCL = "".join(f" -repo:{ex}" for ex in sorted(BLACKLIST))
# 用户级黑名单（整 owner 屏蔽）：名单在 config/exclude_users.txt，一行一个 login。
# 不能拼 -user: 进查询——GitHub Search 查询 256 字符上限，大名单会让查询整条失效；
# 改为结果落地即丢：_slim_many 挡全部检索通道，merge/union 兜底挡 org/白名单/旧池残留
_USER_FILE = ROOT / "config" / "exclude_users.txt"
USER_BLACKLIST = {u.lower() for u in dp.GLOBAL.get("exclude_users") or []}
if _USER_FILE.is_file():
    # utf-8-sig：兼容 Windows 记事本 BOM（裸 utf-8 会把首行读成 \ufeffxxx 匹配不上）
    USER_BLACKLIST |= {ln.strip().lower() for ln in
                       _USER_FILE.read_text(encoding="utf-8-sig").splitlines()
                       if ln.strip() and not ln.startswith("#")}
else:
    log.warning("config/exclude_users.txt 不存在")
log.info("用户黑名单：%d 人", len(USER_BLACKLIST))


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
    }


def _slim_many(items, source: str, label: str) -> dict:
    return {it["full_name"]: slim(it, source, label) for it in items
            if (it.get("full_name") or "").split("/", 1)[0].lower()
            not in USER_BLACKLIST}


# ---------------- 抓取（含截断修复 + 分 section 拆档） ----------------

def _split_by_date(client: GitHubClient, q: str, source: str, label: str) -> dict:
    """按创建年份线性拆；单年仍超限再按月拆（最细粒度）。不引入任何星限定。"""
    out: dict[str, dict] = {}
    for y in range(YEAR0, YEAR1 + 1):
        qy = f"{q} created:{y}-01-01..{y}-12-31"
        st = client.search_total(qy)
        if not st:
            continue
        if st <= CAP:
            out.update(_slim_many(client.search_all(qy), source, label))
        else:
            for m in range(1, 13):
                last = calendar.monthrange(y, m)[1]
                qm = f"{q} created:{y}-{m:02d}-01..{y}-{m:02d}-{last}"
                if client.search_total(qm):
                    out.update(_slim_many(client.search_all(qm), source, label))
    return out


def fetch_all(client: GitHubClient, q: str, source: str, label: str) -> tuple[dict, int]:
    """任意查询全量：total>1000 按创建期拆（keyword 截断修复；也用于新项目窗口）。"""
    total = client.search_total(q)
    if total == 0:
        return {}, 0
    if total <= CAP:
        return _slim_many(client.search_all(q), source, label), total
    log.info("  %s 命中 %d > %d，按创建期拆分", label, total, CAP)
    return _split_by_date(client, q, source, label), total


def fetch_topic(client: GitHubClient, base: str, star: int, label: str) -> tuple[dict, int]:
    """topic 查询：star>0 时主查询带 stars:>=star；超 CAP 时星三档拆、档内再退化日期拆；
    star=0（国产）超 CAP 直接日期拆——星档绝不落到无星线 section 上（评审漏洞二）。"""
    q = f"{base} stars:>={star}" if star else base
    total = client.search_total(q)
    if total == 0:
        return {}, 0
    if total <= CAP:
        return _slim_many(client.search_all(q), "topic", label), total
    log.info("  topic:%s 共 %d > %d，拆分抓取（星档=%s）", label, total, CAP,
             "on" if star else "off")
    if not star:                        # 无星线：直接日期拆，不重复探测总量
        return _split_by_date(client, q, "topic", label), total
    out: dict[str, dict] = {}
    for band in ("stars:>=1000", "stars:100..999", f"stars:{star}..99"):
        sub = f"{base} {band}"
        st = client.search_total(sub)
        if not st:
            continue
        if st <= CAP:
            out.update(_slim_many(client.search_all(sub), "topic", label))
        else:
            out.update(_split_by_date(client, sub, "topic", label))
    return out, total


def org_star_line(o, section: str) -> int:
    cls = strategy.org_class(o, section)
    return 0 if cls == "dedicated" else dp.GLOBAL["star_min"]


def _orgs_dedup(orgs: list) -> dict:
    """同名 org 去重（档案间重复声明，如 percona/ApsaraDB），保首个声明。"""
    out: dict = {}
    for o in orgs:
        out.setdefault(strategy.norm(o), o)
    return out


# ---------------- 查询构造 ----------------

def discovery_base(exclude_topics: list[str]) -> str:
    excl = " ".join(f"-topic:{t}" for t in exclude_topics)
    return f"topic:{dp.GLOBAL['discovery_topics'][0]} fork:false {excl}".strip()


def run(section: str, args) -> None:
    if section == "cn" and args.only == "new":
        print("国产无新项目窗口（主通道无星线，新仓从第 0 天起即被覆盖），--only new 无事可做")
        return
    secs = strategy.derive_sections()
    sec = secs[section]
    star = sec["star_min"]
    snap = HERE / "data" / f"snapshot_{args.date}"
    parts = snap / f"parts_{section}"
    parts.mkdir(parents=True, exist_ok=True)
    state_p = HERE / "state" / f"collect_state_{section}.json"
    state = {"date": args.date, "done": []}
    if state_p.is_file():
        imported = _load(state_p)
        if imported.get("date") == args.date:
            state = imported

    only = args.only
    disc = dp.GLOBAL["discovery_topics"][0]
    big_four_excl = [t for t in dp.GLOBAL["big_four"] if t != disc]

    if args.dry_run:
        print(f"[dry-run] section={section} star_min={star}"
              + (f"（--only {only}：仅执行该阶段，以下为该 section 全部查询预览）" if only else ""))
        for t in sec["topics"]:
            base = (discovery_base(big_four_excl) if t == disc
                    else f"topic:{t} fork:false") + _REPO_EXCL
            print(f"  topic: {base}" + (f" stars:>={star}" if star else "")
                  + ("（大topic自动分档）" if star else "（超1000按创建期拆）"))
        for w, q in sec["queries"].items():
            print(f"  search: {q}")
        for name, o in _orgs_dedup(sec["orgs"]).items():
            print(f"  org: {name} (star_line={org_star_line(o, section)})")
        print("  whitelist:", " ".join(sec["watch"]))
        if section == "intl":
            cutoff = _cutoff(sec["new_days"])
            ns = sec["new_star_min"]
            print(f"[dry-run] 新项目窗口 stars:>={ns} created:>={cutoff}：")
            for t in sec["topics"]:
                base = (discovery_base(big_four_excl) if t == disc
                    else f"topic:{t} fork:false") + _REPO_EXCL
                print(f"  new: {base} stars:>={ns} created:>={cutoff}")
            for w in sec["queries"]:
                print(f"  new: {w} fork:false stars:>={ns} created:>={cutoff}")
        return

    client = GitHubClient(Budget(max_calls=args.max_calls, max_minutes=args.max_minutes))
    budget_stopped = None
    totals: dict[str, int] = {}
    start = time.time()

    try:
        # ① 新项目窗口（仅 intl；最易腐烂，最先跑）。结果并入同通道 parts
        if section == "intl" and only in (None, "new"):
            if "new" not in state["done"]:
                cutoff = _cutoff(sec["new_days"])
                ns = sec["new_star_min"]
                pool_t = _load_parts(parts, "topic")
                pool_k = _load_parts(parts, "keyword")
                for t in sec["topics"]:
                    base = (discovery_base(big_four_excl) if t == disc
                    else f"topic:{t} fork:false") + _REPO_EXCL
                    items, total = fetch_all(client, f"{base} stars:>={ns} created:>={cutoff}",
                                             "topic", t)
                    for fn, r in items.items():
                        pool_t.setdefault(fn, r)
                    totals[f"new:topic:{t}"] = total
                for w in sec["queries"]:
                    items, total = fetch_all(
                        client, f"{w} fork:false stars:>={ns} created:>={cutoff}{_REPO_EXCL}",
                        "keyword", w)
                    for fn, r in items.items():
                        pool_k.setdefault(fn, r)
                    totals[f"new:kw:{w}"] = total
                atomic_write_json(parts / "topic.json", list(pool_t.values()))
                atomic_write_json(parts / "keyword.json", list(pool_k.values()))
                state["done"].append("new")
                _save(state_p, state)
                log.info("新项目窗口完成，topic 累计 %d · keyword 累计 %d",
                         len(pool_t), len(pool_k))

        # ② topic
        if only in (None, "topic"):
            pool = _load_parts(parts, "topic")
            for t in sec["topics"]:
                if f"topic:{t}" in state["done"]:
                    continue
                base = (discovery_base(big_four_excl) if t == disc
                    else f"topic:{t} fork:false") + _REPO_EXCL
                items, total = fetch_topic(client, base, star, t)
                totals[f"topic:{t}"] = total
                if total == 0:
                    log.info("topic:%s = 0（known_empty 或空）", t)
                for fn, r in items.items():
                    pool.setdefault(fn, r)
                atomic_write_json(parts / "topic.json", list(pool.values()))
                state["done"].append(f"topic:{t}")
                _save(state_p, state)
                log.info("topic:%s 完成（%d 条），累计 %d", t, len(items), len(pool))

        # ③ keyword
        if only in (None, "keyword"):
            pool = _load_parts(parts, "keyword")
            for w, q in sec["queries"].items():
                if f"kw:{w}" in state["done"]:
                    continue
                items, total = fetch_all(client, q, "keyword", w)
                totals[f"kw:{w}"] = total
                for fn, r in items.items():
                    pool.setdefault(fn, r)
                atomic_write_json(parts / "keyword.json", list(pool.values()))
                state["done"].append(f"kw:{w}")
                _save(state_p, state)
                log.info("keyword:%s 完成（%d 条），累计 %d", w, len(items), len(pool))

        # ④ org
        if only in (None, "org"):
            pool = _load_parts(parts, "org")
            for name, o in _orgs_dedup(sec["orgs"]).items():
                if f"org:{name}" in state["done"]:
                    continue
                line = org_star_line(o, section)
                for it in client.org_repos(name):
                    if (it.get("stargazers_count") or 0) >= line:
                        r = slim(it, "org", name)
                        pool[r["full_name"]] = r
                atomic_write_json(parts / "org.json", list(pool.values()))
                state["done"].append(f"org:{name}")
                _save(state_p, state)
                log.info("org:%s 完成（star_line=%d），累计 %d", name, line, len(pool))

        # ⑤ 白名单（不受星线约束）
        if only in (None, "whitelist"):
            if "whitelist" not in state["done"]:
                pool = {}
                for fn in sec["watch"]:
                    try:
                        r = slim(client.repo(fn), "whitelist")
                        pool[r["full_name"]] = r
                    except Exception as e:      # noqa: BLE001 白名单失败不中断
                        log.warning("白名单 %s 失败：%s", fn, e)
                atomic_write_json(parts / "whitelist.json", list(pool.values()))
                state["done"].append("whitelist")
                _save(state_p, state)

        # ⑥ merge：先校验本 section 全部阶段完成（防 --only merge 把半成品写成完成标记），
        # 再写完成标记 pool_{section}.json；另一侧标记也在时才写并集 pool.json
        if only in (None, "merge"):
            expected = ({"whitelist"}
                        | {f"topic:{t}" for t in sec["topics"]}
                        | {f"kw:{w}" for w in sec["queries"]}
                        | {f"org:{name}" for name in _orgs_dedup(sec["orgs"])})
            if section == "intl":
                expected.add("new")
            missing = expected - set(state["done"])
            if missing:
                log.warning("阶段未完成（缺 %d 项，样例 %s）——不 merge，本日不出池",
                            len(missing), sorted(missing)[:3])
            else:
                _merge_step(snap, section)
                state["done"].append("merge")
                _save(state_p, state)

    except BudgetOut as e:
        budget_stopped = str(e)
        log.warning("预算先到，优雅收尾（merge 未执行，本日不出池）：%s", budget_stopped)

    summary = {"date": args.date, "section": section, "stage": only or "full",
               "api_calls": client.stats_summary()["calls"],
               "elapsed_min": round((time.time() - start) / 60, 1),
               "budget_stopped": budget_stopped,
               "progress": state["done"]}
    atomic_write_json(snap / "meta" / f"run_summary_{section}.json", summary)
    if totals:
        probe_p = snap / "meta" / f"probe_{section}.json"
        probe = _load(probe_p) if probe_p.is_file() else {"date": args.date, "total_count": {}}
        probe["total_count"].update(totals)
        atomic_write_json(probe_p, probe)
    print("=" * 50)
    print(f"  [{section}] 完成。API {summary['api_calls']} 次 · {summary['elapsed_min']} 分钟")
    if budget_stopped:
        print(f"  预算停止：{budget_stopped}")
        print("  断点已存，同日重跑同命令自动续。")
    print("=" * 50)


def _cutoff(days: int) -> str:
    now = datetime.now(timezone.utc)
    if days <= 0:
        return now.strftime("%Y-%m-%d")
    return (now - timedelta(days=days)).strftime("%Y-%m-%d")


def _load(p: Path):
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}


def _save(p: Path, state) -> None:
    atomic_write_json(p, state)


def _load_parts(parts: Path, stage: str) -> dict:
    p = parts / f"{stage}.json"
    if not p.is_file():
        return {}
    return {it["full_name"]: it for it in json.loads(p.read_text(encoding="utf-8"))}


def _merge_parts(parts: Path) -> dict:
    """单 section 内四通道合并去重（先 topic 后 keyword/org/whitelist，first-writer 为主记录）。"""
    merged: dict[str, dict] = {}
    dropped = 0
    for stage in MERGE_STAGES:
        for it in _load_parts(parts, stage).values():
            fn = it["full_name"]
            if fn in BLACKLIST or fn.split("/", 1)[0].lower() in USER_BLACKLIST:
                dropped += 1
                continue
            if fn not in merged:
                it.setdefault("all_sources", [])
                merged[fn] = it
            else:
                srcs = merged[fn].setdefault("all_sources", [])
                if it["source"] not in srcs and it["source"] != merged[fn]["source"]:
                    srcs.append(it["source"])
    if dropped:
        log.info("黑名单过滤：merge 丢弃 %d 条（parts_%s）", dropped, parts.name)
    return merged


def _merge_step(snap: Path, section: str) -> None:
    """写本 section 完成标记 pool_{section}.json；另一侧标记也在时才写并集 pool.json。

    parts_* 不入库（gitignore）——CI/换机续跑时只有 state（记录"已完成"）而没有 parts，
    此时绝不能从空 parts 重写池（2026-09-29 实发事故：CI 把 3.4 万项的池写成 []），
    应保留既有 pool_{section}.json 直接参与并集。
    """
    parts = snap / f"parts_{section}"
    own_pool = snap / f"pool_{section}.json"
    if parts.is_dir() and any(parts.glob("*.json")):
        merged_list = sorted(_merge_parts(parts).values(),
                             key=lambda x: -(x.get("stars") or 0))
        if merged_list or not own_pool.is_file():   # 空结果不覆盖既有好池
            atomic_write_json(own_pool, merged_list)
        else:
            log.warning("parts_%s 合并结果为空，保留既有 pool_%s.json", section, section)
    elif own_pool.is_file():
        n = len(json.loads(own_pool.read_text(encoding="utf-8")))
        log.warning("parts_%s 不在本机（CI/换机续跑）——保留既有 pool_%s.json（%d 项）",
                    section, section, n)
    else:
        log.warning("既无 parts_%s 也无 pool_%s.json，本 section 无产物可合并", section, section)
    other = "cn" if section == "intl" else "intl"
    if not (snap / f"pool_{other}.json").is_file():
        log.warning("pool_%s.json 未生成（未跑或预算截断），pool.json 暂不更新（下游回退昨池）",
                    other)
        return
    union = _union_pools(snap)
    atomic_write_json(snap / "pool.json",
                      sorted(union.values(), key=lambda x: -(x.get("stars") or 0)))
    log.info("合并：pool_%s → pool.json 并集 %d 项", section, len(union))


def _union_pools(snap: Path) -> dict:
    """跨 section 并集：只读两侧完成标记 pool_{sec}.json，固定 intl→cn 顺序，与执行顺序无关。"""
    union: dict[str, dict] = {}
    dropped = 0
    for sec_name in ("intl", "cn"):
        p = snap / f"pool_{sec_name}.json"
        if not p.is_file():
            continue
        for it in json.loads(p.read_text(encoding="utf-8")):
            fn = it["full_name"]
            if fn in BLACKLIST or fn.split("/", 1)[0].lower() in USER_BLACKLIST:
                dropped += 1
                continue
            if fn not in union:
                it.setdefault("all_sources", [])
                union[fn] = it
            else:
                srcs = union[fn].setdefault("all_sources", [])
                if it["source"] not in srcs and it["source"] != union[fn]["source"]:
                    srcs.append(it["source"])
    if dropped:
        log.info("黑名单过滤：union 丢弃 %d 条", dropped)
    return union


def run_main(section: str) -> None:
    ap = argparse.ArgumentParser(
        description=f"候选池采集·{'国际(stars>=10+新项目窗口)' if section == 'intl' else '国产(无星线)'}")
    ap.add_argument("--date", default=datetime.now(timezone.utc).strftime("%Y%m%d"))
    ap.add_argument("--only", choices=list(STAGES))
    ap.add_argument("--max-calls", type=int, default=4000)
    ap.add_argument("--max-minutes", type=float, default=120.0)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("-v", action="store_true")
    args = ap.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.v else logging.INFO,
                        format="%(asctime)s %(levelname)-6s %(name)s | %(message)s",
                        datefmt="%H:%M:%S")
    run(section, args)
