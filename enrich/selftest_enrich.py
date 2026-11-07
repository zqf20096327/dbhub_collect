# -*- coding: utf-8 -*-
"""enrich 离线自检：滚动窗口衰减 / 派生字段重算 / 隔离复检 / 正文时间窗。

零网络、零磁盘写（假 cache）。跑法：python enrich/selftest_enrich.py（退出码 0=全绿）

覆盖 11-07 修复契约：
  - commit_7d/90d 是滚动窗口计数，无 push 超过窗口 ⇒ 真值 0（不再被 push 闸门冻结）
  - rel_days / rel_n90 是派生值，按今天重算而不是吃采集时快照
  - 三振/404 隔离到期复检（平台故障、空仓不该永久失采）
  - release 正文摘要改 90 天窗 + 最多 10 条（mid 层 30 天节奏不丢正文）
  - security 按通告史分档、TTL 收紧后的档位锁定、staleness SLO 有效性口径
"""
from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
for _d in (ROOT, ROOT / "lib", ROOT / "config", ROOT / "enrich"):
    if str(_d) not in sys.path:
        sys.path.insert(0, str(_d))

import enrich  # noqa: E402

FAILS: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    print(f"[{'PASS' if cond else 'FAIL'}] {name}" + (f"  {detail}" if detail and not cond else ""))
    if not cond:
        FAILS.append(name)


class FakeCache(dict):
    """EnrichCacheStore 的最小替身：只需 get/setdefault/touch 语义。"""

    def __init__(self, data):
        super().__init__(data)
        self.dirty: set[str] = set()

    def touch(self, key) -> None:
        self.dirty.add(key)


TODAY = date(2026, 11, 7)


def test_decay_commit() -> None:
    """滚动窗口衰减：push_age 必须超过「窗口 + 池滞后(8)」才归零。"""
    pool = [
        {"full_name": "a/old", "pushed_at": "2025-01-01"},      # 远超窗口
        {"full_name": "a/new", "pushed_at": "2026-11-07"},      # 今天推过
        {"full_name": "a/edge16", "pushed_at": "2026-10-22"},   # 16 天 → 7d 归零、90d 保留
        {"full_name": "a/edge15", "pushed_at": "2026-10-23"},   # 15 天：未过滞后线，不归零
        {"full_name": "a/edge8", "pushed_at": "2026-10-30"},    # 8 天：池滞后未让过，不归零
        {"full_name": "a/fresh_ts", "pushed_at": "2025-01-01"},  # 值刚采过（dim_ts 今天）
        {"full_name": "a/nopush"},                              # 无 pushed_at：不动
    ]
    cache = FakeCache({
        "a/old": {"commit_7d": 3, "commit_90d": 9, "dim_ts": {"commit": "20260101"}},
        "a/new": {"commit_7d": 2, "commit_90d": 5},
        "a/edge16": {"commit_7d": 1, "commit_90d": 4, "dim_ts": {"commit": "20260901"}},
        "a/edge15": {"commit_7d": 1, "commit_90d": 4, "dim_ts": {"commit": "20260901"}},
        "a/edge8": {"commit_7d": 1, "commit_90d": 4},
        "a/fresh_ts": {"commit_7d": 5, "commit_90d": 5,
                       "dim_ts": {"commit": "20261107"}},
        "a/nopush": {"commit_7d": 1, "commit_90d": 4},
    })
    fixed = enrich.decay_commit_fields(pool, cache, today=TODAY)
    check("衰减：pushed 远超窗口的仓被归零", cache["a/old"]["commit_7d"] == 0
          and cache["a/old"]["commit_90d"] == 0 and fixed == 2)
    check("衰减：近期推送的仓不动", cache["a/new"]["commit_7d"] == 2
          and cache["a/new"]["commit_90d"] == 5)
    check("衰减：16 天前只归零 7d、保留 90d",
          cache["a/edge16"]["commit_7d"] == 0 and cache["a/edge16"]["commit_90d"] == 4)
    check("衰减：15 天在池滞后线内不归零（防周扫携带误杀）",
          cache["a/edge15"]["commit_7d"] == 1)
    check("衰减：8 天不归零（org 周扫携带可滞后 7 天）",
          cache["a/edge8"]["commit_7d"] == 1)
    check("衰减：值刚采过不推导（dim_ts 未过期）",
          cache["a/fresh_ts"]["commit_7d"] == 5)
    check("衰减：无 pushed_at 不推导（不能把未知当 0）",
          cache["a/nopush"]["commit_7d"] == 1)
    check("衰减：dim_ts 不被伪装成今天（语义仍是最后 API 采集）",
          cache["a/old"]["dim_ts"]["commit"] == "20260101")
    check("衰减：只标脏真正改过的桶", cache.dirty == {"a/old", "a/edge16"}, str(cache.dirty))


def test_derived_days() -> None:
    """rel_days / rel_n90 按今天重算；幂等。"""
    pool = [{"full_name": "a/r"}, {"full_name": "a/none"}]
    cache = FakeCache({
        "a/r": {"rel_pub": "2026-10-20", "rel_days": 1,       # 采集时是 1，今天应为 18
                "rel_dates": ["2026-10-20", "2026-08-01"],     # 后者已出 90 天窗
                "rel_n90": 2},
        "a/none": {"rel_none": True},
    })
    n = enrich.refresh_derived_days(pool, cache, today=TODAY)
    check("派生：rel_days 按今天重算", cache["a/r"]["rel_days"] == 18 and n == 1)
    check("派生：rel_n90 按 90 天窗重算（过期发版不再计入）",
          cache["a/r"]["rel_n90"] == 1)
    check("派生：无 rel_pub 不产出 rel_days", "rel_days" not in cache["a/none"])
    check("派生：同日重跑幂等", enrich.refresh_derived_days(pool, cache, today=TODAY) == 0)


def test_security_cadence() -> None:
    """security 按通告史分档：有史加密，零历史维持基础层值（sec_n 来自 cache）。"""
    check("安全分档：head 有史 7 天", enrich._security_days({}, "head", {"sec_n": 2}) == 7)
    check("安全分档：mid 有史 14 天", enrich._security_days({}, "mid", {"sec_n": 1}) == 14)
    check("安全分档：tail 有史 30 天", enrich._security_days({}, "tail", {"sec_n": 1}) == 30)
    check("安全分档：零历史走基础值（30/90/180）",
          [enrich._security_days({}, t, {}) for t in ("head", "mid", "tail")] == [30, 90, 180])
    rec = {"dims": {"security": "20261020"}}          # 18 天前采过
    check("安全分档：有史仓 18 天已到期",
          "security" in enrich.due_dims(rec, "head", False, {"sec_n": 1}))
    check("安全分档：零历史仓 18 天未到期",
          "security" not in enrich.due_dims(rec, "head", False, {}))


def test_ttl_policy() -> None:
    """TTL 收紧后的档位锁定（防回退）。"""
    rd = enrich.REFRESH_DAYS
    check("TTL：head commit 3 天 / release 每晚",
          rd["head"]["commit"] == 3 and rd["head"]["release"] == 1)
    check("TTL：mid commit/release 14 天",
          rd["mid"]["commit"] == 14 and rd["mid"]["release"] == 14)
    check("TTL：tail 仍不采 commit", rd["tail"]["commit"] is None)


def test_health() -> None:
    """staleness SLO：状态量维度没 push 不算陈旧；采集后有 push 算陈旧。"""
    pool = [{"full_name": "a/ok", "stars": 1500, "pushed_at": "2026-11-07"},
            {"full_name": "a/bad", "stars": 1500, "pushed_at": "2026-11-07"},
            {"full_name": "a/pending", "stars": 1500, "pushed_at": "2026-10-28"}]
    all_ts = {"commit": "20261107", "release": "20261107", "security": "20261107",
              "contrib": "20261107", "lang": "20261107"}
    items = {"a/ok": {"dims": dict(all_ts), "pushed_checked": "2026-11-07"},
             "a/bad": {"dims": dict(all_ts), "pushed_checked": "2026-10-01"},  # 采集后又推送过
             "a/pending": {"dims": dict(all_ts), "pushed_checked": "2026-10-28"}}
    cache = {"a/ok": {"dim_ts": all_ts},
             "a/bad": {"dim_ts": dict(all_ts, release="20261001")},
             "a/pending": {"dim_ts": dict(all_ts, commit="20261028")}}   # 池滞后窗内，判不了
    rep = enrich.health_report(pool, cache, items, today=TODAY)
    dims = rep["tiers"]["head"]["dims"]
    check("SLO：head 层仓数", rep["tiers"]["head"]["n"] == 3)
    check("SLO：覆盖率满", dims["release"]["coverage"] == 1.0)
    check("SLO：commit 池滞后窗内的记录归入待定、不算陈旧",
          dims["commit"]["valid_ratio"] == 1.0 and dims["commit"]["age_pending"] == 1)
    check("SLO：release 有 push 未刷新 → 有效占比 0.667",
          dims["release"]["valid_ratio"] == 0.667)
    check("SLO：低于 95% 进告警", any("head.release" in a for a in rep["alerts"]))


def test_etag_paths() -> None:
    """ETag 条件请求：200 落新值+记忆 etag；304 保留旧值不重解析。"""
    from datetime import datetime, timedelta, timezone
    now = datetime.now(timezone.utc)
    d5 = (now - timedelta(days=5)).strftime("%Y-%m-%dT00:00:00Z")
    d30 = (now - timedelta(days=30)).strftime("%Y-%m-%dT00:00:00Z")

    class FakeClient:
        def __init__(self, rel, adv=(200, [], "etag-s")):
            self.rel, self.adv = rel, adv

        def releases_conditional(self, fn, etag, per_page=30):
            return self.rel

        def advisories_conditional(self, fn, etag, per_page=30):
            return self.adv

    # 200：新版本进 rel_ver，90 天内日期进 rel_dates，正文与旧摘要合并
    cache = FakeCache({"a/r": {"rel_ver": "v1", "rel_pub": d30[:10], "rel_days": 30,
                               "rel_notes": [{"t": "v1", "d": d30[:10], "n": "old"}]}})
    sig = enrich.collect_dims(FakeClient((200, [
        {"tag_name": "v2", "published_at": d5, "body": "added MySQL support"},
        {"tag_name": "v1", "published_at": d30, "body": "old body"}], "etag-r")),
        "a/r", cache, ("release",), False)
    check("ETag：200 更新版本与 etag", sig["rel_ver"] == "v2"
          and sig["etag"]["release"] == "etag-r")
    check("ETag：90 天内发版日期落 rel_dates", sig["rel_dates"] == [d5[:10], d30[:10]])
    check("ETag：新正文与旧摘要合并（v1 覆盖、v2 新增）",
          [n["t"] for n in sig["rel_notes"]] == ["v2", "v1"])

    # 304：值全部保留，不产生 rel_dates/正文重写
    cache = FakeCache({"a/r": {"rel_ver": "v1", "rel_pub": d30[:10], "rel_n90": 3,
                               "etag": {"release": "etag-r"}}})
    sig = enrich.collect_dims(FakeClient((304, None, "etag-r")),
                              "a/r", cache, ("release",), False)
    check("ETag：304 保留旧版本与 rel_n90", sig["rel_ver"] == "v1"
          and sig["rel_n90"] == 3 and "rel_dates" not in sig)

    # security 304 同样保留通告摘要
    cache = FakeCache({"a/r": {"sec_n": 2, "sec_worst": "high",
                               "etag": {"security": "etag-s"}}})
    sig = enrich.collect_dims(FakeClient((200, [], "x"), (304, None, "etag-s")),
                              "a/r", cache, ("security",), False)
    check("ETag：security 304 保留旧通告", sig["sec_n"] == 2
          and sig["sec_worst"] == "high")


def test_revive() -> None:
    """隔离复检：failed 90 天 / gone 180 天；无戳老记录给一次机会。"""
    check("复检：failed 89 天未到期",
          not enrich._revive_due({"quarantined_at": "20260810"}, "failed", TODAY))
    check("复检：failed 满 90 天放行",
          enrich._revive_due({"quarantined_at": "20260809"}, "failed", TODAY))
    check("复检：gone 179 天未到期",
          not enrich._revive_due({"quarantined_at": "20260512"}, "gone", TODAY))
    check("复检：gone 满 180 天放行",
          enrich._revive_due({"quarantined_at": "20260511"}, "gone", TODAY))
    check("复检：无 quarantined_at 的老记录给一次机会",
          enrich._revive_due({}, "failed", TODAY))


def test_notes_window() -> None:
    """正文摘要：90 天窗、最多 10 条、按 tag 合并去重。"""
    rels = [
        {"tag_name": "v3", "published_at": "2026-11-01", "body": "dropped MySQL support"},
        {"tag_name": "v2", "published_at": "2026-08-01", "body": "too old"},   # 98 天前
        {"tag_name": "v1", "published_at": "2026-10-01", "body": ""},          # 空正文
    ]
    notes = enrich._release_notes(rels, today=TODAY)
    check("正文窗：只收 90 天内且有正文的", [n["t"] for n in notes] == ["v3"], str(notes))
    many = [{"tag_name": f"v{i}", "published_at": f"2026-10-{i:02d}", "body": "x"}
            for i in range(1, 13)]
    check("正文窗：封顶 10 条", len(enrich._release_notes(many, today=TODAY)) == 10)
    merged = enrich._merge_notes(
        [{"t": "v1", "d": "2026-09-01", "n": "old"}],
        [{"t": "v1", "d": "2026-09-01", "n": "new"}, {"t": "v2", "d": "2026-10-01", "n": "x"}])
    check("正文窗：合并按 tag 去重（新覆盖旧）、日期降序",
          [m["t"] for m in merged] == ["v2", "v1"] and merged[1]["n"] == "new", str(merged))


def main() -> int:
    test_decay_commit()
    test_derived_days()
    test_security_cadence()
    test_ttl_policy()
    test_health()
    test_etag_paths()
    test_revive()
    test_notes_window()
    print()
    if FAILS:
        print(f"==== 自检失败 {len(FAILS)} 项 ====")
        return 1
    print("==== 自检全绿 ====")
    return 0


if __name__ == "__main__":
    sys.exit(main())
