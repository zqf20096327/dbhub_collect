# -*- coding: utf-8 -*-
"""策略生成器 + 一致性校验器：档案 → 四通道清单，五道校验。

用法：
  python strategy.py              # 校验 + 打印通道报告
  python strategy.py --json       # 另存 state/generated_strategy.json
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import sys as _sys, pathlib as _pl
ROOT = _pl.Path(__file__).resolve().parents[1]
for _d in (ROOT, ROOT / "lib", ROOT / "config"):
    _sys.path.insert(0, str(_d))
HERE = ROOT                      # 历史引用兼容：统一指向项目根
import db_profiles as dp  # noqa: E402

PLAIN = re.compile(r"^[A-Za-z0-9\u4e00-\u9fff ]+$")


def norm(v):
    return v["name"] if isinstance(v, dict) else v


def search_words(p) -> list[str]:
    """检索选词：auto → 纯词别名（可作检索词的）；列表则展开（元素可为 auto）。"""
    s = p.get("search")
    if s is None:
        return []
    plain_aliases = [a for a in p["aliases"] if PLAIN.match(a)]
    if s == "auto":
        return plain_aliases
    words = s if isinstance(s, list) else [s]
    out: list[str] = []
    for w in words:
        out += plain_aliases if w == "auto" else [w]
    return out


def derive() -> dict:
    active = [p for p in dp.PROFILES if p.get("enabled", True)]
    topics, orgs, queries, watch = [], [], {}, []
    canon, intl, cn, brand, collide, empty = {}, [], [], {}, [], []
    for p in active:
        topics += [norm(t) for t in p["topics"]]
        orgs += [norm(o) for o in p["orgs"]]
        for w in search_words(p):
            q = f"{w} {dp.GLOBAL['search_qualifiers'].format(star=dp.GLOBAL['star_min'])}"
            for ex in p.get("exclude_repos") or []:
                q += f" -repo:{ex}"
            queries[w] = q
        watch += p.get("watch") or []
        canon[p["name"]] = list(p["aliases"])
        (intl if p["section"] == "intl" else cn).append(p["name"])
        brand.update(p.get("brand_infer") or {})
        collide += [f"{p['name']}: {k} → {v}" for k, v in (p.get("collisions") or {}).items()]
        if p.get("known_empty"):
            empty.append(p["name"])
    topics += dp.GLOBAL["discovery_topics"]
    watch += dp.GLOBAL["watch_insurance"]
    return {"TOPICS": sorted(set(topics)), "ORG_SCAN_LIST": orgs,
            "KEYWORD_SEARCH_QUERIES": queries, "WHITELIST_REPOS": sorted(set(watch)),
            "CANON_PATTERNS": canon, "SCOPE_INTL": intl, "SCOPE_CN": cn,
            "BRAND_INFER": brand, "COLLISION_RULES": collide, "KNOWN_EMPTY_DBS": empty,
            "OUT_OF_SCOPE_DBS": dp.GLOBAL["out_of_scope_dbs"],
            "DISCOVERY_TOPIC": dp.GLOBAL["discovery_topics"][0],
            "BIG_FOUR_MUTUAL_EXCLUDE": dp.GLOBAL["big_four"]}


def validate(gen) -> list[str]:
    problems = []
    canon_words = {w.lower() for pats in gen["CANON_PATTERNS"].values() for w in pats}
    oos = {w.lower() for w in gen["OUT_OF_SCOPE_DBS"]}
    if clash := canon_words & oos:
        problems.append(f"①口径打架：{clash} 同为库别名与范围外词")
    for p in dp.PROFILES:
        if not p.get("enabled", True):
            continue
        if len(p["topics"]) + len(p["orgs"]) == 0 and p.get("search") is None \
                and not p.get("known_empty"):
            problems.append(f"②零通道：{p['name']}")
    owner: dict[str, str] = {}
    for name, pats in gen["CANON_PATTERNS"].items():
        for w in pats:
            if w in owner and owner[w] != name:
                problems.append(f"③撞词：'{w}' 同属 {owner[w]}/{name}")
            owner[w] = name
    orphan = set(gen["ORG_SCAN_LIST"]) - {norm(o) for p in dp.PROFILES for o in p["orgs"]}
    if orphan:
        problems.append(f"④悬空 org：{orphan}")
    for repo, why in dp.LEGACY_WATCH.items():
        problems.append(f"⑤遗留白名单（建议移除）：{repo} —— {why}")
    return problems


def main() -> None:
    gen = derive()
    print("==== 一致性校验 ====")
    for p in validate(gen):
        print("  ", p)
    else:
        print("   ①-④ 通过" if not [p for p in validate(gen) if not p.startswith("⑤")] else "")
    print(f"\n==== 通道清单（{len(gen['TOPICS'])} topics · "
          f"{len(set(gen['ORG_SCAN_LIST']))} orgs · {len(gen['KEYWORD_SEARCH_QUERIES'])} 检索词）====")
    print("topics:", " ".join(gen["TOPICS"]))
    print("orgs  :", " ".join(dict.fromkeys(gen["ORG_SCAN_LIST"])))
    for w, q in gen["KEYWORD_SEARCH_QUERIES"].items():
        print(f"search: {q}")
    if "--json" in sys.argv:
        out = HERE / "state" / "generated_strategy.json"
        out.parent.mkdir(exist_ok=True)
        out.write_text(json.dumps(gen, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"\n已写 {out}")


if __name__ == "__main__":
    main()
