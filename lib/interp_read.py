# -*- coding: utf-8 -*-
"""interp_read —— 解读写库（A1，工作包清单 v4）。

全仓唯一解读读库定义（《v1存档》§3.3"只此一处"）。消费方一律经本模块取数，
不许各自散落拼装。派生 5 项：

  dbs       归属引擎结果首选（dbs_src.kind=='engine'）；引擎未覆盖的存量条目
            以旧 db_verdicts 组装 fallback（rel∈{support,compat}；mention 仅提及
            不算归属）；两者皆无 → []。来源随结果返回（engine/fallback/None），
            fallback 条目数在 audit 模式单列上报。
  ai_flag   = classification.ai.kind 非空（v4 起 AI 只存 kind，flag 为派生值）。
  activity  活跃度：pool.pushed_at + enrich commit_7d/90d 三信号合成——
            active: commit_90d>0 或 pushed_at≤90d；maintenance: pushed_at≤365d
            （无近期提交仍在维护窗口）；stale: pushed_at>365d；unknown: 无 pool 记录。
  license   pool.license（SPDX 名，无则 None）。
  evidence  引句回查：行号（audit.evidence_lines）+ clean_ver（B1 落地后随写；
            存量条目无 clean_ver 时回查退回存量文本口径=audit.evidence，null 为
            常态非异常——《三方案评审报告 v1》S1）。

索引口径：interp 分片按 sha 键控、一个 fn 可能有多个历史 sha——取 generated_at
最新的条目（工作包清单 A1"dbs 读时算"消费的就是最新解读）。

用法：
  python lib/interp_read.py --audit        # 全量对拍（fallback 条目数上报）
  python lib/interp_read.py --selftest     # 抽 100 条派生一致性 + 活跃度边界单测
"""
from __future__ import annotations

import json
import random
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "state"
INTERP_DIR = STATE / "interp_cache_shards"
ENRICH_DIR = STATE / "enrich_cache_shards"
POOL_PATHS = [ROOT / "data/live/pool.ndjson",
              ROOT / "data/live/pool_cn.ndjson",
              ROOT / "data/live/pool_intl.ndjson"]

# fallback 组装收的 rel：support=明确支持；compat=兼容适配；mention=仅提及不进归属
FALLBACK_RELS = {"support", "compat"}


def _read_json(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def _parse_day(s):
    if not s:
        return None
    try:
        return datetime.strptime(str(s)[:10], "%Y-%m-%d").date()
    except ValueError:
        return None


class InterpReader:
    """按需加载三个数据源，fn（owner/repo）为统一键。"""

    def __init__(self, interp_dir: Path = INTERP_DIR, enrich_dir: Path = ENRICH_DIR,
                 pool_paths: list[Path] | None = None):
        self._interp_dir = Path(interp_dir)
        self._enrich_dir = Path(enrich_dir)
        self._pool_paths = [Path(p) for p in (pool_paths or POOL_PATHS)]
        self._by_fn: dict[str, dict] | None = None     # fn → 最新条目
        self._pool: dict[str, dict] | None = None
        self._enrich: dict[str, dict] | None = None

    # ---- 索引加载（懒加载，只加载一次） ----

    def _load_interp(self) -> dict[str, dict]:
        if self._by_fn is not None:
            return self._by_fn
        idx: dict[str, dict] = {}
        for p in sorted(self._interp_dir.glob("*.json")):
            for _sha, v in _read_json(p).items():
                fn = v.get("fn")
                if not fn:
                    continue
                old = idx.get(fn)
                # generated_at 同日比 sha，保证确定性
                if old is None or (v.get("generated_at", ""), v.get("sha", "")) >= \
                        (old.get("generated_at", ""), old.get("sha", "")):
                    idx[fn] = v
        self._by_fn = idx
        return idx

    def _load_pool(self) -> dict[str, dict]:
        if self._pool is not None:
            return self._pool
        idx: dict[str, dict] = {}
        for path in self._pool_paths:
            if not path.is_file():
                continue
            with path.open(encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        rec = json.loads(line)
                    except json.JSONDecodeError:
                        continue        # pool.ndjson 有内嵌 \r/\u2028 历史脏行，跳过勿断
                    fn = rec.get("full_name")
                    if fn:
                        idx[fn] = rec
        self._pool = idx
        return idx

    def _load_enrich(self) -> dict[str, dict]:
        if self._enrich is not None:
            return self._enrich
        idx: dict[str, dict] = {}
        if self._enrich_dir.is_dir():
            for p in sorted(self._enrich_dir.glob("*.json")):
                for fn, v in _read_json(p).items():
                    if isinstance(v, dict):
                        idx[fn] = v
        self._enrich = idx
        return idx

    # ---- 读接口（消费方只许用这几个） ----

    def has(self, fn: str) -> bool:
        return fn in self._load_interp()

    def entry(self, fn: str) -> dict | None:
        """最新解读原始条目（需要原始字段时用；派生字段走下面几个）。"""
        return self._load_interp().get(fn)

    def dbs(self, fn: str) -> dict:
        """返回 {dbs: [...], src: 'engine'|'fallback'|None}。"""
        v = self.entry(fn)
        if v is None:
            return {"dbs": [], "src": None}
        c = v.get("classification", {})
        if isinstance(c.get("dbs_src"), dict) and c["dbs_src"].get("kind") == "engine":
            return {"dbs": list(c.get("dbs") or []), "src": "engine"}
        verdicts = c.get("db_verdicts") or []
        dbs = [d.get("db") for d in verdicts
               if d.get("db") and d.get("rel") in FALLBACK_RELS]
        # 去重保序
        seen, out = set(), []
        for db in dbs:
            if db not in seen:
                seen.add(db)
                out.append(db)
        return {"dbs": out, "src": "fallback" if out else None}

    def ai_flag(self, fn: str) -> bool:
        v = self.entry(fn)
        if not v:
            return False
        kind = (v.get("classification", {}).get("ai") or {}).get("kind")
        return bool(kind)

    def activity(self, fn: str, as_of: date | None = None) -> dict:
        """活跃度合成。返回 {tier, pushed_at, commit_7d, commit_90d}。

        tier: active（90 天内有推送或有 90d 提交）/ maintenance（365 天内有推送，
        近期无提交）/ stale（超过一年）/ unknown（无 pool 记录）。
        """
        pool = self._load_pool().get(fn)
        if pool is None:
            return {"tier": "unknown", "pushed_at": None,
                    "commit_7d": None, "commit_90d": None}
        today = as_of or date.today()
        pushed = _parse_day(pool.get("pushed_at"))
        enr = self._load_enrich().get(fn) or {}
        c7, c90 = enr.get("commit_7d"), enr.get("commit_90d")
        if pushed is None and c7 is None and c90 is None:
            return {"tier": "unknown", "pushed_at": None,
                    "commit_7d": c7, "commit_90d": c90}
        if (c90 or 0) > 0 or (pushed and (today - pushed).days <= 90):
            tier = "active"
        elif pushed and (today - pushed).days <= 365:
            tier = "maintenance"
        else:
            tier = "stale"
        return {"tier": tier, "pushed_at": pool.get("pushed_at"),
                "commit_7d": c7, "commit_90d": c90}

    def license(self, fn: str) -> str | None:
        pool = self._load_pool().get(fn)
        return (pool or {}).get("license") or None

    def evidence(self, fn: str) -> dict | None:
        """引句回查：行号 + clean_ver + 存量引文（clean_ver 缺失时的回查口径）。"""
        v = self.entry(fn)
        if v is None:
            return None
        audit = v.get("audit", {})
        return {
            "lines": audit.get("evidence_lines") or [],
            "clean_ver": v.get("clean_ver"),          # B1 前为 None（常态非异常）
            "quote": audit.get("evidence") or "",      # 存量文本口径
        }

    def record(self, fn: str) -> dict | None:
        """五合一派生记录（dbs/ai_flag/activity/license/evidence）。"""
        if not self.has(fn):
            return None
        d = self.dbs(fn)
        return {
            "fn": fn,
            "dbs": d["dbs"],
            "dbs_src": d["src"],
            "ai_flag": self.ai_flag(fn),
            "activity": self.activity(fn),
            "license": self.license(fn),
            "evidence": self.evidence(fn),
        }

    # ---- 对拍/统计 ----

    def audit(self) -> dict:
        """全量对拍（A1 验收 1）：dbs 引擎一致 + fallback 条目单列 + ai.flag 派生
        vs 缓存落盘不一致计数。"""
        stats = {"total": 0, "engine": 0, "fallback": 0, "no_signal": 0,
                 "ai_flag_mismatch": 0}
        for fn in self._load_interp():
            stats["total"] += 1
            d = self.dbs(fn)
            stats["engine" if d["src"] == "engine"
                  else "fallback" if d["src"] == "fallback" else "no_signal"] += 1
            v = self.entry(fn)
            stored = (v.get("classification", {}).get("ai") or {}).get("flag")
            if stored is not None and bool(stored) != self.ai_flag(fn):
                stats["ai_flag_mismatch"] += 1
        return stats


# ---- selftest（A1 验收 2/3）----

def _selftest() -> int:
    fails = 0

    def chk(name, cond):
        nonlocal fails
        print(f"[{'PASS' if cond else 'FAIL'}] {name}")
        if not cond:
            fails += 1

    # 1) 合成数据：活跃度边界（7d/90d 各 3 例，A1 验收 3）
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        (tmp / "interp").mkdir(); (tmp / "enrich").mkdir()
        as_of = date(2026, 11, 4)
        mk = lambda days: (as_of - __import__("datetime").timedelta(days=days)).isoformat()
        pool_recs = {
            "a/active7": {"full_name": "a/active7", "pushed_at": mk(7)},      # 7d 边界内
            "a/edge7":   {"full_name": "a/edge7", "pushed_at": mk(8)},        # 7d 边界外→active(≤90d)
            "a/edge90":  {"full_name": "a/edge90", "pushed_at": mk(90)},      # 90d 边界内
            "a/edge91":  {"full_name": "a/edge91", "pushed_at": mk(91)},      # 90d 边界外→maintenance
            "a/edge365": {"full_name": "a/edge365", "pushed_at": mk(365)},    # 365d 边界内
            "a/edge366": {"full_name": "a/edge366", "pushed_at": mk(366)},    # →stale
            "a/commitonly": {"full_name": "a/commitonly", "pushed_at": mk(400)},  # 无近推但有 90d 提交→active
            "a/ghost":   {"full_name": "a/ghost"},                            # 无 pool→unknown
        }
        pool_file = tmp / "pool.ndjson"
        pool_file.write_text("\n".join(json.dumps(r) for r in pool_recs.values()),
                             encoding="utf-8")
        (tmp / "enrich" / "00.json").write_text(json.dumps(
            {"a/commitonly": {"commit_7d": 0, "commit_90d": 3}}), encoding="utf-8")
        entry_tpl = {"fn": "", "classification": {"ai": {"kind": []}},
                     "audit": {"evidence_lines": [3]}}
        (tmp / "interp" / "00.json").write_text(json.dumps(
            {f"sha_{fn}": dict(entry_tpl, fn=fn) for fn in pool_recs},
            ensure_ascii=False), encoding="utf-8")
        r = InterpReader(interp_dir=tmp / "interp", enrich_dir=tmp / "enrich",
                         pool_paths=[pool_file])
        chk("active7 边界（pushed 7d→active）",
            r.activity("a/active7", as_of)["tier"] == "active")
        chk("edge7 边界外（8d→active，非 maintenance）",
            r.activity("a/edge7", as_of)["tier"] == "active")
        chk("edge90 边界内（90d→active）",
            r.activity("a/edge90", as_of)["tier"] == "active")
        chk("edge91 边界外（91d→maintenance）",
            r.activity("a/edge91", as_of)["tier"] == "maintenance")
        chk("edge365 边界内（365d→maintenance）",
            r.activity("a/edge365", as_of)["tier"] == "maintenance")
        chk("edge366 边界外（366d→stale）",
            r.activity("a/edge366", as_of)["tier"] == "stale")
        chk("commitonly（pushed 400d 但 commit_90d=3→active）",
            r.activity("a/commitonly", as_of)["tier"] == "active")
        chk("ghost（无 pool→unknown）",
            r.activity("a/ghost", as_of)["tier"] == "unknown")
        # dbs fallback / ai_flag / evidence clean_ver 缺省
        (tmp / "interp" / "01.json").write_text(json.dumps({
            "sha_fb": {"fn": "a/fb", "classification": {
                "db_verdicts": [
                    {"db": "PostgreSQL", "rel": "support"},
                    {"db": "PostgreSQL", "rel": "support"},      # 去重
                    {"db": "SQLite", "rel": "mention"},          # mention 不进
                    {"db": "MySQL", "rel": "compat"}],           # compat 收
                "ai": {"kind": ["mcp"], "flag": True}},
                "audit": {}},
            "sha_old": {"fn": "a/old", "generated_at": "2026-01-01",
                        "classification": {"db_verdicts": [], "ai": {"kind": [], "flag": False}},
                        "audit": {}},
            "sha_new": {"fn": "a/old", "generated_at": "2026-06-01",
                        "classification": {"db_verdicts": [], "ai": {"kind": [], "flag": False}},
                        "audit": {}},
        }, ensure_ascii=False), encoding="utf-8")
        d = r.dbs("a/fb")
        chk("fallback 组装（support+compat、mention 剔除、去重）",
            d == {"dbs": ["PostgreSQL", "MySQL"], "src": "fallback"})
        chk("ai_flag 派生（kind 非空）", r.ai_flag("a/fb") is True)
        ev = r.evidence("a/fb")
        chk("evidence clean_ver 缺省为 None（存量常态）",
            ev["clean_ver"] is None and ev["lines"] == [])
        chk("同 fn 多 sha 取 generated_at 最新",
            r.entry("a/old")["generated_at"] == "2026-06-01")

    # 2) 真实数据：抽 100 条派生一致性（A1 验收 2）
    real = InterpReader()
    idx = real._load_interp()
    fns = random.Random(42).sample(list(idx), min(100, len(idx)))
    bad = 0
    for fn in fns:
        v = idx[fn]
        c = v.get("classification", {})
        # dbs 一致性：引擎条目读库 == 落盘 dbs；fallback 条目重算两遍一致
        d1, d2 = real.dbs(fn), real.dbs(fn)
        if d1 != d2:
            bad += 1
            continue
        if isinstance(c.get("dbs_src"), dict) and c["dbs_src"].get("kind") == "engine":
            if d1["dbs"] != list(c.get("dbs") or []):
                bad += 1
                continue
        # ai_flag 一致性
        kind = (c.get("ai") or {}).get("kind")
        if real.ai_flag(fn) != bool(kind):
            bad += 1
    chk(f"真实抽样 100 条派生一致（bad={bad}）", bad == 0)
    print(f"[INFO] 引擎覆盖/fallback/无信号分布见 --audit；抽样 {len(fns)} 条")

    return fails


def main() -> int:
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "--audit":
        stats = InterpReader().audit()
        print(json.dumps(stats, ensure_ascii=False, indent=1))
        return 0 if stats["ai_flag_mismatch"] == 0 else 1
    if mode == "--selftest":
        fails = _selftest()
        print(f"selftest {'FAIL' if fails else 'PASS'}（{fails} 处失败）")
        return 1 if fails else 0
    print(__doc__)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
