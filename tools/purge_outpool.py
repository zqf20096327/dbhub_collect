# -*- coding: utf-8 -*-
"""出池仓清理（10-02 定稿方案实现）：absent_since 台账 + 宽限 + 备份式删除。

背景：readme_state/enrich_state/enrich_cache 只增不减，出池仓条目与 data/readmes/
正文文件残留。核心风险=出池≠不回来（星标边缘波动、采集抖动假出池），误删代价
=重拉 API+可能重烧解读（贵得多）——故 30 天宽限、回池即清戳。

三模式：
  --stamp   每晚（collect.yml）：维护 state/absent_since.json 台账，出池打戳/
            回池清戳。幂等，不写任何 state 原件（零侵入主流程）。
  （默认）  dry-run：列出到期清单不动盘。
  --apply   执行：md 文件→仓外备份目录（移动非删除）；readme/enrich state
            原件备份后删条目；写 state/purge_list_日期.json manifest。

规则：普通仓 absent ≥30 天；owner ∈ 用户屏蔽清单（exclude_users）或 fn ∈ 仓库
黑名单（exclude_repos——同样在采集落地处即丢弃，物理不可能回池）≥7 天；
readme failed/三振条目整仓跳过（排查线索，state+文件都留）；删 md 前校验安全名
（fn.replace('/','__')）无其他在册仓持有（含大小写不敏感——NTFS/EFCore 教训）；
单次文件上限 500（--limit，防 git 巨量 D 撞 CI 提交步）；解读层缓存永不触碰。

取代 gc_states.py 的每夜 --apply（其判活在 M1 归档后退化为"仅当晚池"=无宽限，
正是本方案要防的假出池误删）。用法：
  python tools/purge_outpool.py --stamp
  python tools/purge_outpool.py                 # dry-run 到期清单
  python tools/purge_outpool.py --apply --limit 500
  python tools/purge_outpool.py --apply --backup-dir D:/x --root D:/sandbox
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

import sys as _sys, pathlib as _pl  # noqa: E401
_ROOT = _pl.Path(__file__).resolve().parents[1]
for _d in (_ROOT, _ROOT / "lib", _ROOT / "collect", _ROOT / "config"):
    _sys.path.insert(0, str(_d))

from gh import atomic_write_json  # noqa: E402
import enrich_store  # noqa: E402  enrich_cache 分片存储（10-09 起，并集读）

GRACE_DAYS = 30
GRACE_BLOCKED = 7
LIMIT_DEFAULT = 500


def _today() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d")


def _age_days(stamp: str) -> int:
    d = datetime.strptime(stamp, "%Y%m%d").replace(tzinfo=timezone.utc)
    return (datetime.now(timezone.utc) - d).days


def _load_users_blocklist(root: Path) -> set[str]:
    """与 pool_core.USER_BLACKLIST 同源：db_profiles 声明 + config/exclude_users.txt。"""
    bl = set()
    try:
        import db_profiles as dp
        bl |= {u.lower() for u in dp.GLOBAL.get("exclude_users") or []}
    except Exception:
        pass
    f = root / "config" / "exclude_users.txt"
    if f.is_file():
        bl |= {ln.strip().lower() for ln in
               f.read_text(encoding="utf-8-sig").splitlines()
               if ln.strip() and not ln.startswith("#")}
    return bl


def _load_repo_blocklist(root: Path) -> set[str]:
    """仓库级静默黑名单（永不回池）：db_profiles 声明（GLOBAL ∪ 各库档案，对齐
    pool_core.BLACKLIST 口径）+ config/exclude_repos.txt。"""
    bl = set()
    try:
        import db_profiles as dp
        bl |= {fn.lower() for fn in dp.GLOBAL.get("exclude_repos") or []}
        bl |= {fn.lower() for p in dp.PROFILES for fn in (p.get("exclude_repos") or [])}
    except Exception:
        pass
    f = root / "config" / "exclude_repos.txt"
    if f.is_file():
        bl |= {ln.strip().lower() for ln in
               f.read_text(encoding="utf-8-sig").splitlines()
               if ln.strip() and not ln.startswith("#")}
    return bl


def _universe(root: Path) -> tuple[dict, dict, dict]:
    """三 state 原件（只读）+ 它们的 fn 全集（enrich_cache 分片并集读）。"""
    def load(p, wrap):
        d = json.loads((root / "state" / p).read_text(encoding="utf-8"))
        return d.get("items", {}) if wrap else d
    rs = load("readme_state.json", True)
    es = load("enrich_state.json", True)
    ec = enrich_store.load_cache(root / "state")
    return rs, es, ec


def do_stamp(root: Path) -> set[str]:
    """台账维护：universe−池 打戳（已有戳保原日期），回池/已消失 清戳。"""
    import pool_store
    if root != _ROOT:                       # 沙箱模式（--root）：重定向池读取基准
        pool_store.DATA_DIR = root / "data"
        pool_store.LIVE_DIR = root / "data" / "live"
    alive = {it["full_name"] for it in pool_store.load_latest("pool")[0]}
    rs, es, ec = _universe(root)
    universe = set(rs) | set(es) | set(ec)
    ledger_p = root / "state" / "absent_since.json"
    ledger = json.loads(ledger_p.read_text(encoding="utf-8")) if ledger_p.is_file() else {}
    today = _today()
    cleared = sum(1 for fn in list(ledger) if fn in alive or fn not in universe)
    for fn in list(ledger):
        if fn in alive or fn not in universe:
            del ledger[fn]
    stamped = 0
    for fn in universe - alive:
        if fn not in ledger:
            ledger[fn] = today
            stamped += 1
    atomic_write_json(ledger_p, ledger)
    print(f"台账：池 {len(alive)} · 在册 {len(universe)} · 出池 {len(ledger)}"
          f"（新打戳 {stamped}，清戳 {cleared}）")
    return alive


def build_plan(root: Path, limit: int) -> dict:
    """到期清单 + 守卫标注。返回 {due, skipped_fail, skipped_collision, ghosts}。"""
    alive = do_stamp(root)                      # 顺带把台账修准
    rs, es, ec = _universe(root)
    ledger = json.loads((root / "state" / "absent_since.json").read_text(encoding="utf-8"))
    users_bl = _load_users_blocklist(root)
    repos_bl = _load_repo_blocklist(root)

    def grace_of(fn: str) -> int:
        # 黑名单（owner 级或仓库级）在采集落地处即丢弃、物理不可能回池——
        # 30 天宽限防的是假出池回池，对它们只剩拖时间，给短宽限
        if fn.split("/", 1)[0].lower() in users_bl or fn.lower() in repos_bl:
            return GRACE_BLOCKED
        return GRACE_DAYS

    kept_holders: dict[str, set[str]] = {}      # 小写安全名 → 持有者 fn 集合（撞名守卫）
    for fn in set(rs) | set(es) | set(ec) | alive:
        kept_holders.setdefault(fn.replace("/", "__").lower() + ".md", set()).add(fn)

    due, skip_fail, skip_coll = [], [], []
    for fn, stamp in sorted(ledger.items(), key=lambda kv: kv[1]):   # 最老优先
        grace = grace_of(fn)
        if _age_days(stamp) < grace:
            continue
        r = rs.get(fn) or {}
        if (r.get("fail_count") or 0) >= 3 or r.get("status") == "failed":
            skip_fail.append(fn)                                  # 排查线索：整仓保留
            continue
        safe = (fn.replace("/", "__") + ".md").lower()
        if len(kept_holders.get(safe) or ()) > 1:
            skip_coll.append((fn, sorted(kept_holders[safe])))     # 共享安全名：整文件保留
            continue
        safe_exact = fn.replace("/", "__") + ".md"
        due.append({"fn": fn, "since": stamp, "grace": grace,
                    "sha": r.get("sha", ""),
                    "file": safe_exact if (root / "data/readmes" / safe_exact).is_file() else ""})
        if sum(1 for d in due if d["file"]) >= limit:
            break                                                 # 文件数触帽即止（state 同步停）

    ghosts = []
    rdir = root / "data" / "readmes"
    if rdir.is_dir():
        state_safe = {fn.replace("/", "__") + ".md"
                      for fn in set(rs) | set(es) | set(ec)}       # 三 state 任一在册都非幽灵
        for f in rdir.iterdir():
            if f.name.endswith(".md") and f.name not in state_safe:
                holders = kept_holders.get(f.name.lower()) or set()
                ghosts.append({"fn": f.name, "holder": ",".join(sorted(holders))})
    return {"due": due, "skip_fail": skip_fail, "skip_coll": skip_coll, "ghosts": ghosts}


def do_apply(root: Path, limit: int, backup_dir: Path | None) -> None:
    plan = build_plan(root, limit)
    due, ghosts = plan["due"], [g for g in plan["ghosts"] if not g["holder"]]
    if not due and not ghosts:
        print("无到期项（dry-run 同款结论），未动任何文件")
        return
    bdir = backup_dir or Path(f"D:/dbhub_purge_backup_{_today()}")
    (bdir / "readmes").mkdir(parents=True, exist_ok=True)
    (bdir / "state").mkdir(parents=True, exist_ok=True)

    rs_p, es_p = (root / "state" / n for n in ("readme_state.json", "enrich_state.json"))
    ec_legacy = root / "state" / "enrich_cache.json"
    for p in (rs_p, es_p):                       # state 原件先备份（git 恢复会丢中间增量）
        if p.is_file():
            shutil.copy2(p, bdir / "state" / p.name)
    ec = enrich_store.load_cache(root / "state")     # 分片 ∪ 旧单文件
    # enrich_cache 备份：有旧单文件备份原件（保字节原貌），已 cutover 则并集落一份
    if ec_legacy.is_file():
        shutil.copy2(ec_legacy, bdir / "state" / "enrich_cache.json")
    else:
        (bdir / "state" / "enrich_cache.json").write_text(
            json.dumps(ec, ensure_ascii=False, indent=1), encoding="utf-8")

    rs = json.loads(rs_p.read_text(encoding="utf-8"))
    es = json.loads(es_p.read_text(encoding="utf-8"))
    ledger = json.loads((root / "state" / "absent_since.json").read_text(encoding="utf-8"))
    manifest, moved = {}, 0
    for d in due:
        fn, safe = d["fn"], d["file"]
        if safe:
            src = root / "data" / "readmes" / safe
            shutil.move(str(src), str(bdir / "readmes" / safe))     # 移动非删除
            moved += 1
        rs.get("items", {}).pop(fn, None)
        es.get("items", es).pop(fn, None)
        ec.pop(fn, None)
        ledger.pop(fn, None)
        manifest[fn] = {**d, "backup": str(bdir / "readmes" / safe) if safe else ""}
    for g in ghosts:                              # 幽灵：state 无记录，直接移出
        src = root / "data" / "readmes" / g["fn"]
        shutil.move(str(src), str(bdir / "readmes" / g["fn"]))
        manifest[g["fn"]] = {"fn": g["fn"], "since": "", "grace": 0,
                             "sha": "", "file": g["fn"], "reason": "ghost",
                             "backup": str(bdir / "readmes" / g["fn"])}
    atomic_write_json(rs_p, rs)
    atomic_write_json(es_p, es)
    enrich_store.save_cache_all(ec, root / "state")
    if ec_legacy.is_file():
        # 过渡期双写收口：旧单文件同步过滤，否则并集读取会把删掉的 fn 复活
        tmp = ec_legacy.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(ec, ensure_ascii=False, indent=1), encoding="utf-8")
        tmp.replace(ec_legacy)
    atomic_write_json(root / "state" / "absent_since.json", ledger)
    atomic_write_json(root / "state" / f"purge_list_{_today()}.json", manifest)
    print(f"清理：到期 {len(due)}（移文件 {moved}）· 幽灵 {len(ghosts)} · "
          f"跳过 failed {len(plan['skip_fail'])} / 撞名 {len(plan['skip_coll'])}")
    print(f"备份与 manifest：{bdir} · state/purge_list_{_today()}.json")


def main() -> None:
    ap = argparse.ArgumentParser(description="出池仓清理（默认 dry-run）")
    ap.add_argument("--stamp", action="store_true", help="只维护 absent_since 台账（每晚）")
    ap.add_argument("--apply", action="store_true", help="执行清理（默认只列清单）")
    ap.add_argument("--limit", type=int, default=LIMIT_DEFAULT, help="单次文件上限")
    ap.add_argument("--backup-dir", type=Path, default=None)
    ap.add_argument("--root", type=Path, default=_ROOT, help="仓库根（沙箱测试用）")
    args = ap.parse_args()
    if args.stamp:
        do_stamp(args.root)
        return
    if args.apply:
        do_apply(args.root, args.limit, args.backup_dir)
        return
    plan = build_plan(args.root, args.limit)
    print(f"到期 {len(plan['due'])}（含文件 {sum(1 for d in plan['due'] if d['file'])}）"
          f"· 幽灵可删 {len([g for g in plan['ghosts'] if not g['holder']])}"
          f"· 跳过 failed {len(plan['skip_fail'])} / 撞名 {len(plan['skip_coll'])}")
    for d in plan["due"][:20]:
        print(f"  {d['since']} 起 {d['grace']}天已满 {d['fn']} {'(有md)' if d['file'] else '(无md)'}")
    print("（dry-run：未动任何文件；--apply 执行，先备份后删）")


if __name__ == "__main__":
    main()
