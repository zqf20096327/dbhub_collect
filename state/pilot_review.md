# T3a 试点复核表（人工逐仓复核；LLM 不预填人工栏）

生成 2026-11-01T06:09:47Z · 引擎 0.3.0 · 命中口径：README 行号提名差 / 全空工具 / 提名被否决 / draft 存档

> 复核用法：逐行看「现判 → 建议（引擎 quorum）」，在人工栏填 归/不归+库位；T3b 汇总命中率——**≥90% 才准进第 4 批，<90% 调词表回 T1 重来**。

## ① 点名缺口 50（README 行号提名 ∉ 现判 dbs） —— 50 仓

| # | 仓 | star | 现判 dbs | 提名/证据摘要 | 引擎建议 | 人工栏 |
|---|---|---|---|---|---|---|
| 1 | Snailclimb/JavaGuide | 159,351 | ∅ | MySQL | MySQL | 　 |
| 2 | macrozheng/mall | 84,990 | MySQL | Oracle | MySQL | 　 |
| 3 | netdata/netdata | 81,226 | ∅ | PostgreSQL | MySQL+PostgreSQL | 　 |
| 4 | prisma/orm | 47,664 | PostgreSQL | MySQL+SQLite | PostgreSQL+SQL Server+MySQL+MariaDB+SQLite | 　 |
| 5 | LeCoupa/awesome-cheatsheets | 46,600 | ∅ | MySQL | no_evidence | 　 |
| 6 | pingcap/tidb | 40,690 | TiDB | MySQL | TiDB+MySQL | 　 |
| 7 | The-Vibe-Company/quivr | 39,617 | ∅ | PostgreSQL | PostgreSQL | 　 |
| 8 | 0voice/interview_internal_reference | 37,262 | ∅ | MySQL | MySQL | 　 |
| 9 | AobingJava/JavaFamily | 36,980 | ∅ | MySQL | MySQL | 　 |
| 10 | cockroachdb/cockroach | 32,596 | ∅ | PostgreSQL | PostgreSQL | 　 |
| 11 | forthespada/CS-Books | 27,787 | ∅ | ClickHouse+MySQL+SQL Server+SQLite | no_evidence | 　 |
| 12 | taosdata/TDengine | 25,179 | ∅ | SQLite | below_quorum | 　 |
| 13 | tursodatabase/turso | 25,095 | ∅ | PostgreSQL+SQLite | SQLite | 　 |
| 14 | dolthub/dolt | 24,775 | ∅ | MySQL+PostgreSQL+SQL Server | MySQL+MariaDB | 　 |
| 15 | Vonng/ddia | 23,885 | ∅ | PostgreSQL | no_evidence | 　 |
| 16 | typicode/lowdb | 22,582 | ∅ | PostgreSQL | no_evidence | 　 |
| 17 | amark/gun | 19,159 | ∅ | SQLite | no_evidence | 　 |
| 18 | windmill-labs/windmill | 18,327 | PostgreSQL | MySQL | PostgreSQL | 　 |
| 19 | itwanger/toBeBetterJavaer | 17,802 | ∅ | MySQL | MySQL | 　 |
| 20 | xerj-org/xerj | 17,698 | ∅ | SQLite | below_quorum | 　 |
| 21 | transact-rs/sqlx | 17,612 | PostgreSQL+MySQL+SQLite+MariaDB | SQL Server | PostgreSQL+MySQL+SQLite+MariaDB | 　 |
| 22 | questdb/questdb | 17,486 | ∅ | ClickHouse+PostgreSQL | PostgreSQL | 　 |
| 23 | tursodatabase/libsql | 17,302 | SQLite | MySQL+PostgreSQL | SQLite | 　 |
| 24 | tikv/tikv | 16,932 | ∅ | MySQL+TiDB | pending_evidence | 　 |
| 25 | ty4z2008/Qix | 15,234 | ∅ | MySQL+PostgreSQL | PostgreSQL | 　 |
| 26 | zhisheng17/flink-learning | 15,100 | ∅ | MySQL | MySQL+ClickHouse | 　 |
| 27 | oxnr/awesome-bigdata | 14,711 | ∅ | ClickHouse+MariaDB+MySQL+Oracle+PostgreSQL+SQL Server+SQLite+TiDB | no_evidence | 　 |
| 28 | boltdb/bolt | 14,630 | ∅ | MySQL+PostgreSQL+SQLite | no_evidence | 　 |
| 29 | sogou/workflow | 14,426 | MySQL | MariaDB+TiDB | MySQL | 　 |
| 30 | dbcli/pgcli | 13,427 | PostgreSQL | MySQL | PostgreSQL | 　 |
| 31 | ccfos/nightingale | 13,417 | PostgreSQL+ClickHouse | MySQL | ClickHouse | 　 |
| 32 | macrozheng/mall-swarm | 13,191 | MySQL | Oracle | MySQL | 　 |
| 33 | mysql/mysql-server | 12,491 | MySQL | Oracle | pending_evidence | 　 |
| 34 | StarRocks/starrocks | 12,221 | ∅ | MySQL | MariaDB+MySQL | 　 |
| 35 | dhamaniasad/awesome-postgres | 12,128 | PostgreSQL | ClickHouse+MariaDB+MySQL+Oracle+SQL Server | PostgreSQL | 　 |
| 36 | manticoresoftware/manticoresearch | 12,073 | PostgreSQL+MySQL | ClickHouse+Oracle | MySQL | 　 |
| 37 | dbcli/mycli | 11,987 | MySQL | MariaDB+PostgreSQL+TiDB | MySQL | 　 |
| 38 | realm/realm-java | 11,450 | ∅ | Oracle+SQLite | no_evidence | 　 |
| 39 | pingcap/awesome-database-learning | 11,237 | ∅ | Oracle+PostgreSQL+SQLite+TiDB | below_quorum | 　 |
| 40 | pingcap/talent-plan | 11,033 | ∅ | TiDB | below_quorum | 　 |
| 41 | yugabyte/yugabyte-db | 10,640 | ∅ | PostgreSQL | PostgreSQL | 　 |
| 42 | oceanbase/oceanbase | 10,358 | OceanBase | MySQL | MySQL+OceanBase | 　 |
| 43 | bxcodec/go-clean-arch | 10,181 | MySQL | Oracle+SQL Server | MySQL | 　 |
| 44 | cloudnative-pg/cloudnative-pg | 9,515 | PostgreSQL | MariaDB | PostgreSQL | 　 |
| 45 | litedb-org/LiteDB | 9,491 | ∅ | SQLite | no_evidence | 　 |
| 46 | spacejam/sled | 9,103 | ∅ | SQLite | no_evidence | 　 |
| 47 | codenotary/immudb | 9,047 | ∅ | PostgreSQL | below_quorum | 　 |
| 48 | deeplethe/utopia | 8,641 | PostgreSQL+MySQL+ClickHouse | SQLite | PostgreSQL | 　 |
| 49 | digoal/blog | 8,604 | ∅ | MySQL+OceanBase+Oracle+PolarDB+PostgreSQL+TiDB | PostgreSQL+MySQL+Oracle | 　 |
| 50 | MariaDB/server | 8,487 | MariaDB | MySQL+Oracle | MariaDB+MySQL | 　 |

## ② 全空工具 30（dbs 空 · eco=tool · 会诊组） —— 30 仓

| # | 仓 | star | 现判 dbs | 提名/证据摘要 | 引擎建议 | 人工栏 |
|---|---|---|---|---|---|---|
| 1 | grafana/grafana | 77,584 | ∅ | topic:MySQL@topic:mysql; dep:MySQL@go.mod | MySQL+PostgreSQL | 　 |
| 2 | coollabsio/coolify | 65,322 | ∅ | image:PostgreSQL@docker-compose.dev-multi.yml; image:PostgreSQL@docker-compose.windows.yml | PostgreSQL+MariaDB+MySQL | 　 |
| 3 | metabase/metabase | 50,025 | ∅ | tree:ClickHouse@modules/drivers/clickhouse/L; tree:ClickHouse@modules/drivers/clickhouse/R | ClickHouse+PostgreSQL+MySQL | 　 |
| 4 | DeusData/codebase-memory-mcp | 47,856 | ∅ | topic:SQLite@topic:sqlite | SQLite | 　 |
| 5 | drawdb-io/drawdb | 40,195 | ∅ | topic:MariaDB@topic:mariadb; topic:Oracle@topic:oracle-database | MariaDB+Oracle+PostgreSQL+SQL Server+SQLite | 　 |
| 6 | sqlmapproject/sqlmap | 38,820 | ∅ | — | no_evidence | 　 |
| 7 | supermemoryai/supermemory | 31,471 | ∅ | topic:PostgreSQL@topic:postgres; dep:PostgreSQL@package.json | PostgreSQL | 　 |
| 8 | airbytehq/airbyte | 22,291 | ∅ | topic:MySQL@topic:mysql; topic:PostgreSQL@topic:postgresql | MySQL+PostgreSQL+SQL Server | 　 |
| 9 | eosphoros-ai/DB-GPT | 20,223 | ∅ | image:MySQL@docker-compose.yml; dep:MySQL@packages/dbgpt-ext/pyproject | MySQL | 　 |
| 10 | sqlc-dev/sqlc | 18,427 | ∅ | image:MySQL@docker-compose.yml; topic:MySQL@topic:mysql | MySQL+PostgreSQL+SQL Server+SQLite+ClickHouse | 　 |
| 11 | baomidou/mybatis-plus | 17,479 | ∅ | topic:MySQL@topic:mysql; topic:PostgreSQL@topic:postgresql | MySQL+PostgreSQL | 　 |
| 12 | realm/realm-swift | 16,599 | ∅ | — | no_evidence | 　 |
| 13 | doctrine/dbal | 9,701 | ∅ | topic:MariaDB@topic:mariadb; ci:MariaDB@.github/workflows/phpunit-ma | MariaDB+MySQL+PostgreSQL+SQL Server+Oracle+SQLite | 　 |
| 14 | activeloopai/deeplake | 9,263 | ∅ | topic:PostgreSQL@topic:postgres; dep:PostgreSQL@postgres/tests/py_tests/requ | PostgreSQL | 　 |
| 15 | twitter/finagle | 8,869 | ∅ | topic:MySQL@topic:mysql | MySQL | 　 |
| 16 | amitshekhariitbhu/Android-Debug-Database | 8,701 | ∅ | topic:SQLite@topic:sqlite | SQLite | 　 |
| 17 | HariSekhon/DevOps-Bash-tools | 8,437 | ∅ | topic:MySQL@topic:mysql; topic:PostgreSQL@topic:postgresql | MySQL+PostgreSQL | 　 |
| 18 | sqlcipher/sqlcipher | 7,318 | ∅ | — | no_evidence | 　 |
| 19 | jOOQ/jOOQ | 6,802 | ∅ | topic:PostgreSQL@topic:postgresql; dep:PostgreSQL@pom.xml | PostgreSQL+MySQL+Oracle+SQL Server | 　 |
| 20 | nraiden/cofounder | 6,649 | ∅ | topic:PostgreSQL@topic:postgresql | PostgreSQL | 　 |
| 21 | DATA-DOG/go-sqlmock | 6,571 | ∅ | — | no_evidence | 　 |
| 22 | TableProApp/TablePro | 6,343 | ∅ | tree:MySQL@.claude/rules/mysql-driver.m; topic:MySQL@topic:mysql | MySQL+PostgreSQL+SQL Server+SQLite | 　 |
| 23 | realm/realm-js | 6,002 | ∅ | — | no_evidence | 　 |
| 24 | liquibase/liquibase | 5,638 | ∅ | topic:MariaDB@topic:mariadb; dep:MariaDB@liquibase-extension-testing/ | MariaDB+SQL Server+MySQL+Oracle+PostgreSQL | 　 |
| 25 | liam-hq/liam | 5,156 | ∅ | topic:PostgreSQL@topic:postgresql | PostgreSQL | 　 |
| 26 | pudo/dataset | 4,866 | ∅ | ci:MySQL@.github/workflows/build.yml; ci:PostgreSQL@.github/workflows/build.yml | below_quorum | 　 |
| 27 | backup/backup | 4,859 | ∅ | topic:MySQL@topic:mysql; dep:MySQL@vagrant/utils/Gemfile | MySQL+PostgreSQL | 　 |
| 28 | sylar-yin/sylar | 4,722 | ∅ | topic:SQLite@topic:sqlite3 | SQLite | 　 |
| 29 | objectbox/objectbox-java | 4,631 | ∅ | topic:SQLite@topic:sqlite | SQLite | 　 |
| 30 | supabase/supabase-js | 4,605 | ∅ | topic:PostgreSQL@topic:postgres; topic:PostgreSQL@topic:postgresql | PostgreSQL | 　 |

## ③ 误杀候选 20（提名过 · AI 否决过 · sqlkata/postgis 级） —— 20 仓

| # | 仓 | star | 现判 dbs | 提名/证据摘要 | 引擎建议 | 人工栏 |
|---|---|---|---|---|---|---|
| 1 | smartcontractkit/chainlink | 8,252 | PostgreSQL | Oracle | PostgreSQL+Oracle | 　 |
| 2 | linkedin/school-of-sre | 8,152 | ∅ | MySQL | MySQL | 　 |
| 3 | WiseLibs/better-sqlite3 | 7,538 | SQLite | PostgreSQL | SQLite | 　 |
| 4 | doocs/technical-books | 7,024 | ∅ | MySQL | no_evidence | 　 |
| 5 | akopytov/sysbench | 6,814 | PostgreSQL+MySQL | MariaDB | MySQL+PostgreSQL | 　 |
| 6 | alibaba/AliSQL | 5,992 | ∅ | MySQL | pending_evidence | 　 |
| 7 | pgsty/pigsty | 5,877 | PostgreSQL+PolarDB | MySQL+Oracle+SQL Server | PostgreSQL | 　 |
| 8 | go-pg/pg | 5,777 | PostgreSQL | ClickHouse+MariaDB+MySQL+SQLite | PostgreSQL | 　 |
| 9 | rfyiamcool/share_ppt | 5,750 | ∅ | MySQL | MySQL | 　 |
| 10 | malisper/pgrust | 5,693 | ∅ | ClickHouse+PostgreSQL | PostgreSQL | 　 |
| 11 | dunwu/db-tutorial | 5,388 | PostgreSQL+MySQL+SQLite | ClickHouse+MariaDB+Oracle | MySQL | 　 |
| 12 | mgramin/awesome-db-tools | 5,352 | ∅ | ClickHouse+MariaDB+MySQL+Oracle+PostgreSQL+SQL Server+SQLite | no_evidence | 　 |
| 13 | TabularisDB/tabularis | 5,339 | PostgreSQL+MySQL+SQLite+MariaDB+Oracle+SQL Server+ClickHouse+Dameng | TiDB | PostgreSQL+MySQL+MariaDB+SQLite | 　 |
| 14 | cube2222/octosql | 5,269 | PostgreSQL+MySQL | SQLite | PostgreSQL+MySQL | 　 |
| 15 | oracle/opengrok | 5,025 | ∅ | Oracle | below_quorum | 　 |
| 16 | orientechnologies/orientdb | 4,996 | ∅ | Oracle | no_evidence | 　 |
| 17 | royeo/awesome-programming-books | 4,917 | ∅ | MySQL | MySQL | 　 |
| 18 | jaywcjlove/mysql-tutorial | 4,802 | ∅ | MariaDB+MySQL | MySQL | 　 |
| 19 | mouredev/python-web | 4,801 | ∅ | PostgreSQL | PostgreSQL | 　 |
| 20 | ydb-platform/ydb | 4,782 | ∅ | PostgreSQL | pending_evidence | 　 |

## ④ 旧判定器 draft 存档（≤122，冻结名单） —— 119 仓

| # | 仓 | star | 现判 dbs | 提名/证据摘要 | 引擎建议 | 人工栏 |
|---|---|---|---|---|---|---|
| 1 | sinaptik-ai/pandas-ai | 23,919 | ∅ | tree:Oracle@extensions/ee/connectors/ora; tree:Oracle@extensions/ee/connectors/ora | Oracle+PostgreSQL | 　 |
| 2 | OmniDB/OmniDB | 3,282 | ∅ | dep:MySQL@requirements.txt; dep:Oracle@requirements.txt | below_quorum | 　 |
| 3 | feldera/feldera | 2,148 | ∅ | dep:PostgreSQL@crates/connectors/Cargo.toml | below_quorum | 　 |
| 4 | schemacrawler/SchemaCrawler | 1,841 | ∅ | dep:PostgreSQL@schemacrawler-dbconnectors/p; dep:PostgreSQL@schemacrawler-distrib/pom.xm | PostgreSQL+MariaDB | 　 |
| 5 | dotnet/ef6 | 1,448 | ∅ | dep:SQL Server@src/EntityFramework/EntityFr; dep:SQL Server@src/EntityFramework/EntityFr | SQL Server | 　 |
| 6 | schotime/NPoco | 879 | ∅ | dep:SQL Server@src/NPoco.SqlServer.SystemDa; dep:SQL Server@src/NPoco.SqlServer/NPoco.Sq | SQL Server | 　 |
| 7 | kubedb/cli | 732 | ∅ | tree:MySQL@vendor/github.com/go-sql-dri; tree:MySQL@vendor/github.com/go-sql-dri | MySQL | 　 |
| 8 | qustavo/sqlhooks | 664 | ∅ | dep:MySQL@go.mod; ci:MySQL@.github/workflows/test.yml | below_quorum | 　 |
| 9 | apache/arrow-adbc | 636 | ∅ | image:PostgreSQL@compose.yaml; image:SQL Server@compose.yaml | PostgreSQL+SQL Server | 　 |
| 10 | aiidateam/aiida-core | 604 | ∅ | dep:PostgreSQL@pyproject.toml; ci:PostgreSQL@.github/workflows/benchmark. | PostgreSQL | 　 |
| 11 | hanami/model | 447 | ∅ | tree:MySQL@lib/hanami/model/migrator/my; dep:MySQL@Gemfile | MySQL+PostgreSQL+SQLite | 　 |
| 12 | top-think/think-orm | 437 | ∅ | tree:PostgreSQL@src/db/connector/Pgsql.php; tree:PostgreSQL@src/db/connector/pgsql.sql | PostgreSQL+MySQL+Oracle+SQLite | 　 |
| 13 | oltpbenchmark/oltpbench | 415 | ∅ | dep:Oracle@pom.xml; dep:PostgreSQL@pom.xml | below_quorum | 　 |
| 14 | apache/cayenne | 347 | ∅ | dep:MariaDB@pom.xml; dep:MySQL@pom.xml | below_quorum | 　 |
| 15 | r2dbc/r2dbc-client | 342 | ∅ | dep:MySQL@pom.xml; dep:PostgreSQL@pom.xml | below_quorum | 　 |
| 16 | hellofresh/klepto | 301 | ∅ | image:MySQL@docker-compose.yml; dep:MySQL@go.mod | MySQL+PostgreSQL | 　 |
| 17 | dao-xyz/peerbit | 278 | ∅ | dep:SQLite@packages/clients/peerbit/pac; dep:SQLite@packages/log/package.json | SQLite | 　 |
| 18 | fuma-nama/fumadb | 259 | ∅ | image:MySQL@docker-compose.yml; dep:MySQL@packages/fumadb/package.json | MySQL+PostgreSQL+SQL Server | 　 |
| 19 | Log2n-io/Typhon | 253 | ∅ | — | no_evidence | 　 |
| 20 | yokyak/react-agent | 237 | ∅ | dep:PostgreSQL@packages/package.json; dep:PostgreSQL@packages/react-agent-server/ | PostgreSQL | 　 |
| 21 | garden-co/jazz | 221 | ∅ | dep:SQLite@crates/jazz-native-relay/Car | below_quorum | 　 |
| 22 | ManyDesigns/Portofino | 186 | ∅ | dep:PostgreSQL@demo-tt/pom.xml; image:PostgreSQL@demo-tt/src/main/docker/data | below_quorum | 　 |
| 23 | polypheny/Polypheny-DB | 176 | ∅ | tree:MySQL@plugins/mysql-adapter/build.; tree:MySQL@plugins/mysql-adapter/gradle | MySQL | 　 |
| 24 | golobby/orm | 162 | ∅ | dep:MySQL@go.mod; dep:MySQL@benchmark/go.mod | below_quorum | 　 |
| 25 | iWinston/typeorm-plus | 155 | ∅ | tree:MySQL@src/driver/mysql/MysqlConnec; tree:MySQL@src/driver/mysql/MysqlConnec | MySQL+Oracle+SQL Server+MariaDB | 　 |
| 26 | mutable-org/mutable | 118 | ∅ | tree:PostgreSQL@benchmark/database_connector; tree:PostgreSQL@benchmark/database_connector | below_quorum | 　 |
| 27 | MatteoGuadrini/pyreports | 114 | ∅ | dep:MySQL@docs/requirements.txt; dep:MySQL@pyproject.toml | MySQL+PostgreSQL | 　 |
| 28 | FROWNINGdev/django-orm-lens | 96 | ∅ | — | pending_evidence | 　 |
| 29 | jaxio/celerio | 83 | ∅ | dep:MySQL@celerio-engine/pom.xml | below_quorum | 　 |
| 30 | FCO/Red | 77 | PostgreSQL+MySQL+SQLite | tree:SQLite@docs/api/Red/Driver/SQLite/S; tree:SQLite@lib/Red/Driver/SQLite.pm6 | SQLite | 　 |
| 31 | kubedb/apimachinery | 71 | ∅ | tree:MySQL@vendor/github.com/go-sql-dri; tree:MySQL@vendor/github.com/go-sql-dri | MySQL | 　 |
| 32 | yeecode/DynamicDataSource | 67 | ∅ | dep:MySQL@pom.xml; dep:MySQL@demo/pom.xml | below_quorum | 　 |
| 33 | mtgjson/mtgsqlive | 66 | ∅ | dep:MySQL@requirements.txt | below_quorum | 　 |
| 34 | cycle/active-record | 65 | ∅ | image:MySQL@docker-compose.yaml; tree:MySQL@tests/Acceptance/Driver/MySQ | MySQL+PostgreSQL+SQL Server | 　 |
| 35 | omnilib/aql | 61 | ∅ | — | no_evidence | 　 |
| 36 | hidal-go/hidalgo | 60 | ∅ | dep:MySQL@go.mod; dep:PostgreSQL@go.mod | below_quorum | 　 |
| 37 | HazelnutParadise/insyra | 58 | ∅ | dep:PostgreSQL@go.mod; dep:MySQL@go.mod | below_quorum | 　 |
| 38 | schic/DQCS | 49 | ∅ | dep:Oracle@pom.xml; dep:PostgreSQL@pom.xml | below_quorum | 　 |
| 39 | Magenic/MAQS | 42 | ∅ | dep:PostgreSQL@Framework/BaseDatabaseTest/B; dep:SQL Server@Framework/BaseDatabaseTest/B | below_quorum | 　 |
| 40 | jhannes/fluent-jdbc | 37 | ∅ | image:Oracle@docker-compose.yaml; dep:Oracle@pom.xml | Oracle+PostgreSQL+SQL Server | 　 |
| 41 | apllodb/apllodb | 35 | ∅ | dep:SQLite@apllodb-immutable-schema-eng | below_quorum | 　 |
| 42 | keeps/dbptk-ui | 34 | ∅ | dep:MySQL@pom.xml; dep:PostgreSQL@pom.xml | below_quorum | 　 |
| 43 | jegelstaff/formulize | 32 | ∅ | image:MariaDB@docker-compose.yaml | MariaDB | 　 |
| 44 | microknights/Log4NetAdoNetAppender | 29 | ∅ | dep:SQL Server@src/MicroKnights.Log4NetAdoN; dep:SQL Server@src/MicroKnights.Log4NetAdoN | SQL Server | 　 |
| 45 | phalcon/migrations | 28 | ∅ | tree:MySQL@src/Db/Adapter/Mysql.php; image:MySQL@docker-compose.yml | MySQL+PostgreSQL+SQLite | 　 |
| 46 | The404Hacking/sqlmap | 21 | ∅ | — | no_evidence | 　 |
| 47 | adambanaszkiewicz/query-builder | 21 | ∅ | tree:MySQL@src/QueryBuilder/ConnectionA; tree:PostgreSQL@src/QueryBuilder/ConnectionA | MySQL+PostgreSQL+SQL Server+SQLite | 　 |
| 48 | dbunit/dbunit-extension | 21 | ∅ | image:SQL Server@dbunit-docker/sqlserver/Dock; dep:SQL Server@pom.xml | SQL Server | 　 |
| 49 | morph-kgc/3xtudio | 21 | ∅ | dep:MySQL@requirements.txt; dep:Oracle@requirements.txt | below_quorum | 　 |
| 50 | toddbirchard/pythonmyadmin | 21 | ∅ | dep:MySQL@pyproject.toml; dep:MySQL@requirements.txt | MySQL | 　 |
| 51 | CognizantOpenSource/maqs-dotnet | 19 | ∅ | dep:PostgreSQL@Framework/BaseDatabaseTest/B; dep:SQL Server@Framework/BaseDatabaseTest/B | below_quorum | 　 |
| 52 | YaoApp/xun | 19 | ∅ | dep:MySQL@go.mod; dep:PostgreSQL@go.mod | below_quorum | 　 |
| 53 | flyway/flyway-community-db-support | 19 | ∅ | dep:PostgreSQL@flyway-database-dsql/pom.xml; dep:PostgreSQL@flyway-database-questdb/pom. | PostgreSQL | 　 |
| 54 | radcortez/flyway-junit5-extensions | 19 | ∅ | dep:PostgreSQL@extension/pom.xml; dep:PostgreSQL@examples/quarkus/pom.xml | below_quorum | 　 |
| 55 | hashicorp/go-dbw | 18 | ∅ | image:PostgreSQL@docker-compose.yml; dep:PostgreSQL@go.mod | PostgreSQL | 　 |
| 56 | FrancoLiberali/cql | 17 | ∅ | image:SQL Server@docker/sqlserver/Dockerfile; dep:SQL Server@go.mod | SQL Server | 　 |
| 57 | SleekwareDB/sleekwaredb | 17 | ∅ | tree:MySQL@backend/system/database/driv; tree:MySQL@backend/system/database/driv | MySQL+SQL Server | 　 |
| 58 | apache/metamodel-membrane | 16 | ∅ | image:PostgreSQL@docker-compose.yml; dep:PostgreSQL@core/pom.xml | PostgreSQL | 　 |
| 59 | htmfilho/digger | 16 | ∅ | dep:PostgreSQL@java/pom.xml; dep:SQL Server@java/pom.xml | below_quorum | 　 |
| 60 | bastienboutonnet/sheetwork | 15 | ∅ | tree:PostgreSQL@sheetwork/core/adapters/post; tree:PostgreSQL@sheetwork/core/adapters/post | PostgreSQL | 　 |
| 61 | Zenithar/go-pkg | 12 | ∅ | tree:PostgreSQL@db/adapter/postgresql/connec; tree:PostgreSQL@db/adapter/postgresql/defaul | PostgreSQL | 　 |
| 62 | kamichidu/goen | 12 | ∅ | tree:PostgreSQL@dialect/postgres/dialect.go; dep:PostgreSQL@go.mod | PostgreSQL+SQLite | 　 |
| 63 | jproggy/snippetory | 11 | ∅ | dep:MySQL@snippetory-sql/pom.xml; dep:SQLite@snippetory-sql/pom.xml | below_quorum | 　 |
| 64 | soul-soft/Soul.SqlBatis | 10 | ∅ | tree:MySQL@tools/MySql/MySqlConnector.d; tree:MySQL@tools/MySql/References/MySql | MySQL+PostgreSQL | 　 |
| 65 | BjoernKW/Schematic | 0 | ∅ | — | pending_evidence | 　 |
| 66 | CERT-Polska/mquery | 0 | ∅ | — | pending_evidence | 　 |
| 67 | FrigadeHQ/remote-storage | 0 | ∅ | — | pending_evidence | 　 |
| 68 | JaCraig/SQLHelper | 0 | ∅ | — | pending_evidence | 　 |
| 69 | LuanMaik/nestjs-typeorm-transaction-unitOfWork-AsyncLocalStorage | 0 | ∅ | — | pending_evidence | 　 |
| 70 | Matific/broken-down-models | 0 | ∅ | — | pending_evidence | 　 |
| 71 | Open-NET-Libraries/Open.Database.Extensions | 0 | ∅ | — | pending_evidence | 　 |
| 72 | RicardoBrazao/systematize | 0 | ∅ | — | pending_evidence | 　 |
| 73 | SatoriCyber/universal-data-permissions-scanner | 0 | ∅ | — | pending_evidence | 　 |
| 74 | SeldonIO/goven | 0 | ∅ | — | pending_evidence | 　 |
| 75 | WailanTirajoh/dbviewer | 0 | ∅ | — | pending_evidence | 　 |
| 76 | Wsiegenthaler/sequelize-embed | 0 | ∅ | — | pending_evidence | 　 |
| 77 | abcsys/libem | 0 | ∅ | — | pending_evidence | 　 |
| 78 | amilajack/compat-db | 0 | ∅ | — | pending_evidence | 　 |
| 79 | andrehertwig/admintool | 0 | ∅ | — | pending_evidence | 　 |
| 80 | apache/cocoon | 0 | ∅ | — | pending_evidence | 　 |
| 81 | ashkrit/corejava | 0 | ∅ | — | pending_evidence | 　 |
| 82 | auraphp/Aura.Sql | 0 | ∅ | — | pending_evidence | 　 |
| 83 | bdurand/capture_migration_sql | 0 | ∅ | — | pending_evidence | 　 |
| 84 | browniebroke/django-remake-migrations | 0 | ∅ | — | pending_evidence | 　 |
| 85 | datacleaner/DataCleaner | 0 | ∅ | — | pending_evidence | 　 |
| 86 | datazip-inc/olake-ui | 0 | ∅ | — | pending_evidence | 　 |
| 87 | dbeaver/dbeaver-common | 0 | ∅ | — | pending_evidence | 　 |
| 88 | emilioforrer/adonis-translatable | 0 | ∅ | — | pending_evidence | 　 |
| 89 | eosphoros-ai/DB-GPT-Hub | 0 | ∅ | — | pending_evidence | 　 |
| 90 | flyway/flyway-ant | 0 | ∅ | — | pending_evidence | 　 |
| 91 | gothunder/thunder | 0 | ∅ | — | pending_evidence | 　 |
| 92 | hhxsv5/gin-x | 0 | ∅ | — | pending_evidence | 　 |
| 93 | hongyuanw/simple-sharding | 0 | ∅ | — | pending_evidence | 　 |
| 94 | ilkerkorkut/gorm-hazelcast | 0 | ∅ | — | pending_evidence | 　 |
| 95 | ilorm/core | 0 | ∅ | — | pending_evidence | 　 |
| 96 | ioquatix/activerecord-rack | 0 | ∅ | — | pending_evidence | 　 |
| 97 | jpsca/sqla-wrapper | 0 | ∅ | — | pending_evidence | 　 |
| 98 | morphik-org/morphik-core | 0 | ∅ | — | pending_evidence | 　 |
| 99 | mwarkentin/django-watchman | 0 | ∅ | — | pending_evidence | 　 |
| 100 | mweibel/connect-session-sequelize | 0 | ∅ | — | pending_evidence | 　 |
| 101 | oscova/syn-bot-samples | 0 | ∅ | — | pending_evidence | 　 |
| 102 | patrick204nqh/dbwatcher | 0 | ∅ | — | pending_evidence | 　 |
| 103 | pavankjadda/LiquibaseDemo | 0 | ∅ | — | pending_evidence | 　 |
| 104 | pioz/plucker | 0 | ∅ | — | pending_evidence | 　 |
| 105 | renuo/hotsheet | 0 | ∅ | — | pending_evidence | 　 |
| 106 | rlemaigre/JMiniORM | 0 | ∅ | — | pending_evidence | 　 |
| 107 | rom-rb/rom-repository | 0 | ∅ | — | pending_evidence | 　 |
| 108 | ronin-rb/ronin | 0 | ∅ | — | pending_evidence | 　 |
| 109 | rusq/osx-callhistory-decryptor | 0 | ∅ | — | pending_evidence | 　 |
| 110 | sayanarijit/sqla-fancy-core | 0 | ∅ | — | pending_evidence | 　 |
| 111 | short-d/app | 0 | ∅ | — | pending_evidence | 　 |
| 112 | speedment/speedment-code-samples | 0 | ∅ | — | pending_evidence | 　 |
| 113 | sqlectron/sqlectron | 0 | ∅ | — | pending_evidence | 　 |
| 114 | ssbc/margaret | 0 | ∅ | — | pending_evidence | 　 |
| 115 | stephenafamo/scan | 0 | ∅ | — | pending_evidence | 　 |
| 116 | stoolap/stoolap-node | 0 | ∅ | — | pending_evidence | 　 |
| 117 | wayofdev/laravel-cycle-orm-adapter | 0 | ∅ | — | pending_evidence | 　 |
| 118 | willsoto/nestjs-objection | 0 | ∅ | — | pending_evidence | 　 |
| 119 | wonderbeyond/SQLAlchemy-Nested-Mutable | 0 | ∅ | — | pending_evidence | 　 |

