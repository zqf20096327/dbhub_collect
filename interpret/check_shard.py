# -*- coding: utf-8 -*-
"""子代理分片预检：与 agent_batch.submit 同一套校验（禁词/枚举/evidence 原文/info_gain）。

用法：python check_shard.py <N>   # 校验 submit_shard_N.json，0 拒收退出码 0
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import sys as _sys, pathlib as _pl
ROOT = _pl.Path(__file__).resolve().parents[1]
for _d in (ROOT, ROOT / "lib", ROOT / "config"):
    _sys.path.insert(0, str(_d))
HERE = ROOT                      # 历史引用兼容：统一指向项目根
import strategy                              # noqa: E402
from interpret import info_gain, validate    # noqa: E402


def main():
    n = sys.argv[1]
    shard_in = HERE / f"shard_{n}.json"
    shard_out = HERE / f"submit_shard_{n}.json"
    gen = strategy.derive()
    batch = {b["fn"]: b for b in json.loads(shard_in.read_text(encoding="utf-8"))}
    out = json.loads(shard_out.read_text(encoding="utf-8"))
    ok, rej = 0, []
    for b in out:
        meta = batch.get(b["fn"])
        if meta is None:
            rej.append({"fn": b.get("fn"), "why": ["分片外项目"]})
            continue
        if b.get("sha") != meta["sha"]:
            rej.append({"fn": b["fn"], "why": [f"sha 与分片不符: {b.get('sha')} != {meta['sha']}"]})
            continue
        p = HERE / "data" / "readmes" / (b["fn"].replace("/", "__") + ".md")
        full = p.read_text(encoding="utf-8", errors="ignore") if p.is_file() else meta.get("desc", "")
        obj, errs = validate(b.get("obj") or {}, gen, full, meta.get("desc", ""))
        if obj is None:
            rej.append({"fn": b["fn"], "why": errs[:4]})
            continue
        review = (obj["identity"].get("review") or "")
        if not info_gain(review, meta.get("desc", "")):
            rej.append({"fn": b["fn"], "why": ["review 相对 desc 无 ≥3 个新实义词（会被清空）"]})
            continue
        ok += 1
    print(f"分片 {n}: 通过 {ok} / 拒收 {len(rej)}（共 {len(batch)} 条待做，已写 {len(out)}）")
    for r in rej:
        print("  拒收:", r["fn"], r["why"])
    sys.exit(1 if rej or ok < len(batch) else 0)


if __name__ == "__main__":
    main()
