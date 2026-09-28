# SQL Client 使用说明

交互式终端 SQL 客户端，用于在 Linux 服务器上快速查询 Oracle、达梦(DM) 和 KingbaseES 数据库。

**核心特性：**
- 交互式 REPL，支持多行 SQL、自动补全历史
- 多数据库连接管理，一键切换
- 表导出为 SQL（DDL + INSERT）或 CSV 格式
- 批量执行 SQL 脚本文件（适合初始化、数据迁移）
- 自动识别数据库类型，零配置直连

---

## 目录

- [环境要求](#环境要求)
- [快速开始](#快速开始)
- [配置文件](#配置文件)
- [启动方式](#启动方式)
- [交互式使用](#交互式使用)
- [批量执行 SQL 脚本](#批量执行-sql-脚本)
- [表导出](#表导出)
- [结果展示特性](#结果展示特性)
- [JDBC URL 格式参考](#jdbc-url-格式参考)
- [从源码构建](#从源码构建)
- [注意事项](#注意事项)

---

## 环境要求

- JDK 8 或更高版本
- 支持 Oracle、达梦(DM) 和 KingbaseES 数据库

## 快速开始

### 1. 构建项目

```bash
mvn clean package
```

构建产物位于 `target/sql-client-1.0.0.jar`（约 7.4MB 的 Fat JAR，包含所有依赖）。

### 2. 创建配置文件

将 `config-example.yaml` 复制为 `config.yaml`，填入实际的数据库连接信息：

```yaml
connections:
  - name: prod-oracle
    type: ORACLE
    url: jdbc:oracle:thin:@192.168.1.100:1521:orcl
    username: scott
    password: tiger

  - name: dev-dm
    type: DM
    url: jdbc:dm://192.168.1.200:5236
    username: SYSDBA
    password: SYSDBA

defaultConnection: dev-dm
```

### 3. 启动客户端

```bash
# 使用配置文件启动
java -jar sql-client.jar -c config.yaml

# 使用命令行参数直连（无需配置文件）
java -jar sql-client.jar -url jdbc:oracle:thin:@host:1521:orcl -user scott -pass tiger

# 批量执行 SQL 脚本
java -jar sql-client.jar -c config.yaml -f init.sql
```

---

## 配置文件

配置文件使用 YAML 格式，支持多个数据库连接：

```yaml
connections:
  - name: prod-oracle
    type: ORACLE
    url: jdbc:oracle:thin:@192.168.1.100:1521:orcl
    username: scott
    password: tiger

  - name: dev-dm
    type: DM
    url: jdbc:dm://192.168.1.200:5236
    username: SYSDBA
    password: SYSDBA

  - name: test-kb
    type: KINGBASE8
    url: jdbc:kingbase8://192.168.1.300:54321/mydb
    username: SYSTEM
    password: password

defaultConnection: dev-dm
```

**字段说明：**

| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | 是 | 连接名称，用于 `\switch` 切换时的标识 |
| `type` | 是 | 数据库类型，可选值：`ORACLE`、`DM`、`KINGBASE8` |
| `url` | 是 | JDBC 连接地址 |
| `username` | 是 | 数据库用户名 |
| `password` | 是 | 数据库密码 |
| `defaultConnection` | 否 | 启动时自动连接的默认连接名称（不填则连接第一个） |

> 如果当前目录下存在 `config.yaml` 文件，即使不指定 `-c` 参数也会自动加载。

---

## 启动方式

### 交互模式

```bash
# 使用配置文件启动（自动连接 defaultConnection 指定的数据库）
java -jar sql-client.jar -c config.yaml

# 使用命令行参数直连（无需配置文件）
java -jar sql-client.jar -url jdbc:oracle:thin:@host:1521:orcl -user scott -pass tiger
java -jar sql-client.jar -url jdbc:dm://host:5236 -user SYSDBA -pass SYSDBA -type DM
java -jar sql-client.jar -url jdbc:kingbase8://host:54321/db -user SYSTEM -pass password -type KINGBASE8

# 指定配置文件 + 命令行覆盖连接
java -jar sql-client.jar -c config.yaml -url jdbc:dm://another-host:5236 -user admin -pass admin123
```

### 批量执行模式

使用 `-f` 参数指定 SQL 脚本文件，执行完毕后自动退出：

```bash
java -jar sql-client.jar -c config.yaml -f init.sql
java -jar sql-client.jar -url jdbc:oracle:thin:@host:1521:orcl -user scott -pass tiger -f migrate.sql
```

### 命令行参数

| 参数 | 说明 |
|------|------|
| `-c <file>` | 配置文件路径（默认：当前目录 `config.yaml`） |
| `-f <file>` | 执行 SQL 脚本文件后退出（批量模式） |
| `-url <url>` | JDBC 连接地址（自动识别数据库类型） |
| `-user <user>` | 数据库用户名 |
| `-pass <pass>` | 数据库密码 |
| `-type <type>` | 数据库类型：`ORACLE`、`DM` 或 `KINGBASE8`（使用 `-url` 时可省略，自动识别） |

**数据库类型自动识别规则：**

| URL 前缀 | 自动识别类型 |
|----------|-------------|
| `jdbc:oracle:` | ORACLE |
| `jdbc:dm:` | DM |
| `jdbc:kingbase8:` | KINGBASE8 |

---

## 交互式使用

### SQL 查询

输入 SQL 语句，以**分号(`;`)**结尾执行：

```
[dev-dm]> SELECT * FROM SYS_OBJECTS WHERE OBJECT_TYPE = 'TABLE' AND ROWNUM <= 5;

+--------+-------------+-------------+
| ID     | NAME        | OBJECT_TYPE |
+--------+-------------+-------------+
| 100    | SYS_TABLES  | TABLE       |
| 101    | SYS_VIEWS   | TABLE       |
| 102    | USER_INFO   | TABLE       |
| 103    | ORDER_LOG   | TABLE       |
| 104    | CONFIG_DATA | TABLE       |
+--------+-------------+-------------+
5 row(s) in set (23 ms)
```

### 多行输入

SQL 可以跨多行输入，以分号结尾时执行。出现 `->` 提示符表示正在输入多行语句：

```
[dev-dm]> SELECT ID, NAME
  -> FROM USER_INFO
  -> WHERE STATUS = 'ACTIVE'
  -> ORDER BY ID DESC
  -> LIMIT 10;
```

按 `Ctrl+C` 可取消当前正在输入的 SQL。

### 支持的 SQL 类型

| 类型 | 关键字 | 执行方式 |
|------|--------|---------|
| 查询 | `SELECT`、`WITH`、`SHOW`、`DESC`、`EXPLAIN` | 返回结果集表格 |
| 更新 | `INSERT`、`UPDATE`、`DELETE` | 返回影响行数 |
| DDL | `CREATE`、`ALTER`、`DROP`、`TRUNCATE` | 返回影响行数 |

### 内置命令

所有命令以 `\` 开头（也支持 `/` 和全角 `\` 作为前缀）：

| 命令 | 说明 |
|------|------|
| `\help` | 显示帮助信息 |
| `\connections` | 列出所有已配置的数据库连接（`*` 标记当前连接） |
| `\switch <name>` | 切换到指定名称的数据库连接 |
| `\current` | 显示当前连接详细信息（状态、Catalog、Schema） |
| `\reconnect` | 重新连接当前数据库 |
| `\export <table> [file]` | 导出表的 DDL + 数据到 SQL 文件 |
| `\exportcsv <table> [file]` | 导出表数据到 CSV 文件 |
| `\quit` 或 `\exit` | 退出客户端 |

#### 连接管理

```
[dev-dm]> \connections
 * dev-dm (DM) -> jdbc:dm://192.168.1.200:5236
   prod-oracle (ORACLE) -> jdbc:oracle:thin:@192.168.1.100:1521:orcl

[dev-dm]> \switch prod-oracle
Connecting to prod-oracle...
Connected to prod-oracle (ORACLE) -> jdbc:oracle:thin:@192.168.1.100:1521:orcl successfully.

[prod-oracle]> \current
Current connection: prod-oracle (ORACLE) -> jdbc:oracle:thin:@192.168.1.100:1521:orcl
Status: connected
Catalog: ORCL
Schema: SCOTT

[prod-oracle]> \reconnect
Connecting to prod-oracle...
Connected to prod-oracle (ORACLE) -> jdbc:oracle:thin:@192.168.1.100:1521:orcl successfully.
```

#### 全角字符兼容

在中文输入法下，`\` 可能被输入为全角字符 `＼`（U+FF3C）或 `¥`（U+00A5/U+FFE5），客户端会自动识别并转换为标准 `\` 前缀。同时 `/` 也可作为命令前缀使用：

```
# 以下写法均等价
\help
/help
＼help       # 全角反斜杠
¥help        # 日元符号
￥help       # 人民币符号
```

### 历史记录

客户端自动保存输入历史到 `~/.sqlclient-history`，支持：

- 上/下方向键浏览历史 SQL
- 跨会话持久化（重启后历史仍在）

---

## 批量执行 SQL 脚本

使用 `-f` 参数可以非交互式执行 SQL 脚本文件，适用于数据库初始化、数据迁移等场景：

```bash
java -jar sql-client.jar -c config.yaml -f init.sql
```

**执行输出示例：**

```
Connected to dev-dm (DM) -> jdbc:dm://192.168.1.200:5236.
Executing 3 statement(s) from init.sql

-- Statement 1 --
CREATE TABLE USER_INFO (ID NUMBER PRIMARY KEY, NAME VARCHAR2(100))

0 row(s) affected.

-- Statement 2 --
INSERT INTO USER_INFO VALUES (1, 'Alice')

1 row(s) affected.

-- Statement 3 --
INSERT INTO USER_INFO VALUES (2, 'Bob')

1 row(s) affected.

Done. 3 succeeded, 0 failed.
```

**脚本文件格式：**

- SQL 语句以分号(`;`)分隔
- 支持 `--` 单行注释
- 支持 `/* ... */` 多行注释
- 正确处理字符串内的分号（不会误拆）
- 正确处理 `''` 转义的单引号
- 以 UTF-8 编码读取

**示例脚本：**

```sql
-- 创建用户表
CREATE TABLE USER_INFO (
    ID NUMBER PRIMARY KEY,
    NAME VARCHAR2(100) NOT NULL,
    EMAIL VARCHAR2(200)
);

/* 插入初始数据 */
INSERT INTO USER_INFO VALUES (1, 'Alice', 'alice@example.com');
INSERT INTO USER_INFO VALUES (2, 'Bob', NULL);

-- 包含分号的字符串不会被误拆
INSERT INTO USER_INFO VALUES (3, 'Test; Name', 'test@example.com');
```

**退出码：**

| 退出码 | 说明 |
|--------|------|
| `0` | 所有语句执行成功 |
| `1` | 文件不存在、连接失败或某条语句执行失败 |

> 遇到错误时立即停止执行后续语句。

---

## 表导出

### 导出为 SQL 文件（`\export`）

将表结构和数据导出为可重执行的 SQL 文件：

```
# 导出表 DDL + 数据，默认保存为 <表名>_backup.sql
[dev-dm]> \export USER_INFO
Exporting table: USER_INFO
Output file: user_info_backup.sql
  Exported 100 rows...
  Exported 200 rows...
Export completed successfully.

# 指定 schema 和输出文件路径
[dev-dm]> \export SCOTT.ORDERS /tmp/orders_backup.sql
Exporting table: SCOTT.ORDERS
Output file: /tmp/orders_backup.sql
Export completed successfully.
```

**导出文件内容示例：**

```sql
-- Export of table: USER_INFO
-- Schema: SCOTT
-- Database: ORACLE
-- Date: 2026-05-21 14:30:00

CREATE TABLE "USER_INFO" (
  "ID" NUMBER(10,0) NOT NULL,
  "NAME" VARCHAR2(100),
  "EMAIL" VARCHAR2(200)
);

-- Data for table "USER_INFO"

INSERT INTO "USER_INFO" ("ID", "NAME", "EMAIL") VALUES (1, 'Alice', 'alice@example.com');
INSERT INTO "USER_INFO" ("ID", "NAME", "EMAIL") VALUES (2, 'Bob', NULL);

-- Export complete: 2 rows exported in 0.15 sec
```

**导出特性：**

- **DDL 提取** — Oracle/DM 使用 `DBMS_METADATA.GET_DDL` 获取精确建表语句；失败时自动回退到 JDBC 元数据；KingBase8 使用 JDBC 元数据
- **INSERT 生成** — 逐行流式导出，支持大表导出不占满内存
- **日期格式** — 使用 ANSI 标准格式（`DATE '2026-01-15'`、`TIMESTAMP '2026-01-15 10:30:00'`）
- **类型处理** — 自动处理 NULL 值、单引号转义、BLOB 跳过（添加注释）、CLOB 内容提取
- **进度反馈** — 每导出 100 行显示一次进度
- **可重执行** — 导出的 SQL 文件可直接用于数据恢复

### 导出为 CSV 文件（`\exportcsv`）

将表数据导出为标准 CSV 格式：

```
# 导出为 CSV，默认保存为 <表名>.csv
[dev-dm]> \exportcsv USER_INFO
Exporting table to CSV: USER_INFO
Output file: user_info.csv
  Exported 100 rows...
Export completed: 100 rows written to user_info.csv

# 指定 schema 和输出路径
[dev-dm]> \exportcsv SCOTT.ORDERS /tmp/orders.csv
```

**CSV 输出示例：**

```csv
ID,NAME,EMAIL
1,Alice,alice@example.com
2,Bob,
3,"Test, Name",test@example.com
```

**CSV 格式规范：**

- 首行为列名
- 逗号分隔，UTF-8 编码
- 包含逗号、双引号、换行的字段自动用双引号包裹
- NULL 值输出为空字符串
- BLOB 类型输出为空
- 日期格式：`yyyy-MM-dd`，时间戳格式：`yyyy-MM-dd HH:mm:ss`

---

## 结果展示特性

| 特性 | 说明 |
|------|------|
| 自动对齐 | 列宽根据内容和列名自动计算 |
| NULL 处理 | 空值显示为 `NULL` |
| 超长截断 | 超过 50 字符的字段自动截断，末尾显示 `...` |
| 换行合并 | 包含换行的字段内容合并为单行显示 |
| 行数统计 | 底部显示返回行数和执行耗时 |
| 空结果集 | 无数据时显示 `Empty set` |
| 行数限制 | 单次查询最多返回 500 行，避免终端卡顿 |

---

## JDBC URL 格式参考

**Oracle：**

```
# 传统格式（SID）
jdbc:oracle:thin:@<host>:<port>:<SID>

# 服务名格式
jdbc:oracle:thin:@//<host>:<port>/<service_name>

# 示例
jdbc:oracle:thin:@192.168.1.100:1521:orcl
jdbc:oracle:thin:@//192.168.1.100:1521/orclpdb
```

**达梦(DM)：**

```
jdbc:dm://<host>:<port>

# 指定 schema
jdbc:dm://<host>:<port>?schema=<schema_name>

# 示例
jdbc:dm://192.168.1.200:5236
jdbc:dm://192.168.1.200:5236?schema=TEST_SCHEMA
```

**KingbaseES：**

```
jdbc:kingbase8://<host>:<port>/<database>

# 示例
jdbc:kingbase8://192.168.1.300:54321/mydb
```

---

## 从源码构建

```bash
# 克隆项目后执行
mvn clean package

# 运行测试
mvn test

# 运行单个测试类
mvn test -Dtest=ConfigLoaderTest

# 仅编译不打包
mvn compile
```

构建要求：Maven 3.6+、JDK 8+。

---

## 注意事项

1. **密码安全** — 配置文件中密码为明文存储，请注意文件权限控制（`chmod 600 config.yaml`）
2. **行数限制** — 单次查询最多返回 500 行（`MAX_ROW_DISPLAY`），避免大量数据导致终端卡顿
3. **连接超时** — 长时间空闲可能导致数据库连接超时，使用 `\reconnect` 重新连接
4. **自动提交** — 每条 SQL 独立执行并自动提交，不支持事务管理
5. **批量执行** — `-f` 模式遇到错误会立即停止，建议执行前先验证脚本
6. **导出大表** — 导出采用流式写入，每 100 行刷新一次，可安全导出大表
