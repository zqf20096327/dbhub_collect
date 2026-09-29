# Tour-AI — AI 智能旅行规划助手

基于 Next.js 15 全栈架构的智能旅行规划应用，集成阿里云通义千问大模型，支持 AI 行程生成、小红书笔记批量解析、地图选城、智能住宿推荐、费用预算管理等完整旅行规划流程。

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端框架 | Next.js 15 (App Router) + React 19 + TypeScript |
| UI | TailwindCSS + shadcn/ui + Framer Motion |
| 地图 | Leaflet + React-Leaflet + 高德瓦片 |
| 数据库 | TiDB Cloud (MySQL) + Prisma ORM |
| AI 服务 | 阿里云通义千问 (qwen-max / qwen-turbo / qwen3.5-plus) |
| 内容抓取 | Puppeteer + Cheerio（Edge 浏览器自动化） |
| 状态管理 | Zustand |

## 功能

- **AI 智能行程生成** — 输入目的地、天数、人数、预算及兴趣标签，生成包含景点、交通、住宿、餐饮的完整方案，附带四维费用预估和当地人宝藏小店推荐
- **交互式地图选城** — 高德地图瓦片覆盖 40+ 热门城市，点击地图反查城市名
- **小红书笔记批量解析** — 支持粘贴多条笔记链接，AI 自动提取景点并去重合并为结构化行程
- **智能住宿推荐** — 先根据当日行程终点推荐住宿区域，再推荐区域内具体酒店
- **AI 旅行助手** — 流式对话 AI，实时解答旅行相关问题
- **旅行日记** — 记录旅途点滴，支持心情标记和图文编辑

## 快速开始

```bash
npm install                  # 安装依赖
# 配置 .env（参考 .env.example）
npx prisma db push           # 初始化数据库
npm run dev                  # 启动开发服务器 → http://localhost:3000
```

## 环境变量

| 必填 | 变量 | 说明 |
|------|------|------|
| 🔴 | `DATABASE_URL` | TiDB Cloud MySQL 连接字符串 |
| 🔴 | `QWEN_API_KEY` | 阿里云 DashScope API Key |
| 🟡 | `AMAP_API_KEY` / `NEXT_PUBLIC_AMAP_API_KEY` | 高德地图 API Key |
| 🟢 | `XHS_COOKIE` | 小红书登录 Cookie（解析笔记用） |

## 免责声明

本项目仅用于学习、研究和非商业用途。
