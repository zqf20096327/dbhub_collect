<p align="center">
  <img src="docs/assets/readme-banner.svg" alt="SeSeGraph" width="960" />
</p>

<p align="center">
  基于 Telegram 私有频道存图、Telegraph 发布图集页的自托管私人图册管理程序<br />
  单文件约 15MB · 内置 SQLite，无需外部数据库
</p>

<p align="center">
  <a href="https://github.com/littleseven2003/SeSeGraph/releases/tag/v1.5.0"><img src="https://img.shields.io/badge/Release-v1.5.0-D04223?style=flat-square" alt="Release" /></a>
  <a href="https://github.com/littleseven2003/SeSeGraph/pkgs/container/sesegraph"><img src="https://img.shields.io/badge/Docker-ghcr.io-0D7A72?style=flat-square" alt="Docker" /></a>
  <img src="https://img.shields.io/badge/Go-1.22%2B-1B1A17?style=flat-square" alt="Go 1.22+" />
  <img src="https://img.shields.io/badge/Vue-3-1B1A17?style=flat-square" alt="Vue 3" />
  <img src="https://img.shields.io/badge/License-AGPL--3.0-7A7469?style=flat-square" alt="AGPL-3.0" />
</p>

<p align="center">
  <a href="#这是什么">这是什么</a> ·
  <a href="#核心特点">核心特点</a> ·
  <a href="#界面预览">界面预览</a> ·
  <a href="#快速部署">快速部署</a> ·
  <a href="#上手指南">上手指南</a> ·
  <a href="#配置说明">配置说明</a>
</p>

<p align="center">
  <img src="docs/screenshots/gallery-desktop.webp" alt="画廊首页：焦点轮播与多列图集" width="960" />
</p>

## 这是什么

SeSeGraph 是一个自托管的私人图册发布与管理程序。你把本地图片、动图、ZIP 压缩包或短视频拖进后台工作台，程序通过你自己的 Telegram Bot 把媒体存入私有频道，通过本站短码网关 `/i/{short_code}` 流式转发，并自动生成可对外分享的 Telegraph 图集页面。

- **后台归自己管**：画廊、工作台、任务中心与设置页均需管理员登录后访问；本地只保存 SQLite 数据库与封面缩略图，不长期占用服务器硬盘存原图。
- **分享对外开放**：访客无需登录，可直接通过生成的 Telegraph 链接浏览图集、通过 `/i/{short_code}` 加载图片/视频，或通过可选的 `/rss.xml` 订阅已发布的公开图集。

### 部署前准备

1. 一台可访问 Telegram 与 Telegraph 接口（或可配置 HTTP/SOCKS5 代理）的 Linux 服务器。
2. 一个已解析到该服务器的 HTTPS 域名（用于拼接外链、分享文案与 RSS）。
3. 通过 [@BotFather](https://t.me/BotFather) 创建的 Telegram Bot Token，以及一个**私有频道**（需将该 Bot 设为频道管理员并授予发消息权限）。频道数字编号形如 `-1001234567890`。把 Bot 设为频道管理员后在频道里发一条测试消息，再在本机终端读取（Token 用隐藏输入，不要填进浏览器地址栏，否则会留在历史记录里）：

   ```bash
   read -rsp "Bot Token: " TG_TOKEN; echo
   # 请求地址经标准输入交给 curl，Token 不会出现在命令行参数或进程列表里
   printf 'url = "https://api.telegram.org/bot%s/getUpdates"\n' "$TG_TOKEN" \
     | curl -fsS --config - \
     | python3 -c 'import json,sys; d=json.load(sys.stdin); [print(u["channel_post"]["chat"]["id"]) for u in d.get("result", []) if "channel_post" in u]'
   unset TG_TOKEN
   ```

   输出的数字就是频道编号；读完后可在频道里撤回那条测试消息。

## 核心特点

### 1. 媒体导入与存图

- **多种素材直传**：支持静态图、动图（GIF / APNG / 动态 WebP，保留动画）、MP4 短视频（单段上限 `20MB`），以及文件夹和 ZIP 压缩包。静态图选择阶段上限 `50MB`，提交时按画质模式判定：`photo` 省流量上限 `10MB`，`document` 原图上限 `20MB`。
- **浏览器端解包与预填**：ZIP 压缩包（上限 500 项、展开总量 512 MiB，包内单个媒体须小于对应模式上限）直接在浏览器内解压、自然排序与拖拽调序，可读取包内 `info.txt` / `meta.txt` / `readme.txt` 自动预填标题与标签。
- **静态图自动压缩**：在工作台开启「自动压缩」后生效。`photo` 模式单图超过 `2.5MB`、`document` 模式超过 `8MB` 时在提交前自动缩放重编码；压缩后体积没有变小或编码失败、且原图未超当前模式上限时保留原图，动图不进入压缩。
- **短码流式转发**：图片与视频对外使用 `/i/{short_code}` 转发，不暴露 Bot Token、频道 ID 或原始 `file_id`；MP4 支持 HTTP `Range` 拖动播放。网关默认 25 路并发、满额最多 100 请求排队（单请求最长等 15 秒），减少多图页面裂图。

### 2. 任务控制与 Telegraph 发布

- **受控并发与断点续传**：前端默认每轮两路并发上传，服务端全局默认三路；任务中心支持按状态筛选，上传与发布中均可随时暂停、继续或停止。传图中断只补服务端缺项，频道转存失败可直接重试存图。
- **自动分篇与无中文短链**：超出 Telegraph 单页上限时自动分篇并互相链接；封面媒体固定排在 Telegraph 首项。支持按标题生成链接（`title`），或开启无中文短链（`slug`）生成纯英文短码路径后恢复真实标题。
- **浏览量与永久删除**：后台定时同步 Telegraph 页面浏览量到本地缓存，详情抽屉可手动刷新（默认 60 秒冷却）。撤回图集会立即停用短码；永久删除会先清空远端所有 Telegraph 页面为「此图集已撤回」，全部成功后才删除本地记录与孤立标签。

### 3. 画廊浏览与详情管理

- **隐私遮罩与双视图**：画廊支持卡片网格、信息列表与「最新 5 组」焦点轮播，支持关键词搜索与多标签筛选；封面默认模糊显示，点击揭开、鼠标移开即恢复遮罩，触屏与键盘采用短时揭开。
- **详情抽屉直达操作**：同一抽屉内集成媒体清单（固定列对齐、逐图小图，桌面悬停、窄屏点按预览）、行内一键「设为封面」、在线编辑标题/说明/标签/作者，以及可自定义的分享文案模板。
- **逐图缩略图缓存**：每项媒体落盘一份最长边 512px 的 WebP，行内 44px 缩略图与 224px 放大气泡共用；缓存命中时打开抽屉、预览与揭开都不再回源原媒体。上限默认 2 GiB，可在设置页调整、查看占用与条目数、清空或按图集重建；小图可重建，默认不进备份。

### 4. 轻量部署与运维保障

- **单文件零外部依赖**：前端通过 `go:embed` 打包进单个 Go 二进制（`linux/amd64` 约 15MB，零 CGO），内置 SQLite（WAL 模式），运行时不需要额外的数据库或缓存服务。
- **流量看护与自动备份**：按自然月统计图片网关出站流量，支持达到预警阈值时经 Bot 通知、达到硬上限后返回 503 熔断；支持每日定时热备 SQLite（可选含封面缩略图）并推送到私有频道，参数均可在设置页修改并立即生效。

## 界面预览

| 图集详情（含浏览量、分享模板与媒体清单） | 发布工作台 |
| :---: | :---: |
| ![图集详情](docs/screenshots/gallery-detail.webp) | ![发布工作台](docs/screenshots/workbench.webp) |
| 浏览量、分享文案与媒体清单（行内缩略图与设封面见上手指南） | 拖入图片/ZIP/MP4 即可排序、自动压缩并预填元信息 |

| 设置与流量看护 | 移动端画廊 |
| :---: | :---: |
| ![设置页](docs/screenshots/settings.webp) | <img src="docs/screenshots/mobile-gallery.webp" alt="移动端画廊" width="210" /> |
| 连通性自检、代理、月度流量阈值与自动备份 | 390px 窄屏适配：焦点轮播与同行标签入口 |

## 快速部署

提供三种部署方式。服务数据目录仅包含 `sesegraph.db`（含 WAL 文件）、`thumbs/`（封面缩略图）、`thumbs/media/`（逐图小图缓存，可随时清理重建）、`tmp/`（待上传临时文件）与 `backups/`（备份包），迁移时直接复制该目录即可。

> 以下命令按 `v1.5.0` 编写；如需安装其他版本，替换其中的版本号即可。

### 方式一：Docker Compose（推荐，含 Caddy 自动 HTTPS）

```bash
mkdir -p /opt/sesegraph && cd /opt/sesegraph
curl -fsSLO https://raw.githubusercontent.com/littleseven2003/SeSeGraph/v1.5.0/docker-compose.yml
mkdir -p deploy && curl -fsSL https://raw.githubusercontent.com/littleseven2003/SeSeGraph/v1.5.0/deploy/Caddyfile -o deploy/Caddyfile
curl -fsSL https://raw.githubusercontent.com/littleseven2003/SeSeGraph/v1.5.0/.env.example -o .env
# 至少填写 DOMAIN，以及 ADMIN_USERNAME/ADMIN_PASSWORD（或 ADMIN_SETUP_TOKEN）
chmod 600 .env
$EDITOR .env
docker compose up -d
```

镜像默认从 `ghcr.io/littleseven2003/sesegraph` 拉取，`SESEGRAPH_VERSION` 默认固定为 `v1.5.0`（如需跟随后续版本可改为 `latest`，也可用 `SESEGRAPH_IMAGE` 指定自定义地址）。宿主机数据位于 `/opt/sesegraph/data`，Caddy 证书保存在命名卷中。

`.env.example` 里代理、画质、Telegraph 链接方式、流量阈值与备份计划默认都是注释状态，这些项留空即由设置页维护；一旦在 `.env` 中填写，该字段就以环境变量为准，设置页对应项会置灰只读。

### 方式二：单容器 Docker（接入已有反向代理）

```bash
install -d -m 700 /opt/sesegraph
install -d -o 1000 -g 1000 /opt/sesegraph/data
curl -fsSL https://raw.githubusercontent.com/littleseven2003/SeSeGraph/v1.5.0/.env.example \
  -o /opt/sesegraph/sesegraph.env
chmod 600 /opt/sesegraph/sesegraph.env
# 容器内数据目录固定为 /app/data；同时在文件中填写 PUBLIC_URL 与管理员初始化项
sed -i 's|^DATA_DIR=.*|DATA_DIR=/app/data|' /opt/sesegraph/sesegraph.env
$EDITOR /opt/sesegraph/sesegraph.env
docker run -d --name sesegraph --restart unless-stopped \
  -p 127.0.0.1:8080:8080 \
  -v /opt/sesegraph/data:/app/data \
  --env-file /opt/sesegraph/sesegraph.env \
  ghcr.io/littleseven2003/sesegraph:v1.5.0
```

通过 `0600` 权限的 `--env-file` 传入凭据，避免密码进入命令历史。若使用已有 Nginx 或 Caddy，请反代至 `http://127.0.0.1:8080` 并关闭响应缓冲，示例见 `deploy/nginx.conf.example` 与 `deploy/Caddyfile.example`。

### 方式三：原生单二进制（systemd）

```bash
install -d /opt/sesegraph
useradd --system --home /opt/sesegraph --shell /usr/sbin/nologin sesegraph || true
curl -fsSL -o /opt/sesegraph/sesegraph \
  https://github.com/littleseven2003/SeSeGraph/releases/download/v1.5.0/sesegraph-v1.5.0-linux-amd64
chmod +x /opt/sesegraph/sesegraph
curl -fsSL https://raw.githubusercontent.com/littleseven2003/SeSeGraph/v1.5.0/deploy/sesegraph.service \
  -o /etc/systemd/system/sesegraph.service
install -d -m 750 /etc/sesegraph
curl -fsSL https://raw.githubusercontent.com/littleseven2003/SeSeGraph/v1.5.0/.env.example \
  -o /etc/sesegraph/sesegraph.env
chmod 600 /etc/sesegraph/sesegraph.env
# 填写 PUBLIC_URL 与管理员初始化项；监听地址与数据目录由单元文件的 --addr / --data 指定
$EDITOR /etc/sesegraph/sesegraph.env
systemctl daemon-reload && systemctl enable --now sesegraph
curl -fsS http://127.0.0.1:8080/api/health
```

上面的单元只监听 `127.0.0.1:8080`，还需要一层 HTTPS 反向代理才能用域名访问：

```bash
# Caddy：示例里的 gallery.example.com 要换成你的域名，证书由 Caddy 自动申请；
# 已有 Caddy 时不要覆盖整份配置，只把示例里的站点段合并进现有 Caddyfile。
install -d /etc/caddy
curl -fsSL https://raw.githubusercontent.com/littleseven2003/SeSeGraph/v1.5.0/deploy/Caddyfile.example -o /tmp/sesegraph.caddy
$EDITOR /tmp/sesegraph.caddy          # 改域名，必要时补 tls 证书路径
cat /tmp/sesegraph.caddy >> /etc/caddy/Caddyfile
systemctl reload caddy

# 或 Nginx：文件名换成你的域名，证书路径改成实际证书；注意关闭响应缓冲并放开请求体上限
curl -fsSL https://raw.githubusercontent.com/littleseven2003/SeSeGraph/v1.5.0/deploy/nginx.conf.example -o /etc/nginx/conf.d/sesegraph.conf
$EDITOR /etc/nginx/conf.d/sesegraph.conf
nginx -t && systemctl reload nginx
```

反代生效后用 `https://你的域名/api/health` 确认可以访问，再把 `/etc/sesegraph/sesegraph.env` 里的 `PUBLIC_URL` 改成这个 HTTPS 地址并 `systemctl restart sesegraph`。systemd 单元通过 `StateDirectory` 自动创建并授权 `/var/lib/sesegraph`。Linux（amd64/arm64）、macOS（arm64）与 Windows（amd64）产物及 `SHA256SUMS` 均在 Release 页面提供。

## 上手指南

部署完成后，按以下五步完成配置并发布第一篇图集：

1. **首次登录与修改账密**
   - 浏览器打开你的域名。已在环境变量预设 `ADMIN_USERNAME` / `ADMIN_PASSWORD` 的直接登录；未预设的，先配置 `ADMIN_SETUP_TOKEN`，首次访问页面按提示输入该令牌完成管理员初始化。
   - 登录后可在 **设置 → 账号安全** 中校验当前密码并修改用户名或密码；修改成功后旧会话立即失效，需使用新凭据重新登录。
2. **配置 Telegram 图床与代理**
   - 进入 **设置 → Telegram 图床**，填写 Bot Token 与私有频道标识（如 `-100…` 或 `@channel`）并保存。
   - 若服务器无法直连 Telegram/Telegraph，可在同页 **网络代理** 中切换系统代理或自定义代理（支持 `http`/`https`/`socks5` 及账密），并分别控制是否对两处上游生效。
3. **申请 Telegraph 账户并自检**
   - 在 **设置 → Telegraph 发布** 中填写默认作者名，点击 **「申请账户」** 自动生成匿名令牌（保存在服务端、不回显），也可通过环境变量 `TELEGRAPH_ACCESS_TOKEN` 手工提供；链接生成方式可选「按标题生成」或「自动生成无中文链接」。
   - 先点 **「保存设置」**，再点 **连通性自检**，确认 Telegram Bot 权限与 Telegraph 令牌均检测通过（自检读取已保存的配置）。
4. **上传素材并发布图集**
   - 进入 **工作台**，拖入图片、MP4、文件夹或 ZIP 压缩包，选择画质（`photo 省流量` / `document 原图`）与是否开启自动压缩，拖拽调序、点选封面并填写标题、说明与标签。
   - 点击 **「提交存图」** 上传至私有频道，存图完成后点击 **「发布到 Telegraph」** 生成图集页。过程随时可在顶栏 **「任务」** 中查看三阶段进度、暂停/继续/停止或重试失败项。
5. **画廊管理、对外分享与 RSS 订阅**
   - 回到 **画廊** 可按卡片或列表浏览、按标签筛选；点击某篇图集打开详情抽屉，可悬停缩略图预览、在列表内直接切换封面、编辑元信息、刷新浏览量、复制外链或按自定义模板复制分享文案。
   - **对外分享**：复制的 Telegraph 链接与 `/i/{short_code}` 媒体外链无需登录即可访问；在详情抽屉禁用或永久删除图集后，短码外链会立即失效。
   - **RSS 订阅**：在环境变量设置 `RSS_ENABLED=true` 且 `PUBLIC_URL` 为有效 HTTPS 地址后重启，即可通过 `https://你的域名/rss.xml` 订阅最近最多 50 篇公开、已发布且未撤回的图集。

## 配置说明

以下配置通过环境变量提供。其中 Bot Token、频道标识、Telegraph 作者名与链接方式、代理、画质、流量阈值与定时备份计划均可在 **设置** 页面在线维护并热生效；某项留空时由设置页接管，填写后该字段以环境变量为准并在界面上显示来源、置灰只读。两份 Compose 文件已透传这些变量，`.env` 留空即可在网页里修改。

| 变量 | 必填 | 说明 |
| --- | :---: | --- |
| `PUBLIC_URL` | 是 | 对外 HTTPS 地址，用于拼接图片外链、分享文案与 RSS，不能带查询串或凭据 |
| `ADMIN_USERNAME` / `ADMIN_PASSWORD` | 首次 | 仅首次初始化使用，初始化后以数据库中的密码哈希为准 |
| `ADMIN_SETUP_TOKEN` | 二选一 | 未预设管理员账密时，用于首次打开页面完成初始化，完成后失效 |
| `TELEGRAM_BOT_TOKEN` | 是 | 图床 Bot 令牌，需具备目标私有频道发消息权限 |
| `TELEGRAM_CHANNEL_ID` | 是 | 私有频道标识，形如 `-100…`，或 `@channel` |
| `TELEGRAPH_ACCESS_TOKEN` | 否 | Telegraph 访问令牌；留空时可在设置页点击「申请账户」自动生成 |
| `TELEGRAPH_AUTHOR_NAME` | 否 | Telegraph 页面显示的默认作者名 |
| `LISTEN_ADDR` / `DATA_DIR` | 否 | 监听地址与数据目录，容器内默认 `:8080` 与 `/app/data` |
| `UPLOAD_MODE` | 否 | 默认画质：`photo`（省流量）或 `document`（原图），工作台单帖可覆盖 |
| `UPLOAD_CONCURRENCY` | 否 | 服务端同时接收上传的上限，默认 `3`（前端每轮两路） |
| `TELEGRAPH_PATH_MODE` | 否 | `title` 按标题生成链接（默认），`slug` 先生成无中文短码路径再恢复标题 |
| `PROXY_CONCURRENCY` | 否 | 图片网关取流并发上限，默认 `25` |
| `PROXY_QUEUE_DEPTH` / `PROXY_QUEUE_WAIT` | 否 | 并发满额后允许排队的请求数（默认 `100`）与单请求最长等待秒数（默认 `15`） |
| `VIEWS_SYNC_MINUTES` | 否 | 后台浏览量同步间隔，默认 `30` 分钟 |
| `VIEWS_COOLDOWN_SECONDS` | 否 | 详情抽屉手动刷新浏览量冷却时间，默认 `60` 秒 |
| `RSS_ENABLED` | 否 | 设为 `true` 且 `PUBLIC_URL` 为有效 HTTPS 地址时提供 `/rss.xml`，默认 `false` |
| `MEDIA_THUMB_LIMIT_BYTES` | 否 | 逐图缩略图缓存上限（字节），默认 2 GiB；填写后设置页该项置灰只读 |

<details>
<summary>进阶配置：代理、流量看护与自动备份</summary>

| 变量 | 说明 |
| --- | --- |
| `PROXY_MODE` | `direct` 直连、`system` 跟随 `HTTP(S)_PROXY` / `ALL_PROXY`、`custom` 使用 `PROXY_URL` |
| `PROXY_URL` | 自定义代理地址（`http` / `https` / `socks5`，可带账密），保存后不回显 |
| `PROXY_FOR_TELEGRAM` / `PROXY_FOR_TELEGRAPH` | 分别控制 Telegram 与 Telegraph 上游是否走代理 |
| `TRAFFIC_ALERT_GB` | 当月出站流量达到该值后经 Bot 提醒一次，`0` 表示关闭 |
| `TRAFFIC_LIMIT_GB` | 当月出站流量硬上限，达到后网关返回 503 并停止取流，`0` 表示关闭 |
| `BACKUP_ENABLED` / `BACKUP_CRON` | 是否开启每日定时备份，默认每天 `0 3 * * *` |
| `BACKUP_KEEP` | 本地保留备份份数，默认 `7`，设置页可改并即时生效 |
| `BACKUP_CHANNEL_ID` / `BACKUP_INCLUDE_THUMBS` | 备份推送目标频道（留空复用图床频道），以及是否打包封面缩略图 |

</details>

## 本地开发

以下命令在仓库根目录执行：

```bash
make build                   # 构建前端并生成 bin/sesegraph
make test                    # 运行后端测试
make typecheck               # 前端 TypeScript 类型检查
(cd frontend && pnpm test)   # 运行前端单元测试
make frontend                # 仅重新构建并嵌入前端静态资源
make cross                   # 交叉编译四个平台二进制
```

前端独立调试可运行 `cd frontend && pnpm dev`，完成后回到根目录执行 `make frontend` 或 `make build`。本地从源码构建镜像：`docker compose -f docker-compose.yml -f docker-compose.build.yml up -d --build`。

## 升级与备份

- **自动迁移**：从 `v1.0.0` 起升级时，数据库会在启动时自动迁移到当前结构版本（版本 12），无需手工执行 SQL，旧图集顺序与链接保持不变。
- **升级前备份**：建议先停止服务并复制整个数据目录，或在 **设置** 页点击 **「立即备份」** 生成一致性快照。
- **Compose 更新**：先重新下载编排文件（新版本可能新增环境变量透传，只更新 `.env` 不会生效），再确认 `.env` 中 `SESEGRAPH_VERSION` 为目标版本：
  ```bash
  cd /opt/sesegraph
  curl -fsSLO https://raw.githubusercontent.com/littleseven2003/SeSeGraph/v1.5.0/docker-compose.yml
  docker compose pull sesegraph && docker compose up -d sesegraph
  ```
  宿主机数据目录与 Caddy 证书卷均会保留。

## 版本与许可

- 版本历史见 [CHANGELOG.md](CHANGELOG.md)。
- 本项目采用 [AGPL-3.0](LICENSE) 许可协议。
