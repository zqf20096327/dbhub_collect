# -*- coding: utf-8 -*-
"""一次性清理：用户黑名单（config/exclude_users.txt）在全仓数据里的存量残留。

用法（在仓库根目录）：
  python tools/purge_blocklist_residue.py --dry-run       # 只读预览，不改任何文件
  python tools/purge_blocklist_residue.py                 # 真删（原件先备份到仓外 D:/dbhub_purge_backup_20261003/）
  python tools/purge_blocklist_residue.py --check-actions # 查 GitHub Actions 是否有在跑/排队的 run（推送前用）

清理范围（10-03 全量扫描实测的残留）：
  1. state/interp_state.json      items 黑名单条目（9 条，含 failed）
  2. state/interp_cache.json      仅被黑名单条目引用的孤儿 sha（7 条解读缓存；
                                  与存活仓共用 sha 的缓存保留，不影响合法仓）
  3. state/manual_review.json     failed 里的黑名单 fn（14 条）
  4. data/snapshot_*/pool*.json   历史快照池里的黑名单仓（0925/0927/0929 共 5 个文件 62 条）
  5. data/snapshot_*/meta/*.json  fn 形键的递归清理（0926 的 release_state/security）
  6. _purge_backup_1001/、_remote_sync_1001/  本地未跟踪备份目录：删黑名单 readme 文件 + json 递归清理
  7. 写 state/purge_list_20261003.json 清单；删扫描临时件 state/_scan_blocklist_hits.json
  8. 全量复扫验证键级零残留（正文级子串提及只报告不计错，存在误报可能）

注意：git 历史里仍有旧版本数据；彻底抹除需重写历史，不做。
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BACKUP_DIR = Path("D:/dbhub_purge_backup_20261003")
DRY = "--dry-run" in sys.argv
TODAY = "20261003"

sys.path.insert(0, str(ROOT / "lib"))
import interp_store as ist  # noqa: E402  interp_cache 分片存储（10-06 起）
import enrich_store as est  # noqa: E402  enrich_cache 分片存储（10-09 起）


def load_blocklist():
    bl = set()
    for ln in open(ROOT / "config" / "exclude_users.txt", encoding="utf-8-sig"):
        ln = ln.strip()
        if ln and not ln.startswith("#"):
            bl.add(ln.lower())
    return bl


BL = load_blocklist()


def owner_blocked(fn):
    return isinstance(fn, str) and "/" in fn and fn.split("/", 1)[0].lower() in BL


def is_fn_key(k):
    return isinstance(k, str) and "/" in k and " " not in k and len(k) < 200


def stem_owners(stem):
    outs, parts = set(), stem.split("__")
    acc = parts[0]
    outs.add(acc)
    for p in parts[1:]:
        acc += "__" + p
        outs.add(acc)
    return outs


def sniff_write(path, obj, backup_rel=None):
    """按原文件的缩进/换行风格原子重写；改动前把原件备份到仓外。"""
    path = Path(path)
    if backup_rel:
        dst = BACKUP_DIR / backup_rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        if not dst.exists():
            shutil.copy2(path, dst)
    if DRY:
        return
    raw_head = path.read_bytes()[:400].decode("utf-8", "ignore")
    lines = [l for l in raw_head.splitlines() if l.strip()]
    indent = len(lines[1]) - len(lines[1].lstrip()) if len(lines) > 1 else 1
    nl = "\r\n" if "\r\n" in raw_head else "\n"
    data = json.dumps(obj, ensure_ascii=False, indent=indent)
    if path.read_bytes()[-1:] in (b"\n", b"\r"):
        data += nl
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
        f.write(data.replace("\n", nl))
    os.replace(tmp, path)


def clean_tree(obj):
    """递归删 fn 形黑名单键/列表项（含 full_name 字典项），返回删除数。"""
    n = 0
    if isinstance(obj, dict):
        for k in [k for k in obj if is_fn_key(k) and owner_blocked(k)]:
            del obj[k]
            n += 1
        for v in obj.values():
            n += clean_tree(v)
    elif isinstance(obj, list):
        keep = []
        for it in obj:
            if isinstance(it, str) and is_fn_key(it) and owner_blocked(it):
                n += 1
                continue
            if isinstance(it, dict) and owner_blocked(it.get("full_name")):
                n += 1
                continue
            keep.append(it)
        obj[:] = keep
        for it in obj:
            n += clean_tree(it)
    return n


def main():
    log = []
    manifest = {"date": TODAY, "blocklist_size": len(BL), "removed": {}}

    # --- 1. interp_state：删条目，收集黑名单 sha ---
    p = ROOT / "state/interp_state.json"
    d = json.load(open(p, encoding="utf-8"))
    removed_items = {fn: v for fn, v in d["items"].items() if owner_blocked(fn)}
    keep_shas = {v.get("sha") for fn, v in d["items"].items() if fn not in removed_items}
    bad_shas = {v.get("sha") for v in removed_items.values() if v.get("sha")}
    if removed_items:
        d["items"] = {fn: v for fn, v in d["items"].items() if fn not in removed_items}
        sniff_write(p, d, "state/interp_state.json")
    log.append(f"interp_state: 删 {len(removed_items)} 条 -> 剩 {len(d['items'])}")
    manifest["removed"]["interp_state"] = sorted(removed_items)

    # --- 2. interp_cache：只删孤儿 sha（存活仓共用的保留）；分片存储走 interp_store ---
    ic = ist.load_cache()
    orphan = sorted(s for s in bad_shas if s in ic and s not in keep_shas)
    if orphan:
        bdst = BACKUP_DIR / "interp_cache_shards"
        if not DRY and ist.SHARD_DIR.is_dir() and not bdst.exists():
            shutil.copytree(ist.SHARD_DIR, bdst)   # 改前备份分片目录到仓外（对齐 sniff_write 语义）
        for s in orphan:
            del ic[s]
        if not DRY:
            ist.save_cache_all(ic)
            if ist.LEGACY.is_file():   # 过渡期双写：旧单文件同步过滤，否则并集读取会把删掉的 sha 复活
                tmp = ist.LEGACY.with_suffix(".json.tmp")
                tmp.write_text(json.dumps(ic, ensure_ascii=False, indent=1), encoding="utf-8")
                tmp.replace(ist.LEGACY)
    shared = len(bad_shas & keep_shas)
    absent = len(bad_shas) - len(orphan) - shared
    log.append(f"interp_cache: 删 {len(orphan)} 条孤儿 sha -> 剩 {len(ic)}"
               f"（黑名单 sha：{absent} 条本就不在缓存，{shared} 条与存活仓共用保留）")
    manifest["removed"]["interp_cache_shas"] = orphan

    # --- 3. manual_review ---
    p = ROOT / "state/manual_review.json"
    d = json.load(open(p, encoding="utf-8"))
    n0 = sum(len(v) if isinstance(v, list) else 0 for v in d.values())
    clean_tree(d)
    n1 = sum(len(v) if isinstance(v, list) else 0 for v in d.values())
    if n0 != n1:
        sniff_write(p, d, "state/manual_review.json")
    log.append(f"manual_review: 删 {n0 - n1} 条")
    manifest["removed"]["manual_review"] = n0 - n1

    # --- 4+5. 历史快照池 + meta（含 fn 键，含轮转副本；无改动的文件不碰） ---
    pool_n, meta_n = 0, 0
    for pf in sorted(ROOT.glob("data/snapshot_*/pool*.json")):
        d = json.load(open(pf, encoding="utf-8"))
        n = clean_tree(d)
        if n:
            pool_n += n
            sniff_write(pf, d, str(pf.relative_to(ROOT)))
    for mf in sorted(ROOT.glob("data/snapshot_*/meta/*.json")):
        d = json.load(open(mf, encoding="utf-8"))
        by_repo = d.get("by_repo") if isinstance(d, dict) else None
        count_synced = isinstance(by_repo, dict) and d.get("count") == len(by_repo)
        n = clean_tree(d)
        if n:
            meta_n += n
            if count_synced:
                d["count"] = len(d["by_repo"])
            sniff_write(mf, d, str(mf.relative_to(ROOT)))
    log.append(f"历史快照池: 删 {pool_n} 条；meta: 删 {meta_n} 条")
    manifest["removed"]["snapshot_pools"] = pool_n
    manifest["removed"]["snapshot_meta"] = meta_n

    # --- 6. 本地备份目录（未跟踪）：黑名单 readme 文件删除 + json 递归清理 ---
    bk_md, bk_json = 0, 0
    for bd in (ROOT / "_purge_backup_1001", ROOT / "_remote_sync_1001"):
        if not bd.is_dir():
            continue
        for f in bd.rglob("*"):
            if f.is_file():
                if f.suffix == ".md" and stem_owners(f.stem) & BL:
                    if not DRY:
                        dst = BACKUP_DIR / str(f.relative_to(ROOT))
                        dst.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(f, dst)
                        f.unlink()
                    bk_md += 1
                elif f.suffix == ".json":
                    try:
                        d = json.load(open(f, encoding="utf-8"))
                    except Exception:
                        continue
                    extra = {k for k in orphan if isinstance(d, dict) and k in d}
                    for k in extra:
                        del d[k]
                    n = clean_tree(d) + len(extra)
                    if n:
                        bk_json += n
                        sniff_write(f, d)
    log.append(f"备份目录: 删 readme 文件 {bk_md} 个、json 条目 {bk_json} 条")
    manifest["removed"]["backup_dirs"] = {"md_files": bk_md, "json_entries": bk_json}

    # --- 7. 清单落盘 + 清扫描临时件 ---
    if not DRY:
        (ROOT / f"state/purge_list_{TODAY}.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
        tmp_scan = ROOT / "state/_scan_blocklist_hits.json"
        if tmp_scan.exists():
            tmp_scan.unlink()

    # --- 8. 全量复扫验证（键级必须为 0） ---
    residue = {}
    hits = [f for f in os.listdir(ROOT / "data/readmes") if stem_owners(f[:-3] if f.endswith(".md") else f) & BL]
    if hits:
        residue["data/readmes"] = len(hits)
    for sp in ["state/readme_state.json", "state/interp_state.json", "state/enrich_state.json",
               "state/enrich_cache.json", "state/db_scan.json", "state/db_scan.v2.json"]:
        if sp == "state/enrich_cache.json":            # 10-09 起分片（cutover 后单文件已删）：并集读
            items = est.load_cache()
        else:
            d = json.load(open(ROOT / sp, encoding="utf-8"))
            items = d.get("items", d) if isinstance(d, dict) else {}
        n = sum(1 for k in items if owner_blocked(k))
        if n:
            residue[sp] = n
    for pf in ROOT.glob("data/snapshot_*/pool*.json"):
        d = json.load(open(pf, encoding="utf-8"))
        n = clean_tree_count_only(d)
        if n:
            residue[str(pf.relative_to(ROOT))] = n
    for mf in ROOT.glob("data/snapshot_*/meta/*.json"):
        try:
            d = json.load(open(mf, encoding="utf-8"))
        except Exception:
            continue
        n = clean_tree_count_only(d)
        if n:
            residue[str(mf.relative_to(ROOT))] = n
    mr = json.load(open(ROOT / "state/manual_review.json", encoding="utf-8"))
    n = sum(1 for v in mr.values() if isinstance(v, list) for fn in v if owner_blocked(fn))
    if n:
        residue["state/manual_review.json"] = n

    # 正文级子串提及（仅报告；登录名可能是别的词的子串，如 htmle~htmleditor）
    mention = []
    t = json.dumps(ist.load_cache(), ensure_ascii=False).lower()
    hit = [u for u in BL if u in t]
    if hit:
        mention.append(("interp_cache(union)", hit))

    print("=" * 60)
    for l in log:
        print(" ", l)
    print("=" * 60)
    if DRY:
        print("[dry-run] 以上为预览，未改任何文件；复扫必显示原样残留，跳过验证。")
        print("[dry-run] 去掉 --dry-run 真正执行（原件先备份到仓外）。")
        return
    print(f"清单已写 state/purge_list_{TODAY}.json；原件备份在 {BACKUP_DIR}")
    if residue:
        print("!! 键级残留未清零，请检查：", json.dumps(residue, ensure_ascii=False))
        sys.exit(1)
    print("复扫验证：键级零残留 ✓")
    if mention:
        print("（仅提示）存活解读正文里出现屏蔽名字符串：", mention, "——多为子串误报，未改动")


def clean_tree_count_only(obj):
    n = 0
    if isinstance(obj, dict):
        for k, v in obj.items():
            if is_fn_key(k) and owner_blocked(k):
                n += 1
            else:
                n += clean_tree_count_only(v)
    elif isinstance(obj, list):
        for it in obj:
            if isinstance(it, str) and is_fn_key(it) and owner_blocked(it):
                n += 1
            elif isinstance(it, dict) and owner_blocked(it.get("full_name")):
                n += 1
            else:
                n += clean_tree_count_only(it)
    return n


def check_actions():
    """推送前确认没有在跑/排队的 workflow run，避免撞车（09-29 教训）。"""
    env = {}
    for ln in open(ROOT / ".env", encoding="utf-8-sig"):
        ln = ln.strip()
        if "=" in ln and not ln.startswith("#"):
            k, v = ln.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    tok = env.get("GITHUB_TOKEN")
    if not tok:
        print("没找到 GITHUB_TOKEN（.env）")
        sys.exit(1)
    url = subprocess.run(["git", "config", "--get", "remote.origin.url"],
                         capture_output=True, text=True).stdout.strip()
    m = re.search(r"[:/]([^/:]+)/([^/.]+?)(?:\.git)?$", url)
    repo = f"{m.group(1)}/{m.group(2)}"
    api = f"https://api.github.com/repos/{repo}/actions/runs?per_page=15"
    for attempt in range(3):
        try:
            req = urllib.request.Request(api, headers={
                "Authorization": f"Bearer {tok}", "Accept": "application/vnd.github+json"})
            runs = json.load(urllib.request.urlopen(req, timeout=30))["workflow_runs"]
            break
        except Exception as e:
            if attempt == 2:
                print("查 Actions 失败：", e, "（github.com 间歇阻断，稍后重试）")
                sys.exit(1)
    live = [r for r in runs if r["status"] in ("queued", "in_progress")]
    if not live:
        print("当前没有在跑/排队的 run，可以 push ✓")
        return
    for r in live:
        print(f"仍在跑: {r['name']}  status={r['status']}  created={r['created_at']}  {r['html_url']}")
    print("等它跑完再 push，否则会撞推送。")


if __name__ == "__main__":
    if "--check-actions" in sys.argv:
        check_actions()
    else:
        main()
