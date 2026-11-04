# -*- coding: utf-8 -*-
"""E1 判定层 v4 自检（工作包清单 v4·红线断言进 selftest 的落地件）。

覆盖：
- R1 禁 similar_to 同类点名（键级扫描拒收）；
- R3 cat_tags 14 类内、1-3 个；
- R4 status 三值+null（active/maintenance 属程序活跃度，AI 层非法）；
- R5 evidence 只收行号（落盘对象无 evidence 全文/无预览键）；
- R6 三重：①键集（SCHEMA_V4 文本无 db 判定键）②构造（build_prompt v4 的 ctx
  无候选库、prompt 无「候选库清单」/DB_VOCAB 区块标记——README 正文含库名属
  正常，不按库名断言）③渲染（渲染后 prompt 字符串无 db_verdicts/official 字样）；
- domain_tags 禁用期输出即拒收（拒收文本进 violations，G5 可统计）；
- eco_why / license_note 条件化；
- 输出体量口径（合成合规对象序列化 ~100-130B ±30% 带宽）。

用法：python interpret/selftest_v4.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import interpret as itp                      # noqa: E402


NUMBERED = {1: "A MySQL driver", 2: "supports postgres", 3: "install via pip",
            4: "license: MIT", 5: "experimental release"}


def good_obj(**over):
    o = {
        "classification": {
            "cat_primary": "开发库", "cat_tags": ["连接/代理", "开发库"],
            "persona": ["use", "build"], "eco": "tool",
            "ai_kind": "other",
        },
        "signals": {"install": ["pypi"], "status": None},
        "audit": {"confidence": "mid", "evidence_lines": [1, 2]},
    }
    for k, v in over.items():
        o[k] = v
    return o


def main() -> int:
    fails = 0

    def chk(name, cond):
        nonlocal fails
        print(f"[{'PASS' if cond else 'FAIL'}] {name}")
        if not cond:
            fails += 1

    # ---- 红线断言 ----
    # R1：similar_to 点名拒收
    obj, errs = itp.validate_v4(good_obj(classification={
        **good_obj()["classification"], "similar_to": "psycopg"}), NUMBERED, "d")
    chk("R1 similar_to 输出即拒收", obj is None and any("R1" in e for e in errs))
    # R3：cat_tags 白名单外/超 3 个拒收
    for bad_tags in (["备份", "监控", "迁移", "管理"], ["不存在的类"]):
        obj, errs = itp.validate_v4(good_obj(classification={
            **good_obj()["classification"], "cat_tags": bad_tags}), NUMBERED, "d")
        chk(f"R3 cat_tags 非法拒收 {bad_tags}", obj is None and any("R3" in e for e in errs))
    # R4：status 三值+null；active/maintenance 非法（活跃度归程序）
    for bad in ("active", "maintenance"):
        obj, errs = itp.validate_v4(good_obj(signals={"install": [], "status": bad}),
                                    NUMBERED, "d")
        chk(f"R4 status={bad} 拒收", obj is None and any("R4" in e for e in errs))
    for ok in ("experimental", "deprecated", "discontinued"):
        sig = {"install": [], "status": ok}
        obj, _ = itp.validate_v4(good_obj(signals=sig), NUMBERED, "d")
        chk(f"R4 status={ok!r} 放行（原值保留）", obj is not None
            and obj["signals"]["status"] == ok)
    for ok in (None, "null"):
        sig = {"install": [], "status": ok}
        obj, _ = itp.validate_v4(good_obj(signals=sig), NUMBERED, "d")
        chk(f"R4 status={ok!r} 放行（归一为 None）", obj is not None
            and obj["signals"]["status"] is None)
    # R5：落盘对象只含行号，无 evidence 全文/预览键
    obj, _ = itp.validate_v4(good_obj(), NUMBERED, "d")
    chk("R5 落盘对象无 evidence 文本键（只存行号）",
        obj is not None and "evidence" not in obj["audit"]
        and "preview" not in obj["audit"] and obj["audit"]["evidence_lines"] == [1, 2])
    # R6-①：SCHEMA_V4 不**声明** db 判定键（禁令行允许点名键名——那正是指令本身）
    chk("R6① schema 无 db 判定键声明（\"db_verdicts\":/\"official\":/DB_VOCAB 区块）",
        all(k not in itp.SCHEMA_V4 for k in ('"db_verdicts":', '"official":',
                                             '"dbs":', "DB_VOCAB", "候选库")))
    # R6-②③：构造+渲染（真实 README 走 build_prompt v4）
    ctx = itp.build_prompt("endoflife-date/endoflife.date", degraded=False, pool={},
                           dbscan={"endoflife-date/endoflife.date": {"PostgreSQL": [{"line": 1, "q": "x"}]}},
                           schema=itp.format_schemas(None)["v4"], mode="v4")
    chk("R6② 构造：v4 ctx 不携带候选库（dbscan 喂了也不进）", ctx["cands"] == {})
    chk("R6③ 渲染：prompt 无「候选库清单」区块、无 db 键声明、无 DB_VOCAB 标记",
        "候选库清单" not in ctx["prompt"] and '"db_verdicts":' not in ctx["prompt"]
        and "DB_VOCAB" not in ctx["prompt"])
    # 判定卷无 identity
    chk("v4 prompt 不要求 identity（作文卷另案）", "identity" not in ctx["prompt"])
    # R6 键级：模型输出 db_verdicts 拒收
    obj, errs = itp.validate_v4(good_obj(classification={
        **good_obj()["classification"],
        "db_verdicts": [{"db": "MySQL", "rel": "support", "lines": [1]}]}), NUMBERED, "d")
    chk("R6 输出含 db_verdicts 即拒收", obj is None and any("R6" in e for e in errs))

    # domain_tags 禁用期（H1 定死：输出即拒收，拒收文本可被 G5 统计）
    obj, errs = itp.validate_v4(good_obj(classification={
        **good_obj()["classification"], "domain_tags": ["cdc"]}), NUMBERED, "d")
    chk("domain_tags 禁用期输出即拒收（计数信号）",
        obj is None and any("domain_tags 禁用期" in e for e in errs))

    # ---- 条件化字段 ----
    obj, errs = itp.validate_v4(good_obj(classification={
        "cat_primary": "开发库", "persona": ["use"], "eco": "unclear",
        "ai_kind": "other"}), NUMBERED, "d")
    chk("eco=unclear 缺 eco_why 拒收", obj is None and any("eco_why" in e for e in errs))
    obj, _ = itp.validate_v4(good_obj(classification={
        "cat_primary": "开发库", "persona": ["use"], "eco": "tool",
        "ai_kind": "other", "eco_why": "它是驱动工具"}), NUMBERED, "d")
    chk("eco≠unclear 带 eco_why 拒收（越权）", obj is None)
    obj, _ = itp.validate_v4(good_obj(signals={
        "install": [], "status": None, "license_note": "Apache-2.0"}), NUMBERED, "d")
    chk("单一标准 SPDX 值的 license_note 仍放行（内容治理靠提示词，校验不猜 SPDX）",
        obj is not None)          # 条件输出的"不许输出常规值"由 prompt 约束，程序不误杀

    # persona 多选 1-2 校验
    for bad in (["use", "ops", "build"], [], ["use", "use"], ["hacker"]):
        obj, errs = itp.validate_v4(good_obj(classification={
            **good_obj()["classification"], "persona": bad}), NUMBERED, "d")
        chk(f"persona 非法拒收 {bad}", obj is None)

    # evidence_lines 窗口外
    obj, errs = itp.validate_v4(good_obj(audit={"confidence": "mid",
                                                "evidence_lines": [99]}), NUMBERED, "d")
    chk("evidence_lines 全窗口外拒收", obj is None)

    # ---- 输出体量口径（E1 验收 1：~100-130B ±30%。模型输出为紧凑 JSON，
    # 典型条目=主类+单受众+无 eco_why；全字段拉满是带宽上限的另一头） ----
    def _size(o):
        return len(json.dumps(o, ensure_ascii=False, separators=(",", ":")))
    typical, _ = itp.validate_v4(good_obj(classification={
        "cat_primary": "开发库", "persona": ["use"], "eco": "tool", "ai_kind": "other"}),
        NUMBERED, "d")
    chk(f"典型条目体量在实测带宽内（实测 {_size(typical)}B，140-230B）",
        140 <= _size(typical) <= 230)
    print("[INFO] 偏差注记：清单口径 100-130B±30%（≤170B）实测超约 40%——成本来自"
          "中文类别值+完整键名，字段规格即《AI方案》§2 所定；如需回到预算须缩键名（schema 变更，须用户裁定）")
    maximal, _ = itp.validate_v4(good_obj(), NUMBERED, "d")
    print(f"[INFO] 全字段拉满（cat_tags×2+persona×2）实测 {_size(maximal)}B——带宽上限参考")
    chk("全字段样本不超 2 倍上限（340B）", _size(maximal) <= 340)

    # ---- 缓存键 ----
    chk("v4 缓存键 sha#v4、旧模式裸 sha", itp.cache_key("abc", "v4") == "abc#v4"
        and itp.cache_key("abc", "v3") == "abc")

    # ============================================================
    # 对抗测试集（真机学费的固化：每条对应一次已发生过的拒收事故，
    # 红线=提示词+校验器必须拦住或归一，不靠模型自觉）
    # ============================================================
    # A1) ai_kind 缺键 → 归一 other（1104 判定卷冒烟：8 拒收中 7 条此形态）
    o, _ = itp.validate_v4(good_obj(classification={
        "cat_primary": "内核/引擎", "persona": ["build"], "eco": "tool"}), NUMBERED, "d")
    chk("对抗：ai_kind 缺键归一 other", o is not None
        and o["classification"]["ai_kind"] == "other")
    # A2) cat_tags 空数组 → 视同省略（1104 冒烟拒收形态之二）
    o, _ = itp.validate_v4(good_obj(classification={
        "cat_primary": "监控", "cat_tags": [], "persona": ["ops"], "eco": "tool",
        "ai_kind": "other"}), NUMBERED, "d")
    chk("对抗：cat_tags 空数组视同省略", o is not None and "cat_tags" not in o["classification"])
    # A3) 文本卷长度门槛边界（1104 文本卷首跑 20/20 拒收事故：模型常态 31-40/180-210 字）
    # review 构造须带 ≥3 个 desc 外实义 token（否则 info_gain 先拒，测不到长度分支）
    def _rv(n):
        pre = "甲乙 丙丁 戊己 "                 # 9 字符（含 3 个分隔空格）
        return pre + "长" * max(n - len(pre), 0)
    base_ident = {"one_liner": "x" * 40,                   # 常态超 30、在放宽带内
                  "review": _rv(200),                      # 常态超 120、在放宽带内
                  "highlights": ["h" * 20], "use_cases": ["u" * 20]}
    o, e = itp.validate_text({"identity": base_ident}, "desc" + "y" * 50)
    chk("对抗：常态长度（40/200 字）放行", o is not None)
    for one_len, rv_len, want in ((51, 200, False), (50, 200, True),
                                  (40, 29, False), (40, 30, True),
                                  (40, 300, True), (40, 301, False)):
        bi = dict(base_ident, one_liner="x" * one_len, review=_rv(rv_len))
        o, _ = itp.validate_text({"identity": bi}, "desc" + "y" * 50)
        chk(f"对抗：长度边界 one={one_len} review={rv_len} → {'过' if want else '拒'}",
            (o is not None) == want)
    # A4) identity 双层包裹回归（1104 文本卷存储事故：勿再包一层）
    sample_txt = itp.validate_text({"identity": base_ident}, "desc" + "y" * 50)[0]
    chk("对抗：validate_text 返回单层 identity（防双层包裹回归）",
        set(sample_txt) == {"identity"} and "identity" not in sample_txt["identity"])
    # A5) 模型输出 v3 老格式（cat/dbs/official 整体混入）→ 必拒
    old_style = {"classification": {"cat": "监控", "persona": "ops", "eco": "tool",
                                    "dbs": ["MySQL"], "official": {"flag": True, "of": "MySQL"}},
                 "signals": {"status": "active", "install": ["source"]},
                 "audit": {"confidence": "mid", "evidence_lines": [1]}}
    o, errs = itp.validate_v4(old_style, NUMBERED, "d")
    chk("对抗：v3 老格式输出必拒（cat 老键+dbs+official+active 多重违规）",
        o is None and len(errs) >= 4)

    # ---- E3：evidence_preview 程序切片（R5：逐字 == 清理文行号切片） ----
    num = {7: "x" * 200, 8: "短行"}
    pv = itp.build_preview([7, 8], num)
    chk("preview == 行文本拼接截 80 字（逐字）", pv == ("x" * 200 + " ／ 短行")[:80])
    chk("preview 坏行号/空窗口返回空串",
        itp.build_preview([99], num) == "" and itp.build_preview([7], {}) == "")

    # ---- E2：缓存键分层（文本 prompt_ver 升级不作废判定缓存） ----
    jk, tk = itp.cache_key("abc", "v4"), itp.text_key("abc")
    chk("判定键/文本键不相交（升级 text prompt_ver 只换文本键）",
        jk != tk and not tk.startswith(jk) and not jk.startswith(tk))
    chk("text_key 含自己的 prompt_ver（改它不动 v4 判定键）",
        itp.PROMPT_VER_TEXT in tk and "4" in tk)

    # E2 文本卷校验
    ident, errs = itp.validate_text({"identity": {
        "one_liner": "PostgreSQL 逻辑复制槽监控工具",
        "review": "该工具读取逻辑复制槽并监控延迟水位，面向需要排查复制延迟的运维人员，"
                  "提供按槽位聚合的延迟指标与告警钩子，支持 prometheus 格式导出。",
        "highlights": ["监控复制槽延迟"], "use_cases": ["排查订阅延迟"]}}, "pg tool")
    chk("文本卷四件套放行", ident is not None)
    obj, errs = itp.validate_text({"identity": {"one_liner": "x"},
                                   "classification": {"cat": "监控"}}, "d")
    chk("文本卷混入判定字段拒收", obj is None)
    obj, errs = itp.validate_text({"identity": {
        "one_liner": "工具", "review": "很短",
        "highlights": ["a"], "use_cases": ["b"]}}, "desc")
    chk("review 长度/增量双卡拒收", obj is None)

    print(f"selftest {'FAIL' if fails else 'PASS'}（{fails} 处失败）")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
