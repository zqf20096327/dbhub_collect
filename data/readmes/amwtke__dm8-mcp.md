# dm-mcp-server

一个从零编写的 **Java + Spring Boot + 官方 MCP Java SDK + 达梦 DM8** 的本地 MCP Server。

适用场景：

- 给 Codex / Claude Desktop / Cursor 接入达梦数据库
- 做企业内部只读数据助手
- 做 schema 探查、SQL 问答、数据查询

---

## 1. 架构设计

```text
+--------------------+
| MCP Client         |
| Codex / Claude     |
+---------+----------+
          |
          | STDIO(JSON-RPC)
          v
+---------+----------+
| MCP Java SDK       |
| Stdio Transport    |
+---------+----------+
          |
          | Tool Call
          v
+---------+----------+
| Spring Boot        |
| Tool Handlers      |
| Database Service   |
+---------+----------+
          |
          | JDBC
          v
+---------+----------+
| Dameng DM8         |
+--------------------+
```

核心思路：

1. **客户端只看到 MCP Tools**，不知道 JDBC 细节。
2. **服务端只暴露只读能力**，先保证安全，再逐步扩展。
3. **schema / table / column 探查优先用 JDBC Metadata**，减少 DM 方言耦合。

---

## 2. 已实现工具

### `ping`
检查 MCP Server 与数据库连通性。

### `list_schemas`
列出允许访问的 schema。

### `list_tables`
列出某个 schema 下的表 / 视图。

参数：

```json
{
  "schema": "SYSDBA"
}
```

### `describe_table`
查看表结构。

参数：

```json
{
  "schema": "SYSDBA",
  "tableName": "USER_INFO"
}
```

### `execute_query`
执行只读查询，仅允许 `SELECT` / `WITH`。

参数：

```json
{
  "sql": "select * from SYSDBA.USER_INFO fetch first 20 rows only"
}
```

---

## 3. 安全设计

### 3.1 只读 SQL 守卫

项目内的 `SqlGuard` 做了三件事：

1. 只允许 `SELECT` / `WITH` 开头
2. 禁止多语句
3. 禁止常见 DDL / DML / 管理关键字

这不是完整 SQL Parser，但对 AI 驱动的数据库查询场景，足够作为第一道硬性闸门。

### 3.2 schema 白名单

通过 `app.database.allowed-schemas` 限制 AI 只能访问指定 schema。

### 3.3 连接池只读

Hikari 数据源设置了 `readOnly=true`。

> 注意：连接池只读不是绝对安全保证，真正的最终保障仍然应该是 **数据库账号本身只有 SELECT 权限**。

建议你专门创建一个：

- 只读账号
- 只开放指定 schema
- 禁止 DDL / DML / 存储过程执行权限

---

## 4. 运行前准备

### 4.1 JDK

要求 **JDK 17+**。

### 4.2 放置达梦 JDBC 驱动

仓库默认从项目根目录加载 `DmJdbcDriver18.jar`。确保该文件存在即可，无需再手工安装到本地 Maven 仓库。

```text
dm-mcp-server/
├── DmJdbcDriver18.jar
├── pom.xml
└── src/
```

如果你替换了驱动文件名或路径，需要同步修改 `pom.xml` 中的 `systemPath`。

---

## 5. 配置

修改 `src/main/resources/application.yml`：

```yaml
app:
  database:
    url: jdbc:dm://127.0.0.1:5236
    username: dm_readonly
    password: your_password
    driver-class-name: dm.jdbc.driver.DmDriver
    schema: APP_SCHEMA
    allowed-schemas:
      - APP_SCHEMA
    max-rows: 200
    query-timeout-seconds: 15
```

---

## 6. 本地启动

```bash
mvn clean package -DskipTests
java -jar target/dm-mcp-server-1.0.0.jar
```

因为这是 STDIO MCP Server，启动后会等待 MCP Client 通过标准输入输出与它通信。

---

## 7. Codex / Claude Desktop MCP 配置示例

### 7.1 通用 JSON 配置

```json
{
  "mcpServers": {
    "dm8": {
      "command": "java",
      "args": [
        "-jar",
        "/absolute/path/to/dm-mcp-server-1.0.0.jar"
      ]
    }
  }
}
```

### 7.2 如需外置配置文件

```json
{
  "mcpServers": {
    "dm8": {
      "command": "java",
      "args": [
        "-jar",
        "/absolute/path/to/dm-mcp-server-1.0.0.jar",
        "--spring.config.location=/absolute/path/to/application.yml"
      ]
    }
  }
}
```

---

## 8. 建议的后续增强

### 8.1 企业可落地增强

1. 增加 SQL 审计日志
2. 增加行数 / 时长 / schema 级限流
3. 增加敏感列脱敏
4. 增加表备注、字段备注增强解释
5. 增加 Prompt 模板，例如“先查表结构，再生成 SQL”

### 8.2 更进一步

你后续可以把它升级成：

- **多数据源 MCP Gateway**：达梦 + MySQL + PostgreSQL 共用一个 MCP Server
- **Spring Security + Token 鉴权**：用于 HTTP/Remote MCP
- **语义层**：把表、字段、业务口径做成 metadata/prompts/resources
- **AI BI**：在 Tool 之上叠加问数与解释链路

---

## 9. 为什么这样分层

```text
DmMcpApplication
  └── Spring Boot 应用入口

DataSourceConfig
  └── 负责 JDBC / Hikari 连接池

DatabaseExplorerService
  └── 负责 schema / table / query 等数据库能力

SqlGuard
  └── 负责只读安全限制

McpServerBootstrap
  └── 负责把数据库能力注册成 MCP Tools
```

这种拆法的好处：

- **MCP协议层** 与 **数据库实现层** 分离
- 将来从达梦换成 MySQL / TiDB / Oracle，只需要替换数据库访问层
- 将来从 STDIO 升级到 HTTP / Streamable HTTP，也只需要调整 transport 层

---

## 10. 已知说明

本工程源码是完整的，但由于达梦 JDBC 驱动通常需要你本地提供，所以在没有驱动 jar 的环境里无法直接打出最终可运行包。

也就是说：

- **工程结构、业务代码、MCP 接入方式已经完整**
- **最后一步编译运行依赖你本地补上达梦驱动**

这也是国产数据库项目里很常见的现实情况。
