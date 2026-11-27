# -*- coding: utf-8 -*-
"""build_site.py v1.0 -- 站点数据出口（P2：卡片不动，只产列表分片/库页数据/sitemap/robots）

用法:
  python -I build_site.py                     # 全部步骤（lists+vs+cmp+sitemap+robots）
  python -I build_site.py --steps lists,sitemap,robots
  python -I build_site.py --selftest
  DBHUB_SITE_BASE=https://x.pages.dev python -I build_site.py   # sitemap 绝对 URL 的域名（P4 部署时注入）

输入（运行位）:
  cache/index.json      池字段+类目+标签+一句话（build_cache 产物）
  cards/manifest.json   活跃卡清单（gen_cards 产物）

输出 site/:
  data/cat/{slug}-{n}.json    类目分页分片（100/页，星数降序；slug=misc 表「综合」兜未分类）
  data/all-{n}.json           全站总览分页（/projects 浏览页数据源）
  data/db/{slug}.json         17 库页数据（每库相关卡聚合，星数降序）
  data/cmp/{bb}.json          对比页富字段 256 分桶（/compare/ 自选对比：综述/亮点/场景/能力/趋势/擂台等，bb=fn 的 FNV 低字节）
  sitemap.xml                 首页 + 17 库页 + 类目分页 + 全部活跃卡（单文件 <5 万 URL）
  robots.txt                  放行全部 + 指向 sitemap

URL 规范（与 P3 dbhub_page 改造约定一致，改这里必须同步那边）:
  卡  /p/{fn}/                      （P3 用 _redirects 映射到 cards/{owner}__{repo}.html）
  库  /db/{db-slug}/
  类  /cat/{cat-slug}/{n}.html      （n=1 省略，即 /cat/{cat-slug}/）
  总  /projects/{n}.html            （n=1 省略）
"""
import argparse, datetime, glob, io, json, os, re, sys, time
import xml.etree.ElementTree as ET

VER = "build_site/1.5"   # 1.5：新增对比页数据出口 build_cmp()（site/data/cmp/ 256 分桶，/compare/ 自选对比的富字段：
                          #     综述/亮点/适用场景/能力标签/面向谁/趋势/擂台/提交量等——瘦索引只有 15 键装不下，单独出口）；
                          # 1.4：部署口径 A（用户裁定 11-21）——站内只部署归属过（dbs 非空）的卡，未归属不删源待归属补证自动回站；
                          # 1.3：light() 增 mnt/off/sec/ai/created/pushed/relpub（P9 站点浏览「属性」筛选/排序字段）；
                          # 1.2：light() 增 dbs（站点旧版排版复刻需要：清单「库」列 + 冠军矩阵通用标记）；1.1：补 urls.json 契约出口
ROOT = os.path.dirname(os.path.abspath(__file__))
PAGE = 100
TODAY = datetime.date.today()

# v4 ai_kind 的 AI 取值（与 lib/interp_read.AI_KINDS 同源；跨仓不 import，两处各写一份并注释）
AI_KINDS = frozenset(("mcp", "rag", "text2sql", "dba-agent"))
STALE_DAYS = 180        # 疑似停维：pushed_at 距生成日 >180 天（与 gen_card 擂台停更口径同源）

def now(): return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
def loadj(p): return json.load(io.open(p, encoding="utf-8"))
def dumpj(obj, p):
    io.open(p, "w", encoding="utf-8", newline="\n").write(json.dumps(obj, ensure_ascii=False))
    return os.path.getsize(p)

def slugify(name):
    """PostgreSQL->postgresql；SQL Server->sql-server。小写、非字母数字折叠成单 -、去首尾。
    中文类目名会折叠成空（->misc）——类目一律走 CAT_SLUG 显式映射，绝不裸用本函数。"""
    s = re.sub(r"[^a-z0-9]+", "-", str(name).lower()).strip("-")
    return s or "misc"

CAT_SLUG = {  # 类目中文->URL slug（SEO 用英文；新增类目必须补这里，防撞断言会拦）
    "开发库": "library", "内核/引擎": "engine", "管理": "management", "迁移": "migration",
    "平台": "platform", "连接/代理": "connector", "监控": "monitoring", "测试/质量": "testing",
    "安全/审计": "security", "备份": "backup", "建模/设计": "modeling", "高可用": "ha", "综合": "misc",
}

def cat_slug(cat):
    s = CAT_SLUG.get(cat) or slugify(cat)
    assert s != "misc" or cat in ("综合", "未分类"), f"类目撞车: {cat!r} -> misc"
    return s

def hostile(fn):
    """Windows 不可建目录的仓名（段尾点/尾空格，如 frank-z7/opengauss-batman.）——站点不部署。
    与 dbhub_page/gen/cards.py 的判定保持同步（跨仓不 import，两处各写一份并注释）。"""
    return any(s != s.rstrip(". ") for s in fn.split("/"))

def deployable(r):
    """P9.7 口径 A（用户裁定 11-21）：站内只部署归属过（dbs 非空）的卡——redis/duckdb/etcd 等
    17 库外引擎与归属漏判工具一律不进清单/类目/卡页/sitemap；源卡不删，归属引擎补上证据即自动回站
    （gen 侧周刊钉住的例外归 weekly/issues 白名单管，见 cards.py）。"""
    return bool(r.get("dbs"))

def cat_of(r):
    return ((r.get("judge") or {}).get("cat")) or ((r.get("desc") or {}).get("cat"))

def one_liner(r):
    return ((r.get("text") or {}).get("one_liner") or (r.get("desc") or {}).get("one_liner") or "").strip()

def mnt_of(r, today=TODAY):
    """维护三态：archived -> gone（弃用/归档）；pushed_at 距 today ≥180 天 -> stale（疑似停维）；else ok。
    天数边界与 gen_card.stale_marker 同口径（days>=180 即停更，勿写 >180 差一天）；无/坏日期按 ok
    （宁松勿误杀）。today 参数供 selftest 定日。"""
    if r.get("archived"): return "gone"
    p = str(r.get("pushed_at") or "")[:10]
    try: d = datetime.date.fromisoformat(p)
    except ValueError: return "ok"
    return "stale" if (today - d).days >= STALE_DAYS else "ok"

def light(fn, r):
    """列表分片轻字段：够列表页渲染即可，严禁整卡拷贝（卡 JSON 有 _fp 等内部字段，且体积失控）。
    dbs=适配库名单全量不截（P8 组合页成员口径：一卡多库须进全部分属组合；曾截前 6 致 dbeaver
    这类多库工具缺席第 7 库起的组合页，+N 徽标也变假数）；展示层截断归渲染端 db_tags 的 [:3]+N。
    P9 增七字段（浏览筛选/排序）：mnt=维护三态(off 见 official)、off=官方 1/0（build_cache 按
    db_profiles orgs 名单判定）、sec=有安全通告 1/0（enrich sec_n>0，宽于旧版「高危」——severity
    已不在管线，勿按高危口径宣传）、ai=AI 项目 1/0（ai_kind 四类）、created/pushed/relpub=排序日期源。"""
    en = r.get("enrich") or {}
    return {"fn": fn, "name": (fn.split("/")[-1] if "/" in fn else fn),
            "stars": r.get("stars"), "lang": r.get("language"), "cat": cat_of(r),
            "dbs": r.get("dbs") or [],
            "ol": one_liner(r)[:120], "url": f"/p/{fn}/",
            "mnt": mnt_of(r), "off": 1 if r.get("official") else 0,
            "sec": 1 if (en.get("sec_n") or 0) > 0 else 0,
            "ai": 1 if (r.get("judge") or {}).get("ai_kind") in AI_KINDS else 0,
            "created": r.get("created_at"), "pushed": r.get("pushed_at"),
            "relpub": en.get("rel_pub")}

def paged(items, page=PAGE):
    return [items[i:i + page] for i in range(0, len(items), page)] or [[]]

def site_base():
    b = os.environ.get("DBHUB_SITE_BASE", "").rstrip("/")
    if not b:
        print("WARN DBHUB_SITE_BASE 未设置，sitemap 用占位域名 https://dbhub.example.com（部署时注入再重出）")
        b = "https://dbhub.example.com"
    return b

# ---------- ① 类目分页 + 全站总览 + 库页 ----------

def build_lists(site):
    t0 = time.time(); idx = loadj(ROOT + "/cache/index.json")["repos"]
    man = loadj(ROOT + "/cards/manifest.json")["cards"]
    miss = [fn for fn in man if fn not in idx]
    assert not miss, f"index 缺活跃仓 {len(miss)} 个，样例 {miss[:3]}"
    items = [light(fn, idx[fn]) for fn in man if deployable(idx[fn])]   # P9.7 口径 A：未归属不部署
    n_unattr = len(man) - len(items)
    skp = sorted(fn for fn in man if hostile(fn))
    if skp: print(f"SKIP 站点不部署 {len(skp)} 个 Windows 敌对仓名: {skp[:3]}")
    items = [it for it in items if not hostile(it["fn"])]
    os.makedirs(site + "/data/cat", exist_ok=True); os.makedirs(site + "/data/db", exist_ok=True)
    for f in glob.glob(site + "/data/all-*.json") + glob.glob(site + "/data/cat/*.json"):
        os.remove(f)     # 全量重写前清场（P9.7 坑：分页数收缩——如 140→114 页——旧尾部分片残留会被 gen 读成新旧混合）
    n_urls = 0; n_files = 0; total = 0
    by_cat = {}
    for it in items:
        by_cat.setdefault(it["cat"] or "综合", []).append(it)
    for cat, lst in sorted(by_cat.items()):
        lst.sort(key=lambda x: (-(x["stars"] or 0), x["fn"]))
        slug = cat_slug(cat)
        assert len({cat_slug(c) for c in by_cat}) == len(by_cat), "类目 slug 有撞车"
        pages = paged(lst)
        for i, pg in enumerate(pages, 1):
            dumpj({"cat": cat, "slug": slug, "page": i, "pages": len(pages), "items": pg},
                  f"{site}/data/cat/{slug}-{i}.json"); n_files += 1
        total += len(lst); n_urls += len(pages)
    pages = paged(sorted(items, key=lambda x: (-(x["stars"] or 0), x["fn"])))
    for i, pg in enumerate(pages, 1):
        dumpj({"cat": "全部", "slug": "all", "page": i, "pages": len(pages), "items": pg},
              f"{site}/data/all-{i}.json"); n_files += 1
    n_urls += len(pages)
    dbs = {}
    for it in items:                                    # 库页：卡适配库聚合（一卡可属多库，跨库不去重）
        r = idx[it["fn"]]
        for d in (r.get("dbs") or []):
            dbs.setdefault(d, []).append(it)
    for d, lst in sorted(dbs.items(), key=lambda x: -len(x[1])):
        lst.sort(key=lambda x: (-(x["stars"] or 0), x["fn"]))
        dumpj({"db": d, "slug": slugify(d), "count": len(lst), "items": lst[:500]},
              f"{site}/data/db/{slugify(d)}.json"); n_files += 1   # 库页封顶 500 热门，长尾走类目页
    assert total == len(items), f"类目分片总数 {total} != 活跃 {len(items)}（一卡多类目=分组 bug）"
    print(f"OK lists: 活跃={len(items)}（未归属不部署 {n_unattr}） 类目={len(by_cat)} 分片文件={n_files} "
          f"库页={len(dbs)} -> site/data in {time.time()-t0:.1f}s")
    return {"cats": by_cat, "pages_all": len(pages), "n_urls": n_urls, "items": items, "dbs": dbs}

# ---------- ①b 对比页数据（vs） ----------

def vs_slug(pair):
    """(fnA, fnB) -> /vs/ 用 slug：owner__repo--owner__repo。理论上仓名含 -- 会歧义，撞车检测兜底（罕见对直接弃）。"""
    return pair[0].replace("/", "__") + "--" + pair[1].replace("/", "__")

VS_HERO_STARS = 1000   # 对比页只做热门主角（长尾主角的对比页搜索量撑不起）

def build_vs(site):
    """主角 ≥1000★ 且擂台有 ≥0.6 候选 -> 取首位候选成对（无序去重，星数高者为 a）。
    数据源=活跃卡 JSON 的 arena.rows（读 1.4 万卡 JSON 约 10s，值这批高转化对比词页面）。"""
    t0 = time.time()
    idx = loadj(ROOT + "/cache/index.json")["repos"]
    man = loadj(ROOT + "/cards/manifest.json")["cards"]
    cards_dir = os.path.join(ROOT, "cards")
    by_slug = {}; dropped = []; n_hero = 0; n_rival_out = 0
    for fn in sorted(man):
        p = os.path.join(cards_dir, fn.replace("/", "__") + ".json")
        if not os.path.exists(p): continue
        try: c = json.load(io.open(p, encoding="utf-8"))
        except Exception: continue
        b = c.get("basics") or {}
        if (b.get("stars") or 0) < VS_HERO_STARS: continue
        if not deployable(idx.get(fn, {})): continue            # P9.7：未归属主角不部署 -> 不出对比页
        rows = (c.get("arena") or {}).get("rows") or []
        hero = next((r for r in rows if r.get("me")), None)
        rival = next((r for r in rows if not r.get("me") and (r.get("score") or 0) >= 0.6), None)
        if not hero or not rival: continue
        if rival["fn"] not in man or hostile(rival["fn"]) or not deployable(idx.get(rival["fn"], {})):
            n_rival_out += 1; continue          # 对手是归档/敌对名/未归属仓 -> 无 /p/ 页可链，弃对（内链 404 会被 gen VERIFY 拦）
        n_hero += 1
        pair = tuple(sorted([fn, rival["fn"]], key=lambda x: (-(idx.get(x, {}).get("stars") or 0), x)))
        slug = vs_slug(pair)
        if slug in by_slug and tuple(by_slug[slug]["pair"]) != pair:   # list!=tuple 恒真，须同型比较
            dropped.append(slug); continue
        a, bfn = pair
        A, B = idx.get(a, {}), idx.get(bfn, {})
        ha = next((r for r in rows if r.get("fn") == a), None) or {}
        hb = next((r for r in rows if r.get("fn") == bfn), None) or {}
        by_slug[slug] = {"pair": list(pair), "a": light(a, A), "b": light(bfn, B),
                         "a_score": (ha.get("score")), "a_why": (ha.get("why") or "")[:200],
                         "b_score": (hb.get("score")), "b_why": (hb.get("why") or "")[:200],
                         "algo": (c.get("arena") or {}).get("sub", "")}
    os.makedirs(site + "/data/vs", exist_ok=True)
    for f in os.listdir(site + "/data/vs"):
        os.remove(os.path.join(site + "/data/vs", f))          # 全量重写前清旧（弃用的对不留死链数据）
    for slug, d in sorted(by_slug.items()):
        d.pop("pair")
        dumpj(d, f"{site}/data/vs/{slug}.json")
    print(f"OK vs: 主角≥{VS_HERO_STARS}★ 且有对手 {n_hero}（对手不部署弃 {n_rival_out}）-> 去重后 {len(by_slug)} 对"
          + (f"（撞车弃 {len(set(dropped))}）" if dropped else "")
          + f" -> site/data/vs in {time.time()-t0:.1f}s")
    return len(by_slug)

# ---------- ①c 对比页数据（cmp：/compare/ 自选对比的富字段） ----------

CMP_BUCKETS = 256
CMP_VER = "cmp/1.0"

def cmp_bucket(fn):
    """分桶号（两位十六进制）：FNV-1a 32 位，按 UTF-16 码元逐个异或再乘质数，取低字节。
    与 dbhub_page assets/compare.js 的 bucket() 逐位同式（跨仓不 import，两处各写一份并注释；
    标准向量断言在两侧 selftest，全量一致性由 gen verify 的「fn 落在算出的桶里」对账兜底）。"""
    h, b = 0x811C9DC5, fn.encode("utf-16-le")
    for i in range(0, len(b), 2):
        h = ((h ^ (b[i] | (b[i + 1] << 8))) * 0x01000193) & 0xFFFFFFFF
    return format(h & 0xFF, "02x")

def rich(fn, r, card, mentions=0):
    """/compare/ 富字段（cmp/1.0）。瘦索引 15 键之外、对比页要并排的全部解读与信号：解读层走索引
    （judge/text/tags，与项目卡同源），趋势/擂台/动态走卡 JSON。缺=None/[]，前端按「无数据 / 未解读」展示。
    能力标签只出 high/mid（同卡面口径，low 不上）；许可证 NOASSERTION=未声明 -> None。"""
    j, t, en = r.get("judge") or {}, r.get("text") or {}, r.get("enrich") or {}
    news = (((card.get("news") or {}).get("items") or [{}])[0] or {})
    pts = [p for p in ((card.get("trend") or {}).get("points") or [])
           if isinstance(p, (list, tuple)) and len(p) == 2 and isinstance(p[1], int)]
    lic = r.get("license")
    return {
        "aik": j.get("ai_kind"), "cf": j.get("conf"),
        "pe": j.get("persona") or [], "eco": j.get("eco"), "ct": j.get("cat_tags") or [],
        "ins": j.get("install") or [],
        "rv": (t.get("review") or "").strip()[:600] or None,
        "hl": [str(x)[:300] for x in (t.get("highlights") or []) if x][:6],
        "uc": [str(x)[:300] for x in (t.get("use_cases") or []) if x][:6],
        "cap": [[x[1], x[2]] for x in (r.get("tags") or []) if len(x) >= 3 and x[2] in ("high", "mid")],
        "lic": lic if lic and lic != "NOASSERTION" else None,
        "sec": en.get("sec_n") or 0,
        "ver": re.sub(r"^(release/|v)", "", en.get("rel_ver") or "") or None,
        "vpub": (en.get("rel_pub") or "")[:10] or None, "n90": en.get("rel_n90"),
        "c90": en.get("commit_90d"), "ctr": en.get("contrib_n"),
        "mts": mentions if isinstance(mentions, int) else 0,
        "tr": [p[1] for p in pts], "td0": str(pts[0][0])[:10] if pts else None, "td1": str(pts[-1][0])[:10] if pts else None,
        "ar": [[x.get("fn"), x.get("score")] for x in ((card.get("arena") or {}).get("rows") or []) if not x.get("me") and x.get("fn")],
        "nw": [news.get("ver"), news.get("date"), (news.get("story") or "")[:220]] if news.get("ver") else None,
        "rm": (r.get("readme0") or "")[:300] or None,
    }

def dumpc(obj, p):
    io.open(p, "w", encoding="utf-8", newline="\n").write(json.dumps(obj, ensure_ascii=False, separators=(",", ":")))
    return os.path.getsize(p)

def build_cmp(site):
    """对比页富字段 256 分桶。部署集与 lists 同口径（deployable + 非敌对名）；浏览器按 fn 算桶号、
    每次对比只取 2 个小文件。gen 侧 verify 对账「桶内条数 == all 分片条数」。"""
    t0 = time.time()
    idx = loadj(ROOT + "/cache/index.json")["repos"]
    man = loadj(ROOT + "/cards/manifest.json")["cards"]
    mp = ROOT + "/cache/mentions.json"
    mcounts = (loadj(mp).get("counts") or {}) if os.path.exists(mp) else {}
    buckets = [{} for _ in range(CMP_BUCKETS)]; n_card = 0
    for fn in sorted(man):
        if fn not in idx or hostile(fn) or not deployable(idx[fn]): continue
        p = os.path.join(ROOT, "cards", fn.replace("/", "__") + ".json")
        card = {}
        if os.path.exists(p):
            try: card = loadj(p); n_card += 1
            except Exception: card = {}
        buckets[int(cmp_bucket(fn), 16)][fn] = rich(fn, idx[fn], card, mcounts.get(fn))
    d = os.path.join(site, "data", "cmp"); os.makedirs(d, exist_ok=True)
    for f in os.listdir(d): os.remove(os.path.join(d, f))       # 清场：条目换桶后旧桶文件不留
    size = sum(dumpc({"asof": TODAY.isoformat(), "ver": CMP_VER, "items": b}, f"{d}/{i:02x}.json")
               for i, b in enumerate(buckets))
    n = sum(len(b) for b in buckets)
    assert n == sum(1 for fn in man if fn in idx and not hostile(fn) and deployable(idx[fn])), "cmp 条数 != 部署集"
    print(f"OK cmp: 部署集 {n} 条（读到卡 {n_card}）-> {CMP_BUCKETS} 桶 {size//1024//1024}.{(size//1024)%1000:03d} MB "
          f"均 {size//max(n,1)} B/条 -> site/data/cmp in {time.time()-t0:.1f}s")
    return n

# ---------- ② sitemap ----------

def build_sitemap(site):
    t0 = time.time(); base = site_base(); ct_vs = "/vs/{slug}/"
    idx = loadj(ROOT + "/cache/index.json")["repos"]
    man = loadj(ROOT + "/cards/manifest.json")["cards"]
    items = [light(fn, idx[fn]) for fn in man if fn in idx and not hostile(fn)
             and deployable(idx[fn])]                          # P9.7：未归属卡不进 sitemap（卡页不部署）
    by_cat = {}
    for it in items: by_cat.setdefault(it["cat"] or "综合", []).append(it)
    urls = ["/", "/projects/"] + [f"/db/{slugify(d)}/" for d in
                                  {d for fn in man if fn in idx for d in (idx[fn].get("dbs") or [])}]
    for cat, lst in by_cat.items():
        slug = cat_slug(cat)
        urls += [f"/cat/{slug}/"] + [f"/cat/{slug}/{i}.html" for i in range(2, len(paged(lst)) + 1)]
    assert len(set(urls)) == len(urls), "sitemap 有重复 URL（slug 撞车）"
    urls += [it["url"] for it in items]
    vs_dir = os.path.join(site, "data", "vs")            # 对比页（vs 步骤产物在即并入）
    if os.path.isdir(vs_dir):
        urls += [ct_vs.format(slug=f[:-5]) for f in os.listdir(vs_dir) if f.endswith(".json")]
    lastmod = datetime.date.today().isoformat()
    root = ET.Element("urlset", {"xmlns": "http://www.sitemaps.org/schemas/sitemap/0.9"})
    for u in urls:
        e = ET.SubElement(root, "url")
        ET.SubElement(e, "loc").text = base + u
        ET.SubElement(e, "lastmod").text = lastmod
    ET.indent(root) if hasattr(ET, "indent") else None
    xml = ET.tostring(root, encoding="unicode", xml_declaration=False)
    p = site + "/sitemap.xml"
    io.open(p, "w", encoding="utf-8", newline="\n").write('<?xml version="1.0" encoding="UTF-8"?>\n' + xml + "\n")
    ET.parse(p)                                          # 落盘后真解析一遍（自证 XML 合法）
    print(f"OK sitemap: urls={len(urls)}（首页/总览/库页/类目/卡）base={base} -> {os.path.getsize(p)//1024} KB in {time.time()-t0:.1f}s")
    return len(urls)

# ---------- ③ robots ----------

def build_robots(site):
    base = site_base()
    txt = f"User-agent: *\nAllow: /\n\nSitemap: {base}/sitemap.xml\n"
    io.open(site + "/robots.txt", "w", encoding="utf-8", newline="\n").write(txt)
    urls = {"base": base, "card": "/p/{fn}/", "db": "/db/{slug}/", "vs": "/vs/{slug}/",
            "cat_first": "/cat/{slug}/", "cat_page": "/cat/{slug}/{n}.html",
            "all_first": "/projects/", "all_page": "/projects/{n}.html",
            "vs_first": "/vs/{slug}/",
            "note": "改模式须同步 gen_card seo_head canonical 与 dbhub_page gen；build --verify 交叉比对"}
    dumpj(urls, site + "/urls.json")
    print(f"OK robots: Allow / + Sitemap 指针 -> {len(txt)} B；urls.json 契约已出")
    return txt

# ---------- 自检 ----------

def _selftest():
    assert slugify("PostgreSQL") == "postgresql" and slugify("SQL Server") == "sql-server"
    assert slugify("测试/质量") == "misc" and slugify("") == "misc"
    assert paged([]) == [[]] and [len(p) for p in paged(list(range(255)))] == [100, 100, 55]
    assert [len(p) for p in paged(list(range(100)))] == [100]
    r = {"stars": 9, "language": "Go", "judge": {"cat": "备份"}, "dbs": ["PostgreSQL"],
         "text": {"one_liner": "x" * 200}}
    it = light("a/b", r)
    assert it == {"fn": "a/b", "name": "b", "stars": 9, "lang": "Go", "cat": "备份",
                  "dbs": ["PostgreSQL"], "ol": "x" * 120, "url": "/p/a/b/",
                  "mnt": "ok", "off": 0, "sec": 0, "ai": 0,
                  "created": None, "pushed": None, "relpub": None}     # P9 七字段缺省安全
    T = datetime.date(2026, 11, 21)
    assert mnt_of({"archived": True}, T) == "gone"
    assert mnt_of({"archived": True, "pushed_at": "2026-11-20"}, T) == "gone"   # archived 优先
    assert mnt_of({"pushed_at": "2026-01-01"}, T) == "stale"                    # 324 天 ≥ 180
    assert mnt_of({"pushed_at": str(T - datetime.timedelta(days=180))}, T) == "stale"   # 恰 180 天也算（同 gen_card）
    assert mnt_of({"pushed_at": str(T - datetime.timedelta(days=179))}, T) == "ok"      # 179 天不算
    assert mnt_of({"pushed_at": "2026-11-15T10:30:00Z"}, T) == "ok"             # datetime 形态取前 10 位
    assert mnt_of({}, T) == "ok" and mnt_of({"pushed_at": "bad"}, T) == "ok"    # 无/坏日期按 ok
    r9 = {"judge": {"cat": "管理", "ai_kind": "mcp"}, "official": True,
          "enrich": {"sec_n": 2, "rel_pub": "2026-11-01"}, "pushed_at": "2020-01-01",
          "created_at": "2015-10-21"}
    it9 = light("p/q", r9)
    assert (it9["ai"], it9["off"], it9["sec"], it9["mnt"]) == (1, 1, 1, "stale")
    assert (it9["relpub"], it9["created"], it9["pushed"]) == ("2026-11-01", "2015-10-21", "2020-01-01")
    assert light("r/s", {"judge": {"cat": "备份", "ai_kind": "other"},
                         "enrich": {"sec_n": 0}})["ai"] == 0                    # other=非 AI
    assert light("c/d", {"desc": {"cat": "管理", "one_liner": "y"}})["cat"] == "管理"
    assert light("e/f", {})["cat"] is None and light("e/f", {})["ol"] == ""   # 空仓安全
    assert slugify("内核/引擎") == "misc" and slugify("YashanDB") == "yashandb"
    assert cat_slug("备份") == "backup" and cat_slug("综合") == "misc" and cat_slug("内核/引擎") == "engine"
    assert len(set(CAT_SLUG.values())) == len(CAT_SLUG), "映射表自身有撞车"
    assert f"/db/{slugify('SQL Server')}/" == "/db/sql-server/"               # 库页 URL 形
    assert hostile("a/b.") and hostile("a./b") and not hostile("a/b") and not hostile("a/b_c")
    u = {"card": "/p/{fn}/", "db": "/db/{slug}/", "cat_page": "/cat/{slug}/{n}.html", "vs": "/vs/{slug}/"}
    assert vs_slug(("a/b", "c/d")) == "a__b--c__d"                     # vs slug 无歧义拼接
    assert u["card"].format(fn="a/b") == "/p/a/b/" and u["db"].format(slug="x") == "/db/x/"  # 契约模式可格式化
    # 1.5 对比页数据出口：分桶函数（FNV-1a 32 标准向量的低字节，与 compare.js 同式）+ 富字段装配
    assert cmp_bucket("") == "c5" and cmp_bucket("a") == "2c" and cmp_bucket("foobar") == "68"
    assert cmp_bucket("o/r") == cmp_bucket("o/r") and len(cmp_bucket("中文/仓")) == 2     # 非 ASCII 走 UTF-16 码元，仍两位
    assert len({cmp_bucket(f"o/r{i}") for i in range(400)}) > 200                          # 分布够散，不挤少数桶
    rr = rich("a/b", {"judge": {"persona": ["ops"], "eco": "tool", "cat_tags": ["高可用"], "conf": "high",
                                "ai_kind": "other", "install": ["source"]},
                      "text": {"review": " 综述 ", "highlights": ["h1", "h2"], "use_cases": []},
                      "tags": [["backup", "备份", "high"], ["orm", "ORM", "low"], ["x", "x"]],
                      "license": "NOASSERTION", "readme0": "rm",
                      "enrich": {"sec_n": 2, "rel_ver": "release/2.60.1", "rel_pub": "2026-11-16", "rel_n90": 4,
                                 "commit_90d": 107, "contrib_n": 66}},
                {"trend": {"points": [["2026-10-18", 4448], ["2026-11-22", 4503], ["bad", "x"]]},
                 "arena": {"rows": [{"fn": "a/b", "me": True, "score": 1.0}, {"fn": "c/d", "score": 0.7}]},
                 "news": {"items": [{"ver": "2.60.1", "date": "2026-11-16", "story": "s"}]}}, mentions=3)
    assert rr["rv"] == "综述" and rr["hl"] == ["h1", "h2"] and rr["uc"] == []
    assert rr["cap"] == [["备份", "high"]]                 # 仅 high/mid，low 与残缺条目不出
    assert rr["lic"] is None and rr["sec"] == 2 and (rr["ver"], rr["vpub"], rr["n90"]) == ("2.60.1", "2026-11-16", 4)
    assert rr["tr"] == [4448, 4503] and (rr["td0"], rr["td1"]) == ("2026-10-18", "2026-11-22")   # 坏点剔除
    assert rr["ar"] == [["c/d", 0.7]] and rr["nw"] == ["2.60.1", "2026-11-16", "s"] and rr["mts"] == 3
    assert rr["pe"] == ["ops"] and rr["ct"] == ["高可用"] and rr["ins"] == ["source"] and rr["cf"] == "high"
    assert rich("p/q", {"license": "GPL-3.0"}, {}, None)["lic"] == "GPL-3.0"
    r0 = rich("x/y", {}, {}, None)                          # 空仓全缺省安全
    assert r0["rv"] is None and r0["hl"] == [] and r0["cap"] == [] and r0["tr"] == [] and r0["ar"] == []
    assert r0["nw"] is None and r0["mts"] == 0 and r0["pe"] == [] and r0["lic"] is None and r0["c90"] is None
    print("OK build_site selftest: 36 asserts passed")
    return 0

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--steps", default="all", help="all | lists,vs,cmp,sitemap,robots 逗号分隔")
    p.add_argument("--out", default="site", help="输出目录（相对运行位）")
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.selftest: sys.exit(_selftest())
    site = os.path.join(ROOT, a.out); os.makedirs(site, exist_ok=True)
    steps = a.steps.split(",")
    for s in (steps if "all" not in steps else ["lists", "vs", "cmp", "sitemap", "robots"]):
        {"lists": lambda: build_lists(site), "vs": lambda: build_vs(site), "cmp": lambda: build_cmp(site),
         "sitemap": lambda: build_sitemap(site),
         "robots": lambda: build_robots(site)}.get(s, lambda: p.error(f"unknown step {s}"))()

if __name__ == "__main__":
    main()
