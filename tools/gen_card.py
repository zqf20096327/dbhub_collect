# -*- coding: utf-8 -*-
"""gen_card.py -- 名片底稿 JSON -> 名片 HTML + 名片 JSON（双出口）

用法:
  python -I gen_card.py --card 名片底稿-dbeaver.json --out 名片样卡-dbeaver.html
  python -I gen_card.py --selftest

v1.1（2026-11-12 用户三条指令）:
  1. 每个内容块一个渲染函数，模板零写死数字；
  2. 程序派生三项直接从仓内数据算:
     - 擂台停更标记: pool.pushed_at 距生成日 >180 天 -> 简介后追加「· N 年/月未更」
     - README 提及数: 查 cache/mentions.json（build_cache 每日 slug(owner/repo) 整串扫描，排除本仓与同 org，仅计池内）
     - 项目年龄: pool.created_at -> 头部 meta 追加「创建于 YYYY」
  3. 生成 HTML 的同时写同名 .json（底稿+derived），供后续建站使用。
"""
import argparse, copy, datetime, html, io, json, os, sys

VER = "gen_card/1.5"   # 1.5：简介块渲染综述段（intro.review，一句话之下、亮点之上）
STALE_DAYS = 180
POOL_DEFAULT = "D:/dbhub_collect/data/live/pool.ndjson"

CSS = """  :root{
    --brand:#0F766E; --brand-soft:rgba(15,118,110,.09);
    --ink:#1F2937; --sub:#6B7280; --line:#E5E7EB;
    --hi:#FEF9E3; --code-bg:#1E293B; --code-ink:#E2E8F0;
  }
  *{box-sizing:border-box; margin:0; padding:0;}
  body{
    background:#F8FAFC; color:var(--ink);
    font-family:-apple-system,"Segoe UI","PingFang SC","Microsoft YaHei","Noto Sans SC",sans-serif;
    font-size:16px; line-height:1.7; -webkit-font-smoothing:antialiased;
    padding:24px 16px 48px;
  }
  b, strong{ font-weight:600; }
  .card{ max-width:680px; margin:0 auto; background:#fff; border:1px solid var(--line);
    border-radius:14px; padding:20px 22px; display:flex; flex-direction:column; }
  .c-top{ display:flex; align-items:center; gap:8px; flex-wrap:wrap; }
  .chip{ font-size:12.5px; font-weight:600; color:var(--brand); background:var(--brand-soft);
    padding:3px 8px; border-radius:4px; }
  .chip.sub{ color:var(--sub); background:transparent; border:1px solid var(--line); font-weight:400; }
  .c-no{ margin-left:auto; font-size:12.5px; color:var(--sub); font-variant-numeric:tabular-nums; }
  .c-body{ display:flex; gap:22px; margin-top:16px; align-items:center; }
  .c-left{ flex:1.5; min-width:0; }
  .c-title{ font-size:28px; font-weight:600; letter-spacing:-0.3px; line-height:1.15; }
  a.c-title{ color:var(--ink); text-decoration:none; }
  a.c-title:hover{ color:var(--brand); }
  .pts-label{ margin-top:8px; font-size:12.5px; font-weight:600; color:var(--ink); }
  .c-anchor{ font-size:12.5px; color:var(--sub); margin-top:6px; }
  .c-anchor b{ color:var(--ink); }
  .c-meta{ margin-top:6px; font-size:12.5px; color:var(--sub);
    display:flex; flex-wrap:wrap; row-gap:2px; line-height:1.5; }
  .c-meta span{ white-space:nowrap; }
  .c-meta span:not(:last-child)::after{ content:"\\00b7"; margin:0 6px; color:#D1D5DB; }
  .c-right{ flex:1; display:flex; flex-direction:column; align-items:flex-end; min-width:0; }
  .c-star{ font-size:28px; font-weight:600; line-height:1; font-variant-numeric:tabular-nums; }
  .c-star .u{ font-size:16px; color:var(--brand); margin-left:2px; }
  .spk{ width:100%; height:auto; display:block; margin-top:10px; }
  .sec{ margin-top:24px; }
  .t-head{ display:flex; justify-content:space-between; align-items:baseline; margin-bottom:10px;
    padding-bottom:8px; border-bottom:1px solid var(--line); }
  .t-title{ font-size:16px; font-weight:600; }
  .t-sub{ font-size:12.5px; color:var(--sub); }
  p{ margin-top:10px; font-size:15px; }
  p.pain{ color:var(--sub); }
  p.pain b{ color:var(--ink); }
  table.t{ width:100%; border-collapse:collapse; font-size:13px; }
  table.t th{ background:var(--brand); color:#fff; text-align:left; padding:8px 10px; font-weight:600; }
  table.t th.stars{ text-align:right; }
  table.t td{ padding:8px 10px; border-bottom:1px solid var(--line); }
  table.t tr:last-child td{ border-bottom:none; }
  table.t tr.me td{ background:var(--hi); font-weight:600; }
  table.t tr.me td:first-child{ border-left:3px solid var(--brand); }
  table.t td.stars{ text-align:right; font-weight:600; font-variant-numeric:tabular-nums; }
  table.t td a{ color:var(--ink); text-decoration:none; border-bottom:1px solid var(--brand); }
  table.t td a:hover{ color:var(--brand); }
  .verdict{ margin-top:4px; display:grid; gap:10px; }
  .v-item{ border:1px solid var(--line); border-radius:10px; padding:11px 13px; font-size:15px; }
  .v-item .t{ font-size:12.5px; font-weight:600; margin-bottom:3px; }
  pre{ background:var(--code-bg); color:var(--code-ink); border-radius:8px;
    padding:13px 15px; margin-top:4px; overflow-x:auto; font-size:13px; line-height:1.6; }
  code{ font-family:ui-monospace,Consolas,"Courier New",monospace; }
  .users{ margin-top:4px; display:grid; gap:8px; }
  .user{ font-size:15px; padding-left:12px; border-left:3px solid var(--brand-soft); }
  ul.pts{ margin-top:8px; padding-left:18px; font-size:14px; color:var(--sub); }
  ul.pts li{ margin-top:4px; }
  @media (max-width:600px){
    .card{ padding:16px; }
    .c-body{ flex-direction:column; align-items:stretch; }
    .c-right{ align-items:flex-start; }
  }
"""

# ---------- 数据派生（程序算，不手填） ----------

def parse_date(s):
    return datetime.date.fromisoformat(str(s)[:10])

def stale_marker(pushed_at, run_date, threshold=STALE_DAYS):
    """>180 天未提交 -> '· N 年未更' / '· N 月未更'；否则空。"""
    if not pushed_at: return ""
    try: days = (run_date - parse_date(pushed_at)).days
    except Exception: return ""
    if days < threshold: return ""
    if days >= 365: return f"· {days // 365} 年未更"
    return f"· {days // 30} 个月未更"

def mention_line(count, corpus, run_date):
    return f"被池内 {count} 个其他项目的 README 以 owner/repo 引用（{corpus} 篇全量扫描，截至 {run_date}）"

def load_pool(path):
    """fn(小写) -> {stars, pushed_at, created_at}"""
    m = {}
    for line in io.open(path, encoding="utf-8"):
        try:
            r = json.loads(line)
            fn = r.get("full_name", "")
            if fn: m[fn.lower()] = {"stars": r.get("stars"), "pushed_at": r.get("pushed_at"),
                                    "created_at": r.get("created_at")}
        except Exception:
            pass
    return m

def load_mentions_cache(path):
    """读 build_cache 产物 cache/mentions.json：提及数唯一来源（slug 口径，键=fn），精选卡与档案卡同口径。"""
    m = json.load(io.open(path, encoding="utf-8"))
    return m["counts"], m["meta"]["corpus"], str(m["meta"].get("built_at", ""))[:10]

def enrich(card, pool_map, mentions, run_date):
    """把三项程序派生数据写进卡片副本：停更标记 / README 提及数 /（年龄在 meta 渲染时读 basics）。
    返回的副本既是渲染输入，也是落盘 JSON——网站源数据与卡面天然一致。"""
    c = copy.deepcopy(card)
    hero_fn = c["fn"]
    h = pool_map.get(hero_fn.lower(), {})
    derived = {"gen_ver": VER, "generated_at": run_date, "fn": hero_fn}

    # ① 擂台停更标记
    stale_rows = []
    for r in c.get("arena", {}).get("rows", []):
        p = pool_map.get(r["fn"].lower(), {}).get("pushed_at") or r.get("pushed_at")
        mk = stale_marker(p, parse_date(run_date))
        days = (parse_date(run_date) - parse_date(p)).days if p else None
        r["stop_days"] = days
        r["pushed_at_pool"] = p
        if mk:
            r["why"] = f"{r.get('why', '')} {mk}".strip()
            stale_rows.append({"fn": r["fn"], "stop_days": days, "marker": mk})
    derived["arena_stale"] = stale_rows

    # ② README 提及数 -> 生产采用追加一条（查表 cache/mentions.json，截至戳=缓存建成日）
    if mentions is not None:
        count, corpus, stamp = mentions
        pu = c.setdefault("production_users", {}).setdefault("items", [])
        pu.append({"text": mention_line(count, corpus, stamp), "type": "mention-count",
                   "source": "data/readmes slug(owner/repo) 整串扫描（排除本仓与同 org，仅计池内）"})
        derived["mentions"] = {"count": count, "corpus": corpus, "in_pool_only": True,
                               "excl": "self+same-owner", "scanned_at": stamp,
                               "src": "cache/mentions.json"}

    # ③ 项目年龄
    if h.get("created_at") or c["basics"].get("created_at"):
        year = str(h.get("created_at") or c["basics"]["created_at"])[:4]
        c["basics"]["created_at"] = h.get("created_at") or c["basics"]["created_at"]
        derived["age"] = {"created_year": year,
                          "age_years": parse_date(run_date).year - int(year)}
    c["derived"] = derived
    return c

# ---------- 基础件 ----------

def esc(s): return str(s)
def fmt_stars(n): return f"{n:,}"
def join_text(x): return "；".join(str(i) for i in x) if isinstance(x, list) else str(x)

def meta_items(b):
    lic = b["license"]["display"] if isinstance(b.get("license"), dict) else b.get("license", "")
    v, a = b.get("version", {}), b.get("activity", {})
    items = []
    if b.get("language"): items.append(f"语言 {b['language']}")
    if lic: items.append(f"协议 {lic}")
    if b.get("created_at"): items.append(f"创建于 {str(b['created_at'])[:4]}")
    if v.get("latest"): items.append(f"版本 {v['latest']}")
    if a.get("contributors") is not None: items.append(f"贡献者 {a['contributors']} 人")
    if b.get("pushed_at"): items.append(f"最近提交 {b['pushed_at']}")
    if a.get("commit_90d") is not None: items.append(f"90 天 {a['commit_90d']} commits")
    return items

# ---------- 每块一个渲染函数 ----------

def render_meta(b):
    spans = "".join(f"<span>{esc(i)}</span>" for i in meta_items(b))
    return f'<div class="c-meta">{spans}</div>'

def render_spark(name, pts):
    """x 轴按日期真实间距布点（全量档会有缺日，索引等距会失真）。"""
    if not pts or len(pts) < 2: return ""
    vals = [p[1] for p in pts]
    ds = [parse_date(p[0]) for p in pts]
    span = (ds[-1] - ds[0]).days or 1
    xs = [8 + 244 * ((d - ds[0]).days) / span for d in ds]
    lo, hi = min(vals), max(vals)
    ys = [58 - 48 * (v - lo) / (hi - lo) if hi > lo else 34 for v in vals]
    P = [f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys)]
    area = f"M{xs[0]:.1f},58 " + " ".join(f"L{p}" for p in P) + f" L{xs[-1]:.1f},58 Z"
    d0, d1 = pts[0][0][5:], pts[-1][0][5:]
    return (
        f'<svg class="spk" viewBox="0 0 260 66" role="img" aria-label="{name} star trend {vals[0]} to {vals[-1]}">'
        f'<title>{name} star 趋势（{pts[0][0]} 至 {pts[-1][0]}）</title>'
        f'<desc>由 {vals[0]} 增长至 {vals[-1]}</desc>'
        f'<line x1="8" y1="58" x2="252" y2="58" stroke="#E5E7EB" stroke-width="1"/>'
        f'<path d="{area}" fill="rgba(15,118,110,.12)"/>'
        f'<polyline points="{" ".join(P)}" fill="none" stroke="#0F766E" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>'
        f'<circle cx="{xs[-1]:.1f}" cy="{ys[-1]:.1f}" r="3" fill="#0F766E"/>'
        f'<text x="8" y="64" font-size="11" fill="#6B7280">{d0}</text>'
        f'<text x="252" y="64" font-size="11" fill="#6B7280" text-anchor="end">{d1}</text></svg>')

def render_head(card):
    b = card["basics"]; badge = card.get("badge", {})
    chips = f'<span class="chip">{esc(badge.get("main", "今日一库 · 项目名片"))}</span>'
    sub = badge.get("sub") or badge.get("text")
    if sub: chips += f'<span class="chip sub">{esc(sub)}</span>'
    if card.get("stale_chip"): chips += f'<span class="chip sub">{esc(card["stale_chip"])}</span>'
    no = f'<span class="c-no">CARD #{card["card_no"]:03d}</span>' if card.get("card_no") else ""
    anchor = f'<div class="c-anchor">{card["anchor"]}</div>' if card.get("anchor") else ""
    spark = render_spark(b["name"], card.get("trend", {}).get("points", []))
    fn = card.get("fn")
    title = (f'<a class="c-title" href="https://github.com/{esc(fn)}" target="_blank" rel="noopener">{esc(b["name"])}</a>'
             if fn else f'<div class="c-title">{esc(b["name"])}</div>')
    return (
        f'<div class="c-top">{chips}{no}</div>\n'
        f'<div class="c-body">\n<div class="c-left">\n'
        f'{title}\n{anchor}\n{render_meta(b)}\n</div>\n'
        f'<div class="c-right"><div class="c-star">{fmt_stars(b["stars"])}<span class="u">★</span></div>{spark}</div>\n</div>')

def arena_rows(rows, disp):
    """擂台展示口径：主角恒在首行；候选 score≥min_score，按 (score desc, star desc) 排序，封顶 max_n。"""
    hero = [r for r in rows if r.get("me")]
    cands = [r for r in rows if not r.get("me") and r.get("score", 0) >= disp.get("min_score", 0.6)]
    cands.sort(key=lambda r: (-r["score"], -r["stars"]))
    return hero[:1] + cands[:disp.get("max_n", 5)]

def sec_solve(card):
    d = card.get("solve") or card.get("pain") or {}
    if not d: return ""
    body = f'<p class="pain">{join_text(d.get("pains", ""))}</p><p>{join_text(d.get("meds", ""))}</p>'
    return _sec("解决什么问题", "🔧", d.get("sub", "痛点与方案"), body)

def sec_adapt(card):
    d = card.get("adapt") or {}
    if not d: return ""
    lines = list(d.get("lines") or [])
    if not lines and d.get("dbs"):
        lines = ["·".join(d["dbs"]) + (f"——{d['nature']}" if d.get("nature") else "")]
    ps = "".join(f"<p>{l}</p>" for l in lines)
    return _sec("适配哪些库", "🔌", d.get("sub", ""), ps)

def sec_arena(card):
    d = card.get("arena") or {}
    rows = d.get("rows", [])
    if not rows: return ""
    disp = d.get("display", {"min_score": 0.6, "max_n": 5})
    trs = []
    for r in arena_rows(rows, disp):
        cls = ' class="me"' if r.get("me") else ""
        trs.append(
            f'<tr{cls}><td><a href="https://github.com/{r["fn"]}" target="_blank" rel="noopener">{esc(r["fn"])}</a></td>'
            f'<td class="stars">{fmt_stars(r["stars"])}</td><td>{html.escape(str(r.get("why", "")), quote=False)}</td>'
            f'<td class="stars">{r["score"]:.2f}</td></tr>')
    body = ('<table class="t"><thead><tr><th scope="col">同类项目</th><th scope="col" class="stars">⭐</th>'
            '<th scope="col">简介</th><th scope="col" class="stars">相似度</th></tr></thead>\n<tbody>\n'
            + "\n".join(trs) + "\n</tbody></table>")
    return _sec("同类擂台", "🎯", d.get("sub", "算法圈选"), body)

def sec_news(card):
    d = card.get("news") or {}
    if not d.get("items") and not d.get("cadence"): return ""
    ps = "".join(
        f'<p><b>{esc(i.get("ver", ""))}</b>（{esc(i["date"][5:] if len(i.get("date", "")) == 10 else i.get("date", ""))}）——{esc(i.get("story", ""))}</p>'
        for i in d.get("items", []))
    if d.get("cadence"): ps += f'<p class="t-sub" style="margin-top:4px;">{esc(d["cadence"])}</p>'
    return _sec("近期动态", "📰", d.get("sub", "近 90 天"), ps)

def sec_production(card):
    d = card.get("production_users") or {}
    items = d.get("items", [])
    if not items: return ""
    body = '<div class="users">' + "".join(f'<div class="user">{esc(i["text"])}</div>' for i in items) + "</div>"
    return _sec("生产采用", "🏭", d.get("sub", "一手来源 + README 提及数"), body)

def sec_verdict(card):
    d = card.get("verdict") or {}
    if not (d.get("should") or d.get("avoid")): return ""
    body = ('<div class="verdict">'
            f'<div class="v-item"><div class="t">✅ 适用</div>{esc(d.get("should", ""))}</div>'
            f'<div class="v-item"><div class="t">⛔ 不适用</div>{esc(d.get("avoid", ""))}</div>'
            '</div>')
    return _sec("适用场景", "🔍", d.get("sub", "选型建议"), body)

def sec_hands_on(card):
    d = card.get("hands_on") or {}
    lines = list(d.get("lines") or []) or ([f"# {d['docs_url']}（官网占位，命令实跑后回填）"] if d.get("docs_url") else [])
    if not lines: return ""
    body = "<pre><code>" + "\n".join(esc(l) for l in lines) + "</code></pre>"
    return _sec("上手一行", "⚡", d.get("sub", ""), body)

def _sec(title, icon, sub, body):
    s = f'<span class="t-sub">{esc(sub)}</span>' if sub else "<span></span>"
    return (f'\n<div class="sec">\n<div class="t-head"><span class="t-title">{icon} {title}</span>{s}</div>\n{body}\n</div>')

def sec_intro(card):
    d = card.get("intro") or {}
    if not (d.get("text") or d.get("review") or d.get("points") or d.get("uses")): return ""
    body = f'<p>{join_text(d.get("text", ""))}</p>' if d.get("text") else ""
    if d.get("review"):   # 综述段：解读层已有内容原样搬（2026-11-14 用户令：只放已解读的，不再解读）
        body += ('<p class="pts-label">综述（解读层）</p>'
                 f'<p class="pain">{html.escape(str(d["review"]), quote=False)}</p>')   # esc=透传，须真转义
    if d.get("points"):
        body += '<ul class="pts">' + "".join(f"<li>{esc(x)}</li>" for x in d["points"]) + "</ul>"
    if d.get("uses"):
        body += ('<p class="pts-label">适用场景（解读层）</p>'
                 '<ul class="pts">' + "".join(f"<li>{esc(x)}</li>" for x in d["uses"]) + "</ul>")
    return _sec("简介", "🧭", d.get("sub", ""), body)

def sec_readme(card):
    d = card.get("readme") or {}
    if not d.get("text"): return ""
    return _sec("README 首段", "📖", d.get("sub", "存档原文 · 程序抽取"),
                f'<p class="pain">{esc(d["text"])}</p>')

SECTIONS = [sec_intro, sec_readme, sec_solve, sec_adapt, sec_arena, sec_news,
            sec_production, sec_verdict, sec_hands_on]

def render(card):
    parts = [render_head(card)] + [f(card) for f in SECTIONS]
    return ("<!DOCTYPE html>\n<html lang=\"zh-CN\">\n<head>\n<meta charset=\"UTF-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n"
            f"<title>项目名片 · {esc(card['basics']['name'])}</title>\n<style>\n{CSS}</style>\n"
            "</head>\n<body>\n<div class=\"card\">\n" + "\n".join(parts) + "\n\n</div>\n</body>\n</html>\n")

# ---------- 自检 ----------

def _selftest():
    b = {"name": "t", "stars": 1234, "language": "Java", "license": {"display": "MIT"},
         "created_at": "2015-07-08", "version": {"latest": "1.0"},
         "activity": {"contributors": 3, "commit_90d": 7}, "pushed_at": "2026-01-01"}
    assert meta_items(b) == ["语言 Java", "协议 MIT", "创建于 2015", "版本 1.0",
                             "贡献者 3 人", "最近提交 2026-01-01", "90 天 7 commits"]
    m = render_meta(b)
    assert m.count("<span>") == 7 and "nowrap" not in m

    rd = datetime.date(2026, 11, 12)
    assert stale_marker("2020-11-02", rd) == "· 6 年未更"
    assert stale_marker("2026-07-12", rd) == ""                       # 123 天，未过线
    assert stale_marker("2025-11-01", rd) == "· 1 年未更"
    assert stale_marker("2026-04-20", rd) == "· 6 个月未更"           # 206 天，按月
    assert stale_marker(None, rd) == ""
    assert "188" in mention_line(188, 35017, "2026-11-12")

    rows = [{"fn": "a/a", "stars": 10, "score": 1.0, "me": True},
            {"fn": "b/b", "stars": 50, "score": 0.9},
            {"fn": "c/c", "stars": 5, "score": 0.59},
            {"fn": "d/d", "stars": 9, "score": 0.61},
            {"fn": "e/e", "stars": 8, "score": 0.61}]
    out = arena_rows(rows, {"min_score": 0.6, "max_n": 5})
    assert [r["fn"] for r in out] == ["a/a", "b/b", "d/d", "e/e"]
    out2 = arena_rows(rows, {"min_score": 0.0, "max_n": 2})
    assert [r["fn"] for r in out2] == ["a/a", "b/b", "d/d"]

    s = render_spark("x", [["2026-01-01", 10], ["2026-01-02", 20]])
    assert "polyline" in s and "01-01" in s
    assert "polyline" in render_spark("x", [["2026-01-01", 5], ["2026-01-02", 5]])

    # enrich：停更标记 + 提及数 + 年龄，全部进副本与 derived
    pool = {"t/t": {"stars": 1234, "pushed_at": "2026-11-01", "created_at": "2015-07-08"},
            "b/b": {"stars": 50, "pushed_at": "2020-11-02", "created_at": "2016-01-01"}}
    card = {"schema": "dbhub.card/1.1", "card_no": 1, "fn": "t/t", "basics": b,
            "trend": {"points": [["2026-01-01", 10], ["2026-01-02", 11]]},
            "badge": {"text": "旧式徽章"}, "pain": {"pains": ["a", "b"], "meds": "m"},
            "adapt": {"dbs": ["PostgreSQL"], "nature": "专用工具"},
            "arena": {"rows": rows + [{"fn": "f/f", "stars": 1, "score": 0.62, "why": "a<b & c"}]}, "news": {"items": [{"ver": "v", "date": "2026-01-02", "story": "s"}]},
            "production_users": {"items": [{"text": "u"}]},
            "verdict": {"should": "s", "avoid": "a"}, "hands_on": {"docs_url": "https://x"},
            "intro": {"text": "one liner", "review": "rv<para>", "sub": "sub", "points": ["p1"], "uses": ["u1"]},
            "readme": {"text": "rm first para"}}
    c2 = enrich(card, pool, (188, 35017, "2026-11-12"), "2026-11-12")
    assert c2["derived"]["mentions"]["count"] == 188
    assert c2["derived"]["age"]["created_year"] == "2015"
    bb = [r for r in c2["arena"]["rows"] if r["fn"] == "b/b"][0]
    assert bb["why"] == "· 6 年未更" and bb["stop_days"] > 2100
    h = render(c2)
    assert h.rstrip().endswith("</html>") and "CARD #001" in h
    assert h.count('class="sec"') == 9 and "a；b" in h            # intro+readme + 7 块
    assert "one liner" in h and "p1" in h and "u1" in h and "rm first para" in h
    assert '<a class="c-title" href="https://github.com/t/t"' in h   # 标题跳 GitHub
    assert 'class="pts-label">适用场景' in h                        # 场景标签加粗
    assert 'class="pts-label">综述（解读层）' in h and "rv&lt;para&gt;" in h   # 综述段上卡且转义
    assert h.index("one liner") < h.index("rv&lt;para&gt;") < h.index("p1")   # 位置：一句话→综述→亮点
    assert "旧式徽章" in h                                          # badge.text 兜底
    assert "188 个其他项目" in h and "创建于 2015" in h
    assert "截至 2026-11-12" in h                                     # 截至戳=缓存建成日
    assert "官网占位" in h and "专用工具" in h                       # hands_on/adapt 兜底
    assert "a&lt;b &amp; c" in h and "a<b & c" not in h         # 擂台简介=外部 description，转义后上 HTML
    print(f"OK {VER} selftest: 19 asserts passed")
    return 0

def main():
    here = os.path.dirname(os.path.abspath(__file__))
    p = argparse.ArgumentParser()
    p.add_argument("--card", nargs="+", help="一张或多张底稿 JSON")
    p.add_argument("--out", help="单张时的输出 HTML；多张时省略，按底稿名自动生成 名片样卡-<name>.html")
    p.add_argument("--pool", default=POOL_DEFAULT)
    p.add_argument("--mentions-cache", default=here + os.sep + "cache" + os.sep + "mentions.json",
                   help="build_cache 产物（提及数唯一来源）")
    p.add_argument("--no-scan", action="store_true", help="不注入 README 提及数")
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.selftest: sys.exit(_selftest())
    if not a.card: p.error("--card required")
    if len(a.card) > 1 and a.out: p.error("--out only valid with a single --card")
    run_date = datetime.date.today().isoformat()
    cards = [json.load(io.open(f, encoding="utf-8")) for f in a.card]
    pool_map = load_pool(a.pool)
    mentions_map = {}
    if not a.no_scan:
        if not os.path.exists(a.mentions_cache):
            sys.exit("FAIL mentions cache not found: " + a.mentions_cache +
                     "\n  run first: python -I build_cache.py --steps mentions")
        mcounts, corpus, mdate = load_mentions_cache(a.mentions_cache)
        for c in cards:   # slug 口径键=fn（owner/repo），不再用裸仓名；0 提及不挂块
            fn = str(c.get("fn", "")).lower()
            if fn in mcounts and mcounts[fn] >= 1:
                mentions_map[fn] = (mcounts[fn], corpus, mdate)
                print(f"  mentions {fn}: {mcounts[fn]} / corpus {corpus} (cache built {mdate})")
    for f, card in zip(a.card, cards):
        name = card["basics"]["name"]
        mentions = mentions_map.get(str(card.get("fn", "")).lower())
        c = enrich(card, pool_map, mentions, run_date)
        out = a.out or (os.path.dirname(f) or ".") + os.sep + f"名片样卡-{name}.html"
        io.open(out, "w", encoding="utf-8", newline="\n").write(render(c))
        json_path = os.path.splitext(out)[0] + ".json"
        io.open(json_path, "w", encoding="utf-8", newline="\n").write(
            json.dumps(c, ensure_ascii=False, indent=2))
        print(f"OK [{VER}] {os.path.basename(f)} -> {os.path.basename(out)} + {os.path.basename(json_path)}")

if __name__ == "__main__":
    main()
