# unattr_judge 判定报告（v2 薄壳：attribution 引擎判定）
生成：2026-11-01 14:09 · 台账 9952 条 · 圈外未解读 1166 条（留给夜间队列）

## 状态分布
- no_evidence: 3875
- recheck: 1774
- oos: 1517
- judged_no_support: 894
- gated_app_cat: 719
- desc_pending: 501
- edu: 334
- draft: 292
- pending_evidence: 40
- partial_scan: 6

## 归属草案（draft 292 条，人工签发进 overrides.json；Top 30）

-  50025★ metabase/metabase → ClickHouse,PostgreSQL,MySQL（strong，ClickHouse=12,PostgreSQL=4.5,MySQL=2.5,MariaDB=0.5）｜路径 modules/drivers/clickhouse/LICENSE.txt
-  31471★ supermemoryai/supermemory → PostgreSQL（med，PostgreSQL=3）｜topic:postgres
-  23919★ sinaptik-ai/pandas-ai → Oracle,PostgreSQL（strong，Oracle=11.5,PostgreSQL=3,MySQL=1,SQL Server=1）｜路径 extensions/ee/connectors/oracle/LICENSE
-  20223★ eosphoros-ai/DB-GPT → MySQL（strong，MySQL=4,OceanBase=1）｜镜像 mysql ∈ docker-compose.yml
-  18427★ sqlc-dev/sqlc → MySQL,PostgreSQL,SQL Server,SQLite,ClickHouse（strong，MySQL=7.5,PostgreSQL=7.5,SQL Server=4.5,SQLite=3.5,ClickHouse=2.5）｜镜像 mysql ∈ docker-compose.yml
-   9701★ doctrine/dbal → MariaDB,MySQL,PostgreSQL,SQL Server,Oracle,SQLite（med，MariaDB=2.5,MySQL=2.5,PostgreSQL=2.5,SQL Server=2.5,Oracle=2,SQLite=2）｜topic:mariadb
-   5638★ liquibase/liquibase → MariaDB,SQL Server,MySQL,Oracle,PostgreSQL（med，MariaDB=4,SQL Server=4,MySQL=3,Oracle=3,PostgreSQL=2,SQLite=1）｜topic:mariadb
-   4757★ sqlectron/sqlectron → SQLite（med，）｜依赖 sqlite3 ∈ package.json
-   3715★ morphik-org/morphik-core → PostgreSQL（med，）｜依赖 psycopg ∈ pyproject.toml
-   3516★ mergestat/mergestat-lite → SQLite（med，SQLite=3,PostgreSQL=1）｜topic:sqlite
-   2167★ motor-admin/motor-admin → PostgreSQL,MySQL,SQL Server（strong，PostgreSQL=5,MySQL=3,SQL Server=2,SQLite=1）｜镜像 postgres ∈ docker-compose.yml
-   2012★ eosphoros-ai/DB-GPT-Hub → MySQL（med，）｜依赖 pymysql ∈ src/dbgpt-hub-gql/setup.py
-   1841★ schemacrawler/SchemaCrawler → PostgreSQL,MariaDB（med，PostgreSQL=3,MariaDB=2,ClickHouse=1,SQL Server=1）｜依赖 postgresql ∈ schemacrawler-dbconnectors/pom.xml
-   1525★ georgysavva/scany → SQL Server,PostgreSQL,MySQL（strong，SQL Server=3.5,PostgreSQL=3,MySQL=2）｜镜像 mssql ∈ docker-compose.yml
-   1525★ gobuffalo/pop → MySQL,PostgreSQL,SQLite,MariaDB（strong，MySQL=8,PostgreSQL=8,SQLite=7.5,MariaDB=2）｜路径 dialect_mysql.go
-   1522★ yulichang/mybatis-plus-join → MySQL,PostgreSQL（med，MySQL=3.5,PostgreSQL=2.5,Oracle=0.5）｜topic:mysql
-   1517★ ServiceStack/ServiceStack.OrmLite → SQL Server,MySQL,Oracle,PostgreSQL,SQLite（strong，SQL Server=14,MySQL=7,Oracle=7,PostgreSQL=5,SQLite=2）｜路径 src/ServiceStack.OrmLite.SqlServer/SqlServer2008OrmLiteDialectProvider.cs
-   1481★ myide/see → MySQL（med，MySQL=3）｜topic:mysql
-   1448★ dotnet/ef6 → SQL Server（med，SQL Server=3,MySQL=0.5）｜依赖 sqlclient ∈ src/EntityFramework/EntityFramework.InternalsVisibleTo.csproj
-   1399★ FrigadeHQ/remote-storage → SQLite（med，）｜依赖 sqlite3 ∈ apps/remote-storage-server/package.json
-   1353★ meteroid-oss/meteroid → ClickHouse（strong，ClickHouse=12）｜路径 modules/metering/src/connectors/clickhouse/extensions/mod.rs
-   1279★ scalikejdbc/scalikejdbc → MySQL,PostgreSQL（med，MySQL=2.5,PostgreSQL=2.5）｜topic:mysql
-   1257★ pmacct/pmacct → MySQL,PostgreSQL,SQLite（strong，MySQL=6,PostgreSQL=6,SQLite=6）｜路径 src/mysql_plugin.c
-    988★ goksan/statusnook → SQLite（med，SQLite=3）｜topic:sqlite
-    879★ schotime/NPoco → SQL Server（med，SQL Server=2）｜依赖 sqlclient ∈ src/NPoco.SqlServer.SystemData/NPoco.SqlServer.SystemData.csproj
-    805★ darbyluv2code/spring-and-hibernate-for-beginners → MySQL（strong，MySQL=7）｜路径 04-spring-mvc-crud-5/web-customer-tracker-starter-files/WebContent/WEB-INF/lib/mysql-connector-java-8.0.12.jar
-    760★ ronin-rb/ronin → SQLite（med，）｜依赖 sqlite3 ∈ Gemfile
-    732★ kubedb/cli → MySQL（strong，MySQL=53）｜路径 vendor/github.com/go-sql-driver/mysql/.gitignore
-    720★ wuba/Antenna → MySQL（strong，MySQL=5）｜镜像 mysql ∈ docker-compose.yml
-    651★ datacleaner/DataCleaner → PostgreSQL（med，）｜依赖 postgresql ∈ pom.xml

## 待复核（recheck：单弱信号只记录——weak/topic_only/dep_only）

-  47856★ DeusData/codebase-memory-mcp → SQLite（topic_only）｜topic:sqlite
-  40195★ drawdb-io/drawdb → PostgreSQL,Oracle,SQLite,SQL Server,MariaDB（topic_only）｜topic:mariadb
-  29427★ chroma-core/chroma → PostgreSQL,MySQL,SQLite,SQL Server（dep_only）｜依赖 lib/pq ∈ go/go.mod
-  25288★ hollischuang/toBeTopJavaer → MySQL（topic_only）｜topic:mysql
-  17479★ baomidou/mybatis-plus → PostgreSQL,MySQL（topic_only）｜topic:mysql
-   8701★ amitshekhariitbhu/Android-Debug-Database → SQLite（topic_only）｜topic:sqlite
-   6789★ webhooksite/webhook.site → SQLite（topic_only）｜topic:sqlite
-   6649★ nraiden/cofounder → PostgreSQL（topic_only）｜topic:postgresql
-   5156★ liam-hq/liam → PostgreSQL（topic_only）｜topic:postgresql
-   4866★ pudo/dataset → PostgreSQL,MySQL（weak）｜矩阵 mysql ∈ .github/workflows/build.yml
-   4655★ tangtangcoding/C-C- → MySQL（topic_only）｜topic:mysql
-   4633★ h2database/h2database → PostgreSQL（dep_only）｜依赖 postgresql ∈ h2/pom.xml
-   4455★ chef/bento → Oracle（topic_only）｜topic:oracle
-   4328★ whoiskatrin/sql-translator → PostgreSQL（topic_only）｜topic:postgresql
-   3413★ liyupi/sql-generator → MySQL（topic_only）｜topic:mysql
-   3282★ OmniDB/OmniDB → PostgreSQL,MySQL,Oracle（dep_only）｜依赖 pymysql ∈ requirements.txt
-   3093★ airingursb/bilibili-user → MySQL（topic_only）｜topic:mysql
-   2826★ notadd/notadd → PostgreSQL,MySQL,SQLite（topic_only）｜topic:mysql
-   2765★ hitchao/Jvedio → SQLite（topic_only）｜topic:sqlite
-   2757★ TencentCloud/TIMSDK → TDSQL（dep_only）｜路径 org:tencentcloud
-   2729★ aimeos/upscheme → PostgreSQL,MySQL,SQLite,SQL Server（topic_only）｜topic:sql-server
-   2534★ garden-co/classic-jazz → SQLite（dep_only）｜依赖 better-sqlite3 ∈ package.json
-   2520★ jarulraj/sqlcheck → PostgreSQL,MySQL,Oracle,SQLite（topic_only）｜topic:mysql
-   2501★ kentcdodds/kentcdodds.com → SQLite（topic_only）｜topic:sqlite
-   2148★ feldera/feldera → PostgreSQL（dep_only）｜依赖 postgres ∈ crates/connectors/Cargo.toml
-   2056★ 3masterplus/book → MySQL（topic_only）｜topic:mysql
-   1846★ tikv/grpc-rs → TiDB（dep_only）｜路径 org:tikv
-   1735★ FOSSBilling/FOSSBilling → MySQL,MariaDB（topic_only）｜topic:mariadb
-   1720★ matt-42/silicon → MySQL,SQLite,SQL Server（weak）｜依赖 sqlite3 ∈ examples/CMakeLists.txt
-   1659★ tikv/pprof-rs → TiDB（dep_only）｜路径 org:tikv
-   1641★ activeloopai/hivemind → PostgreSQL（topic_only）｜topic:postgres
-   1597★ microsoft/tigertoolbox → SQL Server（topic_only）｜topic:sqlserver
-   1493★ darbyluv2code/spring-boot-3-spring-6-hibernate-for-beginners → MySQL（topic_only）｜topic:mysql
-   1452★ dev-xo/remix-saas → SQLite（topic_only）｜topic:sqlite
-   1410★ matt-42/lithium → PostgreSQL,MySQL,SQLite（topic_only）｜topic:mysql
-   1275★ bareos/bareos → PostgreSQL,MySQL（topic_only）｜topic:mysql
-   1215★ kudobuilder/kudo → MySQL（topic_only）｜topic:mysql
-   1206★ Rishabh-creator601/Books → SQLite（topic_only）｜topic:sqlite3
-   1181★ tikv/rust-prometheus → TiDB（dep_only）｜路径 org:tikv
-   1178★ pentaho/mondrian → PostgreSQL,MySQL（dep_only）｜依赖 mysql-connector ∈ pom.xml

## 范围外命中抽检（防词表误伤，人工瞄一眼 Top 20）

-  77584★ grafana/grafana
-  76583★ redis/redis
-  75222★ Asabeneh/30-Days-Of-Python
-  65322★ coollabsio/coolify
-  61745★ makeplane/plane
-  59488★ meilisearch/meilisearch
-  52323★ etcd-io/etcd
-  46594★ LeCoupa/awesome-cheatsheets
-  45588★ payloadcms/payload
-  41902★ duckdb/duckdb
-  33096★ surrealdb/surrealdb
-  32591★ cockroachdb/cockroach
-  32163★ facebook/rocksdb
-  31760★ influxdata/influxdb
-  31743★ dragonflydb/dragonfly
-  30263★ TencentCloud/TencentDB-Agent-Memory
-  28614★ mongodb/mongo
-  27776★ forthespada/CS-Books
-  27369★ valkey-io/valkey
-  25254★ clockworklabs/SpacetimeDB

## 分层小结：desc_pending 501 · judged_no_support 894 · no_evidence 3875 · pending_evidence 40（增量补采队列）
