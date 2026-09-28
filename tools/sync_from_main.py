# -*- coding: utf-8 -*-
"""从主项目（dbhub_v2）同步采集层代码到本仓库，防两份漂移。

同步内容：
  代码：collect/ enrich/ config/{db_profiles,strategy}.py lib/{gh,merge_states}.py
  状态：state/ 下 6 个采集断点文件（不含轮转备份）
  数据：--with-snapshots 时同步各快照日的 pool.json + meta/（不含 parts/ 与 readmes/）

用法：
  python tools/sync_from_main.py                     # 默认源 ../dbhub_v2
  python tools/sync_from_main.py --src D:/dbhub_v2
  python tools/sync_from_main.py --with-snapshots
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

CODE_FILES = [
    "collect/collect_pool.py", "collect/readme_sweep.py",
    "enrich/enrich.py",
    "config/db_profiles.py", "config/strategy.py",
    "lib/gh.py", "lib/merge_states.py",
]
STATE_FILES = [
    "collect_state.json", "readme_state.json", "readme_summary.json",
    "enrich_state.json", "enrich_cache.json", "enrich_summary.json",
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
    for name in STATE_FILES:
        s, d = src / "state" / name, ROOT / "state" / name
        if s.is_file():
            ROOT.joinpath("state").mkdir(exist_ok=True)
            shutil.copy2(s, d)
            n += 1
    print(f"状态文件: {n} 个")
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
                    help="同时同步快照数据（pool.json + meta）")
    args = ap.parse_args()
    src = Path(args.src)
    if not src.is_dir():
        sys.exit(f"源目录不存在: {src}")
    n = sync_code(src)
    sync_state(src)
    if args.with_snapshots:
        sync_snapshots(src)
    print(f"完成：代码 {'无变化' if n == 0 else f'{n} 个文件更新'}。"
          f"记得 git commit + push。")


if __name__ == "__main__":
    main()
