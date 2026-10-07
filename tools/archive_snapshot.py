# -*- coding: utf-8 -*-
"""快照目录归档：plan / pack / verify / unpack（10-06 M1）。

把 data/snapshot_YYYYMMDD/ 打成 {date}.tar.zst 上 Releases 前的全部本地环节。
包内首位 manifest.json 自描述：源目录、文件清单（名/大小/sha256）、工具与时间。

排除（打包时跳过，双保险于 .gitignore）：
- parts_*/            分通道原始结果，断点续采才需要，不归档
- *.part / *.tmp      写入中断残留（10-04 目录实发）；缺全量时用 --from-git 补
- *.json.[0-9]*       atomic_write 轮转副本
- __pycache__ 等

用法（仓库根目录）：
  python tools/archive_snapshot.py plan                      # 列 ≥15 天前待归档目录
  python tools/archive_snapshot.py pack data/snapshot_20260901 -o _archive_tmp/
  python tools/archive_snapshot.py verify _archive_tmp/20260901.tar.zst          # 只校验
  python tools/archive_snapshot.py verify _archive_tmp/20260901.tar.zst -d _r/   # 校验+解包

digest：pack/verify 均输出包级 sha256，stdout 末行固定
  DIGEST <sha256> <bytes>，供 release_archive 上传校验解析。
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import sys
import tarfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
TOOL = "archive_snapshot.py v1"

EXCLUDE_DIRS = {"parts_", "__pycache__", ".git"}
EXCLUDE_SUFFIX = (".part", ".tmp")
# 轮转副本 .1-.4 是 gh.atomic_write_json 的实际深度；扫到 .99 纯防御——
# 万一未来轮转加深也不会把副本打进归档包
EXCLUDE_ROT = lambda n: any(n.endswith(f".{i}") for i in range(1, 100))  # noqa: E731

MIN_AGE_DAYS = 15   # 与方案定的滚动窗口一致：≥15 天前的目录才归档


def _excluded(name: str) -> bool:
    """名字级排除规则（目录段与文件名共用；目录段不会命中后缀规则，无害）。"""
    if any(name.startswith(d) for d in EXCLUDE_DIRS) or name in EXCLUDE_DIRS:
        return True
    return name.endswith(EXCLUDE_SUFFIX) or EXCLUDE_ROT(name)


def plan(min_age_days: int = MIN_AGE_DAYS, data_dir: Path = DATA) -> list[Path]:
    """≥ min_age_days 天前的 snapshot_* 目录（UTC 口径，与目录名一致）。"""
    cutoff = datetime.now(timezone.utc).timestamp() - min_age_days * 86400
    out = []
    for d in sorted(data_dir.glob("snapshot_20*")):
        if not d.is_dir():
            continue
        try:
            dt = datetime.strptime(d.name, "snapshot_%Y%m%d").replace(tzinfo=timezone.utc)
        except ValueError:
            print(f"跳过（目录名非日期）：{d.name}", file=sys.stderr)
            continue
        if dt.timestamp() < cutoff:
            out.append(d)
    return out


def _sha256_file(p: Path) -> tuple[str, int]:
    h = hashlib.sha256()
    n = 0
    with open(p, "rb") as f:
        while chunk := f.read(1 << 20):
            h.update(chunk)
            n += len(chunk)
    return h.hexdigest(), n


def pack(dir_path: Path, out_dir: Path) -> Path:
    import zstandard as zstd

    if not dir_path.is_dir():
        raise SystemExit(f"不是目录：{dir_path}")
    date = dir_path.name.replace("snapshot_", "")
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{date}.tar.zst"

    files: list[Path] = []
    for p in sorted(dir_path.rglob("*")):
        if p.is_file() and not any(_excluded(q) for q in p.relative_to(dir_path).parts):
            files.append(p)

    manifest = {
        "tool": TOOL,
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source_dir": dir_path.name,
        "file_count": len(files),
        "total_bytes": sum(p.stat().st_size for p in files),
        "files": [
            {"name": str(p.relative_to(dir_path)).replace("\\", "/"),
             "size": p.stat().st_size, "sha256": _sha256_file(p)[0]}
            for p in files
        ],
    }

    cctx = zstd.ZstdCompressor(level=10)
    tmp = out.with_suffix(".tar.zst.tmp")   # 原子落盘：rotate 复用已存在包时不会撞上半包
    with open(tmp, "wb") as raw:
        with cctx.stream_writer(raw) as zw:
            with tarfile.open(fileobj=zw, mode="w|") as tf:
                mi = tarfile.TarInfo("manifest.json")
                mbytes = json.dumps(manifest, ensure_ascii=False, indent=1).encode("utf-8")
                mi.size = len(mbytes)
                tf.addfile(mi, io.BytesIO(mbytes))
                for p in files:
                    tf.add(p, arcname=str(p.relative_to(dir_path)).replace("\\", "/"))
    tmp.replace(out)

    digest, nbytes = _sha256_file(out)
    print(f"打包 {dir_path.name}：{len(files)} 文件 → {out.name} "
          f"{out.stat().st_size / 1e6:.1f}MB（原 {manifest['total_bytes'] / 1e6:.1f}MB）")
    print(f"DIGEST {digest} {nbytes}")
    return out


def _open_pkg(pkg: Path):
    import zstandard as zstd
    dctx = zstd.ZstdDecompressor()
    raw = open(pkg, "rb")
    return tarfile.open(fileobj=dctx.stream_reader(raw), mode="r|")


def verify(pkg: Path, unpack_to: Path | None = None) -> int:
    """校验包完整性：manifest 内逐文件 sha256 比对（unpack 时落盘再比，否则内存比）。"""
    if unpack_to:
        unpack_to.mkdir(parents=True, exist_ok=True)
    rc = 0
    with _open_pkg(pkg) as tf:
        member = tf.next()
        if member is None or member.name != "manifest.json":
            print("校验失败：包内首位不是 manifest.json", file=sys.stderr)
            return 1
        manifest = json.loads(tf.extractfile(member).read().decode("utf-8"))
        expect = {f["name"]: f for f in manifest["files"]}
        got = {}
        while (m := tf.next()) is not None:
            if not m.isfile():
                continue
            data = tf.extractfile(m).read()
            got[m.name] = (len(data), hashlib.sha256(data).hexdigest())
            if unpack_to:
                dest = unpack_to / m.name
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(data)
        for name, exp in expect.items():
            if name not in got:
                print(f"缺失：{name}", file=sys.stderr); rc = 1
            elif got[name] != (exp["size"], exp["sha256"]):
                print(f"不一致：{name} 期望 {exp['size']}B/{exp['sha256'][:12]}… "
                      f"实得 {got[name][0]}B/{got[name][1][:12]}…", file=sys.stderr); rc = 1
        for name in got:
            if name not in expect:
                print(f"多出：{name}", file=sys.stderr); rc = 1
    digest, nbytes = _sha256_file(pkg)
    if rc == 0:
        print(f"校验通过：{pkg.name} {manifest['file_count']} 文件 "
              f"（源 {manifest['source_dir']}，{manifest['created_utc']} 打包）")
    print(f"DIGEST {digest} {nbytes}")
    return rc


def main() -> int:
    ap = argparse.ArgumentParser(description="快照目录归档（plan/pack/verify/unpack）")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p1 = sub.add_parser("plan", help=f"列出 ≥{MIN_AGE_DAYS} 天前待归档目录")
    p1.add_argument("--min-age-days", type=int, default=MIN_AGE_DAYS)
    p2 = sub.add_parser("pack", help="打包目录为 {date}.tar.zst")
    p2.add_argument("dir")
    p2.add_argument("-o", "--out", default=str(ROOT / "_archive_tmp"))
    p3 = sub.add_parser("verify", help="校验包（含逐文件 sha256）")
    p3.add_argument("pkg")
    p3.add_argument("-d", "--unpack-to", default=None, help="同时解包到目录")
    args = ap.parse_args()

    if args.cmd == "plan":
        dirs = plan(args.min_age_days)
        for d in dirs:
            print(d)
        print(f"共 {len(dirs)} 个待归档（≥{args.min_age_days} 天前）")
        return 0
    if args.cmd == "pack":
        pack(Path(args.dir), Path(args.out))
        return 0
    if args.cmd == "verify":
        return verify(Path(args.pkg), Path(args.unpack_to) if args.unpack_to else None)
    return 2


if __name__ == "__main__":
    sys.exit(main())
