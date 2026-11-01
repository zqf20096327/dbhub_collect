# -*- coding: utf-8 -*-
"""试点重采（11-01 用户批准试点版）：T3b 漏配大户放宽采集上限重采 → 引擎免费重判。

背景：T3b 金标 31 漏配库位中 26 个属"采集上限截断"（airbyte/grafana 三项满冠、
sqlmap 路径线索字典序截断）——数据在仓库里没采上来，README/AI 都补不了。
本脚本对 10 仓放宽 CAPS（dep 60/image 24/ci 40/路径线索 200）重采，
用引擎 v0.3.0 免费重判，量"漏配回收率"。只读不写证据分片（试点不污染管线）。

用法：python tools/pilot_recollect.py [--only fn1,fn2]
成本：树 ~2 Core 调/仓 + raw CDN 免费不计；10 仓约 3-5 分钟。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for p in (str(ROOT), str(ROOT / "lib"), str(ROOT / "evidence")):
    if p not in sys.path:
        sys.path.insert(0, p)

import evidence_collect as ec                     # noqa: E402  采集器全复用
from gh import GitHubClient                       # noqa: E402
from attribution.api import judge                 # noqa: E402
from attribution.matcher import build_pack        # noqa: E402

# T3b 金标漏配（代码仓；教程/书单 5 库位走内容口径不重采）
TARGETS = {
    "airbytehq/airbyte": ["ClickHouse", "MariaDB", "Oracle", "SQLite", "TiDB"],
    "eosphoros-ai/DB-GPT": ["ClickHouse", "GaussDB", "OceanBase", "PostgreSQL",
                            "SQL Server", "SQLite", "openGauss"],
    "sqlmapproject/sqlmap": ["ClickHouse", "MySQL", "Oracle", "PostgreSQL", "SQL Server"],
    "grafana/grafana": ["SQL Server"],
    "coollabsio/coolify": ["ClickHouse", "SQLite"],
    "alibaba/AliSQL": ["MySQL"],
    "mergestat/mergestat-lite": ["PostgreSQL"],
    "scalikejdbc/scalikejdbc": ["SQLite"],
    "tursodatabase/turso": ["PostgreSQL"],
    "taosdata/TDengine": ["Oracle", "SQLite"],
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default=None, help="只采指定仓（逗号分隔 fn）")
    args = ap.parse_args()
    targets = {k: v for k, v in TARGETS.items()
               if not args.only or k in args.only.split(",")}

    # 放宽上限（试点档；生产接入要回 evidence_collect 正式改）
    ec.CAPS.update(dep=60, image=24, ci=40)
    ec.PATH_CLUE_CAP = 200

    import pool_store
    items, _ = pool_store.load_latest("pool")
    pool = {i.get("full_name"): i for i in items}

    client = GitHubClient()
    raw = ec.RawFetcher(workers=4)

    recovered = total = 0
    for fn, want in targets.items():
        total += len(want)
        try:
            rec = ec.collect_repo(client, raw, fn,
                                  {"stars": (pool.get(fn) or {}).get("stars") or 0,
                                   "pushed_at": (pool.get(fn) or {}).get("pushed_at") or ""},
                                  None)
        except Exception as e:                                   # noqa: BLE001
            print(f"[ERR] {fn}: {e}")
            continue
        from collections import Counter
        kinds = Counter(f.get("kind") for f in rec.get("files") or [])
        n_paths = len((rec.get("clues") or {}).get("paths") or [])
        st = rec.get("status")
        # partial（个别 404/截断）不影响指纹主体——判定按 ok 口径量回收（试点口径）
        rec.setdefault("collected_at", ec._iso_now())
        v = judge(build_pack(fn, dict(rec, status="ok"),
                             {"topics": (pool.get(fn) or {}).get("topics") or []}))
        got = set(v["dbs"])
        hit = [d for d in want if d in got]
        per = {d: e["votes"] for d, e in v["per_db"].items() if d in want}
        recovered += len(hit)
        miss = [d for d in want if d not in got]
        print(f"{fn:32s} files={dict(kinds)} paths={n_paths} status={st}")
        print(f"   引擎判：{v['dbs']} | 回收 {hit}（票 {per}）| 仍缺 {miss}")

    print(f"\n=== 漏配回收：{recovered}/{total} = {recovered/total:.0%}（raw {raw.count} 次"
          f" err {raw.errors}；Core {client.stats_summary()}）===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
