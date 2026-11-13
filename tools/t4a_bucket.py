# -*- coding: utf-8 -*-
"""T4a 槽位引擎可判性分桶（纯程序、零网络）——验证"采集加深后引擎能判多少"。

  python tools/t4a_bucket.py                       分桶 + 落快照 state/t4a_buckets.json
  python tools/t4a_bucket.py --diff state/t4a_buckets.before.json   与旧快照逐槽对比

槽位宇宙 = state/adjudication_slots.json 里 --ruled exclude 的 4,281（固定，便于前后可比）。
每槽取引擎 v0.3.0 对该库的票（build_pack+judge），按来源拆成指纹票（dep/image/ci/tree）
与 topic 票，分桶：
  A  指纹 ≥2 票                     程序立案，可直写
  B  topic + 指纹双源               strong 互证，可直写
  C1 指纹单证 <2 票                 below_quorum
  C2 仅 topic 2 票                  single_strong 待复核
  D  零证据                         引擎无该库任何信号
另记该仓证据记录是否仍打满旧上限（_hit_old_caps，=还在等自愈重采）与 caps_v。
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for p in (ROOT, ROOT / "lib", ROOT / "attribution"):
    sys.path.insert(0, str(p))

import adjudicate as adj                                   # noqa: E402
from attribution.api import ENGINE_VERSION, judge          # noqa: E402
from attribution.matcher import build_pack                 # noqa: E402
from evidence.evidence_collect import _hit_old_caps        # noqa: E402

OUT = ROOT / "state" / "t4a_buckets.json"
FP = {"dep", "image", "ci", "tree"}
ORDER = ["A", "B", "C1", "C2", "D"]
LABEL = {"A": "A 指纹≥2票·程序立案可直写", "B": "B topic+指纹双源·strong互证",
         "C1": "C1 指纹单证<2票·below_quorum", "C2": "C2 仅topic 2票·single_strong",
         "D": "D 零证据"}


def bucket_of(fp_votes: float, topic_votes: float) -> str:
    if fp_votes >= 2:
        return "A"
    if fp_votes > 0 and topic_votes > 0:
        return "B"
    if fp_votes > 0:
        return "C1"
    if topic_votes > 0:
        return "C2"
    return "D"


def run() -> dict:
    plan = json.loads((ROOT / "state" / "adjudication_slots.json").read_text(encoding="utf-8"))
    slots = adj.filter_ruled(plan["slots"], "exclude")
    pool = adj.load_pool()
    ev = adj.load_evidence_for({s["fn"] for s in slots})
    out: dict[str, dict] = {}
    bad = 0
    for s in slots:
        rec = ev.get(s["fn"])
        topics = (pool.get(s["fn"]) or {}).get("topics") or []
        try:
            pack = build_pack(s["fn"], rec, {"topics": topics})
        except ValueError:                                  # 缺采集时间：只按 topic 判
            bad += 1
            pack = build_pack(s["fn"], None, {"topics": topics},
                              collected_at="2026-01-01T00:00:00Z")
        e = (judge(pack)["per_db"].get(s["db"]) or {"chain": []})
        fp_v = sum(it["votes"] for it in e["chain"] if it["kind"] in FP)
        tp_v = sum(it["votes"] for it in e["chain"] if it["kind"] == "topic")
        out[f'{s["fn"]}|{s["db"]}'] = {
            "bucket": bucket_of(fp_v, tp_v), "fp_votes": fp_v, "topic_votes": tp_v,
            "fp_kinds": sorted({it["kind"] for it in e["chain"] if it["kind"] in FP}),
            "capped": bool(rec is not None and _hit_old_caps(rec)),
            "caps_v": (rec or {}).get("caps_v", 1) if rec else None,
            "has_rec": rec is not None, "stars": s["stars"]}
    counts = Counter(v["bucket"] for v in out.values())
    capped = Counter(v["bucket"] for v in out.values() if v["capped"])
    return {"generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "engine": ENGINE_VERSION, "n": len(out), "no_collected_at": bad,
            "counts": {b: counts.get(b, 0) for b in ORDER},
            "capped_by_bucket": {b: capped.get(b, 0) for b in ORDER},
            "slots": out}


def show(rep: dict) -> None:
    n = rep["n"]
    print(f"槽 {n} · 引擎 {rep['engine']} · 生成 {rep['generated_at']}（缺采集时间 {rep['no_collected_at']}）")
    for b in ORDER:
        c = rep["counts"][b]
        print(f"  {LABEL[b]:34s} {c:5d} ({c * 100 / n:4.0f}%)  其中仓仍打满旧上限 {rep['capped_by_bucket'][b]}")
    ab = rep["counts"]["A"] + rep["counts"]["B"]
    print(f"  程序现在可判（A+B）: {ab}（{ab * 100 / n:.0f}%）· 仍打满待自愈的槽 {sum(rep['capped_by_bucket'].values())}")


def diff(prev: dict, cur: dict) -> None:
    trans: Counter = Counter()
    moved_up = []
    healed = 0
    for k, c in cur["slots"].items():
        p = prev["slots"].get(k)
        if p is None:
            continue
        if p["capped"] and not c["capped"]:
            healed += 1
        if p["bucket"] != c["bucket"]:
            trans[(p["bucket"], c["bucket"])] += 1
            if c["bucket"] in ("A", "B") and p["bucket"] not in ("A", "B"):
                moved_up.append((c["stars"], k, p["bucket"], c["bucket"], c["fp_kinds"]))
    print(f"\n=== 对比 {prev['generated_at']} → {cur['generated_at']} ===")
    print(f"槽所在仓本窗治愈（打满→已重采）: {healed}")
    pa, ca = (r["counts"]["A"] + r["counts"]["B"] for r in (prev, cur))
    print(f"程序可判 A+B: {pa} → {ca}（{ca - pa:+d}）")
    if trans:
        print("桶迁移:", " ".join(f"{a}→{b}={n}" for (a, b), n in sorted(trans.items(), key=lambda kv: -kv[1])))
    for stars, k, a, b, kinds in sorted(moved_up, reverse=True)[:15]:
        print(f"  ↑ {stars:>7,} {k:44s} {a}→{b} 指纹 {'+'.join(kinds)}")
    if len(moved_up) > 15:
        print(f"  … 共 {len(moved_up)} 槽升入 A/B")


def main() -> int:
    ap = argparse.ArgumentParser(description="T4a 槽位引擎可判性分桶（零网络）")
    ap.add_argument("--diff", default=None, help="旧快照路径：逐槽对比")
    ap.add_argument("--out", default=str(OUT), help="快照落盘路径")
    args = ap.parse_args()
    rep = run()
    show(rep)
    if args.diff:
        diff(json.loads(Path(args.diff).read_text(encoding="utf-8")), rep)
    Path(args.out).write_text(json.dumps(rep, ensure_ascii=False, indent=1),
                              encoding="utf-8", newline="\n")
    print(f"快照 → {Path(args.out).name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
