# T4b 程序适配回写报告（引擎 0.3.0 + t4a-1）
生成：2026-11-05 23:30 · 入圈 13521 · 回写 1741 · 打原因 11780

## 黑洞归零
- 入圈（最新记录 dbs 空）: 13521
- 回写 dbs: 1741（engine 1741 / adjudicate 0）
- 打原因: 11780 · 真不涉及 5236 · 范围外 461 · 证据不足 6083
- 池内未解读（新仓未解读，台账记数不写记录）: 2089
- 覆盖率: 入圈 100% 带结论（fill+tag = 13521）

## 回写库位分布（engine）
- PostgreSQL: 666
- MySQL: 568
- SQLite: 432
- Oracle: 222
- SQL Server: 162
- TiDB: 143
- ClickHouse: 65
- MariaDB: 65
- GaussDB: 48
- OceanBase: 42
- TDSQL: 32
- YashanDB: 14
- openGauss: 13
- Dameng: 7
- PolarDB: 4
- GBase: 4
- GoldenDB: 2

## 抽检 20 条（star 降序·源混排）

-    732★ kubedb/cli → MySQL（engine；MySQL=53）
-    514★ splitgraph/seafowl → PostgreSQL（engine；PostgreSQL=2）
-    514★ L-codes/pwcrack-framework → MySQL（engine；MySQL=4）
-    514★ tikv/titan → TiDB（engine；TiDB=1）
-    512★ directus/v8-archive → PostgreSQL,MySQL,Oracle,SQLite,SQL Server（engine；PostgreSQL=11.5 MySQL=4 Oracle=2 SQL Server=2 SQLite=2）
-    506★ liaozb/APIJSON.NET → MySQL,SQL Server（engine；MySQL=2 SQL Server=2）
-    505★ alextanhongpin/database-design → PostgreSQL,MySQL,SQLite（engine；MySQL=5 PostgreSQL=2 SQLite=1）
-    501★ jet/equinox → PostgreSQL,MySQL,SQL Server（engine；MySQL=4 SQL Server=4 PostgreSQL=2）
-    496★ agent-next/polymarket-paper-trader → PostgreSQL,SQLite（engine；SQLite=2 PostgreSQL=1）
-    496★ blastrain/vitess-sqlparser → MySQL（engine；MySQL=2）
-    492★ gnormal/gnorm → PostgreSQL,MySQL（engine；PostgreSQL=29.5 MySQL=23）
-    485★ armbian/config → MySQL（engine；MySQL=2）
- 159444★ Snailclimb/JavaGuide → [真不涉及] 教学/内容类
- 114579★ supabase/supabase → [真不涉及] 应用类（cat=其他），引擎立案未采纳: PostgreSQL
- 113503★ thedotmack/claude-mem → [真不涉及] 应用类（cat=其他），引擎立案未采纳: PostgreSQL,SQLite
-  32247★ meta/rocksdb → [范围外] 名称/简介命中范围外词
-  16600★ realm/realm-swift → [范围外] 名称/简介命中范围外词
-    949★ kividbio/kividb → [范围外] 生态命中: redis,valkey
-  60509★ twentyhq/twenty → [证据不足] 证据 partial 树截断（待重采）；简介候选未证实: PostgreSQL；readme 行号提名未证实: PostgreSQL
-  50763★ ClickHouse/ClickHouse → [证据不足] 证据 partial 树截断（待重采）；简介候选未证实: ClickHouse；readme 行号提名未证实: ClickHouse
-  36344★ SheetJS/sheetjs → [证据不足] 无信号
