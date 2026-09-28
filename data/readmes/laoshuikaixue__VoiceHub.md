# VoiceHub - 校园广播站点歌系统

这是一个使用Nuxt 4全栈框架开发的现代化校园广播站点歌管理系统。系统提供完整的点歌、投票、排期管理、通知推送、数据分析、权限控制和数据库管理功能，支持多角色权限管理和灵活的系统配置。

<div align="center">

[交流群](https://qm.qq.com/cgi-bin/qm/qr?k=5DV4vGlqn82YaNi7a3xW4zjmS8ZUr6cz&jump_from=webapi&authKey=axAl02PMsIVVAwrXij0YUUrOrUTeLpqLipu5XcTvyBUOzeWaOnicBB+fmBwNJs5S) | [使用学校收集表](https://laoshuikaixue.feishu.cn/share/base/form/shrcniUKakpNYP6KH7qrU20qq5e) | [项目宣传片](https://www.bilibili.com/video/BV1B9ArzMEkA) | [赞助支持](#sponsor)

</div>

## 项目截图

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/fef6970e-95eb-4cab-a11f-db4e71fc87b5" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/f76e912c-1263-424b-b379-72321de205f7" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/b5de5880-6635-4698-9fd9-dbea9642f06a" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/05472008-57d5-4586-b7ca-572bff8a30ae" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/c30f2e5a-4cc8-48cb-aca2-4d41daeaaaf8" />

## 主要功能

### 🎵 核心功能

- **智能点歌系统**：用户可以点歌或给已有歌曲投票，支持网易云音乐、QQ音乐和哔哩哔哩搜索，可选择期望播出时段
- **多平台登录支持**：
  - **OAuth 账户系统**：支持通过 GitHub、Casdoor 等 OAuth 提供商快速创建和登录账户
    - **直接创建账户**：用户通过 OAuth 认证后可创建新账户，但仍需设置本地用户名和密码
    - **账户绑定**：已有账户的用户可将 OAuth 身份绑定到现有账户，实现多平台统一登录
    - **WebAuthn 支持**：支持 HarmonyOS Passkey、Windows Hello、生物识别和硬件安全密钥（如 YubiKey）登录
    - **双因素认证（2FA）**：支持 TOTP 和邮箱验证，增强账户安全性
  - **网易云音乐登录**：支持扫码登录，登录后可搜索个人歌单、收藏及播客电台内容
    - **一键添加到歌单**：登录后支持将排期中的网易云音乐歌曲一键添加到个人歌单
    - **从歌单投稿**：支持从个人歌单中直接投稿歌曲到系统
    - **从最近播放投稿**：支持从最近播放记录中投稿歌曲
    - **播客电台投稿**：支持搜索和投稿播客电台内容
- **投稿限额管理**：灵活配置用户投稿限制，支持按时间段、用户角色设置不同的投稿额度，有效控制系统负载
- **歌曲去重功能**：智能识别重复歌曲，优化歌曲库管理，避免重复播放
- **歌曲管理**：按热度排序，避免重复播放，动态URL防止链接过期，支持黑名单管理
- **音乐播放器**：内置音乐播放器，支持进度控制和音质实时切换
- **音质切换**：支持多种音质选择（标准、HQ、无损、Hi-Res等），动态获取最新播放链接
- **音乐下载功能**：支持管理员下载歌曲到本地，提供多种音质选择和批量下载
- **歌曲重播功能**：支持用户对已播放过的歌曲发起重播申请，支持查看申请记录和撤回申请

### 👥 用户管理

- **用户管理**：管理员添加用户，支持按年级班级分类
- **账户创建方式**：
  - 管理员直接添加账户
  - 用户通过 OAuth 快速创建账户
  - 用户通过传统用户名/密码注册
- **权限控制**：多级权限管理，支持普通用户、管理员、超级管理员
- **账户安全**：
  - bcrypt 密码加密
  - 双因素认证（TOTP、邮箱验证）
  - WebAuthn 支持（HarmonyOS Passkey、生物识别、硬件密钥）
  - 账户锁定和风险控制
- **身份关联**：支持将多个 OAuth 身份绑定到同一账户，实现统一登录
- **黑名单管理**：支持歌曲和艺术家黑名单，自动过滤不当内容

### 📅 排期管理

- **排期管理**：管理员可以通过拖拽界面进行歌曲排期和顺序管理
- **排期草稿**：支持保存排期草稿功能，允许管理员分步完成排期安排
  - 草稿状态不影响公开展示，可随时修改和完善
  - 支持草稿发布为正式排期，确保排期质量
- **播出时段**：灵活配置播出时段，**支持多时段管理**
- **排期复制**：支持将某日期的排期完整复制到另一日期，原排期保留不变
- **打印排期**：支持自定义纸张大小、内容选择、编写备注和PDF导出的打印功能
- **学期管理**：管理员可设置当前学期，自动关联点歌记录
- **公开展示**：公开展示歌曲播放排期，按日期分组展示

### 🔔 通知系统

- **实时通知**：歌曲被选中、投票和系统通知
- **通知设置**：用户可自定义通知偏好，支持独立页面设置
- **批量通知**：管理员可向特定用户群体发送通知
- **社交账号绑定**：支持绑定MeoW等账号，同步推送通知到外部平台
- **验证码验证**：安全的验证码验证机制，支持动态样式反馈

### 💾 数据管理

- **数据库备份**：完整的数据库备份和恢复功能
- **数据库重置**：支持安全的数据库重置操作，可选择性保留用户数据或完全重置
- **文件导入导出**：支持备份文件的上传、下载和管理
- **数据库自检**：自动数据库验证和修复机制，确保系统稳定性

### 🎨 用户体验

- **现代UI**：响应式设计，深色主题，流畅的动画效果
- **玻璃态设计**：现代化的视觉效果和交互体验
- **交互反馈**：hover效果，点击反馈，状态变化动画
- **移动端优化**：适配支持移动设备访问，触摸友好的交互设计

## 技术栈

### 前端技术

- **Nuxt 4**：Vue.js全栈框架，提供SSR和SPA支持
- **Vue 3**：响应式前端框架，使用Composition API
- **TypeScript**：类型安全的JavaScript，提供完整的类型定义
- **UNO CSS**：实用优先的CSS框架，响应式设计
- **Vue Router**：前端路由管理

### 后端技术

- **Nuxt Server API**：服务端API路由，支持中间件和认证
- **Drizzle ORM**：现代化数据库ORM，提供类型安全的数据库操作和高性能查询
- **Neon Database**：Serverless PostgreSQL数据库，支持自动启停和无缝扩展
- **PostgreSQL**：关系型数据库，支持复杂查询和事务处理
- **Redis**：可选的分布式短期状态服务，仅用于验证码、限流和临时安全状态
- **JWT**：标准JWT认证机制，支持24小时token有效期
- **bcrypt**：密码加密，安全的哈希算法
- **Multer**：文件上传处理，支持多种存储方式

## 系统架构

系统采用了现代化的 Serverless 全栈架构：

- **前端**：使用 Nuxt 4 + Vue 3 组合式API构建响应式用户界面
- **后端**：使用 Nuxt Server API 构建 RESTful API 服务
- **数据库**：使用 Drizzle ORM + Neon Database，提供类型安全和高性能的数据库操作
- **认证**：标准 JWT 认证系统
- **数据读取**：PostgreSQL 是唯一业务数据源，歌曲、排期和用户状态不使用 Redis 缓存
- **部署**：支持 Vercel、Netlify、EdgeOne 等 Serverless 平台一键部署，并提供 Docker、Linux 一键脚本及飞牛 FnOS (fpk安装包) 等多种部署方式

## 部署指南

### 一键部署

本项目可以一键部

[...截断...]

署到Vercel/Netlify/EdgeOne平台：

[![Deploy to Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Flaoshuikaixue%2FVoiceHub&env=DATABASE_URL,JWT_SECRET,NODE_ENV&envDefaults=%7B%22NODE_ENV%22%3A%22production%22%7D&envDescription=%E7%8E%AF%E5%A2%83%E5%8F%98%E9%87%8F%E8%AF%B4%E6%98%8E&envLink=https%3A%2F%2Fgithub.com%2Flaoshuikaixue%2FVoiceHub%23%E7%8E%AF%E5%A2%83%E5%8F%98%E9%87%8F%E8%AF%B4%E6%98%8E)
[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://github.com/laoshuikaixue/VoiceHub)
[![Deploy to EdgeOne Pages](https://cdnstatic.tencentcs.com/edgeone/pages/deploy.svg)](https://edgeone.ai/pages/new?repository-url=https://github.com/laoshuikaixue/VoiceHub&env=DATABASE_URL,JWT_SECRET&env-description=%E9%9C%80%E8%A6%81%E9%85%8D%E7%BD%AE%E6%95%B0%E6%8D%AE%E5%BA%93%E5%9C%B0%E5%9D%80%E3%80%81JWT%E5%AF%86%E9%92%A5)

在部署过程中，需要输入必要的环境变量：

1. `DATABASE_URL`：PostgreSQL数据库连接地址
2. `JWT_SECRET`：JWT令牌签名密钥

### Linux 服务器部署

本项目提供了针对 Ubuntu/Debian 服务器的一键部署脚本，支持自动安装 Node.js 22、配置环境变量、安装依赖和构建项目。

**一键命令：**

```bash
bash <(curl -sL https://raw.githubusercontent.com/laoshuikaixue/VoiceHub/main/sh/main.sh)
```

如果你需要 gh-proxy 加速，使用以下命令：

```bash
bash <(curl -sL https://gh-proxy.com/https://raw.githubusercontent.com/laoshuikaixue/VoiceHub/main/sh/main.sh)
```

### Docker 部署

VoiceHub 支持通过 Docker 进行容器化部署，提供了多种部署方式。

#### 方式一：使用 Docker Compose（推荐）

这是最简单的部署方式，会自动创建应用和数据库容器。

##### 使用预构建镜像

查看 [docker-compose](/docker-compose) 并选择适合的配置文件

##### 本地构建镜像

1. 克隆项目

```bash
git clone https://github.com/laoshuikaixue/VoiceHub.git
cd VoiceHub
```

2. 修改 docker-compose.yml 中的环境变量

```yaml
environment:
  - DATABASE_URL=postgresql://user:password@postgres:5432/voicehub # 可能需要 ?sslmode=disable
  - JWT_SECRET=your-jwt-secret-here # 请修改为强随机字符串
  - NODE_ENV=production
```

3. 启动服务

```bash
docker-compose up -d
```

4. 访问应用
   打开浏览器访问 http://localhost:3000

默认管理员账号：

- 用户名：admin
- 密码：admin123

#### 方式二：使用预构建镜像

如果你已有 PostgreSQL 数据库，可以直接使用预构建的镜像。

使用 GitHub 镜像源：

```bash
docker run -d \
  -p 3000:3000 \
  -e DATABASE_URL="postgresql://username:password@host:port/database?sslmode=require" \
  # 可能需要替换成 ?sslmode=disable
  -e JWT_SECRET="your-very-secure-jwt-secret-key" \
  -e NODE_ENV=production \
  --name voicehub \
  ghcr.io/laoshuikaixue/voicehub:latest
```

使用南京大学镜像源：

```bash
docker run -d \
  -p 3000:3000 \
  -e DATABASE_URL="postgresql://username:password@host:port/database?sslmode=require" \
  # 可能需要替换成 ?sslmode=disable
  -e JWT_SECRET="your-very-secure-jwt-secret-key" \
  -e NODE_ENV=production \
  --name voicehub \
  ghcr.nju.edu.cn/laoshuikaixue/voicehub:latest
```

#### 方式三：本地构建镜像

如果需要自定义构建，可以本地构建镜像。

```bash
git clone https://github.com/laoshuikaixue/VoiceHub.git
cd VoiceHub

# 构建镜像（不使用缓存，确保完全重新构建）
docker build --no-cache -t voicehub .

# 运行容器
docker run -d \
  -p 3000:3000 \
  -e DATABASE_URL="postgresql://username:password@host:port/database?sslmode=require" \
  # 可能需要替换成 ?sslmode=disable
  -e JWT_SECRET="your-very-secure-jwt-secret-key" \
  -e NODE_ENV=production \
  --name voicehub \
  voicehub
```

### Podman 部署

Podman 是一个与 Docker 兼容的容器引擎，无需守护进程，支持 rootless 模式（无需 root 权限）。VoiceHub 的 Docker 配置文件可以直接用于 Podman。

#### 使用 Podman Compose 部署

```bash
podman compose -f docker-compose.yml up -d
```

> **说明**：`podman compose` 完全兼容 `docker-compose.yml` 文件，无需修改配置。

#### rootless 模式

Podman 默认以当前用户身份运行，无需 `sudo`，安全性更高。但容易遇到文件权限问题（特别是挂载卷时）。

### 飞牛 (FnOS) 部署

VoiceHub 现已支持飞牛 OS (FnOS) 的 `.fpk` 安装包。

- 从 [GitHub Actions](https://github.com/laoshuikaixue/VoiceHub/actions/workflows/build-fpk.yml) 获取最新版本

### Nix / NixOS

VoiceHub 提供了一个 Nix flake，用于构建、开发和在 NixOS 上部署。

#### 前提条件

- [Nix](https://nixos.org/download)（带 flake 支持）
- PostgreSQL 数据库

#### NixOS 部署

将 VoiceHub 添加为 flake input：

```nix
{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    voicehub.url = "github:laoshuikaixue/VoiceHub";
  };

  outputs = { self, nixpkgs