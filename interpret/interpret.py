# -*- coding: utf-8 -*-
"""AI 结构化解读 worker（中立客观版）。

v3（默认，ver=3）——行号指认：README 清理文按非空行编号喂入（L行号|原文），
evidence_lines / db_verdicts.lines 只填行号，引句文本由程序按行号回填——
转述型拒收在构造上消灭（模型从"背写原文"变为"选择题"）。行号口径与
db_scan 严格一致（number_lines 共用）。desc 降级路径仍走 v2 引句子串。

质量三件套（关思考下保质量）：
  ① JSON 强制模式 + 金标 few-shot 范例 + 规则锚定（类别关键词提示+采集归属）
  ② 中立性三层强制：契约提示词 → 中英文禁词扫描 → 违规带原因重试一次→拒收
  ③ 枚举别名归一（拒收前能修则修）+ 程序对照 xcheck（install/status 正则独立探测，
     分歧只降一级 confidence 并记备注——不覆盖不预填，防迎合偏差）
程序化验收：evidence 行号必须在可见窗口；verdict 行号必须在该库候选行集合内；
枚举字段超集即拒收；review 须有信息增量。
回归把关：改动先跑 interpret/golden_eval.py（金标集离线评分，base 基线见 state/golden_base.json）。

并发模型：worker 线程只返回结果 dict，共享 cache/state 由主线程统一落账
（避免遍历与插入并发的 dict 竞态）；落盘按 chunk 批量（每条全量重写 55MB
缓存的 O(n²) 磁盘 I/O 不可持续）。
待办过滤：出池 fn 不解读；同 sha 已拒收不重烧（进人工队列，勿反复花钱；
--retry-rejected 可捞回：历史 944 条拒收主因是老的思考截断 bug，v3 下值得重烧）；
no_readme 仓空描述跳过、描述变化（desc:: 键变化）可重试。
缓存两层：state/interp_cache.json（sha→结果，跨仓同内容共用）
         state/interp_state.json（fn→sha）
用法：
  python interpret.py                                # 默认 v3 + 最新池
  python interpret.py --mode v2                      # 回退旧引句模式
  python interpret.py --pool data/snapshot_.../pool.json --max-items 50
  python interpret.py --concurrency 8                # 放量
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

import requests

import sys as _sys, pathlib as _pl
ROOT = _pl.Path(__file__).resolve().parents[1]
for _d in (ROOT, ROOT / "lib", ROOT / "config", ROOT / "interpret"):
    _sys.path.insert(0, str(_d))
HERE = ROOT                      # 历史引用兼容：统一指向项目根
import strategy                    # noqa: E402
from gh import atomic_write_json, load_env  # noqa: E402
from interp_store import InterpCacheStore  # noqa: E402  分片缓存（10-06 起，兼容读旧单文件）
from rm_clean import clean_readme   # noqa: E402
from db_scan import number_lines, _COMPILED as _DB_COMPILED  # noqa: E402  行号口径与 db_scan 严格一致
import runlog                       # noqa: E402  条目级 jsonl（优化决策的数据燃料）

# 提示词版本：rel 定义/引证规则/范例任何改动必须 +0.1 并在日志留痕——
# ver 只标记架构（2=引句子串，3=行号指认），prompt_ver 区分架构内部的提示词迭代。
# 3.3：desc-only 候选标注「仅简介提及」；缺 quote 降级为丢该库裁决（见 check_verdicts*）。
PROMPT_VER = "3.3"

log = logging.getLogger("interpret")

CACHE = HERE / "state" / "interp_cache.json"
ISTATE = HERE / "state" / "interp_state.json"
REVIEW = HERE / "state" / "manual_review.json"


def latest_pool() -> Path:
    """M2b：活文件优先（data/live/pool.ndjson），回退最新快照。调用方用
    pool_store.read_any(path) 兼容读两种格式。"""
    import pool_store
    _recs, src = pool_store.load_latest("pool")
    return src


# ============================================================
# 禁词表（SOP 红线 templates.BANNED_WORDS 为底，扩充中英文）
# ============================================================
_BANNED_CN = [
    # 评判/广告
    "最强", "最快", "颠覆", "必将", "震惊", "碾压", "革命性", "王者",
    "神器", "吊打", "强大", "优秀", "出色", "好用", "漂亮", "完美", "卓越",
    "高效", "高性能", "优雅", "惊艳", "史诗", "炸裂",
    # 绝对（注：唯一/第一/首个/完全/最佳/史上 已豁免——它们是数据库术语或
    # README 事实转述的高频词（唯一约束/完全兼容/最佳实践），误伤率远大于收益）
    "最先进", "最流行", "最完善", "最强大",
    "顶尖", "顶级", "无可替代", "业界领先", "遥遥领先", "大幅", "显著",
    # 对比/预测
    "优于", "超越", "碾压式", "将会取代", "必将取代", "领先于", "完胜",
]
_BANNED_EN = [
    r"\bbest\b", r"\bfastest\b", r"\bultimate\b", r"\brevolutionar\w+",
    r"\brevolutionize\b", r"\bgreatest\b", r"\bleading\b",
    r"\bunmatched\b", r"\bunrivaled\b", r"\bstate-of-the-art\b",
    r"\bcutting-edge\b", r"\bgame-chang\w*", r"\bworld-class\b",
    r"\bamazing\b", r"\bbeautiful\b", r"\belegant\w*",
    r"\bexcellent\b", r"\bimpressive\b", r"\bstunning\b", r"\bpowerful\b",
    r"\bmust-have\b", r"\boutperforms?\b", r"\bcrushes\b",
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
   "db_verdicts": [{{"db": "候选库名（只能取候选清单列出的）", "quote": "支撑原文（从候选上下文逐字引用）", "rel": "support|compat|mention"}}],
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
db_verdicts 只对候选清单里的库逐个表态（db 只能取候选名；无候选时输出空数组）。rel 三选一：support=明确适配（专门的驱动/采集器/连接器/官方文档说明）；compat=仅协议兼容（如『兼容 MySQL 协议』不算适配 MySQL 本身）；mention=仅提及/对比/迁移对象（不算）。dbs 留空数组 []，由程序从 verdicts 组装。
ai.kind 只在 flag=true 时填，从 ["text2sql","mcp","dba-agent","rag","other"] 里选。
official.of 只在 flag=true 时填一个库名（也必须来自 dbs_enum）。"""

PROMPT_TMPL = """你是数据库开源生态的编目员，为周报项目库做中立的结构化编目。
{contract}
{schema}

【范例（照此口径输出，注意 verdict 的 rel 判定与 dbs 组装规则）】
范例1（工具·明确适配）flyway：schema 迁移工具，候选 MySQL「Flyway supports MySQL, PostgreSQL…」→
  "eco":"tool","cat":"迁移","db_verdicts":[{{"db":"MySQL","quote":"Flyway supports MySQL","rel":"support"}},
  {{"db":"PostgreSQL","quote":"Flyway supports PostgreSQL","rel":"support"}}],"dbs":[]
范例2（纯应用）mall：电商系统（用 MySQL 存数据）→
  "eco":"app","cat":"应用","db_verdicts":[{{"db":"MySQL","quote":"基于 MySQL 的电商系统","rel":"support"}}],"dbs":[]
范例3（通用工具·候选≠支持）netdata：通用基础设施监控，候选 PostgreSQL 的上下文是打包应用列表（只是提及）→
  "eco":"tool","cat":"监控","db_verdicts":[{{"db":"PostgreSQL","quote":"packaged applications: nginx, postgres…","rel":"mention"}}],"dbs":[]
范例4（协议兼容不算）某客户端宣称『MySQL compatible』→ MySQL 的 rel 应为 "compat"，dbs 为空（除非另有明确适配证据）。

{dbcands}

仓库：{fn}
描述：{desc}
主题标签：{topics}
采集归属：{chan}（仅提示，可推翻）
类别关键词提示：{hint}（规则通道的关键词命中，仅供参考，可推翻）
--- README 开始 ---
{readme}
--- README 结束 ---"""

PROMPT_DESC = """你是数据库开源生态的编目员。该仓库无 README，仅基于以下简介做保守编目（confidence 最高给 mid）。
{contract}
只输出 identity.one_liner / identity.review（标注基于简介）/ classification(cat,db_verdicts,eco,eco_why,ai,persona) /
audit(confidence,evidence 填简介原句) 字段，JSON 格式，参照：
{schema}
{dbcands}

仓库：{fn}
描述：{desc}
主题标签：{topics}
采集归属：{chan}（仅提示，可推翻）
类别关键词提示：{hint}（规则通道的关键词命中，仅供参考，可推翻）"""

# ---------------- v3：行号指认（引句文本不经过模型） ----------------

SCHEMA_V3 = """输出一个 JSON 对象（只输出 JSON，不要其他文字）：
{{
 "identity": {{
   "one_liner": "一句话定位（≤30字，它是什么+核心机制）",
   "review": "一句话中文解读（60-120字：做什么+给谁用+关键机制/限制；须包含 description 之外的信息）",
   "highlights": ["能力事实 2-3 条"],
   "use_cases": ["适用场景 2-3 条"]
 }},
 "classification": {{
   "cat": "备份|监控|高可用|迁移|连接/代理|管理|平台|开发库|安全/审计|测试/质量|建模/设计|内核/引擎|应用|其他 之一",
   "db_verdicts": [{{"db": "候选库名（只能取候选清单列出的）", "rel": "support|compat|mention", "lines": [行号数组]}}],
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
   "evidence_lines": [支撑 cat/eco 判断的 1-3 个行号]
 }}
}}
cat 裁决规则：{cat_rule}
db_verdicts 只对候选清单里的库逐个表态（db 只能取候选名；无候选时输出空数组）。rel 三选一：support=明确适配——专门的驱动/采集器/连接器/插件、为该库服务的代理或中间件、官方工具集/官方文档仓库、或原文明说 supports 该库；『支持的数据库/Supported databases』声明清单是适配声明，清单里的库记 support（靠 ORM/PDO/DB-API 等通用层工作的工具同样适用此规则）；eco=app 的仓库，README 声明使用/依赖该库存数据的也记 support；compat=仅协议兼容（如『兼容 MySQL 协议』不算适配 MySQL 本身——但专为 MySQL 服务的代理/中间件属 support 不属 compat）；mention=仅提及/对比/同类工具列表/迁移来源/教学示例（不算；『兼容(compatible)/对比/迁移来源』类列表中的库默认 mention，但『支持的数据库』声明清单不属此类）。dbs 留空数组 []，由程序从 verdicts 组装。
引证规则（违反即拒收）：evidence_lines 与 db_verdicts.lines 只填【行号数字数组】（如 [42]），禁止抄写原文引句；db_verdicts 的行号必须指向 README 中【真实出现该库名】的行——候选清单列出的是提示行，指认其它真实出现该库名的行同样有效（如支持矩阵深处的行）；候选清单中标注（窗口外）的行也可指认——它们真实存在于 README，只是未在你可见范围内展示；指认可见范围外且不在候选清单中的行号、或该行不含库名，将被拒收；evidence_lines 必须指向支撑你 cat/eco 判断的关键行。
ai.kind 只在 flag=true 时填，从 ["text2sql","mcp","dba-agent","rag","other"] 里选。
official.of 只在 flag=true 时填一个库名（也必须来自 dbs_enum）。"""

PROMPT_TMPL_V3 = """你是数据库开源生态的编目员，为周报项目库做中立的结构化编目。
{contract}
{schema}

【范例（照此口径输出，注意 rel 判定与 lines 行号指认）】
范例1（工具·明确适配）flyway：schema 迁移工具，候选清单 MySQL 行 L12「Flyway supports MySQL」→
  "eco":"tool","cat":"迁移","db_verdicts":[{{"db":"MySQL","rel":"support","lines":[12]}}],"dbs":[]
范例2（纯应用）mall：电商系统（用 MySQL 存数据），候选 L5「基于 MySQL 的电商系统」→
  "eco":"app","cat":"应用","db_verdicts":[{{"db":"MySQL","rel":"support","lines":[5]}}],"dbs":[]
范例3（通用工具·候选≠支持）netdata：通用基础设施监控，候选 PostgreSQL 行 L40「packaged applications: nginx, postgres…」只是提及 →
  "eco":"tool","cat":"监控","db_verdicts":[{{"db":"PostgreSQL","rel":"mention","lines":[40]}}],"dbs":[]
范例4（协议兼容不算）某客户端 L8「MySQL compatible」→ MySQL 的 rel 应为 "compat"，dbs 为空（除非另有明确适配证据）。

{dbcands}

仓库：{fn}
描述：{desc}
主题标签：{topics}
采集归属：{chan}（仅提示，可推翻）
类别关键词提示：{hint}（规则通道的关键词命中，仅供参考，可推翻）
--- README 开始（「L行号|原文」编号，可见行号范围 {line_range}；候选清单标注（窗口外）的行除外）---
{readme}
--- README 结束 ---"""


# ---------------- AI 客户端（OpenAI 兼容 / DeepSeek 协议同旧管道） ----------------

class AIClient:
    def __init__(self, deadline: float | None = None):
        load_env()                     # gh 的读取（config/.env 与根 .env 都认）
        self.key = os.environ.get("AI_API_KEY") or os.environ.get("DEEPSEEK_API_KEY")
        self.base = (os.environ.get("AI_BASE_URL") or "https://api.deepseek.com").rstrip("/")
        if self.base.endswith("/chat/completions"):          # 容错：粘了完整端点时剥掉，防路径拼重
            self.base = self.base.rsplit("/chat/completions", 1)[0]
        self.model = os.environ.get("AI_MODEL") or "deepseek-chat"
        self.deadline = deadline       # 墙钟截止：额度睡等不得越过（防进程僵尸数小时）
        if not self.key:
            raise SystemExit("AI_API_KEY 未配置：写入本仓库 .env（dbhub_collect/.env）")

    def chat(self, prompt: str, timeout: int = 300) -> dict:
        """返回 {content, reasoning, finish, secs, tries}。思考三档由 AI_THINKING 控制：
        disabled=关（默认，最快）/ 数字=budget_tokens 中档 / enabled=不限（最慢）。
        如 .env 加 AI_THINKING=400 即中档思考。"""
        tk = os.environ.get("AI_THINKING", "disabled")
        thinking = ({"type": "enabled", "budget_tokens": int(tk)} if tk.isdigit()
                    else {"type": tk})
        attempt = 0
        quota_waits = 0                                     # 额度耗尽：10 分钟/次探测，最多 5.5h（套餐窗口重置）
        t_call = time.time()
        while True:
            try:
                r = requests.post(
                    f"{self.base}/chat/completions",
                    headers={"Authorization": f"Bearer {self.key}"},
                    json={"model": self.model,
                          "messages": [{"role": "user", "content": prompt}],
                          "thinking": thinking,
                          # 强制 JSON 输出：消灭空输出/字段全 None 型拒收
                          "response_format": {"type": "json_object"},
                          # 思考型模型的推理过程也计入 max_tokens：4000 会被
                          # 长思考烧尽导致正文（JSON）为空——此前 944 条拒收的根因
                          "temperature": 0, "max_tokens": 8000},
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
                if self.deadline and time.time() + 600 > self.deadline:
                    raise RuntimeError("额度耗尽，等待将超墙钟预算，本条放弃（下次运行续）")
                log.warning("额度耗尽，10 分钟后探测重试（第 %d 次）", quota_waits)
                time.sleep(600)
                continue
            if r.status_code == 429 or r.status_code >= 500:  # 普通限流/服务端错误：短退避
                if attempt >= 5:
                    raise RuntimeError(f"重试耗尽（最后状态码 {r.status_code}）")
                time.sleep(min(2 ** attempt * 3, 60))
                attempt += 1
                continue
            if r.status_code == 400:                # 带响应体抛出（端点偶发 400 需可确诊）
                raise RuntimeError(f"400: {r.text[:150]}")
            r.raise_for_status()
            ch = r.json()["choices"][0]
            msg = ch.get("message") or {}
            return {"content": msg.get("content") or "",
                    "reasoning": msg.get("reasoning_content") or "",
                    "finish": ch.get("finish_reason") or "",
                    "secs": round(time.time() - t_call, 2),
                    "tries": attempt + quota_waits + 1}


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
    if not raw:
        return None
    txt = raw.strip()
    # 优先取 ```json 围栏内的对象（围栏里可能是非贪婪提前收尾，失败再走贪婪全文）
    m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", txt, re.S)
    if m:
        try:
            return json.loads(m.group(1))
        except json.JSONDecodeError:
            pass
    m = re.search(r"\{.*\}", txt, re.S)
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


_CAT_HINT_RULES = [
    ("备份", r"backup|mysqldump|xtrabackup|pgbackrest|barman|dump|pitr"),
    ("监控", r"exporter|prometheus|grafana|monitor|observab|zabbix|metric|alert"),
    ("安全/审计", r"audit|security|脱敏|mask(ing)?|encrypt|sql-?injection|firewall|vault"),
    ("迁移", r"migrat|cdc\b|canal\b|otter\b|data-?sync|flyway|liquibase|etl|dts\b"),
    ("高可用", r"patroni|keepalived|failover|high-?availab|haproxy|switchover"),
    ("连接/代理", r"proxy|pooler|pgbouncer|shard(ing)?|mycat|vitess|gateway|load.?balanc"),
    ("开发库", r"\borm\b|driver|jdbc|odbc|connector|sqlalchemy|gorm\b|mybatis|hibernate|"
            r"prisma|typeorm|psycopg|pymysql|go-sql-driver|query.?builder"),
    ("建模/设计", r"er.?diagram|\berd\b|schema.?design|dbml|data.?model|建模|数据库设计"),
    ("测试/质量", r"fuzz|benchmark|sysbench|jepsen|tpc-?[ch]|stress.?test|性能测试"),
    ("管理", r"\bgui\b|admin|dashboard|studio|console|phpmyadmin|dbeaver|chat2db|web.?client"),
    ("平台", r"dbpaas|db-?ops|一体化平台|one-?stop|database platform"),
]

def cat_hint(item) -> str:
    """规则关键词提示（锚定用，模型可推翻）：从 名字+描述+topics 取前两个命中。"""
    text = " ".join([item.get("full_name") or "",
                     item.get("description") or "",
                     " ".join(item.get("topics") or [])]).lower()
    out = []
    for cat, pat in _CAT_HINT_RULES:
        m = re.search(pat, text)
        if m:
            out.append(f"{cat}({m.group(0)})")
        if len(out) >= 2:
            break
    return "、".join(out) or "无"


def check_verdicts(obj, cands: dict) -> list[str]:
    """db_verdicts 清洗 + 程序组装 dbs（只取 rel=support）。
    返回违规列表（空 = 合规）。超集违规在构造上不可能：db 必须在候选内。
    cands 兼容两种 db_scan 格式：旧 {db: [引句]} 与 新 {db: [{line,q}]}。"""
    if not isinstance(obj, dict):
        return []
    cls = obj.get("classification")
    if cls is None:                      # 注意不能用 `or {}`：空字典会被替换成新对象
        cls = {}
        obj["classification"] = cls
    verdicts = cls.get("db_verdicts")
    errs = []
    if verdicts is None:
        verdicts, errs = [], ["db_verdicts 缺失（无候选时应输出空数组）"]
    if not isinstance(verdicts, list):
        verdicts, errs = [], errs + ["db_verdicts 非数组"]
    all_quotes = []
    for qs in cands.values():
        all_quotes += [q if isinstance(q, str) else q.get("q", "") for q in (qs or [])]
    ctx = _norm_txt(" ".join(all_quotes))
    keep, dbs = [], []
    for v in verdicts:
        if not isinstance(v, dict):
            errs.append("verdict 项非对象")
            continue
        db, rel, q = v.get("db"), v.get("rel"), (v.get("quote") or "").strip()
        if db not in cands:
            errs.append(f"verdict 库不在候选: {db}")
            continue
        if rel not in ("support", "compat", "mention"):
            errs.append(f"rel 非法（{db}）: {rel}")
            continue
        if not q:
            continue                   # 缺 quote：丢该库裁决（同转述待遇），不整条拒收
        if ctx and _norm_txt(q) not in ctx:
            # 转述/改写引句（关思考后常见）：丢弃该库裁决、不给归属——
            # 比整条拒收温和，宁缺归属不凭转述采信
            continue
        keep.append({"db": db, "rel": rel, "quote": q})
        if rel == "support":
            dbs.append(db)
    cls["db_verdicts"] = keep
    cls["dbs"] = dbs                     # 组装结果：只有 support 计入归属
    return errs


def check_verdicts_v3(obj, cands: dict, numbered: dict) -> list[str]:
    """v3 行号指认版：模型只给 {db, rel, lines}，引句由程序按行回填。
    行号合法性 = 可见窗口内且该行真实含库名（db_scan 每库只记 3 条提示行，
    模型指认其它真命中行同样有效——支持矩阵深处的行往往更有支撑力）。
    desc-only 候选（README 全文无该库名）退回 v2 引句子串校验。"""
    if not isinstance(obj, dict):
        return []
    cls = obj.get("classification")
    if cls is None:
        cls = {}
        obj["classification"] = cls
    verdicts = cls.get("db_verdicts")
    errs = []
    if verdicts is None:
        verdicts, errs = [], ["db_verdicts 缺失（无候选时应输出空数组）"]
    if not isinstance(verdicts, list):
        verdicts, errs = [], errs + ["db_verdicts 非数组"]
    keep, dbs = [], []
    for v in verdicts:
        if not isinstance(v, dict):
            errs.append("verdict 项非对象")
            continue
        db, rel, lines = v.get("db"), v.get("rel"), v.get("lines")
        if db not in cands:
            errs.append(f"verdict 库不在候选: {db}")
            continue
        if rel not in ("support", "compat", "mention"):
            errs.append(f"rel 非法（{db}）: {rel}")
            continue
        items = cands[db]
        has_readme_lines = any(it.get("line") is not None for it in items)
        if has_readme_lines:
            if not isinstance(lines, list) or not lines:
                errs.append(f"{db} 的 verdict 缺 lines（行号数组）")
                continue
            cand_q = {it["line"]: it["q"] for it in items if it.get("line") is not None}
            pat = _DB_COMPILED.get(db)
            resolved = []
            bad = []
            for x in lines:
                if x in cand_q:                       # 候选提示行：直接采信
                    resolved.append(cand_q[x])
                elif (isinstance(x, int) and x in numbered and pat
                        and pat.search(numbered[x].lower())):
                    resolved.append(numbered[x])      # 窗口内真命中行（候选清单外）
                else:
                    bad.append(x)
            if bad:
                errs.append(f"{db} 的行号无效（窗口外或该行不含库名）: {bad}")
                continue
            quote = " ／ ".join(resolved)
        else:                              # desc-only 候选：v2 引句子串校验
            q = (v.get("quote") or "").strip()
            if not q:
                continue                   # 缺 quote：丢该库裁决（同转述待遇），不整条拒收
            if not any(_norm_txt(q) in _norm_txt(it["q"]) for it in items):
                continue                   # 转述：丢弃该库裁决，不整条拒收
            quote = q
            lines = []
        keep.append({"db": db, "rel": rel, "quote": quote,
                     "lines": [x for x in lines if isinstance(x, int)]})
        if rel == "support":
            dbs.append(db)
    cls["db_verdicts"] = keep
    cls["dbs"] = dbs
    return errs


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
    official = cls.get("official") or {}
    if official.get("flag") and official.get("of") not in gen["CANON_PATTERNS"]:
        errs.append(f"official.of 非法: {official.get('of')}（不在库名单）")
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


def validate_v3(obj, gen, numbered: dict, desc: str) -> tuple[dict | None, list[str]]:
    """v3：evidence 由 evidence_lines 行号指认，程序按 numbered 回填原文。
    其余校验（枚举/禁词/白名单）与 v2 相同。numbered = {行号: 行文本}（仅可见窗口内）。"""
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
    official = cls.get("official") or {}
    if official.get("flag") and official.get("of") not in gen["CANON_PATTERNS"]:
        errs.append(f"official.of 非法: {official.get('of')}（不在库名单）")
    ai = cls.get("ai") or {}
    kinds = [k for k in (ai.get("kind") or []) if k in _AI_KIND]
    install = [i for i in (sig.get("install") or []) if i in _INSTALL]
    ev_lines = aud.get("evidence_lines")
    ev = ""
    if not isinstance(ev_lines, list) or not ev_lines:
        errs.append("evidence_lines 非法（应为行号数组，如 [42]）")
    elif not all(isinstance(x, int) for x in ev_lines):
        errs.append("evidence_lines 含非整数")
    else:
        bad = [x for x in ev_lines if x not in numbered]
        if bad:
            errs.append(f"evidence_lines 行号不在可见范围: {bad}")
        else:
            ev = " ／ ".join(numbered[x] for x in ev_lines)
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
            "audit": {"confidence": conf, "evidence": ev,
                      "evidence_lines": [x for x in ev_lines if isinstance(x, int)]}}, []


_CN_STOP = {"这是", "一个", "这个", "那个", "可以", "以及", "并且", "该", "此", "它",
            "工具", "项目", "软件", "用于", "支持", "提供", "面向", "基于", "通过",
            "具有", "包括", "等等", "目前", "还是", "都是", "以及", "支持", "开源"}


# ---------------- 枚举归一 + 程序对照（v3 质量件） ----------------

# 别名表刻意保守：只收"同义改写/大小写/常见口语"，拿不准的不收。
# 历史拒收挖矿（991 条）证实真别名违规趋近于零——944 条是老的截断 bug，
# 其余是转述与禁词误伤，此表只为消化零星变体，不做大类映射。
_ENUM_ALIAS = {
    "cat": {"备份工具": "备份", "备份恢复": "备份", "监控工具": "监控", "监控告警": "监控",
            "高可用性": "高可用", "连接代理": "连接/代理", "安全管理": "安全/审计",
            "测试": "测试/质量", "质量": "测试/质量", "建模": "建模/设计", "设计": "建模/设计",
            "内核": "内核/引擎", "引擎": "内核/引擎", "开发": "开发库", "应用程序": "应用"},
    "eco": {"Tool": "tool", "App": "app", "application": "app"},
    "persona": {"Use": "use", "Ops": "ops", "Build": "build", "使用": "use",
                "运维": "ops", "构建": "build"},
    "status": {"maintained": "maintenance", "Maintained": "maintenance",
               "EOL": "discontinued", "停止维护": "deprecated"},
    "install": {"pip": "pypi", "pip3": "pypi", "yarn": "npm", "pnpm": "npm",
                "docker-compose": "docker", "helm chart": "helm", "源码": "source",
                "源码编译": "source", "二进制": "binary", "homebrew": "binary", "apt": "binary"},
}


def normalize_enums(obj) -> int:
    """拒收前的枚举别名归一（就地修），返回修复数。"""
    if not isinstance(obj, dict):
        return 0
    n = 0
    cls = obj.get("classification") or {}
    sig = obj.get("signals") or {}
    for key, section in (("cat", cls), ("eco", cls), ("persona", cls), ("status", sig)):
        fixed = _ENUM_ALIAS[key].get(section.get(key))
        if fixed and fixed != section.get(key):
            section[key] = fixed
            n += 1
    inst = sig.get("install")
    if isinstance(inst, list):
        fixed = [_ENUM_ALIAS["install"].get(i, i) for i in inst]
        if fixed != inst:
            sig["install"] = fixed
            n += 1
    return n


# 程序对照信号：install 只认强信号（包管理器命令）；status 只认危险分歧
# （模型说 active 但文本以项目为主语明说不维护）。金标实测"deprecated"裸词
# 全是误报（某 driver/依赖 deprecated ≠ 项目死），必须锚定项目主语。
_X_INSTALL = [("pypi", r"pip3? install|poetry add"),
              ("npm", r"\bnpm (?:i|install)\b|yarn add|pnpm (?:i|add)"),
              ("docker", r"docker (?:run|compose|pull)|docker-compose")]
_X_STATUS_DEPRE = re.compile(
    r"(?:this|the) (?:project|repo(?:sitory)?) (?:is |has been |was |is now )?"
    r"(?:deprecated|discontinued|no longer maintained|unmaintained|in maintenance mode)"
    r"|no longer (?:maintained|actively developed|under development)"
    r"|(?:project|repo) (?:has been )?archived|停止维护|不再维护|已归档", re.I)


def xcheck(obj: dict, ctx: dict) -> dict:
    """程序对照：install/status 用正则独立探测，与模型结果比对。
    分歧只降一级 confidence 并记 xcheck 备注——不覆盖、不预填（防迎合偏差）。"""
    src = "\n".join(ctx["numbered"].values()) if ctx.get("numbered") else (ctx.get("src_norm") or "")
    notes = {}
    prog_install = {k for k, pat in _X_INSTALL if re.search(pat, src, re.I)}
    model_install = set((obj.get("signals") or {}).get("install") or [])
    if prog_install - model_install:              # 程序有强信号而模型漏报
        notes["install_missing"] = sorted(prog_install - model_install)
    if ((obj.get("signals") or {}).get("status") == "active"
            and _X_STATUS_DEPRE.search(src)):
        notes["status_hint"] = "deprecated"
    if notes:
        aud = obj.setdefault("audit", {})
        aud["confidence"] = {"high": "mid", "mid": "low"}.get(aud.get("confidence"),
                                                             aud.get("confidence"))
        obj["xcheck"] = notes
    return notes


def info_gain(review: str, desc: str) -> bool:
    """review 须包含 description 之外 ≥3 个实义信息点（虚词/通用词不计入）。"""
    if not review:
        return False
    dtoks = set(re.findall(r"[a-z0-9\u4e00-\u9fff]{2,}", (desc or "").lower()))
    btoks = set(re.findall(r"[a-z0-9\u4e00-\u9fff]{2,}", review.lower()))
    return len((btoks - dtoks) - _CN_STOP) >= 3


def merge_review(prev: dict, low_conf: list, rejected: list, failed_fns: list) -> dict:
    """人工复核队列跨运行累积合并——旧版整体覆盖写，历史队列永远只剩最后一次运行。
    rejected/failed 保序去重后裁尾 500：不裁会无限涨（failed 是纯 fn 串无时间戳，
    10-07 实测 24,109 条且绝大多数已出池/救回）。"""
    by_fn = {}
    for r in list(prev.get("rejected") or []) + list(rejected):
        by_fn[r.get("fn")] = r            # 同 fn 保最新
    by_failed = {}
    for fn in list(prev.get("failed") or []) + list(failed_fns):
        by_failed[fn] = None              # 字符串队列无 payload；保序去重同 rejected
    return {"low_confidence": sorted(set(prev.get("low_confidence") or []) | set(low_conf)),
            "rejected": list(by_fn.values())[-500:],
            "failed": list(by_failed)[-500:]}


# ---------------- 一次解读（build_prompt + judge，golden_eval 复用） ----------------

def build_prompt(fn: str, degraded: bool, pool: dict, dbscan: dict,
                 schema: str, mode: str = "v2") -> dict:
    """组装提示词与验收上下文。返回 {prompt, src_norm, desc, cands, numbered, stats}。
    v2：src_norm = evidence 子串核对的源文本；v3：numbered = {行号: 行文本}（仅可见窗口），
    evidence/quote 由程序按行号回填（引句文本不经过模型）。desc 降级路径恒走 v2。
    stats = 输入侧画像（日志用）：原始/清理字符数、可见行数、候选库数、窗口外候选行数。"""
    it = pool.get(fn) or {}
    desc = (it.get("description") or "")[:300]
    topics = ",".join((it.get("topics") or [])[:12])
    cands = (dbscan.get(fn) or {}).get("cands") or {}
    chan = (f"{it.get('source') or '?'} 通道 {it.get('source_topic') or ''}".strip()
            if (it.get("source") or it.get("source_topic")) else "未知")
    hint = cat_hint(it)
    use_v3 = mode == "v3" and not degraded
    stats = {"in_raw_chars": 0, "in_clean_chars": 0, "visible_lines": 0,
             "cand_dbs": len(cands), "cand_lines_out": 0}

    def _v2_cands() -> str:
        # v2 兼容：旧 db_scan 格式（{db: [引句]}）与新格式（{db: [{line,q}]}）
        cand_lines = []
        for db, qs in cands.items():
            quotes = [q if isinstance(q, str) else q.get("q", "") for q in (qs or [])][:2]
            cand_lines.append(f"- {db}：" + " ／ ".join(f"「{q}」" for q in quotes))
        return ("\n候选库清单（程序扫描 README 全文所得，db_verdicts 只能对下列出的库表态）：\n"
                + "\n".join(cand_lines)) if cand_lines \
            else "\n候选库清单：无（全文未出现任何目标库名，db_verdicts 应为空数组，dbs 即空）"

    numbered: dict[int, str] = {}
    if degraded:
        prompt = PROMPT_DESC.format(contract=NEUTRALITY_CONTRACT, schema=schema,
                                    dbcands=_v2_cands(), chan=chan, hint=hint,
                                    fn=fn, desc=desc, topics=topics)
        src_norm = desc.lower()
        stats.update({"in_raw_chars": len(desc), "in_clean_chars": len(desc)})
    elif use_v3:
        path = HERE / "data" / "readmes" / (fn.replace("/", "__") + ".md")
        raw_text = path.read_text(encoding="utf-8", errors="ignore") if path.is_file() else ""
        text = clean_readme(raw_text)
        body, cum = [], 0
        for no, ln in number_lines(text):       # 与 db_scan 同口径：全文非空行编号
            if cum > 10000:                     # 显示窗口截断，编号保持全局一致
                break
            body.append(f"L{no}|{ln}")
            numbered[no] = ln
            cum += len(ln) + 1
        # 候选清单：窗口内行取前 3，窗口外行取前 2 给完整行文本并标注——
        # 三轮验证证实漏判主因是支持矩阵在窗口外（常为该库第 4+ 次提及），
        # db_scan 每库存 5 条 + 这里显式标注，模型看得见才判得了
        cand_parts = []
        for db, items in cands.items():
            in_w = [it2 for it2 in items if it2.get("line") is not None
                    and it2["line"] in numbered][:3]
            out_w = [it2 for it2 in items if it2.get("line") is not None
                     and it2["line"] not in numbered][:2]
            desc_only = [it2 for it2 in items if it2.get("line") is None][:1]
            ps = [f"L{it2['line']}「{(it2.get('q') or '').strip()[:80]}」" for it2 in in_w]
            for it2 in out_w:
                ps.append(f"L{it2['line']}（窗口外）「{(it2.get('q') or '').strip()[:160]}」")
                stats["cand_lines_out"] += 1
            ps += [f"「{(it2.get('q') or '').strip()[:80]}」（仅简介提及，quote 须逐字抄自该句）"
                   for it2 in desc_only]
            cand_parts.append(f"- {db}：" + " ／ ".join(ps))
        dbcands = ("\n候选库清单（程序扫描 README 全文所得，db_verdicts 只能对下列出的库表态；"
                   "标注（窗口外）的行同样可指认）：\n"
                   + "\n".join(cand_parts)) if cand_parts \
            else "\n候选库清单：无（全文未出现任何目标库名，db_verdicts 应为空数组，dbs 即空）"
        prompt = PROMPT_TMPL_V3.format(contract=NEUTRALITY_CONTRACT, schema=schema,
                                       dbcands=dbcands, chan=chan, hint=hint,
                                       fn=fn, desc=desc, topics=topics,
                                       readme="\n".join(body) or "（无 README 正文）",
                                       line_range=f"L1–L{max(numbered)}" if numbered else "无")
        src_norm = ""
        stats.update({"in_raw_chars": len(raw_text), "in_clean_chars": len(text),
                      "visible_lines": len(numbered)})
    else:
        path = HERE / "data" / "readmes" / (fn.replace("/", "__") + ".md")
        raw_text = path.read_text(encoding="utf-8", errors="ignore") if path.is_file() else ""
        text = clean_readme(raw_text)[:10000]
        prompt = PROMPT_TMPL.format(contract=NEUTRALITY_CONTRACT, schema=schema,
                                    dbcands=_v2_cands(), chan=chan, hint=hint,
                                    fn=fn, desc=desc, topics=topics,
                                    readme=text or "（无 README 正文）")
        src_norm = text.lower()
        stats.update({"in_raw_chars": len(raw_text), "in_clean_chars": len(text)})
    stats["prompt_chars"] = len(prompt)
    return {"prompt": prompt, "src_norm": src_norm, "desc": desc, "cands": cands,
            "numbered": numbered, "stats": stats}


def judge(fn: str, sha: str, degraded: bool, ctx: dict, ai, gen,
          mode: str = "v2") -> dict:
    """一次解读全流程：chat → 解析 → 程序裁决/校验 → 违规带原因重试一次。
    返回 {kind: done|rejected|failed, ...}（线程安全：只读入参，不落任何共享态）。
    mode=v3 且非 desc 降级时走行号指认（ver=3），否则走 v2 引句子串（desc 恒 v2）。
    遥测字段（runlog 用）：t_total_s/t_api_s/api_tries/violations_all（逐次违规快照，
    重试自愈与救不回是两类问题）/raw（拒收全文不截断）/attempts=validate_attempts。"""
    use_v3 = mode == "v3" and not degraded
    t0 = time.time()
    t_api = 0.0
    api_tries = 0
    try:
        violations: list[str] = []
        violations_all: list[list[str]] = []      # 每次尝试的违规快照（轨迹）
        obj = None
        raw_full = ""
        out_chars = 0
        enum_fixes = 0
        for attempt in (1, 2):                     # 违规带原因重试一次
            try:
                out = ai.chat(ctx["prompt"] + ("" if attempt == 1 else
                            f"\n\n【上次输出被拒收，原因：{'；'.join(violations)}。请修正后重新输出合规 JSON。】"))
            except Exception as e:                 # noqa: BLE001
                return {"kind": "failed", "fn": fn, "sha": sha, "error": str(e)[:150],
                        "t_total_s": round(time.time() - t0, 2), "t_api_s": t_api,
                        "api_tries": api_tries, "violations_all": violations_all}
            t_api += out.get("secs") or 0
            api_tries += out.get("tries") or 1
            raw_full = out["content"] or out["reasoning"] or ""
            out_chars = max(out_chars, len(out["content"] or ""))
            obj = extract_json(out["content"])
            if obj is None and out["reasoning"]:
                obj = extract_json(out["reasoning"])   # 思考型模型：正文空时从推理流兜底
            if isinstance(obj, dict):
                enum_fixes += normalize_enums(obj)     # 枚举别名归一（拒收前能修则修）
            if use_v3:
                verr = check_verdicts_v3(obj or {}, ctx["cands"], ctx["numbered"])
                obj, violations = validate_v3(obj or {}, gen, ctx["numbered"], ctx["desc"])
            else:
                verr = check_verdicts(obj or {}, ctx["cands"])
                obj, violations = validate(obj or {}, gen, ctx["src_norm"], ctx["desc"])
            if obj is not None and verr:
                obj, violations = None, verr
            elif obj is None:
                violations = list(violations) + verr
            if obj is None and out["finish"] == "length":
                violations = ["输出被 max_tokens 截断（思考耗尽预算，无 JSON）"] + violations
            violations_all.append(list(violations))
            if obj is not None:
                break
        if obj is None:
            return {"kind": "rejected", "fn": fn, "sha": sha,
                    "violations": violations[:5], "raw": raw_full[:8000],
                    "attempts": attempt, "out_chars": out_chars,
                    "t_total_s": round(time.time() - t0, 2), "t_api_s": round(t_api, 2),
                    "api_tries": api_tries, "violations_all": violations_all}
        review = (obj["identity"].get("review") or "")
        review_cleared = False
        if not degraded and not info_gain(review, ctx["desc"]):
            obj["identity"]["review"] = ""          # 无增量则空置，不展示
            review_cleared = True
        xcheck(obj, ctx)                            # 程序对照：分歧降置信+备注，不覆盖
        obj.update({"fn": fn, "sha": sha, "source": "desc" if degraded else "readme",
                    "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                    "ver": 3 if use_v3 else 2,      # v3 = 行号指认（程序回填引句）
                    "prompt_ver": PROMPT_VER})
        return {"kind": "done", "fn": fn, "sha": sha, "obj": obj,
                "attempts": attempt, "out_chars": out_chars, "review_cleared": review_cleared,
                "enum_fixes": enum_fixes,
                "t_total_s": round(time.time() - t0, 2), "t_api_s": round(t_api, 2),
                "api_tries": api_tries, "violations_all": violations_all}
    except Exception as e:                             # noqa: BLE001 worker 全身防御
        return {"kind": "failed", "fn": fn, "sha": sha, "error": str(e)[:150],
                "t_total_s": round(time.time() - t0, 2), "t_api_s": t_api,
                "api_tries": api_tries, "violations_all": []}


# ---------------- 主流程 ----------------

def format_schemas(gen) -> dict:
    """两套 schema 各格式化一份：v3=行号指认（readme 路径），v2=引句（desc 降级路径恒用）。
    interpret.run 与 golden_eval 共用本入口，保证评分器与生产接线一致。"""
    dbs_enum = "、".join(gen["CANON_PATTERNS"])
    return {"v3": SCHEMA_V3.format(dbs_enum=dbs_enum, cat_rule=_CAT_RULE),
            "v2": SCHEMA_DESC.format(dbs_enum=dbs_enum, cat_rule=_CAT_RULE)}


def pick_schema(schemas: dict, degraded: bool, mode: str) -> str:
    """schema 按条目选：v3 模式且非降级才用行号版，其余（含一切降级项）一律引句版。
    判据与 judge() 的 use_v3 同一口径。"""
    return schemas["v3"] if (mode == "v3" and not degraded) else schemas["v2"]


def run(args):
    st = json.loads(ISTATE.read_text(encoding="utf-8")) if ISTATE.is_file() else {"items": {}}
    cache = InterpCacheStore()
    rstate_p = HERE / "state" / "readme_state.json"
    rstate = json.loads(rstate_p.read_text(encoding="utf-8")) if rstate_p.is_file() else {"items": {}}
    dbscan_p = HERE / "state" / "db_scan.json"
    dbscan = json.loads(dbscan_p.read_text(encoding="utf-8")) if dbscan_p.is_file() else {}
    log.info("db_scan 候选库清单：%d 项（缺失时先跑 interpret/db_scan.py）", len(dbscan))
    pool_path = Path(args.pool) if args.pool else latest_pool()
    import pool_store
    pool = {it["full_name"]: it for it in pool_store.read_any(pool_path)}

    gen = strategy.derive()
    # schema 必须按【条目】选而不是按 run 整把选（9-30 与 10-01 两次事故同源）：
    # v3 模式下 no_readme 降级项吃到 SCHEMA_V3（evidence_lines/lines）而其校验走
    # v2（evidence/quote），提示词与验收互斥 → 降级项整夜拒收救不回。
    schemas = format_schemas(gen)

    # 待办：readme 有内容且 sha 未解读（或 sha 变化）；含 no_readme 降级项。
    # 过滤：出池 fn 不解读；同 sha 已拒收不重烧（进人工队列）；空描述降级项跳过
    # 仓库静默黑名单（config/exclude_repos.txt，与 pool_core 同源）：400 contentFilter
    # 必再失败的仓每窗重试纯烧钱（10-07 17 条），todo 直接跳过
    _rb_p = HERE / "config" / "exclude_repos.txt"
    repo_bl: set = set()
    if _rb_p.is_file():
        repo_bl = {ln.strip() for ln in _rb_p.read_text(encoding="utf-8-sig").splitlines()
                   if ln.strip() and not ln.startswith("#")}
    todo: list[tuple[str, str, bool]] = []      # (fn, sha, degraded)
    n_skip = {"out_of_pool": 0, "rejected_same_sha": 0, "empty_desc": 0,
              "repo_blacklist": 0, "failed_same_sha": 0}
    for fn, rec in rstate.get("items", {}).items():
        if fn not in pool:
            n_skip["out_of_pool"] += 1
            continue
        if fn in repo_bl:
            n_skip["repo_blacklist"] += 1
            continue
        sha = rec.get("sha")
        prev = st["items"].get(fn) or {}
        if rec.get("status") in ("done", "oversized") and sha and sha not in cache:
            if prev.get("status") == "rejected" and prev.get("sha") == sha \
                    and not args.retry_rejected:
                n_skip["rejected_same_sha"] += 1
                continue
            todo.append((fn, sha, False))
        elif rec.get("status") == "no_readme":
            desc = (pool.get(fn, {}).get("description") or "")[:100]
            if not desc:
                n_skip["empty_desc"] += 1
                continue
            dkey = "desc::" + desc
            # 10-07 修：原条件 prev.sha != dkey AND dkey not in cache —— done 同 sha 但
            # 缓存丢失的 desc 项永远不重入队（清缓存/迁移丢档即永久卡死，实测 9 条）。
            # 改为缓存缺即入队，但 rejected/failed 同 sha 守卫与普通分支对齐（无守卫
            # 会把拒收/400 家族每窗重烧——复核阶段抓到，49 条里 15 条属于此类）
            if dkey not in cache:
                if prev.get("sha") == dkey:
                    if prev.get("status") == "rejected" and not args.retry_rejected:
                        n_skip["rejected_same_sha"] += 1
                        continue
                    if prev.get("status") == "failed":
                        n_skip["failed_same_sha"] += 1
                        continue
                todo.append((fn, dkey, True))
    todo.sort(key=lambda x: -((pool.get(x[0]) or {}).get("stars") or 0))
    total_todo = len(todo)
    todo = todo[:args.max_items]
    log.info("待解读 %d 项（缓存已有 %d）｜真实剩余 %d，本次截取 %d · 跳过 %s",
             total_todo, len(cache), total_todo, len(todo), n_skip)

    t0 = time.time()
    ai = AIClient(deadline=t0 + args.max_minutes * 60)
    done, low_conf, rejected, failed_n = 0, [], [], 0
    run_id = f"{datetime.now().strftime('%m%d_%H%M')}_{args.mode}_p{PROMPT_VER}"

    def work(job) -> dict:
        """worker 线程只读共享结构、只返回结果——落账一律在主线程（防 dict 竞态）。"""
        fn, sha, degraded = job
        ctx = build_prompt(fn, degraded, pool, dbscan,
                           pick_schema(schemas, degraded, args.mode), mode=args.mode)
        r = judge(fn, sha, degraded, ctx, ai, gen, mode=args.mode)
        r["stats"] = ctx["stats"]
        r["degraded"] = degraded
        return r

    def logrec(r: dict) -> dict:
        """条目日志记录（主线程组装，runlog 落 jsonl）。"""
        o = r.get("obj") or {}
        cls = o.get("classification") or {}
        aud = o.get("audit") or {}
        return {"run_id": run_id, "src": "interpret", "mode": args.mode,
                "prompt_ver": PROMPT_VER, "model": ai.model,
                "fn": r.get("fn"), "sha": r.get("sha"), "degraded": r.get("degraded"),
                **(r.get("stats") or {}),
                "kind": r.get("kind"), "validate_attempts": r.get("attempts"),
                "t_total_s": r.get("t_total_s"), "t_api_s": r.get("t_api_s"),
                "api_tries": r.get("api_tries"), "out_chars": r.get("out_chars"),
                "violations": r.get("violations"),
                "violations_all": r.get("violations_all"),
                "raw": r.get("raw") if r.get("kind") == "rejected" else None,
                "error": r.get("error"),
                "cat": cls.get("cat"), "eco": cls.get("eco"), "dbs": cls.get("dbs"),
                "verdicts": [{"db": v.get("db"), "rel": v.get("rel"), "lines": v.get("lines")}
                             for v in (cls.get("db_verdicts") or [])],
                "evidence_lines": aud.get("evidence_lines"),
                "confidence": aud.get("confidence"), "xcheck": o.get("xcheck"),
                "review_cleared": r.get("review_cleared"),
                "enum_fixes": r.get("enum_fixes")}

    recs: list[dict] = []
    with ThreadPoolExecutor(max_workers=args.concurrency) as ex:
        chunk = max(args.concurrency * 4, 16)
        for i in range(0, len(todo), chunk):
            if (time.time() - t0) / 60 >= args.max_minutes:
                log.warning("墙钟预算先到，收尾（断点已存）")
                break
            futs = [ex.submit(work, job) for job in todo[i:i + chunk]]
            chunk_done = 0
            for f in as_completed(futs):        # 主线程统一落账
                r = f.result()
                rec = logrec(r)
                recs.append(rec)
                runlog.log_item(rec)            # 条目级 jsonl（拒收全文/违规轨迹都在这）
                if r["kind"] == "done":
                    cache[r["sha"]] = r["obj"]
                    st["items"][r["fn"]] = {"sha": r["sha"], "status": "done"}
                    if r["obj"]["audit"]["confidence"] == "low":
                        low_conf.append(r["fn"])
                    done += 1
                elif r["kind"] == "rejected":
                    st["items"][r["fn"]] = {"sha": r["sha"], "status": "rejected",
                                            "violations": r["violations"],
                                            "raw": r.get("raw", "")[:200]}   # 短摘要；全文在 jsonl
                    rejected.append({"fn": r["fn"], "why": r["violations"][:3]})
                else:
                    st["items"][r["fn"]] = {"sha": r["sha"], "status": "failed",
                                            "error": r["error"]}
                    failed_n += 1
                chunk_done += 1
            if chunk_done:                      # 按 chunk 落盘（分片后只重写脏桶，~250KB/桶）
                cache.flush()
                atomic_write_json(ISTATE, st)
                # 心跳：每个 chunk（并发×4 条）一行，长窗不再"静默干活"
                log.info("进度 %d/%d · 成功 %d · 拒收 %d · 失败 %d · 缓存 %d · 已用 %.0f 分钟",
                         min(i + chunk_done, len(todo)), len(todo),
                         done, len(rejected), failed_n, len(cache), (time.time() - t0) / 60)
    # 收尾必落 + 人工队列累积合并
    cache.flush()
    atomic_write_json(ISTATE, st)
    prev_review = json.loads(REVIEW.read_text(encoding="utf-8")) if REVIEW.is_file() else {}
    failed_fns = [fn for fn, r in st["items"].items()
                  if r.get("status") in ("failed", "rejected")]
    atomic_write_json(REVIEW, merge_review(prev_review, low_conf, rejected, failed_fns))
    runlog.log_summary({**runlog.summarize_items(recs), "run_id": run_id,
                        "src": "interpret", "mode": args.mode, "prompt_ver": PROMPT_VER,
                        "model": ai.model, "concurrency": args.concurrency})
    log.info("==== 解读完成：成功 %d · 拒收 %d · 低置信 %d · 缓存 %d · %.1f 分钟 ====",
             done, len(rejected), len(low_conf), len(cache), (time.time() - t0) / 60)


def main():
    ap = argparse.ArgumentParser(description="AI 结构化解读（中立版）")
    ap.add_argument("--pool", default=None, help="池路径（默认活文件 data/live/pool.ndjson，回退最新快照）")
    ap.add_argument("--concurrency", type=int, default=6)
    ap.add_argument("--max-items", type=int, default=800)
    ap.add_argument("--max-minutes", type=float, default=90.0)
    ap.add_argument("--mode", choices=["v3", "v2"], default="v3",
                    help="v3=行号指认（程序回填引句，ver=3）；v2=引句子串（回退用）")
    ap.add_argument("--retry-rejected", action="store_true",
                    help="重试历史拒收项（同 sha 也重跑：用于解析修复后捞回 944 条）")
    ap.add_argument("-v", action="store_true")
    args = ap.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.v else logging.INFO,
                        format="%(asctime)s %(levelname)-6s %(name)s | %(message)s",
                        datefmt="%H:%M:%S")
    run(args)


if __name__ == "__main__":
    main()
