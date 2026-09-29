<h1 align="center">ConsoleX2API</h1>

<p align="center">
  <b>将 console.x.ai 封装为 OpenAI 兼容接口的轻量网关</b>
</p>

<p align="center">
  <a href="#功能特性">功能特性</a> ·
  <a href="#快速开始">快速开始</a> ·
  <a href="#配置说明">配置说明</a> ·
  <a href="#接口调用">接口调用</a> ·
  <a href="#docker-部署">Docker 部署</a> ·
  <a href="#常见问题">常见问题</a> ·
  <a href="./README_EN.md">English</a>
</p>

<p align="center">
  <img alt="Rust" src="https://img.shields.io/badge/Rust-Axum-000000?style=flat-square&logo=rust&logoColor=white">
  <img alt="OpenAI Compatible" src="https://img.shields.io/badge/OpenAI-Compatible-10A37F?style=flat-square&logo=openai&logoColor=white">
  <img alt="SQLite" src="https://img.shields.io/badge/Storage-SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white">
  <img alt="curl_cffi" src="https://img.shields.io/badge/Bridge-curl__cffi-2563EB?style=flat-square&logo=python&logoColor=white">
  <img alt="Docker" src="https://img.shields.io/badge/Deploy-Docker-2496ED?style=flat-square&logo=docker&logoColor=white">
</p>
---

## 项目简介

ConsoleX2API 是一个面向 `console.x.ai` 的 OpenAI 兼容网关。它将上游 `console.x.ai/v1/responses` 能力转换为常见的 OpenAI 风格接口，让现有客户端、脚本和代理工具可以通过 `/v1/chat/completions`、`/v1/responses` 等接口接入。

当前版本采用 **Rust + Python bridge** 架构：Rust 负责网关、账号池、管理后台和协议转换；Python 仅保留一个 `curl_cffi` bridge，用于更接近浏览器的 TLS/HTTP 指纹请求上游。

## 架构

```text
OpenAI Client / Third-party App
        |
        |  OpenAI-compatible /v1/*
        v
Rust Axum Gateway
        |
        |  account rotation, payload mapping, SSE adaptation
        v
Python curl_cffi Bridge
        |
        |  browser-like upstream request
        v
console.x.ai /v1/responses
```

核心目录：

| 路径 | 说明 |
| --- | --- |
| `src/` | Rust 网关主程序 |
| `scripts/curl_cffi_bridge.py` | Python 上游请求 bridge |
| `static/admin/` | 管理后台静态页面 |
| `config.defaults.toml` | 默认配置 |
| `.env.example` | 环境变量示例 |
| `Cargo.toml` / `Cargo.lock` | Rust 依赖配置 |

旧 Python FastAPI 服务已移除，项目不再通过 `python -m app` 或 `uvicorn app.main:app` 启动。

## 功能特性

| 功能 | 状态 | 说明 |
| --- | --- | --- |
| OpenAI Models | 支持 | `GET /v1/models` |
| Chat Completions | 支持 | `POST /v1/chat/completions`，支持流式和非流式 |
| Responses | 支持 | `POST /v1/responses` |
| 多账号池 | 支持 | SQLite 存储 SSO 账号，按请求轮询可用账号 |
| 账号刷新 | 支持 | 管理后台批量刷新，SSE 实时进度 |
| Tools 控制 | 支持 | 可开关 `web_search` / `x_search` |
| Reasoning 参数 | 支持 | 可配置默认 reasoning effort |
| 图片输入 | 支持 | Chat `image_url` 自动映射到 Responses 输入 |
| 管理后台 | 支持 | 账号导入、编辑、启停、删除、配置保存 |
| Realtime client secret | 支持 | `/v1/realtime/client_secrets` |
| Realtime WebSocket | 占位 | Rust 版本暂未完整代理 WebSocket |

> 当前上游请求模式为 `console.x.ai/v1/responses`。项目曾尝试 `grok.com` 新会话接口，但该路径更容易触发 Cloudflare challenge，因此默认保留原 console 请求模式。

## 快速开始

### 1. 安装依赖

需要安装：

- Rust 工具链
- Python 3.10+
- `curl_cffi`

安装 Python bridge 依赖：

```powershell
python -m pip install curl_cffi
```

构建 Rust 服务：

```powershell
cargo build --release
```

### 2. 准备配置

```powershell
Copy-Item .env.example .env
```

编辑 `.env`，至少配置：

```env
OPENAI_API_KEY=replace-with-your-gateway-key
ADMIN_KEY=replace-with-your-admin-key
ACCOUNTS_DB=accounts.sqlite3
GATEWAY_HOST=0.0.0.0
GATEWAY_PORT=8787
UPSTREAM_URL=https://console.x.ai/v1/responses
```

如果上游需要代理：

```env
UPSTREAM_PROXY=http://127.0.0.1:7899
```

如果遇到 Cloudflare 相关问题，可配置：

```env
UPSTREAM_CF_CLEARANCE=your-cf-clearance
UPSTREAM_CF_COOKIES=__cf_bm=xxx; other_cf_cookie=xxx
UPSTREAM_CF_USER_AGENT=Mozilla/5.0 ... Chrome/136.0.0.0 ...
UPSTREAM_IMPERSONATE=chrome136
```

### 3. 启动服务

```powershell
cargo run --release
```

管理后台：

```text
http://127.0.0.1:8787/admin
```

登录使用 `.env` 中的 `ADMIN_KEY`。

## 账号管理

推荐通过管理后台导入账号，每行一个账号：

```text
sso-token-1,team-id-1
sso-token-2,team-id-2
sso=token-3,team-id-3
```

说明：

- `team_id` 用于生成该账号自己的 Referer。
- 不建议把所有账号绑定到一个全局 `UPSTREAM_REFERER`。
- 状态为 `disabled`、`cooling`、`invalid`、`expired`、`failed` 的账号不会参与普通请求轮询。
- 非流式、流式和 Realtime client secret 请求都会使用同一个账号轮询索引。

## 配置说明

运行时配置读取优先级：

```text
config.toml > config.defaults.toml > 环境变量 > .env
```

管理后台保存的配置会写入 `config.toml`。

常用配置：

| 配置 | 说明 |
| --- | --- |
| `OPENAI_API_KEY` | 其他项目调用 `/v1/*` 时使用的 Bearer Key |
| `ADMIN_KEY` | 登录 `/admin` 的管理 Key |
| `ACCOUNTS_DB` | SQLite 账号数据库路径 |
| `GATEWAY_HOST` | 服务监听地址 |
| `GATEWAY_PORT` | 服务监听端口 |
| `UPSTREAM_URL` | 上游 Responses 地址，默认 `https://console.x.ai/v1/responses` |
| `UPSTREAM_PROXY` | 上游代理地址 |
| `UPSTREAM_IMPERSONATE` | `curl_cffi` 浏览器指纹，例如 `chrome136` |
| `UPSTREAM_CF_CLEARANCE` | Cloudflare `cf_clearance` |
| `UPSTREAM_CF_COOKIES` | 其他 Cloudflare cookie |
| `GATEWAY_WEB_SEARCH_ENABLED` | 是否允许 `web_search` |
| `GATEWAY_X_SEARCH_ENABLED` | 是否允许 `x_search` |
| `DEFAULT_REASONING_EFFORT` | 默认 reasoning effort |

## 接口调用

将其他项目的 OpenAI Base URL 指向：

```text
http://127.0.0.1:8787/v1
```

### Chat Completions

```bash
curl http://127.0.0.1:8787/v1/chat/completions \
  -H "Authorization: Bearer replace-with-your-gateway-key" \
  -H "Content-Type: application/json" \
  -d '{
    "model":"grok-4.3",
    "messages":[{"role":"user","content":"hello"}],
    "stream":false
  }'
```

### Responses

```bash
curl http://127.0.0.1:8787/v1/responses \
  -H "Authorization: Bearer replace-with-your-gateway-key" \
  -H "Content-Type: application/json" \
  -d '{
    "model":"grok-4.3",
    "input":"hello",
    "stream":false
  }'
```

### Models

```bash
curl http://127.0.0.1:8787/v1/models \
  -H "Authorization: Bearer replace-with-your-gateway-key"
```

## Docker 部署

构建镜像：

```powershell
docker build -t consolex2api:latest .
```

运行：

```powershell
docker run --rm -p 8787:8787 `
  -e OPENAI_API_KEY=replace-with-your-gateway-key `
  -e ADMIN_KEY=replace-with-your-admin-key `
  -e ACCOUNTS_DB=/app/data/accounts.sqlite3 `
  -v ${PWD}\data:/app/data `
  consolex2api:latest
```

Docker Compose：

```powershell
docker compose up -d --build
```

## 测试

```powershell
cargo test
python -m py_compile scripts/curl_cffi_bridge.py
```

如果 `cargo build --release` 在 Windows 上提示无法删除 `target\release\consolex2api.exe`，通常是服务正在运行。先在运行服务的终端按 `Ctrl + C` 停止，再重新构建。

## 许可证

本项目基于 [MIT License](./LICENSE) 开源。
