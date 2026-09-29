# RAGent - Agentic RAG 企业知识库问答系统

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-async-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg?logo=react&logoColor=white)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6.svg?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Vite](https://img.shields.io/badge/Vite-5-646CFF.svg?logo=vite&logoColor=white)](https://vitejs.dev/)
[![Qdrant](https://img.shields.io/badge/Qdrant-Vector_DB-DC382D.svg)](https://qdrant.tech/)
[![Neo4j](https://img.shields.io/badge/Neo4j-Knowledge_Graph-008CC1.svg)](https://neo4j.com/)
[![LLM: OpenAI-Compatible](https://img.shields.io/badge/LLM-OpenAI_Compatible-412991.svg)]()
[![RAG](https://img.shields.io/badge/Architecture-Agentic_RAG-FF6F00.svg)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](./CONTRIBUTING.md)
[![Last Commit](https://img.shields.io/github/last-commit/qianfengzongheng/agenticRag?color=9cf&label=last%20commit)](./)
[![Repo Size](https://img.shields.io/github/repo-size/qianfengzongheng/agenticRag?color=orange)](./)

基于 Agentic RAG 架构的企业知识库智能问答系统。

## 核心特性

- **多步推理与检索** — ReAct 模式，动态规划检索策略
- **多轮对话管理** — 三层记忆模型（工作记忆/摘要记忆/长期记忆）
- **引用溯源** — 回答标注来源，可点击跳转原文
- **工具调用** — 可扩展的 Tool 体系
- **文档修改** — 编辑文档后自动增量同步向量库，支持任意版本回退
- **多格式支持** — PDF/Office/图片/代码/HTML/文本
- **知识图谱** — 可选增强，路由层支持切换图数据库后端
- **多模型路由** — 支持 OpenAI/Claude/本地模型，任务感知路由 + 自动降级
- **可观测性** — 全链路 Trace，每一步思考和调用可追溯
- **可评估性** — 实时 + 离线评估，前端可视化仪表盘

## 技术栈

- **后端**: Python + FastAPI
- **向量数据库**: Qdrant Cloud
- **知识图谱**: Neo4j AuraDB Free（可选）
- **前端**: React + TypeScript + TailwindCSS

## 项目结构

```
agenticRag/
├── backend/                # 后端服务
│   ├── app/                # 应用代码
│   │   ├── api/            # API 路由
│   │   ├── agent/          # Agent 推理引擎
│   │   ├── auth/           # 认证模块
│   │   ├── core/           # 核心基础设施（配置、存储、LLM、日志）
│   │   ├── ingestion/      # 文档摄入与分块
│   │   ├── retrieval/      # 向量检索
│   │   └── main.py         # FastAPI 入口
│   ├── alembic/            # 数据库迁移
│   ├── tests/              # 测试
│   ├── docs/               # 后端设计文档
│   ├── config.yaml         # 配置文件
│   ├── pyproject.toml      # Python 依赖
│   └── alembic.ini         # Alembic 配置
├── frontend/               # 前端应用
│   ├── src/                # 源码
│   ├── docs/               # 前端设计文档
│   └── package.json
├── Makefile                # 常用命令快捷方式
├── CLAUDE.md               # 开发规范
└── AGENTS.md               # Agent 协作规范
```

## 快速开始

### 环境要求

- Python >= 3.12
- Node.js >= 18
- 外部服务：智谱 AI API Key、Qdrant 向量数据库

### 1. 配置后端环境变量

```bash
cd backend
cp .env.example .env
```

编辑 `backend/.env`，填入以下必填项：

```dotenv
ZHIPU_API_KEY=<你的智谱 AI API Key>
JWT_SECRET=<任意随机字符串，用于 JWT 签名>
QDRANT_API_KEY=<Qdrant API Key>
QDRANT_URL=<Qdrant 服务地址，如 https://xxx.aws.cloud.qdrant.io>
```

> **注意**: `QDRANT_URL` 未在 `.env.example` 中列出，但属于必填项，请手动添加。

### 2. 安装依赖

**后端依赖**

由于 `pip install -e ".[dev]"` 依赖解析可能较慢，推荐逐个安装核心依赖：

```bash
cd backend
pip install fastapi uvicorn pydantic pydantic-settings sqlalchemy aiosqlite \
    qdrant-client openai python-jose passlib bcrypt==3.2.2 pymupdf alembic \
    python-multipart httpx pyyaml python-dotenv jieba python-docx openpyxl \
    python-pptx html2text grpcio grpcio-tools portalocker
```

> **重要**: `bcrypt` 必须使用 `3.2.2` 版本，更高版本（4.x/5.x）与 `passlib` 不兼容，会导致登录报错 `password cannot be longer than 72 bytes`。

**前端依赖**

```bash
cd frontend
npm install
```

### 3. 初始化数据库

```bash
cd backend
python -m alembic upgrade head
```

### 4. 启动服务

在两个终端分别执行：

```bash
# 终端 1 — 启动后端（端口 8001）
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001

# 终端 2 — 启动前端（端口 5173，自动代理 /api 到后端）
cd frontend
npm run dev
```

也可以使用 Makefile：

```bash
make dev-backend    # 启动后端
make dev-frontend   # 启动前端
```

### 5. 注册用户与授权

访问 http://localhost:5173/register 注册账号。新用户默认为 `viewer` 角色。

如需管理员权限，可通过以下命令在数据库中授予 `system_admin` 角色：

```bash
cd backend
python -c "
import sqlite3
from datetime import datetime, timezone
conn = sqlite3.connect('data/agenticrag.db')
cur = conn.cursor()
# 先查询用户 ID
cur.execute('SELECT user_id, username FROM users')
print(cur.fetchall())
# 授予 system_admin 角色（替换 <user_id> 为实际值）
cur.execute(
    'INSERT INTO user_system_roles (user_id, role, granted_at) VALUES (?, ?, ?)',
    ('<user_id>', 'system_admin', datetime.now(timezone.utc).isoformat())
)
conn.commit()
conn.close()
print('Done')
"
```

### 6. 访问应用

| 服务 | 地址 |
|------|------|
| 前端界面 | http://localhost:5173 |
| 后端 API | http://localhost:8001 |
| API 文档 | http://localhost:8001/docs |

## 常用命令

```bash
make test           # 运行后端测试
make migrate        # 数据库迁移
make lint           # 代码检查
make format         # 代码格式化
```

## 常见问题

### 登录报错 `password cannot be longer than 72 bytes`

`bcrypt` 版本过高导致与 `passlib` 不兼容，降级即可：

```bash
pip install bcrypt==3.2.2
```

然后重启后端服务。

### `pip install -e ".[dev]"` 依赖解析卡住

pip 在解析 `qdrant-client`、`ruff` 等包的版本时可能陷入回溯循环。建议直接按步骤 2 中的命令逐个安装。

### 前端页面报错 `Failed to resolve import "@antv/g6"`

缺少前端依赖，执行：

```bash
cd frontend && npm install @antv/g6
```

## 项目状态

设计阶段完成，详见 [设计总览](backend/docs/feature/design-overview.md)
