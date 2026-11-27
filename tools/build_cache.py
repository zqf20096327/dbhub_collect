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

VER = "build_cache/1.6"   # 1.6：judge 增 persona / eco / cat_tags（判定卷三字段，站点 /compare/ 自选对比「面向谁 / 生态位 /
                          #     多标签」数据源；只有 v4 判定卷带这三项，旧代条目缺=空值、下游按「未解读」处理）；
                          # 1.5：dbs 数据源改「判定层引擎优先 + db_scan.v2 兜底」（与 11-01 裁定「归属移交程序判定、
                          #     首选引擎+存量兜底」同口径；修 P9.7 断点：引擎 0.3.0 填入判定层的归属从未被读取，
                          #     metabase/drawdb/airbyte 等仅引擎有归属的 914 仓被误剔出站、768 重叠中 238 仓值偏旧）；
                          # 1.4：judge 增 ai_kind 提升、全仓 official 标记（P9 站点浏览「属性」筛选数据源）；
                          # 1.3：加 readme_file 字段（README 存档文件存在性，无 README 仓归档口径的判定源）
ROOT = "D:/dbhub_collect"
POOL = ROOT + "/data/live/pool.ndjson"
VOCAB = ROOT + "/config/domain_vocab_v0.11.json"
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

def vocab_cn():
    """slug -> 中文名（词表是唯一真源；读不到词表返回空表，调用侧兜底用 slug 原样）。"""
    m = {}
    try:
        for dom in loadj(VOCAB).get("domains") or []:
            for w in dom.get("words") or []:
                if w.get("slug") and w.get("cn"): m[w["slug"]] = w["cn"]
    except Exception:
        pass
    return m

def db_org_map():
    """db_profiles orgs -> {库名小写: (org 登录名小写,…)}，str 与 dict 两种条目形态统一收。
    名单即「厂商官方 org」（dedicated=org 即产品 / cloud=云厂商超集 org，都是官方）。"""
    import importlib.util
    spec = importlib.util.spec_from_file_location("db_profiles_bcache", ROOT + "/config/db_profiles.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    m = {}
    for p in mod.PROFILES:
        if not p.get("enabled", True): continue
        names = {(o.get("name") if isinstance(o, dict) else o or "").lower()
                 for o in (p.get("orgs") or [])}
        names.discard("")
        m[p["name"].lower()] = tuple(sorted(names))
    return m

def is_official(owner, dbs, org_of_db):
    """官方 = owner 命中其适配库之一的厂商 org 名单（大小写不敏感）。工具仓/空 dbs 恒 False。"""
    o = (owner or "").lower()
    return bool(o) and any(o in org_of_db.get(str(d).lower(), ()) for d in (dbs or []))

def dbs_of(judge_e, scan_e):
    """归属来源仲裁：判定层引擎结果（classification.dbs，引擎 0.3.0 填入）优先，db_scan.v2 兜底。
    引擎为空才落兜底，不做并集（引擎判定可能比旧扫描更窄/更准，如 questdb 只剩 PostgreSQL）。"""
    d = ((judge_e or {}).get("classification") or {}).get("dbs") or []
    if d: return sorted(set(d)), "engine"
    c = (scan_e or {}).get("cands") or {}
    return (sorted(c.keys()), "dbscan") if c else ([], "")

def judge_fields(j):
    """判定卷条目 -> 索引 judge 字段。1.6 增 persona/eco/cat_tags（v4 判定卷才有；旧代条目为空值）。"""
    c = j.get("classification") or {}
    return {"cat": c.get("cat_primary"),
            "conf": (j.get("audit") or {}).get("confidence"),
            "install": (j.get("signals") or {}).get("install"),
            "ai_kind": c.get("ai_kind"),
            "persona": c.get("persona") or [],
            "eco": c.get("eco"),
            "cat_tags": c.get("cat_tags") or []}

def build_index():
    t0 = time.time(); repos = {}
    cn = vocab_cn()
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
        repos[k]["readme_file"] = bool(stem)   # 显式 True/False 都写：无 README 仓靠 False 触发归档；
        if not stem: continue                  # 旧缓存（v1.2 前）整仓无此字段 -> 判 False 安全侧不归档
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
    for layer in ("judge", "text", "domain_tags", "desc"):
        m = {}
        for f in glob.glob(f"{INTERP_DIR}/{layer}/shards/*.json"):
            for sha, e in loadj(f).items(): m[sha] = e
        layers[layer] = m
    n_j = n_t = n_tag = n_desc = n_eng = 0
    for fn, ent in loadj(INTERP_STATE)["items"].items():
        k = fn.lower(); sha = ent.get("sha")
        if k not in repos or not sha: continue
        if sha.startswith("desc::"):    # 无 README 仓：desc 降级层（AI·仅据描述·低置信，键不与三层相交）
            d = layers["desc"].get(sha)
            if d:
                repos[k]["desc"] = {"one_liner": (d.get("identity") or {}).get("one_liner"),
                                    "cat": (d.get("classification") or {}).get("cat_primary")}
                n_desc += 1
            continue
        j = layers["judge"].get(sha)
        if j:
            repos[k]["judge"] = judge_fields(j)
            n_j += 1
            d, _ = dbs_of(j, None)               # 引擎归属优先（1.5）：判定层 classification.dbs 在此进 index
            if d:
                repos[k]["dbs"] = d; n_eng += 1
        t = layers["text"].get(sha)
        if t:
            ident = t.get("identity", {})
            repos[k]["text"] = {"one_liner": ident.get("one_liner"),
                                "review": ident.get("review"),
                                "highlights": ident.get("highlights"),
                                "use_cases": ident.get("use_cases")}
            n_t += 1
        g = layers["domain_tags"].get(sha)
        if g:
            repos[k]["tags"] = [[x.get("slug"), cn.get(x.get("slug")) or x.get("slug"), x.get("conf")]
                                for x in (g.get("tags") or []) if x.get("slug")]
            n_tag += 1
    n_db = 0
    if os.path.exists(DBSCAN):
        for fn, e in loadj(DBSCAN).items():
            k = fn.lower()
            if k in repos and e.get("cands") and not repos[k].get("dbs"):   # 引擎已判的不再兜底（引擎优先）
                repos[k]["dbs"] = sorted(e["cands"].keys()); n_db += 1
    org_of_db = db_org_map()                       # P9：官方标记（owner 命中适配库的厂商 org）
    n_off = 0
    for r in repos.values():
        hit = is_official(r.get("owner"), r.get("dbs"), org_of_db)
        r["official"] = hit                        # 显式写 True/False 两边（布尔字段只写 True 的旧坑）
        n_off += hit
    meta = {"ver": VER, "built_at": now(), "pool_file": POOL,
            "counts": {"pool": n_pool, "enrich": n_en, "rel_notes": n_notes, "judge": n_j, "text": n_t,
                       "domain_tags": n_tag, "desc": n_desc, "dbs_engine": n_eng, "dbscan": n_db,
                       "readme0": n_rm, "official": n_off}}
    size = dumpj({"meta": meta, "repos": repos}, CACHE + "/index.json")
    print(f"OK index: pool={n_pool} enrich={n_en} relnotes={n_notes} judge={n_j} text={n_t} tags={n_tag} "
          f"desc={n_desc} dbs_engine={n_eng} dbscan={n_db} readme0={n_rm} official={n_off} "
          f"-> {size//1024} KB in {time.time()-t0:.1f}s")
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
    om = db_org_map()                                    # P9：官方 org 名单（str/dict 两种形态统一收）
    assert om["tidb"] == ("pingcap", "tidb-incubator", "tidb-samples", "tikv")
    assert "percona" in om["postgresql"] and "percona" in om["mysql"]   # 一 org 双库合法
    assert "clickhouse" in om["clickhouse"]                          # 国际 str 形态小写化
    assert is_official("pingcap", ["TiDB", "MySQL"], om) is True     # 命中自家库 org
    assert is_official("PingCAP", ["TiDB"], om) is True              # 大小写不敏感
    assert is_official("dbeaver", ["PostgreSQL", "TiDB"], om) is False   # 工具仓不算
    assert is_official("", ["TiDB"], om) is False and is_official("x", [], om) is False
    assert is_official("postgres", ["MySQL"], om) is False           # 只认「适配了该库」的 org
    assert dbs_of({"classification": {"dbs": ["MySQL", "PostgreSQL", "MySQL"]}},
                  {"cands": {"SQLite": ["x"]}}) == (["MySQL", "PostgreSQL"], "engine")  # 引擎优先+去重排序
    assert dbs_of({"classification": {"dbs": []}},
                  {"cands": {"ClickHouse": ["x"]}}) == (["ClickHouse"], "dbscan")      # 引擎空才兜底
    assert dbs_of(None, {"cands": {"ClickHouse": ["x"]}}) == (["ClickHouse"], "dbscan")
    assert dbs_of({}, {}) == ([], "") and dbs_of(None, None) == ([], "")
    jf = judge_fields({"classification": {"cat_primary": "管理", "persona": ["ops", "build"], "eco": "tool",
                                          "ai_kind": "text2sql", "cat_tags": ["连接/代理"]},
                       "audit": {"confidence": "high"}, "signals": {"install": ["binary", "docker"]}})
    assert jf == {"cat": "管理", "conf": "high", "install": ["binary", "docker"], "ai_kind": "text2sql",
                  "persona": ["ops", "build"], "eco": "tool", "cat_tags": ["连接/代理"]}
    j0 = judge_fields({})                               # 1.6：旧代条目无三项 -> 空值（persona/cat_tags 恒为列表）
    assert j0["persona"] == [] and j0["cat_tags"] == [] and j0["eco"] is None and j0["cat"] is None
    assert judge_fields({"classification": None, "audit": None, "signals": None})["conf"] is None   # 显式 null 安全
    print("OK build_cache selftest: 25 asserts passed")
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
