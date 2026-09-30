# PolarDB-X Zero Qoder Plugin

> **Instant Database for AI Agents.**

[PolarDB-X Zero](https://zero.polardbx.com) 是面向 AI Agent 的即时数据库：100% MySQL 兼容，统一单机与分布式架构。这个插件将 Zero、Vector、Mem0 和 AI Function 集成到 Qoder，让 Agent 可以直接创建数据库、执行 SQL，并构建语义搜索、长期记忆与 SQL AI 应用。

**无需注册。无需预先准备数据库。用完自动回收。**

## 这个插件能帮 Agent 做什么

1. **随时获得一个数据库**：自动创建 PolarDB-X Zero 临时实例，建表、写入数据、执行 SQL 和事务。
2. **构建语义搜索和 RAG**：使用向量列、HNSW 索引和距离函数检索语义相近的内容。
3. **保存 Agent 的长期记忆**：通过 Zero 托管的 Mem0 记录用户偏好、对话历史和需要长期保留的信息。
4. **直接在 SQL 中使用 AI**：调用大模型生成文本、分类、摘要、抽取信息，以及生成 Embedding 和重排检索结果。

## 安装方式

### 方式一：安装完整 Qoder 插件

适合 Qoder 用户，会同时安装 4 个 Skills，并通过根目录的 `.mcp.json` 自动发现 Zero MCP Server。需要 [Qoder CLI](https://qoder.com)、Git 和 [`uvx`](https://docs.astral.sh/uv/guides/tools/)。运行前请确认：

- `uvx` 可通过 `PATH` 访问，可用 `command -v uvx` 检查。
- 首次启动 MCP Server 时允许联网下载固定版本 `polardbx-zero-mcp==0.2.2`。

```bash
git clone https://github.com/polardb/polardbx-zero.git
qodercli plugins validate ./polardbx-zero
qodercli plugins install ./polardbx-zero
```

安装后重启 Qoder CLI，或在 TUI 中执行 `/plugins reload`。本项目不通过 Marketplace 分发；升级时拉取最新代码并重新执行本地安装。插件不包含数据库凭据，也不应将凭据写入 `.mcp.json`。

### 方式二：只安装 Agent Skills

适合只需要 Skill 指令，或使用 Codex、Claude Code、Cursor 等其他 Agent 的用户。通过 [`skills` CLI](https://www.skills.sh/docs/cli) 安装，需要 Node.js 和 `npx`。先查看可安装的 Skill：

```bash
npx skills add polardb/polardbx-zero --list
```

交互式选择并安装：

```bash
npx skills add polardb/polardbx-zero
```

也可以只安装指定 Skill：

```bash
npx skills add polardb/polardbx-zero --skill polardbx-aifunction
```

`npx skills` 只安装 Skill 指令，不会安装插件的 MCP Server。如需 Zero MCP 实例管理和 SQL 工具，请使用上面的 Qoder 插件安装方式。

## 直接对 Agent 说

```text
创建一个 PolarDB-X Zero 标准版实例，建表并导入示例数据。
```

```text
用 PolarDB-X Zero 企业版实现一个 HNSW 向量检索示例。
```

```text
用 AI Function 对表中的文本做分类，先 SELECT 预览 10 行。
```

```text
为我的 Agent 创建 Mem0 长期记忆，并验证写入和检索。
```

## 插件内容

| Skill | 用途 |
| --- | --- |
| `polardbx-zero` | Zero 实例生命周期、版本选择和 SQL 连接 |
| `polardbx-vector` | Vector schema、HNSW、向量召回与 RAG |
| `polardbx-mem0` | Mem0 memory storage 和 `mem0ai` SDK |
| `polardbx-aifunction` | SQL 即 AI：生成、分类、抽取、Embedding 与 Rerank |

[官方 Zero MCP Server](.mcp.json) 会被 Qoder 自动发现，提供实例管理、SQL 执行、批量操作和有状态连接共 10 个工具。

## 版本选择

- 默认使用 **Standard**：Agent 关系数据、MCP、Mem0 和 MySQL 原型。
- 使用 **Enterprise**：Vector/HNSW、RAG、开箱即用的 AI Function 和 PolarDB-X 分布式数据库能力。

AI Function 的业务函数在两个版本中语法相同；模型管理语法不同：标准版使用 `CALL dbms_ai.*` 存储过程，企业版使用 `SELECT AI_*` 函数。当前 Zero 标准版实例未配置默认模型，且 Zero 账号调用 `dbms_ai` 模型管理过程时实测受 `SUPER` 权限限制，因此 Zero 上默认使用企业版执行 AI Function。

## 使用边界

- Zero 是临时体验环境，不应用作生产数据库。
- 不要向代码、日志或 Issue 写入数据库密码、Mem0 API Key 或模型 API Key。
- MCP 会在 `~/.polardbx-zero-mcp/instances.json` 保存本地连接信息；该文件不得提交或分享。

详细说明见 [Security Policy](SECURITY.md)。

## 开发与验证

```bash
python3 scripts/validate_plugin.py
uv run --with 'mcp[cli]>=1.26,<2' python scripts/test_mcp.py
```

GitHub Actions 会在每次 Push 和 Pull Request 时自动执行上述静态检查与 MCP 握手测试。

Apache License 2.0 · [PolarDB-X Zero](https://zero.polardbx.com)
