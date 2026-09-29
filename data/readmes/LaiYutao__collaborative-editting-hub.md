# 多人在线协作编辑平台

支持多人实时协同编辑文档的协作平台，集成任务管理、即时通讯、视频会议等功能。

## 技术栈

| 层级 | 技术 |
|------|------|
| **后端** | Spring Boot 3.2 + Java 21 + MyBatis |
| **前端** | Vue 3 + Vite + Vue Router |
| **数据库** | OpenGauss (PostgreSQL 兼容) |
| **实时通信** | WebSocket + STOMP + SockJS |
| **视频会议** | Jitsi Meet (iframe 集成) |
| **认证** | JWT + Spring Security + BCrypt |

---

## 功能模块

### 📝 文档编辑
- 富文本编辑器 (Quill)
- Markdown 编辑与预览
- 文档导入 (.txt, .md, .html, .docx)
- 文档导出 (TXT, Markdown, HTML, PDF)
- 模板库快速创建

### 📜 版本控制
- 自动版本历史
- 版本预览与对比
- 一键回滚到任意版本
- 全文搜索

### 👥 实时协作
- 多人同时编辑
- 实时光标显示（彩色标识）
- 在线协作者列表
- 内容实时同步

### 💬 评论系统
- 选中文本评论
- 评论回复
- @提及通知
- 评论实时同步

### 📋 任务管理
- 看板视图 (待处理/进行中/已完成)
- 任务分配 (负责人 + 团队成员)
- 检查清单
- 关联文档
- 截止日期提醒

### 🔔 通知系统
- WebSocket 实时推送
- 多类型通知 (评论/任务/消息/版本)
- 通知分类与过滤
- 一键已读

### 💭 即时通讯
- 私聊 / 群聊
- 图片和文件发送
- 消息回复
- 未读消息提示
- 视频会议 (Jitsi Meet)
- 屏幕共享

### ⚙️ 系统管理
- 用户权限管理
- 角色分配
- 实时性能监控
- 系统参数设置 (站点名称/注册开关/维护模式)
- 功能模块开关
- 操作日志

---

## 快速开始

### 1. 启动数据库

```bash
docker run --name opengauss \
  --privileged=true -d \
  -e GS_PASSWORD=Gauss@123 \
  -p 5432:5432 \
  enmotech/opengauss:latest
```

### 2. 初始化数据库

```bash
# 进入容器
docker exec -it opengauss bash
gsql -h localhost -p 5432 -U gaussdb -d postgres -W Gauss@123

# 创建数据库并执行建表脚本
CREATE DATABASE collab_db;
\c collab_db
\i /tmp/schema.sql
\q
```

### 3. 启动后端

```bash
cd backend
mvn spring-boot:run
```

后端运行在 http://localhost:8080

### 4. 启动前端

```bash
cd frontend
npm install
npm run dev
```

前端运行在 http://localhost:5173

### 5. 设置管理员

```sql
-- 注册用户后，执行 SQL 设置管理员（将 1 改为实际用户 ID）
INSERT INTO user_roles (user_id, role_id) VALUES (1, 1);
```

---

## 项目结构

```
homework_2/
├── backend/                      # Spring Boot 后端
│   └── src/main/
│       ├── java/com/collab/
│       │   ├── config/           # 配置 (Security, WebSocket)
│       │   ├── controller/       # REST 控制器
│       │   ├── dto/              # 数据传输对象
│       │   ├── entity/           # 实体类
│       │   ├── mapper/           # MyBatis Mapper
│       │   ├── service/          # 业务逻辑
│       │   └── util/             # 工具类
│       └── resources/
│           ├── application.yml   # 应用配置
│           └── sql/              # 建表脚本
│
├── frontend/                     # Vue 3 前端
│   └── src/
│       ├── api/                  # API 接口封装
│       ├── components/           # 公共组件
│       ├── composables/          # 组合式函数
│       ├── router/               # 路由配置
│       ├── store/                # 状态管理
│       └── views/                # 页面组件
│
└── docs/                         # 技术文档
    ├── 01-文档编辑与导入导出.md
    ├── 02-文档版本控制与搜索.md
    ├── 03-实时协作与评论同步.md
    ├── 04-任务分配与跟踪.md
    ├── 05-通知系统.md
    ├── 06-即时通讯模块.md
    └── 07-系统管理模块.md
```

---

## 核心 API

| 模块 | 端点 | 描述 |
|------|------|------|
| 认证 | `POST /api/auth/login` | 用户登录 |
| 认证 | `POST /api/auth/register` | 用户注册 |
| 文档 | `GET/POST /api/documents` | 文档 CRUD |
| 文档 | `GET /api/documents/{id}/versions` | 版本历史 |
| 评论 | `POST /api/documents/{id}/comments` | 添加评论 |
| 任务 | `GET /api/tasks/my` | 我的任务 (看板) |
| 通知 | `GET /api/notifications` | 通知列表 |
| 聊天 | `GET /api/chat/rooms` | 聊天室列表 |
| 系统 | `GET /api/system/metrics` | 性能监控 |
| 系统 | `PUT /api/system/settings` | 系统设置 |

---

## 角色权限

| 角色 | 权限 |
|------|------|
| **管理员** | 所有功能 + 系统管理 |
| **编辑者** | 文档编辑、任务管理、聊天 |
| **查看者** | 仅查看授权文档 |

---

## 文档

详细技术文档请参考 `docs/` 目录：

- [文档编辑与导入导出](./docs/01-文档编辑与导入导出.md)
- [版本控制与搜索](./docs/02-文档版本控制与搜索.md)
- [实时协作与评论](./docs/03-实时协作与评论同步.md)
- [任务分配与跟踪](./docs/04-任务分配与跟踪.md)
- [通知系统](./docs/05-通知系统.md)
- [即时通讯](./docs/06-即时通讯模块.md)
- [系统管理](./docs/07-系统管理模块.md)
