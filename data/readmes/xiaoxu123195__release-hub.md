# Release Hub

自托管的桌面应用发行与更新服务。用一份简单的 `manifest.json` 契约,给你的桌面客户端(Electron / Wails / Tauri / 其他原生应用)提供统一的版本检查、下载分发能力,**完全自己掌控,无需依赖 GitHub Releases 或 App Store**。

- **单二进制 + SQLite**,一份 Docker 镜像部署整站,数据装在一个 volume 里
- **多应用托管**,一个 Hub 管你名下所有桌面产品
- **管理后台 + 游客下载页** 前后端一体
- 适合国内独立开发者、小团队内部工具分发

## 功能

- 多应用管理:slug / 名字 / 描述 / 图标
- Release 上传(任意二进制,exe / dmg / AppImage / zip),**流式写盘 + 流式 SHA-256**
- Stable / Beta 双 channel,关键更新 (`is_critical`) 标记
- 可"未发布"草稿状态,上传后暂不对外
- 游客下载页:`hub.yourdomain.com/` 打开即看到所有公开应用
- **游客详情页**:`/apps/:slug` 展示所有已发布 stable 版本,支持下载任意历史版本,`changelog` 按 Markdown (GFM) 渲染;beta 对游客不可见
- 公开 manifest API 供桌面客户端消费:
  ```
  GET /api/public/apps/:slug/manifest.json?channel=stable
  ```
- 下载路由带 `Content-Disposition: attachment`,浏览器直接触发下载
- 下载日志(IP + User-Agent),便于统计
- 单管理员 + bcrypt 密码 + HMAC 签名 HTTP-only cookie 会话
- **API Tokens**:后台可生成长期凭证供 CI 自动上传 release,权限等同管理员(不可管理 token 自身)

## 技术栈

- 后端:**Go 1.22+** · Gin · modernc.org/sqlite(纯 Go,无需 CGO) · golang-migrate
- 前端:**React 18** + Vite + TypeScript + Tailwind + shadcn 风格自绘组件 + Zustand + React Router
- 部署:三阶段 Dockerfile → Alpine 运行时镜像 ~30MB,数据持久化在 `/data` volume

## 快速开始(本地开发)

### 依赖

- Go 1.22+(推荐 1.25)
- Node.js 20+
- 一个现代浏览器

### 启动

```bash
# 1. 复制环境变量
cp .env.example .env
# 编辑 .env 设置 ADMIN_PASSWORD

# 2. 后端(终端 1)
go run .
# 看到 "release-hub listening on :8082" 即启动

# 3. 前端 dev server(终端 2)
cd frontend
npm install
npm run dev
```

打开 http://127.0.0.1:5173,用 `.env` 里的密码登录 `/admin`。

**开发期**:前端 Vite 跑在 5173,代理 `/api/*` 到 Go 的 8082,两个进程各司其职。

## 生产部署(Docker + Nginx Proxy Manager)

### 一、拉代码 + 配置环境

```bash
git clone https://github.com/你的账号/release-hub.git
cd release-hub
cp .env.example .env
# 编辑 .env:
#   ADMIN_PASSWORD=某个足够长的随机密码
#   BASE_URL=https://hub.yourdomain.com
```

### 二、准备外部 Docker 网络

`docker-compose.yml` 默认加入一个名为 `npm` 的外部网络,用于对接 Nginx Proxy Manager。如果你的 NPM 所在网络叫别的名字,编辑 `docker-compose.yml` 底部的 `networks.npm.name`。

确认网络存在:
```bash
docker network ls | grep npm
```

### 三、起容器

```bash
docker compose up -d --build
docker compose logs -f release-hub
```

### 四、NPM 配 Proxy Host

1. Domain Names:`hub.yourdomain.com`
2. Scheme `http`,Forward Hostname `release-hub`,Forward Port `8082`
3. SSL 标签页:Let's Encrypt,Force SSL + HTTP/2 + HSTS
4. **Advanced 标签页**(允许大文件上传):
   ```
   client_max_body_size 500M;
   proxy_read_timeout 300s;
   proxy_send_timeout 300s;
   ```

### 五、验证

- `https://hub.yourdomain.com/` → 游客下载页
- `https://hub.yourdomain.com/admin` → 管理后台登录

## 桌面客户端集成示例

任何桌面应用只需请求一个 URL:

```
GET https://hub.yourdomain.com/api/public/apps/your-app/manifest.json?channel=stable
```

返回:
```json
{
  "slug": "your-app",
  "version": "1.2.0",
  "channel": "stable",
  "released_at": "2026-04-20T10:00:00Z",
  "download_url": "https://hub.yourdomain.com/download/your-app/1.2.0",
  "sha256": "abcd...",
  "size_bytes": 52428800,
  "changelog": "- 新增 X\n- 修复 Y",
  "is_critical": false
}
```

客户端对比本地版本号,发现更新 → GET `download_url` 即得到安装包字节流 → 校验 `sha256` → 引导用户安装。

## CI 自动上传(API Tokens)

需要在 GitHub Actions / GitLab CI 里自动把构建产物推到 Hub 时,用 API Token 替代人工登录。

### 生成 token

1. 浏览器进 `/admin/tokens`,点"创建 token"
2. 填一个可识别的名字(例如 `github-actions`)、选是否过期
3. **再次输入登录密码**完成二次验密 → 服务端生成 `rhub_...` 明文
4. **复制明文,关闭弹窗后无法再次查看**(只存 SHA-256 哈希);弄丢了只能撤销重建

token 可以随时在列表里撤销(软删除,保留审计记录)。最近使用时间每个 token 1 分钟最多更新一次,不影响高频 CI 场景。

### 上传示例

```bash
curl -X POST "$HUB_URL/api/admin/apps/<slug>/releases" \
  -H "Authorization: Bearer $RELEASE_HUB_TOKEN" \
  -F file=@./dist/my-app-1.0.0.exe \
  -F version=1.0.0 \
  -F channel=stable \
  -F 'changelog=## v1.0.0\n- 新增 X\n- 修复 Y' \
  -F is_critical=false \
  -F published=true
```

**Windows PowerShell 注意事项**:

- `curl` 是 `Invoke-WebRequest` 的别名,**必须用 `curl.exe`**
- 行续符用反引号 `` ` ``,不是反斜杠 `\`
- 示例:

```powershell
$HUB_URL = "https://hub.yourdomain.com"
$TOKEN   = "rhub_xxxxxxxx"
curl.exe -X POST "$HUB_URL/api/admin/apps/my-app/releases" `
  -H "Authorization: Bearer $TOKEN" `
  -F "file=@./dist/my-app-1.0.0.exe" `
  -F "version=1.0.0" `
  -F "channel=stable"
```

### 安全约束

- Token 认证**不能访问** `/api/admin/tokens/*`(创建/列出/撤销 token 必须走 cookie 会话),防止偷到的 token 自己造新 token 实现持久化
- token 明文仅存在于创建响应中,DB 只存 SHA-256;日志不记录请求头,泄漏检测靠 `rhub_` 前缀做 secret scanning

## 目录结构

```
release-hub/
├── main.go                     # 启动入口(DB + migrate + bootstrap + router)
├── spa_dev.go / spa_prod.go    # build tag 切换是否 embed 前端
├── backend/
│   ├── auth/                   # 登录、session、中间件
│   ├── apps/                   # 应用 CRUD
│   ├── releases/               # 版本 CRUD
│   ├── public/                 # 游客 API + 下载
│   ├── storage/                # 文件读写 + sha256
│   ├── db/                     # SQLite 连接 + migrate + bootstrap
│   │   └── migrations/
│   ├── config/                 # env 读取
│   └── httpx/                  # gin 路由组装 + SPA fallback
├── frontend/
│   └── src/
│       ├── pages/              # Public / Login / Dashboard / AppDetail
│       ├── components/         # AdminShell + UploadReleaseDialog + ui/
│       ├── api/                # 类型化的 fetch 封装
│       └── stores/             # Zustand auth store
├── Dockerfile                  # 三阶段构建
├── docker-compose.yml          # 生产编排(外部 npm 网络)
└── docker-compose.override.yml.example  # 本地测试用(不加入主编排)
```

## 认证说明

- 启动时:`admins` 表为空 → 读 `ADMIN_PASSWORD` env,bcrypt 写入 DB,之后该 env 被忽略
- 启动时:`settings.session_secret` 为空 → 自动生成 32 字节随机密钥写入 DB
- 登录成功发 HMAC 签名的 HTTP-only cookie,默认 7 天有效
- 忘密码恢复:SSH 到服务器 → `docker exec -it release-hub sqlite3 /data/hub.db "DELETE FROM admins;"` → 重启容器,会从 env 重新种子

## 贡献

欢迎 Issue 和 PR。开发前请确保:
- 后端: `go build ./...` 零 warning
- 前端: `npx tsc --noEmit` 通过

## License

MIT © 2026 xuyue
