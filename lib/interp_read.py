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
            滚动窗口兜底：commit_7d/90d 是采集时点的窗口计数，enrich 的 push 闸门
            不会重采死仓，最后推送早于窗口时按真值 0 处理（防假活跃）。
  license   pool.license（SPDX 名，无则 None）。
  evidence  引句回查：行号（audit.evidence_lines）+ clean_ver（B1 落地后随写；
            存量条目无 clean_ver 时回查退回存量文本口径=audit.evidence，null 为
            常态非异常——《三方案评审报告 v1》S1）。

索引口径（G1-2 多卷合并）：台账 `interp_state.json` 的 fn→sha 是唯一权威连接，
缓存按 sha 键控、一个 fn 可能有多个历史 sha。旧实现按条目里的 fn 取"最新一条"，
v4 判定卷与 v4t 文本卷会互相遮蔽（实测 1,318 个头部仓只剩 38 个读到分类），
且内容 sha 镜像共享的仓（同 README 不同仓）取不到条目。现按层合并：

  fn --台账--> sha --interp_keys--> {judge, text, vocab, legacy, desc}
  分类取 judge > legacy > desc；身份取 text > legacy > desc；domain_tags 取 vocab

台账里没有的 fn（出池/历史）退回条目自带的 fn 建索引，同 fn 取 generated_at 最新。

用法：
  python lib/interp_read.py --audit        # 全量对拍（层覆盖 + fallback 条目数上报）
  python lib/interp_read.py --selftest     # 合成三卷用例 + 真实抽样
"""
from __future__ import annotations

import json
import random
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "state"
INTERP_DIR = STATE / "interp_cache_shards"
LEDGER = STATE / "interp_state.json"
ENRICH_DIR = STATE / "enrich_cache_shards"
POOL_PATHS = [ROOT / "data/live/pool.ndjson",
              ROOT / "data/live/pool_cn.ndjson",
              ROOT / "data/live/pool_intl.ndjson"]

import interp_keys as ik                      # noqa: E402  层键契约（G1-1）
import interp_layer_store as ils              # noqa: E402  分层存储（G1-6）

# fallback 组装收的 rel：support=明确支持；compat=兼容适配；mention=仅提及不进归属
FALLBACK_RELS = {"support", "compat"}
# v4 ai_kind 的 AI 取値：other=非 AI（提示词要求非 AI 仓也必须输出 other），
# 其余四类才是 AI 项目。旧代 ai.kind 非空即 AI，两套口径在此统一。
AI_KINDS = {"mcp", "rag", "text2sql", "dba-agent"}
# pushed_at 最大滞后（org 周扫携带 7 天 + 池扫描 1 天，与 enrich.POOL_LAG_DAYS 同源）：
# 推导"窗口内必无提交"必须让过这段滞后，否则活仓会被误判成 0
POOL_LAG_DAYS = 8


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
                 pool_paths: list[Path] | None = None, ledger: Path = LEDGER,
                 layer_base: Path = ils.LAYER_ROOT):
        self._interp_dir = Path(interp_dir)
        self._layer_base = Path(layer_base)
        self._enrich_dir = Path(enrich_dir)
        self._pool_paths = [Path(p) for p in (pool_paths or POOL_PATHS)]
        self._ledger_path = Path(ledger)
        self._by_fn: dict[str, dict] | None = None     # fn → {sha, layers}
        self._cache: dict[str, dict] | None = None     # 层键 → 条目
        self._pool: dict[str, dict] | None = None
        self._enrich: dict[str, dict] | None = None

    # ---- 索引加载（懒加载，只加载一次） ----

    def _load_cache(self) -> dict[str, dict]:
        """旧单目录（带后缀键）+ 新分层目录（裸 sha），统一成后缀键的内存视图。

        新布局后写先读：同 sha 若两处都有，新目录覆盖旧目录（搬迁后以新为准）。
        desc 层键本身就是 desc::<摘要>，直接并入，无需加后缀。
        """
        if self._cache is not None:
            return self._cache
        cache: dict[str, dict] = {}
        for p in sorted(self._interp_dir.glob("*.json")):
            shard = _read_json(p)
            if isinstance(shard, dict):
                cache.update(shard)
        for layer, suffix in (("judge", ik.JUDGE_KEY_SUFFIX),
                              ("text", ik.TEXT_KEY_SUFFIX),
                              ("domain_tags", ik.VOCAB_KEY_SUFFIX)):
            d = self._layer_base / layer / "shards"
            if d.is_dir():
                for p in sorted(d.glob("*.json")):
                    for sha, obj in (_read_json(p) or {}).items():
                        cache[sha + suffix] = obj
        d = self._layer_base / "desc" / "shards"
        if d.is_dir():
            for p in sorted(d.glob("*.json")):
                shard = _read_json(p)
                if isinstance(shard, dict):
                    cache.update(shard)
        self._cache = cache
        return cache

    def _load_ledger(self) -> dict[str, str]:
        if not self._ledger_path.is_file():
            return {}
        items = (_read_json(self._ledger_path) or {}).get("items") or {}
        return {fn: (v or {}).get("sha") for fn, v in items.items() if (v or {}).get("sha")}

    def _layers_for(self, sha: str, cache: dict[str, dict]) -> dict[str, dict | None]:
        """一个 sha 的六种层载荷（形态不符视为缺层）。"""
        out: dict[str, dict | None] = {k: None for k in
                                       ("judge", "text", "vocab", "legacy", "desc", "desc_legacy")}
        if not sha:
            return out
        if sha.startswith(ik.DESC_PREFIX):
            # desc 键：新方案 desc::<12位摘要> 收 desc；旧 desc::<描述> 收 desc_legacy
            layer, _ = ik.parse_key(sha)
            obj = cache.get(sha)
            if obj is not None and ik.accepts(layer, ik.entry_shape(obj)):
                out[layer] = obj
            return out
        for layer, key in (("judge", ik.judge_key(sha)), ("text", ik.text_key(sha)),
                           ("vocab", ik.vocab_key(sha)), ("legacy", ik.legacy_key(sha))):
            obj = cache.get(key)
            if obj is not None and ik.accepts(layer, ik.entry_shape(obj)):
                out[layer] = obj
        return out

    def _load_interp(self) -> dict[str, dict]:
        if self._by_fn is not None:
            return self._by_fn
        cache = self._load_cache()
        idx: dict[str, dict] = {}
        for fn, sha in self._load_ledger().items():
            idx[fn] = {"sha": sha, "layers": self._layers_for(sha, cache)}
        # 台账外的 fn（出池/历史）：用条目自带 fn 建索引，同 fn 取 generated_at 最新
        extra: dict[str, tuple[str, str]] = {}      # fn → (generated_at, sha)
        for key, v in cache.items():
            if not isinstance(v, dict):
                continue
            fn = v.get("fn")
            if not fn or fn in idx:
                continue
            layer, sha = ik.parse_key(key)
            if layer == "unknown":
                continue
            cand = (str(v.get("generated_at") or ""), sha)
            if fn not in extra or cand >= extra[fn]:
                extra[fn] = cand
        for fn, (_gen, sha) in extra.items():
            idx[fn] = {"sha": sha, "layers": self._layers_for(sha, cache)}
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

    def layers(self, fn: str) -> dict[str, dict | None]:
        """该仓六种层载荷（judge/text/vocab/legacy/desc/desc_legacy），缺层为 None。"""
        rec = self._load_interp().get(fn)
        empty = {k: None for k in
                 ("judge", "text", "vocab", "legacy", "desc", "desc_legacy")}
        return dict(rec["layers"]) if rec else empty

    def sha(self, fn: str) -> str | None:
        rec = self._load_interp().get(fn)
        return rec["sha"] if rec else None

    def entry(self, fn: str) -> dict | None:
        """分类来源（判定卷优先）：judge(v4) > legacy(v3) > desc > desc_legacy。"""
        L = self.layers(fn)
        for layer in ("judge", "legacy", "desc", "desc_legacy"):
            if L.get(layer):
                return L[layer]
        return None

    def identity(self, fn: str) -> dict | None:
        """身份来源（文本卷优先）：text(v4t) > legacy(v3) > desc > desc_legacy。"""
        L = self.layers(fn)
        for layer in ("text", "legacy", "desc", "desc_legacy"):
            if L.get(layer):
                return L[layer]
        return None

    def domain_tags(self, fn: str) -> dict | None:
        """受控词表标签（vc1.0）；未跑或拒收返回 None。"""
        return self.layers(fn).get("vocab")

    def dbs(self, fn: str) -> dict:
        """归属引擎结果。返回 {dbs, src, reason}。

        来源优先级（G1-3）：
          1) judge 层 dbs 非空 —— 程序适配结果（v4 禁 AI 写 db，有值必是程序填的）
          2) legacy 层 dbs_src.kind=='engine' —— T4b 程序适配（存量 2,179 条）
          3) legacy 层 db_verdicts 组装 fallback（rel∈support/compat，mention 不算）
          4) 皆无 → []，reason 取 judge 的 dbs_empty_reason（可解释"为什么没有"）
        旧版优先取"最新条目"，v4 判定卷没有 dbs_src 就把引擎结果全丢了（1,963→30）。
        """
        L = self.layers(fn)
        j = L.get("judge")
        reason = None
        if j is not None:
            c = j.get("classification") or {}
            # 判定卷带 dbs 字段（哪怕空数组）= 程序适配已就该 sha 给出结论，以它为准；
            # 空数组 + 原因比旧代的 engine 结果新，不能拿旧值覆盖。
            if "dbs" in c or "dbs_empty_reason" in c:
                dbs = [d for d in (c.get("dbs") or []) if d]
                return {"dbs": dbs, "src": "engine" if dbs else None,
                        "reason": c.get("dbs_empty_reason")}
            reason = c.get("dbs_empty_reason")
        v = None
        for layer in ("legacy", "desc", "desc_legacy"):
            if L.get(layer):
                v = L[layer]
                break
        if v is None:
            return {"dbs": [], "src": None, "reason": reason}
        c = v.get("classification") or {}
        if isinstance(c.get("dbs_src"), dict) and c["dbs_src"].get("kind") == "engine":
            return {"dbs": list(c.get("dbs") or []), "src": "engine", "reason": None}
        verdicts = c.get("db_verdicts") or []
        dbs = [d.get("db") for d in verdicts
               if d.get("db") and d.get("rel") in FALLBACK_RELS]
        # 去重保序
        seen, out = set(), []
        for db in dbs:
            if db not in seen:
                seen.add(db)
                out.append(db)
        return {"dbs": out, "src": "fallback" if out else None,
                "reason": reason or c.get("dbs_empty_reason")}

    def ai_flag(self, fn: str) -> bool:
        """AI 项目标记。判定卷看 ai_kind（other=非 AI），旧代看 ai.kind 非空。"""
        L = self.layers(fn)
        j = L.get("judge")
        if j is not None:
            k = (j.get("classification") or {}).get("ai_kind")
            if k is not None:
                return k in AI_KINDS
        v = None
        for layer in ("legacy", "desc", "desc_legacy"):
            if L.get(layer):
                v = L[layer]
                break
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
        # 滚动窗口衰减（enrich 的 push 闸门不重采死仓，这里兜底）：最后推送早于
        # 窗口+池滞后 ⇒ 窗口内必无提交，计数真值为 0。日期粒度，保守判定。
        if pushed is not None:
            age = (today - pushed).days
            if age > 7 + POOL_LAG_DAYS and c7:
                c7 = 0
            if age > 90 + POOL_LAG_DAYS and c90:
                c90 = 0
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
        """派生记录：五合一（dbs/ai_flag/activity/license/evidence）+ 三卷内容。"""
        if not self.has(fn):
            return None
        d = self.dbs(fn)
        L = self.layers(fn)
        return {
            "fn": fn,
            "sha": self.sha(fn),
            "dbs": d["dbs"],
            "dbs_src": d["src"],
            "dbs_reason": d["reason"],
            "ai_flag": self.ai_flag(fn),
            "activity": self.activity(fn),
            "license": self.license(fn),
            "evidence": self.evidence(fn),
            "identity": self.identity(fn),
            "domain_tags": self.domain_tags(fn),
            "layers": {k: (v is not None) for k, v in L.items()},
        }

    # ---- 对拍/统计 ----

    def audit(self) -> dict:
        """全量对拍：层覆盖 + dbs 引擎一致 + fallback 单列 + ai_flag 不一致计数。"""
        stats = {"total": 0, "engine": 0, "fallback": 0, "no_signal": 0,
                 "ai_flag_mismatch": 0,
                 "class_readable": 0, "identity_readable": 0, "tags": 0,
                 "judge": 0, "text": 0, "vocab": 0, "legacy_fallback": 0}
        for fn in self._load_interp():
            stats["total"] += 1
            d = self.dbs(fn)
            stats["engine" if d["src"] == "engine"
                  else "fallback" if d["src"] == "fallback" else "no_signal"] += 1
            L = self.layers(fn)
            for k in ("judge", "text", "vocab"):
                if L.get(k):
                    stats[k] += 1
            if L.get("legacy"):
                stats["legacy_fallback"] += 1
            if self.entry(fn) is not None:
                stats["class_readable"] += 1
            if self.identity(fn) is not None:
                stats["identity_readable"] += 1
            if self.domain_tags(fn) is not None:
                stats["tags"] += 1
            v = self.entry(fn)
            if v is not None:
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
            "a/commitonly": {"full_name": "a/commitonly", "pushed_at": mk(400)},  # 冻结的 90d 计数必须衰减
            "a/commitonlynopush": {"full_name": "a/commitonlynopush"},       # 无 pushed_at：只剩 enrich 提交信号
            "a/ghost":   {"full_name": "a/ghost"},                            # 无 pool→unknown
        }
        pool_file = tmp / "pool.ndjson"
        pool_file.write_text("\n".join(json.dumps(r) for r in pool_recs.values()),
                             encoding="utf-8")
        (tmp / "enrich" / "00.json").write_text(json.dumps(
            {"a/commitonly": {"commit_7d": 0, "commit_90d": 3},
             "a/commitonlynopush": {"commit_7d": 0, "commit_90d": 3}}), encoding="utf-8")
        # 1b) 多卷合并（G1-2）：台账 fn→sha 是权威连接，按层取条目
        S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12, S13 = (
            f"{i:064x}" for i in range(1, 14))
        S14, S15, S16, S17, S18, S19, S20 = (f"{i:064x}" for i in range(14, 21))
        DSP2 = "desc::0123456789ab"
        DSP = "desc::abcdef123456"

        def v4(fn, sha, **cls):
            return {"fn": fn, "sha": sha, "generated_at": "2026-11-01",
                    "classification": {"cat_primary": "开发库", **cls},
                    "signals": {}, "audit": {"evidence_lines": [1]}}

        def txt(fn, sha, one="一句话"):
            return {"fn": fn, "sha": sha, "generated_at": "2026-11-01", "layer": "text",
                    "identity": {"one_liner": one, "review": "x" * 40,
                                 "highlights": ["h"], "use_cases": ["u"]}}

        def v3(fn, sha, cls=None):
            return {"fn": fn, "sha": sha, "generated_at": "2026-01-01",
                    "identity": {"one_liner": "old"},
                    "classification": cls if cls is not None else {"ai": {"kind": []}},
                    "audit": {}}

        entries = {
            # 三卷齐全
            ik.judge_key(S1): v4("a/three", S1),
            ik.text_key(S1): txt("a/three", S1),
            ik.vocab_key(S1): {"fn": "a/three", "sha": S1,
                               "tags": [{"slug": "cdc"}], "abstain": None},
            S1: v3("a/three", S1),
            # 只有旧代
            S2: v3("a/dual", S2),
            # 旧代 + 文本卷（旧读层会互相遮蔽）
            S3: v3("a/shadow", S3),
            ik.text_key(S3): txt("a/shadow", S3, "文本卷一句话"),
            # desc 新方案：合并条目（source=desc）
            DSP: {"fn": "a/desc", "sha": DSP, "source": "desc",
                  "identity": {"one_liner": "desc 段一句话"},
                  "classification": {"cat_primary": "开发库"}},
            # #v4 里装 v3：形态不符必须当缺层
            ik.judge_key(S4): v3("a/mismatch", S4),
            # 台账权威：S6 更新但台账指向 S5
            S5: dict(v3("a/old", S5), generated_at="2026-01-01"),
            S6: dict(v3("a/old", S6), generated_at="2026-06-01"),
            # 内容镜像：两个 fn 共用同 sha，只有一条带 fn
            ik.judge_key(S7): v4("a/m1", S7),
            # fallback dbs / ai_flag 存量口径
            S8: v3("a/fb", S8, {"db_verdicts": [
                {"db": "PostgreSQL", "rel": "support"},
                {"db": "PostgreSQL", "rel": "support"},      # 去重
                {"db": "SQLite", "rel": "mention"},          # mention 不进
                {"db": "MySQL", "rel": "compat"}],           # compat 收
                "ai": {"kind": ["mcp"], "flag": True}}),
            # 旧 desc 键（v3 结构，desc_legacy 层）
            "desc::A bot for SQL": v3("a/olddesc", "desc::A bot for SQL"),
            # ai_kind 口径：other 不算 AI
            ik.judge_key(S10): v4("a/aikind_ai", S10, ai_kind="mcp"),
            ik.judge_key(S11): v4("a/aikind_other", S11, ai_kind="other"),
            # 判定卷程序字段优先于旧代 engine
            ik.judge_key(S12): v4("a/judge_dbs", S12, dbs=["TiDB"]),
            S12: v3("a/judge_dbs", S12, {"dbs_src": {"kind": "engine"}, "dbs": ["MySQL"]}),
            # 判定卷显式空结论（带原因）不被旧代覆盖
            ik.judge_key(S13): v4("a/judge_empty", S13, dbs=[],
                                  dbs_empty_reason={"reason": "证据不足"}),
            S13: v3("a/judge_empty", S13, {"dbs_src": {"kind": "engine"}, "dbs": ["MySQL"]}),
            # 缺卷 / 双卷 / 形态不符 / desc 新旧并存（G1-4）
            ik.text_key(S14): txt("a/onlytext", S14),                    # 只有文本卷
            ik.judge_key(S15): v4("a/onlyjudge", S15),                   # 只有判定卷
            ik.judge_key(S16): v4("a/conflict", S16, cat_primary="监控"),  # 双卷冲突
            S16: v3("a/conflict", S16),                                  # 旧代身份应让位
            ik.text_key(S17): v4("a/textbad", S17),                      # 文本键装 v4：形态不符
            ik.vocab_key(S18): {"fn": "a/vocabonly", "sha": S18,
                                "tags": [{"slug": "cdc"}], "abstain": None},
            # 新 desc 键（v4 形态也可）+ 旧 desc 键并存，台账指向新键
            DSP2: {"fn": "a/desc2", "sha": DSP2, "source": "desc", "generated_at": "2026-11-07",
                   "identity": {"one_liner": "新 desc"},
                   "classification": {"cat_primary": "开发库"}},
            "desc::旧描述文本": v3("a/desc2", "desc::旧描述文本"),
            # 台账指向普通 sha，但缓存里另有该仓的 desc 条目（不得串用）
            ik.judge_key(S19): v4("a/normal", S19),
            "desc::另一个描述": v3("a/normal", "desc::另一个描述"),
            # 形态不符：legacy 键装 v4（v3 层不认 v4）
            S20: v4("a/legacybad", S20),
        }
        (tmp / "interp" / "00.json").write_text(
            json.dumps(entries, ensure_ascii=False), encoding="utf-8")
        ledger = {"items": {
            "a/three": {"sha": S1}, "a/dual": {"sha": S2}, "a/shadow": {"sha": S3},
            "a/desc": {"sha": DSP}, "a/mismatch": {"sha": S4},
            "a/old": {"sha": S5},                        # 台账权威：不认更新的 S6
            "a/m1": {"sha": S7}, "a/m2": {"sha": S7},    # 内容镜像共享同 sha
            "a/fb": {"sha": S8},
            "a/olddesc": {"sha": "desc::A bot for SQL"},
            "a/none": {"sha": S9},                       # 缓存里没有任何层
            "a/aikind_ai": {"sha": S10}, "a/aikind_other": {"sha": S11},
            "a/judge_dbs": {"sha": S12}, "a/judge_empty": {"sha": S13},
            "a/onlytext": {"sha": S14}, "a/onlyjudge": {"sha": S15},
            "a/conflict": {"sha": S16}, "a/textbad": {"sha": S17},
            "a/vocabonly": {"sha": S18}, "a/desc2": {"sha": DSP2},
            "a/normal": {"sha": S19}, "a/legacybad": {"sha": S20},
        }}
        # 1c) 新分层布局（G1-6）：裸 sha 键 + 层目录；旧目录同 sha 时新布局优先
        S21, S22, S23 = (f"{i:064x}" for i in range(21, 24))
        DSP3 = "desc::fedcba987654"
        lb = tmp / "layers"
        for sub in ("judge", "text", "domain_tags", "desc"):
            (lb / sub / "shards").mkdir(parents=True)
        (lb / "judge" / "shards" / "aa.json").write_text(json.dumps({
            S21: {"sha": S21, "classification": {"cat_primary": "平台"},
                  "generated_at": "2026-11-07"},
            S22: {"sha": S22, "classification": {"cat_primary": "监控"},
                  "generated_at": "2026-11-07"},
        }, ensure_ascii=False), encoding="utf-8")
        (lb / "text" / "shards" / "aa.json").write_text(json.dumps({
            S21: {"sha": S21, "identity": {"one_liner": "新布局文本"}},
        }, ensure_ascii=False), encoding="utf-8")
        (lb / "domain_tags" / "shards" / "aa.json").write_text(json.dumps({
            S21: {"sha": S21, "tags": [{"slug": "cdc", "line": 2}], "abstain": None},
        }, ensure_ascii=False), encoding="utf-8")
        (lb / "desc" / "shards" / "aa.json").write_text(json.dumps({
            DSP3: {"sha": DSP3, "source": "desc",
                   "identity": {"one_liner": "新布局 desc"},
                   "classification": {"cat_primary": "开发库"}},
        }, ensure_ascii=False), encoding="utf-8")
        entries[S22] = v3("a/precedence", S22)          # 旧目录同 sha 的 v3
        (tmp / "interp" / "00.json").write_text(
            json.dumps(entries, ensure_ascii=False), encoding="utf-8")
        ledger["items"]["a/newlayout"] = {"sha": S21}
        ledger["items"]["a/newdesc"] = {"sha": DSP3}
        ledger["items"]["a/precedence"] = {"sha": S22}
        (tmp / "ledger.json").write_text(json.dumps(ledger), encoding="utf-8")
        r = InterpReader(interp_dir=tmp / "interp", enrich_dir=tmp / "enrich",
                         pool_paths=[pool_file], ledger=tmp / "ledger.json",
                         layer_base=lb)

        # 1a) 活跃度边界（7d/90d/365d 各两例 + 无 pool）
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
        chk("commitonly（pushed 400d + 冻结 commit_90d=3→衰减 0→stale，防假活跃）",
            r.activity("a/commitonly", as_of)["tier"] == "stale")
        chk("commitonly 返回的 commit_90d 同步归零",
            r.activity("a/commitonly", as_of)["commit_90d"] == 0)
        chk("commitonlynopush（无 pushed_at 时 commit 是唯一信号→active）",
            r.activity("a/commitonlynopush", as_of)["tier"] == "active")
        chk("ghost（无 pool→unknown）",
            r.activity("a/ghost", as_of)["tier"] == "unknown")

        L = r.layers("a/three")
        chk("三卷齐全（judge/text/vocab/legacy 都在）",
            all(L[k] is not None for k in ("judge", "text", "vocab", "legacy")))
        chk("分类取判定卷（不被文本卷遮蔽）", r.entry("a/three") is L["judge"])
        chk("身份取文本卷", r.identity("a/three") is L["text"])
        chk("domain_tags 取词控卷",
            (r.domain_tags("a/three") or {}).get("tags") == [{"slug": "cdc"}])
        chk("仅旧代：分类与身份都退回 v3",
            r.entry("a/dual") is r.layers("a/dual")["legacy"]
            and r.identity("a/dual") is r.layers("a/dual")["legacy"])
        chk("旧代+文本卷：分类走旧代、身份走文本卷",
            r.entry("a/shadow") is r.layers("a/shadow")["legacy"]
            and r.identity("a/shadow") is r.layers("a/shadow")["text"])
        chk("desc 合并条目同时提供分类与身份",
            r.entry("a/desc") is r.layers("a/desc")["desc"]
            and r.identity("a/desc") is r.layers("a/desc")["desc"])
        chk("#v4 里的 v3 载荷当缺层（不当 v4 用）",
            r.layers("a/mismatch")["judge"] is None and r.entry("a/mismatch") is None)
        chk("台账权威：不认缓存里更新的同 fn 条目",
            r.sha("a/old") == S5 and r.entry("a/old")["sha"] == S5)
        chk("内容镜像共享 sha：两个 fn 都读到分类",
            r.entry("a/m1") is not None and r.entry("a/m2") is not None)
        chk("旧 desc 键归 desc_legacy 且可读",
            r.entry("a/olddesc") is r.layers("a/olddesc")["desc_legacy"])
        chk("无任何层的仓 entry=None", r.entry("a/none") is None)
        chk("新分层布局：三卷都可读（裸 sha + 层目录）",
            r.entry("a/newlayout") is not None
            and r.identity("a/newlayout")["identity"]["one_liner"] == "新布局文本"
            and (r.domain_tags("a/newlayout") or {}).get("tags"))
        chk("新分层布局：旧目录同 sha 时新布局优先",
            r.entry("a/precedence")["classification"]["cat_primary"] == "监控")
        chk("新分层布局：desc 层可读",
            r.entry("a/newdesc")["identity"]["one_liner"] == "新布局 desc")
        d = r.dbs("a/fb")
        chk("fallback 组装（support+compat、mention 剔除、去重）",
            d["dbs"] == ["PostgreSQL", "MySQL"] and d["src"] == "fallback"
            and d["reason"] is None)
        chk("ai_flag 派生（v3 kind 非空）", r.ai_flag("a/fb") is True)
        chk("ai_flag 读 v4 ai_kind（mcp→True）", r.ai_flag("a/aikind_ai") is True)
        chk("ai_flag：v4 other 不算 AI（旧代有值也不翻案）",
            r.ai_flag("a/aikind_other") is False)
        dj = r.dbs("a/judge_dbs")
        chk("判定卷程序 dbs 优先于旧代 engine",
            dj["dbs"] == ["TiDB"] and dj["src"] == "engine")
        de = r.dbs("a/judge_empty")
        chk("判定卷显式空结论不被旧代覆盖，且带原因",
            de["dbs"] == [] and de["src"] is None and bool(de["reason"]))
        ev = r.evidence("a/fb")
        chk("evidence clean_ver 缺省为 None（存量常态）",
            ev["clean_ver"] is None and ev["lines"] == [])
        chk("缺判定卷：身份可读、分类为空",
            r.entry("a/onlytext") is None and r.identity("a/onlytext") is not None)
        chk("缺文本卷：分类可读、身份为空",
            r.entry("a/onlyjudge") is not None and r.identity("a/onlyjudge") is None)
        chk("双卷冲突：分类取判定卷、身份退回旧代",
            r.entry("a/conflict")["classification"]["cat_primary"] == "监控"
            and r.identity("a/conflict")["identity"]["one_liner"] == "old")
        chk("文本键装 v4 形态不符→当缺层",
            r.layers("a/textbad")["text"] is None and r.identity("a/textbad") is None)
        chk("只有词控卷也可读 tags",
            r.entry("a/vocabonly") is None
            and (r.domain_tags("a/vocabonly") or {}).get("tags"))
        chk("desc 新旧并存：台账指向新键就取新键",
            r.entry("a/desc2")["identity"]["one_liner"] == "新 desc")
        chk("台账指向普通 sha 时不串用 desc 条目",
            r.entry("a/normal") is r.layers("a/normal")["judge"])
        chk("legacy 键装 v4 形态不符→当缺层", r.entry("a/legacybad") is None)
        # 稳定性：同一数据两次构建，派生记录逐字段一致
        r2 = InterpReader(interp_dir=tmp / "interp", enrich_dir=tmp / "enrich",
                          pool_paths=[pool_file], ledger=tmp / "ledger.json",
                          layer_base=lb)
        chk("两次构建派生一致",
            json.dumps(r.record("a/three"), ensure_ascii=False, sort_keys=True)
            == json.dumps(r2.record("a/three"), ensure_ascii=False, sort_keys=True))
        chk("record 暴露三卷内容与层可用性",
            r.record("a/three")["layers"]["judge"] is True
            and r.record("a/three")["identity"]["identity"]["one_liner"] == "一句话")

    # 2) 真实数据：三卷合并后 100 仓字段齐全（G1-2 验收）
    real = InterpReader()
    idx = real._load_interp()
    cands = [fn for fn, m in idx.items()
             if m["layers"]["judge"] and m["layers"]["text"]]
    fns = random.Random(42).sample(cands, min(100, len(cands)))
    bad = 0
    for fn in fns:
        L = real.layers(fn)
        e, i = real.entry(fn), real.identity(fn)
        if e is not L["judge"] or i is not L["text"]:
            bad += 1
            continue
        if "cat_primary" not in (e.get("classification") or {}):
            bad += 1
            continue
        if "one_liner" not in (i.get("identity") or {}):
            bad += 1
    chk(f"真实抽样 {len(fns)} 仓三卷字段齐全（bad={bad}）", bad == 0)
    # 旧读层事故回归：v4t 文本卷不得再遮蔽 v4 判定卷
    chk("文本卷不遮蔽判定卷",
        all(real.entry(fn) is not real.layers(fn)["text"] for fn in fns))
    print(f"[INFO] 层覆盖见 --audit；抽样 {len(fns)} 仓（judge+text 双卷候选 {len(cands)}）")

    return fails


def _gate(sample_n: int = 200, min_rate: float = 0.99) -> int:
    """阶段闸门（G1-5）：在池抽样 N 仓，分类与身份都要能读出实义字段。"""
    r = InterpReader()
    idx = r._load_interp()
    pool = r._load_pool()
    cands = sorted(fn for fn in idx if fn in pool)
    fns = random.Random(20261107).sample(cands, min(sample_n, len(cands)))
    c_ok = i_ok = both = 0
    miss = []
    for fn in fns:
        e, i = r.entry(fn), r.identity(fn)
        c = bool(e and (e.get("classification") or {}).get("cat_primary"))
        d = bool(i and (i.get("identity") or {}).get("one_liner"))
        c_ok += c
        i_ok += d
        both += c and d
        if not (c and d) and len(miss) < 10:
            miss.append({"fn": fn, "class": c, "identity": d,
                         "layers": {k: bool(v) for k, v in r.layers(fn).items()}})
    n = len(fns)
    print(f"抽样 {n} 仓（在池候选 {len(cands):,}）")
    print(f"分类可读 {c_ok}/{n} = {c_ok / n:.2%}")
    print(f"身份可读 {i_ok}/{n} = {i_ok / n:.2%}")
    print(f"两者都可读 {both}/{n} = {both / n:.2%}")
    if miss:
        print("缺卷样例：" + json.dumps(miss[:5], ensure_ascii=False))
    ok = n > 0 and c_ok / n >= min_rate and i_ok / n >= min_rate
    print(f"闸门（各 ≥{min_rate:.0%}）→ {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main() -> int:
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "--gate":
        return _gate()
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
