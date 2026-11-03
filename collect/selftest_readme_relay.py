# -*- coding: utf-8 -*-
"""README 月度接力自检（零网络）：复现 2026-11-03 线上崩溃并防回归。

跑法：python collect/selftest_readme_relay.py（退出码 0=全绿）

事故：readme_sweep BudgetOut 续窗路径 pick_targets(args, pool, items) 漏传
cycle → 第一窗跑满调用数后进程崩（readme-monthly 双 job 同崩；两窗 4200 调的
calibrated 断点虽被 always 提交保住，但每个 job 只能推进一窗）。
用例：假客户端 304 应答 + 每窗 2 调上限 → 强制反复走"本窗停止→续窗"崩溃点，
断言 5 目标跨 ≥3 窗全部校准完成（修复前在第一次续窗即 TypeError）。
"""
from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
for d in (ROOT, ROOT / "lib", ROOT / "collect"):
    if str(d) not in sys.path:
        sys.path.insert(0, str(d))

import readme_sweep  # noqa: E402
from gh import BudgetOut  # noqa: E402

CYCLE = "MTEST-RELAY"


class FakeClient:
    """304 应答 + 到窗调用帽抛 BudgetOut（GitHubClient 预算语义的最小面）。"""

    def __init__(self, budget):
        self.budget = budget

    def core_rate_limit(self):
        return {"remaining": 5000}          # 远高于保底线：不触跨窗睡等

    def readme_conditional(self, fn, etag):
        b = self.budget
        if b.calls >= b.max_calls:
            raise BudgetOut(f"调用数达上限 {b.max_calls}")
        b.calls += 1
        return (304, None, None)             # 整数状态码（同 GitHubClient 返回面）


def main() -> int:
    fails = 0
    tmp = Path(tempfile.mkdtemp(prefix="readme_relay_"))
    pool = [{"full_name": f"o/r{i}", "stars": i, "pushed_at": "2026-11-01T00:00:00Z"}
            for i in range(5)]
    pool_path = tmp / "pool.json"
    pool_path.write_text(json.dumps(pool), encoding="utf-8")

    # 隔离产物落点（STATE/READMES/HERE 均为模块全局，run() 读全局名）
    readme_sweep.STATE = tmp / "state" / "readme_state.json"
    readme_sweep.READMES = tmp / "readmes"
    readme_sweep.HERE = tmp
    readme_sweep.GitHubClient = FakeClient

    args = argparse.Namespace(
        mode="monthly", pool=str(pool_path), cycle=CYCLE,
        max_calls=2, max_minutes=30.0, wait_windows=2, max_total_minutes=None,
        limit=0, layer1=False, v=False)
    readme_sweep.run(args)                    # 修复前此处 TypeError（续窗 pick_targets）

    summary = json.loads((tmp / "state" / "readme_summary.json")
                         .read_text(encoding="utf-8"))
    st = json.loads(readme_sweep.STATE.read_text(encoding="utf-8"))
    cal = [fn for fn, r in st["items"].items() if r.get("calibrated") == CYCLE]
    checks = [
        (summary["cycle_complete"] is True, "周期完成标记 cycle_complete",
         f'got {summary["cycle_complete"]}'),
        (summary["counts"]["unchanged"] == 5, "5 目标全 304 过账",
         f'got {summary["counts"]}'),
        (summary["windows"] >= 3, "跨 ≥3 窗接力（每次续窗都经过原崩溃点）",
         f'got {summary["windows"]}'),
        (len(cal) == 5, "state 中 5 仓全打周期戳", f"got {len(cal)}"),
        (not summary["stop_reason"], "自然收尾无预算停止",
         f'got {summary["stop_reason"]}'),
    ]
    for ok, what, detail in checks:
        if ok:
            print(f"[PASS] {what}")
        else:
            print(f"[FAIL] {what}（{detail}）")
            fails += 1

    verdict = "PASS" if not fails else "FAIL"
    print(f"[{verdict}] README 月度接力自检")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
