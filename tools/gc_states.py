# -*- coding: utf-8 -*-
"""state 残渣 GC：连续 N 个快照池都不再出现的仓，从 readme/enrich 状态清除。

背景（方案评审漏洞五）：新项目窗口 45 天未毕业（仍不满足星线）的仓会出池，
但 readme_state / enrich_state / enrich_cache 按 fn 键控的条目会永久残留；
国产无星线后窗口仓虽减少，池口径调整（如星线变化）仍会产生残渣，逐年累积。

规则：fn ∉ 最近 --keep 个 pool.json 的并集 → 从三个 state 文件删除。
data/readmes/ 正文文件保留不删（分类语料，磁盘便宜）。
默认 dry-run（只统计不落盘）；--apply 才写入（原子写 + 轮转）。

用法：
  python tools/gc_states.py                # 看会清多少
  python tools/gc_states.py --apply
  python tools/gc_states.py --keep 5 --apply
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import sys as _sys, pathlib as _pl  # noqa: E401
ROOT = _pl.Path(__file__).resolve().parents[1]
for _d in (ROOT, ROOT / "lib"):
    _sys.path.insert(0, str(_d))

from gh import atomic_write_json  # noqa: E402

STATE = ROOT / "state"
TARGETS = ("readme_state.json", "enrich_state.json", "enrich_cache.json")


def alive_fns(keep: int) -> set[str]:
    """M2b：当前活文件（最新全量池）∪ 最近旧快照 pool.json 并集判活。

    15 天后旧快照归档完只剩活文件——退化为当前池判活；防漏兜底是每晚
    全量重扫（设计意图），此处弱化可接受。"""
    from pool_store import load_latest, read_any
    alive: set[str] = set()
    try:
        items, _src = load_latest("pool")
        alive |= {it["full_name"] for it in items}
    except FileNotFoundError:
        pass
    pools = sorted((ROOT / "data").glob("snapshot_*/pool.json"))
    for p in pools[-keep:]:
        try:
            alive |= {it["full_name"] for it in read_any(p)}
        except (json.JSONDecodeError, KeyError):
            continue
    return alive


def gc(readme_items: dict, alive: set[str]) -> tuple[dict, list[str]]:
    dead = [fn for fn in readme_items if fn not in alive]
    for fn in dead:
        readme_items.pop(fn)
    return readme_items, dead


def main() -> None:
    ap = argparse.ArgumentParser(description="state 残渣 GC（默认 dry-run）")
    ap.add_argument("--keep", type=int, default=3,
                    help="用最近 N 个 pool.json 判定存活（默认 3）")
    ap.add_argument("--apply", action="store_true", help="落盘（默认只统计）")
    args = ap.parse_args()

    alive = alive_fns(args.keep)
    if not alive:
        sys.exit("没有可用 pool.json（先跑采集）")
    print(f"存活口径：最近 {args.keep} 个池的并集，共 {len(alive)} 仓")

    for name in TARGETS:
        p = STATE / name
        if not p.is_file():
            print(f"[{name}] 不存在，跳过")
            continue
        data = json.loads(p.read_text(encoding="utf-8"))
        if name in ("readme_state.json", "enrich_state.json"):   # {"version","items"} 包装
            items = data.setdefault("items", {})
            items, dead = gc(items, alive)
        else:                                                     # enrich_cache 扁平 fn→sig
            items, dead = gc(data, alive)
        print(f"[{name}] 残渣 {len(dead)} / 保留 {len(items)}"
              + (f"，样例 {dead[:5]}" if dead else ""))
        if args.apply and dead:
            atomic_write_json(p, data)
    print("完成（--apply 已落盘）" if args.apply else "（dry-run：未写盘，加 --apply 执行）")


if __name__ == "__main__":
    main()
