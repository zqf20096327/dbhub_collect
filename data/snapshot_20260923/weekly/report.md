# 📋 数据库开源生态周报 · 第 7 期

> 📌 **数据源**：GitHub。聚焦开源工具与实验项目，不涉及厂商内核信息。生产可用性请自行评估。

> _2026-09-23_

---

## 📌 本周 DBA 速览

> _本期为首期（无 7 天基准），活跃榜/新锐自第 02 期起完整。_



## 🗄️ 板块一 · 国际主流数据库
> 范围：Oracle / SQL Server / DB2 / MySQL / PostgreSQL / MariaDB / ClickHouse。仅收录上述数据库生态的开源工具，不含 AI 项目。

### 🔥 活跃榜 Top3

_（首期无基准 / 本板块本周无正向增长项目。）_

### 🌱 新锐发现（最多 3 个）

> ① **[0xmikadzyki/ghost](https://github.com/0xmikadzyki/ghost)** · ⭐ 18 · 本周 **+18**
> `迁移` · 适用：ClickHouse
> Fund-flow pipeline for Robinhood Chain (chain 4663): full ERC-20 Transfer…
> 🤖 **AI 解读**：该项目将Robinhood Chain的ERC-20转账数据回填至ClickHouse，提供只读JSON API，供查询资金流向。

> ② **[Sahil1337/perch](https://github.com/Sahil1337/perch)** · ⭐ 9 · 本周 **+9**
> `其他` · 适用：MySQL / PostgreSQL
> A lightweight SQL workspace for developers. Explore schemas, write and run SQL…
> 🤖 **AI 解读**：Perch是面向开发者的轻量SQL工作区，支持MySQL与PostgreSQL，提供模式浏览、编辑、执行与结果查看，本地运行。

> ③ **[hakureiyuyuko/LMBY](https://github.com/hakureiyuyuko/LMBY)** · ⭐ 6 · 本周 **+6**
> `其他` · 适用：PostgreSQL
> LMBY —— Light 的 Emby：单二进制 + PostgreSQL 的轻量媒体服务器（Go + React，纯 Web 播放、硬件转码、Emby…
> 🤖 **AI 解读**：LMBY 是自托管媒体服务器，用 PostgreSQL 存元数据与任务队列，供浏览器播放影视库。

### 🔍 本周解读

_（本板块本周无解读项目。）_



## 🇨🇳 板块二 · 国内数据库
> 范围：openGauss / GaussDB / TiDB / OceanBase / TDSQL / PolarDB / PolarDB-X / YashanDB / GBase / DM / GoldenDB。仅收录上述数据库生态的开源项目（内核以各厂商官方为准），不含 AI 项目。

### 🔥 活跃榜 Top3

_（首期无基准 / 本板块本周无正向增长项目。）_

### 🌱 新锐发现（最多 3 个）

> ① **[ngclara07/tcm-explorer](https://github.com/ngclara07/tcm-explorer)** · ⭐ 0 · 近7天 1 commits
> `平台` · 适用：MySQL / TiDB
> Traditional Chinese Medicine knowledge-base explorer built with Node.js…
> 🤖 **AI 解读**：该项目基于Node.js与MySQL/TiDB，提供中药知识图谱检索与科研查询面板，便于数据库使用者查询草药、成分、靶点及疾病关联数据。

> ② **[tuxin-labs/trino-418-dameng](https://github.com/tuxin-labs/trino-418-dameng)** · ⭐ 0 · 近7天 0 commits
> `其他` · 适用：DM
> 基于 Trino 418 的达梦数据库(DM8)连接器发行版
> 🤖 **AI 解读**：基于Trino 418的DM连接器发行版，支持SQL查询与写入DM数据。

> ③ **[openeverest/provider-tidb](https://github.com/openeverest/provider-tidb)** · ⭐ 0 · 近7天 0 commits
> `平台` · 适用：TiDB
> OpenEverest provider for TiDB - uses official operator
> 🤖 **AI 解读**：OpenEverest的TiDB provider，借助官方operator在Kubernetes上部署和管理TiDB，供云原生环境使用。

### 🔍 本周解读

_（本板块本周无解读项目。）_



## 🤖 板块三 · AI 工具
> 范围：板块一 / 板块二所列数据库生态的 AI 辅助工具（text2sql / AI DBA / DB-MCP 等）。

### 🔥 活跃榜 Top3

_（首期无基准 / 本板块本周无正向增长项目。）_

### 🌱 新锐发现（最多 3 个）

> ① **[wangke-112/agent-safe-tools](https://github.com/wangke-112/agent-safe-tools)** · ⭐ 3 · 本周 **+3**
> `其他` · 适用：MySQL
> Ask your AI coding agent, in natural language, to search production logs or…
> 🤖 **AI 解读**：该项目提供MySQL只读MCP服务，通过代码校验限制SQL操作，供AI代理安全查询生产库。

> ② **[Sajjad-rafiee/CareerOpportunityEngine](https://github.com/Sajjad-rafiee/CareerOpportunityEngine)** · ⭐ 3 · 本周 **+3**
> `其他` · 适用：PostgreSQL
> FastAPI + Postgres/pgvector backend that ingests job postings, embeds and…
> 🤖 **AI 解读**：该项目用PostgreSQL与pgvector存储职位数据，支持语义检索及资格信息提取，供数据库使用者参考。

> ③ **[Cyrax321/QwerySmith-1.0](https://github.com/Cyrax321/QwerySmith-1.0)** · ⭐ 3 · 本周 **+3**
> `其他` · 适用：PostgreSQL
> QwerySmith: open text-to-SQL models that answer from retrieved evidence with…
> 🤖 **AI 解读**：面向PostgreSQL的文本转SQL模型，可依据检索证据生成带引用SQL或拒答，附训练评估工具。

### 🔍 本周解读

_（本板块本周无解读项目。）_



## 📊 Top 总榜（历史 Star 总数）

| 项目 | 总 Star | 板块 | 分类 | 一句话定位 |
| :--- | ---: | :--- | :--- | :--- |
| **[grafana/grafana](https://github.com/grafana/grafana)** | 76.9k | 国外数据库 | 监控 | The open and composable observability and data visualization… |
| **[dbeaver/dbeaver](https://github.com/dbeaver/dbeaver)** | 51.9k | 国外数据库 | 其他 | Free universal database tool and SQL client |
| **[drawdb-io/drawdb](https://github.com/drawdb-io/drawdb)** | 39.7k | AI工具 | 其他 | Free, simple, and intuitive online database diagram editor and SQL… |
| **[OtterMind/Chat2DB](https://github.com/OtterMind/Chat2DB)** | 28.2k | AI工具 | 管理 | Chat2DB is a free, cross-platform, local-first database client and… |
| **[PostgREST/postgrest](https://github.com/PostgREST/postgrest)** | 27.7k | 国外数据库 | 其他 | REST API for any Postgres database |



## 💬 互动与说明

- 💬 **互动**：本周你最关注哪个项目？欢迎留言分享你的试用体验。
- 📌 **板块范围**：板块一 Oracle / SQL Server / DB2 / MySQL / PostgreSQL / MariaDB / ClickHouse；板块二 openGauss / GaussDB / TiDB / OceanBase / TDSQL / PolarDB / PolarDB-X / YashanDB / GBase / DM / GoldenDB；板块三为上述数据库生态的 AI 辅助工具。范围外数据库项目不入周报。
- 📌 **说明**：由 `ai_db_weekly` 基于 GitHub 数据自动采集（截至 2026-09-23）。项目描述来自 GitHub 项目的 description 字段；AI 解读基于项目 README，由 AI 生成，仅供参考。国产数据库板块仅收录在 GitHub 上活跃的开源项目，内核以各厂商官方为准。分类字段采用固定枚举值。


---
