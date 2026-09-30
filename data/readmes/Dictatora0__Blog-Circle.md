# Blog Circle - 社交内容互动与行为分析平台

一个基于 Spring Boot 3 和 Vue 3 的前后端分离社交内容平台，提供内容发布互动、关系链管理、行为日志采集与统计分析能力。

## 项目概览

本项目最初来源于课程实践，现按可交付软件成果进行整理与包装。当前版本聚焦于“社交内容互动 + 行为统计分析”主线能力，强调可部署、可测试、可演示、可扩展。

- 支持 Docker 化本地部署与虚拟机部署
- 支持 PostgreSQL / openGauss 兼容数据层
- 覆盖内容发布、评论点赞、好友关系、时间线展示
- 提供基础管理后台与 RBAC 权限控制
- 提供内容审核、敏感词自动拦截、举报处理与管理员审计日志能力
- 提供行为日志采集、统计汇总与 Spark/SQL 双模式分析
- 提供前后端自动化测试与离线部署脚本
- 预留主从复制与读写分离扩展配置
- 包装说明见 `docs/software-copyright-packaging.md`

## 快速一键启动（按顺序执行即可跑通）

适用于 macOS / Linux / Windows（含 WSL）。无需本机安装 JDK/Node，只需 Docker。以下步骤均在仓库根目录执行；若只想记一个命令，可以直接运行：

```bash
# 本地 PostgreSQL 模式一键启动
./deploy.sh local up

# 同步并启动虚拟机（默认 openGauss 集群）
./deploy.sh vm up
```

```powershell
# Windows PowerShell 等效命令
./deploy.ps1 -Target local -Action up
./deploy.ps1 -Target vm -Action up
```

如需更多参数（如指定 compose、跳过同步等），执行 `./deploy.sh --help` 或 `./deploy.ps1 -?` 查看说明。

若本机缺少 Maven / Node.js，可直接使用容器化工具链：

```bash
./scripts/dev/doctor.sh
./scripts/dev/mvnw.sh -version
./scripts/dev/npmw.sh --version
```

## 技术栈

**后端**

- Spring Boot 3.1.5 + MyBatis 3.0.3
- PostgreSQL 42.6.0 / openGauss 3.0.0
- JWT 0.11.5 (身份认证)
- Apache Spark 3.5.0 (数据分析)
- JDK 17

**前端**

- Vue 3.3.4 + Vite 4.5.0
- Element Plus 2.4.1 (UI 组件)
- Pinia 2.1.7 (状态管理)
- Axios 1.5.0 (HTTP 客户端)
- Playwright (E2E 测试)

**数据库**

- PostgreSQL 15 (开发/生产)
- openGauss/GaussDB (支持主备集群)

## 核心功能

### 用户系统

- 注册/登录 (JWT 认证)
- 个人资料管理 (昵称、头像、封面图)
- 密码加密存储 (BCrypt)
- 角色标识与账号状态管理 (ADMIN / USER, ACTIVE / DISABLED)

实现说明：

- 后端通过 `AuthController`、`UserController` 提供 `/api/auth` 和 `/api/users` 系列接口，`UserService` + `UserMapper` 负责对 `users` 表的读写。
- `JwtInterceptor` 统一拦截需要登录的接口，从请求头 `Authorization: Bearer <token>` 中解析并校验 JWT。
- 所有接口返回值通过 `common/Result` 统一封装，前端在 `apps/frontend/src/api/auth.js` 中封装登录、注册、获取当前用户等调用。

### 文章系统

- 发布文章 (支持多图上传，最多 9 张)
- 编辑/删除文章
- 文章列表与详情
- 浏览量统计
- 好友时间线 (仅显示自己和好友的文章)

实现说明：

- 后端由 `PostController` 提供 `/api/posts` 相关接口，`PostService`、`PostMapper` 和 `Post` 实体类负责文章表的增删改查。
- 图片上传由 `UploadController` 处理，文件保存路径和访问前缀由 `file.upload.*` 配置控制，对应前端的 `Upload.vue` / `Publish.vue` 等页面。
- 用户访问文章列表、详情、发布动态时，会在 `access_logs` 表中记录访问行为，为后续统计和 Spark 分析提供数据来源。
- 前端主要页面位于 `apps/frontend/src/views/Posts.vue`、`PostDetail.vue`、`Timeline.vue` 和 `MyPosts.vue`，通过 `apps/frontend/src/api/post.js` 调用后端接口。

### 社交功能

- 好友搜索 (用户名/邮箱/昵称)
- 好友请求 (发送/接受/拒绝)
- 好友列表管理
- 文章评论
- 文章点赞

实现说明：

- 好友相关接口由 `FriendshipController`、`FriendshipService` 和 `Friendship` 实体类实现，对应数据库 `friendship` 表，支持好友申请、同意、拒绝、删除等状态流转。
- 评论功能由 `CommentController`、`CommentService`、`CommentMapper` 和 `Comment` 实体实现，前端页面包括 `PostDetail.vue`、`MyComments.vue` 等。
- 点赞功能由 `LikeController`、`LikeService`、`LikeMapper` 和 `Like` 实体实现，接口统一为 `/api/likes` 系列，前端通过 `apps/frontend/src/api/comment.js`、`like` 相关 API 进行调用。
- 前端社交相关页面集中在 `apps/frontend/src/views/Friends.vue`、`Timeline.vue`、`Home.vue` 等，配合用户登录态展示“我的好友”“好友时间线”等视图。

### 平台治理

- 管理后台 RBAC（管理员概览、用户角色/状态管理）
- 内容审核（动态/评论恢复、隐藏、驳回）
- 敏感词自动审核（发帖/编辑/评论自动拦截并记录原因）
- 举报工单处理（支持联动下线目标内容）
- 审计日志与工单 SLA 看板（自动审核命中、超时工单、处理时长）

实现说明：

- 后端通过 `SensitiveContentService` 在动态与评论的创建、编辑链路上执行敏感词匹配，命中后自动将内容标记为隐藏，并写入 `audit_logs` 作为系统审计记录。
- `ReportService` 在举报列表中为每条工单补充 `slaStatus`、`pendingMinutes`、`slaDeadlineAt` 等衍生字段，管理端可按 SLA 状态筛选“正常 / 临近超时 / 已超时 / 已完成”。
- `AdminService` 会聚合自动拦截动态数、自动拦截评论数、待处理举报数和超时工单数，前端 `AdminConsole.vue` 以概览卡片和工单表格形式展示。
- 个人侧页面 `MyPosts.vue`、`MyComments.vue` 与 `PostDetail.vue` 会展示当前审核状态和处理原因，便于演示“自动审核—人工复核—用户整改”的闭环。

### 数据统计

- 实时统计 (文章数、浏览量、点赞数、评论数)
- 用户活跃度分析
- 文章热度排行
- Spark 大数据分析 (可选)

实现说明：

- 后端由 `StatisticsController` 提供 `/api/stats` 系列接口，`SparkAnalyticsService` 负责执行数据分析逻辑。
- 当调用 `/api/stats/analyze` 时，服务优先尝试使用 Spark 从 GaussDB 主库读取 `access_logs` 数据，计算发文数、浏览量、评论数等聚合结果；若 Spark 不可用则回退到基于 SQL 的统计逻辑。
- 分析结果写入 `statistics` 表，并通过 `/api/stats` 接口以聚合 + 明细的形式返回给前端。
- 前端统计页面位于 `apps/frontend/src/views/Statistics.vue`，通过 `apps/frontend/src/api/statistics.js` 调用上述接口，展示文章数、浏览量、活跃用户数等指标。

### 管理与权限

- 管理后台概览
- 用户角色分配
- 账号启用/禁用
- 基于角色的路由与接口访问控制

实现说明：

- 后端新增 `/api/admin/*` 管理接口，配合 `AccessControlService` 校验管理员身份。
- 用户实体增加 `role` 与 `status` 字段，支持 ADMIN / USER 与 ACTIVE / DISABLED 两组基础权限属性。
- 前端新增 `AdminConsole.vue` 管理页，并通过路由守卫与导航入口实现管理员可见、普通用户不可访问。

### 整体工作流程

1. 用户在浏览器中访问前端页面（登录、时间线、统计、个人中心等）。
2. 前端页面通过 `apps/frontend/src/api/*.js` 中封装的函数向后端发送 HTTP JSON 请求。
3. 后端 `controller` 层接收请求，完成参数校验、权限校验后，调用对应的 `service` 层方法。
4. `service` 层根据业务逻辑调用 MyBatis `mapper` 访问数据库：
   - 写操作（注册、发布动态、点赞、评论等）默认路由到主库（PRIMARY）。
   - 只读查询可以使用 `@ReadOnly` 注解，由切面自动路由到备库（REPLICA）。
5. 数据库操作完成后，后端使用统一的 `Result` 返回结构将结果封装为标准 JSON 响应。
6. 对关键操作（访问文章、创建动态、评论等），后端向 `access_logs` 表追加访问记录，为后续统计和 Spark 分析提供原始数据。
7. 当后台或脚本调用 `/api/stats/analyze` 时，`SparkAnalyticsService` 从 GaussDB 读取访问日志，计算聚合统计结果并写入 `statistics` 表。
8. 前端 `Statistics.vue` 页面通过 `/api/stats` 接口获取统计数据，在页面上展示文章数量、访问量、活跃用户等指标。

## 项目结构

```
CloudCom/
├── apps/backend/                 # 后端服务代码（Spring Boot）
│   ├── src/main/java/com/cloudcom/blog/
│   │   ├── controller/           # HTTP API 控制器
│   │   ├── service/              # 业务逻辑与领域用例
│   │   ├── mapper/               # MyBatis 数据访问层
│   │   ├── entity/               # 领域实体类
│   │   ├── config/               # 安全配置、数据源配置、Web 配置
│   │   ├── aspect/annotation/    # 读写分离等 AOP 相关代码
│   │   └── util/common/          # 工具类、统一返回结构等
│   ├── src/main/resources/
│   │   ├── application.yml                   # 本地 PostgreSQL 配置
│   │   ├── application-gaussdb-cluster.yml   # GaussDB 集群配置（读写分离）
│   │   ├── db/01_init.sql                    # 数据库初始化脚本
│   │   └── mapper/*.xml                      # MyBatis SQL 映射
│   └── pom.xml
├── apps/frontend/                # 前端工程（Vue 3 + Vite）
│   ├── src/views/                # 页面组件（登录、时间线、统计、个人中心等）
│   ├── src/components/           # 可复用 UI 组件
│   ├── src/api/                  # 后端 API 封装
│   ├── src/stores/               # Pinia 状态管理
│   ├── src/router/               # 路由配置
│   └── package.json
├── scripts/                      # 部署与维护脚本（full_verify、rebuild-docker-system 等）
├── apps/analytics/               # 数据分析相关脚本与说明
├── docker-compose.yml            # 本地 PostgreSQL 开发环境
├── docker-compose-opengauss.yml  # 本地 openGauss 集群环境
├── start.sh                      # 统一 compose 运维入口（up/down/logs/status/health/initdb/migrate）
├── deploy.sh                     # 统一本地/虚拟机部署入口
├── sync-to-vm.sh                 # 代码同步到虚拟机
├── start-local.sh                # 兼容入口：等价于 ./deploy.sh local up
├── stop-local.sh                 # 兼容入口：等价于 ./deploy.sh local down
├── start-vm.sh                   # 兼容入口：等价于 ./deploy.sh vm up
├── stop-vm.sh                    # 兼容入口：等价于 ./deploy.sh vm down
├── test-vm-api.sh                # 虚拟机 API 自动化测试脚本
└── README.md                     # 项目文档
```

## 数据库表结构

| 表名          | 说明       | 主要字段                                                          |
| ------------- | ---------- | ----------------------------------------------------------------- |
| `users`       | 用户表     | id, username, password, email, nickname, avatar, cover_image, role, status |
| `posts`       | 文章表     | id, title, content, author_id, view_count, images                 |
| `comments`    | 评论表     | id, post_id, user_id, content                                     |
| `likes`       | 点赞表     | id, post_id, user_id (联合唯一索引)                               |
| `friendship`  | 好友关系表 | id, requester_id, receiver_id, status (PENDING/ACCEPTED/REJECTED) |
| `access_logs` | 访问日志表 | id, user_id, post_id, action                                      |
| `statistics`  | 统计结果表 | id, stat_type, stat_key, stat_value                               |

## API 接口

### 认证接口 (`/api/auth`)

- `POST /register` - 用户注册
- `POST /login` - 用户登录

### 用户接口 (`/api/users`)

- `GET /me` - 获取当前用户信息
- `PUT /me` - 更新个人资料
- `GET /{id}` - 获取用户信息

### 管理接口 (`/api/admin`)

- `GET /overview` - 获取平台概览统计 (需管理员)
- `GET /users` - 条件查询用户列表 (需管理员)
- `PUT /users/{id}/role` - 更新用户角色 (需管理员)
- `PUT /users/{id}/status` - 更新用户状态 (需管理员)

### 文章接口 (`/api/posts`)

- `GET /list` - 获取文章列表
- `GET /{id}/detail` - 获取文章详情
- `GET /timeline` - 获取好友时间线
- `POST /` - 创建文章 (需认证)
- `PUT /{id}` - 更新文章 (需认证)
- `DELETE /{id}` - 删除文章 (需认证)

### 评论接口 (`/api/comments`)

- `GET /post/{postId}` - 获取文章评论
- `POST /` - 发表评论 (需认证)
- `PUT /{id}` - 更新评论 (需认证)
- `DELETE /{id}` - 删除评论 (需认证)

### 点赞接口 (`/api/likes`)

- `POST /post/{postId}` - 点赞文章 (需认证)
- `DELETE /post/{postId}` - 取消点赞 (需认证)
- `GET /post/{postId}/check` - 检查是否已点赞

### 好友接口 (`/api/friends`)

- `POST /request/{receiverId}` - 发送好友请求 (需认证)
- `POST /accept/{requestId}` - 接受好友请求 (需认证)
- `POST /reject/{requestId}` - 拒绝好友请求 (需认证)
- `DELETE /user/{friendUserId}` - 删除好友 (需认证)
- `GET /list` - 获取好友列表 (需认证)
- `GET /requests` - 获取待处理请求 (需认证)
- `GET /search?keyword=xxx` - 搜索用户 (需认证)
- `GET /status/{userId}` - 检查好友状态 (需认证)

### 统计接口 (`/api/stats`)

- `POST /analyze` - 运行数据分析 (需认证)
- `GET /` - 获取所有统计数据 (需认证)
- `GET /{type}` - 获取指定类型统计 (需认证)

### 上传接口 (`/api/upload`)

- `POST /avatar` - 上传头像 (需认证)
- `POST /cover` - 上传封面图 (需认证)
- `POST /image` - 上传文章图片 (需认证)

> **认证方式**：需认证的接口需在请求头中携带 `Authorization: Bearer {token}`

## 部署场景

本系统支持多种部署和运行方式，适用于不同的实验和演示需求：

| 场景           | 说明         | 数据库          | 特性             | 适用场景  |
| -------------- | ------------ | --------------- | ---------------- | --------- |
| 本地开发       | 直接运行源码 | PostgreSQL      | 快速调试         | 日常开发  |
| Docker Compose | 标准容器化   | PostgreSQL      | 一键部署         | 演示/测试 |
| GaussDB 集群   | 一主二备集群 | openGauss       | 读写分离、高可用 | 课程实验  |
| Spark 分析     | 大数据分析   | GaussDB + Spark | 分布式计算       | 扩展实验  |
| 虚拟机部署     | 远程服务器   | GaussDB         | 生产环境模拟     | 课程实验  |

### 部署方式与配置文件

项目根目录包含两份主要 Docker Compose 配置：

- `docker-compose.yml`

  - 用途：本地开发环境（PostgreSQL 单库）
  - 组件：PostgreSQL、后端、前端
  - 启动方式：优先执行 `./deploy.sh local up`，也可直接执行 `./start.sh up`
  - 常用命令：`./start.sh up backend`、`./start.sh logs backend`、`./start.sh down`
  - 访问地址：前端 `http://localhost:8080`，后端 `http://localhost:8082`
  - 说明：Docker 模式下后端连接的是容器内数据库服务 `cloudcom-db`，不是本机 Homebrew PostgreSQL

- `docker-compose-opengauss.yml`

  - 用途：在本机启动 openGauss 一主两备集群及应用
  - 组件：openGauss 主库和两个备库、后端、前端
  - 启动方式：`COMPOSE_FILE=docker-compose-opengauss.yml ./start.sh up` 或 `./deploy.sh --compose docker-compose-opengauss.yml local up`

## 目录

- [快速开始](#快速开始)
  - [虚拟机部署（推荐）](#虚拟机部署推荐)
  - [本地开发](#本地开发)
- [虚拟机部署详情](#虚拟机部署详情)
- [API 测试](#api-测试)
- [架构设计](#架构设计)
- [常见问题](#常见问题)

---

## 快速开始

> 推荐优先使用上方“快速一键启动（Docker Compose）”。本节保留历史虚拟机/手动部署说明，便于兼容旧环境。

### 环境配置（首次使用）

项目使用环境变量管理敏感配置，首次使用需要配置：

```bash
# 1. 复制环境变量模板
cp .env.example .env

# 2. 编辑 .env 填入实际密码（可选，默认使用实验环境配置）
vim .env
```

**环境变量说明**：

- `VM_IP`: 虚拟机 IP 地址
- `VM_USER`: 虚拟机用户名
- `VM_PASSWORD`: 虚拟机密码
- `GAUSSDB_PASSWORD`: 数据库密码

⚠️ 对外演示前请检查 `.env` 中的数据库密码、JWT 密钥与 CORS 配置，避免直接使用默认值。

### 虚拟机部署（推荐）

系统支持部署到指定虚拟机环境。以下地址使用占位符示例，请以 `.env` 或部署脚本中的实际配置为准：

- 建议在 `.env` 中配置 `VM_IP`、`VM_PORT`、`VM_USER`，并优先使用 `VM_SSH_KEY` 指向 SSH 私钥；脚本会优先走密钥登录，无法使用时再回退到 `VM_PASSWORD + sshpass`。

#### 访问地址

- **前端页面**: `http://<VM_IP>:8080`
- **后端 API**: `http://<VM_IP>:8082`
- **健康检查**: `http://<VM_IP>:8082/actuator/health`

#### 演示账号

建议通过初始化脚本或部署后的注册流程自行生成演示账号。若使用开发环境默认数据，请在对外演示前及时重置密码，避免将固定凭据写入公开材料。

#### 一键部署/重启

```bash
# 推荐入口：从本地一键同步并启动虚拟机
./deploy.sh vm up

# 兼容旧用法
./start-vm.sh
```

**脚本功能**：

1. ✓ 检查虚拟机连接
2. ✓ 同步仓库中的部署文件与脚本
3. ✓ 按策略选择远端构建或本地打包传输镜像
4. ✓ 启动 openGauss / Blog Circle 应用服务
5. ✓ 支持状态、日志、健康检查与数据库初始化

**首次部署时间**: 15-20 分钟  
**后续重启时间**: 5-8 分钟（Docker 缓存加速）

#### 管理命令

```bash
# 查看服务状态
./deploy.sh vm status

# 查看后端日志
./deploy.sh vm logs backend

# 停止服务
./stop-vm.sh

# 仅同步代码到虚拟机
./sync-to-vm.sh

# 远端构建模式启动
./start-vm.sh --build

# API 功能测试（18 个测试用例）
./test-vm-api.sh

# SSH 连接虚拟机
ssh $VM_USER@$VM_IP
```

---

### 本地开发

> 推荐优先使用下方“方式一：Docker Compose 一键启动”。

#### 方式一：Docker Compose 一键启动

推荐使用仓库内统一运维脚本启动本地 PostgreSQL、后端和前端：

```bash
# 推荐入口
./deploy.sh local up

# 等效入口
./start.sh up
```

脚本会自动完成：

- 启动 PostgreSQL 容器 `cloudcom-db`
- 构建并启动后端容器 `cloudcom-backend`
- 构建并启动前端容器 `cloudcom-frontend`
- 将前端暴露到 `8080`，将后端暴露到 `8082`

启动后访问：

- 前端：`http://localhost:8080`
- 后端：`http://localhost:8082`
- 健康检查：`http://localhost:8082/actuator/health`
- 数据库（容器映射）：`localhost:5432`

常用命令：

```bash
# 仅重建/重启后端
./start.sh up backend

# 查看后端日志
./start.sh logs backend

# 查看容器状态与接口健康
./deploy.sh local status
./deploy.sh local health

# 停止服务
./start.sh down

# 重新执行容器数据库初始化脚本
./start.sh initdb

# 执行增量迁移
./start.sh migrate
```

> 说明：此模式下后端容器连接的是 Docker 网络内的 `cloudcom-db`。即使本机同时运行了 Homebrew PostgreSQL，也不会被 Docker 后端直接使用。

#### 方式二：源码直跑（可选）

当本机已安装 `mvn`、`node`、`npm`，且你希望直接调试源码而不是跑容器时，可使用此方式。

1. **准备本机 PostgreSQL**

确保本机数据库已存在 `blog_db`，并按需执行初始化/迁移：

```bash
# 首次建库/建表
psql -d blog_db -f apps/backend/src/main/resources/db/01_init.sql

# 已有旧库时补齐 RBAC 与治理能力
psql -d blog_db -f apps/backend/src/main/resources/db/migration_add_user_rbac.sql
psql -d blog_db -f apps/backend/src/main/resources/db/migration_add_governance.sql
```

2. **设置后端数据库连接**

```bash
export DB_URL=jdbc:postgresql://localhost:5432/blog_db
export DB_USERNAME=<你的本机数据库用户名>
export DB_PASSWORD=<你的本机数据库密码>
```

3. **启动后端与前端**

```bash
# 终端 1：启动后端
mvn spring-boot:run -f apps/backend/pom.xml

# 终端 2：安装并启动前端
npm install --prefix apps/frontend
npm run dev --prefix apps/frontend
```

访问地址：

- 前端：`http://localhost:5173`
- 后端：`http://localhost:8080`
- 健康检查：`http://localhost:8080/actuator/health`

> 说明：源码直跑模式下，后端使用的是“本机 PostgreSQL”；这与 Docker 模式下使用的容器数据库是两套独立环境。

---

## 虚拟机部署详情

### 部署架构

```
虚拟机 (<VM_IP>)
│
├─ Docker Network: opengauss-network (172.26.0.0/16)
│   │
│   ├─ opengauss-primary (172.26.0.10:5432)
│   │   └─ 数据库: blog_db
│   │       └─ 用户: bloguser
│   │
│   ├─ opengauss-standby1 (172.26.0.11:15432 → 5434)
│   │
│   ├─ opengauss-standby2 (172.26.0.12:25432 → 5436)
│   │
│   ├─ blogcircle-backend (172.26.0.2:8080 → 8082)
│   │   ├─ Spring Boot 应用
│   │   ├─ JVM: 64-128MB, SerialGC
│   │   └─ 连接: opengauss-primary:5432
│   │
│   └─ blogcircle-frontend (8080)
│       ├─ Vue.js 应用
│       ├─ Nginx 反向代理
│       ├─ 上传限制: 50MB
│       └─ 代理至: blogcircle-backend:8080
```

### 虚拟机环境信息

| 项目           | 值                       |
| -------------- | ------------------------ |
| IP 地址        | `<VM_IP>`                |
| 操作系统       | CentOS/openEuler         |
| Docker 版本    | 18.09.0                  |
| Docker Compose | 1.23.1 (legacy 兼容模式) |
| openGauss 版本 | 5.0.3                    |
| 数据库         | blog_db                  |
| 数据库用户     | bloguser / Blog@2025     |

### 部署配置

（旧的 `docker-compose-opengauss-cluster-legacy.yml` 已废弃，不再推荐使用）：

**主要优化**：

- 移除新版 Docker Compose 不支持的语法
- 后端添加 `privileged: true` 解决 JVM 线程创建问题
- JVM 优化：`-Xms64m -Xmx128m -XX:+UseSerialGC`
- 前端 Nginx 上传限制设置为 50MB
- 使用 MERGE 语句替代 ON CONFLICT（openGauss 兼容）

### 已解决的问题

<details>
<summary><b>1. Docker 版本兼容性</b></summary>

**问题**: 虚拟机 Docker 18.09 不支持新版语法  
**解决**: 创建 legacy 版本配置文件，移除 `healthcheck.start_period` 等

</details>

<details>
<summary><b>2. JVM 线程创建失败</b></summary>

**问题**: `pthread_create failed (EPERM)`  
**解决**: 添加 `privileged: true` 和 capabilities

</details>

<details>
<summary><b>3. 数据库权限</b></summary>

**问题**: `permission denied for schema public`  
**解决**: `GRANT ALL ON SCHEMA public TO bloguser`

</details>

<details>
<summary><b>4. 前端 502 错误</b></summary>

**问题**: Nginx 使用 127.0.0.1 无法访问后端  
**解决**: 改为 `blogcircle-backend:8080`

</details>

<details>
<summary><b>5. 文件上传 413 错误</b></summary>

**问题**: Nginx 默认 1MB 限制  
**解决**: 设置 `client_max_body_size 50M`

</details>

<details>
<summary><b>6. SQL 语法不兼容</b></summary>

**问题**: openGauss 不支持 `ON CONFLICT`  
**解决**: 使用 `MERGE INTO` 语句

</details>

### 离线部署说明

系统采用**完全离线部署策略**：

1. **在本地 Mac 构建镜像**（需要外网）

   - 后端镜像: ~500MB
   - 前端镜像: ~50MB
   - openGauss 镜像: ~400MB

2. **传输镜像到虚拟机**（无需外网）

   - 通过 SSH 传输 tar 文件
   - 虚拟机加载镜像

3. **启动服务**（无需外网）
   - 使用预构建镜像
   - 无需 build 步骤

**优势**：

- 虚拟机无需访问外网
- 版本完全一致
- 部署过程可重复
- 故障恢复过程较快

## 配置说明

### 后端配置 (`application.yml`)

```yaml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/blog_db
    username: lying
    password: 456789
    hikari:
      maximum-pool-size: 10
      minimum-idle: 5

jwt:
  secret: cloudcom-blog-system-secret-key-2025
  expiration: 86400000 # 24小时

spark:
  enabled: false # 是否启用 Spark 分析 (默认使用 SQL)

file:
  upload:
    path: ./uploads
    url-prefix: /uploads

server:
  port: 8080
```

### 后端配置 (`application-gaussdb-cluster.yml`)

用于 GaussDB 一主二备集群环境，实现读写分离：

```yaml
spring:
  datasource:
    primary: # 主库配置 (写操作)
      driver-class-name: org.postgresql.Driver
      jdbc-url: ${GAUSSDB_PRIMARY_URL:jdbc:postgresql://<VM_IP>:5432/blog_db}
      username: ${GAUSSDB_USERNAME:bloguser}
      password: ${GAUSSDB_PASSWORD:your_password_here}
      maximum-pool-size: 10
      minimum-idle: 3
      connection-test-query: SELECT 1
      pool-name: GaussDB-Primary-HikariCP

    replica: # 备库配置 (读操作，负载均衡)
      driver-class-name: org.postgresql.Driver
      jdbc-url: ${GAUSSDB_REPLICA_URL:jdbc:postgresql://<VM_IP>:5432/blog_db}
      username: ${GAUSSDB_USERNAME:bloguser}
      password: ${GAUSSDB_PASSWORD:your_password_here}
      maximum-pool-size: 10
      minimum-idle: 3
      connection-test-query: SELECT 1
      pool-name: GaussDB-Replica-HikariCP

jwt:
  secret: cloudcom-blog-system-secret-key-2025
  expiration: 86400000

file:
  upload:
    path: /app/uploads
    url-prefix: /uploads

server:
  port: 8080

logging:
  level:
    com.cloudcom.blog: INFO
    org.opengauss: WARN
    com.zaxxer.hikari: DEBUG
```

**读写分离实现**：

系统通过 AOP 切面自动路由数据库请求：

- `@ReadOnly` 注解的方法 → 备库 (replica)
- 其他方法（INSERT/UPDATE/DELETE）→ 主库 (primary)

示例代码 (`DataSourceAspect.java`)：

```java
@Around("execution(* com.cloudcom.blog.service.*.*(..))")
public Object routeDataSource(ProceedingJoinPoint point) {
    MethodSignature signature = (MethodSignature) point.getSignature();
    Method method = signature.getMethod();

    if (method.isAnnotationPresent(ReadOnly.class)) {
        DataSourceContextHolder.setDataSource("replica");
    } else {
        DataSourceContextHolder.setDataSource("primary");
    }

    return point.proceed();
}
```

### 前端配置

**开发环境** (`vite.config.js`)：

```javascript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8080',
      changeOrigin: true
    }
  }
}
```

**生产环境** (`nginx.conf`)：

```nginx
location /api {
    proxy_pass http://backend:8080;
}
```

## Spark 数据分析

### Spark 架构

系统集成了 Apache Spark 3.5.0 用于数据分析：

**特点**：

- **内嵌模式**: Spark 引擎集成在 Spring Boot 后端服务中
- **local[*] 模式**: 本地多线程执行，无需独立集群
- **读取数据**: 通过 JDBC 从 openGauss 读取数据
- **备用方案**: Spark 失败时自动回退到 SQL 查询

### Spark 分析说明

**运行模式**：

- Spark 采用 **内嵌模式**，集成在 Spring Boot 后端服务中
- 使用 `local[*]` 本地多线程模式，无需独立集群
- 默认关闭；启用后若执行失败会自动回退到 SQL 直接查询

**配置选项** (`apps/backend/src/main/resources/application.yml`):

```yaml
spark:
  enabled: false # 默认关闭；设为 true 时优先尝试 Spark，失败后回退到 SQL
```

### 数据分析任务

**支持的统计类型**：

- `USER_POST_COUNT`: 用户发文数量统计
- `POST_VIEW_COUNT`: 文章浏览量统计
- `COMMENT_COUNT`: 评论数量统计

**触发分析**：

```bash
# 1. 设置接口地址和演示账号
BASE_URL=${BASE_URL:-http://localhost:8082}
DEMO_USERNAME=${DEMO_USERNAME:-your_demo_user}
DEMO_PASSWORD=${DEMO_PASSWORD:-your_demo_password}

# 2. 登录获取 Token
TOKEN=$(curl -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"${DEMO_USERNAME}\",\"password\":\"${DEMO_PASSWORD}\"}" \
  | jq -r '.data.token')

# 3. 触发 Spark 分析
curl -X POST "$BASE_URL/api/stats/analyze" \
  -H "Authorization: Bearer $TOKEN"

# 4. 查看统计结果
curl "$BASE_URL/api/stats" \
  -H "Authorization: Bearer $TOKEN" | jq
```

**Spark 执行流程**：

1. 从数据库日志表读取 `access_logs` 原始数据
2. 使用 Spark SQL 进行聚合计算
3. 将统计结果写入 `statistics` 表
4. 前端通过 API 查询统计数据并可视化展示

### Spark vs SQL 分析对比

| 特性     | Spark 分析            | SQL 分析       |
| -------- | --------------------- | -------------- |
| 适用场景 | 大数据量 (百万级+)    | 中小数据量     |
| 性能     | 分布式并行计算        | 单机数据库查询 |
| 资源消耗 | 需要额外内存 (1G+)    | 仅数据库资源   |
| 复杂度   | 较高                  | 较低           |
| 默认配置 | 禁用 (Java 17 兼容性) | 启用           |

**注意**：默认使用 SQL 分析以保证兼容性，Spark 分析需手动启用。

## 实验验证

### 验证 openGauss 集群

**重要说明**：当前配置使用三个独立的 openGauss 实例。应用连接到 `opengauss-primary` 作为主数据库。

#### 快速验证（推荐）

在虚拟机上执行验证脚本：

```bash
ssh $VM_USER@$VM_IP
cd ~/CloudCom
chmod +x scripts/verify-opengauss.sh
./scripts/verify-opengauss.sh
```

#### 手动验证步骤

**所有命令需要在虚拟机上执行，或通过 SSH 远程执行**

##### 1. 验证主库连接

```bash
# 在虚拟机上执行
docker exec opengauss-primary bash -c 'su - omm -c "gsql -d blog_db -c \"SELECT version();\""'

# 或从本地 Mac 通过 SSH 执行
ssh $VM_USER@$VM_IP "docker exec opengauss-primary bash -c 'su - omm -c \"gsql -d blog_db -c \\\"SELECT version();\\\"\""
```

##### 2. 检查主库复制状态

```bash
# 在虚拟机上执行
docker exec opengauss-primary bash -c 'su - omm -c "gsql -d blog_db -c \"SELECT application_name, state, sync_state FROM pg_stat_replication;\""'

```

##### 3. 检查数据库表和数据

```bash
# 查看表结构
docker exec opengauss-primary bash -c 'su - omm -c "gsql -d blog_db -c \"\\dt\""'

# 查询用户数量
docker exec opengauss-primary bash -c 'su - omm -c "gsql -d blog_db -c \"SELECT COUNT(*) FROM users;\""'

# 查询文章数量
docker exec opengauss-primary bash -c 'su - omm -c "gsql -d blog_db -c \"SELECT COUNT(*) FROM posts;\""'
```

#### 4. 验证读写分离

查看后端日志，确认读写操作路由到正确的数据源：

```bash
# 虚拟机环境
tail -f ~/CloudCom/apps/backend/logs/backend.log | grep "HikariCP"

# Docker 本地环境
docker-compose logs -f backend | grep "HikariCP"
```

### 验证 Spark 分析

#### 1. 执行测试分析任务

```bash
# 1. 设置接口地址和演示账号
BASE_URL=${BASE_URL:-http://localhost:8082}
DEMO_USERNAME=${DEMO_USERNAME:-your_demo_user}
DEMO_PASSWORD=${DEMO_PASSWORD:-your_demo_password}

# 2. 登录系统
curl -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"${DEMO_USERNAME}\",\"password\":\"${DEMO_PASSWORD}\"}"

# 3. 创建测试文章
curl -X POST "$BASE_URL/api/posts" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Post","content":"Test content for Spark analysis"}'

# 4. 触发 Spark 分析
curl -X POST "$BASE_URL/api/stats/analyze" \
  -H "Authorization: Bearer YOUR_TOKEN"

# 5. 查看 Spark 执行日志
# 虚拟机环境
tail -f ~/CloudCom/apps/backend/logs/backend.log | grep "Spark"

# Docker 本地环境
docker-compose logs -f backend | grep "Spark"
```

#### 2. 验证统计结果

```bash
# 查询所有统计数据
curl http://localhost:8082/api/stats \
  -H "Authorization: Bearer YOUR_TOKEN" | jq

# 查询特定类型统计
curl http://localhost:8082/api/stats/USER_POST_COUNT \
  -H "Authorization: Bearer YOUR_TOKEN" | jq
```

### 性能测试

#### 1. 数据库连接池测试

```bash
# 查看连接池状态
# 虚拟机环境
tail -f ~/CloudCom/apps/backend/logs/backend.log | grep "HikariPool"

# Docker 本地环境
docker-compose logs -f backend | grep "HikariPool"
```

#### 2. 并发请求测试

```bash
# 使用 Apache Bench 测试
ab -n 1000 -c 10 http://localhost:8082/api/posts/list

# 或使用 wrk
wrk -t4 -c100 -d30s http://localhost:8082/api/posts/list
```

#### 3. 复制延迟测试

```bash
# 在主库插入数据并记录时间
docker exec -it gaussdb-primary gsql -U bloguser -d blog_db \
  -c "INSERT INTO access_logs (user_id, action) VALUES (1, 'TEST'); SELECT NOW();"

# 立即在备库查询
docker exec -it gaussdb-standby1 gsql -U bloguser -d blog_db \
  -c "SELECT * FROM access_logs WHERE action='TEST'; SELECT NOW();"
```

---

## API 测试

### 自动化测试脚本

系统提供完整的 API 自动化测试脚本：

```bash
./test-vm-api.sh
```

### 测试覆盖

本项目提供 18 个 API 自动化测试用例，当前测试结果如下：

| #   | 测试项               | 状态   |
| --- | -------------------- | ------ |
| 1   | 健康检查 API         | PASSED |
| 2   | 前端页面可访问性     | PASSED |
| 3   | 用户注册 API         | PASSED |
| 4   | 用户登录 API         | PASSED |
| 5   | 获取当前用户信息 API | PASSED |
| 6   | 发布动态 API         | PASSED |
| 7   | 获取动态列表 API     | PASSED |
| 8   | 获取动态详情 API     | PASSED |
| 9   | 点赞动态 API         | PASSED |
| 10  | 发布评论 API         | PASSED |
| 11  | 获取评论列表 API     | PASSED |
| 12  | 获取我的动态 API     | PASSED |
| 13  | 获取统计数据 API     | PASSED |
| 14  | 图片上传 API         | PASSED |
| 15  | 取消点赞 API         | PASSED |
| 16  | 删除评论 API         | PASSED |
| 17  | 删除动态 API         | PASSED |
| 18  | 数据库连接测试       | PASSED |

### 测试示例输出

```text
测试目标: http://<VM_IP>:8082
总测试数: 18
通过: 18
失败: 0
通过率: 100.0%
所有测试通过，系统运行正常。
```

### 手动测试

#### 1. 用户注册

```bash
BASE_URL=${BASE_URL:-http://localhost:8082}

curl -X POST "$BASE_URL/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "Test@123",
    "email": "test@example.com"
  }'
```

#### 2. 用户登录

```bash
DEMO_USERNAME=${DEMO_USERNAME:-your_demo_user}
DEMO_PASSWORD=${DEMO_PASSWORD:-your_demo_password}

TOKEN=$(curl -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"${DEMO_USERNAME}\",\"password\":\"${DEMO_PASSWORD}\"}" \
  | jq -r '.data.token')
```

#### 3. 发布动态

```bash
curl -X POST "$BASE_URL/api/posts" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "这是一条测试动态",
    "visibility": "public"
  }'
```

#### 4. 获取动态列表

```bash
curl "$BASE_URL/api/posts/list" \
  -H "Authorization: Bearer $TOKEN"
```

#### 5. 触发数据分析

```bash
curl -X POST "$BASE_URL/api/stats/analyze" \
  -H "Authorization: Bearer $TOKEN"
```

---

## 架构设计

### 系统架构图

```
┌─────────────────────────────────────────────────────────────┐
│                         用户浏览器                           │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    前端 (Vue 3 + Nginx)                      │
│  • 端口: 8080                                                │
│  • 反向代理到后端                                            │
│  • 上传限制: 50MB                                            │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP/REST API
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                后端 (Spring Boot 3)                          │
│  • 端口: 8082                                                │
│  • JWT 认证                                                  │
│  • 读写分离路由                                              │
│  • Spark 数据分析                                            │
└────────────────────┬────────────────────────────────────────┘
                     │ JDBC
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              openGauss 三实例集群                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  主库 (5432) │──│ 备库1 (5434) │  │ 备库2 (5436) │      │
│  │    写操作    │  │    读操作    │  │    读操作    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         │               ▲                  ▲                 │
│         └───────流复制───┴──────────────────┘                │
└─────────────────────────────────────────────────────────────┘
```

### 技术选型理由

| 技术              | 选择理由                  |
| ----------------- | ------------------------- |
| **Spring Boot 3** | 最新企业级框架，生态完善  |
| **Vue 3**         | 组合式 API，性能优异      |
| **openGauss**     | 华为自研，兼容 PostgreSQL |
| **Docker**        | 容器化部署，环境一致性    |
| **MyBatis**       | 灵活的 SQL 映射           |
| **JWT**           | 无状态认证，适合分布式    |
| **Apache Spark**  | 大数据分析能力            |

## 常见问题

### 虚拟机服务相关

<details>
<summary><b>Q: 虚拟机服务无法启动？</b></summary>

**检查步骤**：

```bash
# 1. 查看服务状态
./status.sh vm

# 2. SSH 连接虚拟机查看日志
ssh $VM_USER@$VM_IP
cd /root/CloudCom
docker-compose ps
docker logs blogcircle-backend
docker logs blogcircle-frontend

# 3. 重启服务
./stop-vm.sh
./start-vm.sh
```

</details>

<details>
<summary><b>Q: 前端显示 502 错误？</b></summary>

**原因**: 前端无法连接后端  
**解决**: 确认后端服务运行正常，容器网络连接正常

```bash
ssh $VM_USER@$VM_IP
docker exec blogcircle-frontend wget -O- http://blogcircle-backend:8080/actuator/health
```

</details>

<details>
<summary><b>Q: 图片上传失败 413 错误？</b></summary>

**原因**: 文件超过 50MB 限制  
**解决**: 压缩图片或修改 `apps/frontend/nginx.conf` 中的 `client_max_body_size`

</details>

<details>
<summary><b>Q: 数据库连接失败？</b></summary>

**检查步骤**：

```bash
ssh $VM_USER@$VM_IP
docker exec opengauss-primary su - omm -c \
  "/usr/local/opengauss/bin/gsql -d blog_db -c 'SELECT 1;'"
```

</details>

### 本地开发相关

<details>
<summary><b>Q: Maven 构建失败？</b></summary>

确保：

- JDK 版本 = 17
- Maven 版本 >= 3.6
- 网络连接正常（需下载依赖）
</details>

<details>
<summary><b>Q: 前端启动失败？</b></summary>

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

</details>

### 更多帮助

遇到问题？

1. 查看日志文件
2. 运行测试脚本 `./test-vm-api.sh`
3. 查看健康检查 `http://<VM_IP>:8082/actuator/health`

---

## 📚 项目结构

```
CloudCom/
├── apps/backend/                 # Spring Boot 后端
│   ├── src/main/java/
│   │   └── com/cloudcom/blog/
│   │       ├── controller/       # API 控制器
│   │       ├── service/          # 业务逻辑
│   │       ├── mapper/           # MyBatis 映射
│   │       ├── entity/           # 实体类
│   │       └── config/           # 配置类
│   ├── src/main/resources/
│   │   ├── application.yml       # 配置文件
│   │   ├── db/01_init.sql       # 数据库初始化
│   │   └── mapper/*.xml          # SQL 映射
│   └── pom.xml
│
├── apps/frontend/                # Vue 3 前端
│   ├── src/
│   │   ├── views/                # 页面组件
│   │   ├── components/           # 公共组件
│   │   ├── api/                  # API 封装
│   │   ├── stores/               # 状态管理
│   │   └── router/               # 路由配置
│   ├── nginx.conf                # Nginx 配置
│   └── package.json
│
├── docker-compose.yml                                # 本地开发配置
├── docker-compose-opengauss.yml                     # openGauss 实验环境配置
│
├── start-vm.sh                   # 虚拟机一键部署
├── stop-vm.sh                    # 虚拟机停止服务
├── status.sh                     # 服务状态检查
├── test-vm-api.sh               # API 自动化测试
│
└── README.md                     # 本文档
```

---

## 🎓 学习资源

### 官方文档

- [Spring Boot 文档](https://spring.io/projects/spring-boot)
- [Vue 3 文档](https://cn.vuejs.org/)
- [openGauss 文档](https://docs.opengauss.org/)
- [Docker 文档](https://docs.docker.com/)
- [MyBatis 文档](https://mybatis.org/mybatis-3/)

### 相关技术

- Element Plus UI: https://element-plus.org/
- Pinia 状态管理: https://pinia.vuejs.org/
- Apache Spark: https://spark.apache.org/

---
