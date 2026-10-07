# -*- coding: utf-8 -*-
"""db_scan —— 库名候选提名器（「程序提名」层）。

全文（不截断）扫描 README 与池描述中的 17 库名/别名/驱动名，
输出每个库的【行号+行文本】候选 → state/db_scan.json。
interpret 的 AI 只对这些候选行做 support/compat/mention 逐项裁决并【指认行号】，
引句文本由程序按行号回填（转述在构造上不可能），dbs 由程序组装。

v3 行号口径（与 interpret.py 的 build_prompt_v3 严格一致，改一处必须同步另一处）：
  - 候选行号 = 清理文（rm_clean v2）非空行从 1 起的编号；
  - README 行号只来自 README 清理文；描述命中不带行号（line=null），
    供 desc 降级路径按 v2 引句子串校验使用。

设计要点：
- 证据定义上必含库名 → 全文扫描的召回在构造上封顶（不受 10k 显示窗口影响）
- GaussDB / openGauss 用全名匹配，避免互撞；"pg" 等短词带词边界
- 幂等可重跑（全量重扫约几十秒，无 API 成本）；词表更新后重跑本文件即可

用法：
  python interpret/db_scan.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for _d in (ROOT, ROOT / "lib", ROOT / "interpret"):
    if str(_d) not in sys.path:
        sys.path.insert(0, str(_d))
from gh import atomic_write_json   # noqa: E402
from rm_clean import clean_readme   # noqa: E402

OUT = ROOT / "state" / "db_scan.json"
READMES = ROOT / "data" / "readmes"

# 17 库词汇表：库名 → 匹配词（小写；ASCII 词带边界，中文直接匹配）
# 词边界 (?![a-z0-9]) 使短词匹配不了带后缀的常用写法——10-01 实测误降级：
# sqlite3 / sqlite2 / mysqli / psql 必须显式列出，否则全文提到也不提名。
DB_VOCAB = {
    "PostgreSQL":  ["postgresql", "postgres", "psql", "pg", "psycopg", "libpq", "pgvector"],
    "MySQL":       ["mysql", "mysqli", "pymysql", "mysqlclient", "go-sql-driver"],
    "Oracle":      ["oracle"],
    "SQLite":      ["sqlite", "sqlite2", "sqlite3"],
    "SQL Server":  ["sql server", "mssql", "sqlserver"],
    "ClickHouse":  ["clickhouse"],
    "MariaDB":     ["mariadb"],
    "TiDB":        ["tidb", "tikv"],
    "OceanBase":   ["oceanbase"],
    "PolarDB":     ["polardb", "polardbx"],
    "Dameng":      ["dameng", "dm8", "达梦"],
    "openGauss":   ["opengauss"],
    "GaussDB":     ["gaussdb"],
    "GBase":       ["gbase"],
    "TDSQL":       ["tdsql"],
    "YashanDB":    ["yashandb", "yashan", "崖山"],
    "GoldenDB":    ["goldendb"],
}
_COMPILED = {db: re.compile("|".join(
                 r"(?<![a-z0-9])" + re.escape(t) + r"(?![a-z0-9])" if t.isascii()
                 else re.escape(t)
                 for t in terms))
             for db, terms in DB_VOCAB.items()}

MAX_QUOTES_PER_DB = 5          # 前 3 条通常在文首；支持矩阵深处的行（窗口外漏判主因）靠后 2 条兜住
QUOTE_MAX = 260


def latest_pool() -> Path:
    """M2b：活文件优先（data/live/pool.ndjson），回退最新非空快照。"""
    import pool_store
    _recs, src = pool_store.load_latest("pool")
    return src


def number_lines(text: str) -> list[tuple[int, str]]:
    """非空行从 1 起编号（interpret.build_prompt_v3 同一实现，口径必须一致）。"""
    return [(i + 1, ln.rstrip()) for i, ln in enumerate(text.split("\n")) if ln.strip()]


def scan_lines(lines: list[tuple[int, str]]) -> dict:
    """返回 {db: [{"line": 行号, "q": 行文本}]}，每库最多 MAX_QUOTES_PER_DB 条。"""
    out = {}
    for db, pat in _COMPILED.items():
        quotes = []
        for no, ln in lines:
            if pat.search(ln.lower()):
                q = re.sub(r"\s+", " ", ln).strip()[:QUOTE_MAX]
                if q not in [x["q"] for x in quotes]:
                    quotes.append({"line": no, "q": q})
                if len(quotes) >= MAX_QUOTES_PER_DB:
                    break
        if quotes:
            out[db] = quotes
    return out


def scan_text(text: str) -> dict:
    """兼容入口：无行号扫描（desc 等短文本用）。返回 {db: [行文本]}。"""
    out = {}
    if not text:
        return out
    for db, pat in _COMPILED.items():
        quotes = []
        for ln in text.split("\n"):
            m = pat.search(ln.lower())
            if m:
                q = re.sub(r"\s+", " ", ln[max(0, m.start() - 120):
                                           m.end() + 160]).strip()[:QUOTE_MAX]
                if q not in quotes:
                    quotes.append(q)
                if len(quotes) >= MAX_QUOTES_PER_DB:
                    break
        if quotes:
            out[db] = quotes
    return out


def main():
    from pool_store import read_any
    pool = {it["full_name"]: it for it in read_any(latest_pool())}
    result, n_with_cand = {}, 0
    for fn, it in pool.items():
        readme_cands, desc_cands = {}, {}
        p = READMES / (fn.replace("/", "__") + ".md")
        if p.is_file():
            try:
                lines = number_lines(clean_readme(p.read_text(encoding="utf-8", errors="ignore")))
                readme_cands = scan_lines(lines)
            except OSError:
                pass
        desc = (it.get("description") or "").strip()
        if desc:
            for db, qs in scan_text(desc).items():
                if db not in readme_cands:                 # README 命中优先（带行号）
                    desc_cands[db] = [{"line": None, "q": q} for q in qs]
        cands = {**readme_cands, **desc_cands}
        if cands:
            n_with_cand += 1
        result[fn] = {"cands": cands}
    OUT.parent.mkdir(exist_ok=True)
    atomic_write_json(OUT, result)
    print(f"扫描 {len(result)} 项 · 含候选 {n_with_cand} · 输出 {OUT}")


if __name__ == "__main__":
    main()
