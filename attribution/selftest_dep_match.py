# -*- coding: utf-8 -*-
"""T1b 离线自检：误伤契约 + 双档互斥 + @types 排除 + 词表完整性。零网络。

跑法：python attribution/selftest_dep_match.py（退出码 0=全绿）
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from attribution.dep_match import load_vocab, match_dep


def main() -> int:
    fails = 0
    cases = json.loads(
        (ROOT / "attribution" / "fixtures" / "false_positives.json")
        .read_text(encoding="utf-8"))["cases"]

    # 1) 契约逐条：命中库集合精确相等 + dev 标志语义正确
    for c in cases:
        got = match_dep(c["pkg"], dev=c.get("dev", False))
        dbs = sorted({h["db"] for h in got})
        if dbs != sorted(c["expect"]):
            print(f"[FAIL] {c['pkg']}: expect {c['expect']} got {dbs}")
            fails += 1
            continue
        if c.get("expect_dev") and not all(h["dev"] for h in got):
            print(f"[FAIL] {c['pkg']}: dev 命中但降档标志缺失")
            fails += 1
        if not c.get("dev") and any(h["dev"] for h in got):
            print(f"[FAIL] {c['pkg']}: 非 dev 输入却带 dev 标志")
            fails += 1

    # 2) 双档互斥：exact 词加任意后缀不得命中（子串档不得漏出 exact 词）
    vocab = load_vocab()
    for w in vocab["exact"]:
        if match_dep(w + "-not-a-driver"):
            print(f"[FAIL] exact 词 '{w}' 加后缀仍被命中——子串档漏出")
            fails += 1

    # 3) @types/ 全排除：对全部词表词生成前缀样本逐个验证
    for w in list(vocab["substring"]) + list(vocab["exact"]):
        if match_dep("@types/" + w):
            print(f"[FAIL] @types/{w} 未被排除")
            fails += 1

    # 4) 词表完整性：17 库 drivers∪exact 覆盖 + exact 词不在子串表
    from config.db_profiles import PROFILES
    names = {p["name"] for p in PROFILES if p.get("enabled", True)}
    covered = set(vocab["substring"].values()) | set(vocab["exact"].values())
    if names - covered:
        print(f"[FAIL] 库无任何驱动词：{names - covered}")
        fails += 1
    if overlap := set(vocab["exact"]) & set(vocab["substring"]):
        print(f"[FAIL] exact 与子串表重叠：{overlap}")
        fails += 1

    verdict = "PASS" if not fails else "FAIL"
    print(f"[{verdict}] 误伤契约 {len(cases) - fails if fails < len(cases) else len(cases)}"
          f"/{len(cases)} + 双档互斥 {len(vocab['exact'])} 词"
          f" + @types 排除 + 词表完整性（{len(names)} 库）")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
