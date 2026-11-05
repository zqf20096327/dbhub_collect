# -*- coding: utf-8 -*-
"""一次性存量清账驱动：只重试 interp_state 里的 rejected/failed 条目（v4）。
不复用 run() 的 todo 逻辑——那里按 star 排序+截断，142 条拒收会被 3.3 万积压挤走。"""
import sys, json, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for d in (ROOT, ROOT / "lib", ROOT / "config", ROOT / "interpret"):
    sys.path.insert(0, str(d))
import interpret as itp
from interp_store import InterpCacheStore

st = json.loads((ROOT / "state/interp_state.json").read_text(encoding="utf-8"))
rstate = json.loads((ROOT / "state/readme_state.json").read_text(encoding="utf-8"))["items"]
dbscan = json.loads((ROOT / "state/db_scan.json").read_text(encoding="utf-8")) \
    if (ROOT / "state/db_scan.json").is_file() else {}
import pool_store
pool = {}
for p in ("data/live/pool.ndjson", "data/live/pool_cn.ndjson", "data/live/pool_intl.ndjson"):
    for r in pool_store.read_any(ROOT / p):
        pool[r["full_name"]] = r

jobs = []
for fn, v in list(st["items"].items()):
    if v.get("status") not in ("rejected", "failed"):
        continue
    rec = rstate.get(fn) or {}
    desc_key = None
    if rec.get("status") == "no_readme":
        desc = (pool.get(fn, {}).get("description") or "")[:100]
        if desc:
            desc_key = "desc::" + desc
    sha = rec.get("sha") if rec.get("status") in ("done", "oversized") and rec.get("sha") else desc_key
    if not sha:
        continue
    jobs.append((fn, sha, desc_key is not None))
print(f"存量重试 {len(jobs)} 条（rejected+failed）")

schema_v4 = itp.format_schemas(None)["v4"]
ai = itp.AIClient(deadline=time.time() + 40 * 60)
cache = InterpCacheStore()
lock_free_results = []

def one(job):
    fn, sha, degraded = job
    if itp.cache_key(sha, "v4") in cache:          # v4 缓存已有（曾重烧成功过）
        return ("cached", fn, sha, None)
    if degraded:
        # desc 降级项恒走 v2 老卷——不属于 v4 清账范围，保留原状
        return ("skip_desc", fn, sha, None)
    ctx = itp.build_prompt(fn, False, pool, dbscan, schema_v4, mode="v4")
    r = itp.judge(fn, sha, False, ctx, ai, {}, mode="v4")
    return (r["kind"], fn, sha, r)

from collections import Counter
kinds = Counter()
new_rej = []
with ThreadPoolExecutor(max_workers=6) as ex:
    futs = [ex.submit(one, j) for j in jobs]
    for f in as_completed(futs):
        kind, fn, sha, r = f.result()
        kinds[kind] += 1
        if kind == "done":
            from rm_clean import CLEAN_VER
            from clean_delta import save as cd_save
            if r.get("clean_delta"):
                cd_save(f"{sha}+{CLEAN_VER}", r["clean_delta"], fn=fn)
                r["obj"]["clean_ver"] = CLEAN_VER
            cache[itp.cache_key(sha, "v4")] = r["obj"]
            st["items"][fn] = {"sha": sha, "status": "done"}
        elif kind == "rejected":
            st["items"][fn] = {"sha": sha, "status": "rejected",
                               "violations": r["violations"][:3], "raw": (r.get("raw") or "")[:200]}
            new_rej.append((fn, r["violations"][:2]))
        elif kind == "failed":
            st["items"][fn] = {"sha": sha, "status": "failed", "error": (r.get("error") or "")[:150]}
print("结果:", dict(kinds))
for fn, v in new_rej[:10]:
    print("  仍拒:", fn, "|", v)
cache.flush()
(ROOT / "state/interp_state.json").write_text(
    json.dumps(st, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print("state 已落盘")
