# -*- coding: utf-8 -*-
"""全池扫描 CLI（ATTRIBUTION T2d，方案 §1 口径 / M1 验收）。

  python attribution/scan.py --gap     全池扫描 → 台账 state/attribution_gap.json
                                      + 复核表 state/attribution_gap.md
  python attribution/scan.py --status  只读打印分布（证据状态/判定/三清单计数）
  --limit N                            只处理前 N 个证据分片（冒烟；不卡验收线）

三清单口径（10-31 交集比对实测，验收 = 复现实测 ±10%，词表已扩只会更高）：
  漏报（匹配不到）     interp dbs 空 & 指纹（dep/image/ci/tree）命中 ≥1 库 → 实测 1,468，验收 ≥1,400
  不完整（匹配不完整） interp dbs 非空 & 指纹命中含 dbs 外的库         → 实测 1,432，验收 ≥1,300
  双源 strong          interp dbs 空 & topic∩指纹同库命中               → 实测   778，验收 ≥700（漏报子集）

边界与防坑：
  - 比对域 = 证据分片 ∩ 解读分片（10-31 交集 30,169 同口径）；无解读记录 =
    新仓未解读，另册计数不进三清单（空白态四类是 T4b 的事）
  - 仅 topic 不算指纹命中——3,126 仅 topic 待复核是另册，不混进漏报
  - 30k+ 仓内存纪律：interp/pool 各建一份最小投影 dict（fn→dbs、fn→stars/topics），
    证据逐分片流式 yield，勿一次载入 256 分片（卡文防坑）
  - 分片键形态不一（interp 键=fn 哈希、evidence 键=fn 或哈希）——一律按 rec["fn"] 对齐
  - 台账写盘 atomic_write_json 三副本轮转（[[atomic-write-rotation]]，勿裸写）
  - 零网络零 API：只读本地分片 + 池快照
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
LIB = ROOT / "lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from gh import atomic_write_json  # noqa: E402  台账原子写（轮转三副本）

from attribution.api import ENGINE_VERSION, judge  # noqa: E402
from attribution.matcher import build_pack  # noqa: E402

EVIDENCE_DIR = ROOT / "state" / "evidence_cache_shards"
INTERP_DIR = ROOT / "state" / "interp_cache_shards"
POOL_PATH = ROOT / "data" / "snapshot_latest" / "pool.json"
STATE_DIR = ROOT / "state"
GAP_JSON = STATE_DIR / "attribution_gap.json"
GAP_MD = STATE_DIR / "attribution_gap.md"

FP_KINDS = frozenset({"dep", "image", "ci", "tree"})   # 指纹四型（topic 是自声明非指纹）
MD_TOP_N = 50                                          # 复核表每清单最多行数

# 验收线（卡文：复现 10-31 实测 ±10% 下限；--limit 冒烟不卡线）
ACCEPT_MIN = {"missed": 1400, "incomplete": 1300, "dual": 700}

LIST_TITLES = {
    "missed": "清单一 · 漏报（匹配不到：dbs 空、指纹有命中）",
    "incomplete": "清单二 · 不完整（已归但指纹显示还支持别的）",
    "dual": "清单三 · 双源 strong（dbs 空、topic∩指纹同库互证）",
}


def load_interp_dbs(interp_dir: Path = INTERP_DIR) -> dict[str, list]:
    """解读分片 → {fn: classification.dbs} 最小投影（键是 fn 哈希，值里取 fn）。"""
    out: dict[str, list] = {}
    for p in sorted(interp_dir.glob("*.json")):
        for rec in json.loads(p.read_text(encoding="utf-8")).values():
            fn = (rec.get("fn") or "").strip()
            if fn:
                out[fn] = list((rec.get("classification") or {}).get("dbs") or [])
    return out


def load_pool_view(pool_path: Path = POOL_PATH) -> dict[str, dict]:
    """池快照 → {fn: {stars, topics}} 最小投影（pool.json 是 list，fn 在 full_name）。"""
    out: dict[str, dict] = {}
    if not Path(pool_path).is_file():
        return out                                    # 池快照缺席：topic 全空、星数走分片
    for e in json.loads(Path(pool_path).read_text(encoding="utf-8")):
        fn = (e.get("full_name") or "").strip()
        if fn:
            out[fn] = {"stars": e.get("stars"), "topics": list(e.get("topics") or [])}
    return out


def iter_evidence_records(evidence_dir: Path = EVIDENCE_DIR,
                          limit_shards: int | None = None):
    """证据分片逐个读、逐条 yield（流式，内存里永远只有一个分片）。"""
    for i, p in enumerate(sorted(evidence_dir.glob("*.json"))):
        if limit_shards is not None and i >= limit_shards:
            return
        for rec in json.loads(p.read_text(encoding="utf-8")).values():
            yield rec


def scan(evidence_dir: Path = EVIDENCE_DIR, interp_dir: Path = INTERP_DIR,
         pool_path: Path = POOL_PATH, limit_shards: int | None = None) -> dict:
    """全池扫描 → 缺口报告 dict（三清单 + 统计；纯本地，可重复跑）。"""
    interp_dbs = load_interp_dbs(interp_dir)
    pool = load_pool_view(pool_path)

    stats: Counter = Counter()
    missed: list[dict] = []
    incomplete: list[dict] = []
    dual: list[dict] = []
    per_db_add: Counter = Counter()                   # 不完整可补库位直方图（方案 §1 对照）
    case_db: Counter = Counter()                      # 全域立案库直方图

    for rec in iter_evidence_records(evidence_dir, limit_shards):
        fn = (rec.get("fn") or "").strip()
        if not fn:
            stats["rec_no_fn"] += 1
            continue
        stats["evidence"] += 1
        stats[f"status_{rec.get('status')}"] += 1
        pool_rec = pool.get(fn)
        if pool_rec is not None:
            stats["pool_linked"] += 1
        stars = (pool_rec or {}).get("stars", rec.get("stars"))
        topics = (pool_rec or {}).get("topics") or []

        try:
            pack = build_pack(fn, rec, {"topics": topics})
            verdict = judge(pack)
        except ValueError:
            stats["skip_bad_pack"] += 1               # 缺采集时间等防御路径：跳过不炸
            continue
        stats[f"verdict_{verdict['status']}"] += 1
        for db in verdict["dbs"]:
            case_db[db] += 1

        fp_dbs = sorted({e["db"] for e in pack["evidences"] if e["kind"] in FP_KINDS})
        if fp_dbs:
            stats["fp_hit"] += 1

        if fn not in interp_dbs:                      # 新仓未解读：另册（空白态四类归 T4b）
            stats["interp_missing"] += 1
            continue
        stats["interp_linked"] += 1
        cur = interp_dbs[fn]
        if cur:
            add = [d for d in fp_dbs if d not in cur]
            if add:
                stats["incomplete"] += 1
                incomplete.append({"fn": fn, "stars": stars, "interp": cur, "add": add,
                                   "add_case": [d for d in verdict["dbs"] if d not in cur]})
                per_db_add.update(add)
        else:
            stats["interp_empty"] += 1
            if fp_dbs:
                stats["missed"] += 1
                missed.append({"fn": fn, "stars": stars, "fp": fp_dbs,
                               "case": verdict["dbs"]})
                both = [d for d in fp_dbs if d in {e["db"] for e in pack["evidences"]
                                                  if e["kind"] == "topic"}]
                if both:
                    stats["dual"] += 1
                    dual.append({"fn": fn, "stars": stars, "dual": both})

    # star 降序；无星记 -1，同星按 fn 升序保确定性（验收可 diff 的前提）
    key = lambda e: (-(e["stars"] if e["stars"] is not None else -1), e["fn"])  # noqa: E731
    missed.sort(key=key)
    incomplete.sort(key=key)
    dual.sort(key=key)

    return {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "engine": ENGINE_VERSION,
        "shard_limit": limit_shards,
        "universe": {k: stats[k] for k in sorted(stats)},
        "counts": {"missed": len(missed), "incomplete": len(incomplete), "dual": len(dual)},
        "per_db_add": dict(per_db_add.most_common()),
        "case_opened_db": dict(case_db.most_common()),
        "lists": {"missed": missed, "incomplete": incomplete, "dual": dual},
    }


def _fmt_stars(s) -> str:
    return "-" if s is None else f"{s:,}"


def render_md(report: dict) -> str:
    """缺口报告 markdown（每清单 top MD_TOP_N + 口径注记，供人工复核）。"""
    u = report["universe"]
    c = report["counts"]
    lines = [
        "# 适配缺口报告（attribution scan --gap）",
        "",
        f"- 生成 {report['generated_at']} · 引擎 {report['engine']}"
        f" · 比对域：证据 {u.get('evidence', 0):,} 条（ok {u.get('status_ok', 0):,}）"
        f" ∩ 解读 {u.get('interp_linked', 0):,}（未解读另册 {u.get('interp_missing', 0):,}）",
        f"- **漏报 {c['missed']:,} / 不完整 {c['incomplete']:,} / 双源 strong {c['dual']:,}**"
        f"（10-31 实测 1,468 / 1,432 / 778，验收线 ≥1,400 / ≥1,300 / ≥700）",
        f"- 口径：dbs=解读分片 classification.dbs；指纹命中=dep/image/ci/tree 四型证据"
        f"（仅 topic 不算）；双源=漏报子集；star 降序",
        "",
    ]
    if report.get("per_db_add"):
        adds = " · ".join(f"{db} {n}" for db, n in list(report["per_db_add"].items())[:10])
        lines += [f"- 不完整可补库位 Top：{adds}", ""]

    cols = {  # 每清单表格列（fn 之后）
        "missed": ("star", "指纹命中", "立案(quorum)"),
        "incomplete": ("star", "现判 dbs", "可补(指纹)", "可补(立案)"),
        "dual": ("star", "topic∩指纹互证"),
    }
    rows = {
        "missed": lambda e: (e["fn"], _fmt_stars(e["stars"]), "+".join(e["fp"]),
                             "+".join(e["case"]) or "—"),
        "incomplete": lambda e: (e["fn"], _fmt_stars(e["stars"]), "+".join(e["interp"]),
                                 "+".join(e["add"]), "+".join(e["add_case"]) or "—"),
        "dual": lambda e: (e["fn"], _fmt_stars(e["stars"]), "+".join(e["dual"])),
    }
    for name in ("missed", "incomplete", "dual"):
        entries = report["lists"][name]
        lines += [f"## {LIST_TITLES[name]} —— {len(entries):,} 仓", "",
                  "| # | 仓 | " + " | ".join(cols[name]) + " |",
                  "|" + "---|" * (len(cols[name]) + 2)]
        for i, e in enumerate(entries[:MD_TOP_N], 1):
            lines.append("| " + " | ".join((str(i),) + rows[name](e)) + " |")
        if len(entries) > MD_TOP_N:
            lines.append(f"\n… 其余 {len(entries) - MD_TOP_N:,} 仓见台账 JSON")
        lines.append("")
    return "\n".join(lines) + "\n"


def write_gap(report: dict, state_dir: Path = STATE_DIR) -> tuple[Path, Path]:
    """台账 + 复核表落盘（JSON 走 atomic_write_json；md tmp+replace，均 LF）。"""
    atomic_write_json(state_dir / GAP_JSON.name, report)
    md = state_dir / GAP_MD.name
    tmp = md.with_suffix(md.suffix + ".tmp")
    tmp.write_text(render_md(report), encoding="utf-8", newline="\n")
    tmp.replace(md)
    return state_dir / GAP_JSON.name, md


def _acceptance_ok(counts: dict) -> list[str]:
    """验收行（10-31 实测 ±10% 下限）；不满则列明——验收是命令不是形容词。"""
    out = []
    for key, label in (("missed", "漏报"), ("incomplete", "不完整"), ("dual", "双源")):
        n, floor = counts[key], ACCEPT_MIN[key]
        out.append(f"{label} {n:,} {'≥' if n >= floor else '<'} {floor:,}"
                   f" {'✓' if n >= floor else '✗'}")
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="适配缺口全池扫描（离线零 API，T2d）")
    ap.add_argument("--gap", action="store_true", help="产出缺口台账+复核表")
    ap.add_argument("--status", action="store_true", help="只打印分布统计")
    ap.add_argument("--limit", type=int, default=None, metavar="N",
                    help="只处理前 N 个证据分片（冒烟；不卡验收线）")
    args = ap.parse_args(argv)
    if not (args.gap or args.status):
        ap.print_usage()
        print("需 --gap 和/或 --status", file=sys.stderr)
        return 2

    report = scan(limit_shards=args.limit)
    u, c = report["universe"], report["counts"]
    print(f"证据 {u.get('evidence', 0):,} 条（ok {u.get('status_ok', 0):,} / "
          f"empty_repo {u.get('status_empty_repo', 0):,} / partial {u.get('status_partial', 0):,}"
          f" / gone {u.get('status_gone', 0):,}）· 池对齐 {u.get('pool_linked', 0):,}")
    print(f"∩ 解读 {u.get('interp_linked', 0):,}（未解读另册 {u.get('interp_missing', 0):,}；"
          f"dbs 空 {u.get('interp_empty', 0):,}）· 指纹命中 {u.get('fp_hit', 0):,}")
    vd = {k: v for k, v in u.items() if k.startswith("verdict_")}
    print("判定分布 " + " ".join(f"{k[8:]}={v:,}" for k, v in sorted(vd.items())))
    if report["case_opened_db"]:
        top = " ".join(f"{db}={n}" for db, n in list(report["case_opened_db"].items())[:8])
        print(f"立案库 Top {top}")
    print(f"缺口：漏报 {c['missed']:,} / 不完整 {c['incomplete']:,} / 双源 {c['dual']:,}")

    if args.gap:
        write_gap(report)
        print(f"台账 {GAP_JSON.name}（三清单全量）+ 复核表 {GAP_MD.name}（top {MD_TOP_N}/清单）")
        if args.limit is None:
            print("验收（10-31 实测 ±10%）：" + " / ".join(_acceptance_ok(c)))
            if any(c[k] < ACCEPT_MIN[k] for k in ACCEPT_MIN):
                return 1                            # 验收不过：数字说话
    return 0


if __name__ == "__main__":
    sys.exit(main())
