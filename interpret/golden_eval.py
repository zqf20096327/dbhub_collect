# -*- coding: utf-8 -*-
"""golden_eval —— 金标集回归评分器（一切 prompt/清理/参数改动的离线验收关）。

三步用法：
  python interpret/golden_eval.py --build            # ① 从存量缓存分层抽金标 ~150 + 边界例 30
  python interpret/golden_eval.py --run --tag base   # ② 跑分（默认 v2 提示词），结果存 state/golden_base.json
  python interpret/golden_eval.py --compare base v3  # ③ 两版对比

指标口径：
  pass1  = 第一次调用即过全部校验的比例（含 ai 失败的分母）
  pass2  = 违规重试一次内通过的比例（= 现行 interpret.py 的最终通过率）
  agree* = 通过项与金标的字段一致率（cat/eco/persona/status/dbs 精确集）
  边界例（历史拒收）无金标，只看通过率——衡量"新方案能不能把拒收捞回来"

采样口径：金标取自 interp_cache 中「sha 与 interp_state/readme_state 当前一致」的条目
（防内容漂移导致对比失真）；分层按 cat 每类 ≤12，另含少量 desc 降级路径。
"""
from __future__ import annotations

import argparse
import json
import logging
from datetime import datetime
import random
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import sys as _sys, pathlib as _pl
ROOT = _pl.Path(__file__).resolve().parents[1]
for _d in (ROOT, ROOT / "lib", ROOT / "config", ROOT / "interpret"):
    _sys.path.insert(0, str(_d))
HERE = ROOT
import strategy                              # noqa: E402
from gh import atomic_write_json             # noqa: E402
from interp_store import load_cache          # noqa: E402  分片缓存读取（兼容旧单文件）
import interpret as interp                   # noqa: E402
import runlog                                # noqa: E402
from interpret import AIClient, build_prompt, judge, latest_pool   # noqa: E402
from interpret import HERE as _IHERE         # noqa: E402
from pathlib import Path as _P
ISTATE_P = _P(_IHERE) / "state" / "interp_state.json"
CACHE_P = _P(_IHERE) / "state" / "interp_cache.json"
RSTATE_P = _P(_IHERE) / "state" / "readme_state.json"
GOLDEN = _P(_IHERE) / "state" / "golden_set.json"


def golden_path(set_no: int) -> _P:
    return GOLDEN if set_no <= 1 else _P(_IHERE) / "state" / f"golden_set{set_no}.json"

log = logging.getLogger("golden")


def readme_path(fn: str) -> Path:
    return _P(_IHERE) / "data" / "readmes" / (fn.replace("/", "__") + ".md")


def build(set_no: int = 1, per_cat: int = 12, boundary_n: int = 30):
    from pool_store import read_any
    pool = {it["full_name"]: it for it in read_any(latest_pool())}
    cache = load_cache()
    ist = json.loads(ISTATE_P.read_text(encoding="utf-8")).get("items", {})
    rst = json.loads(RSTATE_P.read_text(encoding="utf-8")).get("items", {})
    used = set()
    for prev in range(1, set_no):        # 排除所有更早金标集的条目（防重叠）
        p = golden_path(prev)
        if p.is_file():
            g = json.loads(p.read_text(encoding="utf-8"))
            used |= {e["fn"] for e in g["gold"]} | {e["fn"] for e in g["boundary"]}

    # ---- 金标：sha 未漂移 + readme 在盘 + 在池 ----
    rng = random.Random(42 * set_no + set_no)
    by_cat: dict[str, list[dict]] = {}
    desc_items = []
    for e in cache.values():
        fn = e.get("fn")
        if not fn or fn not in pool or fn in used:
            continue
        if e.get("source") == "desc":
            desc_items.append(e)
            continue
        rec = ist.get(fn) or {}
        if rec.get("status") != "done" or rec.get("sha") != e.get("sha"):
            continue                        # 漂移或非当前解读结果
        if rst.get(fn, {}).get("sha") != e.get("sha"):
            continue
        if not readme_path(fn).is_file():
            continue
        cat = ((e.get("classification") or {}).get("cat")) or "无"
        by_cat.setdefault(cat, []).append(e)
    gold = []
    for cat, lst in sorted(by_cat.items()):
        rng.shuffle(lst)
        gold += lst[:per_cat]
    rng.shuffle(desc_items)
    gold += desc_items[:max(4, per_cat // 3)]  # 降级路径少量覆盖
    rng.shuffle(gold)

    # ---- 边界：历史拒收（在池 + readme 在盘 + sha 未漂移） ----
    boundary = []
    for fn, rec in ist.items():
        if rec.get("status") != "rejected" or fn not in pool or fn in used:
            continue
        if rst.get(fn, {}).get("sha") != rec.get("sha"):
            continue
        if not readme_path(fn).is_file():
            continue
        boundary.append({"fn": fn, "sha": rec["sha"]})
    rng.shuffle(boundary)
    boundary = boundary[:boundary_n]

    out = {"built_at": time.strftime("%Y-%m-%d"), "set": set_no,
           "gold": [{"fn": e["fn"], "sha": e["sha"]} for e in gold],
           "boundary": boundary,
           "gold_data": {e["fn"]: e for e in gold}}
    atomic_write_json(golden_path(set_no), out)
    cats = {}
    for e in gold:
        cats[e["classification"]["cat"]] = cats.get(e["classification"]["cat"], 0) + 1
    print(f"金标 {len(gold)} 条（cat 分布 {cats}）· 边界 {len(boundary)} 条 → {golden_path(set_no)}")


def _dbs_of(obj):
    return set(((obj or {}).get("classification") or {}).get("dbs") or [])


def _cmp(res_obj, gold_obj) -> dict:
    r, g = (res_obj.get("classification") or {}), (gold_obj.get("classification") or {})
    rd, gd = (res_obj.get("signals") or {}), (gold_obj.get("signals") or {})
    ds, gs = _dbs_of(res_obj), _dbs_of(gold_obj)
    j = len(ds & gs) / len(ds | gs) if (ds | gs) else 1.0
    return {"cat": r.get("cat") == g.get("cat"), "eco": r.get("eco") == g.get("eco"),
            "persona": r.get("persona") == g.get("persona"),
            "status": rd.get("status") == gd.get("status"),
            "dbs_exact": ds == gs, "dbs_jaccard": j}


def run(tag: str, mode: str, limit: int, only: str, workers: int, dbscan_p: str | None,
        set_no: int = 1):
    out_p = _P(_IHERE) / "state" / f"golden_{tag}.json"
    if re.fullmatch(r"set\d+", tag or ""):       # golden_set*.json 是金标集命名空间，禁用
        raise SystemExit(f"tag '{tag}' 与金标集命名空间冲突，请换一个 tag")
    for p in (_P(_IHERE) / "state").glob("golden_set*.json"):   # 防结果文件覆盖已有金标集
        if out_p == p:
            raise SystemExit(f"tag '{tag}' 与金标集文件名冲突，请换一个 tag")
    gs = json.loads(golden_path(set_no).read_text(encoding="utf-8"))
    from pool_store import read_any
    pool = {it["full_name"]: it for it in read_any(latest_pool())}
    if mode == "v2":
        dbscan = json.loads((_P(dbscan_p) if dbscan_p else
                             _P(_IHERE) / "state" / "db_scan.v2.json").read_text(encoding="utf-8"))
    else:
        dbscan = json.loads((_P(dbscan_p) if dbscan_p else
                             _P(_IHERE) / "state" / "db_scan.json").read_text(encoding="utf-8"))
    gen = strategy.derive()
    schemas = interp.format_schemas(gen)   # schema 按条目选（与生产 run() 同口径）
    ai = AIClient()
    t0 = time.time()
    run_id = f"{datetime.now().strftime('%m%d_%H%M')}_g_{mode}_p{interp.PROMPT_VER}"

    jobs = []
    if only in ("gold", "all"):
        jobs += [(e, True) for e in gs["gold"]]
    if only in ("boundary", "all"):
        jobs += [(e, False) for e in gs["boundary"]]
    if limit:
        jobs = jobs[:limit]
    log.info("跑分 %s：%d 条（mode=%s）", tag, len(jobs), mode)

    results = []

    def one(entry, is_gold):
        fn, sha = entry["fn"], entry["sha"]
        degraded = sha.startswith("desc::")
        try:
            ctx = build_prompt(fn, degraded, pool, dbscan,
                               interp.pick_schema(schemas, degraded, mode), mode=mode)
        except Exception as e:               # noqa: BLE001
            return {"fn": fn, "kind": "failed", "error": f"ctx: {e}", "degraded": degraded}
        t1 = time.time()
        r = judge(fn, sha, degraded, ctx, ai, gen, mode=mode)
        r["secs"] = round(time.time() - t1, 1)
        r["is_gold"] = is_gold
        r["stats"] = ctx["stats"]
        r["degraded"] = degraded
        if is_gold and r["kind"] == "done":
            r["cmp"] = _cmp(r["obj"], gs["gold_data"][fn])
        return r

    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = [ex.submit(one, e, g) for e, g in jobs]
        for i, f in enumerate(as_completed(futs), 1):
            r = f.result()
            results.append(r)
            runlog.log_item({                                  # 金标跑分同样落条目日志
                "run_id": run_id, "src": "golden", "tag": tag, "mode": mode,
                "prompt_ver": interp.PROMPT_VER, "model": ai.model, "is_gold": r.get("is_gold"),
                "fn": r.get("fn"), "sha": r.get("sha"), "degraded": r.get("degraded"),
                **(r.get("stats") or {}),
                "kind": r.get("kind"), "validate_attempts": r.get("attempts"),
                "t_total_s": r.get("t_total_s"), "t_api_s": r.get("t_api_s"),
                "api_tries": r.get("api_tries"), "out_chars": r.get("out_chars"),
                "violations": r.get("violations"),
                "violations_all": r.get("violations_all"),
                "raw": r.get("raw") if r.get("kind") == "rejected" else None,
                "error": r.get("error"), "cmp": r.get("cmp")})
            if i % 20 == 0:
                log.info("进度 %d/%d", i, len(jobs))

    summary = _summarize(results)
    atomic_write_json(out_p,
                      {"tag": tag, "mode": mode, "summary": summary, "results": results})
    runlog.log_summary({**runlog.summarize_items(results), "run_id": run_id,
                        "src": "golden", "tag": tag, "mode": mode,
                        "prompt_ver": interp.PROMPT_VER, "model": ai.model,
                        "concurrency": workers, "golden_summary": summary})
    print(json.dumps(summary, ensure_ascii=False, indent=1))


def _summarize(results: list) -> dict:
    def block(rs: list) -> dict:
        n = len(rs)
        if not n:
            return {}
        done = [r for r in rs if r["kind"] == "done"]
        pass1 = [r for r in done if r.get("attempts") == 1]
        failed = [r for r in rs if r["kind"] == "failed"]
        rej = [r for r in rs if r["kind"] == "rejected"]
        d = {"n": n, "pass1%": round(len(pass1) * 100 / n, 1),
             "pass2%": round(len(done) * 100 / n, 1),
             "rejected": len(rej), "api_failed": len(failed),
             "avg_secs": round(sum(r.get("secs", 0) for r in rs) / n, 1),
             "avg_out_chars": round(sum(r.get("out_chars", 0) for r in rs) / n)}
        cmps = [r["cmp"] for r in done if r.get("is_gold") and r.get("cmp")]
        if cmps:
            for k in ("cat", "eco", "persona", "status", "dbs_exact"):
                d[f"agree_{k}%"] = round(sum(c[k] for c in cmps) * 100 / len(cmps), 1)
            d["avg_dbs_jaccard"] = round(sum(c["dbs_jaccard"] for c in cmps) / len(cmps), 3)
        return d
    out = {"gold": block([r for r in results if r.get("is_gold")]),
           "boundary": block([r for r in results if not r.get("is_gold")])}
    viols = {}
    for r in results:
        if r["kind"] == "rejected":
            for v in r.get("violations") or []:
                key = v.split("：")[0][:30]
                viols[key] = viols.get(key, 0) + 1
    if viols:
        out["reject_reasons"] = dict(sorted(viols.items(), key=lambda x: -x[1])[:10])
    return out


def compare(a: str, b: str):
    out = {}
    for tag in (a, b):
        p = _P(_IHERE) / "state" / f"golden_{tag}.json"
        if not p.is_file():
            raise SystemExit(f"缺 {p}")
        out[tag] = json.loads(p.read_text(encoding="utf-8"))["summary"]
    keys = ["n", "pass1%", "pass2%", "rejected", "api_failed", "avg_secs", "avg_out_chars",
            "agree_cat%", "agree_eco%", "agree_persona%", "agree_status%",
            "agree_dbs_exact%", "avg_dbs_jaccard"]
    print(f"{'指标':<18}{a:>12}{b:>12}")
    for grp in ("gold", "boundary"):
        print(f"—— {grp} ——")
        ga, gb = out[a].get(grp) or {}, out[b].get(grp) or {}
        for k in keys:
            if k in ga or k in gb:
                print(f"{k:<18}{ga.get(k, '-'):>12}{gb.get(k, '-'):>12}")


def main():
    ap = argparse.ArgumentParser(description="金标集回归评分器")
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--compare", nargs=2, metavar=("TAG_A", "TAG_B"))
    ap.add_argument("--tag", default="run")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--only", choices=["gold", "boundary", "all"], default="all")
    ap.add_argument("--mode", choices=["v2", "v3"], default="v2")
    ap.add_argument("--set", type=int, choices=[1, 2, 3, 4], default=1,
                    help="金标集：1=首套 / 2/3/4=后续套（均排除更早集合的条目）")
    ap.add_argument("--per-cat", type=int, default=12, help="每类别抽样上限")
    ap.add_argument("--boundary", type=int, default=30, help="边界例数量")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--dbscan", default=None, help="db_scan 文件路径（默认按 mode 选）")
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)-6s | %(message)s", datefmt="%H:%M:%S")
    if args.build:
        build(args.set, args.per_cat, args.boundary)
    if args.run:
        run(args.tag, args.mode, args.limit, args.only, args.workers, args.dbscan, args.set)
    if args.compare:
        compare(*args.compare)
    if not (args.build or args.run or args.compare):
        ap.error("--build / --run / --compare 至少其一")


if __name__ == "__main__":
    main()
