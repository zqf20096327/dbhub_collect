# GaussDB MCP

华为云 GaussDB 云数据库 MCP 服务器。基于华为官方 GaussDB 专属 Node.js 驱动 [gaussdb-node](https://github.com/huaweicloud-samples/database-gaussdb-node),遵循 MCP 2026-07-28 规范,提供连接测试、查询、数据写入、事务、元数据、诊断运维、用户权限等 24 个工具与 1 个表结构资源。

## 快速开始

```bash
npm install
cp .env.example .env   # Windows: copy .env.example .env 后编辑
# 编辑 .env,填入 GaussDB 实例地址、密码等
npm run build
node build/index.js    # 启动(stdio,供 MCP 客户端拉起)
```

要求 Node.js ≥ 20。

## 连接配置

### 全部环境变量

| 变量 | 必填 | 默认值 | 说明 |
|---|---|---|---|
| `GAUSSDB_HOST` | 是 | — | GaussDB 实例地址;主备多节点用英文逗号分隔(如 `10.0.0.1,10.0.0.2`) |
| `GAUSSDB_PORT` | 否 | `8000` | 数据库端口,华为云 GaussDB 云实例默认 8000 |
| `GAUSSDB_DATABASE` | 否 | `postgres` | 数据库名 |
| `GAUSSDB_USER` | 否 | `root` | 登录用户,默认管理员为 root |
| `GAUSSDB_PASSWORD` | 是 | — | 登录密码 |
| `GAUSSDB_SEARCH_PATH` | 否 | — | 默认 schema,对应 JDBC 的 `currentSchema`(经连接 options 以 `search_path` GUC 下发,如 `gycwd`) |
| `GAUSSDB_MASTER_ONLY` | 否 | `0` | 主备多节点时仅连主节点(对应 JDBC `targetServerType=master`,按 `pg_is_in_recovery()` 判别) |
| `GAUSSDB_SSL` | 否 | `0` | 设为 `1` 开启 SSL 加密连接 |
| `GAUSSDB_SSL_CA` | 否 | — | CA 根证书路径(华为云控制台下载 `root.crt`) |
| `GAUSSDB_SSL_CERT` | 否 | — | 客户端证书路径(仅双向认证需要) |
| `GAUSSDB_SSL_KEY` | 否 | — | 客户端私钥路径(仅双向认证需要) |
| `GAUSSDB_SSL_REJECT_UNAUTHORIZED` | 否 | `true` | 是否校验服务器证书;调试时可设 `false`(不安全,仅测试) |

### 内网连接配置

应用与 GaussDB 实例在同一 VPC 内时使用。**不需要 SSL**(内网流量不外泄,华为云官方默认内网直连):

```env
GAUSSDB_HOST=10.0.1.11              # 实例"节点列表"中的内网地址
GAUSSDB_PORT=8000
GAUSSDB_DATABASE=postgres
GAUSSDB_USER=root
GAUSSDB_PASSWORD=你的密码
# 不设置任何 GAUSSDB_SSL_* 变量,保持 GAUSSDB_SSL=0(默认)
```

### 公网连接配置

应用不在实例 VPC 内、通过弹性公网 IP 访问时使用。**必须开启 SSL 并配置 CA 证书**(华为云官方 `sslmode=verify-ca` 方式):

```env
GAUSSDB_HOST=114.114.114.114        # 实例绑定的弹性公网 IP
GAUSSDB_PORT=8000
GAUSSDB_DATABASE=postgres
GAUSSDB_USER=root
GAUSSDB_PASSWORD=你的密码
GAUSSDB_SSL=1
GAUSSDB_SSL_CA=C:/path/to/root.crt   # 华为云控制台下载的 CA 证书(公网连接必需)
GAUSSDB_SSL_REJECT_UNAUTHORIZED=true
```

公网连接前还需在华为云控制台安全组中放行客户端出口 IP 对 8000 端口的访问。

### 环境变量如何添加

两种方式,任选其一(同时存在时环境变量优先于 `.env`):

1. **项目 `.env` 文件**(推荐):把 `.env.example` 复制为项目根目录下的 `.env` 并填写。`.env` 的定位**锚定项目根目录**,与服务器从哪个目录启动无关——MCP 客户端从任何工作目录拉起 `build/index.js` 都能读到。上面两种配置直接写入 `.env` 即可。
2. **MCP 客户端 `env` 字段**:在 `mcpServers` 配置里直接传环境变量(见下文接入示例),适合不想在项目里放凭据文件的场景。

主备部署时 `GAUSSDB_HOST` 用英文逗号分隔多个节点 IP,服务器启动时依次试连,自动选用第一个可用节点。

## 工具一览(24 个)

所有工具按 MCP 规范标注了 annotations(`readOnlyHint`/`destructiveHint`),客户端可据此对写操作弹出确认。

**连接与状态**

| 工具 | 说明 |
|---|---|
| `test_connection` | 测试连接,返回 GaussDB 版本、当前库、当前用户 |

**查询与写入**

| 工具 | 说明 |
|---|---|
| `query` | 执行只读查询(SELECT/WITH/EXPLAIN/SHOW/VALUES 开头,单语句,写语句与多语句会被拒绝),limit(默认100)/offset 截断返回,可选 `tx_handle` |
| `execute` | 执行任意 SQL(DDL/DML),返回受影响行数,可选 `tx_handle` |
| `insert_rows` | 参数化批量插入(表名 + 行数组,可选 schema) |
| `update_rows` | 参数化更新(set + where,where 必填防全表误更新,可选 schema) |
| `delete_rows` | 参数化删除(where 必填防全表误删除,可选 schema,destructive 标注) |

**事务(显式 handle 模式)**

| 工具 | 说明 |
|---|---|
| `transaction_begin` | 开启事务,返回 `tx_handle`(空闲 5 分钟自动回滚回收) |
| `transaction_commit` | 提交事务 |
| `transaction_rollback` | 回滚事务 |

用法:`transaction_begin` → 多次 `query`/`execute`(传入同一 `tx_handle`)→ `transaction_commit` 或 `transaction_rollback`。

**元数据(只读)**

| 工具 | 说明 |
|---|---|
| `list_databases` / `list_schemas` / `list_tables` | 库 / schema / 表清单 |
| `describe_table` | 列定义:类型、长度、可空、默认值、主键 |
| `list_indexes` / `list_views` / `list_sequences` | 索引 / 视图 / 序列清单 |

**诊断运维(只读)**

| 工具 | 说明 |
|---|---|
| `explain_query` | 执行计划;`analyze=true` 时真实执行并统计(自动事务回滚,写语句不落盘);拒绝含分号的多语句 |
| `list_sessions` | 当前活跃会话 |
| `list_lock_conflicts` | 锁冲突(被阻塞方与阻塞来源) |
| `database_stats` | 版本、库大小、连接数、服务器地址与时间 |

**用户与权限**

| 工具 | 说明 |
|---|---|
| `list_users` | 用户清单(只读) |
| `create_user` | 创建可登录用户 |
| `grant_privilege` / `revoke_privilege` | 授权 / 回收(如 `ALL ON DATABASE d`) |

**资源**

| 资源 URI | 说明 |
|---|---|
| `gaussdb://{schema}/{table}/schema` | 以 JSON 读取表结构 |

## MCP 客户端接入

构建后在客户端配置文件中注册(以 Claude Desktop / Cursor 的 `mcpServers` 格式为例)。Windows 用双反斜杠路径(`E:\\MCP\\GaussDBMCP\\build\\index.js`),Linux/macOS 用正斜杠(`/home/user/GaussDBMCP/build/index.js`)。

### 内网连接接入

```json
{
  "mcpServers": {
    "gaussdb": {
      "command": "node",
      "args": ["E:\\MCP\\GaussDBMCP\\build\\index.js"],
      "env": {
        "GAUSSDB_HOST": "10.0.1.11",
        "GAUSSDB_PORT": "8000",
        "GAUSSDB_DATABASE": "postgres",
        "GAUSSDB_USER": "root",
        "GAUSSDB_PASSWORD": "你的密码"
      }
    }
  }
}
```

内网连接不需要 SSL,不设置任何 `GAUSSDB_SSL_*` 变量即可。

### 公网连接接入

```json
{
  "mcpServers": {
    "gaussdb": {
      "command": "node",
      "args": ["E:\\MCP\\GaussDBMCP\\build\\index.js"],
      "env": {
        "GAUSSDB_HOST": "114.114.114.114",
        "GAUSSDB_PORT": "8000",
        "GAUSSDB_DATABASE": "postgres",
        "GAUSSDB_USER": "root",
        "GAUSSDB_PASSWORD": "你的密码",
        "GAUSSDB_SSL": "1",
        "GAUSSDB_SSL_CA": "C:\\path\\to\\root.crt",
        "GAUSSDB_SSL_REJECT_UNAUTHORIZED": "true"
      }
    }
  }
}
```

公网连接必须开启 SSL 并配置 CA 证书,并确保安全组放行客户端出口 IP 的 8000 端口。

也可不传 `env`,依赖项目根目录下 `.env` 文件(服务器启动时自动读取,锚定项目根,与启动目录无关)。

## 多租户隔离(stream = schema)

`GAUSSDB_SEARCH_PATH` 同时充当 **MCP 层 schema 白名单**:配置后访问被限制在对应 stream 自己的 schema 内,看不到其他 stream 的表。

**MCP 层拦截**(可靠,靠结构参数):

- `list_schemas` 只返回白名单内的 schema,不泄露其他 schema 名
- `list_tables`/`list_indexes`/`list_views`/`list_sequences` 不传 schema 时**默认钉到首个白名单 schema**,不再返回全库表
- `describe_table`/`insert_rows`/`update_rows`/`delete_rows` 显式传 `schema` 时,若不在白名单内直接报错拒绝
- 表结构资源 `gaussdb://{schema}/{table}/schema` 同样受白名单约束,跨 schema 读取被拒

**数据库权限层兜底**(必需,不可省):`execute` 是任意 SQL,MCP 层不做 SQL 解析(手写解析器必有绕过路径);`query` 虽强制只读(首关键字白名单 + 写关键字黑名单 + 拒绝多语句),但 SELECT 形式的有副作用函数(如 `pg_terminate_backend`、`setval`)无法穷举拦截。跨 schema 访问与副作用函数由 GaussDB 权限保证。每个 stream 用独立受限账号,只授权自己的 schema:

```sql
-- 以管理员执行:为 stream 建受限账号,只授予自己 schema 的权限
CREATE USER gycwd_app WITH PASSWORD 'xxx' LOGIN;
REVOKE ALL ON DATABASE postgres FROM PUBLIC;            -- 收紧库级默认权限
GRANT CONNECT ON DATABASE postgres TO gycwd_app;
GRANT USAGE ON SCHEMA gycwd TO gycwd_app;               -- 只给自己的 schema
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA gycwd TO gycwd_app;
-- 该账号未授予其他 schema 的 USAGE,即使手写跨 schema SQL 也会被数据库拒绝
```

然后 `.env` 里 `GAUSSDB_USER=gycwd_app`、`GAUSSDB_SEARCH_PATH=gycwd`,两层叠加:结构入口 MCP 拦、任意 SQL 数据库拦。

## 安全说明

- stdio 服务器日志全部写 stderr,stdout 仅承载 MCP 消息
- 结构化工具(insert_rows/update_rows/delete_rows 等)的表名/列名/用户名等标识符均做字符校验,值一律走参数化占位符,防 SQL 注入;`query`/`explain_query` 为自由 SQL 入口,靠只读校验与单语句限制收窄(见上)
- `delete_rows`/`update_rows` 强制要求 where 条件
- `explain_query` 的 analyze=true 真实执行语句,仅允许 SELECT/WITH 开头并自动包裹事务回滚(序列推进、函数副作用不可回滚)
- `DROP`/`TRUNCATE` 等语句可通过 `execute` 执行,客户端请依赖 destructiveHint 注解做确认
- 请勿将 `.env` 提交到版本库

## 开发与构建

```bash
npm run build   # tsc 编译到 build/
```

源码结构:`src/config.ts`(配置)、`src/db.ts`(连接池与事务句柄)、`src/sql.ts`(SQL 构造与只读校验)、`src/format.ts`(结果格式化)、`src/index.ts`(MCP 服务器与工具注册)。

拿到真实 GaussDB 实例后:填写 `.env` → `npm run build` → `node build/index.js` 配合任意 MCP 客户端实测;或先单独验证连接:配置 env 后运行 `test_connection` 工具。
