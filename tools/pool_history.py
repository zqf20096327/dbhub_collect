# -*- coding: utf-8 -*-
"""查任意日期某项目的池记录（10-06 M4）。日期口径 = UTC（快照目录名口径）。

数据源自动选择（按日期）：
- data/live/pool.ndjson 在该日 commit 里存在 → NDJSON 逐行取（切换日之后）
- 否则 data/snapshot_YYYYMMDD/pool.json 在该日 commit 里存在 → 旧 pretty JSON
- 都没有（已出 git 历史窗口）→ 提示月归档 Release；--download 自动下载解包查询

用法（仓库根目录）：
  python tools/pool_history.py --repo ClickHouse/ClickHouse --date 2026-09-15
  python tools/pool_history.py --repo x/y --date 2026-09-15 --field stars
  python tools/pool_history.py --repo x/y --field stars --from 2026-09-01 --to 2026-10-05
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tarfile
import urllib.request
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
# 归档命名契约（archive-YYYY-MM）与 repo 解析单点在 release_archive——
# 上传侧与查询侧必须同源，改月命名规则只动一处
from release_archive import month_of, repo_slug  # noqa: E402


def _git(*args: str) -> str:
    r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    return r.stdout.strip()


def _commit_before(day: date) -> str | None:
    """该日（UTC）结束前最后一个 commit。"""
    iso = f"{day.isoformat()}T23:59:59+00:00"
    sha = _git("rev-list", "-1", "--before", iso, "main")
    return sha or None


def _show_file(sha: str, path: str) -> bytes | None:
    r = subprocess.run(["git", "show", f"{sha}:{path}"], cwd=ROOT,
                       capture_output=True)
    return r.stdout if r.returncode == 0 else None


def fetch_day(day: date, repo: str) -> tuple[dict | None, str]:
    """取该日池中 repo 的记录。返回 (record, 来源说明)。"""
    sha = _commit_before(day)
    if not sha:
        return None, "无 commit（日期超出本地历史）"
    d8 = day.strftime("%Y%m%d")
    blob = _show_file(sha, f"data/live/pool.ndjson")
    if blob is not None:
        key = repo.casefold()
        for line in blob.decode("utf-8", "replace").splitlines():
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            if (rec.get("full_name") or "").casefold() == key:
                return rec, f"git {sha[:8]} data/live/pool.ndjson"
        return None, f"git {sha[:8]} live（未找到该 repo）"
    blob = _show_file(sha, f"data/snapshot_{d8}/pool.json")
    if blob is not None:
        try:
            recs = json.loads(blob.decode("utf-8", "replace"))
        except json.JSONDecodeError:
            return None, f"git {sha[:8]} snapshot_{d8}（JSON 损坏）"
        key = repo.casefold()
        for rec in recs:
            if (rec.get("full_name") or "").casefold() == key:
                return rec, f"git {sha[:8]} snapshot_{d8}/pool.json"
        return None, f"git {sha[:8]} snapshot_{d8}（未找到该 repo）"
    return None, "该日 git 中无池文件（可能已归档出历史）"


def fetch_day_from_release(day: date, repo: str, cache_dir: Path) -> tuple[dict | None, str]:
    """从月归档 Release 下载包并查询（--download 时用）。"""
    d8 = day.strftime("%Y%m%d")
    tag = month_of(d8)
    pkg = cache_dir / f"{d8}.tar.zst"
    if not pkg.is_file():
        cache_dir.mkdir(parents=True, exist_ok=True)
        url = (f"https://github.com/{repo_slug()}/releases/download/{tag}/{d8}.tar.zst")
        print(f"下载 {url}")
        urllib.request.urlretrieve(url, pkg)
    import zstandard as zstd
    dctx = zstd.ZstdDecompressor()
    key = repo.casefold()
    with tarfile.open(fileobj=dctx.stream_reader(open(pkg, "rb")), mode="r|") as tf:
        while (m := tf.next()) is not None:
            if m.name == "pool.json" or m.name.endswith("/pool.json"):
                recs = json.loads(tf.extractfile(m).read().decode("utf-8", "replace"))
                for rec in recs:
                    if (rec.get("full_name") or "").casefold() == key:
                        return rec, f"release {tag}/{d8}.tar.zst"
                return None, f"release {tag}（未找到该 repo）"
    return None, f"release {tag} 包内无 pool.json"


def _print_rec(rec: dict | None, src: str, field: str | None) -> None:
    if rec is None:
        print(f"  → 未找到（{src}）")
        return
    if field:
        print(f"  {field} = {rec.get(field, '<无此字段>')}")
    else:
        print(json.dumps(rec, ensure_ascii=False, indent=1))
    print(f"  来源：{src}")


def main() -> int:
    ap = argparse.ArgumentParser(description="查任意日期某项目的池记录（UTC 口径）")
    ap.add_argument("--repo", required=True, help="full_name，如 ClickHouse/ClickHouse")
    ap.add_argument("--date", help="YYYY-MM-DD")
    ap.add_argument("--field", help="只看某字段，如 stars")
    ap.add_argument("--from", dest="dfrom")
    ap.add_argument("--to", dest="dto")
    ap.add_argument("--download", action="store_true",
                    help="超出 git 历史窗口时自动从 Release 归档下载查询")
    args = ap.parse_args()

    if not args.date and not (args.dfrom and args.dto):
        ap.error("需要 --date，或 --from + --to")

    def get(day: date) -> tuple[dict | None, str]:
        rec, src = fetch_day(day, args.repo)
        if rec is None and args.download and ("超出本地历史" in src or "已归档" in src):
            return fetch_day_from_release(day, args.repo, ROOT / "_archive_tmp")
        return rec, src

    if args.date:
        day = date.fromisoformat(args.date)
        rec, src = get(day)
        _print_rec(rec, src, args.field)
        return 0 if rec else 1

    d0, d1 = date.fromisoformat(args.dfrom), date.fromisoformat(args.dto)
    day = d0
    print(f"{'日期':<12}{'值':>12}  来源")
    while day <= d1:
        rec, src = get(day)
        v = rec.get(args.field, "-") if rec else "-"
        print(f"{day.isoformat():<12}{str(v):>12}  {src}")
        day += timedelta(days=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
