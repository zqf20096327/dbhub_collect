# -*- coding: utf-8 -*-
"""runlog —— 条目级结构化日志（jsonl），优化决策的数据燃料。

一行一条解读（生产 interpret 与 golden_eval 共用 schema，run_id 区分）：
  输入侧   in_raw_chars / in_clean_chars / prompt_chars / visible_lines /
           cand_dbs / cand_lines_out（窗口外候选行数，漏判归因的关键）
  耗时     t_api_s（AIClient 打点累计）/ t_total_s（judge 全程含重试）/ api_tries
  轨迹     validate_attempts / violations_all（每次尝试的违规快照，重试自愈≠救不回）
  结果     kind / cat / eco / dbs / verdicts / evidence_lines / confidence /
           xcheck / enum_fixes / review_cleared；拒收附全文 raw（不截断）
运行收尾追加 run_summary 一行（通过率、拒收原因帕累托、p50/p95、总字符量）。

约定：只在主线程调用（与缓存落账同点，无竞态）；logs/*.jsonl 不入 git（体积）；
      按天分文件，单条 ~600B，月度 gzip 归档即可。
"""
from __future__ import annotations

import json
import statistics
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOGDIR = ROOT / "state" / "logs"


def _path() -> Path:
    LOGDIR.mkdir(exist_ok=True)
    return LOGDIR / f"interp_{datetime.now().strftime('%Y%m%d')}.jsonl"


def _append(rec: dict) -> None:
    rec["ts"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with _path().open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def log_item(rec: dict) -> None:
    """条目级一行。调用方保证在主线程。"""
    _append({"type": "item", **rec})


def log_summary(rec: dict) -> None:
    """运行级汇总一行。"""
    _append({"type": "run_summary", **rec})


def pct(vals: list[float], p: float) -> float:
    """简单分位数（p95 观测尾部用）。"""
    if not vals:
        return 0.0
    s = sorted(vals)
    k = min(len(s) - 1, max(0, int(round(p / 100 * (len(s) - 1)))))
    return round(s[k], 1)


def summarize_items(items: list[dict]) -> dict:
    """从条目记录聚合运行摘要（interpret.run 与 golden_eval 共用）。"""
    done = [r for r in items if r.get("kind") == "done"]
    rej = [r for r in items if r.get("kind") == "rejected"]
    fail = [r for r in items if r.get("kind") == "failed"]
    secs = [r.get("t_total_s") or 0 for r in items]
    viol: dict[str, int] = {}
    for r in rej:
        for v in (r.get("violations") or [])[:5]:
            key = str(v).split("（")[0].split(":")[0][:36]
            viol[key] = viol.get(key, 0) + 1
    return {"n": len(items), "done": len(done), "rejected": len(rej), "failed": len(fail),
            "pass2%": round(len(done) * 100 / len(items), 1) if items else 0,
            "pass1%": round(sum(1 for r in done if r.get("validate_attempts") == 1) * 100
                            / len(items), 1) if items else 0,
            "t_total_p50": pct(secs, 50), "t_total_p95": pct(secs, 95),
            "t_api_mean": round(statistics.mean([r.get("t_api_s") or 0 for r in items]), 1)
            if items else 0,
            "out_chars_total": sum(r.get("out_chars") or 0 for r in items),
            "reject_reasons": dict(sorted(viol.items(), key=lambda x: -x[1])[:10])}
