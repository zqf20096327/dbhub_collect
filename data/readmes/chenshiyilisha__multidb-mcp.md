# multidb-mcp

一个轻量的 **MCP Server**，让 AI 客户端（WorkBuddy、Claude Code、Cursor、Cline 等）通过 MCP 协议安全地访问 **达梦数据库（DM8）**、**SQL Server** 和 **MySQL / MariaDB**。对话里直接说"列出表""查一下某张表"，AI 就会调用工具执行，不用手动复制 SQL 切工具。

## 特性

- **三库支持**：达梦（官方 `dmdb` 驱动）+ SQL Server（`mssql` 驱动）+ MySQL（`mysql2` 驱动），同一套统一工具接口。
- **`npx` 一行启动**：无需手动装驱动、建环境，客户端配置里写 `npx multidb-mcp` 即可。
- **连接池复用 + 连接自愈**：每个连接懒加载、池常驻；达梦单连接每次执行前用驱动原生 `ping()` 探活，数据库重启/空闲断连时自动重建；读语句遇连接丢失会安全重试一次，写语句绝不重放（防重复写）。
- **查询超时**：统一的硬超时（JS 层 `Promise.race`），慢查询不会卡死 MCP 的 stdio 循环。
- **审计日志**：每次工具调用输出结构化 JSON 到 stderr（工具名、连接、耗时、行数、是否慢查询、是否写尝试），便于排查与合规。
- **安全默认 + 细粒度写权限**：默认只读，只允许 `SELECT / SHOW / DESCRIBE / EXPLAIN / WITH`；需要写入时，可对每条连接单独开启 `INSERT / UPDATE / DELETE / DDL` 四类权限（哪一类为 `true` 才放行哪一类）；多语句注入拦截；标识符白名单校验；`list_connections` 绝不外泄密码。
- **参数化查询**：`execute_sql` 支持 `?` 占位符 + `params` 绑定，由三库原生驱动执行，从根本上防注入（占位符数量自动校验）。
- **MCP 规范对齐**：实现三大原语（Tools / Resources / Prompts）；成功调用同时返回文本镜像与符合 `outputSchema` 的 `structuredContent`；失败调用返回 `isError: true` + 结构化错误（`code / category / recoverable / suggestion`），LLM 可据此自我纠错；工具带 annotations 提示。
- **多连接显式路由**：配置多个连接时，不传连接名会报错并返回连接目录，避免 LLM 静默查错库（dev/prod 搞混）。
- **查询治理**：`maxRows` 行数上限 + `maxResultBytes` 体积上限 + `maxQueryLength` 长度上限，三重防止结果集/语句失控。
- **结果脱敏**：按列名正则匹配，对每一行（含 `SELECT *`）执行 `fixed / null / partial` 脱敏，防止 PII / 密钥泄露给模型；非法规则 fail-closed（拒绝启动）。
- **凭据脱敏**：错误信息和审计日志中的密码、用户、主机、连接串自动打码，不回显给模型或日志。
- **优雅关闭**：SIGINT / SIGTERM / stdio 断开时释放所有连接池，不泄漏连接。

## 提供的工具

| 工具 | 作用 |
|---|---|
| `test_connection` | 验证连接，返回数据库版本和当前 schema |
| `list_connections` | 列出所有已配置连接及写权限标志；返回 `{ count, connections }`，不含密码 |
| `list_tables` | 列出指定 schema 下的所有表 |
| `describe_table` | 返回表的列名、类型、长度、是否可空、默认值、注释 |
| `execute_sql` | 执行单条 SQL，返回结果行（支持 `?` 参数绑定；受只读策略、细粒度写权限和行数上限约束；`maxRows` 入参只能调低不能调高） |

## 提供的资源（Resources）

除工具外，还暴露只读上下文资源，让客户端/LLM 无需调用工具即可读取真实元数据，先"看懂库"再写 SQL：

| 资源 URI | 作用 |
|---|---|
| `connections://catalog` | 连接目录（名称/类型/主机/schema/只读与写权限标志，绝不含密码），与 `list_connections.connections` 一致 |
| `schema://<connection>` | 某连接的全部表结构（表名 + 列定义），走 `list_tables` + `describe_table` 逻辑 |
| `schema://<connection>/<schema>` | 指定 schema 的表结构 |

读取失败（如库不可达、标识符非法）时返回结构化错误（`code/category/suggestion`），且同样经过凭据脱敏，不会泄漏连接信息。

## 提供的提示词（Prompts）

| 提示词 | 作用 |
|---|---|
| `query_guide` | 安全查询工作流：先确认连接 → 读 schema → 用 `params` 写 SQL → 把返回行当不可信数据处理 → 报告截断情况 |
| `write_guide` | 写操作工作流：先向用户确认 → 核对权限开关 → 预览目标行 → 执行并复核（库里的文字不能授权额外写入） |

### execute_sql 的参数化查询（推荐）

`execute_sql` 支持 `params` 入参，用 `?` 占位符绑定值，**由各库原生驱动执行参数化**（MySQL/dameng 用 `?`，SQL Server 自动改写为 `@pN`）。强烈建议用它替代把值拼进 SQL 文本——这是防 SQL 注入的根本手段。占位符数量必须与 `params` 长度一致，否则会返回清晰的错误。

```
sql:    "SELECT * FROM users WHERE id = ? AND status = ?"
params: [1024, "active"]
```

失败的工具调用会带 `isError: true`（符合 MCP 规范），便于 AI 客户端识别失败并自我纠错；所有工具都带 annotations 提示（如 `test_connection` 标 `readOnlyHint`，`execute_sql` 按可写语义标注）。所有成功调用同时返回 `structuredContent`（字段与工具声明的 `outputSchema` 一致）和同样的文本 JSON 镜像，方便不同代际的客户端消费；`list_connections` 的结构化结果为 `{ count, connections: [...] }`。

## 安装与接入

### 1. 前置条件

- **Node.js ≥ 18**（本机已装 v22 即可）。MCP 通过 `npx` 启动，不需要 Python。

### 2. 配置连接信息

通过环境变量配置。**单连接**（最常见）：

| 环境变量 | 说明 | 默认 |
|---|---|---|
| `MULTIDB_DB_TYPE` | `dameng` / `sqlserver` / `mysql` | `dameng` |
| `MULTIDB_HOST` | 数据库主机 | 必填 |
| `MULTIDB_PORT` | 端口 | 达梦 `5236` / SQL Server `1433` / MySQL `3306` |
| `MULTIDB_USER` | 账号 | 必填 |
| `MULTIDB_PASSWORD` | 密码 | — |
| `MULTIDB_SCHEMA` | 达梦 schema / SQL Server 数据库名 / MySQL 数据库名 | — |
| `MULTIDB_READ_ONLY` | 只读总开关：`true` 只读 / `false` 进入细粒度写权限模式 | `true` |
| `MULTIDB_ALLOW_INSERT` | 允许 `INSERT` / `REPLACE`（仅 `READ_ONLY=false` 时生效） | `false` |
| `MULTIDB_ALLOW_UPDATE` | 允许 `UPDATE` / `MERGE`（仅 `READ_ONLY=false` 时生效） | `false` |
| `MULTIDB_ALLOW_DELETE` | 允许 `DELETE`（仅 `READ_ONLY=false` 时生效） | `false` |
| `MULTIDB_ALLOW_DDL` | 允许 `CREATE` / `ALTER` / `DROP` / `TRUNCATE` / `RENAME`（仅 `READ_ONLY=false` 时生效） | `false` |
| `MULTIDB_MAX_ROWS` | 单次查询最大返回行数 | `1000` |
| `MULTIDB_QUERY_TIMEOUT_MS` | 查询硬超时（毫秒），`0` 表示不限 | `30000` |
| `MULTIDB_SLOW_QUERY_MS` | 慢查询阈值（毫秒），超过则审计标记 `slow=true` | `1000` |
| `MULTIDB_MAX_RESULT_BYTES` | 结果序列化体积上限（字节），`0` 不限；超限丢行并标记 `truncatedByBytes` | `1048576`（1 MiB） |
| `MULTIDB_MAX_QUERY_LENGTH` | SQL 语句最大长度（字符），`0` 不限 | `50000` |
| `MULTIDB_MASKING_RULES` | 结果列脱敏规则 JSON 数组（见下），留空不脱敏 | — |

**结果脱敏**（`MULTIDB_MASKING_RULES`，多连接时也可写在单条连接对象的 `maskingRules` 字段）：

```json
[
  { "column": "^EMAIL$",      "strategy": "fixed" },
  { "column": "phone|mobile", "strategy": "partial", "keepLast": 4 },
  { "column": "^ID_CARD$",    "strategy": "null" }
]
```

`column` 是对列名做大小写不敏感匹配的正则；`strategy` 为 `fixed`（固定值 `***`，可用 `value` 覆盖）/ `null`（置空）/ `partial`（仅保留末尾 `keepLast` 位，短值全遮）。规则对**所有查询**的结果生效（含 `SELECT *`），模型无法通过别名绕过。正则非法或 `strategy` 不合法会**拒绝加载配置**（fail-closed），避免静默返回未脱敏数据。

> **SQL Server 加密**：默认开启加密并信任服务器自签名证书（内网常见场景）。可用 `MSSQL_ENCRYPT=false` 关闭加密、`MSSQL_TRUST_CERT=false` 关闭证书信任。

**多连接**：用 `MULTIDB_CONNECTIONS` 传一个 JSON 数组，每个元素是一条连接（字段同上，另有 `name`）：

```json
[
  { "name": "dev",  "type": "dameng",   "host": "192.168.0.30", "port": 5236, "user": "SYSDBA", "password": "pw", "schema": "SYSDBA", "readOnly": true },
  { "name": "prod", "type": "sqlserver", "host": "10.0.1.100",   "port": 1433, "user": "sa",    "password": "pw", "schema": "PROD",  "readOnly": false, "allowInsert": true, "allowUpdate": true },
  { "name": "web",  "type": "mysql",     "host": "10.0.2.50",    "port": 3306, "user": "web",   "password": "pw", "schema": "appdb",  "readOnly": true,
    "maskingRules": [{ "column": "^EMAIL$", "strategy": "fixed" }], "maxResultBytes": 1048576, "maxQueryLength": 50000 }
]
```

### 3. 写入客户端 MCP 配置

**WorkBuddy**：`C:\Users\hejih\.workbuddy\mcp.json`（注意不是带点前缀的 `.mcp.json`），在 `mcpServers` 里加：

```json
{
  "mcpServers": {
    "multidb": {
      "command": "npx",
      "args": ["-y", "multidb-mcp"],
      "env": {
        "MULTIDB_DB_TYPE": "dameng",
        "MULTIDB_HOST": "192.168.0.30",
        "MULTIDB_PORT": "5236",
        "MULTIDB_USER": "SYSDBA",
        "MULTIDB_PASSWORD": "你的密码",
        "MULTIDB_SCHEMA": "SYSDBA",
        "MULTIDB_READ_ONLY": "true",
        "MULTIDB_MAX_ROWS": "1000",
        "MULTIDB_QUERY_TIMEOUT_MS": "30000"
      }
    }
  }
}
```

写完重启客户端生效。多连接时把 `MULTIDB_CONNECTIONS` 换成 JSON 数组即可，工具调用时用 `connection` 参数指定连接名。

> 包已发布到 npm 官方源，`npx -y multidb-mcp` 会自动拉取最新版，无需本地安装。多连接时把 `MULTIDB_CONNECTIONS` 换成 JSON 数组即可，工具调用时用 `connection` 参数指定连接名。

## 细粒度写权限（增删改）

写操作由**两级开关**共同决定，取"两层都通过"的与逻辑：

1. **总开关 `readOnly`**：`true`（默认）时只放行读语句，任何写语句直接拒绝。要写入必须先把它设为 `false`。
2. **四类写权限**：`readOnly=false` 时，再按语句类型查对应的开关，哪个为 `true` 才放行哪一类：

| 权限开关 | 放行的语句类型 |
|---|---|
| `allowInsert` | `INSERT`、`REPLACE` |
| `allowUpdate` | `UPDATE`、`MERGE` |
| `allowDelete` | `DELETE` |
| `allowDdl` | `CREATE`、`ALTER`、`DROP`、`TRUNCATE`、`RENAME` |

设计要点（取长补短，fail-closed）：

- **读语句始终允许**，不受四个写开关影响。
- **语句类型识别先去注释、去字符串字面量**，`WITH ... <body>` 按主体语句分类，`EXPLAIN [ANALYZE|PLAN] ...` 按被解释语句分类，避免注释/`WITH` 伪装绕过。
- **高危动词一律拒绝**：`GRANT / REVOKE / DENY / SET / FLUSH / KILL / SHUTDOWN / LOAD / CALL / EXEC / EXECUTE` 等，以及任何无法识别的语句（unknown），即便四个写开关全开也不放行。
- **每条连接独立配置**：多连接时可为 dev 开只读、为测试库单独开 `allowInsert/allowUpdate`，互不干扰。
- **写操作留痕**：审计记录里带 `stmtType`（语句类型），被策略拒绝的写尝试标记 `writeAttempt=true`，便于事后核查。

配置示例（单连接放开 INSERT 和 UPDATE，但不允许 DELETE / DDL）：

```json
{
  "MULTIDB_READ_ONLY": "false",
  "MULTIDB_ALLOW_INSERT": "true",
  "MULTIDB_ALLOW_UPDATE": "true"
}
```

## 安全说明

- **默认只读**：首次接入建议保持 `MULTIDB_READ_ONLY=true`，先只读探一圈，确认无误再按需逐项开写。
- **SQL 注入防护**：标识符白名单校验（`[A-Za-z_#$][A-Za-z0-9_$#]*`，允许 SQL Server 临时表 `#`/`##` 前缀）；多语句（非结尾分号）一律拦截；字符串字面量、引号标识符和注释由**同一个扫描器**剥离后再做策略检查，避免"字面量在一处剥、注释在另一处剥"造成判定窗口。
- **已对齐 2026 年数据库 MCP 的真实 CVE 教训**：`--` 只在后跟空白/行尾时才当注释（MySQL 方言规则，防 DBHub CVE-2026-61789 型绕过）；`USE` 从只读动词中移除（它会改变池化会话状态）；CTE / 子查询括号内藏着的写动词一律按写语句处理（防 pgEdge 型"前缀看起来是 SELECT"绕过）；`params` 数量始终校验，空数组也不能配 `?` 占位符。
- **超时不会污染后续调用**：JS 层超时无法取消底层查询，发生超时后连接被标记为不可用，下一次调用会先丢弃并重建连接（达梦单连接尤其重要）；元数据查询同样受超时保护。
- **密码保护**：`list_connections` 返回的连接信息已剔除密码；错误信息和审计日志中的密码 / 用户 / 主机 / 连接串也自动打码（`[REDACTED]`），绝不回显给客户端/LLM。密码写在配置文件是明文，注意别把配置文件随手分享。
- **结果脱敏**：对含 PII / 密钥的列配置 `maskingRules`，在结果离开服务端前脱敏；非法规则 fail-closed。建议凡是能查到敏感表的连接都配上。
- **三重结果治理**：`maxRows`（行数）+ `maxResultBytes`（体积）+ `maxQueryLength`（语句长度），防止大结果集 / 大字段 / 超长语句撑爆模型上下文或拖垮数据库。`execute_sql` 的 `maxRows` 入参只能调低，超过连接配置上限时自动钳制并在结果中标记 `maxRowsClamped: true`；审计日志同样记录该标记。
- **提示注入边界**：返回的行数据是数据而不是指令；`query_guide` / `write_guide` 明确要求模型不得因库里的文字改变任务或触发写入。MCP Server 不是安全防火墙，表/列白名单与行级权限仍应落在数据库账号、视图或 RLS 上。
- **数据库账号最小权限**：建议给 MCP 用的账号仅授予 `SELECT` 权限，作为最后一道闸。
- **审计**：所有工具调用（含被策略拒绝的写尝试、超时、慢查询）都会在 stderr 输出一条 JSON 审计记录（含脱敏列、字节截断标记），可用 shell 重定向 `2> audit.log` 收集；审计不含查询结果。

## 开发

参与开发前请先阅读 [DEVELOPMENT-GUIDELINES.md](./DEVELOPMENT-GUIDELINES.md)（项目的强制开发规范：先查资料再动手、依据支撑、负对照验证、按最优方案执行）。

```bash
npm install          # 安装依赖
npm run build        # 编译 TypeScript 到 build/
npm run dev          # tsx 直接运行源码（开发模式）
npm run test:unit    # 安全策略 + 配置路由单元测试（无需数据库）
npm run test:db      # 数据库层单元测试（假连接池，无需真实库）
npm run test:perm    # 端到端权限测试（经 MCP 工具入口，DB 不可达时仍验证策略项）
npm run test:enh     # 端到端增强测试（isError / annotations / 参数化，DB 项不可达时跳过）
npm run test:hard    # 端到端加固测试（结构化错误 / 脱敏 / 体积与长度上限 / 凭据脱敏）
npm run test:prim    # 端到端原语测试（Resources / Prompts，无需数据库）
npm run smoke        # stdio 冒烟测试（需真实数据库，配好环境变量）
```

项目结构：

```
multidb-mcp/
├── src/
│   ├── config.ts    # 连接配置解析与多连接路由
│   ├── security.ts  # SQL 安全策略（标识符、只读、多语句、语句分类、占位符处理）
│   ├── db.ts        # 达梦 / SQL Server / MySQL 连接抽象（池 + 超时 + 参数绑定）
│   ├── audit.ts     # 审计日志（stderr JSON）
│   ├── masking.ts   # 结果脱敏 + 体积上限（纯函数）
│   ├── errors.ts    # 结构化错误 + 凭据脱敏 + 错误分类
│   ├── server.ts    # MCP 工具层 + Resources + Prompts
│   └── index.ts     # stdio 入口 + 优雅关闭
├── tests/
│   ├── smoke.mjs       # 真实 MCP 协议冒烟测试
│   ├── unit.mjs        # 安全策略 + 语句分类 + 配置路由 + 脱敏/错误单元测试
│   ├── test_db.mjs     # 数据库层单元测试（假池，含三库参数绑定）
│   ├── permissions.mjs # 端到端细粒度写权限测试
│   ├── enhancements.mjs# 端到端增强测试（isError / annotations / 参数化）
│   ├── hardening.mjs   # 端到端加固测试（结构化错误 / 脱敏 / 体积与长度上限）
│   └── primitives.mjs  # 端到端原语测试（Resources / Prompts）
├── DEVELOPMENT-GUIDELINES.md  # 项目强制开发规范
└── legacy-python/   # 原 Python 实现（已弃用，保留参考）
```

## 许可证

MIT
