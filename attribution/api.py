# -*- coding: utf-8 -*-
"""适配引擎判定入口（ATTRIBUTION T2a，2026-11-01）。

纯函数 judge(evidence_pack) → verdict：不碰网络、不碰存储、同输入同输出
（无时钟无随机——可 diff 验收）。分层接线：
  T2a（本卡）  schema 校验 + 按库聚合票数与证据链（机械层）
  T2b          matcher：采集侧指纹 → 证据包（本入口的输入生产者）
  T2c          quorum ≥2 票立案 + E-CI 消歧，在本入口内接线——接线前 dbs 恒空，
               骨架不抢政策（不达标不硬推，见台账 T2c 卡）

verdict 字段（证据卡片骨架，方案 §3.2「每仓一张证据卡片」）：
  fn / meta    证据包原样透传
  engine       引擎版本（结论可追溯到代码版本）
  status       no_evidence（空包/全空——验收要求不炸）
               pending_quorum（有票，待 T2c 立案裁决）
  dbs          立案库名单——quorum 接线前恒为 []
  per_db       {db: {"votes": 合计票, "kinds": {型: 条数},
                     "chain": [该库全部证据条目，票降序+型序，人读证据链]}}
  notes        判定层备注（E-CI 消歧/互补标记等，T2c 起写入）
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from attribution.evidence_model import EVIDENCE_KINDS, normalize_pack

ENGINE_VERSION = "0.1.0"   # T2a 骨架；T2b/T2c 接线时递增次版本

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

    return {
        "fn": fn,
        "meta": meta,
        "engine": ENGINE_VERSION,
        "status": "pending_quorum" if per_db else "no_evidence",
        "dbs": [],   # quorum（T2c）接线前恒空——聚合是机械，立案是政策
        "per_db": dict(sorted(per_db.items(), key=lambda kv: (-kv[1]["votes"], kv[0]))),
        "notes": [],
    }
