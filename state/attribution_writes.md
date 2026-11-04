# T4b 程序适配回写报告（引擎 0.3.0 + t4a-1）
生成：2026-11-04 12:57 · 入圈 12028 · 回写 1963 · 打原因 10065

## 黑洞归零
- 入圈（最新记录 dbs 空）: 12028
- 回写 dbs: 1963（engine 1963 / adjudicate 0）
- 打原因: 10065 · 真不涉及 3653 · 范围外 459 · 证据不足 5953
- 池内未解读（新仓未解读，台账记数不写记录）: 1998
- 覆盖率: 入圈 100% 带结论（fill+tag = 12028）

## 回写库位分布（engine）
- PostgreSQL: 791
- MySQL: 669
- SQLite: 503
- Oracle: 262
- SQL Server: 205
- TiDB: 159
- ClickHouse: 90
- MariaDB: 89
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

-  81265★ netdata/netdata → PostgreSQL,MySQL,Oracle,SQL Server,ClickHouse,MariaDB（engine；MySQL=82.5 PostgreSQL=73.5 SQL Server=50 ClickHouse=39 MariaDB=12.5 Oracle=6）
-  77664★ grafana/grafana → PostgreSQL,MySQL,Oracle,SQLite,ClickHouse（engine；MySQL=8 PostgreSQL=6.5 Oracle=2 SQLite=2 ClickHouse=0.5）
-  65588★ coollabsio/coolify → PostgreSQL,MySQL,MariaDB（engine；PostgreSQL=6 MariaDB=2 MySQL=2）
-  50143★ metabase/metabase → PostgreSQL,MySQL,Oracle,SQLite,SQL Server,ClickHouse,MariaDB（engine；ClickHouse=66 PostgreSQL=16.5 MySQL=14.5 SQL Server=14 Oracle=12 SQLite=6.5 MariaDB=2）
-  48067★ DeusData/codebase-memory-mcp → SQLite（engine；SQLite=2）
-  40233★ drawdb-io/drawdb → PostgreSQL,Oracle,SQLite,SQL Server,MariaDB（engine；MariaDB=2 Oracle=2 PostgreSQL=2 SQL Server=2 SQLite=2）
-  39626★ The-Vibe-Company/quivr → PostgreSQL（engine；PostgreSQL=238.5）
-  38842★ sqlmapproject/sqlmap → PostgreSQL,MySQL,Oracle,SQLite,SQL Server,ClickHouse（engine；MySQL=16 Oracle=16 PostgreSQL=16 SQL Server=16 ClickHouse=14 SQLite=14）
-  32602★ cockroachdb/cockroach → PostgreSQL（engine；PostgreSQL=6.5）
-  31521★ supermemoryai/supermemory → PostgreSQL（engine；PostgreSQL=3）
-  29627★ chroma-core/chroma → PostgreSQL,MySQL,SQL Server（engine；PostgreSQL=1.5 MySQL=0.5 SQL Server=0.5）
-  25137★ tursodatabase/turso → SQLite（engine；SQLite=14）
- 159408★ Snailclimb/JavaGuide → [真不涉及] 教学/内容类
-  64251★ usememos/memos → [真不涉及] 应用类（cat=应用），引擎立案未采纳: PostgreSQL,MySQL,SQLite
-  61915★ makeplane/plane → [真不涉及] 应用类（cat=应用），引擎立案未采纳: PostgreSQL
-  16599★ realm/realm-swift → [范围外] 名称/简介命中范围外词
-    745★ kividbio/kividb → [范围外] 生态命中: redis,valkey
-    583★ memvid/claude-brain → [范围外] 名称/简介命中范围外词
-  36342★ SheetJS/sheetjs → [证据不足] 无信号
-  25182★ taosdata/TDengine → [证据不足] 无信号；弱路径信号不直通: PostgreSQL,MySQL；范围外痕迹: 生态命中: tdengine；简介候选未证实: SQLite；readme 行号提名
-  23908★ Vonng/ddia → [证据不足] 无信号；简介候选未证实: PostgreSQL；readme 行号提名未证实: PostgreSQL
