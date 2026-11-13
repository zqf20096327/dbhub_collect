# -*- coding: utf-8 -*-
"""定点裁决（ATTRIBUTION T4a，2026-11-01）：只问"该仓是否实际支持库 X"。

  python attribution/adjudicate.py --plan                 零网络：点名库位清单 → state/adjudication_slots.json
  python attribution/adjudicate.py --run --limit 20       烧 AI 冒烟（卡文防坑：烧全量前先 20 条）
  python attribution/adjudicate.py --run                  全量：幂等/断点续跑，追加 state/adjudications.ndjson
  python attribution/adjudicate.py --review 50            零网络：分层抽 50 条 → state/adjudications_review.md
                                                          （人工过目，人工栏留空——LLM 不预填）
  python attribution/adjudicate.py --status               零网络：台账分布 + 对清单覆盖率

点名库位（卡文"输入"）= 一个 (仓, 库) 对，两来源并集（同对合并 sources）：
  readme  db_scan cands 有 README 行号引证提名库 X（line≠None，T3a nominated_gap
          同口径）且 X ∉ interp dbs ——「README 提名差」桶
  topic   池 topics 专有名命中库 X（matcher.match_topic；泛词 database/sql 不算）
          且 X ∉ interp dbs ——「topics 差」桶
  范围 = 有解读记录的仓（缺口相对 interp dbs 而言；未解读仓是 T4b 空白态四类）。
  卡文 10-31 实测 3,894（3,283+611）是口径参照；本脚本按现行分片实算——T1a 扩词
  + db_scan 重跑后提名量上升是预期收益（T1c 验收已记录），以 --plan 实算数为准。

T4a/T4c 分工（11-01 实算定案：全量 11,006 = 未表态 4,281 + AI 表过态 6,725）：
  --ruled exclude（默认，T4a）  只裁 AI 解读时对同库**从未表过态**的库位
      （ai_verdict None——解读链只看 README，topic 声明的库大多没进它的视野；
      实算 4,281 ≈ 卡文 3,894 的扩词后现值）
  --ruled only（T4c 误杀复审）   只裁 AI 明确表过态的（mention 6,257/compat 468
      ——sqlkata/postgis 级"提名过被否决"，配合 --only/--limit 从 star 降序头部烧）
  --ruled all                    不分（排查/补漏用）

一问一证据包（"省 90% AI 费"的核心）：不发全文 README，只发编号证据——
  R*  README 提名行（db_scan 引证 + 盘上 README 同口径编号行 ±1 行语境；
      文件缺席/行文本漂移则只给引证，不猜）
  T*  topic 自声明（作者打的标签）
  E*  引擎指纹证据（dep/image/ci/tree，build_pack 同库条目票降序 ≤6 条）
AI 结论必须引用编号（cite ⊆ 给出的编号；supports 时 cite 非空；role 与 verdict
配套）——程序可校验，与解读链 v3「行号指认」同一思想：不引证据的结论不收。
违规带原因重试一次（interpret.judge 同款），仍违规 = rejected。

台账 state/adjudications.ndjson：一行一库位，key = fn|db，逐行追加即 flush
（断点 = 行；进程被杀最后一行可能半截——续跑前补换行，读取跳过畸形行并计数）。
同 key 多行**后者为准**（--retry-rejected 重裁才会出现）。默认跳过 done/rejected；
failed（API 层错）每次运行自动重试——断点续跑语义。

防坑（卡文 + 09-29 铁律）：
  - BudgetOut 原样 raise：预算在 worker 每次 chat 前 check+计数（gh.Budget 同款），
    异常穿过 per-item 代码不得吞（readme 假振事故）；主线程捕获后停止派发、
    收完在飞结果、exit 0（仓边界收尾铁律）
  - 烧 API 前先 --limit 20 冒烟
  - 墙钟 deadline 透传 AIClient：额度等待不得越过预算（防进程僵尸数小时）
"""
from __future__ import annotations

import argparse
import json
import random
import re
import sys
import threading
import time
from collections import Counter
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
for _d in (ROOT, ROOT / "lib", ROOT / "config", ROOT / "interpret"):
    sys.path.insert(0, str(_d))          # interpret 目录在最前：import interpret → interpret.py

from gh import Budget, BudgetOut, atomic_write_json  # noqa: E402  预算/原子写同款
from interpret import AIClient, extract_json        # noqa: E402  解读链同一 AI 客户端/JSON 抽取
from db_scan import number_lines                    # noqa: E402  行号口径与 db_scan 严格一致
from rm_clean import clean_readme                   # noqa: E402
from attribution.api import ENGINE_VERSION, judge   # noqa: E402
from attribution.matcher import build_pack, match_topic  # noqa: E402

DB17 = frozenset({"PostgreSQL", "MySQL", "Oracle", "SQLite", "SQL Server", "ClickHouse",
                  "MariaDB", "TiDB", "OceanBase", "PolarDB", "Dameng", "openGauss",
                  "GaussDB", "GBase", "TDSQL", "YashanDB", "GoldenDB"})
INTERP_DIR = ROOT / "state" / "interp_cache_shards"
EVIDENCE_DIR = ROOT / "state" / "evidence_cache_shards"
SCAN_P = ROOT / "state" / "db_scan.json"
READMES = ROOT / "data" / "readmes"
SLOTS_P = ROOT / "state" / "adjudication_slots.json"
LEDGER_P = ROOT / "state" / "adjudications.ndjson"
REVIEW_P = ROOT / "state" / "adjudications_review.md"

PROMPT_VER = "t4a-1"
MAX_README_CITES = 3          # 每库位 README 引证上限（db_scan 每库本就 ≤MAX_QUOTES_PER_DB）
MAX_ENGINE_ITEMS = 6          # E* 条目上限（票降序截断——引擎证据是佐证不是主角）
KIND_CN = {"dep": "依赖清单", "image": "容器镜像", "ci": "CI 矩阵", "tree": "文件树路径"}

VERDICTS = ("supports", "not_supports", "unclear")
SUPPORT_ROLES = ("storage_backend", "supported_dialect", "data_source_target", "compat_layer")
REJECT_ROLES = ("mention_only", "planned", "dropped", "name_collision", "other")
UNCLEAR_ROLES = ("insufficient", "other")
ROLES = SUPPORT_ROLES + REJECT_ROLES + ("insufficient",)


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------- 数据装载（pilot_build/scan 同款最小投影） ----------------

def load_interp(interp_dir: Path = INTERP_DIR) -> dict[str, dict]:
    """解读分片 → {fn: {dbs, db_verdicts}}（同 fn 多条 generated_at 新者胜）。"""
    out: dict[str, dict] = {}
    for p in sorted(interp_dir.glob("*.json")):
        for rec in json.loads(p.read_text(encoding="utf-8")).values():
            fn = (rec.get("fn") or "").strip()
            if not fn:
                continue
            g = rec.get("generated_at") or ""
            cur = out.get(fn)
            if cur is not None and g < cur["_g"]:
                continue
            cls = rec.get("classification") or {}
            out[fn] = {"dbs": list(cls.get("dbs") or []),
                       "db_verdicts": list(cls.get("db_verdicts") or []), "_g": g}
    return out


def load_pool() -> dict[str, dict]:
    """池活文件 → {fn: {stars, topics, description, language}}。"""
    import pool_store
    try:
        items, _ = pool_store.load_latest("pool")
    except FileNotFoundError:
        return {}
    return {it.get("full_name"): {"stars": it.get("stars") or 0,
                                  "topics": list(it.get("topics") or []),
                                  "description": it.get("description") or "",
                                  "language": it.get("language") or ""}
            for it in items if it.get("full_name")}


def load_evidence_for(scope: set[str]) -> dict[str, dict]:
    """证据分片 → {fn: rec}（只载 scope 内；逐分片读，内存只有一个分片全量字符串）。"""
    out: dict[str, dict] = {}
    if not scope:
        return out
    for p in sorted(EVIDENCE_DIR.glob("*.json")):
        for rec in json.loads(p.read_text(encoding="utf-8")).values():
            fn = rec.get("fn") or ""
            if fn in scope:
                out[fn] = rec
    return out


# ---------------- 点名库位清单（纯函数，零网络） ----------------

def build_slots(interp: dict, scan: dict, pool: dict) -> list[dict]:
    """(仓, 库) 库位清单：readme 行号提名差 ∪ topics 专有名差，star 降序。"""
    slots: dict[tuple[str, str], dict] = {}

    def slot(fn: str, db: str) -> dict:
        s = slots.get((fn, db))
        if s is None:
            ip = interp[fn]
            s = slots[(fn, db)] = {
                "fn": fn, "db": db,
                "stars": (pool.get(fn) or {}).get("stars") or 0,
                "sources": [], "readme": [], "topics": [],
                "interp_dbs": list(ip["dbs"]),
                "ai_verdict": next((v.get("rel") for v in ip["db_verdicts"]
                                    if v.get("db") == db), None)}
        return s

    for fn, ip in interp.items():
        have = set(ip["dbs"])
        cands = ((scan.get(fn) or {}).get("cands") if isinstance(scan.get(fn), dict) else {}) or {}
        for db, entries in cands.items():
            cites = [e for e in entries or [] if e.get("line") is not None]
            if db not in DB17 or db in have or not cites:
                continue
            s = slot(fn, db)
            if "readme" not in s["sources"]:
                s["sources"].append("readme")
                s["readme"] = [{"line": e["line"], "q": e["q"]}
                               for e in cites[:MAX_README_CITES]]
        for t in (pool.get(fn) or {}).get("topics") or []:
            db = match_topic(t)
            if not db or db not in DB17 or db in have:
                continue
            s = slot(fn, db)
            if "topic" not in s["sources"]:
                s["sources"].append("topic")
            if t not in s["topics"]:
                s["topics"].append(t)
    return sorted(slots.values(), key=lambda s: (-s["stars"], s["fn"], s["db"]))


def filter_ruled(slots: list[dict], mode: str) -> list[dict]:
    """T4a/T4c 分工开关：exclude=只留 AI 未表态（T4a）/ only=只留表过态（T4c）/ all。"""
    if mode == "exclude":
        return [s for s in slots if not s["ai_verdict"]]
    if mode == "only":
        return [s for s in slots if s["ai_verdict"]]
    return list(slots)


# ---------------- 编号证据包（prompt 的全部输入） ----------------

def readme_context(fn: str, line: int, q: str, cache: dict | None = None) -> list[str] | None:
    """盘上 README 同口径编号 → 引证行 ±1 行（非空行语境）。

    行号口径 = number_lines(clean_readme(text))（db_scan/interpret v3 同款）。
    文件缺席 / 编号不存在 / 行文本与引证漂移 → None：只给 db_scan 引证，不猜语境。
    """
    if cache is not None and fn in cache:
        lines = cache[fn]
    else:
        p = READMES / (fn.replace("/", "__") + ".md")
        if not p.is_file():
            lines = None
        else:
            try:
                lines = number_lines(clean_readme(
                    p.read_text(encoding="utf-8", errors="ignore")))
            except Exception:                               # noqa: BLE001  读文件防御：无语境不影响裁决
                lines = None
        if cache is not None:
            cache[fn] = lines
    if not lines:
        return None
    idx = next((i for i, (no, _) in enumerate(lines) if no == line), None)
    if idx is None:
        return None
    norm = lambda s: re.sub(r"\s+", " ", s).strip()[:160]    # noqa: E731  db_scan q 同款归一
    if not norm(lines[idx][1]).startswith((norm(q)[:40] or "\0")):
        return None                                          # README 已更新、行文本漂移
    return [norm(ln) for _, ln in lines[max(0, idx - 1):idx + 2]]


def evidence_items(slot: dict, ev_rec: dict | None, pool_rec: dict | None,
                   readme_cache: dict | None = None) -> tuple[list[dict], dict]:
    """库位 → (编号证据列表, 引擎摘要)。引擎证据是佐证（E*），topic 由 T* 表达不重复。"""
    items: list[dict] = []
    for i, c in enumerate(slot["readme"], 1):
        items.append({"id": f"R{i}", "kind": "readme", "line": c["line"], "text": c["q"],
                      "ctx": readme_context(slot["fn"], c["line"], c["q"], readme_cache)})
    for i, t in enumerate(slot["topics"], 1):
        items.append({"id": f"T{i}", "kind": "topic", "text": t})

    engine = {"status": "no_evidence", "votes": 0.0, "dbs": []}
    try:
        pack = build_pack(slot["fn"], ev_rec,
                          {"topics": (pool_rec or {}).get("topics") or []})
        v = judge(pack)
        engine = {"status": v["status"],
                  "votes": round((v["per_db"].get(slot["db"]) or {}).get("votes", 0.0), 1),
                  "dbs": v["dbs"]}
        chain = [e for e in pack["evidences"]
                 if e["db"] == slot["db"] and e["kind"] != "topic"]
        chain.sort(key=lambda e: (-e["votes"], e["kind"], e["source"]))
        for i, e in enumerate(chain[:MAX_ENGINE_ITEMS], 1):
            det = e.get("detail") or {}
            items.append({"id": f"E{i}", "kind": e["kind"], "source": e["source"],
                          "words": det.get("words") or [], "votes": e["votes"],
                          "weak": bool(det.get("weak_path") or det.get("dev"))})
    except ValueError:                                       # 缺采集时间等防御路径：无引擎佐证
        pass
    return items, engine


def item_text(it: dict) -> str:
    """证据条目一行（prompt 与台账 review 共用同一渲染）。"""
    if it["kind"] == "readme":
        body = " / ".join(it["ctx"]) if it.get("ctx") else it["text"]
        return f"README 第 {it['line']} 行：{body}"
    if it["kind"] == "topic":
        return f"仓库 topic 标签：{it['text']}"
    weak = "（测试/示例语境，弱）" if it.get("weak") else ""
    return (f"{KIND_CN.get(it['kind'], it['kind'])} {it['source']}："
            f"命中 {'、'.join(it['words'])}{weak}")


def render_prompt(slot: dict, items: list[dict], engine: dict, pool_rec: dict | None) -> str:
    fn, db = slot["fn"], slot["db"]
    p = pool_rec or {}
    desc = (p.get("description") or "").strip()[:200] or "（无描述）"
    cur = "、".join(slot["interp_dbs"]) or "无"
    ev = "\n".join(f"{it['id']}. {item_text(it)}" for it in items) or "（无）"
    return f"""你是开源数据库生态的归属裁决员。只回答一个问题：仓库 {fn} 是否【实际支持】{db}？

判定口径：
- supports = 实际支持：{db} 可作为项目的存储后端；或项目实现了 {db} 方言/驱动/适配器；或把 {db} 作为数据源/目标（同步、迁移、导入导出、监控、审计、压测等）；或提供 {db} 兼容层。
- not_supports = 不算支持：仅对比/致谢/举例（mention_only）、仅路线图计划（planned）、曾支持已移除（dropped）、同名撞车指别的东西（name_collision）、其他（other）。
- unclear = 证据不足以下结论（insufficient）。

仓库背景：{desc}；主语言 {p.get('language') or '未知'}；stars {slot['stars']:,}
现有归属判定：{cur}（本次问的 {db} 不在其中）
离线引擎（指纹×词表投票）对 {db} 的票数：{engine['votes']}（≥2 票立案；本次判定状态 {engine['status']}）——仅供参考，与你的结论独立。

证据（编号；结论必须引用）：
{ev}

只输出一个 JSON 对象，不要任何其他文字：
{{"verdict": "supports|not_supports|unclear",
 "role": "storage_backend|supported_dialect|data_source_target|compat_layer|mention_only|planned|dropped|name_collision|insufficient|other",
 "confidence": 0.0到1.0的数,
 "reason": "一句话（≤120字），引用证据编号如 [R1][E2]",
 "cite": ["R1", "E2"]}}
约束：cite 只能用上面出现的编号；verdict=supports 时 cite 不得为空；role 必须与 verdict 配套（supports→前四种；not_supports→mention_only/planned/dropped/name_collision/other；unclear→insufficient/other）。"""


# ---------------- 输出校验（程序裁决，可测） ----------------

def validate(parsed, ids: set[str]) -> tuple[dict | None, list[str]]:
    """裁决 JSON → (obj|None, violations)；cite 越编号/配套错 = 拒收重试。"""
    v: list[str] = []
    if not isinstance(parsed, dict):
        return None, ["输出不是 JSON 对象"]
    verdict, role = parsed.get("verdict"), parsed.get("role")
    if verdict not in VERDICTS:
        v.append(f"verdict 非法：{verdict!r}")
    if role not in ROLES:
        v.append(f"role 非法：{role!r}")
    elif verdict in VERDICTS and role not in {"supports": SUPPORT_ROLES,
                                              "not_supports": REJECT_ROLES,
                                              "unclear": UNCLEAR_ROLES}[verdict]:
        v.append(f"role {role} 与 verdict {verdict} 不配套")
    try:
        conf = float(parsed.get("confidence"))
        if not 0.0 <= conf <= 1.0:
            raise ValueError
    except (TypeError, ValueError):
        conf = None
        v.append(f"confidence 须为 0~1 数值：{parsed.get('confidence')!r}")
    cite = parsed.get("cite")
    if not isinstance(cite, list) or not all(isinstance(c, str) for c in cite):
        cite = None
        v.append("cite 须为编号字符串数组")
    else:
        bad = sorted({c for c in cite if c not in ids})
        if bad:
            v.append(f"cite 引用了不存在的编号：{bad}")
        seen: set[str] = set()
        cite = [c for c in cite if not (c in seen or seen.add(c))]
    reason = parsed.get("reason")
    if not isinstance(reason, str) or not reason.strip():
        v.append("reason 缺失")
    elif len(reason) > 300:
        v.append(f"reason 过长 {len(reason)} 字")
    if verdict == "supports" and not cite:
        v.append("verdict=supports 但 cite 为空")
    if v:
        return None, v
    return {"verdict": verdict, "role": role, "confidence": round(conf, 2),
            "reason": reason.strip(), "cite": cite or []}, []


# ---------------- 单库位裁决（worker；BudgetOut 原样上抛） ----------------

def adjudicate_one(slot: dict, items: list[dict], engine: dict, prompt: str,
                   ai, budget: Budget, lock: threading.Lock) -> dict:
    """chat → 抽 JSON → validate → 违规带原因重试一次（interpret.judge 同款节奏）。

    BudgetOut 在 chat 前的预算检查处 raise，**不进 except**——per-item 不得吞
    （09-29 铁律）；API 层其他异常算本条 failed，下次运行自动重试。
    """
    ids = {it["id"] for it in items}
    t0 = time.time()
    calls = 0
    violations: list[str] = []
    raw = ""
    base = {"key": f'{slot["fn"]}|{slot["db"]}', "fn": slot["fn"], "db": slot["db"],
            "stars": slot["stars"], "sources": slot["sources"],
            "interp_dbs": slot["interp_dbs"], "ai_verdict": slot["ai_verdict"],
            "engine": engine, "evidence": [{"id": it["id"],
                                            "t": item_text(it)[:100]} for it in items],
            "prompt_ver": PROMPT_VER, "engine_ver": ENGINE_VERSION,
            "model": getattr(ai, "model", "?")}
    for attempt in (1, 2):
        with lock:
            budget.check()                     # BudgetOut 原样上抛
            budget.calls += 1
        calls += 1
        try:
            p = prompt if attempt == 1 else (
                prompt + f"\n\n【上次输出被拒收，原因：{'；'.join(violations)}。"
                         f"请修正后重新输出合规 JSON。】")
            out = ai.chat(p, timeout=120)
        except Exception as e:                  # noqa: BLE001  API 层错误：本条 failed
            return {**base, "kind": "failed", "error": str(e)[:150], "attempts": attempt,
                    "api_calls": calls, "secs": round(time.time() - t0, 1),
                    "generated_at": _now()}
        raw = out.get("content") or out.get("reasoning") or ""
        parsed = extract_json(out.get("content") or "")
        if parsed is None and out.get("reasoning"):
            parsed = extract_json(out["reasoning"])   # 思考型模型正文空时兜底
        obj, violations = validate(parsed, ids)
        if obj is None and out.get("finish") == "length":
            violations = ["输出被 max_tokens 截断"] + violations
        if obj is not None:
            return {**base, **obj, "kind": "done", "attempts": attempt,
                    "api_calls": calls, "secs": round(time.time() - t0, 1),
                    "generated_at": _now()}
    return {**base, "kind": "rejected", "violations": violations[:5],
            "raw": raw[:1500], "attempts": 2, "api_calls": calls,
            "secs": round(time.time() - t0, 1), "generated_at": _now()}


# ---------------- 台账 NDJSON（幂等 / 断点续跑） ----------------

def load_ledger(path: Path = LEDGER_P) -> tuple[dict[str, dict], int]:
    """NDJSON → ({key: 最后一条}, 畸形行数)；半截行（被杀进程）跳过并计数。"""
    recs: dict[str, dict] = {}
    bad = 0
    if not Path(path).is_file():
        return recs, 0
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                bad += 1
                continue
            if isinstance(r, dict) and r.get("key"):
                recs[r["key"]] = r            # 同 key 多行后者为准
            else:
                bad += 1
    return recs, bad


def _ensure_trailing_newline(path: Path) -> None:
    """半截行治理：上次被杀的尾行补 \\n——否则续写会把新记录粘进畸形行一起丢。"""
    if not path.is_file() or path.stat().st_size == 0:
        return
    with open(path, "rb") as fb:
        fb.seek(-1, 2)
        if fb.read(1) != b"\n":
            with open(path, "ab") as fb2:
                fb2.write(b"\n")


# ---------------- 主循环（有界派发；预算停 = 收尾 exit 0） ----------------

def run_loop(slots: list[dict], ledger_path: Path, ai, budget: Budget, *,
             workers: int = 4, limit: int = 0, retry_rejected: bool = False,
             only: set[str] | None = None, evidence: dict | None = None,
             pool: dict | None = None, log=print) -> dict:
    """裁决主循环。返回统计 dict；BudgetOut 在此收尾（不向上抛——exit 0 铁律）。"""
    ledger_path = Path(ledger_path)
    done, bad_lines = load_ledger(ledger_path)
    skip_kinds = {"done"} | (set() if retry_rejected else {"rejected"})
    todo = [s for s in slots
            if (done.get(f'{s["fn"]}|{s["db"]}') or {}).get("kind") not in skip_kinds]
    if only:
        todo = [s for s in todo if s["fn"] in only]
    if limit:
        todo = todo[:limit]

    evidence = evidence if evidence is not None else {}
    pool = pool if pool is not None else {}
    readme_cache: dict = {}
    stats: Counter = Counter({"todo": len(todo), "ledger_done": len(done), "ledger_bad": bad_lines})
    lock = threading.Lock()
    stopped: str | None = None
    submitted = 0

    def ctx_of(s: dict) -> tuple[list[dict], dict, str]:
        items, engine = evidence_items(s, evidence.get(s["fn"]), pool.get(s["fn"]),
                                       readme_cache)
        return items, engine, render_prompt(s, items, engine, pool.get(s["fn"]))

    _ensure_trailing_newline(ledger_path)
    with open(ledger_path, "a", encoding="utf-8", newline="\n") as fh:
        with ThreadPoolExecutor(max_workers=workers) as ex:
            pending: set = set()
            it = iter(todo)
            while True:
                while len(pending) < workers and stopped is None:
                    s = next(it, None)
                    if s is None:
                        break
                    try:
                        items, engine, prompt = ctx_of(s)
                    except Exception as e:                  # noqa: BLE001  组包防御：单库位失败不拖全盘
                        log(f"[WARN] 组包失败 {s['fn']}|{s['db']}: {e}")
                        stats["ctx_error"] += 1
                        continue
                    pending.add(ex.submit(adjudicate_one, s, items, engine, prompt,
                                          ai, budget, lock))
                    submitted += 1
                if not pending:
                    break
                fin, pending = wait(pending, return_when=FIRST_COMPLETED)
                for f in fin:
                    try:
                        rec = f.result()
                    except BudgetOut as e:                    # 在飞库位撞预算：未裁，下次续
                        stopped = str(e)
                        stats["budget_stop"] += 1
                        continue
                    fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
                    fh.flush()
                    stats[rec["kind"]] += 1
                    if rec["kind"] == "done":
                        stats[f"v_{rec['verdict']}"] += 1
                    if rec["kind"] == "rejected":
                        stats[f"r_{(rec.get('violations') or ['?'])[0].split('：')[0][:20]}"] += 1
                if stopped is not None:
                    log(f"[预算停] {stopped}——收完在飞 {len(pending)} 条后退出（断点续跑）")
    stats["submitted"] = submitted
    stats["budget_stopped"] = bool(stopped)
    return dict(stats)


# ---------------- 抽检表（人工过目；LLM 不预填人工栏） ----------------

def sample_review(recs: dict[str, dict], n: int = 50, seed: int = 42) -> list[dict]:
    """done 里按 verdict 分层抽样：每层保底 min(5, n//层数)，余量按占比补（最大缺口优先）；
    层内随机（固定种子可复现）、总表 star 降序。"""
    done = [r for r in recs.values() if r.get("kind") == "done"]
    if not done:
        return []
    by: dict[str, list[dict]] = {}
    for r in done:
        by.setdefault(r["verdict"], []).append(r)
    rng = random.Random(seed)
    for l in by.values():
        rng.shuffle(l)
    base = min(5, n // len(by))
    quota = {v: min(len(l), base) for v, l in by.items()}
    while sum(quota.values()) < n:
        cands = [v for v in by if quota[v] < len(by[v])]
        if not cands:
            break
        v = max(cands, key=lambda k: (n * len(by[k]) / len(done) - quota[k], len(by[k])))
        quota[v] += 1
    pick = [r for v, l in sorted(by.items()) for r in l[:quota[v]]]
    pick.sort(key=lambda r: (-(r.get("stars") or 0), r["fn"], r["db"]))
    return pick[:n]


def render_review(recs: dict[str, dict], picks: list[dict], n_want: int) -> str:
    dist = Counter(r.get("kind") for r in recs.values())
    vd = Counter(r["verdict"] for r in recs.values() if r.get("kind") == "done")
    strat = " · ".join(f"{v} {sum(1 for r in picks if r['verdict'] == v)}"
                       for v in ("supports", "not_supports", "unclear") if any(
                           r["verdict"] == v for r in picks))
    lines = ["# T4a 定点裁决抽检表（人工过目；LLM 不预填人工栏）", "",
             f"生成 {_now()} · 台账 {len(recs)} 条（done {dist.get('done', 0)} /"
             f" rejected {dist.get('rejected', 0)} / failed {dist.get('failed', 0)}）"
             f" · 裁决分布 {dict(vd)}", "",
             f"> 用法：逐行核「裁决+理由」是否成立（证据摘要在行内，完整证据见台账 NDJSON），"
             f"人工栏填 ✓/✗+正确结论。**抽检过了才准进 T4b 回写**（卡文验收）。", "",
             f"抽样 {len(picks)}/{n_want}（verdict 分层保底 5、层内随机、表内 star 降序：{strat}）", "",
             "| # | 仓 | star | 库 | 来源 | 现判 dbs | 引擎票 | 裁决 | 角色 | 置信 | 理由（引证据编号） | 人工栏 |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for i, r in enumerate(picks, 1):
        cited = {e["id"]: e["t"] for e in r.get("evidence") or []}
        trail = "；".join(f'{c}“{(cited.get(c) or "")[:60]}…”' for c in r.get("cite", [])[:3])
        lines.append(
            f"| {i} | {r['fn']} | {r.get('stars') or 0:,} | {r['db']} |"
            f"{'+'.join(r.get('sources') or [])} |"
            f"{'+'.join(r.get('interp_dbs') or []) or '∅'} |"
            f"{(r.get('engine') or {}).get('votes')} |"
            f"{r['verdict']} | {r['role']} | {r['confidence']} |"
            f"{r['reason']}{('｜' + trail) if trail else ''} | 　 |")
    return "\n".join(lines) + "\n"


# ---------------- CLI ----------------

def cmd_plan() -> int:
    interp = load_interp()
    scan = json.loads(SCAN_P.read_text(encoding="utf-8"))
    pool = load_pool()
    slots = build_slots(interp, scan, pool)
    t4a = filter_ruled(slots, "exclude")
    by_src = Counter("+".join(s["sources"]) for s in slots)
    by_src_a = Counter("+".join(s["sources"]) for s in t4a)
    by_db_a = Counter(s["db"] for s in t4a)
    ruled = Counter(s["ai_verdict"] for s in slots if s["ai_verdict"])
    report = {"generated_at": _now(), "engine": ENGINE_VERSION, "prompt_ver": PROMPT_VER,
              "total": len(slots), "t4a_unruled": len(t4a), "t4c_ruled": dict(ruled.most_common()),
              "by_source": dict(by_src.most_common()),
              "t4a_by_source": dict(by_src_a.most_common()),
              "t4a_by_db": dict(by_db_a.most_common()),
              "slots": slots}
    atomic_write_json(SLOTS_P, report)
    print(f"点名库位全量 {len(slots)}（来源 {dict(by_src)}）")
    print(f"  T4a 未表态 {len(t4a)}（来源 {dict(by_src_a)}）← 默认裁决范围"
          f"（卡文 10-31 参照 3,894，扩词后现值）")
    print(f"  T4c 表过态 {sum(ruled.values())}（{dict(ruled)}）← --ruled only")
    print("T4a 按库 Top:", " ".join(f"{db}={n}" for db, n in by_db_a.most_common(10)))
    print(f"台账 {SLOTS_P.name}")
    return 0


def cmd_run(args) -> int:
    interp = load_interp()
    scan = json.loads(SCAN_P.read_text(encoding="utf-8"))
    pool = load_pool()
    slots = filter_ruled(build_slots(interp, scan, pool), args.ruled)
    only = set(args.only.split(",")) if args.only else None
    done, _ = load_ledger(LEDGER_P)
    skip = {"done"} | (set() if args.retry_rejected else {"rejected"})
    need = {s["fn"] for s in slots
            if (done.get(f'{s["fn"]}|{s["db"]}') or {}).get("kind") not in skip
            and (not only or s["fn"] in only)}
    evidence = load_evidence_for(need)                    # 只载待裁仓的分片（内存纪律）
    ai = AIClient(deadline=time.time() + args.max_minutes * 60)
    budget = Budget(max_calls=args.max_calls, max_minutes=args.max_minutes)
    print(f"范围 --ruled {args.ruled}：{len(slots)} 库位；待裁仓证据分片已载 {len(evidence)}")
    stats = run_loop(slots, LEDGER_P, ai, budget, workers=args.workers,
                     limit=args.limit, retry_rejected=args.retry_rejected,
                     only=only, evidence=evidence, pool=pool)
    st = {k: v for k, v in stats.items() if not k.startswith("r_")}
    print(f"提交 {stats.get('submitted', 0)} / 待裁 {stats['todo']}"
          f"（台账已有 {stats['ledger_done']}、畸形行 {stats['ledger_bad']}）")
    print("结果分布:", st)
    if stats.get("budget_stopped"):
        print("预算先到，断点已保住（重跑续裁）——exit 0（仓边界收尾铁律）")
    return 0


def cmd_review(n: int) -> int:
    recs, bad = load_ledger(LEDGER_P)
    picks = sample_review(recs, n)
    if not picks:
        print("台账无 done 记录，先 --run")
        return 1
    REVIEW_P.write_text(render_review(recs, picks, n), encoding="utf-8", newline="\n")
    vd = Counter(r["verdict"] for r in picks)
    print(f"抽 {len(picks)} 条（{dict(vd)}）→ {REVIEW_P.name}；台账畸形行 {bad}")
    return 0


def cmd_status() -> int:
    recs, bad = load_ledger(LEDGER_P)
    dist = Counter(r.get("kind") for r in recs.values())
    vd = Counter(r["verdict"] for r in recs.values() if r.get("kind") == "done")
    roles = Counter(r["role"] for r in recs.values() if r.get("kind") == "done")
    print(f"台账 {len(recs)} 条（{dict(dist)}；畸形行 {bad}）")
    print("裁决分布:", dict(vd.most_common()))
    print("角色分布:", dict(roles.most_common()))
    if SLOTS_P.is_file():
        plan = json.loads(SLOTS_P.read_text(encoding="utf-8"))
        keys = {f'{s["fn"]}|{s["db"]}' for s in filter_ruled(plan["slots"], "exclude")}
        cov = sum(1 for k, r in recs.items() if r.get("kind") == "done" and k in keys)
        print(f"T4a 清单 {len(keys)} 库位 · 已裁 {cov}"
              f"（{cov * 100 / max(1, len(keys)):.0f}%，清单为 --plan 时点快照；"
              f"全量 {plan['total']}，T4c 表过态 {sum(plan.get('t4c_ruled', {}).values())}）")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="T4a 定点裁决（点名库位一问一证据包）")
    ap.add_argument("--plan", action="store_true", help="零网络：生成点名库位清单")
    ap.add_argument("--run", action="store_true", help="烧 AI：裁决（幂等断点续跑）")
    ap.add_argument("--review", type=int, metavar="N", help="零网络：抽 N 条裁决 → 复核表")
    ap.add_argument("--status", action="store_true", help="零网络：台账分布")
    ap.add_argument("--ruled", choices=["exclude", "only", "all"], default="exclude",
                    help="exclude=AI 未表态（T4a 默认）/ only=表过态（T4c 误杀复审）/ all")
    ap.add_argument("--limit", type=int, default=0, help="本次最多新裁 N 个库位（0=不限；冒烟用）")
    ap.add_argument("--only", default=None, help="只裁指定仓（逗号分隔 fn，金丝雀/复裁用）")
    ap.add_argument("--retry-rejected", action="store_true", help="连 rejected 一起重裁（默认跳过）")
    ap.add_argument("--max-calls", type=int, default=9000, help="AI 调用上限（含重试）")
    ap.add_argument("--max-minutes", type=float, default=110.0, help="墙钟上限（分钟）")
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args(argv)
    if not (args.plan or args.run or args.review is not None or args.status):
        ap.print_usage()
        print("需 --plan / --run / --review N / --status 至少其一", file=sys.stderr)
        return 2
    if args.plan:
        return cmd_plan()
    if args.run:
        return cmd_run(args)
    if args.review is not None:
        return cmd_review(args.review)
    return cmd_status()


if __name__ == "__main__":
    sys.exit(main())
