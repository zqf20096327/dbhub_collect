# -*- coding: utf-8 -*-
"""unattr draft 预筛：把判定器的归属草案按证据强度分组成可签发清单。

定位：unattr_judge 产 draft（人工签发进 config/overrides.json），本工具只做
"备料"——分组、去重（已签发的跳过）、红旗标记（语言与依赖清单错配）、
按 overrides 条目格式生成直签批。签发权永远在人：批文件合并进 overrides
前须人工过目 state/unattr_prescreen_*.md。

分组：
  T1 直签批  strength==strong（路径/文件类硬证据）
  T2 复核批  med 且 ≥2 条独立证据
  T3 低把握  单证据 med
红旗：证据清单类型与仓库主语言错配（package.json 证据却非 JS/TS 仓等）——
      可能是开发工具链依赖而非产品支持，签发前必看。

用法：python tools/unattr_prescreen.py           # 全部只读，仅写 state/ 两文件
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERDICTS = ROOT / "state" / "unattr_verdicts.json"
OVERRIDES = ROOT / "config" / "overrides.json"

# 清单类型 → 合理主语言（错配=红旗，非否决：多语言仓真实存在）
_MANIFEST_LANG = {
    "package.json": {"JavaScript", "TypeScript"},
    "pom.xml": {"Java", "Kotlin", "Scala", "Clojure"},
    "requirements.txt": {"Python"}, "pyproject.toml": {"Python"},
    "setup.py": {"Python"},
    "go.mod": {"Go"}, "Cargo.toml": {"Rust"},
    "Gemfile": {"Ruby"}, "composer.json": {"PHP"},
}


def _manifest_of(ev: str) -> str:
    for m in _MANIFEST_LANG:
        if f"∈ {m}" in ev or ev.endswith(m):
            return m
    return ""


def _red_flags(entry: dict) -> list[str]:
    flags = []
    lang = entry.get("lang") or ""
    for ev in entry.get("evidence") or []:
        m = _manifest_of(ev)
        if m and lang and lang not in _MANIFEST_LANG[m]:
            flags.append(f"{lang} 仓出现 {m} 证据（疑开发工具链）")
    return sorted(set(flags))


def _override_row(fn: str, e: dict) -> dict:
    """按 config/overrides.json 条目格式备料（date 预填今日，签发时可改）。"""
    branch = e.get("branch") or "main"
    evs = e.get("evidence") or []
    deps = [x for x in evs if x.startswith("依赖")]
    paths = [x for x in evs if x.startswith("路径") or x.startswith("文件")]
    if paths:
        where = paths[0].split(" ", 1)[1]
        link = f"github.com/{fn}/tree/{branch}/{where.split('/')[0]}"
        why = f"{'、'.join(paths[:2])} 等 {len(paths)} 处路径证据"
    else:
        where = deps[0].split(" ∈ ")[1] if " ∈ " in deps[0] else deps[0]
        link = f"github.com/{fn}/blob/{branch}/{where}"
        why = f"依赖指纹：{'；'.join(d.replace('依赖 ', '') for d in deps[:3])}"
    return {"dbs": e["dbs"], "why": why, "evidence": link,
            "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"), "by": "user"}


def main() -> int:
    uv = json.loads(VERDICTS.read_text(encoding="utf-8"))
    signed = {k for k in json.loads(OVERRIDES.read_text(encoding="utf-8"))
              if not k.startswith("_")}
    drafts = {fn: e for fn, e in uv.items()
              if e.get("status") == "draft" and fn not in signed}
    t1 = {fn: e for fn, e in drafts.items() if e.get("strength") == "strong"}
    rest = {fn: e for fn, e in drafts.items() if e.get("strength") != "strong"}
    t2 = {fn: e for fn, e in rest.items() if len(e.get("evidence") or []) >= 2}
    t3 = {fn: e for fn, e in rest.items() if len(e.get("evidence") or []) < 2}
    flagged = {fn: _red_flags(e) for fn, e in drafts.items()}
    flagged = {fn: f for fn, f in flagged.items() if f}

    by_stars = lambda d: sorted(d.items(), key=lambda kv: -(kv[1].get("stars") or 0))
    today = datetime.now(timezone.utc).strftime("%Y%m%d")
    md = [f"# unattr draft 预筛（{today}）",
          f"draft {len(drafts)} 条（已签发 {len(signed & set(uv))} 条去重后）｜"
          f"T1 直签 {len(t1)} · T2 复核 {len(t2)} · T3 低把握 {len(t3)} · 红旗 {len(flagged)}",
          f"证据类型：{dict(Counter(x.split()[0] for e in drafts.values() for x in e['evidence']))}",
          "\n> 签发流程：过目下表 → 把 state/unattr_signoff_batch.json 的 T1 条目（或自行加选 T2）"
          "合并进 config/overrides.json → build_demo 并集生效。红旗条目签发前必看。\n"]

    def emit(title: str, group, note: str):
        md.append(f"\n## {title}（{len(group)}）{note}")
        for fn, e in by_stars(group):
            stars = e.get("stars") or 0
            fl = f" ｜🚩{'；'.join(flagged[fn])}" if fn in flagged else ""
            md.append(f"- {stars}★ {fn} → {','.join(e['dbs'])}{fl}")
            for ev in (e.get("evidence") or [])[:3]:
                md.append(f"  - {ev}")

    emit("T1 直签批（strong，建议签发）", t1, "— 批文件已按 overrides 格式备好")
    emit("T2 复核批（med，≥2 独立证据）", t2, "— 交叉证据，扫一眼可签")
    emit("T3 低把握（单证据 med）", t3, "— 建议留给判定器下周补充侦查")
    (ROOT / "state" / f"unattr_prescreen_{today}.md").write_text(
        "\n".join(md), encoding="utf-8")
    batch = {fn: _override_row(fn, e) for fn, e in by_stars(t1)}
    (ROOT / "state" / "unattr_signoff_batch.json").write_text(
        json.dumps(batch, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"draft {len(drafts)}（去重已签 {len(uv) and len([k for k in uv if k in signed])}）"
          f" → T1 {len(t1)} / T2 {len(t2)} / T3 {len(t3)} / 红旗 {len(flagged)}")
    print(f"产出：state/unattr_prescreen_{today}.md + state/unattr_signoff_batch.json（T1 直签批）")
    for fn, f in list(flagged.items())[:5]:
        print(f"  🚩 {fn}: {f[0]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
