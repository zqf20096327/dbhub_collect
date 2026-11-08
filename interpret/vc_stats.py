# -*- coding: utf-8 -*-
"""domain_tags 验收统计（G4-3 试点 / G4-5 全量共用）。

口径（与工作清单闸门一一对应）：
  拒收率   = rejected / (done+rejected+failed)          ≤5%
  词表外率 = 拒收原因含「词表外」/ total                ≤1%
  证据命中 = 已接受条目里所有 tag 行号都在证据包内 / 已接受   ≥95%
            （validate 本已强制，这里复算一遍防口径漂移）
  非空率   = tags 非空的条目 / 已接受                    ≥45%
另外报：触发命中率（证据包里至少 1 行词表命中）、每仓标签数、abstain 分布、
平均耗时、尝试次数分布。

用法：
  python interpret/vc_stats.py                 # 全量库存
  python interpret/vc_stats.py --limit 100     # 只看最近 100 个仓（按 state 记录顺序）
  python interpret/vc_stats.py --json out.json
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for _d in (ROOT, ROOT / "lib", ROOT / "config", ROOT / "interpret"):
    sys.path.insert(0, str(_d))

import pool_store                            # noqa: E402
import vocab_control as vc                   # noqa: E402
import run_domain_tags as rd                 # noqa: E402
from interp_layer_store import LayerStore    # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--since", metavar="ISO", help="只看 at ≥ 该时间的条目（分层试点用）")
    ap.add_argument("--json", metavar="PATH")
    ap.add_argument("--gate", action="store_true", help="按 G4-3 闸门判定（非零退出）")
    a = ap.parse_args()

    vocab = vc.load_vocab()
    allowed = vc.all_slugs(vocab)
    st = LayerStore("domain_tags")
    st.load()
    state = st.state()
    pool = rd.load_pool()

    rows = []
    for fn, rec in state.items():
        if a.since and (rec.get("at") or "") < a.since:
            continue
        sha = rec.get("sha")
        rows.append({"fn": fn, "sha": sha, "status": rec.get("status"),
                     "at": rec.get("at"), "entry": st.get(sha)})
    if a.limit:
        rows = rows[-a.limit:]

    stat = Counter()
    strata = {k: Counter() for k in rd.STRATA}
    tag_counts = Counter()
    abstains = Counter()
    bad_evidence = []
    for r in rows:
        sk = rd.stratum_of(int((pool.get(r["fn"]) or {}).get("stars") or 0))
        strata[sk]["total"] += 1
        stat[f"status_{r['status']}"] += 1
        if r["status"] in ("rejected", "failed"):
            strata[sk][r["status"]] += 1
        ent = r["entry"]
        if r["status"] != "done" or not ent:
            continue
        stat["accepted"] += 1
        strata[sk]["accepted"] += 1
        tags = ent.get("tags") or []
        if tags:
            stat["non_empty"] += 1
            strata[sk]["non_empty"] += 1
        else:
            stat["empty"] += 1
            abstains[ent.get("abstain") or "none"] += 1
        tag_counts[len(tags)] += 1
        # 证据复算：标签行号必须在该仓证据包内
        item = pool.get(r["fn"]) or {}
        pack = vc.build_evidence_pack(r["fn"], item, vocab)
        if pack["matched"] and pack["matched"] != "（无）":
            stat["trigger_hit"] += 1
        for t in tags:
            if t.get("slug") not in allowed or t.get("line") not in pack["lines"]:
                bad_evidence.append({"fn": r["fn"], "tag": t})
        if any(k not in allowed for k in ent.keys()):
            pass

    total = stat["accepted"] + stat["status_rejected"] + stat["status_failed"]
    gate = {
        "reject_rate": stat["status_rejected"] / max(total, 1),
        "oov_rate": None,          # 由 runlog 补算（见下）
        "evidence_rate": 1 - len(bad_evidence) / max(sum(tag_counts.values()), 1),
        "nonempty_rate": stat["non_empty"] / max(stat["accepted"], 1),
    }
    # 词表外：从 runlog 的拒收原因里数
    oov = 0
    try:
        for p in st.runlog_dir.glob("*.jsonl"):
            for line in p.read_text(encoding="utf-8").splitlines():
                try:
                    j = json.loads(line)
                except Exception:
                    continue
                if j.get("rejected") and any("词表外" in str(e) for e in (j.get("errs") or [])):
                    oov += 1
    except FileNotFoundError:
        pass
    gate["oov_rate"] = oov / max(total, 1)

    rep = {
        "layer": "domain_tags",
        "vocab": {"ver": vocab.get("vocab_ver"), "n_words": vocab.get("n_words")},
        "total": total,
        "accepted": stat["accepted"],
        "rejected": stat["status_rejected"],
        "failed": stat["status_failed"],
        "non_empty": stat["non_empty"],
        "empty": stat["empty"],
        "trigger_hit": stat["trigger_hit"],
        "trigger_hit_rate": stat["trigger_hit"] / max(stat["accepted"], 1),
        "tags_per_repo": dict(sorted(tag_counts.items())),
        "abstain": dict(abstains),
        "strata": {k: {"total": v["total"], "accepted": v["accepted"],
                       "non_empty": v["non_empty"],
                       "nonempty_rate": v["non_empty"] / max(v["accepted"], 1),
                       "rejected": v["rejected"], "failed": v["failed"]}
                   for k, v in strata.items()},
        "bad_evidence": bad_evidence[:10],
        "gate": gate,
    }
    print(json.dumps(rep, ensure_ascii=False, indent=1))
    if a.json:
        Path(a.json).write_text(json.dumps(rep, ensure_ascii=False, indent=1),
                                encoding="utf-8")
    if a.gate:
        ok = (gate["reject_rate"] <= 0.05 and gate["oov_rate"] <= 0.01
              and gate["evidence_rate"] >= 0.95 and gate["nonempty_rate"] >= 0.45)
        print(f"闸门：拒收 {gate['reject_rate']:.2%}≤5% · 词表外 {gate['oov_rate']:.2%}≤1%"
              f" · 证据 {gate['evidence_rate']:.2%}≥95% · 非空 {gate['nonempty_rate']:.2%}≥45%"
              f" → {'PASS' if ok else 'FAIL'}")
        s = rep["strata"]
        print("分层非空率：" + " · ".join(
            f"{k} {s[k]['nonempty_rate']:.2%}（n={s[k]['accepted']}）"
            for k in rd.STRATA if s[k]["total"]))
        return 0 if ok else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
