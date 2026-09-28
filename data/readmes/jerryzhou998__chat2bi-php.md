# chat2BI · 对话式数据分析

用 PHP 写的对话式 BI：**自然语言提问 → 两阶段 NL2SQL → 取数 → ECharts 可视化**。
大模型基于（Anthropic 兼容接口），支持 MySQL、达梦(DM) 与 Excel 目录三种数据源、多数据源、一个数据源跨多个库/文件。

Conversational BI written in PHP: Natural language question input → Two-stage NL2SQL → Data retrieval → ECharts visualization. The large model is built on the ‌Anthropic-compatible interface‌, and supports three data sources including MySQL, Dameng (DM) and Excel directories, as well as multi-data source scenarios and cross-database/file operations within a single data source.

## 功能特性

- **自然语言取数**：先选表再生成 SQL+图表推荐（两阶段 NL2SQL）。
- **只读安全**：代码层白名单校验，仅允许 SELECT/SHOW/DESC/EXPLAIN，拒绝写操作与危险函数。
- **前端渲染图表**：ECharts 客户端画图（饼/柱/折线），大模型只返回文字，不生成图片。
- **存下来的图表**：一键收藏，存下当时返回的完整 JSON，可新页展示、用原 SQL 重新取数、导出 CSV。
- **仪表盘**：把多个存图组合成栅格仪表盘（每行 1–3 个，宽度可调）。
- **多数据源**：数据源定义入库（密码 AES 加密），管理界面增删改查、测试连接、自动发现库。
- **一源多库**：一个数据源可跨多个数据库查询，表名带 `库.表` 前缀。
- **Excel 目录数据源**：指定一个目录，目录下所有 Excel/CSV 即数据源（文件名=库、sheet=表、首行=字段），支持跨文件查询。
- **清除 Schema 缓存**：表结构变更后一键重读。

## 架构

- **元数据库 `chat2bi`**：存 `data_source`（数据源定义）、`saved_chart`（存图）、`dashboard*`（仪表盘）。
- **业务数据源**：可多个，MySQL 或达梦，连接信息存于元库并按 `data_source_id` 隔离。
- **元数据与业务数据分离**：业务库不再有内部表，LLM 选表目录干净。

## 目录结构

```
common.php            大模型 JSON 调用封装
config.php            元库连接 / LLM / AES 密钥 / 缓存目录
sql/*.sql             演示业务库造数脚本（demo 数据）
lib/datasource.php    元库连接、AES、数据源 CRUD、按源连业务库
lib/excel.php         Excel 目录数据源：扫描、读取、SQLite 缓存 + ATTACH 执行
lib/schema.php        按数据源提取表目录 + 建表语句（带缓存）
lib/engine.php        两阶段 NL2SQL + 图表兜底校验
lib/execute.php       只读安全执行 + 行数上限
lib/saved.php         存图 / 仪表盘（元库，按数据源隔离）
public/index.html     聊天主界面（数据源切换 / 存图 / 仪表盘入口）
public/report.html    存图 / 仪表盘展示页（URL 参数控制显示）
public/dashboard.html 仪表盘设计器
public/admin.html     数据源管理
```

## 快速开始

1. **建库并授权**：新建元库 `chat2bi` 与业务库（如 `chat2bi_demo`），给应用账号授权：
   ```sql
   CREATE DATABASE chat2bi CHARACTER SET utf8mb4;
   CREATE DATABASE chat2bi_demo CHARACTER SET utf8mb4;
   CREATE DATABASE chat2bi_demo_mult CHARACTER SET utf8mb4;
   GRANT ALL ON chat2bi.* TO 'chat2bi_user'@'%' IDENTIFIED BY 'your_pwd';
   GRANT ALL ON chat2bi_demo.* TO 'chat2bi_user'@'%';
   GRANT ALL ON chat2bi_demo_mult.* TO 'chat2bi_user'@'%';
   FLUSH PRIVILEGES;
   ```
2. **配置 `config.php`**：改 `META_DB_*`（元库）、`LLM_BASE_URL/LLM_AUTH_TOKEN/LLM_MODEL*`、`DATA_SOURCE_AES_KEY`。
3. **安装依赖**：`composer install`（Excel 数据源需要 PhpSpreadsheet）。
4. **导入演示数据**（可选）：`mysql -uchat2bi_user -p chat2bi_demo < db/chat2bi_demo.sql`、`mysql -uchat2bi_user -p chat2bi_demo < db/chat2bi_demo_mult.sql`。mysql账号换成有权限的账号。
5. **启动**：把 `public/` 作为站点根目录，或 `php -S 0.0.0.0:8000 -t public`，浏览器访问。

> 元表（`data_source`/`saved_chart`/`dashboard`/`dashboard_item`）在首次使用时自动创建，无需手工建。

## 数据源管理

打开 `admin.html`（或 index 右上「⚙ 数据源」）：

- **新增/编辑/删除**：名称、类型（MySQL/达梦/Excel）、主机、端口、库名、账号、密码（编辑时留空则不修改）、快捷提问、是否默认。
- **测试连接**：验证当前配置能否连通。
- **自动发现库**：一键列出连接账号可访问的库/模式（过滤系统库），勾选后填入。
- **一源多库**：在「可访问的库/模式」里填多个库（每行一个），保存后该源的表目录、SQL 都带 `库.表` 前缀，可跨库查询。

> ⚠️ 跨库查询要求：连接账号对所有目标库有 SELECT 权限；且各库**排序规则需一致**（MySQL 如 `utf8mb4_general_ci`），否则字符串等值 JOIN 会报 `Illegal mix of collations`。

## Excel 目录数据源

在 `admin.html` 选择类型 **Excel 目录**，只需填「名称」与「目录路径」，其余账号/密码/端口不用填。映射规则：

| Excel 概念 | 映射为 |
|---|---|
| 目录（递归扫描所有层级） | 数据源 |
| 文件名（去扩展名，如 `销售数据.xlsx`） | 库名（schema） |
| 工作表名（sheet） | 表名 |
| 每个 sheet 的第一行 | 字段名 |
| 其余行 | 数据 |

- 支持 `.xlsx` / `.xls` / `.csv`；一个文件里多个 sheet 均为表，表目录与 SQL 用 `库名.表名` 前缀。
- **跨文件查询**：可以 `销售数据.订单明细` JOIN `客户.客户信息`，只要都在该数据源目录下。
- **执行引擎**：每个 Excel 文件灌进一个缓存 SQLite（放在 `cache/excel_<id>/`，按文件 mtime 增量重建），查询时 `ATTACH` 为同名 schema，直接跑 SQL。字段类型按首 30 行采样推断（INTEGER/REAL/TEXT），日期列自动转 `YYYY-MM-DD`。
- **自动发现库**：「自动发现库」会列出目录下所有文件名（库名）。
- 依赖 `phpoffice/phpspreadsheet`，首次使用需 `composer install`。
- 表结构/sheet 变更后，在 `schema.html` 点「🔄 初始化」或清除 Schema 缓存即可重读。

## 存图 / 仪表盘

- **存图**：聊天结果点「📌 存下图表」，存下完整 JSON（含当时返回的 columns/rows/sql 等）。
- **查看**：左侧列表点击存图 → 新页 `report.html?id=<id>`。
- **仪表盘**：左侧「＋ 新建仪表盘」→ `dashboard.html` 选择存图、设置每行宽度、保存；点 ✎ 编辑、✕ 删除。
- **重新取数**：`report.html` 的「🔄 重新取数」用保存时的 SQL 在**该图所属数据源**上重跑。

## report.html URL 参数

| 参数 | 作用 |
|------|------|
| `?id=<id>` | 展示单个存图 |
| `?dash=<id>` | 展示仪表盘 |
| `title=0` | 隐藏标题 |
| `explanation=0` | 隐藏说明 |
| `chart=0` | 隐藏图表 |
| `table=0` | 隐藏表格 |
| `export=0` / `download=0` | 禁用导出 |
| `refresh=0` | 隐藏「重新取数」 |

默认显示：标题、说明、图表、重新取数；默认隐藏：表格、导出。存图/SQL/涉及表在 report 页恒不显示。

## API 一览（`public/api.php`）

| 接口 | 说明 |
|------|------|
| `chat` | 聊天取数（`?ds=` 指定数据源） |
| `schemas` | 某数据源的表目录 |
| `quick` | 某数据源的快捷提问 |
| `run_sql` | 执行只读 SQL（重新取数） |
| `clear_schema` | 清除某数据源的结构缓存 |
| `save_chart` / `saved_charts` / `get_chart` / `delete_chart` | 存图管理 |
| `save_dashboard` / `list_dashboards` / `get_dashboard` / `delete_dashboard` | 仪表盘管理 |
| `list_data_sources` / `get_data_source` / `save_data_source` / `delete_data_source` / `test_data_source` / `discover_schemas` | 数据源管理 |

## 注意事项

- `config.php` 含大模型 Token 与 AES 密钥，**注意保密**。
- 大模型接口为 Anthropic 兼容格式，已在 `common.php` 封装；换模型改 `config.php` 的 `LLM_MODEL*` 即可。
- 达梦(DM) 需 PHP 安装 `pdo_dm` 驱动；建表语句经 `SP_TABLEDEF` 获取，表目录经 `SYS.SYSOBJECTS`。
- **导出格式**：`config.php` 的 `EXPORT_FORMAT` 决定前端「导出」按钮下载 CSV 还是 Excel（`csv`/`excel`）。导出由后端 `api.php?action=export` 生成（Excel 用 PhpSpreadsheet），前端按钮文案随之显示。
