# -*- coding: utf-8 -*-
"""死信表（工作清单 G0-3）：新代不产出 / 不覆盖的仓，逐条留痕。

为什么要单独一张表：旧代靠"缓存里没有 = 没解析"隐式表达缺口，页面无法区分
"没跑"和"跑了但拒收"，也无法回答"这个仓为什么没有介绍"。新代把缺口显式化，
删除旧数据后仍能解释每个仓的状态。

四类原因（与工作清单固定决策对齐）：
  no_desc      无 README 且 description 为空 → 新代不生成介绍，页面显示"暂无简介"
  rejected     模型输出不合规，重试后仍拒收
  failed       调用失败/超时，超过重试上限
  out_of_pool  当前池外，不再产出（旧代记录随 G7 删除）

键 = "<fn>|<layer>"：同一个仓可以在判定卷被拒、在文本卷正常，必须分层记账；
同键重复写入以最新一次为准（append 语义只保留终态，避免表无限膨胀）。

用法：
  python interpret/dead_letter.py --init                  # 建空表（G0-3）
  python interpret/dead_letter.py --summary               # 四类计数
  python interpret/dead_letter.py --add owner/repo rejected judge "cat_primary 非法"
  python interpret/dead_letter.py --get owner/repo        # 看某仓所有层
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "lib"))

from gh import atomic_write_json   # noqa: E402

DL = ROOT / "state" / "dead_letter.json"
SCHEMA = 1
GEN_ID = "g2-20261107"
LAYERS = ("judge", "text", "domain_tags", "desc", "all")

REASONS = {
    "no_desc": "无 README 且 description 为空；新代不生成介绍，页面显示『暂无简介』",
    "rejected": "模型输出不合规（schema/红线/长度/词表），重试后仍拒收",
    "failed": "调用失败或超时，超过重试上限；下轮可再试",
    "out_of_pool": "当前池外；不再产出，旧代记录随 G7 删除",
}


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def empty() -> dict:
    return {
        "schema": SCHEMA,
        "gen_id": GEN_ID,
        "created_at": _now(),
        "updated_at": _now(),
        "reason_codes": REASONS,
        "layers": list(LAYERS),
        "items": {},
        "counts": {r: 0 for r in REASONS},
    }


def load(path: Path = DL) -> dict:
    if not path.is_file():
        return empty()
    return json.loads(path.read_text(encoding="utf-8"))


def save(d: dict, path: Path = DL) -> None:
    d["updated_at"] = _now()
    items = d.get("items") or {}
    d["counts"] = dict(Counter(v.get("reason") for v in items.values()))
    for r in REASONS:                       # 四类恒在，0 也显示
        d["counts"].setdefault(r, 0)
    atomic_write_json(path, d)


def key(fn: str, layer: str) -> str:
    return f"{fn}|{layer}"


def add(fn: str, reason: str, layer: str = "all", detail: str = "",
        sha: str | None = None, path: Path = DL) -> dict:
    """写一条死信（同 fn+layer 覆盖）。返回更新后的整表，调用方决定何时 save。"""
    if reason not in REASONS:
        raise ValueError(f"未知原因 {reason}；允许 {sorted(REASONS)}")
    if layer not in LAYERS:
        raise ValueError(f"未知层 {layer}；允许 {LAYERS}")
    d = load(path)
    d["items"][key(fn, layer)] = {
        "fn": fn,
        "layer": layer,
        "reason": reason,
        "detail": detail.strip(),
        "sha": sha,
        "at": _now(),
    }
    return d


def get(fn: str, path: Path = DL) -> list[dict]:
    d = load(path)
    return [v for k, v in (d.get("items") or {}).items() if v.get("fn") == fn]


def summary(path: Path = DL) -> dict:
    d = load(path)
    return {"total": len(d.get("items") or {}), **{r: d["counts"].get(r, 0) for r in REASONS}}


def _selftest() -> int:
    """API 断言（临时文件，不碰 state/dead_letter.json）。"""
    import tempfile
    fails = 0

    def chk(name, cond):
        nonlocal fails
        print(f"[{'PASS' if cond else 'FAIL'}] {name}")
        if not cond:
            fails += 1

    tmp = Path(tempfile.mkdtemp()) / "dl.json"
    d = load(tmp)
    chk("空表可读且四类计数为 0",
        d["items"] == {} and set(d["counts"]) == set(REASONS))
    save(add("a/b", "no_desc", "desc", path=tmp), tmp)
    chk("写一条 no_desc", summary(tmp)["no_desc"] == 1)
    save(add("a/b", "rejected", "judge", "cat_primary 非法", path=tmp), tmp)
    chk("同仓不同层各记一条", len(load(tmp)["items"]) == 2)
    save(add("a/b", "rejected", "judge", "改主因 2 版", path=tmp), tmp)
    chk("同键覆盖不膨胀", len(load(tmp)["items"]) == 2)
    chk("覆盖保留最新 detail", get("a/b", tmp)[1]["detail"] == "改主因 2 版")
    save(add("c/d", "out_of_pool", "all", path=tmp), tmp)
    chk("计数按原因聚合", summary(tmp) == {"total": 3, "no_desc": 1,
                                          "rejected": 1, "failed": 0, "out_of_pool": 1})
    for reason, layer in (("bogus", "judge"), ("rejected", "bogus")):
        try:
            add("x/y", reason, layer, path=tmp)
            chk(f"非法输入被拒（{reason}/{layer}）", False)
        except ValueError:
            chk(f"非法输入被拒（{reason}/{layer}）", True)
    chk("save 刷新 updated_at 与计数", load(tmp)["updated_at"] >= load(tmp)["created_at"])
    print(f"\nselftest {'PASS' if not fails else 'FAIL'}（{fails} 处失败）")
    return 0 if not fails else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--init", action="store_true", help="建空表（已存在则不动）")
    ap.add_argument("--selftest", action="store_true", help="API 断言（临时文件）")
    ap.add_argument("--summary", action="store_true")
    ap.add_argument("--add", nargs=3, metavar=("FN", "REASON", "LAYER"))
    ap.add_argument("--detail", default="")
    ap.add_argument("--get", metavar="FN")
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    if a.init:
        if DL.is_file():
            print(f"已存在，未覆盖：{DL.relative_to(ROOT)}")
        else:
            atomic_write_json(DL, empty())
            print(f"已建 {DL.relative_to(ROOT)}（四类原因，空表）")
        return 0
    if a.add:
        fn, reason, layer = a.add
        save(add(fn, reason, layer, a.detail))
        print(f"已记 {fn} · {layer} · {reason}")
        return 0
    if a.get:
        for v in get(a.get):
            print(json.dumps(v, ensure_ascii=False))
        return 0
    print(json.dumps(summary(), ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
