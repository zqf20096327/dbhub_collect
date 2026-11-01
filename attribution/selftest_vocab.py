# -*- coding: utf-8 -*-
"""T1c 离线自检：三套词表派生 vs 改动前基线 diff 断言。零网络。

跑法：python attribution/selftest_vocab.py（退出码 0=全绿）

判定规则（卡验收"diff 仅含白名单新增，逐条可追溯"）：
  - readme_vocab vs 原 db_scan.DB_VOCAB      → 零 diff（词表搬家不改行为）
  - dir_vocab    vs 原 unattr E1 DIR_ALIAS   → 仅白名单新增
  - dep_vocab    vs 原 unattr E3 DEP_ALIAS   → 仅 T1a 新增词白名单
出现任何删除/白名单外新增即 FAIL——词表一变全线漂（T1c 防坑）。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from attribution.vocab import dir_vocab, readme_vocab  # noqa: E402
from attribution.dep_match import load_vocab as dep_vocab_raw  # noqa: E402

# dir_vocab 允许的新增（派生自带的有益修复，逐条理由）
DIR_ALLOWED_NEW = {
    ("Dameng", "达梦"),          # alias 纯词自动带入（中文目录存在）
    ("SQL Server", "sql server"),  # 库名小写自动带入（路径语境无害）
    ("YashanDB", "yashandb"),    # 修 E1 缺陷：原 token 只有 yashan 打不中 yashandb
}

# dep_vocab 允许的新增 = T1a 新增词（lower 归一）
DEP_ALLOWED_NEW = {
    ("SQL Server", "mssql"),
    ("ClickHouse", "clickhouse"),
    ("TiDB", "tidb-lite"),
    ("OceanBase", "obclient"),
    ("Dameng", "dmjdbcdriver"),
    ("Dameng", "dmprovider"),
    ("PolarDB", "polardb"),
    ("GaussDB", "gaussdb"),
    ("GaussDB", "huaweicloud-gaussdb"),
    ("YashanDB", "yashandb"),
    ("GoldenDB", "goldendb"),
    ("PostgreSQL", "tokio-postgres"),   # 11-01 用户过目补入（rust 驱动，pivotlake 案例）
    ("PostgreSQL", "postgres"),
}


def _diff(base: dict, derived: dict, allowed: frozenset = frozenset()) -> tuple[set, set, set]:
    """返回 (删除词对, 白名单外新增, 新增词对全集)。"""
    removed, added = set(), set()
    for db in set(base) | set(derived):
        b = {w.lower() for w in base.get(db, [])}
        d = {w.lower() for w in derived.get(db, [])}
        removed |= {(db, w) for w in b - d}
        added |= {(db, w) for w in d - b}
    return removed, added - allowed, added


def main() -> int:
    fails = 0
    base = json.loads((ROOT / "attribution" / "fixtures" / "vocab_baseline.json")
                      .read_text(encoding="utf-8"))

    # 1) readme_vocab：零 diff（db_scan 行为不变的最强保证）
    removed, illegal, _ = _diff(base["db_scan_DB_VOCAB"], readme_vocab())
    if removed or illegal:
        print(f"[FAIL] readme_vocab 非零 diff：删除 {sorted(removed)} "
              f"白名单外新增 {sorted(illegal)}")
        fails += 1
    else:
        print("[PASS] readme_vocab vs 原 DB_VOCAB：零 diff（词表纯搬家）")

    # 2) dir_vocab：仅白名单新增
    removed, illegal, added = _diff(base["unattr_DIR_ALIAS"], dir_vocab(),
                                    frozenset(DIR_ALLOWED_NEW))
    if removed or illegal:
        print(f"[FAIL] dir_vocab：删除 {sorted(removed)} "
              f"白名单外新增 {sorted(illegal)}")
        fails += 1
    else:
        print(f"[PASS] dir_vocab vs 原 DIR_ALIAS：新增 {len(added)} 条全在白名单"
              f"（{sorted(added)}）零删除")

    # 3) dep_vocab：仅 T1a 新增词
    dep = {}
    for w, db in dep_vocab_raw()["substring"].items():
        dep.setdefault(db, []).append(w)
    removed, illegal, added = _diff(base["unattr_DEP_ALIAS"], dep,
                                    frozenset(DEP_ALLOWED_NEW))
    if removed or illegal:
        print(f"[FAIL] dep_vocab：删除 {sorted(removed)} "
              f"白名单外新增 {sorted(illegal)}")
        fails += 1
    else:
        print(f"[PASS] dep_vocab vs 原 DEP_ALIAS：新增 {len(added)} 条全为 T1a 新增词"
              "零删除")

    # 4) 17 库全覆盖
    from config.db_profiles import PROFILES
    names = {p["name"] for p in PROFILES if p.get("enabled", True)}
    for fn, voc in (("readme_vocab", readme_vocab), ("dir_vocab", dir_vocab)):
        if names - set(voc()):
            print(f"[FAIL] {fn} 库缺失：{names - set(voc())}")
            fails += 1
    if not fails:
        print("[PASS] 17 库三视图全覆盖")

    print(f"[{'PASS' if not fails else 'FAIL'}] T1c 词表派生 diff 自检")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
