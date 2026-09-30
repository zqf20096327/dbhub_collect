# dameng-mcp

Java 实现的达梦数据库 (DM8) MCP Server。基于官方 MCP Java SDK 2.0 + 达梦 JDBC 驱动,通过 stdio 与 Claude Code 等 MCP 客户端通信。

## 功能

只读 5 个工具(对齐 npm 的 mcp-dm8-server):

| 工具 | 说明 |
|------|------|
| `list_schemas` | 每个连接可访问的 schema 目录,跨连接同名 schema 警告 |
| `list_tables` | 指定连接 + Schema 下的所有表名 |
| `describe_table` | 列名、类型、长度、是否可空、列注释 (ALL_COL_COMMENTS) |
| `list_indexes` | 索引名、是否唯一、索引列及列序 (ALL_INDEXES + ALL_IND_COLUMNS) |
| `execute_query` | 只读 SQL(仅 SELECT/SHOW/DESCRIBE/EXPLAIN),支持 maxRows 截断 |

## 环境要求

- JDK 17+
- 无需安装 Maven(项目自带 `./mvnw`)

## 构建

```bash
./mvnw package
# 产物: target/dameng-mcp.jar(fat jar)
```

## 运行

```bash
java -jar target/dameng-mcp.jar [--config <path>]
# 标准做法是显式指定配置,见下;缺省读取工作目录下的 dm8-mcp.json
```

## 配置

真实连接配置**放在仓库之外**的 `~/.claude/dm8-mcp.json`(避免数据库密码入库),仓库内只提交 `dm8-mcp.json.example` 模板。格式与 mcp-dm8-server 一致:

```json
{
  "activeEnv": "dev",
  "environments": {
    "dev": {
      "connections": [
        {
          "name": "my-dm8",
          "host": "127.0.0.1",
          "port": 5236,
          "username": "SYSDBA",
          "password": "change-me",
          "schema": "SYSDBA",
          "default": true
        }
      ]
    }
  }
}
```

支持多连接;`default: true` 的连接作为缺省连接,工具调用时可用 `connection` 参数切换。

## 接入 Claude Code

在 `~/.claude/.mcp.json` 的 `mcpServers` 中加入(本机已配置好):

```json
{
  "mcpServers": {
    "dm8": {
      "command": "java",
      "args": ["-jar", "/Users/lem/IdeaProjects/dameng-mcp/target/dameng-mcp.jar", "--config", "/Users/lem/.claude/dm8-mcp.json"]
    }
  }
}
```

## 验证

```bash
# 用 MCP Inspector 交互调试
npx @modelcontextprotocol/inspector -- java -jar target/dameng-mcp.jar --config dm8-mcp.json
```
