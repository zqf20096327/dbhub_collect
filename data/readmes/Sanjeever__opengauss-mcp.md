# openGauss MCP Server

基于 Spring AI MCP Server 的 openGauss 数据库工具服务，支持通过 MCP 客户端以 `stdio` 方式连接，并调用数据库相关工具完成表结构查看、统计信息查询与 SQL 执行。

## 功能特性

- 基于 MCP 标准协议，支持 `stdio` 传输
- 内置 openGauss 数据库连接能力（JDBC）
- 提供 5 个数据库工具：
  - `list_tables`：列出当前 schema 下的表、视图、物化视图
  - `describe_table`：查看表结构（列、类型、主键、索引、注释、默认值）
  - `get_table_stats`：查看表统计信息（估算行数、分析时间、表大小、索引大小）
  - `run_select`：执行只读 SQL（仅 `SELECT / WITH / EXPLAIN`）
  - `execute_sql`：执行 DDL / DML SQL
- 对只读 SQL 做了语句类型与关键字校验，降低误写风险

## 环境要求

- JDK 17+
- Node.js 18+
- openGauss 数据库（可访问）

## 快速开始

### 1) 配置 MCP 客户端

该服务使用 `stdio`，客户端通常通过命令启动方式接入。

```json
{
  "mcpServers": {
    "opengauss": {
      "command": "npx",
      "args": [
        "-y",
        "opengauss-mcp"
      ],
      "env": {
        "OPENGAUSS_HOST": "127.0.0.1",
        "OPENGAUSS_PORT": "5432",
        "OPENGAUSS_DATABASE": "postgres",
        "OPENGAUSS_SCHEMA": "public",
        "OPENGAUSS_USERNAME": "your_username",
        "OPENGAUSS_PASSWORD": "your_password"
      }
    }
  }
}
```

### 2) 本地启动（stdio 模式）

```bash
npx -y opengauss-mcp
```

### 3) 可视化运行（MCP Inspector）

复制配置模板：

```bash
cp mcp.json.template mcp.json
```

修改 `mcp.json` 中 `env` 的数据库连接信息，然后执行：

```bash
npx @modelcontextprotocol/inspector --config ./mcp.json --server opengauss
```

请根据你的 openGauss 实例更新以下环境变量：

- `OPENGAUSS_HOST`
- `OPENGAUSS_PORT`
- `OPENGAUSS_DATABASE`
- `OPENGAUSS_SCHEMA`
- `OPENGAUSS_USERNAME`
- `OPENGAUSS_PASSWORD`

## 开发者构建

### 1) 克隆并进入项目

```bash
git clone https://github.com/Sanjeever/opengauss-mcp
cd opengauss-mcp
```

### 2) 构建 jar

```bash
mvn clean package
```

构建成功后可执行包路径：

```text
target/opengauss-mcp.jar
```

### 3) 准备 npm 包

```bash
pnpm install
pnpm run prepare:npm
```

### 4) 打包或发布 npm 包

```bash
pnpm run pack:npm
```

发布到 npm：

```bash
pnpm run publish:npm
```

### 5) CI 自动发布 npm 包

GitHub Actions 会在推送 `v*` tag 或手动触发 `Publish npm Package` workflow 时发布 npm 包。

首次发布前，需要在 GitHub 仓库配置 npm token：

1. 在 npm 创建 automation token
2. 在 GitHub 仓库 `Settings` -> `Secrets and variables` -> `Actions` 中添加 `NPM_TOKEN`

发布流程：

```bash
git tag v1.0.4
git push origin v1.0.4
```

### 6) 本地 jar 启动

```bash
java -Dfile.encoding=UTF-8 -Dsun.stdout.encoding=UTF-8 -Dsun.stderr.encoding=UTF-8 -jar target/opengauss-mcp.jar
```

## 工具说明

### list_tables

- 入参：无
- 返回：当前 schema 下对象列表（`object_name`、`object_type`）

### describe_table

- 入参：`tableName`
- 返回：字段名、数据类型、是否主键、索引、注释、默认值等信息
- 约束：表名仅允许合法标识符（字母/数字/下划线）

### get_table_stats

- 入参：`tableName`
- 返回：估算行数、最近分析时间、表大小、索引大小

### run_select

- 入参：`sql`
- 允许：`SELECT` / `WITH` / `EXPLAIN`
- 拒绝：写操作关键字、多语句执行

### execute_sql

- 入参：`sql`
- 能力：执行 DDL/DML，返回受影响行数或结果集

## 常见问题

### 1) 启动后无法连接数据库

请检查：

- `OPENGAUSS_HOST`、`OPENGAUSS_PORT`、`OPENGAUSS_DATABASE`、`OPENGAUSS_SCHEMA`、`OPENGAUSS_USERNAME`、`OPENGAUSS_PASSWORD` 是否正确
- 数据库实例是否可达（网络、端口、防火墙）
- 账号是否具有目标 schema 的权限

### 2) `run_select` 提示不允许执行

`run_select` 只允许只读查询。如需执行建表、更新、删除等操作，请使用 `execute_sql`。

## License

[MIT](LICENSE)
