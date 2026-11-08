# -*- coding: utf-8 -*-
"""G6-2 本地双读对拍：同一批仓，旧读（legacy v3 条目直查）vs 新读（InterpReader
四层拼接）逐字段 diff，差异必须落在可解释类目里。

旧读的还原方式：旧管线 = fn → interp_state.sha → 旧缓存裸 sha 条目（v3）。
G3 后 desc 类 fn 的台账已指新键（旧缓存查不到）→ 记作「旧读无、新读有」，
正是 desc 层新增覆盖，可解释。

对拍字段（语义对齐新旧两代）：
  分类    旧 classification.cat          vs 新 entry().classification.cat_primary
  一句话  旧 identity.one_liner          vs 新 identity().identity.one_liner
  引擎    旧 db_verdicts 组装            vs 新 dbs().dbs
  AI 标记 旧 classification.ai.kind      vs 新 ai_flag()

用法：
  python tools/dual_read_check.py --n 200            # 抽样对拍（默认 200）
  python tools/dual_read_check.py --json out.json    # 明细落盘
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "lib"))
sys.path.insert(0, str(ROOT / "interpret"))

from interp_store import load_cache                    # noqa: E402
from interp_read import InterpReader, FALLBACK_RELS    # noqa: E402


def old_read(cache: dict, sha: str) -> dict | None:
    """旧管线读法：台账 sha 直接查旧缓存（裸 sha=v3；desc 新键查不到=旧读无）。"""
    return cache.get(sha)


def old_dbs(leg: dict | None) -> list[str]:
    if not leg:
        return []
    verdicts = ((leg.get("classification") or {}).get("db_verdicts")) or []
    seen, out = set(), []
    for v in verdicts:
        db = v.get("db")
        if db and v.get("rel") in FALLBACK_RELS and db not in seen:
            seen.add(db)
            out.append(db)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=200)
    ap.add_argument("--seed", type=int, default=20261108)
    ap.add_argument("--json", metavar="PATH")
    a = ap.parse_args()

    cache = load_cache()
    r = InterpReader()
    idx = r._load_interp()
    pool = r._load_pool()
    # 验收口径：在池 fn（读层的扩展索引含台账外历史条目，混入会污染样本）
    fns = sorted(fn for fn in idx if fn in pool)
    sample = random.Random(a.seed).sample(fns, min(a.n, len(fns)))

    cat = Counter()
    rows = []
    for fn in sample:
        sha = idx[fn].get("sha") or ""
        leg = old_read(cache, sha)
        lcls = (leg or {}).get("classification") or {}
        lident = (leg or {}).get("identity") or {}
        new_e, new_i = r.entry(fn), r.identity(fn)
        ncls = (new_e or {}).get("classification") or {}
        nident = (new_i or {}).get("identity") or {}
        new_dbs = r.dbs(fn)
        # 字段名感知：v4 条目用 cat_primary，legacy/desc_legacy 条目用 cat——
        # 读链对 legacy 服务的 fn 返回的就是同一条 v3 数据，取对字段再比
        ncat = ncls.get("cat_primary") or ncls.get("cat")

        # 分类
        if not lcls.get("cat") and ncat:
            cat["分类:新读独有(desc 层/词控新覆盖)"] += 1
            d_cat = "new_only"
        elif lcls.get("cat") and not ncat:
            cat["分类:旧有新无(异常)"] += 1
            d_cat = "lost"
        elif lcls.get("cat") == ncat:
            cat["分类:一致"] += 1
            d_cat = "same"
        else:
            cat["分类:复审判定变更(v4 重烧)"] += 1
            d_cat = "rejudged"

        # 一句话
        lo, no = (lident.get("one_liner") or "").strip(), (nident.get("one_liner") or "").strip()
        if not lo and no:
            cat["一句话:新读独有(v4t/desc 新写)"] += 1
            d_one = "new_only"
        elif lo and not no:
            cat["一句话:旧有新无(异常)"] += 1
            d_one = "lost"
        elif lo == no:
            cat["一句话:逐字一致"] += 1
            d_one = "same"
        else:
            cat["一句话:重写(v4t 复烧,同义)"] += 1
            d_one = "rewritten"

        # 引擎归属
        od, nd = old_dbs(leg), new_dbs["dbs"]
        if od == nd:
            cat["引擎:一致"] += 1
        elif not od and nd:
            cat["引擎:新结论(程序引擎物化,G5-1)"] += 1
        elif od and not nd:
            cat["引擎:旧verdict清零(A修裁决/降级)"] += 1
        else:
            cat["引擎:结论变更(裁决推翻旧AI)"] += 1

        # AI 标记
        old_ai = bool((lcls.get("ai") or {}).get("kind"))
        if old_ai == r.ai_flag(fn):
            cat["AI标记:一致"] += 1
        else:
            cat["AI标记:变更(v4 ai_kind 复判)"] += 1

        rows.append({"fn": fn, "cat": d_cat, "one": d_one,
                     "old_cat": lcls.get("cat"), "new_cat": ncat,
                     "old_one": lo[:40], "new_one": no[:40],
                     "old_dbs": od, "new_dbs": nd})

    anomalies = [k for k in cat if "异常" in k]
    print(f"双读对拍 {len(sample)} 仓（seed {a.seed}）：")
    for k, v in sorted(cat.items()):
        print(f"  {k}: {v}")
    ok = not any(cat[k] for k in anomalies)
    print(f"结论：差异全部落在可解释类目 → {'PASS' if ok else 'FAIL'}"
          + ("（异常=旧有新无，需人工看）" if not ok else ""))
    if a.json:
        Path(a.json).write_text(
            json.dumps({"n": len(sample), "categories": dict(cat), "rows": rows},
                       ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"明细：{a.json}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
