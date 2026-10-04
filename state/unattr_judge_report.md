# unattr_judge 判定报告
生成：2026-10-04 08:36 · 台账 401 条 · 圈外未解读 276 条（留给夜间队列）

## 状态分布
- no_evidence: 155
- oos: 129
- judged_no_support: 51
- edu: 32
- draft: 17
- recheck: 11
- gated_app_cat: 4
- desc_pending: 2

## 归属草案（draft 17 条，人工签发进 overrides.json；Top 30）

-  38587★ sqlmapproject/sqlmap → PostgreSQL,MySQL,Oracle,SQLite,SQL Server,ClickHouse｜路径 plugins/dbms/clickhouse
-  23811★ sinaptik-ai/pandas-ai → PostgreSQL,MySQL,Oracle,SQL Server｜路径 extensions/ee/connectors/oracle
-  20074★ eosphoros-ai/DB-GPT → PostgreSQL,MySQL,Oracle,SQLite,SQL Server,ClickHouse,OceanBase,openGauss,GaussDB｜文件 packages/dbgpt-ext/src/dbgpt_ext/datasource/rdbms/conn_clickhouse.py
-   4873★ pudo/dataset → PostgreSQL,MySQL｜依赖 psycopg ∈ pyproject.toml
-   4757★ sqlectron/sqlectron → SQLite｜依赖 sqlite3 ∈ package.json
-   3715★ morphik-org/morphik-core → PostgreSQL｜依赖 psycopg ∈ pyproject.toml
-   3284★ OmniDB/OmniDB → PostgreSQL,MySQL,Oracle｜依赖 psycopg ∈ requirements.txt
-   2111★ feldera/feldera → PostgreSQL｜路径 crates/adapters/src/integrated/postgres.rs
-   2012★ eosphoros-ai/DB-GPT-Hub → MySQL｜依赖 pymysql ∈ src/dbgpt-hub-gql/setup.py
-   1838★ schemacrawler/SchemaCrawler → PostgreSQL,MySQL,Oracle,SQLite,SQL Server,ClickHouse,MariaDB｜路径 schemacrawler-dbconnectors/src/main/resources/dbconnectors/clickhouse.yaml
-   1449★ dotnet/ef6 → SQL Server｜依赖 sqlclient ∈ src/EntityFramework.NuGet/EntityFramework.NuGet.csproj
-   1399★ FrigadeHQ/remote-storage → SQLite｜依赖 sqlite3 ∈ apps/remote-storage-server/package.json
-    880★ schotime/NPoco → PostgreSQL,SQL Server｜依赖 microsoft.data.sqlclient ∈ src/NPoco.SqlServer.SystemData/NPoco.SqlServer.SystemData.csproj
-    760★ ronin-rb/ronin → SQLite｜依赖 sqlite3 ∈ Gemfile
-    733★ kubedb/cli → MySQL｜路径 vendor/github.com/go-sql-driver/mysql
-    664★ qustavo/sqlhooks → PostgreSQL,MySQL,SQLite｜依赖 lib/pq ∈ go.mod
-    651★ datacleaner/DataCleaner → PostgreSQL｜依赖 postgresql ∈ pom.xml

## 待复核（recheck：弱证据 / 独立库依赖模式）

-  29427★ chroma-core/chroma → PostgreSQL,MySQL,SQLite,SQL Server（dep_only）｜依赖 lib/pq ∈ go/go.mod
-   4633★ h2database/h2database → PostgreSQL（dep_only）｜依赖 postgresql ∈ h2/pom.xml
-   2534★ garden-co/classic-jazz → SQLite（dep_only）｜依赖 better-sqlite3 ∈ package.json
-   1720★ matt-42/silicon → MySQL,SQLite,SQL Server（weak）｜依赖 sqlite3 ∈ examples/CMakeLists.txt
-   1178★ pentaho/mondrian → PostgreSQL,MySQL（dep_only）｜依赖 mysql-connector ∈ pom.xml
-   1063★ khonsulabs/bonsaidb → PostgreSQL,SQLite（weak）｜依赖 postgresql ∈ benchmarks/Cargo.toml
-    922★ cometbft/cometbft → PostgreSQL（dep_only）｜依赖 lib/pq ∈ go.mod
-    920★ pixelsdb/pixels → MySQL（dep_only）｜依赖 mysql-connector ∈ pom.xml
-    895★ sourcenetwork/defradb → PostgreSQL（dep_only）｜依赖 lib/pq ∈ go.mod
-    871★ hyrise/hyrise → PostgreSQL,SQLite（dep_only）｜依赖 sqlite3 ∈ CMakeLists.txt
-    838★ akumuli/Akumuli → SQLite（dep_only）｜依赖 sqlite3 ∈ CMakeLists.txt

## 范围外命中抽检（防词表误伤，人工瞄一眼 Top 20）

-  76574★ redis/redis
-  75097★ Asabeneh/30-Days-Of-Python
-  59471★ meilisearch/meilisearch
-  52323★ etcd-io/etcd
-  41875★ duckdb/duckdb
-  33094★ surrealdb/surrealdb
-  32539★ cockroachdb/cockroach
-  32154★ facebook/rocksdb
-  31759★ influxdata/influxdb
-  31737★ dragonflydb/dragonfly
-  28615★ mongodb/mongo
-  27396★ forthespada/CS-Books
-  27359★ valkey-io/valkey
-  25250★ clockworklabs/SpacetimeDB
-  25150★ taosdata/TDengine
-  22583★ typicode/lowdb
-  21804★ dgraph-io/dgraph
-  21358★ valeriansaliou/sonic
-  17809★ VictoriaMetrics/VictoriaMetrics
-  17619★ apache/pouchdb

## 分层小结：desc_pending 2 · judged_no_support 51 · no_evidence 155 · api_error/partial 0（--retry-errors 补扫）
