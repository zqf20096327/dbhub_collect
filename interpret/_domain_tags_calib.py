# -*- coding: utf-8 -*-
"""domain_tags 校准工具（B 包，一次性）：eco 路由验证 + 词-仓共现矩阵 + 混淆对清单。

输入：state/shadow/domain_tags_shadow_500.json（500 条影子结果）+ sha#v4 缓存条目
输出：
  state/shadow/cooccur_words.csv      词×词 共现（同仓被同时标注的次数）
  state/shadow/cooccur_domains.csv    域×域 共现
  state/shadow/cat_domain.csv         cat_primary × 域 矩阵（§5 xcheck 实证）
  state/shadow/confusion_pairs.md     混淆对清单（设计近邻 / 实测共现 / 双跑摇摆）
不写生产缓存与状态。
"""
import io
import json
import re
import sys
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for _d in (ROOT, ROOT / "lib", ROOT / "config", ROOT / "interpret"):
    sys.path.insert(0, str(_d))

import _shadow_vocab as sv                                  # noqa: E402

OUT = ROOT / "state" / "shadow"
DOC = Path.home() / "OneDrive" / "桌面" / "受控词表v0.10（A类修复版）.md"


def load_v4():
    idx = {}
    for p in sorted((ROOT / "state/interp_cache_shards").glob("*.json")):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
        for k, v in d.items():
            if k.endswith("#v4") and isinstance(v, dict) \
                    and (v.get("classification") or {}).get("cat_primary"):
                idx[v.get("fn")] = v
    return idx


def load_design_pairs() -> set[tuple[str, str]]:
    """从词表文档第 4 列抽设计好的 ↔ 近邻对（"该分开"的对）。"""
    text = io.open(DOC, encoding="utf-8").read()
    pairs = set()
    cur_slug = None
    for ln in text.splitlines():
        if not ln.startswith("|"):
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) < 4:
            continue
        if re.match(r"^[a-z][a-z0-9\-]+$", cells[0]) and cells[1] not in ("中文",):
            cur_slug = cells[0]
            for tgt in re.findall(r"↔\s*([a-z][a-z0-9\-]+)", cells[3]):
                if tgt != cur_slug:
                    pairs.add(tuple(sorted((cur_slug, tgt))))
    return pairs


def main():
    rep = json.loads((OUT / "domain_tags_shadow_500.json").read_text(encoding="utf-8"))
    v4 = load_v4()
    vocab = sv.parse_vocab()
    w2d = {w["slug"]: d["domain"] for d in vocab["domains"] for w in d["words"]}

    ok = [r for r in rep["items"] if r["run"] == 1 and r.get("tags") is not None]
    rows = []
    for r in ok:
        cls = (v4.get(r["fn"]) or {}).get("classification") or {}
        rows.append({"fn": r["fn"], "stratum": r["stratum"], "tags": r["tags"],
                     "eco": cls.get("eco"), "cat": cls.get("cat_primary"),
                     "prompt_bytes": r.get("prompt_bytes") or 0})

    # ---------- 1. eco 路由：空率 + 保住多少信号 + token 账 ----------
    route = defaultdict(lambda: {"n": 0, "empty": 0, "kept": 0, "bytes": 0})
    for r in rows:
        g = route[r["eco"] or "None"]
        g["n"] += 1
        g["empty"] += 0 if r["tags"] else 1
        g["kept"] += 1 if r["tags"] else 0
        g["bytes"] += r["prompt_bytes"]
    avg_b = sum(r["prompt_bytes"] for r in rows) / max(1, len(rows))
    LITE = 5547                                 # 应用类短提示实测字节（词表块 4.9K + 元信息，不投 README）
    print("=== eco 路由实证 ===")
    print(f"{'eco':8} {'n':>4} {'空率':>6} {'非空':>5} {'均prompt':>9}")
    for k, g in sorted(route.items(), key=lambda x: -x[1]["n"]):
        print(f"{k:8} {g['n']:>4} {g['empty']/g['n']:>6.0%} {g['kept']:>5} {g['bytes']/g['n']:>9.0f}B")
    n_app, n_unc = route["app"]["n"], route["unclear"]["n"]
    save_app = n_app * (avg_b - LITE) / 1024
    save_unc = n_unc * avg_b / 1024
    print(f"\n路由建议：unclear 硬跳过（{route['unclear']['empty']}/{n_unc} 空，"
          f"损失 {route['unclear']['kept']} 条）· app 走短提示（保住 {route['app']['kept']} 条非空）")
    print(f"抽样 500 条口径省 ~{save_app + save_unc:.0f} KB 输入"
          f"（占抽样总输入的 {(save_app+save_unc)/(sum(r['prompt_bytes'] for r in rows)/1024):.0%}）；"
          f"全量 3.4 万条外推 ~{(save_app+save_unc)*68/1024:.0f} MB")

    # ---------- 2. 词×词 / 域×域 共现 ----------
    wc, dc, cd = Counter(), Counter(), Counter()
    for r in rows:
        for t in r["tags"]:
            wc[t] += 1
            dc[w2d[t]] += 1
            if r["cat"]:
                cd[(r["cat"], w2d[t])] += 1
    wpair, dpair = Counter(), Counter()
    for r in rows:
        for a, b in combinations(sorted(set(r["tags"])), 2):
            wpair[(a, b)] += 1
            da, db = sorted((w2d[a], w2d[b]))
            dpair[(da, db)] += 1

    with (OUT / "cooccur_words.csv").open("w", encoding="utf-8-sig", newline="") as f:
        f.write("词A,词B,共现次数\n")
        for (a, b), n in wpair.most_common():
            f.write(f"{a},{b},{n}\n")
    with (OUT / "cooccur_domains.csv").open("w", encoding="utf-8-sig", newline="") as f:
        f.write("域A,域B,共现次数\n")
        for (a, b), n in dpair.most_common():
            f.write(f"{a},{b},{n}\n")
    cats = sorted({r["cat"] for r in rows if r["cat"]})
    doms = [d["domain"] for d in vocab["domains"]]
    with (OUT / "cat_domain.csv").open("w", encoding="utf-8-sig", newline="") as f:
        f.write("cat," + ",".join(doms) + ",合计\n")
        for c in cats:
            vals = [cd[(c, d)] for d in doms]
            f.write(f"{c}," + ",".join(map(str, vals)) + f",{sum(vals)}\n")
    print(f"\n共现矩阵：词对 {len(wpair)} 组 · 域对 {len(dpair)} 组 · cat×域 {len(cats)}×{len(doms)}")

    # ---------- 2b. 词-仓 关联矩阵（71 词 × 仓，0/1）----------
    slugs = [w["slug"] for d in vocab["domains"] for w in d["words"]]
    with (OUT / "word_repo_incidence.csv").open("w", encoding="utf-8-sig", newline="") as f:
        f.write("fn,stratum,stars," + ",".join(slugs) + "\n")
        for r in sorted(rows, key=lambda x: -(x.get("stars") or 0)):
            vec = ["1" if s in r["tags"] else "0" for s in slugs]
            f.write(f'{r["fn"]},{r["stratum"]},{r.get("stars") or 0},' + ",".join(vec) + "\n")
    # 每词代表仓（按 star 降序取前 5，人工核对词定义用）
    by_word = defaultdict(list)
    for r in rows:
        for t in r["tags"]:
            by_word[t].append(r)
    md = ["# 词 → 代表仓（按 star 降序，最多 5 个）", "",
          "用途：人工核对词定义。若某词的代表仓看着不对，说明判据要改写或该词该合并。", ""]
    for s in slugs:
        lst = sorted(by_word.get(s, []), key=lambda x: -(x.get("stars") or 0))[:5]
        md.append(f"## {s}（{w2d[s]}，命中 {len(by_word.get(s, []))}）")
        md.append("")
        if not lst:
            md.append("（500 抽样内零命中）")
        for r in lst:
            md.append(f"- {r['fn']} · {r.get('stars') or 0}★ · cat={r['cat']}")
        md.append("")
    (OUT / "word_top_repos.md").write_text("\n".join(md), encoding="utf-8")
    print(f"词-仓矩阵：word_repo_incidence.csv（{len(rows)} 仓 × {len(slugs)} 词）· word_top_repos.md")

    # ---------- 3. 混淆对清单 ----------
    design = load_design_pairs()
    # 双跑摇摆对：一次标了、一次没标 / 两次标了不同词
    r1 = {r["fn"]: set(r["tags"]) for r in ok}
    r2 = {r["fn"]: set(r["tags"]) for r in rep["items"]
          if r["run"] == 2 and r.get("tags") is not None}
    swing = Counter()
    for fn in r2:
        a, b = r1.get(fn) or set(), r2[fn]
        if a == b:
            continue
        only_a, only_b = a - b, b - a
        for x in only_a:
            for y in (only_b or {None}):
                if y:
                    swing[tuple(sorted((x, y)))] += 1
                else:
                    swing[(x, "—")] += 1
        for y in only_b:
            if not only_a:
                swing[("—", y)] += 1

    lines = ["# domain_tags 混淆对清单（1107 B 包）", "",
             "证据来源：①词表设计里的 ↔ 近邻对；②500 条实测同仓共现；③50 条双跑摇摆。", ""]
    lines.append("## A. 双跑摇摆对（同一仓两次结果不同，最直接的不稳定证据）")
    lines.append("")
    lines.append("| 词A | 词B | 次数 | 建议 |")
    lines.append("|---|---|---|---|")
    for (a, b), n in swing.most_common(30):
        tip = "合并或强化判据" if n >= 2 else "样本少，观察"
        lines.append(f"| {a} | {b} | {n} | {tip} |")
    lines.append("")
    lines.append("## B. 设计近邻对 × 实测共现（设计说该分开，实际是否一起出现）")
    lines.append("")
    lines.append("| 词A | 词B | 实测共现 | 判读 |")
    lines.append("|---|---|---|---|")
    for a, b in sorted(design):
        n = wpair.get(tuple(sorted((a, b))), 0)
        note = "共现高 → 判据需更硬" if n >= 2 else ("无共现 → 分离良好" if n == 0 else "偶发")
        lines.append(f"| {a} | {b} | {n} | {note} |")
    lines.append("")
    lines.append("## C. 高频共现词对（可能该合并，或只是常配套出现）")
    lines.append("")
    lines.append("| 词A | 词B | 共现 | 域 |")
    lines.append("|---|---|---|---|")
    for (a, b), n in wpair.most_common(20):
        lines.append(f"| {a} | {b} | {n} | {w2d[a]} × {w2d[b]} |")
    (OUT / "confusion_pairs.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"混淆对清单：{OUT / 'confusion_pairs.md'}")
    print("摇摆对 Top:", swing.most_common(8))
    print("设计近邻对共现高者:",
          [(f'{a}↔{b}', wpair.get(tuple(sorted((a, b))), 0)) for a, b in sorted(design)
           if wpair.get(tuple(sorted((a, b))), 0) >= 2][:10])


if __name__ == "__main__":
    main()
