# AngelNT

自研的即时通讯应用：一套服务端 + Windows / Linux 桌面端 + 安卓端，交互形态参考 QQ。
支持单聊与群聊、好友申请、@ 提醒、图片与语音消息、消息撤回 / 转发 / 收藏、全局搜索、
多端实时同步与应用内更新。

> **许可：PolyForm Noncommercial 1.0.0**
> 允许个人学习、研究、自用、修改与再分发；**禁止任何商业用途**（包括但不限于企业内部
> 经营使用、对外提供收费服务、集成进商业产品）。商用需单独书面授权。全文见 [LICENSE](LICENSE)。

## 技术栈

| 端 | 技术 |
| --- | --- |
| 服务端 | TypeScript · Fastify 5 · WebSocket（@fastify/websocket）· SQLite（better-sqlite3）· zod · JWT · bcrypt |
| 桌面端 | Electron 31 · Vue 3 · TypeScript · Pinia · Vite · electron-builder |
| 安卓端 | Flutter · Dart（Android / iOS 同源） |

## 目录结构

```
server/          Fastify + SQLite 服务端（REST + WebSocket）
  src/routes/    各业务路由（auth / users / friends / conversations / groups / messages / files / bots ...）
  src/*.ts       db、auth、ws、bots、config 等核心模块
  scripts/       smoke.mjs（端到端冒烟）、cleanup.ts（文件清理）
  version.json   版本与更新清单示例
desktop/         Electron + Vue3 桌面客户端
  src/main/      主进程（窗口、托盘、文件缓存、更新）
  src/preload/   预加载脚本（上下文隔离 + 白名单 API）
  src/renderer/  渲染进程（Vue3 + Pinia）
android/         Flutter 客户端
  lib/pages/     页面（会话、联系人、群组、资料、设置 ...）
  lib/*.dart     网络层、WebSocket、本地缓存、媒体、语音、更新
deploy/          Ubuntu + Caddy 一键部署脚本
```

## 主要功能

- **账号**：邀请码注册、登录、记住账号（密码只进系统密钥库）、同平台顶号（桌面与手机可同时在线）
- **关系**：好友申请、好友列表、黑名单、按账号 / 昵称搜索用户
- **消息**：单聊 / 群聊、已读回执、撤回、转发与合并转发、收藏、全局搜索、群内 @ 提醒
- **媒体**：图片与语音消息（按住说话、上滑取消）、头像 / 背景裁剪上传（512×512、1600×900）、本地磁盘缓存
- **群组**：建群、成员管理、群主 / 管理员角色、退群
- **同步**：WebSocket 按单条连接投递 + 断线后 `?since` 增量补拉
- **运维**：`/api/app/version` 版本检查与应用内更新、上传配额与磁盘水位保护、文件 TTL 定时清理
- **机器人**：Bot API（webhook 回调、流式消息、HMAC-SHA256 签名校验）

## 快速开始

### 1. 服务端

```bash
cd server
npm install
JWT_SECRET=dev-secret npm run dev        # 默认 http://127.0.0.1:8788
npm run smoke                            # 端到端冒烟测试（使用临时数据库）
```

首次启动时**第一个注册的用户即 owner**（账号编号 000001），系统会为它自动生成一个
不限次数的邀请码；其余用户注册必须带邀请码。

环境变量：

| 变量 | 默认值 | 说明 |
| --- | --- | --- |
| `PORT` | `8788` | 监听端口 |
| `HOST` | `0.0.0.0` | 监听地址 |
| `JWT_SECRET` | 内置开发值 | **生产必须注入**，否则登录令牌可被伪造 |
| `DB_PATH` | `server/data/chat.db` | SQLite 数据库路径 |
| `UPLOADS_DIR` | `server/data/uploads` | 上传文件目录 |
| `FILE_TTL_DAYS` | `7` | 上传文件保留天数 |
| `FILE_CLEANUP_INTERVAL_MS` | `3600000` | 清理任务间隔 |
| `DISK_MIN_FREE_BYTES` | `3GB` | 磁盘水位保护，低于该值拒绝上传 |

### 2. 桌面端

```bash
cd desktop
npm install
npm run dev                              # 默认连接 http://127.0.0.1:8788
QQ_API=http://192.168.1.10:8788 npm run dev   # 指向其它服务端
npm run typecheck                        # 主进程 / 渲染进程类型检查
npm run build                            # 打包渲染进程与主进程
npx electron-builder --win nsis          # 出 Windows 安装包
```

### 3. 安卓端

```bash
cd android
flutter pub get
flutter run --dart-define=ANGELNT_BASE_URL=http://192.168.1.10:8788
flutter build apk --release --dart-define=ANGELNT_BASE_URL=https://im.example.com
```

`ANGELNT_BASE_URL` 未指定时默认 `http://10.0.2.2:8788`（安卓模拟器访问宿主机的地址）；
真机调试请填电脑在局域网内的 IP。

**安卓发布签名**：仓库内不含任何密钥文件。需要可覆盖安装的 release 包时，在
`android/keystore.properties` 中配置（该文件已被 `.gitignore` 排除）：

```properties
storeFile=my-release.jks
storePassword=******
keyAlias=angelnt
keyPassword=******
```

未提供该文件时，release 构建落到 debug 签名——只适合本地自测，因为 debug keystore
每次生成都不一样，覆盖安装会报「签名不一致」。

### 4. 版本更新清单

`server/version.json` 是 `/api/app/version` 返回的示例内容，把 `latest` 与 `url` 换成
你自己的版本号和下载地址即可。安卓端需要单独配置 `platforms.android` 段，否则会拿桌面端
版本号做比较。

### 5. 服务端部署

`deploy/install.sh` 提供 Ubuntu 24.04 + systemd + Caddy（自动 HTTPS）的一键部署：

```bash
sudo bash deploy/install.sh --mode local --src /path/to/server --domain im.example.com
```

## 数据与隐私

- 数据库与上传文件都在 `server/data/`，已在 `.gitignore` 中排除，仓库不含任何聊天数据。
- 图片 / 文件的鉴权走 `Authorization: Bearer` 请求头，URL 本身不带凭证，因此可以长期命中
  浏览器与客户端的磁盘缓存。
- 密码只存 bcrypt 哈希，服务端无法还原明文；忘记密码只能重置。

## 商业使用

本项目禁止商业用途。如需商用（包括内部经营系统、SaaS、集成进商业产品），请通过
GitHub Issue 或仓库主页的联系方式取得书面授权。

## 免责声明

本项目为个人学习与技术实践作品，按「现状」提供，不附带任何担保。使用本项目搭建的服务
请自行做好数据备份与安全加固。
