<p align="center">
  <img src="./assets/readme/hero.svg" width="100%" alt="MailHub 多邮箱聚合书房客户端：左侧展示项目定位与核心技术栈，右侧展示四栏 2.5D 立体书籍邮箱界面结构">
</p>

<p align="center">
  <a href="https://github.com/A-510/MailHub/releases"><img src="https://img.shields.io/badge/Release-MailHubLauncher.exe-E7749B?style=flat-square" alt="下载 Windows 启动器"></a>
  <a href="https://github.com/A-510/MailHub/issues"><img src="https://img.shields.io/badge/Issues-Bug%20%7C%20Feature%20%7C%20Q%26A-F08DB8?style=flat-square" alt="GitHub Issues 模板反馈"></a>
  <img src="https://img.shields.io/badge/Frontend-Vue%203%20%2B%20TypeScript-8C6BE8?style=flat-square" alt="Vue 3 与 TypeScript">
  <img src="https://img.shields.io/badge/Backend-FastAPI%20%2B%20SQLite%20FTS5-2E8B57?style=flat-square" alt="FastAPI 与 SQLite FTS5">
  <img src="https://img.shields.io/badge/Security-Fernet%20%2B%20OAuth2%20PKCE-6E4FD4?style=flat-square" alt="Fernet 本地加密与 OAuth2 PKCE">
</p>

---

**MailHub** 是一款**本地优先（Local-First）**的多邮箱聚合桌面客户端。它将日常多账号邮件收发重新组织为“书桌上的 2.5D 立体书籍手账”——左侧书签栏管理文件夹，翻开书页左栏浏览列表、右栏阅读信笺与内联回复，最右侧随时勾选合并多个真实邮箱或单箱翻页切换。

所有邮件缓存、全文索引与加密凭据均保存在本机 `data/` 目录中，**不经过任何第三方云端中转服务器**。

## 目录

- [核心特性](#核心特性)
- [系统架构与本地隐私边界](#系统架构与本地隐私边界)
- [快速开始](#快速开始)
- [支持的邮箱渠道与 OAuth2 配置](#支持的邮箱渠道与-oauth2-配置)
- [隐私与安全设计](#隐私与安全设计)
- [键盘快捷键](#键盘快捷键)
- [目录结构](#目录结构)
- [无图降级与自定义视觉扩展](#无图降级与自定义视觉扩展)
- [常见问题](#常见问题)
- [问题反馈与参与贡献](#问题反馈与参与贡献)
- [开发与测试](#开发与测试)
- [环境变量说明（可选）](#环境变量说明可选)

---

## 核心特性

- **2.5D 四栏书籍手账交互**：左侧书签面板（8 大文件夹）、书本左页（邮件列表与分页）、书脊中缝与书本右页（信纸阅读、附件下载与内联回复）、右侧磨砂「我的邮箱」渠道面板。
- **明暗双主题与物理动效**：内置 **Sakura Daylight（樱花白昼）** 与 **Starlight Study（暗黑星夜）** 双主题（支持跟随系统与 View Transitions 圆扩散切换），结合 `motion-v` 实现 3D 翻页、共享滑移指示器及三档动效强度（`full` / `gentle` / `off`）与 `prefers-reduced-motion` 无障碍降级。
- **多邮箱聚合与单箱切换**：支持复选框动态勾选多个邮箱汇入「全部聚合邮箱」，也可点击任意单箱以 3D 翻页切换独立视角；支持自定义渠道排序与独立发信签名。
- **协议级兼容与智能同步**：
  - 按 **RFC 6154 Special-Use Flags** 自动映射收件箱、已发送、草稿、归档、垃圾邮件与回收站，并基于 UID 做增量去重同步；
  - 自动为网易 **163 / 126 / yeah.net** 发送 **RFC 2971 IMAP ID** 客户端识别指令，避免安全拦截；
  - SMTP 发信支持 **465 (SSL) → 587 (STARTTLS)** 自动回退、非 ASCII 主机名自动转码安全 `local_hostname` 以及延迟撤销发送（默认 5 秒可调）。
- **FTS5 秒级全文检索与智能分类**：基于 SQLite `emails_fts` 虚拟表实时索引邮件主题、发件人、摘要与正文；支持自定义分类规则（发件人/主题匹配至工作、学习、社交、订阅）。
- **开箱即用演示沙盒**：首次启动自动载入 5 个示例账号与精选测试邮件；随时可在「设置中心」一键重置或清空演示数据，不影响已绑定的真实邮箱。
- **精准排障与脱敏诊断**：内置「设置中心 → 关于与诊断」面板，支持查看版本与运行环境、生成诊断 `Event ID`、一键复制脱敏 Markdown 诊断报告或导出 `.zip` 诊断包（自动遮罩邮箱前缀、用户路径、主机名与凭据），助力快速定位与修复 Issue。

---

## 系统架构与本地隐私边界

<p align="center">
  <img src="./assets/readme/architecture.svg" width="100%" alt="MailHub 系统架构图：包含 PyQt6 桌面启动器、Vue 3 前端、FastAPI 分层后端与本地加密数据隔离区">
</p>

后端严格遵循 `api → service → repository → schema / model` 分层架构，所有运行态数据库、主密钥、附件缓存与运行日志均被隔离在本地 `data/` 目录下并由 `.gitignore` 强制排除。

---

## 快速开始

<p align="center">
  <img src="./assets/readme/workflow.svg" width="100%" alt="MailHub 四步快速上手流程：下载启动器、环境自检拉起、接入真实邮箱、书房聚合收发">
</p>

### 方式一：使用 Windows 一体化桌面启动器（推荐）

`MailHubLauncher.exe` 基于 PyQt6 构建，已打包至 [GitHub Releases](https://github.com/A-510/MailHub/releases)（未直接放入源码仓库以保持仓库轻量化）。

1. 克隆或下载本仓库源码：
   ```bash
   git clone https://github.com/A-510/MailHub.git
   cd MailHub
   ```
2. 前往 [**Releases 页面**](https://github.com/A-510/MailHub/releases) 下载最新版本的 **`MailHubLauncher.exe`**，将其放到项目根目录 `MailHub/` 下（与 `backend/`、`frontend/` 同级）。
3. **前置环境**：电脑需安装 **Node.js（含 npm）**（若源码未预先编译 `frontend/dist/`，启动器会自动执行 `npm install && npm run build`）；Python 3.10+ 若缺失，启动器会尝试通过 `winget` 自动安装。
4. 双击 **`MailHubLauncher.exe`**：
   - 启动器会自动检测并创建 `backend/.venv`、补全 `backend/requirements.txt` 依赖（默认源超时时自动切换清华 PyPI 镜像源）、检查或构建 `frontend/dist`；
   - 自动拉起 `127.0.0.1:8765` 的 FastAPI 服务并打开系统默认浏览器；
   - **守护机制**：启动器通过 Windows Job Object 与后端服务进程树强绑定。服务运行期间请保持启动器在线，点击右上角关闭按钮时可选择**「最小化到系统托盘」**静默守护，直接退出则会干净终止后台服务避免端口残留。

### 方式二：命令行 / 开发者源码运行

#### 1. 启动后端服务

```bash
cd backend
python -m venv .venv
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8765 --reload
```

#### 2. 构建或开发运行前端

```bash
cd frontend
npm install

# 生产构建（构建后可直接由 FastAPI 单进程在 8765 端口托管）：
npm run build

# 或者启动 Vite 开发服务器（http://127.0.0.1:5173，已配置 /api 代理至 8765）：
npm run dev
```

#### 3. 使用轻量回退启动脚本

若已准备好 `backend/.venv` 与 `frontend/dist`，也可以直接运行根目录的 `python launcher.py` 或双击 `启动MailHub.bat`（优先调用 `MailHubLauncher.exe`，否则回退 `launcher.py` 并以 Edge/Chrome `--app` 独立窗口打开）。

---

## 支持的邮箱渠道与 OAuth2 配置

在 MailHub 右侧栏点击 **`+`** 即可打开「添加邮箱」面板，输入邮箱地址后系统会自动识别服务商并填充推荐协议参数：

| 邮箱渠道 | IMAP 服务器 | SMTP 服务器 | 推荐认证方式 | 协议兼容特性 |
| :--- | :--- | :--- | :--- | :--- |
| **QQ / Foxmail** | `imap.qq.com:993` (SSL) | `smtp.qq.com:465` (SSL) | 16 位客户端授权码 | 自动剔除授权码空格 |
| **网易 163 / yeah.net** | `imap.163.com:993` (SSL) | `smtp.163.com:465` (SSL) | 客户端授权密码 | 自动发送 RFC 2971 IMAP ID；独立识别 `yeah.net` 主机 |
| **网易 126** | `imap.126.com:993` (SSL) | `smtp.126.com:465` (SSL) | 客户端授权密码 | 自动发送 RFC 2971 IMAP ID |
| **Gmail** | `imap.gmail.com:993` (SSL) | `smtp.gmail.com:587` (STARTTLS) | 浏览器 OAuth2 PKCE / 应用专用密码 | 支持自动刷新令牌与 XOAUTH2 |
| **Outlook / Microsoft 365** | `outlook.office365.com:993` (SSL) | `smtp.office365.com:587` (STARTTLS) | 浏览器 OAuth2 PKCE | 适配微软停用基础密码登录策略 |
| **iCloud** | `imap.mail.me.com:993` (SSL) | `smtp.mail.me.com:587` (STARTTLS) | Apple ID App 专用密码 | — |
| **学校 / 教育邮箱** | 手动填写（默认 `993` SSL） | 手动填写（默认 `465` SSL） | 校园邮局密码 / 授权码 | 自动匹配 `.edu.cn` / `.edu` |
| **企业 / 自定义邮局** | 自定义主机与端口 | 自定义主机与端口 | 密码 / 授权码 | 支持自定义 SSL / STARTTLS |

### Gmail / Outlook 浏览器 OAuth2 PKCE 配置说明

MailHub 采用 **OAuth2 Authorization Code + PKCE (S256)** 与本地回环回调（无需将客户端密钥硬编码在源码中）：

1. 在 Google Cloud Console 或 Microsoft Entra ID 注册桌面 / Web 应用，将授权回调地址（Redirect URI）设置为：
   ```text
   http://127.0.0.1:8765/api/v1/oauth/callback
   ```
2. 打开 MailHub 右上角 **设置中心 → 邮箱渠道 → OAuth2 客户端配置**，填入你自己的 `Client ID`（Google 桌面/Web 客户端按需填写 `Client Secret`）。
3. 返回添加邮箱页点击**「跳转浏览器 OAuth2 登录」**，授权完成后令牌将加密写入本机 `data/mailhub.db`。

> 📘 **完整配置手册**：各服务商授权码开启入口、Google 测试用户配置、Microsoft Entra 权限清单及错误码对照，请参阅 [**邮箱渠道与 OAuth2 配置指南**](docs/guide/email-providers-and-oauth2.md)。

---

## 隐私与安全设计

- **对称加密落盘**：邮箱授权码、应用专用密码与 OAuth2 `access_token` / `refresh_token` 均使用 `cryptography.fernet.Fernet`（AES-128-CBC + HMAC-SHA256）加密后写入 SQLite；主密钥自动生成于 `data/.secret.key`（也可通过环境变量 `MAILHUB_SECRET_KEY` 覆盖）。
- **响应模型最小暴露**：后端返回给前端的 `AccountOut` 数据模型严格剔除所有密文字段与密钥。
- **HTML 正文与 XSS 防护**：前端使用 `DOMPurify` 对所有邮件 HTML 正文进行严格消毒（禁用 `<script>`、`<iframe>`、`<object>`、`<embed>`、`<form>`、`<style>`、内联事件属性及非安全位图 `data:` URI），外部链接统一附加 `rel="noopener noreferrer"`。
- **反追踪拦截**：在「设置中心」开启**拦截外链图片**后，自动过滤 `<= 2×2 px` 的隐形追踪像素并将远程图片替换为安全占位提示；正常加载时亦附加 `referrerpolicy="no-referrer"`。
- **路径穿越防护**：附件下载、自定义立绘读取及前端静态资源托管均包含路径边界校验。

---

## 键盘快捷键

在主阅读界面（未打开弹窗或输入框时）可使用以下快捷键：

| 快捷键 | 功能说明 |
| :--- | :--- |
| `C` | 打开「写邮件」弹窗 |
| `J` / `↓` | 选中列表下一封邮件 |
| `K` / `↑` | 选中列表上一封邮件 |
| `S` | 切换当前邮件星标状态 |

---

## 目录结构

```text
MailHub/
├── .github/ISSUE_TEMPLATE/        # GitHub Issue 模板（Bug 反馈 / 新功能支持 / 使用问题咨询）
├── assets/readme/                 # README 纯矢量 SVG 图示（无位图依赖）
├── docs/guide/                    # 邮箱渠道与 OAuth2 PKCE 详细配置与排障指南
├── backend/
│   ├── app/
│   │   ├── api/                   # FastAPI 路由层（accounts / emails / oauth / settings_rules）
│   │   ├── core/                  # 全局配置（pydantic-settings）、SQLite WAL & FTS5、文件轮转日志
│   │   ├── model/                 # SQLAlchemy 2.0 ORM 模型（Account / Email / Attachment 等）
│   │   ├── repository/            # 数据库访问层（含 FTS5 检索与分页计数）
│   │   ├── schema/                # Pydantic v2 请求与响应校验模型
│   │   └── service/               # 业务逻辑（IMAP/SMTP、OAuth2 PKCE、Fernet 加密、脱敏诊断导出等）
│   ├── tests/                     # 后端集成、协议与脱敏诊断测试套件
│   └── requirements.txt
├── frontend/
│   ├── public/vendor/             # Live2D Cubism Core 运行时（仅作用于本地可选模型加载）
│   ├── scripts/                   # 本地素材切图工具脚本
│   ├── src/
│   │   ├── api/                   # 前端 HTTP 请求封装
│   │   ├── components/            # 书房四栏 UI 组件、设置中心（含关于与诊断）、向导与可选立绘槽位
│   │   ├── composables/           # 主题切换、3D 动效、HTML 安全清洗、向导定位逻辑
│   │   ├── stores/                # Pinia 全局状态与撤销发送队列
│   │   ├── styles/                # Sakura / Starlight 色彩令牌与 3D 书页样式
│   │   ├── types/                 # TypeScript 领域类型定义
│   │   └── utils/                 # 可选静态资源安全加载器（无图环境优雅降级）
│   ├── index.html
│   ├── package.json
│   └── vite.config.ts
├── launcher_app/
│   ├── main.py                    # PyQt6 无边框桌面启动器主程序与托盘守护
│   ├── service_manager.py         # 依赖自检、虚拟环境构建与 Windows Job Object 进程管理
│   ├── shinku_lines.py            # 启动器交互文案库
│   ├── ui_widgets.py              # 自定义标题栏、羊皮纸终端日志与防误关弹窗
│   ├── MailHubLauncher.spec       # PyInstaller 单文件打包配置
│   ├── build_exe.ps1              # 一键构建脚本
│   └── tests/                     # 启动器核心逻辑单元测试
├── CONTRIBUTING.md                # Issue 提交规范与代码贡献指南
├── launcher.py                    # 命令行轻量启动回退入口
├── 启动MailHub.bat                # Windows 批处理启动脚本
├── .gitignore                     # 排除运行时数据、密钥、构建缓存、可执行包、参考草稿与原始素材
└── README.md
```

---

## 无图降级与自定义视觉扩展

为保持开源仓库体积轻量并避免附带未授权的第三方插画、角色立绘与模型资产，本仓库**未包含**背景壁纸、装饰立绘、Live2D 模型及启动器切图资源。

- **开箱可编译与运行**：前端已内置优雅降级机制（`frontend/src/utils/optionalAssets.ts` 与 `AmbientBackground.vue`）。直接克隆仓库执行 `npm run build` 可无错通过；无外部图片时会自动呈现纯 CSS 绘制的樱花白昼 / 暗黑星夜渐变书房背景，且不会出现破图图标。
- **在界面内自定义角色立绘**：运行应用后，前往右上角 **设置中心 → 外观与主题**，即可上传你喜欢的 `PNG / WEBP / JPG` 图片（8 MB 以内）作为书房左下角与书背右侧的自定义立绘，并实时调节透明度。
- **可选扩展桌面壁纸 / Live2D**：若需本地替换完整桌面壁纸，可将 `bg-light.png`、`bg-dark.png` 放入 `frontend/src/assets/` 后重新构建前端；若在项目根目录放置兼容的 Cubism 4 模型至对应 `/live2d/` 路径，右下角看板娘画布会自动激活，缺失时则静默隐藏。

---

## 常见问题

<details>
<summary><strong>1. QQ / 163 / 126 / Gmail 使用网页登录密码一直提示认证失败？</strong></summary>

这些服务商通常不允许第三方桌面客户端直接使用邮箱网页登录密码：
- **QQ / Foxmail**：需在网页版 **设置 → 账户** 开启 IMAP/SMTP 后生成 **16 位授权码**；
- **网易 163 / 126 / yeah.net**：需在网页版 **设置 → POP3/SMTP/IMAP** 开启服务并创建 **客户端授权密码**（MailHub 会自动发送 RFC 2971 IMAP ID 避免 `Unsafe Login` 拦截）；
- **Gmail**：需开启 Google 账号两步验证后生成 **16 位应用专用密码**（带空格直接粘贴即可，后端会自动去空格），或改用浏览器 OAuth2 登录。

详细步骤与常见报错对照见 [**邮箱渠道与 OAuth2 配置指南**](docs/guide/email-providers-and-oauth2.md)。

</details>

<details>
<summary><strong>2. Microsoft Outlook / Hotmail 为什么不能填密码直接登录？</strong></summary>

微软已针对个人 Outlook / Hotmail 账户全面停用基础密码登录（Basic Auth）。请在添加邮箱时切换到右上角的 **「跳转浏览器登录」**，在设置中心配置好自己的 `Microsoft Entra Client ID`（回调地址填写 `http://127.0.0.1:8765/api/v1/oauth/callback`）后通过 OAuth2 PKCE 授权接入。

</details>

<details>
<summary><strong>3. 发信或测试连接时提示 TLS/SSL 握手中断（如 465 端口）或超时怎么办？</strong></summary>

本机代理工具或校园网/企业防火墙有时会拦截 SMTPS `465` 端口。MailHub 内置自动回退策略：当 `465 (SSL)` 握手失败且非密码错误时，会自动尝试 `587 (STARTTLS)`（网易 `163/126/yeah.net` 会额外尝试 `994` SSL）。你也可以在添加账号时点击 **「展开自定义 IMAP / SMTP 服务器参数」** 手动切换端口与 SSL 开关。

</details>

<details>
<summary><strong>4. 桌面启动器提示端口 8765 被占用或无法自动构建前端？</strong></summary>

- **端口冲突**：说明本机已有其他服务或上次异常残留的进程占用了 `8765`，可关闭占用进程，或通过环境变量 `MAILHUB_PORT` 指定其他端口；
- **前端自动构建失败**：当仓库中尚未生成 `frontend/dist/` 时，启动器会调用本机 `npm` 自动执行 `npm install && npm run build`，请确保系统已安装 Node.js（含 npm）并可在终端运行 `npm --version`；
- **查看完整启动日志**：启动器运行日志保存在本机 `data/launcher.log`，后端运行日志保存在 `data/backend.log`。

</details>

<details>
<summary><strong>5. 首次启动为什么自带 5 个示例邮箱？清理演示数据会影响我自己的邮箱吗？</strong></summary>

为了让你克隆即体验四栏书籍手账、搜索、分类规则与附件下载，MailHub 首次检测到空库时会自动注入 5 个演示账号。所有演示账号均带有 `is_demo` 标记，前往 **设置中心 → 隐私与数据 → 清空演示邮箱数据** 只会清理演示数据，**不会删除你绑定的真实邮箱**；随时也可以点击 **重新生成演示数据** 恢复体验环境。

</details>

<details>
<summary><strong>6. 为什么画面里没有显示背景壁纸、人物立绘或 Live2D 看板娘？</strong></summary>

本开源仓库为了保持体积轻量化与版权合规，默认不附带商业插画与 Live2D 模型。缺少外部资源时前端会自动降级为纯 CSS 书房渐变，不影响任何收发功能；你可在 **设置中心 → 外观与氛围** 中直接上传自己的 `PNG / WEBP / JPG` 立绘图片。

</details>

<details>
<summary><strong>7. 遇到 Bug 时如何快速提交精准、安全的诊断信息？</strong></summary>

请打开右上角 **设置中心 → 关于与诊断**：
1. 点击 **「刷新快照」** 生成本次诊断 `Event ID`；
2. 点击 **「复制脱敏诊断报告 (Markdown)」** 或 **「导出脱敏诊断包 (.zip)」**；
3. 展开预览框确认其中已自动遮罩邮箱前缀、本地用户路径、主机名与凭据（绝不包含数据库与邮件正文），然后前往 [**Issues 页面**](https://github.com/A-510/MailHub/issues/new/choose) 选择 **Bug 反馈** 模板提交。

</details>

---

## 问题反馈与参与贡献

为了让维护者能够快速复现问题并给出精准修复，本仓库已配置标准 GitHub Issue 模板与配套说明文档：

| 入口 / 文档 | 适用场景 | 链接 |
| :--- | :--- | :--- |
| **Bug 反馈 (`[BUG]`)** | 启动器报错、界面异常、收发同步失败或加密/搜索缺陷 | [提交 Bug 反馈](https://github.com/A-510/MailHub/issues/new?template=bug_report.md) |
| **新功能支持 (`[功能]`)** | 期望新增协议兼容、交互功能、快捷键或设置选项 | [提交功能建议](https://github.com/A-510/MailHub/issues/new?template=feature_request.md) |
| **使用问题咨询 (`[问题]`)** | 授权码获取、OAuth2 回调设置、自建邮局或环境配置疑问 | [提交使用咨询](https://github.com/A-510/MailHub/issues/new?template=question.md) |
| **邮箱配置深度指南** | 各渠道授权步骤、OAuth2 控制台设置与常见错误排查 | [docs/guide/email-providers-and-oauth2.md](docs/guide/email-providers-and-oauth2.md) |
| **贡献与协作规范** | 提交 Issue 前自检、脱敏诊断流程与 PR 开发规范 | [CONTRIBUTING.md](CONTRIBUTING.md) |

> 🔐 **提交 Issue 前请先脱敏**：优先使用客户端 **「设置中心 → 关于与诊断」** 生成的脱敏 Markdown 报告或 `.zip` 诊断包；分享截图与终端日志前，请务必隐藏个人完整邮箱、授权码、`Client Secret` 与 `data/.secret.key`。

---

## 开发与测试

```bash
# 1. 运行后端全量测试（包含 API、SQLite FTS5、加密存储、IMAP/SMTP 兼容、OAuth2 PKCE 与脱敏诊断导出）
cd backend
.\.venv\Scripts\python.exe -m pytest tests/test_mailhub.py -v

# 2. 运行启动器核心单元测试（路径解析、依赖检测、命令构造与安全只读统计）
cd ..
.\backend\.venv\Scripts\python.exe -m pytest launcher_app/tests/test_launcher_core.py -v

# 3. 前端类型检查与生产构建校验
cd frontend
npm run build
```

---

## 环境变量说明（可选）

后端支持通过 `.env` 或系统环境变量覆盖默认运行配置（前缀为 `MAILHUB_`）：

| 变量名 | 默认值 | 说明 |
| :--- | :--- | :--- |
| `MAILHUB_HOST` | `127.0.0.1` | 后端监听地址（若修改，OAuth2 回调地址需同步调整） |
| `MAILHUB_PORT` | `8765` | 后端监听端口 |
| `MAILHUB_SECRET_KEY` | `None` | 可选手动指定 Fernet 密钥（未指定时自动读取或生成 `data/.secret.key`） |
