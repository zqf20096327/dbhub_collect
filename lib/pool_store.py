# -*- coding: utf-8 -*-
"""pool NDJSON 活文件读写层（10-06 M2b：单一活文件替代每日快照全量复制）。

背景：data/snapshot_DATE/pool*.json 每天整表重写进 git（27+23+4.5MB/天），
pretty-JSON 字段散布变化使 git delta 失效，推拉双堵。改为每行一条、按
full_name 大小写折叠排序的 NDJSON 活文件后，每日只有变化的行字节变动，
git delta 极小（与 interp_cache 256 桶同一思想）。

规则：
- 活文件：data/live/pool.ndjson / pool_intl.ndjson / pool_cn.ndjson。
- 每行一条记录，json.dumps(sort_keys=True, ensure_ascii=False)——字段序固定，
  同一记录任何端写出字节一致。
- 排序键：(full_name.casefold(), full_name)——防大小写撞车（tedious-code
  假改动旧案）；折叠键相同而原名不同的记录对会被 detect_case_collisions 报出。
- 原子写：tmp + replace，**不轮转**（27MB 级文件滚三份副本是 332MB 旧事重演；
  gitignore 已挡 data/live/*.tmp 瞬态件——由本文件写入前保证）。
- 读兼容：load_latest() 优先活文件，回退最新 snapshot_20*/<name>.json——
  切换期读方（enrich/readme_sweep/interpret 系）无需改造即可用上活文件，
  回退语义等价旧的"ls -t 取最新、当日未写回退昨池"。
- 语义比对：semantic_diff 按折叠键对齐逐字段比，是切换验收的唯一口径
  （新旧格式不同，文件级 sha 必然不等，不能作验收）。
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIVE_DIR = ROOT / "data" / "live"
DATA_DIR = ROOT / "data"

NAMES = ("pool", "pool_intl", "pool_cn")   # 三件套共用本层


def live_path(name: str = "pool") -> Path:
    return LIVE_DIR / f"{name}.ndjson"


def _sort_key(rec: dict) -> tuple[str, str]:
    fn = rec.get("full_name") or ""
    return (fn.casefold(), fn)


def write_live(records: list, name: str = "pool") -> Path:
    """排序 + 逐行原子写活文件。返回路径。记录缺 full_name 按 "" 排（排最前，便于发现）。"""
    p = live_path(name)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(".ndjson.tmp")
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        for rec in sorted(records, key=_sort_key):
            f.write(json.dumps(rec, ensure_ascii=False, sort_keys=True))
            f.write("\n")
    tmp.replace(p)
    return p


def read_ndjson(path: Path) -> list:
    out = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def load_latest(name: str = "pool") -> tuple[list, Path]:
    """当日池：活文件优先，回退最新快照。返回 (records, source_path)。

    回退语义对齐旧 CI：snapshot_DATE/pool.json 是"两侧完成才写"的并集，
  未完成时 ls -t 自然回退昨日——活文件模式下"未写"即文件仍是昨日状态，
  等价。
    """
    lp = live_path(name)
    if lp.is_file():
        return read_ndjson(lp), lp
    cands = sorted(DATA_DIR.glob(f"snapshot_20*/{name}.json"))
    for p in reversed(cands):
        if p.stat().st_size > 2:
            return json.loads(p.read_text(encoding="utf-8")), p
    raise FileNotFoundError(f"无可用池：{lp} 不存在且无 snapshot_20*/{name}.json")


def convert_snapshot(json_path: Path, out_path: Path | None = None) -> tuple[int, Path]:
    """旧 pretty-JSON 快照 → NDJSON（切换工具）。返回 (条数, 输出路径)。"""
    records = json.loads(Path(json_path).read_text(encoding="utf-8"))
    out_path = Path(out_path) if out_path else live_path(Path(json_path).stem)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = out_path.with_suffix(".ndjson.tmp")
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        for rec in sorted(records, key=_sort_key):
            f.write(json.dumps(rec, ensure_ascii=False, sort_keys=True))
            f.write("\n")
    tmp.replace(out_path)
    return len(records), out_path


def detect_case_collisions(records: list) -> list:
    """折叠键相同而 full_name 不同的记录组（大小写撞车预警）。"""
    seen: dict[str, str] = {}
    bad = []
    for r in records:
        fn = r.get("full_name") or ""
        k = fn.casefold()
        if k in seen and seen[k] != fn:
            bad.append((seen[k], fn))
        else:
            seen.setdefault(k, fn)
    return bad


def semantic_diff(a: list, b: list, max_report: int = 10) -> dict:
    """语义等价比对（切换验收唯一口径）。a/b 为记录列表（任意顺序）。

    返回 {only_a, only_b, field_diffs, case_collisions, equal}。
    equal=True 才算验收通过；case_collisions 非空也算失败（大小写漂移）。
    """
    ka = {(r.get("full_name") or "").casefold(): r for r in a}
    kb = {(r.get("full_name") or "").casefold(): r for r in b}
    only_a = sorted(set(ka) - set(kb))
    only_b = sorted(set(kb) - set(ka))
    field_diffs = []
    for k in sorted(set(ka) & set(kb)):
        ra, rb = ka[k], kb[k]
        fa, fb = set(ra), set(rb)
        if fa != fb:
            field_diffs.append((k, sorted(fa - fb), sorted(fb - fa)))
        else:
            for f in sorted(fa):
                if ra[f] != rb[f]:
                    field_diffs.append((k, f, (ra[f], rb[f])))
        if len(field_diffs) >= max_report:
            break
    return {
        "only_a": only_a[:max_report],
        "only_a_n": len(only_a),
        "only_b": only_b[:max_report],
        "only_b_n": len(only_b),
        "field_diffs": field_diffs,
        "case_collisions": detect_case_collisions(b),
        "equal": not (only_a or only_b or field_diffs or detect_case_collisions(b)),
    }
