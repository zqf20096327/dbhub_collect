# -*- coding: utf-8 -*-
"""依赖名 → 库 匹配（ATTRIBUTION T1b：精确词档位机制）。

纯函数、零网络零存储。词表从 config/db_profiles 派生（T1a 字段），
本层只管匹配语义：

  - drivers_exact：包名 == 精确词（lower 归一）才命中——防 pg-electron 撞 pg
  - drivers     ：包名含子串安全词即命中——psycopg2-binary ⊃ psycopg
  - @types/ 前缀整体排除（TypeScript 类型声明非驱动本体）
  - dev=True 透传降档标志（devDeps 命中是弱信号，票制归 T2c）

铁律（词表侧保证）：只收驱动/连接器性质依赖；
sqlalchemy/typeorm 等通用库与 ORM 不在词表，永不命中。
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config.db_profiles import PROFILES

_EXCLUDE_PREFIX = ("@types/",)


def load_vocab() -> dict:
    """db_profiles → {substring: {词: 库}, exact: {词: 库}}（lower 归一）。"""
    sub: dict[str, str] = {}
    exact: dict[str, str] = {}
    for p in PROFILES:
        if not p.get("enabled", True):
            continue
        for w in p.get("drivers") or []:
            sub[w.lower()] = p["name"]
        for w in p.get("drivers_exact") or []:
            exact[w.lower()] = p["name"]
    return {"substring": sub, "exact": exact}


_VOCAB = load_vocab()


def match_dep(name: str, *, dev: bool = False) -> list[dict]:
    """依赖名 → 命中列表 [{db, word, mode, dev}]；空列表 = 不命中。

    name 支持 npm/pypi/go require/maven groupId:artifactId 等任意字符串形态；
    多词命中同一库会返回多条（不同命中词=不同证据，去重归调用方）。
    子串吸收（11-01 真实流量实测）：词 A ⊂ 词 B（A≠B）时 A 的命中是 B 的
    影子——如 SQL Server 的 sqlclient ⊂ MySQL 驱动名 mysqlclient，双判即误判。
    互不包含的词（mysql-to-mssql 桥接类）双命中合法保留。
    """
    n = (name or "").strip().lower()
    if not n or n.startswith(_EXCLUDE_PREFIX):
        return []
    hits: list[dict] = []
    if n in _VOCAB["exact"]:
        hits.append({"db": _VOCAB["exact"][n], "word": n, "mode": "exact", "dev": dev})
    for w, db in _VOCAB["substring"].items():
        if w in n:
            hits.append({"db": db, "word": w, "mode": "substring", "dev": dev})
    words = {h["word"] for h in hits}
    return [h for h in hits
            if not any(h["word"] != w and h["word"] in w for w in words)]
