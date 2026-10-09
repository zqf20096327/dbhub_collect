# -*- coding: utf-8 -*-
"""复查复现：昨日 22 条拒收按家族各挑代表，走当前代码全流程验证。
只读状态文件，不写任何 state。"""
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "interpret"))
sys.path.insert(0, str(ROOT / "config"))
sys.path.insert(0, str(ROOT / "lib"))

for ln in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
    ln = ln.strip()
    if ln and not ln.startswith("#") and "=" in ln:
        k, v = ln.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())

import strategy                      # noqa: E402
import interpret                     # noqa: E402

gen = strategy.derive()
schemas = interpret.format_schemas(gen)
from pool_store import read_any
pool = {it["full_name"]: it
        for it in read_any(interpret.latest_pool())}
dbscan = json.loads((ROOT / "state" / "db_scan.json").read_text(encoding="utf-8"))
ai = interpret.AIClient()

# (fn, degraded, 失败家族) —— 10-09 软放行改造后的代表项
CASES = [
    ("imqueue/pg-pubsub", False, "禁词『优雅』(软放行:scrub)"),
    ("ZhengHe-MD/tidb-hp-hw", False, "禁词三字段(软放行:scrub)"),
    ("diguage/mysql-notes", False, "禁词书名《高性能MySQL》(软放行:scrub)"),
    ("winterland1989/mysql-haskell", False, "行号窗外(行号提示/丢裁决)"),
]

for fn, degraded, why in CASES:
    ctx = interpret.build_prompt(fn, degraded, pool, dbscan,
                                 interpret.pick_schema(schemas, degraded, "v3"),
                                 mode="v3")
    r = interpret.judge(fn, "repro", degraded, ctx, ai, gen, mode="v3")
    if r["kind"] == "done":
        o = r["obj"]
        cls, aud = o["classification"], o["audit"]
        vsum = [f"{v['db']}:{v['rel']}" for v in cls.get("db_verdicts") or []]
        print(f"[PASS] {fn} ({why})")
        print(f"       cat={cls.get('cat')} eco={cls.get('eco')} dbs={cls.get('dbs')} "
              f"conf={aud.get('confidence')} verdicts={vsum} attempts={r.get('attempts')}")
    else:
        print(f"[{r['kind'].upper()}] {fn} ({why})")
        print(f"       violations={r.get('violations') or r.get('error')}")
        print(f"       raw_head={(r.get('raw') or '')[:300]!r}")
    sys.stdout.flush()
