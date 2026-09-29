# starwill_base — 通用业务系统脚手架

一套把网站常见功能都做好的通用业务系统脚手架（基于 **PHP 8 + ThinkPHP 8 + Layui**）：内置登录注册、用户管理、在线聊天、流量统计、网站配置、主题设置，以及 **OAuth 2.1 / OIDC 授权服务器** 与 **MCP 大模型接入** 能力；还自带**待办、每日名言**等开箱即用的示例模块。**功能支持"即插即拔"**：通过 `tp8/tools/scaffold-build.php` 按需裁剪（聊天 / AI / 流量统计等均可移除），未被选择的功能代码物理不出现在目标脚手架，安装向导中也可按勾选初始化对应数据表。配置数据库即可开箱即用，你只需编写自己的业务功能。

---

## 快速开始（Windows + XAMPP，零基础可跟做）

> 前提：你已经装好 XAMPP（含 Apache、MySQL、PHP），浏览器能打开 `http://127.0.0.1/`（XAMPP 欢迎页）。**全程不用敲命令行**，跟着下面的步骤走，每一步都写了"怎么算成功"。下面路径以 XAMPP 默认安装位置 `C:\xampp\` 为例，如果你安装时改了位置，把 `C:\xampp` 换成你的实际路径即可。

### 第 1 步：把项目放进 XAMPP 的网站目录

1. 打开文件管理器，进入 `C:\xampp\htdocs\`（这就是 XAMPP 的"网站目录"，放这里的文件夹都能用网址访问）；
2. 把整个 `starwill_base` 文件夹**整个复制**进去（看到 `C:\xampp\htdocs\starwill_base` 就对了）；
3. 打开 **XAMPP 控制面板**（开始菜单 → XAMPP → XAMPP Control Panel），点 Apache 和 MySQL 两行右边的 **Start**，让两行都变成绿色；
4. 浏览器打开 `http://127.0.0.1/starwill_base/view/pages/starwill/login.html`，能看到登录页（带图形验证码）就算环境正常。此时登录不了是正常的（数据库还没配），继续下一步。

> 💡 推荐用 Chrome / Edge / 360 等现代浏览器，不要用老版 IE（页面样式会乱）。

### 第 2 步：一键初始化（浏览器安装向导，全自动）

打开 `http://127.0.0.1/starwill_base/view/pages/starwill/login.html`，**系统会自动检测到"尚未初始化"并跳转到安装向导页面**，你只需在浏览器里：

1. **选择功能插件**（向导第 1 步）：即时通讯 / 待办 / 每日名言 / API Key / 流量统计等默认全部勾选；不勾选的插件不会建对应数据表，可随时全选或按需裁剪；
2. 填写**你自己 MySQL 的数据库信息**（主机 `127.0.0.1`、端口 `3306`、库名 `starwill_base`；用户名和密码填你的实际账号——例如 XAMPP 的 `root` 若设了密码，就填 `root` + 你的密码，**不要用空密码**）；
3. 点"**测试连接**"实时校验，无误后进入下一步；
4. 测试库默认"复用主库账号"，无需额外配置；附加库区域仅显示**已勾选插件**对应的归档库（如未勾选"即时通讯"则聊天归档库不出现、不会创建）；
5. 点"**开始安装**"，系统自动完成：
   - **导入数据库**：执行 `tp8\database\install.sql`（按所选插件自动裁剪），创建 4 个库（`starwill_base` 主库 / `starwill_base_test` 测试库 / `starwill_chat_archive` 聊天归档库 / `starwill_traffic_archive` 流量审计库），建好主库表并写入基础数据（每日名言、首页图标、待办示例）；**测试库的表**已随脚本一并建好；**聊天归档库 / 流量审计库**的表由系统迁移时自动创建；
   - **生成随机 JWT_SECRET**：自动生成 64 位随机密钥；
   - **生成 `tp8\.env`**：账号密码、随机密钥自动填好。
6. 看到"初始化完成"，点"进入系统"即跳转登录页。

> 💡 **手动替代方案**：也可完全手动：复制 `tp8/.example.env` 为 `.env` 改配置 + phpMyAdmin 导入 `install.sql`。两种方式任选其一。

**系统不内置任何账号**——首次注册的用户自动成为管理员（见第 3 步）。

### 第 3 步：启动系统

打开 `http://127.0.0.1/starwill_base/view/pages/starwill/login.html`，点"注册"创建**你自己的账号和密码**并登录（**首个注册的账号自动成为管理员**）。能看到图形验证码、登录成功进入首页、首页快捷图标显示正常——**系统就跑通了**。

### 第 4 步：启动聊天服务（可选，要用网页聊天才需要）

网页里的即时聊天靠一个**独立的常驻程序**（Workerman，端口 9512 起，被占用自动 +1）支撑，它和网站本体是分开启动的。两种启动方式任选：

**方式 A：手动启动（每次开机都要做一次）**
1. 按 `Win + R`，输入 `cmd` 回车，打开黑色命令行窗口；
2. 输入 `cd C:\xampp\htdocs\starwill_base\tp8` 回车；
3. 输入 `php think worker:server` 回车；
4. 看到端口 9512（或自动 +1 后的实际端口）的启动日志就是成功了，**这个窗口不能关**——关了聊天就停了。每次开机想用聊天，都要先这样启动一次。

**方式 B：注册开机自启（推荐，装一次自动生效）**
在安装向导完成页点击"**注册开机自启（生成脚本）**"，会生成 `worker_service/` 下的脚本（`start_worker.bat` / `register_worker_service.bat` / `unregister_worker_service.bat`，仅本机路径有效、不入库）。然后：
1. 打开文件夹 `C:\xampp\htdocs\starwill_base\worker_service\`；
2. **右键** `register_worker_service.bat` → 选择"**以管理员身份运行**"（注册计划任务需要管理员权限，普通双击会提示"需要管理员权限"）；
3. 看到"已注册开机自启任务"即成功——**以后开机自动启动聊天服务，无需手动开窗口**。
4. 如需卸载：右键 `unregister_worker_service.bat` → 以管理员身份运行（会删除自启任务并**自动停止正在运行的聊天服务**）。

> 引导页完成页的聊天状态旁有"**重新检测**"按钮：运行注册/卸载脚本后点击即可刷新"已启动 / 未启动 / 端口被占用"状态，无需刷新页面。

> 💡 如果只学增删改查、暂不用聊天，这一步可以跳过，其他功能完全不受影响。

### 环境要求与扩展（只有出问题时才看）

- **PHP 版本**：需要 ≥ 8.2。在 XAMPP 控制面板 Apache 那行点 "Config → PHP (php.ini)"，或打开 `C:\xampp\php\php.ini`，或浏览器访问 `http://127.0.0.1/dashboard/phpinfo.php` 查看；若低于 8.2，请安装较新的 XAMPP 版本。
- **必需 PHP 扩展**：`gd`（验证码/图片）、`curl`（第三方登录）、`openssl`（加密）、`mbstring`（中文）、`pdo_mysql`（数据库）。XAMPP 默认一般都已开启；若登录页验证码显示成破图，多半是 `gd` 没开——编辑 `C:\xampp\php\php.ini`，把 `;extension=gd` 这行开头的分号 `;` 删掉，保存后在 XAMPP 控制面板里重启 Apache（Stop 再 Start）。
- **伪静态（路由）**：`tp8/public/` 下的 `.htaccess` 已随项目自带，XAMPP 默认允许，一般**无需任何配置**。若登录成功但接口报 404，检查 `C:\xampp\apache\conf\httpd.conf` 中网站目录的 `AllowOverride` 是否为 `All`。
- **依赖（不用装 Composer）**：`tp8/vendor/`（第三方代码库）已随项目一起提供，clone 下来就能跑。

### 常见问题速查

| 现象 | 原因 | 解决 |
|---|---|---|
| 登录页提示"数据库连接失败"或接口报 500 | `.env` 里数据库配置不对 | 重点检查 `DB_USER`/`DB_PASS` 是否填了你的 MySQL 实际账号密码（不要用 `root` 空密码） |
| 验证码不显示或显示破图 | PHP 的 `gd` 扩展没开 | 见上方"环境要求与扩展"第 2 条 |
| phpMyAdmin 导入提示文件过大 | 上传大小限制 | 编辑 `C:\xampp\php\php.ini`，把 `upload_max_filesize` 和 `post_max_size` 调大（如 256M），保存后重启 Apache |
| 首页图标 / 样式全乱 | 浏览器缓存旧资源 | 按 `Ctrl + F5` 强制刷新；或清浏览器缓存 |
| 首页图标显示为方框 | 旧版系统（如 Windows 7 / 旧浏览器）缺 emoji 字体 | 首页图标编辑弹窗里把"图标"改为**图片 URL**（如 `static/xxx.png`，先把图片放进 `view/static/`；前端已支持 emoji 与图片两种图标，图片无需联网） |
| 别的机器访问不了 | 防火墙拦截 | 在 Windows 防火墙中放行 Apache（`httpd.exe`）的入站规则，并确认同一局域网 |
| 聊天窗一直连不上 | Workerman 聊天服务没启动，或端口被其他程序占用 | 见快速开始"第 4 步"：启动 `php think worker:server`（端口 9512 起自动 +1），保持命令行窗口不关；若提示端口占用，用 `netstat -ano \| findstr :9512` 排查占用进程 |

**首页图标显示方框（旧系统）快速替换**：脚手架已内置 15 个线性 SVG 图标（`view/static/icons/starwill/`，主题紫，本地文件无需联网，含 13 个功能图标 + lock/unlock 界面用图标）。旧系统用户可在 phpMyAdmin 对 `sys_icon_config` 执行批量替换，或逐条在首页图标编辑弹窗手动改为对应图片路径：

```sql
UPDATE `sys_icon_config` SET `icon`='static/icons/starwill/login.svg'        WHERE `icon`='🔑';
UPDATE `sys_icon_config` SET `icon`='static/icons/starwill/authorization.svg' WHERE `icon`='🔐';
UPDATE `sys_icon_config` SET `icon`='static/icons/starwill/users.svg'         WHERE `icon`='👥';
UPDATE `sys_icon_config` SET `icon`='static/icons/starwill/oauth.svg'         WHERE `icon`='⚙️';
UPDATE `sys_icon_config` SET `icon`='static/icons/starwill/daily-quote.svg'   WHERE `icon`='📝';
UPDATE `sys_icon_config` SET `icon`='static/icons/starwill/apikey.svg'        WHERE `icon`='🗝️';
UPDATE `sys_icon_config` SET `icon`='static/icons/starwill/chat.svg'          WHERE `icon`='💬';
UPDATE `sys_icon_config` SET `icon`='static/icons/starwill/site-settings.svg' WHERE `icon`='🛠️';
UPDATE `sys_icon_config` SET `icon`='static/icons/starwill/traffic.svg'       WHERE `icon`='📊';
UPDATE `sys_icon_config` SET `icon`='static/icons/starwill/theme.svg'         WHERE `icon`='🎨';
UPDATE `sys_icon_config` SET `icon`='static/icons/starwill/api-docs.svg'      WHERE `icon`='📄' OR `icon_name`='API 文档';
UPDATE `sys_icon_config` SET `icon`='static/icons/starwill/frontend-test.svg' WHERE `icon`='🧪' OR `icon_name`='前端测试';
UPDATE `sys_icon_config` SET `icon`='static/icons/starwill/backend-test.svg'  WHERE `icon`='🛠️' OR `icon_name`='后端测试';
```

> OAuth 密钥：首次调用 OAuth 接口自动生成 RSA 密钥对（`tp8/config/oauth2-keys/`），**私钥不入库**，请备份并限制权限；公钥已入库供验证 id_token。
> 依赖：`tp8/vendor/` **已完整随仓库提交**（含验证码字体与 PHPUnit），**内网无互联网也无需 composer**，clone/pull 即可运行；仅新增第三方包时才需在能联网的环境执行 `composer install` 后把 vendor 重新提交入库。

---

## 功能特性

按"帮你解决什么问题"分组，技术要点供查阅：

> 💡 零基础读者：下面每条都是**装好就能用、不用自己写**的功能。先看粗体标题知道"能干什么"就行，括号里的技术词看不懂没关系。

**账号体系**：注册/登录/登出/改密码/头像上传，图形验证码开箱即用，登录态基于服务端 Session（库内 token 供 Bearer / API 场景校验）；用户管理 + API Key（`ak_` 开头，Bearer / X-Api-Key 双通道鉴权）；兜底：系统无管理员时，首个注册用户自动成为管理员（配合"不能删除最后一个管理员"保护）。

**对外授权登录（OAuth 2.1 / OIDC）**：让第三方应用能安全地"用你的账号体系登录"。授权码 + PKCE（RFC 7636）、Refresh Token、令牌撤销（RFC 7009）、动态客户端注册（RFC 7591）；`.well-known` 发现端点位于 issuer 根下（openid-configuration / oauth-authorization-server / jwks / 受保护资源元数据，RFC 9728，无版本号）；**授权/令牌等业务端点统一走 `/api/v1/oauth2/*`**；令牌 SHA-256 哈希存储、RSA RS256 签名 id_token、客户端可视化管理与密钥重生成。

**接入大模型（MCP）**：MCP Streamable HTTP 端点 `/api/ai/mcp`，兼容 OpenWebUI、CodeBuddy 等客户端；统一 AI 接口 `/api/ai`（API Key 鉴权）；工具集覆盖待办/名言/图标，写操作管理员校验、数据按 API Key 所属用户隔离。

**网站配置**：可扩展 K-V 配置（`sys_site_config` 表，值支持字符串/数字/布尔/JSON），内置 `site_name`/`site_logo`/`site_description`/`copyright`/`icp`/`site_version` 默认值；独立管理页 `site-settings.html`，页脚版权、聊天窗标题、导出文件头统一读取配置。

**聊天与消息**：用户单聊/群聊/系统消息，已读回执实时推送，消息统一落库；WebSocket（Workerman，端口 9512 起自动递增）：30 秒一次性票据换身份、心跳保活、断线指数退避重连、离线消息补发；双入口（右下角悬浮聊天窗 + 独立聊天页 `chat.html`）；附件图片与安全格式文件（白名单 + 真实性校验 + 尺寸边界）；按月自动分表，**超过 12 个月自动迁移至聊天归档库**（主库保持近 12 个月，历史跨库查询并提示耗时更长）；聊天记录导出（UUID + SM3 摘要 + 国密 HMAC-SM3 签名，可校验防篡改）。

**流量统计（管理员）**：PV/UV / API 调用量 / 数据传输量，前端自动上报 + 服务端中间件记录；首页概览卡片 + 独立报表页 `traffic.html`（趋势折线、TopN 联动）；聚合按月分表，**超过 12 个月自动迁移至流量审计库**（备审计，部署时创建），上报匿名化、接口 IP 限流。

**前端脚手架**：前后端分离，原生静态页 + Layui 2.13 / ECharts 6 / sm-crypto（国密）；统一框架层 `auth.js`/`components.js`/`api.js`/`storage.js`，路径前缀**运行时自动推导**（顶层目录名可任意改名）。

> **Vue3 前端（新，可选）**：`view/vue3/` 提供基于 **Vue3 + TypeScript + Vite** 的全量重写前端（组合式 API + Pinia + Vue Router + Element Plus），复用 `view/static/` 主题资源。构建产物 `dist/` 随仓库提交（内网离线可直接访问），URL：`http://127.0.0.1/starwill_base/view/vue3/dist/index.html`。开发：`cd view/vue3 && npm install && npm run dev`；构建：`npm run build`（`vue-tsc` 类型检查 + `vite build`）。新旧前端并存可切换，旧 Layui 页面保留可回退。

**业务示例（待办 / 每日名言）**：两个开箱即用的完整模块——待办清单、每日名言，前端页面 + 后端接口 + 数据表都齐了。它们也是新功能开发的"学习蓝本"：照着其中一个抄，就能做出自己的业务模块。

**主题设置**：3 套预设主题（量子紫 / 夜间 / 浅色）+ 自定义 6 项取色；独立主题页 + 首页悬浮球双入口，切换立即生效，下次打开不闪变。

**工程化与安全**：Swagger/OpenAPI 接口文档；一键数据库安装脚本（已清洗）；安全基线：RSA 私钥不入库、`.env` 不入库、PKCE 强制、字段白名单。

## 技术栈

| 层 | 技术 |
|---|---|
| 后端 | PHP 8.x · ThinkPHP 8 |
| 数据库 | MySQL / MariaDB（utf8mb4） |
| 前端 | 原生 JS · Layui 2.13 · ECharts 6 · sm-crypto |
| 协议 | OAuth 2.1 / OIDC · MCP (Streamable HTTP) · OpenAPI |

## 目录结构

```
starwill_base/
├── index.html                # 入口跳转页（自动跳到 view/index.html，即网站首页）
├── view/                     # 前端（浏览器里看到的全部页面）：js/starwill/ 框架 JS · static/ 主题资源 · pages/ 页面容器 · plugs/ 第三方库
├── tp8/                      # 后端（ThinkPHP 8）：app/ 业务代码 · public/ Web 入口 · config/ 配置 · route/ 路由 · database/ 安装脚本 · vendor/ 依赖
├── thinkphp8所需composer/    # 本地 Composer 工具（composer.phar，一般用不到）
└── .gitea/                   # Gitea Actions 工作流（CI，可选启用）
```

> `gitea_webhook/` 门禁部署工具**已随仓库入库**（项目根目录 `gitea_webhook/`）：使用时将整个目录**复制到 Web 根目录、与项目同级**（如 `htdocs\gitea_webhook`）独立运行，避免部署脚本的 `reset --hard` 波及本工具；用法见 `docs/内网快速部署指南.md` 第六章，或 `gitea_webhook/README.md`。

## 前端静态化与缓存策略

- **前端完全静态**：`view/` 由 Web 服务器直接静态托管，不依赖后端 PHP 处理。
- **主题机制**（纯静态三件套）：`theme.css` 全部主题规则（页面静态引用，首帧生效）→ `theme-head.js` 首屏脚本（读 localStorage 立即设置，防首帧闪烁）→ `components.js` 运行时切换（漏引 theme.css 时兜底加载）。
- **缓存策略**（`view/.htaccess`，全静态资源 no-cache 协商缓存，普通刷新（F5）即生效，无需清缓存/强刷）：`.html` → `no-cache, must-revalidate`；`.js/.css`、图片/SVG/字体（含图标 `static/icons/starwill/*.svg`）→ `no-cache`（浏览器每次带 If-Modified-Since/If-None-Match 校验，未改返回 304 用缓存、已改返回 200 新内容，改文件自动生效，零手动操作）。**SVG 已在 mod_deflate 排除名单**（避免 gzip 压缩导致 ETag 弱化、协商缓存失效）；资源引用不依赖 `?v=` 版本戳，首页图标接口还会为图标 URL 自动追加文件 mtime 参数（`?t=filemtime`），任何浏览器（含 IDE 内置预览）修改文件后必然重新下载最新。

## API 规范

- 业务 API 统一带 `v1` 前缀（`/api/v1/auth/login`）；OAuth/OIDC 业务端点统一 `/api/v1/oauth2/*`（含 `/api/v1/oauth/*` 第三方登录），`.well-known` 发现端点位于 issuer 根下无版本号（符合 RFC 8414 / OIDC Discovery）
- 分页：`page`/`page_size`（兼容 `limit`），响应统一 `{list, total, page, page_size, has_more}`
- 异常统一 JSON `{code, message, data}`（api/ 请求 404/405/422/500，不再返回 HTML 错误页）
- 限流标准头 `X-RateLimit-Limit/Remaining/Reset`；健康检查 `GET /api/v1/health`；OpenAPI `GET /api/v1/openapi.json`（运行时生成，缓存 60 秒）

## 脚手架与用户代码边界

后端按"脚手架 vs 用户代码"物理分离，便于区分可改与不可改区：脚手架代码放 `tp8/app/controller/starwill/`、`model/starwill/`、`route/starwill.php` 等（**请勿修改**，文件头带 `[星毅脚手架]` 标记）；你的业务代码放 `tp8/app/controller/`、`model/`、`route/app.php`（先加载，同 URL 优先，可覆盖脚手架路由）。

**完整性校验**（检测脚手架是否被误改）：
```bash
php tp8/tools/check-scaffold.php --init   # 首次生成基线清单（scaffold-manifest.json）
php tp8/tools/check-scaffold.php          # 校验：输出被修改/缺失文件，有问题退出码非 0
php tp8/tools/check-scaffold.php --files  # 查看受保护脚手架文件清单
```

**示例三件套**：`ExampleController.php`（控制器）+ `Example.php`（模型）+ `route/app.php` 示例路由 `/api/example`，访问可验证"控制器 → 模型"调用链。注意：脚手架路由用 TP8 多级控制器语法（`starwill.auth/register`），用户子目录控制器用 `.` 分隔（`custom.demo/index`）。

**数据表前缀约定**：脚手架全部数据表统一使用 `sys_` 前缀（`sys_user`、`sys_todo` 等，由 `.env` 的 `DB_PREFIX = sys_` 全局配置驱动）。**你的业务表请使用自己的独立前缀**（如 `biz_`），不要用 `sys_`，避免与脚手架表冲突；表前缀由你自行维护（建表/备份/迁移）。升级脚手架只动 `sys_` 表，不影响你的业务表。

## .env 配置说明

`.env` 是项目自己的**配置文件**（在 `tp8/` 目录下）：包含数据库密码、JWT 密钥等敏感信息，**已被 gitignore，不会提交到仓库**。**首次访问系统时，浏览器会引导进入 Web 安装向导自动生成 `.env`**（自动建库 + 填好账号密码 + 随机 JWT）；也可手动复制模板 `tp8/.example.env` 为 `.env` 后按需修改。两种方式任选其一。

**快速开始第 2 步（Web 向导）已自动填好 `DB_USER`/`DB_PASS`/`JWT_SECRET` 及测试/审计/归档库凭据**；手动改时注意：`DB_NAME` 模板已对（`starwill_base`），`TEST_DB_*`（跑后端测试时配）、`TRAFFIC_DB_*`（流量审计库）、`CHAT_DB_*`（聊天归档库）按需配置。完整配置项参考：

| 配置项 | 作用 | 默认值 | 什么时候改 |
|---|---|---|---|
| `APP_DEBUG` | 调试开关（`true` 显示错误详情） | `false` | 开发排查问题时临时改 `true`，生产必须 `false` |
| `DB_TYPE` / `DB_HOST` | 数据库类型 / 地址 | `mysql` / `127.0.0.1` | 数据库不在本机时改 `DB_HOST` |
| `DB_NAME` | 数据库名 | `starwill_base` | 一般不用动（与 install.sql 建库名一致） |
| `DB_USER` / `DB_PASS` | 数据库账号 / 密码 | 占位值 | **必须改**：填你自己 MySQL 的账号密码 |
| `DB_PORT` / `DB_CHARSET` | 端口 / 字符集 | `3306` / `utf8mb4` | 一般不用动 |
| `JWT_SECRET` | 登录"签名钥匙"（HS256） | 占位串 | **必须改**：填一段随机英文+数字（越长越安全），本机开发随便填 |
| `DEFAULT_LANG` | 默认语言 | `zh-cn` | 一般不用动 |
| `CORS_ALLOWED_ORIGINS` | 允许跨站访问的来源（逗号分隔） | `http://127.0.0.1,http://localhost` | 前端跨端口联调 / 内网其他机器访问时添加 |
| `TEST_DB_USER` / `TEST_DB_PASS` | 测试库账号 / 密码（跑后端测试需要） | 占位值 | 跑 `phpunit` 时配置（或改用同名系统环境变量） |
| `TRAFFIC_DB_HOST` / `NAME` / `USER` / `PASS` / `PORT` | 流量审计库连接（12 个月前的流量表迁移至此） | `127.0.0.1` / `starwill_traffic_archive` | 库已由 `install.sql` 一键创建，填连接即启用迁移；不配置则迁移自动跳过 |
| `CHAT_DB_HOST` / `NAME` / `USER` / `PASS` / `PORT` | 聊天归档库连接（12 个月前的聊天分表迁移至此） | `127.0.0.1` / `starwill_chat_archive` | 库已由 `install.sql` 一键创建，填连接即启用迁移；不配置则迁移自动跳过 |

> 💡 改完 `.env` 后**无需重启**（ThinkPHP 每次请求读取）；若修改后仍生效旧值，清一次浏览器缓存 / 确认保存的是 `.env` 而非 `.example.env`。

## 测试

- **CI 自动测试（可选）**：仓库内置 Gitea Actions 工作流 `.gitea/workflows/test.yml`，推送后自动运行 PHPUnit（MariaDB 服务 + PHP 8.2）；内网 Gitea 无互联网的部署参考与 Secrets 配置见 `.gitea/README.md`。内网 Windows 服务器如不想用 runner，可用免 runner **门禁部署**方案：将项目根的 `gitea_webhook/` 目录**复制到 Web 根目录、与项目同级**（如 `htdocs\gitea_webhook`），推送后先在测试目录跑后端 + 前端测试，全部通过才更新生产目录（坏代码不会上线），见 `docs/内网快速部署指南.md` 第六章。
- **前端测试页**（QUnit）：浏览器打开 `http://127.0.0.1/starwill_base/view/js/starwill/__tests__/test-runner.html`，全部通过会显示绿色/`ALL-PASS`。测试为**离线 mock 模式**（fetch/WebSocket 已桩化，无需登录、不请求真实接口）。
- **后端测试**（PHPUnit）：`cd tp8 && php vendor/bin/phpunit`，分 Unit / Model / Integration 三组。测试连独立的 `starwill_base_test` 库（**库与表已由 `install.sql` 一键创建**——导入一次即可，重复导入幂等）。测试连接凭据由 `TEST_DB_USER`/`TEST_DB_PASS` 提供（**必需，无内置默认账号**）——**优先读取系统环境变量（CI 直接注入）**，未设置时读取 `tp8/.env` 配置（模板已含示例）。请自行创建测试账号并授权 `starwill_base_test` 库（如 `CREATE USER 'test_user'@'localhost' IDENTIFIED BY '你的密码'; GRANT ALL ON starwill_base_test.* TO 'test_user'@'localhost';`）。

## 部署与运维

**`.env` 配置文件**：`.env` 不入库，**服务器部署目录首次部署前必须创建 `tp8/.env`**。有图形界面的服务器**推荐直接访问站点，用 Web 安装向导**（浏览器内引导建库 + 生成随机 JWT + 写 `.env`）；无图形界面（纯命令行服务器）可手动复制 `tp8/.example.env` 为 `.env` 后填写 `DB_*`、`JWT_SECRET`（跑测试再配 `TEST_DB_*`）。若使用 `gitea_webhook` 门禁部署，测试会自动复用该 `.env`——未配置将导致测试失败并拦截部署。

**Web 服务器**：Web 根指向 `tp8/public/`，配置 ThinkPHP 伪静态重写（Apache RewriteBase / Nginx location 指向 index.php）。前端缓存等价配置（Nginx 替代 `view/.htaccess`，与 Apache 规则保持一致——全部 `no-cache` 协商缓存，普通刷新即生效）：

```nginx
location ~* \.html$  { add_header Cache-Control "no-cache, must-revalidate"; }
location ~* \.(js|css)$ { add_header Cache-Control "no-cache"; }
location ~* \.(png|jpg|jpeg|gif|webp|svg|ico|woff2?)$ { add_header Cache-Control "no-cache"; }
```

任意静态托管（OSS/CDN）也适用：只需保证 JS/CSS/图片/SVG 响应带 `no-cache` 头即可，前端无需后端配合。

**聊天服务（Workerman）**：`php think worker:server` 需**常驻运行**（端口 9512 起自动递增，`tp8/app/http/Worker.php`，端口被占用自动 +1，实际端口可通过 `GET /api/v1/ws/port` 查询）。服务器部署建议用进程守护工具（NSSM / supervisor）保活；纯静态托管不涉及。

**流量审计库（可选但推荐）**：部署时创建 `starwill_traffic_archive` 库并在 `.env` 配置 `TRAFFIC_DB_*`，12 个月前的流量聚合表将自动迁移至此（备审计）；未配置则迁移跳过（数据保留在主库）。

**聊天归档库（可选但推荐）**：部署时创建 `starwill_chat_archive` 库并在 `.env` 配置 `CHAT_DB_*`，12 个月前的聊天分表将自动迁移至此（主库保持近 12 个月，历史查询跨库读取并提示耗时更长）；未配置则迁移跳过（数据保留在主库）。

**更改项目名称**：顶层项目目录名可任意改名（运行时自动推导，**无需改业务代码**），但 `tp8/`、`view/` 两个子目录名不可改。步骤：改名 → 调整 Web 服务器伪静态中旧目录名 → 清理浏览器缓存 → 验证登录/验证码/OAuth 正常。注意：数据库库名是 `starwill_base` 由 `install.sql` 创建，与目录名无关；第三方客户端若把 redirect_uri 写死旧地址需同步更新。

## 安全说明

- **私钥红线**：`tp8/config/oauth2-keys/` 下 RSA 私钥、所有 `*.pem` / `*.key` 均 gitignore，绝不入库
- **环境配置**：`tp8/.env`（含数据库密码/JWT 密钥）gitignore，仅保留 `.example.env` 模板；全量库 `starwill_base.sql`（含测试数据）勿提交
- **二进制文件**默认 gitignore（验证码字体等运行必需文件按例外入库）
- **暴力破解防护**：登录图形验证码一次性 + 按 IP 连续失败 5 次锁定 15 分钟（HTTP 429）
- **上传防护**：`uploads/.htaccess` 禁止脚本执行与目录浏览；聊天附件扩展名白名单 + 图片真实性校验 + 尺寸边界（单边 ≤8192px / 像素 ≤5000 万 / 宽高比 ≤50:1，`ImageUpload` 验证器三处复用）+ 随机文件名；站点 Logo 禁 svg（防脚本注入）
- **聊天文件地址**：服务端严格正则校验 `/uploads/chat/YYYY/MM/随机文件名`（防属性注入与路径穿越）
