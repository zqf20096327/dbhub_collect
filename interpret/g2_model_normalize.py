# -*- coding: utf-8 -*-
"""G2-2 模型归一：把 deepseek 产出的旧条目清出缓存，让 v4/v4t 用 glm-5.3-flash 重烧。

为什么不能直接改条目：缓存条目不记模型（只有 state/logs/interp_*.jsonl 逐条记）。
所以口径是「同一个键的最后一条 done 日志是谁产的」——最后一条是 deepseek 的才清。
清之前整条备份到 state/shadow/g2_deepseek_backup.json；重跑由 interpret.py 的
「缓存缺即入队」自然驱动，不需要额外清单。

用法：
  python interpret/g2_model_normalize.py --dry-run   # 只看清单，不写盘
  python interpret/g2_model_normalize.py --apply     # 备份 + 从缓存删除
  python interpret/g2_model_normalize.py --verify    # 重跑后核对：不应再有 deepseek 为最后一条
  python interpret/g2_model_normalize.py --selftest
"""
from __future__ import annotations

import argparse
import glob
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for _d in (ROOT, ROOT / "lib", ROOT / "config", ROOT / "interpret"):
    sys.path.insert(0, str(_d))

import interpret as itp                          # noqa: E402
from interp_store import InterpCacheStore        # noqa: E402

TARGET_MODEL = "glm-5.3-flash"
BACKUP = ROOT / "state" / "shadow" / "g2_deepseek_backup.json"
LOGS = ROOT / "state" / "logs"


def key_of(mode: str, sha: str) -> str:
    return itp.cache_key(sha, "v4") if mode == "v4" else itp.text_key(sha)


def collect_latest(paths: list[str]) -> dict[tuple[str, str], tuple[str, str, str, str]]:
    """(mode, cache_key) -> (ts, model, fn, sha)，取该键最后一条 done 日志。"""
    latest: dict[tuple[str, str], tuple[str, str, str, str]] = {}
    for path in sorted(paths):
        for line in open(path, encoding="utf-8"):
            try:
                j = json.loads(line)
            except Exception:
                continue
            if j.get("kind") != "done":
                continue
            mode, sha = j.get("mode"), j.get("sha")
            if mode not in ("v4", "v4t") or not sha:
                continue
            k = key_of(mode, sha)
            cur = latest.get((mode, k))
            ts = j.get("ts") or ""
            if cur is None or ts >= cur[0]:
                latest[(mode, k)] = (ts, j.get("model") or "", j.get("fn") or "", sha)
    return latest


def plan(latest: dict, cache) -> list[tuple[str, str, tuple[str, str, str, str]]]:
    """最后一条 done 不是 glm 且仍在缓存里的键。"""
    return [(m, k, v) for (m, k), v in sorted(latest.items())
            if v[1] and v[1] != TARGET_MODEL and k in cache]


def main() -> int:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--dry-run", action="store_true", help="只看清单（默认）")
    g.add_argument("--apply", action="store_true")
    g.add_argument("--verify", action="store_true")
    g.add_argument("--selftest", action="store_true")
    ap.add_argument("--max-missing", type=int, default=-1,
                    help="--verify 时允许尚未重烧的条数（默认不限）")
    a = ap.parse_args()

    if a.selftest:
        fake = {
            ("v4", "a#v4"): ("2026-11-04T00:00:00Z", "deepseek-flash", "x/a", "a"),
            ("v4", "b#v4"): ("2026-11-07T00:00:00Z", "glm-5.3-flash", "x/b", "b"),
            ("v4t", "c#txt4.0"): ("2026-11-04T00:00:00Z", "deepseek-flash", "x/c", "c"),
            ("v4t", "d#txt4.0"): ("2026-11-04T00:00:00Z", "deepseek-flash", "x/d", "d"),  # 不在缓存
        }
        cache = {"a#v4": {}, "b#v4": {}, "c#txt4.0": {}}
        got = plan(fake, cache)
        chk = [
            ("只挑 deepseek 且仍在缓存", {k for _, k, _ in got} == {"a#v4", "c#txt4.0"}),
            ("glm 条目不进清单", "b#v4" not in {k for _, k, _ in got}),
            ("缓存已缺的键不重复清", "d#txt4.0" not in {k for _, k, _ in got}),
            ("v4/v4t 键规则", key_of("v4", "sha") == "sha#v4"
             and key_of("v4t", "sha") == "sha#txt4.0"),
        ]
        for name, ok in chk:
            print(f"[{'PASS' if ok else 'FAIL'}] {name}")
        bad = sum(not ok for _, ok in chk)
        print(f"\nselftest {'PASS' if not bad else 'FAIL'}（{bad} 处失败）")
        return 0 if not bad else 1

    cache = InterpCacheStore()
    latest = collect_latest(glob.glob(str(LOGS / "interp_*.jsonl")))
    todo = plan(latest, cache)
    print(f"最后一条 done 为 deepseek 的键：{len(todo)} "
          f"（v4 {sum(m == 'v4' for m, _, _ in todo)} / "
          f"v4t {sum(m == 'v4t' for m, _, _ in todo)}）")
    for m, k, v in todo[:5]:
        print(f"  {m} {k} ← {v[2]} @ {v[0]}")
    print(f"待备份 {len(todo)} 条 → {BACKUP.relative_to(ROOT)}")

    if a.apply:
        BACKUP.parent.mkdir(parents=True, exist_ok=True)
        backup = {"reason": f"G2-2 deepseek → {TARGET_MODEL}",
                  "count": len(todo),
                  "entries": {f"{m}|{k}": cache[k] for m, k, _ in todo}}
        tmp = BACKUP.with_suffix(".tmp")
        tmp.write_text(json.dumps(backup, ensure_ascii=False), encoding="utf-8")
        tmp.replace(BACKUP)
        for _, k, _ in todo:
            del cache[k]
        n = cache.flush()
        print(f"已备份并删除 {len(todo)} 条，脏桶落盘 {n} 个")
        return 0

    if a.verify:
        rs = json.loads((ROOT / "state" / "readme_state.json").read_text(encoding="utf-8"))
        ritems = rs.get("items") or {}
        deep = [(m, k, v) for (m, k), v in sorted(latest.items())
                if v[1] and v[1] != TARGET_MODEL]
        left = [k for _, k, _ in deep if k in cache]
        cur = [(m, k, v) for m, k, v in deep
               if k not in cache and (ritems.get(v[2]) or {}).get("sha") == v[3]]
        stale = [(m, k, v) for m, k, v in deep
                 if k not in cache and (ritems.get(v[2]) or {}).get("sha") != v[3]]
        print(f"仍属 deepseek 且在缓存：{len(left)}（应为 0）")
        print(f"已删除且仍是当前 sha：{len(cur)}")
        print(f"已过期（sha 已变，旧内容自然作废）：{len(stale)}")
        ok = (not left) and (a.max_missing < 0 or len(cur) <= a.max_missing)
        print(f"核对 → {'PASS' if ok else 'FAIL'}（left={len(left)} current_missing={len(cur)}）")
        return 0 if ok else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
