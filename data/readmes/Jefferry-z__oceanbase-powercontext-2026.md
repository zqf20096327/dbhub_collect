# oceanbase-powercontext-2026

第六届 OceanBase 数据库大赛 **PowerContext 赛题方向**仓库（上下文工程 / Agent 记忆与交接）。

> 本仓库为 **Private 私有仓库**。参赛代码不得对外公开，网络发现重复代码一律按作弊处理。

## 官方要求速记

- 依赖：**Python 3.11+**、Git、uv、Agent CLI（Codex / Claude Code 等）
- 安装：`uv tool install --force "powercontext[cli,server]==<赛题指定版本>"`
- 初始化：`powercontext config init --language zh --output .env`
- 校验：`powercontext config validate --env-file .env`
- 启动：`powercontext server run --env-file .env`（默认 `http://127.0.0.1:8000`，MCP 端点 `/mcp`）
- 存储后端：SQLite（上手）/ 嵌入式 SeekDB（更强）
- 记忆能力：**Basic** 无需模型 API；**Full** 需要 Generation + Embedding 两组凭据

⚠️ 版本号必须与赛题指定版本一致（1.0.0 / 1.1.0 / 1.2.0 混用会出兼容问题）

## 提交规范

- 提测时填写 **仓库地址 + 分支名/commit id**，前后**不要加空格**
- `.env` 含服务端 Token 与 API Key，已加入 .gitignore，**切勿提交**
