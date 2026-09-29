# -*- coding: utf-8 -*-
"""GLM-5.3 会话内解读批处理（agent-as-interpreter）。

用法（三步一循环）：
  python agent_batch.py --next 30          # ① 选 30 条待解读（star 降序），导出给我读
  （我在会话里读取 pending_batch.json，亲自写解读，存为 submit.json）
  python agent_batch.py --submit submit.json   # ② 同一套校验（禁词/枚举/evidence原文）入库

缓存与 API 路径完全共用（interp_cache.json，sha 键控）：我做的和以后 API 做的
无缝衔接、互不重复；每个项目一条文本，下次直接用，SHA 变了才增量。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import sys as _sys, pathlib as _pl
ROOT = _pl.Path(__file__).resolve().parents[1]
for _d in (ROOT, ROOT / "lib", ROOT / "config"):
    _sys.path.insert(0, str(_d))
HERE = ROOT                      # 历史引用兼容：统一指向项目根
import strategy                              # noqa: E402
from gh import atomic_write_json             # noqa: E402
from interpret import (CACHE, ISTATE, REVIEW, info_gain, validate)  # noqa: E402

BATCH = HERE / "state" / "pending_batch.json"


def next_batch(n: int):
    rstate = json.loads((HERE / "state" / "readme_state.json").read_text(encoding="utf-8"))
    cache = json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.is_file() else {}
    pool = {it["full_name"]: it
            for it in json.loads((HERE / "data" / "snapshot_20260925" / "pool.json").read_text(encoding="utf-8"))}
    todo = [(fn, rec["sha"]) for fn, rec in rstate.get("items", {}).items()
            if rec.get("status") in ("done", "oversized") and rec.get("sha")
            and rec["sha"] not in cache]
    todo.sort(key=lambda x: -((pool.get(x[0]) or {}).get("stars") or 0))
    todo = todo[:n]
    out = []
    for fn, sha in todo:
        p = HERE / "data" / "readmes" / (fn.replace("/", "__") + ".md")
        readme = p.read_text(encoding="utf-8", errors="ignore")[:2500] if p.is_file() else ""
        it = pool.get(fn) or {}
        out.append({"fn": fn, "sha": sha, "stars": it.get("stars"),
                    "desc": (it.get("description") or "")[:300],
                    "topics": (it.get("topics") or [])[:12], "readme": readme})
    atomic_write_json(BATCH, out)
    print(f"导出 {len(out)} 条 → {BATCH}（缓存已有 {len(cache)}）")


def submit(path: str):
    gen = strategy.derive()
    cache = json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.is_file() else {}
    st = json.loads(ISTATE.read_text(encoding="utf-8")) if ISTATE.is_file() else {"items": {}}
    batch = {b["fn"]: b for b in json.loads(Path(path).read_text(encoding="utf-8"))}
    ok, rej = 0, []
    # 与 interpret.py 相同的校验：readme 全文做 evidence 原文核对；sha 须与批次一致防缓存键错位
    for fn, b in batch.items():
        p = HERE / "data" / "readmes" / (fn.replace("/", "__") + ".md")
        full = p.read_text(encoding="utf-8", errors="ignore") if p.is_file() else b.get("desc", "")
        if not b.get("sha"):
            rej.append({"fn": fn, "why": ["sha 缺失"]})
            st["items"][fn] = {"sha": None, "status": "rejected", "violations": ["sha 缺失"]}
            continue
        obj, errs = validate(b.get("obj") or {}, gen, full, b.get("desc", ""))
        review = ((b.get("obj") or {}).get("identity") or {}).get("review") or ""
        if obj and not info_gain(review, b.get("desc", "")):
            obj["identity"]["review"] = ""
        if obj is None:
            rej.append({"fn": fn, "why": errs[:3]})
            st["items"][fn] = {"sha": b.get("sha"), "status": "rejected", "violations": errs[:5]}
            continue
        obj.update({"fn": fn, "sha": b["sha"], "source": "glm-5.3-session",
                    "generated_at": "2026-09-26"})
        cache[b["sha"]] = obj
        st["items"][fn] = {"sha": b["sha"], "status": "done"}
        ok += 1
    atomic_write_json(CACHE, cache)
    atomic_write_json(ISTATE, st)
    atomic_write_json(REVIEW, {"rejected": rej})
    print(f"入库 {ok} / 拒收 {len(rej)}（缓存总 {len(cache)}）")
    for r in rej:
        print("  拒收:", r["fn"], r["why"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--next", type=int)
    ap.add_argument("--submit")
    args = ap.parse_args()
    if args.next:
        next_batch(args.next)
    if args.submit:
        submit(args.submit)


if __name__ == "__main__":
    main()
