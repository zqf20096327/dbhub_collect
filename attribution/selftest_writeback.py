# -*- coding: utf-8 -*-
"""T4b 回写器离线自检：四类原因映射 + 铁律（只补空缺）+ 幂等 + 回滚。零网络零真实分片。

跑法：python attribution/selftest_writeback.py（退出码 0=全绿）
宇宙为 tmp 合成 interp/evidence 分片 + 注入 pool/scan/adjudications（run() 的
注入参数），不依赖真实 256 分片——CI 可跑（T5a 前置）。金标核对只读真实
state/golden_*.json 计交集数，不作断言（读-only）。
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import attribution.writeback as W          # noqa: E402

TS = "2026-11-02T10:00:00Z"
fails: list[str] = []


def ck(cond, name: str) -> None:
    print(f"[{'PASS' if cond else 'FAIL'}] {name}")
    if not cond:
        fails.append(name)


def dep(path, names):
    return {"path": path, "kind": "dep", "names": names}


def img(path, images):
    return {"path": path, "kind": "image", "images": images}


def irec(fn, cat="开发库", dv=None, dbs=None, g="2026-11-01T00:00:00Z"):
    return {"fn": fn, "generated_at": g, "ver": "v3", "prompt_ver": "p",
            "classification": {"cat": cat, "db_verdicts": dv or [], "dbs": dbs or [],
                               "eco": "tool", "ai": {"flag": False, "kind": []}}}


def ev_ok(fn, files=None):
    return {"fn": fn, "status": "ok", "collected_at": TS, "files": files or []}


def _build_universe(base: Path):
    """13 仓宇宙：3 fill（engine/adjudicate/dual）+ 8 tag 四类 + keeper 反例 + 多记录同仓。"""
    ip, ev = base / "interp", base / "evidence"
    ip.mkdir(), ev.mkdir()
    (ip / "aa.json").write_text(json.dumps({
        "k_fill": irec("u/fill"),                                  # dep+image 3 票 → engine fill
        "k_adj": irec("u/adj", cat="其他"),                        # 裁决 supports → adjudicate fill
        "k_oos": irec("u/oos"),                                    # desc redis → 范围外
        "k_edu": irec("u/edu"),                                    # awesome → 真不涉及
        "k_judged": irec("u/judged", dv=["MySQL"]),                # 问过判过 → 真不涉及
        "k_gated": irec("u/gated", cat="应用"),                    # 立案但应用类 → 真不涉及+dbs_raw
        "k_weak": irec("u/weak"),                                  # 单 dep 1 票 → 证据不足
        "k_topic": irec("u/topic"),                                # topic 2 票单通道 → 证据不足
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    (ip / "bb.json").write_text(json.dumps({
        "k_dual": irec("u/dual"),                                  # dep+topic 3 票 → engine fill
        "k_noev": irec("u/noev"),                                  # 无证据记录 → 证据不足
        "k_cited": irec("u/cited"),                                # 行号提名未证实 → 证据不足
        "k_emptyrepo": irec("u/emptyrepo"),                        # 空仓 → 证据不足
        "k_old": irec("u/keeper", g="2026-10-01T00:00:00Z"),       # 老记录空——
        "k_new": irec("u/keeper", dbs=["MySQL"], g="2026-11-02T00:00:00Z"),  # 最新非空 → 整仓跳过
        "k_m1": irec("u/multi", g="2026-10-05T00:00:00Z"),         # 同仓两空记录 → 统一落 op
        "k_m2": irec("u/multi"),
        "k_nocls": {"fn": "u/nocls", "generated_at": TS},          # 无 classification → 不入黑洞口径
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    (ev / "ev.json").write_text(json.dumps({
        "u/fill": ev_ok("u/fill", [dep("requirements.txt", ["mysql-connector-java"]),
                                   img("docker-compose.yml", ["mysql:8"])]),
        "u/gated": ev_ok("u/gated", [dep("requirements.txt", ["psycopg2"]),
                                     img("compose.yml", ["postgres:15"])]),
        "u/weak": ev_ok("u/weak", [dep("requirements.txt", ["psycopg2"])]),
        "u/dual": ev_ok("u/dual", [dep("go.mod", ["go-sql-driver/mysql"])]),
        "u/topic": ev_ok("u/topic"),                               # 空指纹：只剩 topic 证据
        "u/cited": ev_ok("u/cited"),
        "u/emptyrepo": {"fn": "u/emptyrepo", "status": "empty_repo", "collected_at": TS},
    }, ensure_ascii=False), encoding="utf-8")
    adj = base / "adjudications.ndjson"
    adj.write_text(json.dumps({"fn": "u/adj", "db": "MySQL", "verdict": "supports"}) + "\n"
                   + json.dumps({"fn": "u/adj", "db": "NotALib", "verdict": "supports"}) + "\n"
                   + json.dumps({"fn": "u/other", "db": "MySQL", "verdict": "unclear"}) + "\n",
                   encoding="utf-8")
    pool = {
        "u/fill": {"desc": "", "stars": 10, "topics": []},
        "u/adj": {"desc": "", "stars": 500, "topics": []},
        "u/oos": {"desc": "A redis GUI client", "stars": 300, "topics": []},
        "u/edu": {"desc": "awesome mysql list", "stars": 200, "topics": []},
        "u/topic": {"desc": "", "stars": 5, "topics": ["mysql"]},
        "u/dual": {"desc": "", "stars": 400, "topics": ["mysql"]},
        "u/never": {"desc": "", "stars": 1, "topics": []},         # 池内未解读 → 台账记数
    }
    scan = {"u/cited": {"cands": {"MySQL": [{"line": 3}]}}}
    return ip, ev, adj, pool, scan


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        base = Path(td)
        ip, ev, adj, pool, scan = _build_universe(base)
        ledger, report = base / "attribution_writes.json", base / "attribution_writes.md"
        snap = {p.name: p.read_bytes() for p in ip.glob("*.json")}

        # 1) dry-run：只读——分片字节零变化
        st = W.run(dry_run=True, interp_dir=ip, evidence_dir=ev, adjudications_path=adj,
                   ledger_path=ledger, report_path=report, pool=pool, scan=scan)
        ck({p.name: p.read_bytes() for p in ip.glob("*.json")} == snap, "dry-run 分片零变化")
        ck(not ledger.is_file(), "dry-run 不落台账")

        # 2) 圈范围与分布：13 入圈（keeper 最新非空跳过 / nocls 无 classification 跳过）
        ck(st["in_scope"] == 13, f"入圈 13（实测 {st['in_scope']}）")
        ck(st["fill"] == 3 and st["fill_engine"] == 2 and st["fill_adjudicate"] == 1,
           f"fill 3=engine2+adj1（实测 {st['fill']}/{st['fill_engine']}/{st['fill_adjudicate']}）")
        ck(st["tag"] == 10, f"tag 10（实测 {st['tag']}）")
        ck(st["tag_reasons"].get(W.R_TRUE_UNRELATED) == 3
           and st["tag_reasons"].get(W.R_OUT_OF_SCOPE) == 1
           and st["tag_reasons"].get(W.R_INSUFFICIENT) == 6,
           f"四类分布 真不涉及3/范围外1/证据不足6（实测 {st['tag_reasons']}）")
        ck(st["pool_uninterpreted"] == 1, "池内未解读记数 1")

        # 3) 实写：落点正确（dbs/dbs_src/dbs_empty_reason）+ 铁律（非空/圈外零触碰）
        W.run(interp_dir=ip, evidence_dir=ev, adjudications_path=adj,
              ledger_path=ledger, report_path=report, pool=pool, scan=scan)
        aa = json.loads((ip / "aa.json").read_text(encoding="utf-8"))
        bb = json.loads((ip / "bb.json").read_text(encoding="utf-8"))
        c = aa["k_fill"]["classification"]
        ck(c["dbs"] == ["MySQL"] and c["dbs_src"]["kind"] == "engine"
           and c["dbs_src"]["ver"] == W.ENGINE_VERSION, "engine fill 落点+溯源")
        c = aa["k_adj"]["classification"]
        ck(c["dbs"] == ["MySQL"] and c["dbs_src"]["kind"] == "adjudicate",
           "adjudicate fill（NotALib 不入库）")
        ck(aa["k_oos"]["classification"]["dbs_empty_reason"]["reason"] == W.R_OUT_OF_SCOPE
           and aa["k_oos"]["classification"]["dbs"] == [], "范围外 tag")
        ck(aa["k_edu"]["classification"]["dbs_empty_reason"]["reason"] == W.R_TRUE_UNRELATED,
           "教学 tag")
        ck(aa["k_judged"]["classification"]["dbs_empty_reason"]["reason"] == W.R_TRUE_UNRELATED,
           "AI 判过无 support tag")
        g = aa["k_gated"]["classification"]
        ck(g["dbs_empty_reason"]["reason"] == W.R_TRUE_UNRELATED and g["dbs"] == []
           and "PostgreSQL" in g["dbs_empty_reason"]["detail"], "应用类立案不回写（detail 留痕）")
        ck(aa["k_weak"]["classification"]["dbs_empty_reason"]["reason"] == W.R_INSUFFICIENT,
           "单弱信号 tag")
        ck(aa["k_topic"]["classification"]["dbs_empty_reason"]["reason"] == W.R_INSUFFICIENT
           and "topic" in aa["k_topic"]["classification"]["dbs_empty_reason"]["detail"],
           "topic 单通道不放直通")
        ck(bb["k_dual"]["classification"]["dbs"] == ["MySQL"], "dep+topic 双源 fill")
        ck("无证据记录" in bb["k_noev"]["classification"]["dbs_empty_reason"]["detail"],
           "无证据记录 tag")
        ck("行号提名" in bb["k_cited"]["classification"]["dbs_empty_reason"]["detail"],
           "行号提名未证实 tag（提名≠支持不硬填）")
        ck("empty_repo" in bb["k_emptyrepo"]["classification"]["dbs_empty_reason"]["detail"],
           "空仓 tag")
        ck(bb["k_new"]["classification"]["dbs"] == ["MySQL"]
           and "dbs_src" not in bb["k_new"]["classification"], "铁律：最新非空记录零触碰")
        ck(bb["k_old"]["classification"]["dbs"] == []
           and "dbs_empty_reason" not in bb["k_old"]["classification"],
           "铁律：已有归属仓的老空记录不改历史")
        m1, m2 = bb["k_m1"]["classification"], bb["k_m2"]["classification"]
        ck(m1.get("dbs_empty_reason") == m2.get("dbs_empty_reason") or m1["dbs"] == m2["dbs"],
           "同仓多空记录统一落 op")
        ck("classification" not in bb["k_nocls"], "无 classification 记录不动")

        # 4) 台账可回滚 + ledger 结构（ops 带 keys 可定位记录）
        led = json.loads(ledger.read_text(encoding="utf-8"))
        ck(set(led["ops"]["u/fill"]["keys"][0]) == {"aa.json", "k_fill"}, "台账 keys 定位记录")
        W.rollback(ledger, ip)
        aa = json.loads((ip / "aa.json").read_text(encoding="utf-8"))
        bb = json.loads((ip / "bb.json").read_text(encoding="utf-8"))
        ck(aa["k_fill"]["classification"]["dbs"] == []
           and "dbs_src" not in aa["k_fill"]["classification"], "回滚：fill 还原为空+摘溯源")
        ck("dbs_empty_reason" not in aa["k_oos"]["classification"], "回滚：tag 摘原因")
        ck(bb["k_new"]["classification"]["dbs"] == ["MySQL"], "回滚：非本工具记录不受影响")
        ck(json.loads(ledger.read_text(encoding="utf-8"))["ops"] == {}
           and list(base.glob("attribution_writes.json.rolled-*")), "回滚：台账滚档")
        # 内容级比对非字节级：_write_shard_file 强制 LF（CI Linux 同款），测试宇宙
        # 初始文件是 Windows 默认 CRLF——回滚后内容还原、行尾归一为 LF 是设计行为
        back = json.loads((ip / "aa.json").read_text(encoding="utf-8"))
        ck(back == json.loads(snap["aa.json"].decode("utf-8")), "回滚后 aa 分片内容还原")

        # 5) 幂等：回滚后重跑 → 同结论；再跑一遍 → 分片字节零变化（零脏写）
        W.run(interp_dir=ip, evidence_dir=ev, adjudications_path=adj,
              ledger_path=ledger, report_path=report, pool=pool, scan=scan)
        again = {p.name: p.read_bytes() for p in ip.glob("*.json")}
        W.run(interp_dir=ip, evidence_dir=ev, adjudications_path=adj,
              ledger_path=ledger, report_path=report, pool=pool, scan=scan)
        ck({p.name: p.read_bytes() for p in ip.glob("*.json")} == again, "二次运行零脏写")

        # 6) 报告可重出（--report-only 路径）
        W.run(report_only=True, ledger_path=ledger, report_path=report,
              interp_dir=ip, evidence_dir=ev)
        md = report.read_text(encoding="utf-8")
        ck("黑洞归零" in md and "回写库位分布" in md and "抽检" in md, "报告三段齐全")

    verdict = "PASS" if not fails else "FAIL"
    print(f"[{verdict}] T4b 回写器：四类映射 + 铁律只补空缺 + 裁决频道 + "
          f"幂等 + 回滚内容还原 + dry-run 零副作用（{len(fails)} 失败）")
    for f in fails:
        print(f)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
