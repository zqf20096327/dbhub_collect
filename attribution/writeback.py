# -*- coding: utf-8 -*-
"""T4b 回写器：引擎立案结论写回 interp 分片 dbs + 空适配打四类原因（2026-11-03）。

11-01 用户裁定：db 归属整体移交程序判定（方案 v1.5，AI 定点停烧）——本模块是
纯程序回写的唯一入口，零网络零 AI，全部结论可追溯、可回滚。

判定优先级（与 T2e 薄壳/T3b 验证面同口径，只换落点）：
  ① adjudicate：已烧的 T4a 定点裁决 supports（cite 强制、622 条已授权素材，不浪费）
  ② 信号层（口径与 unattr_judge 逐字一致）：范围外词表/oos 正则 → oos；
     教程正则 → edu；db_verdicts 非空（问过判过非 support）→ judged_no_support
  ③ 证据层：分片无记录/partial → pending；empty_repo/gone/error → no_evidence
  ④ 引擎层：build_pack × judge → case_opened 且 cat∈工具类 且非 topic 单通道
     → 回写 dbs（draft 质量门 = T3b 实测 79/79=100% 精度那一个面）

四类空白原因（方案 §3.5 产品语义，13,242 黑洞归零）：
  真不涉及 = edu / judged_no_support / gated_app_cat（应用类立案，dbs_raw 留痕）
  范围外   = oos（Redis/DuckDB 等池外生态，detail 带命中 token）
  证据不足 = no_evidence / pending / recheck（单弱信号）/ topic 单通道 /
             行号引证未证实（提名≠支持，不硬填——T4a 停烧后由引擎复核）
  新仓未解读 = 池内无解读记录（台账记数，无记录可写）

铁律（ATTRIBUTION_TASKS T4b）：只补空缺不改历史——fn 的最新记录 dbs 非空即整仓
跳过；记录级只动 dbs==[] 的记录，非空记录零触碰。写盘走 interp_store._write_shard
同款格式（indent=1、tmp+replace、无轮转副本），逐分片读改写、勿全量载入。

溯源与回滚：回写记录加 classification.dbs_src={kind,ver,at}；打原因记录加
classification.dbs_empty_reason={reason,detail,at}。台账 state/attribution_writes.json
（fn → op/dbs/src/reason/keys）幂等可断点，--rollback 按台账逆操作还原。

CLI：默认全量；--dry-run 只出分布与报告不写盘；--limit N 冒烟；
--report-only 由台账重出报告；--rollback 逆写回滚（台账滚档为 .rolled-<ts>）。
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for p in (str(ROOT), str(ROOT / "lib"), str(ROOT / "config")):
    if p not in sys.path:
        sys.path.insert(0, p)

from attribution.api import judge, ENGINE_VERSION          # noqa: E402
from attribution.matcher import build_pack                  # noqa: E402
from interpret.unattr_judge import (                        # noqa: E402  口径复用，零漂移
    DB_ORDER, DB17, EDU_RE, OOS_RE, TOOL_CATS, _recheck_strength,
)

STATE = ROOT / "state"
INTERP_SHARDS = STATE / "interp_cache_shards"
EVIDENCE_SHARDS = STATE / "evidence_cache_shards"
DB_SCAN = STATE / "db_scan.json"
ADJUDICATIONS = STATE / "adjudications.ndjson"
LEDGER = STATE / "attribution_writes.json"
REPORT = STATE / "attribution_writes.md"

TODAY = datetime.now().strftime("%Y-%m-%d")
R_TRUE_UNRELATED = "真不涉及"      # edu / AI 判过无 support / 应用类立案
R_OUT_OF_SCOPE = "范围外"          # Redis/DuckDB 等池外生态
R_INSUFFICIENT = "证据不足"        # 采证了没信号/信号弱/提名未证实
R_NOT_INTERPRETED = "新仓未解读"   # 池内无解读记录（台账记数）


# ── 读取层（流式，勿全量载入）──────────────────────────────────────────

def load_interp_index(interp_dir: Path) -> dict[str, dict]:
    """分片流式索引：fn → {cat,db_verdicts,latest_empty,keys=[(shard,key),...]}。

    "最新记录 dbs 为空"才入圈（unattr_judge 投影同款"最新者代表该仓"——老记录空、
    最新非空的 fn 视为已有归属，铁律不碰）。入圈 fn 的 keys 收齐该 fn 名下所有
    dbs==[] 的记录（dbs 是仓级事实，统一落 op）。无 classification 的记录不属于
    13,242 黑洞口径，不索引。
    """
    latest: dict[str, dict] = {}
    for name in sorted(p.name for p in interp_dir.glob("*.json")):
        for key, rec in json.loads((interp_dir / name).read_text(encoding="utf-8")).items():
            fn = rec.get("fn") or ""
            cls = rec.get("classification")
            if not fn or not isinstance(cls, dict):
                continue
            g = rec.get("generated_at") or ""
            cur = latest.get(fn)
            if cur is None or g >= cur["_g"]:
                latest[fn] = {"cat": cls.get("cat") or "其他",
                              "db_verdicts": cls.get("db_verdicts") or [],
                              "latest_empty": not (cls.get("dbs") or []),
                              "keys": (cur or {}).get("keys", []), "_g": g}
            if not (cls.get("dbs") or []):
                latest[fn]["keys"].append((name, key))
    return latest


def load_pool() -> dict[str, dict]:
    """池活文件 → {fn: {desc,stars,topics}}（出池仓无记录=无 topic 证据，保守）。"""
    import pool_store
    items, _src = pool_store.load_latest("pool")
    out: dict[str, dict] = {}
    for it in items:
        fn = it.get("full_name") or ""
        if fn:
            out[fn] = {"desc": it.get("description") or "", "stars": it.get("stars") or 0,
                       "topics": list(it.get("topics") or [])}
    return out


def load_adjudications(path: Path) -> dict[str, set[str]]:
    """T4a 已烧裁决（cite 强制）→ {fn: {db,...}}，只收 verdict=supports。"""
    out: dict[str, set[str]] = {}
    if not path.is_file():
        return out
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        if r.get("verdict") == "supports" and r.get("fn") and r.get("db") in DB17:
            out.setdefault(r["fn"], set()).add(r["db"])
    return out


def oos_topic_tokens() -> set[str]:
    """db_profiles GLOBAL.out_of_scope_dbs 小写集（薄壳 collect_rows 同源）。"""
    import db_profiles as dp
    return {w.lower() for w in dp.GLOBAL.get("out_of_scope_dbs", [])}


# ── 判定层（单 fn → op；纯函数，可单测）─────────────────────────────────

def _cited_libs(scan_rec: dict | None) -> list[str]:
    """db_scan 行号引证命中的 17 库（提名≠支持，只作 detail 留痕）。"""
    cands = ((scan_rec or {}).get("cands") if isinstance(scan_rec, dict) else None) or {}
    hit = {d for d, lst in cands.items() if d in DB17
           and any(isinstance(c, dict) and c.get("line") is not None for c in (lst or []))}
    return sorted(hit, key=DB_ORDER.index)


def _desc_libs(scan_rec: dict | None) -> list[str]:
    cands = ((scan_rec or {}).get("cands") if isinstance(scan_rec, dict) else None) or {}
    return [d for d in sorted(cands, key=DB_ORDER.index) if d in DB17]


def _cite_note(scan_rec: dict | None) -> str:
    libs = _cited_libs(scan_rec)
    return f"；readme 行号提名未证实: {','.join(libs)}" if libs else ""


def compute_op(fn: str, latest: dict, pool_rec: dict | None, evidence_rec: dict | None,
               scan_rec: dict | None, adj_dbs: set[str], oos_tokens: set[str]) -> dict:
    """单 fn 判定 → op（fill 打 dbs / tag 打原因）。

    与 unattr_judge.judge_one 同口径同顺序（adjudicate 频道插队最前——已授权素材），
    区别只在落点：那里写台账等人工签发，这里按 11-01 裁定直接程序回写。
    """
    base = {"fn": fn, "stars": (pool_rec or {}).get("stars", 0)}
    if adj_dbs:                                        # ① 已授权定点裁决
        return {**base, "op": "fill", "dbs": [d for d in DB_ORDER if d in adj_dbs],
                "src": "adjudicate", "ver": "t4a-1"}

    desc = (pool_rec or {}).get("desc") or ""
    topics = (pool_rec or {}).get("topics") or []

    # ② 信号层（口径与薄壳逐字一致；出池仓无 desc/topics 只查仓名）
    oos_hit = sorted({t.lower() for t in topics} & oos_tokens)[:2]
    if oos_hit or OOS_RE.search(fn + " " + desc):
        return {**base, "op": "tag", "reason": R_OUT_OF_SCOPE,
                "detail": ("生态命中: " + ",".join(oos_hit)) if oos_hit
                          else "名称/简介命中范围外词"}
    if EDU_RE.search(fn + " " + desc):
        return {**base, "op": "tag", "reason": R_TRUE_UNRELATED, "detail": "教学/内容类"}
    if latest["db_verdicts"]:
        return {**base, "op": "tag", "reason": R_TRUE_UNRELATED,
                "detail": "AI 判过非 support（db_verdicts 非空）"}

    # ③ 证据层（无记录/partial → 补采队列；empty_repo/gone → 终局无证据）
    if evidence_rec is None:
        return {**base, "op": "tag", "reason": R_INSUFFICIENT,
                "detail": "无证据记录（待增量补采）" + _cite_note(scan_rec)}
    st = evidence_rec.get("status")
    if st == "partial":
        return {**base, "op": "tag", "reason": R_INSUFFICIENT,
                "detail": "证据 partial 树截断（待重采）" + _cite_note(scan_rec)}
    if st != "ok":
        return {**base, "op": "tag", "reason": R_INSUFFICIENT,
                "detail": f"证据状态: {st}" + _cite_note(scan_rec)}

    # ④ 引擎层：draft 质量门（≥2 票立案 + 工具类 + 非 topic 单通道）才回写
    verdict = judge(build_pack(fn, evidence_rec, {"topics": topics}))
    if verdict["status"] == "no_evidence":
        desc_libs = _desc_libs(scan_rec)
        det = "无信号" + (f"；简介候选未证实: {','.join(desc_libs)}" if desc_libs else "")
        return {**base, "op": "tag", "reason": R_INSUFFICIENT,
                "detail": det + _cite_note(scan_rec)}
    if verdict["status"] == "below_quorum":
        dbs = sorted(verdict["per_db"], key=DB_ORDER.index)
        return {**base, "op": "tag", "reason": R_INSUFFICIENT,
                "detail": f"单弱信号未立案（{_recheck_strength(verdict)}: {','.join(dbs)}）"
                          + _cite_note(scan_rec)}
    chains = [it for e in verdict["per_db"].values() for it in e["chain"]]
    if all(it["kind"] == "topic" for it in chains):
        dbs = sorted(verdict["per_db"], key=DB_ORDER.index)
        return {**base, "op": "tag", "reason": R_INSUFFICIENT,
                "detail": f"topic 单通道不放直通（{','.join(dbs)}）" + _cite_note(scan_rec)}
    if latest["cat"] not in TOOL_CATS:
        return {**base, "op": "tag", "reason": R_TRUE_UNRELATED,
                "detail": f"应用类（cat={latest['cat']}），引擎立案未采纳: "
                          + ",".join(verdict["dbs"]),
                "dbs_raw": verdict["dbs"]}
    return {**base, "op": "fill", "dbs": verdict["dbs"],
            "src": "engine", "ver": ENGINE_VERSION,
            "votes": {db: e["votes"] for db, e in verdict["per_db"].items()}}


# ── 写盘层（逐分片读改写）──────────────────────────────────────────────

def _write_shard_file(interp_dir: Path, bucket_file: str, entries: dict) -> None:
    """与 interp_store._write_shard 同款格式落盘（indent=1、tmp+replace、无轮转）——
    自带目录参数：interp_store 版写死全局 SHARD_DIR，自测宇宙会写穿真实分片。
    newline='\\n' 必须显式：仓内分片是 CI(Linux) 写的 LF，Windows 本机不带此参
    会整片翻成 CRLF——2.9M 行假 diff（[[ci-resume-pitfalls]] CRLF 归一坑）。"""
    tmp = interp_dir / (bucket_file + ".tmp")
    tmp.write_text(json.dumps(entries, ensure_ascii=False, indent=1),
                   encoding="utf-8", newline="\n")
    tmp.replace(interp_dir / bucket_file)


def apply_ops(interp_dir: Path, ops: dict[str, dict]) -> int:
    """ops 落盘：只动 fn 名下 dbs==[] 的记录（铁律），值整体替换走 _write_shard。
    已带同结论 dbs_src/dbs_empty_reason 的记录跳过（二次运行零脏分片=幂等）。"""
    by_shard: dict[str, dict] = {}
    for fn, op in ops.items():
        if op.get("op") not in ("fill", "tag"):
            continue
        for shard, key in op.get("keys", []):
            by_shard.setdefault(shard, {})[key] = fn
    for shard, keys in sorted(by_shard.items()):
        entries = json.loads((interp_dir / shard).read_text(encoding="utf-8"))
        for key, fn in keys.items():
            cls = (entries.get(key) or {}).get("classification")
            if not isinstance(cls, dict) or (cls.get("dbs") or []):
                continue                            # 铁律：非空零触碰
            op = ops[fn]
            if op["op"] == "fill":
                if cls.get("dbs_src") == {"kind": op["src"], "ver": op["ver"], "at": TODAY}:
                    continue                        # 幂等：同结论已写
                cls["dbs"] = list(op["dbs"])
                cls["dbs_src"] = {"kind": op["src"], "ver": op["ver"], "at": TODAY}
                cls.pop("dbs_empty_reason", None)
            else:
                want = {"reason": op["reason"], "detail": op["detail"], "at": TODAY}
                if cls.get("dbs_empty_reason") == want:
                    continue
                cls["dbs_empty_reason"] = want
                cls.pop("dbs_src", None)
        _write_shard_file(interp_dir, shard, entries)
    return len(by_shard)


def rollback(ledger_path: Path, interp_dir: Path) -> int:
    """按台账逆操作还原：dbs 置 []、摘 dbs_src/dbs_empty_reason；台账滚档。"""
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    by_shard: dict[str, list] = {}
    for fn, op in (ledger.get("ops") or {}).items():
        if op.get("op") not in ("fill", "tag"):
            continue
        for shard, key in op.get("keys") or []:
            by_shard.setdefault(shard, []).append(key)
    for shard, keys in sorted(by_shard.items()):
        p = interp_dir / shard
        if not p.is_file():
            continue
        entries = json.loads(p.read_text(encoding="utf-8"))
        for key in keys:
            cls = (entries.get(key) or {}).get("classification")
            if not isinstance(cls, dict):
                continue
            if cls.get("dbs_src") or cls.get("dbs_empty_reason"):
                cls["dbs"] = []                     # 只回滚本工具写过的记录
                cls.pop("dbs_src", None)
                cls.pop("dbs_empty_reason", None)
        _write_shard_file(interp_dir, shard, entries)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    ledger_path.rename(ledger_path.with_name(ledger_path.name + ".rolled-" + stamp))
    _atomic_json(ledger_path, {"generated_at": datetime.now().isoformat(),
                               "rolled_back_from": ledger.get("generated_at"), "ops": {}})
    return len(by_shard)


def _atomic_json(path: Path, obj) -> None:
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8", newline="\n")
    tmp.replace(path)


# ── 主流程 ─────────────────────────────────────────────────────────────


def write_report(report_path: Path, stats: dict, ops: dict[str, dict], samples: list[str]) -> None:
    lines = [
        "# T4b 程序适配回写报告（引擎 " + ENGINE_VERSION + " + t4a-1）",
        f"生成：{datetime.now().strftime('%Y-%m-%d %H:%M')} · "
        f"入圈 {stats['in_scope']} · 回写 {stats['fill']} · 打原因 {stats['tag']}",
        "",
        "## 黑洞归零",
        f"- 入圈（最新记录 dbs 空）: {stats['in_scope']}",
        f"- 回写 dbs: {stats['fill']}（engine {stats['fill_engine']} / "
        f"adjudicate {stats['fill_adjudicate']}）",
        f"- 打原因: {stats['tag']}"
        + "".join(f" · {k} {stats['tag_reasons'].get(k, 0)}"
                  for k in (R_TRUE_UNRELATED, R_OUT_OF_SCOPE, R_INSUFFICIENT)),
        f"- 池内未解读（{R_NOT_INTERPRETED}，台账记数不写记录）: {stats['pool_uninterpreted']}",
        f"- 覆盖率: 入圈 100% 带结论（fill+tag = {stats['fill'] + stats['tag']}）",
        "",
        "## 回写库位分布（engine）",
    ]
    for db, n in sorted(stats["fill_dbs"].items(), key=lambda x: -x[1]):
        lines.append(f"- {db}: {n}")
    lines += ["", "## 抽检 20 条（star 降序·源混排）", ""]
    lines += samples
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def run(*, dry_run: bool = False, limit: int = 0, report_only: bool = False,
        interp_dir: Path = INTERP_SHARDS, evidence_dir: Path = EVIDENCE_SHARDS,
        scan_path: Path = DB_SCAN, adjudications_path: Path = ADJUDICATIONS,
        ledger_path: Path = LEDGER, report_path: Path = REPORT,
        pool: dict | None = None, scan: dict | None = None) -> dict:
    if report_only:
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
        ops = ledger.get("ops") or {}
        stats = ledger.get("counts") or {}
        write_report(report_path, stats, ops, ledger.get("samples") or [])
        print(f"报告已重出 {report_path}")
        return stats

    latest = load_interp_index(interp_dir)
    in_scope = {fn: ip for fn, ip in latest.items()
                if ip["latest_empty"] and ip["keys"]}
    if pool is None:
        pool = load_pool()
    if scan is None:
        scan = json.loads(scan_path.read_text(encoding="utf-8"))
    adj = load_adjudications(adjudications_path)
    oos_tokens = oos_topic_tokens()

    fns = sorted(in_scope, key=lambda f: -(pool.get(f) or {}).get("stars", 0))
    if limit > 0:
        fns = fns[:limit]
    evidence = _load_evidence(evidence_dir, set(fns))

    ops: dict[str, dict] = {}
    for fn in fns:
        op = compute_op(fn, in_scope[fn], pool.get(fn), evidence.get(fn),
                        scan.get(fn), adj.get(fn) or set(), oos_tokens)
        op["keys"] = in_scope[fn]["keys"]
        ops[fn] = op

    fill = [o for o in ops.values() if o["op"] == "fill"]
    tag = [o for o in ops.values() if o["op"] == "tag"]
    from collections import Counter
    stats = {
        "in_scope": len(in_scope), "judged": len(fns),
        "fill": len(fill), "tag": len(tag),
        "fill_engine": sum(1 for o in fill if o["src"] == "engine"),
        "fill_adjudicate": sum(1 for o in fill if o["src"] == "adjudicate"),
        "tag_reasons": dict(Counter(o["reason"] for o in tag)),
        "fill_dbs": dict(Counter(db for o in fill for db in o["dbs"])),
        "pool_uninterpreted": len(set(pool) - set(latest)),
    }
    # 抽检 20 条：fill 优先 star 降序 12 条 + tag 各原因头牌 8 条
    samples = []
    for o in sorted(fill, key=lambda x: -x["stars"])[:12]:
        v = " ".join(f"{d}={w:g}" for d, w in (o.get("votes") or {}).items())
        samples.append(f"- {o['stars']:>6}★ {o['fn']} → {','.join(o['dbs'])}"
                       f"（{o['src']}{'；' + v if v else ''}）")
    for reason in (R_TRUE_UNRELATED, R_OUT_OF_SCOPE, R_INSUFFICIENT):
        for o in sorted((x for x in tag if x["reason"] == reason),
                        key=lambda x: -x["stars"])[:3]:
            samples.append(f"- {o['stars']:>6}★ {o['fn']} → [{reason}] {o['detail'][:80]}")

    if dry_run:
        print(json.dumps({k: v for k, v in stats.items() if k != "fill_dbs"},
                         ensure_ascii=False, indent=1))
        print("fill_dbs:", dict(sorted(stats["fill_dbs"].items(), key=lambda x: -x[1])))
        return stats

    n_shards = apply_ops(interp_dir, ops)
    ledger = {"generated_at": datetime.now().isoformat(),
              "engine": ENGINE_VERSION, "counts": stats,
              "ops": {fn: {k: v for k, v in op.items() if k != "stars"}
                      for fn, op in ops.items()},
              "samples": samples}
    _atomic_json(ledger_path, ledger)
    write_report(report_path, stats, ops, samples)
    print(f"回写 {len(fill)} · 打原因 {len(tag)} · 脏分片 {n_shards}")
    print(f"台账 {ledger_path}\n报告 {report_path}")
    return stats


def _load_evidence(evidence_dir: Path, scope: set[str]) -> dict[str, dict]:
    """unattr_judge.load_evidence_for 的目录参数化版（该函数写死 STATE 目录）。"""
    out: dict[str, dict] = {}
    for p in sorted(evidence_dir.glob("*.json")):
        for rec in json.loads(p.read_text(encoding="utf-8")).values():
            fn = rec.get("fn") or ""
            if fn in scope:
                out[fn] = rec
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="T4b 程序适配回写器（零网络零 AI）")
    ap.add_argument("--dry-run", action="store_true", help="只出分布不写盘")
    ap.add_argument("--limit", type=int, default=0, help="只判前 N 仓（star 降序冒烟）")
    ap.add_argument("--report-only", action="store_true", help="由台账重出报告")
    ap.add_argument("--rollback", action="store_true",
                    help="按台账逆写还原（台账滚档 .rolled-<ts>）")
    args = ap.parse_args()
    if args.rollback:
        n = rollback(LEDGER, INTERP_SHARDS)
        print(f"已回滚 {n} 个分片；台账滚档完成")
        return 0
    run(dry_run=args.dry_run, limit=args.limit, report_only=args.report_only)
    return 0


if __name__ == "__main__":
    sys.exit(main())
