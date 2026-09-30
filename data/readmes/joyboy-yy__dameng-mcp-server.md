# DM8 MCP Server

为 Claude Code、Codex 等 AI Agent 提供达梦 DM8 数据库查询能力的 MCP Server。

通过 **JDBC 桥接**（jaydebeapi + DmJdbcDriver）连接数据库，无需安装达梦客户端。

## 功能

- 通过 MCP stdio 协议暴露 DM8 查询工具。
- 支持任意 SQL 查询和 DM8 元数据浏览。
- 自动检测失效连接并在下次调用时重连。
- 元数据工具会校验 schema/table 标识符，降低 SQL 拼接风险。

## 安装

```bash
pip install -e .
```

安装后也会注册命令行入口：

```bash
dm8-mcp-server
```

## JDBC 驱动

本仓库不包含达梦 JDBC 驱动 jar。请从达梦数据库安装包或官方渠道获取 `DmJdbcDriver18-8.1.3.62.jar`，然后任选一种方式配置：

```bash
export DM_JDBC_JAR=/path/to/DmJdbcDriver18-8.1.3.62.jar
```

或将 jar 放到项目根目录的 `lib/DmJdbcDriver18-8.1.3.62.jar`。`lib/*.jar` 已被 `.gitignore` 忽略，请不要提交驱动二进制文件。

## 配置

在 Claude Code 项目根目录的 `.mcp.json` 中添加。建议只保留 `dm8-server` 一个名称，避免同一数据库能力重复注册：

```json
{
  "mcpServers": {
    "dm8-server": {
      "command": "python",
      "args": ["-m", "dm8_mcp_server"],
      "env": {
        "DM_HOST": "你的DM8主机地址",
        "DM_PORT": "5236",
        "DM_USER": "用户名",
        "DM_PASSWORD": "密码",
        "DM_SCHEMA": "默认Schema名",
        "DM_JDBC_JAR": "/path/to/DmJdbcDriver18-8.1.3.62.jar"
      }
    }
  }
}
```

也可以使用安装后的入口命令：

```json
{
  "mcpServers": {
    "dm8-server": {
      "command": "dm8-mcp-server",
      "env": {
        "DM_HOST": "你的DM8主机地址",
        "DM_PORT": "5236",
        "DM_USER": "用户名",
        "DM_PASSWORD": "密码",
        "DM_SCHEMA": "默认Schema名",
        "DM_JDBC_JAR": "/path/to/DmJdbcDriver18-8.1.3.62.jar"
      }
    }
  }
}
```

### OpenCode

在 OpenCode 配置文件 `opencode.json` 或 `opencode.jsonc` 中添加：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "dm8-server": {
      "type": "local",
      "command": ["python", "-m", "dm8_mcp_server"],
      "enabled": true,
      "environment": {
        "DM_HOST": "你的DM8主机地址",
        "DM_PORT": "5236",
        "DM_USER": "用户名",
        "DM_PASSWORD": "密码",
        "DM_SCHEMA": "默认Schema名",
        "DM_JDBC_JAR": "/path/to/DmJdbcDriver18-8.1.3.62.jar"
      }
    }
  }
}
```

如果已经安装了命令行入口，也可以将 `command` 改为：

```json
["dm8-mcp-server"]
```

服务进程会在进入 stdio/asyncio 主循环前预启动 JPype JVM 和加载 JDBC 驱动，避免 Windows 下首次工具调用因延迟启动 JVM 而超时；数据库连接仍按需建立。连接默认带 `connectTimeout=5000` 和 `socketTimeout=30000` JDBC 参数；连接失效后会自动丢弃缓存连接，下次工具调用重新连接。

## 工具列表

| 工具名 | 参数 | 说明 |
|--------|------|------|
| `dm_query` | `sql` | 执行任意 SQL，返回 JSON 结果集 |
| `dm_list_tables` | `schema?` | 列出表名。不传=默认schema，`*`=全部schema |
| `dm_describe_table` | `table`, `schema?` | 查看表结构（字段/类型/注释等） |
| `dm_show_index` | `table`, `schema?` | 查看表索引 |
| `dm_table_count` | `table?`, `schema?` | 统计行数 |

说明：

- `dm_query` 保留执行任意 SQL 的能力，适合受信任的本地调试和运维场景。
- 元数据工具会校验 `schema` 和 `table` 标识符，只允许普通 DM/SQL 标识符，避免拼接查询被注入。
- 跨 schema 查询请在 `dm_query` 中使用 `SCHEMA.TABLE`。

## 技术栈

| 项 | 选择 | 原因 |
|----|------|------|
| 语言 | Python | MCP Python SDK 成熟 |
| 驱动 | JDBC (jaydebeapi) | JDBC 连接稳定，无需额外安装达梦客户端 |
| MCP SDK | `mcp` (官方) | 标准实现，stdio 通信 |
| 依赖管理 | pip / pyproject.toml | 标准方式 |

## 开发

```bash
pip install -e ".[dev]"
pytest tests/ -v
```

集成测试需要真实 DM8 连接和 JDBC 驱动。未设置连接环境变量时会自动跳过。

`tests/test_migrate.py` 是可选 DDL 迁移验证，默认不会执行 DDL。需要显式设置：

```bash
DM8_MCP_RUN_MIGRATION_TESTS=1 DM8_MCP_MIGRATION_SQL=/path/to/migration.sql pytest tests/test_migrate.py -v
```

## 安全说明

`dm_query` 会执行调用方传入的任意 SQL，包括写入和 DDL。建议仅在受信任的本地环境中使用，并为 MCP Server 配置最小权限数据库账号。

不要将真实数据库地址、账号、密码、私有 SQL 文件路径或 JDBC 驱动二进制文件提交到仓库。

## License

MIT
