# Orbit · Emby Suite

> 面向 Emby 的一体化运营与观影门户：用户端、管理端、API 三个独立端口，真实接入你的 Emby / TMDB / Telegram / Webhook。

Orbit 不包含演示账号、演示媒体或模拟播放。首次启动只创建一个管理员，之后由你在管理端填写自己的服务地址与密钥，再同步真实媒体库。

- 用户端：`http://<host>:3000`
- 管理端：`http://<host>:3001`
- API / Webhook：`http://<host>:4000`

---

## 功能

### 用户端

- **追剧 / 订阅**：订阅剧集，暂停、恢复、取消，更新与入库提醒。
- **观影大屏**：全屏精选墙、正在播放、最近入库与在线人数，自适应电视 / 桌面 / 手机；媒体总数取真实库存，长标题自动分级缩放。
- **发现与媒体库**：按类型、画质、年代、关键词筛选；TMDB 未配置时只展示本地库。
- **用户数据**：观看时长、播放次数、追剧数量、最近观看、会员有效期。
- **求片海报墙**：按片名 / 原名搜索 TMDB 与本地库，海报流式加载、下滑自动翻页；已入库可直接进入详情，未入库一键求片，并实时显示审批与入库状态。
- **通知中心**：入库、更新、会员到期、求片状态、管理员广播。
- **线路中心**：普通线路全员可用，会员专线仅有效期内的会员可见；支持一键测速、设为个人默认线路，播放时自动按默认线路进入 Emby。
- **账号中心**：修改资料、密码、查看套餐与到期时间、生成邀请码。

### 管理端

- **首次初始化向导** `/setup`：创建唯一管理员，不写入任何示例数据。
- **服务设置**：Emby、TMDB、Telegram Bot、出站 Webhook 全部可视化配置，可随时修改并测试连接。
- **开号 / 用户管理**：创建账号、生成随机密码、续费、重置密码、停用/启用、设置套餐与并发数。
- **Emby 用户同步**：预览 Emby 真实用户后一键导入/映射到面板，自动跳过 Emby 管理员，可同步停用状态与并发数，不覆盖昵称、套餐与到期时间。
- **媒体库**：真实统计电影/剧集/集数/存储/画质/类型；手动添加媒体；一键从 Emby 同步；支持 Emby 封面补全、TMDB 按片名/年份补图、占位图与批量修复。
- **最近入库**：按真实 `added_at` 排序。
- **缺集 / 少集**：基于 TMDB 已播出集数与本地 `episodes` 比对，生成缺集记录。
- **实时监控**：Emby 会话、播放事件、在线状态、14 天流量趋势。
- **线路管理**：维护多条 Emby 线路，区分普通线路与会员线路，设置地区、排序、启用状态与站点默认线路，支持从当前 Emby 地址一键导入和单条连通性测速。
- **设备访问控制**：按设备名、播放器、IP、设备 ID、浏览器 UA 设置黑 / 白名单，支持 `*` 通配、`/正则/i` 与 CIDR；命中后可拒绝面板登录、自动停止播放、一键踢下线，并通过 Telegram 推送封禁详情、写拦截日志。
- **Telegram Bot**：`/bind` 绑定、命令交互、主动推送、消息记录。
- **Webhook**：Emby 入站回调 + 出站事件签名投递，带投递历史。
- **活跃保号**：设置最近活跃窗口（天）、自动续期天数与到期前检查天数；最近有登录/播放/会话/求片/订阅的会员在到期前自动延长有效期，支持一键预览与立即执行，每 6 小时自动检查。
- **通知与审计**：广播通知、渠道状态、操作审计日志。

---

## 更新日志

### v1.3.0（2026-10-23）

- 新增线路模块：管理端维护普通线路 / 会员线路，支持导入、测速、排序、启用与站点默认线路。
- 新增用户端线路中心：会员专线权限隔离、个人默认线路、一键测速与复制地址。
- 媒体详情页与账号中心接入多线路播放选择，非会员不会拿到会员线路地址。

### v1.2.0（2026-10-23）

- 新增设备访问控制：黑 / 白名单、在线设备、拉黑 / 踢下线、拦截日志与 Telegram 封禁通知。
- 新增求片海报墙：TMDB + 本地库搜索、无限滚动、海报预览与一键求片。
- 新增活跃保号：按最近活跃时间自动续期，支持预览与立即执行。
- 新增求片推送管理员 Telegram，附带 TMDB 海报、题材、评分与简介。
- 修复媒体库海报缺失、TMDB 补图、管理端概览 500、Telegram / TMDB 代理错误提示等问题。

完整记录见 [CHANGELOG.md](CHANGELOG.md)。

---

## 快速开始

### 方式一：Docker Compose（推荐，直接拉镜像）

```bash
git clone https://github.com/xiguazhu1998/orbit-emby-suite.git
cd orbit-emby-suite
cp .env.example .env
# 至少修改 JWT_SECRET
docker compose pull
docker compose up -d
```

镜像由 GitHub Actions 自动构建并发布到 GHCR：

```text
ghcr.io/xiguazhu1998/orbit-emby-suite:latest
ghcr.io/xiguazhu1998/orbit-emby-suite:1.2.1
```

> `docker compose pull` 只负责下载镜像，不会自动替换正在运行的容器；拉取后必须执行 `docker compose up -d`。如果本地没有新版镜像，`up -d` 仍会复用旧容器。
>
> 如需本地构建而不是拉镜像：`docker compose build && docker compose up -d`。

打开 `http://<host>:3001/setup` 创建管理员（表单默认账号 / 密码均为 `admin`，登录后请立即修改），然后进入 **设置**：

1. 填写 Emby 地址、API Key、对外播放地址。
2. 填写 TMDB API Key（用于发现、元数据、缺集比对）。
3. 可选：填写 Telegram Bot Token / Chat ID。
4. 保存后点击 **测试连接**。
5. 在媒体库点击 **从 Emby 同步**。

> 首次进入时媒体库为空是正常状态。同步完成前不会出现任何虚构内容。

### 更新到新版本

```bash
cd orbit-emby-suite
docker compose pull          # 拉取最新镜像
docker compose up -d         # 用新镜像重建容器，数据卷保持不变
docker image prune -f        # 可选：清理旧镜像
```

如果使用固定版本：

```bash
ORBIT_TAG=1.2.1 docker compose pull
ORBIT_TAG=1.2.1 docker compose up -d
```

查看当前版本：

```bash
curl http://127.0.0.1:4000/api/health
docker inspect orbit-emby-suite --format '{{.Config.Image}}'
```

### 方式二：本地运行

```bash
npm install --include=dev
npm run dev
```

开发模式会同时启动 API、用户端 Vite、管理端 Vite。生产模式：

```bash
npm run build
npm start
```

---

## 首次初始化

系统没有管理员时：

- `GET /api/setup/status` 返回 `initialized: false`
- 管理端任意页面会引导到 `/setup`
- `POST /api/setup/init` 创建唯一管理员并写入干净的默认设置
- 已存在管理员时再次初始化返回 `409`

初始化只创建管理员与空配置，不会创建媒体、会员、播放记录、缺集或通知。

> 管理端初始化表单默认填入 `admin / admin`，密码最少 5 位。默认凭据仅用于首次部署，登录后请立即在「设置 → 账号安全」修改密码；公网部署尤其不要保留默认密码。

```bash
curl -X POST http://127.0.0.1:4000/api/setup/init \
  -H 'Content-Type: application/json' \
  -d '{"siteName":"My Orbit","username":"admin","displayName":"管理员","password":"admin"}'
```

---

## 服务配置

所有配置保存在 SQLite 的 `settings` 表中，管理端保存后立即生效。密钥在读取接口中只返回掩码。

### Emby

| 字段 | 说明 |
| --- | --- |
| `host` | 服务端访问地址，例如 `http://192.168.1.10:8096` |
| `apiKey` | Emby API Key（用户设置 → 高级 → API 密钥） |
| `publicUrl` | 浏览器/播放器访问地址，可填反向代理域名 |
| `webhookToken` | 初始化时随机生成，用于 Emby 入站回调校验 |

同步行为：

- 分页拉取 `Movie` / `Series`
- 写入真实标题、年份、简介、评分、类型、画质、体积、季/集数
- 剧集逐部拉取 `Episodes`，写入 `episodes` 表
- 按 `emby_id` → `tmdb_id + type` → `title + type` 匹配已有记录

Emby Webhook 地址（在设置页直接复制）：

```text
http://<host>:4000/api/webhooks/emby?token=<webhookToken>
```

### 线路

在「管理端 → 线路管理」维护多条 Emby 入口，用户端「线路中心」和媒体详情页会按权限展示。

| 类型 | 可见范围 |
| --- | --- |
| 普通线路（`all`） | 所有已登录用户 |
| 会员线路（`member`） | 管理员、状态正常且未过期、套餐不属于「普通 / 免费 / 试用」的会员 |

- 非会员请求会员线路时，接口只返回 `locked: true`，不会下发真实地址。
- 站点默认线路全局唯一；删除默认线路后自动提升排序最靠前的一条。
- 用户可在用户端选择个人默认线路（保存在浏览器本地），媒体详情页的多线路播放会优先使用该线路。
- 地址必须是完整的 `http(s)` URL，填写 Emby 根地址即可，不要带 `/web` 路径。
- 测速使用 Emby 公开接口 `/System/Info/Public`，无需 API Key。

### TMDB

- 未配置：发现页只返回本地媒体库，不生成假数据。
- 已配置：趋势、搜索结果、剧集元数据、缺集比对。
- 同时支持 TMDB v3 API Key 与 v4 Read Access Token（`eyJ...`，自动使用 Bearer 认证）。
- TMDB 代理可单独填写；留空时自动复用 Telegram 代理，解决服务器无法直连 `api.themoviedb.org` 的问题。
- 海报通过 `/api/tmdb-image/*` 反向代理加载，浏览器无需直连 `image.tmdb.org`。
- 请求失败时返回本地结果并附带可读错误（超时、代理不可用、Key 无效、429 等），不会静默回退演示目录。

缺集扫描会读取 TMDB 已播出季/集，与 `episodes.present` 比对；已入库的集会清理对应缺集记录。

### Telegram

- 填写 Bot Token 后可测试连接、接收命令、主动推送。
- 国内服务器通常必须填写 HTTP 代理地址，例如 `http://127.0.0.1:7890`；支持省略 `http://`。
- 管理端会显示 Bot 用户名、最近一次成功时间与轮询错误（Token 无效、Chat ID 不存在、409 冲突等），不再静默失败。
- 命令：`/start` `/help` `/bind` `/whoami` `/stats` `/latest` `/search` `/subscriptions` `/subscribe` `/unsubscribe` `/mystatus` `/unbind` `/check`。
- `/bind 用户名 密码` 支持站内密码或 Emby 密码（首次校验通过后写入本地哈希），绑定成功后即可使用全部命令；建议只在私聊中使用，避免密码留在群聊记录里。
- 成员提交求片后，默认推送到「默认 Chat ID」和所有已绑定 Telegram 的管理员，附带 TMDB 海报、题材、评分、原名与简介；可在「系统设置 → Telegram Bot → 求片推送到管理员 Bot」关闭。
- 未配置时状态为 `not_configured`，不会伪造在线状态或延迟。

### 出站 Webhook

- 支持 `*` 或具体事件，例如 `subscription.created`、`media.imported`。
- 使用 `X-Orbit-Signature: sha256=<HMAC>` 签名原始请求体。
- 管理端可发送测试事件并查看投递历史。

---

## 环境变量

`docker-compose.yml` 会读取 `.env`。完整示例见 [.env.example](.env.example)。

| 变量 | 默认 | 说明 |
| --- | --- | --- |
| `USER_PORT` | `3000` | 用户端端口 |
| `ADMIN_PORT` | `3001` | 管理端端口 |
| `API_PORT` | `4000` | API / Webhook 端口 |
| `JWT_SECRET` | 无 | **生产必须设置**，至少 16 位随机字符串 |
| `DATA_DIR` | `./data` | SQLite 与运行数据目录 |
| `CORS_ORIGINS` | 空 | 需要跨域时填写，逗号分隔 |
| `EMBY_HOST` | 空 | 容器内访问 Emby 的默认地址，可被设置页覆盖 |
| `TMDB_API_KEY` | 空 | 可被设置页覆盖；支持 v3 Key 或 v4 Read Access Token |
| `TMDB_PROXY_URL` | 空 | TMDB 出站代理，留空复用 Telegram 代理 |
| `TG_BOT_TOKEN` | 空 | 可被设置页覆盖 |
| `TG_PROXY_URL` | 空 | Telegram 出站代理，例如 `http://127.0.0.1:7890` |
| `OUTBOUND_WEBHOOK_SECRET` | 空 | 默认出站签名密钥，首次初始化会生成随机值 |

数据库设置优先于环境变量；环境变量只作为默认值。

---

## 端口与反向代理

三个端口职责分离：

| 端口 | 服务 | 示例路由 |
| --- | --- | --- |
| `3000` | 用户端 SPA | `/`、`/library`、`/wall` |
| `3001` | 管理端 SPA | `/setup`、`/media`、`/monitor`、`/settings` |
| `4000` | API + 入站 Webhook | `/api/*`、`/api/webhooks/emby` |

Nginx 示例：

```nginx
server {
  listen 80;
  server_name orbit.example.com;
  location / { proxy_pass http://127.0.0.1:3000; }
}

server {
  listen 80;
  server_name admin.orbit.example.com;
  location / { proxy_pass http://127.0.0.1:3001; }
}

server {
  listen 80;
  server_name api.orbit.example.com;
  location / { proxy_pass http://127.0.0.1:4000; }
}
```

管理端建议加 IP 白名单、Basic Auth 或 VPN。Emby Webhook 必须能从 Emby 服务器访问 API 端口。

---

## 数据与备份

```text
data/
└── orbit.db        # SQLite 主库（WAL 模式）
```

备份：

```bash
docker compose stop orbit
cp data/orbit.db data/orbit.db.bak-$(date +%Y%m%d%H%M%S)
docker compose start orbit
```

升级不会自动删除数据。若要彻底重置，请先备份再删除数据库文件：

```bash
cp data/orbit.db data/orbit.db.bak
rm -f data/orbit.db data/orbit.db-wal data/orbit.db-shm
docker compose restart orbit
```

---

## 测试

```bash
npm run typecheck
npm run build
```

冒烟测试与 E2E 使用独立临时库，不会碰生产数据：

```bash
# 终端 1
DATA_DIR=/tmp/orbit-test USER_PORT=3100 ADMIN_PORT=3101 API_PORT=4100 \
JWT_SECRET=test-secret-123456 node server/index.mjs

# 终端 2
API_BASE=http://127.0.0.1:4100 \
USER_BASE=http://127.0.0.1:3100 \
ADMIN_BASE=http://127.0.0.1:3101 \
npm run smoke

API_BASE=http://127.0.0.1:4100 \
USER_BASE=http://127.0.0.1:3100 \
ADMIN_BASE=http://127.0.0.1:3101 \
npm run test:e2e
```

首次运行时测试会自动调用 `/api/setup/init` 创建管理员：

- 账号：`admin`
- 密码：`orbit-test-12345`

可通过 `ORBIT_ADMIN_USER` / `ORBIT_ADMIN_PASSWORD` 覆盖。请只在一次性数据库中运行。

无浏览器渲染检查：

```bash
npm run check:render
```

---

## 项目结构

```text
server/
├── index.mjs             # Express 入口、路由、SSE、静态托管
├── config.mjs            # 设置/环境变量读取
├── db.mjs                # SQLite 结构
├── setup.mjs             # 首次初始化与默认设置
├── library.mjs           # 真实媒体库统计
├── services/
│   ├── emby.mjs          # Emby 连接、条目、剧集、同步、密码校验
│   ├── emby-users.mjs    # Emby 用户预览、导入与映射同步
│   ├── tmdb.mjs          # TMDB 搜索、发现、缺集扫描
│   ├── telegram.mjs      # Bot 命令与推送
│   └── webhooks.mjs      # 出站签名投递
src/
├── user/                 # 用户端 React SPA
├── admin/                # 管理端 React SPA（含 /setup）
└── shared/               # 组件、样式、API 客户端
scripts/
├── smoke.mjs             # HTTP / 初始化 / 主要接口
├── e2e-workflows.mjs     # 全写流程
└── dom-render-check.mjs  # jsdom 路由渲染检查
```

---

## 安全

- 生产环境必须设置强随机 `JWT_SECRET`。
- 初始管理员默认为 `admin / admin`，登录后必须立即修改密码；公网环境请勿保留默认凭据。
- 管理端不要直接暴露公网，至少加一层访问控制。
- `.env`、`data/`、日志、数据库备份不要提交到 Git。
- 仅管理你拥有合法访问权的媒体内容。

漏洞报告方式见 [SECURITY.md](SECURITY.md)。

---

## License

MIT
