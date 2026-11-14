# -*- coding: utf-8 -*-
"""gen_cards.py v1.0 -- 批量生成静态项目档案卡（HTML + JSON 双出口，读 cache/ 查表，毫秒/张）

用法:
  python -I gen_cards.py --limit 50            # 冒烟：前 50 张（按 star 降序）
  python -I gen_cards.py                       # 全量（默认全星段；--min-stars 0 与默认等价）
  python -I gen_cards.py --fn patroni/patroni dbeaver/dbeaver   # 指定仓
  python -I gen_cards.py --fn patroni/patroni --force           # 指定仓强制重写（忽略指纹）
  python -I gen_cards.py --sweep-archive       # 全量+盘面清点：把历史孤儿卡（盘上有、清单无）一并归档
  python -I gen_cards.py --selftest

产出 cards/:
  {owner}/{repo}.html / .json    档案卡（增量：指纹不变不重写）
  manifest.json                  清单 {fn -> {html, stars, fp}}，建站索引用；
                                 fp 并入清单后增量比对只读这一个文件，不再逐张读盘上 json
产出 archive/:                   出池卡归档（2026-11-14 用户令：出池卡是档案，只搬不删，后期人工处理）
  {owner}/{repo}.html / .json    从 cards/ 搬来的卡（全量跑时自动：旧清单有、新清单没有）
  manifest.json                  {fn -> {html, stars, fp, archived_at, reason, absent_since[, restored_at]}}
                                 reason = pool-exit / github-archived / app-category；低星未选中的不搬
"""
import argparse, datetime, io, json, os, re, shutil, sys, tempfile, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_card as gc

VER = "gen_cards/1.1"
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = HERE + os.sep + "cache"
OUT = HERE + os.sep + "cards"
ARCHIVE = HERE + os.sep + "archive"
ROOT = "D:/dbhub_collect"
SKIP_CATS = {"应用"}   # judge cat_primary 属应用类的仓不出卡（2026-11-13 用户令；无解读层的不受影响）

def loadj(p): return json.load(io.open(p, encoding="utf-8"))

def clean_ver(t):
    """剥版本标签前缀：release/2.60.0、v2.60.0 -> 2.60.0（空值原样）。"""
    if not t: return t
    return re.sub(r"^[^0-9]+", "", str(t)) or str(t)

def build_card(fn, r, hist, mcounts, arenas, repos, run_date, arena_ver="arena_v?"):
    dates = hist.get("dates", [])
    pts = [[dates[i], s] for i, s in hist.get("series", {}).get(fn, []) if i < len(dates)]
    en = r.get("enrich") or {}
    jd = r.get("judge") or {}
    tx = r.get("text") or {}
    name = fn.split("/")[1]
    card = {
        "schema": "dbhub.card/1.2", "bulk": True, "card_no": 0, "fn": fn,
        "badge": {"main": "dbhub · 项目档案", "sub": jd.get("cat") or "未解读",
                  "basis": "judge.cat_primary；未解读=四层缺该仓"},
        "basics": {
            "name": name, "stars": r.get("stars"), "language": r.get("language"),
            "license": {"display": r.get("license")},
            "pushed_at": r.get("pushed_at"), "created_at": r.get("created_at"),
            "version": {"latest": clean_ver(en.get("rel_ver")), "published": en.get("rel_pub"),
                        "n90": en.get("rel_n90"), "src": "enrich"},
            "activity": {"commit_90d": en.get("commit_90d"), "contributors": en.get("contrib_n"),
                         "security_advisories": en.get("sec_n"), "src": "enrich"},
        },
        "trend": {"points": pts, "src": "cache/stars_history.json（git 历史 N 个日值实抽）"},
        "derived": {"gen_ver": VER, "generated_at": run_date, "fn": fn,
                    "sources": {"basics": "pool", "version/activity": "enrich", "trend": "git 历史",
                                "intro/adapt": "interp 层（AI·带证据行）+ db_scan",
                                "mentions": "data/readmes slug 整串扫描"}},
    }
    mk = gc.stale_marker(r.get("pushed_at"), datetime.date.fromisoformat(run_date))
    if mk: card["stale_chip"] = mk[2:].strip()            # 去掉前导「· 」
    if tx.get("one_liner") or tx.get("highlights") or tx.get("use_cases"):
        card["intro"] = {"text": tx.get("one_liner") or "", "sub": "解读层（AI·证据行可回查）",
                         "points": tx.get("highlights") or [], "uses": tx.get("use_cases") or []}
    if r.get("readme0"):
        card["readme"] = {"text": r["readme0"], "sub": "存档原文 · 程序抽取"}
    # 擂台（cache/arena_all.json，算法 ver 以其 meta.algorithm 为准；简介=池内 description（无则退共享标签），停更自动标记）
    ar = arenas.get(fn)
    if ar and ar.get("top"):
        ttags = {t for t, c in (r.get("tags") or [])}
        def _why_desc(f):
            d = ((repos.get(f) or {}).get("description") or "").strip()
            return (d[:120] + "...") if len(d) > 120 else d
        rows = [{"fn": fn, "stars": r.get("stars"), "score": 1.0,
                 "why": _why_desc(fn) or "·".join(sorted(ttags)) or jd.get("cat") or "主角", "me": True}]
        for c in ar["top"]:
            if c["score"] < 0.6 or len(rows) > 5: break
            why = _why_desc(c["fn"])
            if not why:
                shared = sorted(set(c.get("tags") or []) & ttags)
                why = "·".join(shared) if shared else ("类目相同" if c.get("source") == "cat_fallback" else "标签覆盖")
            p2 = (repos.get(c["fn"].lower()) or {}).get("pushed_at")
            m2 = gc.stale_marker(p2, datetime.date.fromisoformat(run_date))
            if m2: why = f"{why} {m2}"
            rows.append({"fn": c["fn"], "stars": c["stars"], "score": c["score"], "why": why})
        if len(rows) > 1:
            card["arena"] = {"sub": f"算法圈选 {arena_ver} · 相似度 ≥0.60 起展",
                             "display": {"min_score": 0.6, "max_n": 5}, "rows": rows}
    if r.get("dbs"):
        card["adapt"] = {"sub": "db_scan 程序判定", "lines": ["、".join(r["dbs"])]}
    # 近期动态：90 天窗口只展示最近一条发布（版本+日期+英文原文首句），无明细退回单条最新版
    notes = en.get("rel_notes") or []
    if notes:
        card["news"] = {"sub": "enrich · 近 90 天",
                        "items": [{"ver": clean_ver(t), "date": d or "",
                                   "story": s or "（说明见仓库 releases）"} for t, d, s in notes[:1]],
                        "cadence": f"90 天 {en.get('rel_n90') or 0} 发 · 安全通告 {en.get('sec_n') or 0}"}
    elif en.get("rel_ver"):
        card["news"] = {"sub": "enrich · 近 90 天",
                        "items": [{"ver": clean_ver(en["rel_ver"]), "date": en.get("rel_pub") or "",
                                   "story": "最新版本（说明见仓库 releases）"}],
                        "cadence": f"90 天 {en.get('rel_n90') or 0} 发 · 安全通告 {en.get('sec_n') or 0}"}
    mc = mcounts.get(fn)          # slug 口径键=fn（owner/repo），天然唯一零借数；>=1 才挂块
    if mc is not None and mc >= 1:
        card["_mc"] = mc
    ins = jd.get("install") or []
    if "pypi" in ins:
        card["hands_on"] = {"sub": "安装线索（未实跑）",
                            "lines": [f"# pip install {name}（解读层线索，命令未实跑）"]}
    return card

def fingerprint(card):
    """整卡内容 md5（剔除 generated_at 与 _fp）+ 渲染器版本：内容或模板任何变化都触发重写。"""
    import hashlib
    c = dict(card)
    c.pop("_fp", None)
    c["derived"] = {k: v for k, v in (c.get("derived") or {}).items() if k != "generated_at"}
    blob = VER + "/" + gc.VER + json.dumps(c, ensure_ascii=False, sort_keys=True)
    return hashlib.md5(blob.encode("utf-8")).hexdigest()[:16]

# ---------- 出池归档（只搬不删） ----------

def exit_reason(fn, repos):
    """一张卡为什么退出活跃清单。below-min-stars = 仓仍是合格目标、只是本次没选中，不算出池不归档
    （防 --min-stars 300 跑一次把 1.9 万张低星卡整批搬走）。"""
    r = repos.get(fn)
    if r is None: return "pool-exit"
    if r.get("archived"): return "github-archived"
    if (r.get("judge") or {}).get("cat") in SKIP_CATS: return "app-category"
    return "below-min-stars"

def sweep_strays(out_dir, active):
    """盘面清点：盘上有、活跃清单没有的卡（清单机制上线前遗留的孤儿），返回 {fn: 仿清单条目}。"""
    ex = {}
    for owner in os.listdir(out_dir):
        d = os.path.join(out_dir, owner)
        if not os.path.isdir(d): continue
        for f in os.listdir(d):
            if not f.endswith(".json"): continue
            fn = (owner + "/" + f[:-5]).lower()
            if fn in active: continue
            try: c = loadj(os.path.join(d, f))
            except Exception: c = {}
            ex[fn] = {"stars": (c.get("basics") or {}).get("stars"), "fp": c.get("_fp")}
    return ex

def archive_exited(exited, repos, out_dir, arc_dir, run_date, active, absent=None):
    """把退出活跃清单的卡搬进归档目录并落归档清单。只搬不删；回池的仓只打 restored_at 标、档案不动。
    exited: {fn: 旧清单条目}；active: 本次活跃清单；absent: 出池台账 {fn: 出池日}。"""
    absent = absent or {}
    amp = os.path.join(arc_dir, "manifest.json")
    acards = (loadj(amp).get("cards") or {}) if os.path.exists(amp) else {}
    st = {"moved": 0, "kept": 0, "restored": 0, "by": {}}
    changed = False
    for fn, old in sorted(exited.items()):
        reason = exit_reason(fn, repos)
        if reason == "below-min-stars": st["kept"] += 1; continue
        owner, repo = fn.split("/")
        moved = False
        for ext in (".html", ".json"):
            src = os.path.join(out_dir, owner, repo + ext)
            if os.path.exists(src):
                os.makedirs(os.path.join(arc_dir, owner), exist_ok=True)
                os.replace(src, os.path.join(arc_dir, owner, repo + ext))
                moved = True
        try: os.rmdir(os.path.join(out_dir, owner))        # 只在目录已空时成功
        except OSError: pass
        if moved or fn not in acards:
            acards[fn] = {"html": f"archive/{owner}/{repo}.html", "stars": (old or {}).get("stars"),
                          "fp": (old or {}).get("fp"), "archived_at": run_date, "reason": reason,
                          "absent_since": absent.get(fn)}
            changed = True
        if moved:
            st["moved"] += 1; st["by"][reason] = st["by"].get(reason, 0) + 1
    for fn, e in acards.items():
        if fn in active and not e.get("restored_at"):
            e["restored_at"] = run_date; st["restored"] += 1; changed = True
    if changed:
        os.makedirs(arc_dir, exist_ok=True)
        io.open(amp, "w", encoding="utf-8", newline="\n").write(
            json.dumps({"ver": VER, "updated_at": run_date, "count": len(acards), "cards": acards},
                       ensure_ascii=False, indent=1))
    st["total"] = len(acards)
    return st

def _selftest():
    rc = gc._selftest() or 0
    repos = {"a/live": {"stars": 5}, "a/arch": {"archived": True}, "a/app": {"judge": {"cat": "应用"}}}
    assert exit_reason("x/gone", repos) == "pool-exit"
    assert exit_reason("a/arch", repos) == "github-archived"
    assert exit_reason("a/app", repos) == "app-category"
    assert exit_reason("a/live", repos) == "below-min-stars"          # 合格目标没选中：不算出池
    assert clean_ver("release/2.60.0") == "2.60.0" and clean_ver("v1.2") == "1.2" and clean_ver(None) is None
    with tempfile.TemporaryDirectory() as td:                          # 归档搬迁实测
        out, arc = os.path.join(td, "cards"), os.path.join(td, "archive")
        for fn in ("x/gone", "a/live"):
            o, rp = fn.split("/"); os.makedirs(os.path.join(out, o), exist_ok=True)
            for ext in (".html", ".json"):
                io.open(os.path.join(out, o, rp + ext), "w", encoding="utf-8").write('{"_fp": "f1"}')
        assert set(sweep_strays(out, {"a/live": {}})) == {"x/gone"}       # 盘面清点只认清单外的
        st = archive_exited({"x/gone": {"stars": 9, "fp": "f1"}, "a/live": {"stars": 5}},
                            repos, out, arc, "2026-11-14", {"a/live": {}}, {"x/gone": "20261112"})
        assert st["moved"] == 1 and st["kept"] == 1 and st["by"] == {"pool-exit": 1}
        assert os.path.exists(os.path.join(arc, "x", "gone.html")) and not os.path.exists(os.path.join(out, "x"))
        assert os.path.exists(os.path.join(out, "a", "live.json"))       # 低星未选中：原地不动
        am = loadj(os.path.join(arc, "manifest.json"))["cards"]
        assert am["x/gone"]["reason"] == "pool-exit" and am["x/gone"]["absent_since"] == "20261112"
        st2 = archive_exited({}, repos, out, arc, "2026-11-15", {"x/gone": {}})   # 回池：打标不删档
        assert st2["restored"] == 1 and st2["moved"] == 0 and os.path.exists(os.path.join(arc, "x", "gone.json"))
        assert loadj(os.path.join(arc, "manifest.json"))["cards"]["x/gone"]["restored_at"] == "2026-11-15"
    print("OK gen_cards selftest: 13 asserts passed")
    return rc

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--min-stars", type=int, default=0,
                   help="星数下限，默认 0=全星段（全量口径，2026-11-14 用户定案）")
    p.add_argument("--limit", type=int, default=0)
    p.add_argument("--fn", nargs="+")
    p.add_argument("--force", action="store_true", help="忽略指纹强制重写（配合 --fn 重新生成指定卡）")
    p.add_argument("--cache-dir", default=CACHE)
    p.add_argument("--out-dir", default=OUT)
    p.add_argument("--archive-dir", default=ARCHIVE)
    p.add_argument("--sweep-archive", action="store_true",
                   help="全量跑前先盘面清点，把历史孤儿卡（盘上有、清单无）一并归档")
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.selftest: sys.exit(_selftest() or 0)
    t0 = time.time(); run_date = datetime.date.today().isoformat()
    idx = loadj(a.cache_dir + "/index.json")
    hist = loadj(a.cache_dir + "/stars_history.json")
    men = loadj(a.cache_dir + "/mentions.json")
    ap = a.cache_dir + "/arena_all.json"
    adoc = loadj(ap) if os.path.exists(ap) else {}
    arenas = adoc.get("arenas") or {}
    arena_ver = (adoc.get("meta") or {}).get("algorithm") or "arena_v?"   # 卡面标签跟算法版本走
    if not arenas: print("WARN no arena cache (run arena_batch.py first); cards go without arena")
    mcounts = men["counts"]; corpus = men["meta"]["corpus"]
    mdate = str(men["meta"].get("built_at", ""))[:10]   # 截至戳=缓存建成日，与精选卡同口径
    repos = idx["repos"]
    if a.fn:
        targets = [f.lower() for f in a.fn]
    else:
        targets = [fn for fn, r in repos.items()
                   if (r.get("stars") or 0) >= a.min_stars and not r.get("archived")
                   and (r.get("judge") or {}).get("cat") not in SKIP_CATS]
        targets.sort(key=lambda fn: -(repos[fn].get("stars") or 0))
        if a.limit: targets = targets[:a.limit]
    n_new = n_skip = 0; cov = {"trend": 0, "intro": 0, "readme": 0, "adapt": 0, "arena": 0,
                               "news": 0, "mentions": 0, "stale": 0}
    manifest = {}
    mp = os.path.join(a.out_dir, "manifest.json")
    old_cards = {}   # 已有清单：指纹用于增量比对（只读这一个文件），条目用于出池归档
    if os.path.exists(mp):
        try: old_cards = loadj(mp).get("cards") or {}
        except Exception: old_cards = {}
    old_fps = {fn: (e or {}).get("fp") for fn, e in old_cards.items()}
    for fn in targets:
        r = repos.get(fn)
        if not r: print(f"SKIP not-in-index {fn}"); continue
        if (r.get("judge") or {}).get("cat") in SKIP_CATS: print(f"SKIP app-category {fn}"); continue
        card = build_card(fn, r, hist, mcounts, arenas, repos, run_date, arena_ver)
        mc = card.pop("_mc", None)
        if mc is not None:
            card["production_users"] = {"sub": "README 提及数",
                "items": [{"text": gc.mention_line(mc, corpus, mdate), "type": "mention-count",
                           "source": "data/readmes slug(owner/repo) 整串扫描（排除本仓与同 org，仅计池内）"}]}
        card["_fp"] = fingerprint(card)
        owner, repo = fn.split("/")
        d = os.path.join(a.out_dir, owner); os.makedirs(d, exist_ok=True)
        jp = os.path.join(d, repo + ".json"); hp = os.path.join(d, repo + ".html")
        if old_fps.get(fn) == card["_fp"] and not a.force:
            # 指纹比对走 manifest 单文件；清单缺指纹/丢清单时回退到重写，安全侧
            n_skip += 1
            manifest[fn] = {"html": f"cards/{owner}/{repo}.html", "stars": r.get("stars"), "fp": card["_fp"]}
            continue
        io.open(hp, "w", encoding="utf-8", newline="\n").write(gc.render(card))
        io.open(jp, "w", encoding="utf-8", newline="\n").write(json.dumps(card, ensure_ascii=False, indent=2))
        n_new += 1
        manifest[fn] = {"html": f"cards/{owner}/{repo}.html", "stars": r.get("stars"), "fp": card["_fp"]}
        if card["trend"]["points"]: cov["trend"] += 1
        if card.get("intro"): cov["intro"] += 1
        if card.get("readme"): cov["readme"] += 1
        if card.get("arena"): cov["arena"] += 1
        if card.get("adapt"): cov["adapt"] += 1
        if card.get("news"): cov["news"] += 1
        if card.get("production_users"): cov["mentions"] += 1
        if card.get("stale_chip"): cov["stale"] += 1
    if (a.fn or a.limit) and os.path.exists(mp):
        # 局部重跑：并入已有清单，绝不能把 2,981 张覆盖成只剩本次几张
        manifest = {**loadj(mp)["cards"], **manifest}
    io.open(mp, "w", encoding="utf-8", newline="\n").write(
        json.dumps({"ver": VER, "generated_at": run_date, "count": len(manifest),
                    "index_built_at": idx["meta"]["built_at"], "cards": manifest}, ensure_ascii=False, indent=1))
    print(f"OK gen_cards: targets={len(targets)} new={n_new} skip-unchanged={n_skip} "
          f"coverage={cov} total={time.time()-t0:.1f}s")
    if not (a.fn or a.limit):
        # 出池归档只在全量跑做：局部跑的清单是并入的，「旧有新无」不成立
        exited = {fn: e for fn, e in old_cards.items() if fn not in manifest}
        if a.sweep_archive: exited = {**sweep_strays(a.out_dir, manifest), **exited}
        ab = {}
        try: ab = {k.lower(): v for k, v in loadj(ROOT + "/state/absent_since.json").items()}
        except Exception: pass
        st = archive_exited(exited, repos, a.out_dir, a.archive_dir, run_date, manifest, ab)
        if st["moved"] or st["kept"] or st["restored"]:
            print(f"ARCHIVE moved={st['moved']} {st['by']} kept-below-min-stars={st['kept']} "
                  f"restored-marked={st['restored']} -> archive total={st['total']}")

if __name__ == "__main__":
    main()
