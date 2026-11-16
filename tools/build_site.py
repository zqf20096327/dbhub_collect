# -*- coding: utf-8 -*-
"""build_site.py v1.0 -- 站点数据出口（P2：卡片不动，只产列表分片/库页数据/sitemap/robots）

用法:
  python -I build_site.py                     # 全部步骤（lists+vs+sitemap+robots）
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
  sitemap.xml                 首页 + 17 库页 + 类目分页 + 全部活跃卡（单文件 <5 万 URL）
  robots.txt                  放行全部 + 指向 sitemap

URL 规范（与 P3 dbhub_page 改造约定一致，改这里必须同步那边）:
  卡  /p/{fn}/                      （P3 用 _redirects 映射到 cards/{owner}__{repo}.html）
  库  /db/{db-slug}/
  类  /cat/{cat-slug}/{n}.html      （n=1 省略，即 /cat/{cat-slug}/）
  总  /projects/{n}.html            （n=1 省略）
"""
import argparse, datetime, io, json, os, re, sys, time
import xml.etree.ElementTree as ET

VER = "build_site/1.1"   # 1.1：补 urls.json URL 契约出口（站点侧唯一权威，防 gen_card canonical/sitemap/站点页三处漂移）
ROOT = os.path.dirname(os.path.abspath(__file__))
PAGE = 100

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

def cat_of(r):
    return ((r.get("judge") or {}).get("cat")) or ((r.get("desc") or {}).get("cat"))

def one_liner(r):
    return ((r.get("text") or {}).get("one_liner") or (r.get("desc") or {}).get("one_liner") or "").strip()

def light(fn, r):
    """列表分片轻字段：够列表页渲染即可，严禁整卡拷贝（卡 JSON 有 _fp 等内部字段，且体积失控）。"""
    return {"fn": fn, "name": (fn.split("/")[-1] if "/" in fn else fn),
            "stars": r.get("stars"), "lang": r.get("language"), "cat": cat_of(r),
            "ol": one_liner(r)[:120], "url": f"/p/{fn}/"}

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
    items = [light(fn, idx[fn]) for fn in man if fn in idx]
    assert len(items) == len(man), f"index 缺活跃仓 {len(man) - len(items)} 个"
    skp = sorted(fn for fn in man if hostile(fn))
    if skp: print(f"SKIP 站点不部署 {len(skp)} 个 Windows 敌对仓名: {skp[:3]}")
    items = [it for it in items if not hostile(it["fn"])]
    os.makedirs(site + "/data/cat", exist_ok=True); os.makedirs(site + "/data/db", exist_ok=True)
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
    print(f"OK lists: 活跃={len(items)} 类目={len(by_cat)} 分片文件={n_files} "
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
        rows = (c.get("arena") or {}).get("rows") or []
        hero = next((r for r in rows if r.get("me")), None)
        rival = next((r for r in rows if not r.get("me") and (r.get("score") or 0) >= 0.6), None)
        if not hero or not rival: continue
        if rival["fn"] not in man or hostile(rival["fn"]):
            n_rival_out += 1; continue          # 对手是归档/敌对名仓 -> 无 /p/ 页可链，弃对（内链 404 会被 gen VERIFY 拦）
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

# ---------- ② sitemap ----------

def build_sitemap(site):
    t0 = time.time(); base = site_base(); ct_vs = "/vs/{slug}/"
    idx = loadj(ROOT + "/cache/index.json")["repos"]
    man = loadj(ROOT + "/cards/manifest.json")["cards"]
    items = [light(fn, idx[fn]) for fn in man if fn in idx and not hostile(fn)]
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
    r = {"stars": 9, "language": "Go", "judge": {"cat": "备份"},
         "text": {"one_liner": "x" * 200}}
    it = light("a/b", r)
    assert it == {"fn": "a/b", "name": "b", "stars": 9, "lang": "Go", "cat": "备份",
                  "ol": "x" * 120, "url": "/p/a/b/"}
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
    print("OK build_site selftest: 13 asserts passed")
    return 0

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--steps", default="all", help="all | lists,sitemap,robots 逗号分隔")
    p.add_argument("--out", default="site", help="输出目录（相对运行位）")
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.selftest: sys.exit(_selftest())
    site = os.path.join(ROOT, a.out); os.makedirs(site, exist_ok=True)
    steps = a.steps.split(",")
    for s in (steps if "all" not in steps else ["lists", "vs", "sitemap", "robots"]):
        {"lists": lambda: build_lists(site), "vs": lambda: build_vs(site),
         "sitemap": lambda: build_sitemap(site),
         "robots": lambda: build_robots(site)}.get(s, lambda: p.error(f"unknown step {s}"))()

if __name__ == "__main__":
    main()
