# -*- coding: utf-8 -*-
"""G5-2 重建 interp_state：只收在池 fn，sha 与 pool/readme_state 对账。

为什么重建：台账历史上滚了全量 fn（含出池 2,225），G7 删旧数据前要把它收敛成
「读链真正会用的人口」——在池 + readme_state 对得上的 fn。条目字段（status/
reused/source 等）原样保留，只动两样：
  ① 出池 fn 整条删除（G7-3 出池条目清理的一部分，先在这里收敛台账）
  ② sha 与 readme_state 当前 sha 对齐（README 变更后台账还停旧 sha 的，按当前值修）

no_readme + 空描述的 912 仓本就不在台账（v2 时代也没烧过，死信表管），不补。
desc 键 fn（G3 后）台账已是新键，对账只验证不重算。

用法：
  python tools/rebuild_interp_state.py --dry-run   # 只报差异（默认）
  python tools/rebuild_interp_state.py --apply     # 备份后重建
  python tools/rebuild_interp_state.py --verify    # 对账：0 差异才过
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "lib"))
sys.path.insert(0, str(ROOT / "interpret"))

import pool_store                            # noqa: E402
from gh import atomic_write_json             # noqa: E402

ISTATE = ROOT / "state" / "interp_state.json"
BACKUP = ROOT / "state" / "shadow" / "g5_interp_state_backup.json"


def _pool() -> dict[str, dict]:
    out: dict[str, dict] = {}
    for name in ("pool", "pool_intl", "pool_cn"):
        p = pool_store.live_path(name)
        if not p.is_file():
            continue
        for rec in pool_store.read_ndjson(p):
            if rec.get("full_name"):
                out[rec["full_name"]] = rec
    return out


def rebuild(items: dict, rs_items: dict, pool: dict[str, dict]):
    """返回 (新台账, 统计)。"""
    new_items: dict[str, dict] = {}
    stat = Counter()
    for fn, meta in items.items():
        if fn not in pool:
            stat["drop_out_of_pool"] += 1
            continue
        rec = rs_items.get(fn)
        if rec is None:
            stat["drop_not_in_readme_state"] += 1
            continue
        meta = dict(meta or {})
        if rec.get("status") in ("done", "oversized") and rec.get("sha") \
                and meta.get("sha") != rec["sha"]:
            stat["sha_fixed_to_readme"] += 1
            meta["sha"] = rec["sha"]
        new_items[fn] = meta
    return new_items, stat


def main() -> int:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--dry-run", action="store_true")
    g.add_argument("--apply", action="store_true")
    g.add_argument("--verify", action="store_true")
    a = ap.parse_args()

    doc = json.loads(ISTATE.read_text(encoding="utf-8"))
    items = doc.get("items") or {}
    rs_items = json.loads((ROOT / "state" / "readme_state.json").read_text(
        encoding="utf-8")).get("items") or {}
    pool = _pool()
    new_items, stat = rebuild(items, rs_items, pool)
    print(f"现台账 {len(items):,} → 重建后 {len(new_items):,}："
          + " / ".join(f"{k} {v:,}" for k, v in stat.most_common()))

    if a.apply:
        BACKUP.parent.mkdir(parents=True, exist_ok=True)
        BACKUP.write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")
        out = {"schema": 1, "rebuilt_at": datetime.now(timezone.utc).strftime(
                   "%Y-%m-%dT%H:%M:%SZ"),
               "rule": "在池 + readme_state 对账（G5-2）；备份 " + BACKUP.name,
               "items": new_items}
        atomic_write_json(ISTATE, out)
        print(f"已重建并落盘（备份 {BACKUP.relative_to(ROOT)}，{len(items):,} 条原件）")
        return 0

    if a.verify:
        # 对账 0 差异：① 全部在池 ② sha 与 readme_state/desc 推导一致
        # ③ pool∩readme∩有解读 == 台账人口（空描述 912 仓除外，死信管）
        bad_pool = bad_sha = 0
        for fn, meta in new_items.items():
            if fn not in pool:
                bad_pool += 1
                continue
            rec = rs_items.get(fn) or {}
            if rec.get("status") in ("done", "oversized") and rec.get("sha"):
                if meta.get("sha") != rec["sha"]:
                    bad_sha += 1
        # 反向：readme 可解读（done/oversized 有 sha，或 no_readme 有描述且台账有 fn）
        expect = set()
        for fn in pool:
            rec = rs_items.get(fn) or {}
            if rec.get("status") in ("done", "oversized") and rec.get("sha"):
                expect.add(fn)
            elif rec.get("status") == "no_readme" and fn in items:
                expect.add(fn)          # desc 类：台账有就收（键 G3 已对齐）
        got = set(new_items)
        print(f"对账：出池残留 {bad_pool} · sha 漂移 {bad_sha} ·"
              f" 应有 {len(expect):,} vs 实有 {len(got):,}"
              f"（差 {len(expect ^ got)}）")
        ok = bad_pool == 0 and bad_sha == 0 and expect == got
        print("验收（0 差异）→ " + ("PASS" if ok else "FAIL"))
        return 0 if ok else 1

    print("dry-run 结束（--apply 重建 / --verify 对账）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
