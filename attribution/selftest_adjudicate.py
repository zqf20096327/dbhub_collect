# -*- coding: utf-8 -*-
"""T4a 离线自检：点名库位清单 / 编号证据包 / 输出校验 / 预算不吞 / NDJSON 幂等续跑。

跑法：python attribution/selftest_adjudicate.py（退出码 0=全绿）。零网络——
AI 用 FakeAI（从 prompt 里解析 fn/db 与证据编号，回 canned 合规 JSON），
台账/README 落 tempfile（不碰仓库 state 与 data）。
"""
from __future__ import annotations

import json
import re
import sys
import tempfile
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
for _d in (ROOT, ROOT / "lib", ROOT / "config", ROOT / "interpret"):
    sys.path.insert(0, str(_d))

import adjudicate as adj                       # noqa: E402
from gh import Budget, BudgetOut              # noqa: E402

TS = "2026-11-01T12:00:00Z"

# ---------------- FakeAI：从 prompt 解析槽位与证据编号 ----------------

_SLOT_RE = re.compile(r"仓库 (\S+) 是否【实际支持】(.+?)？")
_ID_RE = re.compile(r"^([RTE]\d+)\. ", re.M)


class FakeAI:
    """canned 应答机。script: key → [raw1, raw2, ...]（弹尽用默认合规应答）；
    fail_fns: 这些 fn 抛 RuntimeError（模拟 API 层错误）。"""

    model = "fake-t4a"

    def __init__(self, script: dict | None = None, fail_fns: set[str] | None = None):
        self.script = script or {}
        self.fail_fns = fail_fns or set()
        self.calls: list[tuple[str, str]] = []          # (fn|db, 第几次)

    def chat(self, prompt: str, timeout: int = 300) -> dict:
        m = _SLOT_RE.search(prompt)
        fn, db = (m.group(1), m.group(2)) if m else ("?", "?")
        key = f"{fn}|{db}"
        n = 1 + sum(1 for k, _ in self.calls if k == key)
        self.calls.append((key, str(n)))
        if fn in self.fail_fns:
            raise RuntimeError("重试耗尽（最后状态码 503）")
        q = self.script.get(key) or []
        if n <= len(q):
            raw = q[n - 1]
        else:                                            # 默认：合规 supports 引首个编号
            ids = _ID_RE.findall(prompt)
            cite = (ids or ["E1"])[0]
            raw = json.dumps({"verdict": "supports", "role": "storage_backend",
                              "confidence": 0.9,
                              "reason": f"提供 {db} 连接支持 [{cite}]",
                              "cite": [cite]})
        return {"content": raw, "reasoning": "", "finish": "stop", "secs": 0.01, "tries": 1}


# ---------------- 夹具 ----------------

INTERP = {
    "a/tool": {"dbs": ["MySQL"], "db_verdicts": [
        {"db": "PostgreSQL", "rel": "reject", "quote": "not supported"}], "_g": "2026-10-30"},
    "b/tool": {"dbs": [], "db_verdicts": [], "_g": "2026-10-30"},
    "c/big": {"dbs": ["SQLite"], "db_verdicts": [], "_g": "2026-10-30"},
    "d/full": {"dbs": ["PostgreSQL", "MySQL"], "db_verdicts": [], "_g": "2026-10-30"},
}
SCAN = {
    "a/tool": {"cands": {
        "PostgreSQL": [{"line": 3, "q": "connects to PostgreSQL"},
                       {"line": None, "q": "desc only PostgreSQL"}],   # line=None 是 desc 通道，不算
        "MongoDB": [{"line": 5, "q": "mongodb support"}]}},           # 非 DB17
    "b/tool": {"cands": {"ClickHouse": [{"line": 1, "q": "clickhouse fast"}]}},
    "c/big": {"cands": {"PostgreSQL": [{"line": 9, "q": "postgres url"}]}},
    "d/full": {"cands": {"PostgreSQL": [{"line": 2, "q": "postgres again"}]}},   # 已在 dbs → 不算
    "x/nointerp": {"cands": {"MySQL": [{"line": 1, "q": "mysql"}]}},             # 无解读记录 → 不算
}
POOL = {
    "a/tool": {"stars": 10, "topics": [], "description": "db tool", "language": "Go"},
    "b/tool": {"stars": 5, "topics": ["clickhouse", "database"], "description": "", "language": "Rust"},
    "c/big": {"stars": 900, "topics": ["postgresql"], "description": "big", "language": "Python"},
    "d/full": {"stars": 7, "topics": [], "description": "", "language": ""},
}


def slot_of(slots: list[dict], fn: str, db: str) -> dict | None:
    return next((s for s in slots if s["fn"] == fn and s["db"] == db), None)


def fake_slot(fn="a/tool", db="PostgreSQL", stars=10) -> dict:
    return {"fn": fn, "db": db, "stars": stars, "sources": ["readme"],
            "readme": [{"line": 3, "q": "connects to PostgreSQL"}], "topics": [],
            "interp_dbs": ["MySQL"], "ai_verdict": "reject"}


def main() -> int:
    fails: list[str] = []
    ck = lambda ok, msg: None if ok else fails.append(f"[FAIL] {msg}")  # noqa: E731
    mark = [0]
    def sect(name: str) -> None:
        print(f"[{'PASS' if len(fails) == mark[0] else 'FAIL'}] {name}")
        mark[0] = len(fails)
    tmp = tempfile.mkdtemp(prefix="t4a_selftest_")
    budget = lambda mc=99: Budget(max_calls=mc, max_minutes=30)         # noqa: E731

    # ============ 1) build_slots：两来源并集 + 排除口径 + star 降序 ============
    slots = adj.build_slots(INTERP, SCAN, POOL)
    s = slot_of(slots, "a/tool", "PostgreSQL")
    ck(s is not None and s["sources"] == ["readme"], f"a/tool PG 应 readme 源：{s and s['sources']}")
    ck(s and s["ai_verdict"] == "reject", "db_verdicts 同库表态应注记 ai_verdict（T4c 素材）")
    ck(s and s["readme"] == [{"line": 3, "q": "connects to PostgreSQL"}],
       f"line=None 的 desc 引证不得入证据：{s and s['readme']}")
    s = slot_of(slots, "b/tool", "ClickHouse")
    ck(s is not None and s["sources"] == ["readme", "topic"],
       f"b/tool CH 应双源合并：{s and s['sources']}")
    ck(s and s["topics"] == ["clickhouse"], "topic 词应入槽")
    ck(slot_of(slots, "d/full", "PostgreSQL") is None, "已在 dbs 的库位不得成槽")
    ck(slot_of(slots, "a/tool", "MongoDB") is None, "非 DB17 提名不得成槽")
    ck(slot_of(slots, "x/nointerp", "MySQL") is None, "无解读记录的仓不得成槽")
    ck(all("database" not in str(s2["topics"]) for s2 in slots), "泛词 topic 不得成槽")
    stars = [s2["stars"] for s2 in slots]
    ck(stars == sorted(stars, reverse=True), f"清单应 star 降序：{stars}")
    # T4a/T4c 分工开关：a/tool PG 带 ai_verdict=reject → exclude 剔、only 留
    ex = adj.filter_ruled(slots, "exclude")
    on = adj.filter_ruled(slots, "only")
    ck(slot_of(ex, "a/tool", "PostgreSQL") is None and slot_of(on, "a/tool", "PostgreSQL") is not None,
       "exclude 剔表态库位、only 只留表态库位")
    ck(len(ex) + len(on) == len(slots) == len(adj.filter_ruled(slots, "all")),
       "exclude ∪ only = all（不重不漏）")
    sect(f"build_slots：{len(slots)} 槽（readme∪topic、排除四口径、降序）")

    # ============ 2) 证据包编号 + 引擎摘要 + README 语境 ============
    ev_rec = {"fn": "a/tool", "status": "ok", "collected_at": TS, "stars": 10,
              "files": [{"path": "requirements.txt", "kind": "dep", "names": ["psycopg2"]},
                        {"path": "go.mod", "kind": "dep", "names": ["go-sql-driver/mysql"]}],
              "clues": {"paths": ["internal/postgres/dsn.go"]}}
    items, engine = adj.evidence_items(fake_slot(), ev_rec, POOL["a/tool"])
    ids = [it["id"] for it in items]
    ck(ids[0] == "R1" and items[0]["kind"] == "readme", f"首条应 R1：{ids}")
    e_kinds = sorted(it["kind"] for it in items if it["id"].startswith("E"))
    ck(e_kinds == ["dep", "tree"], f"E* 只收本库（PG）证据：psycopg2 dep + postgres 路径，不收 MySQL dep：{e_kinds}")
    ck(all(not (it["id"].startswith("E") and it["kind"] == "topic") for it in items),
       "topic 由 T* 表达，E* 不得重复")
    ck(engine["votes"] == 3.0 and engine["status"] == "case_opened",
       f"PG dep 1 + tree 2 = 3 票立案：{engine}")
    items2, engine2 = adj.evidence_items(fake_slot(), None, POOL["a/tool"])
    ck(engine2["votes"] == 0.0 and engine2["status"] == "no_evidence",
       "无证据仓引擎摘要应为空档")
    prompt = adj.render_prompt(fake_slot(), items, engine, POOL["a/tool"])
    ck("仓库 a/tool 是否【实际支持】PostgreSQL" in prompt, "prompt 应点名仓与库")
    ck(prompt.count("R1. ") == 1 and "E1. " in prompt, "prompt 应含编号证据")
    ck('"verdict"' in prompt and '"cite"' in prompt, "prompt 应含输出契约")

    # README 语境（真函数链：clean_readme → number_lines → ±1 行；漂移→None）
    adj.READMES = Path(tmp)
    (Path(tmp) / "a__tool.md").write_text(
        "Tool\n\nconnects to PostgreSQL\n\nand more\n", encoding="utf-8")
    # 行号口径 = 原始行位置（跳过空行不重编）：number_lines 与 db_scan/interpret v3 同款
    ctx = adj.readme_context("a/tool", 3, "connects to PostgreSQL")
    ck(ctx == ["Tool", "connects to PostgreSQL", "and more"], f"语境应为引证行 ±1 非空行：{ctx}")
    ck(adj.readme_context("a/tool", 2, "connects to PostgreSQL") is None, "空行位置编号不存在 → None")
    ck(adj.readme_context("a/tool", 99, "connects to PostgreSQL") is None, "行号不存在 → None")
    ck(adj.readme_context("a/tool", 3, "totally different line") is None, "行文本漂移 → None")
    ck(adj.readme_context("no/such", 1, "x") is None, "文件缺席 → None")
    sect("evidence_items/render_prompt")

    # ============ 3) validate：契约四查 + verdict/role 配套 ============
    ok, v = adj.validate({"verdict": "supports", "role": "storage_backend",
                          "confidence": 0.8, "reason": "x [R1]", "cite": ["R1"]}, {"R1"})
    ck(ok is not None and v == [], "合规应过")
    ck(adj.validate({"verdict": "supports", "role": "storage_backend",
                     "confidence": 0.8, "reason": "x", "cite": []}, {"R1"})[0] is None,
       "supports 空 cite 应拒")
    ck(adj.validate({"verdict": "supports", "role": "storage_backend",
                     "confidence": 0.8, "reason": "x", "cite": ["R9"]}, {"R1"})[0] is None,
       "cite 越编号应拒")
    ck(adj.validate({"verdict": "supports", "role": "mention_only",
                     "confidence": 0.8, "reason": "x", "cite": ["R1"]}, {"R1"})[0] is None,
       "supports+mention_only 配套错应拒")
    ck(adj.validate({"verdict": "no", "role": "other", "confidence": 0.5,
                     "reason": "x", "cite": []}, set())[0] is None, "verdict 非法应拒")
    ck(adj.validate({"verdict": "not_supports", "role": "planned", "confidence": "high",
                     "reason": "x", "cite": []}, set())[0] is None, "confidence 非数值应拒")
    ck(adj.validate(None, set())[0] is None, "非对象应拒")
    o, _ = adj.validate({"verdict": "supports", "role": "data_source_target",
                         "confidence": 0.66666, "reason": "x", "cite": ["R1", "R1"]}, {"R1"})
    ck(o and o["cite"] == ["R1"] and o["confidence"] == 0.67, "cite 去重、confidence 两位")
    sect("validate")

    # ============ 4) adjudicate_one：重试一次 / failed / BudgetOut 不吞 ============
    lock = threading.Lock()
    slot = fake_slot()
    items, engine = adj.evidence_items(slot, None, POOL["a/tool"])
    pr = adj.render_prompt(slot, items, engine, POOL["a/tool"])
    ai = FakeAI()
    rec = adj.adjudicate_one(slot, items, engine, pr, ai, budget(), lock)
    ck(rec["kind"] == "done" and rec["attempts"] == 1 and rec["api_calls"] == 1,
       f"一次过应 done：{rec['kind']}")
    ck(rec["key"] == "a/tool|PostgreSQL" and rec["engine"]["votes"] == 0.0,
       "台账键 fn|db + 引擎摘要随行")
    bad_then_good = {"a/tool|PostgreSQL": [
        '{"verdict": "supports", "role": "storage_backend", "confidence": 0.9,'
        ' "reason": "x", "cite": ["R7"]}']}          # cite 越编号 → 拒；第二次用默认合规
    ai2 = FakeAI(script=bad_then_good)
    rec2 = adj.adjudicate_one(slot, items, engine, pr, ai2, budget(), lock)
    ck(rec2["kind"] == "done" and rec2["attempts"] == 2 and rec2["api_calls"] == 2,
       "违规应带原因重试一次再过")
    ai3 = FakeAI(script={"a/tool|PostgreSQL": ["not json", "still not json"]})
    rec3 = adj.adjudicate_one(slot, items, engine, pr, ai3, budget(), lock)
    ck(rec3["kind"] == "rejected" and rec3["violations"], "两次违规应 rejected 留痕")
    ai4 = FakeAI(fail_fns={"a/tool"})
    rec4 = adj.adjudicate_one(slot, items, engine, pr, ai4, budget(), lock)
    ck(rec4["kind"] == "failed" and "503" in rec4["error"], "API 错应 failed 不炸全盘")
    try:
        adj.adjudicate_one(slot, items, engine, pr, FakeAI(), Budget(max_calls=0, max_minutes=30), lock)
        ck(False, "预算尽应 raise BudgetOut")
    except BudgetOut:
        ck(True, "")                                   # noqa: E501  原样上抛：per-item 不吞（09-29 铁律）
    sect("adjudicate_one")

    # ============ 5) 台账：后者为准 / 畸形行跳过 / 半截行补换行 ============
    led = Path(tmp) / "ledger.ndjson"
    led.write_text(
        json.dumps({"key": "a|X", "kind": "done", "verdict": "supports"}) + "\n"
        + "{broken json\n"
        + json.dumps({"key": "a|X", "kind": "done", "verdict": "unclear"}) + "\n"
        + json.dumps({"key": "b|Y", "kind": "failed", "error": "e"}) + "\n",
        encoding="utf-8", newline="\n")
    recs, bad = adj.load_ledger(led)
    ck(bad == 1 and recs["a|X"]["verdict"] == "unclear" and len(recs) == 2,
       f"后者为准+畸形跳过：bad={bad} n={len(recs)}")
    led2 = Path(tmp) / "half.ndjson"
    led2.write_text('{"key": "a|X", "kind":', encoding="utf-8")     # 无尾换行的半截行
    adj._ensure_trailing_newline(led2)
    with open(led2, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps({"key": "b|Y", "kind": "done"}) + "\n")
    r2, bad2 = adj.load_ledger(led2)
    ck(bad2 == 1 and "b|Y" in r2, f"半截行补换行后续写不粘行：bad={bad2}")
    sect("ledger")

    # ============ 6) run_loop：limit/续跑/failed 重试/rejected 跳过/预算停 ============
    slots6 = [fake_slot(fn=f"{c}/r", db="PostgreSQL", stars=100 - i)
              for i, c in enumerate("abcde")]
    ai6 = FakeAI(fail_fns={"c/r"})
    led3 = Path(tmp) / "run3.ndjson"
    st = adj.run_loop(slots6, led3, ai6, budget(), workers=2, limit=3)
    ck(st["submitted"] == 3 and led3.read_text(encoding="utf-8").count("\n") == 3,
       f"limit 3 应只裁 3：{st}")
    st = adj.run_loop(slots6, led3, FakeAI(fail_fns={"c/r"}), budget(), workers=2)
    ck(st["todo"] == 3 and st["submitted"] == 3 and st["ledger_done"] == 3,
       f"续跑：done 跳过、failed 自动重试、剩余补裁 → 待裁 3（c 重试+d+e）：{st}")
    ck(st.get("done") == 2 and st.get("failed") == 1, f"d/e 过、c 仍失败入账：{st}")
    recs3, _ = adj.load_ledger(led3)
    ck(recs3["c/r|PostgreSQL"]["kind"] == "failed" and len(recs3) == 5,
       "failed 后者为准仍 failed；台账 5 键")
    st = adj.run_loop(slots6, led3, FakeAI(), budget(), workers=2)
    recs3, _ = adj.load_ledger(led3)
    ck(st["todo"] == 1 and recs3["c/r|PostgreSQL"]["kind"] == "done",
       f"API 恢复后只补 c 一条且转 done：{st}")
    # rejected 默认跳过、--retry-rejected 重裁（后者为准）
    rej_ai = FakeAI(script={f"{c}/r|PostgreSQL": ["nope", "nope2"] for c in "abcde"})
    led4 = Path(tmp) / "run4.ndjson"
    st = adj.run_loop(slots6, led4, rej_ai, budget(), workers=2, limit=3)
    n_rej = st["rejected"]
    st = adj.run_loop(slots6, led4, FakeAI(), budget(), workers=2)          # 默认跳过 rejected
    ck(st["submitted"] == 2, f"默认应跳过 rejected 只裁剩余：{st}")
    st = adj.run_loop(slots6, led4, FakeAI(), budget(), workers=2, retry_rejected=True)
    recs4, _ = adj.load_ledger(led4)
    ck(recs4["a/r|PostgreSQL"]["kind"] == "done", "retry_rejected 应重裁（后者为准）")
    # 预算停：max_calls=2、5 槽 → 收尾不炸、台账只含已完条目
    led5 = Path(tmp) / "run5.ndjson"
    st = adj.run_loop(slots6, led5, FakeAI(), Budget(max_calls=2, max_minutes=30), workers=2)
    ck(st["budget_stopped"] and st["submitted"] <= 4, f"预算停应停止派发并收尾：{st}")
    sect("run_loop（limit/续跑/重试/预算停）")

    # ============ 7) 抽检表：分层保底 + 人工栏留空 ============
    recs7 = {}
    for i in range(20):
        recs7[f"r{i}|DB"] = {"key": f"r{i}|DB", "fn": f"r{i}", "db": "DB",
                             "stars": i, "verdict": "supports" if i < 15 else "unclear",
                             "role": "storage_backend", "confidence": 0.9,
                             "reason": "reason [R1]", "cite": ["R1"],
                             "kind": "done", "sources": ["readme"], "interp_dbs": [],
                             "engine": {"votes": 1}, "evidence": [{"id": "R1", "t": "t"}]}
    picks = adj.sample_review(recs7, 8)
    vd = [p["verdict"] for p in picks]
    ck(len(picks) == 8 and vd.count("unclear") == 4 and vd.count("supports") == 4,
       f"n=8 两层：保底 min(5, 8//2)=4 各 4：{vd}")
    recs7b = {}
    for i in range(100):
        v = "supports" if i < 80 else ("not_supports" if i < 95 else "unclear")
        recs7b[f"q{i}|DB"] = {**recs7["r0|DB"], "key": f"q{i}|DB", "fn": f"q{i}",
                              "stars": i, "verdict": v}
    picks_b = adj.sample_review(recs7b, 50)
    vb = [p["verdict"] for p in picks_b]
    ck(len(picks_b) == 50 and vb.count("unclear") == 5 and vb.count("not_supports") >= 5
       and vb.count("supports") >= 35,
       f"n=50 三层：保底 5、余量按占比（80/15/5）：{ {v: vb.count(v) for v in set(vb)} }")
    ck(adj.sample_review(recs7b, 50) == picks_b, "固定种子可复现")
    md = adj.render_review(recs7, picks, 8)
    ck("人工栏" in md and "　 |" in md, "抽检表人工栏必须留空（LLM 不预填）")
    ck("supports" in md and "unclear" in md, "抽检表应含裁决与理由列")
    sect("review")

    print(f"\n{'='*60}\nT4a 自检：{len(fails)} 处失败" if fails else "\nT4a 自检全绿")
    for f in fails:
        print(" ", f)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
