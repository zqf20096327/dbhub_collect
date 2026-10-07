#!/usr/bin/env python3
"""unattr_judge.py — 未归类项目判定器（手工执行，只读采集数据、只写自己的台账）。

定位：给每个未归类项目一个可查的判定——为什么没归上 + 属于哪类；
疑似 17 库生态的给出带证据的归属草案（签发权永远在人，进 config/overrides.json）。
不动 collect/interpret/db_scan 任何逻辑；不写归属。

四步流水：
  ① 圈范围：页面池未归类 ∩ 已解读（未解读留给夜间队列，不重复花钱）
  ② 信号层（零网络）：范围外标记/词表 → oos；教程词表 → edu；
     db_scan 有候选但从未裁决 → desc_pending；AI 裁决过无 support → judged_no_support
  ③ 侦查层（GitHub API）：E1 仓库树结构 + E3 依赖指纹（七语言清单）
  ④ 判定层：draft / recheck / gated_app_cat / no_evidence / partial_scan / api_error

用法（手工，建议 PYTHONUTF8=1）：
  python interpret/unattr_judge.py --dry-run          # 只看信号层统计，不联网不写盘
  python interpret/unattr_judge.py --limit 400        # 默认分批（API 配额安全）
  python interpret/unattr_judge.py --limit 0          # 全量（配额墙前优雅收尾，续跑接力）
  python interpret/unattr_judge.py --retry-errors     # 只补扫 api_error / partial_scan
  python interpret/unattr_judge.py --report-only      # 不联网，仅重出报告

产物：state/unattr_verdicts.json（幂等台账）+ state/unattr_judge_report.md（报告）。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]          # dbhub_collect
sys.path.insert(0, str(ROOT / "lib"))
from gh import load_env                             # noqa: E402  与现管线同款 .env 装载
from interp_store import load_cache                 # noqa: E402  分片缓存读取（兼容旧单文件）

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

CACHE = ROOT / "state" / "interp_cache.json"
SCAN = ROOT / "state" / "db_scan.json"
OUT = ROOT / "state" / "unattr_verdicts.json"
REPORT = ROOT / "state" / "unattr_judge_report.md"

DB_ORDER = ["PostgreSQL", "MySQL", "Oracle", "SQLite", "SQL Server", "ClickHouse",
            "MariaDB", "TiDB", "OceanBase", "PolarDB", "Dameng", "openGauss",
            "GaussDB", "GBase", "TDSQL", "YashanDB", "GoldenDB"]
DB17 = set(DB_ORDER)

# ── 词表 v2：范围外补 ignite/immudb/sled/convex/isar/heavydb/featurebase 等独立库本体；
#    命中名单在报告里列出供人工抽检（防普通英文词误伤） ──────────────────────
OOS_RE = re.compile(
    r"(redis|valkey|dragonfly|kvrocks|etcd|zookeeper|mongo|couch|neo4j|falkordb|"
    r"memgraph|arangodb|nebulagraph|qdrant|milvus|weaviate|pinecone|faiss|lancedb|"
    r"chromadb|elasticsearch|opensearch|meilisearch|typesense|solr|manticore|"
    r"duckdb|doris|starrocks|greenplum|vertica|trino|presto|bigquery|redshift|"
    r"databricks|snowflake|influx|timescale|tdengine|iotdb|questdb|cockroach|"
    r"yugabyte|singlestore|memsql|surreal|libsql|turso|realm|firebase|firestore|"
    r"dynamodb|hbase|cassandra|scylla|kafka|pulsar|rocksdb|badger|boltdb|sled|"
    r"leveldb|pebble|foundationdb|spacetimedb|dgraph|lowdb|dexie|indexeddb|pouchdb|"
    r"firebird|ignite|immudb|convex|isar|heavydb|heavyai|featurebase|monetdb|cratedb)", re.I)
EDU_RE = re.compile(
    r"(awesome|curated|interview|面试|教程|笔记|八股|roadmap|tutorial|cheatsheet|"
    r"leetcode|ebook|学习|入门|手册|宝典|boilerplate|starter[-_ ]?kit|study[-_ ]?notes|"
    r"源码解析|waking[-_ ]?up|30[-_ ]?days)", re.I)

# ── E1：库 ↔ 目录/文件名别名 ─────────────────────────────────────────────
DIR_ALIAS = {
    "PostgreSQL": ["postgres", "postgresql", "pgsql", "psycopg"],
    "MySQL": ["mysql"],
    "Oracle": ["oracle"],
    "SQLite": ["sqlite"],
    "SQL Server": ["mssql", "sqlserver", "sql_server", "mssqlserver"],
    "ClickHouse": ["clickhouse"],
    "MariaDB": ["mariadb"],
    "TiDB": ["tidb", "tikv"],
    "OceanBase": ["oceanbase"],
    "PolarDB": ["polardb", "polardbx"],
    "Dameng": ["dameng", "dm8"],
    "openGauss": ["opengauss"],
    "GaussDB": ["gaussdb"],
    "GBase": ["gbase"],
    "TDSQL": ["tdsql"],
    "YashanDB": ["yashan"],
    "GoldenDB": ["goldendb"],
}
DIR_CTX = re.compile(r"(connector|driver|adapter|dbms|dialect|backend|engine)", re.I)
FILE_PAT = re.compile(
    r"^(conn|dialect|driver|adapter|connector)_([a-z0-9_]+)\.(py|go|java|ts|js|rs|cs|rb|php|cpp)$", re.I)

# ── E3：依赖指纹（七语言清单通用的驱动/连接器名，精度优先） ────────────────
DEP_ALIAS = {
    "PostgreSQL": ["psycopg", "asyncpg", "pg8000", "lib/pq", "jackc/pgx",
                   "postgresql", "npgsql", "libpq"],
    "MySQL": ["pymysql", "mysqlclient", "mysql-connector", "go-sql-driver/mysql",
              "mysql2", "mysql-connector-java", "com.mysql", "mysql.data",
              "libmysql", "mysqlconnector"],
    "Oracle": ["oracledb", "cx-oracle", "cx_oracle", "go-oci8", "godror", "ojdbc",
               "oracle.manageddataaccess", "oracle-enhanced"],
    "SQLite": ["better-sqlite3", "sqlite-jdbc", "go-sqlite3", "rusqlite",
               "system.data.sqlite", "sqlite3"],
    "SQL Server": ["pymssql", "mssql-jdbc", "go-mssqldb", "sqljdbc",
                   "microsoft.data.sqlclient", "sqlclient"],
    "ClickHouse": ["clickhouse-driver", "clickhouse-connect", "clickhouse-jdbc",
                   "clickhouse-go", "clickhouse-rs"],
    "MariaDB": ["mariadb"],
    "TiDB": ["go-tidb", "pytidb"],
    "OceanBase": ["pyobclient", "oceanbase"],
    "Dameng": ["dmPython", "dm8"],
    "openGauss": ["psycopg2-opengauss", "opengauss"],
    "GBase": ["gbase"],
    "TDSQL": ["tdsql"],
}
DEP_FILE_RE = re.compile(
    r"(^|/)(requirements[\w.]*\.txt|pyproject\.toml|setup\.py|package\.json|go\.mod|"
    r"pom\.xml|Cargo\.toml|composer\.json|Gemfile|vcpkg\.json|conanfile\.(?:txt|py)|"
    r"[\w.\-]+\.csproj|CMakeLists\.txt)$")
WEAK_PATH_RE = re.compile(r"(^|/)(docs?|examples?|samples?|tests?|benchmarks?|demo)(/|$)", re.I)

TOOL_CATS = {"内核/引擎", "安全/审计", "测试/质量", "备份", "监控", "高可用",
             "迁移", "建模/设计", "连接/代理", "开发库", "管理", "平台"}

SESSION = requests.Session()
LOCK = threading.Lock()
API = "https://api.github.com"


def token_to_db(tok: str):
    for db, al in DIR_ALIAS.items():
        if tok in al:
            return db
    return None


def latest_by_fn(cache: dict) -> dict:
    m = {}
    for e in cache.values():
        if isinstance(e, dict) and e.get("fn"):
            cur = m.get(e["fn"])
            if cur is None or (e.get("generated_at") or "") >= (cur.get("generated_at") or ""):
                m[e["fn"]] = e
    return m


# ── collect-only 兜底：GitHub Actions 上无页面池，从本仓数据推导未归类名单 ──
def load_collect_rows(byfn: dict):
    """快照 pool.json + 规则词表(config/db_profiles) + AI 支持缓存 → 页面池同构行。
    口径镜像 build_demo 的四通道 + AI dbs（独立实现，仅用于候选发现，容许微小偏差）。"""
    sys.path.insert(0, str(ROOT / "config"))
    import db_profiles as dp

    def norm_topic(t):
        if isinstance(t, dict):
            t = t.get("name", "")
        return t.strip().lower()                 # 与 build_demo 逐字符一致（键不去引号）

    topic2db, org2db, watch2db, alias2db = {}, {}, {}, {}
    for p in dp.PROFILES:
        if not p.get("enabled", True):
            continue
        name = p["name"]
        for t in p.get("topics", []):
            topic2db[norm_topic(t)] = name
        for o in p.get("orgs", []):
            org2db[(o["name"] if isinstance(o, dict) else o).lower()] = name
        for w in p.get("watch", []):
            watch2db[w.lower()] = name
        for kw in p.get("search") or []:
            if isinstance(kw, str) and kw != "auto":
                topic2db[kw.strip('"').lower()] = name
        for a in p.get("aliases", []):
            try:
                re.compile(a)
                if any(c in a for c in r"\s[]()|*+?{}"):
                    continue
            except re.error:
                pass
            alias2db[a.lower()] = name
    topic2db.update(org2db)
    oos_tokens = {w.lower() for w in dp.GLOBAL.get("out_of_scope_dbs", [])}

    import pool_store
    try:
        items, _src = pool_store.load_latest("pool")
    except FileNotFoundError:
        raise SystemExit("collect 模式需要池（活文件或快照均无）")
    rows, seen = [], set()
    for it in items:
        fn = it.get("full_name") or ""
        if not fn or fn in seen:                     # 与 build_demo 主循环同款去重（first-wins）
            continue
        seen.add(fn)
        stopic = (it.get("source_topic") or "").strip().strip('\'"').strip().lower()
        dbs = set()
        db = topic2db.get(stopic, "")
        if not db and it.get("source") == "org":
            db = org2db.get(stopic, "")
        if db:
            dbs.add(db)
        for t in it.get("topics") or []:
            tl = t.lower()
            if tl in topic2db:
                dbs.add(topic2db[tl])
            elif tl in alias2db:
                dbs.add(alias2db[tl])
        if (it.get("owner") or "").lower() in org2db:
            dbs.add(org2db[it["owner"].lower()])
        e = byfn.get(fn)
        ai_dbs = ((e.get("classification") or {}).get("dbs") or []) if e else []
        if dbs or [d for d in ai_dbs if d in DB17]:
            continue                                    # 已归属（规则或 AI）→ 非未归类
        cat = (((e.get("classification") or {}).get("cat")) if e else "") or "其他"
        oos_hit = sorted({t for t in (it.get("topics") or [])} & oos_tokens)[:2]
        ev = ("范围外:" + ",".join(oos_hit)) if oos_hit else ""
        row = [fn, it.get("description") or "", it.get("language") or "",
               it.get("stars") or 0, 0, "", [], cat] + [""] * 14 + [ev]
        rows.append(row)
    rows.sort(key=lambda r: -r[3])
    return rows


def fetch_tree(fn: str):
    """main/master 直试；罕见默认分支（develop/2.x 等）用一次 repo API 兜底。"""
    for br in ("main", "master"):
        try:
            r = SESSION.get(f"{API}/repos/{fn}/git/trees/{br}?recursive=1",
                            timeout=(4, 25))
            if r.status_code == 200:
                j = r.json()
                return br, [t.get("path", "") for t in j.get("tree", [])], bool(j.get("truncated"))
        except requests.RequestException:
            continue
    try:
        info = SESSION.get(f"{API}/repos/{fn}", timeout=(4, 15))
        if info.status_code == 200:
            br = info.json().get("default_branch") or ""
            if br and br not in ("main", "master"):
                r = SESSION.get(f"{API}/repos/{fn}/git/trees/{br}?recursive=1",
                                timeout=(4, 25))
                if r.status_code == 200:
                    j = r.json()
                    return br, [t.get("path", "") for t in j.get("tree", [])], bool(j.get("truncated"))
    except requests.RequestException:
        pass
    return None


def fetch_raw(fn: str, branch: str, path: str) -> str:
    try:
        r = SESSION.get(f"https://raw.githubusercontent.com/{fn}/{branch}/{path}",
                        timeout=(4, 10))
        return r.text if r.status_code == 200 else ""
    except requests.RequestException:
        return ""


def scan_tree(paths):
    """E1：连接器语境路径 / conn_ 文件名 → [(db, 强度, 证据)]（强度恒 strong）。"""
    hits = []
    for p in paths:
        parts = p.lower().split("/")
        if len(parts) < 2:
            continue
        ctx = any(DIR_CTX.search(x) for x in parts[:-1])
        stem = parts[-1].rsplit(".", 1)[0] if "." in parts[-1] else parts[-1]
        db = token_to_db(stem) or (token_to_db(parts[-2]) if parts[-2] and "." not in parts[-2] else None)
        if ctx and db:
            hits.append((db, "strong", f"路径 {p}"))
            continue
        m = FILE_PAT.match(parts[-1])
        if m:
            db = token_to_db(m.group(2).lower().strip("_"))
            if db:
                hits.append((db, "strong", f"文件 {p}"))
    return hits


def scan_deps(paths, fn, branch):
    """E3：依赖清单 → [(db, 强度, 证据)]。根级优先+深度次之封顶 6 文件；
    docs/examples/tests 路径下的依赖证据降为 weak。"""
    dep_paths = [p for p in paths if DEP_FILE_RE.search(p)]
    dep_paths.sort(key=lambda p: (p.count("/"), p))
    hits, seen = [], set()
    for p in dep_paths[:6]:
        raw = fetch_raw(fn, branch, p)
        if not raw:
            continue
        strength = "weak" if WEAK_PATH_RE.search(p) else "med"
        low = raw.lower()
        for db, toks in DEP_ALIAS.items():
            for t in toks:
                if t in low and (db, p) not in seen:
                    seen.add((db, p))
                    hits.append((db, strength, f"依赖 {t} ∈ {p}"))
    return hits


def judge_one(r, scan, byfn):
    """单条判定：信号层（零网络）→ 侦查层（联网）→ 判定层。"""
    fn, stars, cat, lang, desc, ev_field = r[0], r[3], r[7], r[2], r[1], r[22]
    base = {"stars": stars, "cat": cat, "lang": lang or "无",
            "scanned": datetime.now().strftime("%Y-%m-%d")}

    # ② 信号层
    if (ev_field or "").find("范围外") >= 0 or OOS_RE.search(fn + " " + (desc or "")):
        return fn, {**base, "dbs": [], "status": "oos"}
    if EDU_RE.search(fn + " " + (desc or "")):
        return fn, {**base, "dbs": [], "status": "edu"}
    sc = scan.get(fn)
    cands = [d for d in ((sc.get("cands") if isinstance(sc, dict) else None) or {}) if d in DB17]
    e = byfn.get(fn)
    verdicts = ((e.get("classification") or {}).get("db_verdicts") or []) if e else []
    if cands and not verdicts:
        return fn, {**base, "dbs": [], "status": "desc_pending",
                    "evidence": ["简介候选: " + ",".join(cands)]}
    if verdicts:                                     # 问过、判过非 support
        return fn, {**base, "dbs": [], "status": "judged_no_support"}

    # ③ 侦查层
    got = fetch_tree(fn)
    if got is None:
        return fn, {**base, "dbs": [], "status": "api_error",
                    "evidence": ["取树失败/仓库不存在"]}
    branch, paths, truncated = got
    ev = scan_tree(paths) + (scan_deps(paths, fn, branch) if len(paths) <= 20000 else [])
    dbs = sorted({db for db, _, _ in ev}, key=DB_ORDER.index)
    if truncated:
        return fn, {**base, "dbs": dbs, "status": "partial_scan",
                    "evidence": [d for _, _, d in ev][:6], "branch": branch}
    if not dbs:
        return fn, {**base, "dbs": [], "status": "no_evidence", "branch": branch}

    # ④ 判定层：cat 门 + 证据强度（弱证据/独立库依赖模式 → recheck）
    strong = {db for db, s, _ in ev if s == "strong"}
    all_weak = all(s == "weak" for _, s, _ in ev)
    if cat not in TOOL_CATS:
        return fn, {**base, "dbs": [], "dbs_raw": dbs, "status": "gated_app_cat",
                    "evidence": [d for _, _, d in ev][:6], "branch": branch}
    if all_weak or (cat == "内核/引擎" and not strong):
        return fn, {**base, "dbs": dbs, "status": "recheck",
                    "evidence": [d for _, _, d in ev][:6], "branch": branch,
                    "strength": "weak" if all_weak else "dep_only"}
    return fn, {**base, "dbs": dbs, "status": "draft",
                "evidence": [d for _, _, d in ev][:6], "branch": branch,
                "strength": "strong" if strong else "med"}


def write_report(ledger: dict, skipped_n: int):
    st = {}
    for v in ledger.values():
        st[v.get("status", "?")] = st.get(v.get("status", "?"), 0) + 1
    lines = [
        "# unattr_judge 判定报告",
        f"生成：{datetime.now().strftime('%Y-%m-%d %H:%M')} · 台账 {len(ledger)} 条"
        f" · 圈外未解读 {skipped_n} 条（留给夜间队列）",
        "",
        "## 状态分布",
    ]
    lines += [f"- {k}: {v}" for k, v in sorted(st.items(), key=lambda x: -x[1])]
    hits = sorted([(fn, v) for fn, v in ledger.items() if v.get("status") == "draft"],
                  key=lambda x: -x[1]["stars"])
    lines += ["", f"## 归属草案（draft {len(hits)} 条，人工签发进 overrides.json；Top 30）", ""]
    for fn, v in hits[:30]:
        lines.append(f"- {v['stars']:>6}★ {fn} → {','.join(v['dbs'])}"
                     f"｜{v['evidence'][0] if v['evidence'] else ''}")
    lines += ["", "## 待复核（recheck：弱证据 / 独立库依赖模式）", ""]
    for fn, v in sorted([(a, b) for a, b in ledger.items() if b.get("status") == "recheck"],
                        key=lambda x: -x[1]["stars"]):
        lines.append(f"- {v['stars']:>6}★ {fn} → {','.join(v['dbs'])}（{v.get('strength')}）"
                     f"｜{v['evidence'][0] if v['evidence'] else ''}")
    lines += ["", "## 范围外命中抽检（防词表误伤，人工瞄一眼 Top 20）", ""]
    for fn, v in sorted([(a, b) for a, b in ledger.items() if b.get("status") == "oos"],
                        key=lambda x: -x[1]["stars"])[:20]:
        lines.append(f"- {v['stars']:>6}★ {fn}")
    lines += ["", f"## 分层小结：desc_pending {st.get('desc_pending', 0)}"
              f" · judged_no_support {st.get('judged_no_support', 0)}"
              f" · no_evidence {st.get('no_evidence', 0)}"
              f" · api_error/partial {st.get('api_error', 0) + st.get('partial_scan', 0)}"
              f"（--retry-errors 补扫）"]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description="未归类项目判定器（手工执行）")
    ap.add_argument("--page-pool", default="D:/dbhub_page/data/pool.js",
                    help="页面池 pool.js 路径（本地优先；缺失自动切 collect 模式）")
    ap.add_argument("--mode", choices=["auto", "page", "collect"], default="auto",
                    help="auto=页面池在用 page 否则 collect；collect=仅本仓数据推导（Actions 用）")
    ap.add_argument("--limit", type=int, default=400,
                    help="本轮扫描条数上限（0=全量；默认分批保 API 配额）")
    ap.add_argument("--threads", type=int, default=3)
    ap.add_argument("--retry-errors", action="store_true",
                    help="只补扫 api_error / partial_scan 条目")
    ap.add_argument("--dry-run", action="store_true", help="信号层统计，不联网不写盘")
    ap.add_argument("--report-only", action="store_true", help="不联网，仅重出报告")
    args = ap.parse_args()

    load_env()                                       # 读本仓 .env（GITHUB_TOKEN）
    tok = os.environ.get("GITHUB_TOKEN", "")
    if tok:
        SESSION.headers.update({"Authorization": f"Bearer {tok}",
                                "User-Agent": "unattr-judge"})
    else:
        print("警告：.env 无 GITHUB_TOKEN，匿名限速 60/hr", flush=True)

    cache = load_cache()
    byfn = latest_by_fn(cache)
    scan = json.loads(SCAN.read_text(encoding="utf-8"))

    use_collect = args.mode == "collect" or (
        args.mode == "auto" and not Path(args.page_pool).is_file())
    if use_collect:
        unattr = load_collect_rows(byfn)
        mode_note = "collect 模式（仅本仓数据推导，口径容许微小偏差）"
    else:
        s = Path(args.page_pool).read_text(encoding="utf-8")
        pool = json.loads(re.search(r"window\.POOL=(\[.*?\]);?\n", s, re.S).group(1))
        unattr = [r for r in pool if not r[5]]
        mode_note = "page 模式"

    todo = [r for r in unattr if r[0] in byfn]
    todo.sort(key=lambda r: -r[3])
    skipped_n = len(unattr) - len(todo)
    print(f"[{mode_note}] 未归类 {len(unattr)} · 已解读 {len(todo)} · 未解读(圈外) {skipped_n}", flush=True)

    # 信号层预演（零网络出数）
    sig = {"oos": 0, "edu": 0, "desc_pending": 0, "judged_no_support": 0, "需侦查": 0}
    for r in todo:
        fn, desc, evf = r[0], r[1], r[22]
        if (evf or "").find("范围外") >= 0 or OOS_RE.search(fn + " " + (desc or "")):
            sig["oos"] += 1
        elif EDU_RE.search(fn + " " + (desc or "")):
            sig["edu"] += 1
        else:
            cands = [d for d in (((scan.get(fn) or {}).get("cands")) or {}) if d in DB17]
            vd = (byfn[fn].get("classification") or {}).get("db_verdicts") or []
            sig["desc_pending" if (cands and not vd) else ("judged_no_support" if vd else "需侦查")] += 1
    print("信号层预演:", sig, flush=True)
    if args.dry_run:
        return

    ledger = json.loads(OUT.read_text(encoding="utf-8")) if OUT.is_file() else {}
    # 幂等策略：网络产物（draft/recheck/gated/no_evidence）粘住不重扫；
    # 信号层产物（oos/edu/desc_pending/judged）随管线/快照演变——垫后重算。
    # 批次排序：全新条目优先（先消化积压），可重试次之，易变态重算垫后——
    # 否则星序头部的重算会吃掉 limit，新侦查推进不动（实测批次2仅净进80条）。
    STICKY_NET = {"draft", "recheck", "gated_app_cat", "no_evidence"}
    RETRYABLE = {"api_error", "partial_scan"}
    fresh, retry, volatile = [], [], []
    for r in todo:
        st_old = (ledger.get(r[0]) or {}).get("status")
        if st_old is None:
            fresh.append(r)
        elif st_old in RETRYABLE:
            retry.append(r)
        elif st_old not in STICKY_NET:
            volatile.append(r)
    batch = retry if args.retry_errors else (fresh + retry + volatile)
    batch = batch if args.limit <= 0 else batch[:args.limit]
    if not args.report_only:
        print(f"本轮联网扫描 {len(batch)} 条 · {args.threads} 线程", flush=True)
        t0, err_streak, done_n = time.time(), 0, 0
        with ThreadPoolExecutor(max_workers=args.threads) as ex:
            futs = {ex.submit(judge_one, r, scan, byfn): r[0] for r in batch}
            for fut in as_completed(futs):
                try:
                    fn, rec = fut.result()
                except Exception as exc:              # 单条异常不拖垮整轮
                    fn, rec = futs[fut], {"status": "api_error", "evidence": [f"异常 {exc}"]}
                with LOCK:
                    ledger[fn] = rec
                    done_n += 1
                    err_streak = err_streak + 1 if rec.get("status") == "api_error" else 0
                    if done_n % 20 == 0:
                        OUT.write_text(json.dumps(ledger, ensure_ascii=False), encoding="utf-8")
                        hit = sum(1 for v in ledger.values() if v.get("dbs"))
                        print(f"  进度 {done_n}/{len(batch)} · 有据 {hit}"
                              f" · {(time.time()-t0)/60:.1f} 分钟", flush=True)
                if err_streak >= 8:                   # 连续失败≈配额/网络墙
                    ex.shutdown(cancel_futures=True)  # 真正取消未起跑的任务（否则 with 块会跑完全部）
                    print("连续 8 条失败（疑似配额墙），本轮收尾——续跑自动接力", flush=True)
                    break
        OUT.write_text(json.dumps(ledger, ensure_ascii=False), encoding="utf-8")
        print(f"扫描完成：{done_n} 条 · {(time.time()-t0)/60:.1f} 分钟", flush=True)

    write_report(ledger, skipped_n)
    drafts = sum(1 for v in ledger.values() if v.get("status") == "draft")
    print(f"台账 {OUT}\n报告 {REPORT}", flush=True)
    print(f"==== 判定小结：draft {drafts} 条 · 详见报告 ====", flush=True)


if __name__ == "__main__":
    main()
