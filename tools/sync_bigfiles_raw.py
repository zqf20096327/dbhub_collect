# -*- coding: utf-8 -*-
"""大文件走 raw.githubusercontent.com Range 断点续传拉取。

背景（10-08）：sync_remote_api.py 的 --max-blob-mb 会跳过大文件（blobs API 单请求
base64 整传，链路差时 5MB+ 反复断），但这些文件同样需要同步。实测 raw 通道带
token 支持 Range（206），断点续传可累计完成。下载到 <file>.tmp_raw，blob sha
校验通过才原子替换本地文件。

用法：
  python tools/sync_bigfiles_raw.py data/live/pool.ndjson state/db_scan.json ...
  python tools/sync_bigfiles_raw.py --dry-run data/...   # 只报远端 sha/大小/本地状态
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REPO = "zqf20096327/dbhub_collect"
RAW = f"https://raw.githubusercontent.com/{REPO}/main/"
API = f"https://api.github.com/repos/{REPO}"
UA = {"User-Agent": "dbhub-sync", "Accept": "application/vnd.github+json"}


def load_token() -> str:
    env = ROOT / ".env"
    if env.is_file():
        for line in env.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("GITHUB_TOKEN"):
                _, _, v = line.partition("=")
                v = v.strip().strip('"').strip("'")
                if v:
                    return v
    tok = os.environ.get("GITHUB_TOKEN", "")
    if tok:
        return tok
    sys.exit("未找到 GITHUB_TOKEN（.env 或环境变量）")


def blob_sha(data: bytes) -> str:
    h = hashlib.sha1()
    h.update(f"blob {len(data)}\0".encode())
    h.update(data)
    return h.hexdigest()


def remote_meta(token: str, path: str) -> tuple[str, int]:
    """contents API 拿远端 blob sha + 字节数。"""
    req = urllib.request.Request(
        f"{API}/contents/{path}", headers={**UA, "Authorization": f"Bearer {token}"})
    for i in range(6):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                d = json.loads(r.read())
                return d["sha"], int(d["size"])
        except Exception as e:  # noqa: BLE001
            if i == 5:
                raise
            print(f"  meta 重试 {i+1}/6（{e}）", flush=True)
            time.sleep(5 * (i + 1))
    raise RuntimeError("unreachable")


def fetch_ranged(token: str, url: str, tmp: Path, total: int, attempts: int = 40) -> bool:
    """Range 断点续传到 tmp；从 tmp 现有字节数续。

    10-08 实测：链路只杀"持续大流"（python HTTP/1.1、gh HTTP/2 全 alike，3m46 零字节），
    小请求 1s 即通，且掐断阈值会漂（同日见过 3MB 窗与 300KB 窗）——所以小块请求 +
    自适应：失败块大小减半（最低 96KB），连续成功再回升（封顶 768KB）。
    """
    chunk_sz = 768 * 1024
    min_sz, max_sz = 96 * 1024, 768 * 1024
    start = tmp.stat().st_size if tmp.exists() else 0
    if start > total:
        tmp.unlink()
        start = 0
    fails = 0
    while start < total:
        end = min(start + chunk_sz, total) - 1
        headers = {"User-Agent": "dbhub-sync", "Authorization": f"token {token}",
                   "Range": f"bytes={start}-{end}"}
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                data = r.read()
            if r.status != 206 or len(data) != end - start + 1:
                raise RuntimeError(f"status={r.status} len={len(data)}")
            with open(tmp, "ab") as f:
                f.write(data)
            start += len(data)
            fails = 0
            chunk_sz = min(int(chunk_sz * 1.5), max_sz)
        except Exception as e:  # noqa: BLE001
            fails += 1
            chunk_sz = max(chunk_sz // 2, min_sz)
            if fails >= attempts:
                print(f"  连续 {fails} 块失败止步于 {start}/{total}", flush=True)
                return False
            if fails % 5 == 1:
                print(f"  块失败 {fails}（{str(e)[:50]}），块降至 {chunk_sz//1024}KB，{start}/{total}", flush=True)
            time.sleep(min(3 * fails, 20))
    return start >= total


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+", help="仓库内路径，如 data/live/pool.ndjson")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    token = load_token()
    for path in args.paths:
        sha, size = remote_meta(token, path)
        local = ROOT / path
        cur = blob_sha(local.read_bytes()) if local.is_file() else "-"
        state = "已一致" if cur == sha else ("本地旧" if cur != "-" else "本地无")
        print(f"{path}：远端 {size/1048576:.1f}MB sha={sha[:10]}  {state}", flush=True)
        if args.dry_run or cur == sha:
            continue
        tmp = local.with_suffix(local.suffix + ".tmp_raw")
        if not fetch_ranged(token, RAW + path, tmp, size):
            print(f"  失败：{path} 未完成（tmp 保留可续跑）", flush=True)
            continue
        data = tmp.read_bytes()
        if len(data) != size or blob_sha(data) != sha:
            print(f"  校验不过（len={len(data)}），删 tmp 重来", flush=True)
            tmp.unlink()
            continue
        tmp.replace(local)
        print(f"  完成：{path}（{size/1048576:.1f}MB）", flush=True)


if __name__ == "__main__":
    main()
