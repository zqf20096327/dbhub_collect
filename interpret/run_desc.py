# -*- coding: utf-8 -*-
"""desc 降级层 runner（工作清单 G3-3）：无 README 仓只凭描述做轻判定+轻介绍。

范围（在池 + readme_state=no_readme）：
  - 有描述（1,009）→ AI 轻判定，写入 state/interp/desc/，键 desc::<sha1(fn+desc)[:12]>
  - 空描述（912）→ 不调 AI，进 dead-letter（layer=desc, reason=empty_desc）；
    页面显示"暂无简介"（固定决策）
台账双写：desc 层 state.json（断点）+ interp_state.json（读链 fn→sha→desc 层，
G3 起指向新键；旧 desc::<描述> 键自然退役，G7 删）。

机制与 interpret.py / run_domain_tags.py 同一套（不另写）：
AIClient（glm-5.3-flash，超时重试/429 退避/额度 1113 等窗口）+ LayerStore
（256 分片脏桶 + 断点 + runlog）+ 主线程统一落账。

用法：
  python interpret/run_desc.py --limit 20 --dry-run    # 只看待办与 prompt 体积
  python interpret/run_desc.py --limit 20 --concurrency 4 --max-minutes 30
  python interpret/run_desc.py --fn owner/repo          # 调试单仓
  python interpret/run_desc.py --retry-rejected --limit 100
"""
from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for _d in (ROOT, ROOT / "lib", ROOT / "interpret"):
    sys.path.insert(0, str(_d))

import interpret as itp                      # noqa: E402  AIClient / ISTATE 常量
import pool_store                            # noqa: E402
import desc_control as dc                    # noqa: E402
import dead_letter as dl                     # noqa: E402
from interp_keys import desc_key             # noqa: E402
from interp_layer_store import LayerStore    # noqa: E402
from gh import atomic_write_json             # noqa: E402

log = logging.getLogger("desc")
STATE = ROOT / "state"
ISTATE = STATE / "interp_state.json"


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


def load_todo(pool: dict[str, dict], desc_store) -> tuple[list, list, Counter]:
    """返回 (待办 [(fn, key, desc)], 空描述清单, 跳过计数)。"""
    rs = json.loads((STATE / "readme_state.json").read_text(encoding="utf-8"))
    _rb = STATE.parent / "config" / "exclude_repos.txt"
    repo_bl: set = set()
    if _rb.is_file():
        repo_bl = {ln.strip() for ln in _rb.read_text(encoding="utf-8-sig").splitlines()
                   if ln.strip() and not ln.startswith("#")}
    skip = Counter()
    todo: list[tuple[str, str, str]] = []
    empties: list[tuple[str, str]] = []
    for fn, rec in (rs.get("items") or {}).items():
        if fn not in pool:
            continue                        # 池外不烧（G7 前旧目录不动）
        if fn in repo_bl:
            skip["repo_blacklist"] += 1
            continue
        if rec.get("status") != "no_readme":
            continue
        desc = (pool[fn].get("description") or "").strip()
        if not desc:
            empties.append((fn, "empty_desc"))
            continue
        key = desc_key(fn, desc)
        if key in desc_store:
            skip["already"] += 1
            continue
        todo.append((fn, key, desc))
    todo.sort(key=lambda x: x[0])
    return todo, empties, skip


def ask(client: itp.AIClient, prompt: str, retries: int = 1) -> tuple[dict | None, list[str], int]:
    """一次调用 + 最多 retries 次带原因的纠正重试（同 run_domain_tags.ask 口径）。"""
    r1 = client.chat(prompt)
    tries = r1.get("tries", 1)
    res = dc.validate(r1["content"])
    if res["ok"]:
        return res, [], tries
    if not retries:
        return None, res["violations"], tries
    hint = ("\n\n【上次输出被拒：" + "；".join(res["violations"][:4])
            + "。请严格按 schema 重新输出，只输出 JSON。】")
    r2 = client.chat(prompt + hint)
    tries += r2.get("tries", 1)
    res2 = dc.validate(r2["content"])
    return (res2, [], tries) if res2["ok"] else (None, res2["violations"], tries)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="最多调用多少条（0=不限）")
    ap.add_argument("--concurrency", type=int, default=4)
    ap.add_argument("--max-minutes", type=int, default=60)
    ap.add_argument("--fn", help="只处理某个仓（调试）")
    ap.add_argument("--dry-run", action="store_true", help="只看待办与 prompt，不调用")
    ap.add_argument("--retry-rejected", action="store_true")
    ap.add_argument("--no-dead-letter-empty", dest="dead_letter_empty",
                    action="store_false", default=True,
                    help="空描述仓不进 dead-letter（默认进；只补 AI 项时用）")
    a = ap.parse_args()

    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)-5s %(name)s | %(message)s",
                        datefmt="%H:%M:%S")
    store = LayerStore("desc")
    store.load()
    rejected_keys = {v.get("sha") for v in store.state().values()
                     if v.get("status") == "rejected"}
    pool = load_pool()
    todo, empties, skip = load_todo(pool, store)
    if a.fn:
        todo = [t for t in todo if t[0] == a.fn]
    if not a.retry_rejected:
        n_rej = sum(1 for _, k, _ in todo if k in rejected_keys)
        if n_rej:
            todo = [t for _, k, _ in todo if k not in rejected_keys]
            skip["rejected_same_key"] = n_rej
    if a.limit:
        todo = todo[:a.limit]

    # G3-1 验收口径：同键去重后条数不变（fn 参与哈希，碰撞在构造上不可能）
    keys = [k for _, k, _ in todo]
    chk_col = len(set(keys)) == len(keys)
    log.info("待办 %d 条（键零碰撞：%s）· 空描述 %d · 跳过 %s · 层库存 %d",
             len(todo), "是" if chk_col else "否！", len(empties),
             " / ".join(f"{k} {v}" for k, v in skip.most_common()) or "无",
             len(store.items))

    if a.dry_run:
        for fn, key, desc in todo[:10]:
            pr = dc.build_prompt(fn, pool[fn])
            log.info("  %-45s %s ← %.40s · prompt %dB", fn, key, desc, pr["bytes"])
        avg = sum(dc.build_prompt(fn, pool[fn])["bytes"] for fn, _, _ in todo[:50]) \
            / max(min(len(todo), 50), 1)
        log.info("dry-run：%d 条 · prompt 均值 %.0fB · 空描述 %d 条待进 dead-letter",
                 len(todo), avg, len(empties))
        return 0 if chk_col else 1

    # 空描述 → dead-letter（固定决策：新代不生成介绍，页面显示"暂无简介"）
    if a.dead_letter_empty and empties:
        d = dl.load()
        n0 = len(d["items"])
        for fn, reason in empties:
            d["items"][dl.key(fn, "desc")] = {"fn": fn, "layer": "desc",
                                              "reason": reason,
                                              "detail": "无 README 且描述为空：新代不生成介绍",
                                              "at": _now()}
        dl.save(d)
        log.info("空描述 %d 条进 dead-letter（%d → %d）", len(empties), n0, len(d["items"]))

    # interp_state 读链更新：fn → 新 desc 键（读层靠它定位 desc 层条目）
    istate = json.loads(ISTATE.read_text(encoding="utf-8")) if ISTATE.is_file() \
        else {"items": {}}
    n_istate = 0

    client = itp.AIClient(deadline=time.time() + a.max_minutes * 60)
    stats = Counter()
    dead: list[dict] = []
    t0 = time.time()

    def job(item: tuple[str, str, str]) -> dict:
        fn, key, _ = item
        pr = dc.build_prompt(fn, pool[fn])
        t0w = time.time()
        try:
            res, errs, tries = ask(client, pr["prompt"])
        except Exception as e:                       # 单条失败不拖垮整窗
            return {"fn": fn, "key": key, "failed": True, "err": str(e)[:200],
                    "secs": round(time.time() - t0w, 1)}
        if res is None:
            return {"fn": fn, "key": key, "rejected": True, "errs": errs,
                    "tries": tries, "secs": round(time.time() - t0w, 1)}
        return {"fn": fn, "key": key, "ok": True,
                "classification": res["classification"], "identity": res["identity"],
                "tries": tries, "secs": round(time.time() - t0w, 1)}

    def apply(r: dict) -> None:
        nonlocal n_istate
        fn, key = r["fn"], r["key"]
        if r.get("ok"):
            store.put(key, {"classification": r["classification"],
                            "identity": r["identity"], "source": "desc",
                            "confidence": "low",
                            "generated_at": _now(),
                            "prompt_ver": dc.DESC_PROMPT_VER, "model": client.model})
            store.mark(fn, key, "done")
            istate["items"][fn] = {"sha": key, "status": "done", "source": "desc"}
            n_istate += 1
            stats["ok"] += 1
        elif r.get("rejected"):
            store.mark(fn, key, "rejected", detail="；".join(r["errs"])[:200])
            istate["items"][fn] = {"sha": key, "status": "rejected"}
            dead.append({"fn": fn, "sha": key, "reason": "rejected",
                         "detail": "；".join(r["errs"])[:300]})
            stats["rejected"] += 1
        else:
            store.mark(fn, key, "failed", detail=(r.get("err") or "")[:200])
            istate["items"][fn] = {"sha": key, "status": "failed"}
            dead.append({"fn": fn, "sha": key, "reason": "failed",
                         "detail": (r.get("err") or "")[:300]})
            stats["failed"] += 1
        store.log({**{k: r.get(k) for k in ("fn", "sha", "ok", "rejected",
                                            "failed", "secs", "errs", "tries")},
                   "sha": key})
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
                store.save_state({"prompt_ver": dc.DESC_PROMPT_VER, "model": client.model})
                atomic_write_json(ISTATE, istate)
            if n % 50 == 0:
                log.info("进度 %d/%d · ok %d · 拒收 %d · 失败 %d · %.1fs/条",
                         n, len(todo), stats["ok"], stats["rejected"],
                         stats["failed"], stats["secs"] / max(n, 1))
            if time.time() > client.deadline - 30:
                log.warning("接近墙钟预算，停止派发（已完成 %d/%d）", n, len(todo))
                for g in futs:
                    g.cancel()
                break

    store.flush()
    store.save_state({"prompt_ver": dc.DESC_PROMPT_VER, "model": client.model,
                      "last_run": _now()})
    atomic_write_json(ISTATE, istate)
    if dead:
        d = dl.load()
        for x in dead:
            d["items"][dl.key(x["fn"], "desc")] = {
                "fn": x["fn"], "layer": "desc", "reason": x["reason"],
                "detail": x["detail"], "sha": x["sha"], "at": _now()}
        dl.save(d)
    n = stats["ok"] + stats["rejected"] + stats["failed"]
    log.info("结束：处理 %d · ok %d · 拒收 %d · 失败 %d · 均 %.1fs/条 · interp_state 更新 %d 条",
             n, stats["ok"], stats["rejected"], stats["failed"],
             stats["secs"] / max(n, 1), n_istate)
    log.info("累计库存 %d 条（state.json %d 仓）", len(store.items), len(store.state()))
    return 0 if stats["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
