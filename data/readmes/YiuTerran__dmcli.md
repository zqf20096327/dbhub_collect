# dmcli

`dmcli` 是一个使用 Go 编写的 DM8 交互式命令行客户端，提供多行 SQL 编辑、DMSQL 程序块、事务管理、查询取消、历史搜索、基础智能补全和流式结果展示。

当前版本固定使用 DM8 Go 驱动 `8.1.5.60`，不支持运行时切换驱动或连接其他数据库产品。

## 功能

- YAML 多连接 profile
- 命令行参数和环境变量覆盖
- 密码无回显输入
- 单行及多行 SQL
- DMSQL 匿名块、过程、函数、触发器和包
- SQL 关键字高亮
- 模式、表、视图、字段和单层别名补全
- 固定物理连接与显式事务
- `Ctrl+C` 取消查询
- 表格和垂直结果展示
- CLOB、BLOB 有界预览
- 查询历史和 `Ctrl+R` 搜索
- SQL 文件执行
- Linux、Windows、macOS 构建

## 环境要求

- Go 1.25 或更高版本
- 可访问的 DM8 数据库
- 构建源码时需要能够下载 Go 模块依赖

## 构建

克隆仓库后执行：

```bash
go build -o bin/dmcli ./cmd/dmcli
```

或使用 Makefile：

```bash
make build
```

查看版本：

```bash
./bin/dmcli version
```

示例输出：

```text
dmcli dev
commit: unknown
built: unknown
go: go1.26.5
driver: DM8 Go 8.1.5.60
platform: darwin/arm64
```

交叉构建所有目标平台：

```bash
make cross-build
```

产物生成在 `dist/` 目录。

## 快速开始

### 使用命令行参数连接

通过环境变量提供密码：

```bash
export DMCLI_PASSWORD='your-password'
./bin/dmcli --host 127.0.0.1 --port 5236 --user SYSDBA --schema SYSDBA
```

如果没有设置密码环境变量，交互模式会安全提示输入密码：

```text
Password for SYSDBA:
```

密码不会显示在终端中。

不建议把密码直接写在 Shell 命令或脚本里。`dmcli` 不提供 `--password` 参数。

### 执行一条 SQL

```bash
export DMCLI_PASSWORD='your-password'

./bin/dmcli \
  --host 127.0.0.1 \
  --port 5236 \
  --user SYSDBA \
  --execute 'SELECT SYSDATE;'
```

也可以使用短参数：

```bash
./bin/dmcli --user SYSDBA -e 'SELECT * FROM V$INSTANCE;'
```

非交互模式不会提示输入密码。必须通过 `DMCLI_PASSWORD`、profile 的 `password_env` 或 `password` 提供密码。

### 执行 SQL 文件

```bash
./bin/dmcli --user SYSDBA --file ./script.sql
```

短参数形式：

```bash
./bin/dmcli --user SYSDBA -f ./script.sql
```

SQL 文件必须使用 UTF-8 编码，可以包含 UTF-8 BOM。

### 导出查询结果

dmcli 可以将 `SELECT` 或查询型 `WITH` 的完整结果集导出为 CSV：

```sql
EXPORT CSV TO './users.csv' AS
SELECT ID, NAME, CREATED_AT
FROM APP.USERS
WHERE STATUS = 1;
```

也可以生成逐行 `INSERT` SQL。目标表必须明确指定，查询结果列名将作为 INSERT 字段名：

```sql
EXPORT INSERT INTO APP.USERS TO './users.sql' AS
WITH T AS (
    SELECT ID, NAME, CREATED_AT
    FROM APP.USERS
    WHERE STATUS = 1
)
SELECT ID, NAME, CREATED_AT FROM T;
```

该语法可在交互模式、`--execute` 和 SQL 文件中使用：

```bash
./bin/dmcli local -e "EXPORT CSV TO './users.csv' AS SELECT * FROM APP.USERS;"
```

导出规则：

- CSV 使用 UTF-8 和 RFC 4180 格式，第一行为列名；NULL 写为 `\N`，空字符串仍为空字符串，二进制写为十六进制。
- INSERT 导出会引用 schema、表名和列名，并转义字符串中的单引号；查询列名为空或重复时拒绝导出，应在 SELECT 中使用 `AS` 指定唯一别名。
- 导出逐行读取，不经过终端表格、分页器、`execution.max_rows` 或 `output.max_lob_preview`，不会因终端显示限制而截断。
- `execution.timeout`、`Ctrl+C` 和当前事务仍然有效；事务内导出可以读取当前事务尚未提交的数据。
- 默认拒绝覆盖已有文件。导出先写入同目录权限为 `0600` 的临时文件，全部成功后才原子提交；失败或取消会清理临时文件。
- 相对路径以 dmcli 当前工作目录为基准，支持路径开头的 `~/`。
- INSERT 文件默认不附加 `COMMIT`，导入时由使用者决定事务边界。
- CSV 支持完整 CLOB/BLOB；INSERT 对常规标量和不超过配置上限的 LOB 生成 DM8 字面量。超过 `export.max_lob_bytes` 时明确失败，不会静默截断。

## 配置文件

### 默认位置

无参数启动时按以下顺序查找默认配置文件，使用第一个存在的普通文件：

1. `~/.dmcli.yml`
2. `~/.dmcli.yaml`

同时存在 `.yml` 和 `.yaml` 时优先使用 `~/.dmcli.yml`。

也可以显式指定配置文件：

```bash
./bin/dmcli --config ./dmcli.yaml local
```

或者使用环境变量：

```bash
export DMCLI_CONFIG=/path/to/dmcli.yaml
./bin/dmcli local
```

### 配置示例

```yaml
version: 1
default_profile: local

profiles:
  local:
    host: 127.0.0.1
    port: 5236
    user: SYSDBA
    schema: SYSDBA
    password_env: DMCLI_LOCAL_PASSWORD
    connect_timeout: 5s
    properties:
      socketTimeout: "60"
      rowPrefetch: "100"
      LobMode: "1"

  test:
    host: dm8-test.example.com
    port: 5236
    user: APP_USER
    schema: APP
    password: "change-me"
    connect_timeout: 10s

ui:
  prompt: "{profile}:{schema}> "
  continuation_prompt: "...> "
  color: auto

editor:
  mode: emacs
  multiline: true

completion:
  enabled: true
  fuzzy: true
  keyword_case: upper
  metadata_ttl: 10m
  max_items: 100

execution:
  timeout: 0s
  max_rows: 10000
  sample_rows: 50
  stop_on_error: true
  timing: true

output:
  format: table
  null: "NULL"
  max_column_width: 60
  max_lob_preview: 256
  pager: auto

export:
  max_lob_bytes: 67108864

history:
  enabled: true
  file: "~/.local/share/dmcli/history"
  max_entries: 10000
  ignore_duplicates: true
  ignore_sensitive: true

logging:
  level: warn
  file: ""
  log_sql: false
```

配置采用严格校验。未知字段、非法端口、错误的时间格式或保留的连接属性都会导致启动失败。

### profile 驱动属性

`profiles.<name>.properties` 用于向固定的 DM8 Go 驱动传递额外连接属性。dmcli 会把这些键值追加到连接 DSN 的查询参数中；它们不是 dmcli 自身的 UI 或执行配置。

```yaml
profiles:
  local:
    host: 127.0.0.1
    port: 5236
    user: SYSDBA
    password_env: DMCLI_LOCAL_PASSWORD
    properties:
      socketTimeout: "60"
      compatibleMode: oracle
      loginEncrypt: "true"
```

常见属性包括：

| 属性 | 用途 |
|---|---|
| `socketTimeout` | 设置驱动网络读写超时 |
| `compatibleMode` | 指定驱动兼容模式，例如 `oracle` 或 `mysql` |
| `rowPrefetch` | 设置结果集预取行数 |
| `LobMode` | 设置驱动的大对象读取模式 |
| `loginEncrypt` | 控制登录用户名和密码的加密协商 |
| `sslFilesPath`、`sslCertPath`、`sslKeyPath` | 配置需要 SSL 认证的连接 |
| `logLevel`、`logDir` | 配置 DM 驱动自身的诊断日志 |

属性名称、可选值和单位由当前 DM8 Go 驱动定义。YAML 中建议将属性值写成字符串；普通单机连接通常不需要 `properties`，可以省略。

dmcli 会自动设置 `appName=dmcli`，并根据 profile 的 `connect_timeout` 生成驱动的 `connectTimeout`，不建议在 `properties` 中重复配置。`url`、`host`、`port`、`user`、`password`、`schema` 是保留键，放入 `properties` 会导致配置校验失败。密码应使用 profile 的 `password`、`password_env` 或 `DMCLI_PASSWORD`，不要作为驱动属性传递。

profile 可以直接配置 `password`，也可以使用 `password_env` 指定保存密码的环境变量名称：

```yaml
profiles:
  local:
    user: SYSDBA
    password: "your-password"
```

更推荐在共享环境使用环境变量：

```bash
export DMCLI_LOCAL_PASSWORD='your-password'
./bin/dmcli local
```

### 选择连接 profile

连接默认 profile：

```bash
./bin/dmcli
```

连接指定 profile：

```bash
./bin/dmcli test
```

命令行参数可以覆盖 profile：

```bash
./bin/dmcli test --host 192.168.1.20 --schema APP_TEST
```

### 配置优先级

普通配置按以下优先级合并：

```text
命令行参数
  > DMCLI_* 环境变量
    > YAML 配置
      > 内置默认值
```

密码来源优先级：

```text
DMCLI_PASSWORD
  > profile.password_env 指向的环境变量
    > profile.password
      > 交互式无回显输入
```

### 环境变量

| 环境变量 | 用途 |
|---|---|
| `DMCLI_CONFIG` | 配置文件路径 |
| `DMCLI_PROFILE` | 默认 profile |
| `DMCLI_HOST` | 数据库主机 |
| `DMCLI_PORT` | 数据库端口 |
| `DMCLI_USER` | 数据库用户 |
| `DMCLI_SCHEMA` | 初始模式 |
| `DMCLI_PASSWORD` | 当前连接密码 |
| `DMCLI_FORMAT` | `table` 或 `vertical` |
| `DMCLI_MAX_ROWS` | 最大返回行数 |
| `DMCLI_CONNECT_TIMEOUT` | 连接超时，例如 `5s` |
| `NO_COLOR` | 设置为非空值时关闭颜色 |

## 命令行参数

```text
dmcli [PROFILE] [flags]
dmcli version
```

主要参数：

| 参数 | 说明 |
|---|---|
| `--config PATH` | 指定 YAML 配置文件 |
| `--host HOST` | 数据库主机 |
| `--port PORT` | 数据库端口，默认 `5236` |
| `--user USER` | 数据库用户 |
| `--schema NAME` | 初始模式 |
| `--execute SQL`, `-e SQL` | 执行 SQL 后退出 |
| `--file PATH`, `-f PATH` | 执行 SQL 文件后退出 |
| `--format FORMAT` | `table` 或 `vertical` |
| `--no-color` | 禁用 ANSI 颜色 |
| `--help`, `-h` | 显示帮助 |

`--execute` 和 `--file` 不能同时使用。

## 交互使用

### 普通 SQL

普通 SQL 使用分号结束：

```sql
SELECT ID, NAME
FROM APP_USER
WHERE STATUS = 'ACTIVE';
```

可以在一次输入中执行多条 SQL：

```sql
CREATE TABLE DEMO(ID INT, NAME VARCHAR(100));
INSERT INTO DEMO VALUES (1, 'dmcli');
SELECT * FROM DEMO;
```

字符串、双引号标识符、注释和括号中的分号不会提前结束语句。

### DMSQL 程序块

DMSQL 匿名块以及过程、函数、触发器、包和模式定义，必须使用独立一行的 `/` 结束：

```sql
BEGIN
  INSERT INTO DEMO(ID, NAME) VALUES (2, 'DMSQL');
  COMMIT;
END;
/
```

创建过程示例：

```sql
CREATE OR REPLACE PROCEDURE ADD_DEMO(
  P_ID INT,
  P_NAME VARCHAR
)
AS
BEGIN
  INSERT INTO DEMO(ID, NAME) VALUES (P_ID, P_NAME);
END;
/
```

`/` 只用于客户端判断程序块结束，不会发送给数据库服务器。

### 对象浏览快捷命令

`LIST` 命令大小写不敏感，可以像普通 SQL 一样在交互模式、`--execute` 或 SQL 文件中使用：

```sql
LIST DATABASES;  -- 当前数据库
LIST SCHEMAS;    -- 可见模式
LIST TABLES;     -- 当前模式的表
LIST VIEWS;      -- 当前模式的视图
LIST INDEXES;    -- 当前模式的索引
LIST SEQUENCES;  -- 当前模式的序列
LIST PROCEDURES; -- 当前模式的存储过程
LIST FUNCTIONS;  -- 当前模式的函数
LIST TRIGGERS;   -- 当前模式的触发器
```

除 `DATABASES` 和 `SCHEMAS` 外，查询范围随 `\schema NAME` 切换到当前模式。对象类型也接受单数形式，例如 `LIST TABLE;` 和 `LIST FUNCTION;`。

兼容 MySQL 使用习惯，所有 `LIST` 命令都可以改写为 `SHOW`：

```sql
SHOW DATABASES;
SHOW SCHEMAS;
SHOW TABLES;
SHOW VIEWS;
SHOW INDEXES;
SHOW SEQUENCES;
SHOW PROCEDURES;
SHOW FUNCTIONS;
SHOW TRIGGERS;
```

`LIST` 和 `SHOW` 支持 SQL `LIKE` 名称过滤，模式作为参数传递给数据库：

```sql
SHOW TABLES LIKE 'USER%';
LIST VIEWS LIKE 'REPORT_202_';
SHOW INDEXES LIKE 'IDX_USER_%';
LIST SCHEMAS LIKE 'APP%';
```

这里使用 SQL 通配符：`%` 匹配任意长度字符串，`_` 匹配单个字符。DM8 对未加双引号创建的对象通常使用大写名称，因此模式通常也应使用大写。此语法与元命令 `\tables APP_*` 的 `*`、`?` 通配规则不同。

### 切换数据库和模式

切换当前模式，效果与 `\schema NAME` 相同：

```sql
SET SCHEMA APP;
SET SCHEMA "My Schema";
```

DM8 的模式切换使用服务器原生 `SET SCHEMA`。切换成功后，提示符中的模式和补全元数据会同步更新。

数据库或多租户 UDB 需要重新建立连接。`SET DATABASE` 将名称解析为同名 YAML profile：

```sql
SET DATABASE reporting;
```

也可以使用 MySQL 风格的 `USE`。不指定对象类型时默认切换数据库 profile：

```sql
USE reporting;
USE DATABASE reporting;
USE SCHEMA APP;
```

对应配置示例：

```yaml
profiles:
  reporting:
    host: dm8-reporting.example.com
    port: 5236
    user: REPORT_USER
    schema: REPORT
    password_env: DMCLI_REPORTING_PASSWORD
```

新连接建立并探测成功后才会关闭旧连接；连接失败时保留原会话。事务中禁止执行 `SET DATABASE` 和 `SET SCHEMA`。数据库、profile 或模式名称包含空白时使用双引号。

### 快捷键

| 快捷键 | 行为 |
|---|---|
| `Enter` | 语句完整时执行；否则继续输入 |
| `Ctrl+J` | 强制执行当前缓冲区 |
| `Ctrl+C` | 编辑时清空输入；查询时取消查询 |
| `Ctrl+D` | 空输入时退出 |
| `Ctrl+R` | 搜索当前 readline 历史 |

查询取消后，`dmcli` 会检查当前物理连接是否仍然可用。如果连接已损坏，会提示执行 `\reconnect`。

## 事务

默认情况下，普通 SQL 使用驱动的自动提交行为。

显式事务：

```text
local:SYSDBA> \begin
local:SYSDBA> UPDATE ACCOUNT SET BALANCE = BALANCE - 100 WHERE ID = 1;
local:SYSDBA> UPDATE ACCOUNT SET BALANCE = BALANCE + 100 WHERE ID = 2;
local:SYSDBA> \commit
```

回滚事务：

```text
local:SYSDBA> \begin
local:SYSDBA> DELETE FROM DEMO;
local:SYSDBA> \rollback
```

事务期间不能切换 profile、重连或切换模式。`dmcli` 不会自动重放事务内的 SQL。

## 元命令

元命令以反斜杠开头：

| 命令 | 说明 |
|---|---|
| `\?` | 显示帮助 |
| `\q` | 退出 |
| `\connect PROFILE` | 连接指定 profile |
| `\reconnect` | 重新连接当前 profile |
| `\conninfo` | 显示当前连接信息 |
| `\schemas` | 列出可见模式 |
| `\schema NAME` | 切换当前模式 |
| `\tables [PATTERN]` | 列出表 |
| `\views [PATTERN]` | 列出视图 |
| `\indexes [SCHEMA.]TABLE` | 显示指定表的索引及索引字段 |
| `\describe OBJECT` | 显示对象字段结构及列注释 |
| `\source FILE` | 执行 SQL 文件 |
| `\history [PATTERN]` | 查看历史 |
| `\rehash` | 后台刷新元数据 |
| `\timing on\|off` | 开关耗时显示 |
| `\pager auto\|on\|off` | 设置分页行为 |
| `\format table\|vertical` | 设置输出格式 |
| `\x` | 切换表格和垂直输出 |
| `\begin` | 开始事务 |
| `\commit` | 提交事务 |
| `\rollback` | 回滚事务 |
| `\set NAME VALUE` | 设置当前会话客户端选项 |

### Tab 补全

补全不区分大小写，并根据光标位置提供候选：

- `SHOW`、`LIST`：补全 `TABLES`、`VIEWS`、`INDEXES` 等对象类别；`SHOW/LIST INDEXES FROM` 补全当前模式的表。
- `USE DATABASE`、`SET DATABASE`、`USE name`：补全 YAML profile。
- `USE SCHEMA`、`SET SCHEMA`、`\schema`：补全可见模式。
- `\connect`：补全 profile；`\tables`、`\views`、`\indexes`、`\describe`：补全当前模式对象。
- `\format`、`\pager`、`\timing`、`\set`：补全允许的参数。
- 普通 SQL：补全关键字、模式、表、视图、字段和单层表别名。

模式及对象元数据在连接后异步加载，补全过程不会查询数据库。刚连接时至少会提供当前模式；如数据库对象刚发生变化，可执行 `\rehash` 刷新快照。

通配符示例：

```text
\tables APP_*
\views REPORT_?
```

`*` 匹配任意字符，`?` 匹配单个字符。

### `\set` 选项

```text
\set max_rows 5000
\set null <NULL>
\set max_column_width 80
\set max_lob_preview 512
```

这些设置只影响当前进程，不会写回 YAML。

## 输出

### 表格输出

默认输出格式为 `table`：

```text
+----+-------+
| ID | NAME  |
+----+-------+
| 1  | dmcli |
+----+-------+
1 行  耗时: 3ms
```

切换表格格式：

```text
\format table
```

普通查询、`\describe` 以及其他表格型元命令使用同一套分页输出。当表格总宽度超过终端时，Linux 和 macOS 会在 `less` 中保持单行显示。底部会提示操作方式：使用 `←`、`→` 查看左右隐藏列，使用 `↑`、`↓` 翻行，按 `q` 返回 dmcli。右侧出现 `>` 表示该方向还有内容。

列数很多时，也可以按 `\x` 临时切换为垂直输出，避免横向滚动。

### 垂直输出

```text
\format vertical
```

或使用：

```text
\x
```

输出示例：

```text
*************************** 1. row ***************************
ID: 1
NAME: dmcli
```

### 大结果集

- 默认最多显示 10,000 行。
- 达到 `max_rows` 后停止读取，并显示“结果已截断”。
- 查询结果逐行扫描，不会一次性加载完整结果集。
- CLOB 和 BLOB 默认只读取有限预览。
- TTY 下可使用分页器；stdout 重定向时自动关闭分页和 ANSI。

重定向示例：

```bash
./bin/dmcli local -e 'SELECT * FROM APP_USER;' > result.txt
```

## SQL 文件

SQL 文件支持普通 SQL、DMSQL 和有限的元命令：

```sql
CREATE TABLE DEMO(ID INT, NAME VARCHAR(100));

BEGIN
  INSERT INTO DEMO VALUES (1, 'first');
  INSERT INTO DEMO VALUES (2, 'second');
END;
/

SELECT * FROM DEMO;
```

文件中允许：

- `\set`
- `\timing`
- `\format`
- `\source`

嵌套文件示例：

```text
\source ./schema.sql
\source ./data.sql
```

相对路径以当前 SQL 文件所在目录为基准。最多嵌套 16 层，并会检测循环引用。

默认遇到第一条错误就停止。可在配置中设置：

```yaml
execution:
  stop_on_error: false
```

## 退出码

| 退出码 | 含义 |
|---:|---|
| `0` | 执行成功 |
| `1` | 未分类内部错误 |
| `2` | 参数或配置错误 |
| `3` | 连接、认证或驱动初始化失败 |
| `4` | SQL、SQL 文件或元命令失败 |

## 安全说明

- 不支持通过命令行参数传入密码；YAML 允许 profile `password`，但应将配置文件权限限制为当前用户可读。
- 密码不会写入历史或连接信息输出。
- 包含 `IDENTIFIED BY`、`PASSWORD`、`TOKEN`、`SECRET` 等敏感模式的 SQL 默认不保存到历史。
- 日志默认不记录 SQL 正文、查询结果、参数或完整 DSN。
- Linux 和 macOS 上建议将配置文件权限设置为 `0600`。

```bash
chmod 600 ~/.dmcli.yml
```

## 测试

运行单元测试：

```bash
make test
```

或：

```bash
go test ./...
```

运行竞态检测：

```bash
go test -race ./internal/...
```

验证固定驱动元数据：

```bash
make verify-driver
```

## 驱动与许可

当前分支固定使用官方 DM8 Go 驱动 `8.1.5.60`。驱动来源和完整性信息见：

- [`third_party/dm/ORIGIN.yaml`](third_party/dm/ORIGIN.yaml)
- [`third_party/dm/PATCHES.yaml`](third_party/dm/PATCHES.yaml)
- [`LICENSES/dm-go-driver-LICENSE`](LICENSES/dm-go-driver-LICENSE)

官方驱动许可证对修改和二次发布有限制。未取得适用的书面授权前，包含驱动的源码和二进制仅应用于组织内部或个人用途。

官方驱动没有提供 Darwin 第三方密码插件加载器。项目增加了一个独立的 Darwin-only 垫片，在请求该可选功能时明确返回“不支持”；其他连接功能不受影响。

## 当前限制

- 只支持 DM8。
- 固定驱动版本，不能运行时切换。
- 不提供完整 SQL 语法分析和语义校验。
- 复杂 CTE、嵌套子查询和多层作用域只提供降级补全。
- 不支持返回游标的存储过程结果展示。
- 当前正式输出格式只有 `table` 和 `vertical`。
- 不提供执行计划、锁诊断、备份恢复或 GUI。

完整实现约束和架构说明见 [`docs/dmcli-v1-design.md`](docs/dmcli-v1-design.md)。
