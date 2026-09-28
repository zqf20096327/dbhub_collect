# 🏴‍☠️ 纵横四海

一款基于 Web 的文字航海冒险网页游戏，包含游戏客户端、管理后台和服务端。

## 技术栈

| 端 | 技术 |
|---|---|
| **服务端** | Node.js + Express + MySQL2 + WebSocket (ws) + JWT |
| **管理后台** | Vue 3 + Vue Router + Pinia + Element Plus + ECharts + Axios + Vite |
| **游戏客户端** | Vue 3 + Vue Router + Pinia + Vite |
| **部署** | Nginx 反向代理 + nohup 进程管理 |

## 项目结构

```
zhsh-game/
├── server/                 # 服务端（Express API + WebSocket）
│   ├── src/
│   │   ├── app.js          # 入口，HTTP + WS 服务
│   │   ├── config.js       # 全局配置（从 .env 读取敏感值）
│   │   ├── db.js           # MySQL 连接池
│   │   ├── middleware/      # 中间件（错误处理、JWT 验证等）
│   │   ├── models/          # 数据模型
│   │   ├── routes/          # API 路由
│   │   │   ├── admin/       # 后台管理 API（15 个模块）
│   │   │   ├── auth.js      # 注册/登录
│   │   │   ├── battle.js    # 战斗系统
│   │   │   ├── chat.js      # 聊天系统
│   │   │   ├── ...          # 地图/NPC/任务/宠物/公会/市场/航海/赌场/排行/好友/铁匠
│   │   └── ws/              # WebSocket 实时通信
│   └── .env                 # 环境变量（不提交到仓库）
│
├── admin/                  # 管理后台（Vue 3 SPA）
│   └── src/
│       ├── views/           # 14 个管理页面
│       ├── components/      # 通用组件（ProTable、PageHeader）
│       ├── layout/          # 布局（侧边栏、顶栏、标签页）
│       ├── stores/          # Pinia 状态管理
│       ├── api/             # API 请求封装
│       └── router/          # 路由配置
│
├── client/                 # 游戏客户端（Vue 3 SPA）
│   └── src/
│       ├── views/           # 23 个游戏页面
│       ├── components/      # 游戏组件
│       ├── composables/     # 组合式函数
│       ├── stores/          # Pinia 状态管理
│       └── router/          # 路由配置
│
├── DB_CHANGES.md           # 数据库变更记录
└── .gitignore
```

## 功能概览

### 管理后台（14 个模块）

| 模块 | 功能 |
|---|---|
| 仪表盘 | 在线人数、注册趋势、资源分布、货币统计 |
| 玩家管理 | 玩家列表、搜索筛选、详情（背包/航海/战斗/任务记录） |
| 地图管理 | 7 个城市地图、场景配置、导航关系 |
| 场景管理 | 功能建筑/野外场景/市场/港口分组显示 |
| NPC 管理 | 商人/铁匠/宠物师/任务NPC 配置 |
| 怪物管理 | 怪物属性、掉落配置 |
| 物品管理 | 武器/防具/消耗品/材料/特殊物品 |
| 任务管理 | 主线/支线/日常任务配置 |
| 宠物管理 | 宠物属性、进化、技能 |
| 船舶管理 | 船只属性、速度限制（1-5） |
| 游戏配置 | 分类下拉、键值对配置管理 |
| 枚举管理 | 物品类型/品质/任务状态等枚举维护 |
| 操作日志 | 管理员操作审计 |
| 数据日志 | 数据变更记录 |

### 游戏客户端（23 个页面）

地图探索、城市导航、商店、银行、铁匠铺、市场交易、宠物系统、任务系统、航海、赌场、聊天、公会、排行榜、好友、背包、装备、角色状态、玩家主页、剧情

## 环境要求

- **Node.js** 18+
- **MySQL** 5.7+
- **Nginx**（推荐）
- **npm** 9+

## 部署指南

### 1. 克隆项目

```bash
git clone https://github.com/975269528/zhsh-game_astrbot.git
cd zhsh-game_astrbot
```

### 2. 安装依赖

```bash
# 服务端
cd server && npm install && cd ..

# 管理后台
cd admin && npm install && cd ..

# 游戏客户端
cd client && npm install && cd ..
```

### 3. 配置环境变量

```bash
cp server/.env.example server/.env
```

编辑 `server/.env`：

```env
PORT=3000
WS_PORT=8282
JWT_SECRET=your_random_secret_here
ADMIN_JWT_SECRET=your_admin_secret_here
DB_HOST=127.0.0.1
DB_USER=root
DB_PASSWORD=your_db_password
DB_NAME=zhsh_game
```

### 4. 创建数据库

```sql
CREATE DATABASE zhsh_game CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

导入表结构和初始数据（需根据实际情况准备 SQL 文件）。

### 5. 构建前端

```bash
cd admin && npm run build && cd ..
cd client && npm run build && cd ..
```

### 6. 启动服务

```bash
cd server && npm start
```

或使用 nohup 后台运行：

```bash
cd server && nohup npm start > /dev/null 2>&1 &
```

### 7. Nginx 配置示例

```nginx
server {
    listen 80;
    server_name your-domain.com;

    root /path/to/zhsh-game_astrbot/client/dist;
    index index.html;

    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml;
    gzip_min_length 1000;

    # 游戏 API
    location /api/ {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # WebSocket
    location /ws {
        proxy_pass http://127.0.0.1:8282;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_read_timeout 3600s;
        proxy_send_timeout 3600s;
    }

    # 管理后台 API
    location /admin/api/ {
        proxy_pass http://127.0.0.1:3000/api/admin/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # 管理后台 SPA
    location = /admin {
        return 301 /admin/;
    }

    location ^~ /admin/ {
        alias /path/to/zhsh-game_astrbot/admin/dist/;
        index index.html;
        error_page 404 = /admin/index.html;
    }
}
```

## 本地开发

```bash
# 终端 1 — 启动服务端（端口 3000 + WS 8282）
cd server && npm run dev

# 终端 2 — 启动管理后台（端口 5174，已配置 /api 代理）
cd admin && npm run dev

# 终端 3 — 启动游戏客户端（端口 5173，已配置 /api 和 /ws 代理）
cd client && npm run dev
```

- 管理后台访问：`http://localhost:5174/admin/`
- 游戏客户端访问：`http://localhost:5173/`
- 默认管理员密码：`admin123`（首次登录后请修改）

## 已知问题

| 问题 | 说明 | 状态 |
|---|---|---|
| 进程管理 | 使用 nohup 启动，非 PM2，服务器重启后需手动拉起 | 待优化 |
| 战斗日志 | battle_log 表 result 字段为数字（0/1），前端期望 win/lose，需 SQL 转换 | 已兼容 |
| 注册 IP | Nginx 反向代理下需 `trust proxy` 才能获取真实 IP | 已修复 |
| GitHub 推送 | 邮箱隐私设置需使用 noreply 格式邮箱 | 已修复 |

## 游戏货币

| 货币 | 说明 |
|---|---|
| 铜币 (money) | 基础货币，通过任务/战斗/交易获取 |
| 金币 (gold) | 高级货币，用于特殊功能 |
