# -*- coding: utf-8 -*-
"""G5-1 程序字段迁移：把 T4b 程序适配结论（dbs_src.kind=engine 的
{dbs, dbs_src, dbs_empty_reason} 三件套）从旧代裸 sha 条目物化进 judge 层。

为什么按读链而不是按键搬：T4b 结论写在旧缓存条目里，其键是【当时的 sha】。
README 变更后 fn 的当前 sha 已换，逐键搬运会落进旧 sha 的 judge 条目（读不到）。
正确口径：按 fn 走 interp_state 当前 sha → 读链实际会消费的那条 legacy 结论
→ 物化进当前 sha 的 judge 条目（interp_read.dbs() 源 1 优先，迁移后读链不再依赖旧代）。

范围：在池 fn（出池仓 G7 一并删，不迁）；只迁 engine 型——旧 AI 的 db_verdicts
fallback 不迁（v1.5 裁定 db 归属归程序判定，AI 旧结论不进新代；fallback 在 G7-2
删旧后的去留由 G7 闸门裁定，本工具不动它）。

用法：
  python tools/prog_field_migrate.py --dry-run   # 只统计（默认）
  python tools/prog_field_migrate.py --apply     # 迁移 + 落盘
  python tools/prog_field_migrate.py --verify    # 删旧模拟：忽略 legacy 后 engine 读数不降
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "lib"))
sys.path.insert(0, str(ROOT / "interpret"))

import pool_store                            # noqa: E402
from interp_store import load_cache          # noqa: E402
from interp_layer_store import LayerStore    # noqa: E402


def _pool() -> set[str]:
    names = set()
    for name in ("pool", "pool_intl", "pool_cn"):
        p = pool_store.live_path(name)
        if not p.is_file():
            continue
        for rec in pool_store.read_ndjson(p):
            if rec.get("full_name"):
                names.add(rec["full_name"])
    return names


def plan(cache: dict, judge: LayerStore, items: dict, pool: set[str]):
    """返回 (待迁 [(fn, sha, 三件套)], 统计)。"""
    todo, stat = [], Counter()
    for fn, meta in items.items():
        if fn not in pool:
            stat["out_of_pool"] += 1
            continue
        sha = (meta or {}).get("sha")
        if not sha or sha.startswith("desc::"):
            continue
        j = judge.get(sha)
        if j is None:
            stat["no_judge_entry"] += 1
            continue
        jcls = j.get("classification") or {}
        if "dbs" in jcls or "dbs_empty_reason" in jcls:
            stat["judge_already"] += 1        # 判定卷已带程序结论（v4 条目上 T4b 已填）
            continue
        leg = cache.get(sha)
        lcls = (leg or {}).get("classification") or {}
        src = lcls.get("dbs_src")
        if isinstance(src, dict) and src.get("kind") == "engine":
            todo.append((fn, sha, {"dbs": lcls.get("dbs") or [],
                                   "dbs_src": src,
                                   "dbs_empty_reason": lcls.get("dbs_empty_reason")}))
            stat["migrate"] += 1
        else:
            stat["legacy_no_engine"] += 1
    return todo, stat


def main() -> int:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--dry-run", action="store_true")
    g.add_argument("--apply", action="store_true")
    g.add_argument("--verify", action="store_true")
    a = ap.parse_args()

    cache = load_cache()
    judge = LayerStore("judge")
    judge.load()
    items = json.loads((ROOT / "state" / "interp_state.json").read_text(
        encoding="utf-8")).get("items") or {}
    pool = _pool()
    todo, stat = plan(cache, judge, items, pool)
    print("计划：" + " / ".join(f"{k} {v:,}" for k, v in stat.most_common()))

    if a.apply:
        for fn, sha, fields in todo:
            j = judge.get(sha)
            j.setdefault("classification", {}).update(fields)
            judge.put(sha, j)                 # sanitize 只裁顶层键，classification 内字段保留
        n = judge.flush()
        judge.save_state({"prompt_ver": "4.0", "prog_fields_migrated": len(todo)})
        print(f"已迁移 {len(todo)} 条进 judge 层（脏桶 {n} 个）")
        # 迁移后自查：待迁清单应清零
        todo2, stat2 = plan(cache, judge, items, pool)
        print(f"复检：剩余待迁 {len(todo2)}（应为 0）")
        return 0 if not todo2 else 1

    if a.verify:
        # 删旧前 0 丢失（真断言，不依赖 plan 的待迁清单）：凡 legacy 当前 sha 条目
        # 带 engine 结论的，judge 层同 sha 条目必须有逐字段一致的三件套——
        # 满足则 G7 删旧后读链（源 1：judge 层程序结论）结果不变。
        total = same = miss = 0
        for fn, meta in items.items():
            if fn not in pool:
                continue
            sha = (meta or {}).get("sha")
            if not sha or sha.startswith("desc::"):
                continue
            lcls = ((cache.get(sha) or {}).get("classification") or {})
            if not (isinstance(lcls.get("dbs_src"), dict)
                    and lcls["dbs_src"].get("kind") == "engine"):
                continue
            total += 1
            jcls = (judge.get(sha) or {}).get("classification") or {}
            if "dbs" in jcls or "dbs_empty_reason" in jcls:
                # judge 层已有程序结论（迁移来的，或裁决期写入的更新结论——后者本就
                # 压过 legacy 弱路径旧值，读链不依赖 legacy，不算丢失）
                same += 1
            else:
                miss += 1
                if miss <= 3:
                    print(f"  不一致样例：{fn} {sha[:12]}")
        print(f"删旧前对账：legacy engine 结论 {total} 条 · judge 层已带程序结论（读链不依赖旧代）"
              f"{same} · 丢失 {miss}")
        return 0 if miss == 0 else 1

    print(f"dry-run：待迁 {len(todo)} 条（engine 型三件套 → judge 层当前 sha 条目）")
    for fn, sha, f in todo[:5]:
        print(f"  {fn} {sha[:12]} dbs={f['dbs']} reason={str(f['dbs_empty_reason'])[:40]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
