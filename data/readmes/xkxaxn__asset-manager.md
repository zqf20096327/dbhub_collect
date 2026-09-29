# Asset Manager (资产管理系统)

一个基于 Next.js + Prisma + SQLite 构建的个人资产管理系统，提供直观的资产统计、图表分析以及对账功能。

## 🛠️ 技术栈

- **前端框架**: Next.js (App Router), React 19
- **样式方案**: Tailwind CSS (v4)
- **图表库**: Recharts
- **图标库**: Lucide React
- **数据库**: SQLite (通过 Prisma ORM 访问)
- **鉴权**: 基于 JWT 的简单密码访问控制

***

## 🚀 快速开始 (本地开发)

### 1. 环境准备

请确保你的开发环境已安装：

- [Node.js](https://nodejs.org/) (建议 v20+)
- npm 或 pnpm

### 2. 安装依赖

```bash
npm install
```

### 3. 环境变量配置

在项目根目录创建一个 `.env` 文件（或直接使用系统环境变量），配置你的 JWT 密钥：

```env
JWT_SECRET=your_secure_jwt_secret_key_here
```

*如果不配置，系统将使用默认密钥（仅限开发环境）。*

### 4. 数据库初始化

本项目使用 SQLite 作为数据库。运行以下命令生成 Prisma 客户端并初始化本地数据库：

```bash
npx prisma generate
npx prisma db push
```

### 5. 启动开发服务器

```bash
npm run dev
```

打开浏览器访问 <http://localhost:3000>，首次访问会要求你设置一个访问密码。

***

## 📦 Docker 容器化部署 (推荐)

本项目已配置了高度优化的多阶段 `Dockerfile`，推荐使用 Docker 进行生产环境部署。

### 方式一：使用 Docker Compose (最简单)

项目根目录提供了 `docker-compose.yml`，它会自动构建镜像、映射端口，并挂载 SQLite 数据卷以实现数据持久化。

1. **构建并启动容器**：
   ```bash
   docker-compose up -d --build
   ```
2. **停止容器**：
   ```bash
   docker-compose down
   ```
3. **查看日志**：
   ```bash
   docker-compose logs -f
   ```

**数据持久化说明**：
SQLite 数据库文件会自动保存在 Docker 挂载的 `asset-manager-data` 卷中。即使容器被删除，只要数据卷还在，你的资产数据就不会丢失。

### 方式二：手动构建与运行 Docker 镜像

如果你不使用 Docker Compose，也可以手动执行：

1. **构建镜像**：
   ```bash
   docker build -t asset-manager:latest .
   ```
2. **运行容器**：
   ```bash
   # 请在宿主机创建一个目录用于存放数据库，例如 /path/to/your/data
   docker run -d \
     -p 3000:3000 \
     --name asset-manager \
     -v /path/to/your/data:/app/data \
     -e JWT_SECRET=your_production_secret_key \
     asset-manager:latest
   ```

***

## 📂 核心目录结构

- `src/app/`: Next.js 页面路由和全局布局。
- `src/components/`: 可复用的通用 UI 组件和图表组件。
- `src/features/`: 按照业务功能划分的复杂组件（如资产表单、对账面板）。
- `src/server/actions/`: Next.js Server Actions，处理所有的后端业务逻辑和数据库交互。
- `src/lib/`: 工具函数，如 Prisma 实例实例化和汇率格式化。
- `prisma/`: 包含数据库 Schema 和迁移记录。

