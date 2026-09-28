<!-- markdownlint-disable MD033 -->
<h1 align="center">Cocoon</h1>

<p align="center">
  <em>本地优先的凭证管理器 — 一个主密码，管理你所有的账号、密钥和令牌</em>
</p>

<p align="center">
  <a href="./README_EN.md">English</a> | 简体中文
</p>

<p align="center">
  <a href="https://github.com/ilolicon/cocoon/releases"><img src="https://img.shields.io/github/v/release/ilolicon/cocoon?style=flat-square" alt="Release"></a>
  <a href="./LICENSE"><img src="https://img.shields.io/github/license/ilolicon/cocoon?style=flat-square" alt="License"></a>
  <img src="https://img.shields.io/badge/platform-macOS%20%7C%20Windows%20%7C%20Linux-blue?style=flat-square" alt="Platform">
</p>

---

Cocoon 是一款本地优先的凭证管理桌面应用，帮助你集中管理散落各处的账号密码、API Key、数据库连接、SSH 凭证和 Token。所有数据使用 AES-256-GCM 加密后仅保存在本地，零云端依赖。

## 界面预览

<p align="center">
  <img src="./screenshots/setup.png" width="48%" alt="初始化" />
  <img src="./screenshots/home_list.png" width="48%" alt="主页列表" />
</p>
<p align="center">
  <img src="./screenshots/home_card.png" width="48%" alt="主页卡片" />
  <img src="./screenshots/add_credential.png" width="48%" alt="添加凭证" />
</p>
<p align="center">
  <img src="./screenshots/tag_filter.png" width="48%" alt="标签筛选" />
  <img src="./screenshots/setting.png" width="48%" alt="设置界面" />
</p>

## 特性

- **本地优先** — 数据存储在 `~/.cocoon/cocoon.db`，不联网、不上传
- **强加密** — AES-256-GCM 加密 + Argon2id 密钥派生，主密码解锁
- **多凭证类型** — 账号密码、API Key、数据库、SSH、Token、自定义
- **标签系统** — 灵活标记和筛选，支持交集过滤
- **自动锁定** — 闲置超时自动锁屏，内存密钥安全擦除
- **快速复制** — 点击即复制，敏感字段按需解密
- **主题切换** — 深色/浅色/跟随系统，多种主题色可选

## 安全架构

```text
主密码 → Argon2id(salt, 64MB, 3次迭代) → 32字节主密钥
                                              │
                          ┌───────────────────┴───────────────────┐
                          ▼                                       ▼
                   AES-256-GCM 加密                      SHA-256 验证哈希
                   每条凭证独立 Nonce                     (仅用于密码校验)
```

- 凭证数据加密后写入 SQLite，解密仅在读取时发生
- 锁屏时主密钥从内存中安全擦除
- 修改主密码时，所有凭证在单一事务中重新加密

## 技术栈

| 层级 | 技术                                                                                   |
| ---- | -------------------------------------------------------------------------------------- |
| 框架 | [Wails v2](https://wails.io) (Go + WebView)                                            |
| 后端 | Go 1.23                                                                                |
| 前端 | Vue 3 + TypeScript                                                                     |
| UI   | [Naive UI](https://www.naiveui.com)                                                    |
| 存储 | SQLite ([mattn/go-sqlite3](https://github.com/mattn/go-sqlite3))                       |
| 加密 | AES-256-GCM + Argon2id ([golang.org/x/crypto](https://pkg.go.dev/golang.org/x/crypto)) |

## 快速开始

### 前置依赖

- [Go](https://go.dev/dl/) >= 1.21
- [Node.js](https://nodejs.org/) >= 16
- [Wails CLI](https://wails.io/docs/gettingstarted/installation) v2
- 平台构建工具：macOS 需要 Xcode，Linux 需要 `gcc` + `libgtk-3-dev` + `libwebkit2gtk-4.0-dev`

### 开发

```bash
# 克隆项目
git clone https://github.com/ilolicon/cocoon.git
cd cocoon

# 安装前端依赖
cd frontend && npm install && cd ..

# 启动开发模式（Go 后端 + Vite 前端热重载）
wails dev
```

### 构建

```bash
# 构建生产版本
wails build
```

构建产物位于 `build/bin/` 目录。

### 测试

```bash
go test ./internal/...
```

## 项目结构

```bash
cocoon/
├── app.go                  # Wails 绑定层，所有前端可调用的 API
├── main.go                 # 入口
├── internal/
│   ├── crypto/             # AES-256-GCM 加密 & Argon2id 密钥派生
│   ├── model/              # 数据结构
│   ├── service/            # 业务逻辑（认证、凭证管理）
│   └── store/              # SQLite 存储 & 迁移
└── frontend/
    └── src/
        ├── views/          # 页面（Setup / Lock / Home）
        ├── components/     # UI 组件
        ├── store/          # Pinia 状态管理
        └── composables/    # 组合式函数
```

## 路线图

- [x] 主密码保护 & AES-256-GCM 加密
- [x] 多凭证类型（密码、API Key、数据库、SSH、Token、自定义）
- [x] 标签系统 & 交集筛选
- [x] 收藏夹 & 搜索
- [x] 自动锁定
- [x] 深色/浅色主题
- [ ] 密码生成器
- [ ] 数据导入/导出
- [ ] 全局快捷键呼出
- [ ] 浏览器扩展

## 许可证

[MIT](./LICENSE)
