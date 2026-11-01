# 适配缺口报告（attribution scan --gap）

- 生成 2026-11-01T06:09:44Z · 引擎 0.3.0 · 比对域：证据 31,884 条（ok 31,345） ∩ 解读 30,169（未解读另册 1,715）
- **漏报 2,483 / 不完整 1,710 / 双源 strong 1,343**（10-31 实测 1,468 / 1,432 / 778，验收线 ≥1,400 / ≥1,300 / ≥700）
- 口径：dbs=解读分片 classification.dbs；指纹命中=dep/image/ci/tree 四型证据（仅 topic 不算）；双源=漏报子集；star 降序

- 不完整可补库位 Top：MySQL 876 · PostgreSQL 406 · SQLite 255 · SQL Server 184 · MariaDB 126 · Oracle 97 · ClickHouse 95 · OceanBase 30 · TiDB 19 · openGauss 19

## 清单一 · 漏报（匹配不到：dbs 空、指纹有命中） —— 2,483 仓

| # | 仓 | star | 指纹命中 | 立案(quorum) |
|---|---|---|---|---|
| 1 | netdata/netdata | 80,810 | MySQL+PostgreSQL+SQL Server | MySQL+PostgreSQL |
| 2 | grafana/grafana | 77,112 | MySQL+PostgreSQL | MySQL+PostgreSQL |
| 3 | usememos/memos | 63,563 | MySQL+PostgreSQL | SQLite |
| 4 | coollabsio/coolify | 62,659 | PostgreSQL | PostgreSQL+MariaDB+MySQL |
| 5 | makeplane/plane | 60,450 | PostgreSQL | PostgreSQL |
| 6 | metabase/metabase | 49,557 | ClickHouse+MariaDB+MySQL+PostgreSQL | ClickHouse+PostgreSQL+MySQL |
| 7 | payloadcms/payload | 45,113 | PostgreSQL+SQLite | PostgreSQL |
| 8 | cockroachdb/cockroach | 32,551 | PostgreSQL | PostgreSQL |
| 9 | supermemoryai/supermemory | 31,122 | PostgreSQL | PostgreSQL |
| 10 | TencentCloud/TencentDB-Agent-Memory | 29,863 | TDSQL | — |
| 11 | taosdata/TDengine | 25,151 | MySQL+PostgreSQL | — |
| 12 | dubinc/dub.link | 24,998 | MySQL | — |
| 13 | tursodatabase/turso | 24,655 | SQLite | SQLite |
| 14 | dolthub/dolt | 24,582 | MariaDB+MySQL+PostgreSQL+SQL Server | MySQL+MariaDB |
| 15 | sinaptik-ai/pandas-ai | 23,846 | MySQL+Oracle+PostgreSQL+SQL Server | Oracle+PostgreSQL |
| 16 | oracle/graal | 21,728 | Oracle | Oracle |
| 17 | eosphoros-ai/DB-GPT | 20,079 | MySQL+OceanBase | MySQL |
| 18 | sqlc-dev/sqlc | 18,347 | ClickHouse+MySQL+PostgreSQL+SQL Server+SQLite | MySQL+PostgreSQL+SQL Server+SQLite+ClickHouse |
| 19 | xerj-org/xerj | 17,555 | SQLite | — |
| 20 | questdb/questdb | 17,423 | PostgreSQL | PostgreSQL |
| 21 | tikv/tikv | 16,931 | TiDB | — |
| 22 | zhisheng17/flink-learning | 15,097 | MySQL | MySQL+ClickHouse |
| 23 | TencentCloud/CubeSandbox | 13,024 | TDSQL | — |
| 24 | StarRocks/starrocks | 12,158 | MariaDB+MySQL | MariaDB+MySQL |
| 25 | pingcap/awesome-database-learning | 11,174 | TiDB | — |
| 26 | blinkospace/blinko | 11,062 | PostgreSQL+SQLite | PostgreSQL |
| 27 | pingcap/talent-plan | 11,030 | TiDB | — |
| 28 | zfile-dev/zfile | 10,853 | MySQL+SQLite | MySQL |
| 29 | getlago/lago | 10,661 | ClickHouse+PostgreSQL | ClickHouse+PostgreSQL |
| 30 | yugabyte/yugabyte-db | 10,580 | PostgreSQL | PostgreSQL |
| 31 | doctrine/dbal | 9,702 | MariaDB+MySQL+PostgreSQL+SQL Server | MariaDB+MySQL+PostgreSQL+SQL Server+Oracle+SQLite |
| 32 | activeloopai/deeplake | 9,248 | PostgreSQL | PostgreSQL |
| 33 | codenotary/immudb | 9,041 | PostgreSQL | — |
| 34 | benawad/dogehouse | 9,017 | PostgreSQL | PostgreSQL |
| 35 | growthbook/growthbook | 8,478 | ClickHouse+MySQL+PostgreSQL+SQL Server | ClickHouse+MySQL+SQL Server+PostgreSQL |
| 36 | jOOQ/jOOQ | 6,794 | ClickHouse+MariaDB+PostgreSQL | PostgreSQL+MySQL+Oracle+SQL Server |
| 37 | TableProApp/TablePro | 6,214 | ClickHouse+MySQL+PostgreSQL+SQL Server | MySQL+PostgreSQL+SQL Server+SQLite |
| 38 | liquibase/liquibase | 5,621 | MariaDB+MySQL+Oracle+PostgreSQL+SQL Server+SQLite | MariaDB+SQL Server+MySQL+Oracle+PostgreSQL |
| 39 | lukevella/rallly | 5,293 | PostgreSQL | PostgreSQL |
| 40 | malisper/pgrust | 5,233 | PostgreSQL | PostgreSQL |
| 41 | oracle/opengrok | 4,970 | Oracle | — |
| 42 | pudo/dataset | 4,874 | MySQL+PostgreSQL | — |
| 43 | backup/backup | 4,856 | MySQL+PostgreSQL | MySQL+PostgreSQL |
| 44 | linhaojun857/aurora | 4,663 | MySQL | MySQL |
| 45 | supabase/supabase-js | 4,576 | PostgreSQL | PostgreSQL |
| 46 | crate/crate | 4,443 | PostgreSQL | PostgreSQL |
| 47 | oceanbase/miniob | 4,427 | OceanBase | — |
| 48 | cozodb/cozo | 4,131 | SQLite | — |
| 49 | flippercloud/flipper | 3,972 | MySQL+PostgreSQL+SQLite | PostgreSQL+MySQL |
| 50 | rbmonster/learning-note | 3,815 | MySQL | MySQL |

… 其余 2,433 仓见台账 JSON

## 清单二 · 不完整（已归但指纹显示还支持别的） —— 1,710 仓

| # | 仓 | star | 现判 dbs | 可补(指纹) | 可补(立案) |
|---|---|---|---|---|---|
| 1 | thedotmack/claude-mem | 97,099 | SQLite | PostgreSQL | PostgreSQL |
| 2 | nocodb/nocodb | 65,206 | PostgreSQL+SQLite | ClickHouse+MySQL | — |
| 3 | prisma/orm | 47,701 | PostgreSQL+SQLite | MySQL | SQL Server+MySQL+MariaDB |
| 4 | pingcap/tidb | 40,630 | TiDB | MySQL | MySQL |
| 5 | YunaiV/ruoyi-vue-pro | 39,562 | MySQL+PostgreSQL+Oracle+SQL Server+MariaDB+TiDB+Dameng | GBase+openGauss | — |
| 6 | directus/directus | 38,094 | PostgreSQL+MySQL+SQLite+MariaDB | Oracle+SQL Server | SQL Server+Oracle |
| 7 | Dokploy/dokploy | 37,686 | PostgreSQL+MySQL+MariaDB | SQLite | — |
| 8 | hasura/graphql-engine | 32,129 | PostgreSQL+SQL Server+ClickHouse | SQLite | — |
| 9 | Infisical/infisical | 29,634 | PostgreSQL+MySQL | ClickHouse | ClickHouse |
| 10 | OtterMind/Chat2DB | 28,301 | PostgreSQL+MySQL+Oracle+SQLite+SQL Server+ClickHouse+MariaDB+TiDB | GBase+GaussDB+OceanBase+openGauss | GBase+GaussDB+OceanBase+openGauss |
| 11 | neondatabase/neon | 23,175 | PostgreSQL | ClickHouse | — |
| 12 | chartdb/chartdb | 22,986 | PostgreSQL+MySQL+SQL Server+MariaDB+SQLite+ClickHouse | Oracle | Oracle |
| 13 | teableio/teable | 21,863 | PostgreSQL | SQLite | SQLite |
| 14 | vitessio/vitess | 21,370 | MySQL | ClickHouse | — |
| 15 | gravitational/teleport | 20,966 | PostgreSQL+MySQL | ClickHouse | — |
| 16 | apache/shardingsphere | 20,804 | PostgreSQL+MySQL+Oracle+SQL Server+MariaDB | ClickHouse+openGauss | openGauss+ClickHouse |
| 17 | YunaiV/yudao-cloud | 19,593 | PostgreSQL+MySQL+Oracle+SQL Server+MariaDB+TiDB+OceanBase+PolarDB+Dameng+openGauss+GaussDB | GBase | — |
| 18 | windmill-labs/windmill | 18,116 | PostgreSQL | MySQL+SQLite | — |
| 19 | Canner/WrenAI | 17,808 | PostgreSQL+ClickHouse | MySQL+Oracle+SQL Server | MySQL+Oracle+SQL Server |
| 20 | transact-rs/sqlx | 17,549 | PostgreSQL+MySQL+SQLite+MariaDB | SQL Server | — |
| 21 | electric-sql/pglite | 16,130 | PostgreSQL | SQLite | — |
| 22 | github/gh-ost | 13,590 | MySQL | SQLite | SQLite |
| 23 | ccfos/nightingale | 13,417 | PostgreSQL+ClickHouse | MySQL | — |
| 24 | debezium/debezium | 13,190 | PostgreSQL+Oracle | MariaDB+MySQL+SQL Server | MariaDB+MySQL+SQL Server |
| 25 | graphile/crystal | 12,933 | PostgreSQL | SQLite | — |
| 26 | encoredev/encore | 12,413 | PostgreSQL | MySQL+SQLite | — |
| 27 | pressly/goose | 11,546 | PostgreSQL+MySQL+SQLite+SQL Server+ClickHouse+MariaDB | TiDB | TiDB |
| 28 | TencentCloud/Octop | 11,366 | PostgreSQL+SQLite | TDSQL | — |
| 29 | dtm-labs/dtm | 10,921 | PostgreSQL+MySQL+MariaDB+TDSQL | SQL Server | — |
| 30 | frappe/frappe | 10,886 | MariaDB | MySQL | PostgreSQL |
| 31 | oceanbase/oceanbase | 10,299 | OceanBase | MySQL | MySQL |
| 32 | nopSolutions/nopCommerce | 10,158 | PostgreSQL+MySQL | SQL Server | SQL Server |
| 33 | SeaQL/sea-orm | 9,914 | PostgreSQL+SQLite+SQL Server | MariaDB+MySQL | MariaDB+MySQL |
| 34 | risingwavelabs/risingwave | 9,360 | PostgreSQL+MySQL | Oracle+SQLite | — |
| 35 | nhost/nhost | 9,347 | PostgreSQL | SQLite | — |
| 36 | saulpw/visidata | 9,319 | SQLite | PostgreSQL | — |
| 37 | XiaoMi/soar | 8,759 | MySQL | TiDB | TiDB |
| 38 | MariaDB/server | 8,324 | MariaDB | MySQL | MySQL |
| 39 | warp-tech/warpgate | 8,015 | PostgreSQL+MySQL+SQLite | MariaDB | — |
| 40 | microsoft/azuredatastudio | 7,680 | PostgreSQL+MySQL+SQL Server | SQLite | — |
| 41 | samuelclay/NewsBlur | 7,642 | PostgreSQL | MySQL | MySQL |
| 42 | apache/hertzbeat | 7,415 | PostgreSQL+MySQL | ClickHouse+Dameng+Oracle+SQL Server | — |
| 43 | authzed/spicedb | 7,119 | PostgreSQL+MySQL | ClickHouse | — |
| 44 | Gentleman-Programming/engram | 7,062 | SQLite | PostgreSQL | PostgreSQL |
| 45 | dimitri/pgloader | 6,543 | PostgreSQL+MySQL+SQLite+SQL Server | MariaDB | — |
| 46 | apache/hive | 6,028 | PostgreSQL+MySQL+Oracle+SQL Server | OceanBase | — |
| 47 | openark/orchestrator | 5,773 | MySQL | SQLite | SQLite |
| 48 | riverqueue/river | 5,747 | PostgreSQL | SQLite | SQLite |
| 49 | dbeaver/cloudbeaver | 5,182 | PostgreSQL+MySQL+ClickHouse+MariaDB | Oracle+SQL Server+SQLite | Oracle+SQL Server+SQLite |
| 50 | jitsucom/jitsu | 5,101 | PostgreSQL+ClickHouse | MySQL | MySQL |

… 其余 1,660 仓见台账 JSON

## 清单三 · 双源 strong（dbs 空、topic∩指纹同库互证） —— 1,343 仓

| # | 仓 | star | topic∩指纹互证 |
|---|---|---|---|
| 1 | netdata/netdata | 80,810 | MySQL+PostgreSQL |
| 2 | grafana/grafana | 77,112 | MySQL+PostgreSQL |
| 3 | coollabsio/coolify | 62,659 | PostgreSQL |
| 4 | makeplane/plane | 60,450 | PostgreSQL |
| 5 | metabase/metabase | 49,557 | MySQL+PostgreSQL |
| 6 | payloadcms/payload | 45,113 | PostgreSQL |
| 7 | supermemoryai/supermemory | 31,122 | PostgreSQL |
| 8 | tursodatabase/turso | 24,655 | SQLite |
| 9 | dolthub/dolt | 24,582 | MariaDB+MySQL |
| 10 | sqlc-dev/sqlc | 18,347 | MySQL+PostgreSQL+SQLite |
| 11 | zhisheng17/flink-learning | 15,097 | MySQL |
| 12 | blinkospace/blinko | 11,062 | PostgreSQL |
| 13 | zfile-dev/zfile | 10,853 | MySQL |
| 14 | getlago/lago | 10,661 | ClickHouse |
| 15 | doctrine/dbal | 9,702 | MariaDB+MySQL+PostgreSQL+SQL Server |
| 16 | activeloopai/deeplake | 9,248 | PostgreSQL |
| 17 | benawad/dogehouse | 9,017 | PostgreSQL |
| 18 | growthbook/growthbook | 8,478 | ClickHouse |
| 19 | jOOQ/jOOQ | 6,794 | PostgreSQL |
| 20 | TableProApp/TablePro | 6,214 | MySQL+PostgreSQL+SQL Server |
| 21 | liquibase/liquibase | 5,621 | MariaDB+MySQL+Oracle+SQL Server |
| 22 | lukevella/rallly | 5,293 | PostgreSQL |
| 23 | malisper/pgrust | 5,233 | PostgreSQL |
| 24 | backup/backup | 4,856 | MySQL+PostgreSQL |
| 25 | linhaojun857/aurora | 4,663 | MySQL |
| 26 | supabase/supabase-js | 4,576 | PostgreSQL |
| 27 | crate/crate | 4,443 | PostgreSQL |
| 28 | flippercloud/flipper | 3,972 | MySQL+PostgreSQL |
| 29 | rbmonster/learning-note | 3,815 | MySQL |
| 30 | mergestat/mergestat-lite | 3,519 | SQLite |
| 31 | fluentmigrator/fluentmigrator | 3,517 | MySQL+Oracle+PostgreSQL |
| 32 | sqlkata/querybuilder | 3,384 | MySQL |
| 33 | serverpod/serverpod | 3,303 | PostgreSQL |
| 34 | oceanbase/seekdb | 3,103 | MySQL+OceanBase |
| 35 | datafold/data-diff | 2,992 | MySQL+Oracle+PostgreSQL |
| 36 | acepanel/panel | 2,980 | MySQL+PostgreSQL |
| 37 | codigoencasa/builderbot | 2,971 | MySQL |
| 38 | chdb-io/chdb | 2,914 | ClickHouse |
| 39 | Meituan-Dianping/Zebra | 2,763 | MySQL |
| 40 | TIGERB/easy-tips | 2,710 | MySQL |
| 41 | geekgeekrun/geekgeekrun | 2,690 | SQLite |
| 42 | mybatis-flex/mybatis-flex | 2,671 | MySQL |
| 43 | dolthub/go-mysql-server | 2,658 | MySQL |
| 44 | gridaco/grida | 2,656 | PostgreSQL |
| 45 | supabase/supabase-py | 2,597 | PostgreSQL |
| 46 | vietnam-devs/coolstore-microservices | 2,531 | PostgreSQL |
| 47 | oguimbal/pg-mem | 2,368 | PostgreSQL |
| 48 | azimuttapp/azimutt | 2,190 | MariaDB+PostgreSQL |
| 49 | zio/zio-quill | 2,166 | MySQL+PostgreSQL |
| 50 | motor-admin/motor-admin | 2,165 | MySQL+PostgreSQL |

… 其余 1,293 仓见台账 JSON

