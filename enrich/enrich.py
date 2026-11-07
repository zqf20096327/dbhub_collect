# -*- coding: utf-8 -*-
"""信号富集采集：commit 活跃 / release / GHSA 安全通告 / contributor / 语言构成。

维度刷新原则（按数据变化成因二分）：
  状态量维度（release/contrib/lang）——无 push 物理上不会变
  （发版必有 tag push、贡献者必有 commit、语言构成随代码变）：
      首轮必采；此后仅当 pushed_at 变化且到期才重采
  滚动窗口维度（commit）——push 变化时重采；但计数随时间自然衰减（死仓的
      commit_7d/90d 真值应为 0），无 push 时按 pushed_at 推导归零（零调用，
      见 decay_commit_fields），不能被 push 闸门永久冻结
  时间依赖维度（security）——GHSA 披露是外部事件，与仓库死活无关：到期即采
  整仓跳过：pushed_at 未变且无任何到期维度才跳过（修复旧版死仓连 security
  到期都被短路豁免的问题）；进 targets 只采到期维度（死仓只花 1 次调用）
分层（star 分层 + 国产 floor）：
  head(star>=1000)：commit/release 7 天、security 30 天、contrib 90 天、lang 一次性
  mid(star>=100)：commit/release 30 天、security 90 天、contrib/lang 一次性
  tail：仅 security 180 天；release/contrib/lang 首轮一次；死活看池 pushed_at（免费）
  国产仓 floor=mid（识别双信号：topics ∩ 国产 topic 集，或发现通道命中国产词/org），
  活跃国产仓享受 30 天 commit/release，死仓也只花 security 轮转
状态：state/enrich_state.json（断点/三振）+ state/enrich_cache_shards/ 256 分片
      （信号数据侧车，10-09 起分片，存取走 lib/enrich_store.py）
预算：--max-calls / --max-minutes / 保底线（gh.py 内置）

用法：
  python enrich.py --tier head                 # 头部增量刷新
  python enrich.py --tier all                  # 首轮铺全量（断点续采）
  python enrich.py --only commit --tier tail   # 单维度
"""
from __future__ import annotations

import argparse
import json
import logging
import time
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import sys as _sys, pathlib as _pl
ROOT = _pl.Path(__file__).resolve().parents[1]
for _d in (ROOT, ROOT / "lib", ROOT / "config"):
    _sys.path.insert(0, str(_d))
HERE = ROOT                      # 历史引用兼容：统一指向项目根

import requests  # noqa: E402

import strategy                  # noqa: E402
from gh import Budget, BudgetOut, CoreReserveOut, GitHubClient, QuotaPatienceOut, atomic_write_json  # noqa: E402
from enrich_store import EnrichCacheStore  # noqa: E402  enrich_cache 分片存取（10-09 起）

log = logging.getLogger("enrich")
STATE = HERE / "state" / "enrich_state.json"
THREE_STRIKES = 3
DIMS = ("commit", "release", "security", "contrib", "lang")
TIER_STAR = {"head": 1000, "mid": 100, "tail": 0}
# 每层采集的维度集合
TIER_DIMS = {
    "head": ("commit", "release", "security", "contrib", "lang"),
    "mid": ("commit", "release", "security", "contrib", "lang"),
    "tail": ("release", "security", "contrib", "lang"),   # 长尾不采 commit（死活看 pushed_at）
}
# 每层每维度刷新天数（None = 首轮采过即不再采）
# 11-07 TTL 收紧：首轮铺量已完成（34.6k 仓设计内维度全齐），实测每晚只花
# 500-600 调对 5000 预算——把余量换成新鲜度。release 每晚不是每晚全扫：
# push 闸门（无 push 不查）+ ETag（未变 304 不计配额）双重限流。
REFRESH_DAYS = {
    "head": {"commit": 3, "release": 1, "security": 30, "contrib": 90, "lang": None},
    "mid":  {"commit": 14, "release": 14, "security": 90, "contrib": None, "lang": None},
    "tail": {"commit": None, "release": None, "security": 180, "contrib": None, "lang": None},
}
# 有安全通告史的仓加密轮转（全池实测仅 0.88% 有通告，它们才是会再发的）；
# 零历史仓维持基础值——不为 99% 的空结果牺牲首条通告的发现时延。
SEC_HISTORY_DAYS = {"head": 7, "mid": 14, "tail": 30}
# staleness SLO：每个（层×维度）里"值仍然可信"的仓占比低于此线就告警
SLO_FRESH_RATIO = 0.95
SEV_ORDER = {"critical": 4, "high": 3, "moderate": 2, "low": 1}
# 滚动窗口（天）：commit_7d/90d 是"采集时点往前 N 天"的计数，不 push 也会随时间
# 衰减到 0——与 release/contrib/lang 这些状态量不同，不能被 push 闸门永久冻结。
WINDOW_DAYS = {"commit_7d": 7, "commit_90d": 90}
# pushed_at 的最大滞后：org 周扫携带（huaweicloud/tencentcloud）= 7 天 + 池扫描
# 本身最多 1 天。推导归零必须让过这段滞后，否则会把"昨天刚 push、池里还写着
# 8 天前"的活仓误判成 0（11-07 全量验证实测到这类仓）。
POOL_LAG_DAYS = 8
# 隔离复检期（天）：三振/404 不是永久死刑。平台级故障（连续三晚 5xx）会批量
# 隔离，空仓拿到首个 commit 后也不再有机会——到期给一次复检，成本 1 调/仓。
REVIVE_DAYS = {"failed": 90, "gone": 180}
# release 正文摘要：90 天窗（> 最长轮转 30 天，mid 层不漏正文）+ 最多 10 条
NOTE_DAYS, NOTE_MAX, NOTE_CAP = 90, 10, 512


def _cn_signals():
    """国产识别信号（双信号：仓库自身 topics ∪ 发现通道命中），不改池 schema。"""
    cn = strategy.derive_sections()["cn"]
    return (set(cn["topics"]), set(cn["queries"]),
            {strategy.norm(o) for o in cn["orgs"]})


CN_TOPICS, CN_WORDS, CN_ORGS = _cn_signals()


def is_cn_item(it: dict) -> bool:
    if set(it.get("topics") or []) & CN_TOPICS:
        return True
    st = it.get("source_topic") or ""
    if it.get("source") == "keyword":
        return st in CN_WORDS
    if it.get("source") == "org":
        return st in CN_ORGS
    return False


def load_json(path: Path, default):
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return default


def tier_of(stars: int, cn: bool = False) -> str:
    for name in ("head", "mid"):
        if stars >= TIER_STAR[name]:
            return name
    return "mid" if cn else "tail"    # 国产 floor=mid


def iso_days_ago(days: int) -> str:
    return (datetime.now(timezone.utc) - timedelta(days=days)) \
        .strftime("%Y-%m-%dT%H:%M:%SZ")


def days_since(date_str: str) -> int | None:
    """日历天差（与 refresh_derived_days 同口径；按小时折算会在跨日时差 1 天）。"""
    d = _day_of(date_str)
    if d is None:
        return None
    return (datetime.now(timezone.utc).date() - d).days


def _day_of(s) -> date | None:
    """日期串 → date（兼容 "YYYY-MM-DD…" 与 "YYYYMMDD"）。"""
    if not s:
        return None
    raw = str(s)[:10]
    for fmt in ("%Y-%m-%d", "%Y%m%d"):
        try:
            return datetime.strptime(raw, fmt).date()
        except ValueError:
            continue
    return None


def _today_compact() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d")


def decay_commit_fields(pool: list, cache, today: date | None = None) -> int:
    """滚动窗口计数按 pushed_at 归零（零 API 调用），返回修正仓数。

    push 闸门对 release/contrib/lang 成立（状态量，push 才变），但
    commit_7d/commit_90d 是滚动窗口计数：不 push 也会随时间衰减。
    最后推送比窗口还老 ⇒ 窗口内必无提交，真值就是 0。但 pushed_at 本身有滞后
    （org 周扫携带 7 天 + 池扫描 1 天，见 POOL_LAG_DAYS），所以要求 push_age
    超过「窗口 + 滞后」才算得出 0；dim_ts 也要真过期（采集后没再采过）。
    只改值不动 dim_ts：dim_ts 语义是"最后一次 API 采集"，推导值不装成采集。
    """
    today = today or datetime.now(timezone.utc).date()
    touch = getattr(cache, "touch", None)
    fixed = 0
    for it in pool:
        fn = it.get("full_name")
        sig = cache.get(fn)
        if not sig:
            continue
        pushed = _day_of(it.get("pushed_at"))
        if pushed is None:
            continue
        age = (today - pushed).days
        ts = _day_of((sig.get("dim_ts") or {}).get("commit"))
        ts_age = None if ts is None else (today - ts).days
        changed = False
        for key, win in WINDOW_DAYS.items():
            if (sig.get(key) or 0) > 0 \
                    and age > win + POOL_LAG_DAYS \
                    and (ts_age is None or ts_age > win):
                sig[key] = 0
                changed = True
        if changed:
            if touch:
                touch(fn)
            fixed += 1
    return fixed


def refresh_derived_days(pool: list, cache, today: date | None = None) -> int:
    """时间相关派生值按今天重算（rel_days / rel_n90），零 API。

    rel_days = 今天 - rel_pub；rel_n90 = 90 天窗内发版数（来源 rel_dates）。
    两者落库后都会随天数自然失真，采集时快照不能当现值用。
    """
    today = today or datetime.now(timezone.utc).date()
    touch = getattr(cache, "touch", None)
    cutoff = (today - timedelta(days=NOTE_DAYS)).isoformat()
    fixed = 0
    for it in pool:
        fn = it.get("full_name")
        sig = cache.get(fn)
        if not sig:
            continue
        changed = False
        pub = _day_of(sig.get("rel_pub"))
        if pub is not None:
            days = (today - pub).days
            if sig.get("rel_days") != days:
                sig["rel_days"] = days
                changed = True
        dates = sig.get("rel_dates")
        if isinstance(dates, list):
            n90 = sum(1 for d in dates if isinstance(d, str) and d[:10] >= cutoff)
            if sig.get("rel_n90") != n90:
                sig["rel_n90"] = n90
                changed = True
        if changed:
            if touch:
                touch(fn)
            fixed += 1
    return fixed


def _revive_due(rec: dict, status: str, today: date) -> bool:
    """隔离到期复检：无戳老记录给一次机会；有戳按 REVIVE_DAYS 判定。"""
    q = _day_of(rec.get("quarantined_at"))
    if q is None:
        return True
    return (today - q).days >= REVIVE_DAYS.get(status, 90)


def _needs_refresh(rec: dict, dim: str, refresh_days) -> bool:
    if refresh_days is None:
        return False
    ts = (rec.get("dims") or {}).get(dim)
    if not ts:
        return True
    try:
        done = datetime.strptime(ts, "%Y%m%d").replace(tzinfo=timezone.utc)
    except ValueError:
        return True
    return (datetime.now(timezone.utc) - done).days >= refresh_days


def _security_days(rec: dict, tier: str, sig: dict | None = None) -> int:
    """安全轮转天数：有通告史的仓加密（SEC_HISTORY_DAYS），零历史走基础层值。

    sec_n 在 cache（信号侧车）而非 state：due_dims 由调用方把 sig 传进来。
    rec 兜底只为兼容将来把 sec_n 挪进 state 的写法。
    """
    base = REFRESH_DAYS[tier]["security"]
    n = (sig or {}).get("sec_n")
    if n is None:
        n = rec.get("sec_n")
    if (n or 0) > 0:
        return SEC_HISTORY_DAYS.get(tier, base)
    return base


def due_dims(rec: dict, tier: str, pushed_changed: bool,
             sig: dict | None = None) -> list[str]:
    """到期维度：security 到期即采（有通告史加密）；状态量（release/contrib/lang）
    首轮必采、其后需 pushed_at 变化且到期。commit 也走此闸门，但窗口衰减由
    decay_commit_fields 零调用归零，不在这里产生 API 调用。"""
    due = []
    for d in TIER_DIMS[tier]:
        rd = _security_days(rec, tier, sig) if d == "security" else REFRESH_DAYS[tier][d]
        if d == "security":
            if _needs_refresh(rec, d, rd):
                due.append(d)
        elif not (rec.get("dims") or {}).get(d):
            due.append(d)
        elif pushed_changed and rd and _needs_refresh(rec, d, rd):
            due.append(d)
    return due


# 采集口径（10-30 定）：行级只要提到某个数据库就收，不要求 support/drop 等变更词；
# 变更词只用于排序——先把 DB 相关行采下来，判断留到适配引擎。
# ① 17 库口径（config/db_profiles.py）精确词；改口径时同步这里，selftest 有覆盖断言
DB_WORDS_17 = ("postgres", "postgre", "mysql", "oracle", "sqlite", "sql server",
               "mssql", "clickhouse", "mariadb", "tidb", "tikv", "oceanbase",
               "polardb", "dameng", "达梦", "dm8", "dm database", "opengauss",
               "gaussdb", "gbase", "tdsql", "yashandb", "yashan", "goldendb")
# ② 口径外常见库：同收（适配引擎可能用得上）
DB_WORDS_EXTRA = ("mongo", "redis", "cassandra", "dynamodb", "elasticsearch",
                  "duckdb", "snowflake", "bigquery", "spanner", "hbase", "neo4j")
# ③ 泛词兜底：非口径库（CockroachDB/InfluxDB…）靠它命中，代价是噪声（dbbench/dbms）
DB_WORDS_GENERIC = ("database", "db")
DB_WORDS = DB_WORDS_17 + DB_WORDS_EXTRA + DB_WORDS_GENERIC
# 强度分档：0=移除/弃用 1=新增支持 2=兼容/连接/迁移 3=仅提到库名
STRONG_WORDS = ("drop", "remove", "no longer", "deprecat", "eol", "end of life",
                "breaking", "discontinu", "sunset", "retire")
MEDIUM_WORDS = ("support", "add ", "adds", "added", "introduc", "new ")
WEAK_WORDS = ("compat", "connect", "driver", "migrat", "integrat")
CHANGE_WORDS = STRONG_WORDS + MEDIUM_WORDS + WEAK_WORDS


def note_rank(line: str) -> int | None:
    """库名行强度：0=移除/弃用 1=新增支持 2=兼容/连接 3=仅提到库名；不含库名 None。

    判档顺序即优先级：同时含 drop 和 support 的行算 0（"Dropped support for …"）。
    """
    low = line.lower()
    if not any(w in low for w in DB_WORDS):
        return None
    for rank, words in ((0, STRONG_WORDS), (1, MEDIUM_WORDS), (2, WEAK_WORDS)):
        if any(w in low for w in words):
            return rank
    return 3


def _cut_utf8(s: str, cap: int) -> str:
    """按 UTF-8 字节截断，不劈开多字节字符（中文 1 字 3 字节，字符截会超预算）。"""
    b = s.encode("utf-8")
    return s if len(b) <= cap else b[:cap].decode("utf-8", errors="ignore")


def _excerpt(body: str, cap: int) -> str:
    """超长正文摘要：只取提到库名的行，按强度排序；无库名行退回整段前缀。

    模板头部（What's Changed / PR 列表）不占预算——版本和日期在 t/d 字段里，
    库名信息才是要采的数据。
    """
    if len(body.encode("utf-8")) <= cap:
        return body
    picked = []
    for line in body.splitlines():
        s = line.strip()
        if not s or s in picked:
            continue
        if note_rank(s) is not None:
            picked.append(s)
    if not picked:
        return _cut_utf8(body, cap)
    picked.sort(key=note_rank)      # 稳定排序：同强度保持正文顺序
    return _cut_utf8("\n".join(picked), cap)


def _release_notes(rels: list[dict], days: int = NOTE_DAYS, cap: int = NOTE_CAP,
                   max_n: int = NOTE_MAX, today: date | None = None) -> list[dict] | None:
    """最近 days 天内所有有正文的 release 摘要（最多 max_n 条）。

    body 本就在 releases 响应里，零新增调用；只在有正文时产出。
    10-30 起是"取前 3 条"；11-07 改为时间窗（> 最长轮转 30 天）：mid 层 30 天
    节奏下固定取前 3 会把两次检查之间的 release 正文永久丢掉（实测 308 个
    mid 仓月均发版 >3，适配变更史是产品核心素材，不能漏）。
    cap=512 字节（UTF-8）够容纳"新增/移除数据库支持"级别的条目，控存储体积；
    超长正文不再盲取开头——开头常是 "What's Changed" 模板和 PR 列表，
    改为只收提到库名的行（模板头部不占预算，版本/日期在 t/d 字段），
    按强度排序：移除/弃用 > 新增支持 > 兼容/连接 > 仅提到库名。
    """
    today = today or datetime.now(timezone.utc).date()
    cutoff = today - timedelta(days=days)
    out = []
    for r in rels:
        d = _day_of(r.get("published_at"))
        if d is None or d < cutoff:
            continue
        body = (r.get("body") or "").strip()
        if body:
            out.append({"t": r.get("tag_name"), "d": d.isoformat(),
                        "n": _excerpt(body, cap)})
        if len(out) >= max_n:
            break
    return out or None


def _merge_notes(old: list, new: list, max_n: int = NOTE_MAX) -> list:
    """新旧正文摘要按 tag 去重（新覆盖旧）、日期降序、最多 max_n 条。"""
    by_tag = {}
    for n in list(old) + list(new):
        if isinstance(n, dict) and n.get("t"):
            by_tag[n["t"]] = n
    return sorted(by_tag.values(), key=lambda x: x.get("d") or "",
                  reverse=True)[:max_n]


def collect_dims(client: GitHubClient, fn: str, cache: dict, dims: tuple,
                 pushed_changed: bool) -> dict:
    """对一个仓库执行到期的维度采集，返回信号字段（异常由调用方处理）。"""
    sig = cache.setdefault(fn, {})
    cache.touch(fn)          # 值字段是原地 update，脏桶追踪看不见——采集前显式标脏
    today = datetime.now(timezone.utc).strftime("%Y%m%d")
    if "commit" in dims:
        # 7 天必采；90 天条件采——死仓（7 天 0 提交且 pushed_at 未变）的 90 天数不会变
        c7 = client.commits_count(fn, iso_days_ago(7))
        if c7 or pushed_changed or "commit_90d" not in sig:
            sig["commit_90d"] = client.commits_count(fn, iso_days_ago(90))
        sig["commit_7d"] = c7
    if "release" in dims:
        etags = sig.setdefault("etag", {})
        try:
            status, rels, etag = client.releases_conditional(fn, etags.get("release"))
        except requests.HTTPError as e:
            if getattr(e.response, "status_code", None) == 404:
                status, rels, etag = 200, [], None
            else:
                raise
        if status == 304:
            pass      # 资源未变：旧值仍有效；rel_days/rel_n90 由零调用修正按今天重算
        elif rels:
            latest = rels[0]
            cutoff = datetime.now(timezone.utc) - timedelta(days=90)
            cut = cutoff.strftime("%Y-%m-%d")
            n90 = sum(1 for r in rels if (r.get("published_at") or "")[:10] >= cut)
            sig.update({"rel_ver": latest.get("tag_name"),
                        "rel_pub": (latest.get("published_at") or "")[:10],
                        "rel_days": days_since(latest.get("published_at") or ""),
                        "rel_n90": n90, "rel_pre": bool(latest.get("prerelease")),
                        "rel_none": False,
                        # 90 天窗内的发版日期：rel_n90 的派生源（304 后窗口仍在走，
                        # 只靠采集时快照会把过期发版一直算在数里）
                        "rel_dates": [(r.get("published_at") or "")[:10]
                                      for r in rels
                                      if (r.get("published_at") or "")[:10] >= cut]})
            etags["release"] = etag
            # 适配变更史素材：90 天窗全收（10-30 起取前 3 条会丢 mid 层正文），
            # 与已有摘要按 tag 合并去重，避免某次抓取失败把历史摘要冲掉
            notes = _release_notes(rels)
            if notes:
                sig["rel_notes"] = _merge_notes(sig.get("rel_notes") or [], notes)
        else:
            sig.update({"rel_ver": None, "rel_none": True, "rel_dates": []})
            etags["release"] = etag
    if "security" in dims:
        etags = sig.setdefault("etag", {})
        try:
            status, advs, etag = client.advisories_conditional(fn, etags.get("security"))
        except requests.HTTPError as e:
            if getattr(e.response, "status_code", None) == 404:
                status, advs, etag = 200, [], None
            else:
                raise
        if status != 304:                       # 304：通告集未变，旧值仍有效
            etags["security"] = etag
            live = [a for a in advs if a.get("withdrawn_at") is None]
            worst = max((a.get("severity") for a in live if a.get("severity") in SEV_ORDER),
                        key=lambda s: SEV_ORDER[s], default=None)
            sig.update({"sec_n": len(live),
                        "sec_worst": worst,
                        "sec_last": max(((a.get("published_at") or "")[:10] for a in live),
                                        default=None),
                        "sec_ids": [f'{a.get("ghsa_id")}({(a.get("cve_id") or "-")},{a.get("severity")})'
                                    for a in live[:8]]})
    if "contrib" in dims:
        try:
            sig["contrib_n"] = client.contributors_count(fn)
        except requests.HTTPError as e:
            if getattr(e.response, "status_code", None) in (404, 409):
                sig["contrib_n"] = None
            else:
                raise
    if "lang" in dims:
        langs = client.languages(fn)
        total = sum(langs.values()) or 1
        sig["lang"] = {k: round(v * 100 / total) for k, v in
                       sorted(langs.items(), key=lambda x: -x[1])[:5]}
    sig["enriched_at"] = today
    # 字段级采集时间：enriched_at 是记录级触碰时间（多机合并取新用），
    # security-only 刷新会 bump enriched_at 而不动 commit_7d/rel_ver 等旧值——
    # 解读侧判断这些字段的新鲜度必须以 dim_ts 为准，防止陈旧值被"洗白"成今天
    tsmap = sig.setdefault("dim_ts", {})
    for d in dims:
        tsmap[d] = today
    return sig


def _pctl(vals: list, q: float):
    if not vals:
        return None
    vals = sorted(vals)
    return vals[min(len(vals) - 1, int(len(vals) * q))]


def health_report(pool: list, cache, items: dict, tiers=("head", "mid", "tail"),
                  today: date | None = None) -> dict:
    """staleness SLO：每层每维的覆盖率、数据年龄分位、值有效性占比。

    有效性不是简单看年龄——状态量维度没有 push 就不会变，年龄大也依然可信：
      security            —— 时间驱动：年龄 ≤ 2×TTL
      commit              —— 年龄 ≤ 2×TTL，或推送已过「7 天窗 + 池滞后」且采集后
                             无新推送（decay 已归零 c7，c90 的 >0 语义仍成立）
      release/contrib/lang—— 状态量：年龄 ≤ 2×TTL 或 pushed_at 与采集时一致
    一次性维度（TTL=None）只报覆盖率，不参与新鲜度告警。
    tiers 只报本次跑到的层（--tier head 不拿 mid/tail 的待采当告警）。
    """
    today = today or datetime.now(timezone.utc).date()
    cells = {t: {"n": 0, "dims": {d: {"ages": [], "covered": 0, "valid": 0,
                                      "checked": 0, "pending": 0}
                                  for d in TIER_DIMS[t]}}
             for t in tiers}
    for it in pool:
        fn = it.get("full_name")
        tier = tier_of(it.get("stars") or 0, cn=is_cn_item(it))
        if tier not in cells:
            continue
        cell = cells[tier]
        cell["n"] += 1
        sig = cache.get(fn) or {}
        rec = items.get(fn) or {}
        tsmap = sig.get("dim_ts") or {}
        pushed = _day_of(it.get("pushed_at"))
        push_age = (today - pushed).days if pushed else None
        for d, c in cell["dims"].items():
            if d in (rec.get("dims") or {}):
                c["covered"] += 1              # 真实覆盖：状态里有该维度
            ts = _day_of(tsmap.get(d))
            if ts is None:
                continue                       # 缺 dim_ts（10-29 前老记录）：年龄未知
            age = (today - ts).days
            c["ages"].append(age)
            ttl = (_security_days(rec, tier, sig) if d == "security"
                   else REFRESH_DAYS[tier][d])
            if ttl is None:
                continue                       # 一次性维度：无新鲜度 SLO
            pending = False
            if d == "security":
                ok = age <= 2 * ttl
            elif d == "commit":
                # 推送已超出 7 天窗 + 池滞后且采集后无新推送 ⇒ decay 已把 c7 归零，
                # c90 的“90 天内有提交”语义仍成立，值可信（不按 90 天窗卡）
                unchanged = rec.get("pushed_checked") == it.get("pushed_at")
                if age <= 2 * ttl:
                    ok = True
                elif push_age is not None and push_age > WINDOW_DAYS["commit_7d"] + POOL_LAG_DAYS \
                        and unchanged:
                    ok = True
                elif push_age is not None and push_age <= WINDOW_DAYS["commit_7d"] + POOL_LAG_DAYS \
                        and unchanged:
                    # 池滞后未让过：池说没 push，但可能是周扫携带的旧值，判不了
                    ok, pending = False, True
                else:
                    ok = False
            else:
                ok = age <= 2 * ttl or (bool(rec.get("pushed_checked"))
                                        and rec.get("pushed_checked") == it.get("pushed_at"))
            if pending:
                c["pending"] += 1
                continue
            c["checked"] += 1
            if ok:
                c["valid"] += 1
    out = {"ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "pool": len(pool), "slo_fresh_ratio": SLO_FRESH_RATIO,
           "tiers": {}, "alerts": []}
    for t, cell in cells.items():
        dims = {}
        for d, c in cell["dims"].items():
            ratio = round(c["valid"] / c["checked"], 3) if c["checked"] else None
            dims[d] = {"ttl": REFRESH_DAYS[t][d],
                       "coverage": round(c["covered"] / cell["n"], 3) if cell["n"] else 0,
                       "age_known": c["checked"],
                       "age_pending": c["pending"],
                       "age_unknown": c["covered"] - c["checked"] - c["pending"],
                       "age_p50": _pctl(c["ages"], 0.5),
                       "age_p95": _pctl(c["ages"], 0.95),
                       "valid_ratio": ratio}
            if ratio is not None and ratio < SLO_FRESH_RATIO:
                out["alerts"].append(f"{t}.{d} 有效占比 {ratio:.3f} < {SLO_FRESH_RATIO}")
        out["tiers"][t] = {"n": cell["n"], "dims": dims}
    return out


def run(args):
    pool_path = Path(args.pool)
    if not pool_path.is_file():
        raise SystemExit(f"pool 不存在：{pool_path}（先跑 collect_intl.py / collect_cn.py）")
    pool = json.loads(pool_path.read_text(encoding="utf-8"))
    st = load_json(STATE, {"version": 1, "items": {}})
    cache = EnrichCacheStore()
    items = st["items"]

    # 零调用修正：滚动窗口衰减 + 派生字段重算（纯本地计算，不花 API）
    n_decay = decay_commit_fields(pool, cache)
    n_days = refresh_derived_days(pool, cache)
    if n_decay or n_days:
        log.info("零调用修正：commit 窗口衰减 %d 仓 · rel_days 重算 %d 仓",
                 n_decay, n_days)

    tiers = ["head", "mid", "tail"] if args.tier == "all" else [args.tier]
    want_dims = [args.only] if args.only else None

    def pick_due() -> list:
        """到期目标：star 降序；已新鲜（无到期维度——含长尾死仓 pushed_at 未变）排除。
        跨窗重取：上一窗盖过时间戳的维度自动退出目标集（天然断点续采）。"""
        out = []
        today = datetime.now(timezone.utc).date()
        for it in sorted(pool, key=lambda x: -(x.get("stars") or 0)):
            fn = it["full_name"]
            rec = items.get(fn) or {}
            status = rec.get("status")
            if status in ("failed", "gone"):
                # 隔离到期复检：平台级故障/空仓不该永久失采（REVIVE_DAYS）
                if not _revive_due(rec, status, today):
                    continue
                rec.pop("status", None)
                rec["fail_count"] = 0
                log.info("%s 隔离复检（原状态 %s）", fn, status)
            tier = tier_of(it.get("stars") or 0, cn=is_cn_item(it))
            if tier not in tiers:
                continue
            changed = (it.get("pushed_at") or "") != rec.get("pushed_checked")
            due = due_dims(rec, tier, changed, cache.get(fn) or {})
            if want_dims:
                due = [d for d in due if d in want_dims]
            if due:
                out.append(fn)
        return out

    # 星层 tail、被 floor 提到 mid 的国产仓（日志口径）
    n_cn = sum(1 for it in pool
               if is_cn_item(it) and tier_of(it.get("stars") or 0) == "tail")

    client = GitHubClient(Budget(max_calls=args.max_calls, max_minutes=args.max_minutes))
    t0 = time.time()
    deadline = t0 + args.max_minutes * 60
    counts = {"done": 0, "failed": 0}
    quarantined = []
    stop_reason = None
    windows = waits = stuck_rounds = 0
    visited = 0                                    # 冒烟用：本次已处理的目标数

    by_fn = {it["full_name"]: it for it in pool}
    targets: list = []                             # deadline 先触发时 summary 不炸
    log.info("层 %s · 维度 %s · 跨窗等待上限 %d 次 · 总时长 %s 分钟",
             tiers, want_dims or "按层", args.wait_windows, args.max_minutes)

    while True:
        if time.time() >= deadline:
            stop_reason = f"总时长达上限 {args.max_minutes} 分钟"
            break
        targets = pick_due()
        if not targets:
            # 无到期目标也要落盘：零调用修正/pick_due 的隔离复检可能已改内存
            atomic_write_json(STATE, st)
            cache.flush()
            break
        # 预算按窗发新的（跨窗续跑时每窗各得一份 max_calls/max_minutes，同 readme）
        client.budget = Budget(max_calls=args.max_calls, max_minutes=args.max_minutes)
        windows += 1
        done0 = counts["done"] + counts["failed"]
        log.info("第 %d 窗：到期目标 %d 项（池 %d · 国产 floor=mid 命中 %d）",
                 windows, len(targets), len(pool), n_cn)
        try:
            for i, fn in enumerate(targets):
                visited += 1
                if args.limit and visited > args.limit:
                    break
                it = by_fn.get(fn, {})
                tier = tier_of(it.get("stars") or 0, cn=is_cn_item(it))
                rec = items.setdefault(fn, {"dims": {}, "fail_count": 0})
                changed = (it.get("pushed_at") or "") != rec.get("pushed_checked")
                dims = due_dims(rec, tier, changed, cache.get(fn) or {})
                if want_dims:
                    dims = [d for d in dims if d in want_dims]
                if not dims:
                    continue
                try:
                    collect_dims(client, fn, cache, tuple(dims), changed)
                    today = datetime.now(timezone.utc).strftime("%Y%m%d")
                    for d in dims:                 # 只给真正采到的维度盖时间戳
                        rec["dims"][d] = today
                    rec["pushed_checked"] = it.get("pushed_at") or ""
                    rec["fail_count"] = 0
                    rec.pop("last_error", None)
                    counts["done"] += 1
                except requests.HTTPError as e:
                    code = getattr(e.response, "status_code", None)
                    if code in (404, 410):          # 仓库已删/私有：标记并隔离
                        rec.update({"status": "gone", "last_error": f"HTTP {code}",
                                    "quarantined_at": _today_compact()})
                        counts["failed"] += 1
                        continue
                    # 其余 HTTP 状态（409 空仓类/5xx 重试耗尽）按仓记振继续——
                    # 绝不 raise：毒仓会每晚卡死在同一位置，阻断其后全部目标
                    rec["fail_count"] += 1
                    rec["last_error"] = f"HTTP {code}"[:200]
                    if rec["fail_count"] >= THREE_STRIKES:
                        rec["status"] = "failed"
                        rec["quarantined_at"] = _today_compact()
                        quarantined.append(fn)
                    counts["failed"] += 1
                    log.warning("%s HTTP %s(%d)：%s", fn, code, rec["fail_count"], str(e)[:60])
                    continue
                except (BudgetOut, QuotaPatienceOut):
                    raise                            # 预算/配额停止不算仓库失败
                except Exception as e:               # noqa: BLE001
                    rec["fail_count"] += 1
                    rec["last_error"] = str(e)[:200]
                    if rec["fail_count"] >= THREE_STRIKES:
                        rec["status"] = "failed"
                        rec["quarantined_at"] = _today_compact()
                        quarantined.append(fn)
                    counts["failed"] += 1
                    log.warning("%s 失败(%d)：%s", fn, rec["fail_count"], str(e)[:80])
                    continue
                if (i + 1) % 50 == 0:
                    atomic_write_json(STATE, st)
                    cache.flush()
                    log.info("进度 %d/%d · %s", i + 1, len(targets), counts)
            if args.limit and visited >= args.limit:
                stop_reason = f"达到 --limit {args.limit}（冒烟）"
            break                                  # 本窗自然扫完且无剩余到期项 → 收尾
        except CoreReserveOut as e:
            # Core 触保底线：按响应头 reset 睡到下一小时窗再续（跨窗推进的关键，
            # 否则 220 分钟预算只跑 ~50 分钟就收工——10-01 实测 4200 调/49.9 分）
            if args.wait_windows <= 0 or waits >= args.wait_windows:
                stop_reason = str(e)
                break
            reset = getattr(e, "reset", None)
            wait_sec = max(5.0, reset - time.time() + 5) if reset else 600.0
            if time.time() + wait_sec > deadline:
                stop_reason = f"{e}，等下一窗需 {wait_sec / 60:.0f} 分钟将超总时长上限"
                break
            waits += 1
            log.warning("Core 触保底线——睡 %.0f 分钟到下一小时窗再续（等待 %d/%d）",
                        wait_sec / 60, waits, args.wait_windows)
            time.sleep(wait_sec)
            continue
        except (BudgetOut, QuotaPatienceOut) as e:
            # 调用数达上限：有进展且允许跨窗 → 发新预算续跑；连续无进展收尾防空转
            progressed = (counts["done"] + counts["failed"]) > done0
            stuck_rounds = 0 if progressed else stuck_rounds + 1
            if args.wait_windows <= 0 or stuck_rounds >= 2:
                stop_reason = str(e) + ("（连续无进展，收尾防空转）"
                                        if stuck_rounds >= 2 else "")
                break
            if time.time() >= deadline:
                stop_reason = f"{e}，已达总时长上限"
                break
            log.info("本窗停止：%s（断点已存，续跑）", e)
            continue
        finally:
            atomic_write_json(STATE, st)
            cache.flush()

    summary = {"tiers": tiers, "dims": want_dims or "per-tier", "targets": len(targets),
               "cn_floor_mid": n_cn,
               "zero_call_fixes": {"commit_decay": n_decay, "rel_days": n_days},
               "counts": counts,
               "api_calls": client.stats_summary()["calls"],
               "not_modified": client.stats_summary()["not_modified"],
               "elapsed_min": round((time.time() - t0) / 60, 1),
               "windows": windows, "waits": waits,
               "stop_reason": stop_reason, "quarantined": quarantined[:20]}
    atomic_write_json(HERE / "state" / "enrich_summary.json", summary)
    health = health_report(pool, cache, items, tiers=tuple(tiers))
    atomic_write_json(HERE / "state" / "enrich_health.json", health)
    for a in health["alerts"]:
        log.warning("staleness SLO：%s", a)
    log.info("==== enrich 完成：%s · API %d 次 · %s 分钟 ====", counts,
             summary["api_calls"], summary["elapsed_min"])
    if stop_reason:
        log.warning("预算停止：%s（断点已存，重跑同命令续）", stop_reason)
    if quarantined:
        log.warning("三振隔离 %d 项：%s", len(quarantined), quarantined[:10])


def main():
    ap = argparse.ArgumentParser(description="信号富集：commit/release/security/contrib/lang")
    ap.add_argument("--pool", default=str(HERE / "data" / "snapshot_latest" / "pool.json"))
    ap.add_argument("--tier", choices=["head", "mid", "tail", "all"], default="head")
    ap.add_argument("--only", choices=DIMS, help="只跑单维度")
    ap.add_argument("--max-calls", type=int, default=4000)
    ap.add_argument("--max-minutes", type=float, default=90.0)
    ap.add_argument("--wait-windows", type=int, default=0,
                    help="Core 触保底线后按响应头 reset 睡到下一小时窗续跑的最多次数"
                         "（0=触线即收尾，旧行为）")
    ap.add_argument("--limit", type=int, default=0,
                    help="本次最多处理 N 个目标（0=不限，冒烟用）")
    ap.add_argument("-v", action="store_true")
    args = ap.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.v else logging.INFO,
                        format="%(asctime)s %(levelname)-6s %(name)s | %(message)s",
                        datefmt="%H:%M:%S")
    run(args)


if __name__ == "__main__":
    main()
