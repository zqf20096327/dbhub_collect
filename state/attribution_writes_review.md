# T4b 回写抽检 20 条人工过目表

> 生成 2026-11-03 · 12 条回写(fill) + 8 条打原因(tag)。**人工结论栏请填：同意 / 不同意+改判**。

| # | 仓 | ★ | 动作 | 写后结论 | 证据链 | 人工结论 |
|---|---|---|---|---|---|---|
| 1 | netdata/netdata | 81,226 | 回写 | MySQL（adjudicate） | MySQL: 仓库 topic 标签：mysql；依赖清单 src/go/go.mod：命中 go-sql-driver/mysql |  |
| 2 | grafana/grafana | 77,584 | 回写 | PostgreSQL,MySQL（adjudicate） | MySQL: 仓库 topic 标签：mysql；依赖清单 go.mod：命中 go-sql-driver/mysql ｜ PostgreSQL: 仓库 topic 标签：postgres；依赖清单 apps/dashboard/go.mod：命中 lib/pq（测试/示例语境，弱） |  |
| 3 | coollabsio/coolify | 65,322 | 回写 | PostgreSQL,MySQL,MariaDB（adjudicate） | MariaDB: 仓库 topic 标签：mariadb ｜ PostgreSQL: 仓库 topic 标签：postgres；容器镜像 docker-compose.dev-multi.yml：命中 postgres；容器镜像 docker-compose.windows.yml：命中 postgres；容器镜像 dock ｜ MySQL: 仓库 topic 标签：mysql |  |
| 4 | usememos/memos | 64,188 | 回写 | SQLite（adjudicate） | SQLite: 仓库 topic 标签：sqlite |  |
| 5 | makeplane/plane | 61,745 | 回写 | PostgreSQL（adjudicate） | PostgreSQL: 仓库 topic 标签：postgresql；容器镜像 docker-compose-local.yml：命中 postgres；容器镜像 docker-compose.yml：命中 postgres；容器镜像 docker-compose |  |
| 6 | metabase/metabase | 50,025 | 回写 | PostgreSQL,MySQL（adjudicate） | MySQL: 仓库 topic 标签：mysql；CI 矩阵 .github/workflows/app-db.yml：命中 mysql ｜ PostgreSQL: 仓库 topic 标签：postgres；仓库 topic 标签：postgresql；CI 矩阵 .github/workflows/app-db.yml：命中 postgres |  |
| 7 | payloadcms/payload | 45,588 | 回写 | PostgreSQL（adjudicate） | PostgreSQL: 仓库 topic 标签：postgres；CI 矩阵 .github/workflows/main.yml：命中 postgres；依赖清单 examples/multi-tenant/package.json：命中 postgres（测试 |  |
| 8 | drawdb-io/drawdb | 40,195 | 回写 | PostgreSQL,Oracle,SQLite,SQL Server,MariaDB（adjudicate） | MariaDB: 仓库 topic 标签：mariadb ｜ Oracle: 仓库 topic 标签：oracle-database ｜ PostgreSQL: 仓库 topic 标签：postgresql ｜ SQL Server: 仓库 topic 标签：sql-server ｜ SQLite: 仓库 topic 标签：sqlite |  |
| 9 | sqlmapproject/sqlmap | 38,820 | 回写 | MySQL,Oracle,PostgreSQL,SQL Server,ClickHouse,SQLite（engine） | MySQL: 路径 mysql@plugins/dbms/mysql/__init__.py(2); 路径 mysql@plugins/dbms/mysql/audit.py(2) ｜ Oracle: 路径 oracle@plugins/dbms/oracle/__init__.py(2); 路径 oracle@plugins/dbms/oracle/audit.py(2) ｜ PostgreSQL: 路径 postgresql@plugins/dbms/postgresql/__init__.py(2); 路径 postgresql@plugins/dbms/postgresql/audit.py(2) ｜ SQL Server: 路径 mssqlserver@plugins/dbms/mssqlserver/__init__.py(2); 路径 mssqlserver@plugins/ |  |
| 10 | supermemoryai/supermemory | 31,471 | 回写 | PostgreSQL（adjudicate） | PostgreSQL: 仓库 topic 标签：postgres；依赖清单 package.json：命中 pg、postgres |  |
| 11 | dubinc/dub.link | 25,038 | 回写 | MySQL,ClickHouse（adjudicate） | ClickHouse: 仓库 topic 标签：clickhouse ｜ MySQL: 仓库 topic 标签：mysql；CI 矩阵 .github/workflows/playwright.yaml：命中 mysql |  |
| 12 | sinaptik-ai/pandas-ai | 23,919 | 回写 | Oracle,PostgreSQL（engine） | Oracle: 路径 oracle@extensions/ee/connectors/oracle/LICENSE(2); 路径 oracle@extensions/ee/connectors/oracle/README.md(2) ｜ PostgreSQL: 镜像 postgres@docker-compose.yml(2); 依赖 psycopg@extensions/connectors/sql/pyproject.toml(1) ｜ MySQL: 依赖 pymysql@extensions/connectors/sql/pyproject.toml(1) ｜ SQL Server: 依赖 pymssql@extensions/connectors/sql/pyproject.toml(1) |  |
| 13 | The-Vibe-Company/quivr | 39,617 | 打原因 | [真不涉及] AI 判过非 support（db_verdicts 非空） | — |  |
| 14 | dolthub/dolt | 24,775 | 打原因 | [真不涉及] AI 判过非 support（db_verdicts 非空） | — |  |
| 15 | Vonng/ddia | 23,885 | 打原因 | [真不涉及] AI 判过非 support（db_verdicts 非空） | — |  |
| 16 | Snailclimb/JavaGuide | 159,351 | 打原因 | [范围外] 生态命中: redis | — |  |
| 17 | LeCoupa/awesome-cheatsheets | 46,600 | 打原因 | [范围外] 生态命中: redis | — |  |
| 18 | 0voice/interview_internal_reference | 37,262 | 打原因 | [范围外] 生态命中: mongodb,redis | — |  |
| 19 | DeusData/codebase-memory-mcp | 47,856 | 打原因 | [证据不足] topic 单通道不放直通（SQLite） | — |  |
| 20 | hollischuang/toBeTopJavaer | 25,288 | 打原因 | [证据不足] topic 单通道不放直通（MySQL） | — |  |
| 21 | jiji262/douyin-downloader | 12,499 | 打原因 | [证据不足] 无信号；简介候选未证实: SQLite | — |  |
