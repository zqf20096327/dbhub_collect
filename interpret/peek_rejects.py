# -*- coding: utf-8 -*-
"""peek_rejects —— 把某天所有拒收/失败项目列全（fn + 原因，不截断）。

用法：
  python interpret/peek_rejects.py                # 今天
  python interpret/peek_rejects.py 20261001       # 指定日期（可多个）
  python interpret/peek_rejects.py --raw 20261001 # 屏幕也出原文（默认脱敏）
按 fn 去重：跨 run 重跑成功的项目不算问题，只列最终未通过者。
三块输出：
  1) 拒收按原因分组，逐条列 fn（一个项目可出现在多组）
  2) 「缺 quote」专项分辨：readme 原文其实含该库名（清洗/db_scan 漏 → 误降级
     desc-only，附原文命中行）vs 原文也没有（真 desc-only，模型没给 quote）
  3) api 失败按 error 分组
【贴大模型注意】屏幕输出默认脱敏：README 命中行只给结构标签（代码块/徽章/
链接/表格/标题/正文），不带原文——语料里难免敏感词，原文贴出去会被内容
审查拦截。要看原文用 --raw 或翻写盘文件。全文（含原文）写入
state/logs/rejects_<日期>.txt 供本地 less 翻看，不要直接外贴该文件。
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOGDIR = ROOT / "state" / "logs"
RMDIR = ROOT / "data" / "readmes"


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


def cat_of(v) -> str:
    return str(v).split("（")[0].split(":")[0][:36]


def _line_tag(ln: str, in_fence: bool) -> str:
    """脱敏用：只报该行的结构类型，不外露原文。"""
    s = ln.strip()
    if not s:
        return "空行"
    if in_fence:
        return "代码块内"
    if s.startswith("|"):
        return "表格行"
    if s.startswith("#"):
        return "标题"
    low = s.lower()
    if "[![" in s or "shields.io" in low or "badge" in low or "<img" in low:
        return "徽章/图片"
    if "](http" in s or low.startswith("http"):
        return "链接行"
    if s.startswith("<"):
        return "HTML"
    return f"正文({len(s)}字符)"


def readme_hit_lines(fn: str, dbs: list[str], cap: int = 2,
                     safe: bool = True) -> list[str]:
    """readme 原文中含库名的行（带行号），用于判断为何被清理器剥掉。
    safe=True 只给结构标签（贴大模型不触内容审查）；safe=False 给原文。"""
    p = RMDIR / (fn.replace("/", "__") + ".md")   # 磁盘文件名是 owner__repo.md
    if not p.is_file():
        return ["(readme 文件缺失——多为 no_readme 降级项)"]
    hits = []
    in_fence = False
    for i, ln in enumerate(p.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
        if ln.lstrip().startswith("```"):
            in_fence = not in_fence
        low = ln.lower()
        for d in dbs:
            if d.lower() in low:
                detail = _line_tag(ln, in_fence) if safe else ln.strip()[:110]
                hits.append(f"L{i}[{d}] <{detail}>" if safe
                            else f"L{i}[{d}] {ln.strip()[:110]}")
                break
        if len(hits) >= cap:
            break
    return hits or ["(无命中行)"]


def build(days: list[str], raw: bool) -> str:
    lines: list[str] = []
    say = lines.append
    for day in days:
        recs = [r for r in load(day) if r.get("type") == "item"]
        # 按 fn 归并：done 覆盖 rejected/failed（重跑成功的不算问题项目），
        # 未通过者取最后一次记录的原因
        final: dict[str, dict] = {}
        for r in recs:
            fn = r.get("fn")
            if not fn:
                continue
            if r.get("kind") == "done" or fn not in final:
                final[fn] = r
        rej = [r for r in final.values() if r.get("kind") == "rejected"]
        fail = [r for r in final.values() if r.get("kind") == "failed"]
        say(f"════ {day} · 条目 {len(recs)} · 项目 {len(final)} · "
            f"最终拒收 {len(rej)} · 最终api失败 {len(fail)} ════")

        bywhy: dict[str, list] = defaultdict(list)
        for r in rej:
            for v in (r.get("violations") or [])[:5]:
                bywhy[cat_of(v)].append((r["fn"], v))
        for why in sorted(bywhy, key=lambda k: -len(bywhy[k])):
            say(f"\n── {why} · {len(bywhy[why])} 处 ──")
            for fn, v in bywhy[why]:
                say(f"  {fn}  |  {v}")

        hit_rows, miss_rows = [], []     # 原文有（误降级）/ 原文没有（真 desc-only）
        for r in rej:
            vs = [str(v) for v in (r.get("violations") or []) if "缺 quote" in str(v)]
            if not vs:
                continue
            dbs = sorted({v.split(" 的 ")[0] for v in vs})
            p = RMDIR / (r["fn"].replace("/", "__") + ".md")
            txt = (p.read_text(encoding="utf-8", errors="ignore").lower()
                   if p.is_file() else "")
            absent = [d for d in dbs if d.lower() not in txt]
            (miss_rows if len(absent) == len(dbs) else hit_rows).append((r["fn"], dbs, absent))
        say(f"\n── 缺 quote · readme 原文含该库名（清洗/db_scan 漏，误降级）"
            f"共 {len(hit_rows)} 条 ──")
        for fn, dbs, absent in hit_rows:
            for h in readme_hit_lines(fn, [d for d in dbs if d not in absent],
                                      safe=not raw):
                say(f"  {fn}  {h}")
        say(f"\n── 缺 quote · readme 原文也没有（真 desc-only，模型没给 quote）"
            f"共 {len(miss_rows)} 条 ──")
        for fn, dbs, _ in miss_rows:
            say(f"  {fn}  {dbs}")

        if fail:
            say(f"\n── api 失败 {len(fail)} 条 ──")
            byerr: dict[str, list] = defaultdict(list)
            for r in fail:
                byerr[str(r.get("error") or "?")[:60]].append(r["fn"])
            for e, fns in sorted(byerr.items(), key=lambda kv: -len(kv[1])):
                say(f"  [{len(fns)} 条] {e}")
                for fn in fns:
                    say(f"      {fn}")

    return "\n".join(lines)


def main(days: list[str], raw_stdout: bool = False) -> None:
    print(build(days, raw=raw_stdout))
    p = LOGDIR / f"rejects_{'+'.join(days)}.txt"
    p.write_text(build(days, raw=True), encoding="utf-8")
    mode = "原文（--raw，外贴可能触发内容审查）" if raw_stdout else "已脱敏，可直接贴大模型"
    print(f"\n屏幕输出{mode}；全文含原文已写入 {p}（本地翻看用，勿外贴）",
          file=sys.stderr)


if __name__ == "__main__":
    argv = sys.argv[1:]
    days = [a for a in argv if not a.startswith("-")] or \
        [datetime.now().strftime("%Y%m%d")]
    main(days, raw_stdout="--raw" in argv)
