# -*- coding: utf-8 -*-
"""A/B 验证：应用类短提示（lite）vs 全量 README 提示（full）。
对象 = 500 条影子里 eco=app 的仓（已有一份 full 结果），再跑一遍 lite 对照。
产出 state/shadow/app_lite_ab.json，不写生产缓存。"""
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for _d in (ROOT, ROOT / "lib", ROOT / "config", ROOT / "interpret"):
    sys.path.insert(0, str(_d))

import interpret as itp                                     # noqa: E402
import pool_store                                           # noqa: E402
import _shadow_vocab as sv                                  # noqa: E402
from _run_domain_tags_shadow import (build_lite_prompt, load_v4_index, parse_out)  # noqa: E402

OUT = ROOT / "state" / "shadow"


def main():
    vocab = sv.parse_vocab()
    vblock = sv.vocab_block(vocab)
    vset = {w["slug"] for d in vocab["domains"] for w in d["words"]}
    rep = json.loads((OUT / "domain_tags_shadow_500.json").read_text(encoding="utf-8"))
    v4 = load_v4_index()

    # 取 500 条里 eco=app 且有 full 结果的仓
    base = {}
    for r in rep["items"]:
        if r["run"] != 1 or r.get("tags") is None:
            continue
        eco = ((v4.get(r["fn"]) or {}).get("classification") or {}).get("eco")
        if eco == "app":
            base[r["fn"]] = r
    print(f"eco=app 且有 full 结果：{len(base)} 条", flush=True)

    pool = {}
    for p in ("data/live/pool.ndjson", "data/live/pool_cn.ndjson", "data/live/pool_intl.ndjson"):
        for rec in pool_store.read_any(ROOT / p):
            pool[rec["full_name"]] = rec

    ai = itp.AIClient(deadline=time.time() + 2 * 3600)

    def one(fn):
        prompt, pb = build_lite_prompt(fn, pool[fn], vblock)
        t0 = time.time()
        try:
            r = ai.chat(prompt)
        except Exception as e:                              # noqa: BLE001
            return {"fn": fn, "error": str(e)[:160]}
        tags, gap, oov, err = parse_out(r.get("content") or "", vset)
        return {"fn": fn, "tags": tags, "gap": gap, "out_of_vocab": oov, "err": err,
                "secs": round(time.time() - t0, 1), "prompt_bytes": pb}

    res = []
    fns = list(base)
    with ThreadPoolExecutor(max_workers=3) as ex:
        futs = [ex.submit(one, fn) for fn in fns]
        done = 0
        for f in as_completed(futs):
            res.append(f.result())
            done += 1
            if done % 20 == 0:
                print(f"进度 {done}/{len(fns)}", flush=True)

    pairs = []
    for r in res:
        if r.get("tags") is None:
            continue
        full = base[r["fn"]]
        A, B = set(full["tags"]), set(r["tags"])
        jac = 1.0 if not A and not B else len(A & B) / max(1, len(A | B))
        pairs.append({"fn": r["fn"], "stratum": full["stratum"], "full": sorted(A),
                      "lite": sorted(B), "same": A == B, "jac": round(jac, 3),
                      "full_bytes": full.get("prompt_bytes"), "lite_bytes": r.get("prompt_bytes"),
                      "gap": r.get("gap"), "oov": r.get("out_of_vocab"), "err": r.get("err")})

    n = len(pairs)
    exact = sum(1 for p in pairs if p["same"])
    mean_j = sum(p["jac"] for p in pairs) / max(1, n)
    full_ne = sum(1 for p in pairs if p["full"])
    lite_ne = sum(1 for p in pairs if p["lite"])
    fb = sum(p["full_bytes"] or 0 for p in pairs) / max(1, n)
    lb = sum(p["lite_bytes"] or 0 for p in pairs) / max(1, n)
    oov = sum(len(p["oov"]) for p in pairs)
    err = sum(1 for r in res if r.get("tags") is None)
    out = {"ran_at": time.strftime("%Y-%m-%d %H:%M"), "model": ai.model,
           "n": n, "exact": exact, "exact_rate": round(exact / max(1, n), 3),
           "mean_jaccard": round(mean_j, 3),
           "full_nonempty": full_ne, "lite_nonempty": lite_ne,
           "full_bytes_avg": round(fb), "lite_bytes_avg": round(lb),
           "saved_bytes_avg": round(fb - lb),
           "out_of_vocab": oov, "parse_err": err, "pairs": pairs}
    (OUT / "app_lite_ab.json").write_text(json.dumps(out, ensure_ascii=False, indent=1),
                                          encoding="utf-8")
    print(f"\n=== A/B 结果（{n} 条）===")
    print(f"完全一致 {exact}/{n} = {exact/max(1,n):.0%} · 平均 Jaccard {mean_j:.3f}")
    print(f"非空：full {full_ne} vs lite {lite_ne}")
    print(f"输入：full {fb:.0f}B → lite {lb:.0f}B（省 {fb-lb:.0f}B / {(fb-lb)/max(1,fb):.0%}）")
    print(f"词表外 {oov} · 解析失败 {err}")
    print(f"报告：{OUT / 'app_lite_ab.json'}")


if __name__ == "__main__":
    main()
