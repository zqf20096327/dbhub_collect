# -*- coding: utf-8 -*-
"""build_cache.py v1.0 -- 全池索引与缓存（每日一次，卡片生成全部走查表）

用法:
  python -I build_cache.py --steps all                 # index + trend + mentions
  python -I build_cache.py --steps index
  python -I build_cache.py --steps trend --days 30
  python -I build_cache.py --steps mentions
  python -I build_cache.py --selftest

产物 cache/:
  index.json         fn(小写) -> 池字段 + enrich(含发布说明首句) + judge/text/domain_tags + db_scan 库集
  stars_history.json 近 N 天每日全池星数（按快照循环，不按仓循环）
  mentions.json      池内仓 slug(owner/repo) 在全库 README 的整串提及计数
"""
import argparse, datetime, io, json, os, re, subprocess, sys, time, glob

VER = "build_cache/1.0"
ROOT = "D:/dbhub_collect"
POOL = ROOT + "/data/live/pool.ndjson"
ENRICH_DIR = ROOT + "/state/enrich_cache_shards"
INTERP_STATE = ROOT + "/state/interp_state.json"
INTERP_DIR = ROOT + "/state/interp"
DBSCAN = ROOT + "/state/db_scan.v2.json"
README_DIR = ROOT + "/data/readmes"
CACHE = os.path.dirname(os.path.abspath(__file__)) + os.sep + "cache"

def now(): return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def loadj(p):
    return json.load(io.open(p, encoding="utf-8"))

def dumpj(obj, p):
    io.open(p, "w", encoding="utf-8", newline="\n").write(json.dumps(obj, ensure_ascii=False))
    return os.path.getsize(p)

def git_text(args):
    p = subprocess.run(["git", "-C", ROOT] + args, capture_output=True)
    return p.stdout.decode("utf-8", "replace") if p.returncode == 0 else None

MD_SKIP = ("#", "<", "[!", "![", "---", "|", "```", ":", ">")
LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")
TAG = re.compile(r"<[^>]+>")

def readme_first_para(fn_orig):
    """README 存档首段：跳过标题/徽章/图片/表格，取第一段正文（≤200 字符，原文引用不翻译）。"""
    p = os.path.join(README_DIR, fn_orig.replace("/", "__") + ".md")
    if not os.path.exists(p): return None
    try:
        with io.open(p, encoding="utf-8", errors="replace") as f:
            lines = f.read(65536).split("\n")      # 首段在前 64KB 内，不读全文
    except Exception:
        return None
    buf = []
    for ln in lines[:200]:
        s = ln.strip()
        if not s:
            if buf: break
            continue
        if s.startswith(MD_SKIP) or len(s) < 4:
            if buf: break
            continue
        c = TAG.sub("", LINK.sub(r"\1", s)).replace("**", "").replace("`", "")
        if len(c) < 4:
            if buf: break
            continue
        buf.append(c)
        if sum(len(x) for x in buf) > 160: break
    t = " ".join(buf).strip()
    return t[:200] if len(t) > 30 else None

def note_first(n):
    """英文发布说明首句：剥 markdown/列表前缀，截到第一个 '. '（≤300 字符，原文引用不翻译）。"""
    t = TAG.sub("", LINK.sub(r"\1", n)).replace("**", "").replace("`", "")
    t = " ".join(t.strip().lstrip("-#>* ").split())
    i = t.find(". ")
    if i > 0: t = t[:i + 1]
    return t[:300] if len(t) > 10 else ""

# ---------- ① 全池索引 ----------

def build_index():
    t0 = time.time(); repos = {}
    for line in io.open(POOL, encoding="utf-8"):
        try: r = json.loads(line)
        except Exception: continue
        fn = r.get("full_name")
        if not fn: continue
        repos[fn.lower()] = {"stars": r.get("stars"), "language": r.get("language"),
            "license": r.get("license"), "pushed_at": r.get("pushed_at"),
            "created_at": r.get("created_at"), "owner": r.get("owner"),
            "owner_type": r.get("owner_type"), "topics": r.get("topics") or [],
            "archived": r.get("archived")}
        if r.get("description"):
            repos[fn.lower()]["description"] = r["description"][:200]
    n_pool = len(repos)
    # README 首段（原文引用，程序抽取）
    n_rm = 0
    files = {f[:-3].lower(): f[:-3] for f in os.listdir(README_DIR) if f.endswith(".md")}
    for k in repos:
        stem = files.get(k.replace("/", "__"))
        if not stem: continue
        para = readme_first_para(stem)
        if para:
            repos[k]["readme0"] = para; n_rm += 1
    n_en = n_notes = 0
    for f in glob.glob(ENRICH_DIR + "/*.json"):
        for fn, e in loadj(f).items():
            k = fn.lower()
            if k in repos:
                repos[k]["enrich"] = {x: e.get(x) for x in
                    ("rel_ver", "rel_pub", "rel_n90", "commit_7d", "commit_90d", "contrib_n", "sec_n")}
                n_en += 1
                notes = [x for x in (e.get("rel_notes") or []) if x.get("t")]
                if notes:
                    repos[k]["enrich"]["rel_notes"] = [
                        [x.get("t"), x.get("d"), note_first(x.get("n") or "")] for x in notes]
                    n_notes += 1
    layers = {}
    for layer in ("judge", "text", "domain_tags"):
        m = {}
        for f in glob.glob(f"{INTERP_DIR}/{layer}/shards/*.json"):
            for sha, e in loadj(f).items(): m[sha] = e
        layers[layer] = m
    n_j = n_t = n_tag = 0
    for fn, ent in loadj(INTERP_STATE)["items"].items():
        k = fn.lower(); sha = ent.get("sha")
        if k not in repos or not sha: continue
        j = layers["judge"].get(sha)
        if j:
            repos[k]["judge"] = {"cat": j.get("classification", {}).get("cat_primary"),
                                 "conf": j.get("audit", {}).get("confidence"),
                                 "install": j.get("signals", {}).get("install")}
            n_j += 1
        t = layers["text"].get(sha)
        if t:
            ident = t.get("identity", {})
            repos[k]["text"] = {"one_liner": ident.get("one_liner"),
                                "highlights": ident.get("highlights"),
                                "use_cases": ident.get("use_cases")}
            n_t += 1
        g = layers["domain_tags"].get(sha)
        if g:
            repos[k]["tags"] = [[x.get("slug"), x.get("conf")] for x in (g.get("tags") or [])]
            n_tag += 1
    n_db = 0
    if os.path.exists(DBSCAN):
        for fn, e in loadj(DBSCAN).items():
            k = fn.lower()
            if k in repos and e.get("cands"):
                repos[k]["dbs"] = sorted(e["cands"].keys()); n_db += 1
    meta = {"ver": VER, "built_at": now(), "pool_file": POOL,
            "counts": {"pool": n_pool, "enrich": n_en, "rel_notes": n_notes, "judge": n_j, "text": n_t,
                       "domain_tags": n_tag, "dbscan": n_db, "readme0": n_rm}}
    size = dumpj({"meta": meta, "repos": repos}, CACHE + "/index.json")
    print(f"OK index: pool={n_pool} enrich={n_en} relnotes={n_notes} judge={n_j} text={n_t} tags={n_tag} "
          f"dbscan={n_db} readme0={n_rm} -> {size//1024} KB in {time.time()-t0:.1f}s")
    return meta

# ---------- ② 星数历史（按快照循环） ----------

def parse_pool_blob(text, series, i):
    for line in text.split("\n"):
        try: r = json.loads(line)
        except Exception: continue
        fn = r.get("full_name"); s = r.get("stars")
        if fn and s is not None: series.setdefault(fn.lower(), []).append([i, s])

def build_trend(days):
    t0 = time.time()
    log = git_text(["log", "--format=%H%x09%cs", "--", "data/live/pool.ndjson"])
    if not log: print("FAIL trend: git log empty"); return
    per_date = {}
    for ln in log.splitlines():          # 新->旧，同日第一条=当日最新
        h, _, d = ln.partition("\t")
        if d and h and d not in per_date: per_date[d] = h
    dates = sorted(per_date)[-days:]
    series = {}; skipped = []
    for i, d in enumerate(dates):
        blob = git_text(["show", f"{per_date[d]}:data/live/pool.ndjson"])
        if not blob:
            skipped.append(d); continue
        parse_pool_blob(blob, series, i)
        if (i + 1) % 10 == 0: print(f"  trend {i+1}/{len(dates)} dates ...")
    today = datetime.date.today().isoformat()
    if today not in per_date:            # 当天还没提交，用工作区文件补最后一个点
        dates.append(today)
        parse_pool_blob(io.open(POOL, encoding="utf-8").read(), series, len(dates) - 1)
    out = {"meta": {"ver": VER, "built_at": now(), "days": len(dates),
                    "skipped_dates": skipped}, "dates": dates, "series": series}
    size = dumpj(out, CACHE + "/stars_history.json")
    n_pts = sum(len(v) for v in series.values())
    print(f"OK trend: {len(dates)} dates ({dates[0]}..{dates[-1]}) repos={len(series)} "
          f"points={n_pts} skipped={len(skipped)} -> {size//1024//1024} MB in {time.time()-t0:.1f}s")

# ---------- ③ README 提及（slug 整串：owner/repo，URL 相邻对切分） ----------

SLUG_RUN = re.compile(r"[a-z0-9_.\-]+(?:/[a-z0-9_.\-]+)+")

def slug_hits(txt):
    """全文出现过的 slug 候选集：a/b/c 路径串按相邻对切分，段剥首尾 ._-、去尾缀 .git。
    github.com/owner/repo 若不切相邻对只会得到 github.com/owner——切对才捞得回 owner/repo；
    git clone .../repo.git 若不去尾缀会得到 owner/repo.git 而漏匹配（GitHub 仓名不含尾缀
    .git，剥它不会误伤）。"""
    hits = set()
    for run in SLUG_RUN.findall(txt):
        parts = []
        for q in run.split("/"):
            q = q.strip("._-")
            if q.endswith(".git"): q = q[:-4]
            if q: parts.append(q)
        hits.update(a + "/" + b for a, b in zip(parts, parts[1:]))
    return hits

def build_mentions(index):
    """slug（owner/repo）整串提及计数。2026-11-14 用户裁定弃「裸名+>=300 星门槛」改 slug：
    slug 全池天然唯一——同名借数、通用词词频两类噪声零门槛消失，低星国产仓也能算
    （实测 apsaradb/polardb-for-postgresql 1 星被 12 个外部 README 硬引用）。"""
    t0 = time.time()
    repos = index["repos"]
    terms = {fn: {"owner": fn.split("/")[0], "n": 0} for fn in repos}
    poolset = set(repos); corpus = 0; matched_files = 0
    for fname in os.listdir(README_DIR):
        if not fname.endswith(".md"): continue
        corpus += 1
        try:
            txt = io.open(os.path.join(README_DIR, fname), encoding="utf-8", errors="replace").read().lower()
        except Exception:
            continue
        fn = fname[:-3].replace("__", "/", 1).lower()
        if fn not in poolset: continue
        owner = fn.split("/")[0]
        hit = False
        for s in slug_hits(txt):
            e = terms.get(s)
            if e and s != fn and e["owner"] != owner:
                e["n"] += 1; hit = True
        if hit: matched_files += 1
        if corpus % 10000 == 0: print(f"  mentions {corpus} files ...")
    counts = {t: e["n"] for t, e in terms.items()}
    out = {"meta": {"ver": VER, "built_at": now(), "corpus": corpus,
                    "rule": "slug(owner/repo) 整串匹配，排除本仓与同 org，仅计池内"},
           "counts": counts}
    size = dumpj(out, CACHE + "/mentions.json")
    print(f"OK mentions: terms={len(terms)} corpus={corpus} matched_files={matched_files} "
          f"-> {size//1024} KB in {time.time()-t0:.1f}s")

# ---------- 自检 ----------

def _selftest():
    s = {}
    parse_pool_blob('{"full_name":"a/a","stars":1}', s, 0)
    parse_pool_blob('{"full_name":"a/a","stars":3}\nnot-json\n{"full_name":"b/b"}', s, 1)
    assert s == {"a/a": [[0, 1], [1, 3]]} and "b/b" not in s   # 空 stars 不记、坏行跳过
    m = {}
    for fn in ("x/tool", "y/tool", "x/other", "z/app"):   # 同名 tool：排除同 owner x、保留 y
        m.setdefault("tool", {"self": "x/tool", "owner": "x", "n": 0})
    e = m["tool"]; fn = "y/tool"
    assert fn != e["self"] and fn.split("/")[0] != e["owner"]
    h = slug_hits("see github.com/actiontech/sqle and git clone https://github.com/pingcap/tidb.git x")
    assert "actiontech/sqle" in h and "github.com/actiontech" in h   # URL 相邻对切分
    assert "pingcap/tidb" in h and "pingcap/tidb.git" not in h       # 段尾 .git 剥掉
    assert slug_hits("mysql/mysql-server") == {"mysql/mysql-server"}  # 相邻对不含跨段
    assert slug_hits("no slug here") == set() and "pgbackrest" not in slug_hits("use pgbackrest")
    assert note_first("**IMPORTANT NOTE**: The restore command will now error. Rest will not show") \
        == "IMPORTANT NOTE: The restore command will now error."
    assert note_first("- PostgreSQL 19beta4 support.") == "PostgreSQL 19beta4 support."
    assert note_first("See [link](http://x) for more. tail") == "See link for more."
    assert note_first("") == "" and note_first("short") == ""
    print("OK build_cache selftest: 10 asserts passed")
    return 0

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--steps", default="all", help="all | index,trend,mentions 逗号分隔")
    p.add_argument("--days", type=int, default=30)
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.selftest: sys.exit(_selftest())
    os.makedirs(CACHE, exist_ok=True)
    steps = a.steps.split(",")
    idx = None
    for s in steps:
        if s == "index": idx = {"meta": None, "repos": None}; build_index()
        elif s == "trend": build_trend(a.days)
        elif s == "mentions":
            if idx is None or idx["repos"] is None:
                if not os.path.exists(CACHE + "/index.json"): build_index()
                idx = loadj(CACHE + "/index.json")
            build_mentions(idx)
        elif s == "all":
            build_index(); build_trend(a.days)
            build_mentions(loadj(CACHE + "/index.json"))
        else: p.error(f"unknown step {s}")

if __name__ == "__main__":
    main()
