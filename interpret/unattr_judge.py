#!/usr/bin/env python3
"""unattr_judge.py — 未归类项目判定器 v2（T2e 薄壳，零网络，2026-11-01 重写）。

定位不变：给每个未归类项目一个可查的判定——为什么没归上 + 属于哪类；
疑似 17 库生态的给出带证据的归属草案（签发权永远在人，进 config/overrides.json）。

旧版（10-29 口径修正版已 stash 存档，六处修正全部吸收）自打 GitHub API 的
E1/E3 侦查层退役——证据层分片（evidence_collect 31,884 仓）+ attribution
引擎（T2b matcher × T2c quorum）接管判定；本文件只剩四步薄壳：

  ① 圈范围：无 README 行号引证 ∩ 已解读（10-29 口径沿用：唯有行号引证算
     已有归属，规则/AI 预归属照常进判定；未解读留给夜间队列）
  ② 信号层（口径与旧版逐字不变，零网络）：范围外词表 → oos（v3 含 graal）；
     教程词表 → edu；db_scan 有候选从未裁决 → desc_pending；
     AI 裁决过无 support → judged_no_support
  ③ 证据层读取（零网络）：state/evidence_cache_shards 按 rec["fn"] 对齐；
     无记录/partial → pending_evidence（进增量补采队列；
     api_error/partial_scan 两状态退役）；empty_repo/gone → no_evidence 终局
  ④ 判定层（attribution 引擎）：build_pack × judge →
     case_opened   → draft（quorum ≥2 票立案；镜像/目录级单证 strength=strong）
     below_quorum  → recheck（单弱信号只记录：全 0.5=weak / 仅 topic=topic_only /
                      其余凑不满 2 票=dep_only）——43 案例 dep_only 清单同源
     空包          → no_evidence；cat 非 Tool → gated_app_cat（dbs_raw 留痕）

CLI 兼容：--mode/--limit/--dry-run/--report-only/--min-stars 保留
（零网络后 --limit 默认 0=全量，跑一轮 ≈ 十秒级）；--threads/--retry-errors
随网络层一起退役。台账 state/unattr_verdicts.json 字段结构兼容
（status/dbs/evidence/strength/branch/stars/lang/cat/scanned）——
collect/pool_core 出池闸门与 tools/unattr_prescreen 两消费方零改动。
evidence 字符串保持旧格式（"依赖 w ∈ 清单"/"路径 p"/"镜像 w ∈ p"），
prescreen 的红旗解析（∈ 清单名）与 overrides 备料照常工作。

产物：state/unattr_verdicts.json（幂等台账，compact+tmp/replace+LF 原子写）+
state/unattr_judge_report.md（报告）。旧 draft 122 名单已冻结存档
state/unattr_draft_122_archive.md（T3a 素材）。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]          # dbhub_collect
for p in (str(ROOT), str(ROOT / "lib")):
    if p not in sys.path:
        sys.path.insert(0, p)

from attribution.api import judge                    # noqa: E402  T2a/T2c 引擎入口
from attribution.matcher import build_pack           # noqa: E402  T2b 匹配器

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

SCAN = ROOT / "state" / "db_scan.json"
OUT = ROOT / "state" / "unattr_verdicts.json"
REPORT = ROOT / "state" / "unattr_judge_report.md"
EVIDENCE_SHARDS = ROOT / "state" / "evidence_cache_shards"
INTERP_SHARDS = ROOT / "state" / "interp_cache_shards"

DB_ORDER = ["PostgreSQL", "MySQL", "Oracle", "SQLite", "SQL Server", "ClickHouse",
            "MariaDB", "TiDB", "OceanBase", "PolarDB", "Dameng", "openGauss",
            "GaussDB", "GBase", "TDSQL", "YashanDB", "GoldenDB"]
DB17 = set(DB_ORDER)

# ── 信号层词表（口径与旧版逐字不变；v3 含 graal）─────────────────────────
OOS_RE = re.compile(
    r"(redis|valkey|dragonfly|kvrocks|etcd|zookeeper|mongo|couch|neo4j|falkordb|"
    r"memgraph|arangodb|nebulagraph|qdrant|milvus|weaviate|pinecone|faiss|lancedb|"
    r"chromadb|elasticsearch|opensearch|meilisearch|typesense|solr|manticore|"
    r"duckdb|doris|starrocks|greenplum|vertica|trino|presto|bigquery|redshift|"
    r"databricks|snowflake|influx|timescale|tdengine|iotdb|questdb|cockroach|"
    r"yugabyte|singlestore|memsql|surreal|libsql|turso|realm|firebase|firestore|"
    r"dynamodb|hbase|cassandra|scylla|kafka|pulsar|rocksdb|badger|boltdb|sled|"
    r"leveldb|pebble|foundationdb|spacetimedb|dgraph|lowdb|dexie|indexeddb|pouchdb|"
    r"firebird|ignite|immudb|convex|isar|heavydb|heavyai|featurebase|monetdb|"
    r"cratedb|graal)", re.I)
EDU_RE = re.compile(
    r"(awesome|curated|interview|面试|教程|笔记|八股|roadmap|tutorial|cheatsheet|"
    r"leetcode|ebook|学习|入门|手册|宝典|boilerplate|starter[-_ ]?kit|study[-_ ]?notes|"
    r"源码解析|waking[-_ ]?up|30[-_ ]?days)", re.I)

TOOL_CATS = {"内核/引擎", "安全/审计", "测试/质量", "备份", "监控", "高可用",
             "迁移", "建模/设计", "连接/代理", "开发库", "管理", "平台"}


def load_interp_projection() -> dict[str, dict]:
    """解读分片流式最小投影：fn → {cat, db_verdicts}（99MB 分片勿全载进 dict；
    generated_at 取最新，等价旧版 latest_by_fn）。"""
    out: dict[str, dict] = {}
    for p in sorted(INTERP_SHARDS.glob("*.json")):
        for rec in json.loads(p.read_text(encoding="utf-8")).values():
            fn = rec.get("fn") or ""
            if not fn:
                continue
            g = rec.get("generated_at") or ""
            cur = out.get(fn)
            if cur is not None and g < cur["_g"]:
                continue
            cls = rec.get("classification") or {}
            out[fn] = {"cat": cls.get("cat") or "其他",
                       "db_verdicts": cls.get("db_verdicts") or [], "_g": g}
    return out


def load_evidence_for(scope: set[str]) -> dict[str, dict]:
    """证据分片流式读取，只留圈内 fn（75MB 勿全载；分片键形态不一按 rec["fn"]）。"""
    out: dict[str, dict] = {}
    for p in sorted(EVIDENCE_SHARDS.glob("*.json")):
        for rec in json.loads(p.read_text(encoding="utf-8")).values():
            fn = rec.get("fn") or ""
            if fn in scope:
                out[fn] = rec
    return out


def collect_rows(interp: dict, scan: dict) -> list[dict]:
    """池（pool_store 滚动活文件）→ 圈内行：无行号引证者进判定（10-29 口径：
    唯有 README 行号引证算已有归属；规则/AI 预归属照常进判定）。"""
    sys.path.insert(0, str(ROOT / "config"))
    import db_profiles as dp
    oos_tokens = {w.lower() for w in dp.GLOBAL.get("out_of_scope_dbs", [])}

    import pool_store
    try:
        items, _src = pool_store.load_latest("pool")
    except FileNotFoundError:
        raise SystemExit("collect 模式需要池（活文件或快照均无）")
    rows, seen = [], set()
    for it in items:
        fn = it.get("full_name") or ""
        if not fn or fn in seen:                     # first-wins 去重（同旧版）
            continue
        seen.add(fn)
        cands = ((scan.get(fn) or {}).get("cands") if isinstance(scan.get(fn), dict) else None) or {}
        if any(any(c.get("line") is not None for c in v) for v in cands.values()):
            continue                                 # 已有 README 行号引证 → 无需判定
        oos_hit = sorted({t for t in (it.get("topics") or [])} & oos_tokens)[:2]
        rows.append({"fn": fn, "desc": it.get("description") or "",
                     "lang": it.get("language") or "", "stars": it.get("stars") or 0,
                     "topics": list(it.get("topics") or []),
                     "cat": (interp.get(fn) or {}).get("cat", "其他"),
                     "ev": ("范围外:" + ",".join(oos_hit)) if oos_hit else ""})
    rows.sort(key=lambda r: -r["stars"])
    return rows


def page_rows(interp: dict) -> list[dict]:
    """页面池 pool.js → 圈内行（本地调试用；行结构 [fn,desc,lang,stars,?,?,'',[],cat,…,ev]）。"""
    s = Path(_PAGE_POOL_DEFAULT).read_text(encoding="utf-8")
    pool = json.loads(re.search(r"window\.POOL=(\[.*?\]);?\n", s, re.S).group(1))
    rows = []
    for r in pool:
        if r[5]:
            continue                                 # 已归属
        rows.append({"fn": r[0], "desc": r[1], "lang": r[2], "stars": r[3],
                     "topics": [],                   # 页面行无 topics → 无 topic 证据
                     "cat": r[7] or "其他", "ev": r[22] if len(r) > 22 else ""})
    rows.sort(key=lambda r: -r["stars"])
    return rows


def evidence_strings(verdict: dict) -> list[str]:
    """证据链 → 旧格式字符串（prescreen 依赖：『依赖 w ∈ 清单』可解析红旗、
    『路径 p』可拼 evidence 链接；同源去重，票降序）。镜像/矩阵证据是旧台账
    没有的形态——纯镜像立案的 draft 若无任何 依赖/路径 前缀串，prescreen 的
    _override_row 会因 paths/deps 双空越界，故兜底补一条纯「路径 {文件}」
    （证据本就在该文件，非伪造）。"""
    out, seen = [], set()
    src_of_nonpath = None
    for e in verdict["per_db"].values():
        for it in e["chain"]:
            key = (it["kind"], it["source"])
            if key in seen:
                continue
            seen.add(key)
            if it["kind"] != "topic" and src_of_nonpath is None:
                src_of_nonpath = it["source"]
            words = (it.get("detail") or {}).get("words") or []
            w = words[0] if words else it["db"]
            out.append({"dep": f"依赖 {w} ∈ {it['source']}",
                        "tree": f"路径 {it['source']}",
                        "image": f"镜像 {w} ∈ {it['source']}",
                        "ci": f"矩阵 {w} ∈ {it['source']}",
                        "topic": it["source"]}[it["kind"]])
    out = out[:6]
    if src_of_nonpath and not any(s.startswith(("依赖", "路径", "文件")) for s in out):
        out.append(f"路径 {src_of_nonpath}")        # 兜底放 cap 后，防被 [:6] 切掉
    return out


def _recheck_strength(verdict: dict) -> str:
    """below_quorum 的强度标签（沿用旧报告语义）：全 0.5=weak / 仅 topic=topic_only /
    其余（有 1 票级证据但凑不满 2 票）=dep_only。"""
    chains = [it for e in verdict["per_db"].values() for it in e["chain"]]
    if chains and all(it["kind"] == "topic" for it in chains):
        return "topic_only"
    if chains and all(it["votes"] <= 0.5 for it in chains):
        return "weak"
    return "dep_only"


def judge_one(row: dict, scan: dict, evidence: dict) -> dict:
    """单条判定：信号层（口径不变）→ 证据层 → 引擎判定层。"""
    fn = row["fn"]
    base = {"stars": row["stars"], "cat": row["cat"], "lang": row["lang"] or "无",
            "scanned": datetime.now().strftime("%Y-%m-%d")}

    # ② 信号层（零网络，口径与旧版逐字一致）
    if "范围外" in (row["ev"] or "") or OOS_RE.search(fn + " " + (row["desc"] or "")):
        return {**base, "dbs": [], "status": "oos"}
    if EDU_RE.search(fn + " " + (row["desc"] or "")):
        return {**base, "dbs": [], "status": "edu"}
    sc = scan.get(fn)
    cands = [d for d in ((sc.get("cands") if isinstance(sc, dict) else None) or {}) if d in DB17]
    verdicts = row.get("db_verdicts") or []
    if cands and not verdicts:
        return {**base, "dbs": [], "status": "desc_pending",
                "evidence": ["简介候选: " + ",".join(cands)]}
    if verdicts:                                     # 问过、判过非 support
        return {**base, "dbs": [], "status": "judged_no_support"}

    # ③ 证据层：分片对齐（无记录/partial → 补采队列；empty_repo/gone → 终局）
    rec = evidence.get(fn)
    if rec is None:
        return {**base, "dbs": [], "status": "pending_evidence",
                "evidence": ["证据分片无记录（进增量补采队列）"]}
    if rec.get("status") == "partial":
        return {**base, "dbs": [], "status": "pending_evidence",
                "evidence": ["证据 partial 树截断（待重采）"]}
    if rec.get("status") != "ok":
        return {**base, "dbs": [], "status": "no_evidence",
                "evidence": [f"证据状态: {rec.get('status')}"]}

    # ④ 判定层：matcher × quorum 引擎
    verdict = judge(build_pack(fn, rec, {"topics": row["topics"]}))
    branch = rec.get("default_branch") or "main"
    ev = evidence_strings(verdict)
    if verdict["status"] == "no_evidence":           # 空包（含 42/43 历史出池路径）
        return {**base, "dbs": [], "status": "no_evidence", "branch": branch}
    if verdict["status"] == "below_quorum":          # 单弱信号只记录 → recheck
        dbs = sorted(verdict["per_db"], key=DB_ORDER.index)
        return {**base, "dbs": dbs, "status": "recheck", "evidence": ev,
                "branch": branch, "strength": _recheck_strength(verdict)}
    chains = [it for e in verdict["per_db"].values() for it in e["chain"]]
    if all(it["kind"] == "topic" for it in chains):
        # 同通道叠票不放直通：postgres+postgresql 双 topic 同库叠满 2 票是
        # 自声明重复计数非双源互证（方案 §4.5 topic 不绕过证据体系）→ recheck
        dbs = sorted(verdict["per_db"], key=DB_ORDER.index)
        return {**base, "dbs": dbs, "status": "recheck", "evidence": ev,
                "branch": branch, "strength": "topic_only"}
    if row["cat"] not in TOOL_CATS:                  # case_opened 但非工具类 → 门后
        return {**base, "dbs": [], "dbs_raw": verdict["dbs"], "status": "gated_app_cat",
                "evidence": ev, "branch": branch}
    strong = any(it["votes"] >= 2.0 and it["kind"] in ("image", "tree") for it in chains)
    return {**base, "dbs": verdict["dbs"], "status": "draft", "evidence": ev,
            "branch": branch, "strength": "strong" if strong else "med",
            "votes": {db: e["votes"] for db, e in verdict["per_db"].items()}}


def signal_preview(rows: list[dict], scan: dict) -> dict:
    """--dry-run 信号层预演（不触证据分片，零网络出数）。"""
    sig = {"oos": 0, "edu": 0, "desc_pending": 0, "judged_no_support": 0, "需证据判定": 0}
    for r in rows:
        fn, desc, ev = r["fn"], r["desc"], r["ev"]
        if "范围外" in (ev or "") or OOS_RE.search(fn + " " + (desc or "")):
            sig["oos"] += 1
        elif EDU_RE.search(fn + " " + (desc or "")):
            sig["edu"] += 1
        else:
            sc = scan.get(fn)
            cands = [d for d in ((sc.get("cands") if isinstance(sc, dict) else None) or {}) if d in DB17]
            vd = r.get("db_verdicts") or []
            sig["desc_pending" if (cands and not vd)
                else ("judged_no_support" if vd else "需证据判定")] += 1
    return sig


def write_report(ledger: dict, skipped_n: int) -> None:
    st: dict[str, int] = {}
    for v in ledger.values():
        st[v.get("status", "?")] = st.get(v.get("status", "?"), 0) + 1
    lines = [
        "# unattr_judge 判定报告（v2 薄壳：attribution 引擎判定）",
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
                     f"（{v.get('strength')}，"
                     f"{','.join(f'{d}={w:g}' for d, w in (v.get('votes') or {}).items())}）"
                     f"｜{v['evidence'][0] if v['evidence'] else ''}")
    lines += ["", "## 待复核（recheck：单弱信号只记录——weak/topic_only/dep_only）", ""]
    for fn, v in sorted([(a, b) for a, b in ledger.items() if b.get("status") == "recheck"],
                        key=lambda x: -x[1]["stars"])[:40]:
        lines.append(f"- {v['stars']:>6}★ {fn} → {','.join(v['dbs'])}（{v.get('strength')}）"
                     f"｜{v['evidence'][0] if v['evidence'] else ''}")
    lines += ["", "## 范围外命中抽检（防词表误伤，人工瞄一眼 Top 20）", ""]
    for fn, v in sorted([(a, b) for a, b in ledger.items() if b.get("status") == "oos"],
                        key=lambda x: -x[1]["stars"])[:20]:
        lines.append(f"- {v['stars']:>6}★ {fn}")
    lines += ["", f"## 分层小结：desc_pending {st.get('desc_pending', 0)}"
              f" · judged_no_support {st.get('judged_no_support', 0)}"
              f" · no_evidence {st.get('no_evidence', 0)}"
              f" · pending_evidence {st.get('pending_evidence', 0)}（增量补采队列）"]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def atomic_write_compact(path: Path, obj) -> None:
    """台账原子写：tmp+replace + LF（compact——4k+ 条 indent 会翻三倍；
    轮转三副本对每轮全量重写的台账只添 .N 垃圾，不采用）。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8", newline="\n")
    tmp.replace(path)


_PAGE_POOL_DEFAULT = "D:/dbhub_page/data/pool.js"


def main() -> int:
    ap = argparse.ArgumentParser(description="未归类项目判定器 v2（T2e 薄壳，零网络）")
    ap.add_argument("--page-pool", default=_PAGE_POOL_DEFAULT,
                    help="页面池 pool.js 路径（本地优先；缺失自动切 collect 模式）")
    ap.add_argument("--mode", choices=["auto", "page", "collect"], default="auto",
                    help="auto=页面池在用 page 否则 collect；collect=池活文件推导（规范模式）")
    ap.add_argument("--limit", type=int, default=0,
                    help="本轮判定条数上限（0=全量；零网络跑一轮≈十秒级）")
    ap.add_argument("--min-stars", type=int, default=0,
                    help="只判 Star ≥ N 的项目（长尾分批消化）")
    ap.add_argument("--dry-run", action="store_true", help="信号层统计，不写盘")
    ap.add_argument("--report-only", action="store_true", help="不重判，仅重出报告")
    args = ap.parse_args()

    scan = json.loads(SCAN.read_text(encoding="utf-8"))
    interp = load_interp_projection()

    use_collect = args.mode == "collect" or (
        args.mode == "auto" and not Path(args.page_pool).is_file())
    if use_collect:
        rows = collect_rows(interp, scan)
        mode_note = "collect 模式（闸门=有行号引证才跳过；规则/AI 预归属仍进判定）"
    else:
        rows = page_rows(interp)
        mode_note = "page 模式（页面行无 topics → 无 topic 证据）"
    for r in rows:                                   # 判定要用的解读字段挂到行上
        ip = interp.get(r["fn"]) or {}
        r["db_verdicts"] = ip.get("db_verdicts") or []
        r["cat"] = ip.get("cat") or r.get("cat") or "其他"

    if args.min_stars > 0:
        before = len(rows)
        rows = [r for r in rows if r["stars"] >= args.min_stars]
        mode_note += f" · Star≥{args.min_stars} 过滤 {before}→{len(rows)}"

    todo = [r for r in rows if r["fn"] in interp]
    todo.sort(key=lambda r: -r["stars"])
    skipped_n = len(rows) - len(todo)
    print(f"[{mode_note}] 未归类 {len(rows)} · 已解读 {len(todo)} · 未解读(圈外) {skipped_n}", flush=True)

    print("信号层预演:", signal_preview(todo, scan), flush=True)
    if args.dry_run:
        return 0

    ledger = json.loads(OUT.read_text(encoding="utf-8")) if OUT.is_file() else {}
    if not args.report_only:
        batch = todo if args.limit <= 0 else todo[:args.limit]
        evidence = load_evidence_for({r["fn"] for r in batch})
        for r in batch:
            ledger[r["fn"]] = judge_one(r, scan, evidence)
        atomic_write_compact(OUT, ledger)
        fst: dict[str, int] = {}
        for r in batch:
            st = ledger[r["fn"]].get("status", "?")
            fst[st] = fst.get(st, 0) + 1
        st_all: dict[str, int] = {}
        for v in ledger.values():
            st_all[v.get("status", "?")] = st_all.get(v.get("status", "?"), 0) + 1
        print(f"本轮判定 {len(batch)} 条：{sorted(fst.items(), key=lambda x: -x[1])}", flush=True)
        print(f"台账累计 {len(ledger)} 条：{sorted(st_all.items(), key=lambda x: -x[1])}", flush=True)

    write_report(ledger, skipped_n)
    drafts = sum(1 for v in ledger.values() if v.get("status") == "draft")
    print(f"台账 {OUT}\n报告 {REPORT}", flush=True)
    print(f"==== 判定小结：draft {drafts} 条 · 详见报告 ====", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
