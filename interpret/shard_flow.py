# -*- coding: utf-8 -*-
"""主会话调度用：切分 pending_batch 为分片 / 合并 submit_shard_* 为 submit.json。

工作文件统一放 state/（不入库，gitignore 覆盖），不再散落仓库根目录。

用法：
  python shard_flow.py split 5    # 切 5 片 → state/shard_0.json ... shard_4.json
  python shard_flow.py merge      # 合并 state/submit_shard_*.json → state/../submit.json
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import sys as _sys, pathlib as _pl
ROOT = _pl.Path(__file__).resolve().parents[1]
for _d in (ROOT, ROOT / "lib", ROOT / "config"):
    _sys.path.insert(0, str(_d))
HERE = ROOT
BATCH = HERE / "state" / "pending_batch.json"
SUBMIT = HERE / "submit.json"


def split(n: int):
    items = json.loads(BATCH.read_text(encoding="utf-8"))
    size = (len(items) + n - 1) // n
    for i in range(n):
        chunk = items[i * size:(i + 1) * size]
        (HERE / "state" / f"shard_{i}.json").write_text(
            json.dumps(chunk, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"state/shard_{i}.json: {len(chunk)} 条")


def merge():
    merged = []
    for p in sorted((HERE / "state").glob("submit_shard_*.json")):
        merged += json.loads(p.read_text(encoding="utf-8"))
    SUBMIT.write_text(json.dumps(merged, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"合并 {len(merged)} 条 → submit.json")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="分片切分/合并")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sp = sub.add_parser("split"); sp.add_argument("n", type=int)
    sub.add_parser("merge")
    a = ap.parse_args()
    split(a.n) if a.cmd == "split" else merge()
