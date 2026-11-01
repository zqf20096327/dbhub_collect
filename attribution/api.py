# -*- coding: utf-8 -*-
"""适配引擎判定入口（ATTRIBUTION T2a 骨架 → T2c 接线，2026-11-01）。

纯函数 judge(evidence_pack) → verdict：不碰网络、不碰存储、同输入同输出
（无时钟无随机——可 diff 验收）。分层接线：
  T2a  schema 校验 + 按库聚合票数与证据链（机械层）
  T2b  matcher：采集侧指纹 → 证据包（本入口的输入生产者）
  T2c  quorum.vote 在本入口末段接线：≥2 票立案 + E-CI 消歧 → dbs 终局

verdict 字段（证据卡片，方案 §3.2「每仓一张证据卡片」）：
  fn / meta    证据包原样透传
  engine       引擎版本（结论可追溯到代码版本）
  status       no_evidence（空包/全空——验收要求不炸）
               below_quorum（有票无一立案——单弱信号只记录）
               case_opened（立案， dbs 非空；复核/签发归 T3/T4 人与 AI）
  dbs          立案库名单（票降序；国产立案的兼容基座联动双标殿后）
  per_db       {db: {"votes": 合计票, "kinds": {型: 条数},
                     "chain": [该库全部证据条目，票降序+型序，人读证据链]}}
  recheck      topic 有而指纹无的库（矛盾=互补，进人工复核）
  notes        single_strong（2 票单证须复核）/ ci_linkage（双标联动）等注记
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from attribution import quorum
from attribution.evidence_model import EVIDENCE_KINDS, normalize_pack

ENGINE_VERSION = "0.2.0"   # 0.1.0=T2a 骨架；0.2.0=T2c quorum+E-CI 接线

_KIND_ORDER = {k: i for i, k in enumerate(EVIDENCE_KINDS)}


def _chain_order(it: dict):
    """证据链排序键：票降序 → 型序 → 出处 → 采集时间（全量可比，输出确定）。"""
    return (-it["votes"], _KIND_ORDER[it["kind"]], it["source"], it["collected_at"])


def judge(pack) -> dict:
    """evidence_pack → verdict（契约见模块 docstring；非法包 ValueError 宁炸勿吞）。"""
    p = normalize_pack(pack)
    fn, items, meta = p["fn"], p["evidences"], p["meta"]

    per_db: dict[str, dict] = {}
    for it in items:
        e = per_db.setdefault(it["db"], {"votes": 0.0, "kinds": {}, "chain": []})
        e["votes"] += it["votes"]
        e["kinds"][it["kind"]] = e["kinds"].get(it["kind"], 0) + 1
        e["chain"].append(it)
    for e in per_db.values():
        e["chain"].sort(key=_chain_order)

    return quorum.vote({
        "fn": fn,
        "meta": meta,
        "engine": ENGINE_VERSION,
        "dbs": [],
        "per_db": dict(sorted(per_db.items(), key=lambda kv: (-kv[1]["votes"], kv[0]))),
        "notes": [],
    })
