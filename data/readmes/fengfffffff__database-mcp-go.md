# database-mcp-go

中文 | [English](README.en.md)

> 把 MySQL、MariaDB、TiDB、OceanBase、KingbaseES、PostgreSQL、SQL Server、SQLite、MongoDB 与 Redis 以 MCP 工具暴露给 AI 客户端. 连接凭证留在服务端, 客户端只用实例别名加库名调用; 数据源可存文件或库表; 单个静态二进制自带管理页.

---

## 一、功能

| 能力 | 说明 |
|------|------|
| 十种数据库 | 一套接口覆盖十种库, 每个库独立连接池 |
| 六个 MCP 工具 | 执行语句与命令, 查询与增删改数据源, 刷新配置 |
| 凭证集中 | 客户端只能拿到别名与库名 |
| 事务语义 | SQL 类库多条语句同事务, 失败整体回滚 |
| 双存储 | file 零依赖; mysql 密码加密落库 |
| 配置热生效 | 增删改后缓存失效, 下次访问回源 |
| 内嵌管理页 | `/admin` 提供搜索、分页、批量删除、状态开关、列设置, 界面中英文切换, 默认中文 |
| 中文错误 | 错误类别、错误码、SQLSTATE 与修正建议 |
| 单文件交付 | 纯 Go 无 cgo, 复制二进制与配置即可运行 |
| 日志 | 按天切分, 超期自动清理 |

### (1)、支持的数据库

| databaseType | 数据库 | 驱动 | 连接要点 |
|------|------|------|------|
| 0 | MySQL | go-sql-driver/mysql | 地址、端口、账号、库名 |
| 1 | KingbaseES V8 | pgx, PostgreSQL 协议 | 同上 |
| 2 | PostgreSQL | pgx | 同上, 默认 sslmode=prefer |
| 4 | SQL Server | microsoft/go-mssqldb | 命名实例填实际监听端口, encrypt 默认 disable |
| 5 | MariaDB | 复用 MySQL 驱动 | 同 MySQL |
| 6 | TiDB | 复用 MySQL 驱动 | 同 MySQL |
| 7 | OceanBase MySQL 模式 | 复用 MySQL 驱动 | 同 MySQL |
| 8 | SQLite | modernc.org/sqlite | 地址填文件绝对路径, 库名建议填 main |
| 9 | MongoDB | mongo-driver v2 | 地址、端口、库名, 账号可空 |
| 10 | Redis | go-redis v9 | 地址、端口, 库名填逻辑库编号 |

driverClass 仅用于展示, 实际驱动按 databaseType 选择. 一个实例可配多个库, 每个库独立连接池, `poolMaximumPoolSize` 是单库上限.

## 二、快速开始

### (1)、编译

需要 Go 1.27 及以上:

```bash
go build -o database-mcp-go ./cmd/database-mcp-go

# 静态单文件
CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags "-s -w" -o database-mcp-go ./cmd/database-mcp-go

# 注入版本号
CGO_ENABLED=0 go build -ldflags "-s -w -X main.version=v1.0.0" -o database-mcp-go ./cmd/database-mcp-go
```

命令行参数只有两个: `-config` 指定配置文件, 默认 config.yaml; `-version` 输出版本号. Windows 下产物名写成 `database-mcp-go.exe`.

### (2)、最小配置

```yaml
server:
  port: 47319

mcp:
  auth_token: "change-me"

admin:
  username: "admin"
  password: "${ADMIN_PASSWORD}"

source:
  type: file
  file:
    path: datasources.json
```

`admin.username` 与 `admin.password` 必填, 账号或密码为空时启动直接失败; 上例用环境变量注入密码, 启动前先设置 `ADMIN_PASSWORD`.

### (3)、准备数据源

file 模式编辑 `datasources.json`, 其余字段见第三章 file 模式一节:

```json
{
  "datasources": [
    {
      "id": 1,
      "alias": "本地库",
      "host": "127.0.0.1",
      "port": 3306,
      "username": "root",
      "password": "your-password",
      "databaseName": "app",
      "databaseType": 0,
      "driverClass": "com.mysql.cj.jdbc.Driver"
    }
  ]
}
```

文件不存在时按空清单处理, 首次新增会自动创建.

### (4)、启动与验证

```bash
./database-mcp-go -config config.yaml
curl http://127.0.0.1:47319/healthz
```

启动前先填好 `config.yaml` 里的 `admin.username` 与 `admin.password`, 或用 `${ADMIN_PASSWORD}` 从环境变量注入密码, 缺一项进程会直接退出. 管理页始终开启, 访问 `http://127.0.0.1:47319/admin`, 支持类型统计、四条件筛选、分页、批量删除、状态开关、详情、列设置与重载, 界面在右上角切换中英文, 默认中文.

### (5)、接入 MCP 客户端

以 ZCode 为例, 其他支持 MCP Streamable HTTP 的客户端同理:

```json
{
  "mcpServers": {
    "database-mcp-go": {
      "type": "http",
      "url": "http://127.0.0.1:47319/mcp",
      "headers": {
        "Authorization": "Bearer change-me"
      }
    }
  }
}
```

### (6)、HTTP 端点

| 端点 | 说明 |
|------|------|
| `/mcp` | MCP 端点, 路径可配, 配置 token 后需 Bearer Token |
| `/admin` | 内嵌管理页, 始终开启, 需基础认证 |
| `/healthz` | 健康检查 |

配置刷新只在配置被服务外部改过时使用, 规则见第三章(3).

## 三、配置教程

`config.yaml` 的全部配置项, 未写的按默认值生效, 取值支持 `${ENV_NAME}` 环境变量注入. 本章都是启动配置, 改完需重启.

### (1)、服务与 MCP

| 配置项 | 默认值 | 说明 |
|------|------|------|
| `server.port` | 47319 | 服务端口 |
| `mcp.endpoint` | `/mcp` | MCP 端点路径, 须以 / 开头且不能是根路径, 结尾多余斜杠自动去掉 |
| `mcp.auth_token` | 空 | Bearer Token, 留空不校验, 只适合本机回环 |
| `mcp.session_timeout_seconds` | 600 | 空闲会话超时秒数 |
| `mcp.max_request_body_bytes` | 0 | 请求体上限字节, 0 用 SDK 默认值 |
| `mcp.disable_localhost_protection` | false | 经隧道或反向代理访问时置 true |
| `mcp.stateless` | false | true 时不维持会话, 每个请求独立 |

### (2)、执行与限额

| 配置项 | 默认值 | 说明 |
|------|------|------|
| `database.query_timeout_seconds` | 30 | 单条语句超时秒数, 超时中止整批; 0 或负数按 30 处理 |
| `database.slow_query_threshold_ms` | 1000 | 慢操作告警阈值毫秒 |
| `database.max_rows` | 1000 | 单次执行累计返回行数上限, 超出截断 |

### (3)、数据源存储

| 配置项 | 默认值 | 说明 |
|------|------|------|
| `source.type` | file | `file` 或 `mysql`, 二选一 |
| `source.file.path` | datasources.json | 数据源清单文件, file 模式生效 |
| `source.mysql.dsn` | 无 | 配置库 DSN, mysql 模式必填 |
| `source.mysql.aes_key` | 无 | AES-256-GCM 密钥, Base64 的 32 字节 |
| `source.mysql.table` | sys_mcp_database_config | 配置表名, 只允许字母数字下划线 |

配置在进程内按缓存处理: 增删改成功后只失效, 下一次访问才回源. 连接池按「别名::库」懒建并记录配置指纹, 连接参数变了才重建, 别名或库消失后在回源时回收. 配置被服务外部改过时, 用管理页的重载按钮或 MCP 的 `refresh-config` 刷一次.

### (4)、日志与管理页

| 配置项 | 默认值 | 说明 |
|------|------|------|
| `log.dir` | logs | 日志目录 |
| `log.level` | info | 日志级别 |
| `log.retain_days` | 14 | 保留天数, 超期文件自动清理 |
| `log.console` | false | 是否同时输出到控制台 |
| `log.command` | true | 是否记录执行内容, SQL 语句、MongoDB 命令文档与 Redis 命令都记, 截断到 500 字 |
| `admin.username` | 无默认值 | 基础认证账号, 必填, 不能包含冒号 |
| `admin.password` | 无默认值 | 基础认证密码, 必填 |

旧版的 `admin.enabled` 已移除, 配置里保留该键也不会生效; 管理页始终开启, 只由账号密码控制访问.

### (5)、连接属性

`connectionProperties` 沿用 JDBC 写法, `key=value&key=value`. 未识别的键直接忽略.

| 数据库 | 常用属性 | 说明 |
|------|------|------|
| MySQL 族 | `useSSL`, `connectTimeout`, `socketTimeout`, `sessionVariables` | useSSL 转 tls, 超时按毫秒 |
| PostgreSQL 与金仓 | `sslmode`, `currentSchema`, `connectTimeout` | currentSchema 转 search_path |
| SQL Server | `encrypt`, `TrustServerCertificate`, `databaseName`, `connectTimeout` | connectTimeout 按毫秒 |
| SQLite | 不生效 | 行为由驱动内置参数决定 |
| MongoDB | `authSource`, `replicaSet`, `tls`, `connectTimeoutMS` | connectTimeout 按毫秒 |
| Redis | `readtimeout` | 毫秒, 默认 30000, 阻塞命令用 |

同一个超时既写在连接属性里、又配在连接池参数里时, 以连接属性为准.

### (6)、file 模式

数据源存在独立 JSON 文件, 增删改直接回写该文件. 密码明文, 适合本机与内网试用.

| 字段 | 必填 | 说明 |
|------|------|------|
| `alias` | 是 | 实例别名, 唯一 |
| `databaseType` | 是 | 类型编号, 见支持矩阵 |
| `host` | 是 | 实例地址, SQLite 填文件绝对路径 |
| `port` | 是 | 实例端口, SQLite 填 0 |
| `databaseName` | 是 | 库名, 多个用英文逗号分隔; SQLite 建议填 main, 实际由实例地址决定 |
| `username` | SQL 类必填 | MongoDB 与 Redis 可空, SQLite 不用填 |
| `password` | 否 | MongoDB 有密码时必须同时给用户名; Redis 可只填密码 |
| `driverClass` | SQL 类必填 | 展示用, SQLite、MongoDB 与 Redis 留空 |
| `connectionProperties` | 否 | JDBC 写法, 见连接属性一节 |
| `poolMinimumIdle` 等五项 | 否 | 不写用默认值 2、10、5000、600000、1800000; 写 0 保留 0, 连接超时 0 表示不设上限 |
| `poolValidationTimeout` | 否 | 保留兼容, 当前驱动未使用 |
| `status` | 否 | 0 停用, 1 启用, 不写按 1 |
| `id` | 否 | 管理页维护需要唯一, 手工编辑时建议写 |

### (7)、mysql 模式

数据源存在 MySQL 配置表, 密码以 AES-256-GCM 密文落库.

```yaml
source:
  type: mysql
  mysql:
    dsn: "user:password@tcp(127.0.0.1:3306)/core_service?parseTime=true&loc=Asia/Shanghai"
    aes_key: "wS4WeHm2opebcZ9p6O8TcurmelrMZ1iVR75OmbGxN6Q="
    table: sys_mcp_database_config
```

生成密钥:

```bash
openssl rand -base64 32
```

首次使用先建表, 需要 MySQL 8.0.13 及以上:

```sql
CREATE TABLE `sys_mcp_database_config` (
  `id`                      BIGINT UNSIGNED  NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `alias`                   VARCHAR(128)     NOT NULL DEFAULT '' COMMENT '实例别名',
  `database_name`           VARCHAR(512)     NOT NULL DEFAULT '' COMMENT '数据库名, 多个用英文逗号分隔',
  `database_type`           TINYINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '实例类型, 取值见支持矩阵',
  `database_version`        VARCHAR(32)      NOT NULL DEFAULT '' COMMENT '实例版本, 仅展示',
  `host`                    VARCHAR(128)     NOT NULL DEFAULT '' COMMENT '实例地址',
  `port`                    INT UNSIGNED     NOT NULL DEFAULT 3306 COMMENT '实例端口',
  `username`                VARCHAR(128)     NOT NULL DEFAULT '' COMMENT '实例用户名',
  `password`                VARCHAR(256)     NOT NULL DEFAULT '' COMMENT '实例密码, AES-256-GCM 密文',
  `driver_class`            VARCHAR(256)     NOT NULL DEFAULT '' COMMENT '驱动类',
  `connection_properties`   VARCHAR(512)     NOT NULL DEFAULT '' COMMENT '连接属性, JDBC 写法',
  `pool_minimum_idle`       INT UNSIGNED     NOT NULL DEFAULT 2 COMMENT '最小空闲连接数',
  `pool_maximum_pool_size`  INT UNSIGNED     NOT NULL DEFAULT 10 COMMENT '最大连接数',
  `pool_connection_timeout` BIGINT UNSIGNED  NOT NULL DEFAULT 5000 COMMENT '连接超时毫秒',
  `pool_idle_timeout`       BIGINT UNSIGNED  NOT NULL DEFAULT 600000 COMMENT '空闲超时毫秒',
  `pool_max_lifetime`       BIGINT UNSIGNED  NOT NULL DEFAULT 1800000 COMMENT '连接最大存活毫秒',
  `pool_validation_timeout` BIGINT UNSIGNED  NOT NULL DEFAULT 3000 COMMENT '连接校验超时毫秒',
  `status`                  TINYINT UNSIGNED NOT NULL DEFAULT 1 COMMENT '状态 0-停用 1-启用',
  `create_by_id`            BIGINT UNSIGNED  NOT NULL DEFAULT 0 COMMENT '创建人ID',
  `create_by_name`          VARCHAR(128)     NOT NULL DEFAULT '' COMMENT '创建人名称',
  `create_by_type`          VARCHAR(64)      NOT NULL DEFAULT '' COMMENT '创建人类型',
  `create_time`             DATETIME         NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_by_id`            BIGINT UNSIGNED  NOT NULL DEFAULT 0 COMMENT '修改人ID',
  `update_by_name`          VARCHAR(128)     NOT NULL DEFAULT '' COMMENT '修改人名称',
  `update_by_type`          VARCHAR(64)      NOT NULL DEFAULT '' COMMENT '修改人类型',
  `update_time`             DATETIME         DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  `is_deleted`              TINYINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '是否删除 0-否 1-是',
  `remark`                  VARCHAR(500)     NOT NULL DEFAULT '' COMMENT '备注',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_alias` ((CASE WHEN `is_deleted` = 0 THEN `alias` END))
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_bin COMMENT = 'MCP 数据库代理配置表';
```

## 四、工具与返回

### (1)、工具列表

| 工具 | 用途 |
|------|------|
| `execute-command` | 执行语句或命令, SQL 用分号分隔多条; MongoDB 传 JSON 命令文档; Redis 每行一条命令 |
| `get-datasources` | 查询启用的实例与所辖数据库, 支持别名模糊过滤 |
| `add-database-config` | 新增实例配置, 成功后配置缓存自动失效 |
| `update-database-config` | 修改实例配置, 不传的字段保留原值 |
| `delete-database-config` | 删除实例配置 |
| `refresh-config` | 立即回源刷新配置缓存 |

`get-datasources` 只列启用的实例, 停用实例查不到也执行不了; 任何工具都不返回实例密码.

### (2)、三种输入

SQL 类库:

```json
{"alias": "生产库", "databaseName": "order", "command": "SELECT id, status FROM t_order ORDER BY id DESC LIMIT 20"}
```

MongoDB 传 runCommand 语法的 JSON:

```json
{"alias": "文档库", "databaseName": "app", "command": "{\"find\": \"users\", \"filter\": {\"age\": {\"$gt\": 18}}, \"limit\": 5}"}
```

Redis 每行一条命令:

```json
{"alias": "缓存", "databaseName": "0", "command": "SET greeting \"hello world\"\nGET greeting"}
```

### (3)、返回结构

单条语句:

```json
{"code": 200, "message": "操作成功", "data": {"rows": [{"id": 1}], "rowCount": 1, "affectedRows": 0, "executionTime": 8}}
```

多条语句时 `rows` 为空, 按语句放在 `results`:

```json
{"code": 200, "data": {"rows": [], "rowCount": 2, "affectedRows": 1, "statementCount": 2, "results": [{"statementIndex": 1, "rows": [{"cnt": 3}], "rowCount": 1, "affectedRows": 0}, {"statementIndex": 2, "rows": [], "rowCount": 0, "affectedRows": 1}]}}
```

| 字段 | 说明 |
|------|------|
| `rows` | 单条语句的行数据, 列顺序与查询一致, 同名列加 `_2`、`_3` 后缀 |
| `results` | 多条语句的逐条结果, 带 `statementIndex` |
| `rowCount` | 本次返回的行数, 受 `database.max_rows` 截断 |
| `affectedRows` | 写操作受影响行数; `WITH` 写语句、带 `RETURNING` 或 `OUTPUT` 的写语句与 MongoDB 命令记为 0, Redis 为成功命令条数 |
| `truncated` | 是否因超出上限被截断 |
| `executionTime` | 毫秒 |

值的格式: NULL 输出 null; 二进制合法 UTF-8 按文本、否则 Base64; 时间统一 `2006-01-02 15:04:05`; `NaN` 与 `Infinity` 按文本输出; JSON 与 JSONB 输出 JSON 文本.

### (4)、错误格式

```text
执行失败 - 错误类别: 表不存在, 错误码: 1146, SQLSTATE: 42S02, 原始信息: Table 'db.t' doesn't exist, 建议: 核对库名与表名
第 2/3 条语句执行失败 - ... 语句: UPDATE t SET a = 1
```

金仓与 PostgreSQL 另带服务端详情、提示与出错行列; SQL Server 带行号; SQLite 带约束细分; Redis 按错误前缀归类; 超时提示附语句原文.

## 五、各库行为差异

### (1)、SQL 类库

1. 多条语句按分号拆开逐条执行, 整批共用一个事务, 全部成功才提交; 每条语句单独走查询或执行通道, 因此能给出各自的受影响行数.
2. 语句里不要自带 BEGIN 与 COMMIT, 事务由服务统一控制.
3. DDL 与 DML 不要混批, 改表等 DDL 单独调用; MySQL 的 DDL 隐式提交, 混批无法整体回滚.
4. SQL Server 带 `OUTPUT` 的写语句与 `EXEC` 存储过程按查询处理, 受影响行数记 0; 以 `WITH` 开头的写语句同样按查询处理, 行数也记 0; `GO` 是客户端批分隔符, 协议层不认, 多条语句用分号.
5. SQLite 地址填文件绝对路径, 库名建议填 main, 端口、用户名、密码与驱动类留空; 连接串自动开启 WAL 与忙等待, 连接数上限 4; 带 `RETURNING` 的写语句返回行数据.

### (2)、MongoDB

1. 每条命令原样经 RunCommand 下发, 是否合法由服务端判断, 命令名须写在文档首位.
2. 命令按顺序执行, 无事务, 中途失败已执行的命令不回滚.
3. 回复按顶层字段平铺成一行, 嵌套文档与数组输出 JSON 文本; `rowCount` 是回复文档条数, 不是 cursor 里的文档数.
4. `find` 只返回 `cursor.firstBatch`, 取后续结果用 `getMore` 带 cursor id.
5. 写入类命令的部分失败写在回复的 `writeErrors` 里, 顶层仍是 `ok: 1`, 需要检查该字段.
6. 命令按扩展 JSON 解析成有序文档, `sort` 与 `$sort` 的键序即排序优先级; 支持 `$oid`、`$date`、`$numberLong`、`$numberInt`、`$numberDouble`.
7. `_id` 上的 24 位十六进制字符串自动按 ObjectId 处理, 需要按字符串匹配时写成 `{"_id": {"$eq": "值"}}`.
8. 必须在 admin 库执行的命令如 `renameCollection`, 把数据源库名配成 admin 另登记一个别名.
9. 允许不填用户名与密码; 一旦填了密码就必须同时填用户名.

### (3)、Redis

1. 每行一条命令, 参数空格分隔, 含空格的参数用引号包裹, 井号开头的行当注释; 命令按顺序执行, 无事务.
2. 库名填逻辑库编号 0 至 65535, 可配多个逻辑库.
3. 回复转行: 标量单行一列 `result`, 数组每个元素一行, 映射输出 JSON 文本, 非 UTF-8 的二进制按 Base64.
4. `affectedRows` 为成功执行的命令条数.
5. 拒绝会独占连接或必须落在同一条连接上的命令: `SUBSCRIBE`、`PSUBSCRIBE`、`MONITOR`、`SYNC`、`PSYNC` 会独占或接管连接; `MULTI`、`EXEC`、`DISCARD`、`WATCH`、`UNWATCH` 要求同一条连接, 事务请改用 Lua 脚本.
6. `SELECT` 会改掉池内连接的逻辑库, 换库请改数据源配置; `HELLO` 会切换连接的协议版本; `CLIENT REPLY`、`CLIENT KILL`、`CLIENT PAUSE`、`CLIENT TRACKING` 会关闭回包或波及其它客户端. 以上均拦截, `CLIENT LIST`、`CLIENT INFO` 这类只读诊断照旧可用.
7. 阻塞命令的等待由 `readtimeout` 兜底, 默认 30000 毫秒.
8. 可只填密码不填用户名, 适配单机 Redis; 需要 ACL 用户时两个都填.

## 六、安全

1. `auth_token` 留空表示不校验, 只适合本机回环; 服务离开本机必须配置 token.
2. 管理页始终开启, 只有一组基础认证, 没有权限体系; 必须配置账号与密码, 缺一项启动即失败, 不存在无认证放行. 基础认证走明文 HTTP, 跨机访问请套 HTTPS 或 SSH 隧道.
3. file 模式的密码是明文, 注意文件权限; 要求密文存储时选 mysql 模式.
4. `log.command` 会把执行内容写入日志, 含 Redis 命令与缓存值, 敏感场景设为 false.
5. 代理层不做业务语义过滤, 只拦会破坏连接的协议级命令; 能执行什么由数据库账号权限决定, 建议为每个数据源配置只读或受限账号.

## 七、已知限制

1. 累计返回行数默认上限 1000, 超出截断并标记 `truncated`; 截断只限返回体积, 数据库仍会跑完全量, 大表查询请自带 LIMIT 或 TOP.
2. 含块体的 DDL 会被分号切错: SQL Server 的存储过程与 `BEGIN ... END`, MySQL 用 `DELIMITER` 定义的存储过程. 这类对象请在其他客户端建好.
3. 金仓与 PostgreSQL 的极端自定义类型可能退化为文本返回.
4. 二进制按 Base64 输出, 合法 UTF-8 的字节显示为文本; 大字段建议在查询里裁剪.
5. SQLite 是单写者模型, 并发写会互相等待.
6. SQL Server 命名实例请直接填监听端口, 不支持 SQL Browser 自动发现.
7. MongoDB 与 Redis 见第五章对应小节.
8. 管理页只做数据源维护, 不含 Excel 导入导出.

## 八、开发

### (1)、目录结构

```text
cmd/database-mcp-go           启动入口, 只做装配
internal/config               配置加载与环境变量注入
internal/cryptox              AES-256-GCM 加解密, 用于实例密码
internal/model                配置、结果与统一响应体
internal/driver               驱动契约、注册表、值归一化
internal/driver/mysql         MySQL 协议族, 覆盖 MySQL 与 MariaDB、TiDB、OceanBase
internal/driver/kingbase      金仓
internal/driver/postgresql    PostgreSQL
internal/driver/sqlserver     SQL Server
internal/driver/sqlite        SQLite
internal/driver/mongodb       MongoDB
internal/driver/redis         Redis
internal/driver/sqlsplit      语句切分, 覆盖 MySQL、PostgreSQL、T-SQL、SQLite 方言
internal/pool                 按别名与库维度懒建连接池
internal/repository           数据源存储, file 与 mysql 两种实现
internal/service              业务编排: 执行、增删改查、配置缓存失效与回源
internal/tool                 MCP 工具定义
internal/transport            HTTP 路由、MCP 端点、鉴权中间件
internal/admin                管理页与后台接口, static 下是 Vue 与 Element Plus 构建产物
internal/logx                 日志与滚动清理
```

### (2)、本机联调

`mcp.stateless: true` 时可直接调工具:

```bash
curl -s -X POST http://127.0.0.1:47319/mcp \
  -H 'Authorization: Bearer change-me' \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get-datasources","arguments":{}}}'
```

返回是 SSE, 取 `data:` 后那行 JSON. 会话模式需先 initialize 并带 `Mcp-Session-Id`.

### (3)、静态检查

```bash
go vet ./...
```

### (4)、第三方依赖

1. MCP 官方 Go SDK: `github.com/modelcontextprotocol/go-sdk`.
2. 数据库驱动: `go-sql-driver/mysql`、`jackc/pgx/v5`、`microsoft/go-mssqldb`、`modernc.org/sqlite`、`go.mongodb.org/mongo-driver/v2`、`github.com/redis/go-redis/v9`, 全部纯 Go.
3. 管理页资源是 Vue 3 与 Element Plus 官方发布包, MIT 许可, 随二进制分发.
