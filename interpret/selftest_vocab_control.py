# -*- coding: utf-8 -*-
"""词控提示词 vc1.0 自检（G4 固化）。跑法：python interpret/selftest_vocab_control.py"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for _d in (ROOT, ROOT / "lib", ROOT / "config", ROOT / "interpret"):
    sys.path.insert(0, str(_d))

import pool_store                                           # noqa: E402
import vocab_control as vc                                  # noqa: E402

PASS = FAIL = 0


def chk(name, cond, detail=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"[PASS] {name}")
    else:
        FAIL += 1
        print(f"[FAIL] {name} {detail}")


def main():
    v = vc.load_vocab()
    slugs = vc.all_slugs(v)
    blk = vc.vocab_block(v)

    # --- 词表资产 ---
    chk("词表 75 词 / 15 域", v["n_words"] == 75 and len(v["domains"]) == 15,
        f"{v['n_words']}/{len(v['domains'])}")
    chk("词表区块 ≤6KB（§0 预算）", len(blk.encode()) <= 6144, f"{len(blk.encode())}B")
    chk("同义词环不进 prompt", "同义词" not in blk and "change data capture" not in blk)
    chk("候选档词未被特殊标注", "候选" not in blk and "（草）" not in blk)
    chk("platform 域 4 个草案词已并入", {"baas", "semantic-layer", "db-branching",
                                        "local-db-manager"} <= slugs)

    # --- 提示词结构 ---
    pool = {}
    for p in ("data/live/pool.ndjson", "data/live/pool_cn.ndjson", "data/live/pool_intl.ndjson"):
        for r in pool_store.read_any(ROOT / p):
            pool[r["full_name"]] = r
    fn = next((f for f in ("cube-js/cube", "roistat/go-clickhouse", "matomo-org/matomo") if f in pool), None)
    if fn is None:
        fn = next(iter(pool))
    pack = vc.build_evidence_pack(fn, pool[fn], v)
    out = vc.build_prompt(fn, pool[fn], pack, v)
    pr = out["prompt"]
    chk("prompt 无未替换占位符", "{" + "fn}" not in pr and "{" + "vocab}" not in pr)
    chk("全部 75 词进 prompt", all(s in pr for s in slugs))
    for kw in ("evidence_line", "默认引力词", "abstain", "词表外 slug", "最多 3 个", "易混提醒"):
        chk(f"纪律关键词在 prompt：{kw}", kw in pr)
    for sec in ("--- 标题层级 ---", "--- 安装/依赖线索 ---", "--- 词表命中行", "--- 证据包结束 ---"):
        chk(f"证据包段落：{sec}", sec in pr)
    chk("prompt 体积 ≤12KB", len(pr.encode()) <= 12288, f"{len(pr.encode())}B")
    chk("确定性：同仓两次渲染逐字一致", pr == vc.build_prompt(fn, pool[fn], None, v)["prompt"])
    chk("证据包 ≤4KB", sum(len(x) for x in (pack["headings"], pack["install"], pack["matched"])) <= 4096)

    # --- 校验器 ---
    ok_raw = ('{"tags":[{"slug":"cdc","line":%d,"conf":"high"}],"abstain":null,"gap":null}'
              % (sorted(pack["lines"])[0] if pack["lines"] else 1))
    r = vc.validate(ok_raw, slugs, pack)
    chk("合法输出通过", r["ok"] and r["tags"] and r["tags"][0]["conf"] == "high", str(r["violations"]))

    r = vc.validate('{"tags":[{"slug":"no-such-word","line":1,"conf":"high"}]}', slugs, pack)
    chk("词表外 slug 拒收（§4.3 计数信号）", not r["ok"] and any("词表外" in x for x in r["violations"]))

    line_ok = sorted(pack["lines"])[0] if pack["lines"] else 1
    r = vc.validate('{"tags":[{"slug":"cdc","line":%d,"conf":"high"},{"slug":"etl","line":%d,"conf":"high"},'
                    '{"slug":"orm","line":%d,"conf":"high"},{"slug":"backup","line":%d,"conf":"high"}]}'
                    % (line_ok, line_ok, line_ok, line_ok), slugs, pack)
    chk("超 3 个标签拒收", not r["ok"] and any("超 3" in x for x in r["violations"]))

    r = vc.validate('{"tags":[{"slug":"cdc","conf":"high"}]}', slugs, pack)
    chk("缺 evidence_line 拒收", not r["ok"] and any("缺 evidence_line" in x for x in r["violations"]))

    r = vc.validate('{"tags":[{"slug":"cdc","line":999999,"conf":"high"}]}', slugs, pack)
    chk("行号不在证据包内拒收", not r["ok"] and any("不在证据包" in x for x in r["violations"]))

    r = vc.validate('{"tags":[],"abstain":null}', slugs, pack)
    chk("空标签无 abstain 拒收", not r["ok"] and any("abstain" in x for x in r["violations"]))

    r = vc.validate('{"tags":[],"abstain":"insufficient"}', slugs, pack)
    chk("空标签 + abstain=insufficient 通过", r["ok"] and r["abstain"] == "insufficient")

    r = vc.validate('{"tags":[],"abstain":"insufficient=证据不足"}', slugs, pack)
    chk("abstain 整句归一为码", r["ok"] and r["abstain"] == "insufficient")

    r = vc.validate('{"tags":[],"abstain":"app"}', slugs, pack)
    chk("app/not-db 已退役，旧码拒收", not r["ok"])

    r = vc.validate('{"tags":[{"slug":"cdc","line":%d,"conf":"high"}],"abstain":"insufficient"}' % line_ok, slugs, pack)
    chk("有标签却给 abstain → 忽略并告警", r["ok"] and r["abstain"] is None and r["warnings"])

    r = vc.validate(ok_raw, slugs, pack, oov_policy="record")
    chk("oov_policy=record 时词表外只记录", r["ok"])
    r2 = vc.validate('{"tags":[{"slug":"zzz-fake","line":%d,"conf":"high"}],"abstain":"insufficient"}'
                     % line_ok, slugs, pack, oov_policy="record")
    chk("record 口径：词表外进 warnings 不拒收", r2["ok"] and r2["warnings"])

    # --- 缓存键 ---
    chk("缓存键 sha#vc1.0", vc.vocab_key("abc123") == "abc123#vc1.0")
    chk("缓存键与 v4/txt 分层", vc.vocab_key("abc").endswith("#vc1.0")
        and "#v4" not in vc.vocab_key("abc") and "#txt" not in vc.vocab_key("abc"))

    # --- 与已跑的 G4 对照（同仓同 prompt 字节） ---
    try:
        d = __import__("json").loads((ROOT / "state/shadow/vocab_control_ab_300_G4.json")
                                     .read_text(encoding="utf-8"))
        target = next((x for x in d["items"]["G4"] if x["fn"] == fn), None)
        if target:
            # 1107 v0.11 定版：abstain 三码→单码，prompt 伸缩属预期；只做量级校验
            chk(f"G4 实测 {target['prompt_bytes']}B → 当前 {len(pr.encode())}B（±10% 内）",
                abs(len(pr.encode()) - target["prompt_bytes"]) <= target["prompt_bytes"] * 0.1,
                f"{len(pr.encode())} vs {target['prompt_bytes']}")
    except (FileNotFoundError, KeyError, StopIteration):
        print("[SKIP] 无 G4 报告可比对")

    print(f"\nselftest {'PASS' if not FAIL else 'FAIL'}（{FAIL} 处失败）")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
