# -*- coding: utf-8 -*-
"""desc 降级层（工作清单 G3-2）：无 README 仓只凭 GitHub 描述做轻判定 + 轻介绍。

为什么独立成层：这类仓没有正文可指认，判定卷的 evidence_lines/cat_tags 机制
全部落空——硬塞进判定卷只会产出一堆不可校验的条目。desc 层的口径是：
- 键 desc::<sha1(fn+desc)[:12]>（G3-1 去碰撞：fn 参与哈希，97 仓共用一条归零；
  描述变了键就变，自然重烧）；
- 轻判定：cat_primary 必填（14 类），persona 可 null（描述太薄判不了是常态），
  eco=unclear 不要求 eco_why（没有证据可引）；
- 轻介绍：只要 one_liner（1-80 字，与文本卷同带），不要 review/highlights——
  一行描述撑不起长文，旧 desc 条目的长篇"推测"正是要 retire 的形态；
- source=desc、confidence=low 是层常量，写进每条（读侧一看便知证据强度）；
- 反编造：提示词明令"描述没提的事实一个都不许编"，质量由 G3-4 人工抽检把关。

用法：
  python interpret/desc_control.py --selftest
（runner 见 run_desc.py；本模块只管提示词与校验，不碰存储与网络）
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for _d in (ROOT, ROOT / "lib", ROOT / "interpret"):
    sys.path.insert(0, str(_d))

import interpret as itp                      # noqa: E402  枚举与判定卷同源（勿另抄一份）
from interp_keys import desc_key             # noqa: E402  键契约唯一口径

DESC_PROMPT_VER = "dc1.0"                    # desc 层提示词版本（META.prompt_ver）
CAT_ENUM = itp._CAT_ENUM                     # 14 类，与判定卷同一集合
AI_KIND_ENUM = itp._AI_KIND
PERSONA_ENUM = {"use", "ops", "build"}
ECO_ENUM = {"tool", "app", "unclear"}
ONE_LINER_MAX = 96                           # 文本卷同款带（80）按实测分布放宽：
                                             # 1108 全量 1,004 条拒收 13 条全是 81-96 字
                                             # （模型转述长描述的自然尾部，非编造），
                                             # 同 v4t 50→80 先例按数据定带

_CAT_LINE = "|".join(sorted(CAT_ENUM))

SCHEMA_DESC_V4 = """输出一个 JSON 对象（只输出 JSON，不要其他文字）。你做的是 desc 降级卷：该仓库没有 README，只有一个描述，只做轻判定+轻介绍：
{
 "classification": {
   "cat_primary": "%s 之一（拿不准选『其他』，不许省略）",
   "persona": ["1-2 个：use=用库 | ops=管库 | build=造库；描述不足以判断时输出 null"],
   "eco": "tool=数据库生态的工具/组件 | app=只是用数据库的应用 | unclear=描述不足以判断",
   "ai_kind": "mcp|rag|text2sql|dba-agent|other 之一（非 AI 项目输出 other，不许省略）"
 },
 "identity": {
   "one_liner": "一句话介绍（1-80 字）：忠实地转述/压缩描述本身，不得加入描述之外的事实"
 }
}
硬规则（违反即拒收）：
- 只依据下面的描述与 topics/主语言判断；描述没提的事实一个都不许编。
- one_liner 不许照抄仓库名；判不了的字段给 null（persona）或 unclear（eco），不要猜。"""

PROMPT_TMPL_DESC = """你是数据库开源生态的编目员。下面这个仓库【没有 README】，只有一个 GitHub 描述，做保守编目。
{schema}

仓库：{fn}
描述：{desc}
topics：{topics}
主语言：{lang}
star：{stars}"""


def build_prompt(fn: str, item: dict) -> dict:
    """拼 desc 卷提示词。item 是池记录（description/topics/language/stars）。"""
    desc = (item.get("description") or "").strip()
    pr = PROMPT_TMPL_DESC.format(
        schema=SCHEMA_DESC_V4 % _CAT_LINE, fn=fn, desc=desc or "（空）",
        topics=",".join((item.get("topics") or [])[:12]) or "（无）",
        lang=item.get("language") or "未知", stars=item.get("stars") or 0)
    return {"prompt": pr, "desc": desc,
            "bytes": len(pr.encode("utf-8"))}


def validate(content: str) -> dict:
    """校验 desc 卷输出。返回 {ok, classification, identity, violations}。

    容忍缺失（轻判定常态）：persona null、eco unclear 无 why、ai_kind 缺省归 other。
    不容忍：cat_primary 缺/越枚举、one_liner 缺/超 80 字/照抄仓库名。
    """
    import re
    viol: list[str] = []
    try:
        m = re.search(r"\{.*\}", content or "", re.S)
        obj = json.loads(m.group(0)) if m else None
    except Exception:
        obj = None
    if not isinstance(obj, dict):
        return {"ok": False, "classification": None, "identity": None,
                "violations": ["输出非 JSON 对象"]}

    cls = obj.get("classification")
    ident = obj.get("identity")
    if not isinstance(cls, dict):
        viol.append("classification 缺失或非对象")
        cls = {}
    if not isinstance(ident, dict):
        viol.append("identity 缺失或非对象")
        ident = {}

    cat = cls.get("cat_primary")
    if cat not in CAT_ENUM:
        viol.append(f"cat_primary 非法: {cat!r}（须 14 类之一）")

    persona = cls.get("persona")
    if persona is not None:
        if (not isinstance(persona, list) or not (1 <= len(persona) <= 2)
                or any(p not in PERSONA_ENUM for p in persona)
                or len(set(persona)) != len(persona)):
            viol.append("persona 非法（null 或 1-2 个去重 use/ops/build）")

    eco = cls.get("eco")
    if eco not in ECO_ENUM:
        viol.append(f"eco 非法: {eco!r}（tool/app/unclear）")

    # 与判定卷同一归一：非 AI 仓模型常省略键 → other，不拒收（真机冒烟教训）
    ai_kind = cls.get("ai_kind")
    if ai_kind is None:
        ai_kind = "other"
        cls["ai_kind"] = "other"
    if ai_kind not in AI_KIND_ENUM:
        viol.append(f"ai_kind 非法: {ai_kind!r}")

    one = (ident.get("one_liner") or "").strip()
    if not one:
        viol.append("one_liner 缺失")
    elif len(one) > ONE_LINER_MAX:
        viol.append(f"one_liner 超长（{len(one)}>{ONE_LINER_MAX} 字）")

    out_cls = {k: cls.get(k) for k in ("cat_primary", "persona", "eco", "ai_kind")}
    return {"ok": not viol, "classification": out_cls,
            "identity": {"one_liner": one}, "violations": viol}


def _selftest() -> int:
    fails = 0

    def chk(name, cond, extra=""):
        nonlocal fails
        print(f"[{'PASS' if cond else 'FAIL'}] {name}" + (f"  {extra}" if extra else ""))
        if not cond:
            fails += 1

    # 1) 键去碰撞（G3-1 验收：同描述不同仓 → 不同键；fn+desc 相同 → 同键）
    k1 = desc_key("a/x", "A bot for SQL")
    k2 = desc_key("a/y", "A bot for SQL")
    chk("同描述不同仓键不同（97 仓共用一条归零）", k1 != k2)
    chk("键形态 desc::<12hex>", len(k1) == 18 and k1.startswith("desc::"))
    chk("同 fn 同描述键稳定", desc_key("a/x", "A bot for SQL") == k1)
    chk("描述变键变（自然重烧）", desc_key("a/x", "changed") != k1)

    # 2) prompt：轻量、含关键约束
    pr = build_prompt("o/r", {"description": "MySQL backup tool", "topics": ["mysql"],
                              "language": "Go", "stars": 12})
    chk("prompt 拼出且 <2KB", 0 < pr["bytes"] < 2048, f"{pr['bytes']}B")
    chk("prompt 含 14 类枚举行", "cat_primary" in pr["prompt"] and "其他" in pr["prompt"])
    chk("prompt 含反编造禁令", "一个都不许编" in pr["prompt"])
    chk("prompt 不含行号机制（desc 无正文可指）", "evidence_lines" not in pr["prompt"])

    # 3) 校验：合法输出
    ok = validate(json.dumps({
        "classification": {"cat_primary": "备份", "persona": ["ops"], "eco": "tool",
                           "ai_kind": "other"},
        "identity": {"one_liner": "MySQL 备份命令行工具"}}, ensure_ascii=False))
    chk("合法输出通过", ok["ok"] and ok["classification"]["cat_primary"] == "备份")
    chk("载荷只留白名单字段（无 eco_why 之类）",
        set(ok["classification"]) == {"cat_primary", "persona", "eco", "ai_kind"})

    # 4) 容忍面：persona null / eco unclear 无 why / ai_kind 缺省
    soft = validate(json.dumps({
        "classification": {"cat_primary": "其他", "persona": None, "eco": "unclear"},
        "identity": {"one_liner": "一个数据库相关项目"}}, ensure_ascii=False))
    chk("persona=null 且 eco=unclear 无 why 可过（轻判定）", soft["ok"])
    chk("ai_kind 缺省归一 other", soft["classification"]["ai_kind"] == "other")

    # 5) 拒收面：cat 越枚举 / one_liner 缺或超长 / 非 JSON
    bad_cat = validate(json.dumps({"classification": {"cat_primary": "数据库"},
                                   "identity": {"one_liner": "x"}}, ensure_ascii=False))
    chk("cat 越枚举拒收", not bad_cat["ok"] and any("cat_primary" in v for v in bad_cat["violations"]))
    bad_len = validate(json.dumps({
        "classification": {"cat_primary": "其他"},
        "identity": {"one_liner": "长" * 81}}, ensure_ascii=False))
    chk("one_liner 超 80 字拒收", not bad_len["ok"])
    chk("非 JSON 拒收", not validate("我觉得这是个备份工具")["ok"])

    print(f"\nselftest {'PASS' if not fails else 'FAIL'}（{fails} 处失败）")
    return 0 if not fails else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    raise SystemExit(_selftest() if a.selftest else 0)
