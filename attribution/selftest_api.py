# -*- coding: utf-8 -*-
"""T2a 离线自检：六型 schema 契约 + judge 纯函数行为。零网络。

跑法：python attribution/selftest_api.py（退出码 0=全绿）
覆盖：空包四变体不炸、五字段/票档/库名/ISO 时间校验、rel_notes 占位不砍、
rich 样本票数聚合+证据链排序、同输入同输出（确定性）。
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from attribution.api import ENGINE_VERSION, judge
from attribution.evidence_model import (
    DB_NAMES, DEFAULT_VOTES, EVIDENCE_KINDS, normalize_pack,
)

FIX = json.loads((ROOT / "attribution" / "fixtures" / "evidence_packs.json")
                 .read_text(encoding="utf-8"))


def _expect_raise(label: str, pack, fails: list) -> None:
    try:
        normalize_pack(pack)
    except ValueError:
        return
    fails.append(f"[FAIL] {label}：未抛 ValueError")


def main() -> int:
    fails: list[str] = []

    # 1) 空包四变体 → 全空结论（不炸）：status/dbs/per_db 全空，fn 与引擎版本带出
    for v in FIX["empty_variants"]:
        try:
            got = judge(v)
        except Exception as e:                                   # noqa: BLE001
            fails.append(f"[FAIL] 空包 {v!r} 炸了：{e}")
            continue
        if (got["status"], got["dbs"], got["per_db"]) != ("no_evidence", [], {}):
            fails.append(f"[FAIL] 空包 {v!r} 结论非全空：{got['status']}/{got['dbs']}/{got['per_db']}")
        if got["engine"] != ENGINE_VERSION:
            fails.append(f"[FAIL] 空包未带引擎版本：{got['engine']}")
    if judge({"fn": "a/b", "evidences": []})["fn"] != "a/b":
        fails.append("[FAIL] 空包 fn 未透传")

    # 2) schema 反例：逐条必须 ValueError（契约违规宁炸勿吞）
    base = {"kind": "dep", "db": "MySQL", "votes": 1.0,
            "source": "pom.xml", "collected_at": "2026-10-30T15:10:33Z"}
    _expect_raise("缺字段 votes", {"fn": "a/b", "evidences": [
        {k: v for k, v in base.items() if k != "votes"}]}, fails)
    _expect_raise("字段错拼 vote", {"fn": "a/b", "evidences": [
        {**base, "vote": 1.0}]}, fails)
    _expect_raise("kind 非六型", {"fn": "a/b", "evidences": [
        {**base, "kind": "readme"}]}, fails)
    _expect_raise("db 非 17 库", {"fn": "a/b", "evidences": [
        {**base, "db": "MongoDB"}]}, fails)
    for bad in (0.7, 3.0, 0, True, "1.0", None):
        _expect_raise(f"votes 非法 {bad!r}", {"fn": "a/b", "evidences": [
            {**base, "votes": bad}]}, fails)
    _expect_raise("source 空串", {"fn": "a/b", "evidences": [
        {**base, "source": "  "}]}, fails)
    _expect_raise("collected_at 非 ISO", {"fn": "a/b", "evidences": [
        {**base, "collected_at": "yesterday"}]}, fails)
    _expect_raise("detail 非 dict", {"fn": "a/b", "evidences": [
        {**base, "detail": "psycopg"}]}, fails)
    _expect_raise("包级字段错拼 repo", {"fn": "a/b", "repo": "c/d", "evidences": []}, fails)
    _expect_raise("包非 dict", ["a/b"], fails)
    _expect_raise("evidences 非 list", {"fn": "a/b", "evidences": base}, fails)
    _expect_raise("条目非 dict", {"fn": "a/b", "evidences": ["pg"]}, fails)

    # 3) rel_notes 占位不砍：在六型枚举内；恰是无默认票的唯一型（无源即不定档）
    if "rel_notes" not in EVIDENCE_KINDS:
        fails.append("[FAIL] rel_notes 被砍出六型——T5b 前留空位是设计意图")
    if set(EVIDENCE_KINDS) - set(DEFAULT_VOTES) != {"rel_notes"}:
        fails.append(f"[FAIL] 无默认票的型应恰为 {{rel_notes}}：{set(EVIDENCE_KINDS) - set(DEFAULT_VOTES)}")

    # 4) rich 样本：聚合票数精确 + T2c 接线后立案（OceanBase 5 票 + MySQL 联动双标）
    got = judge(FIX["rich"])
    if got["status"] != "case_opened":
        fails.append(f"[FAIL] rich status 应 case_opened：{got['status']}")
    if got["dbs"] != ["OceanBase", "MySQL"]:
        fails.append(f"[FAIL] rich 应立案 OceanBase(5.0 票)+MySQL(E-CI 联动)：{got['dbs']}")
    if not any("ci_linkage" in n and "MySQL" in n for n in got["notes"]):
        fails.append(f"[FAIL] MySQL 应带 ci_linkage 联动注记：{got['notes']}")
    votes = {db: e["votes"] for db, e in got["per_db"].items()}
    if votes != {"OceanBase": 5.0, "MySQL": 1.0, "SQLite": 0.5}:
        fails.append(f"[FAIL] rich 票数错：{votes}")
    if list(got["per_db"]) != ["OceanBase", "MySQL", "SQLite"]:
        fails.append(f"[FAIL] per_db 未按票降序：{list(got['per_db'])}")
    ob = got["per_db"]["OceanBase"]
    if [it["kind"] for it in ob["chain"]] != ["tree", "image", "topic"]:
        fails.append(f"[FAIL] OceanBase 证据链未按票降序+型序：{ob['chain']}")
    if ob["kinds"] != {"tree": 1, "image": 1, "topic": 1}:
        fails.append(f"[FAIL] kinds 计数错：{ob['kinds']}")
    if got["fn"] != FIX["rich"]["fn"] or got["meta"] != FIX["rich"]["meta"]:
        fails.append("[FAIL] fn/meta 未透传")
    if got["per_db"]["MySQL"]["chain"][0]["detail"].get("word") != "mysql:mysql-connector-java":
        fails.append("[FAIL] detail 未透传")

    # 5) 纯函数确定性：同包两次判定 deep 相等（可 diff 验收的前提）
    if judge(copy.deepcopy(FIX["rich"])) != got:
        fails.append("[FAIL] 同输入不同输出——judge 非确定")

    # 6) 对账：六型=6、17 库档案名全覆盖票档校验域
    if len(EVIDENCE_KINDS) != 6 or len(DB_NAMES) != 17:
        fails.append(f"[FAIL] 六型/17 库口径漂移：{len(EVIDENCE_KINDS)} 型/{len(DB_NAMES)} 库")

    verdict = "PASS" if not fails else "FAIL"
    print(f"[{verdict}] 空包 4 变体不炸 + schema 反例 17 条 + rel_notes 占位"
          f" + rich 聚合 5.0/1.0/0.5 立案双标 + 确定性 + 6 型×{len(DB_NAMES)} 库对账")
    for f in fails:
        print(f)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
