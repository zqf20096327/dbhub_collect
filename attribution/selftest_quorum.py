# -*- coding: utf-8 -*-
"""T2c 离线自检：quorum 票制立案 + E-CI 消歧三规则。零网络。

跑法：python attribution/selftest_quorum.py（退出码 0=全绿）
活案例（卡文验收钦定，素材 fixtures/ci_cases.json 冻结快照）：
  SSE-DZH/OceanBase 纯国际依赖 → 不猜 OceanBase（真实快照单证 below_quorum；
  双证合成 → 只判 MySQL）；加 oceanbase 镜像 → 双标 MySQL+OceanBase；
  单 topic → 立案但打 single_strong 注记（v0.3.0 用户裁定：明确标注须判出，
  纯 topic 立案的降级防线在 unattr_judge 薄壳）。
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from attribution.api import ENGINE_VERSION, judge
from attribution.evidence_model import normalize_pack
from attribution.matcher import build_pack
from attribution.quorum import QUORUM_THRESHOLD, vote
from attribution.rules_ci import CN_DBS, CN_COMPAT_BASE, compat_bases, is_cn

FIX = json.loads((ROOT / "attribution" / "fixtures" / "ci_cases.json")
                 .read_text(encoding="utf-8"))
TS = "2026-10-30T15:10:33Z"


def main() -> int:
    fails: list[str] = []
    ck = lambda ok, msg: None if ok else fails.append(f"[FAIL] {msg}")  # noqa: E731

    # 1) 活案例①：真实快照——纯国际单证 1 票，below_quorum 且不猜 OceanBase
    v = judge(build_pack("SSE-DZH/OceanBase", FIX["sse_real"],
                         {"topics": FIX["sse_topics"]}))
    ck(v["status"] == "below_quorum", f"真实快照应 below_quorum：{v['status']}")
    ck(v["dbs"] == [], "单证 1 票不得立案")
    ck(set(v["per_db"]) == {"MySQL"} and v["per_db"]["MySQL"]["votes"] == 1.0,
       f"真实快照只有 MySQL 1 票方向：{ {k: e['votes'] for k, e in v['per_db'].items()} }")
    ck("OceanBase" not in v["per_db"], "不猜国产：OceanBase 不得凭仓名出现（规则 2）")

    # 2) 活案例②：纯国际双证（pom + 树路径）→ 只判 MySQL 不判 OceanBase
    rec = copy.deepcopy(FIX["sse_real"])
    rec["clues"]["paths"] = ["src/main/java/com/mysql/connector"]
    v = judge(build_pack("SSE-DZH/OceanBase", rec, {"topics": FIX["sse_topics"]}))
    ck(v["status"] == "case_opened" and v["dbs"] == ["MySQL"],
       f"纯国际双证应只立案 MySQL：{v['dbs']}")
    ck(not (set(v["dbs"]) & CN_DBS), "纯国际证据不得立案任何国产库（规则 2）")

    # 3) 活案例③：加 oceanbase 镜像（MySQL 保持单证 1 票）→ OB 单证 strong 立案
    #    + MySQL 靠兼容基座联动双标——联动的存在意义正是补齐单证基座
    rec = copy.deepcopy(FIX["sse_real"])
    rec["files"].append({"path": "docker-compose.yml", "kind": "image",
                         "images": ["oceanbase/oceanbase:4.2.1"]})
    v = judge(build_pack("SSE-DZH/OceanBase", rec, {"topics": FIX["sse_topics"]}))
    ck(v["dbs"] == ["OceanBase", "MySQL"], f"镜像版应双标：{v['dbs']}")
    ck(v["per_db"]["OceanBase"]["votes"] == 2.0
       and v["per_db"]["MySQL"]["votes"] == 1.0, "双标票数 OB 镜像 2.0 / MySQL dep 1.0")
    ck(any("single_strong" in n and "OceanBase" in n for n in v["notes"]),
       "镜像单证 strong 应打 single_strong 注记（不放直通）")
    ck(any("ci_linkage" in n and "MySQL" in n for n in v["notes"]),
       "OceanBase 立案应 ci_linkage 联动 MySQL（规则 3）")

    # 4) 活案例④（v0.3.0 用户裁定改写）：topic 自声明 2 票单证立案 + single_strong
    #    注记 + recheck 留互补；纯 topic 立案的降级防线在 unattr_judge 薄壳（T2e）。
    v = judge({"fn": "a/b", "evidences": [
        {"kind": "topic", "db": "TiDB", "votes": 2.0, "source": "topic:tidb",
         "collected_at": TS}]})
    ck(v["status"] == "case_opened" and v["dbs"] == ["TiDB"],
       f"单 topic 2 票应立案（明确标注须判出）：{v['dbs']}")
    ck(any("single_strong" in n and "topic" in n for n in v["notes"]),
       "topic 单证立案应打 single_strong 注记（须复核不放直通）")

    # 5) topic 互补进 recheck；与指纹双源同库则不进
    pack = build_pack("a/b", {"fn": "a/b", "status": "ok", "collected_at": TS,
                              "files": [{"path": "go.mod", "kind": "dep",
                                         "names": ["go-sql-driver/mysql"]}]},
                      {"topics": ["tidb"]})
    v = judge(pack)
    ck(v["recheck"] == ["TiDB"], f"topic 独有库应进 recheck：{v['recheck']}")
    v2 = judge(build_pack("a/b", {"fn": "a/b", "status": "ok", "collected_at": TS,
                                  "files": [{"path": "go.mod", "kind": "dep",
                                             "names": ["go-sql-driver/mysql"]},
                                            {"path": "docker-compose.yml", "kind": "image",
                                             "images": ["pingcap/tidb"]}]},
                          {"topics": ["tidb"]}))
    ck(v2["recheck"] == [], f"topic 与指纹同库互证不进 recheck：{v2['recheck']}")
    ck(v2["dbs"] == ["TiDB", "MySQL"], f"TiDB 镜像立案联动 MySQL：{v2['dbs']}")
    ck(v2["per_db"]["TiDB"]["votes"] == 4.0, "TiDB 镜像2+topic2=4.0")
    ck(v2["per_db"]["MySQL"]["votes"] == 1.0, "MySQL 仅 dep 1 票，靠联动立案")

    # 6) 票制边界：三弱信号 0.5×4=2.0 立案；1.5 不立案；阈值恰 2.0 立案
    def _pack(votes_list, db="SQLite"):
        return {"fn": "x/y", "evidences": [
            {"kind": "dep", "db": db, "votes": v, "source": f"f{i}.toml",
             "collected_at": TS} for i, v in enumerate(votes_list)]}
    ck(judge(_pack([0.5, 0.5, 0.5, 0.5]))["dbs"] == ["SQLite"], "0.5×4=2.0 应立案")
    ck(judge(_pack([1.0, 0.5]))["dbs"] == [], "1.5 不立案")
    ck(judge(_pack([1.0, 1.0]))["dbs"] == ["SQLite"], "恰 2.0 立案")
    ck(judge(_pack([2.0]))["dbs"] == ["SQLite"], "2 票单证立案（注记须复核）")

    # 7) rules_ci 单元：国产集合 + 兼容基座映射 + 结构保障
    ck(len(CN_DBS) == 10 and not (CN_DBS & {"MySQL", "PostgreSQL", "Oracle", "SQLite",
                                            "SQL Server", "ClickHouse", "MariaDB"}),
       "国产 10 库与国际 7 库不相交")
    ck(compat_bases("TiDB") == ("MySQL",) and compat_bases("OceanBase") == ("MySQL",),
       "TiDB/OceanBase 兼容 MySQL")
    ck(compat_bases("openGauss") == ("PostgreSQL",) and compat_bases("GaussDB") == ("PostgreSQL",),
       "openGauss/GaussDB 兼容 PostgreSQL")
    ck(set(compat_bases("PolarDB")) == {"MySQL", "PostgreSQL"}, "PolarDB 双形态")
    ck(compat_bases("Dameng") == ("Oracle",) and compat_bases("YashanDB") == ("Oracle",),
       "Dameng/YashanDB 兼容 Oracle")
    ck(compat_bases("GBase") == () and compat_bases("TDSQL") == ()
       and compat_bases("GoldenDB") == (), "GBase/TDSQL/GoldenDB 宁缺勿滥不联动")
    ck(compat_bases("MySQL") == () and not is_cn("MySQL"), "国际库无基座")
    ck(set(CN_COMPAT_BASE) <= CN_DBS, "基座映射只指向国产库")
    ck(QUORUM_THRESHOLD == 2.0, "立案阈值 2.0")

    # 8) 确定性与纯度：vote 不改入参；同包两次判定相等；引擎版本带出
    src = {"fn": "a/b", "meta": {}, "engine": ENGINE_VERSION, "dbs": [],
           "per_db": {"MySQL": {"votes": 2.0, "kinds": {"dep": 2}, "chain": [
               {"kind": "dep", "db": "MySQL", "votes": 1.0, "source": "a", "collected_at": TS},
               {"kind": "dep", "db": "MySQL", "votes": 1.0, "source": "b", "collected_at": TS}]}},
           "notes": []}
    frozen = copy.deepcopy(src)
    out = vote(src)
    ck(src == frozen, "vote 不得改动入参")
    ck(out["dbs"] == ["MySQL"] and out["status"] == "case_opened", "vote 直连可用")
    ck(judge(_pack([1.0])) == judge(_pack([1.0])), "同输入同输出")
    ck(judge(_pack([1.0]))["engine"] == ENGINE_VERSION, "引擎版本带出")

    # 9) 空包不炸（T2a 契约在 quorum 接线后保持）
    ck(judge(None)["status"] == "no_evidence" and judge({})["dbs"] == [], "空包全空结论")
    ck(normalize_pack(build_pack("a/b")) is not None, "空包 schema 合法")

    verdict = "PASS" if not fails else "FAIL"
    print(f"[{verdict}] 活案例四断言（真实快照不猜国产/双证判 MySQL/镜像双标/单 topic 立案须复核）"
          f"+ recheck 互补 + 票制边界 4 组 + rules_ci 映射 + 确定性 + 空包不炸")
    for f in fails:
        print(f)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
