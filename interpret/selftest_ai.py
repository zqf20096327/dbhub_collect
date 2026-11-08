# -*- coding: utf-8 -*-
"""AI 解析测试总闸（工作清单通用验收命令）。

每完成一个工作项，先跑本闸：全绿才允许在工作清单打勾。单测各自独立进程，
任一非零即整体非零，便于 CI / 手工一眼判定。

覆盖：
  selftest_v4.py           判定卷 v4 红线（R1/R3/R4/R5/R6）+ 文本卷长度/增量
  selftest_vocab_control.py vc1.0 词控（75 词/证据包/校验器/键分层）
  lib/interp_read.py       读层（dbs/ai_flag/activity/evidence 派生）
  tools/check_layer_keys.py 层键规则（拼键/解键/形态/契约对拍）
  lib/interp_layer_store.py 分层存储（解耦/分片/断点/拼接）
  gen_manifest.py          代际清单结构（键模板对拍代码、计数自洽、词表指纹）
  dead_letter.py           死信表 API（四类/分层/覆盖/非法输入）
  selftest_runner.py       runner 机制（超时/429/额度等待/校验重试/断点）

用法：
  python interpret/selftest_ai.py            # 全跑
  python interpret/selftest_ai.py -v         # 保留各套完整输出
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable
SUITES = [
    ("v4 判定卷/文本卷", [PY, "interpret/selftest_v4.py"]),
    ("vc1.0 词控", [PY, "interpret/selftest_vocab_control.py"]),
    ("读层 interp_read", [PY, "lib/interp_read.py", "--selftest"]),
    ("层键规则", [PY, "tools/check_layer_keys.py", "--selftest"]),
    ("分层存储", [PY, "lib/interp_layer_store.py", "--selftest"]),
    ("代际清单", [PY, "interpret/gen_manifest.py", "--selftest"]),
    ("死信表", [PY, "interpret/dead_letter.py", "--selftest"]),
    ("runner 机制", [PY, "interpret/selftest_runner.py"]),
]


def main() -> int:
    verbose = "-v" in sys.argv
    failed = []
    for name, cmd in SUITES:
        p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        tail = [ln for ln in (p.stdout or "").splitlines() if ln.strip()][-1:]
        ok = p.returncode == 0
        print(f"[{'PASS' if ok else 'FAIL'}] {name}"
              + (f" · {tail[0].strip()}" if tail else ""))
        if verbose or not ok:
            print((p.stdout or "") + (p.stderr or ""))
        if not ok:
            failed.append(name)
    print(f"\n总闸 {'PASS' if not failed else 'FAIL'}"
          f"（{len(SUITES) - len(failed)}/{len(SUITES)} 套通过）")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
