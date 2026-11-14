# -*- coding: utf-8 -*-
"""daily_cards.py v1.0 -- 名片日更一键：建缓存 → 擂台批跑(按需) → 全量出卡

把日更三条命令并成一条（2026-11-14 用户令「合并，并测试」）：
  1. build_cache --steps all          索引/趋势/提及三缓存（blob 全在本地约 1 分钟）
  2. arena_batch --min-stars 0        只在擂台输入变了才跑（池/解读两层分片/db_scan/absent/算法版本，
                                      指纹并进 cache/arena_inputs.json；对不上=重跑，永远安全侧）
  3. gen_cards                        全量出卡（指纹增量，全量约 30 秒/空跑约 6 秒）

用法:
  python -I daily_cards.py                # 日更
  python -I daily_cards.py --dry-run      # 只打印擂台决策与计划，不执行
  python -I daily_cards.py --force-arena  # 无视指纹强制重跑擂台
  python -I daily_cards.py --skip-arena   # 跳过擂台步（优先于 --force-arena）
  python -I daily_cards.py --days 30      # 趋势窗口（默认 30，build_cache 会补当天点）
  python -I daily_cards.py --selftest

前置：先同步仓库（当晚池快照 commit 之后才建趋势，规则清单 30 条）。
"""
import argparse, datetime, glob, hashlib, io, json, os, subprocess, sys, time

VER = "daily_cards/1.0"
ROOT = "D:/dbhub_collect"
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = HERE + os.sep + "cache"
ARENA_CACHE = CACHE + os.sep + "arena_all.json"
SIDECAR = CACHE + os.sep + "arena_inputs.json"
PY = sys.executable or "python"

ARENA_FILES = ["data/live/pool.ndjson", "state/interp_state.json",
               "state/db_scan.v2.json", "state/absent_since.json"]      # arena_select.load_layers + select 的全部输入
ARENA_GLOBS = ["state/interp/domain_tags/shards/*.json", "state/interp/judge/shards/*.json"]

def now(): return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
def loadj(p): return json.load(io.open(p, encoding="utf-8"))

def md5_file(p):
    h = hashlib.md5()
    with io.open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def inputs_fp(root=ROOT, files=None, globs=None):
    """擂台输入指纹：内容 md5（不看 mtime，git 收敛不触发假重跑）；globs 排序后并序，换机器可复算。"""
    files = ARENA_FILES if files is None else files
    globs = ARENA_GLOBS if globs is None else globs
    parts = []
    for rel in files:
        p = os.path.join(root, *rel.split("/"))
        parts.append((rel, md5_file(p)))
    for pat in globs:
        for p in sorted(glob.glob(os.path.join(root, *pat.split("/")))):
            parts.append((os.path.relpath(p, root).replace(os.sep, "/"), md5_file(p)))
    h = hashlib.md5()
    for name, fp in parts:
        h.update((name + ":" + fp + "\n").encode())
    return h.hexdigest()[:16], len(parts)

def arena_decision(side, cur_fp, cur_algo, arena_built_at, force=False, skip=False):
    """擂台要不要重跑：返回 (run, reason)。任何对不上=重跑（安全侧，同规则清单 39 条回退哲学）。"""
    if skip: return False, "flag--skip-arena"
    if force: return True, "flag--force-arena"
    if not side: return True, "no-sidecar"
    if arena_built_at is None: return True, "arena-cache-missing"
    if side.get("fp") != cur_fp: return True, "inputs-changed"
    if side.get("algorithm") != cur_algo: return True, "algorithm-changed"
    if side.get("arena_built_at") != arena_built_at: return True, "arena-cache-replaced"
    return False, "unchanged"

def current_algorithm():
    sys.path.insert(0, ROOT + "/tools")
    import arena_select as az
    return az.VER

def run_step(name, args):
    print(f"\n=== [{name}] python -I {' '.join(args)}", flush=True)
    t0 = time.time()
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    p = subprocess.run([PY, "-I"] + args, cwd=HERE, env=env)
    print(f"=== [{name}] exit={p.returncode} in {time.time()-t0:.1f}s", flush=True)
    if p.returncode != 0:
        sys.exit(f"FAIL daily_cards: step {name} exited {p.returncode}, later steps skipped")
    return time.time() - t0

def _selftest():
    d = arena_decision
    assert d(None, "f1", "a1", "T1") == (True, "no-sidecar")
    assert d({}, "f1", "a1", "T1") == (True, "no-sidecar")
    assert d({"fp": "f1", "algorithm": "a1", "arena_built_at": "T1"}, "f1", "a1", "T1") == (False, "unchanged")
    assert d({"fp": "f1", "algorithm": "a1", "arena_built_at": "T1"}, "f2", "a1", "T1") == (True, "inputs-changed")
    assert d({"fp": "f1", "algorithm": "a1", "arena_built_at": "T1"}, "f1", "a2", "T1") == (True, "algorithm-changed")
    assert d({"fp": "f1", "algorithm": "a1", "arena_built_at": "T1"}, "f1", "a1", "T2") == (True, "arena-cache-replaced")
    assert d({"fp": "f1", "algorithm": "a1", "arena_built_at": "T1"}, "f1", "a1", None) == (True, "arena-cache-missing")
    assert d({"fp": "f1", "algorithm": "a1", "arena_built_at": "T1"}, "f1", "a1", "T1", force=True) == (True, "flag--force-arena")
    assert d(None, "f1", "a1", "T1", skip=True) == (False, "flag--skip-arena")     # skip 优先于一切
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        os.makedirs(os.path.join(td, "state", "x", "shards"))
        io.open(os.path.join(td, "f1"), "wb").write(b"a")
        io.open(os.path.join(td, "state", "x", "shards", "s2.json"), "wb").write(b"bb")
        io.open(os.path.join(td, "state", "x", "shards", "s1.json"), "wb").write(b"ccc")
        f1, n1 = inputs_fp(td, ["f1"], ["state/x/shards/*.json"])
        assert n1 == 3 and len(f1) == 16
        os.utime(os.path.join(td, "f1"), (0, 0))                    # 只动 mtime：指纹不变
        assert inputs_fp(td, ["f1"], ["state/x/shards/*.json"]) == (f1, 3)
        io.open(os.path.join(td, "state", "x", "shards", "s2.json"), "wb").write(b"zz")   # 内容变：指纹变
        assert inputs_fp(td, ["f1"], ["state/x/shards/*.json"])[0] != f1
    print("OK daily_cards selftest: 13 asserts passed")
    return 0

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true", help="只打印计划与擂台决策，不执行")
    p.add_argument("--force-arena", action="store_true")
    p.add_argument("--skip-arena", action="store_true", help="跳过擂台步（优先于 --force-arena）")
    p.add_argument("--days", type=int, default=30)
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.selftest: sys.exit(_selftest())
    os.makedirs(CACHE, exist_ok=True)
    algo = current_algorithm()
    fp, n_files = inputs_fp()
    side = loadj(SIDECAR) if os.path.exists(SIDECAR) else None
    arena_built_at = (loadj(ARENA_CACHE).get("meta") or {}).get("built_at") if os.path.exists(ARENA_CACHE) else None
    run, why = arena_decision(side, fp, algo, arena_built_at, a.force_arena, a.skip_arena)
    print(f"daily_cards {VER} | arena: {'RUN' if run else 'SKIP'} ({why}) | inputs {n_files} files fp={fp} algo={algo}")
    if a.dry_run:
        print("dry-run: nothing executed")
        return
    t0 = time.time()
    dt1 = run_step("build_cache", ["build_cache.py", "--steps", "all", "--days", str(a.days)])
    sh = loadj(CACHE + os.sep + "stars_history.json")               # 11-02~04 教训：缺日静默跳过必须显式示警
    skipped = (sh.get("meta") or {}).get("skipped_dates") or []
    if skipped:
        print(f"WARN trend skipped_dates={skipped} —— 快照 blob 缺失被跳过；查法: GIT_NO_LAZY_FETCH=1 git -C {ROOT} cat-file -s <blob>",
              flush=True)
    dt2 = 0.0
    if run:
        dt2 = run_step("arena_batch", ["arena_batch.py", "--min-stars", "0"])
        io.open(SIDECAR, "w", encoding="utf-8", newline="\n").write(
            json.dumps({"fp": fp, "algorithm": algo,
                        "arena_built_at": loadj(ARENA_CACHE)["meta"]["built_at"],
                        "inputs": n_files, "updated_at": now()}, ensure_ascii=False))
        print(f"OK arena sidecar -> {os.path.basename(SIDECAR)}", flush=True)
    dt3 = run_step("gen_cards", ["gen_cards.py"])
    warn = f" | WARN trend skipped {len(skipped)} dates" if skipped else ""
    print(f"OK daily_cards: build_cache={dt1:.1f}s arena={'%.1fs' % dt2 if run else 'skip(%s)' % why} "
          f"gen_cards={dt3:.1f}s total={time.time()-t0:.1f}s{warn}")

if __name__ == "__main__":
    main()
