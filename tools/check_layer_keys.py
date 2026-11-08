# -*- coding: utf-8 -*-
"""层键只读体检（工作清单 G1-1）。

回答三个问题，不写任何数据：
  1. 缓存里的键能不能全部归层？（失效键=0 才合格）
  2. 键归对了层，载荷形态对不对？（取到键 ≠ 层里有货）
  3. 台账里的每个仓，分类/身份能不能读到？删掉旧代后还剩多少？

验收闸门（G1-1 定、G5-2 后按在池台账口径调整）：
  分类可读 ≥ 33,600 · 身份可读 ≥ 33,500 · 失效键 = 0

用法：
  python tools/check_layer_keys.py              # 体检 + 闸门（红则非零退出）
  python tools/check_layer_keys.py --json out.json
  python tools/check_layer_keys.py --selftest   # 键规则单测（不读缓存）
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "lib"))
sys.path.insert(0, str(ROOT / "interpret"))

import interp_keys as ik                      # noqa: E402
import interpret as itp                      # noqa: E402
import vocab_control as vc                   # noqa: E402
from interp_store import load_cache          # noqa: E402

GATE_CLASS_MIN = 33600   # G5-2 台账收敛到在池 33,701 后的在池口径（≈99.7%）；
GATE_ID_MIN = 33500      # 旧值 35,800/35,200 是含 2,225 池外条目的全集口径
POOL = ROOT / "data" / "live" / "pool.ndjson"


def _contract_fails() -> list[str]:
    """键规则必须与生产代码同源（本模块复刻常量，靠这里防漂移）。"""
    bad = []
    if ik.judge_key("abc") != itp.cache_key("abc", "v4"):
        bad.append("judge_key != interpret.cache_key")
    if ik.text_key("abc") != itp.text_key("abc"):
        bad.append("text_key != interpret.text_key")
    if ik.vocab_key("abc") != vc.vocab_key("abc"):
        bad.append("vocab_key != vocab_control.vocab_key")
    if ik.PROMPT_VER_TEXT != itp.PROMPT_VER_TEXT:
        bad.append("PROMPT_VER_TEXT 漂移")
    if ik.VOCAB_PROMPT_VER != vc.VOCAB_PROMPT_VER:
        bad.append("VOCAB_PROMPT_VER 漂移")
    return bad


def _pool() -> set[str]:
    names = set()
    if POOL.is_file():
        for line in POOL.read_text(encoding="utf-8", errors="replace").split("\n"):
            line = line.strip()
            if not line:
                continue
            try:
                fn = json.loads(line).get("full_name")
            except Exception:
                continue
            if fn:
                names.add(fn)
    return names


def check() -> dict:
    from interp_layer_store import LayerStore
    cache = load_cache()
    st = json.loads((ROOT / "state" / "interp_state.json").read_text(encoding="utf-8"))
    items = st.get("items") or {}
    pool = _pool()

    # 查找链（G1-6/G3 后）：先新层目录（生产位置），后旧缓存（过渡期兼容）。
    # 键族 → 层目录映射：vocab 键的条目在 domain_tags 层。
    _layer_of = {"judge": "judge", "text": "text", "vocab": "domain_tags", "desc": "desc"}
    stores = {l: LayerStore(l) for l in _layer_of.values()}
    for s in stores.values():
        s.load()

    def get(key):
        fam, sha = ik.parse_key(key)
        s_ = stores.get(_layer_of.get(fam, ""))
        if s_ is not None:
            obj = s_.get(sha)
            if obj is not None:
                return obj
        return cache.get(key)

    fam = Counter()
    invalid = Counter()
    mismatch = Counter()
    bad_examples = {}
    for k, v in cache.items():
        layer, sha = ik.parse_key(k)
        fam[layer] += 1
        if layer == "unknown":
            invalid["unknown_key"] += 1
            bad_examples.setdefault("unknown_key", k)
            continue
        shape = ik.entry_shape(v)
        if shape == "bad":
            invalid["bad_payload"] += 1
            bad_examples.setdefault("bad_payload", k)
            continue
        if isinstance(v, dict) and v.get("sha") not in (None, sha):
            invalid["sha_mismatch"] += 1
            bad_examples.setdefault("sha_mismatch", (k, v.get("sha")))
        if not ik.accepts(layer, shape):
            mismatch[f"{layer}/{shape}"] += 1
            bad_examples.setdefault(f"mismatch:{layer}/{shape}", k)

    rows = Counter()
    gaps = []
    for fn, meta in items.items():
        sha = (meta or {}).get("sha")
        if not sha:
            rows["no_sha"] += 1
            continue
        # G3 起 desc-only 仓台账指向新键 desc::<12hex>：一条载荷同时供分类与身份
        key_fam, _ = ik.parse_key(sha)
        if key_fam == "desc":
            obj = get(sha)
            new_c = bool(obj and (obj.get("classification") or {}).get("cat_primary"))
            new_i = bool(obj and (obj.get("identity") or {}).get("one_liner"))
            old = False
            c_ok, i_ok = new_c, new_i
        else:
            pr = ik.probe(sha, get)
            new_c = pr["judge"]["ok"]
            new_i = pr["text"]["ok"]
            old = pr["legacy"]["ok"]
            c_ok, i_ok = new_c or old, new_i or old
        side = "pool" if fn in pool else "out"
        rows[f"{side}_class"] += 1 if c_ok else 0
        rows[f"{side}_id"] += 1 if i_ok else 0
        rows[f"{side}_total"] += 1
        rows[f"{side}_class_new"] += 1 if new_c else 0
        rows[f"{side}_id_new"] += 1 if new_i else 0
        rows[f"{side}_class_legacy_only"] += 1 if (c_ok and not new_c) else 0
        rows[f"{side}_id_legacy_only"] += 1 if (i_ok and not new_i) else 0
        if side == "pool" and not c_ok:
            gaps.append({"fn": fn, "sha": sha, "reason": "classification_unreadable"})

    invalid_total = sum(invalid.values())
    mismatch_total = sum(mismatch.values())
    return {
        "cache_keys": len(cache),
        "families": dict(fam),
        "invalid": dict(invalid),
        "mismatch": dict(mismatch),
        "bad_examples": {k: str(v)[:120] for k, v in bad_examples.items()},
        "readability": dict(rows),
        "gaps_sample": gaps[:10],
        "gate": {
            "class_min": GATE_CLASS_MIN,
            "id_min": GATE_ID_MIN,
            "class_ok": rows["pool_class"] + rows["out_class"],
            "id_ok": rows["pool_id"] + rows["out_id"],
            "invalid_total": invalid_total,
            "mismatch_total": mismatch_total,
        },
    }


def _selftest() -> int:
    fails = 0

    def chk(name, cond):
        nonlocal fails
        print(f"[{'PASS' if cond else 'FAIL'}] {name}")
        if not cond:
            fails += 1

    chk("judge 键", ik.judge_key("ab12") == "ab12#v4")
    chk("text 键", ik.text_key("ab12") == "ab12#txt4.0")
    chk("vocab 键", ik.vocab_key("ab12") == "ab12#vc1.0")
    chk("legacy 键", ik.legacy_key("ab12") == "ab12")
    chk("desc 键 12 位摘要", len(ik.desc_key("a/b", "x")) == len("desc::") + 12)
    chk("desc 键随 fn 变化", ik.desc_key("a/b", "x") != ik.desc_key("a/c", "x"))
    chk("desc 键随描述变化", ik.desc_key("a/b", "x") != ik.desc_key("a/b", "y"))
    chk("desc 同输入稳定", ik.desc_key("a/b", "x") == ik.desc_key("a/b", "x"))
    cases = {
        "ab12#v4": ("judge", "ab12"),
        "ab12#txt4.0": ("text", "ab12"),
        "ab12#vc1.0": ("vocab", "ab12"),
        "ab12cd": ("legacy", "ab12cd"),
        "desc::abcdef123456": ("desc", "desc::abcdef123456"),
        "desc::A bot for # v4": ("desc_legacy", "desc::A bot for # v4"),
        "desc::A bot #v4": ("desc_legacy", "desc::A bot "),
        "desc::x#txt4.0": ("unknown", "desc::x#txt4.0"),
        "weird#v5": ("unknown", "weird#v5"),
        "": ("unknown", ""),
    }
    for key, want in cases.items():
        got = ik.parse_key(key)
        chk(f"解键 {key!r} → {want[0]}", got == want)
    chk("v4 形态", ik.entry_shape({"classification": {"cat_primary": "开发库"}}) == "v4")
    chk("v3 形态", ik.entry_shape({"identity": {}, "classification": {"ai": {}}}) == "v3")
    chk("text 形态", ik.entry_shape({"identity": {}}) == "text")
    chk("vocab 形态", ik.entry_shape({"tags": [], "abstain": None}) == "vocab")
    chk("非 dict 判 bad", ik.entry_shape([]) == "bad")
    desc_v3 = {"identity": {}, "classification": {"ai": {}}, "source": "desc"}
    chk("desc 旧条目按结构判 v3（出处不混进形态）", ik.entry_shape(desc_v3) == "v3")
    chk("出处单独可取", ik.entry_source(desc_v3) == "desc")
    chk("judge 拒 v3 形态", not ik.accepts("judge", "v3"))
    chk("legacy 拒 v4 形态", not ik.accepts("legacy", "v4"))
    chk("desc 收 v3/v4", ik.accepts("desc", "v3") and ik.accepts("desc", "v4"))
    fake = {"ab12#v4": {"classification": {"cat_primary": "x"}, "sha": "ab12"},
            "ab12": {"identity": {}, "classification": {"ai": {}}, "sha": "ab12"}}
    pr = ik.probe("ab12", fake.get)
    chk("probe judge ok", pr["judge"]["ok"])
    chk("probe text 缺层", not pr["text"]["ok"])
    chk("probe legacy ok", pr["legacy"]["ok"])
    chk("best 优先 judge", (ik.best("ab12", fake.get) or {}).get("layer") == "judge")
    chk("契约与代码一致", not _contract_fails())
    print(f"\nselftest {'PASS' if not fails else 'FAIL'}（{fails} 处失败）")
    return 0 if not fails else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", metavar="PATH")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return _selftest()

    bad = _contract_fails()
    rep = check()
    g = rep["gate"]
    fam = rep["families"]
    r = rep["readability"]

    print("键形态：" + " / ".join(f"{k} {v}" for k, v in sorted(fam.items())))
    print("失效键：" + (f"{g['invalid_total']} " + json.dumps(rep["invalid"], ensure_ascii=False)
                       if g["invalid_total"] else "0"))
    print("形态不符：" + (f"{g['mismatch_total']} " + json.dumps(rep["mismatch"], ensure_ascii=False)
                        if g["mismatch_total"] else "0"))
    for side, label in (("pool", "在池"), ("out", "池外")):
        tot = r.get(f"{side}_total", 0)
        if not tot:
            continue
        c, i = r.get(f"{side}_class", 0), r.get(f"{side}_id", 0)
        print(f"{label} {tot:,}：分类 {c:,} ({c / tot:.2%}) · 身份 {i:,} ({i / tot:.2%})"
              f" · 仅旧代可读 分类 {r.get(f'{side}_class_legacy_only', 0):,}"
              f"/身份 {r.get(f'{side}_id_legacy_only', 0):,}")

    ok = (g["class_ok"] >= GATE_CLASS_MIN and g["id_ok"] >= GATE_ID_MIN
          and g["invalid_total"] == 0 and not bad)
    print(f"闸门：分类 {g['class_ok']:,}≥{GATE_CLASS_MIN:,} · 身份 {g['id_ok']:,}≥{GATE_ID_MIN:,}"
          f" · 失效键={g['invalid_total']} · 契约{'一致' if not bad else '漂移'} → "
          f"{'PASS' if ok else 'FAIL'}")
    if bad:
        print("契约漂移：" + "; ".join(bad))
    if rep["gaps_sample"]:
        print("在池不可读样例：" + json.dumps(rep["gaps_sample"][:3], ensure_ascii=False))
    if a.json:
        Path(a.json).write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"报告：{a.json}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
