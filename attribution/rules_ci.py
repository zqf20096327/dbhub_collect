# -*- coding: utf-8 -*-
"""E-CI 兼容协议消歧规则（ATTRIBUTION T2c，方案 §3.4）。

国产库走 MySQL/PG 兼容协议——依赖清单里只有 mysql-connector/psycopg，
区分不了连的是开源版还是国产版。三规则：
  1 国产专属信号优先：国产库的票只能来自国产专属词（词表结构保证——
    pytidb/pyobclient/dmPython/官方镜像名不与任何国际库共词），有证据就立得住；
  2 纯国际依赖不猜国产：只有 mysql-connector/psycopg 证据 → 只可能立案国际库，
    仓名/联想永不推断 TiDB/OceanBase（SSE-DZH/OceanBase 实测活案例）；
  3 双信号双标：国产库立案 + 兼容基座库有任何证据 → 基座联动双标
    （与现有 622 个双适配仓口径一致；TiDB→MySQL 补归属 45 条的机制化）。

兼容基座映射只收公开协议无争议的；GBase/TDSQL/GoldenDB 协议归属信息弱，
宁缺勿滥不联动（联动是加分项不是必须项），待实测案例支撑再扩。
"""
from __future__ import annotations

CN_DBS = frozenset({
    "TiDB", "OceanBase", "PolarDB", "Dameng", "openGauss",
    "GaussDB", "GBase", "TDSQL", "YashanDB", "GoldenDB",
})

# 国产库 → 兼容基座（PolarDB 双形态 MySQL/PG 两系）
CN_COMPAT_BASE = {
    "TiDB": ("MySQL",),
    "OceanBase": ("MySQL",),
    "openGauss": ("PostgreSQL",),
    "GaussDB": ("PostgreSQL",),
    "PolarDB": ("MySQL", "PostgreSQL"),
    "Dameng": ("Oracle",),
    "YashanDB": ("Oracle",),
    # GBase/TDSQL/GoldenDB：暂不联动（无公开协议实锤，宁缺勿滥）
}


def is_cn(db: str) -> bool:
    return db in CN_DBS


def compat_bases(db: str) -> tuple[str, ...]:
    """国产库的兼容基座库；国际库/未映射国产库 → ()。"""
    return CN_COMPAT_BASE.get(db, ())
