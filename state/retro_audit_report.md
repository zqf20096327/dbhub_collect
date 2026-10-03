# retro_audit 重审报告（候选覆盖度判据）
生成：2026-10-03 12:46 UTC

- 基线 111 条：**已完成 63** · 待续跑 0（再触发直到=0）· 不可跑/停滞 48（出池/no_readme/超重试上限）
- 归属新增（旧空 → 新有）：2 条
- 归属变化（宽度/构成）：5 条
- 类别翻转：9 条
- **>9 库归属（护栏改造的审计底册）**：0 条

## 结构性缺口清单（候选来自描述、v3 行号规则不可判——interpret 提示词改进工单）

- SpoonX/wetland：缺问 PostgreSQL
- devasherr/Nexom：缺问 PostgreSQL,SQLite
- gazeldx/db_admin：缺问 Oracle
- gideaoms/clark-orm：缺问 PostgreSQL,MySQL,SQL Server
- soul-soft/SqlBatis：缺问 SQLite,SQL Server
- zzzprojects/Dapper.Transaction：缺问 MySQL,SQLite
- xiaonuobase/Snowy-Layui：缺问 PostgreSQL,SQL Server,Dameng
- grafana/grafana：缺问 PostgreSQL
- prisma/orm：缺问 SQL Server,MariaDB
- The-Vibe-Company/quivr：缺问 PostgreSQL

## 归属新增明细（Top 50）

- jokruger/dec128 → PostgreSQL（补判 Oracle）
- tikv/migration → TiDB（补判 TiDB）

## 归属变化明细（Top 50）

- prisma/orm：PostgreSQL → PostgreSQL,SQLite（补判 SQL Server,MariaDB）
- tconbeer/harlequin：PostgreSQL,MySQL,SQLite → PostgreSQL,MySQL,MariaDB,SQLite（补判 MariaDB）
- alienwithin/OWASP-mth3l3m3nt-framework：PostgreSQL,MySQL,SQLite → PostgreSQL,MySQL,SQLite,SQL Server（补判 SQL Server）
- wenb1n-dev/SmartDB_MCP：PostgreSQL,MySQL,Oracle,SQL Server,MariaDB → PostgreSQL,MySQL,Oracle,SQL Server,MariaDB,Dameng（补判 Dameng）
- ofershap/cursor-usage-tracker：SQLite → SQLite,PostgreSQL（补判 PostgreSQL）

## 类别翻转明细（Top 20）

- diadata-org/diadata：其他 → 平台
- douglasmonsky/codex-usage-tracker：监控 → 应用
- EskoSalaka/mtgtools：应用 → 开发库
- wenb1n-dev/SmartDB_MCP：管理 → 连接/代理
- xyproto/permissionsql：安全/审计 → 开发库
- nonbeing/mysqlclient-python3-aws-lambda：开发库 → 其他
- ofershap/cursor-usage-tracker：应用 → 监控
- frekele/docker-java：应用 → 其他
- kychee-com/run402：平台 → 应用

逐条明细见 retro_audit_report.jsonl（status 含 pending/skipped/stalled）。
