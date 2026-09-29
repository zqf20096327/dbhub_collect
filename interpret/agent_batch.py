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
from datetime import datetime, timezone
from pathlib import Path

import sys as _sys, pathlib as _pl
ROOT = _pl.Path(__file__).resolve().parents[1]
for _d in (ROOT, ROOT / "lib", ROOT / "config", ROOT / "interpret"):
    _sys.path.insert(0, str(_d))
HERE = ROOT                      # 历史引用兼容：统一指向项目根
import strategy                              # noqa: E402
from gh import atomic_write_json             # noqa: E402
from interpret import (CACHE, ISTATE, REVIEW, info_gain,  # noqa: E402
                       latest_pool, merge_review, validate)

BATCH = HERE / "state" / "pending_batch.json"


def next_batch(n: int, pool_path: Path | None):
    rstate_p = HERE / "state" / "readme_state.json"
    if not rstate_p.is_file() or not (pool_path or (HERE / "data")).is_dir():
        sys.exit("readme_state.json 或 pool 不存在（先跑采集）")
    rstate = json.loads(rstate_p.read_text(encoding="utf-8"))
    cache = json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.is_file() else {}
    pool = {it["full_name"]: it
            for it in json.loads(pool_path.read_text(encoding="utf-8"))}
    todo = [(fn, rec["sha"]) for fn, rec in rstate.get("items", {}).items()
            if rec.get("status") in ("done", "oversized") and rec.get("sha")
            and rec["sha"] not in cache and fn in pool]
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
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
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
            st["items"][fn] = {"sha": b["sha"], "status": "rejected", "violations": errs[:5]}
            continue
        obj.update({"fn": fn, "sha": b["sha"], "source": "glm-5.3-session",
                    "generated_at": today})
        cache[b["sha"]] = obj
        st["items"][fn] = {"sha": b["sha"], "status": "done"}
        ok += 1
    atomic_write_json(CACHE, cache)
    atomic_write_json(ISTATE, st)
    prev_review = json.loads(REVIEW.read_text(encoding="utf-8")) if REVIEW.is_file() else {}
    failed_fns = [fn for fn, r in st["items"].items()
                  if r.get("status") in ("failed", "rejected")]
    atomic_write_json(REVIEW, merge_review(prev_review, [], rej, failed_fns))
    print(f"入库 {ok} / 拒收 {len(rej)}（缓存总 {len(cache)}）")
    for r in rej:
        print("  拒收:", r["fn"], r["why"])


def main():
    ap = argparse.ArgumentParser(description="会话内解读批处理")
    ap.add_argument("--next", type=int, help="导出 N 条待解读")
    ap.add_argument("--submit", help="提交 submit.json 入库")
    ap.add_argument("--pool", default=None, help="池路径（默认取最新 snapshot_20*/pool.json）")
    args = ap.parse_args()
    if not args.next and not args.submit:
        ap.error("--next 与 --submit 至少其一")
    pool_path = Path(args.pool) if args.pool else latest_pool()
    if args.next:
        next_batch(args.next, pool_path)
    if args.submit:
        submit(args.submit)


if __name__ == "__main__":
    main()
