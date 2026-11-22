# SciLoam · 科研知识协同工作台

**面向小型科研团队的知识协同工作台。负责人以项目为单位管理资料与成员；成员共享材料，并在授权范围内使用可信 AI 知识库问答。**

![SciLoam](docs/images/social-preview.png)

![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.11--3.13-3776AB)
![React](https://img.shields.io/badge/react-18-61DAFB)
![TypeScript](https://img.shields.io/badge/typescript-5-3178C6)
![FastAPI](https://img.shields.io/badge/FastAPI-0.11x-009688)
![Docker](https://img.shields.io/badge/docker-ready-2496ED)
![CI](https://github.com/theyiliang/SciLoam/actions/workflows/ci.yml/badge.svg)

[功能](#功能) · [界面](#界面) · [架构](#架构) · [快速开始](#快速开始) · [配置](#配置) · [产品需求文档](docs/prd/README.md) · [FAQ](#faq) · [Roadmap](#roadmap)

## 要解决的问题

课题组至少有 5 个问题会重复出现：

- 资料发在哪里了？
- 这个文件是哪一个版本？
- 项目新人怎么找旧文件？
- 通用 AI 的回答可靠吗？
- 文件过期了怎么办？

这些问题看似都能靠临时询问解决，但每次都要重新找人、找文件、核对版本；使用通用 AI 时还要重复上传资料，回答也难以共享和复核。

## 使用前后

| 环节 | 现在 | 之后 |
| --- | --- | --- |
| 找材料 | 群里问、翻聊天记录、找个人电脑 | 在问答入口按项目范围提问 |
| 版本确认 | 逐个打开文件，查看具体内容 | 在问答入口直接询问所需内容，回答带版本和段落，可点回原文 |
| AI 问答 | 各问各的通用 AI，每问一次都需要重复上传资料 | 系统按权限检索，无需再次上传资料，结论带出处 |
| 多人协作 | 依靠聊天软件传资料、沟通任务进度 | 创建共享知识库，成员围绕同一批资料询问 AI |
| 成果沉淀 | 项目负责人自己收集；成果文件由各成员掌握，想看其他成员的公开成果需要向负责人索要 | 公开成果形成共享知识库，成员想看什么成果可以自己查 |
| 项目管理 | 建立群聊、开线下组会、文件自己收集发布、资料在本地进行管理 | 项目资料、任务、成员权限和公开成果统一在线管理 |

## 产品是什么

SciLoam 不是再增加一个孤立的知识库，而是把 **知识录入 → 版本沉淀 → 指定版本送审 → 成果发布 → 授权问答** 连成一条可追溯的协作链路。

- **私有与共享有明确边界**：项目成员身份不等于资料权限；个人库默认私有，负责人也没有默认访问特权，送审只开放指定版本快照。
- **版本成为协作依据**：每次修改保留历史，送审、审核与成果发布绑定具体版本，后续编辑不会覆盖已经提交的内容。
- **知识随协作过程沉淀**：项目依据、个人资料、协作知识与审核成果各归其位，历史工作不再只能依靠聊天记录和反复询问成员找回。
- **AI 回答可以核验**：只检索当前用户有权访问的资料，回答关联具体版本与原文片段；默认本地检索，外部模型与向量服务需显式开启。

**SciLoam 的核心不是“存得更多”，而是让科研知识在协作中始终有权限、有版本、有出处。**

完整的产品定位、使用前后对照、业务目标、能力边界与版本规划见 [产品需求文档](docs/prd/README.md)，也可下载 [PDF](docs/prd/SciLoam-PRD-v1.0.pdf)。

## 功能

| 模块 | 说明 |
| --- | --- |
| **基于知识库问答** | 在授权范围内检索与回答；材料不足时明确说明缺口，不编造依据 |
| **我的知识库** | 项目依据、个人、协作、成果四类空间；文档保留完整版本，支持上传、手动录入、送审与撤回 |
| **审核管理** | 负责人审阅成员提交的指定版本，通过后仅将该副本发布到成果知识库 |
| **我的提交** | 成员查看送审状态、审核意见与被审核版本 |
| **任务管理** | 以目标树组织研究任务，维护验收标准、阶段状态、进展与知识关联 |
| **成员与权限** | 项目管理与知识库授权分离，按空间授予负责人/编辑/只读 |
| **账号安全** | 单密码登录、CSRF 校验、密码修改即时撤销旧会话 |

## 界面

> 截图使用演示数据，不含真实成员信息。

| 登录 | 基于知识库问答 |
| --- | --- |
| ![登录](docs/images/login.png) | ![问答](docs/images/chat.png) |

| 我的知识库 | 审核管理 |
| --- | --- |
| ![知识库](docs/images/knowledge.png) | ![审核](docs/images/reviews.png) |

| 任务管理 | 成员与权限 |
| --- | --- |
| ![任务](docs/images/tasks.png) | ![成员](docs/images/members.png) |

## 架构

![SciLoam 架构：知识协作、授权问答与技术底座](docs/images/architecture.svg)

- 权限以服务端实时状态为准，前端提示不替代后端校验。
- 外部模型只读取当前请求方有权访问的片段；未配置模型时仅返回本地证据摘录。
- 详细设计见 [docs/architecture.md](docs/architecture.md) 与 [docs/security.md](docs/security.md)。

## 快速开始

要求：Python 3.11–3.13、Node.js 22+、[uv](https://docs.astral.sh/uv/)。

### 本地开发（推荐首次体验）

```bash
uv sync
npm --prefix frontend ci
npm --prefix frontend run build

cp .env.research.example .env        # Windows: copy .env.research.example .env

uv run python -m app.presentation.cli bootstrap \
  --email owner@example.org \
  --project "我的研究项目" \
  --db research-data/research.db

uv run python -m uvicorn app.presentation.server:app \
  --host 127.0.0.1 --port 8000 --workers 1
```

打开 <http://127.0.0.1:8000>，接口文档位于 <http://127.0.0.1:8000/docs>，健康检查为 `/health`。

首次 `bootstrap` 会交互式要求设置至少 12 位密码，系统不提供默认账号或密码。

前端开发模式：

```bash
npm --prefix frontend run dev   # 5174，/api 代理到 8000
```

### Docker 部署（生产或内网 HTTPS）

```bash
cp .env.research.example .env
# 写入 LLM 配置，并设置 RESEARCH_ALLOWED_HOSTS=你的域名,localhost,127.0.0.1
docker compose -f docker/research-compose.yaml up -d
```

容器以 `RESEARCH_ENV=production`、`RESEARCH_COOKIE_SECURE=1` 运行，**必须置于 HTTPS 之后**，否则登录 Cookie 不会生效。首次启动后仍需执行一次 bootstrap：

```bash
docker compose -f docker/research-compose.yaml exec research \
  python -m app.presentation.cli bootstrap \
  --email owner@example.org --project "我的研究项目"
```

部署细节见 [docs/deployment.md](docs/deployment.md)。

## 配置

| 变量 | 默认 | 说明 |
| --- | --- | --- |
| `RESEARCH_DATA_DIR` | `./research-data` | SQLite、上传文件与本地索引的根目录 |
| `LLM_API_KEY` | 空 | 为空时仅本地证据摘录，不调用外部模型 |
| `LLM_BASE_URL` / `LLM_MODEL` | DashScope / `qwen3-max` | OpenAI 兼容接口地址与模型名 |
| `RESEARCH_RETRIEVAL_MODE` | `local` | `local` 本地 BM25；`hybrid` 需显式允许外发 |
| `RESEARCH_RAG_ALLOW_EXTERNAL` | `0` | 是否允许把授权片段发送到 Embedding/重排服务 |
| `RESEARCH_ALLOWED_HOSTS` | `localhost,127.0.0.1` | 允许的 Host，生产必须写实际域名 |
| `RESEARCH_COOKIE_SECURE` | `0` | 生产置于 HTTPS 后设为 `1` |
| `RESEARCH_ENV` | `development` | 设为 `production` 启用生产安全策略 |

完整配置见 `.env.research.example`。

## 技术栈

| 层 | 选型 |
| --- | --- |
| 前端 | React 18 · TypeScript · Vite |
| 后端 | Python · FastAPI · 分层架构（表现/应用/领域/基础设施） |
| 存储 | SQLite（单文件，可直接备份） |
| 检索 | 本地 BM25；可选混合检索、向量索引与重排 |
| 模型 | OpenAI 兼容接口，默认关闭外部调用 |
| 测试 | pytest · Node.js Test Runner |

## 质量与测试

```bash
uv run pytest -q
npm --prefix frontend test
npm --prefix frontend run build
```

CI 覆盖前端全量测试与构建，以及后端核心用例（详见 `.github/workflows/ci.yml`）。

## 安全与隐私

- 所有知识访问以服务端实时权限为准，权限变更立即生效。
- 审核只读取送审版本快照，来源知识库不向审核人开放。
- 通过审核仅发布该版本副本到成果知识库，不回写来源库。
- 删除与撤回保留版本记录，便于复核。
- 外部模型与向量服务默认关闭，开启前需确认资料可以外发。

细节见 [docs/security.md](docs/security.md)。

## FAQ

**不配置模型能使用吗？**
可以。问答会基于授权材料返回本地证据摘录；配置模型后才能生成归纳式回答。

**资料会被发送到外部吗？**
默认不会。只有显式设置 `RESEARCH_RAG_ALLOW_EXTERNAL=1` 或配置模型密钥后才会外发，且仅限当前请求方有权访问的片段。

**如何备份与升级？**
备份整个 `RESEARCH_DATA_DIR`（默认 `research-data/`）即可，也可使用 `scripts/research_backup.py`。升级前先停止服务并备份目录。

**可以多个课题组共用一个实例吗？**
当前以单项目实例为设计目标，建议每个项目独立部署与备份，避免权限与数据边界混淆。

## Roadmap

### 优先推进：完善协作体验

- **原文件与附件管理**：原件保存、授权下载与提交清单
- **目标与行动协同**：承接确认、修改记录与 DDL 调整
- **版本与成果管理**：按用途标记采用版本，灵活配置共享范围

### 持续完善：提升知识与 AI 体验

- **导入与问答优化**：批量导入、更多格式、检索与引用质量改进
- **引用辅助创作**：基于可核验引用生成综述或研究草稿

### 后续拓展：支持多项目与灵活部署

- **多项目协作**：统一账号与项目切换，保持数据、会话和权限隔离
- **审核与部署扩展**：灵活审核配置、一键部署、升级与迁移

## 贡献

欢迎提交 Issue 与 PR。请先阅读 [docs/architecture.md](docs/architecture.md) 了解分层与权限约束；涉及权限、版本与审核的改动需附带测试。

## 许可证

[MIT](LICENSE)
