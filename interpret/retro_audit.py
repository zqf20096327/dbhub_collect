#!/usr/bin/env python3
"""retro_audit.py — 解读缓存重审编排器（判据：裁决覆盖度，非条目版本）。

背景：缓存条目可信的完备判据是「db_verdicts 覆盖 db_scan 当前候选」。db_scan 每窗刷新，
早于候选就绪被解读的条目 = 空判（AI 从未被问过任何库）或半陈旧（漏问新候选）。
本脚本把这类条目（外加 ver<3 且有候选的旧架构条目）从缓存"请出去"，让 interpret.py
按最新候选原样重跑，随后与基线逐条对比出报告。不改动 interpret.py 任何逻辑。

目标判据（latest-per-fn，全部满足才入目标集）：
  ① 缺问库中存在 README 文内可判者（db_scan 候选 - 已裁决库；仅描述来源的候选
     在 v3 行号证据规则下结构性不可判，不烧 API，报告单列"结构性缺口清单"）
  ② fn 在最新 pool 内（出池项 interpret 永不入队，重试无意义）
  ③ readme_state 状态 ∈ (done, oversized)（no_readme 降级项剪掉也不会重新入队）
  ④ 基线 attempts < 3（顽固条目退出目标集，防无限重烧）

安全设计（三层回滚）：
  R1 基线 state/retro_audit_baseline.json 先落盘再动手，捕获目标全部原始缓存键值
     （条目快照只增不覆盖；attempts 为可变元数据）；
  R2 对账规则"剪后存在即新结果"：本轮子进程跑完后仍无任何缓存键的 fn，原键原值写回
     （自动还原，运行中永不丢数据）；启动时先修复上轮崩溃残留（基线在案但缓存为空的 fn）；
  R3 --restore 用基线一键全量回滚（README 变更过的 fn 属尽力还原，精确回滚走 git revert）。

用法：
  python interpret/retro_audit.py --dry-run             # 只读：目标清单/剩余数/不可跑原因
  python interpret/retro_audit.py                       # 重审（--max-items 控制批量）
  python interpret/retro_audit.py --restore             # 全量回滚到基线（可反复执行）
  python interpret/retro_audit.py --restore --dry-run   # 预览回滚影响面，不写盘
"""
from __future__ import annotations

import argparse
import json
import logging
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import sys as _sys
import pathlib as _pl
ROOT = _pl.Path(__file__).resolve().parents[1]
for _d in (ROOT, ROOT / "lib", ROOT / "config", ROOT / "interpret"):
    _sys.path.insert(0, str(_d))
from gh import atomic_write_json, load_env  # noqa: E402  与现管线同一套原子写/环境装载
from interp_store import load_cache  # noqa: E402  分片缓存读取（兼容旧单文件）

load_env()   # 本地跑时读 .env；Actions 由 workflow env 提供（setdefault 不覆盖）

log = logging.getLogger("retro_audit")

CACHE = ROOT / "state" / "interp_cache.json"
SCAN = ROOT / "state" / "db_scan.json"
RSTATE = ROOT / "state" / "readme_state.json"
BASE = ROOT / "state" / "retro_audit_baseline.json"
REPORT_MD = ROOT / "state" / "retro_audit_report.md"
REPORT_JSONL = ROOT / "state" / "retro_audit_report.jsonl"

MAX_ATTEMPTS = 3   # 同一条目最多重审次数（防引句校验顽固丢弃导致无限重烧）

# 17 库清单（与 build_demo.py DB_ORDER 同源的独立副本，避免耦合采集配置）
DB_ORDER = ["PostgreSQL", "MySQL", "Oracle", "SQLite", "SQL Server", "ClickHouse",
            "MariaDB", "TiDB", "OceanBase", "PolarDB", "Dameng", "openGauss",
            "GaussDB", "GBase", "TDSQL", "YashanDB", "GoldenDB"]
DB17 = set(DB_ORDER)

# 库名 → README 文内检索词（宽松子串即可：预筛"模型能否在 README 里找到证据"用，
# 宁可多留目标也不误杀；db_scan 词表更严，此处只是可判性下界）。
DB_PATTERNS = {
    "PostgreSQL": ["postgres"], "MySQL": ["mysql"], "Oracle": ["oracle"],
    "SQLite": ["sqlite"], "SQL Server": ["sql server", "sqlserver", "mssql"],
    "ClickHouse": ["clickhouse"], "MariaDB": ["mariadb"], "TiDB": ["tidb"],
    "OceanBase": ["oceanbase"], "PolarDB": ["polardb"],
    "Dameng": ["dameng", "dm8", "达梦"], "openGauss": ["opengauss"],
    "GaussDB": ["gaussdb"], "GBase": ["gbase"], "TDSQL": ["tdsql"],
    "YashanDB": ["yashan", "崖山"], "GoldenDB": ["goldendb"],
}

_RMD_CACHE: dict = {}


def readme_text(fn: str) -> str:
    """fn 的 README 原文（小写缓存；无文件返回空串）。"""
    if fn not in _RMD_CACHE:
        p = ROOT / "data" / "readmes" / (fn.replace("/", "__") + ".md")
        try:
            _RMD_CACHE[fn] = p.read_text(encoding="utf-8", errors="ignore").lower()
        except OSError:
            _RMD_CACHE[fn] = ""
    return _RMD_CACHE[fn]


def split_missing(fn: str, missing: list) -> tuple[list, list]:
    """缺问库拆为（README 文内可判, 仅描述候选）。
    v3 证据规则要求行号指向 README 可见行，描述来源候选（db_scan line=None）结构性不可判。"""
    text = readme_text(fn)
    in_rd, desc_only = [], []
    for d in missing:
        pats = DB_PATTERNS.get(d, [d.lower()])
        (in_rd if any(p in text for p in pats) else desc_only).append(d)
    return in_rd, desc_only


def jload(p: Path, default):
    if not p.is_file():
        return default
    return json.loads(p.read_text(encoding="utf-8"))


def pool_stars() -> dict:
    """最新快照 pool.json → {full_name: stars}（目标资格 + 排序用，缺失记 0）。"""
    import pool_store
    try:
        items, _src = pool_store.load_latest("pool")
    except FileNotFoundError:
        return {}
    return {it.get("full_name") or "": it.get("stars") or 0
            for it in items}


def fn_cache_keys(cache: dict, fn: str) -> list:
    """该 fn 在缓存里的全部键（sha 键与 desc:: 降级键都算）。"""
    return [k for k, e in cache.items()
            if isinstance(e, dict) and e.get("fn") == fn]


def latest_by_fn(cache: dict) -> dict:
    """{fn: 最新 generated_at 的条目}（同 fn 多键取最新）。"""
    m: dict = {}
    for e in cache.values():
        if not isinstance(e, dict) or not e.get("fn"):
            continue
        cur = m.get(e["fn"])
        if cur is None or (e.get("generated_at") or "") >= (cur.get("generated_at") or ""):
            m[e["fn"]] = e
    return m


def classify(e: dict, scan: dict):
    """→ (ver, 已裁决库集合, 当前候选库列表, 缺问库列表)。"""
    c = e.get("classification") or {}
    judged = {v.get("db") for v in (c.get("db_verdicts") or []) if v.get("db")}
    sc = scan.get(e.get("fn") or "")
    cur = [d for d in ((sc or {}).get("cands") or {}) if d in DB17] if isinstance(sc, dict) else []
    ver = e.get("ver") or c.get("ver") or 3
    return ver, judged, cur, [d for d in cur if d not in judged]


def find_targets(cache: dict, scan: dict, baseline: dict) -> tuple[list, dict]:
    """→ (目标清单[星数降序], 不可跑统计)。幂等：以当前缓存+当前候选+当前池为准。
    仅描述候选（README 文内无据）结构性不可判，不进目标集——重跑必然空判。"""
    stars = pool_stars()
    rstate = (jload(RSTATE, {}).get("items") or jload(RSTATE, {}))
    out, skip = [], {"out_of_pool": 0, "no_readme": 0, "stalled": 0, "desc_only": 0}
    for fn, e in latest_by_fn(cache).items():
        ver, _judged, cur, missing = classify(e, scan)
        in_rd, desc_only = split_missing(fn, missing)
        cur_in_rd, _ = split_missing(fn, cur)
        if not (in_rd or (ver < 3 and cur_in_rd)):
            if missing or (ver < 3 and cur):
                skip["desc_only"] += 1     # 缺问全来自描述候选，v3 行号规则不可判
            continue
        if fn not in stars:
            skip["out_of_pool"] += 1          # interpret 永不入队，重试无意义
            continue
        rs = rstate.get(fn) or {}
        if rs.get("status") not in ("done", "oversized"):
            skip["no_readme"] += 1            # 降级项剪掉也不会重新入队
            continue
        if baseline.get(fn, {}).get("attempts", 0) >= MAX_ATTEMPTS:
            skip["stalled"] += 1              # 顽固条目退出，防无限重烧
            continue
        out.append({"fn": fn, "ver": ver, "missing": in_rd,
                    "desc_only": desc_only, "stars": stars.get(fn, 0)})
    out.sort(key=lambda x: -x["stars"])
    return out, skip


def build_baseline(cache: dict, batch: list, baseline: dict) -> int:
    """捕获目标 fn 的全部原始缓存键值（含旧 sha 历史键）；条目快照只增不覆盖。
    attempts 为可变元数据（每轮 +1）。返回新增 fn 数。"""
    added = 0
    for t in batch:
        fn = t["fn"]
        if fn not in baseline:
            keys = fn_cache_keys(cache, fn)
            if not keys:
                log.warning("基线跳过 %s：缓存中无键（异常，请人工核查）", fn)
                continue
            latest_key = max(keys, key=lambda k: cache[k].get("generated_at") or "")
            c = cache[latest_key].get("classification") or {}
            baseline[fn] = {
                "captured": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                "key": latest_key,
                "keys_entry": {k: cache[k] for k in keys},   # 全键全值快照（还原用）
                "ver": t["ver"], "missing_then": t["missing"],
                "desc_only_then": t.get("desc_only", []),
                "dbs_then": list(c.get("dbs") or []),
                "cat_then": c.get("cat") or "",
                "attempts": 0,
            }
            added += 1
        baseline[fn]["attempts"] = baseline[fn].get("attempts", 0) + 1
    return added


def restore_fn(cache: dict, b: dict) -> None:
    """原键原值写回一个 fn 的全部缓存条目。"""
    for k, entry in (b.get("keys_entry") or {}).items():
        cache[k] = entry


def run_interpret(batch_n: int, concurrency: int, max_minutes: float) -> int:
    """子进程跑现管线。始终 --retry-rejected：目标被拒后下轮仍能再进队。
    max-items 余量 = min(batch, 300)：吸收"从未解读项"按星数插队，又不让小批验证变慢。"""
    cmd = [sys.executable, str(ROOT / "interpret" / "interpret.py"),
           "--concurrency", str(concurrency),
           "--max-items", str(batch_n + min(batch_n, 300)),
           "--max-minutes", str(max_minutes),
           "--retry-rejected"]
    log.info("子进程：%s", " ".join(cmd))
    p = subprocess.run(cmd, cwd=str(ROOT))
    if p.returncode != 0:
        log.warning("interpret.py 退出码 %s（照常对账，未完成项自动还原）", p.returncode)
    return p.returncode


def report(baseline: dict, scan: dict) -> dict:
    """全量重生成报告（幂等）。三态：done / pending（仍在目标集）/ skipped（不可跑）。"""
    cache = load_cache()
    byfn = latest_by_fn(cache)
    stars = pool_stars()
    rstate = (jload(RSTATE, {}).get("items") or jload(RSTATE, {}))
    rows, done, pending, skipped, over9 = [], 0, 0, 0, []
    for fn, b in baseline.items():
        e = byfn.get(fn)
        ver, _j, _cur, missing = classify(e, scan) if e else (b["ver"], set(), [], [])
        in_rd_now, desc_now = split_missing(fn, missing)
        c_now = (e.get("classification") or {}) if e else {}
        dbs_now = list(c_now.get("dbs") or [])
        covered = bool(e) and not in_rd_now and ver >= 3   # 文内可判项补齐即达标
        if covered:
            status = "done"
            done += 1
        elif fn not in stars or (rstate.get(fn) or {}).get("status") not in ("done", "oversized"):
            status = "skipped"
            skipped += 1
        elif b.get("attempts", 0) >= MAX_ATTEMPTS:
            status = "stalled"
            skipped += 1
        else:
            status = "pending"
            pending += 1
        if len(dbs_now) > 9:
            over9.append({"fn": fn, "n": len(dbs_now)})
        rows.append({
            "fn": fn, "stars": stars.get(fn, 0), "status": status, "ver": ver,
            "attempts": b.get("attempts", 0),
            "missing_then": b["missing_then"],
            "missing_desc_only": desc_now or b.get("desc_only_then", []),
            "missing_now": missing,
            "dbs_then": b["dbs_then"], "dbs_now": dbs_now,
            "verdicts_now": [{"db": v.get("db"), "rel": v.get("rel")}
                             for v in (c_now.get("db_verdicts") or [])],
            "cat_then": b["cat_then"], "cat_now": c_now.get("cat") or "",
            "conf": ((e.get("audit") or {}).get("confidence")) if e else None,
        })
    rows.sort(key=lambda r: (r["status"] == "done", -r["stars"]))
    return {"targets": len(baseline), "done": done, "pending": pending,
            "skipped": skipped, "over9": over9, "rows": rows}


def write_report(s: dict) -> None:
    REPORT_JSONL.write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in s["rows"]) + "\n",
        encoding="utf-8")
    done_rows = [r for r in s["rows"] if r["status"] == "done"]
    newly = [r for r in done_rows if r["dbs_now"] and not r["dbs_then"]]
    widened = [r for r in done_rows if r["dbs_now"] and r["dbs_then"]
               and set(r["dbs_now"]) != set(r["dbs_then"])]
    catflip = [r for r in done_rows if r["cat_then"] and r["cat_now"]
               and r["cat_then"] != r["cat_now"]]
    lines = [
        "# retro_audit 重审报告（候选覆盖度判据）",
        f"生成：{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        "",
        f"- 基线 {s['targets']} 条：**已完成 {s['done']}** · 待续跑 {s['pending']}"
        f"（再触发直到=0）· 不可跑/停滞 {s['skipped']}（出池/no_readme/超重试上限）",
        f"- 归属新增（旧空 → 新有）：{len(newly)} 条",
        f"- 归属变化（宽度/构成）：{len(widened)} 条",
        f"- 类别翻转：{len(catflip)} 条",
        f"- **>9 库归属（护栏改造的审计底册）**：{len(s['over9'])} 条",
    ]
    lines += [f"  - {o['fn']}（{o['n']} 库）" for o in s["over9"]]
    struct = [r for r in s["rows"] if r.get("missing_desc_only")]
    lines += ["", "## 结构性缺口清单（候选来自描述、v3 行号规则不可判——interpret 提示词改进工单）", ""]
    lines += [f"- {r['fn']}：缺问 {','.join(r['missing_desc_only'])}" for r in struct[:30]]
    if len(struct) > 30:
        lines.append(f"- …共 {len(struct)} 条，全量见 jsonl 的 missing_desc_only 字段")
    lines += ["", "## 归属新增明细（Top 50）", ""]
    lines += [f"- {r['fn']} → {','.join(r['dbs_now'])}"
              f"（补判 {','.join(r['missing_then']) or '无'}）" for r in newly[:50]]
    lines += ["", "## 归属变化明细（Top 50）", ""]
    lines += [f"- {r['fn']}：{','.join(r['dbs_then']) or '空'} →"
              f" {','.join(r['dbs_now'])}（补判 {','.join(r['missing_then'])}）"
              for r in widened[:50]]
    lines += ["", "## 类别翻转明细（Top 20）", ""]
    lines += [f"- {r['fn']}：{r['cat_then']} → {r['cat_now']}" for r in catflip[:20]]
    lines += ["", "逐条明细见 retro_audit_report.jsonl（status 含 pending/skipped/stalled）。"]
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    log.info("报告已写：%s / %s", REPORT_MD.name, REPORT_JSONL.name)


def main():
    ap = argparse.ArgumentParser(description="解读缓存重审编排器（覆盖度判据）")
    ap.add_argument("--concurrency", type=int, default=4)
    ap.add_argument("--max-items", type=int, default=0, help="0=本轮全量目标")
    ap.add_argument("--max-minutes", type=float, default=90.0)
    ap.add_argument("--dry-run", action="store_true", help="只读，不写任何文件")
    ap.add_argument("--restore", action="store_true",
                    help="用基线全量回滚（可反复执行；--dry-run 预览）")
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)-6s %(name)s | %(message)s",
                        datefmt="%H:%M:%S")

    cache = load_cache()
    scan = jload(SCAN, {})
    baseline = jload(BASE, {})

    # ── R3 全量回滚模式 ──────────────────────────────────────────────────
    if args.restore:
        if args.dry_run:
            n_keys = sum(len(b.get("keys_entry") or {}) for b in baseline.values())
            log.info("[dry-run] 回滚将还原 %d 个 fn / %d 个缓存键（不写盘）",
                     len(baseline), n_keys)
            return
        for b in baseline.values():
            restore_fn(cache, b)
        atomic_write_json(CACHE, cache)
        log.info("已全量回滚 %d 个 fn（基线保留；README 变更过的属尽力还原，"
                 "精确回滚走 git revert）", len(baseline))
        return

    # ── R2 启动修复：基线在案但缓存为空 = 上轮剪后崩溃残留，先原样写回 ────
    leaked = [fn for fn in baseline if not fn_cache_keys(cache, fn)]
    if leaked:
        log.info("发现上轮崩溃残留 %d 个 fn，先还原到一致状态", len(leaked))
        for fn in leaked:
            restore_fn(cache, baseline[fn])
        if not args.dry_run:
            atomic_write_json(CACHE, cache)

    # ── 目标识别（幂等：缓存+候选+池+readme_state 四要素） ───────────────
    targets, skip = find_targets(cache, scan, baseline)
    batch = targets if args.max_items <= 0 else targets[:args.max_items]
    log.info("重审目标 %d 条（本轮 batch %d）· 不可跑跳过 %s",
             len(targets), len(batch), skip)
    for t in batch[:20]:
        log.info("  %-44s ★%-7d 缺问:%s", t["fn"], t["stars"],
                 ",".join(t["missing"]) or f"(ver{t['ver']}→3)")

    if args.dry_run:
        log.info("[dry-run] 剩余 %d 条待重审（不写盘、不调 API）", len(targets))
        return

    # ── R1 基线先落盘，再剪缓存 ─────────────────────────────────────────
    added = build_baseline(cache, batch, baseline)
    atomic_write_json(BASE, baseline)
    log.info("基线 +%d（累计 %d 个 fn 在案，先落盘再动手）", added, len(baseline))

    for t in batch:
        for k in fn_cache_keys(cache, t["fn"]):
            del cache[k]
    atomic_write_json(CACHE, cache)
    log.info("已剪出 %d 个 fn 的缓存条目，交给 interpret.py 重跑", len(batch))

    # ── 子进程重跑（v3 默认；--retry-rejected 保证拒收项下轮可再战） ─────
    t0 = time.time()
    run_interpret(len(batch), args.concurrency, args.max_minutes)

    # ── R2 对账："剪后存在即新结果"；无键者原键原值写回 ───────────────────
    cache = load_cache()      # 子进程已按 chunk 落盘，重新装载
    done = restored = 0
    for t in batch:
        b = baseline.get(t["fn"])
        if not b:
            continue
        if fn_cache_keys(cache, t["fn"]):
            done += 1
        else:
            restore_fn(cache, b)
            restored += 1
    atomic_write_json(CACHE, cache)
    log.info("对账：本轮完成 %d · 自动还原 %d（下轮自动再战）· 用时 %.0f 分钟",
             done, restored, (time.time() - t0) / 60)

    # ── 报告（幂等全量重生成） ───────────────────────────────────────────
    s = report(baseline, scan)
    write_report(s)
    log.info("==== 重审收官判定：基线 %d · 已完成 %d · 待续跑 %d · 不可跑/停滞 %d"
             "（待续跑=0 即收官）====", s["targets"], s["done"], s["pending"], s["skipped"])


if __name__ == "__main__":
    main()
