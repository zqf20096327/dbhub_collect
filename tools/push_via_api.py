# -*- coding: utf-8 -*-
"""git 断连时用 GitHub Data API 推送本地 commit（与 sync_remote_api.py 的拉取对称）。

背景：github.com:443 间歇阻断时 git push/fetch 反复挂（invalid index-pack /
connection reset），api.github.com 通常仍通。本工具把一个本地 commit 的文件
变更经 blobs/trees/commits/refs API 重放到远端，等价 rebase 到远端 HEAD：

  1. GET  ref/heads/main          → 远端 HEAD sha
  2. GET  commits/{head}          → 远端 tree sha（作 base_tree）
  3. POST git/blobs  × N          → 每个变更文件（base64，内容寻址幂等）
  4. POST git/trees  (base_tree)  → 263 条目增量树
  5. POST git/commits (parents=[远端HEAD], message 沿用)
  6. PATCH refs/heads/main        → 快进（force=false）

限制与注意：
  - 只重放"文件变更"，不重放 merge 结构（本仓主线无 merge 需求）。
  - API commit 与本地 commit 内容相同但 sha 不同（committer/时间）——
    成功后本地应 git reset --hard origin/main 收敛（等 git 通道恢复 fetch 后）。
  - blob ≤100MB（API 限），本仓单文件远低于此；顺序上传无并发压力。
  - Core API 小时帽 ~5000：一次几百文件内。重跑幂等（blob 内容寻址）。

用法（仓库根目录）：
  python tools/push_via_api.py <commit_sha> [--dry-run]
"""
from __future__ import annotations

import argparse
import base64
import json
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API = "https://api.github.com"
RETRIES = 5


GH_EXES = [r"C:\Program Files\GitHub CLI\gh.exe",
           Path.home() / "AppData/Local/Programs/GitHub CLI/gh.exe"]


def _load_token(use_gh: bool = False) -> str:
    if use_gh:
        # gh 登录的 OAuth token 默认带 workflow scope——改 .github/workflows/**
        # 走 Data API 必须 workflow 权限（无权限时 GitHub 一律伪装 404，防 CI 注入探测）
        for exe in GH_EXES:
            if Path(exe).is_file():
                out = subprocess.run([str(exe), "auth", "token"],
                                     capture_output=True, text=True)
                tok = out.stdout.strip()
                if out.returncode == 0 and tok:
                    return tok
        raise SystemExit("找不到 gh CLI 或未登录（--gh-token 需要 gh auth login）")
    for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
        if line.startswith("GITHUB_TOKEN="):
            return line.split("=", 1)[1].strip().strip('"')
    raise SystemExit(".env 里没有 GITHUB_TOKEN")


def _repo_slug() -> str:
    out = subprocess.run(["git", "remote", "get-url", "origin"], cwd=ROOT,
                         capture_output=True, text=True).stdout.strip()
    import re
    m = re.search(r"github\.com[:/]([^/]+/[^/\s]+?)(?:\.git)?$", out)
    if not m:
        raise SystemExit(f"无法从 remote 解析 repo：{out}")
    return m.group(1)


def _req(url: str, token: str, method: str = "GET", payload: dict | None = None) -> dict:
    """带重试的 API 请求；4xx 快速失败，403/429/5xx 与连接类异常重试。"""
    last = None
    for i in range(RETRIES):
        data = json.dumps(payload).encode() if payload is not None else None
        req = urllib.request.Request(url, method=method, data=data)
        req.add_header("Authorization", f"Bearer {token}")
        req.add_header("Accept", "application/vnd.github+json")
        req.add_header("User-Agent", "dbhub-push")
        if data:
            req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code in (403, 429) or e.code >= 500:
                last = e
                wait = 5 * (i + 1)
                print(f"  HTTP {e.code}，{wait}s 后重试 {i + 1}/{RETRIES}", file=sys.stderr)
                time.sleep(wait)
                continue
            raise SystemExit(f"HTTP {e.code}（不重试）：{method} {url} {e.read()[:200]}")
        except Exception as e:  # noqa: BLE001 连接重置等间歇阻断
            last = e
            wait = 5 * (i + 1)
            print(f"  请求失败（{e}），{wait}s 后重试 {i + 1}/{RETRIES}", file=sys.stderr)
            time.sleep(wait)
    raise SystemExit(f"重试耗尽：{method} {url}（{last}）")


def main() -> int:
    ap = argparse.ArgumentParser(description="git 断连时经 Data API 推送本地 commit")
    ap.add_argument("commit", help="本地 commit sha（重放其文件变更到远端 HEAD）")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--gh-token", action="store_true",
                    help="用 gh CLI 的 token（含 workflow scope，推 .github/ 改动必须）")
    args = ap.parse_args()

    token, slug = _load_token(args.gh_token), _repo_slug()

    # 变更清单：A新增/M修改/D删除（D 在 tree API 里以 sha:null 表达）
    diff = subprocess.run(
        ["git", "diff-tree", "--no-commit-id", "-r", "--name-status",
         "--diff-filter=AMD", "-z", args.commit],
        cwd=ROOT, capture_output=True, text=True).stdout.split("\0")
    changes = [(diff[i], diff[i + 1]) for i in range(0, len(diff) - 1, 2)]
    if not changes:
        print("该 commit 无文件变更，无需推送")
        return 0

    head = _req(f"{API}/repos/{slug}/git/ref/heads/main", token)["object"]["sha"]
    print(f"远端 HEAD {head[:8]}，本地待重放 {len(changes)} 个文件")

    entries = []
    total = 0
    for i, (status, path) in enumerate(changes, 1):
        if status.startswith("D"):
            entries.append({"path": path, "mode": "100644", "type": "blob", "sha": None})
            print(f"  [{i}] 删除 {path}")
            continue
        blob = subprocess.run(["git", "show", f"{args.commit}:{path}"],
                              cwd=ROOT, capture_output=True).stdout
        total += len(blob)
        if not args.dry_run:
            b64 = base64.b64encode(blob).decode()
            obj = _req(f"{API}/repos/{slug}/git/blobs", token, "POST",
                       {"content": b64, "encoding": "base64"})
            sha = obj["sha"]
        else:
            sha = "(dry-run)"
        entries.append({"path": path, "mode": "100644", "type": "blob", "sha": sha})
        if i % 32 == 0 or i == len(changes):
            print(f"  blob {i}/{len(changes)}（累计 {total / 1e6:.1f}MB）")
    if args.dry_run:
        print(f"dry-run：共 {len(changes)} 文件 {total / 1e6:.1f}MB，未上传")
        return 0

    remote_tree = _req(f"{API}/repos/{slug}/git/commits/{head}", token)["tree"]["sha"]
    tree = _req(f"{API}/repos/{slug}/git/trees", token, "POST",
                {"base_tree": remote_tree, "tree": entries})["sha"]
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
