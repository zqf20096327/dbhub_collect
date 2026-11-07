# -*- coding: utf-8 -*-
"""富集 staleness 体检（零 API、不采集）：python enrich/health.py [--json]

每晚 enrich 收尾会写同一份 state/enrich_health.json；本脚本用于随时单跑：
  - 每层每维覆盖率（有 dim_ts 的仓 / 该层仓数）
  - 数据年龄 p50/p95（天）
  - 值有效性占比（状态量维度没有 push 就不算陈旧，口径见 health_report）
告警线 95%，退出码 1=有告警（便于手动巡检；CI 不挂它，避免告警阻断采集）。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = ROOT
for _d in (ROOT, ROOT / "lib", ROOT / "config", ROOT / "enrich"):
    if str(_d) not in sys.path:
        sys.path.insert(0, str(_d))

import enrich                      # noqa: E402
from enrich_store import load_cache  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description="富集 staleness 体检（零 API）")
    ap.add_argument("--pool", default=str(HERE / "data" / "snapshot_latest" / "pool.json"))
    ap.add_argument("--json", action="store_true", help="打印完整 JSON")
    args = ap.parse_args()
    pool = json.loads(Path(args.pool).read_text(encoding="utf-8"))
    st_path = HERE / "state" / "enrich_state.json"
    st = (json.loads(st_path.read_text(encoding="utf-8"))
          if st_path.is_file() else {"items": {}})
    rep = enrich.health_report(pool, load_cache(), st["items"])
    if args.json:
        print(json.dumps(rep, ensure_ascii=False, indent=1))
    else:
        for t, cell in rep["tiers"].items():
            print(f"{t:4s} n={cell['n']}")
            for d, m in cell["dims"].items():
                print(f"  {d:9s} ttl={str(m['ttl']):>4s} 覆盖={m['coverage']:.2f} "
                      f"p50={m['age_p50']} p95={m['age_p95']} "
                      f"有效={m['valid_ratio']} "
                      f"(已知 {m['age_known']}/待定 {m['age_pending']}/未知 {m['age_unknown']})")
        print()
        print("告警：" + ("无" if not rep["alerts"] else ""))
        for a in rep["alerts"]:
            print("  " + a)
    return 1 if rep["alerts"] else 0


if __name__ == "__main__":
    sys.exit(main())
