# -*- coding: utf-8 -*-
"""log_report —— 晨间读数：聚合 state/logs/ 的条目级 jsonl。

用法：
  python interpret/log_report.py                # 今天
  python interpret/log_report.py 20260930       # 指定日期（可多个）
输出四张视图：量与通过率 / 速度 / 拒收原因帕累托 / 字段填充画像。
"""
from __future__ import annotations

import json
import statistics
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOGDIR = ROOT / "state" / "logs"


def load(day: str) -> list[dict]:
    p = LOGDIR / f"interp_{day}.jsonl"
    if not p.is_file():
        return []
    out = []
    for ln in p.read_text(encoding="utf-8").splitlines():
        try:
            out.append(json.loads(ln))
        except json.JSONDecodeError:
            continue
    return out


def pct(vals: list[float], p: int) -> float:
    if not vals:
        return 0.0
    s = sorted(vals)
    return round(s[min(len(s) - 1, p * (len(s) - 1) // 100)], 1)


def report(days: list[str]) -> None:
    recs = [r for d in days for r in load(d) if r.get("type") == "item"]
    if not recs:
        print(f"{days} 无条目日志（{LOGDIR}）")
        return
    runs = sorted({r.get("run_id") for r in recs if r.get("run_id")})
    done = [r for r in recs if r.get("kind") == "done"]
    rej = [r for r in recs if r.get("kind") == "rejected"]
    fail = [r for r in recs if r.get("kind") == "failed"]
    t_all = [r.get("t_total_s") or 0 for r in recs]
    t_api = [r.get("t_api_s") or 0 for r in recs]

    print(f"═══ {days} · {len(recs)} 条 · runs={len(runs)} · prompt_ver="
          f"{sorted({r.get('prompt_ver') for r in recs})} ═══")
    print(f"[量] done {len(done)} · rejected {len(rej)} · api_failed {len(fail)} · "
          f"最终通过率 {len(done)*100/max(len(recs),1):.1f}% · "
          f"一次通过率 {sum(1 for r in done if r.get('validate_attempts')==1)*100/max(len(recs),1):.1f}%")
    hrs = (max(t_all) and 1) and sum(t_all) / 60 / max(1, len({r.get('run_id') for r in recs})) / 60
    print(f"[速] 单条 p50 {pct(t_all,50)}s · p95 {pct(t_all,95)}s · api 段均值 "
          f"{statistics.mean(t_api):.1f}s · 平均输出 {statistics.mean([r.get('out_chars') or 0 for r in recs]):.0f} 字符")
    viol: Counter = Counter()
    for r in rej:
        for v in (r.get("violations") or [])[:5]:
            viol[str(v).split("（")[0].split(":")[0][:36]] += 1
    if viol:
        print("[拒收帕累托]", dict(viol.most_common(8)))
    cats = Counter((r.get("cat") or "?") for r in done)
    print("[cat 分布]", dict(cats.most_common()))
    n = max(len(done), 1)
    for f, key in (("dbs", "dbs"), ("review空置", "review_cleared"), ("xcheck触发", "xcheck"),
                   ("低置信", None)):
        if key:
            c = sum(1 for r in done if r.get(key))
        else:
            c = sum(1 for r in done if (r.get("confidence") == "low"))
        print(f"[画像] {f}: {c} ({c*100//n}%)")
    empty_inst = sum(1 for r in done if not (r.get("verdicts")))
    print(f"[画像] 无库归属(verdicts空): {empty_inst} ({empty_inst*100//n}%)")
    # 重试自愈 vs 救不回（violations_all 双元素=重试过）
    healed = sum(1 for r in done if len(r.get("violations_all") or []) > 1)
    print(f"[轨迹] 靠重试救回: {healed} ({healed*100//n}%) · 枚举归一修复: "
          f"{sum(r.get('enum_fixes') or 0 for r in done)} 处")


if __name__ == "__main__":
    from datetime import datetime
    days = sys.argv[1:] or [datetime.now().strftime("%Y%m%d")]
    report(days)
