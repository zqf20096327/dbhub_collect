# -*- coding: utf-8 -*-
"""T0 出池闸门自检（ATTRIBUTION_TASKS T0 验收）：零网络，tmp 目录写 audit。

跑法：python collect/selftest_exit_gate.py（退出码 0=全绿）

验收三条（卡原文）：构造 3 个用例（真无关/没证据/已判 no_evidence）
→ 只有第一类出池；audit 可查。
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
for d in (ROOT, ROOT / "lib", ROOT / "config", ROOT / "collect"):
    if str(d) not in sys.path:
        sys.path.insert(0, str(d))

from pool_core import _apply_exit_gate  # noqa: E402


def main() -> int:
    fails = 0
    tmp = Path(tempfile.mkdtemp(prefix="exit_gate_"))
    audit = tmp / "pool_exit_audit.json"

    # ── 用例 1：三类混批——只有"真无关"（judged_no_support/oos/edu）准出 ──
    verdicts = {
        "a/real-unrelated": {"status": "judged_no_support"},   # 真无关（卡例 1）
        "b/no-record": {},                                     # 没证据：台账无记录（卡例 2）
        "c/no-evidence": {"status": "no_evidence"},            # 已判 no_evidence（卡例 3）
        "d/draft": {"status": "draft"},                        # 有候选证据：绝不出
        "e/recheck": {"status": "recheck"},
        "f/gated": {"status": "gated_app_cat"},
        "g/desc": {"status": "desc_pending"},
        "h/oos": {"status": "oos"},                            # 范围外=真无关类
        "i/edu": {"status": "edu"},                            # 教学类=真无关类
        "j/api-error": {"status": "api_error"},                # 侦查未完成：HOLD
    }
    cands = set(verdicts)
    got = _apply_exit_gate(cands, verdicts=verdicts, audit_path=audit)
    expect = {"a/real-unrelated", "h/oos", "i/edu"}
    if got != expect:
        print(f"[FAIL] 混批过闸：expect {sorted(expect)} got {sorted(got)}")
        fails += 1
    else:
        print(f"[PASS] 混批 10 用例：仅真无关 3 条出池，其余 7 条拦下留池")

    # ── 用例 2：台账整体缺失 = 关闸全 HOLD（宁多收不漏收）──
    got2 = _apply_exit_gate(cands, verdicts={}, audit_path=tmp / "a2.json")
    if got2:
        print(f"[FAIL] 台账缺失应关闸，却出池 {sorted(got2)}")
        fails += 1
    else:
        print("[PASS] 台账缺失：关闸，全部留池")

    # ── 用例 3：audit 可查（fn/原因/当时证据状态 + 轮摘要 + 幂等覆盖）──
    doc = json.loads(audit.read_text(encoding="utf-8"))
    items, runs = doc["items"], doc["runs"]
    need = {"a/real-unrelated": "judged_no_support",
            "h/oos": "oos", "i/edu": "edu"}
    for fn, st in need.items():
        it = items.get(fn)
        if not it or it["status"] != st or not it["reason"] or not it["first_exit"]:
            print(f"[FAIL] audit 缺记录：{fn} → {it}")
            fails += 1
    if not runs or runs[-1]["exits"] != 3 or runs[-1]["holds"] != 7:
        print(f"[FAIL] audit 轮摘要不对：{runs[-1] if runs else None}")
        fails += 1
    if fails == 0:
        # 幂等覆盖：同批再过一轮，new=0、items 不翻倍
        _apply_exit_gate(cands, verdicts=verdicts, audit_path=audit)
        doc2 = json.loads(audit.read_text(encoding="utf-8"))
        if len(doc2["items"]) != len(items) or doc2["runs"][-1]["new"] != 0:
            print("[FAIL] audit 幂等：重复过闸 items 翻倍或 new≠0")
            fails += 1
        else:
            print("[PASS] audit 可查：3 条出池记录含 status/reason/日期，轮摘要"
                  " exits=3 holds=7，重复过闸幂等")

    verdict = "PASS" if not fails else "FAIL"
    print(f"[{verdict}] T0 出池闸门自检")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
