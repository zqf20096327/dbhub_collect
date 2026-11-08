# -*- coding: utf-8 -*-
"""一次性把旧单目录缓存按层拆进独立目录（工作清单 G1-6）。

前置：v4t 守夜跑完（它正在写旧目录，中途搬会互相覆盖）。
旧布局：state/interp_cache_shards/<xx>.json，键带后缀（sha#v4 / sha#txt4.0 / sha#vc1.0）。
新布局：state/interp/<layer>/shards/<xx>.json，键=裸 sha（层由目录表达）。

只搬新代四层：
  judge       ← *#v4
  text        ← *#txt4.0
  domain_tags ← *#vc1.0
  desc        ← desc::<12位摘要>（G3 起产生）
不搬：裸 sha（v3 旧代）、desc::<描述>[#v4]（旧 desc），它们随 G7 删除。

每层同时生成 state.json 断点台账（judge 复制现有 interp_state，其余按条目存在性推导）。
搬迁后做逐键对拍：新布局拼接结果与旧条目载荷逐字段一致。

用法：
  python tools/split_layers.py --dry-run    # 只统计与对拍（默认，不写盘）
  python tools/split_layers.py --apply      # 实际写盘
  python tools/split_layers.py --verify     # 只对拍已搬结果
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "lib"))
sys.path.insert(0, str(ROOT / "interpret"))

import interp_keys as ik                      # noqa: E402
import interp_store                           # noqa: E402
from interp_layer_store import (LAYERS, LayerStore, join, sanitize)   # noqa: E402

LEDGER = ROOT / "state" / "interp_state.json"
NEW_BASE = ROOT / "state" / "interp"

# 键族 → 新层；None = 不搬（旧代，G7 删）
MOVE = {"judge": "judge", "text": "text", "vocab": "domain_tags", "desc": "desc",
        "legacy": None, "desc_legacy": None, "unknown": None}


def _ledger() -> dict[str, dict]:
    if not LEDGER.is_file():
        return {}
    return (json.loads(LEDGER.read_text(encoding="utf-8")) or {}).get("items") or {}


def plan(old: dict[str, dict]) -> tuple[dict[str, dict], Counter, Counter]:
    """把旧键分到新层。返回 (每层 {key: 旧条目}, 层计数, 不搬原因计数)。"""
    per: dict[str, dict] = {l: {} for l in LAYERS}
    skip = Counter()
    for key, obj in old.items():
        layer, sha = ik.parse_key(key)
        dst = MOVE.get(layer)
        if dst is None:
            skip[layer] += 1
            continue
        if dst == "desc" and not key.startswith("desc::"):
            skip["desc_key_shape"] += 1
            continue
        per[dst][sha] = obj
    return per, Counter({l: len(v) for l, v in per.items()}), skip


def build_states(per: dict[str, dict]) -> dict[str, dict]:
    """每层断点台账：fn → {sha,status}。judge 用现有台账，其余按条目存在性推导。"""
    led = _ledger()
    states: dict[str, dict] = {l: {} for l in LAYERS}
    for fn, rec in led.items():
        sha = (rec or {}).get("sha")
        if not sha:
            continue
        status = (rec or {}).get("status") or "done"
        if sha in per["judge"]:
            states["judge"][fn] = {"sha": sha, "status": status}
        if sha in per["text"]:
            states["text"][fn] = {"sha": sha, "status": "done"}
        if sha in per["domain_tags"]:
            states["domain_tags"][fn] = {"sha": sha, "status": "done"}
        if sha.startswith("desc::") and sha in per["desc"]:
            states["desc"][fn] = {"sha": sha, "status": status}
    return states


def write(per: dict[str, dict], states: dict[str, dict]) -> dict:
    out = {}
    for layer in LAYERS:
        exists = (NEW_BASE / layer / "shards").is_dir()             and any((NEW_BASE / layer / "shards").glob("*.json"))
        if exists and not per[layer]:
            out[layer] = {"skipped": "已有数据且本次无搬迁项，保留"}
            continue
        st = LayerStore(layer)
        st.load()
        for sha, obj in per[layer].items():
            st.put(sha, obj)
        n = st.flush()
        for fn, rec in states[layer].items():
            st.mark(fn, rec["sha"], rec.get("status") or "done")
        st.save_state({"prompt_ver": {"judge": "4.0", "text": "4.0",
                                      "domain_tags": "vc1.0", "desc": "3.0"}[layer],
                       "migrated_from": "state/interp_cache_shards"})
        out[layer] = {"entries": len(st.items), "buckets": n,
                      "state": len(states[layer]), "dropped": dict(st.dropped)}
    return out


def verify(per: dict[str, dict]) -> tuple[int, list]:
    """逐键对拍：新布局条目 == 旧条目解耦后的载荷（字段级）。"""
    bad, samples = 0, []
    stores = {l: LayerStore(l) for l in LAYERS}
    for l in LAYERS:
        stores[l].load()
    for layer in LAYERS:
        for sha, old in per[layer].items():
            want, _ = sanitize(layer, old)
            got = stores[layer].get(sha)
            if got != want:
                bad += 1
                if len(samples) < 5:
                    samples.append({"layer": layer, "sha": sha[:24],
                                    "want": sorted(want), "got": sorted(got or {})})
    return bad, samples


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    old = interp_store.load_cache()
    per, counts, skip = plan(old)
    states = build_states(per)
    print("旧缓存 " + f"{len(old):,} 条")
    print("分层计划：" + " / ".join(f"{l} {counts[l]:,}" for l in LAYERS))
    print("不搬：" + (" / ".join(f"{k} {v:,}" for k, v in sorted(skip.items())) or "0"))
    print("台账：" + " / ".join(f"{l} {len(states[l]):,}" for l in LAYERS))
    if a.verify:
        bad, samples = verify(per)
        print(f"对拍：{'0 差异' if bad == 0 else f'{bad} 条差异'}"
              + ("" if not bad else " " + json.dumps(samples, ensure_ascii=False)))
        return 0 if bad == 0 else 1
    if not a.apply:
        print("dry-run 结束（未写盘；对拍用 --verify）")
        return 0
    # 只挡"要搬的层已有数据"：domain_tags/desc 可能是独立跑出来的新数据，不能覆盖
    clash = [l for l in ("judge", "text")
             if per[l] and (NEW_BASE / l / "shards").is_dir()
             and any((NEW_BASE / l / "shards").glob("*.json"))]
    if clash:
        print(f"目标层已有数据：{clash}；如需重搬先手动移走（防重复写）")
        return 2
    rep = write(per, states)
    print("已写：" + json.dumps(rep, ensure_ascii=False))
    bad, samples = verify(per)
    print(f"搬迁后对拍：{'0 差异' if bad == 0 else f'{bad} 条差异'}")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
