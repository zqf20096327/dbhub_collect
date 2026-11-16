# -*- coding: utf-8 -*-
"""migrate_flat.py -- 一次性：cards/ 与 archive/ 两级目录（owner/repo.*）搬平（owner__repo.*）

用法（运行位项目卡片/ 目录下）:
  python -I migrate_flat.py --dry-run     # 只数不动
  python -I migrate_flat.py               # 真搬：移动文件 + 重写两份 manifest 的 html 路径 + 删空 owner 目录

幂等：已平铺的目录直接跳过。移动用 os.replace（同盘 rename，不重写内容，OneDrive 友好）。
"""
import argparse, io, json, os, sys

def flat_name(fn, ext=""):
    return fn.replace("/", "__") + ext

def migrate_dir(base, label, dry):
    if not os.path.isdir(base):
        print(f"SKIP {label}: not a dir"); return 0, 0
    moved = skipped_dirs = 0
    for owner in sorted(os.listdir(base)):
        d = os.path.join(base, owner)
        if not os.path.isdir(d): continue
        skipped_dirs += 1
        for f in sorted(os.listdir(d)):
            src = os.path.join(d, f); dst = os.path.join(base, owner + "__" + f)
            if os.path.exists(dst):
                print(f"  CONFLICT skip (dst exists): {dst}"); continue
            if not dry: os.replace(src, dst)
            moved += 1
        if not dry:
            try: os.rmdir(d)
            except OSError as ex: print(f"  WARN rmdir {d}: {ex}")
    print(f"{label}: moved={moved} owner-dirs={skipped_dirs}{' (dry-run)' if dry else ''}")
    return moved, skipped_dirs

def fix_manifest(mp, base_label, dry):
    """manifest 条目 html 路径直接按 fn 键重建为 {base}/owner__repo.html（不解析旧值，幂等）。"""
    if not os.path.exists(mp): return
    doc = json.load(io.open(mp, encoding="utf-8"))
    cards = doc.get("cards") or {}
    for fn, e in cards.items():
        if isinstance(e, dict) and e.get("html"):
            e["html"] = f"{base_label}/{flat_name(fn, '.html')}"
    if not dry:
        io.open(mp, "w", encoding="utf-8", newline="\n").write(json.dumps(doc, ensure_ascii=False, indent=1))
    print(f"{base_label} manifest: fixed {len(cards)} html paths{' (dry-run)' if dry else ''}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    here = os.path.dirname(os.path.abspath(__file__))
    for sub in ("cards", "archive"):
        migrate_dir(os.path.join(here, sub), sub, a.dry_run)
        fix_manifest(os.path.join(here, sub, "manifest.json"), sub, a.dry_run)
    if not a.dry_run: print("OK migrate done")
    return 0

if __name__ == "__main__":
    sys.exit(main())
