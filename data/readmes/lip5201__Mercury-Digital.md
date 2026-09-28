# Mercury Digital - 数字商品交易平台

Mercury Digital 是一个基于 Go 语言构建的高性能数字商品交易平台后端服务，支持文件下载、卡密销售、Wiki 订阅等多态商品类型，内置强大的插件系统和完善的用户权限管理。

## ✨ 核心特性

- 🏗️ **分层架构**: kernel（基础设施）→ modules（业务）→ pkg（通用）的清晰架构
- 🔐 **JWT 双令牌认证**: Access Token + Refresh Token，支持角色权限控制（customer/owner）
- 💰 **多态商品系统**: 支持 file（文件）、card（卡密）、wiki（订阅）三种商品类型
- 🎯 **VIP 分档定价**: Silver/Gold/Plat 三级 VIP 享受不同折扣
- 🔌 **插件扩展机制**: 基于 hashicorp/go-plugin 和 gRPC 的独立进程插件系统
- 📦 **存储抽象层**: 支持本地存储和云存储插件扩展
- ⚡ **高性能**: Gin Web 框架 + PostgreSQL + Redis 缓存
- 🛡️ **生产级特性**: 链路追踪、限流、CORS、Gzip、审计日志、优雅关闭

## 📋 技术栈

| 类别 | 技术 |
|------|------|
| **语言** | Go 1.23.2 |
| **Web 框架** | Gin v1.10.1 |
| **ORM** | GORM v1.25.12 |
| **数据库** | PostgreSQL 16 |
| **缓存** | Redis 7 |
| **认证** | JWT (HS256) |
| **配置管理** | Viper v1.19.0 |
| **日志** | Logrus v1.9.4 |
| **插件系统** | hashicorp/go-plugin + gRPC + Protobuf |

## 🚀 快速开始

### 前置要求

- Go 1.21+
- Node.js 18+
- PostgreSQL 14+
- Redis 6+

### 方式一：Docker Compose（推荐）

一键启动所有服务（PostgreSQL + Redis + Mercury Digital API）：

```bash
# 克隆仓库
git clone <repository-url>
cd Mercury

# 启动所有服务
make docker-up

# 查看服务状态
make docker-ps

# 查看日志
make docker-logs
```

### 方式二：本地运行

详细安装指南请参考 [INSTALL.md](docs/INSTALL.md)。

#### 1. 配置数据库

编辑 `config.yaml`：

```yaml
server:
  port: 8080

database:
  dsn: "postgresql://user:password@localhost:5432/mercury?sslmode=disable"
  auto_migrate: true

redis:
  addr: "localhost:6379"
  password: ""
  db: 0

jwt:
  secret_key: "your-256-bit-secret-key-here"
  access_expire: 1h
  refresh_expire: 168h
```

#### 2. 启动后端

```bash
go build -o mercury.exe .
./mercury.exe
```

后端启动后会自动检测系统安装状态，首次运行会生成临时安装令牌。

#### 3. 启动前端

```bash
cd web
npm install
npm run dev
```

#### 4. 完成安装

打开浏览器访问 `http://localhost:3000`，按向导完成系统安装。

#### 5. 验证安装

```bash
# 后端健康检查
curl http://localhost:8080/health

# 前端
curl http://localhost:3000
```

## 📁 项目结构

```
Mercury/
├── cmd/                    # CLI 工具入口
│   ├── main.go            # 后端主入口
│   └── setup/             # 安装 CLI
├── internal/               # 应用启动装配层
│   └── app/               # 统一启动入口
├── kernel/                # 基础设施层
│   ├── auth/              # JWT 认证与中间件
│   ├── config/             # 配置管理
│   ├── db/                 # PostgreSQL 连接
│   ├── redis/              # Redis 客户端
│   ├── eventbus/           # 事件总线
│   ├── gateway/            # 插件网关
│   ├── middleware/         # HTTP 中间件
│   └── storage/            # 存储服务抽象
├── modules/                # 业务模块层
│   ├── user/               # 用户模块
│   ├── product/             # 商品模块
│   ├── order/               # 订单模块
│   └── setup/               # 安装模块
├── seed/                   # 种子数据
├── web/                    # 前端 (Next.js 16)
│   ├── app/               # 页面路由
│   ├── components/        # UI 组件
│   ├── core/              # 核心功能（含插件系统）
│   ├── lib/               # 工具库
│   ├── plugins/           # 前端插件
│   │   └── admin-setup/  # 安装向导插件
│   └── styles/            # 样式
├── docs/                   # 文档
│   ├── INSTALL.md         # 安装指南
│   └── PLUGIN_SYSTEM.md   # 插件系统文档
├── bin/                    # 编译输出目录
├── logs/                   # 日志目录
├── config.yaml             # 配置文件
├── Dockerfile              # Docker 构建文件
├── docker-compose.yml      # Docker Compose 编排
├── Makefile                # 常用命令封装
└── CODE_WIKI.md            # 详细代码文档
```

## 📖 API 文档

### 基础信息

- **Base URL**: `http://localhost:8080/api/v1`
- **认证方式**: JWT Bearer Token
- **响应格式**: JSON

### 主要端点

#### 认证模块（公开）

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/auth/register` | 用户注册 |
| POST | `/auth/login` | 用户登录 |
| POST | `/auth/token/refresh` | 刷新 Token |

#### 消费者端（需登录）

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/customer/me` | 获取个人资料 |
| PUT | `/customer/me` | 更新资料 |
| POST | `/customer/orders` | 创建订单 |
| GET | `/customer/products` | 浏览商品 |

#### 管理员端（仅 owner）

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/owner/users` | 用户列表 |
| POST | `/owner/products` | 发布商品 |
| POST | `/owner/users/:id/ban` | 封禁用户 |

完整 API 文档请参考 [CODE_WIKI.md](CODE_WIKI.md)。

## 🔧 配置说明

Mercury 支持通过环境变量或 `config.yaml` 文件进行配置：

| 配置项 | 环境变量 | 默认值 | 说明 |
|--------|----------|--------|------|
| 服务端口 | `SERVER_PORT` | 8080 | HTTP 服务端口 |
| 数据库 DSN | `DATABASE_DSN` | - | PostgreSQL 连接字符串 |
| Redis 地址 | `REDIS_ADDR` | localhost:6379 | Redis 服务器地址 |
| JWT 密钥 | `JWT_SECRET_KEY` | - | JWT 签名密钥 |
| 日志级别 | `LOGGING_LEVEL` | info | 日志级别（debug/info/warn/error） |

完整配置项请参考 [.env.example](.env.example)。

## 🔌 插件系统

Mercury 采用前后端双层插件架构：

### 前端插件

基于 TypeScript 的前端插件系统，支持：
- **页面路由注册**：插件可以注册独立的页面路由
- **全局组件**：支持弹窗、通知条等全局 UI
- **导航菜单**：插件可注册后台管理菜单项
- **内置插件**：admin-setup（安装向导）

详细文档请参考 [PLUGIN_SYSTEM.md](docs/PLUGIN_SYSTEM.md)。

### 后端插件

基于 hashicorp/go-plugin 和 gRPC 的独立进程插件系统：

- **Hook 拦截点**: 改价、额度校验、邀请码验证、自定义交付等
- **KV 沙箱隔离**: 每个插件拥有独立的存储空间
- **独立进程**: 插件以独立进程运行，故障不影响主服务
- **热插拔**: 支持动态加载和卸载插件

## 🧪 测试

```bash
# 运行所有测试
make test

# 生成覆盖率报告
make test-coverage

# 代码检查
make lint
```

## 📝 开发指南

### 添加新模块

1. 在 `modules/` 下创建新目录
2. 按照 `model → dto → service → handler` 四层架构编写代码
3. 在 `internal/app/app.go` 中注册模块路由

### 数据库迁移

启用自动迁移（开发环境）：

```yaml
database:
  auto_migrate: true
```

生产环境建议使用手动迁移脚本。

## 🚢 部署

### Docker 部署

```bash
# 构建镜像
docker build -t mercury:latest .

# 运行容器
docker run -d \
  --name mercury \
  -p 8080:8080 \
  --env-file .env \
  mercury:latest
```

### Kubernetes 部署

参考 `k8s/` 目录下的 manifests 文件（待添加）。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- [Gin](https://github.com/gin-gonic/gin) - Web 框架
- [GORM](https://github.com/go-gorm/gorm) - ORM 库
- [Redis](https://redis.io/) - 缓存系统
- [hashicorp/go-plugin](https://github.com/hashicorp/go-plugin) - 插件系统

## 📞 联系方式

- 项目主页: <repository-url>
- 问题反馈: <issues-url>
