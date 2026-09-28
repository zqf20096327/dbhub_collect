# Permission-Aware Agentic RAG

一个面向企业共享文档的权限感知型 Agentic RAG 参考实现。系统将目录 ACL 贯穿到知识路由、混合检索、Rerank、LLM Evidence 和 Citation 访问链路，让不同用户可以通过同一个知识库入口安全问答。

> 核心原则：权限由确定性后端逻辑判断，Agent 和大模型不参与授权决策。

## 核心能力

- 目录级 ACL：支持用户、用户组、父目录继承和实时 Allowed Scope 计算。
- 权限感知检索：Dense/Sparse 使用相同的 Qdrant Filter，经 RRF 融合后再以 MySQL 当前事实二次验权。
- 受控 Agent 路由：只能在当前用户可读的知识目录中路由，只能调用允许列表内的只读工具。
- 多格式入库：支持 Markdown、PDF、DOCX 和 DOC，包含文档图片提取、扫描页判定和中英文 OCR。
- 混合检索与重排：Qdrant Dense/Sparse + RRF，可接入外部 Embedding 和 Rerank HTTP Provider。
- 可追溯问答：基于授权 Evidence 生成答案，Citation 支持 Markdown 行号定位和 PDF 页码跳转。
- 即时失效：文档删除、移动或目录撤权后，下一次检索和 Citation 访问按新权限判定，不依赖立即改写每个向量。
- 安全版本发布：新版本只有在解析和索引成功后才原子切换为 active version。
- 管理与可观测性：提供管理台、无登录身份演示页、任务管理、审计、评测、运行指标和索引对账。

## 权限安全链路

```text
用户 + 知识库
       │
       ▼
MySQL 实时计算 Allowed Scope
       │
       ▼
Qdrant 强制 knowledge_base_id + folder_scope_id Filter
       │
       ▼
MySQL 二次校验文档状态、active version 和索引状态
       │
       ▼
Rerank → permission_version 再检查 → LLM Evidence
       │
       ▼
Citation 创建与打开时再次鉴权
```

Chunk 和 Qdrant Payload 只保存 `folder_scope_id`，不复制用户或用户组 ACL。MySQL 始终是身份、授权、文档状态和当前版本的事实源。详细设计见 [权限模型](docs/PERMISSION_MODEL.md) 和 [系统架构](docs/ARCHITECTURE.md)。

## 技术栈

| 领域 | 实现 |
|---|---|
| API 与管理页 | Python 3.12+、FastAPI、原生 HTML/CSS/JavaScript |
| 关系数据 | MySQL 8.4、SQLAlchemy Async、Alembic |
| 对象存储 | MinIO |
| 向量检索 | Qdrant Dense/Sparse、RRF |
| 文档处理 | pdfplumber、pypdfium2、OOXML Parser、隔离 LibreOffice |
| OCR | RapidOCR + ONNX Runtime |
| 模型接入 | 可替换 HTTP Embedding、Rerank 和 LLM Provider |
| 后台任务 | MySQL 持久队列、租约、失败重试、常驻 Worker 与 Scheduler |

## 快速开始

### 前置条件

- Python 3.12～3.14
- [uv](https://docs.astral.sh/uv/)
- Docker 与 Docker Compose

### 1. 初始化配置

```bash
cp .env.example .env
uv sync --dev
```

编辑 `.env`，至少更换以下本地默认值：

```dotenv
RAG_ADMIN_PASSWORD=<strong-admin-password>
RAG_ADMIN_SESSION_SECRET=<random-session-secret>
RAG_PROVIDER_SETTINGS_ENCRYPTION_KEY=<stable-random-encryption-key>
RAG_MYSQL_ROOT_PASSWORD=<mysql-root-password>
```

`RAG_PROVIDER_SETTINGS_ENCRYPTION_KEY` 用于加密数据库中的 Provider API Key。已保存密钥后不要更换该值，否则历史密文将无法解密。

### 2. 启动依赖与 API

```bash
docker compose up -d mysql minio qdrant doc-converter doc-converter-gateway
uv run alembic upgrade head
uv run uvicorn app.main:app --reload
```

### 3. 启动后台进程

在三个独立终端中运行：

```bash
uv run python -m app.workers.ingestion
```

```bash
uv run python -m app.workers.indexing
```

```bash
uv run python -m app.workers.scheduler
```

Ingestion Worker 默认处理 Markdown、DOCX 和 PDF。若需处理旧版 `.doc`，将 `RAG_DOC_CONVERTER` 设为 `http`，并确保转换服务已启动。

### 4. 配置模型服务

登录管理台，在“模型服务设置”中配置 Embedding、Rerank 和 LLM。Endpoint 应填写完整接口路径，例如：

```text
https://provider.example/v1/embeddings
https://provider.example/v1/rerank
https://provider.example/v1/chat/completions
```

管理页可在保存前发送最小真实请求测试连接。API Key 在服务端加密后保存到 MySQL，读取接口和前端都不回显明文。

## 本地入口

| 入口 | 地址 |
|---|---|
| 管理台 | <http://127.0.0.1:8000/admin> |
| 身份问答演示 | <http://127.0.0.1:8000/demo> |
| OpenAPI | <http://127.0.0.1:8000/docs> |
| Liveness | <http://127.0.0.1:8000/api/v1/ops/health/live> |
| Readiness | <http://127.0.0.1:8000/api/v1/ops/health/ready> |
| Metrics | <http://127.0.0.1:8000/api/v1/ops/metrics> |
| MinIO Console | <http://127.0.0.1:9101> |
| Qdrant Dashboard | <http://127.0.0.1:6333/dashboard> |

## 使用流程

1. 在管理台创建知识库和目录树。
2. 创建演示用户、用户组和成员关系。
3. 将目录读权限授予用户或用户组。
4. 将文档上传到非根目录，由 Worker 执行解析、OCR、Chunk 和索引。
5. 在“身份检索预览”检查用户的 Allowed Scope 和检索结果。
6. 打开 `/demo`，选择知识库和用户身份进行权限问答。
7. 点击 Citation 验证来源定位，再通过撤销 Grant 验证旧引用即时失效。

`/demo` 是用于快速切换身份的演示入口，不是生产环境的用户认证方案。

## 测试

运行不依赖外部服务的测试：

```bash
uv run pytest
```

运行所有本地集成测试：

```bash
RAG_RUN_DB_TESTS=1 \
RAG_RUN_MINIO_TESTS=1 \
RAG_RUN_QDRANT_TESTS=1 \
RAG_RUN_OCR_TESTS=1 \
RAG_RUN_DOC_CONVERTER_TESTS=1 \
uv run pytest -vv
```

更细的测试分组、手动验收步骤和安全断言见 [测试指南](docs/TESTING.md)。可公开的虚构样本位于 [`testdocs/`](testdocs/README.md)。

## 项目结构

```text
app/
├── api/                    # API 聚合路由
├── core/                   # 配置、数据库、安全与基础设施
├── modules/
│   ├── admin/              # 管理认证与管理 API
│   ├── agent/              # Router、Tool Gateway 与 LLM 编排
│   ├── document/           # 文档、版本与对象存储
│   ├── ingestion/          # 解析、OCR、Chunk 与任务队列
│   ├── permission/         # ACL、继承与 Allowed Scope
│   ├── provider_config/    # 模型 Provider 配置与密钥加密
│   └── retrieval/          # Qdrant、RRF、二次验权与 Rerank
├── web/                    # 管理台和 Demo 页面
└── workers/                # Ingestion、Indexing、Scheduler、评测和压测
migrations/                 # Alembic 迁移
services/                   # 隔离 DOC 转换服务
testdocs/                   # 可公开的虚构验收样本
tests/                      # 单元与集成测试
```

## 文档

- [系统架构](docs/ARCHITECTURE.md)
- [权限模型](docs/PERMISSION_MODEL.md)
- [配置说明](docs/CONFIGURATION.md)
- [测试指南](docs/TESTING.md)
- [安全政策](SECURITY.md)
- [贡献指南](CONTRIBUTING.md)
- [数据库迁移](migrations/README.md)

## 设计边界

- 授权粒度为目录，文档继承所属目录权限；不支持文件级单独授权。
- 用户和用户组用于演示权限模型，未实现完整组织架构、SSO 或 SaaS 多租户控制面。
- 网盘接入仅提供变更事件收件箱抽象，未绑定某一家网盘厂商的文件拉取 API。
- 外部 Embedding、Rerank 和 LLM 会接收经过授权与最小化处理的文本；部署前需要根据数据分级选择合规 Provider。
- 生产部署仍需结合实际身份系统、密钥管理、网络隔离、容量规划、备份恢复和安全评审。

## 贡献与安全

提交问题或代码前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。安全漏洞不要通过公开 Issue 披露，请按 [SECURITY.md](SECURITY.md) 的方式私下报告。

## License

本项目使用 [MIT License](LICENSE)。
