# -*- coding: utf-8 -*-
"""domain_tags 影子运行（patch 模式，一次性工具）。

设计要点（与生产 v4 的关系）：
- 不重烧分类：读旧 sha#v4 缓存条目的 cat_primary/persona/eco/ai_kind 作为锚点，只追烧 domain_tags；
- 不写 interp_cache / interp_state：只产 state/shadow/ 下报告；
- 词表外 slug 不拒收（生产是拒收计数）：影子要收集"模型想输出但词表没有"的缺口信号；
- 额外 gap 字段：词表完全不贴切时用一句话描述核心领域，用于观察覆盖缺口（不参与 consistency）。

抽样 500 条按 star 分层（head≥1000 / mid 100-999 / tail<100），前 50 条双跑测一致率。
"""
import argparse
import json
import os
import random
import sys
import time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for _d in (ROOT, ROOT / "lib", ROOT / "config", ROOT / "interpret"):
    sys.path.insert(0, str(_d))

import interpret as itp                                    # noqa: E402
import pool_store                                          # noqa: E402
import _shadow_vocab as sv                                 # noqa: E402
from interp_read import InterpReader                       # noqa: E402

OUT = ROOT / "state" / "shadow"
OUT.mkdir(parents=True, exist_ok=True)

# §5 cat↔域 xcheck 映射（软校验：预警不拒收；应用/其他/横切域豁免）
CAT_DOMAIN = {"备份": ["backup-restore"], "监控": ["observability"], "高可用": ["ha"],
              "迁移": ["migration", "data-pipeline"], "连接/代理": ["connectivity"],
              "管理": ["admin-client"], "平台": ["platform"],
              "开发库": ["orm-query", "connectivity"], "安全/审计": ["security"],
              "测试/质量": ["testing"], "建模/设计": ["modeling"], "内核/引擎": ["engine"]}

TMPL = """你是数据库开源生态的编目员。本任务只做一件事：为一个仓库选择 domain_tags（领域标签）。
{contract}
【该仓已有判定——已定稿，无需复核，仅作一致性锚点】
cat_primary: {cat}
persona: {persona} ／ eco: {eco} ／ ai_kind: {ai_kind}

输出一个 JSON 对象（只输出 JSON，不要其他文字）：
{{
 "domain_tags": ["0-3 个词表 slug（只能取下方词表）；只标 README 有明确依据的，宁缺勿编；"
                 "无任何贴切词时输出空数组 []"],
 "gap": "（可选，≤12字）若词表完全不贴切，用一个词描述本仓最核心的领域；贴切则省略本键"
}}

可用词表（domain_tags 只能取下列 slug）：
{vocab}

仓库：{fn}
描述：{desc}
主题标签：{topics}
--- README 开始（「L行号|原文」编号，可见行号范围 {line_range}）---
{readme}
--- README 结束 ---"""


LITE_TMPL = """你是数据库开源生态的编目员。本任务只做一件事：判断这个项目**用到/涉及**哪些数据库领域能力，选 0-3 个词表标签。
（这是应用类项目：它本身不是数据库工具，标签描述它依赖了什么数据库能力。例：用 pgvector 做检索 → vector-search）

输出一个 JSON 对象（只输出 JSON）：
{{"domain_tags": ["0-3 个词表 slug，只能取下方词表；无法判断输出 []"]}}

可用词表：
{vocab}

仓库：{fn}
描述：{desc}
主题标签：{topics}"""


def build_lite_prompt(fn, it, vblock):
    """应用类短提示：不投 README 全文（省 ~90% 输入），只给描述+topics。"""
    prompt = LITE_TMPL.format(
        vocab=vblock, fn=fn, desc=(it.get("description") or "")[:300],
        topics=",".join((it.get("topics") or [])[:12]))
    return prompt, len(prompt.encode())


def route_of(entry, app_mode="lite", unclear_mode="skip"):
    """eco 路由：unclear 证据不足→跳过；app→短提示；tool→全量提示。"""
    eco = ((entry.get("classification") or {}).get("eco")) or "None"
    if eco == "unclear" and unclear_mode == "skip":
        return "skip_unclear"
    if eco == "app" and app_mode in ("lite", "skip"):
        return "skip_app" if app_mode == "skip" else "lite_app"
    return "full"


def build_patch_prompt(fn, it, entry, vblock):
    path = ROOT / "data" / "readmes" / (fn.replace("/", "__") + ".md")
    raw = path.read_text(encoding="utf-8", errors="ignore") if path.is_file() else ""
    text = itp.clean_readme(raw)
    body, numbered, cum = [], {}, 0
    for no, ln in itp.number_lines(text):
        if cum > 10000:
            break
        body.append(f"L{no}|{ln}")
        numbered[no] = ln
        cum += len(ln) + 1
    cls, sig = entry.get("classification") or {}, entry.get("signals") or {}
    prompt = TMPL.format(
        contract=itp.NEUTRALITY_CONTRACT, cat=cls.get("cat_primary"),
        persona=",".join(cls.get("persona") or []), eco=cls.get("eco"),
        ai_kind=cls.get("ai_kind"), vocab=vblock, fn=fn,
        desc=(it.get("description") or "")[:300],
        topics=",".join((it.get("topics") or [])[:12]),
        readme="\n".join(body) or "（无 README 正文）",
        line_range=f"L1–L{max(numbered)}" if numbered else "无")
    return prompt, len(prompt.encode())


def parse_out(raw, vset):
    """→ (tags, gap, out_of_vocab, err)。影子口径：格式错才算 err，词表外只记录。"""
    obj = itp.extract_json(raw)
    if not isinstance(obj, dict):
        return None, None, [], "非法 JSON"
    tags = obj.get("domain_tags")
    if not isinstance(tags, list):
        return None, None, [], "domain_tags 非数组"
    tags = [str(t).strip() for t in tags if str(t).strip()]
    if len(tags) > 3:
        return None, None, [], f"domain_tags 超 3 个（{len(tags)}）"
    out = [t for t in tags if t not in vset]
    gap = (obj.get("gap") or "").strip() or None
    return [t for t in tags if t in vset], gap, out, None


def load_v4_index():
    """直读 sha#v4 条目（fn → 判定卷对象）。
    不用 InterpReader._load_interp：它按 fn 取"最新"，文本卷条目会顶掉判定卷条目
    （实测 1,318 个头部仓只剩 38 个读到 classification，见 1107 诊断）。"""
    idx = {}
    for p in sorted((ROOT / "state/interp_cache_shards").glob("*.json")):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
        for k, v in data.items():
            if not (k.endswith("#v4") and isinstance(v, dict)):
                continue
            if (v.get("classification") or {}).get("cat_primary"):
                idx[v.get("fn") or ""] = v
    return idx


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=500)
    ap.add_argument("--head", type=int, default=150)
    ap.add_argument("--mid", type=int, default=200)
    ap.add_argument("--tail", type=int, default=150)
    ap.add_argument("--concurrency", type=int, default=3)
    ap.add_argument("--double", type=int, default=50, help="双跑条数（一致率）")
    ap.add_argument("--app-mode", choices=["lite", "skip", "full"], default="full",
                    help="eco=app 路由：full=全量提示（1107 用户裁定，lite 实测多标 4 倍已否决）")
    ap.add_argument("--unclear-mode", choices=["skip", "full"], default="skip",
                    help="eco=unclear 路由：skip=不调模型（推荐，实测 94%% 空）")
    ap.add_argument("--only-cat", default=None, help="只跑指定 cat_primary（如 平台）")
    ap.add_argument("--seed", type=int, default=1107)
    args = ap.parse_args()

    vocab = sv.parse_vocab()
    vblock = sv.vocab_block(vocab)
    vset = {w["slug"] for d in vocab["domains"] for w in d["words"]}
    word2dom = {w["slug"]: d["domain"] for d in vocab["domains"] for w in d["words"]}

    pool = {}
    for p in ("data/live/pool.ndjson", "data/live/pool_cn.ndjson", "data/live/pool_intl.ndjson"):
        for r in pool_store.read_any(ROOT / p):
            pool[r["full_name"]] = r
    rd = json.loads((ROOT / "state/readme_state.json").read_text(encoding="utf-8"))["items"]
    by_fn = load_v4_index()
    print(f"v4 判定条目 {len(by_fn)} 条", flush=True)

    # 候选：有 readme + 有旧 sha#v4 条目（patch 前提）
    strata = {"head": [], "mid": [], "tail": []}
    for fn, rec in rd.items():
        if rec.get("status") != "done" or fn not in pool:
            continue
        e = by_fn.get(fn)
        if not e or not (e.get("classification") or {}).get("cat_primary"):
            continue
        if args.only_cat and (e["classification"].get("cat_primary") != args.only_cat):
            continue
        if not (ROOT / "data/readmes" / (fn.replace("/", "__") + ".md")).is_file():
            continue
        st = pool[fn].get("stars") or 0
        strata["head" if st >= 1000 else ("mid" if st >= 100 else "tail")].append(fn)

    want = {"head": args.head, "mid": args.mid, "tail": args.tail}
    rnd = random.Random(args.seed)
    sample = []
    for k, lst in strata.items():
        lst = sorted(lst)
        rnd.shuffle(lst)
        sample += [(fn, k) for fn in lst[:want[k]]]
    print(f"候选池 head/mid/tail = {len(strata['head'])}/{len(strata['mid'])}/{len(strata['tail'])}"
          f" · 抽样 {len(sample)}", flush=True)

    ai = itp.AIClient(deadline=time.time() + 3 * 3600)

    def one(job, run_no=1):
        fn, strat = job
        it, entry = pool[fn], by_fn[fn]
        route = route_of(entry, args.app_mode, args.unclear_mode)
        if route in ("skip_unclear", "skip_app"):        # 程序置空，不调模型
            return {"fn": fn, "stratum": strat, "run": run_no, "route": route,
                    "stars": it.get("stars"),
                    "cat": (entry.get("classification") or {}).get("cat_primary"),
                    "tags": [], "gap": None, "out_of_vocab": [], "err": None,
                    "xcheck_warn": None, "secs": 0.0, "prompt_bytes": 0}
        prompt, pb = (build_lite_prompt(fn, it, vblock) if route == "lite_app"
                      else build_patch_prompt(fn, it, entry, vblock))
        t0 = time.time()
        try:
            r = ai.chat(prompt)
        except Exception as e:                                  # noqa: BLE001
            return {"fn": fn, "stratum": strat, "run": run_no, "route": route,
                    "error": str(e)[:160]}
        tags, gap, oov, err = parse_out(r.get("content") or "", vset)
        cls = entry.get("classification") or {}
        cat = cls.get("cat_primary")
        warn = None
        if tags is not None and cat in CAT_DOMAIN:
            doms = {word2dom.get(t) for t in tags}
            if not (doms & set(CAT_DOMAIN[cat])):
                warn = f"cat={cat} 而 domain_tags 无 {CAT_DOMAIN[cat]} 域词"
        return {"fn": fn, "stratum": strat, "run": run_no, "route": route,
                "stars": it.get("stars"),
                "cat": cat, "tags": tags, "gap": gap, "out_of_vocab": oov,
                "err": err, "xcheck_warn": warn, "secs": round(time.time() - t0, 1),
                "prompt_bytes": pb}

    jobs = sample + sample[:args.double]
    results = []
    with ThreadPoolExecutor(max_workers=args.concurrency) as ex:
        futs = [ex.submit(one, j, 1 if i < len(sample) else 2) for i, j in enumerate(jobs)]
        done = 0
        for f in as_completed(futs):
            results.append(f.result())
            done += 1
            if done % 20 == 0:
                ok = sum(1 for r in results if r.get("tags") is not None)
                print(f"进度 {done}/{len(jobs)} · 有效 {ok}", flush=True)

    first = [r for r in results if r["run"] == 1 and r.get("tags") is not None]
    second = {r["fn"]: r for r in results if r["run"] == 2 and r.get("tags") is not None}

    # ---- 路由账：省了多少调用/输入 ----
    route_stat = defaultdict(lambda: {"n": 0, "api": 0, "bytes": 0, "nonempty": 0})
    for r in [x for x in results if x["run"] == 1]:
        g = route_stat[r.get("route") or "?"]
        g["n"] += 1
        g["api"] += 0 if (r.get("route") or "").startswith("skip") else 1
        g["bytes"] += r.get("prompt_bytes") or 0
        g["nonempty"] += 1 if r.get("tags") else 0

    # ---- 统计 ----
    by_str = defaultdict(lambda: {"n": 0, "empty": 0, "warn": 0, "err": 0})
    word_cnt = Counter()
    gap_cnt = Counter()
    oov = Counter()
    for r in first:
        s = by_str[r["stratum"]]
        s["n"] += 1
        s["empty"] += 1 if not r["tags"] else 0
        s["warn"] += 1 if r["xcheck_warn"] else 0
        word_cnt.update(r["tags"])
        if r["gap"]:
            gap_cnt[r["gap"]] += 1
        oov.update(r["out_of_vocab"])
    for r in results:
        if r["run"] == 1 and r.get("err"):
            by_str[r["stratum"]]["err"] += 1

    cons = []
    for r in first:
        b = second.get(r["fn"])
        if b:
            A, B = set(r["tags"]), set(b["tags"])
            # 空-空 记 1.0：两边都判定"无贴切词"就是一致，Jaccard 分母不能拿 max(1,0) 充数
            jac = 1.0 if not A and not B else len(A & B) / len(A | B)
            cons.append((A == B, jac))
            if os.environ.get("DT_DEBUG"):
                print(f"DBG {r['fn']} run{r['run']}#{id(r)}={sorted(A)} "
                      f"vs run{b['run']}#{id(b)}={sorted(B)} eq={A == B}", flush=True)

    rep = {
        "ran_at": time.strftime("%Y-%m-%d %H:%M"), "model": ai.model,
        "n_sample": len(sample), "n_double": args.double,
        "vocab": {"n_words": vocab["n_words"], "block_bytes": len(vblock.encode())},
        "routes": dict(route_stat),
        "per_stratum": dict(by_str),
        "word_counts": word_cnt.most_common(),
        "gap_proposals": gap_cnt.most_common(40),
        "out_of_vocab": oov.most_common(40),
        "consistency": {"n": len(cons),
                        "exact": sum(1 for e, _ in cons if e),   # 1107 修：原式丢 if e，恒等于 n
                        "exact_rate": round(sum(1 for e, _ in cons if e) / len(cons), 3) if cons else None,
                        "mean_jaccard": round(sum(j for _, j in cons) / len(cons), 3) if cons else None},
        "prompt_bytes_avg": round(sum(r.get("prompt_bytes") or 0 for r in first) / max(1, len(first))),
        "secs_avg": round(sum(r.get("secs") or 0 for r in first) / max(1, len(first)), 2),
        "items": results,
    }
    p = OUT / f"domain_tags_shadow_{len(sample)}.json"
    p.write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")

    # 自校验：从落盘数据复算一致率，必须与内存值一致（1107 首次跑出过 50/50 vs 38/50 的分裂）
    disk = json.loads(p.read_text(encoding="utf-8"))["items"]
    f1 = [r for r in disk if r["run"] == 1 and r.get("tags") is not None]
    f2 = {r["fn"]: r for r in disk if r["run"] == 2 and r.get("tags") is not None}
    re_exact = sum(1 for r in f1 if r["fn"] in f2 and set(r["tags"]) == set(f2[r["fn"]]["tags"]))
    assert re_exact == rep["consistency"]["exact"], \
        f"一致率自校验失败：内存 {rep['consistency']['exact']} vs 落盘 {re_exact}"

    # ---- 控制台摘要 ----
    print("\n=== 路由账（eco 分层）===")
    for k, g in sorted(route_stat.items(), key=lambda x: -x[1]["n"]):
        print(f"{k}: n={g['n']} 调模型={g['api']} 非空={g['nonempty']} "
              f"均输入={g['bytes']/max(1,g['n']):.0f}B")
    print("\n=== 分层结果 ===")
    for k, s in by_str.items():
        cov = 1 - s["empty"] / max(1, s["n"])
        print(f"{k}: n={s['n']} 空标签={s['empty']} 覆盖率={cov:.1%} xcheck预警={s['warn']} 格式错={s['err']}")
    print("\n=== 词频 Top15 ===", word_cnt.most_common(15))
    print("=== 词表外提案 ===", oov.most_common(15) or "无")
    print("=== gap 提案 Top10 ===", gap_cnt.most_common(10) or "无")
    print("=== 一致率 ===", rep["consistency"])
    print(f"\n报告：{p}")


if __name__ == "__main__":
    main()
