# -*- coding: utf-8 -*-
"""AI 结构化解读 worker（中立客观版）。

三层中立性强制：
  ① 提示词中立性契约（只陈述 README 可验证事实，禁评价/绝对/对比/预测）
  ② 输出禁词扫描（复用旧管道 SOP 红线禁词表并扩充中英文）
  ③ 违规拒收→带原因重试一次→再违规清空文本字段、降 confidence=low 进人工队列
程序化验收：evidence 必须是 README 原文子串（防幻觉）；review 须有信息增量；
枚举字段超集即拒收。

缓存两层：state/interp_cache.json（sha→结果，跨仓同内容共用）
         state/interp_state.json（fn→sha）
用法：
  python interpret.py --pool data/snapshot_.../pool.json --max-items 50   # 小样本
  python interpret.py --concurrency 4                                     # 放量
"""
from __future__ import annotations

import argparse
import json
import logging
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

import requests

import sys as _sys, pathlib as _pl
ROOT = _pl.Path(__file__).resolve().parents[1]
for _d in (ROOT, ROOT / "lib", ROOT / "config"):
    _sys.path.insert(0, str(_d))
HERE = ROOT                      # 历史引用兼容：统一指向项目根
import db_profiles as dp           # noqa: E402
import strategy                    # noqa: E402
from gh import atomic_write_json   # noqa: E402

log = logging.getLogger("interpret")

CACHE = HERE / "state" / "interp_cache.json"
ISTATE = HERE / "state" / "interp_state.json"
REVIEW = HERE / "state" / "manual_review.json"

# ============================================================
# 禁词表（SOP 红线 templates.BANNED_WORDS 为底，扩充中英文）
# ============================================================
_BANNED_CN = [
    # 评判/广告
    "最强", "最快", "颠覆", "必将", "重大", "震惊", "碾压", "革命性", "王者",
    "神器", "吊打", "强大", "优秀", "出色", "好用", "漂亮", "完美", "卓越",
    "高效", "高性能", "优雅", "惊艳", "史诗", "炸裂",
    # 绝对
    "最好", "最佳", "最优", "最先进", "最流行", "最完善", "最强大",
    "唯一", "第一", "首个", "完全", "彻底", "绝对", "永远", "极致",
    "顶尖", "顶级", "无可替代", "业界领先", "遥遥领先", "史上", "大幅", "显著",
    # 对比/预测
    "优于", "超越", "碾压式", "将会取代", "必将取代", "领先于", "完胜",
]
_BANNED_EN = [
    r"\bbest\b", r"\bfastest\b", r"\bultimate\b", r"\brevolutionar\w+",
    r"\brevolutionize\b", r"\bperfect\b", r"\bgreatest\b", r"\bleading\b",
    r"\bunmatched\b", r"\bunrivaled\b", r"\bstate-of-the-art\b",
    r"\bcutting-edge\b", r"\bgame-chang\w*", r"\bworld-class\b",
    r"\bamazing\b", r"\bawesome\b", r"\bbeautiful\b", r"\belegant\w*",
    r"\bexcellent\b", r"\bimpressive\b", r"\bstunning\b", r"\bpowerful\b",
    r"\bmust-have\b", r"\bfirst-ever\b", r"\boutperforms?\b", r"\bcrushes\b",
    r"\bsuperior\b", r"\bbetter than\b", r"\bwill replace\b", r"\bpoised to\b",
    r"\bincredibly\b", r"\bworld's (?:first|best|fastest)\b", r"#1",
]
BANNED_RE = re.compile("|".join(_BANNED_CN + _BANNED_EN), re.I)

TEXT_FIELDS = ["one_liner", "review", "highlights", "use_cases", "eco_why", "license_note"]

NEUTRALITY_CONTRACT = """
【中立性契约——违反即拒收】
- 只陈述 README 可验证的事实：它是什么、做什么、给谁用、怎么安装运行
- 禁止：评价词（强大/优秀/好用/perfect…）、绝对词（最X/唯一/第一/完全/永远/#1…）、
  对比（优于/超越/better than…）、预测（必将/将会取代/will replace…）
- 动词用事实性动词：提供/支持/读取/写入/生成/用于/包含/实现/运行
- highlights 只列能力事实，不写价值判断；不确定的内容宁可不写
"""

SCHEMA_DESC = """输出一个 JSON 对象（只输出 JSON，不要其他文字）：
{{
 "identity": {{
   "one_liner": "一句话定位（≤30字，它是什么+核心机制）",
   "review": "一句话中文解读（60-120字：做什么+给谁用+关键机制/限制；须包含 description 之外的信息）",
   "highlights": ["能力事实 2-3 条"],
   "use_cases": ["适用场景 2-3 条"]
 }},
 "classification": {{
   "cat": "备份|监控|高可用|迁移|连接/代理|管理|平台|开发库|安全/审计|测试/质量|建模/设计|内核/引擎|应用|其他 之一",
   "dbs": ["适用库，只能从这些里选：{dbs_enum}"],
   "eco": "tool=为数据库生态服务的工具/组件 | app=只是使用数据库的应用 | unclear=证据不足",
   "eco_why": "生态位判断依据（一句话，事实性）",
   "ai": {{"flag": false, "kind": []}},
   "persona": "use=用库 | ops=管库 | build=造库 之一",
   "official": {{"flag": false, "of": null}}
 }},
 "signals": {{
   "status": "active|maintenance|experimental|deprecated|discontinued 之一",
   "license_note": "双许可/open-core 等说明，无则空字符串",
   "install": ["npm|pypi|docker|binary|source|helm 的子集"]
 }},
 "audit": {{
   "confidence": "high|mid|low",
   "evidence": "README 中支撑 cat/eco 判断的一句原文（中英文均可，原样逐字引用，不要改写/翻译）"
 }}
}}
cat 裁决规则：{cat_rule}
ai.kind 只在 flag=true 时填，从 ["text2sql","mcp","dba-agent","rag","other"] 里选。
official.of 只在 flag=true 时填一个库名。"""

PROMPT_TMPL = """你是数据库开源生态的编目员，为周报项目库做中立的结构化编目。
{contract}
{schema}

仓库：{fn}
描述：{desc}
主题标签：{topics}
--- README 开始 ---
{readme}
--- README 结束 ---"""

PROMPT_DESC = """你是数据库开源生态的编目员。该仓库无 README，仅基于以下简介做保守编目（confidence 最高给 mid）。
{contract}
只输出 identity.one_liner / identity.review（标注基于简介）/ classification(cat,dbs,eco,eco_why,ai,persona) /
audit(confidence,evidence 填简介原句) 字段，JSON 格式，参照：
{schema}

仓库：{fn}
描述：{desc}
主题标签：{topics}"""


# ---------------- AI 客户端（OpenAI 兼容 / DeepSeek 协议同旧管道） ----------------

class AIClient:
    def __init__(self):
        import os
        env = HERE / ".env"
        if env.is_file():
            for line in env.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, _, v = line.partition("=")
                    os.environ.setdefault(k.strip(), v.strip())
        self.key = os.environ.get("AI_API_KEY") or os.environ.get("DEEPSEEK_API_KEY")
        self.base = (os.environ.get("AI_BASE_URL") or "https://api.deepseek.com").rstrip("/")
        if self.base.endswith("/chat/completions"):          # 容错：粘了完整端点时剥掉，防路径拼重
            self.base = self.base.rsplit("/chat/completions", 1)[0]
        self.model = os.environ.get("AI_MODEL") or "deepseek-chat"
        if not self.key:
            raise SystemExit("AI_API_KEY 未配置：写入 dbhub_v2/.env")

    def chat(self, prompt: str, timeout: int = 180) -> str:
        attempt = 0
        quota_waits = 0                                     # 额度耗尽：10 分钟/次探测，最多 5.5h（套餐窗口重置）
        while True:
            try:
                r = requests.post(
                    f"{self.base}/chat/completions",
                    headers={"Authorization": f"Bearer {self.key}"},
                    json={"model": self.model,
                          "messages": [{"role": "user", "content": prompt}],
                          "temperature": 0.1, "max_tokens": 4000},
                    timeout=timeout)
            except requests.exceptions.Timeout:             # 思考模型偶发 >90s：超时重试最多 2 次
                if attempt >= 2:
                    raise
                attempt += 1
                log.warning("读超时，重试（第 %d 次）", attempt)
                continue
            if r.status_code == 429 and "1113" in r.text:   # 余额/额度不足——等窗口，不烧 failed
                quota_waits += 1
                if quota_waits > 33:
                    raise RuntimeError("额度等待超 5.5 小时仍报 1113，放弃本条")
                log.warning("额度耗尽，10 分钟后探测重试（第 %d 次）", quota_waits)
                time.sleep(600)
                continue
            if r.status_code == 429 or r.status_code >= 500:  # 普通限流/服务端错误：短退避
                if attempt >= 5:
                    raise RuntimeError(f"重试耗尽（最后状态码 {r.status_code}）")
                time.sleep(min(2 ** attempt * 3, 60))
                attempt += 1
                continue
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"]


# ---------------- 解析与校验 ----------------

_CAT_ENUM = {"备份", "监控", "高可用", "迁移", "连接/代理", "管理", "平台", "开发库",
             "安全/审计", "测试/质量", "建模/设计", "内核/引擎", "应用", "其他"}
_CAT_RULE = ("cat 互斥裁决：专用场景优先于通用场景（带 GUI 的备份工具归备份不归管理）；"
             "数据库本体/存储引擎/raft 共识/执行器归内核/引擎；ER 图/schema 设计归建模/设计；"
             "脱敏/SQL 审计/防火墙/权限/加密归安全/审计；fuzz/基准/测试数据归测试/质量；"
             "schema 文档生成归管理；BI/报表暂归管理；"
             "eco=app 的项目 cat 固定填『应用』，不再判其他任务类")
_AI_KIND = {"text2sql", "mcp", "dba-agent", "rag", "other"}
_STATUS = {"active", "maintenance", "experimental", "deprecated", "discontinued"}
_INSTALL = {"npm", "pypi", "docker", "binary", "source", "helm"}


def extract_json(raw: str) -> dict | None:
    m = re.search(r"\{.*\}", raw, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return None


def neutral_violations(obj: dict) -> list[str]:
    """文本字段禁词扫描。"""
    hits = []
    def scan(txt, path):
        if not txt:
            return
        m = BANNED_RE.search(txt)
        if m:
            hits.append(f"{path}:『{m.group(0)}』")
    ident, cls, sig = obj.get("identity") or {}, obj.get("classification") or {}, obj.get("signals") or {}
    scan(ident.get("one_liner"), "one_liner")
    scan(ident.get("review"), "review")
    for h in ident.get("highlights") or []:
        scan(h, "highlights")
    for u in ident.get("use_cases") or []:
        scan(u, "use_cases")
    scan(cls.get("eco_why"), "eco_why")
    scan(sig.get("license_note"), "license_note")
    return hits


def _norm_txt(s: str) -> str:
    """比较用归一：剥 HTML/链接语法（空串替换防词内加粗断裂）+ 压空白 +
    去 markdown 强调符 + 弯引号归直 + 标点前去空格。"""
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s or "")      # [text](url) → text
    s = re.sub(r"<[^>]+>", "", s)                             # <tag> → 空（不拆词）
    s = s.translate(str.maketrans({"‘": "'", "’": "'", "“": '"',
                                   "”": '"', "–": "-", "—": "-", "…": "..."}))
    s = re.sub(r"[\s`*_>#]+", " ", s)
    return re.sub(r"\s+([.,;:!?])", r"\1", s).strip().lower()


def validate(obj: dict, gen, readme_norm: str, desc: str) -> tuple[dict | None, list[str]]:
    """返回 (规整后的对象 | None, 违规列表)。"""
    errs = []
    if not isinstance(obj, dict):
        return None, ["输出非对象"]
    ident = obj.get("identity") or {}
    cls = obj.get("classification") or {}
    sig = obj.get("signals") or {}
    aud = obj.get("audit") or {}
    if cls.get("cat") not in _CAT_ENUM:
        errs.append(f"cat 非法: {cls.get('cat')}")
    if cls.get("eco") not in ("tool", "app", "unclear"):
        errs.append(f"eco 非法: {cls.get('eco')}")
    if cls.get("persona") not in ("use", "ops", "build"):
        errs.append("persona 非法")
    if sig.get("status") not in _STATUS:
        errs.append(f"status 非法: {sig.get('status')}")
    dbs = [d for d in (cls.get("dbs") or []) if d in gen["CANON_PATTERNS"]]
    if len(dbs) != len(cls.get("dbs") or []):
        errs.append("dbs 含白名单外库名")
    ai = cls.get("ai") or {}
    kinds = [k for k in (ai.get("kind") or []) if k in _AI_KIND]
    install = [i for i in (sig.get("install") or []) if i in _INSTALL]
    ev = (aud.get("evidence") or "").strip()
    if not ev:
        errs.append("evidence 缺失")
    elif readme_norm and _norm_txt(ev) not in _norm_txt(readme_norm):
        errs.append("evidence 不是 README 原文（疑似改写/幻觉）")
    conf = aud.get("confidence")
    if conf not in ("high", "mid", "low"):
        conf = "low"
        errs.append("confidence 非法")
    errs += neutral_violations(obj)
    if errs:
        return None, errs
    return {"identity": ident, "classification": {**cls, "dbs": dbs, "ai":
            {"flag": bool(ai.get("flag")), "kind": kinds}},
            "signals": {**sig, "install": install},
            "audit": {"confidence": conf, "evidence": ev}}, []


_CN_STOP = {"这是", "一个", "这个", "那个", "可以", "以及", "并且", "该", "此", "它",
            "工具", "项目", "软件", "用于", "支持", "提供", "面向", "基于", "通过",
            "具有", "包括", "等等", "目前", "还是", "都是", "以及", "支持", "开源"}


def info_gain(review: str, desc: str) -> bool:
    """review 须包含 description 之外 ≥3 个实义信息点（虚词/通用词不计入）。"""
    if not review:
        return False
    dtoks = set(re.findall(r"[a-z0-9\u4e00-\u9fff]{2,}", (desc or "").lower()))
    btoks = set(re.findall(r"[a-z0-9\u4e00-\u9fff]{2,}", review.lower()))
    return len((btoks - dtoks) - _CN_STOP) >= 3


# ---------------- 主流程 ----------------

def run(args):
    st = json.loads(ISTATE.read_text(encoding="utf-8")) if ISTATE.is_file() else {"items": {}}
    cache = json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.is_file() else {}
    rstate = json.loads((HERE / "state" / "readme_state.json").read_text(encoding="utf-8")) \
        if (HERE / "state" / "readme_state.json").is_file() else {"items": {}}
    pool = {it["full_name"]: it
            for it in json.loads(Path(args.pool).read_text(encoding="utf-8"))}

    gen = strategy.derive()
    schema = SCHEMA_DESC.format(dbs_enum="、".join(gen["CANON_PATTERNS"]), cat_rule=_CAT_RULE)

    # 待办：readme 有内容且 sha 未解读（或 sha 变化）；含 no_readme 降级项
    todo: list[tuple[str, str, bool]] = []      # (fn, sha, degraded)
    for fn, rec in rstate.get("items", {}).items():
        sha = rec.get("sha")
        if rec.get("status") in ("done", "oversized") and sha and sha not in cache:
            todo.append((fn, sha, False))
        elif rec.get("status") == "no_readme":
            dkey = "desc::" + (pool.get(fn, {}).get("description") or "")[:100]
            if fn not in st["items"] and dkey not in cache:
                todo.append((fn, dkey, True))
    todo.sort(key=lambda x: -((pool.get(x[0]) or {}).get("stars") or 0))
    total_todo = len(todo)
    todo = todo[:args.max_items]
    log.info("待解读 %d 项（缓存已有 %d）｜真实剩余 %d，本次截取 %d",
             total_todo, len(cache), total_todo, len(todo))

    ai = AIClient()
    t0 = time.time()
    done, failed, low_conf, rejected = 0, 0, [], []

    def work(job):
        nonlocal done, failed
        fn, sha, degraded = job
        it = pool.get(fn) or {}
        desc = (it.get("description") or "")[:300]
        topics = ",".join((it.get("topics") or [])[:12])
        if degraded:
            prompt = PROMPT_DESC.format(contract=NEUTRALITY_CONTRACT, schema=schema,
                                        fn=fn, desc=desc, topics=topics)
            readme_norm = desc.lower()
        else:
            path = HERE / "data" / "readmes" / (fn.replace("/", "__") + ".md")
            text = path.read_text(encoding="utf-8", errors="ignore")[:10000] if path.is_file() else ""
            prompt = PROMPT_TMPL.format(contract=NEUTRALITY_CONTRACT, schema=schema,
                                        fn=fn, desc=desc, topics=topics,
                                        readme=text or "（无 README 正文）")
            readme_norm = text.lower()
        violations: list[str] = []
        obj = None
        for attempt in (1, 2):                     # 违规带原因重试一次
            try:
                raw = ai.chat(prompt + ("" if attempt == 1 else
                              f"\n\n【上次输出被拒收，原因：{'；'.join(violations)}。请修正后重新输出合规 JSON。】"))
            except Exception as e:                 # noqa: BLE001
                failed += 1
                st["items"][fn] = {"sha": sha, "status": "failed", "error": str(e)[:150]}
                return False
            obj, violations = validate(extract_json(raw) or {}, gen, readme_norm, desc)
            if obj is not None:
                break
        if obj is None:
            rejected.append((fn, violations[:3]))
            st["items"][fn] = {"sha": sha, "status": "rejected", "violations": violations[:5]}
            return False
        review = (obj["identity"].get("review") or "")
        if not degraded and not info_gain(review, desc):
            obj["identity"]["review"] = ""          # 无增量则空置，不展示
        obj.update({"fn": fn, "sha": sha, "source": "desc" if degraded else "readme",
                    "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d")})
        cache[sha] = obj
        st["items"][fn] = {"sha": sha, "status": "done"}
        if obj["audit"]["confidence"] == "low":
            low_conf.append(fn)
        return True

    with ThreadPoolExecutor(max_workers=args.concurrency) as ex:
        chunk = max(args.concurrency * 4, 16)
        for i in range(0, len(todo), chunk):
            if (time.time() - t0) / 60 >= args.max_minutes:
                log.warning("墙钟预算先到，收尾（断点已存）")
                break
            futs = [ex.submit(work, job) for job in todo[i:i + chunk]]
            for f in as_completed(futs):        # 按完成序消费：单条卡住（如额度熔断长等待）不阻塞落盘
                done += 1 if f.result() else 0
                atomic_write_json(CACHE, cache)  # 每完成一条立即落盘
                atomic_write_json(ISTATE, st)
    # 失败计数并入人工队列
    atomic_write_json(CACHE, cache)
    atomic_write_json(ISTATE, st)
    atomic_write_json(REVIEW, {"low_confidence": low_conf,
                               "rejected": [{"fn": f, "why": v} for f, v in rejected[:50]],
                               "failed": [fn for fn, r in st["items"].items()
                                          if r.get("status") in ("failed", "rejected")]})
    log.info("==== 解读完成：成功 %d · 拒收 %d · 失败 %d · 低置信 %d · 缓存 %d · %.1f 分钟 ====",
             done, len(rejected), failed, len(low_conf), len(cache), (time.time() - t0) / 60)


def main():
    ap = argparse.ArgumentParser(description="AI 结构化解读（中立版）")
    ap.add_argument("--pool", default=str(HERE / "data" / "snapshot_20260925" / "pool.json"))
    ap.add_argument("--concurrency", type=int, default=1)
    ap.add_argument("--max-items", type=int, default=800)
    ap.add_argument("--max-minutes", type=float, default=90.0)
    ap.add_argument("-v", action="store_true")
    args = ap.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.v else logging.INFO,
                        format="%(asctime)s %(levelname)-6s %(name)s | %(message)s",
                        datefmt="%H:%M:%S")
    run(args)


if __name__ == "__main__":
    main()
