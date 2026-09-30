# -*- coding: utf-8 -*-
"""db_scan —— 库名候选提名器（「程序提名」层）。

全文（不截断）扫描 README 与池描述中的 17 库名/别名/驱动名，
输出每个库的上下文引句 → state/db_scan.json。
interpret 的 AI 只对这些候选做 support/compat/mention 逐项裁决，
dbs 由程序从裁决组装（详见 interpret.py 的 db_verdicts）。

设计要点：
- 证据定义上必含库名 → 全文扫描的召回在构造上封顶（不受 10k 截断影响）
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
for _d in (ROOT, ROOT / "lib"):
    if str(_d) not in sys.path:
        sys.path.insert(0, str(_d))
from gh import atomic_write_json   # noqa: E402

OUT = ROOT / "state" / "db_scan.json"
READMES = ROOT / "data" / "readmes"

# 17 库词汇表：库名 → 匹配词（小写；ASCII 词带边界，中文直接匹配）
DB_VOCAB = {
    "PostgreSQL":  ["postgresql", "postgres", "pg", "psycopg", "libpq", "pgvector"],
    "MySQL":       ["mysql", "pymysql", "mysqlclient", "go-sql-driver"],
    "Oracle":      ["oracle"],
    "SQLite":      ["sqlite"],
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

MAX_QUOTES_PER_DB = 3
QUOTE_CTX_BEFORE, QUOTE_CTX_AFTER = 120, 160
QUOTE_MAX = 260


def latest_pool() -> Path:
    base = ROOT / "data"
    cands = []
    for d in base.iterdir():
        if d.is_dir() and re.fullmatch(r"snapshot_\d{8}", d.name):
            pj = d / "pool.json"
            if pj.is_file() and pj.stat().st_size > 1000:
                cands.append(pj)
    if not cands:
        raise SystemExit("no non-empty snapshot pool.json found")
    return max(cands)


def scan_text(text: str) -> dict:
    """返回 {db: [上下文引句]}，每库最多 MAX_QUOTES_PER_DB 条。"""
    out = {}
    if not text:
        return out
    low = text.lower()
    for db, pat in _COMPILED.items():
        quotes = []
        for m in pat.finditer(low):
            s = max(0, m.start() - QUOTE_CTX_BEFORE)
            e = min(len(text), m.end() + QUOTE_CTX_AFTER)
            q = re.sub(r"\s+", " ", text[s:e]).strip()[:QUOTE_MAX]
            if q not in quotes:
                quotes.append(q)
            if len(quotes) >= MAX_QUOTES_PER_DB:
                break
        if quotes:
            out[db] = quotes
    return out


def main():
    pool = {it["full_name"]: it for it in json.loads(latest_pool().read_text(encoding="utf-8"))}
    result, n_with_cand = {}, 0
    for fn, it in pool.items():
        parts = [it.get("description") or ""]
        p = READMES / (fn.replace("/", "__") + ".md")
        if p.is_file():
            try:
                parts.append(p.read_text(encoding="utf-8", errors="ignore"))
            except OSError:
                pass
        cands = scan_text("\n".join(parts))
        if cands:
            n_with_cand += 1
        result[fn] = {"cands": cands}
    OUT.parent.mkdir(exist_ok=True)
    atomic_write_json(OUT, result)
    print(f"扫描 {len(result)} 项 · 含候选 {n_with_cand} · 输出 {OUT}")


if __name__ == "__main__":
    main()
