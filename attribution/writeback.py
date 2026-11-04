# -*- coding: utf-8 -*-
"""T4b 回写器：引擎立案结论写回 interp 分片 dbs + 空适配打四类原因（2026-11-03）。

11-01 用户裁定：db 归属整体移交程序判定（方案 v1.5，AI 定点停烧）——本模块是
纯程序回写的唯一入口，零网络零 AI，全部结论可追溯、可回滚。

判定优先级（2026-11-03 v2：用户五刀修法，50 金标分层归因后定案）：
  ① 裁决只补集不覆盖：622 条已烧裁决与引擎结果并集，不再整集压过引擎；
     裁决不受证据预检影响（AliSQL 类无证据记录仓裁决照进）
  ② 引擎结论直通：per_db 全部信号库（立案与非立案、topic 单通道、单弱信号）
     都进 fill；质量门只剩 cat∈工具类 一道
  ③ oos 让位：范围外词命中只在"17 库信号全无"（无裁决/引擎信号/行号提名）
     时才打范围外，否则降为证据不足（带提名/范围外痕迹注记）
  ④ AI 旧 db_verdicts 不采信：mention 等旧结论不再短路（v1.5 dbs 归程序落地）
  ⑤ edu 口径不变（金标对内容仓的裁定走 v1.5 读时 dbs，本次不动）

四类空白原因（方案 §3.5 产品语义，13,242 黑洞归零）：
  真不涉及 = edu / judged_no_support / gated_app_cat（应用类立案，dbs_raw 留痕）
  范围外   = oos（Redis/DuckDB 等池外生态，detail 带命中 token）
  证据不足 = no_evidence / pending / recheck（单弱信号）/ topic 单通道 /
             行号引证未证实（提名≠支持，不硬填——T4a 停烧后由引擎复核）
  新仓未解读 = 池内无解读记录（台账记数，无记录可写）

铁律（ATTRIBUTION_TASKS T4b + v2 修订）：非本工具产物（无 dbs_src/dbs_empty_reason）
且 dbs 非空的记录零触碰（AI 时代历史结论不碰）；本工具写过的记录按新口径重写
（fill→fill 更新、fill→tag 清空，溯源字段在即视为本工具产物）。写盘走
interp_store._write_shard 同款格式（indent=1、tmp+replace、无轮转副本），
逐分片读改写、勿全量载入。

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
                              "latest_ours": bool(cls.get("dbs_src")),
                              "latest_key": (name, key),
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
    """单 fn 判定 → op（fill 打 dbs / tag 打原因）。v2 口径见模块 docstring。

    结构：edu 短路（口径不变）→ 裁决补集 → 引擎直通 → 质量门（只挡应用类）→
    空信号终局（oos 让位：有提名就降证据不足）。
    """
    base = {"fn": fn, "stars": (pool_rec or {}).get("stars", 0)}
    desc = (pool_rec or {}).get("desc") or ""
    topics = (pool_rec or {}).get("topics") or []
    oos_hit = sorted({t.lower() for t in topics} & oos_tokens)[:2]
    oos_note = ("生态命中: " + ",".join(oos_hit)) if oos_hit else \
        ("名称/简介命中范围外词" if OOS_RE.search(fn + " " + desc) else "")

    if EDU_RE.search(fn + " " + desc):                   # edu 口径不变（五刀未动）
        return {**base, "op": "tag", "reason": R_TRUE_UNRELATED, "detail": "教学/内容类"}

    # ① 裁决补集（先落裁决库位；不受证据预检影响——AliSQL 类无记录仓照进）
    dbs: list[str] = []
    votes: dict[str, float | None] = {}
    srcs: dict[str, tuple[str, str]] = {}
    for d in sorted(adj_dbs, key=DB_ORDER.index):
        if d not in dbs:
            dbs.append(d)
        srcs[d] = ("adjudicate", "t4a-1")

    # ② 引擎直通（evidence ok 才跑；per_db 信号库进 fill——立案与单弱信号同权；
    #    A 修：test/example/sample 弱路径 0.5 票不直通，防测试夹具误配）
    ev_note = ""
    weak_only: list[str] = []
    if evidence_rec is None:
        ev_note = "无证据记录（待增量补采）"
    elif evidence_rec.get("status") == "partial":
        ev_note = "证据 partial 树截断（待重采）"
    elif evidence_rec.get("status") != "ok":
        ev_note = f"证据状态: {evidence_rec.get('status')}"
    else:
        verdict = judge(build_pack(fn, evidence_rec, {"topics": topics}))
        for db, e in sorted(verdict["per_db"].items(), key=lambda kv: -kv[1]["votes"]):
            strong = sum(it["votes"] for it in e["chain"]
                         if not ((it.get("detail") or {}).get("weak_path")))
            if strong <= 0:
                weak_only.append(db)
                continue
            if db not in dbs:
                dbs.append(db)
            votes[db] = e["votes"]
            srcs[db] = ("engine", ENGINE_VERSION)
    dbs.sort(key=DB_ORDER.index)

    # ③ 决策：质量门只剩 cat∈工具类
    if dbs:
        if latest["cat"] not in TOOL_CATS:
            return {**base, "op": "tag", "reason": R_TRUE_UNRELATED,
                    "detail": f"应用类（cat={latest['cat']}），引擎立案未采纳: "
                              + ",".join(dbs),
                    "dbs_raw": dbs}
        kinds = sorted({k for k, _ in srcs.values()})
        return {**base, "op": "fill", "dbs": dbs, "src": "+".join(kinds),
                "ver": ENGINE_VERSION if "engine" in kinds else "t4a-1",
                "votes": votes or None, "ev_note": ev_note or None}

    # ④ 空信号终局：oos 只在 17 库信号全无（含行号提名）时打范围外
    if oos_note and not _cited_libs(scan_rec):
        return {**base, "op": "tag", "reason": R_OUT_OF_SCOPE, "detail": oos_note}
    det = ev_note or "无信号"
    if weak_only:
        det += f"；弱路径信号不直通: {','.join(sorted(weak_only, key=DB_ORDER.index))}"
    if oos_note:
        det += "；范围外痕迹: " + oos_note
    desc_libs = _desc_libs(scan_rec)
    if desc_libs:
        det += f"；简介候选未证实: {','.join(desc_libs)}"
    return {**base, "op": "tag", "reason": R_INSUFFICIENT,
            "detail": det + _cite_note(scan_rec)}


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
    """ops 落盘：铁律=非本工具产物且 dbs 非空 → 零触碰（AI 时代历史结论不碰）；
    本工具写过（带 dbs_src/dbs_empty_reason）的记录按新口径重写（含 fill→fill 更新、
    fill→tag 清空）。同结论（dbs 内容+溯源）跳过=幂等。值整体替换走 _write_shard。"""
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
            if not isinstance(cls, dict):
                continue
            ours = bool(cls.get("dbs_src") or cls.get("dbs_empty_reason"))
            if not ours and (cls.get("dbs") or []):
                continue                            # 铁律：历史结论零触碰
            op = ops[fn]
            if op["op"] == "fill":
                if cls.get("dbs") == list(op["dbs"]) and \
                        cls.get("dbs_src") == {"kind": op["src"], "ver": op["ver"],
                                               "at": TODAY}:
                    continue                        # 幂等：同结论已写
                cls["dbs"] = list(op["dbs"])
                cls["dbs_src"] = {"kind": op["src"], "ver": op["ver"], "at": TODAY}
                cls.pop("dbs_empty_reason", None)
            else:
                want = {"reason": op["reason"], "detail": op["detail"], "at": TODAY}
                if cls.get("dbs_empty_reason") == want:
                    continue
                cls["dbs"] = []                     # 本工具旧 fill 按新口径改 tag
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
    # 圈范围：最新记录 dbs 空（补空缺）∪ 本工具旧 fill（带 dbs_src，按新口径重判；
    # 旧 fill 单记录仓 keys 为空，落点靠 latest_key 补）
    in_scope = {fn: ip for fn, ip in latest.items()
                if (ip["latest_empty"] and ip["keys"]) or ip["latest_ours"]}
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
        ip = in_scope[fn]
        op = compute_op(fn, ip, pool.get(fn), evidence.get(fn),
                        scan.get(fn), adj.get(fn) or set(), oos_tokens)
        keys = list(ip["keys"])
        # 旧 fill 重判：最新记录 dbs 非空，落点键不在空记录集里，补进去
        if ip["latest_ours"] and not ip["latest_empty"] \
                and ip["latest_key"] not in keys:
            keys.append(ip["latest_key"])
        op["keys"] = keys
        ops[fn] = op

    fill = [o for o in ops.values() if o["op"] == "fill"]
    tag = [o for o in ops.values() if o["op"] == "tag"]
    from collections import Counter
    stats = {
        "in_scope": len(in_scope), "judged": len(fns),
        "fill": len(fill), "tag": len(tag),
        "fill_engine": sum(1 for o in fill if "engine" in o["src"]),
        "fill_adjudicate": sum(1 for o in fill if "adjudicate" in o["src"]),
        "tag_reasons": dict(Counter(o["reason"] for o in tag)),
        "fill_dbs": dict(Counter(db for o in fill for db in o["dbs"])),
        "pool_uninterpreted": len(set(pool) - set(latest)),
    }
    # 抽检 20 条：fill 优先 star 降序 12 条 + tag 各原因头牌 8 条
    samples = []
    for o in sorted(fill, key=lambda x: -x["stars"])[:12]:
        v = " ".join(f"{d}={w:g}" for d, w in (o.get("votes") or {}).items() if w)
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
