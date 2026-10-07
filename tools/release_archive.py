# -*- coding: utf-8 -*-
"""归档包上 Releases + digest 校验 + 滚动归档（10-06 M1）。

上传/校验走 GitHub REST（免 gh，token 取 .env 的 GITHUB_TOKEN；API 触发
Actions 同款模式）。间歇阻断按次重试。

组织：按月一个 Release（tag=archive-YYYY-MM），资产名 {date}.tar.zst——
避免 365 个资产堆一个 release。

用法（仓库根目录）：
  python tools/release_archive.py plan                    # 本地待归档目录 → 计划
  python tools/release_archive.py upload _archive_tmp/20260901.tar.zst
  python tools/release_archive.py verify 20260901.tar.zst _archive_tmp/20260901.tar.zst
  python tools/release_archive.py rotate [--apply]        # 滚动：pack→upload→verify→删目录

verify 口径：资产 API 的 digest 字段（sha256:hex）与本地包 sha256 比对，零下载；
API 未返回 digest 时退化为 size 比对并明确警告（此时需抽样下载复核）。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from archive_snapshot import plan as plan_dirs, pack, MIN_AGE_DAYS  # noqa: E402

API = "https://api.github.com"
UPLOADS = "https://uploads.github.com"
RETRIES = 5


def _load_token() -> str:
    for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
        if line.startswith("GITHUB_TOKEN="):
            return line.split("=", 1)[1].strip().strip('"')
    raise SystemExit(".env 里没有 GITHUB_TOKEN")


def repo_slug() -> str:
    """repo 全名（owner/name）——归档体系内唯一取用处，防查询/上传两侧各自解析漂移。"""
    out = subprocess.run(["git", "remote", "get-url", "origin"], cwd=ROOT,
                         capture_output=True, text=True).stdout.strip()
    m = re.search(r"github\.com[:/]([^/]+/[^/\s]+?)(?:\.git)?$", out)
    if not m:
        raise SystemExit(f"无法从 remote 解析 repo：{out}")
    return m.group(1)


def _req(url: str, token: str, method: str = "GET", data=None,
         ctype: str = "application/json") -> dict | bytes:
    """带重试的 GitHub API 请求。JSON 响应返回 dict，二进制/空返回 bytes。

    非 2xx 由 urlopen 抛 HTTPError（无需自行判 status）：4xx 快速失败，
    403/429/5xx 与连接类异常按次重试（github.com 间歇阻断）。
    """
    last = None
    for i in range(RETRIES):
        req = urllib.request.Request(url, method=method, data=data)
        req.add_header("Authorization", f"Bearer {token}")
        req.add_header("Accept", "application/vnd.github+json")
        req.add_header("Content-Type", ctype)
        req.add_header("User-Agent", "dbhub-archive")
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                body = r.read()
                return json.loads(body) if isinstance(body, bytes) and body[:1] in (b"{", b"[") else body
        except urllib.error.HTTPError as e:
            # 4xx 语义错误重试无意义（403/429 限流与 5xx 才值得等）——快速失败省 75s
            if e.code in (403, 429) or e.code >= 500:
                last = e
                wait = 5 * (i + 1)
                print(f"  HTTP {e.code}，{wait}s 后重试 {i + 1}/{RETRIES}", file=sys.stderr)
                time.sleep(wait)
                continue
            detail = e.read()[:200].decode("utf-8", "replace")
            raise SystemExit(f"HTTP {e.code}（不重试）：{method} {url} {detail}")
        except Exception as e:  # noqa: BLE001 连接重置/超时等间歇阻断，重试
            last = e
            wait = 5 * (i + 1)
            print(f"  请求失败（{e}），{wait}s 后重试 {i + 1}/{RETRIES}", file=sys.stderr)
            time.sleep(wait)
    raise SystemExit(f"重试耗尽：{method} {url}（{last}）")


def _sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        while chunk := f.read(1 << 20):
            h.update(chunk)
    return h.hexdigest()


def month_of(date: str) -> str:
    """20260901 → archive-2026-09（tag 与 release 名）。"""
    return f"archive-{date[:4]}-{date[4:6]}"


def _get_release(slug: str, token: str, name: str) -> dict | None:
    for i in range(1, 5):
        rels = _req(f"{API}/repos/{slug}/releases?per_page=100&page={i}", token)
        if not rels:
            return None
        for r in rels:
            if r.get("name") == name or r.get("tag_name") == name:
                return r
    return None


def upload(slug: str, token: str, pkg: Path, date: str) -> dict:
    """传包到月 release。资产同名已存在则先删再传（幂等重传）。"""
    rel_name = month_of(date)
    rel = _get_release(slug, token, rel_name)
    if rel is None:
        rel = _req(f"{API}/repos/{slug}/releases", token, "POST",
                   json.dumps({"tag_name": rel_name, "name": rel_name,
                               "body": f"快照归档 {rel_name}（data/snapshot_*，zstd）"}).encode())
        print(f"创建 release {rel_name}（id={rel['id']}）")
    for a in rel.get("assets", []):
        if a["name"] == pkg.name:
            _req(a["url"], token, "DELETE")
            print(f"删除旧资产 {pkg.name}（重传）")
    asset = _req(f"{UPLOADS}/repos/{slug}/releases/{rel['id']}/assets?name={pkg.name}",
                 token, "POST", pkg.read_bytes(), ctype="application/octet-stream")
    print(f"上传 {pkg.name} → {rel_name}（{pkg.stat().st_size / 1e6:.1f}MB）")
    return asset


def verify_remote(slug: str, token: str, date: str, pkg: Path) -> int:
    """远端资产 digest vs 本地 sha256。digest 字段缺失退化为 size 比对。"""
    rel = _get_release(slug, token, month_of(date))
    if rel is None:
        print(f"未找到 release {month_of(date)}", file=sys.stderr)
        return 1
    asset = next((a for a in rel.get("assets", []) if a["name"] == pkg.name), None)
    if asset is None:
        print(f"资产缺失：{pkg.name}", file=sys.stderr)
        return 1
    local_sha, local_size = _sha256_file(pkg), pkg.stat().st_size
    if asset.get("digest", "").replace("sha256:", "") == local_sha:
        print(f"digest 一致：{pkg.name} sha256:{local_sha[:16]}…")
        return 0
    if "digest" not in asset or not asset["digest"]:
        if asset["size"] == local_size:
            print(f"警告：API 无 digest，仅 size 一致（{local_size}B）——需抽样下载复核",
                  file=sys.stderr)
            return 0
        print(f"size 不一致：远 {asset['size']} vs 本地 {local_size}", file=sys.stderr)
        return 1
    print(f"digest 不一致：远 {asset['digest']} vs 本地 sha256:{local_sha}", file=sys.stderr)
    return 1


def rotate(slug: str, token: str, apply: bool, out_dir: Path) -> int:
    """滚动归档：plan(≥15天) → pack（原子）→ upload → verify → 删工作树目录。CI 每日调用。"""
    from archive_snapshot import verify as verify_pkg
    rc = 0
    for d in plan_dirs():
        date = d.name.replace("snapshot_", "")
        pkg = out_dir / f"{date}.tar.zst"
        if pkg.is_file():
            # 复用旧包前先本地校验（历史半包/损坏包不能上远端）
            if verify_pkg(pkg) != 0:
                print(f"本地包校验未过，重新打包 {pkg.name}", file=sys.stderr)
                pkg.unlink()
        if not pkg.is_file():
            pkg = pack(d, out_dir)
        upload(slug, token, pkg, date)
        if verify_remote(slug, token, date, pkg) != 0:
            print(f"校验未过，保留本地目录 {d.name}", file=sys.stderr)
            rc = 1
            continue
        if apply:
            import shutil
            shutil.rmtree(d)
            print(f"已删工作树目录 {d.name}")
            pkg.unlink(missing_ok=True)
        else:
            print(f"[dry-run] 校验通过，可删 {d.name}（--apply 生效）")
    return rc


def main() -> int:
    ap = argparse.ArgumentParser(description="归档包上 Releases（plan/upload/verify/rotate）")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("plan")
    p2 = sub.add_parser("upload")
    p2.add_argument("pkg")
    p3 = sub.add_parser("verify")
    p3.add_argument("date", help="YYYYMMDD")
    p3.add_argument("pkg")
    p4 = sub.add_parser("rotate")
    p4.add_argument("--apply", action="store_true", help="真删工作树目录（默认 dry-run）")
    p4.add_argument("-o", "--out", default=str(ROOT / "_archive_tmp"))
    args = ap.parse_args()

    token, slug = _load_token(), repo_slug()
    if args.cmd == "plan":
        for d in plan_dirs():
            print(f"{d.name}  →  {month_of(d.name.replace('snapshot_', ''))}")
        return 0
    if args.cmd == "upload":
        pkg = Path(args.pkg)
        upload(slug, token, pkg, pkg.name.split(".")[0])
        return verify_remote(slug, token, pkg.name.split(".")[0], pkg)
    if args.cmd == "verify":
        return verify_remote(slug, token, args.date, Path(args.pkg))
    if args.cmd == "rotate":
        return rotate(slug, token, args.apply, Path(args.out))
    return 2


if __name__ == "__main__":
    sys.exit(main())
