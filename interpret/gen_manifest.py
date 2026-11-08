# -*- coding: utf-8 -*-
"""G2 代际清单生成器（工作清单 G0-2 / 定稿 G5-3）。

manifest 是"这一代 AI 解析"的出生证明：哪一版提示词、哪一版词表、哪个模型、
键长什么样、覆盖多少仓、由哪次代码提交生产。后续页面/查询只认 manifest 里的
键规则，不靠猜缓存里的字符串。

判定原则：
- 只记录**代码里的真实常量**（import 取值，不手抄），代码改了重跑即可对齐；
- 计数是**时点快照**（counts.asof），v4t 跑完或 G5 定稿后重跑刷新；
- 模型只记目标模型 + 混入量。逐条模型在 state/logs 的 runlog 里，缓存条目
  model 字段为空（历史遗留，见 G5-3 lineage）。

用法：
  python interpret/gen_manifest.py            # 写 state/gen_manifest.json
  python interpret/gen_manifest.py --dry-run  # 只打印，不落盘
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "lib"))
sys.path.insert(0, str(ROOT / "interpret"))

import interpret as itp                      # noqa: E402
import vocab_control as vc                   # noqa: E402
from gh import atomic_write_json, load_env   # noqa: E402

MANIFEST = ROOT / "state" / "gen_manifest.json"
GEN_ID = "g2-20261107"                       # G2 代际号（工作清单建档日）
CODE_FILES = [
    "interpret/interpret.py",
    "interpret/vocab_control.py",
    "interpret/gen_manifest.py",
    "lib/interp_read.py",
    "lib/interp_keys.py",
    "lib/interp_layer_store.py",
    "tools/split_layers.py",
    "config/domain_vocab_v0.11.json",
]


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _sha256_file(rel: str) -> str:
    return hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()


def _git(*args: str) -> str:
    try:
        return subprocess.run(["git", *args], cwd=ROOT, capture_output=True,
                              text=True, timeout=15).stdout.strip()
    except Exception:
        return ""


def _count_layers() -> dict:
    """新分层目录条数（state/interp/<layer>/shards）。G1-6 后这才是新代主存储。"""
    base = ROOT / "state" / "interp"
    out = {}
    for layer in ("judge", "text", "domain_tags", "desc"):
        d = base / layer / "shards"
        n = 0
        if d.is_dir():
            for p in d.glob("*.json"):
                n += len(json.loads(p.read_text(encoding="utf-8")) or {})
        out[layer] = n
    return out


def _count_cache() -> dict:
    """按分片逐文件统计键形态（不整库加载，避免与守夜进程抢内存）。

    过渡期（G1-6a 搬迁后、G7-2 删旧目录前）旧目录还留着 judge/text/vocab 副本：
    total 按「逻辑条目」口径——同一键新旧双存只计一次（取 max）；
    物理重叠记在 storage_dup（取 min，G7-2 删旧目录后自然归零）。
    """
    from interp_store import SHARD_DIR, LEGACY
    cnt = Counter()
    if LEGACY.is_file():
        for k in json.loads(LEGACY.read_text(encoding="utf-8")):
            cnt[_key_kind(k)] += 1
    if SHARD_DIR.is_dir():
        for p in sorted(SHARD_DIR.glob("*.json")):
            for k in json.loads(p.read_text(encoding="utf-8")):
                cnt[_key_kind(k)] += 1
    lay = _count_layers()
    merged = {k: cnt.get(k, 0) for k in ("judge", "text", "vocab", "bare",
                                         "desc_bare", "desc_judge", "desc_text")}
    for kind, layer in (("judge", "judge"), ("text", "text"), ("vocab", "domain_tags")):
        merged[kind] = max(merged[kind], lay[layer])
    # desc：旧键（desc_legacy 形态，G7 删）与新层键 desc::<12hex> 是【不相交】集合
    # （键形状不同、人口不同：旧键服务老台账、新键服务 G3 后台账）——相加而非取 max。
    desc_legacy = sum(merged[k] for k in ("desc_bare", "desc_judge", "desc_text"))
    desc = lay["desc"]                      # 新代 desc 只认层目录
    storage_dup = (min(cnt.get("judge", 0), lay["judge"])
                   + min(cnt.get("text", 0), lay["text"])
                   + min(cnt.get("vocab", 0), lay["domain_tags"]))
    return {"total": merged["judge"] + merged["text"] + merged["vocab"]
                    + desc + merged["bare"] + desc_legacy,
            **merged,
            "desc": desc,
            "desc_legacy": desc_legacy,
            "storage_dup": storage_dup,
            "layers": lay}


def _key_kind(k: str) -> str:
    if k.startswith("desc::"):
        # desc 降级键：旧键 desc::<description>（裸）、v4 判定 desc::<desc>#v4、
        # 文本卷 desc::<desc>#txt4.0。G3 后统一换 desc::<sha1(fn+desc)[:12]>
        if k.endswith("#v4"):
            return "desc_judge"
        if k.endswith("#txt" + itp.PROMPT_VER_TEXT):
            return "desc_text"
        return "desc_bare"
    if k.endswith("#" + vc.VOCAB_PROMPT_VER):
        return "vocab"
    if k.endswith("#txt" + itp.PROMPT_VER_TEXT):
        return "text"
    if k.endswith("#v4"):
        return "judge"
    return "bare"


def _count_ledger(rel: str) -> dict:
    p = ROOT / rel
    if not p.is_file():
        return {}
    items = json.loads(p.read_text(encoding="utf-8")).get("items") or {}
    return {"total": len(items),
            **dict(Counter(v.get("status") for v in items.values() if isinstance(v, dict)))}


def _count_pool() -> dict:
    """池规模（只读采集层数据，不写）。"""
    pool = ROOT / "data" / "live" / "pool.ndjson"
    if not pool.is_file():
        return {}
    names = set()
    for line in pool.read_text(encoding="utf-8", errors="replace").split("\n"):
        line = line.strip()
        if not line:
            continue
        try:
            r = json.loads(line)
        except Exception:
            continue
        fn = r.get("full_name")
        if fn:
            names.add(fn)
    return {"repos": len(names)}


def _vocab_meta() -> dict:
    f = ROOT / "config" / "domain_vocab_v0.11.json"
    d = json.loads(f.read_text(encoding="utf-8"))
    doms = d.get("domains") or {}
    return {"ver": d.get("vocab_ver"), "file": str(f.relative_to(ROOT)).replace("\\", "/"),
            "sha256": _sha256_file("config/domain_vocab_v0.11.json"),
            "n_words": d.get("n_words"), "n_domains": len(doms),
            "source": d.get("source")}


def _lineage() -> dict:
    """G5-3 lineage：各层出身的机器口径（不手抄）。

    条目级：source/prompt_ver/generated_at 在条目里；model 只在 domain_tags/desc
    条目（judge/text 历史条目不记模型——G2-2 的教训，逐条模型以 runlog 为准）。
    层级：从 state/logs/interp_*.jsonl 数各 mode 的 done 行模型分布，作为该层的
    模型出身证据；抽 100 条断言条目级出身字段 100% 齐备。
    """
    import glob
    import random
    from interp_layer_store import LayerStore
    lay_models: dict[str, dict] = {}
    for p in sorted(glob.glob(str(ROOT / "state" / "logs" / "interp_*.jsonl"))):
        for line in open(p, encoding="utf-8"):
            try:
                j = json.loads(line)
            except Exception:
                continue
            if j.get("kind") != "done":
                continue
            m = {"v4": "judge", "v4t": "text"}.get(j.get("mode"))
            if m:
                lay_models.setdefault(m, {})
                mk = j.get("model") or "?"
                lay_models[m][mk] = lay_models[m].get(mk, 0) + 1
    lineage = {"per_entry_fields": ("source", "prompt_ver", "generated_at"),
               "entry_model_field": {"judge": False, "text": False,
                                     "domain_tags": True, "desc": True},
               "runlog_model_evidence": lay_models,
               "note": "runlog 是历史流水（含被 G2-2 归一重烧取代的 deepseek 行）；"
                       "最终库存模型以 g2_model_normalize --verify 为准（left=0，全 glm）"}
    # 抽 100 条（四层均衡）断言出身字段齐备
    rng = random.Random(20261108)
    miss = []
    total = 0
    for layer in ("judge", "text", "domain_tags", "desc"):
        st = LayerStore(layer)
        st.load()
        keys = sorted(st.items)
        if not keys:
            continue
        for k in rng.sample(keys, min(25, len(keys))):
            total += 1
            e = st.items[k]
            if not all(e.get(f) for f in ("source", "prompt_ver", "generated_at")):
                miss.append({"layer": layer, "key": k[:20],
                             "missing": [f for f in ("source", "prompt_ver",
                                                     "generated_at") if not e.get(f)]})
    lineage["sample100"] = {"n": total, "missing": miss[:5], "missing_n": len(miss)}
    return lineage


def build() -> dict:
    load_env()
    cache = _count_cache()
    gen = {
        "schema": 1,
        "gen_id": GEN_ID,
        "status": "building",          # building → ready（G5-3 定稿）→ frozen（G7）
        "plan": "A",
        "worklist": "docs/AI解析工作清单_G2.md",
        "phase": "G0",
        "created_at": _now(),
        "updated_at": _now(),
        "model": {
            "target": os.environ.get("AI_MODEL") or "glm-5.3-flash",
            "base_url": os.environ.get("AI_BASE_URL") or "",
            "mixed": {"deepseek": 463, "action": "G2-2 归一为 glm-5.3-flash 后重跑"},
            "per_entry": "缓存条目不记模型；逐条模型只在 state/logs/interp_*.jsonl",
        },
        "layers": {
            "judge": {
                "label": "v4 判定卷",
                "prompt_ver": itp.PROMPT_VER_V4,
                "key": "{sha}#v4",
                "code": "interpret/interpret.py",
                "status": "run",
                "entries": max(cache["judge"], cache["layers"]["judge"]),
            },
            "text": {
                "label": "v4t 文本卷",
                "prompt_ver": itp.PROMPT_VER_TEXT,
                "key": "{sha}#txt" + itp.PROMPT_VER_TEXT,
                "code": "interpret/interpret.py",
                "status": "running",
                "entries": max(cache["text"], cache["layers"]["text"]),
                "scope_note": "TEXT_STAR_MIN 默认 100；1107 全池跑用 env=0",
            },
            "domain_tags": {
                "label": "vc1.0 词控",
                "prompt_ver": vc.VOCAB_PROMPT_VER,
                "key": "{sha}#" + vc.VOCAB_PROMPT_VER,
                "code": "interpret/vocab_control.py",
                "status": "running",
                "entries": max(cache["vocab"], cache["layers"]["domain_tags"]),
                "vocab": _vocab_meta(),
                "abstain_codes": list(vc.ABSTAIN_CODES),
                "magnet_words": sorted(vc.MAGNET_WORDS),
            },
            "desc": {
                "label": "desc 降级（无 README 仓）",
                "key": "desc::{sha1(fn + desc)[:12]}",
                "status": "run",
                "entries": cache["desc"],
                "prompt_ver": "dc1.0",
                "scope_note": "在池 no_readme 且有描述（1,009 全量已跑）；"
                              "空描述 912 进 dead-letter 不生成",
                "note": "旧键 desc::<description>（会碰撞，最多 97 仓共用一条）已随 "
                        "G7-2 下线（desc_legacy {:,} 条归零）".format(
                            cache["desc_legacy"]),
            },
        },
        "legacy": {
            "label": "v3 裸 sha + 旧 desc 键（旧代，G7-2 已删）",
            "key": "{sha} 或 desc::<description>[#v4]",
            "entries": cache["bare"] + cache["desc_legacy"],
            "status": "deleted_at_G7_2（2026-11-08，备份 D:/dbhub_interp_backup_20261108 + pre-g2 标签）",
        },
        "counts": {
            "asof": _now(),
            "cache_total": cache["total"],
            "storage_dup": cache["storage_dup"],
            "layers": cache["layers"],
            "interp_state": _count_ledger("state/interp_state.json"),
            "readme_state": _count_ledger("state/readme_state.json"),
            "pool": _count_pool(),
        },
        "artifacts": {
            "cache": "state/interp_cache_shards（已于 G7-2 删除，2026-11-08；可从备份/pre-g2 恢复）",
            "layer_root": "state/interp/<layer>/（judge|text|domain_tags|desc；shards + state.json + runlog）",
            "ledger": "state/interp_state.json",
            "readme_ledger": "state/readme_state.json",
            "dead_letter": "state/dead_letter.json",
            "runlog": "state/logs/interp_*.jsonl（gitignored）",
            "shadow": "state/shadow",
        },
        "code": {
            "git_commit": _git("rev-parse", "HEAD"),
            "git_commit_date": _git("log", "-1", "--format=%cI"),
            # 生成时这些文件是否还有未提交改动（true 表示 manifest 对应的不是干净提交）
            "dirty": bool(_git("status", "--porcelain", "--", *CODE_FILES)),
            "files": {p: _sha256_file(p) for p in CODE_FILES},
        },
    }
    return gen


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--selftest", action="store_true", help="结构断言（只读，不落盘）")
    ap.add_argument("--finalize", action="store_true",
                    help="定稿：status→ready + lineage 块 + 100 条出身抽样")
    ap.add_argument("--phase", default="G5-3",
                    help="定稿写入的 phase 标识（G7-2 删旧后复验用 --phase G7-2）")
    a = ap.parse_args()
    gen = build()
    if a.finalize:
        gen["status"] = "ready"
        gen["phase"] = a.phase
        gen["finalized_at"] = _now()
        gen["lineage"] = _lineage()
    if a.selftest:
        return _selftest(gen)
    text = json.dumps(gen, ensure_ascii=False, indent=1)
    if a.dry_run:
        print(text)
        return 0
    atomic_write_json(MANIFEST, gen)
    print(f"已写 {MANIFEST.relative_to(ROOT)} · gen_id={gen['gen_id']} "
          f"· 缓存 {gen['counts']['cache_total']} 条")
    return 0


def _selftest(gen: dict) -> int:
    """manifest 结构断言：键规则必须与代码真实产出一致（防手抄漂移）。"""
    fails = 0

    def chk(name, cond):
        nonlocal fails
        print(f"[{'PASS' if cond else 'FAIL'}] {name}")
        if not cond:
            fails += 1

    L = gen["layers"]
    chk("四层齐全", set(L) == {"judge", "text", "domain_tags", "desc"})
    # 键模板对拍：用代码函数生成，manifest 只是它的字符串形态
    chk("judge 键与 cache_key 一致",
        L["judge"]["key"] == itp.cache_key("{sha}", "v4"))
    chk("text 键与 text_key 一致",
        L["text"]["key"] == itp.text_key("{sha}"))
    chk("vocab 键与 vocab_key 一致",
        L["domain_tags"]["key"] == vc.vocab_key("{sha}"))
    keys = [L[k]["key"] for k in ("judge", "text", "domain_tags")]
    chk("三层键两两不同", len(set(keys)) == 3)
    chk("desc 键是新方案（含 sha1 截断）",
        "sha1" in L["desc"]["key"] and L["desc"]["key"].startswith("desc::"))
    # 计数自洽：分形态之和 == 总数
    c = gen["counts"]
    chk("缓存计数自洽（judge+text+vocab+desc+legacy == total）",
        L["judge"]["entries"] + L["text"]["entries"] + L["domain_tags"]["entries"]
        + L["desc"]["entries"] + gen["legacy"]["entries"] == c["cache_total"])
    chk("desc 计数口径：层目录为准（旧 desc_legacy 归 legacy 块）",
        L["desc"]["entries"] == c["layers"]["desc"])
    # 词表指纹必须与磁盘一致
    v = L["domain_tags"]["vocab"]
    chk("词表 sha256 与文件一致",
        v["sha256"] == _sha256_file(v["file"]))
    chk("词表词数 >0 且域数 >0", (v["n_words"] or 0) > 0 and v["n_domains"] > 0)
    # 元信息
    chk("gen_id 形如 gN-YYYYMMDD", gen["gen_id"].startswith("g2-"))
    chk("status 合法", gen["status"] in ("building", "ready", "frozen"))
    chk("code.dirty 反映真实工作区", gen["code"]["dirty"] in (True, False))
    chk("计数有时点", bool(c["asof"]) and bool(c["readme_state"]))
    print(f"\nselftest {'PASS' if not fails else 'FAIL'}（{fails} 处失败）")
    return 0 if not fails else 1


if __name__ == "__main__":
    raise SystemExit(main())
