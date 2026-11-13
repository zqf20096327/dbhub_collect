# -*- coding: utf-8 -*-
"""push_via_api.py 的分片建树变体：单 commit 文件数 >~200 时，GitHub git/trees
单次 POST 会 422（"input too large / request timed out"），本工具把树条目按批
（默认 50）增量叠加：每批 base_tree=上一批产出的树 sha，最后 commit+ref 与
原工具一致。blob 先行全部上传（内容寻址幂等，重跑安全）。

用法（仓库根目录）：
  python tools/push_via_api_chunked.py <commit_sha> [--gh-token] [--dry-run] [--chunk 50]
"""
from __future__ import annotations

import argparse
import base64
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API = "https://api.github.com"

GH_EXES = [r"C:\Program Files\GitHub CLI\gh.exe",
           Path.home() / "AppData/Local/Programs/GitHub CLI/gh.exe"]


def _load_token() -> str:
    for exe in GH_EXES:
        if Path(exe).is_file():
            out = subprocess.run([str(exe), "auth", "token"],
                                 capture_output=True, text=True)
            if out.returncode == 0 and out.stdout.strip():
                return out.stdout.strip()
    raise SystemExit("找不到 gh CLI 或未登录")


def _repo_slug() -> str:
    import re
    out = subprocess.run(["git", "remote", "get-url", "origin"], cwd=ROOT,
                         capture_output=True, text=True).stdout.strip()
    m = re.search(r"github\.com[:/]([^/]+/[^/\s]+?)(?:\.git)?$", out)
    if not m:
        raise SystemExit(f"无法从 remote 解析 repo：{out}")
    return m.group(1)


def _req(url: str, token: str, method: str = "GET", payload: dict | None = None) -> dict:
    import time
    import urllib.error
    import urllib.request
    # 强制直连：本机 urllib 默认吃 Windows 系统代理（Clash 7897），Clash 上游抖动
    # 会把大 blob 上传拖到超时；直连 api.github.com 实测可用（gh CLI 同路径）。
    urllib.request.install_opener(
        urllib.request.build_opener(urllib.request.ProxyHandler({})))
    for i in range(5):
        data = json.dumps(payload).encode() if payload is not None else None
        req = urllib.request.Request(url, method=method, data=data)
        req.add_header("Authorization", f"Bearer {token}")
        req.add_header("Accept", "application/vnd.github+json")
        req.add_header("User-Agent", "dbhub-push-chunked")
        if data:
            req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code in (403, 429) or e.code >= 500:
                print(f"  HTTP {e.code}，{5 * (i + 1)}s 后重试 {i + 1}/5", file=sys.stderr)
                time.sleep(5 * (i + 1))
                continue
            raise SystemExit(f"HTTP {e.code}（不重试）：{method} {url} {e.read()[:200]}")
        except Exception as e:  # noqa: BLE001
            print(f"  请求失败（{e}），{5 * (i + 1)}s 后重试 {i + 1}/5", file=sys.stderr)
            time.sleep(5 * (i + 1))
    raise SystemExit(f"重试耗尽：{method} {url}")


def main() -> int:
    ap = argparse.ArgumentParser(description="分片建树版 API 推送（大 commit 用）")
    ap.add_argument("commit")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--chunk", type=int, default=50, help="每批树条目数（默认 50）")
    ap.add_argument("--jobs", type=int, default=8, help="blob 并行上传数（默认 8）")
    args = ap.parse_args()

    token, slug = _load_token(), _repo_slug()
    diff = subprocess.run(
        ["git", "diff-tree", "--no-commit-id", "-r", "--name-status",
         "--diff-filter=AMD", "-z", args.commit],
        cwd=ROOT, capture_output=True, text=True).stdout.split("\0")
    changes = [(diff[i], diff[i + 1]) for i in range(0, len(diff) - 1, 2)]
    if not changes:
        print("该 commit 无文件变更，无需推送")
        return 0

    head = _req(f"{API}/repos/{slug}/git/ref/heads/main", token)["object"]["sha"]
    print(f"远端 HEAD {head[:8]}，本地待重放 {len(changes)} 个文件（chunk={args.chunk}）")

    # ① blob 并行上传（内容寻址幂等；网络抖时串行慢且易卡，8 并发压到分钟级）
    def _one(idx: int):
        status, path = changes[idx]
        if status.startswith("D"):
            return idx, {"path": path, "mode": "100644", "type": "blob", "sha": None}, 0
        blob = subprocess.run(["git", "show", f"{args.commit}:{path}"],
                              cwd=ROOT, capture_output=True).stdout
        if args.dry_run:
            return idx, {"path": path, "mode": "100644", "type": "blob",
                         "sha": "(dry-run)"}, len(blob)
        b64 = base64.b64encode(blob).decode()
        obj = _req(f"{API}/repos/{slug}/git/blobs", token, "POST",
                   {"content": b64, "encoding": "base64"})
        return idx, {"path": path, "mode": "100644", "type": "blob",
                     "sha": obj["sha"]}, len(blob)

    from concurrent.futures import ThreadPoolExecutor
    entries, total = [None] * len(changes), 0
    with ThreadPoolExecutor(max_workers=args.jobs) as ex:
        for idx, e, size in ex.map(_one, range(len(changes))):
            entries[idx], total = e, total + size
            if (idx + 1) % 16 == 0 or idx + 1 == len(changes):
                print(f"  blob {idx + 1}/{len(changes)}（累计 {total / 1e6:.1f}MB）",
                      flush=True)
    if args.dry_run:
        print(f"dry-run：共 {len(changes)} 文件 {total / 1e6:.1f}MB，未上传")
        return 0

    # ② 增量建树：每批 ≤chunk 条，base_tree 接上一批产出的树
    tree = _req(f"{API}/repos/{slug}/git/commits/{head}", token)["tree"]["sha"]
    for b in range(0, len(entries), args.chunk):
        batch = entries[b:b + args.chunk]
        tree = _req(f"{API}/repos/{slug}/git/trees", token, "POST",
                    {"base_tree": tree, "tree": batch})["sha"]
        print(f"  树批次 {b // args.chunk + 1}/{(len(entries) + args.chunk - 1) // args.chunk}"
              f"（{len(batch)} 条）→ {tree[:8]}", flush=True)

    # ③ commit + ref（与原工具一致）
    msg = subprocess.run(["git", "log", "-1", "--format=%B", args.commit],
                         cwd=ROOT, capture_output=True, text=True).stdout.strip()
    new_c = _req(f"{API}/repos/{slug}/git/commits", token, "POST",
                 {"message": msg, "tree": tree, "parents": [head]})
    _req(f"{API}/repos/{slug}/git/refs/heads/main", token, "PATCH",
         {"sha": new_c["sha"], "force": False})
    print(f"推送成功：远端 main → {new_c['sha'][:8]}（本地同名内容 commit 保留为悬空，"
          f"git 恢复后 fetch + reset --hard origin/main 收敛）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
