# -*- coding: utf-8 -*-
"""arena_batch.py v1.1 -- 擂台圈选批处理（算法=tools/arena_select.py v2.6，零改动口径）

单跑版每张卡重载池+标签+db_scan（秒级/张）；本脚本：
  1. 池/四层标签/judge/db_scan/absent/idf 只载一次；
  2. 候选集用倒排索引（db_index / topic_index）直取，不再全池扫描；
  3. 循环全部目标仓，写 cache/arena_all.json。
v1.1（2026-11-14 用户令）：应用类（judge cat=应用）不当候选、也不当主角——
  应用类不出档案卡，其擂台永不被消费，跳过主角省 1/3 跑批时间。

用法:
  python -I arena_batch.py --min-stars 300
  python -I arena_batch.py --fn patroni/patroni dbeaver/dbeaver
"""
import argparse, datetime, io, json, os, sys, time
from pathlib import Path

sys.path.insert(0, "D:/dbhub_collect/tools")
import arena_select as az

VER = "arena_batch/1.1"
ROOT = "D:/dbhub_collect"
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = HERE + os.sep + "cache"

def loadj(p): return json.load(io.open(p, encoding="utf-8"))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-stars", type=int, default=300)
    ap.add_argument("--fn", nargs="+")
    a = ap.parse_args()
    t0 = time.time()
    pool = az.load_pool(Path(ROOT) / "data/live/pool.ndjson")
    tags, judge, items = az.load_layers()
    dscan = loadj(ROOT + "/state/db_scan.v2.json")
    absent = {k.lower() for k in loadj(ROOT + "/state/absent_since.json")}
    idf = az.idf_map(tags)
    items_l = {fn.lower(): e.get("sha", "") for fn, e in items.items()}
    dscan_l = {fn.lower(): (e or {}) for fn, e in dscan.items()}

    info = {}; db_index = {}; topic_index = {}; db_topics = set()
    for fn0, r in pool.items():
        fn = fn0.lower()
        sha = items_l.get(fn, "")
        dbs = {k.lower() for k in dscan_l.get(fn, {}).get("cands", {})}
        info[fn] = {"stars": r.get("stars", 0), "archived": r.get("archived"),
                    "fork": r.get("fork"), "tb": tags.get(sha),
                    "cat": judge.get(sha), "dbs": dbs,
                    "topics": {x.lower() for x in (r.get("topics") or [])}}
        for d in dbs: db_index.setdefault(d, set()).add(fn)
    for e in dscan.values():
        for k in (e or {}).get("cands", {}): db_topics.add(k.lower())
    for fn, i in info.items():
        for tp in i["topics"]: topic_index.setdefault(tp, set()).add(fn)

    targets = a.fn or [fn for fn, i in info.items()
                       if (i["stars"] or 0) >= a.min_stars and not i["archived"]
                       and i["cat"] not in az.EXCL_CAT]   # 应用类不当主角（无卡可挂擂台）
    arenas = {}
    n_no_tags = n_empty = n_app_cand = 0
    for n, t in enumerate(targets, 1):
        ti = info.get(t)
        if ti is None: print(f"SKIP not-in-pool {t}"); continue
        ta = ti["tb"] or {}
        if not ta: n_no_tags += 1; continue
        cands = set()
        for d in ti["dbs"]: cands |= db_index.get(d, set())
        for tp in (ti["topics"] & db_topics): cands |= topic_index.get(tp, set())
        rows = []
        for fn in cands:
            if fn == t or fn in absent: continue
            i2 = info[fn]
            if i2["archived"] or i2["fork"]: continue
            if i2["cat"] in az.EXCL_CAT: n_app_cand += 1; continue   # v2.6 应用类不当候选
            tb = i2["tb"]
            if tb is None:
                if ti["cat"] and i2["cat"] == ti["cat"]:
                    rows.append({"fn": fn, "stars": i2["stars"], "score": az.CAT_FALLBACK_SCORE,
                                 "source": "cat_fallback", "tags": []})
                continue
            if az.UI_TAGS & set(tb) and not (az.UI_TAGS & set(ta)): continue
            s = az.sim(ta, tb, idf) * (0.7 + 0.3 * az.specificity(i2["dbs"], ti["dbs"]))
            if s >= 0.45:
                rows.append({"fn": fn, "stars": i2["stars"], "score": round(s, 3),
                             "source": "tags", "tags": sorted(tb), "dbs": sorted(i2["dbs"])})
        passing = [c for c in rows if c["source"] == "tags"]
        p50 = sorted([c["stars"] for c in passing])[len(passing) // 2] if passing else 300
        floor = min(2000, max(300, p50))
        kept = [c for c in rows if c["stars"] >= floor]
        kept.sort(key=lambda c: (-c["score"], -c["stars"]))
        top = kept[:5]
        if top:
            arenas[t] = {"floor": floor, "passing": len(passing), "kept": len(kept),
                         "target_tags": sorted(ta), "top": top}
        else:
            n_empty += 1
        if n % 500 == 0: print(f"  arena {n}/{len(targets)} done ...")
    out = {"meta": {"ver": VER, "built_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "algorithm": az.VER, "targets": len(targets), "with_arena": len(arenas),
                    "no_tags": n_no_tags, "empty_after_gates": n_empty,
                    "excl_app_cands": n_app_cand},
           "arenas": arenas}
    io.open(CACHE + "/arena_all.json", "w", encoding="utf-8", newline="\n").write(
        json.dumps(out, ensure_ascii=False))
    print(f"OK arena_batch: targets={len(targets)} with_arena={len(arenas)} "
          f"no_tags={n_no_tags} empty={n_empty} excl_app_cands={n_app_cand} in {time.time()-t0:.1f}s")

if __name__ == "__main__":
    main()
