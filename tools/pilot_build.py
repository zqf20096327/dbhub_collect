# -*- coding: utf-8 -*-
"""T3a 试点清单生成：四段名单 + 人工复核表（ATTRIBUTION_TASKS 第 3 批）。

段定义（卡文口径）：
  nominated_gap    50  点名缺口——db_scan 有 README 行号引证提名库 X（line≠None）
                        且 X ∉ interp dbs（「README 提名差 3,283」桶，star 降序取头）
  empty_tools      30  全空工具——dbs 空 & classification.eco == tool（会诊组样本）
  wrongly_rejected 20  误杀候选——「提名过被 AI 否决」（cands 提名 ∩ DB17 非空 +
                        db_verdicts 非空，820 桶；sqlkata/postgis 级）
  draft_122        ≤122 旧判定器 draft 存档（state/unattr_draft_122_archive.md 冻结）

段间去重：后段剔除先段已选 fn（nominated → empty → wrongly → draft，无重叠优先于全量）。
每仓证据卡：现判 dbs / 引擎建议判（attribution matcher×quorum，证据分片+池 topics）/
证据 top3 / 提名差或提名库位 / **人工栏全留空**（[[interp-task-redesign]] 金标独立性：
LLM 永不预填人工复核栏）。

产物：state/pilot_100.json（台账）+ state/pilot_review.md（复核表）。
验收（脚本内断言，退出码即结论）：50/30/20 齐额、各段 star 降序、四段两两无重叠、
证据卡字段完整。零网络。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for p in (str(ROOT), str(ROOT / "lib")):
    if p not in sys.path:
        sys.path.insert(0, p)

from attribution.api import ENGINE_VERSION, judge      # noqa: E402
from attribution.matcher import build_pack             # noqa: E402

SCAN = ROOT / "state" / "db_scan.json"
DRAFT_ARCHIVE = ROOT / "state" / "unattr_draft_122_archive.md"
OUT = ROOT / "state" / "pilot_100.json"
MD = ROOT / "state" / "pilot_review.md"

DB17 = {"PostgreSQL", "MySQL", "Oracle", "SQLite", "SQL Server", "ClickHouse",
        "MariaDB", "TiDB", "OceanBase", "PolarDB", "Dameng", "openGauss",
        "GaussDB", "GBase", "TDSQL", "YashanDB", "GoldenDB"}
SIZES = {"nominated_gap": 50, "empty_tools": 30, "wrongly_rejected": 20}


def load_interp() -> dict[str, dict]:
    """解读分片流式最小投影：fn → {dbs, db_verdicts, eco}。"""
    out: dict[str, dict] = {}
    for p in sorted((ROOT / "state" / "interp_cache_shards").glob("*.json")):
        for rec in json.loads(p.read_text(encoding="utf-8")).values():
            fn = rec.get("fn") or ""
            if not fn:
                continue
            g = rec.get("generated_at") or ""
            cur = out.get(fn)
            if cur is not None and g < cur["_g"]:
                continue
            cls = rec.get("classification") or {}
            out[fn] = {"dbs": cls.get("dbs") or [],
                       "db_verdicts": cls.get("db_verdicts") or [],
                       "eco": cls.get("eco") or "", "_g": g}
    return out


def load_pool() -> dict[str, dict]:
    """池活文件 → fn → {stars, topics}（星数缺省走证据分片兜底）。"""
    sys.path.insert(0, str(ROOT / "lib"))
    import pool_store
    try:
        items, _ = pool_store.load_latest("pool")
    except FileNotFoundError:
        return {}
    return {it.get("full_name"): {"stars": it.get("stars") or 0,
                                  "topics": list(it.get("topics") or [])}
            for it in items if it.get("full_name")}


def load_evidence_for(scope: set[str]) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for p in sorted((ROOT / "state" / "evidence_cache_shards").glob("*.json")):
        for rec in json.loads(p.read_text(encoding="utf-8")).values():
            fn = rec.get("fn") or ""
            if fn in scope:
                out[fn] = rec
    return out


def parse_draft_archive() -> list[str]:
    """冻结存档 md → fn 列表（star 降序原样保留）。"""
    fns = []
    for line in DRAFT_ARCHIVE.read_text(encoding="utf-8").splitlines():
        m = re.match(r"-\s*\d+★\s+(\S+)\s+→", line)
        if m:
            fns.append(m.group(1))
    return fns


def evidence_card(fn: str, interp: dict, pool: dict, evidence: dict) -> dict:
    """证据卡：现判 / 引擎建议判（quorum）/ 证据 top3 / 人工栏（留空）。"""
    rec = evidence.get(fn)
    stars = (pool.get(fn) or {}).get("stars") or ((rec or {}).get("stars") or 0)
    card = {"fn": fn, "stars": stars,
            "dbs_current": (interp.get(fn) or {}).get("dbs") or [],
            "engine_status": "pending_evidence", "engine_dbs": [], "evidence": []}
    if rec is None or rec.get("status") != "ok":
        return card
    verdict = judge(build_pack(fn, rec, {"topics": (pool.get(fn) or {}).get("topics") or []}))
    card["engine_status"] = verdict["status"]
    card["engine_dbs"] = verdict["dbs"]
    card["evidence"] = [
        {"kind": it["kind"], "db": it["db"], "votes": it["votes"],
         "source": it["source"]}
        for e in verdict["per_db"].values() for it in e["chain"]][:3]
    return card


def select(interp: dict, scan: dict, pool: dict) -> dict[str, list[tuple[int, str, dict]]]:
    """四段候选（全量、各自 star 降序）——不触证据分片，纯索引运算。"""
    def stars_of(fn):
        return ((pool.get(fn) or {}).get("stars")) or 0

    nominated = []
    for fn, ip in interp.items():
        sc = scan.get(fn)
        cands = ((sc.get("cands") if isinstance(sc, dict) else None) or {})
        cited = {d for d, entries in cands.items()
                 if d in DB17 and any(e.get("line") is not None for e in entries)}
        missing = sorted(cited - set(ip["dbs"]))
        if missing:
            nominated.append((stars_of(fn), fn, {"cited_missing": missing}))

    empties = [(stars_of(fn), fn, {}) for fn, ip in interp.items()
               if not ip["dbs"] and ip["eco"] == "tool"]

    rejected = []
    for fn, ip in interp.items():
        sc = scan.get(fn)
        cands = ((sc.get("cands") if isinstance(sc, dict) else None) or {})
        cited = {d for d, entries in cands.items()
                 if d in DB17 and any(e.get("line") is not None for e in entries)}
        missing = cited - set(ip["dbs"])
        # 误杀签名（sqlkata/postgis 级）：README 行号提名过 + AI 明确否决过
        #（db_verdicts 非空）+ 提名差至今未采纳——10-31 审计「820」的同族收紧口径
        if missing and ip["db_verdicts"]:
            rejected.append((stars_of(fn), fn,
                             {"nominated": sorted(missing),
                              "ai_verdicts": ip["db_verdicts"][:3]}))

    out = {"nominated_gap": sorted(nominated, key=lambda t: (-t[0], t[1])),
           "empty_tools": sorted(empties, key=lambda t: (-t[0], t[1])),
           "wrongly_rejected": sorted(rejected, key=lambda t: (-t[0], t[1])),
           "draft_122": [(0, fn, {}) for fn in parse_draft_archive()]}
    out["__counts__"] = [(k, len(v)) for k, v in out.items() if k != "__counts__"]
    return out


def scope_of(cands_by_seg: dict) -> set[str]:
    """按段序模拟去重入选 → 需要证据卡的 fn 集（只载这些仓的分片记录）。"""
    taken: set[str] = set()
    scope: set[str] = set()
    for name in ("nominated_gap", "empty_tools", "wrongly_rejected", "draft_122"):
        n = SIZES.get(name, 10 ** 9)
        got = 0
        for _s, fn, _extra in cands_by_seg[name]:
            if fn in taken:
                continue
            taken.add(fn)
            scope.add(fn)
            got += 1
            if got >= n:
                break
    return scope


def build(cands_by_seg: dict, interp: dict, pool: dict, evidence: dict) -> dict:
    taken: set[str] = set()
    segs: dict[str, list] = {}
    for name in ("nominated_gap", "empty_tools", "wrongly_rejected", "draft_122"):
        n = SIZES.get(name, 10 ** 9)
        seg = []
        for _s, fn, extra in cands_by_seg[name]:
            if fn in taken:
                continue                   # 段间去重：先段优先（无重叠优先于全量）
            taken.add(fn)
            seg.append({**evidence_card(fn, interp, pool, evidence), **extra})
            if len(seg) >= n:
                break
        seg.sort(key=lambda e: (-e["stars"], e["fn"]))   # 统一按现行星数降序
        segs[name] = seg
    return {"generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "engine": ENGINE_VERSION,
            "candidate_pools": dict(cands_by_seg["__counts__"]),
            "segments": segs}


def verify(report: dict) -> int:
    """验收断言（命令不是形容词）：齐额/降序/无重叠/字段完整。"""
    fails: list[str] = []
    segs = report["segments"]
    for name, n in SIZES.items():
        if len(segs[name]) != n:
            fails.append(f"{name} 应 {n} 条实 {len(segs[name])}")
    all_fns = [e["fn"] for seg in segs.values() for e in seg]
    if len(all_fns) != len(set(all_fns)):
        fails.append("四段存在重叠")
    for name, seg in segs.items():
        stars = [e["stars"] for e in seg]
        if stars != sorted(stars, reverse=True):
            fails.append(f"{name} 未按 star 降序")
    for name, seg in segs.items():               # draft 段星序来自存档原样
        for e in seg:
            for k in ("fn", "stars", "dbs_current", "engine_status", "engine_dbs", "evidence"):
                if k not in e:
                    fails.append(f"{name}/{e.get('fn')} 缺字段 {k}")
    print(f"[{'PASS' if not fails else 'FAIL'}] 四段 {len(segs['nominated_gap'])}/"
          f"{len(segs['empty_tools'])}/{len(segs['wrongly_rejected'])}/"
          f"{len(segs['draft_122'])} · 共 {len(all_fns)} 仓无重叠 · star 降序 · 证据卡字段完整")
    for f in fails:
        print(" ", f)
    return 1 if fails else 0


def render_md(report: dict) -> str:
    titles = {"nominated_gap": "① 点名缺口 50（README 行号提名 ∉ 现判 dbs）",
              "empty_tools": "② 全空工具 30（dbs 空 · eco=tool · 会诊组）",
              "wrongly_rejected": "③ 误杀候选 20（提名过 · AI 否决过 · sqlkata/postgis 级）",
              "draft_122": "④ 旧判定器 draft 存档（≤122，冻结名单）"}
    lines = ["# T3a 试点复核表（人工逐仓复核；LLM 不预填人工栏）", "",
             f"生成 {report['generated_at']} · 引擎 {report['engine']} · "
             f"命中口径：README 行号提名差 / 全空工具 / 提名被否决 / draft 存档", "",
             "> 复核用法：逐行看「现判 → 建议（引擎 quorum）」，在人工栏填 归/不归+库位；"
             "T3b 汇总命中率——**≥90% 才准进第 4 批，<90% 调词表回 T1 重来**。", ""]
    for name, seg in report["segments"].items():
        lines += [f"## {titles[name]} —— {len(seg)} 仓", "",
                  "| # | 仓 | star | 现判 dbs | 提名/证据摘要 | 引擎建议 | 人工栏 |",
                  "|---|---|---|---|---|---|---|"]
        for i, e in enumerate(seg, 1):
            nom = "+".join(e.get("cited_missing") or e.get("nominated") or [])
            ev = "; ".join(f"{x['kind']}:{x['db']}@{x['source'][:28]}"
                           for x in e["evidence"][:2]) or "—"
            sug = "+".join(e["engine_dbs"]) or e["engine_status"]
            lines.append(f"| {i} | {e['fn']} | {e['stars']:,} | "
                         f"{'+'.join(e['dbs_current']) or '∅'} | {nom or ev} | {sug} | 　 |")
        lines.append("")
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description="T3a 试点清单生成（零网络）")
    ap.add_argument("--verify-only", action="store_true", help="只验已落盘清单不重建")
    args = ap.parse_args()

    if args.verify_only:
        report = json.loads(OUT.read_text(encoding="utf-8"))
        return verify(report)

    interp = load_interp()
    scan = json.loads(SCAN.read_text(encoding="utf-8"))
    pool = load_pool()
    cands_by_seg = select(interp, scan, pool)
    evidence = load_evidence_for(scope_of(cands_by_seg))   # 只载入选仓的分片记录

    report = build(cands_by_seg, interp, pool, evidence)
    rc = verify(report)
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=1),
                   encoding="utf-8", newline="\n")
    MD.write_text(render_md(report), encoding="utf-8", newline="\n")
    print("候选池规模:", report["candidate_pools"])
    print(f"台账 {OUT.name} + 复核表 {MD.name}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
