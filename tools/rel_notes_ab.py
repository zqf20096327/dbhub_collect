# -*- coding: utf-8 -*-
"""rel_notes 摘要 A/B 手动测试：旧法 body[:512 字符] vs 新法 _excerpt(512 字节+强度排序)。

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
RANK_NAME = ("移除/弃用", "新增支持", "兼容/连接", "仅提到库名")


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
    """正文里的库名行（只要求提到数据库），与线上 enrich.note_rank 同一判定。"""
    lines = []
    for line in body.splitlines():
        s = line.strip()
        if s and enrich.note_rank(s) is not None:
            lines.append(s)
    return lines


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
    fails = []
    rows = []
    for i, (grp, fn) in enumerate(picks, 1):
        try:
            rels = client.releases(fn)
        except Exception as e:                      # 单仓失败不影响整体
            errs[type(e).__name__] += 1
            resp = getattr(e, "response", None)
            fails.append((fn, getattr(resp, "status_code", None), str(e)[:120]))
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
    rank_total = [0, 0, 0, 0]
    rank_old = [0, 0, 0, 0]
    rank_new = [0, 0, 0, 0]
    misses = []
    grp_stat = collections.defaultdict(lambda: [0, 0])   # grp -> [保留, 总行]
    per = collections.defaultdict(lambda: dict(sig=0, sig_old=0, sig_new=0,
                                               hi=0, hi_old=0, hi_new=0))

    def keep_all(fn: str, lines: list[str]) -> None:
        """短正文：新旧两法都完整保留。"""
        for s in lines:
            per[fn]["sig"] += 1
            per[fn]["sig_old"] += 1
            per[fn]["sig_new"] += 1
            if enrich.note_rank(s) <= 1:            # 强/中强度 = 支持变更
                per[fn]["hi"] += 1
                per[fn]["hi_old"] += 1
                per[fn]["hi_new"] += 1

    for grp, fn, rels in rows:
        for r in rels:
            body = (r.get("body") or "").strip()
            if not body:
                continue
            lines = signal_lines(body)
            for s in lines:
                grp_stat[grp][1] += 1
            if len(body.encode("utf-8")) <= OLD_CAP:
                for s in lines:
                    grp_stat[grp][0] += 1
                keep_all(fn, lines)
                continue
            long_releases += 1
            old = body[:OLD_CAP]
            new = enrich._excerpt(body, NEW_CAP)
            old_b.append(len(old.encode("utf-8")))
            new_b.append(len(new.encode("utf-8")))
            for s in lines:
                total += 1
                rk = enrich.note_rank(s)
                rank_total[rk] += 1
                per[fn]["sig"] += 1
                if rk <= 1:
                    per[fn]["hi"] += 1
                key = s[:30]
                if key in old:
                    old_hit += 1
                    rank_old[rk] += 1
                    per[fn]["sig_old"] += 1
                    if rk <= 1:
                        per[fn]["hi_old"] += 1
                if key in new:
                    new_hit += 1
                    grp_stat[grp][0] += 1
                    rank_new[rk] += 1
                    per[fn]["sig_new"] += 1
                    if rk <= 1:
                        per[fn]["hi_new"] += 1
                else:
                    misses.append((fn, r.get("tag_name"), s[:100]))

    print("=== rel_notes A/B 手动测试 ===")
    print(f"仓 {len(rows)} 个；有正文 release 参与 A/B（>{OLD_CAP} 字节）: {long_releases} 条")
    if old_b:
        print(f"落盘字节  旧: 中位 {statistics.median(old_b):.0f} 最大 {max(old_b)}"
              f" | 新: 中位 {statistics.median(new_b):.0f} 最大 {max(new_b)}")
        over = sum(1 for b in new_b if b > NEW_CAP)
        print(f"新法超预算条数: {over}")
    print(f"库名行（超长正文内）: {total} 行")
    if total:
        print(f"  旧法保留 {old_hit}/{total} = {100*old_hit/total:.0f}%")
        print(f"  新法保留 {new_hit}/{total} = {100*new_hit/total:.0f}%")
        for rk in range(4):
            if rank_total[rk]:
                print(f"  强度{rk} {RANK_NAME[rk]}: {rank_new[rk]}/{rank_total[rk]} = "
                      f"{100*rank_new[rk]/rank_total[rk]:.0f}%"
                      f"（旧法 {100*rank_old[rk]/rank_total[rk]:.0f}%）")
    for grp in ("cn", "intl"):
        keep, tot = grp_stat[grp]
        if tot:
            print(f"  分组 {grp}: 保留 {keep}/{tot} = {100*keep/tot:.0f}%（含短正文）")

    # 更有效的指标：以仓为单位，是否至少保住一条「支持变更」（强/中强度）行
    repos = [v for v in per.values() if v["hi"]]
    if repos:
        o = sum(1 for v in repos if v["hi_old"])
        n = sum(1 for v in repos if v["hi_new"])
        print(f"\n每仓至少保住一条支持变更行（强度0/1）: "
              f"旧 {o}/{len(repos)} = {100*o/len(repos):.0f}% | "
              f"新 {n}/{len(repos)} = {100*n/len(repos):.0f}%")
    if fails:
        print("\n拉取失败的仓（明细）:")
        for fn, code, msg in fails:
            print(f"  - {fn} status={code} {msg}")
    if misses:
        print(f"\n新法仍漏检的信号行（共 {len(misses)} 行，列前 20）:")
        for fn, tag, s in misses[:20]:
            print(f"  - {fn} {tag}: {s}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
