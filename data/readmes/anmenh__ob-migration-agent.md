# OceanBase 智能评估 Agent

一个面向 **MySQL / Oracle 迁移 OceanBase** 场景的智能评估与辅助分析项目，包含后端服务、前端界面、知识库检索、SQL 评估、智能对话、模型加载与配置管理等能力。

## 项目简介

本项目用于帮助用户完成以下工作：

- 评估 MySQL / Oracle SQL 迁移到 OceanBase 的兼容性与风险
- 通过知识库检索回答迁移、SQL、运维、使用方法相关问题
- 提供智能对话能力，支持基于知识库的问答
- 管理知识库文档的上传、预览、删除与搜索
- 统一管理模型加载、系统配置和运行状态

项目采用前后端分离架构：

- **后端**：FastAPI + Python
- **前端**：React + TypeScript + Vite + Ant Design
- **知识库**：本地文档 + 向量检索 + 本地持久化
- **模型**：本地离线加载大模型、LoRA、Embedding 模型

---

## 功能特性

### 1. 智能对话

- 支持多轮对话
- 支持基于知识库的问答
- 支持回答来源展示
- 支持长问题的上下文处理

### 2. SQL 评估

- 对 MySQL / Oracle SQL 进行 OceanBase 迁移评估
- 识别高风险语法与兼容性问题
- 支持 SQL 解析、静态规则检查与迁移建议

### 3. 知识库管理

- 上传文档到知识库
- 预览文档内容
- 删除文档
- 检索文档并在对话中引用
- 文档持久化保存，重启后可恢复

### 4. 配置与模型管理

- 支持查看模型与服务状态
- 支持后端配置项管理
- 支持本地离线模型目录加载

---

## 技术栈

### 后端

- FastAPI
- Pydantic / Pydantic Settings
- Uvicorn
- Transformers
- PEFT
- Torch
- Sentence Transformers
- ChromaDB
- SQLGlot

### 前端

- React 18
- TypeScript
- Vite
- Ant Design
- TanStack Query
- Zustand
- Axios
- Tailwind CSS

---

## 目录结构

```text
obagent/
├─ backend/                 # 后端服务
├─ frontend/                # 前端应用
├─ knowledge/               # 知识库文档
├─ data/                    # 持久化数据
├─ tmp_uploads/             # 上传临时文件
├─ test/                    # 后端测试
└─ README.md
```

---

## 运行环境要求

### 基本要求

- Python 3.10+
- Node.js 18+
- npm / pnpm / yarn（任选其一）
- Windows / Linux / macOS 均可

### 模型与依赖

后端依赖本地模型文件，首次启动前请确保：

- 大模型目录存在
- Embedding 模型目录存在
- LoRA 权重（如启用）存在
- 相关模型均为本地离线文件，不依赖在线下载

---

## 快速开始

### 1. 克隆项目

```bash
git clone <your-repo-url>
cd obagent
```

### 2. 配置后端环境变量

后端示例配置位于 `backend/.env`。

如果你需要调整模型目录、端口、RAG 参数或 CORS 配置，请直接修改该文件。

### 3. 启动后端

进入 `backend/` 目录后运行：

```bash
python main.py
```

默认地址：

- `http://127.0.0.1:8000`

### 4. 启动前端

进入 `frontend/` 目录后运行：

```bash
npm install
npm run dev
```

默认地址：

- `http://127.0.0.1:5173`

---

## 详细启动步骤

### 后端

```bash
cd backend
pip install -r requirements.txt
python main.py
```

### 前端

```bash
cd frontend
npm install
npm run dev
```

如果你要构建前端生产包：

```bash
npm run build
```

---

## 环境变量说明

### 后端常用配置

配置文件：`backend/.env`

- `PROJECT_NAME`：项目名称
- `APP_HOST`：后端监听地址
- `APP_PORT`：后端监听端口
- `APP_DEBUG`：是否开启热重载
- `KNOWLEDGE_DIR`：知识库目录
- `CHROMA_DB_DIR`：向量库目录
- `MODELS_DIR`：模型根目录
- `LORA_OUTPUT_DIR`：LoRA 输出目录
- `QWEN_MODEL_DIR`：大模型目录
- `BGE_M3_MODEL_DIR`：Embedding 模型目录
- `RAG_CHUNK_SIZE`：RAG 切片大小
- `RAG_CHUNK_OVERLAP`：RAG 切片重叠大小
- `RAG_TOP_K`：默认检索条数
- `LLM_MAX_NEW_TOKENS`：模型生成长度上限
- `LLM_TIMEOUT_SECONDS`：模型推理超时
- `CORS_ALLOW_ORIGINS`：允许跨域来源

### 前端常用配置

配置文件：`frontend/.env.development` 或 `frontend/.env.example`

- `VITE_API_BASE_URL`：后端地址
- `VITE_APP_NAME`：前端应用名称
- `VITE_ENABLE_MOCK`：是否启用 mock

---

## 核心页面

### 1. 工作台

用于查看整体功能入口、模型状态与常用操作。

### 2. SQL 评估

用于输入 SQL 并获取迁移评估结果。

### 3. 智能对话

用于与模型进行多轮问答，并结合知识库返回答案与来源。

### 4. 知识库

用于文档管理、预览与检索。

### 5. 系统配置

用于查看和管理系统配置。

---

## API 概览

以下为常见接口，具体以后端路由实现为准。

### 健康检查

- `GET /api/health`

### 智能对话

- `POST /api/chat/answer`
- `GET /api/chat/stream`

### 知识库

- `GET /api/rag/documents`
- `GET /api/rag/documents/{file_id}`
- `POST /api/rag/documents`
- `DELETE /api/rag/documents/{file_id}`
- `POST /api/rag/search`

### SQL 评估

- `POST /api/sql/...` 相关接口

### 系统配置

- `GET /api/config/...` 相关接口

---

## 知识库说明

### 文档来源

你可以将迁移手册、FAQ、操作文档、排错指南等放入知识库目录，或通过前端页面上传。

### 检索方式

系统会对文档进行切片并建立检索索引，问答时会先搜索相关内容，再结合模型生成回答。

### 数据持久化

知识库文档会持久化到本地数据文件，常见路径为：

- `data/rag_documents.json`

上传临时文件会保存在：

- `tmp_uploads/`

---

## 模型说明

后端依赖本地模型加载，通常包括：

- Chat LLM
- Embedding 模型
- LoRA 可选权重

如果模型目录不存在或权重不完整，后端会在启动时提示错误。

建议确保以下目录有效：

- `backend/models/Qwen2.5-1.5B-Instruct`
- `backend/models/bge-m3`
- `backend/lora_output/`（如启用 LoRA）

---

## 开发与调试

### 后端开发

```bash
cd backend
python main.py
```

### 前端开发

```bash
cd frontend
npm run dev
```

### 后端测试

```bash
cd backend
pytest
```

### 前端检查

```bash
cd frontend
npm run lint
npm run build
```

---

## 常见问题

### 1. 后端启动失败

请检查：

- Python 版本是否满足要求
- 依赖是否安装完整
- 模型目录是否存在
- `.env` 中路径是否正确
- 端口是否被占用

### 2. 智能对话没有回复

请检查：

- 后端健康状态是否正常
- 模型是否已加载完成
- 知识库是否有命中内容
- 前端是否正确连接到后端地址

### 3. 检索不到知识库

请检查：

- 文档是否已上传成功
- 文档是否被切片并入库
- 检索阈值是否过高
- 相关文档是否确实包含用户问题关键词

### 4. 前端请求失败

请检查：

- `VITE_API_BASE_URL` 是否与后端一致
- 后端 CORS 配置是否允许当前前端地址
- 浏览器控制台与网络请求是否有报错

---

## 建议的工作流

1. 启动后端
2. 确认健康检查正常
3. 启动前端
4. 上传知识库文档
5. 先在知识库页面验证文档已入库
6. 再进入智能对话进行问答
7. 必要时在 SQL 评估页测试迁移场景

---

## 许可证

当前仓库未显式声明许可证。若你准备开源，请补充 LICENSE 文件。

---

## 致谢

感谢你使用 OceanBase 智能评估 Agent。该项目面向 OceanBase 迁移分析、SQL 评估与知识库问答场景，可作为内部辅助工具或进一步产品化的基础。
