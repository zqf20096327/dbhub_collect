# 🌌 梦境星云档案馆

## Dream Nebula Archive

> **每一个梦境都是宇宙中独特的星辰，让 AI 解析你的潜意识，在星空中找到属于你的那颗星**

---

**YashanDB AI 应用挑战赛** 参赛作品

[![Next.js](https://img.shields.io/badge/Next.js-15.5-black?style=flat-square&logo=next.js)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.8-blue?style=flat-square&logo=typescript)](https://www.typescriptlang.org/)
[![Python](https://img.shields.io/badge/Python-3.9-yellow?style=flat-square&logo=python)](https://www.python.org/)
[![YashanDB](https://img.shields.io/badge/YashanDB-23.2-orange?style=flat-square)](https://yashandb.com/)
[![DeepSeek](https://img.shields.io/badge/DeepSeek-API-purple?style=flat-square)](https://www.deepseek.com/)

---

## 项目简介

**梦境星云档案馆**是一个融合了 AI 分析、3D 可视化和诗意交互的沉浸式梦境记录平台。

在这里，每一个梦境都被转化为一颗独特的星星，漂浮在以情感为引力的星云之中。通过 DeepSeek AI 的情感分析和荣格心理学视角的解梦报告，用户可以深入探索自己的潜意识世界，发现那些隐藏在梦境背后的心灵密码。

### 🎯 核心功能

| 功能 | 描述 |
|------|------|
| 📝 **诗意梦境记录** | 自由记录梦境内容，支持实时字数统计 |
| 🎭 **AI 情感分析** | DeepSeek 驱动的情感分类（愉悦、平静、忧郁、焦虑、恐惧） |
| 🔮 **赛博周公解梦** | 基于荣格心理学流派的深度梦境解读 |
| 🌌 **3D 梦境星云** | Canvas 渲染的动态星空，每颗星星代表一个梦境 |
| 🎨 **程序化星云生成** | 根据梦境情感类型生成独特的星云背景图 |
| 📊 **情感统计仪表板** | 可视化展示梦境情感分布与时间趋势 |
| 💾 **YashanDB 数据持久化** | 使用 YashanDB 存储和检索梦境数据 |
| 🌊 **沉浸式交互体验** | 果冻质感 UI、流光动画、诗意化交互反馈 |

---

## 技术架构

```
┌─────────────────────────────────────────────────────────┐
│                   用户界面层                            │
│  Next.js 15.5 + React 19 + TailwindCSS + Canvas API    │
│  • 3D 星云可视化  • 程序化星云生成  • 沉浸式交互       │
└─────────────────────────────────────────────────────────┘
                         ↕ HTTP/REST API
┌─────────────────────────────────────────────────────────┐
│                   应用服务层                            │
│  FastAPI + Python 3.9 + yaspy (YashanDB Driver)        │
│  • 梦境 CRUD  • 情感分析  • 梦境解读  • 统计分析       │
└─────────────────────────────────────────────────────────┘
                         ↕ YashanDB Protocol
┌─────────────────────────────────────────────────────────┐
│                   数据存储层                            │
│  YashanDB 23.2 + Connection Pool + Transactions        │
│  • 梦境数据  • 情感标签  • 解读报告  • 统计聚合       │
└─────────────────────────────────────────────────────────┘
                         ↕ HTTPS
┌─────────────────────────────────────────────────────────┐
│                   AI 服务层                             │
│  DeepSeek API (deepseek-chat)                          │
│  • 情感分类  • 关键词提取  • 心理学解读               │
└─────────────────────────────────────────────────────────┘
```

### 技术栈详情

#### 前端技术栈
- **框架**: Next.js 15.5 (App Router + Turbopack)
- **语言**: TypeScript 5.8
- **样式**: TailwindCSS 4.0 + CSS Variables
- **3D 渲染**: Canvas API (原生 2D Canvas 绘制星空)
- **状态管理**: React Hooks + Context API
- **UI 组件**: 自定义组件系统

#### 后端技术栈
- **框架**: FastAPI (异步 Python Web 框架)
- **语言**: Python 3.9+
- **数据库驱动**: yaspy (YashanDB 官方 Python 驱动)
- **API 集成**: DeepSeek API (AI 分析引擎)

#### 数据库
- **数据库**: YashanDB 23.2
- **特性**: 连接池管理、事务支持、JSON 数据类型
- **表设计**:
  - `dreams` - 梦境主表
  - `emotions` - 情感分析表
  - `interpretations` - 解读报告表

#### AI 服务
- **提供商**: DeepSeek
- **模型**: deepseek-chat
- **功能**: 情感分类、关键词提取、荣格心理学解读

---

## 核心特性展示

### 🌌 3D 梦境星云可视化

```typescript
// 核心星空渲染逻辑
stars.forEach(star => {
  const emotion = getEmotionColor(star.emotion);
  const size = calculateStarSize(star.emotion_score);
  drawStar(ctx, star.x, star.y, size, emotion);
});
```

每颗星星的位置由梦境的创建时间和情感分数决定，颜色反映情感类型，大小表示情感强度。整个星空构成了一幅用户的情感宇宙图谱。

### 🎭 AI 情感分析

```python
async def analyze_emotion(content: str) -> EmotionAnalysis:
    """使用 DeepSeek API 分析梦境情感"""
    prompt = f"""分析以下梦境的情感类型...

    梦境内容：{content}

    请返回：
    - 情感类型（愉悦/平静/忧郁/焦虑/恐惧）
    - 情感分数（0-1）
    - 关键词列表
    """
    return await deepseek_api.chat(prompt)
```

### 🔮 赛博周公解梦

```python
async def interpret_dream(dream_content: str, emotion: str) -> DreamInterpretation:
    """基于荣格心理学流派的梦境解读"""
    prompt = f"""作为荣格心理学派的分析师，请解读以下梦境...

    梦境内容：{dream_content}
    情感基调：{emotion}

    请提供：
    - 梦境摘要
    - 象征符号解读
    - 心理学意义
    - 潜意识信息
    - 生活指引
    """
    return await deepseek_api.chat(prompt)
```

### 💾 YashanDB 数据持久化

```python
# 使用 YashanDB 连接池
async with yashandb_pool.get_connection() as conn:
    async with conn.transaction():
        # 事务性插入梦境数据
        dream_id = await conn.execute(
            "INSERT INTO dreams (user_id, content) VALUES (:1, :2) RETURNING id",
            [user_id, content]
        )
        # 插入情感分析结果
        await conn.execute(
            "INSERT INTO emotions (dream_id, emotion_type, emotion_score) VALUES (:1, :2, :3)",
            [dream_id, emotion_type, emotion_score]
        )
```

---

## 快速开始

### 方式一：Demo 模式（推荐，无需配置）

**在线预览**: [dream-nebula-archive.vercel.app](https://dream-nebula-archive.vercel.app)

本地运行 Demo 模式：

```bash
# 1. 克隆项目
git clone https://github.com/ach3rry/dream-nebula-archive.git
cd dream-nebula-archive

# 2. 安装依赖
npm install

# 3. 启动开发服务器
npm run dev

# 4. 访问 http://localhost:3000
```

Demo 模式使用 32 条精心编写的诗意梦境和完整的 AI 解读报告，无需配置后端和数据库即可体验完整功能。

### 方式二：完整版（需要 YashanDB + DeepSeek API）

#### 前置要求
- Node.js 18+
- Python 3.9+
- YashanDB 23.2+
- DeepSeek API Key

#### 1. 配置环境变量

**前端配置** (`.env.local`):
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_DEMO_MODE=false
```

**后端配置** (`backend/.env`):
```env
YASHANDB_HOST=localhost
YASHANDB_PORT=1688
YASHANDB_USER=sys
YASHANDB_PASSWORD=your_password
YASHANDB_DATABASE=dream_archive

DEEPSEEK_API_KEY=your_deepseek_api_key
```

#### 2. 启动 YashanDB

```bash
# Docker 方式（推荐）
docker run -d \
  -p 1688:1688 \
  -e SYS_PASSWORD=your_password \
  --name yashandb \
  yashandb/yashandb:latest
```

#### 3. 初始化数据库

```bash
cd backend
python init_db.py
```

#### 4. 启动后端服务

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

#### 5. 启动前端服务

```bash
npm run dev
```

访问 http://localhost:3000 开始使用！

---

## 项目结构

```
dream-nebula-archive/
├── app/                      # Next.js App Router
│   ├── page.tsx             # 首页
│   ├── layout.tsx           # 布局
│   ├── globals.css          # 全局样式
│   └── api/                 # API 路由（Next.js 代理）
├── components/              # React 组件
│   ├── dream-nebula.tsx     # 3D 星云可视化
│   ├── dream-form.tsx       # 梦境记录表单
│   ├── dream-card.tsx       # 梦境卡片
│   └── stats-dashboard.tsx  # 统计仪表板
├── lib/                     # 工具库
│   ├── mock-data.ts         # Demo 模式数据
│   ├── api-client.ts        # API 客户端
│   └── nebula-generator.ts  # 星云生成器
├── backend/                 # Python 后端
│   ├── main.py              # FastAPI 应用
│   ├── database.py          # YashanDB 连接池
│   ├── services/
│   │   ├── dream_interpreter.py  # AI 解梦服务
│   │   └── emotion_analyzer.py   # 情感分析服务
│   └── models/              # 数据模型
├── public/                  # 静态资源
└── package.json             # 依赖配置
```

---

## 竞赛亮点

### 🏆 技术创新

1. **YashanDB 深度应用**
   - 连接池管理，提升并发性能
   - 事务处理，保证数据一致性
   - JSON 字段存储复杂解读报告
   - 序列化自动生成梦境 ID

2. **AI 心理学解读**
   - 基于 DeepSeek 的情感分析
   - 荣格心理学流派的解梦框架
   - 结构化解读报告（象征、心理意义、生活指引）

3. **程序化星云生成**
   - 根据情感类型生成不同颜色星云
   - 3D 粒子系统模拟星空运动
   - 每个梦境都有独特的视觉表现

### 🎨 设计理念

- **诗意化交互**: "记录梦境" → "Manifest"（显现）
- **情感可视化**: 将抽象情感转化为具象的星空
- **沉浸式体验**: 果冻质感 UI + 流光动画 + 渐变背景
- **响应式设计**: 适配桌面和移动设备

### 📊 数据展示

- 情感分布饼图
- 时间趋势折线图
- 关键词云图
- 个人梦境统计

---

## 常见问题

### Q: Demo 模式和完整版有什么区别？

**A**: Demo 模式使用预置的 32 条梦境数据和 AI 解读，无需配置后端和数据库，适合快速体验。完整版需要配置 YashanDB 和 DeepSeek API，支持真实的梦境记录和 AI 分析。

### Q: 如何获取 DeepSeek API Key？

**A**: 访问 [DeepSeek 开放平台](https://platform.deepseek.com/) 注册账号并创建 API Key。

### Q: YashanDB 如何部署？

**A**: 推荐使用 Docker 部署，详见 [YashanDB Docker 部署文档](https://yashandb.com/docs/deployment/docker)。

### Q: 梦境数据安全吗？

**A**: 本地部署版本数据完全存储在你的 YashanDB 实例中，不上传到任何第三方服务器（DeepSeek API 仅用于分析，不存储数据）。

---

## 贡献指南

欢迎提交 Issue 和 Pull Request！

---

## 许可证

MIT License

---

## 致谢

- [YashanDB](https://yashandb.com/) - 提供强大的数据库支持
- [DeepSeek](https://www.deepseek.com/) - 提供 AI 分析能力
- [Next.js](https://nextjs.org/) - 现代化的 Web 框架
- [FastAPI](https://fastapi.tiangolo.com/) - 高性能 Python Web 框架

---

## 联系方式

- 作者: ach3rry
- GitHub: [ach3rry/dream-nebula-archive](https://github.com/ach3rry/dream-nebula-archive)
- Email: (参赛联系方式)

---

**让每一个梦境都在星空中找到它的位置** ✨

**参赛项目**: YashanDB AI 应用挑战赛
