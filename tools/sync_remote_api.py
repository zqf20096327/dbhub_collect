# -*- coding: utf-8 -*-
"""git 断连时用 GitHub API 把远端最新采集数据同步到本地（只读数据，不动 git 历史）。

背景：github.com 443 间歇阻断时 git fetch 拉不动，但 api.github.com 通常还能通。
之前 10-01 用过一次临时命令（产物在 _remote_sync_1001/），本脚本是它的固化版。

原理：
  1. GET /repos/{repo}/git/trees/main?recursive=1  拿远端全量文件树（1 次请求）
  2. 本地算 git blob sha（sha1("blob {len}\0" + content)）比对，找出变更/新增文件
     注意换行符：本地部分文件是 CRLF、远端 blob 是 LF（内容等价），
     所以同时算原样/归一化(CRLF→LF)两种 sha，任一匹配即视为相同——
     不做这一步会把 3 万+ 文件全误判成差异（10-02 实测踩过）
  3. 只对 data/ state/ 下的差异文件逐个拉 blob（base64 解码落盘）
  4. 远端已删除的本地文件不动（只读同步，防止误删本地未提交内容）

注意：
  - 落盘后 git status 会显示这些文件"已修改"——属预期（工作区=远端，HEAD 落后），
    等 git 恢复后 fetch + 正常合并即可对齐。
  - Core API 小时帽 ~5000：增量几百文件没问题；若差异上千请分批（--limit）。
  - 大 blob（>1MB）走 blobs API 仍限 100MB，仓库数据文件远小于此。

用法：
  python tools/sync_remote_api.py                 # 同步 data/ + state/
  python tools/sync_remote_api.py --dry-run       # 只看差异不落盘
  python tools/sync_remote_api.py --limit 300     # 本次最多拉 300 个文件
  python tools/sync_remote_api.py --prefixes data,state,deploy
  python tools/sync_remote_api.py --via-compare   # 用 compare API 增量拉（见下）

--via-compare 背景（10-06）：间歇阻断下全量树（~9MB）单请求传不完（IncompleteRead
反复断在 2~9MB 处）。compare API 只返回本地 HEAD...origin/main 的变更文件清单
（几百~1MB 级），链路扛得住。限制：本地 HEAD 必须已推送到远端（否则 404）；
removed 文件跳过（保持只读不删本地）。
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REPO = "zqf20096327/dbhub_collect"
API = f"https://api.github.com/repos/{REPO}"
DEFAULT_PREFIXES = ("data/", "state/")

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


def api_get(url: str, token: str, retries: int = 8):
    """GET with retry；429/5xx/网络失败退避重试。返回 (bytes, remaining)。"""
    for i in range(retries):
        req = urllib.request.Request(url, headers={**UA, "Authorization": f"Bearer {token}"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read(), r.headers.get("X-RateLimit-Remaining", "?")
        except Exception as e:  # noqa: BLE001
            code = getattr(e, "code", None)
            if code == 404:
                raise
            if i == retries - 1:
                raise
            wait = 10 * (i + 1)
            print(f"  重试 {i+1}/{retries}（{code or e}），{wait}s 后…", flush=True)
            time.sleep(wait)
    raise RuntimeError("unreachable")


def blob_sha(data: bytes) -> str:
    h = hashlib.sha1()
    h.update(f"blob {len(data)}\0".encode())
    h.update(data)
    return h.hexdigest()


def fetch_compare_files(token: str, base: str, head: str, depth: int = 0):
    """compare API 拿 base...head 变更文件；超 300 条被截断时按中间 commit 分段递归。

    返回 [(path, blob_sha)]，removed 的不返回（只读同步不删本地）。
    注意（10-06 实测）：diff 大时 files 数组被静默截到 300 条且 truncated 字段
    不置位——所以把 len(files)>=290 也当截断信号，不信任 truncated 标志。
    分段最多 1 层：本仓单个采集/解读提交常超 300 文件，深递归只会层层触底
    （每段仍截断+请求翻倍），readmes 漏项交给 git 恢复后的正常合并兜底。
    """
    raw, rem = api_get(f"{API}/compare/{base}...{head}", token)
    data = json.loads(raw)
    files = [f for f in data.get("files", []) if f.get("status") != "removed" and f.get("sha")]
    truncated = data.get("truncated") or len(files) >= 290
    if not truncated:
        return files, rem
    commits = data.get("commits", [])
    if depth >= 1 or len(commits) < 3:
        print(f"提示：compare 截断（files={len(files)}），readmes 清单不全；"
              f"snapshot/state 由 contents 目录补全，readmes 差异等 git 恢复对齐", flush=True)
        return files, rem
    mid = commits[len(commits) // 2]["sha"]
    print(f"  compare 截断（files={len(files)}），按 {mid[:8]} 分段 …", flush=True)
    left, rem = fetch_compare_files(token, base, mid, depth + 1)
    right, rem = fetch_compare_files(token, mid, head, depth + 1)
    merged = {f["filename"]: f for f in left}
    for f in right:
        if f["filename"] in merged and f.get("status") == "removed":
            merged.pop(f["filename"], None)
        else:
            merged[f["filename"]] = f
    return list(merged.values()), rem


def list_remote_dir(token: str, dir_path: str):
    """contents API 列目录（含一层子目录，如 snapshot 的 meta/）；404 视为不存在。

    返回 [(path, sha, size)]——size 用于落盘前按 --max-blob-mb 过滤大文件。
    """
    out: list[tuple[str, str, int]] = []

    def _list(path: str):
        try:
            raw, _ = api_get(f"{API}/contents/{path}", token)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return
            raise
        for e in json.loads(raw):
            if e["type"] == "file":
                out.append((e["path"], e["sha"], e.get("size") or 0))
            elif e["type"] == "dir" and path.count("/") <= 1:  # 只下钻一层
                _list(e["path"])

    _list(dir_path)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="只列出差异，不落盘")
    ap.add_argument("--limit", type=int, default=0, help="本次最多拉取文件数（0=不限）")
    ap.add_argument("--prefixes", default=",".join(p.rstrip("/") for p in DEFAULT_PREFIXES),
                    help="同步的顶层目录（逗号分隔，默认 data,state）")
    ap.add_argument("--via-compare", action="store_true",
                    help="用 compare API 只拉本地 HEAD 之后的变更（绕开 9MB 全量树）")
    ap.add_argument("--skip-compare", action="store_true",
                    help="配合 --via-compare：跳过 compare（链路差时 1.2MB 反复传断），"
                         "只走 contents 目录补全（state/ + 近几天快照），不追 readmes 增量")
    ap.add_argument("--max-blob-mb", type=float, default=5.0,
                    help="跳过超过此大小（MB）的文件（10-06 实测：链路差时 1.2MB 都传断，"
                         "interp_cache 60MB/db_scan 16MB+ 必死且重试耗时长；"
                         "本地切片改造后远端大缓存拉下来也是倒退）。默认 5")
    args = ap.parse_args()

    prefixes = tuple(p.strip().strip("/") + "/" for p in args.prefixes.split(",") if p.strip())
    token = load_token()
    sizes: dict[str, int] = {}  # path -> 远端文件字节数（contents 补全时填，用于大文件过滤）

    if args.via_compare:
        import subprocess
        head_local = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True,
        ).stdout.strip()
        if not head_local:
            sys.exit("拿不到本地 HEAD，无法 compare")
        print(f"compare {head_local[:10]}...main …", flush=True)
        if args.skip_compare:
            print("  --skip-compare：跳过 compare，readmes 增量留给 git 恢复后对齐", flush=True)
            files, rem = [], "?"
        else:
            try:
                files, rem = fetch_compare_files(token, head_local, "main")
            except Exception as e:  # noqa: BLE001 链路差时 compare 1.2MB 反复传不完；
                # readmes 增量本就是尽力而为，跳过继续走 contents 补全（state/快照）
                print(f"compare 失败（{str(e)[:70]}），跳过 readmes 增量，仅用 contents 补全", flush=True)
                files, rem = [], "?"
        remote = {f["filename"]: f["sha"] for f in files
                  if f["filename"].startswith(prefixes)}
        # compare 300 条静默截断会漏文件（readms 大头注定漏，等 git 恢复对齐）；
        # 文件数少的目录用 contents API 全量列出补齐：state/ + 新快照目录（含 meta）
        for d in ["state", "data/snapshot_20261005", "data/snapshot_20261006",
                  "data/snapshot_20261007"]:
            n = 0
            for p, sha, sz in list_remote_dir(token, d):
                if p.startswith(prefixes):
                    remote[p] = sha
                    sizes[p] = sz
                    n += 1
            if n:
                print(f"  contents 补全 {d}/：{n} 个文件", flush=True)
        n_removed = sum(1 for f in files
                        if f.get("status") == "removed" and f["filename"].startswith(prefixes))
        print(f"远端变更 {len(remote)} 个（removed {n_removed} 个不拉；Core 余量 {rem}）",
              flush=True)
    else:
        print(f"拉取远端树 {REPO}@main …", flush=True)
        raw, rem = api_get(f"{API}/git/trees/main?recursive=1", token)
        tree = json.loads(raw)
        if tree.get("truncated"):
            print("警告：树被截断（文件太多），差异清单可能不全")
        remote = {e["path"]: e["sha"] for e in tree.get("tree", [])
                  if e["type"] == "blob" and e["path"].startswith(prefixes)}
        print(f"远端 {prefixes} 下 blob 共 {len(remote)} 个（Core 余量 {rem}）", flush=True)

    changed, added = [], []
    for path, sha in sorted(remote.items()):
        local = ROOT / path
        if not local.is_file():
            added.append(path)
            continue
        data = local.read_bytes()
        if blob_sha(data) != sha:
            # 本地 CRLF / 远端 LF 内容等价的情况：归一化后再比一次
            lf = data.replace(b"\r\n", b"\n")
            if blob_sha(lf) != sha:
                changed.append(path)

    print(f"差异：修改 {len(changed)}，新增 {len(added)}")
    todo = changed + added
    if args.max_blob_mb and sizes:
        limit = args.max_blob_mb * 1048576
        skipped = [p for p in todo if sizes.get(p, 0) > limit]
        if skipped:
            print(f"跳过 {len(skipped)} 个大文件（> {args.max_blob_mb}MB，git 恢复后对齐）：")
            for p in skipped:
                print(f"    {p}（{sizes[p] / 1048576:.1f}MB）")
            todo = [p for p in todo if p not in set(skipped)]
    if not todo:
        print("本地已是最新。")
        return
    if args.dry_run:
        for p in todo[:50]:
            print(f"  {'新' if p in added else '改'} {p}")
        if len(todo) > 50:
            print(f"  … 其余 {len(todo) - 50} 个略")
        return

    if args.limit and len(todo) > args.limit:
        print(f"--limit {args.limit}：本次只拉前 {args.limit} 个，剩余下次再跑")
        todo = todo[: args.limit]

    ok = fail = 0
    for i, path in enumerate(todo, 1):
        try:
            raw, rem = api_get(f"{API}/git/blobs/{remote[path]}", token)
            data = base64.b64decode(json.loads(raw)["content"])
            target = ROOT / path
            target.parent.mkdir(parents=True, exist_ok=True)
            tmp = target.with_suffix(target.suffix + ".tmp_sync")
            tmp.write_bytes(data)
            tmp.replace(target)
            ok += 1
            if i % 50 == 0 or i == len(todo):
                print(f"  {i}/{len(todo)} 完成（Core 余量 {rem}）", flush=True)
        except Exception as e:  # noqa: BLE001
            fail += 1
            print(f"  失败 {path}: {e}", flush=True)
        if rem not in ("?", None) and int(rem) < 50:
            print(f"Core 余量不足（{rem}），中止；剩余下次再跑")
            break

    print(f"完成：落盘 {ok}，失败 {fail}。"
          f"git status 会显示这些文件已修改——属预期，git 恢复后正常 fetch 合并对齐。")


if __name__ == "__main__":
    main()
