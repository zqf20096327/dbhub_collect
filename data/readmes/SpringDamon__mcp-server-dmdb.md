# mcp-server-dmdb

达梦 DM8 的 MCP server，基于官方 `dmdb` Node.js 驱动，用 TypeScript 实现。默认**纯只读**，写操作与改表结构分别由环境变量开关控制，未开启时对应工具根本不会注册。

## 安装

```bash
npm install -g mcp-server-dmdb@latest     # 全局安装最新版
npx -y mcp-server-dmdb@latest             # 或按需临时拉取最新版，不落盘
```

`@latest` 始终拉取 npm 上**最新的已发布版本**（每次 `npm publish` 后自动生效），不锁具体版本号。

要求 Node >= 20（ESM only），无原生编译步骤。

## 接入 MCP 客户端

在客户端的 MCP 配置里加一条：

```json
{
  "mcpServers": {
    "dmdb-dev": {
      "command": "npx",
      "args": ["-y", "mcp-server-dmdb@latest"],
      "env": {
        "DM_HOST": "your-host",
        "DM_PORT": "5236",
        "DM_USER": "your-user",
        "DM_PASSWORD": "your-password",
        "DM_SCHEMA": "your-schema",
        "DM_ALLOW_WRITE": "false",
        "DM_ALLOW_DDL": "false"
      }
    }
  }
}
```

> **Windows 注意**：MCP 客户端用 Win32 `spawn` 启动进程，`npx` 是 `.cmd` 包装脚本，常解析失败而表现为"客户端静默无响应"。建议改成直接指向 `node.exe` 和已安装包的绝对路径：
>
> ```json
> {
>   "command": "C:/Program Files/nodejs/node.exe",
>   "args": ["C:/Users/<you>/AppData/Roaming/npm/node_modules/mcp-server-dmdb/dist/index.js"]
> }
> ```
>
> 先 `npm install -g mcp-server-dmdb@latest` 装最新版，再用 `npm root -g` 确认上方路径。Linux / macOS 上 `npx` 写法没问题。

## 使用

1. 按上文配好 `DM_*` 连接信息。
2. 客户端以 stdio 方式启动本进程，自动完成 `initialize` 握手并拉取 `tools/list`。
3. 调用工具：默认 9 个只读工具；设 `DM_ALLOW_WRITE=true` 出现 `dm_execute_dml`，再设 `DM_ALLOW_DDL=true` 出现 `dm_execute_ddl`，共 11 个。
4. 排查连接：先用 `dm_ping` 确认连通性与两个写开关的运行时状态。

> 进程以本地子进程方式运行，凭据通过环境变量注入，**不监听任何网络端口**，无外部鉴权面。

## 支持的 MCP 协议

本 server 兼容 **MCP（Model Context Protocol）2025-era 规范**，基于官方 TypeScript SDK v2 实现。

| 维度 | 说明 |
|---|---|
| 传输方式 | **stdio**（标准输入/输出）。stdout 为 JSON-RPC 2.0 通道，所有日志走 stderr，避免污染协议流导致客户端静默卡死 |
| SDK | `@modelcontextprotocol/server` **v2**（`^2.0.0`），ESM-only |
| 协议版本 | `protocolVersion = 2025-06-18`（legacy `initialize` 握手）。**未启用** 2026-07-28 的 opt-in 新协议，以保证与现有客户端（WorkBuddy / CodeBuddy / Claude Desktop 等）兼容 |
| 能力声明 | 仅 **`tools`**。未声明 `resources` / `prompts` / `logging`（日志直接写 stderr） |
| 工具调用 | JSON-RPC `tools/call`；每个工具带 `title`（人类可读标题）、`inputSchema`（zod v4 生成）；部分带 `outputSchema` 并回传 `structuredContent`（结构化 JSON，便于客户端解析） |
| 结果格式 | 以 `content` 数组（text）回传，并附带 `structuredContent`；超长单元格/总字符数按环境变量三层截断 |
| 连接模型 | 每次 stdio 连接对应一个独立 `McpServer` 实例（factory 模式）；数据库连接**懒加载**，启动不触网，故 `tools/list` 即使库不可达也能立即返回 |
| 生命周期 | 捕获 `SIGINT` / `SIGTERM`，关闭连接池后退出；未捕获异常与 Promise 拒绝落 stderr，不致命 |

### 兼容性边界

- **支持**：stdio 传输、2025-06-18 握手、工具发现与调用、结构化输出（`outputSchema` / `structuredContent`）。
- **不支持**：
  - SSE / Streamable HTTP 传输（仅 stdio）；
  - OAuth 等网络鉴权（凭据由环境变量注入，进程本地运行，不暴露端口）；
  - 资源（`resources`）订阅、提示模板（`prompts`）、服务端主动日志推送（`logging` 通知）。

## 环境变量

| 变量 | 默认值 | 说明 |
|---|---|---|
| `DM_HOST` | `127.0.0.1` | 数据库地址 |
| `DM_PORT` | `5236` | 端口 |
| `DM_USER` | *必填* | 用户名 |
| `DM_PASSWORD` | *必填* | 密码 |
| `DM_SCHEMA` | 无 | 登录 schema |
| **`DM_ALLOW_WRITE`** | `false` | 开启 `dm_execute_dml` |
| **`DM_ALLOW_DDL`** | `false` | 开启 `dm_execute_ddl` |
| `DM_MAX_ROWS` | `100` | 单次返回行数上限 |
| `DM_MAX_ROWS_HARD` | `1000` | 硬顶，`DM_MAX_ROWS` 不会超过它 |
| `DM_CELL_CHAR_LIMIT` | `200` | 单个单元格字符上限 |
| `DM_TOTAL_CHAR_LIMIT` | `24000` | 单次响应总字符上限 |
| `DM_CONNECT_TIMEOUT_MS` | `10000` | 连接超时 |
| `DM_SOCKET_TIMEOUT_MS` | `60000` | 网络超时（驱动原生） |
| `DM_QUERY_TIMEOUT_MS` | `30000` | JS 层兜底超时，触发即丢弃并重建连接 |
| `DM_PING_TIMEOUT_MS` | `3000` | 探活超时 |
| `DM_LOGIN_ENCRYPT` | 自动 | 见下文"连接加密" |
| `DM_LOG_LEVEL` | `ERROR` | `OFF`/`ERROR`/`WARN`/`INFO`/`DEBUG` |
| `DM_DICT_SCOPE` | `all` | `all` 用 `ALL_*` 视图；权限不足时改 `user` 用 `USER_*` |

## 工具清单

默认注册 9 个；`DM_ALLOW_WRITE=true` 加第 10 个；再开 `DM_ALLOW_DDL=true` 共 11 个。

| 工具 | 用途 | 开关 |
|---|---|---|
| `dm_ping` | 连接自检、服务端版本、实例信息、**两个写开关的当前状态** | — |
| `dm_list_schemas` | 列出可访问的模式 | — |
| `dm_list_tables` | 按模式 + 表名关键字列模糊搜表，带行数与表注释 | — |
| `dm_describe_table` | 列定义 + 主键/外键/唯一/检查约束 + 索引及包含列 + 注释 + 可选 DDL | — |
| `dm_query` | 只读 SELECT，绑定参数 | — |
| `dm_table_sample` | 采样看数据，自动处理标识符引号与大小写 | — |
| `dm_table_count` | 精确 `COUNT(*)`（也可用统计估算值） | — |
| `dm_explain` | 执行计划 | — |
| `dm_search_objects` | 按关键字搜表名/列名/列注释（支持中文注释） | — |
| `dm_execute_dml` | INSERT / UPDATE / DELETE，结构化入参 | `DM_ALLOW_WRITE` |
| `dm_execute_ddl` | CREATE / ALTER / DROP | `DM_ALLOW_DDL` |

## 安全边界

SQL 语句必须连续通过五层检查才会执行，任一层失败即拒绝：

1. **归一化** —— 词法扫描剥离注释（不误伤字符串字面量内的 `--` 和 `/* */`）
2. **顶层切分** —— 分号必须位于末尾，否则拒绝。**服务端本身不拦多语句**：`SELECT 1; SELECT 2` 会被归类为 PL/SQL 块，只能靠这一层
3. **关键字黑名单** —— 在已抹平字符串字面量的文本上按词边界匹配
4. **服务端判定** —— `getStatementInfo()` 返回的语句类型；异常或缺失一律 **fail-closed**
5. **交叉裁决** —— 第 3 层与第 4 层结论必须一致

**永久禁止**（任何开关状态下都不放行）：
`TRUNCATE`、`DROP DATABASE/USER/SCHEMA/TABLESPACE/ROLE`、`ALTER DATABASE/SYSTEM/SESSION`、`SHUTDOWN`、`GRANT`、`REVOKE`、`SP_*`、`SF_*`、`DBMS_*`、`EXECUTE IMMEDIATE`。

**DDL 额外三道锁**：
- 上面的永久黑名单
- `DROP TABLE/VIEW/INDEX/SEQUENCE` 与 `ALTER TABLE ... DROP COLUMN` 必须传 `confirm`，值严格等于 `DROP <对象名>`
- 每条 DDL 写审计日志（stderr，不受 `DM_LOG_LEVEL` 影响）

**DML 保护**：`update`/`delete` 强制要求 `where`；`autoCommit=false` 执行 → 超 `max_rows_affected` 即回滚，否则提交；建议先用 `dry_run=true` 统计命中行数。

> 达梦的 DDL 隐式提交，包不进事务，**无法回滚**。

## 已知行为与坑

### 连接加密默认关闭

`dmdb` 的 `loginEncrypt` 默认为 `true`，但其加密套件在 Node 17+ 的 OpenSSL 3 下会被拒绝：

```
errCode 6071 消息加密失败
error:0308010C:digital envelope routines::unsupported
```

所以默认改为 `false`（想强制加密可显式设 `DM_LOGIN_ENCRYPT=true`）。本驱动只暴露 `true`/`false`，不能指定套件。

### BIGINT 精度

DM8 的 `BIGINT` 主键普遍超过 2^53，驱动的默认 number 转换会**静默抹平末三位**：

```
真实值 1989221485636136962  ->  到达 JS 时变成 1989221485636137000
```

`fetchAsString: [dmdb.NUMBER]` 修不了——DM8 里 BIGINT 与 NUMBER 是不同类型。本实现在检测到不安全整数后，**只把出问题的那几列用字符串重读一次**，因此正常数值列仍是数字，而 ID 保持完整精度。

### 分页

DM8 原生支持 `LIMIT ? OFFSET ?` 且可绑定参数（官方实测执行计划优于 ROWNUM/TOP）。`dm_query` 要求分页写在 SQL 里、值放 `params`，服务端不做子查询包装——包装会包不住 `WITH` CTE。

### 执行计划要用 `EXPLAIN FOR`

裸 `EXPLAIN <sql>` 不返回结果集，只回 `rowsAffected`。必须用 `EXPLAIN FOR <sql>`。也因此 `EXPLAIN` 不接受绑定参数，`dm_explain` 会把 `params` 安全地内联为字面量。

### 行数统计

`ALL_TABLES.NUM_ROWS` 来自统计信息，多数库未收集，值为 `NULL`。**不要拿 `dm_list_tables` 里的 NUM_ROWS 当真实行数**，用 `dm_table_count`。

### 语句类型码

`getStatementInfo()` 返回的是达梦内部码，与 `dmdb` 自带 `.d.ts` 声明的 `STMT_TYPE_*`（声称 SELECT=1）**完全不同**。实测值：

| 语句 | 码 | 语句 | 码 |
|---|---|---|---|
| SELECT（含 FOR UPDATE） | 160 | DROP TABLE | 139 |
| INSERT | 157 | ALTER TABLE | 146 |
| UPDATE | 159 | TRUNCATE | 194 |
| DELETE | 158 | EXPLAIN | 149 |
| MERGE | 164 | COMMIT / ROLLBACK | 147 / 148 |
| CREATE TABLE | 129 | SET SCHEMA | 153 |
| CREATE VIEW / INDEX / SEQ | 131 / 133 / 196 | CALL / BEGIN / **多语句** | 162 |

`SELECT ... FOR UPDATE` 与普通 SELECT 同为 160，所以 `FOR UPDATE` 只能靠关键字拦截。

### 标识符大小写

实测环境中标识符**大小写不敏感**，`data_after_sale` 与 `DATA_AFTER_SALE` 都能命中。但这取决于服务端 `CASE_SENSITIVE` 参数，不是 DM8 的保证，所以字典查询一律用 `UPPER(...) = UPPER(?)` 比较。

## 开发

```bash
git clone https://github.com/SpringDamon/mcp-server-dmdb.git
cd mcp-server-dmdb
npm install
npm run build      # tsc -> dist/
npm test           # 构建 + node --test 跑门禁用例（43 条）
```

下面两个脚本要连真实库，凭据**只从环境变量读取**，缺失即报错（见 `scripts/env.mjs`）：

```bash
export DM_HOST=<host> DM_USER=<user> DM_PASSWORD=<pwd> DM_SCHEMA=<schema>
node scripts/probe-connect.mjs   # 验证数据库连通性
node scripts/verify-dict.mjs     # 导出字典视图真实列名
node scripts/e2e-mcp.mjs         # 端到端 JSON-RPC 验证（43 项检查）
```

## 依赖

运行时只有 3 个，刻意保持最小：

| 依赖 | 版本 | 说明 |
|---|---|---|
| `@modelcontextprotocol/server` | `^2.0.0` | MCP SDK v2，ESM-only。协议细节见上文「支持的 MCP 协议」 |
| `dmdb` | `1.0.52452` | 官方驱动，**精确锁版本**（非 semver，加 `^` 无意义）。CJS 包，只能用默认导入 |
| `zod` | `^4.5.2` | schema 校验 |

开发依赖：`typescript@^5.9.3`（**不用 7.x**——那是 Go 重写的 tsgo）、`@types/node@^22.19.1`。

不引入 ORM：达梦没有 Prisma/Drizzle/Knex/MikroORM 方言，社区 fork（`typeorm-dm`、`sequelize-dm8` 等）周下载量仅个位数到两位数且基座老旧。更重要的是场景错配——ORM 的价值是实体映射，而 MCP 是运行时动态发现 schema，Entity 模型完全用不上。

测试用 Node 22 内置 `node --test`，不引 jest/vitest。

## 附录：字典视图真实列名

以下在真实 DM8 实例上实测所得，与 Oracle 文档有出入，勿照搬 Oracle 经验：

| 视图 | 关键列 |
|---|---|
| `ALL_TABLES` | `OWNER, TABLE_NAME, TABLESPACE_NAME, NUM_ROWS, BLOCKS, STATUS, LAST_ANALYZED` |
| `ALL_TAB_COLUMNS` | `OWNER, TABLE_NAME, COLUMN_NAME, DATA_TYPE, DATA_LENGTH, DATA_PRECISION, DATA_SCALE, NULLABLE, COLUMN_ID, DATA_DEFAULT` |
| `ALL_CONSTRAINTS` | `OWNER, CONSTRAINT_NAME, CONSTRAINT_TYPE(P/R/U/C), TABLE_NAME, SEARCH_CONDITION, R_OWNER, R_CONSTRAINT_NAME, STATUS` |
| `ALL_CONS_COLUMNS` | `OWNER, CONSTRAINT_NAME, TABLE_NAME, COLUMN_NAME, **POSITION**` |
| `ALL_INDEXES` | `OWNER, INDEX_NAME, INDEX_TYPE, TABLE_OWNER, TABLE_NAME, UNIQUENESS, STATUS` |
| `ALL_IND_COLUMNS` | `INDEX_OWNER, INDEX_NAME, TABLE_OWNER, TABLE_NAME, COLUMN_NAME, **COLUMN_POSITION**, DESCEND` |
| `ALL_TAB_COMMENTS` | `OWNER, TABLE_NAME, TABLE_TYPE, COMMENTS` |
| `ALL_COL_COMMENTS` | `OWNER, TABLE_NAME, SCHEMA_NAME, COLUMN_NAME, COMMENTS` |
| `ALL_USERS` | `USERNAME, USER_ID, CREATED` |
| `V$VERSION` | `BANNER` |
| `V$INSTANCE` | `NAME, INSTANCE_NAME, SVR_VERSION, DB_VERSION, START_TIME, STATUS$` |

> 注意不对称：**索引位置列叫 `COLUMN_POSITION`，约束位置列叫 `POSITION`**。

`SP_TABLEDEF(schema, table)` 可用，返回 `COLUMN_VALUE` 列拼成的 DDL 文本。

## 目录结构

```
src/
├─ index.ts            stdout 保护 + serveStdio + 退出清理
├─ server.ts           createServer()：建 McpServer 并按需注册工具
├─ config.ts           环境变量解析
├─ log.ts              stderr-only 日志 + DDL/DML 审计
├─ db/
│  ├─ driver.ts        【唯一 import dmdb 的地方】CJS/ESM 互操作 + 真实语句类型码
│  ├─ connection.ts    懒加载/ping探活/毒化重连/mutex串行/大整数精确化重读
│  ├─ sql-guard.ts     五层门禁
│  ├─ identifiers.ts   标识符校验与引号
│  └─ types.ts
├─ tools/              register.ts（按开关注册）+ 每个工具一个文件
└─ format/             序列化 / 三层截断 / markdown 渲染
scripts/               env.mjs（凭据校验）+ probe-connect / verify-dict / e2e-mcp
```

## License

[MIT](./LICENSE)
