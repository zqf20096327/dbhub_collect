# -*- coding: utf-8 -*-
"""一次性垃圾文件清理：移出到仓外备份目录（不删除，可整体还原）。

对象三类：
  1. .git/objects/pack/tmp_pack_*   中断 fetch 的遗留（git 从不引用 tmp_ 前缀）
  2. state/*.json.{1,2,3} 轮转副本   仅当基文件存在且为合法 JSON 且副本 mtime>7 天
  3. _archive_tmp/ 空目录            M1 归档遗留

明确不动：*.tmp_raw / *.ghdl（断点续传工具活性文件）、全部基文件、data/。

用法：
  python tools/gc_garbage_files.py            # dry-run，只列清单
  python tools/gc_garbage_files.py --apply    # 移出并写 manifest
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKUP_ROOT = Path("D:/dbhub_purge_backup_20261008/garbage")
STALE_DAYS = 7


def sha256_head(p: Path, n: int = 16) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        h.update(f.read(1 << 20))
        h.update(str(p.stat().st_size).encode())  # 区分同前缀不同长度的文件
    return h.hexdigest()[:n]


def candidates() -> list[tuple[Path, str]]:
    """返回 [(文件, 原因)]，附闸门校验不通过的直接剔除并列出。"""
    out: list[tuple[Path, str]] = []
    skipped: list[str] = []

    for p in sorted((ROOT / ".git/objects/pack").glob("tmp_pack_*")):
        out.append((p, "中断 fetch 遗留"))

    now = time.time()
    for p in sorted((ROOT / "state").glob("*.json.*")):
        suffix = p.name.split(".", 2)[-1]  # 只认纯数字轮转档
        if not suffix.isdigit():
            continue
        base = ROOT / "state" / p.name[: p.name.rfind(".")]
        age_days = (now - p.stat().st_mtime) / 86400
        if not base.exists():
            skipped.append(f"{p.name}: 基文件不存在，不动")
            continue
        try:
            json.load(open(base, encoding="utf-8"))
        except Exception as e:
            skipped.append(f"{p.name}: 基文件 {base.name} JSON 校验失败({e})，不动")
            continue
        if age_days < STALE_DAYS:
            skipped.append(f"{p.name}: 仅 {age_days:.1f} 天，未过 {STALE_DAYS} 天线，不动")
            continue
        out.append((p, f"轮转副本({suffix}档, {age_days:.0f} 天前)"))
    return out, skipped


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="真正移出（默认 dry-run）")
    args = ap.parse_args()

    files, skipped = candidates()
    total = sum(p.stat().st_size for p, _ in files)
    print(f"候选 {len(files)} 个, 共 {total/1e6:.1f} MB")
    for p, why in files:
        print(f"  {p.relative_to(ROOT)}  ({p.stat().st_size/1e6:.2f} MB)  {why}")
    for s in skipped:
        print(f"  [跳过] {s}")

    empty_dirs = [d for d in [ROOT / "_archive_tmp"] if d.is_dir() and not any(d.iterdir())]
    for d in empty_dirs:
        print(f"  {d.name}/  (空目录)")

    if not args.apply:
        print("\ndry-run 结束（未动任何文件）——加 --apply 执行移出")
        return 0

    BACKUP_ROOT.mkdir(parents=True, exist_ok=True)
    manifest = []
    for p, why in files:
        dst = BACKUP_ROOT / p.name
        if dst.exists():  # 防覆盖：同名加序号
            dst = BACKUP_ROOT / f"{p.name}.{int(time.time())}"
        size = p.stat().st_size
        if not (p.stat().st_mode & 0o200):  # 只读 tmp_pack 先放开属主写权限，跨盘 move 才不会卡删除
            p.chmod(0o644)
        shutil.move(str(p), str(dst))
        manifest.append({"orig": str(p), "backup": str(dst), "size": size,
                         "sha256_1m": sha256_head(dst), "reason": why})
        print(f"移出 {p.name} -> {dst.name}")
    for d in empty_dirs:
        d.rmdir()
        print(f"删除空目录 {d.name}/")

    (BACKUP_ROOT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\nmanifest 写入 {BACKUP_ROOT/'manifest.json'}（{len(manifest)} 项，可整体还原）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
