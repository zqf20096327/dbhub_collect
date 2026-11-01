# T3b 抽查版复核表（50 条 · 每行看 README 引证 + 引擎建议 → 人工栏打 ✓/✗）

> 填法：同意引擎建议 → 人工栏抄引擎的库清单前加 ✓；某库认为误配 → ✗库名；整仓不涉及 → 不涉及。
> 50 条命中 ≥45（90%）过闸进第 4 批。填完说一声，我算命中率。

## ① 点名缺口（抽头 15）

| # | 仓 | star | 现判 | 引擎建议 | README 引证/证据 | 人工栏 |
|---|---|---|---|---|---|---|
| 1 | Snailclimb/JavaGuide | 159,351 | ∅ | MySQL | L223: ### MySQL | 同意引擎建议　 |
| 2 | macrozheng/mall | 84,990 | MySQL | MySQL | L164: |JDK|17|https://www.oracle.com/java/technologies/javase/ | 　同意引擎建议 |
| 3 | netdata/netdata | 81,226 | ∅ | MySQL+PostgreSQL | L121: |**Packaged Applications**<small> nginx, apache, postgre | 同意引擎建议　 |
| 4 | prisma/orm | 47,664 | PostgreSQL | PostgreSQL+SQL Server+MySQL+MariaDB+SQLite | L95: MySQL follows after SQLite. See the feature scoreboard f |同意引擎建议 　 |
| 5 | LeCoupa/awesome-cheatsheets | 46,600 | ∅ | no_evidence | L81: - MySQL | 　MySQL |
| 6 | pingcap/tidb | 40,690 | TiDB | TiDB+MySQL | L30: - **MySQL Compatibility**: TiDB is compatible with MySQL | 同意引擎建议　 |
| 7 | The-Vibe-Company/quivr | 39,617 | ∅ | PostgreSQL | L43: api --> store[(PostgreSQL + object storage<br/>every ver | 同意引擎建议　 |
| 8 | 0voice/interview_internal_reference | 37,262 | ∅ | MySQL | L19: ##### 1.1.7 MySQL的数据如何恢复到任意时间点？ | 　同意引擎建议 |
| 9 | AobingJava/JavaFamily | 36,980 | ∅ | MySQL | L112: - MySQL基础知识 | 同意引擎建议　 |
| 10 | cockroachdb/cockroach | 32,596 | ∅ | PostgreSQL | L33: 4. Use a PostgreSQL-compatible driver or ORM to build an | 同意引擎建议　 |
| 11 | forthespada/CS-Books | 27,787 | ∅ | no_evidence | L395: - 《ClickHouse中文文档》 百度云链接 提取码：vjb3 | ClickHouse+MySQL+SQL Server+SQLite　 |
| 12 | taosdata/TDengine | 25,179 | ∅ | below_quorum | L160: |`BUILD_WITH_SQLITE`|`OFF`|Build with SQLite support.| | SQLite+oracle　 |
| 13 | tursodatabase/turso | 25,095 | ∅ | SQLite | L4: An in-process SQL database, compatible with SQLite, and  | 　PostgreSQL+SQLite |
| 14 | dolthub/dolt | 24,775 | ∅ | MySQL+MariaDB | L6: Connect to Dolt just like any MySQL database to read or  | 同意引擎建议　 |
| 15 | Vonng/ddia | 23,885 | ∅ | no_evidence | L9: **译者**：冯若航 / Vonng (rh@vonng.com) Pigsty 创始人，活跃开源贡献者，Pos | 同意引擎建议　 |

## ② 全空工具（抽头 10）

| # | 仓 | star | 现判 | 引擎建议 | README 引证/证据 | 人工栏 |
|---|---|---|---|---|---|---|
| 1 | grafana/grafana | 77,584 | ∅ | MySQL+PostgreSQL | topic:MySQL@topic:mysql; dep:MySQL@go.mod | 　MySQL+PostgreSQL+SQL SERVER |
| 2 | coollabsio/coolify | 65,322 | ∅ | PostgreSQL+MariaDB+MySQL | image:PostgreSQL@docker-compose.dev-multi; image:PostgreSQL@docker-compose.windows.y | PostgreSQL+MariaDB+MySQL+CLICKHOUSE+SQLITE　 |
| 3 | metabase/metabase | 50,025 | ∅ | ClickHouse+PostgreSQL+MySQL | tree:ClickHouse@modules/drivers/clickhou; tree:ClickHouse@modules/drivers/clickhou | 同意引擎建议 |
| 4 | DeusData/codebase-memory-mcp | 47,856 | ∅ | SQLite | topic:SQLite@topic:sqlite | 　同意引擎建议 |
| 5 | drawdb-io/drawdb | 40,195 | ∅ | MariaDB+Oracle+PostgreSQL+SQL Server+SQLite | topic:MariaDB@topic:mariadb; topic:Oracle@topic:oracle-database | 　同意引擎建议 |
| 6 | sqlmapproject/sqlmap | 38,820 | ∅ | no_evidence | — | 　ClickHouse+sql server +mysql+oracle+postgresql |
| 7 | supermemoryai/supermemory | 31,471 | ∅ | PostgreSQL | topic:PostgreSQL@topic:postgres; dep:PostgreSQL@package.json | 　同意引擎建议 |
| 8 | airbytehq/airbyte | 22,291 | ∅ | MySQL+PostgreSQL+SQL Server | topic:MySQL@topic:mysql; topic:PostgreSQL@topic:postgresql | 　ClickHouse+PostgreSQL+MySQL+mariadb+oracle+sql server+sqlite+tidb |
| 9 | eosphoros-ai/DB-GPT | 20,223 | ∅ | MySQL | image:MySQL@docker-compose.yml; dep:MySQL@packages/dbgpt-ext/pypro | ClickHouse+gaussdb+sql server+mysql+oceanbase+opengauss+postgresql+sqlite　 |
| 10 | sqlc-dev/sqlc | 18,427 | ∅ | MySQL+PostgreSQL+SQL Server+SQLite+ClickHouse | image:MySQL@docker-compose.yml; topic:MySQL@topic:mysql | 　同意引擎建议 |

## ③ 误杀候选（抽头 10）

| # | 仓 | star | 现判 | 引擎建议 | README 引证/证据 | 人工栏 |
|---|---|---|---|---|---|---|
| 1 | smartcontractkit/chainlink | 8,252 | PostgreSQL | PostgreSQL+Oracle | L14: This repo contains the Chainlink core node and contracts | 同意引擎建议　 |
| 2 | linkedin/school-of-sre | 8,152 | ∅ | MySQL | L21: - Relational Databases (MySQL) | 同意引擎建议　 |
| 3 | WiseLibs/better-sqlite3 | 7,538 | SQLite | SQLite | L77: For these situations, you should probably use a full-fle | 同意引擎建议　 |
| 4 | doocs/technical-books | 7,024 | ∅ | no_evidence | L69: |2|[高性能 MySQL 第三版[2013]](https://item.jd.com/11220393.ht | 同意引擎建议　 |
| 5 | akopytov/sysbench | 6,814 | PostgreSQL+MySQL | MySQL+PostgreSQL | L131: yum -y install mariadb-devel openssl-devel | 　同意引擎建议 |
| 6 | alibaba/AliSQL | 5,992 | ∅ | pending_evidence | L5: Alibaba's MySQL Branch with DuckDB Analytics and Native  | 　mysql |
| 7 | pgsty/pigsty | 5,877 | PostgreSQL+PolarDB | PostgreSQL | L60: |OpenHalo|**MySQL Simulation**|MySQL wire-protocol compa | 同意引擎建议　 |
| 8 | go-pg/pg | 5,777 | PostgreSQL | PostgreSQL | L132: - Golang ClickHouse ORM | 同意引擎建议　 |
| 9 | rfyiamcool/share_ppt | 5,750 | ∅ | MySQL | L396: ### mysql快速讲义 | 同意引擎建议　 |
| 10 | malisper/pgrust | 5,693 | ∅ | PostgreSQL | L296: engine and runs analytical queries as much as 3x faster  | 　同意引擎建议 |

## ④ 现行 draft 未签发·引擎已立案（头 15，star 降序）

| # | 仓 | star | 引擎建议（含票数） | 证据 | 人工栏 |
|---|---|---|---|---|---|
| 1 | sqlectron/sqlectron | 4,757 | SQLite（） | 依赖 sqlite3 ∈ package.json | 同意引擎建议　 SQLite |
| 2 | morphik-org/morphik-core | 3,715 | PostgreSQL（） | 依赖 psycopg ∈ pyproject.toml | 同意引擎建议　  PostgreSQL|
| 3 | mergestat/mergestat-lite | 3,516 | SQLite（SQLite=3,PostgreSQL=1） | topic:sqlite; 依赖 go-sqlite3 ∈ go.mod | SQLite+　PostgreSQL |
| 4 | motor-admin/motor-admin | 2,167 | PostgreSQL+MySQL+SQL Server（PostgreSQL=5,MySQL=3,SQL Server=2,SQLite=1） | 镜像 postgres ∈ docker-compose.yml; topic:postgresql | 同意引擎建议 PostgreSQL+MySQL+SQL Server　 |
| 5 | eosphoros-ai/DB-GPT-Hub | 2,012 | MySQL（） | 依赖 pymysql ∈ src/dbgpt-hub-gql/setup.py | 同意引擎建议　 MySQL |
| 6 | gobuffalo/pop | 1,525 | MySQL+PostgreSQL+SQLite+MariaDB（MySQL=8,PostgreSQL=8,SQLite=7.5,MariaDB=2） | 路径 dialect_mysql.go; 镜像 mysql ∈ docker-compose.yml | 同意引擎建议　MySQL+PostgreSQL+SQLite+MariaDB |
| 7 | georgysavva/scany | 1,525 | SQL Server+PostgreSQL+MySQL（SQL Server=3.5,PostgreSQL=3,MySQL=2） | 镜像 mssql ∈ docker-compose.yml; 依赖 go-mssqldb ∈ go.mod | 同意引擎建议　SQL Server+PostgreSQL+MySQL |
| 8 | yulichang/mybatis-plus-join | 1,522 | MySQL+PostgreSQL（MySQL=3.5,PostgreSQL=2.5,Oracle=0.5） | topic:mysql; 依赖 mysql-connector ∈ mybatis-plus-join-test/pom.xml | 同意引擎建议　 MySQL+PostgreSQL |
| 9 | ServiceStack/ServiceStack.OrmLite | 1,517 | SQL Server+MySQL+Oracle+PostgreSQL+SQLite（SQL Server=14,MySQL=7,Oracle=7,PostgreSQL=5,SQLite=2） | 路径 src/ServiceStack.OrmLite.SqlServer/SqlServer2008OrmLiteDialectProvider.cs; 路径 src/ServiceStack.OrmLite.SqlServer/SqlServer2012OrmLiteDialectProvider.cs |同意引擎建议 SQL Server+MySQL+Oracle+PostgreSQL+SQLite　 |
| 10 | myide/see | 1,481 | MySQL（MySQL=3） | topic:mysql; 依赖 pymysql ∈ backend/requirements.txt | 　同意引擎建议 mysql |
| 11 | FrigadeHQ/remote-storage | 1,399 | SQLite（） | 依赖 sqlite3 ∈ apps/remote-storage-server/package.json | 同意引擎建议 sqlite　 |
| 12 | meteroid-oss/meteroid | 1,353 | ClickHouse（ClickHouse=12） | 路径 modules/metering/src/connectors/clickhouse/extensions/mod.rs; 路径 modules/metering/src/connectors/clickhouse/extensions/openstack_ext.rs | 同意引擎建议 ClickHouse　 |
| 13 | scalikejdbc/scalikejdbc | 1,279 | MySQL+PostgreSQL（MySQL=2.5,PostgreSQL=2.5） | topic:mysql; 矩阵 mysql ∈ .github/workflows/ci.yml |同意引擎建议  MySQL+PostgreSQL+sqlite　 |
| 14 | pmacct/pmacct | 1,257 | MySQL+PostgreSQL+SQLite（MySQL=6,PostgreSQL=6,SQLite=6） | 路径 src/mysql_plugin.c; 路径 src/mysql_plugin.h | 同意引擎建议  MySQL+PostgreSQL+sqlite　 |
| 15 | goksan/statusnook | 988 | SQLite（SQLite=3） | topic:sqlite; 依赖 go-sqlite3 ∈ go.mod | 同意引擎建议   sqlite　 |
