# T4b 程序适配回写报告（引擎 0.3.0 + t4a-1）
生成：2026-11-04 19:42 · 入圈 12028 · 回写 1964 · 打原因 10064

## 黑洞归零
- 入圈（最新记录 dbs 空）: 12028
- 回写 dbs: 1964（engine 1964 / adjudicate 0）
- 打原因: 10064 · 真不涉及 3653 · 范围外 453 · 证据不足 5958
- 池内未解读（新仓未解读，台账记数不写记录）: 1727
- 覆盖率: 入圈 100% 带结论（fill+tag = 12028）

## 回写库位分布（engine）
- PostgreSQL: 792
- MySQL: 669
- SQLite: 504
- Oracle: 263
- SQL Server: 202
- TiDB: 160
- ClickHouse: 90
- MariaDB: 88
- GaussDB: 49
- OceanBase: 45
- TDSQL: 36
- openGauss: 14
- YashanDB: 14
- Dameng: 7
- PolarDB: 5
- GBase: 4
- GoldenDB: 2

## 抽检 20 条（star 降序·源混排）

-  81226★ netdata/netdata → PostgreSQL,MySQL,Oracle,SQL Server,ClickHouse,MariaDB（engine；MySQL=82.5 PostgreSQL=73.5 SQL Server=50 ClickHouse=39 MariaDB=12.5 Oracle=6）
-  77584★ grafana/grafana → PostgreSQL,MySQL,Oracle,SQLite,ClickHouse（engine；MySQL=16 PostgreSQL=6.5 Oracle=2 SQLite=2 ClickHouse=0.5）
-  65322★ coollabsio/coolify → PostgreSQL,MySQL,MariaDB（engine；PostgreSQL=8 MariaDB=2 MySQL=2）
-  50025★ metabase/metabase → PostgreSQL,MySQL,Oracle,SQLite,SQL Server,ClickHouse,MariaDB（engine；ClickHouse=66 PostgreSQL=16.5 MySQL=14.5 SQL Server=14 Oracle=12 SQLite=6.5 MariaDB=2）
-  47856★ DeusData/codebase-memory-mcp → SQLite（engine；SQLite=2）
-  40195★ drawdb-io/drawdb → PostgreSQL,Oracle,SQLite,SQL Server,MariaDB（engine；MariaDB=2 Oracle=2 PostgreSQL=2 SQL Server=2 SQLite=2）
-  39617★ The-Vibe-Company/quivr → PostgreSQL（engine；PostgreSQL=238.5）
-  38820★ sqlmapproject/sqlmap → PostgreSQL,MySQL,Oracle,SQLite,SQL Server,ClickHouse（engine；MySQL=16 Oracle=16 PostgreSQL=16 SQL Server=16 ClickHouse=14 SQLite=14）
-  32596★ cockroachdb/cockroach → PostgreSQL（engine；PostgreSQL=6.5）
-  31471★ supermemoryai/supermemory → PostgreSQL（engine；PostgreSQL=3）
-  25095★ tursodatabase/turso → SQLite（engine；SQLite=14）
-  24775★ dolthub/dolt → PostgreSQL,MySQL,SQL Server,MariaDB（engine；MySQL=16 SQL Server=9.5 MariaDB=5 PostgreSQL=1）
- 159351★ Snailclimb/JavaGuide → [真不涉及] 教学/内容类
-  64188★ usememos/memos → [真不涉及] 应用类（cat=应用），引擎立案未采纳: PostgreSQL,MySQL,SQLite
-  61745★ makeplane/plane → [真不涉及] 应用类（cat=应用），引擎立案未采纳: PostgreSQL
-  16599★ realm/realm-swift → [范围外] 名称/简介命中范围外词
-    581★ memvid/claude-brain → [范围外] 名称/简介命中范围外词
-    365★ zszszszsz/.config → [范围外] 名称/简介命中范围外词
-  25179★ taosdata/TDengine → [证据不足] 无信号；弱路径信号不直通: PostgreSQL,MySQL；范围外痕迹: 生态命中: tdengine；简介候选未证实: SQLite；readme 行号提名
-  23885★ Vonng/ddia → [证据不足] 无信号；简介候选未证实: PostgreSQL；readme 行号提名未证实: PostgreSQL
-  22582★ typicode/lowdb → [证据不足] 无信号；范围外痕迹: 名称/简介命中范围外词；简介候选未证实: PostgreSQL；readme 行号提名未证实: PostgreSQL
