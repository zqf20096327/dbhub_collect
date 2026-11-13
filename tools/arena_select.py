# -*- coding: utf-8 -*-
"""同类擂台圈选器 arena_select v2.3（2026-11-09）

相对 v2.2 的三处修正（消融实验结论）：
  1. judge 类目加分降级为安全网——仅"无标签候选"用类目兜底（记 0.40 分并标
     cat_fallback，不与标签分混算），消除门槛渗漏与双重计分；
  2. 标签相似度改为 IDF 加权覆盖度——score = Σ共享 idf×min(conf) / Σ主角 idf×conf，
     稀有标签更值钱；候选自己的额外专长不惩罚（擂台问"谁干主角一样的活"，
     Jaccard 会把"同核心+不同专长"错杀，首跑实测 pghoard 被挤出即是此病）；
  3. 置信修正——候选私有标签不计入分母（覆盖度天然满足）；
  4. 生态专注度——score × (0.7 + 0.3×specificity)，specificity =
     |候选库集∩主角库集| / |候选库集|：PG 专属工具保持满分，多库通用工具最多
     降 30%（区分"PG 专属引擎"与"顺带支持 PG 的通用工具"，库集来自 db_scan）。

门槛：同生态（db_scan 库交集，或 db 名 topics 交集）∩ 在池 ∩ 未出池 ∩ 非归档非 fork
星数门槛：默认过线候选星数 P75（钳位 [100,1000]），--star-floor 显式覆盖
界面层剔除：候选带 UI 标签（web-console/gui-client/dashboard）而主角无 → excluded_ui
人工否决：--veto owner/repo,...（进 adjudications 留痕）

用法：
  python tools/arena_select.py --fn pgbackrest/pgbackrest
  python tools/arena_select.py --fn dbeaver/dbeaver --top 10 --out D:/tmp/arena.json
  python tools/arena_select.py --selftest
"""
from __future__ import annotations

import argparse
import glob
import json
import math
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VER = "arena_v2.4"
CONF_W = {"high": 1.0, "mid": 0.6, "low": 0.3}
UI_TAGS = {"web-console", "gui-client", "dashboard"}
CAT_FALLBACK_SCORE = 0.40


# ---------- 纯函数（selftest 覆盖） ----------

def idf_map(tags_by_repo: dict) -> dict:
    """全池文档频率 → idf。tags_by_repo: repo -> {tag: conf_weight}"""
    df: dict[str, int] = {}
    for tw in tags_by_repo.values():
        for t in tw:
            df[t] = df.get(t, 0) + 1
    n = max(len(tags_by_repo), 1)
    return {t: math.log(n / (1 + c)) for t, c in df.items()}


def sim(ta: dict, tb: dict, idf: dict) -> float:
    """IDF 加权覆盖度：候选覆盖主角身份的比例。
    分子 = Σ共享标签 idf×max(conf)——两边都提取到即算覆盖，置信取乐观侧
    （候选侧 mid/low 是提取噪声，实测 barman restore@mid 被 min() 错杀到 0.489）；
    分母 = Σ主角标签 idf×conf；候选私有标签不计入（不惩罚额外专长）。"""
    den = sum(idf.get(t, 1.0) * ta[t] for t in ta)
    if not den:
        return 0.0
    num = sum(idf.get(t, 1.0) * max(ta[t], tb[t]) for t in set(ta) & set(tb))
    return num / den


def p75(vals: list) -> int:
    if not vals:
        return 100
    s = sorted(vals)
    return s[int(0.75 * (len(s) - 1))]


def specificity(c_dbs: set, t_dbs: set) -> float:
    """生态专注度：候选引用的库集有多大比例落在主角库集内。
    候选或主角无库集时中性 1.0（无证据不惩罚）。"""
    if not c_dbs or not t_dbs:
        return 1.0
    return len(c_dbs & t_dbs) / len(c_dbs)


# ---------- 数据装载 ----------

def load_pool(path: Path) -> dict:
    pool = {}
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip().rstrip(",")
            if not line or line in "[]":
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            pool[r["full_name"]] = r
    return pool


def load_layers():
    tags: dict[str, dict] = {}
    for f in glob.glob(str(ROOT / "state/interp/domain_tags/shards/*.json")):
        for k, v in json.load(open(f, encoding="utf-8")).items():
            if isinstance(v, dict) and "tags" in v:
                tags[k.split("#")[0]] = {
                    t["slug"]: CONF_W.get(t.get("conf"), 0.3) for t in v["tags"]
                }
    judge: dict[str, str] = {}
    for f in glob.glob(str(ROOT / "state/interp/judge/shards/*.json")):
        for k, v in json.load(open(f, encoding="utf-8")).items():
            c = (v or {}).get("classification") or {}
            judge[k.split("#")[0]] = c.get("cat_primary")
    state = json.load(open(ROOT / "state/interp_state.json", encoding="utf-8"))
    return tags, judge, state.get("items", {})


def select(target_fn: str, top_n=5, min_score=0.45, star_floor=None,
           veto: list[str] | None = None) -> dict:
    veto = veto or []
    pool = load_pool(ROOT / "data/live/pool.ndjson")
    tags, judge, items = load_layers()
    dscan = json.load(open(ROOT / "state/db_scan.v2.json", encoding="utf-8"))
    absent = json.load(open(ROOT / "state/absent_since.json", encoding="utf-8"))

    if target_fn not in pool:
        raise SystemExit(f"主角不在池内: {target_fn}")
    tsha = items.get(target_fn, {}).get("sha", "")
    ta = tags.get(tsha, {})
    tcat = judge.get(tsha)
    trow = pool[target_fn]
    t_dbs = {k.lower() for k in (dscan.get(target_fn) or {}).get("cands", {})}
    t_topics = {x.lower() for x in (trow.get("topics") or [])}
    db_topics = {k.lower() for e in dscan.values() for k in (e or {}).get("cands", {})}
    idf = idf_map(tags)

    cand_rows, excluded_ui, below_floor_pool = [], [], []
    for fn, r in pool.items():
        if fn == target_fn or fn in absent or r.get("archived") or r.get("fork"):
            continue
        sha = items.get(fn, {}).get("sha", "")
        tb = tags.get(sha)
        c_dbs = {k.lower() for k in (dscan.get(fn) or {}).get("cands", {})}
        c_topics = {x.lower() for x in (r.get("topics") or [])}
        if not ((c_dbs & t_dbs) or (c_topics & t_topics & db_topics)):
            continue
        stars = r.get("stars", 0)
        if tb is None:  # 安全网：无标签 + 类目相同 → 兜底分
            if tcat and judge.get(sha) == tcat:
                cand_rows.append({"fn": fn, "stars": stars, "score": CAT_FALLBACK_SCORE,
                                  "source": "cat_fallback", "tags": []})
            continue
        if UI_TAGS & set(tb) and not (UI_TAGS & set(ta)):
            excluded_ui.append({"fn": fn, "stars": stars, "tags": sorted(tb)})
            continue
        s = sim(ta, tb, idf) * (0.7 + 0.3 * specificity(c_dbs, t_dbs))
        if s >= min_score:
            cand_rows.append({"fn": fn, "stars": stars, "score": round(s, 3),
                              "source": "tags", "tags": sorted(tb),
                              "dbs": sorted(c_dbs)})

    passing = [c for c in cand_rows if c["source"] == "tags"]
    # 星门槛：绝对下限 300，cohort P50 更高则取 P50（跨领域可移植），封顶 2000
    p50 = sorted([c["stars"] for c in passing])[len(passing) // 2] if passing else 300
    floor = star_floor if star_floor is not None else min(2000, max(300, p50))
    kept = [c for c in cand_rows if c["stars"] >= floor]
    below_floor_pool = [c for c in cand_rows if c["stars"] < floor]
    kept.sort(key=lambda c: (-c["score"], -c["stars"]))
    top = [c for c in kept if c["fn"] not in veto][:top_n]
    vetoed = [c for c in kept if c["fn"] in veto]

    return {
        "ver": VER, "fn": target_fn, "generated_at": date.today().isoformat(),
        "params": {"top_n": top_n, "min_score": min_score, "star_floor": floor,
                   "star_floor_source": "explicit" if star_floor is not None else "cohort_p75"},
        "stamps": {"pool_repos": len(pool), "tagged_repos": len(tags),
                   "dscan_repos": len(dscan), "target_sha": tsha,
                   "target_tags": sorted(ta), "target_cat": tcat},
        "hero": {"fn": target_fn, "stars": trow.get("stars"), "tags": sorted(ta)},
        "top": top,
        "adjudications": {"veto": vetoed, "excluded_ui": excluded_ui,
                          "below_star_floor": below_floor_pool},
        "cohort_kept": len(kept), "cohort_passing_score": len(passing),
    }


# ---------- selftest ----------

def selftest() -> int:
    idf = {"backup": 2.0, "encryption": 5.0, "restore": 2.2, "pitr": 4.0}
    # 1) 稀有标签 idf 更高
    m = idf_map({"a": {"backup": 1}, "b": {"backup": 1, "encryption": 1},
                 "c": {"backup": 1}, "d": {"backup": 1}})
    assert m["encryption"] > m["backup"]
    # 2) 自相似 = 1.0
    t = {"backup": 1.0, "encryption": 1.0}
    assert abs(sim(t, t, idf) - 1.0) < 1e-9
    # 3) 候选私有标签不惩罚：覆盖主角全部标签后，加再多额外专长仍是 1.0
    assert abs(sim(t, {"backup": 1.0, "encryption": 1.0, "pitr": 0.3, "wal": 1.0}, idf) - 1.0) < 1e-9
    # 4) 稀有标签缺失比常见标签缺失扣分更重
    t3 = {"backup": 1.0, "encryption": 1.0}
    drop_rare = sim(t3, {"backup": 1.0}, idf)   # 缺 encryption（稀有）
    drop_common = sim(t3, {"encryption": 1.0}, idf)  # 缺 backup（常见）
    assert drop_rare < drop_common
    # 5) 候选侧低置信共享不折损覆盖（barman 实测案例）
    t2 = {"backup": 1.0, "restore": 1.0}
    assert abs(sim(t2, {"backup": 1.0, "restore": 0.6}, idf) - 1.0) < 1e-9
    # 6) 生态专注度：单库候选不降分，多库通用工具降分
    assert specificity({"postgresql"}, {"postgresql"}) == 1.0
    assert specificity({"postgresql", "mysql"}, {"postgresql"}) == 0.5
    assert specificity(set(), {"postgresql"}) == 1.0
    # 7) p75 钳位
    assert p75([]) == 100
    print("[PASS] arena_select selftest 9 断言")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fn", help="主角 full_name，如 pgbackrest/pgbackrest")
    ap.add_argument("--top", type=int, default=5)
    ap.add_argument("--min-score", type=float, default=0.45)
    ap.add_argument("--star-floor", type=int, default=None)
    ap.add_argument("--veto", default="", help="逗号分隔 fn 列表，人工否决留痕")
    ap.add_argument("--out", default=None, help="结果 JSON 落盘路径")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.fn:
        ap.error("需要 --fn 或 --selftest")
    res = select(a.fn, a.top, a.min_score, a.star_floor,
                 [x.strip() for x in a.veto.split(",") if x.strip()])
    print(f"== {VER} {a.fn} 主角标签 {res['stamps']['target_tags']} "
          f"类目 {res['stamps']['target_cat']} ==")
    print(f"过线 {res['cohort_passing_score']} · 星门槛 {res['params']['star_floor']} "
          f"({res['params']['star_floor_source']}) · 保留 {res['cohort_kept']}")
    print(f"{'score':>6} {'star':>6}  repo")
    for c in res["top"]:
        print(f"{c['score']:6.3f} {c['stars']:6d}  {c['fn']}  [{c['source']}]")
    if res["adjudications"]["excluded_ui"]:
        print(f"界面层剔除 {len(res['adjudications']['excluded_ui'])} 个（详情见 JSON）")
    if a.out:
        Path(a.out).write_text(json.dumps(res, ensure_ascii=False, indent=1),
                               encoding="utf-8")
        print(f"已写 {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
