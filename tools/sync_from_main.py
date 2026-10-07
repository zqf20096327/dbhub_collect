# -*- coding: utf-8 -*-
"""从主项目（dbhub_v2）同步 interpret（解读）层到本仓库。

方向约定（2026-09-29 定）：
  采集层（collect/enrich/config/lib）以【本仓库】为唯一开发主线——
  主项目里是过时副本，绝不反向同步（会回滚修复，09-29 实发过一次事故）。
  本工具只搬 interpret 层代码与其进度 state；分类/渲染仍在主项目。

同步内容：
  代码：interpret/*.py
  状态：state/{interp_cache,interp_state,manual_review}.json（--code-only 可跳过）
  数据：--with-snapshots 时同步历史快照 pool.json + meta/（一般不用）

用法：
  python tools/sync_from_main.py                     # 默认源 ../dbhub_v2
  python tools/sync_from_main.py --src D:/dbhub_v2
  python tools/sync_from_main.py --code-only         # 只搬代码不覆盖 interpret 进度
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

# 只同步 interpret 层——采集层文件绝不允许出现在此清单（见文件头方向约定）
CODE_FILES = [
    "interpret/interpret.py", "interpret/agent_batch.py",
    "interpret/shard_flow.py", "interpret/check_shard.py",
]
STATE_FILES = [
    "interp_cache.json", "interp_state.json", "manual_review.json",
]


def sync_code(src: Path) -> int:
    n = 0
    for rel in CODE_FILES:
        s, d = src / rel, ROOT / rel
        if not s.is_file():
            print(f"跳过（源不存在）: {rel}")
            continue
        d.parent.mkdir(parents=True, exist_ok=True)
        if not d.is_file() or s.read_bytes() != d.read_bytes():
            shutil.copy2(s, d)
            print(f"同步: {rel}")
            n += 1
    return n


def sync_state(src: Path) -> int:
    n = 0
    sdir = src / "state" / "interp_cache_shards"
    if sdir.is_dir():                      # 分片缓存整目录搬运（10-06 起；以源为准覆盖）
        ddir = ROOT / "state" / "interp_cache_shards"
        shutil.rmtree(ddir, ignore_errors=True)
        shutil.copytree(sdir, ddir)
        n += 1
    for name in STATE_FILES:
        s, d = src / "state" / name, ROOT / "state" / name
        if s.is_file():
            ROOT.joinpath("state").mkdir(exist_ok=True)
            shutil.copy2(s, d)
            n += 1
    print(f"interpret state: {n} 个")
    return n


def sync_snapshots(src: Path) -> int:
    n = 0
    for snap in sorted((src / "data").glob("snapshot_*")):
        if not snap.is_dir():
            continue
        pool, meta = snap / "pool.json", snap / "meta"
        old = snap / "merged" / "all_projects.json"
        dst = ROOT / "data" / snap.name
        if pool.is_file() and pool.stat().st_size > 0:
            (dst).mkdir(parents=True, exist_ok=True)
            shutil.copy2(pool, dst / "pool.json")
            if meta.is_dir():
                shutil.copytree(meta, dst / "meta", dirs_exist_ok=True)
            n += 1
        elif old.is_file() and old.stat().st_size > 0:
            (dst / "merged").mkdir(parents=True, exist_ok=True)
            shutil.copy2(old, dst / "merged" / "all_projects.json")
            n += 1
    print(f"快照日: {n} 个（仅 pool.json + meta，不含 parts/readmes）")
    return n


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=str(ROOT.parent / "dbhub_v2"),
                    help="主项目路径（默认 ../dbhub_v2）")
    ap.add_argument("--with-snapshots", action="store_true",
                    help="同时同步历史快照数据（一般不用）")
    ap.add_argument("--code-only", action="store_true",
                    help="只搬 interpret 代码，不覆盖其进度 state")
    args = ap.parse_args()
    src = Path(args.src)
    if not src.is_dir():
        sys.exit(f"源目录不存在: {src}")
    n = sync_code(src)
    if not args.code_only:
        sync_state(src)
    if args.with_snapshots:
        sync_snapshots(src)
    print(f"完成：interpret 代码 {'无变化' if n == 0 else f'{n} 个文件更新'}。"
          f"记得 git commit + push。")


if __name__ == "__main__":
    main()
