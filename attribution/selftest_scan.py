# -*- coding: utf-8 -*-
"""T2d 离线自检：全池扫描 CLI 三清单口径 + 流式/防御/确定性。零网络零大文件。

跑法：python attribution/selftest_scan.py（退出码 0=全绿）
宇宙为 tmp 合成分片（evidence 2 分片含哈希键/无 fn/缺时间戳防御 + interp 键=fn 哈希
+ pool.json list 形态），不依赖真实 256 分片与 23MB 池快照——CI 可跑（T5a 前置）。
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import attribution.scan as S  # noqa: E402
from attribution.api import ENGINE_VERSION  # noqa: E402

TS = "2026-10-30T15:10:33Z"


def dep(path, names):
    return {"path": path, "kind": "dep", "names": names}


def img(path, images):
    return {"path": path, "kind": "image", "images": images}


def _build_universe(base: Path):
    """合成宇宙：覆盖三清单正例/反例 + 边角（未解读/仅topic/空仓/无池/缺fn/缺时间戳）。"""
    ev = base / "evidence"
    ip = base / "interp"
    ev.mkdir(), ip.mkdir()
    shard0 = {
        # 漏报正例：dep+image 双证 3 票 → case 非空
        "u/missed2": {"fn": "u/missed2", "status": "ok", "collected_at": TS, "stars": 0,
                      "files": [dep("requirements.txt", ["mysql-connector-java"]),
                                img("docker-compose.yml", ["mysql:8"])]},
        # 漏报正例：单 dep 1 票 → case 空（below_quorum 也进漏报清单——指纹有命中即可）
        "u/missed1": {"fn": "u/missed1", "status": "ok", "collected_at": TS,
                      "files": [dep("requirements.txt", ["psycopg2"])]},
        # 双源：dep 1 + topic 1 = 2 票 → missed 且 dual（topic∩指纹同库）
        "u/dual": {"fn": "u/dual", "status": "ok", "collected_at": TS,
                   "files": [dep("go.mod", ["go-sql-driver/mysql"])]},
        # 不完整：现判 MySQL，指纹 PG 1 票可补但未过 quorum → add 有 add_case 空
        "u/inc": {"fn": "u/inc", "status": "ok", "collected_at": TS,
                  "files": [dep("requirements.txt", ["mysql-connector-java", "psycopg2"])]},
        # 不完整：PG dep+image 3 票过 quorum → add_case 非空
        "u/inc_case": {"fn": "u/inc_case", "status": "ok", "collected_at": TS,
                       "files": [dep("requirements.txt", ["psycopg2"]),
                                 img("compose.yml", ["postgres:15"])]},
        # 反例：指纹命中库 ⊆ 现判 → 不进任何清单
        "u/full": {"fn": "u/full", "status": "ok", "collected_at": TS,
                   "files": [dep("requirements.txt", ["mysql-connector-java"])]},
        # 反例：empty_repo 无指纹 → 不进漏报（verdict no_evidence）
        "u/emptyrepo": {"fn": "u/emptyrepo", "status": "empty_repo", "collected_at": TS},
        # 反例：仅 topic（1 票）→ 不算指纹命中，不进漏报/双源
        "u/topiconly": {"fn": "u/topiconly", "status": "ok", "collected_at": TS},
        # 另册：有指纹无解读记录（新仓未解读）
        "u/nointerp": {"fn": "u/nointerp", "status": "ok", "collected_at": TS,
                       "files": [dep("requirements.txt", ["psycopg2"])]},
        # 不在池：星数走证据分片 stars
        "u/nopool": {"fn": "u/nopool", "status": "ok", "collected_at": TS, "stars": 7,
                     "files": [dep("requirements.txt", ["mysql-connector-java"])]},
        # 池里 stars=None → 排序记 -1 沉底
        "u/none_star": {"fn": "u/none_star", "status": "ok", "collected_at": TS,
                        "files": [img("compose.yml", ["mysql:8"])]},
        # 同星并列 → fn 升序保确定性
        "u/tie_a": {"fn": "u/tie_a", "status": "ok", "collected_at": TS,
                    "files": [img("compose.yml", ["mysql:8"])]},
        "u/tie_b": {"fn": "u/tie_b", "status": "ok", "collected_at": TS,
                    "files": [img("compose.yml", ["mysql:8"])]},
        # 防御：有文件无 collected_at → build_pack ValueError → skip 不炸
        "u/badts": {"fn": "u/badts", "status": "ok",
                    "files": [dep("requirements.txt", ["psycopg2"])]},
        # 防御：无 fn 记录
        "nokey": {"status": "ok", "collected_at": TS},
    }
    shard1 = {  # 第二分片：测流式 --limit 与跨分片
        "u/highstar": {"fn": "u/highstar", "status": "ok", "collected_at": TS, "stars": 9000,
                       "files": [img("compose.yml", ["mysql:8", "postgres:15"])]},
    }
    (ev / "00.json").write_text(json.dumps(shard0), encoding="utf-8")
    (ev / "01.json").write_text(json.dumps(shard1), encoding="utf-8")

    # interp 键 = fn 哈希（真实形态），值里带 fn——按 rec["fn"] 对齐
    interp = {f"h{i}": {"fn": fn, "classification": {"dbs": dbs}} for i, (fn, dbs) in enumerate([
        ("u/missed2", []), ("u/missed1", []), ("u/dual", []), ("u/inc", ["MySQL"]),
        ("u/inc_case", ["MySQL"]), ("u/full", ["MySQL"]), ("u/emptyrepo", []),
        ("u/topiconly", []), ("u/nopool", []), ("u/none_star", []),
        ("u/tie_a", []), ("u/tie_b", []), ("u/highstar", ["MySQL"]),
    ])}
    (ip / "00.json").write_text(json.dumps(interp), encoding="utf-8")

    pool = [  # pool.json 是 list，fn 在 full_name；nopool/nointerp/highstar/badts 不在池
        {"full_name": "u/missed2", "stars": 500, "topics": []},
        {"full_name": "u/missed1", "stars": 1200, "topics": []},
        {"full_name": "u/dual", "stars": 50, "topics": ["mysql", "database"]},
        {"full_name": "u/inc", "stars": 300, "topics": []},
        {"full_name": "u/inc_case", "stars": 400, "topics": []},
        {"full_name": "u/full", "stars": 10, "topics": []},
        {"full_name": "u/topiconly", "stars": 80, "topics": ["postgresql"]},
        {"full_name": "u/none_star", "stars": None, "topics": []},
        {"full_name": "u/tie_a", "stars": 100, "topics": []},
        {"full_name": "u/tie_b", "stars": 100, "topics": []},
    ]
    pool_path = base / "pool.json"
    pool_path.write_text(json.dumps(pool), encoding="utf-8")
    return ev, ip, pool_path


def main() -> int:
    fails: list[str] = []
    ck = lambda ok, msg: None if ok else fails.append(f"[FAIL] {msg}")  # noqa: E731

    with tempfile.TemporaryDirectory() as td:
        base = Path(td)
        ev, ip, pool_path = _build_universe(base)
        rep = S.scan(evidence_dir=ev, interp_dir=ip, pool_path=pool_path)

        # 1) 三清单一一对应：成员 + star 降序（无星 -1 沉底，同星 fn 升序）
        L = rep["lists"]
        got_missed = [e["fn"] for e in L["missed"]]
        want_missed = ["u/missed1", "u/missed2", "u/tie_a", "u/tie_b",
                       "u/dual", "u/nopool", "u/none_star"]
        ck(got_missed == want_missed, f"漏报清单应 star 降序：{got_missed}")
        ck([e["fn"] for e in L["incomplete"]] == ["u/highstar", "u/inc_case", "u/inc"],
           "不完整清单应 [highstar(9000), inc_case(400), inc(300)]")
        ck([e["fn"] for e in L["dual"]] == ["u/dual"], "双源清单应恰 [u/dual]")
        ck(set(got_missed) >= {e["fn"] for e in L["dual"]}, "双源应是漏报子集")
        for name in ("u/nointerp", "u/topiconly", "u/emptyrepo", "u/full", "u/badts"):
            ck(name not in got_missed, f"{name} 不应进漏报清单")
            ck(all(e["fn"] != name for e in L["incomplete"]), f"{name} 不应进不完整清单")

        # 2) 条目字段：quorum 立案数与 add/add_case 档位区分
        hs = L["incomplete"][0]                     # 第二分片高星仓：现判 MySQL 指纹补 PG
        ck(hs["stars"] == 9000 and hs["interp"] == ["MySQL"]
           and hs["add"] == ["PostgreSQL"] and hs["add_case"] == ["PostgreSQL"],
           f"highstar 条目：{hs}")
        m1 = L["missed"][0]
        ck(m1["fn"] == "u/missed1" and m1["stars"] == 1200 and m1["case"] == [],
           "单 dep 1 票 below_quorum → case 空（漏报按指纹命中收）")
        ns = next(e for e in L["missed"] if e["fn"] == "u/none_star")
        ck(ns["stars"] is None and ns["case"] == ["MySQL"], "池 stars=None 透传；镜像 2 票立案")
        inc = next(e for e in L["incomplete"] if e["fn"] == "u/inc")
        ck(inc["interp"] == ["MySQL"] and inc["add"] == ["PostgreSQL"]
           and inc["add_case"] == [], f"inc：add 有 add_case 空（未过 quorum）：{inc}")
        icc = L["incomplete"][0]
        ck(icc["add"] == ["PostgreSQL"] and icc["add_case"] == ["PostgreSQL"],
           "inc_case：3 票过 quorum → add_case 非空")
        np_ = next(e for e in L["missed"] if e["fn"] == "u/nopool")
        ck(np_["stars"] == 7, "不在池 → 星数走证据分片 stars")
        ck(L["dual"][0]["dual"] == ["MySQL"], "双源条目 dual=topic∩指纹")

        # 3) universe 对账：另册/防御计数 + 判定直方图（全记录有归宿）
        u = rep["universe"]
        ck(u["evidence"] == 15 and u["rec_no_fn"] == 1, f"evidence/rec_no_fn：{u.get('evidence')}/{u.get('rec_no_fn')}")
        ck(u["status_ok"] == 14 and u["status_empty_repo"] == 1, "状态直方图")
        ck(u["skip_bad_pack"] == 1, "缺 collected_at → skip_bad_pack 不炸")
        ck(u["interp_linked"] == 13 and u["interp_missing"] == 1, "交集/未解读另册")
        ck(u["interp_empty"] == 9 and u["fp_hit"] == 12, f"interp_empty/fp_hit：{u.get('interp_empty')}/{u.get('fp_hit')}")
        ck(u["verdict_case_opened"] == 7 and u["verdict_below_quorum"] == 6
           and u["verdict_no_evidence"] == 1, "判定分布 7/6/1")
        ck(rep["counts"] == {"missed": 7, "incomplete": 3, "dual": 1}, rep["counts"])
        ck(rep["per_db_add"] == {"PostgreSQL": 3}, "可补库位直方图")
        ck(rep["engine"] == ENGINE_VERSION and rep["case_opened_db"]["MySQL"] == 6,
           "引擎版本/立案直方图（MySQL 6 仓，inc_case/highstar 只立 PG）")

        # 4) 流式 --limit：只处理第一个分片（highstar 在 01.json）
        lim = S.scan(evidence_dir=ev, interp_dir=ip, pool_path=pool_path, limit_shards=1)
        ck(lim["universe"]["evidence"] == 14, "--limit 1 少一个分片")
        ck(all(e["fn"] != "u/highstar" for e in lim["lists"]["incomplete"]),
           "limit 不触第二分片")
        ck(lim["shard_limit"] == 1, "limit 记入台账")

        # 5) 池快照缺席：topic 全空、星数走分片，扫描不炸
        nop = S.scan(evidence_dir=ev, interp_dir=ip, pool_path=base / "nope.json")
        ck(nop["lists"]["dual"] == [], "无池 → 无 topic → 双源空")
        ck(len(nop["lists"]["missed"]) == 7, "无池 → 漏报照收（星数走分片）")

        # 6) 确定性：两跑除 generated_at 外逐字段相等（在副本上 pop，rep 留给 9) 用）
        again = S.scan(evidence_dir=ev, interp_dir=ip, pool_path=pool_path)
        a, b = dict(rep), dict(again)
        a.pop("generated_at"), b.pop("generated_at")
        ck(a == b, "scan 非确定（可 diff 验收前提）")

        # 7) 落盘：台账 JSON 可读回 + 复核表三清单标题/表头/行
        out = base / "state"
        out.mkdir()
        S.write_gap(again, out)
        back = json.loads((out / "attribution_gap.json").read_text(encoding="utf-8"))
        ck(back["counts"] == rep["counts"] and len(back["lists"]["missed"]) == 7, "台账回读")
        md = (out / "attribution_gap.md").read_text(encoding="utf-8")
        for t in S.LIST_TITLES.values():
            ck(t in md, f"复核表缺清单标题：{t}")
        ck("| 1 | u/missed1 | 1,200 | PostgreSQL | — |" in md
           and "| 1 | u/highstar | 9,000 | MySQL | PostgreSQL | PostgreSQL |" in md,
           "复核表首行（star 千分位+库加号拼接+未立案长划）")
        ck("漏报 7 / 不完整 3 / 双源 strong 1" in md, "复核表计数行")

        # 8) 验收门：数字说话（≥1,400/≥1,300/≥700）
        good = S._acceptance_ok({"missed": 1500, "incomplete": 1400, "dual": 800})
        ck(all(s.endswith("✓") for s in good), f"达标应全 ✓：{good}")
        bad = S._acceptance_ok({"missed": 1399, "incomplete": 1300, "dual": 699})
        ck(sum(s.endswith("✗") for s in bad) == 2, f"不达标应 2 ✗：{bad}")

        # 9) CLI 接线：--status/--gap/验收退出码（stub 掉扫描与落盘，只测接线）
        orig_scan, orig_write = S.scan, S.write_gap
        written = []
        ok_rep = dict(rep)
        ok_rep["counts"] = {"missed": 1500, "incomplete": 1400, "dual": 800}
        low = dict(rep)
        low["counts"] = {"missed": 100, "incomplete": 100, "dual": 100}
        try:
            S.scan = lambda **kw: ok_rep
            S.write_gap = lambda r, d=None: written.append(1) or (None, None)
            ck(S.main([]) == 2, "无参 → usage 退出码 2")
            ck(S.main(["--status"]) == 0, "--status 退出码 0")
            ck(S.main(["--gap"]) == 0 and written, "--gap 落盘+验收过 → 0")
            S.scan = lambda **kw: low
            ck(S.main(["--gap"]) == 1, "验收不过 → 退出码 1")
            ck(S.main(["--gap", "--limit", "2"]) == 0, "--limit 冒烟不卡验收线")
        finally:
            S.scan, S.write_gap = orig_scan, orig_write

    verdict = "PASS" if not fails else "FAIL"
    print(f"[{verdict}] 三清单口径（7 漏报/3 不完整/1 双源 + 5 反例另册）+ star 降序确定性"
          f"+ quorum 档位区分 + 流式 --limit + 无池防御 + 台账/复核表落盘 + 验收门")
    for f in fails:
        print(f)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
