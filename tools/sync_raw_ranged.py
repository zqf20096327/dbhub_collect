# -*- coding: utf-8 -*-
"""sync_remote_api.py 的补位：大文件用 raw CDN + Range 分段下载。

背景：github.com/api.github.com 间歇阻断时，>10MB 的 blob 单次 GET 极易
IncompleteRead（60s 内拉不完连接就被重置），sync_remote_api.py 的整段重试
对 23~28MB 的快照/pool 文件基本必败（2026-10-05 实测 db_scan.json 5 连败）。

raw.githubusercontent.com 走 Fastly CDN，与 github.com 阻断不同源，且支持
Range 断点续传——把大文件切成 4MB 段逐段拉，单段失败只重试该段。

校验：拼装完成后算 git blob sha，与远端 tree 里记录的 sha 不一致则不落盘
（raw 返回的就是 blob 原始内容，应当严格相等，无需 CRLF 归一化）。

用法：
  python tools/sync_raw_ranged.py                # 处理 data/+state/ 全部差异，>8MB 走分段
  python tools/sync_raw_ranged.py --dry-run
  python tools/sync_raw_ranged.py --paths state/db_scan.json,data/snapshot_20261005/pool.json
  python tools/sync_raw_ranged.py --threshold 8  # MB，超过才走分段，小的仍走 blobs API
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import socket
import sys
import time
import urllib.request
from pathlib import Path

socket.setdefaulttimeout(90)  # DNS 解析卡住不触发 urlopen timeout，用全局兜底

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REPO = "zqf20096327/dbhub_collect"
API = f"https://api.github.com/repos/{REPO}"
RAW = f"https://raw.githubusercontent.com/{REPO}/main/"
DEFAULT_PREFIXES = ("data/", "state/")

UA = {"User-Agent": "dbhub-sync", "Accept": "application/vnd.github+json"}
SEG = 2 * 1024 * 1024  # 2MB/段：窗口越短越容易在阻断间隙里钻过去


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


def api_get(url: str, token: str, retries: int = 5):
    for i in range(retries):
        req = urllib.request.Request(url, headers={**UA, "Authorization": f"Bearer {token}"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read(), r.headers.get("X-RateLimit-Remaining", "?")
        except Exception as e:  # noqa: BLE001
            if getattr(e, "code", None) == 404:
                raise
            if i == retries - 1:
                raise
            wait = 10 * (i + 1)
            print(f"  重试 {i+1}/{retries}（{code_of(e)}），{wait}s 后…", flush=True)
            time.sleep(wait)
    raise RuntimeError("unreachable")


def code_of(e: Exception) -> str:
    return str(getattr(e, "code", None) or e)


def blob_sha(data: bytes) -> str:
    h = hashlib.sha1()
    h.update(f"blob {len(data)}\0".encode())
    h.update(data)
    return h.hexdigest()


def fetch_raw_ranged(path: str, size: int, part: Path | None = None) -> bytes:
    """raw CDN 分段拉取；size 来自远端 tree，用于分段与总长校验。

    part 非 None 时段落盘到 .part 文件（跨进程续传）：中断后重跑只补缺的段，
    不再从 0 开始——4MB×8 次重试仍可能整文件失败的教训（10-05）。
    """
    url = RAW + path.replace("#", "%23").replace("?", "%3F")
    out = bytearray()
    if part is not None and part.is_file():
        out += part.read_bytes()
        if len(out) >= size:
            out = out[:size]  # 长度异常时截断，交给 sha 校验兜底
    seg_retries = 6
    while len(out) < size:
        start, end = len(out), min(len(out) + SEG - 1, size - 1)
        got = False
        for i in range(seg_retries):
            req = urllib.request.Request(
                url, headers={"User-Agent": "dbhub-sync", "Range": f"bytes={start}-{end}"})
            try:
                with urllib.request.urlopen(req, timeout=60) as r:
                    chunk = r.read()
                if r.status == 200:  # CDN 忽略 Range，整文件返回
                    if len(chunk) != size:
                        raise IOError(f"200 无 Range 且长度不符 {len(chunk)}!={size}")
                    if part is not None:
                        part.write_bytes(chunk)
                    return bytes(chunk)
                if len(chunk) != end - start + 1:
                    raise IOError(f"段长不符 {len(chunk)}!={end - start + 1}")
                out += chunk
                got = True
                break
            except Exception as e:  # noqa: BLE001
                if i == seg_retries - 1:
                    raise
                wait = 3 * (i + 1)
                print(f"    段 {start//SEG} 重试 {i+1}（{code_of(e)}），{wait}s…", flush=True)
                time.sleep(wait)
        if not got:
            raise IOError(f"段 {start}-{end} 重试用尽")
        if part is not None:
            part.write_bytes(bytes(out))  # 已过段落盘，进程死了也能续
        print(f"    段 {start//SEG + 1}/{(size + SEG - 1)//SEG} 累计 {len(out)}/{size}", flush=True)
    if len(out) != size:
        raise IOError(f"拼装长度不符 {len(out)}!={size}")
    return bytes(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--paths", default="", help="逗号分隔的指定文件；缺省则全目录比对")
    ap.add_argument("--threshold", type=float, default=5, help="超过此 MB 数才走 raw 分段，否则 blobs API（注意 blobs 响应是 base64，膨胀 ~1.37 倍）")
    args = ap.parse_args()

    token = load_token()

    if args.paths:
        wanted = {p.strip() for p in args.paths.split(",") if p.strip()}
    else:
        wanted = None

    print(f"拉取远端树 {REPO}@main …", flush=True)
    tree_cache = ROOT / "state" / ".sync_tree_cache.json"
    try:
        raw, rem = api_get(f"{API}/git/trees/main?recursive=1", token)
        tree_cache.write_bytes(raw)  # 拉成功才更新缓存
    except Exception as e:  # noqa: BLE001
        if not tree_cache.is_file():
            raise
        print(f"树请求失败（{e}），用上次缓存 {tree_cache.name}", flush=True)
        raw, rem = tree_cache.read_bytes(), "?"
    tree = json.loads(raw)
    if tree.get("truncated"):
        print("警告：树被截断，差异清单可能不全")
    entries = {e["path"]: (e["sha"], e.get("size", 0)) for e in tree.get("tree", [])
               if e["type"] == "blob" and e["path"].startswith(DEFAULT_PREFIXES)}
    print(f"远端 {DEFAULT_PREFIXES} 下 blob 共 {len(entries)} 个（Core 余量 {rem}）", flush=True)

    todo = []
    if wanted:
        for p in sorted(wanted):
            if p not in entries:
                sys.exit(f"远端树里没有 {p}")
            todo.append(p)
    else:
        for path, (sha, _size) in sorted(entries.items()):
            local = ROOT / path
            if not local.is_file():
                todo.append(path)
                continue
            data = local.read_bytes()
            if blob_sha(data) != sha and blob_sha(data.replace(b"\r\n", b"\n")) != sha:
                todo.append(path)
    print(f"待同步 {len(todo)} 个", flush=True)
    if not todo:
        print("本地已是最新。")
        return
    if args.dry_run:
        for p in todo:
            print(f"  {p}（{entries[p][1] / 1e6:.1f}MB）")
        return

    ok = fail = 0
    for i, path in enumerate(todo, 1):
        sha, size = entries[path]
        part = ROOT / (path + ".part")
        try:
            if size > args.threshold * 1e6:
                print(f"  [{i}/{len(todo)}] raw分段 {path}（{size / 1e6:.1f}MB，"
                      f"已有 .part {part.stat().st_size if part.is_file() else 0}B）", flush=True)
                data = fetch_raw_ranged(path, size, part)
            else:
                raw, rem = api_get(f"{API}/git/blobs/{sha}", token)
                data = base64.b64decode(json.loads(raw)["content"])
            got = blob_sha(data)
            if got != sha:
                if part.is_file():
                    part.unlink()  # 内容不对，续传缓存不可信
                raise IOError(f"sha 不符 {got}!={sha}，不落盘")
            target = ROOT / path
            target.parent.mkdir(parents=True, exist_ok=True)
            tmp = target.with_suffix(target.suffix + ".tmp_sync")
            tmp.write_bytes(data)
            tmp.replace(target)
            ok += 1
            if part.is_file():
                part.unlink()
        except Exception as e:  # noqa: BLE001
            fail += 1
            print(f"  失败 {path}: {e}", flush=True)
        if rem not in ("?", None) and int(rem) < 50 and i < len(todo):
            print(f"Core 余量不足（{rem}），中止；剩余下次再跑")
            break
    print(f"完成：落盘 {ok}，失败 {fail}。")
    if fail:
        sys.exit(1)  # 外层轮询循环靠退出码决定是否继续磨


if __name__ == "__main__":
    main()
