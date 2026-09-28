<div align="center">

# ✨ Aureka

**开源 AI 数据分析平台 · 上传表格，像聊天一样做数据分析**

上传 Excel / CSV，用自然语言提问，AI 自动生成 SQL、图表与分析报告。
无需编程，即时洞察，让数据价值触手可及。

[![License](https://img.shields.io/badge/license-GPL--3.0-blue.svg)](./LICENSE)
[![Node](https://img.shields.io/badge/node-%3E%3D20-339933?logo=node.js&logoColor=white)](https://nodejs.org)
[![pnpm](https://img.shields.io/badge/pnpm-%3E%3D9-F69220?logo=pnpm&logoColor=white)](https://pnpm.io)
[![Vue](https://img.shields.io/badge/Vue-3.5-4FC08D?logo=vue.js&logoColor=white)](https://vuejs.org)
[![NestJS](https://img.shields.io/badge/NestJS-10-E0234E?logo=nestjs&logoColor=white)](https://nestjs.com)
[![LangGraph](https://img.shields.io/badge/LangGraph-Agent-1C3C3C?logo=langchain&logoColor=white)](https://langchain-ai.github.io/langgraphjs/)
[![DuckDB](https://img.shields.io/badge/DuckDB-Analytics-FFF000?logo=duckdb&logoColor=black)](https://duckdb.org)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/MrXujiang/opne-aureka/pulls)

**简体中文** · [English](./README.en.md) · [日本語](./README.ja.md)

[快速开始](#-快速开始) · [功能特性](#-功能特性) · [技术架构](#-技术架构) · [配置说明](#-环境配置) · [参与贡献](#-参与贡献)

![Aureka 演示](./demo.jpg)

</div>

---

## 🔗 更多开源 / 产品推荐

> 如果你喜欢 Aureka，也欢迎了解作者的其他开源项目与产品 👇

| 项目 | 简介 |
| --- | --- |
| 📝 [JitWord 协同AI文档](https://jitword.com) | 类word风格的 AI 文档编辑器，支持知识库管理与 AI 写作 |
| 🎨 [H5-Dooring](https://github.com/MrXujiang/h5-Dooring) | 功能强大的开源 H5 可视化页面搭建平台（LowCode / 零代码） |
| 🗂 [JitKnow AI知识库](https://know.jitword.com) | 多模态AI支持库，支持文档、表格、多媒体混合AI知识管理 |

---

## 📖 项目简介

**Aureka** 是一个开箱即用的 **对话式智能数据分析平台（Chat BI）**：

1. 📤 上传 Excel / CSV 数据集
2. 💬 用自然语言提问，例如「近三个月各渠道销售额对比，哪个渠道下滑最严重？」
3. 🤖 AI Agent 自动完成 **意图识别 → SQL 生成 → DuckDB 查询 → 数据分析 → 图表推荐**
4. 📊 实时流式输出分析结论、数据表格与 ECharts 可视化图表
5. 📑 一键沉淀为分析报告，随时回溯历史会话

整个过程无需编写任何代码，数据全程保存在本地（SQLite + DuckDB），**隐私可控、私有化部署友好**。

## ✨ 功能特性

- 🗣 **自然语言查询**：像聊天一样提问，自动翻译为可执行 SQL
- 🧠 **多意图智能路由**：内置数据查询、对比分析、归因分析、异常检测、趋势预测、统计汇总等分析意图
- ⚡ **流式响应体验**：基于 SSE 的打字机式输出，SQL / 表格 / 图表 / 结论分阶段实时呈现
- 📊 **智能图表推荐**：根据查询结果自动选择合适的图表类型，生成 ECharts 可视化
- 🦆 **高性能分析引擎**：DuckDB 列式引擎驱动，百万行级数据秒级聚合
- 📁 **多格式数据接入**：支持 Excel（.xlsx / .xls）与 CSV 文件上传，自动解析表结构
- 🔌 **多模型支持**：兼容 OpenAI / DeepSeek / 通义千问 / Kimi 等主流 LLM，可自由切换
- 📑 **报告与历史会话**：分析结果可保存为报告，历史对话随时回看
- 🌍 **国际化**：内置中 / 英双语界面
- 🔐 **账号体系**：JWT 鉴权，支持对接 [JitWord](https://next.jitword.com) SSO 单点登录
- 🖥 **精美 UI**：Vue 3 + UnoCSS 打造的玻璃拟态（Glassmorphism）界面

## 🏗 技术架构

### AI Agent 工作流

```mermaid
graph LR
    A[用户提问] --> B[意图识别<br/>Intent Router]
    B --> C[SQL 生成<br/>SQL Generator]
    C --> D[DuckDB<br/>执行查询]
    D --> E[数据分析<br/>Analysis]
    E --> F[图表推荐<br/>Chart Advisor]
    F --> G[SSE 流式输出<br/>结论 + 表格 + 图表]
```

### 技术栈

| 分层 | 技术选型 |
| --- | --- |
| **前端** | Vue 3 · Vite · Pinia · Vue Router · UnoCSS · ECharts · vue-i18n |
| **后端** | NestJS 10 · Passport JWT · SSE 流式推送 |
| **AI 编排** | LangGraph · LangChain · 多 LLM Provider（OpenAI / DeepSeek / Qwen / Kimi） |
| **数据引擎** | DuckDB（分析查询）· SQLite（元数据）· Keyv（缓存） |
| **工程化** | pnpm workspace · Turborepo · TypeScript 全栈共享类型 |

### 目录结构

```
opne-aureka
├── apps
│   ├── server/                 # NestJS 后端
│   │   └── src/modules
│   │       ├── agent/          # LangGraph AI Agent（意图路由 / SQL 生成 / 图表构建）
│   │       ├── analysis/       # DuckDB 分析引擎
│   │       ├── auth/           # JWT 鉴权 + JitWord SSO
│   │       ├── conversation/   # 会话管理（SSE 流式对话）
│   │       ├── dataset/        # 数据集上传与解析
│   │       ├── report/         # 分析报告
│   │       └── settings/       # LLM 模型配置
│   └── web/                    # Vue 3 前端
│       └── src
│           ├── components/     # 业务组件（聊天面板 / 图表 / 数据表格）
│           ├── composables/    # useSSE / useChart / useUpload
│           ├── stores/         # Pinia 状态管理
│           └── views/          # 工作台 / 数据集 / 报告 / 历史 / 设置
└── packages
    └── shared/                 # 前后端共享类型与常量
```

## 🚀 快速开始

### 环境要求

- Node.js >= 20
- pnpm >= 9（`npm i -g pnpm`）

### 一键启动

```bash
# 克隆项目
git clone https://github.com/MrXujiang/opne-aureka.git
cd opne-aureka

# 一键启动（自动安装依赖 + 创建 .env + 同时启动前后端）
pnpm start
```

启动成功后访问：

| 服务 | 地址 |
| --- | --- |
| 🖥 前端界面 | http://localhost:5173 |
| ⚙️ 后端 API | http://localhost:3000 |

### 手动启动

```bash
pnpm install              # 安装依赖
cp .env.example .env      # 配置环境变量（填入你的 LLM API Key）

pnpm dev                  # 同时启动前后端
pnpm dev:web              # 仅启动前端
pnpm dev:server           # 仅启动后端
```

### 生产构建

```bash
pnpm build                # 构建全部
pnpm build:web            # 仅构建前端
pnpm build:server         # 仅构建后端
```

## ⚙️ 环境配置

复制 `.env.example` 为 `.env`，重点关注 LLM 配置：

```bash
# LLM Provider（openai | deepseek | qwen | kimi）
LLM_PROVIDER=deepseek
LLM_API_KEY=your-api-key-here
LLM_BASE_URL=https://api.deepseek.com
LLM_MODEL=deepseek-chat
```

<details>
<summary>📄 完整配置项说明（点击展开）</summary>

| 变量 | 说明 | 默认值 |
| --- | --- | --- |
| `PORT` | 后端服务端口 | `3000` |
| `DATABASE_URL` | 元数据库（SQLite） | `sqlite:./data/metadata.db` |
| `CACHE_STORE` | 缓存驱动（memory / sqlite） | `memory` |
| `STORAGE_DRIVER` | 文件存储驱动 | `local` |
| `UPLOAD_DIR` | 上传文件目录 | `./uploads` |
| `DUCKDB_DATABASE` | DuckDB 数据库文件 | `./data/analysis.duckdb` |
| `JWT_SECRET` | JWT 密钥（生产环境务必修改） | - |
| `JWT_EXPIRES_IN` | Token 有效期 | `7d` |
| `JITWORD_BASE_URL` | JitWord SSO 服务地址 | `https://next.jitword.com` |
| `LLM_PROVIDER` | 大模型提供商 | `deepseek` |
| `LLM_API_KEY` | 大模型 API Key | - |
| `LLM_MODEL` | 模型名称 | `deepseek-chat` |
| `LLM_TEMPERATURE` | 采样温度 | `0.1` |
| `LLM_MAX_TOKENS` | 最大输出 Token | `4096` |

</details>

## 🧭 使用流程

1. **登录**：本地账号或 JitWord SSO 登录
2. **上传数据**：在数据集页面上传 Excel / CSV，系统自动解析表结构并导入 DuckDB
3. **开始提问**：进入工作台，选择数据集后自然语言提问，例如：
   - *「统计各城市的订单总额，按降序排列」*
   - *「对比 Q1 和 Q2 的销售额，分析变化原因」*
   - *「找出销量异常波动的日期」*
4. **查看结果**：AI 实时输出分析思路、SQL、数据表格与可视化图表
5. **沉淀报告**：将有价值的分析保存为报告，供团队回顾

## 🗺 Roadmap

- [ ] 多表关联查询（JOIN 分析）
- [ ] 数据库直连（MySQL / PostgreSQL 数据源）
- [ ] 仪表盘（Dashboard）自由编排
- [ ] 分析报告导出（PDF / 图片）
- [ ] Docker 一键部署
- [ ] 更多图表类型与自定义主题

## 🤝 参与贡献

欢迎任何形式的贡献！

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feat/amazing-feature`
3. 提交更改：`git commit -m 'feat: add amazing feature'`
4. 推送分支：`git push origin feat/amazing-feature`
5. 提交 [Pull Request](https://github.com/MrXujiang/opne-aureka/pulls)

发现问题？欢迎提交 [Issue](https://github.com/MrXujiang/opne-aureka/issues)。

## 📄 开源协议

本项目基于 [GPL-3.0](./LICENSE) 协议开源。

---

<div align="center">

**如果这个项目对你有帮助，欢迎点一个 ⭐️ Star 支持一下！**

Made with ❤️ by [MrXujiang](https://github.com/MrXujiang)

</div>
