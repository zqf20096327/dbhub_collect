# AI Novel Studio · 小说自动化创作工作台

<p align="center">
  <img src="https://img.shields.io/badge/Next.js-16-black?logo=nextdotjs&logoColor=white" alt="Next.js 16" />
  <img src="https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=white" alt="React 19" />
  <img src="https://img.shields.io/badge/FastAPI-latest-009688?logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/SQLite-SingleFile-003B57?logo=sqlite&logoColor=white" alt="SQLite" />
  <img src="https://img.shields.io/badge/AI-DeepSeek%20%2F%20OpenAI-FF6F00" alt="AI Providers" />
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License" />
</p>

> **AI 驱动的小说自动化创作工作台**：内置 AI 创作台（Planner / Character / Writer / Editor）、去 AI 味精修、国产绘图模型插画、章节导出（Word / TXT / MD）。基于 Next.js 16 + React 19 + FastAPI + SQLite，**免 Docker 一键启动**。

AI Novel Studio 帮助你从灵感走到成稿：创建与管理作品、维护人物与世界观、编写章节、统计字数、沉淀长期记忆，并由四个专业 Agent 调用 DeepSeek / OpenAI 辅助创作；另提供「去 AI 味」精修、国产绘图模型插画、章节导出等增强能力。

> 本仓库为**代码仓库**，不包含任何小说正文数据库与密钥。小说内容保存在本地 SQLite 文件，密钥保存在被忽略的 `.env`，均不随 Git 同步（详见下文「数据安全」）。

## 功能特性

- 作品全生命周期管理：书名、类型、状态、目标字数、梗概，独立作品工作台。
- 故事资产管理：角色档案、世界观（前提/地点/阵营/规则/时间线）、章节（视角/大纲/正文/摘要/状态）、长期记忆。
- AI 创作台：Planner / Character / Writer / Editor 四 Agent，自动组合作品上下文进行真实调用。
- 章节起草与续写：Writer Agent 按大纲生成，先进入可编辑预览，审核通过后写回，不自动覆盖原正文。
- **去 AI 味（humanize）**：章节级 + 全本级，支持 gentle / standard / aggressive 三档强度，零事实改动、去翻译腔与模板化表达。
- **插画**：国产绘图模型多选，插画画廊支持放大 / 下载 / 预览，提示词联想单章正文。
- **章节导出**：全书或单章导出为 Word(.docx) / TXT(带 BOM) / Markdown。
- 字数统计：自动统计中文字符与英文单词并汇总作品进度。
- 可切换 AI Provider（DeepSeek / OpenAI），运行时可在 UI 配置，无需改代码。
- 跨库兼容数据层：默认 SQLite 单文件（零外部依赖），可选 PostgreSQL 双后端；Redis 仅作可选缓存。

## 技术栈

- 前端：Next.js 16、React 19、TypeScript、App Router、Tailwind CSS 4
- 后端：Python 3.13+、FastAPI、SQLAlchemy 2、Pydantic Settings
- 数据（独立版，默认）：SQLite 单文件（`apps/backend/data/novel_studio.db`），无外部依赖；Redis 可选
- 数据（Docker 备选）：PostgreSQL 16 + pgvector、Redis 7
- 运行：独立版双击 `start.bat` 免 Docker；Docker Compose 可选

## 项目结构

```text
ai-novel-studio/
├─ apps/
│  ├─ frontend/
│  │  ├─ src/app/                 # Next.js App Router 页面与全局样式
│  │  ├─ src/components/          # 可复用前端组件（workbench / 插画 / 导出菜单等）
│  │  ├─ Dockerfile
│  │  └─ package.json
│  └─ backend/
│     ├─ app/
│     │  ├─ agents/               # 四个专业 Agent（planner/character/writer/editor）
│     │  ├─ api/                  # 健康检查、CRUD 与 Agent API
│     │  ├─ core/                 # 环境配置
│     │  ├─ db/                   # SQLAlchemy 引擎与初始化（SQLite/PG 双后端）
│     │  ├─ models/               # Novel/Character/World/Chapter/Memory
│     │  ├─ prompts/              # Agent Prompt 模板与加载器（含 deslop.md）
│     │  ├─ schemas/              # Pydantic API 契约
│     │  ├─ services/             # 工作台逻辑与可切换 AI Provider
│     │  └─ main.py               # FastAPI 入口
│     ├─ Dockerfile
│     ├─ requirements.txt         # Docker / 全量依赖
│     └─ requirements-standalone.txt  # 独立版依赖（SQLite，无 PG/pgvector）
├─ scripts/                       # 数据导入、独立性启动器、校验脚本
├─ .env.example                   # 环境变量模板（提交到仓库）
├─ .gitignore                     # 忽略 .env、.venv、.next、data/ 等
├─ docker-compose.yml
├─ start.bat / stop.bat           # 独立版一键启动 / 停止（Windows）
├─ package.json
└─ DAY1_REPORT.md
```

## 快速开始

### 方式 A：独立版（推荐，免 Docker）

前置：Node.js 22+、Python 3.13+。

**最简方式**：双击根目录 `start.bat`，首次自动创建后端虚拟环境、安装依赖、导入数据并构建前端；`stop.bat` 停止服务。

手动启动：

```powershell
# 后端（PowerShell 窗口 1）
cd apps/backend
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-standalone.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 9000

# 前端（PowerShell 窗口 2）——独立版 standalone 产物
cd apps/frontend
npm install
npm run build
node .next/standalone/apps/frontend/server.js
```

默认地址（独立版）：

- Web 工作台：http://localhost:3000
- FastAPI：http://localhost:9000
- OpenAPI 文档：http://localhost:9000/docs
- 健康检查：http://localhost:9000/api/v1/health

### 方式 B：Docker 全栈

前置：Docker Desktop 已启动。

```powershell
cd ai-novel-studio
Copy-Item .env.example .env   # 首次克隆时执行
docker compose up --build -d
docker compose ps
```

默认地址（Docker 模式）：

- Web 工作台：http://localhost:3000
- FastAPI：http://localhost:8001
- OpenAPI：http://localhost:8001/docs
- 健康检查：http://localhost:8001/api/v1/health
- PostgreSQL：`localhost:5434`
- Redis：`localhost:6380`

停止服务：`docker compose down`（加 `-v` 会同时删除本项目数据库与 Redis 数据卷）。

### 本地开发模式

```powershell
# 后端热更新
cd apps/backend
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8001

# 前端热更新
cd apps/frontend
npm install
npm run dev
```

后端启动时会按需建表。生产环境应引入 Alembic 迁移并关闭 `APP_AUTO_CREATE_TABLES`。

## 配置 AI Provider

所有变量记录在 `.env.example`。克隆后执行 `Copy-Item .env.example .env` 再填写真实密钥。

### DeepSeek（默认）

- 开放平台：https://platform.deepseek.com/
- 创建 API Key：https://platform.deepseek.com/api_keys

```env
AI_PROVIDER=deepseek
DEEPSEEK_API_KEY=你的密钥
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-v4-pro
```

### OpenAI（可选切换）

```env
AI_PROVIDER=openai
OPENAI_API_KEY=sk-你的密钥
OPENAI_MODEL=gpt-5.6-terra
```

切换后只需重建后端：`docker compose up -d --build backend`（Docker 模式）或重启 uvicorn（独立版）。

API 调用示例：

```powershell
Invoke-RestMethod -Method Post `
  -Uri http://localhost:9000/api/v1/novels/你的作品ID/agents/planner_agent/generate `
  -ContentType 'application/json' `
  -Body '{"task":"根据现有作品设定规划三幕结构"}'
```

## 数据安全与仓库说明（重要）

本仓库**只包含可公开分享的代码与配置模板**，不含有任何个人数据：

- `.gitignore` 已忽略：`.env`、`.env.local`、`.venv*/`、`node_modules/`、`.next/`、`.out/`、`*.log`、`apps/backend/data/`（SQLite 数据库）、`apps/backend/config/ai_config.json`、`apps/backend/generated/`、`.workbuddy/`。
- 真实 API Key 只写入本地 `.env`，**切勿提交**；`.env.example` 是空模板，可安全入库。
- 小说正文保存在本地 `apps/backend/data/novel_studio.db`，属于个人资产，不随 Git 同步；如需备份请单独复制该文件。
- 公开仓库意味着后端逻辑、Agent 注册表、`app/prompts/`（含 `deslop.md`）等代码对外可见，但不暴露你的小说内容与密钥。

## 数据模型

- `User`：账户、展示名、启用状态及其作品
- `Novel`：书名、梗概、类型、目标字数、状态和创作设置
- `Character`：人物设定、动机、关系、声音和背景
- `World`：世界前提、时代、地点、阵营、规则与时间线
- `Chapter`：章节顺序、大纲、正文、摘要、视角与状态
- `Memory`：可检索故事事实、重要度、来源章节；Docker/PG 模式下可附向量用于语义检索，独立版 SQLite 不强制向量

## 配置四个 AI Agent

已注册以下 Agent：

- `planner_agent`：故事结构与章节规划
- `character_agent`：角色弧光、动机与关系一致性
- `writer_agent`：基于大纲与记忆的章节写作
- `editor_agent`：逻辑、连续性、节奏与文风审校

四个 Agent 共用一个 Provider 配置，保留各自独立的 Prompt。本地默认选择 DeepSeek `deepseek-v4-pro`。

## 章节导出

章节编辑器工具栏提供「导出本章」，工作台提供「导出全书」。支持三种格式：

- **Word(.docx)**：使用 `docx` 库动态生成真正的 OOXML 文档；
- **TXT**：带 BOM 的 UTF-8 纯文本；
- **Markdown**：便于二次编辑与发布。

## 去 AI 味（humanize）

在章节正文工具栏或 AI 创作台调用，提示词见 `app/prompts/deslop.md`（融合去翻译腔 / 去模板 / 去排比 / 降 AI 高频词）。端点：

```
POST /api/v1/novels/{id}/chapters/{cid}/optimize
```

参数：`intensity`（gentle / standard / aggressive）、`apply`（true 则写回 `chapter.content`）。前端提供「预览 → 应用替换」与「整部去 AI 味」两种入口。

## API

- `GET /`：API 元信息
- `GET /live`：进程存活检查
- `GET /health`：数据库与 Redis 健康检查
- `GET /api/v1/health`：版本化健康检查
- `GET /api/v1/studio`：模型和 Agent 清单
- `GET/POST/PATCH/DELETE /api/v1/novels...`：作品及故事资产 CRUD
- `POST /api/v1/novels/{id}/agents/{agent}/generate`：带作品上下文的真实 Agent 调用
- `POST /api/v1/novels/{id}/chapters/{cid}/ai-draft`：自动写作
- `POST /api/v1/novels/{id}/chapters/{cid}/optimize`：去 AI 味精修

> 端口说明：独立版后端为 `9000`，Docker 模式后端为 `8001`，前端均为 `3000`。

## 环境变量

所有变量均记录在 `.env.example`。默认开发端口：`3000`（前端）、`9001`/`9000`（后端，依模式）、`5434`（PG）、`6380`（Redis）。真实密钥只能写入被 Git 忽略的 `.env`。

## 《五世情缘》蓝图数据

当前本地数据库已录入《五世情缘》全文蓝图，共 **310 章**：其中已完成 **71 章（约 27.1 万字）**，待续写 **239 章**；作品目标字数为 **100 万（1,000,000）**。

- 序章从第五世的 ICU 抢救切入，黑白无常奉命接引男主神魂，并尊称其为「星君大人」。
- 楔子在奈何桥旁的照影轩揭示男主是孤辰星君下凡历劫的一缕本源。
- 第一世扩写为 67 章，每章暂定 3000 字，总预算 201000 字；时间从 959 年后周世宗暮年延伸至 965 年平蜀后余乱。
- 第二至第四世各 12 章，通过照影轩继续展开，并穿插照影轩框架章。
- 第一世每个历史阶段均有明确的百姓功德线，包括救流民、立失散簿、护军属、救俘卒、平粮价、安退卒、禁掠、救疫、开仓和撤民。
- 第五世从疫情前夕重新展开，在后段追上序章的 ICU 时间点。
- 孤辰星君历劫圆满后回归天庭，自愿分出部分功德愿力；功德只护住凡身生机，真正完成复苏的是 ICU 医疗团队和凡人宇文信自己的求生意志。
- 神身与第五世凡身最终成为两个连续、独立的生命主体，避免「神魂替代凡人」的伦理问题；凡人宇文信复苏后与秦恒相守。
- 男主五世凡身的共同烙印统一为右手腕内侧天生的心形胎记。历史卷遵循「大事不虚、小事不拘」，不得用神力改变正史结局。

在全新空数据库中重建这套蓝图时，先启动基础设施，再创建本地后端虚拟环境并严格按顺序执行导入脚本：

```powershell
# Docker 模式
docker compose up -d postgres redis
# 或独立版：确保 apps/backend/data 可写

python -m venv apps\backend\.venv
.\apps\backend\.venv\Scripts\python.exe -m pip install -r .\apps\backend\requirements.txt
.\apps\backend\.venv\Scripts\python.exe .\scripts\import_five_lives.py
.\apps\backend\.venv\Scripts\python.exe .\scripts\upgrade_five_lives_v2.py
.\apps\backend\.venv\Scripts\python.exe .\scripts\upgrade_five_lives_star_lord.py
.\apps\backend\.venv\Scripts\python.exe .\scripts\upgrade_first_life_200k.py
```

`upgrade_five_lives_v2.py` 负责胎记统一、初版地府间章、章节字数预算、正史护栏和五世退场逻辑；`upgrade_five_lives_star_lord.py` 建立「第五世危机开场—照影轩回看四世—第五世追平开场—星君归位—凡身复苏」的倒叙框架；`upgrade_first_life_200k.py` 最后把旧版第一世 12 章替换为 67 章历史与功德蓝图。最后一步完成后不要重新运行前面的 v3 脚本；v3 已设置保护性拒绝，避免破坏 310 章排序。所有升级均使用单一数据库事务，失败时不会留下半套数据。

三部宋初题材参考文本的结构统计、优缺点和原创转化边界见 `docs/song-reference-analysis.md`。

录入后可执行完整性检查：

```powershell
.\apps\backend\.venv\Scripts\python.exe .\scripts\verify_five_lives_star_lord.py
```

## 后续迭代建议

1. ✅ 已引入 Alembic 迁移（见 `apps/backend/migrations`），保留开发期自动建表作为兜底；表结构变更统一走迁移。
2. ✅ 已落地去 AI 味、插画画廊、章节导出（Word/TXT/MD）、国产绘图模型多选。
3. 为 Agent 增加结构化输出和「一键写回大纲/章节/记忆」。
4. 实现 `Planner → Character → Writer → Editor → Memory` 可恢复任务队列。
5. 使用向量检索完成长篇记忆切分、嵌入、语义检索和事实冲突检测（Docker/PG 模式）。
6. 增加多用户认证、作品权限、自动化测试和 Token 成本预算。

## License

本项目代码仅供学习与个人创作使用，具体授权以仓库 LICENSE 文件为准。
