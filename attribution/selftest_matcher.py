# -*- coding: utf-8 -*-
"""T2b 离线自检：指纹×词表×topic 三规则匹配器。零网络。

跑法：python attribution/selftest_matcher.py（退出码 0=全绿）
覆盖：topic 三规则（专有名/泛词排除/归一）、镜像段匹配、路径段边界、
弱路径票档、43 个 recheck 活案例合成重构（票档与报告 weak/dep_only 标注
逐条对齐）、nopCommerce 真实快照（SQL Server 指纹+topic 同库互证非冲突）、
互补标记（矛盾=互补不丢弃）、防御（partial/sha_mismatch/dev-only/缺时间戳）。
素材全部来自 fixtures/recheck_cases.json 冻结快照——分片后续重采不破坏本测试。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from attribution.api import judge
from attribution.evidence_model import normalize_pack
from attribution.matcher import (
    GENERIC_TOPICS, _TOPIC_VIEW, build_pack, is_weak_path, match_filename,
    match_image, match_path, match_topic,
)

FIX = json.loads((ROOT / "attribution" / "fixtures" / "recheck_cases.json")
                 .read_text(encoding="utf-8"))
TS = "2026-10-30T15:10:33Z"


def main() -> int:
    fails: list[str] = []
    ck = lambda ok, msg: None if ok else fails.append(f"[FAIL] {msg}")  # noqa: E731

    # 1) topic 三规则：专有名才算 + 归一 + 泛词排除
    ck(match_topic("sqlserver") == "SQL Server", "topic sqlserver 应命中 SQL Server")
    ck(match_topic("sql-server") == "SQL Server", "归一：sql-server")
    ck(match_topic("SQL_Server") == "SQL Server", "归一：大小写")
    ck(match_topic("postgresql") == "PostgreSQL" and match_topic("postgres") == "PostgreSQL",
       "topic postgresql/postgres → PostgreSQL")
    ck(match_topic("sqlite3") == "SQLite", "topic sqlite3（topics 通道词）→ SQLite")
    ck(match_topic("tidb") == "TiDB" and match_topic("oceanbase") == "OceanBase", "国产库 topic")
    for generic in ("database", "sql", "rdbms", "dbms", "javascript", ""):
        ck(match_topic(generic) is None, f"泛词/未知 topic '{generic}' 应为 None")
    ck(not (GENERIC_TOPICS & set(_TOPIC_VIEW)), "泛词与库 topic 词冲突")
    ck(set(_TOPIC_VIEW.values()) == {p["name"] for p in __import__(
        "config.db_profiles", fromlist=["PROFILES"]).PROFILES if p.get("enabled", True)},
       "topic 视图应覆盖 17 库")

    # 2) 镜像段匹配：tag/digest/registry 剥离 + 段相等不子串
    ck([h["db"] for h in match_image("postgres:15")] == ["PostgreSQL"], "镜像 postgres:15")
    ck([h["db"] for h in match_image("mcr.microsoft.com/mssql/server:2019-latest")]
       == ["SQL Server"], "registry 前缀 mssql 镜像")
    ck([h["db"] for h in match_image("pingcap/tidb:v8.5.0")] == ["TiDB"], "多段词 pingcap/tidb")
    ck([h["db"] for h in match_image("postgres@sha256:abc123")] == ["PostgreSQL"], "digest 剥离")
    ck(match_image("keinos/sqlite3:latest")[0]["db"] == "SQLite", "命名空间镜像 sqlite3")
    ck(not match_image("postgresml/postgresml:latest"), "postgresml 不得撞 postgres")
    ck(not match_image("mysql-backup"), "mysql-backup 不得撞 mysql")

    # 3) 路径段边界：前缀可过（psycopg2）、字母粘连不过（oraclelinux）
    ck(any(h["db"] == "PostgreSQL" for h in match_path("src/psycopg2/__init__.py")),
       "psycopg ⊂ psycopg2 段前缀")
    ck(not any(h["db"] == "Oracle" for h in match_path("drivers/oraclelinux/fs/")),
       "oraclelinux 不得撞 oracle")
    ck(any(h["db"] == "SQL Server" for h in match_path("src/sql_server/conn.cs")),
       "sql_server 整段")
    ck(any(h["db"] == "PostgreSQL" for h in match_path("drivers/postgres/util")),
       "drivers/postgres")
    for weak, strong in (("examples/x", "src/x"), ("Tests/Net5TestProject/a.cs", "go.mod"),
                         ("testdata/sqlc.rs", "lib/conn.rs"), ("benches/a.rs", "bin/a.rs")):
        ck(is_weak_path(weak) and not is_weak_path(strong), f"弱路径判定 {weak} vs {strong}")
    ck(not is_weak_path("attest/latest"), "字母粘连 latest/attest 非弱路径")

    # 4) 43 个 recheck 活案例合成重构：dep 命中 ⊆ 报告 dbs + 票档对齐 weak/dep_only。
    #    唯一分歧：NoKV-Lab/holt 旧侦查把 benches/Cargo.toml 标 dep_only，但 benches
    #    与 benchmarks 同语义（Cargo 基准目录）——规则判 0.5 更严，此处按规则锁。
    KNOWN_DIVERGENCE = {"NoKV-Lab/holt"}
    for c in FIX["cases"]:
        rec = {"fn": c["fn"], "status": "ok", "collected_at": TS,
               "files": [{"path": c["path"], "kind": "dep", "names": [c["word"]]}]}
        try:
            pack = build_pack(c["fn"], rec)
        except Exception as e:                                   # noqa: BLE001
            fails.append(f"[FAIL] {c['fn']} 构包炸：{e}")
            continue
        deps = [e for e in pack["evidences"] if e["kind"] == "dep"]
        if not deps:
            fails.append(f"[FAIL] {c['fn']}：{c['word']} 未产 dep 证据")
            continue
        if any(e["db"] not in c["dbs"] for e in deps):
            fails.append(f"[FAIL] {c['fn']}：dep 命中超出报告 dbs "
                         f"{[e['db'] for e in deps]} ∉ {c['dbs']}")
        want = 0.5 if (c["strength"] == "weak" or c["fn"] in KNOWN_DIVERGENCE) else 1.0
        if any(e["votes"] != want for e in deps):
            fails.append(f"[FAIL] {c['fn']}：票档 { [e['votes'] for e in deps] } 应全 {want}"
                         f"（报告标注 {c['strength']}，路径 {c['path']}）")
        try:
            normalize_pack(pack)
        except ValueError as e:
            fails.append(f"[FAIL] {c['fn']} 包不过 T2a schema：{e}")

    # 5) nopCommerce 真实快照：指纹(SQL Server dep+镜像)×topic(sqlserver) 同库互证
    snap = FIX["snapshots"]["nopsolutions/nopcommerce"]
    pack = build_pack(snap["fn"], snap, {"topics": FIX["topics"]["nopsolutions/nopcommerce"]})
    v = judge(pack)
    ss = v["per_db"].get("SQL Server", {})
    ck(ss.get("votes") == 5.0, f"SQL Server 应 5.0 票(dep1+image2+topic2)：{ss.get('votes')}")
    ck(ss.get("kinds") == {"dep": 1, "image": 1, "topic": 1}, f"SQL Server kinds：{ss.get('kinds')}")
    ck(v["per_db"].get("MySQL", {}).get("votes") == 1.0, "MySQL dep 1 票")
    ck(v["per_db"].get("PostgreSQL", {}).get("votes") == 1.0, "PostgreSQL dep 1 票")
    ck("topic_complement" not in pack["meta"], "topic(SQL Server) 与指纹同库互证，非互补")
    ck(v["status"] == "case_opened" and v["dbs"] == ["SQL Server"],
       f"SQL Server 4.0 票(dep+image+topic 三证)应立案：{v['dbs']}")

    # 6) 矛盾=互补：topic 库无指纹同库命中 → 互补标记，不判冲突不丢弃
    pack = build_pack("x/y", {"fn": "x/y", "status": "ok", "collected_at": TS,
                              "files": [{"path": "go.mod", "kind": "dep",
                                         "names": ["go-sql-driver/mysql"]}]},
                      {"topics": ["tidb", "database"]})
    top = [e for e in pack["evidences"] if e["kind"] == "topic"]
    ck(len(top) == 1 and top[0]["db"] == "TiDB" and top[0]["detail"].get("complementary"),
       "topic tidb 应带 complementary=True")
    ck(pack["meta"].get("topic_complement") == ["TiDB"], "meta.topic_complement")
    ck(len(pack["evidences"]) == 2, f"泛词 database 不产证据：{len(pack['evidences'])} 条")

    # 7) 防御：partial 不产 / sha_mismatch·parse_error 跳过 / dev-only 降档 / 缺时间戳
    base_files = [{"path": "pom.xml", "kind": "dep", "names": ["psycopg2"]}]
    ck(not build_pack("a/b", {"fn": "a/b", "status": "partial", "files": base_files})["evidences"],
       "status=partial 不产指纹证据")
    bad = {"fn": "a/b", "status": "ok", "collected_at": TS,
           "files": [{"path": "pom.xml", "kind": "dep", "names": ["psycopg2"], "sha_mismatch": True},
                     {"path": "x/pom.xml", "kind": "dep", "names": ["psycopg2"], "parse_error": True}]}
    ck(not build_pack("a/b", bad)["evidences"], "sha_mismatch/parse_error 文件跳过")
    devf = {"fn": "a/b", "status": "ok", "collected_at": TS,
            "files": [{"path": "package.json", "kind": "dep", "names": [], "dev": ["sqlite3"]}]}
    de = build_pack("a/b", devf)["evidences"]
    ck(len(de) == 1 and de[0]["votes"] == 0.5 and de[0]["detail"].get("dev"),
       "dev-only 命中 0.5 票带 dev 标")
    mix = {"fn": "a/b", "status": "ok", "collected_at": TS,
           "files": [{"path": "package.json", "kind": "dep", "names": ["sqlite3"], "dev": ["sqlite3"]}]}
    me = build_pack("a/b", mix)["evidences"]
    ck(len(me) == 1 and me[0]["votes"] == 1.0 and "dev" not in me[0]["detail"],
       "main+dev 同库：非 dev 命中为准 1 票")
    ci_rec = {"fn": "a/b", "status": "ok", "collected_at": TS,
              "files": [{"path": ".github/workflows/ci.yml", "kind": "ci", "images": ["mysql:8"]}]}
    ce = build_pack("a/b", ci_rec)["evidences"]
    ck(len(ce) == 1 and ce[0]["kind"] == "ci" and ce[0]["votes"] == 0.5, "ci 矩阵镜像 0.5 票")
    try:
        build_pack("a/b", None, {"topics": ["mysql"]})
        fails.append("[FAIL] 有 topic 无时间戳应 ValueError")
    except ValueError:
        pass
    ck(build_pack("a/b")["evidences"] == [] and judge(build_pack("a/b"))["status"] == "no_evidence",
       "无证据仓 → 空包 no_evidence（42/43 历史出池路径）")

    # 8) pivotlake 真实快照：schema 合法可判（不锁命中集——tokio-postgres 词表
    #    缺口已呈报待 T1a 补词，锁死会挡补词回归）
    pv = FIX["snapshots"]["pivotlake/pivot"]
    try:
        v = judge(build_pack(pv["fn"], pv, {"topics": FIX["topics"]["pivotlake/pivot"]}))
        ck(v["status"] in ("no_evidence", "below_quorum", "case_opened"),
           "pivotlake 可判不炸")
    except Exception as e:                                       # noqa: BLE001
        fails.append(f"[FAIL] pivotlake 构包炸：{e}")

    # 9) v0.3.0 新信号①文件名模式：前缀+库 token；弱路径降 0.5；误伤反例
    ck(any(h["db"] == "TiDB" for h in match_filename("pkg/server/driver_tidb.go")),
       "driver_tidb.go 应命中 TiDB（旧 E1 FILE_PAT 移植）")
    ck(any(h["db"] == "MySQL" for h in match_filename("src/conn_mysql.py")),
       "conn_mysql.py 应命中 MySQL")
    ck(not match_filename("conn_oraclelinux.py"), "conn_oraclelinux 不得撞 oracle")
    ck(not match_filename("driver_tidb.go.bak"), "扩展名不符不命中")
    fn_ev = build_pack("acme/x", {"fn": "acme/x", "status": "ok",
                                  "collected_at": TS,
                                  "clues": {"paths": ["pkg/server/driver_tidb.go"]}})
    te = [e for e in fn_ev["evidences"] if e["kind"] == "tree"]
    ck(len(te) == 1 and te[0]["db"] == "TiDB" and te[0]["votes"] == 2.0,
       "driver_tidb.go 强路径 2 票 tree")
    wk = build_pack("acme/x", {"fn": "acme/x", "status": "ok", "collected_at": TS,
                               "clues": {"paths": ["tests/driver_mysql.go"]}})
    ck(any(e["votes"] == 0.5 for e in wk["evidences"]), "tests/ 下文件名证据降 0.5")

    # 10) v0.3.0 新信号②官方 org：owner 精确命中 1 票（全家桶误伤校准：
    #     TencentCloud SDK/tikv 通用库 org-only 不立案进 recheck）
    ob = build_pack("pingcap/whatever", {"fn": "pingcap/whatever", "status": "ok",
                                         "collected_at": TS})
    org = [e for e in ob["evidences"] if e["kind"] == "tree"]
    ck(len(org) == 1 and org[0]["db"] == "TiDB" and org[0]["votes"] == 1.0
       and org[0]["source"] == "org:pingcap", "官方 org pingcap → TiDB 1 票")
    v = judge(ob)
    ck(v["status"] == "below_quorum" and v["dbs"] == [],
       "org-only（无指纹无 topic）不立案——tikv/grpc-rs 全家桶防线")
    pe = build_pack("percona/x", {"fn": "percona/x", "status": "ok", "collected_at": TS})
    ck({e["db"] for e in pe["evidences"]} == {"PostgreSQL", "MySQL"},
       "percona 双挂 PG+MySQL（真实双生态双标）")
    sse = build_pack("SSE-DZH/OceanBase", {"fn": "SSE-DZH/OceanBase", "status": "ok",
                                           "collected_at": TS})
    ck(not sse["evidences"], "SSE-DZH 非官方 org：仓名子串不推断（规则 2 保持）")
    # 用户裁定回放：pingcap/tidb 形态（org+文件名+topic）→ TiDB+MySQL 双标
    pt = build_pack("pingcap/tidb", {"fn": "pingcap/tidb", "status": "ok",
                                     "collected_at": TS,
                                     "files": [{"path": "go.mod", "kind": "dep",
                                                "names": ["go-sql-driver/mysql"]}],
                                     "clues": {"paths": ["pkg/server/driver_tidb.go"]}},
                    {"topics": ["tidb", "mysql"]})
    v = judge(pt)
    ck(v["dbs"] == ["TiDB", "MySQL"], f"pingcap/tidb 应双标：{v['dbs']}")
    ck(v["per_db"]["TiDB"]["votes"] == 5.0, "TiDB org1+文件名2+topic2=5.0")

    verdict = "PASS" if not fails else "FAIL"
    print(f"[{verdict}] topic 三规则 + 镜像/路径段匹配 + 弱路径 + 43 案例重构"
          f"（票档对齐 weak/dep_only）+ nopCommerce 互证 5.0 票 + 互补标记 + 防御 8 组"
          f"+ v0.3.0 文件名模式 2 票/官方 org 1 票（pingcap 双标 5.0 回放、"
          f"org-only 不立案、SSE-DZH 不推断）")
    for f in fails:
        print(f)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
