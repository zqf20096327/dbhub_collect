# -*- coding: utf-8 -*-
"""策略生成器 + 一致性校验器：档案 → 分 section 通道清单，六道校验。

分 section 是采集策略的单一事实源（db_profiles.GLOBAL["sections"] + orgs 的 class）：
  intl：topic/keyword 带 stars:>=star_min；新项目窗口 stars:>=new_star_min
  cn  ：国产不设星（star_min=0）——查询不加星限定，超 1000 结果纯按创建期拆分
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
ORG_CLASSES = {"dedicated", "cloud", "standard"}


def norm(v):
    return v["name"] if isinstance(v, dict) else v


def org_class(o, section: str) -> str:
    """org 过滤线：dedicated=0（org 即产品）/ cloud 与 standard=star_min（范围噪音闸）。"""
    if isinstance(o, dict) and o.get("class"):
        return o["class"]
    return "cloud" if section == "cn" else "standard"


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


def derive_sections() -> dict:
    """按 section 生成通道包：查询词带各自星线（cn 不带）。"""
    secs = {}
    gbl = dp.GLOBAL.get("exclude_repos") or []
    for sec_name in ("intl", "cn"):
        pol = dp.GLOBAL["sections"][sec_name]
        star = pol.get("star_min") or 0
        topics, orgs, queries, watch = [], [], {}, []
        for p in dp.PROFILES:
            if not p.get("enabled", True) or p.get("section") != sec_name:
                continue
            topics += [norm(t) for t in p["topics"]]
            orgs += list(p["orgs"])
            for w in search_words(p):
                q = f"{w} fork:false"
                if star:
                    q += f" stars:>={star}"
                for ex in gbl + (p.get("exclude_repos") or []):
                    q += f" -repo:{ex}"
                queries[w] = q
            watch += p.get("watch") or []
        if sec_name == "intl":
            topics += dp.GLOBAL["discovery_topics"]
            watch += dp.GLOBAL["watch_insurance"]
        secs[sec_name] = {
            "star_min": star,
            "new_star_min": pol.get("new_star_min", 0),
            "new_days": pol.get("new_days", 45),
            "topics": sorted(set(topics)),
            "orgs": orgs,
            "queries": queries,
            "watch": sorted(set(watch)),
            "blacklist": gbl,
        }
    return secs


def derive() -> dict:
    secs = derive_sections()
    canon, intl, cn, brand, collide, empty = {}, [], [], {}, [], []
    for p in dp.PROFILES:
        if not p.get("enabled", True):
            continue
        canon[p["name"]] = list(p["aliases"])
        (intl if p["section"] == "intl" else cn).append(p["name"])
        brand.update(p.get("brand_infer") or {})
        collide += [f"{p['name']}: {k} → {v}" for k, v in (p.get("collisions") or {}).items()]
        if p.get("known_empty"):
            empty.append(p["name"])
    return {
        # 分 section 通道包（新脚本消费）
        "SECTIONS": secs,
        # 扁平兼容视图（跨 section 并集）
        "TOPICS": sorted({t for s in secs.values() for t in s["topics"]}),
        "ORG_SCAN_LIST": [norm(o) for s in secs.values() for o in s["orgs"]],
        "KEYWORD_SEARCH_QUERIES": {w: q for s in secs.values()
                                   for w, q in s["queries"].items()},
        "WHITELIST_REPOS": sorted({w for s in secs.values() for w in s["watch"]}),
        "BLACKLIST_REPOS": sorted({ex for s in secs.values() for ex in s["blacklist"]}
                                  | {ex for p in dp.PROFILES if p.get("enabled", True)
                                     for ex in (p.get("exclude_repos") or [])}),
        "CANON_PATTERNS": canon, "SCOPE_INTL": intl, "SCOPE_CN": cn,
        "BRAND_INFER": brand, "COLLISION_RULES": collide, "KNOWN_EMPTY_DBS": empty,
        "OUT_OF_SCOPE_DBS": dp.GLOBAL["out_of_scope_dbs"],
        "DISCOVERY_TOPIC": dp.GLOBAL["discovery_topics"][0],
        "BIG_FOUR_MUTUAL_EXCLUDE": dp.GLOBAL["big_four"],
    }


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
    # ⑥ org 声明规范：国产 org 必须 dict+class；class 值合法
    for p in dp.PROFILES:
        if not p.get("enabled", True):
            continue
        for o in p["orgs"]:
            if isinstance(o, dict) and o.get("class") not in ORG_CLASSES:
                problems.append(f"⑥org class 非法：{p['name']}/{o}")
            if p["section"] == "cn" and not isinstance(o, dict):
                problems.append(f"⑥国产 org 必须 dict+class：{p['name']}/{o}")
    if clash := set(gen["WHITELIST_REPOS"]) & set(gen["BLACKLIST_REPOS"]):
        problems.append(f"⑦黑白冲突：{clash} 同时在 watch 白名单与黑名单")
    return problems


def main() -> None:
    gen = derive()
    print("==== 一致性校验 ====")
    problems = validate(gen)
    for p in problems:
        print("  ", p)
    if not [p for p in problems if not p.startswith("⑤")]:
        print("   ①-⑥ 通过")
    for sec_name, s in gen["SECTIONS"].items():
        orgs = " ".join(f"{norm(o)}"
                        + (f"({o['class']})" if isinstance(o, dict) and o.get("class") else "")
                        for o in s["orgs"])
        print(f"\n==== [{sec_name}] {len(s['topics'])} topics · "
              f"{len(set(norm(o) for o in s['orgs']))} orgs · "
              f"{len(s['queries'])} 检索词 · star_min={s['star_min']} ====")
        print("topics:", " ".join(s["topics"]))
        print("orgs  :", orgs)
        for w, q in s["queries"].items():
            print(f"search: {q}")
    if "--json" in sys.argv:
        out = HERE / "state" / "generated_strategy.json"
        out.parent.mkdir(exist_ok=True)
        out.write_text(json.dumps(gen, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"\n已写 {out}")


if __name__ == "__main__":
    main()
