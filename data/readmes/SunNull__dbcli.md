# dbcli — 多数据库 SQL CLI

多数据库命令行工具，支持 **Dameng、MySQL、PostgreSQL、SQL Server、SQLite**。UTF-8 输入输出，专为 AI Agent 调用设计。

## 快速开始

### 1. 构建

需要 .NET 11 SDK。

```bash
dotnet publish damengcli.csproj -c Release -r win-x64 -p:PublishSingleFile=true --self-contained true
```

产物在 `bin/Release/net11.0/win-x64/publish/` 目录下，单文件 `dbcli.exe`。

### 2. 配置

在 `dbcli.exe` 同目录下创建 `config.json`：

```json
{
  "Default": "dameng",
  "Connections": {
    "dameng": {
      "Type": "Dameng",
      "Server": "127.0.0.1",
      "Port": 5234,
      "User": "SYSDBA",
      "Password": "your_password",
      "Database": "YOUR_SCHEMA"
    },
    "sqlserver": {
      "Type": "SqlServer",
      "Server": "127.0.0.1",
      "Port": 1433,
      "User": "sa",
      "Password": "your_password",
      "Database": "your_database"
    },
    "sqlite_local": {
      "Type": "Sqlite",
      "Server": "",
      "Port": 0,
      "User": "",
      "Password": "",
      "Database": "C:/data/local.db"
    }
  }
}
```

- `Default`：不传 `--conn` 时使用的默认连接名
- `Type`：`Dameng` / `MySql` / `PostgreSQL` / `SqlServer` / `Sqlite`
- 所有连接字段统一，不用的留空

### 3. 使用

```bash
# 用 Default 连接
dbcli -e "SELECT * FROM users;"

# 用命名连接
dbcli -e "SELECT 1;" --conn sqlserver

# 执行 SQL 文件
dbcli -f create_tables.sql --conn dameng

# 管道输入
echo "SELECT COUNT(*) FROM orders;" | dbcli

# 命令行指定连接（不需要 config.json）
dbcli -e "SELECT 1;" --type MySql --server 127.0.0.1 --port 3306 --user root --password pwd --database testdb

# JSON 输出
dbcli -e "SELECT * FROM users LIMIT 10;" --format json

# SQLite（无需服务器）
dbcli -e "CREATE TABLE t (id INT, name TEXT);" --type Sqlite --database "C:/data/test.db"
```

## 命令行参数

| 参数 | 说明 |
|------|------|
| `-e`, `--execute` | 内联 SQL 语句 |
| `-f`, `--file` | SQL 文件路径 |
| （无参数） | 从 stdin 读取 |
| `--conn` | 命名连接（来自 config.json） |
| `--type` | 数据库类型覆盖 |
| `--server` | 服务器地址覆盖 |
| `--port` | 端口覆盖 |
| `--user` | 用户名覆盖 |
| `--password` | 密码覆盖 |
| `--database` | 数据库名/Schema 覆盖 |
| `--format` | 输出格式：`text`（默认）或 `json` |
| `-h`, `--help` | 显示帮助 |

优先级：命令行参数 > `--conn` 命名连接 > `Default` 默认连接

输入来源互斥：`-e` > `-f` > stdin

## 输出格式

### Text（默认）

```
SELECT: Id    Code     Name
        1     P01      测试数据
        2     P02      示例数据
---
2 rows selected
```

DML：`INSERT 3 rows affected`
DDL：`CREATE TABLE users OK`
汇总：`3 statements executed, 3 succeeded`

### JSON（--format json）

查询：`{"type":"query","columns":["id","name"],"rows":[{"id":1,"name":"张三"}],"rowCount":1}`
DML：`{"type":"dml","action":"INSERT","rowsAffected":3}`
DDL：`{"type":"ddl","statement":"CREATE TABLE users"}`
错误：`{"type":"error","message":"违反唯一约束"}`

每条语句输出一个 JSON 对象，无汇总行。

## 执行模型

所有 SQL 在单个事务中执行：

```
BEGIN TRANSACTION
  → 语句 1
  → 语句 2
  → ...
COMMIT（全部成功） / ROLLBACK（任一失败）
```

## 退出码

| 退出码 | 含义 |
|--------|------|
| 0 | 执行成功 |
| 1 | SQL 执行失败（已回滚） |
| 2 | 参数错误 |
| 3 | 连接失败 |

## AI 调用示例

```bash
# 查看表结构
dbcli -e "SELECT COLUMN_NAME, DATA_TYPE FROM ALL_TAB_COLUMNS WHERE TABLE_NAME='users';"

# 插入中文数据
dbcli -e "INSERT INTO users (id, name) VALUES (1, '张三');"

# JSON 格式便于程序解析
dbcli -e "SELECT COUNT(*) AS total FROM orders WHERE status='pending';" --format json

# 批量建表
dbcli -f create_tables.sql --conn dameng

# 事务回滚（第二条失败，第一条自动撤销）
dbcli -e "INSERT INTO t VALUES (1); INVALID_SQL;"

# SQLite 本地测试
dbcli -e "CREATE TABLE test (id INT, name TEXT);" --type Sqlite --database "test.db"
dbcli -e "INSERT INTO test VALUES (1, 'hello'); SELECT * FROM test;" --type Sqlite --database "test.db"
```

## 各数据库注意事项

| 数据库 | 要点 |
|--------|------|
| Dameng | `Database` 映射为 Schema；用 `TOP N` 限制行数 |
| SQL Server | 中文字符串用 `N'...'` 前缀；用 `TOP N` 限制行数 |
| MySQL | 用 `LIMIT N` 限制行数；反引号引用标识符 |
| PostgreSQL | 用 `LIMIT N` 限制行数；双引号引用标识符 |
| SQLite | 只需 `Database`（文件路径），其余留空；无需服务器，自动创建文件 |

## 运行测试

```bash
dotnet test
```

## 项目结构

```
dbcli/
├── damengcli.csproj        # 项目文件 (.NET 11)
├── Program.cs              # 入口 + 参数解析 + 配置加载
├── ConnectionConfig.cs     # 多连接配置模型
├── Executor.cs             # SqlSugar 执行引擎 + 事务管理
├── OutputFormatter.cs      # Text/JSON 双格式输出
├── SqlSplitter.cs          # SQL 语句分割（状态机）
├── SqlClassifier.cs        # 语句类型识别
├── config.json             # 数据库连接配置（不入版本控制）
├── Tests/                  # 单元测试 (MSTest, 73 个用例)
│   ├── ConnectionConfigTests.cs
│   ├── OutputFormatterTests.cs
│   ├── SqlClassifierTests.cs
│   ├── SqlSplitterTests.cs
│   └── IntegrationTests.cs
├── skill/dbcli/            # 独立 Skill 包（可直接复制到 AI Agent）
│   ├── SKILL.md
│   ├── scripts/dbcli.exe
│   ├── assets/config-template.json
│   └── references/database-types.md
└── docs/                   # 设计文档
```

## 技术栈

- .NET 11
- SqlSugarCore + SqlSugarCore.Dm
- MSTest（73 个单元测试用例）
