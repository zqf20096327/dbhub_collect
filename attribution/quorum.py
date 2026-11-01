# -*- coding: utf-8 -*-
"""quorum 投票立案（ATTRIBUTION T2c，方案 §3.2/§3.4）。

误配比漏配贵一个量级 → 精度优先于召回：
  票制（T2b 赋票）  镜像/官方驱动目录/连接器路径/文件名模式 2 票；普通依赖与
                    官方 org 1 票（org 全家桶误伤校准）；topic 自声明 2 票
                    （v0.3.0 用户裁定：明确标注须判出）；dev/弱路径/矩阵 0.5 票
  立案              合计 ≥2.0 票；单弱信号（0.5/1 档凑不满）不立案只记录
  单证 strong       恰 1 条证据凑满 2 票（镜像/官方目录/文件名/topic 自声明）
                    → 立案但打 single_strong 注记——须复核，不放直通；
                    纯 topic 立案在 unattr_judge 薄壳降 recheck（防标签抢注）
  复核              topic 有而指纹无的库 → recheck 列表（矛盾=互补，不二选一）
  E-CI              国产立案 → 兼容基座有任意证据则联动双标（rules_ci 规则 3）

入口：vote(verdict) 吃 api.judge 的聚合产物，返回补全 dbs/recheck/notes/status
的终局 verdict（纯函数，不改动入参）。
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from attribution.rules_ci import CN_DBS, compat_bases

QUORUM_THRESHOLD = 2.0


def vote(verdict: dict) -> dict:
    """聚合 verdict → 终局 verdict（dbs 立案名单 + 复核清单 + 注记）。"""
    per_db = verdict.get("per_db") or {}
    notes = list(verdict.get("notes") or [])

    dbs: list[str] = []
    for db, e in sorted(per_db.items(), key=lambda kv: (-kv[1]["votes"], kv[0])):
        if e["votes"] < QUORUM_THRESHOLD:
            continue                            # 单弱信号不立案只记录
        dbs.append(db)
        if len(e["chain"]) == 1:
            notes.append(f"single_strong: {db} 仅 1 条 {e['votes']:g} 票证据"
                         f"（{e['chain'][0]['kind']} 单证——镜像/官方目录/文件名/"
                         f"topic 自声明均须复核，不放直通）")

    # E-CI 规则 3：国产立案 → 兼容基座有任意证据 → 联动双标
    for db in list(dbs):
        if db not in CN_DBS:
            continue
        for base in compat_bases(db):
            if base in per_db and base not in dbs:
                dbs.append(base)
                notes.append(f"ci_linkage: {db} 立案 → 兼容基座 {base} 联动双标"
                             f"（§3.4 双信号双标）")

    out = dict(verdict)
    out["dbs"] = dbs
    out["recheck"] = list((verdict.get("meta") or {}).get("topic_complement") or [])
    out["notes"] = notes
    out["status"] = ("case_opened" if dbs
                     else "below_quorum" if per_db else "no_evidence")
    return out
