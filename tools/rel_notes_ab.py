# -*- coding: utf-8 -*-
"""rel_notes 摘要 A/B 手动测试：旧法 body[:512 字符] vs 新法 _excerpt(512 字节)。

抽样口径：从 enrich 分片里取有 release 的仓，按池归属分层（中文池 / 国际池），
同一随机种子可复现；每仓取最近 3 个 release（与线上一致）。
只读：不写任何数据，只调 releases 端点。

用法：python tools/rel_notes_ab.py --n 180 --cn 60
"""
from __future__ import annotations

import argparse
import collections
import glob
import json
import random
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "lib"))
sys.path.insert(0, str(ROOT / "enrich"))

import gh          # noqa: E402
import enrich      # noqa: E402

OLD_CAP = 512      # 旧法：字符
NEW_CAP = 512      # 新法：UTF-8 字节


def eligible() -> set[str]:
    fns = set()
    for f in sorted(glob.glob(str(ROOT / "state" / "enrich_cache_shards" / "*.json"))):
        for fn, sig in json.load(open(f, encoding="utf-8")).items():
            if sig.get("rel_ver"):
                fns.add(fn)
    return fns


def pool(path: Path) -> set[str]:
    out = set()
    if not path.is_file():
        return out
    with path.open(encoding="utf-8") as f:
        for line in f:              # 只按 \n 切：splitlines 会被 U+2028 劈碎 JSON
            line = line.strip()
            if line:
                out.add(json.loads(line)["full_name"])
    return out


def signal_lines(body: str) -> list[str]:
    """正文里同时命中「库名/数据库」与「增删/弃用」的行。"""
    out = []
    for line in body.splitlines():
        s = line.strip()
        low = s.lower()
        if not s:
            continue
        if (any(w in low for w in enrich.DB_WORDS)
                and any(w in low for w in enrich.CHANGE_WORDS)):
            out.append(s)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=180)
    ap.add_argument("--cn", type=int, default=60, help="其中中文池仓数")
    ap.add_argument("--seed", type=int, default=20261030)
    args = ap.parse_args()

    el = eligible()
    cn = pool(ROOT / "data" / "live" / "pool_cn.ndjson") & el
    rnd = random.Random(args.seed)
    n_cn = min(args.cn, len(cn))
    pick_cn = rnd.sample(sorted(cn), n_cn) if n_cn else []
    rest = sorted(el - cn)
    n_rest = min(args.n - n_cn, len(rest))
    pick_rest = rnd.sample(rest, n_rest) if n_rest else []
    picks = [("cn", f) for f in pick_cn] + [("intl", f) for f in pick_rest]
    print(f"有 release 的仓 {len(el)}（中文池 {len(cn)}）；抽样 {len(picks)}"
          f"（cn={n_cn} intl={n_rest}）", flush=True)

    gh.load_env()
    client = gh.GitHubClient(gh.Budget(max_calls=len(picks) + 50))
    started = time.time()
    errs = collections.Counter()
    rows = []
    for i, (grp, fn) in enumerate(picks, 1):
        try:
            rels = client.releases(fn)
        except Exception as e:                      # 单仓失败不影响整体
            errs[type(e).__name__] += 1
            continue
        rows.append((grp, fn, rels[:3]))
        if i % 20 == 0:
            print(f"  [{i}/{len(picks)}] ok={len(rows)} err={dict(errs)} "
                  f"{time.time()-started:.0f}s", flush=True)
    print(f"拉取完成：ok={len(rows)} err={dict(errs)} "
          f"耗时 {time.time()-started:.0f}s\n", flush=True)

    old_b, new_b = [], []
    total = old_hit = new_hit = 0
    long_releases = 0
    misses = []
    grp_stat = collections.defaultdict(lambda: [0, 0])   # grp -> [命中行, 总行]
    for grp, fn, rels in rows:
        for r in rels:
            body = (r.get("body") or "").strip()
            if not body:
                continue
            lines = signal_lines(body)
            for s in lines:
                grp_stat[grp][1] += 1
            if len(body.encode("utf-8")) <= OLD_CAP:
                # 短正文两法一致，不计入 A/B，但命中行天然全保留
                for s in lines:
                    grp_stat[grp][0] += 1
                continue
            long_releases += 1
            old = body[:OLD_CAP]
            new = enrich._excerpt(body, NEW_CAP)
            old_b.append(len(old.encode("utf-8")))
            new_b.append(len(new.encode("utf-8")))
            for s in lines:
                total += 1
                key = s[:30]
                if key in old:
                    old_hit += 1
                if key in new:
                    new_hit += 1
                    grp_stat[grp][0] += 1
                else:
                    misses.append((fn, r.get("tag_name"), s[:100]))

    print("=== rel_notes A/B 手动测试 ===")
    print(f"仓 {len(rows)} 个；有正文 release 参与 A/B（>{OLD_CAP} 字节）: {long_releases} 条")
    if old_b:
        print(f"落盘字节  旧: 中位 {statistics.median(old_b):.0f} 最大 {max(old_b)}"
              f" | 新: 中位 {statistics.median(new_b):.0f} 最大 {max(new_b)}")
        over = sum(1 for b in new_b if b > NEW_CAP)
        print(f"新法超预算条数: {over}")
    print(f"DB 变更行（超长正文内）: {total} 行")
    if total:
        print(f"  旧法保留 {old_hit}/{total} = {100*old_hit/total:.0f}%")
        print(f"  新法保留 {new_hit}/{total} = {100*new_hit/total:.0f}%")
    for grp in ("cn", "intl"):
        keep, tot = grp_stat[grp]
        if tot:
            print(f"  分组 {grp}: 保留 {keep}/{tot} = {100*keep/tot:.0f}%"
                  f"（含短正文）")
    if misses:
        print("\n新法仍漏检的 DB 行:")
        for fn, tag, s in misses:
            print(f"  - {fn} {tag}: {s}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
