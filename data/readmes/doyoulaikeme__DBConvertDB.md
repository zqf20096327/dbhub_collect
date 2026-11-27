# DBConvertDB — 数据库结构与数据迁移工具

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![.NET Framework](https://img.shields.io/badge/.NET%20Framework-4.8-512BD4)](https://dotnet.microsoft.com/download/dotnet-framework/net48)

一个自带引擎的数据库迁库工具：在 MySQL、PostgreSQL、Oracle、SQL Server、SQLite、达梦 DM、金仓 KingbaseES、openGauss、OceanBase、TiDB、GBase 8a、瀚高等任意两种库之间迁移，源库和目标库都可以是其中任意一种，不限国产库。

提供两套入口，共用同一个引擎：

- `DbConvert.Cli.exe`：命令行，适合写成脚本、批处理、上线迁移单。
- `DbConvert.Gui.exe`：WPF 图形界面，勾选表、点按钮就能迁，适合现场实施。

核心能力：读源库结构 → 生成目标库建表/索引/注释/默认值/生成列/CHECK/外键/视图 DDL → 分批搬数据 → 行数 + 逐行校验和核对 → 同类型库直接创建过程/函数/触发器（跨类型库生成改造草稿）→ 输出脚本、类型映射、对象问题清单、迁移报告。

**运行环境：.NET Framework 4.8。** Windows 10/11 自带；Windows 7 SP1 需安装 4.8 运行时。不支持 Windows XP。

![DBConvertDB 主界面](https://cdn.jsdelivr.net/gh/doyoulaikeme/DBConvertDB@main/docs/screenshot.png)

---

## 典型迁移场景

- **MySQL → 达梦 DM / 金仓 KingbaseES**：表结构、数据、视图、过程/函数、触发器一次迁移；同类型库对象直接创建，跨类型对象生成改造草稿。
- **Oracle → 金仓 / openGauss**：表、默认值、CHECK、外键、视图迁移，按目标语法改写函数和类型。
- **SQL Server → PostgreSQL / MySQL**：默认值、计算列、CHECK、外键、视图迁移，保留行数与校验和核对。
- **SQLite → MySQL / PostgreSQL**：离线库、现场临时库、历史数据搬迁，适合先迁结构再搬数。
- **医院、政务、内网环境**：不依赖外网，GUI 和 CLI 共用同一引擎，可先“只生成 SQL”再人工审核上线。

## 1. 支持的库

| 类别 | kind 取值 | 说明 |
|---|---|---|
| MySQL 系 | `mysql` `tidb` `oceanbase` `gbase8a` | 走 information_schema，MySQL 协议 |
| PostgreSQL 系 | `postgres` `opengauss` `kingbase` `highgo` | 走 pg_class / pg_indexes / information_schema |
| Oracle | `oracle` | ALL_TAB_COLUMNS 等数据字典，11g 支持 |
| 达梦 | `dm` | 同 Oracle 字典结构，方言单独适配（IDENTITY、FLOAT/DOUBLE） |
| SQL Server | `sqlserver` | sys.* 目录视图 |
| SQLite | `sqlite` | PRAGMA，适合做中间库 / 离线交付 |

驱动处理方式：

- MySQL / PostgreSQL / Oracle / SQL Server / SQLite 的驱动已随程序打包，Windows 10/11 自带 .NET Framework 4.8；Windows 7 SP1 需要先安装 4.8 运行时。
- 达梦、金仓等厂商驱动不随包分发（授权原因），把 `DmProvider.dll` / `Kdbndp.dll` 及其依赖放到 **程序目录** 或 **程序目录下的 `providers` 子目录**，工具会自动找到；也可以在配置里显式指定 `providerAssembly` / `providerType`。具体文件清单和获取方式见 [providers/README.md](providers/README.md)。

先用这条命令确认驱动状态：

```powershell
DbConvert.Cli.exe providers
```

---

## 2. 目录结构

```
DBConvertDB
├─ DBConvertDB.sln
├─ src
│  ├─ DbConvert.Core        # 引擎：方言、结构读取、DDL、数据泵、校验、报告
│  ├─ DbConvert.Providers   # 内置驱动注册（NuGet 驱动都在这）
│  ├─ DbConvert.Cli         # 命令行
│  └─ DbConvert.Gui         # WPF 界面
├─ samples                  # 示例配置和造数脚本（真实库文件不入库）
├─ providers                # 厂商驱动目录说明（DLL 不入库）
├─ assets                   # 应用图标
├─ docs                     # 文档与界面截图
├─ .github/workflows        # GitHub Actions 编译检查
├─ Directory.Build.props    # net48 引用程序集与 SDK 兼容配置
├─ LICENSE                  # MIT
├─ CONTRIBUTING.md          # 贡献指南
├─ publish.ps1              # 一键发布到 dist
└─ README.md
```

厂商驱动 `DmProvider.dll` / `Kdbndp.dll` 因授权原因不放在仓库里，运行时放到程序目录或程序目录下的 `providers` 子目录即可。

---

## 3. 快速开始（命令行）

```powershell
git clone https://github.com/doyoulaikeme/DBConvertDB.git
cd DBConvertDB

# 0) 先编译（需要 .NET SDK 8.0 或更高）
dotnet build DBConvertDB.sln -c Debug

# 1) 生成配置模板
.\src\DbConvert.Cli\bin\Debug\net48\DbConvert.Cli.exe init --out mysql2dm.json --source-kind mysql --target-kind dm

# 2) 改 json 里的连接信息，然后测试连接
.\src\DbConvert.Cli\bin\Debug\net48\DbConvert.Cli.exe test --config mysql2dm.json
.\src\DbConvert.Cli\bin\Debug\net48\DbConvert.Cli.exe test --config mysql2dm.json --side target

# 3) 先看结构：会生成建表脚本 + 类型映射 CSV + 报告，不碰目标库
.\src\DbConvert.Cli\bin\Debug\net48\DbConvert.Cli.exe plan --config mysql2dm.json

# 4) 真正迁移（建表 + 搬数 + 校验）
.\src\DbConvert.Cli\bin\Debug\net48\DbConvert.Cli.exe migrate --config mysql2dm.json

# 5) 只做核对 / 迁移中断后续传
.\src\DbConvert.Cli\bin\Debug\net48\DbConvert.Cli.exe verify  --config mysql2dm.json
.\src\DbConvert.Cli\bin\Debug\net48\DbConvert.Cli.exe migrate --config mysql2dm.json --resume
```

常用开关：`--drop`（先删目标表）、`--truncate`（清空数据保留表）、`--only "patient,visit*"`、`--exclude "*_log"`、`--mode schema|data|verify`、`--verify-mode count|none`、`--batch 2000`、`--identity-mode sequence`、`--script-only`（只生成 SQL、不连目标库）、`--log-file run.log`、`--dry-run`。

命令一览：

| 命令 | 作用 |
|---|---|
| `providers` | 列出支持的类型和驱动是否就绪 |
| `init` | 生成配置模板 |
| `test` | 测试源/目标连接 |
| `inspect` | 打印表结构（可 `--json` 导出） |
| `plan` | 只生成脚本/映射/报告，不动目标库 |
| `script` | 只输出建表脚本 |
| `migrate` | 建表 + 搬数据 + 校验 |
| `verify` | 只核对行数与校验和 |

### 示例数据

`samples/` 下的配置可以直接参考，但密码字段已替换为 `YOUR_PASSWORD`，运行前要改成本地实际密码。

```powershell
# SQLite 示例源库（生成 samples/src.db，已被 .gitignore 排除）
python samples/make_sqlite.py

# MySQL 示例源库对象（需要本机有 MySQL）
mysql -uroot -p dbconvert_test < samples/demo_objects.sql

# 跑一个 SQLite → SQLite 示例
.\src\DbConvert.Cli\bin\Debug\net48\DbConvert.Cli.exe migrate --config samples/sqlite2sqlite.json
```

---

## 4. 图形界面

```powershell
.\src\DbConvert.Gui\bin\Debug\net48\DbConvert.Gui.exe
```

界面流程：填源库和目标库 → `测试连接` → `读取源表结构`（列出表、行数、列数，可勾选）→ 右侧选选项 → 勾选 `只生成 SQL（不连目标库）` 时按钮变成 `生成 SQL`，只产出脚本；不勾选则 `开始迁移` 直连目标库执行 → `校验` → `打开输出目录`。

迁移过程日志实时滚动，结束后弹窗给出每张表的行数汇总，报告和脚本都写在输出目录里。

---

## 5. 配置文件

```json
{
  "source": {
    "kind": "mysql",
    "host": "127.0.0.1",
    "port": 3306,
    "database": "his",
    "user": "root",
    "password": "YOUR_PASSWORD"
  },
  "target": {
    "kind": "dm",
    "host": "127.0.0.1",
    "port": 5236,
    "database": "HIS",
    "schema": "HIS",
    "user": "SYSDBA",
    "password": "YOUR_PASSWORD",
    "providerAssembly": "DmProvider.dll"
  },
  "options": {
    "mode": "both",
    "include": "*",
    "exclude": "*_tmp,*_bak",
    "dropExisting": false,
    "truncateTarget": false,
    "createIndexes": true,
    "createIndexesAfterLoad": true,
    "batchSize": 2000,
    "identifierCase": "auto",
    "identityMode": "auto",
    "emptyStringAsNull": false,
    "overflowPolicy": "truncate",
    "verifyMode": "checksum",
    "scriptOnly": false,
    "outDir": "output"
  },
  "tables": [
    { "source": "patient", "target": "PATIENT" },
    { "source": "visit", "target": "VISIT", "where": "visit_date >= '2024-01-01'" },
    { "source": "dict", "skipColumns": ["photo"], "overrides": [ { "source": "memo", "targetType": "VARCHAR2(2000)" } ] }
  ]
}
```

`source` / `target` 字段：`kind`、`host`、`port`、`database`、`schema`、`user`、`password`、`connectionString`（填了就完全按它连）、`providerAssembly`、`providerType`。

`tables` 段可选，用来改表名、按条件抽数、只迁部分列、覆盖列类型/可空/注释。不写就按 `include/exclude` 全量迁。

常用 `options`：

| 配置 | 默认 | 说明 |
|---|---|---|
| `mode` | both | `both` / `schema`（只建表）/ `data`（只搬数）/ `verify` |
| `scriptOnly` | false | true 时只生成结构 SQL/报告（含表、视图、过程/函数/触发器），不连目标库、不搬数据、不生成 INSERT（GUI 的“只生成 SQL”勾选） |
| `dropExisting` | false | 目标同名表先删再建，风险高，建议先看 plan |
| `truncateTarget` | false | 保留表结构，只清空数据 |
| `createIndexesAfterLoad` | true | 索引等数据搬完再建，大表快很多 |
| `identifierCase` | auto | `auto` 跟目标库走（Oracle/达梦大写、PG 小写、其余保留），也可 `upper`/`lower`/`preserve` |
| `identityMode` | auto | `auto` 按目标版本决定；Oracle 11g 自动切成 `sequence` |
| `varcharLengthMode` | auto | `auto`/`chars`/`bytes`，按字节算长度时用 `bytesPerChar`（默认 3） |
| `emptyStringAsNull` | false | Oracle/达梦把 `''` 当 NULL，需要严格对齐时打开 |
| `overflowPolicy` | fail | 超长值处理：`fail` 报错 / `truncate` 截断 / `skipRow` 跳过该行 |
| `verifyMode` | checksum | `checksum` 行数+逐行校验和 / `count` 只比行数 / `none` |
| `resume` | false | 断点续传，配合 `stateFile` |
| `skipUnsupportedColumns` | true | 跳过空间类型等目标库不支持、也搬不了的列 |

---

## 6. 各库连接要点

| 目标 | 默认端口 | 驱动 | 备注 |
|---|---|---|---|
| 达梦 DM8 | 5236 | `DmProvider.dll` | `database` 填库名，`schema` 填模式名（通常与用户同名） |
| 金仓 KingbaseES | 54321 | `Kdbndp.dll` | 走 PG 协议；连接串是 `Host/Port/Database/Username/Password` 风格 |
| openGauss / 瀚高 | 5432 | Npgsql（内置） | 与 PG 基本一致 |
| OceanBase(MySQL) | 2881 | MySqlConnector（内置） | kind 用 `oceanbase` |
| TiDB | 4000 | MySqlConnector（内置） | kind 用 `tidb` |
| Oracle 11g/12c+ | 1521 | Oracle 托管驱动（内置） | `database` 填 service name；11g 用 `--identity-mode sequence` |
| SQL Server | 1433 | Microsoft.Data.SqlClient（内置） | 也可 `Integrated Security`，`user` 留空即可 |
| SQLite | — | 内置 | `database` 直接写文件路径 |

厂商驱动放的两种方式：

```
DbConvert.Cli.exe
DmProvider.dll          ← 与 exe 同目录
providers\Kdbndp.dll    ← 或子目录
```

找不到驱动时命令行会直接提示“请把驱动 DLL 放到程序目录或 providers 子目录”，不会抛一堆栈。

---

## 7. 迁移语义里最容易踩的坑

- **VARCHAR 长度**：MySQL 的 `varchar(50)` 是 50 字符，Oracle/达梦默认按字节算（utf8 一个汉字 3 字节）。默认 `varcharLengthMode=auto` 会按目标库字符语义换算，必要时用 `bytesPerChar` 调整。
- **空串 vs NULL**：Oracle/达梦里 `''` 就是 NULL。校验时对这两类目标库会自动把空串视作 NULL，避免“看着不一样其实一样”的假报警。
- **标识符大小写**：`identifierCase=auto` 让达梦/金仓下的表名按目标库习惯大写，否则加引号建出来的小写表，应用不带引号查询会找不到。
- **主键类型**：主键列如果源库是 TEXT/CLOB，会被自动收敛成 `VARCHAR(255)` / `VARCHAR2(255)` / `NVARCHAR(255)`，否则目标库不让做主键。
- **自增**：MySQL `AUTO_INCREMENT` → 达梦 `IDENTITY(1,1)` / PG `GENERATED ... AS IDENTITY` / Oracle 12c+ identity / Oracle 11g 序列+触发器（自动判断）。
- **索引名**：`PRIMARY`、`sqlite_autoindex_*` 这类不合法的名字会改写成 `PK_表名` / `IX_表名`。
- **断点续传**：只有单列主键才支持；续传前会清掉目标表里“断点之后但已写进去”的行，保证不重不漏。实测中断后续传 50000 行数据完整、校验和一致。

---

## 8. 校验与产物

每次 `plan` / `migrate` 会在 `outDir` 里生成：

- `schema_<时间>.sql`：目标库脚本（含索引、注释、序列/触发器、过程/函数）
- `mapping_<时间>.csv`：每列的类型映射、长度、可空、警告
- `report_<时间>.md`：表级结果（`verified` / `ok` / `failed` / `skipped`）、行数、错误、警告
- `migration-state.json`：断点状态

校验方式：行数比对 + 逐行归一化（类型、空串、日期格式统一后）算 FNV-1a 校验和求和，两边一致才算 `verified`；不一致会自动定位第一处差异。所以“搬完显示成功”不是空话，是真比对过。

---

## 9. 性能参考（本机实测，5 万行 6 列，含校验）

| 场景 | 耗时 |
|---|---|
| MySQL → SQLite | 约 11 秒（写库 9.9s，校验 2s） |
| SQLite → MySQL | 约 4 秒（写库 1.8s） |
| SQLite → SQLite（含建表） | 约 9 秒 |

几点提速建议：

- 大表用 `createIndexesAfterLoad=true`（默认已开），先灌数再建索引。
- 目标 SQLite 已自动开 WAL + `synchronous=NORMAL`，别再手工降级。
- `batchSize` 2000 起步；Oracle/达梦逐行绑定，批次大一点更划算。
- 千万级表建议按 `where` 分片跑，或先 `schema` 再分表 `data`。

---

## 10. 对象迁移范围与已知限制

### 10.1 会尝试一比一复现的对象

| 对象 | 处理方式 |
|---|---|
| 表 | 列类型/长度/精度、非空、主键、索引、表与列注释、自增 |
| 默认值 | 常量、`CURRENT_TIMESTAMP`、`SYSDATE` 等直接生成 `DEFAULT`；表达式型默认值按目标语法改写，拿不准的记“需人工” |
| 生成列 / 计算列 | MySQL `VIRTUAL/STORED`、PostgreSQL `STORED`、SQLite `STORED`、SQL Server 计算列均读表达式并改写；目标语法差异记“需人工” |
| CHECK 约束 | 读表达式并做函数/列名改写后内联进建表语句 |
| 外键 | 读列、引用表/列、`ON DELETE/UPDATE` 动作，所有表建完后统一 `ALTER TABLE ... ADD CONSTRAINT` |
| 视图 | 读定义、剥掉 `CREATE VIEW` 头、改写函数与表名，按视图间引用关系排序后创建；MySQL/PG/Oracle/达梦用 `CREATE OR REPLACE`，SQLite 用 `IF NOT EXISTS`，SQL Server 用 `CREATE OR ALTER` |
| 函数 / 存储过程 | 抽取完整 DDL（MySQL `SHOW CREATE`、PG `pg_get_functiondef`、SQL Server `sys.sql_modules`）；**源/目标同为一种数据库且拿到完整 CREATE 时，直接写入目标库并执行成功校验**；语法家族不同或只能拿到正文（Oracle/达梦 `ALL_SOURCE`）时生成 `objects_manual_*.sql` |
| 触发器 | 抽取 `BEFORE/AFTER`、事件、表、完整 `CREATE TRIGGER`；同类型库在**数据搬完后直接创建**，避免搬数期间触发业务规则；跨类型库生成草稿 |

函数改写覆盖：`IFNULL→NVL/ISNULL/COALESCE`、`IF()→CASE WHEN`、`NOW/CURDATE`、`DATE_FORMAT→TO_CHAR`（格式串 `%Y→YYYY`）或 SQLite `strftime`、`STR_TO_DATE→TO_DATE`、`GROUP_CONCAT→LISTAGG/STRING_AGG`、`CONCAT→||`、`CHAR_LENGTH→LENGTH`、`TRUNCATE→TRUNC`、`UUID→SYS_GUID`、`CAST` 类型映射等；`DATE_ADD/DATEDIFF/JSON_*/LOCATE/FIND_IN_SET` 等没有稳定等价写法的函数会原样保留并标“需人工”。

每次 `plan` / `migrate` 都会在输出目录生成：

- `schema_*.sql`：迁移时下发给目标库的建表 + 外键 + 视图 + 过程/函数/触发器脚本（审计副本，不是让你再手工执行）
- `issues_*.csv`：对象级问题清单，级别为 **阻断 / 需人工 / 已改写 / 已跳过**，带原文、改写后、建议
- `objects_manual_*.sql`：**只有无法直接创建**的过程/函数/触发器才生成；全部直接成功时不会产生这个文件
- `report_*.md`：行数、校验结果、问题统计

默认“非 strict”：某个视图/外键创建失败只记阻断并继续迁其它对象；配置 `options.strictObjects=true` 才会在第一个对象失败时中止。`options.directObjects=false` 可关闭过程/函数/触发器的直接创建，退回全部生成草稿。

### 10.2 仍然存在的限制

- 并行度目前固定为 1（`parallel>1` 只给警告）。
- 表达式索引、部分索引、空间类型（geometry/geography）会跳过并记入警告。
- 过程/函数/触发器：同类型库且拿到完整 DDL 时直接创建；跨类型库（例如 MySQL→达梦）的 `DECLARE`、游标、异常处理、包（package）、`NEW/OLD` 语义差异太大，仍会生成 `objects_manual_*.sql` 并登记“需人工”，不会假装已自动转换。
- 生成列、虚拟列、表达式默认值在达梦/金仓上的具体语法随版本差异较大，脚本里已标注，需现场验证一次。
- 触发器按“先灌数、后建触发器”处理；如果业务要求搬数期间也触发，需要自行调整执行顺序。
- 达梦 / 金仓 / openGauss / Oracle 的真实联调需要现场库和驱动，本机只验证到 DDL 生成这一层；MySQL / SQLite 是端到端跑通并校验过的（含视图、外键、CHECK、默认值、生成列）。
- SQL Server 只支持 SQL 认证（集成认证在部分环境会报 18452）。

---

## 11. 构建与发布

```powershell
cd DBConvertDB
dotnet build DBConvertDB.sln -c Release

# 发布成一个可直接拷贝给实施的目录
.\publish.ps1            # 产物在 dist\
```

`dist\` 里会有 `DbConvert.Cli.exe`、`DbConvert.Gui.exe`、驱动 DLL、`providers\` 目录和样例配置。

构建目标是 `net48`；运行程序只需要 .NET Framework 4.8，不需要安装 .NET 5 运行时。CI 使用 .NET SDK 8.0 编译。

发布说明见 [docs/RELEASE_NOTES_v1.0.0.md](docs/RELEASE_NOTES_v1.0.0.md)。

---

## 12. 开源协议

本项目使用 **MIT License**，详见 [LICENSE](LICENSE)。可以自由使用、修改、分发和商业使用；请保留版权与许可声明。

第三方 NuGet 依赖（MySqlConnector、Npgsql、Microsoft.Data.SqlClient、Microsoft.Data.Sqlite、Oracle.ManagedDataAccess）遵循各自的许可证；达梦 `DmProvider.dll`、金仓 `Kdbndp.dll` 等厂商驱动不随本项目分发，需要使用者自行获取并按厂商授权使用。

## 13. 贡献

欢迎提交 Issue 和 Pull Request。提交前请先阅读 [CONTRIBUTING.md](CONTRIBUTING.md)：

1. Fork 本仓库并新建分支。
2. 运行 `dotnet build DBConvertDB.sln -c Release` 确认编译通过。
3. 涉及数据库方言的改动，请尽量附上源库/目标库版本与复现 SQL。
4. 不要提交真实连接密码、生产库导出文件、厂商授权驱动。

```powershell
git checkout -b feature/your-change
git add .
git commit -m "feat: ..."
git push origin feature/your-change
```

## English

DBConvertDB is a .NET Framework 4.8 database migration tool for MySQL, PostgreSQL, Oracle, SQL Server, SQLite, Dameng DM, KingbaseES, openGauss, OceanBase, TiDB, GBase 8a and HighGo. It migrates table schemas, data, views, routines and triggers, with row-count and checksum verification. It supports both direct migration and SQL-script-only mode, and ships with a WPF GUI and a CLI.

Typical use cases include MySQL to Dameng/KingbaseES, Oracle to KingbaseES/openGauss, SQL Server to PostgreSQL/MySQL, and SQLite offline database migration.




