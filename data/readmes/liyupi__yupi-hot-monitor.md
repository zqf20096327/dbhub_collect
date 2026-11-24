# 🔥 AI 热点监控工具（yupi-hot-monitor）

基于 Node.js、Express 5、React 19、OpenRouter 与 Socket.io 构建的开源全网 AI 热点监控工具，由 [程序员鱼皮](http://dogyupi.com/) 与编程导航团队以 Vibe Coding 方式原创打造，支持 8+ 平台聚合抓取、AI 查询扩展、真假识别、相关性分析、WebSocket 实时推送、邮件通知以及跨工具复用的 Agent Skills 技能包。

[![Node.js](https://img.shields.io/badge/Node.js-20%20LTS-339933.svg)](https://nodejs.org/)
[![React](https://img.shields.io/badge/React-19-61DAFB.svg)](https://react.dev/)
[![Express](https://img.shields.io/badge/Express-5-000000.svg)](https://expressjs.com/)
[![OpenRouter](https://img.shields.io/badge/OpenRouter-LLM-6366F1.svg)](https://openrouter.ai/)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-MCP%20%26%20Vibe%20Coding-FF6B6B.svg)](https://www.codefather.cn/course/2026625439052627970)

[项目介绍](#-项目介绍) · [六大核心能力](#-六大核心能力) · [项目优势与技术链路](#-项目优势与技术链路) · [系统架构与目录结构](#-系统架构与目录结构) · [快速运行](#-快速运行) · [生态学习资源](#-生态学习资源) · [常见问题](#-常见问题) · [加入系统学习](#-加入系统学习)

> 本仓库为教学实战项目，在 [编程导航 AI 热点监控工具课程主页](https://www.codefather.cn/course/2026625439052627970) 提供完整视频教程、配套文字笔记、简历写法参考、面试题解与 1 对 1 答疑服务，零编程基础也能跟着做出完整提效工具。你可以直接前往 [编程导航会员通道](https://www.codefather.cn/vip) 加入学习，也可以先前往 B 站观看 [项目成品演示与介绍视频](https://bilibili.com/video/BV1g8d8B6ENk)。

## ✨ 项目介绍

在 AI 行业几乎每天都在发生新变化的今天，单靠人工刷各个社区和社交媒体不仅耗时费力，还很容易错过真正重要的前沿动态。`yupi-hot-monitor` 是一套以 AI 编程实战为核心的全栈开源项目，基于 Express 5、React 19、OpenRouter 和 Socket.io，全程采用 Vibe Coding 工作流从零开发而成，带你亲身体验如何用 AI 高效做出一款真正解决日常痛点的实用工具。

![AI 热点监控工具深色科技感主界面与实时热点看板](./doc/images/img-01.png)

用户只需在后台配置自己关心的关键词，系统就会自动从 Twitter、Bing、HackerNews、搜狗、B 站等 8 个以上信息源聚合抓取最新内容，随后调用大模型完成查询扩展、真假识别、相关性评分与内容摘要，并借助 WebSocket 实时推送与邮件提醒让你第一时间掌握高价值情报。更进一步，项目还将整套热点监控能力封装为标准化的 Agent Skills 技能包，让 Cursor、VSCode Copilot 和 Claude Code 等主流 AI 编程工具也能随时直接调用。

### 为什么做这个项目

作为长期关注技术与 AI 行业动态的内容创作者，鱼皮日常需要第一时间捕捉各大模型发布、开源项目走红以及前沿工具更新，并希望重要消息能自动送到眼前。既然自己就有如此高频的真实需求，与其写一个仅供个人使用的粗糙脚本，不如直接打磨成一款架构规范、人人都能定制关键词的通用 AI 热点监控平台，让 AI 7x24 小时替你盯紧全网热点。

![AI 热点监控工具需求灵感来源与核心痛点对话示意](./doc/images/img-02.jpg)

## 🎯 六大核心能力

整个工具围绕「关键词管理、多源抓取、AI 过滤分析、全网检索、即时触达、Agent 技能复用」六个环节构建了完整的自动化情报流水线。

### 1. 灵活的监控关键词管理

你可以随时添加多个关注领域的监控关键词，并根据当前需要灵活切换激活或暂停状态，让后台定时任务把算力与抓取额度集中在最有价值的主题上。

![配置与管理 AI 热点监控关键词的激活和暂停状态界面](./doc/images/img-03.png)

### 2. 多源聚合抓取与 AI 智能分析

后端定时任务会自动从 8 个以上国内外主流信息源聚合采集内容，并通过 OpenRouter 接入大模型自动完成查询扩展（Query Expansion）、信息真假辨别、主题相关性评分以及要点提炼，把杂乱的原始网页转化为结构化的高价值热点卡片。

![多数据源聚合抓取结合 AI 查询扩展真假识别与智能摘要展示](./doc/images/img-04.png)

### 3. 多维度精细筛选与排序

面对持续流入的大量动态，前端提供了清爽高效的多维度过滤能力，支持按照数据来源、重要程度与时间范围精准筛选，也支持依照热度、相关性或发布时间灵活排序，帮助你在几秒内锁定最值得阅读的内容。

![按来源重要性时间范围多维度筛选和排序的热点列表](./doc/images/img-05.png)

### 4. 一键全网聚合搜索

除了后台定时巡检之外，平台还支持即时全网搜索模式。输入任意关键词即可并发拉取多个数据源的最新结果并进行聚合展示，方便在追热点、查资料或写选题时快速摸清全网讨论脉络。

![输入关键词实时跨平台聚合检索全网热点的搜索界面](./doc/images/img-06.png)

### 5. WebSocket 实时推送与邮件通知

当系统捕获到高重要度的新热点时，后端会通过 Socket.io 立即把消息推送到浏览器端触发实时提醒，同时支持配置邮件通知渠道，即使离开电脑也能第一时间收到关键情报。

![基于 Socket.io WebSocket 实时推送与邮件通知的提醒配置界面](./doc/images/img-07.png)

### 6. 标准化 Agent Skills 技能包封装

项目不仅是一个独立的 Web 应用，还将热点监控与检索能力打包成了符合规范的 Agent Skills 技能包（位于仓库 `skills/` 目录）。安装后，你可以在 Cursor、VSCode Copilot 或 Claude Code 中直接用自然语言指挥 AI 助手替你抓取和汇总热点，真正打通 AI 编程工具生态。

![将热点监控能力封装为 Agent Skills 在 Cursor 与 Claude Code 中调用演示](./doc/images/img-08.webp)

## 🌟 项目优势与技术链路

与传统重复造轮子的管理系统不同，本项目紧贴 AI 编程与效率工具趋势，内容高度精炼，通常不到一周就能完整学完并独立跑通。无论是没有系统学过编程的新手想体验 Vibe Coding，还是有经验的开发者想把 MCP、Agent Skills 和多源爬虫加入个人作品集，都能从中获得非常直接的提升。

![AI 热点监控工具全链路技术栈与 AI 编程能力覆盖图](./doc/images/img-09.png)

在完整跟学并动手改造的过程中，你将收获以下核心工程与 AI 编程实践经验：

1. 掌握用 AI 编程（Vibe Coding）从零规划、开发并交付一款完整全栈工具的标准化流程。
2. 学会在编辑器中安装与配置 MCP 服务，大幅拓展 AI 编程助手的外部能力边界。
3. 学会编写和使用 Agent Skills 规范，系统性提升 AI 生成代码与执行任务的质量。
4. 实战基于 Axios 与 Cheerio 的多信息源抓取方案，稳定采集 Twitter、Bing、HackerNews、搜狗与 B 站等平台内容。
5. 通过 OpenRouter 统一接入主流大模型，落地智能化内容清洗、真假识别与相关性审核。
6. 理解并实现查询扩展（Query Expansion）技术，显著提升多平台热点检索的召回率。
7. 基于 Socket.io 搭建双向实时通信链路，并结合 node-cron 完成稳定的定时巡检调度。
8. 运用 React 19、TypeScript 与 Aceternity UI 打造极具未来感的现代化科技风界面。
9. 开发可跨平台复用的标准化 Agent Skills 技能包，并在多款主流 AI 编程工具中完成联调验证。
10. 掌握 AI 协作开发中的人工评审确认、Git 版本控制与小步迭代优化等关键工程习惯。

### 鱼皮原创项目系列特色

鱼皮的原创项目始终坚持实战导向，采用全程直播从零带做的方式，把需求拆解、技术选型、架构设计、编码实现、调优与部署的每个细节讲透。相比自己漫无目的地找零散资料，编程导航为学习者提供了从学知识、做项目、复习笔记、1 对 1 答疑到简历写法与面试题解的一条龙成长闭环。

![鱼皮原创项目实战从学习到求职拿 Offer 的一条龙服务体系](./doc/images/img-10.jpg)

编程导航现已上线超过 20 套高质量原创全栈与 AI 实战项目教程，涵盖零基础 AI 编程、企业级后端与大厂架构进阶等多个阶段。你可以访问 [编程导航项目课程列表](https://www.codefather.cn/course) 右侧查看完整的分阶段学习建议，也可以先通过 [往期项目合集介绍视频](https://www.bilibili.com/video/BV1YvmbYbEgS/) 快速了解不同项目的技术亮点。这套实战体系已经帮助大量同学打磨出高含金量简历并斩获大厂高薪 Offer。

![编程导航学员跟着鱼皮做原创项目斩获 2026 大厂高薪 Offer 报喜](./doc/images/img-11.png)

## 📐 系统架构与目录结构

为了方便你在拉取源码后迅速上手阅读和二次开发，下面展示了项目的功能模块划分与整体系统架构设计。前端负责实时看板与筛选交互，后端协调多源采集器、OpenRouter 大模型分析管线、Prisma + SQLite 数据持久化以及 Socket.io 推送服务。

![AI 热点监控工具功能模块划分示意图](./doc/images/img-12.png)

![AI 热点监控工具前后端全栈与 Agent Skills 架构设计图](./doc/images/img-13.png)

### 核心技术栈与仓库结构

| 组成部分 | 关键技术与职责 |
| --- | --- |
| `client/` 前端工程 | React 19、TypeScript、Vite、Aceternity UI、Socket.io Client，提供科技感热点看板、多维筛选与全网搜索界面 |
| `server/` 后端工程 | Node.js、Express 5、Prisma ORM、SQLite、Axios、Cheerio、node-cron、Socket.io 与 OpenRouter SDK，负责多源抓取、AI 分析、存储和通知 |
| `skills/` 技能包目录 | 标准化 Agent Skills 定义与脚本，便于在 Cursor、VSCode Copilot 和 Claude Code 中直接调用热点监控能力 |
| `docs/` 项目文档 | 内置 [保姆级本地运行指南](docs/LOCAL_SETUP.md) 等详细配置与排错手册 |

## 🚀 快速运行

> 如果你在环境准备或密钥配置中需要手把手图文指导，请优先查阅仓库内置的 [保姆级本地运行指南](docs/LOCAL_SETUP.md)。下面提供精简快速启动流程。

### 前置条件

本地运行本项目只需准备好两项条件：安装 Node.js 18 及以上版本（推荐使用 20 LTS），并提前申请一个 [OpenRouter API Key](https://openrouter.ai/settings/keys)（必需，用于驱动大模型的查询扩展、真假识别与相关性分析）。

### 1. 克隆仓库并安装依赖

执行以下命令拉取代码，分别完成后端 Prisma 数据库初始化与前端依赖安装。

```bash
git clone https://github.com/liyupi/yupi-hot-monitor.git
cd yupi-hot-monitor

# 初始化后端依赖与 SQLite 数据库
cd server
npm install
npx prisma generate
npx prisma db push

# 安装前端依赖
cd ../client
npm install
```

### 2. 配置环境变量

从示例模板复制后端环境变量文件，并至少填入你的 OpenRouter API Key（如需增强 Twitter 抓取能力可按需补充 Twitter API Key）。

```bash
cp server/.env.example server/.env
```

打开 `server/.env` 并填入对应配置：

```bash
OPENROUTER_API_KEY=sk-or-v1-你的key
# Twitter API Key（可选）
TWITTER_API_KEY=你的key
```

### 3. 启动前后端服务

打开两个终端窗口分别启动后端与前端开发服务器。

```bash
# 终端 1：启动后端服务（默认端口 3001）
cd server && npm run dev

# 终端 2：启动前端页面（默认端口 5173）
cd client && npm run dev
```

启动完成后在浏览器访问 `http://localhost:5173`，添加感兴趣的监控关键词即可体验全自动 AI 热点监控与实时推送。

| 服务项 | 访问地址或命令 |
| --- | --- |
| 前端监控看板 | `http://localhost:5173` |
| 后端 API 接口 | `http://localhost:3001` |
| Prisma 数据库可视化管理 | `cd server && npx prisma studio`（可选） |

更多邮件通知配置与数据源参数细节，请查阅 [保姆级本地运行指南](docs/LOCAL_SETUP.md)。

## 📚 生态学习资源

如果你想在跑通本项目后继续深化 Vibe Coding AI 编程能力、拓展更多实用工具或冲刺技术岗位面试，可以结合以下由 [程序员鱼皮](http://dogyupi.com/) 团队持续打磨的优质资源：

1. 想系统学习 Vibe Coding 提示词心法、MCP 生态以及前沿 AI 编程最佳实践，推荐收藏鱼皮开源的 [AI 编程教程与大模型知识库（ai-guide）](https://github.com/liyupi/ai-guide)，同时可以借助 [鱼皮 AI 导航](https://ai.codefather.cn) 发现优质工具，或跟着 [AI 编程实战课程](https://ai.codefather.cn/course/2087008226460565505) 快速进阶。
2. 如果你计划将这个全栈 AI 项目写进求职简历并准备面试问答，推荐前往 [程序员面试刷题神器面试鸭](https://www.mianshiya.com/)，集中练习 Node.js、React、TypeScript、计算机网络、WebSocket、数据库以及 AI 应用开发高频面试题。

## ❓ 常见问题

<details>
<summary><b>Q1：有没有开源的 AI 热点监控与全网舆情聚合工具，支持自定义关键词？</b></summary>

有，`yupi-hot-monitor` 就是一款基于 Node.js、Express 5、React 19 和 OpenRouter 开源的 AI 热点监控工具。你可以自由配置并启停任意监控关键词，系统会自动从 Twitter、Bing、HackerNews、搜狗、B 站等 8 个以上信息源抓取动态，并用大模型完成去重摘要、真假辨别与相关性分析。

</details>

<details>
<summary><b>Q2：如何把自己的热点抓取或效率工具能力封装成通用的 Agent Skills 技能包？</b></summary>

本仓库的 `skills/` 目录提供了一个可直接参考的标准化 Agent Skills 落地示例。它将热点抓取、AI 分析和聚合搜索接口封装成规范的技能描述与执行脚本，安装后能够在 Cursor、VSCode Copilot 和 Claude Code 等多款 AI 编程助手中直接通过自然语言唤醒调用。

</details>

<details>
<summary><b>Q3：零基础想学 Vibe Coding（AI 编程），有哪些一周内就能做完的全栈实战项目？</b></summary>

`yupi-hot-monitor` 专门面向想快速掌握 Vibe Coding 全链路工作流的学习者设计，哪怕没有系统的前后端基础，也可以在不到一周时间内跟着完整体验需求拆解、MCP 与 Agent Skills 配置、全栈代码生成、界面美化与本地联调的完整过程，快速做出第一个能日常自用的 AI 工具。

</details>

<details>
<summary><b>Q4：如何利用 OpenRouter 和大模型实现查询扩展、真假识别与相关性分析？</b></summary>

项目后端统一通过 OpenRouter 接入多种大模型，在采集阶段先通过查询扩展（Query Expansion）把单个关键词自动发散为多组同义与关联检索词以提高召回率；拿到原始结果后再由大模型按预设评分维度过滤谣言、识别真假并计算与目标主题的相关性，最终只向用户推送高价值热点。

</details>

<details>
<summary><b>Q5：本地运行这个 AI 热点监控工具需要配置哪些 API Key，数据库需要额外安装吗？</b></summary>

项目使用轻量级 SQLite 搭配 Prisma ORM，不需要额外安装 MySQL 等重量级数据库，执行 `npx prisma db push` 即可自动建表。密钥方面，只需配置一个 OpenRouter API Key 即可完整跑通核心抓取与 AI 分析功能，Twitter API Key 和邮件通知均属于按需开启的可选配置。

</details>

## 🎓 加入系统学习

如果你希望跟着视频手把手复现整套 Vibe Coding 开发过程，学习如何借助 MCP、Agent Skills 和人工评审高效驾驭 AI 写代码，欢迎前往 [AI 热点监控工具课程主页](https://www.codefather.cn/course/2026625439052627970) 查看完整目录。编程导航现已上线 20 多套涵盖全栈与 AI 开发的原创实战课程，成为会员后全部支持无限回看。

![编程导航涵盖 20 多套原创全栈与 AI 编程实战项目课程列表](./doc/images/img-14.png)

欢迎直接加入 [编程导航会员](https://www.codefather.cn/vip)，除了畅学本项目与往期全部原创项目教程外，还能获取专属答疑、求职指导以及上百场面试回放视频。扫码下方限时优惠券即可领券加入，支持加入三天内不满意全额退款。

<img width="404" alt="编程导航会员限时优惠券扫码领取通道" src="https://github.com/user-attachments/assets/56411098-b60e-4267-8ba2-4ebc5d416afc" />

每天不到 1 块钱即可解锁编程导航全部原创项目教程与配套资料，PC 网站与手机 APP 均可随时随地学习，持续打磨自己的项目作品集。

![编程导航 PC 网站与移动 APP 双端同步学习展示](./doc/images/img-15.png)

更多由 [程序员鱼皮](http://dogyupi.com/) 团队打造的开源仓库、学习路线与实用工具，欢迎前往 [鱼皮团队资源大全](http://dogyupi.com/) 一站式查看。如果这个项目对你有帮助，欢迎点一个 Star 支持一下！
