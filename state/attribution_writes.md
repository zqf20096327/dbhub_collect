# T4b 程序适配回写报告（引擎 0.3.0 + t4a-1）
生成：2026-11-07 11:17 · 入圈 20826 · 回写 979 · 打原因 19847

## 黑洞归零
- 入圈（最新记录 dbs 空）: 20826
- 回写 dbs: 979（engine 979 / adjudicate 0）
- 打原因: 19847 · 真不涉及 12440 · 范围外 466 · 证据不足 6941
- 池内未解读（新仓未解读，台账记数不写记录）: 2105
- 覆盖率: 入圈 100% 带结论（fill+tag = 20826）

## 回写库位分布（engine）
- PostgreSQL: 340
- MySQL: 320
- SQLite: 227
- TiDB: 109
- Oracle: 106
- SQL Server: 88
- ClickHouse: 38
- OceanBase: 37
- MariaDB: 27
- GaussDB: 27
- TDSQL: 17
- YashanDB: 14
- openGauss: 11
- Dameng: 6
- GBase: 4
- PolarDB: 3
- GoldenDB: 2

## 抽检 20 条（star 降序·源混排）

-    280★ pingcap/dumpling → MySQL,TiDB（engine；MySQL=3.5 TiDB=3）
-     56★ BankOfCommunications/CBASE → PostgreSQL,MySQL,Oracle,OceanBase（engine；MySQL=41.5 Oracle=10 PostgreSQL=10 OceanBase=2.5）
-     38★ AnghelLeonard/Hibernate-SpringBoot-4 → PostgreSQL,MySQL,Oracle（engine；PostgreSQL=32 MySQL=31 Oracle=2）
-     31★ percona/community → PostgreSQL,MySQL（engine；MySQL=3 PostgreSQL=3）
-     31★ sonhmai/how-sqlite-works → SQLite（engine；SQLite=3）
-     31★ rusq/osx-callhistory-decryptor → SQLite（engine；SQLite=1）
-     31★ youkeihinn/redis-monitor → SQLite（engine；SQLite=1）
-     31★ umeshiscreative/AVSQLDebugger → SQLite（engine；SQLite=2）
-     31★ Trivadis/plsql-cop-sqldev → Oracle（engine；Oracle=2）
-     31★ joomla-framework/database → PostgreSQL,MySQL,SQLite,SQL Server,MariaDB（engine；MySQL=5 PostgreSQL=5 SQLite=4.5 SQL Server=2.5 MariaDB=0.5）
-     31★ mpgn/CRIME-poc → Oracle（engine；Oracle=2）
-     31★ Astrix-Labs/papez → PostgreSQL（engine；PostgreSQL=2）
- 159455★ Snailclimb/JavaGuide → [真不涉及] 教学/内容类
- 114626★ supabase/supabase → [真不涉及] 应用类（cat=其他），引擎立案未采纳: PostgreSQL
- 114189★ thedotmack/claude-mem → [真不涉及] 应用类（cat=其他），引擎立案未采纳: PostgreSQL,SQLite
-  32252★ meta/rocksdb → [范围外] 名称/简介命中范围外词
-  16600★ realm/realm-swift → [范围外] 名称/简介命中范围外词
-   6172★ apache/pinot → [范围外] 生态命中: vector-database,vector-search
-  60583★ twentyhq/twenty → [证据不足] 证据 partial 树截断（待重采）；简介候选未证实: PostgreSQL；readme 行号提名未证实: PostgreSQL
-  50800★ ClickHouse/ClickHouse → [证据不足] 证据 partial 树截断（待重采）；简介候选未证实: ClickHouse；readme 行号提名未证实: ClickHouse
-  36339★ SheetJS/sheetjs → [证据不足] 无信号
