# -*- coding: utf-8 -*-
"""三套词表归一派生层（ATTRIBUTION T1c，2026-11-01）。

单一事实源 = config/db_profiles（T1a 字段）；本文件只做派生 + 语境补充表。
消灭的三处硬编码漂移及其去向：

  原 db_scan.DB_VOCAB      → readme_vocab()   README 全文提名词（词边界正则用）
  原 unattr_judge E1       → dir_vocab()      路径/文件名 token（T2e 重写版消费）
  原 unattr_judge E3       → dep_match.load_vocab()（T1b 已落，deps 语境）

语境补充表原则：只收"档案纯词覆盖不到"的词（来源=原硬编码差集，逐词可
追溯）；加新库 = 写一份档案，补充表零增长。diff 验收基线见
fixtures/vocab_baseline.json（selftest_vocab 断言零漂移/白名单新增）。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config.db_profiles import PROFILES

# README 提名词补充（db_scan 语境）：库名/纯词别名覆盖不到的显式提名词。
# 词边界正则 (?<![a-z0-9])..(?![a-z0-9]) 下短词必须显式列出（10-01 误降级教训）。
README_TERMS_EXTRA = {
    "PostgreSQL": ["psql", "pg", "psycopg", "libpq", "pgvector"],
    "MySQL": ["mysqli", "pymysql", "mysqlclient", "go-sql-driver"],
    "SQLite": ["sqlite2", "sqlite3"],
    "PolarDB": ["polardbx"],
    "YashanDB": ["yashan", "崖山"],
}

# 路径/文件名 token 补充（E1 语境）：目录名里的连接器写法变体。
DIR_TOKENS_EXTRA = {
    "PostgreSQL": ["pgsql", "psycopg"],
    "SQL Server": ["sql_server", "mssqlserver"],
    "PolarDB": ["polardbx"],
    "YashanDB": ["yashan"],
}

# 正则元字符出现即视为正则型 alias（如 r"sql\s*server"、r"dm[- ]database"），
# 不进纯词派生（词边界/语境由各消费方自带）。
_RE_META = re.compile(r"[\\()\[\]{}*+?|^$]")


def _plain_aliases(p: dict) -> list[str]:
    return [a.lower() for a in (p.get("aliases") or []) if not _RE_META.search(a)]


def _derive(extra: dict[str, list[str]]) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for p in PROFILES:
        if not p.get("enabled", True):
            continue
        words = [p["name"].lower()] + _plain_aliases(p) + (extra.get(p["name"]) or [])
        seen, uniq = set(), []
        for w in words:                      # 保序去重
            if w not in seen:
                seen.add(w)
                uniq.append(w)
        out[p["name"]] = uniq
    return out


def readme_vocab() -> dict[str, list[str]]:
    """README 全文提名词（db_scan 兼容视图；与原 DB_VOCAB 零 diff）。"""
    return _derive(README_TERMS_EXTRA)


def dir_vocab() -> dict[str, list[str]]:
    """路径/文件名 token（E1 兼容视图；T2e 重写 unattr_judge 时消费）。"""
    return _derive(DIR_TOKENS_EXTRA)
