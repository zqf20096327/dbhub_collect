# T4b 程序适配回写报告（引擎 0.3.0 + t4a-1）
生成：2026-11-04 23:22 · 入圈 12050 · 回写 1953 · 打原因 10097

## 黑洞归零
- 入圈（最新记录 dbs 空）: 12050
- 回写 dbs: 1953（engine 1953 / adjudicate 0）
- 打原因: 10097 · 真不涉及 3674 · 范围外 460 · 证据不足 5963
- 池内未解读（新仓未解读，台账记数不写记录）: 2049
- 覆盖率: 入圈 100% 带结论（fill+tag = 12050）

## 回写库位分布（engine）
- PostgreSQL: 782
- MySQL: 664
- SQLite: 498
- Oracle: 257
- SQL Server: 201
- TiDB: 159
- ClickHouse: 86
- MariaDB: 85
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

-  29634★ chroma-core/chroma → PostgreSQL,MySQL,SQL Server（engine；PostgreSQL=1.5 MySQL=0.5 SQL Server=0.5）
-  25154★ tursodatabase/turso → SQLite（engine；SQLite=14）
-  24816★ dolthub/dolt → PostgreSQL,MySQL,SQL Server,MariaDB（engine；MySQL=16 SQL Server=9.5 MariaDB=5 PostgreSQL=1）
-  23927★ sinaptik-ai/pandas-ai → PostgreSQL,MySQL,Oracle,SQL Server（engine；Oracle=11.5 PostgreSQL=3 MySQL=1 SQL Server=1）
-  22316★ airbytehq/airbyte → PostgreSQL,MySQL,Oracle,SQLite,SQL Server,ClickHouse,TiDB（engine；SQL Server=74 MySQL=67 ClickHouse=42.5 PostgreSQL=29.5 Oracle=26 TiDB=7 SQLite=2）
-  21750★ oracle/graal → Oracle（engine；Oracle=203）
-  20258★ eosphoros-ai/DB-GPT → PostgreSQL,MySQL,Oracle,SQLite,SQL Server,ClickHouse,OceanBase,openGauss,GaussDB（engine；OceanBase=11 MySQL=6 ClickHouse=2 GaussDB=2 Oracle=2 PostgreSQL=2 SQL Server=2 SQLite=2 openGauss=2）
-  18432★ sqlc-dev/sqlc → PostgreSQL,MySQL,SQLite,SQL Server,ClickHouse（engine；PostgreSQL=111.5 SQLite=25.5 SQL Server=12.5 ClickHouse=8.5 MySQL=7.5）
-  17499★ questdb/questdb → PostgreSQL（engine；PostgreSQL=8）
-  17483★ baomidou/mybatis-plus → PostgreSQL,MySQL,Oracle,SQL Server（engine；MySQL=2 Oracle=2 PostgreSQL=2 SQL Server=2）
-  16935★ tikv/tikv → TiDB（engine；TiDB=5）
-  14180★ geldata/gel → SQLite（engine；SQLite=2）
- 159424★ Snailclimb/JavaGuide → [真不涉及] 教学/内容类
- 114526★ supabase/supabase → [真不涉及] 应用类（cat=其他），引擎立案未采纳: PostgreSQL
- 112768★ thedotmack/claude-mem → [真不涉及] 应用类（cat=其他），引擎立案未采纳: PostgreSQL,SQLite
-  32242★ meta/rocksdb → [范围外] 名称/简介命中范围外词
-  16599★ realm/realm-swift → [范围外] 名称/简介命中范围外词
-    924★ kividbio/kividb → [范围外] 生态命中: redis,valkey
-  60436★ twentyhq/twenty → [证据不足] 证据 partial 树截断（待重采）；简介候选未证实: PostgreSQL；readme 行号提名未证实: PostgreSQL
-  50747★ ClickHouse/ClickHouse → [证据不足] 证据 partial 树截断（待重采）；简介候选未证实: ClickHouse；readme 行号提名未证实: ClickHouse
-  36341★ SheetJS/sheetjs → [证据不足] 无信号
