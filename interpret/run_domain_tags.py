# -*- coding: utf-8 -*-
"""domain_tags 独立 runner（工作清单 G4-2）。

为什么能独立跑：本层只依赖 README + 池元信息 + 词表，不读判定卷/文本卷的输出
（是否应用、是否数据库工具由判定卷负责，本层只认证据）。写入自己的
state/interp/domain_tags/，与 v4/v4t 的旧目录零冲突，可并行。

机制与 interpret.py 同一套（不另写）：
  - AIClient：超时重试 / 429 退避 / 额度 1113 等窗口（import interpret，不改它）
  - LayerStore：256 分片脏桶落盘 + state.json 断点 + runlog
  - 主线程统一落账：worker 只返回结果，避免并发写 dict

用法：
  python interpret/run_domain_tags.py --limit 20 --dry-run     # 只拼 prompt 看体积
  python interpret/run_domain_tags.py --limit 300 --concurrency 4 --max-minutes 100
  python interpret/run_domain_tags.py --fn owner/repo --dry-run
  python interpret/run_domain_tags.py --retry-rejected --limit 100
"""
from __future__ import annotations

import argparse
import json
import logging
import random
import sys
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for _d in (ROOT, ROOT / "lib", ROOT / "config", ROOT / "interpret"):
    sys.path.insert(0, str(_d))

import interpret as itp                      # noqa: E402  AIClient / extract_json / clean_readme
import pool_store                            # noqa: E402
import vocab_control as vc                   # noqa: E402
import dead_letter as dl                     # noqa: E402
from interp_layer_store import LayerStore    # noqa: E402

log = logging.getLogger("domain_tags")
STATE = ROOT / "state"
README_DIR = ROOT / "data" / "readmes"


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_pool() -> dict[str, dict]:
    out: dict[str, dict] = {}
    for name in ("pool", "pool_intl", "pool_cn"):
        p = pool_store.live_path(name)
        if not p.is_file():
            continue
        for rec in pool_store.read_ndjson(p):
            fn = rec.get("full_name")
            if fn:
                out[fn] = rec
    return out


def load_pairs(pool: dict[str, dict] | None = None) -> tuple[list[tuple[str, str]], Counter]:
    """readme_state 里 done/oversized 且在池的 (fn, sha)；返回待办与跳过原因。"""
    rs = json.loads((STATE / "readme_state.json").read_text(encoding="utf-8"))
    pool = pool if pool is not None else load_pool()
    skip = Counter()
    seen_sha: dict[str, str] = {}
    pairs: list[tuple[str, str]] = []
    for fn, rec in (rs.get("items") or {}).items():
        if fn not in pool:
            skip["out_of_pool"] += 1
            continue
        if rec.get("status") not in ("done", "oversized"):
            skip["no_readme"] += 1
            continue
        sha = rec.get("sha")
        if not sha:
            skip["no_sha"] += 1
            continue
        if not (README_DIR / (fn.replace("/", "__") + ".md")).is_file():
            skip["readme_file_missing"] += 1
            continue
        if sha in seen_sha:
            skip["mirror_same_sha"] += 1
            continue
        seen_sha[sha] = fn
        pairs.append((fn, sha))
    return pairs, skip


STRATA = ("head", "mid", "tail")          # head≥1000★ / mid 100–999★ / tail<100★


def stratum_of(stars: int) -> str:
    return "head" if stars >= 1000 else "mid" if stars >= 100 else "tail"


def stratified_sample(pairs: list[tuple[str, str]], pool: dict[str, dict],
                      n: int, seed: int) -> list[tuple[str, str]]:
    """每层各抽 n 条（不足则全取）；固定 seed + 按 fn 排序 → 同一候选集可复现。"""
    groups: dict[str, list[tuple[str, str]]] = {k: [] for k in STRATA}
    for fn, sha in sorted(pairs):
        groups[stratum_of(int((pool.get(fn) or {}).get("stars") or 0))].append((fn, sha))
    rng = random.Random(seed)
    out: list[tuple[str, str]] = []
    for k in STRATA:
        out.extend(rng.sample(groups[k], min(n, len(groups[k]))))
    out.sort()
    return out


def ask(client: itp.AIClient, prompt: str, allowed: set[str], pack: dict,
        retries: int = 1) -> tuple[dict | None, list[str], int]:
    """一次调用 + 最多 retries 次带原因的纠正重试。返回 (结果, 违规, 总尝试次数)。

    tries 含网络层重试（AIClient 内部：超时/429/额度 1113），用于事后核对
    "超时/重试/额度等待"是否真的发生过。
    """
    r1 = client.chat(prompt)
    tries = r1.get("tries", 1)
    res = vc.validate(r1["content"], allowed, pack)
    if res["ok"]:
        return res, [], tries
    if not retries:
        return None, res["violations"] or ["未知拒收"], tries
    hint = ("\n\n【上次输出被拒：" + "；".join(res["violations"][:4])
            + "。请严格按 schema 重新输出，只输出 JSON。】")
    r2 = client.chat(prompt + hint)
    tries += r2.get("tries", 1)
    res2 = vc.validate(r2["content"], allowed, pack)
    return (res2, [], tries) if res2["ok"] else (
        None, res2["violations"] or ["未知拒收"], tries)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="最多调用多少条（0=不限）")
    ap.add_argument("--concurrency", type=int, default=4)
    ap.add_argument("--max-minutes", type=int, default=100)
    ap.add_argument("--fn", help="只处理某个仓（调试）")
    ap.add_argument("--stratum", type=int, default=0, metavar="N",
                    help="分层抽样：head/mid/tail 各 N 条（0=不分层，全量候选）")
    ap.add_argument("--seed", type=int, default=20261107, help="分层抽样种子")
    ap.add_argument("--dry-run", action="store_true", help="只拼 prompt，不调用")
    ap.add_argument("--retry-rejected", action="store_true")
    a = ap.parse_args()

    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)-5s %(name)s | %(message)s",
                        datefmt="%H:%M:%S")
    vocab = vc.load_vocab()
    allowed = vc.all_slugs(vocab)
    store = LayerStore("domain_tags")
    store.load()
    log.info("词表 %s · %d 词 · 已有 %d 条", vocab.get("vocab_ver"),
             vocab.get("n_words"), len(store.items))

    pool = load_pool()
    pairs, skip = load_pairs(pool)
    pairs.sort()
    if a.fn:
        pairs = [p for p in pairs if p[0] == a.fn]
    if a.stratum:
        pairs = stratified_sample(pairs, pool, a.stratum, a.seed)
        cnt = Counter(stratum_of(int((pool.get(fn) or {}).get("stars") or 0))
                      for fn, _ in pairs)
        log.info("分层抽样 %d 条（head %d / mid %d / tail %d，seed=%d）",
                 len(pairs), cnt["head"], cnt["mid"], cnt["tail"], a.seed)
    todo: list[tuple[str, str]] = []
    rejected_sha = {v.get("sha") for v in store.state().values()
                    if v.get("status") == "rejected"}
    for fn, sha in pairs:
        if sha in store.items:
            if store.state().get(fn, {}).get("status") != "done":
                store.mark(fn, sha, "done")   # 补台账，不刷新已完成项的 at
            continue
        if sha in rejected_sha and not a.retry_rejected:
            skip["rejected_same_sha"] += 1
            continue
        todo.append((fn, sha))
    if a.limit:
        todo = todo[:a.limit]
    log.info("待办 %d 条（跳过：%s）", len(todo),
             " / ".join(f"{k} {v:,}" for k, v in skip.most_common()) or "无")

    def job(fn_sha: tuple[str, str]) -> dict:
        fn, sha = fn_sha
        item = pool.get(fn) or {}
        pack = vc.build_evidence_pack(fn, item, vocab)
        pr = vc.build_prompt(fn, item, pack, vocab)
        t0 = time.time()
        if a.dry_run:
            return {"fn": fn, "sha": sha, "dry": True,
                    "bytes": len(pr["prompt"].encode()),
                    "lines": len(pack["lines"]), "matched": pack["matched"].count("L")}
        try:
            res, errs, tries = ask(client, pr["prompt"], allowed, pack)
        except Exception as e:                       # 单条失败不拖垮整窗
            return {"fn": fn, "sha": sha, "failed": True, "err": str(e)[:200],
                    "secs": round(time.time() - t0, 1)}
        if res is None:
            return {"fn": fn, "sha": sha, "rejected": True, "errs": errs,
                    "tries": tries, "secs": round(time.time() - t0, 1)}
        return {"fn": fn, "sha": sha, "ok": True, "tags": res["tags"],
                "abstain": res["abstain"], "gap": res["gap"],
                "warns": res["warnings"], "tries": tries,
                "secs": round(time.time() - t0, 1)}

    if a.dry_run:
        rows = [job(p) for p in todo[: a.limit or 20]]
        for r in rows:
            log.info("  %-45s prompt %5dB · 证据行 %d · 命中行 %d",
                     r["fn"], r["bytes"], r["lines"], r["matched"])
        avg = sum(r["bytes"] for r in rows) / max(len(rows), 1)
        log.info("dry-run：%d 条 · prompt 均值 %.0fB", len(rows), avg)
        return 0

    client = itp.AIClient(deadline=time.time() + a.max_minutes * 60)
    stats = Counter()
    dead: list[dict] = []
    t_start = time.time()

    def apply(r: dict) -> None:
        fn, sha = r["fn"], r["sha"]
        if r.get("ok"):
            store.put(sha, {"tags": r["tags"], "abstain": r["abstain"],
                            "gap": r["gap"], "source": "readme",
                            "generated_at": _now(), "prompt_ver": vc.VOCAB_PROMPT_VER,
                            "model": client.model})
            store.mark(fn, sha, "done")
            stats["ok"] += 1
            stats["tags_nonempty"] += 1 if r["tags"] else 0
            stats["tags"] += len(r["tags"])
        elif r.get("rejected"):
            store.mark(fn, sha, "rejected", detail="；".join(r["errs"])[:200])
            dead.append({"fn": fn, "sha": sha, "reason": "rejected",
                         "detail": "；".join(r["errs"])[:300]})
            stats["rejected"] += 1
        else:
            store.mark(fn, sha, "failed", detail=(r.get("err") or "")[:200])
            dead.append({"fn": fn, "sha": sha, "reason": "failed",
                         "detail": (r.get("err") or "")[:300]})
            stats["failed"] += 1
        store.log({**{k: r.get(k) for k in ("fn", "sha", "ok", "rejected",
                                            "failed", "secs", "errs", "tries")}})
        stats["secs"] += r.get("secs") or 0

    with ThreadPoolExecutor(max_workers=a.concurrency) as ex:
        futs = {ex.submit(job, p): p for p in todo}
        n = 0
        for f in as_completed(futs):
            r = f.result()
            apply(r)
            n += 1
            if n % 20 == 0:
                store.flush()
                store.save_state({"vocab_ver": vocab.get("vocab_ver"),
                                  "prompt_ver": vc.VOCAB_PROMPT_VER,
                                  "model": client.model})
            if n % 50 == 0:
                el = time.time() - t_start
                log.info("进度 %d/%d · ok %d · 拒收 %d · 失败 %d · %.1fs/条",
                         n, len(todo), stats["ok"], stats["rejected"],
                         stats["failed"], stats["secs"] / max(n, 1))
            if time.time() > client.deadline - 30:
                log.warning("接近墙钟预算，停止派发（已完成 %d/%d）", n, len(todo))
                for g in futs:
                    g.cancel()
                break

    store.flush()
    store.save_state({"vocab_ver": vocab.get("vocab_ver"),
                      "prompt_ver": vc.VOCAB_PROMPT_VER,
                      "model": client.model, "last_run": _now()})
    if dead:
        d = dl.load()
        for x in dead:
            d["items"][dl.key(x["fn"], "domain_tags")] = {
                "fn": x["fn"], "layer": "domain_tags", "reason": x["reason"],
                "detail": x["detail"], "sha": x["sha"], "at": _now()}
        dl.save(d)
    n = stats["ok"] + stats["rejected"] + stats["failed"]
    tries = Counter()
    for p in store.runlog_dir.glob("*.jsonl"):
        for line in p.read_text(encoding="utf-8").splitlines():
            try:
                tries[json.loads(line).get("tries") or 1] += 1
            except Exception:
                continue
    log.info("结束：处理 %d · ok %d（非空 %d）· 拒收 %d · 失败 %d · 均 %.1fs/条",
             n, stats["ok"], stats["tags_nonempty"], stats["rejected"],
             stats["failed"], stats["secs"] / max(n, 1))
    log.info("尝试次数分布（含网络重试）：%s",
             " / ".join(f"{k}次×{v}" for k, v in sorted(tries.items())) or "无")
    log.info("累计库存 %d 条（state.json %d 仓）", len(store.items), len(store.state()))
    return 0 if stats["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
