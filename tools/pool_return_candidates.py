# -*- coding: utf-8 -*-
"""T0b 历史出池回流候选清单（只读历史 + 产清单，不直接改 pool）。

2026-11-03。卡文：T0 只挡未来误杀；已出池的 sqlc 式仓要捞回——用快照历史差集
生成回流候选清单。输出 state/pool_return_candidates.json（fn/出池类别/当时证据状态/
建议动作：overrides 签发 or 重扫 or 维持）+ markdown 摘要。

口径：
  出池仓 = readme_state（累积状态机，含出池历史仓）− 当前池（data/live/pool.ndjson）
  类别注记：
    10-09 桶剔口径 = 出池 ∩ 已解读 ∩ db_verdicts 空（49767ea9"只留已关联 17 库"，
        按口径重放注记——当时无名单留档，此为重建近似非逐仓名单）
    overrides 签发 = config/overrides.json signed 集（每晚重扫自动回池，b45576c3）
  建议动作（只建议不执行）：
    overrides 签发 —— 解读 dbs 非空（sqlc 式误杀：有归属却出池）
                       或 unattr draft（证据立案草案未签发）
    overrides 签发 —— 引擎指纹可立案（evidence ok + matcher ≥2 票，重扫成本 0）
    重扫 —— 无归属无草案但有 17 库指纹弱信号（evidence 非空，随每晚重扫自然回池）
    维持 —— oos/edu/judged_no_support/无证据/gone（设计内剔除，不捞）

零网络零写池；只写 state/pool_return_candidates.json 与 .md（atomic LF）。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for p in (str(ROOT), str(ROOT / "lib"), str(ROOT / "config")):
    if p not in sys.path:
        sys.path.insert(0, p)

STATE = ROOT / "state"
OUT = STATE / "pool_return_candidates.json"
OUT_MD = STATE / "pool_return_candidates.md"

DB17 = ["PostgreSQL", "MySQL", "Oracle", "SQLite", "SQL Server", "ClickHouse",
        "MariaDB", "TiDB", "OceanBase", "PolarDB", "Dameng", "openGauss",
        "GaussDB", "GBase", "TDSQL", "YashanDB", "GoldenDB"]


def load_pool_now() -> set[str]:
    out: set[str] = set()
    # 只按 \n 切：池里有 4 条记录字符串内含 \r/\u2028 类字符，
    # splitlines() 会从字符串中间切断毁掉整行（line 1 即炸）。
    for line in (ROOT / "data" / "live" / "pool.ndjson").read_text(
            encoding="utf-8").split("\n"):
        line = line.strip()
        if not line:
            continue
        fn = json.loads(line).get("full_name") or ""
        if fn:
            out.add(fn)
    return out


def load_ever() -> dict[str, dict]:
    """readme_state 累积状态机：fn → {status, sha, fetched}（含出池历史仓）。"""
    rs = json.loads((STATE / "readme_state.json").read_text(encoding="utf-8"))
    if isinstance(rs, dict) and "items" not in rs:
        return rs
    items = rs.get("items") or rs.get("repos") or {}
    return {it.get("fn"): it for it in items} if isinstance(items, list) \
        else {fn: it for fn, it in (items.items() if isinstance(items, dict) else [])}


def load_interp_latest() -> dict[str, dict]:
    latest: dict[str, dict] = {}
    for p in sorted((STATE / "interp_cache_shards").glob("*.json")):
        for rec in json.loads(p.read_text(encoding="utf-8")).values():
            fn = rec.get("fn") or ""
            cls = rec.get("classification")
            if not fn or not isinstance(cls, dict):
                continue
            g = rec.get("generated_at") or ""
            cur = latest.get(fn)
            if cur is not None and g < cur["_g"]:
                continue
            latest[fn] = {"dbs": cls.get("dbs") or [],
                          "db_verdicts": cls.get("db_verdicts") or [],
                          "cat": cls.get("cat") or "其他", "_g": g}
    return latest


def load_verdicts() -> dict[str, dict]:
    return json.loads((STATE / "unattr_verdicts.json").read_text(encoding="utf-8"))


def load_evidence_statuses(scope: set[str]) -> dict[str, str]:
    out: dict[str, str] = {}
    for p in sorted((STATE / "evidence_cache_shards").glob("*.json")):
        for rec in json.loads(p.read_text(encoding="utf-8")).values():
            fn = rec.get("fn") or ""
            if fn in scope:
                out[fn] = rec.get("status") or "?"
    return out


def load_overrides() -> tuple[set[str], set[str]]:
    ov = json.loads((ROOT / "config" / "overrides.json").read_text(encoding="utf-8"))
    signed = set()
    for k, v in (ov or {}).items():
        if isinstance(v, dict) and v.get("dbs"):
            signed.add(k)
    # 仓库黑名单 = db_profiles GLOBAL.exclude_repos + 各库档案 + config/exclude_users.txt
    import db_profiles as dp
    bl = set(dp.GLOBAL.get("exclude_repos") or []) \
        | {ex for p in dp.PROFILES for ex in (p.get("exclude_repos") or [])}
    uf = ROOT / "config" / "exclude_users.txt"
    if uf.is_file():
        bl |= {u.strip() for u in uf.read_text(encoding="utf-8-sig").splitlines()
               if u.strip() and not u.startswith("#")}
    return signed, bl


def engine_can_case(fn: str, ev_rec: dict | None, topics: list[str]) -> set[str]:
    """引擎指纹是否可立案（与 writeback 质量门同口径：≥2 票立案）。"""
    try:
        from attribution.api import judge
        from attribution.matcher import build_pack
        v = judge(build_pack(fn, ev_rec, {"topics": topics}))
        if v["status"] == "case_opened":
            chains = [it for e in v["per_db"].values() for it in e["chain"]]
            if any(it["kind"] != "topic" for it in chains):
                return set(v["dbs"])
    except Exception:
        pass
    return set()


def main() -> int:
    pool_now = load_pool_now()
    ever = load_ever()
    out_fns = sorted(set(ever) - pool_now)
    print(f"池 {len(pool_now)} · 累积状态机 {len(ever)} · 出池 {len(out_fns)}", flush=True)

    interp = load_interp_latest()
    verdicts = load_verdicts()
    ev_status = load_evidence_statuses(set(out_fns))
    signed, blocklist = load_overrides()

    # dbhub_page 卡片池（页面在用名单，交叉注记）
    page_fns: set[str] = set()
    pp = Path("D:/dbhub_page/data/pool.js")
    if pp.is_file():
        import re
        s = pp.read_text(encoding="utf-8")
        m = re.search(r"window\.POOL=(\[.*?\]);?\n", s, re.S)
        if m:
            for row in json.loads(m.group(1)):
                if row and isinstance(row[0], str):
                    page_fns.add(row[0])

    cats: dict[str, list[dict]] = {}
    for fn in out_fns:
        ip = interp.get(fn) or {}
        dbs = [d for d in ip.get("dbs") or [] if d in DB17]
        dv = ip.get("db_verdicts") or []
        st = verdicts.get(fn, {}).get("status")
        es = ev_status.get(fn)
        is_signed = fn in signed
        bucket_note = ""
        if ip and not dv:
            bucket_note = "10-09桶剔口径"          # 已解读且 db_verdicts 空

        rec = {"fn": fn,
               "readme": (ever.get(fn) or {}).get("status"),
               "dbs": dbs, "cat": ip.get("cat"),
               "verdict": st, "evidence": es,
               "signed": is_signed, "note": bucket_note,
               "in_page": fn in page_fns, "blocked": fn in blocklist}

        if dbs:
            cats.setdefault("overrides签发·有归属误杀", []).append(rec)
        elif st == "draft":
            cats.setdefault("overrides签发·证据草案", []).append(rec)
        elif es == "ok" and not bucket_note:
            cats.setdefault("重扫·有指纹信号", []).append(rec)
        elif is_signed:
            cats.setdefault("维持·已签发每晚重扫自动回", []).append(rec)
        else:
            cats.setdefault("维持·设计内剔除", []).append(rec)

    payload = {
        "generated_at": __import__("datetime").datetime.now().isoformat(),
        "counts": {"pool": len(pool_now), "ever": len(ever), "out": len(out_fns),
                   **{k: len(v) for k, v in cats.items()}},
        "signed_out": sorted(set(signed) & set(out_fns)),
        "candidates": {k: sorted(v, key=lambda r: -len(r["dbs"])) for k, v in cats.items()},
    }
    tmp = OUT.with_name(OUT.name + ".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=1),
                   encoding="utf-8", newline="\n")
    tmp.replace(OUT)

    lines = ["# T0b 历史出池回流候选清单", "",
             f"生成 {payload['generated_at'][:16]} · 池 {len(pool_now)} · 出池 {len(out_fns)}", "",
             "## 分类计数", ""]
    for k, v in cats.items():
        lines.append(f"- {k}: {len(v)}")
    for k in ("overrides签发·有归属误杀", "overrides签发·证据草案", "重扫·有指纹信号"):
        lines += ["", f"## {k}（Top 30，dbs 数降序）", "",
                  "| 仓 | dbs | cat | 台账/证据 | 页面在用 | 建议 |"]
        for r in payload["candidates"][k][:30]:
            lines.append(f"| {r['fn']} | {','.join(r['dbs'])} | {r['cat']} | "
                         f"{r['verdict'] or '—'}/{r['evidence'] or '—'} | "
                         f"{'✓' if r['in_page'] else ''} | 人工签 or 重扫 |")
    lines += ["", "## 口径注记", "",
              "- 10-09 桶剔无名单留档（49767ea9），按口径重建注记：出池 ∩ 已解读 ∩ "
              "db_verdicts 空。重建是近似，非逐仓当时名单。",
              "- overrides 已签发而暂出池者（b45576c3 的 39 仓同族）每晚重扫自动回池，"
              "本清单归维持不重复建议。",
              "- 清单只建议不执行；回流动作走人工签发/重扫既有机制。"]
    tmp = OUT_MD.with_name(OUT_MD.name + ".tmp")
    tmp.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    tmp.replace(OUT_MD)
    print(f"清单 {OUT}\n摘要 {OUT_MD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
