# PMS 前端

[![CI](https://github.com/xiebinJava/pms-front/actions/workflows/ci.yml/badge.svg)](https://github.com/xiebinJava/pms-front/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

PMS Front 是 PMS 的浏览器端应用，负责页面展示、交互和前端路由；账号、权限、组织关系、项目数据和文件上传都由 [`pms-backend`](https://github.com/xiebinJava/pms-backend) 提供。项目面向单个企业本地部署，不是独立 SaaS 前端。

当前统一发行包镜像版本：`1.0.7`。最终用户请使用 [`pms-distribution`](https://github.com/xiebinJava/pms-distribution) 的预构建镜像；本仓库面向前端本地开发。

第一次使用时，先启动后端，再按下面的「本地开发」运行前端。只想快速体验完整系统时，使用发行仓库的 `./scripts/bootstrap.sh`。

## 本地开发

### 1. 准备后端

在兄弟仓库 `pms-backend` 中完成 MySQL 配置并启动 API。后端默认地址：

```text
http://localhost:8080/api
```

推荐方式：

```bash
cd ../pms-backend
docker compose -f docker-compose.example.yml up -d --build
```

确认后端就绪：

```bash
curl http://127.0.0.1:8080/api/health/ready
```

### 2. 安装前端依赖

```bash
cd ../pms-front
corepack enable
pnpm install
```

项目已锁定 `pnpm@9.15.9`，请不要用 npm 或 pnpm 11 生成新的 lockfile。

### 3. 启动开发服务器

```bash
pnpm dev
```

打开 <http://localhost:5173>。开发服务器会把浏览器的 `/api` 请求代理到 `VITE_PROXY_TARGET`（默认 `http://localhost:8080`），因此浏览器不需要直接配置跨域。

本地 / 发行包默认初始管理员：`admin@example.com` / `PmsAdmin123!`（由后端 `PMS_BOOTSTRAP_*` 注入；空库首次启动创建，登录后请立刻改密）。登录使用邮箱，不区分大小写；姓名缺失时页面回退展示邮箱。

## 推荐启动方式：发行仓库

```bash
git clone https://github.com/xiebinJava/pms-distribution.git
cd pms-distribution
./scripts/bootstrap.sh
```

访问 <http://localhost:5173>，使用 `admin@example.com` / `PmsAdmin123!` 登录。发行 Compose 使用固定版本的前端和后端镜像，不需要在本仓库重复维护部署文件。

从源码联调时，仍可用后端仓库的 `docker-compose.example.yml` 本地构建。生产部署、升级和备份请看 [`pms-distribution`](https://github.com/xiebinJava/pms-distribution) 与后端的 [发布验收清单](https://github.com/xiebinJava/pms-backend/blob/main/docs/operations/release-checklist.md)。

## 页面和业务模块

| 导航 | 主要用途 |
| --- | --- |
| 工作台 | 查看分配给我的任务、参与项目和最近动态 |
| 研发管理 / 项目管理 | 项目列表、搜索、状态、进度和项目经理 |
| 项目详情 | 流程节点、节点负责人 / 排期、任务看板、里程碑、成员和动态 |
| 配置管理 / 人员与权限 | 员工邮箱身份、主归属、兼职归属、角色和账号状态 |
| 配置管理 / 组织架构 | 可缩放拖拽的组织画布、负责人、层级和变更历史 |
| 配置管理 / 角色管理 | 角色编码、中文名称、权限点和数据范围 |
| 配置管理 / 批量导入 | Excel/CSV 预览、错误校验、幂等提交、错误报告下载 |
| 配置管理 / 审计日志 | 按动作、资源、操作人和时间查询敏感操作 |
| 通知中心 | 查看站内通知，按未读 / 临期 / 逾期筛选并分页处理 |
| 使用手册 | 按当前导航结构查找模块说明、截图和操作步骤 |

业务规则以 [后端业务规范](https://github.com/xiebinJava/pms-backend/blob/main/docs/business-specification.md) 为准。特别注意：组织负责人和员工主归属是两套独立关系。

## 前端工作方式

```text
用户访问页面
  ↓
vue-router 登录守卫
  ↓
Pinia 保存用户和语言状态
  ↓
axios 请求 /api
  ↓
后端返回统一响应（成功 / 业务错误 / 401）
```

- 首次访问受保护页面会跳转 `/login?redirect=...`。
- Axios 只在 HTTP 401 时尝试刷新会话；刷新失败会清理本地会话并回到登录页。
- 前端不自行判断角色能否访问数据，按钮显隐只是体验层；最终权限由后端 RBAC 和数据范围校验决定。
- 中文是默认语言，右上角可切换英文；语言写入浏览器 `localStorage` 的 `pms.locale`。
- 页面统一使用 PMS 设计令牌（`--pms-*`），不要在单页随意复制颜色和间距。

## 环境变量

开发环境配置在 `.env.development`，通常不需要修改：

| 变量 | 说明 | 默认值 |
| --- | --- | --- |
| `VITE_PORT` | Vite 开发服务器端口 | `5173` |
| `VITE_PROXY_TARGET` | `/api` 代理目标 | `http://localhost:8080` |

例如后端使用其他端口：

```bash
VITE_PROXY_TARGET=http://127.0.0.1:18080 pnpm dev
```

不要把 JWT、数据库密码、SMTP 密码或对象存储密钥写进 `VITE_*` 变量。Vite 会把 `VITE_*` 值打进浏览器产物，前端变量不是秘密存储。

## 开发命令

```bash
pnpm test       # Node 测试（组件契约和关键交互）
pnpm typecheck  # vue-tsc 类型检查
pnpm build      # 生产构建到 dist/
pnpm preview    # 预览生产构建
./scripts/check-privacy.sh
```

提交前至少执行：

```bash
pnpm test && pnpm typecheck && pnpm build
```

浏览器端到端验收由后端仓库的集成工作流统一编排，覆盖登录、项目主流程、桌面端和窄屏布局。出现页面 500 时先查看后端日志和 `/api/health/ready`，不要只在前端重试。

## 目录速览

```text
src/
├── api/          后端接口封装（auth / project / task / admin…）
├── auth/         登录、OIDC/LDAP 回调
├── components/   可复用页面组件和空状态
├── enums/        状态、优先级、角色等枚举
├── i18n/         vue-i18n 初始化
├── layout/       侧边栏、顶栏、搜索和通知
├── locales/      zh-CN / en-US 文案
├── plugins/      axios、token 刷新和错误处理
├── router/       路由和登录守卫
├── store/        用户、语言等 Pinia 状态
├── styles/       全局样式和 PMS 设计令牌
├── types/        API 与领域类型
├── utils/        日期、展示等工具
└── views/        登录、工作台、项目、管理后台、使用手册
```

新增页面时建议按以下顺序：

1. 在 `src/api` 定义接口和类型；
2. 在 `src/locales/zh-CN.ts`、`src/locales/en-US.ts` 同步文案；
3. 在 `src/views` 实现页面，优先复用现有组件和 `--pms-*` 令牌；
4. 在 `src/router` 添加路由和权限元数据；
5. 补充测试、类型检查和窄屏验证。

## Docker 镜像

单独构建前端镜像（要求当前目录存在构建产物所需文件）：

```bash
docker build -t pms-front:local .
docker run --rm -p 5173:8080 pms-front:local
```

镜像使用非 root Nginx，默认只提供静态页面和 `/api` 代理。正式环境应把 HTTPS、域名、CORS 和安全响应头交给企业反向代理或 Ingress；不要把后端管理端口 8081 暴露到公网。

## 常见问题

| 现象 | 处理 |
| --- | --- |
| 页面提示 `Request failed with status code 500` | 查看后端日志；先确认 MySQL 迁移已到当前基线，再访问 `/api/health/ready` |
| 一直跳回登录页 | 检查后端登录接口、JWT 密钥和浏览器时间；刷新令牌失败会主动清理会话 |
| `localhost` 能访问、`127.0.0.1` 异常 | 开发环境优先使用 <http://localhost:5173>，并检查 `VITE_PROXY_TARGET` |
| 页面能打开但 API 404 | 确认访问的是前端开发端口 5173，且 Vite 代理目标为后端 8080 |
| 中文 / 英文缺文案 | 同时补充 `src/locales/zh-CN.ts` 和 `src/locales/en-US.ts`，不要在模板硬编码 |
| 生产构建后页面空白 | 检查浏览器控制台、Nginx 回退页和反向代理的 `/api` 路径 |

## 相关文档

- [后端 README：架构、MySQL 和部署](https://github.com/xiebinJava/pms-backend)
- [使用手册](docs/user-manual.md)
- [前端设计规范](docs/frontend-design-system.md)
- [设计逻辑](docs/design-logic.md)
- [贡献指南](CONTRIBUTING.md)
- [安全策略](SECURITY.md)

## 许可证

Apache-2.0。贡献前请阅读 [贡献指南](CONTRIBUTING.md)。
