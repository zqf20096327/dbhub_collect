# opendbx-mcp-for-codex

> GaussDB / openGauss DBA MCP server — bringing opendb's DBA skills to Codex / codexgo / any MCP client.

把 opendb 的数据库专家能力,封装成一个**标准 MCP server**(stdio JSON-RPC),供
[codexgo](https://github.com/sqlrush/codexgo)、OpenAI Codex、Claude Code、VS Code 等任何支持 MCP 的 agent 使用。
当前内置 **GaussDB / openGauss** 服务(`codexgo-db-gaussdb`),全部工具**只读**(不修改数据或配置)。

- **作者**:Sqlrush(AAA 数据库老王) · `sqlrush@gmail.com`
- **协议**:Apache License 2.0
- **定位**:与上层 agent 框架**零运行时耦合**——唯一接口是 MCP 协议(stdio)。opendb 只是知识/SQL 来源。

## 能力(~36 个只读工具)

| 域 | 工具 |
|---|---|
| 诊断/体检 | `health`(开放式 6 维诊断)、`ash`、`alert` |
| 会话/锁 | `sessions`、`locks`(含阻塞链树)、`lwlocks`、`longtx` |
| 事务/空间/膨胀 | `vacuum`、`xid`、`bloat`、`space`、`tempusage`、`hotkey` |
| 内存/WAL/复制 | `gsmem`、`wal`、`replication`、`bgworker` |
| 系统/元数据 | `resource`、`os`、`users`、`params`、`sqlcount`、`tableinfo` |
| SQL 性能/调优 | `slowsql`、`topsql`、`explain`、`sqlfetch`、`sqltune`(计划+[Pn]热点+校验改写)、`indexadvise`、`planhistory` |
| WDR/趋势 | `wdr`、`wdranalyze`、`perfsnap` |

数据展示类工具**确定性渲染**对齐表格(数字不经模型);`health`/`sqltune`/`wdranalyze` 采集确定性证据后由模型叠加分析。

## 构建

```bash
go build -o bin/codexgo-db-gaussdb ./cmd/codexgo-db-gaussdb
```
纯 Go(无 CGO);GaussDB 用专有 `gaussdb-go` 驱动(SCRAM-SHA256),系统视图复用 openGauss(`pg_stat_*`、`dbe_perf.*`)。

## 接入

**作为标准 MCP server**,任何 MCP 客户端把 `command` 指向二进制即可。

- **codexgo**:作为插件(`.codex-plugin/plugin.json` + `.mcp.json`),工具自动映射成 `/health` 等**确定性 slash** 命令。
- **Claude Code**:`claude mcp add gaussdb /abs/path/to/codexgo-db-gaussdb`,工具由模型调用(自然语言触发)。
- **OpenAI Codex**:在 `~/.codex/config.toml` 配置 MCP server,工具由模型调用。

连接:默认读取 `~/.dbaa`(opendb 配置)自动连接,或用 `connect` 工具显式传 `host/port/user/password`。

## 版本

本仓库(MCP server)与 codexgo 框架仓库**独立管理版本**。当前 server 版本见 `cmd/codexgo-db-gaussdb/main.go` 的 `version`。

## License

Apache License 2.0 — see [LICENSE](./LICENSE)。Copyright 2026 Sqlrush(AAA 数据库老王) `<sqlrush@gmail.com>`。
