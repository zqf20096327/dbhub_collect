<div align="center">

<img src="docs/images/logo.svg" alt="NexaClip" width="112">

# NexaClip

**把视频变成你的知识库。**

[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL--3.0-blue.svg)](LICENSE)
[![CI](https://github.com/hougeai/nexaclip/actions/workflows/ci.yml/badge.svg)](https://github.com/hougeai/nexaclip/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python&logoColor=white)
![Vue 3](https://img.shields.io/badge/Vue-3-42B883?logo=vuedotjs&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?logo=fastapi&logoColor=white)
[![GitHub stars](https://img.shields.io/github/stars/hougeai/nexaclip?style=social)](https://github.com/hougeai/nexaclip)
[![GitHub forks](https://img.shields.io/github/forks/hougeai/nexaclip?style=social)](https://github.com/hougeai/nexaclip/forks)

[特性](#特性) · [快速开始](#快速开始) · [已知限制](#已知限制) · [部署指南](docker/README.md) · [反馈问题](https://github.com/hougeai/nexaclip/issues)

<img src="docs/images/landing.webp" alt="NexaClip 落地页" width="920">

</div>

粘贴链接或上传文件，自动完成下载 → 句级转写 → AI 图文报告 → 向量索引；之后你可以跨库检索问答、在时间轴上标注高光，也能把外语视频译成带双语字幕和母语配音的版本。

自托管：FastAPI + Vue 3 + SQLite（sqlite-vec），AI 能力走千流云 OpenAI 兼容网关（一把 key），无 GPU、无本地大模型依赖。

---

## 目录

- [NexaClip](#nexaclip)
  - [目录](#目录)
  - [特性](#特性)
  - [界面](#界面)
  - [快速开始](#快速开始)
    - [Docker](#docker)
    - [本地开发](#本地开发)
    - [关键环境变量](#关键环境变量)
    - [反爬 cookies](#反爬-cookies)
  - [已知限制](#已知限制)
  - [架构与结构](#架构与结构)
  - [文档](#文档)
  - [参与贡献](#参与贡献)
  - [许可证](#许可证)
  - [免责声明](#免责声明)

## 特性

- 📥 **多源采集** — 抖音 / B 站（链接、BV 号、b23.tv 短链）/ yt-dlp 支持的上千站点 / 本地上传（DRM、私密视频的兜底）；贴链接即自动下载，批量并发
- 🔄 **订阅自动采集** — 关注创作者主页，每日定点自动枚举新视频并入库（下载 → 转写 → 报告 → 索引全链路）
- 📝 **句级转写** — ASR 产出带时间戳的逐句文案，点任意一句跳到视频对应进度；自动检测源语言
- 🤖 **AI 图文报告** — 大纲 + 章节时间轴 + Markdown 报告，两分钟看完长视频
- 🔍 **知识库问答** — 向量 + 关键词混合召回、RRF 融合、重排；跨视频问答与单视频问答，**答案引用可点击直跳原视频秒数**
- ✨ **时间轴高光** — LLM 标注金句 / 冲突 / 核心概念 / 转折点，时间轴可视化；选中片段可导出（合并 mp4 或分条 zip）
- 🌐 **翻译与配音** — 外语视频译成中/英：双语 srt、画面烧录译文字幕、TTS 自然语速配音替换原音轨
- 🔐 **多用户隔离** — 全局共享库按用户归属（同一视频只下载一次），配额与并发闸

## 界面

| 视频采集 | 订阅账号 |
| :-: | :-: |
| <img src="docs/images/collect.webp" alt="视频采集页面" width="470"> | <img src="docs/images/subscriptions.webp" alt="订阅账号页面" width="470"> |

| 采集卡片详情 | 检索与知识库 |
| :-: | :-: |
| <img src="docs/images/detail.webp" alt="采集卡片详情：播放器 + 时间轴高光 + 文案 / 问答 / 报告 / 字幕 / 配音" width="470"> | <img src="docs/images/knowledge.webp" alt="检索与知识库：跨视频混合召回" width="470"> |

## 快速开始

**环境要求**：Python ≥ 3.12、Node ≥ 20、FFmpeg、uv、pnpm

### Docker

```bash
# 构建上下文必须是仓库根（Dockerfile 里 COPY backend/...）
docker build -f docker/Dockerfile -t nexaclip .
docker run -d -p 7860:7860 -v $PWD/data:/app/data --env-file backend/app/.env nexaclip
```

### 本地开发

```bash
# 后端
cd backend && uv sync
cp app/.env.example app/.env          # 填 QL_KEY（千流云）等，见下
cd app && ../.venv/bin/python main.py  # 端口见 BACK_END_PORT，默认 7860

# 前端（另开终端）
cd frontend && pnpm install && pnpm dev  # Vite proxy 转发 /api 到后端
```

打开 `http://localhost:5173`，注册即用。API 交互文档：`http://<后端>/docs`。

更细的部署说明（反向代理、持久卷、静态托管）见 [docker/README.md](docker/README.md)。

### 关键环境变量

| 变量 | 说明 |
| --- | --- |
| `QL_KEY` | 千流云 key——chat / embedding / rerank / ASR / TTS 全链路共用一把 |
| `JWT_SECRET_KEY` | 务必固定，随机值会令每次重启全员掉线 |
| `SUPER_ADMIN_EMAIL` / `SUPER_ADMIN_PASSWORD` | 首启自动创建管理员 |
| `BACK_END_PORT` | 后端端口（默认 7860） |
| `DOWNLOAD_CONCURRENCY` / `USER_QUOTA_*` | 下载并发闸与配额 |

### 反爬 cookies

用浏览器扩展「Get cookies.txt LOCALLY」登录目标站后导出 Netscape txt，放到 `backend/app/data/cookies/` 下对应文件即可：

```
www.youtube.com_cookies.txt
www.douyin.com_cookies.txt
www.bilibili.com_cookies.txt
```

路径可用 `.env` 的 `YOUTUBE_COOKIES` / `DOUYIN_COOKIES` / `BILIBILI_COOKIES` 覆盖。单视频采集无需登录，订阅抖音 / B 站创作者主页需要 cookies。

## 已知限制

- **平台反爬会变**：抖音 Web detail 接口要求 SecSDK 签名（缺失时 403 `Blocked by ArgusSecurityPlugin ...`）；B 站 API 要求访客指纹 `buvid3`（缺失时 412 `request was banned`）。实现与换盐步骤见 [docs/douyin-secsdk.md](docs/douyin-secsdk.md)。
- **cookies 需自备，且会过期**：按导出文件自带的过期时间戳，抖音 `sessionid` 约 **60 天**、B 站 `SESSDATA` 约 **90 天**；但平台风控可提前作废（异地登录、改密码、触发验证）。失效表现为 403 / 412 或「未登录」文案，重新导出覆盖即可。
- **DRM / 私密 / 会员视频**：不绕过 DRM，请用「本地上传」兜底。
- **AI 能力依赖千流云**：未配置 `QL_KEY` 时，转写 / 报告 / 问答 / 配音不可用。

## 架构与结构

- **后端** FastAPI · Tortoise ORM · SQLite + sqlite-vec + FTS5 · APScheduler · yt-dlp / f2 / B 站 API · FFmpeg · httpx
- **前端** Vue 3 · Vite · Pinia · UnoCSS（无组件库）
- **AI** 千流云：chat · embedding · reranker · asr-pro 转写 · tts-flash 配音

```
backend/app/
├── core/          # 渠道(douyin/bilibili/ytdlp)、转写、AI 报告、RAG、高光、翻译配音、Range、调度…
├── models/        # User / Video(全局媒体库) / UserVid / VideoChunk / Subscription / UserSub
├── controllers/   # 采集编排与全链路状态机
├── api/v1/        # base(用户) / media(采集·知识库·订阅·高光·翻译) / system
└── data/          # db.sqlite3 · store/(成品与派生产物) · work/ · logs/ · cookies/

frontend/src/
├── views/console/ # 采集 / 采集记录 / 知识库 / 订阅
└── components/    # VideoDetailModal（播放器 + 时间轴高光 + 文案/问答/报告/高光/字幕/配音 6 tab）等
```

## 文档

| 文档 | 内容 |
| --- | --- |
| [docs/architecture.md](docs/architecture.md) | 架构、核心设计决策、数据模型、API 契约 |
| [docs/frontend.md](docs/frontend.md) | 前端技术栈与设计系统 |
| [docs/rag-design.md](docs/rag-design.md) | 语义检索与视频问答的实现设计 |
| [docs/roadmap.md](docs/roadmap.md) | 设计取舍与明确不做的事 |
| [docs/douyin-secsdk.md](docs/douyin-secsdk.md) | 抖音签名算法与换盐维护手册 |
| [docker/README.md](docker/README.md) | 部署细节 |

## 参与贡献

欢迎 issue / PR。动代码前请先看 [docs/architecture.md](docs/architecture.md)。

- **规范**：后端 `cd backend && uvx ruff check app && uvx ruff format app`；前端 `cd frontend && pnpm lint && pnpm build`。
- 一个 PR 只做一件事；涉及采集渠道 / 风控的改动请附实测结果。
- **不要提交** `.env`、cookies（`data/cookies/`）、任何密钥，或 `data/` 下的数据库与产物。
- 安全问题请走仓库的 **Security → Report a vulnerability**（私密通告），不要开公开 issue；日志贴出来前先脱敏（cookie / token / 带签名的地址）。

## 许可证

本项目基于 [GNU Affero General Public License v3](LICENSE) 开源。

Copyright (c) 2026 NexaClip contributors.

## 免责声明

本项目仅供个人学习与合法用途，作者不对用途及后果负责：

- 开源协议只授予对**本项目源码**的著作权许可，不构成对任何第三方平台服务条款的豁免。
- 请遵守目标平台的服务条款与著作权法规，勿用于批量抓取、内容盗版或商业分发。
- 采集依赖你自己导出的 cookies / 登录态，账号行为由你负责；触发风控导致的限流、封号等后果自负。
- 本项目不绕过 DRM；受版权保护的内容请勿二次分发。
