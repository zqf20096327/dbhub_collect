# -*- coding: utf-8 -*-
"""六型证据统一 schema（ATTRIBUTION T2a，2026-11-01）。

适配引擎的输入契约：判定层（api.judge）只认本 schema 的证据条目；
采集侧原始形态（evidence 分片的 files[].names/dev/images、clues.paths、
pool topics）由 T2b matcher 翻译成本格式——翻译规则不进本层。

六型（ATTRIBUTION_PLAN 附录速查，勿增删）：
  dep        依赖清单（pom/requirements/go.mod…；dev 依赖 0.5 票降档）
  tree       文件树路径（connector/driver 目录、官方驱动目录）
  image      docker 镜像（compose 服务镜像 / Dockerfile FROM）
  ci         测试矩阵（workflow matrix、tox、build 阵列）
  rel_notes  发行说明——T5b 前无数据源，schema 留空位是设计意图，勿因无源砍型
  topic      作者自声明（pool.json topics；泛词不算由 T2b 三规则过滤）

证据条目五字段（缺一即非法，多余字段即错拼）：
  kind         六型之一
  db           17 库档案名之一（config/db_profiles 单一事实源）
  votes        票档 {0.5, 1.0, 2.0}——赋票是 T2b matcher 的职责（档位语义见
               api.DEFAULT_VOTES，弱路径可降 0.5，sqlc 先例），本层只校验档位合法
  source       出处，人可读定位：文件路径 / "topic:postgresql" / 镜像名带文件
  collected_at 采集时间，ISO-8601（日期或时间戳，来自证据分片/池快照的采集侧字段）

可选字段：
  detail       dict 透传（匹配词/命中方式/dev 降档原因等，T2b 填写、judge 原样带出）

证据包（evidence_pack）：
  {"fn": "owner/repo", "evidences": [条目…], "meta": {star/eco 等调用方自由携带}}
  fn/evidences/meta 缺失一律按空处理（空包 → 全空结论，验收要求不炸）；
  出现但类型/取值非法 → normalize_pack 抛 ValueError（契约违规宁炸勿吞）。
"""
from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config.db_profiles import PROFILES

EVIDENCE_KINDS = ("dep", "tree", "image", "ci", "rel_notes", "topic")

KIND_LABELS = {
    "dep": "依赖清单",
    "tree": "文件树路径",
    "image": "docker 镜像",
    "ci": "测试矩阵",
    "rel_notes": "发行说明",
    "topic": "作者自声明",
}

# 方案 §3.2 票档参考（镜像/官方驱动目录/连接器路径 2 票；普通依赖与 topic 1 票；
# tests/端口/服务名 0.5 票）。rel_notes 故意无默认票：无数据源即不定档，T5b 再补。
DEFAULT_VOTES = {"image": 2.0, "tree": 2.0, "dep": 1.0, "topic": 1.0, "ci": 0.5}

VOTE_TIERS = (0.5, 1.0, 2.0)

REQUIRED_ITEM_FIELDS = ("kind", "db", "votes", "source", "collected_at")
ITEM_OPTIONAL_FIELDS = ("detail",)

DB_NAMES = frozenset(p["name"] for p in PROFILES if p.get("enabled", True))


def _iso_ok(s: str) -> bool:
    try:
        datetime.fromisoformat(s.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False


def validate_item(item) -> list[str]:
    """单条证据 → 错误清单（空 = 合法）。不抛异常，批量校验用。"""
    if not isinstance(item, dict):
        return [f"证据条目非 dict：{type(item).__name__}"]
    errs: list[str] = []
    for f in REQUIRED_ITEM_FIELDS:
        if f not in item:
            errs.append(f"缺字段 {f}")
    if unknown := (set(item) - set(REQUIRED_ITEM_FIELDS) - set(ITEM_OPTIONAL_FIELDS)):
        errs.append(f"未知字段 {sorted(unknown)}（防错拼）")
    if "kind" in item and item["kind"] not in EVIDENCE_KINDS:
        errs.append(f"kind '{item['kind']}' 不在六型 {list(EVIDENCE_KINDS)}")
    if "db" in item and item["db"] not in DB_NAMES:
        errs.append(f"db '{item['db']}' 不在 17 库档案名")
    if "votes" in item:
        v = item["votes"]
        if isinstance(v, bool) or not isinstance(v, (int, float)) or float(v) not in VOTE_TIERS:
            errs.append(f"votes {v!r} 不在票档 {list(VOTE_TIERS)}")
    if "source" in item and (not isinstance(item["source"], str) or not item["source"].strip()):
        errs.append("source 空（出处必填，人可读定位）")
    if "collected_at" in item and (
        not isinstance(item["collected_at"], str)
        or not item["collected_at"].strip()
        or not _iso_ok(item["collected_at"].strip())
    ):
        errs.append(f"collected_at {item['collected_at']!r} 非 ISO-8601")
    if "detail" in item and not isinstance(item["detail"], dict):
        errs.append(f"detail {type(item['detail']).__name__} 非 dict")
    return errs


def validate_pack(pack) -> list[str]:
    """证据包 → 错误清单（空 = 合法；None/缺 fn/evidences 按空包合法）。"""
    if pack is None:
        return []
    if not isinstance(pack, dict):
        return [f"证据包非 dict：{type(pack).__name__}"]
    errs: list[str] = []
    if unknown := (set(pack) - {"fn", "evidences", "meta"}):
        errs.append(f"包级未知字段 {sorted(unknown)}（防错拼）")
    if "fn" in pack and (not isinstance(pack["fn"], str) or not pack["fn"].strip()):
        errs.append("fn 非非空字符串")
    if "evidences" in pack:
        ev = pack["evidences"]
        if not isinstance(ev, list):
            errs.append(f"evidences {type(ev).__name__} 非 list")
        else:
            for i, it in enumerate(ev):
                errs.extend(f"[{i}] {e}" for e in validate_item(it))
    if "meta" in pack and not isinstance(pack["meta"], dict):
        errs.append(f"meta {type(pack['meta']).__name__} 非 dict")
    return errs


def normalize_pack(pack) -> dict:
    """校验 + 归一：字段序规范、votes 转 float、字符串去首尾空白。

    返回 {"fn","evidences","meta"}（三项必有）；非法即 ValueError（信息含全部错误）。
    """
    errs = validate_pack(pack)
    if errs:
        raise ValueError("证据包不合法：\n  " + "\n  ".join(errs))
    pack = pack or {}
    items = []
    for it in pack.get("evidences") or []:
        norm = {
            "kind": it["kind"],
            "db": it["db"],
            "votes": float(it["votes"]),
            "source": it["source"].strip(),
            "collected_at": it["collected_at"].strip(),
        }
        if "detail" in it:
            norm["detail"] = it["detail"]
        items.append(norm)
    return {
        "fn": (pack.get("fn") or "").strip(),
        "evidences": items,
        "meta": pack.get("meta") or {},
    }
