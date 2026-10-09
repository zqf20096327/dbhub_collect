# -*- coding: utf-8 -*-
"""多源采集结果回收：键控并集合并 state 缓存文件。

用途：服务器 / 多台机器分头采集后，把各自的成果合并回本地，不覆盖、不丢任何一边。
支持输入：tar.gz 包（内部含 state/*.json）或散装 json 文件，多个输入依次合并。

合并规则（文件即接口，见 ARCHITECTURE.md）：
  enrich_cache.json  主键 fn   → 冲突取 enriched_at 较新
  enrich_state.json  主键 fn   → dims 各维度时间戳取新；fail_count 取小；
                                  status 优先级 gone > failed > 其他
  interp_cache.json  主键 sha  → 纯并集（同 sha 同内容，无真冲突）

用法：
  python lib/merge_states.py results.tgz interp.tgz          # 合并两个包
  python lib/merge_states.py server_cache.json --as enrich_cache
  python lib/merge_states.py results.tgz --dry-run           # 只看会怎么合
"""
from __future__ import annotations

import argparse
import json
import sys
import tarfile
import tempfile
from pathlib import Path

import sys as _sys, pathlib as _pl  # noqa: E401
ROOT = _pl.Path(__file__).resolve().parents[1]
for _d in (ROOT, ROOT / "lib"):
    _sys.path.insert(0, str(_d))

from gh import atomic_write_json  # noqa: E402
import interp_store  # noqa: E402  interp_cache 分片存储（10-06 起）
import enrich_store  # noqa: E402  enrich_cache 分片存储（10-09 起）

STATE = ROOT / "state"
TARGETS = ("enrich_cache.json", "enrich_state.json", "interp_cache.json")


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def collect_inputs(args) -> dict[str, list[dict]]:
    """把所有输入展开成 {目标文件名: [外来 dict, ...]}。"""
    gathered: dict[str, list[tuple[str, dict]]] = {t: [] for t in TARGETS}
    for src in args.inputs:
        p = Path(src)
        if not p.is_file():
            sys.exit(f"输入不存在：{p}")
        if p.suffix == ".gz" or p.name.endswith(".tgz"):
            with tempfile.TemporaryDirectory() as td:
                with tarfile.open(p) as tf:
                    members = [m for m in tf.getmembers()
                               if Path(m.name).name in TARGETS and m.isfile()]
                    tf.extractall(td, members=members)
                    for m in members:
                        name = Path(m.name).name
                        gathered[name].append((f"{p}!{m.name}",
                                               load_json(Path(td) / m.name)))
        else:
            key = args.as_ or next((t for t in TARGETS if t.startswith(p.stem)), None)
            if not key:
                sys.exit(f"无法识别 {p} 属于哪个 state 文件，用 --as 指定")
            gathered[key].append((str(p), load_json(p)))
    return gathered


def newer_date(a, b):
    return max(a or "", b or "")


def merge_enrich_cache(local: dict, foreigns: list) -> dict:
    added = updated = 0
    for _, fcache in foreigns:
        for fn, sig in fcache.items():
            cur = local.get(fn)
            if cur is None:
                local[fn] = sig
                added += 1
            elif (sig.get("enriched_at") or "") > (cur.get("enriched_at") or ""):
                local[fn] = sig
                updated += 1
    print(f"  enrich_cache: 新增 {added} · 更新 {updated} · 合计 {len(local)}")
    return local


def merge_enrich_state(local: dict, foreigns: list) -> dict:
    added = merged = 0
    items = local.setdefault("items", {})
    prio = {"gone": 3, "failed": 2}
    for _, fstate in foreigns:
        for fn, rec in (fstate.get("items") or {}).items():
            cur = items.get(fn)
            if cur is None:
                items[fn] = rec
                added += 1
                continue
            merged += 1
            dims = cur.setdefault("dims", {})
            for d, ts in (rec.get("dims") or {}).items():
                dims[d] = newer_date(dims.get(d), ts)
            cur["fail_count"] = min(cur.get("fail_count", 0), rec.get("fail_count", 0))
            s_cur = prio.get(cur.get("status") or "", 1)
            s_new = prio.get(rec.get("status") or "", 1)
            if s_new > s_cur:
                cur["status"] = rec["status"]
                cur["last_error"] = rec.get("last_error", "")
            elif not cur.get("last_error"):
                cur["last_error"] = rec.get("last_error", "")
            cur["pushed_checked"] = newer_date(cur.get("pushed_checked"),
                                               rec.get("pushed_checked"))
    print(f"  enrich_state: 新增 {added} · 就地合并 {merged} · 合计 {len(items)}")
    return local


def merge_interp_cache(local: dict, foreigns: list) -> dict:
    added = 0
    for _, fcache in foreigns:
        for sha, obj in fcache.items():
            if sha not in local:
                local[sha] = obj
                added += 1
    print(f"  interp_cache: 新增 {added} · 合计 {len(local)}")
    return local


MERGERS = {
    "enrich_cache.json": merge_enrich_cache,
    "enrich_state.json": merge_enrich_state,
    "interp_cache.json": merge_interp_cache,
}


def main():
    ap = argparse.ArgumentParser(description="state 缓存并集合并（多机回收）")
    ap.add_argument("inputs", nargs="+", help="tar.gz 包或散装 json 文件")
    ap.add_argument("--as", dest="as_", choices=TARGETS,
                    help="散装 json 显式指定目标文件")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    gathered = collect_inputs(args)
    for name, foreigns in gathered.items():
        if not foreigns:
            continue
        path = STATE / name
        if name == "interp_cache.json":      # 分片存储：读并集（∪旧单文件）、写全桶
            local = interp_store.load_cache()
        elif name == "enrich_cache.json":    # 分片存储：同上（10-09 起）
            local = enrich_store.load_cache()
        else:
            local = load_json(path)
        print(f"[{name}] 来源 {len(foreigns)} 个：")
        MERGERS[name](local, foreigns)
        if not args.dry_run:
            if name == "interp_cache.json":
                interp_store.save_cache_all(local)
            elif name == "enrich_cache.json":
                enrich_store.save_cache_all(local)
            else:
                atomic_write_json(path, local)   # 原子写 + 自动轮转备份
    if args.dry_run:
        print("（dry-run：未写盘）")
    else:
        print("完成。建议接着跑：python classify/classify.py && cd render && python gen_demo.py")


if __name__ == "__main__":
    main()
