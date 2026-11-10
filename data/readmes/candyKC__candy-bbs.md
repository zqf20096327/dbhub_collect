<div align="center">

# 🍬 Candy BBS

**一款现代化、高颜值、可拓展的开源社区论坛系统**

_基于 ThinkPHP 6 · Vue 3 · Vite · Element Plus 构建，前后端分离、开箱即用_

[![PHP](https://img.shields.io/badge/PHP-8.0%2B-777BB4?logo=php&logoColor=white)](https://www.php.net/)
[![ThinkPHP](https://img.shields.io/badge/ThinkPHP-6.1-1E90FF?logo=laravel&logoColor=white)](https://www.thinkphp.cn/)
[![Vue](https://img.shields.io/badge/Vue-3.5-42B883?logo=vue.js&logoColor=white)](https://vuejs.org/)
[![Vite](https://img.shields.io/badge/Vite-6.x-646CFF?logo=vite&logoColor=white)](https://vitejs.dev/)
[![Element Plus](https://img.shields.io/badge/Element%20Plus-2.10-409EFF?logo=element&logoColor=white)](https://element-plus.org/)
[![MySQL](https://img.shields.io/badge/MySQL-5.7%2B-4479A1?logo=mysql&logoColor=white)](https://www.mysql.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](#-开发协作)

<p>
  <a href="#-项目简介">📖 简介</a> ·
  <a href="#-核心亮点">✨ 亮点</a> ·
  <a href="#-快速开始">🚀 快速开始</a> ·
  <a href="#-项目结构">📁 结构</a> ·
  <a href="#-核心能力">🎯 能力</a> ·
  <a href="#-数据库约定">🗄 数据库</a> ·
  <a href="#-api-与路由约定">🧭 API</a> ·
  <a href="#-部署指南">🚢 部署</a> ·
  <a href="#-常见问题">❓ FAQ</a>
</p>

</div>

---

## 📖 项目简介

**Candy BBS** 是一个「开箱即用、前后端分离」的社区论坛全套解决方案，
覆盖了从 **用户浏览发帖** → **版主/管理员运营** → **系统运维** 的完整业务闭环。

项目由 **三大模块** 组成，均在同一仓库内维护，前后端通过统一 API 层通信：

<table>
  <thead>
    <tr>
      <th align="center">🧩 模块</th>
      <th align="center">📁 目录</th>
      <th align="center">🛠 技术栈</th>
      <th>🎯 定位</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="center"><b>后端 API</b></td>
      <td><code>app/</code> <code>route/</code> <code>public/</code> <code>config/</code></td>
      <td>ThinkPHP 6 · PHP 8.x · MySQL 8</td>
      <td>前后台统一接口层、业务、权限、审核、Feed、上传</td>
    </tr>
    <tr>
      <td align="center"><b>论坛前端</b></td>
      <td><code>论坛前端代码/</code></td>
      <td>Vue 3 · Pinia · Element Plus · wangEditor · Tailwind</td>
      <td>用户浏览、发帖、私信、任务、签到、版主中心</td>
    </tr>
    <tr>
      <td align="center"><b>后台前端</b></td>
      <td><code>后台前端代码/</code></td>
      <td>Vue 3 · Pinia · Element Plus · Tiptap · ECharts</td>
      <td>员工登录、菜单/角色/权限、内容审核、运营配置、系统运维</td>
    </tr>
  </tbody>
</table>

### 📊 项目规模一览

| 维度 | 数量 | 说明 |
| :--- | :---: | :--- |
| 前台 API 控制器 | **23** | `app/controller/api/` 论坛所有对外接口 |
| 后台 API 控制器 | **29** | `app/controller/admin/` 管理端接口 |
| 数据模型（Model） | **49** | 与数据表 1:1 映射 |
| 业务服务（Service） | **20** | 认证、Token、通知、上传、敏感词等 |
| 数据表 | **50** | `ca_` 前缀，`utf8mb4_unicode_ci` |
| 论坛前端页面 | **44** | 覆盖首页、发帖、个人中心、版主 |
| 后台管理页面 | **31** | 内容治理 + 运营 + 系统运维 |
| Feed 订阅入口 | **9+** | RSS / Atom / JSON Feed / OPML |

---

## ✨ 核心亮点

<table>
<tr>
<td width="33%" valign="top">

### 🔐 完善的账户体系
- 账号 / 邮箱验证码登录
- OAuth（GitHub / Gitee 预留）
- 邀请码 · 找回密码
- JWT Token 双端复用
- RBAC 角色-菜单-权限

</td>
<td width="33%" valign="top">

### 💬 丰富的社区互动
- 主题帖 / 问答 / 投票
- 多级回复 · @提及 · 标签
- 点赞 / 收藏 / 关注
- 私信 · 通知 · 浏览历史
- 匿名帖 · 悬赏问答

</td>
<td width="33%" valign="top">

### 🎮 玩法与激励
- 积分 · 经验 · 等级
- 新手任务 · 排行榜
- 每日签到 · 抽奖
- 红包 · 竞拍
- 附件购买 · 打赏

</td>
</tr>
<tr>
<td width="33%" valign="top">

### 🛡 严格的审核治理
- 敏感词库 · 审核队列
- 举报处理 · 回收站
- 批量操作 · 板块申请审批
- 版主中心 · 操作日志

</td>
<td width="33%" valign="top">

### 📢 强大的运营配置
- 仪表盘 · 数据看板
- 板块 / 标签 / 首页模块
- 友情链接 · 站内公告
- RSS · Atom · JSON Feed
- OPML 订阅目录

</td>
<td width="33%" valign="top">

### ⚙ 稳定的系统运维
- 员工 · 部门 · 角色 · 菜单
- 登录日志 · 操作日志
- 数据库备份 · 优化
- 缓存清理 · 维护模式
- 一键安装向导

</td>
</tr>
</table>

### 🏆 相较传统论坛的差异化优势

- **纯前后端分离**：后端只吐 JSON，可无缝替换前端 UI；未来接入小程序 / App 无需重写业务
- **前后台共用一份 Model & Service**：审核、通知、积分等业务逻辑统一，避免双写
- **可视化安装向导**：无需手写 SQL，浏览器点几下即可完成部署
- **模块化首页**：首页布局在后台可视化配置，「轮播 / 板块 / 排行 / 热帖」自由组合
- **RSS 一等公民**：主贴、回复、板块、标签、用户，全部支持订阅
- **可拓展的玩法层**：抽奖 / 红包 / 竞拍 / 悬赏 都是独立 Service，可关可开可加新

---

## 🚀 快速开始

### 1️⃣ 环境要求

| 组件 | 最低版本 | 推荐版本 | 说明 |
| :--- | :---: | :---: | :--- |
| 🐘 **PHP** | 7.4 | **8.2** | 需启用 `pdo_mysql · mbstring · openssl · fileinfo · gd · curl · json` |
| 🐬 **MySQL** | 5.7 | 8.0 | 字符集必须为 `utf8mb4 / utf8mb4_unicode_ci` |
| 🟢 **Node.js** | 18 | 20 LTS | 仅前端打包时需要 |
| 🎼 **Composer** | 2.x | 2.7+ | 后端依赖管理 |
| 🌐 **Web 服务器** | — | Nginx 1.20+ | 站点根目录必须指向 `public/` |
| 📮 **SMTP**（可选） | — | — | 邮件验证码 / 找回密码所需 |

#### 💡 Windows 本机 phpstudy_pro 参考路径

```
PHP        E:\phpstudy_pro\Extensions\php\php8.2.9nts\php.exe
MySQL      E:\phpstudy_pro\Extensions\MySQL8.0.12\bin
Composer   E:\phpstudy_pro\Extensions\composer2.5.8
```

#### 📦 推荐的 PHP 扩展检查命令

```bash
php -m | findstr /I "pdo_mysql mbstring openssl fileinfo gd curl json bcmath"
```

### 2️⃣ 安装启动（三步走）

```bash
# ① 克隆仓库
git clone <your-repo-url> candy_bbs && cd candy_bbs

# ② 安装后端依赖
composer install

# ③ 安装前端依赖（两个前端各装一次）
npm --prefix 论坛前端代码 install
npm --prefix 后台前端代码 install
```

之后**用浏览器访问 `http://<你的域名>/install.php`**，跟随可视化安装向导：

1. **环境检测** — 自动检查 PHP 版本、扩展、目录权限
2. **数据库配置** — 填写数据库连接信息，导入 `schema.sql` + `seed.sql`
3. **超级管理员** — 设置后台首个超管账号
4. **完成** — 生成 `.env` 与 `runtime/install.lock`，浏览器可跳转前台 / 后台

> ⚠️ **安装完成后请立即删除或禁用 `install/`、`public/install.php`、`public/install/`**，
> 否则任何人访问 `/install.php` 都能重装并覆盖你的数据库。

### 3️⃣ 本地开发

```bash
# 启动后端（PHP 内置服务器）
php think run --host 0.0.0.0 --port 8899

# 启动论坛前端  → 默认  http://localhost:5173
npm --prefix 论坛前端代码 run dev

# 启动后台前端  → 默认  http://localhost:5174
npm --prefix 后台前端代码 run dev
```

> Vite 已配置好把 `/api`、`/feed` 代理到后端域名（默认 `http://ca.com`），
> 本地无需处理 CORS。若后端地址不同，改前端 `vite.config.js` 里的 `proxy.target` 即可。

### 4️⃣ 生产打包

```bash
# 前端产物：论坛前端代码/dist
npm --prefix 论坛前端代码 run build

# 前端产物：后台前端代码/dist
npm --prefix 后台前端代码 run build
```

打包完成后：

- 后端：Nginx 站点根目录指向 `public/`
- 论坛前端：把 `论坛前端代码/dist` 上传到 `forum.example.com` 的静态根目录
- 后台前端：把 `后台前端代码/dist` 上传到 `admin.example.com` 的静态根目录

---

## 📁 项目结构

```
candy_bbs/
├── 📂 app/                          # ThinkPHP 应用目录
│   ├── controller/
│   │   ├── api/                     # 🟦 前台 API 控制器（23 个）
│   │   │   ├── ForumAuthController         # 登录 / 注册 / OAuth / 找回密码
│   │   │   ├── ForumHomeController         # 首页 / 侧边栏 / 全站统计
│   │   │   ├── ForumPostController         # 帖子 CRUD + 点赞/收藏/关注/购买
│   │   │   ├── ForumReplyController        # 回复 / 最佳答案
│   │   │   ├── ForumCategoryController     # 板块树 / 板块聚合
│   │   │   ├── ForumTagController          # 标签列表 / 标签聚合
│   │   │   ├── ForumSearchController       # 全站搜索
│   │   │   ├── ForumUserController         # 个人主页 / 资料 / 关注
│   │   │   ├── ForumNotificationController # 通知列表 / 已读
│   │   │   ├── ForumMessageController      # 私信会话 & 单条
│   │   │   ├── ForumCheckinController      # 签到
│   │   │   ├── ForumNewbieTaskController   # 新手任务
│   │   │   ├── ForumRankController         # 排行榜
│   │   │   ├── ForumInviteController       # 邀请码
│   │   │   ├── ForumReportController       # 举报
│   │   │   ├── ForumPollController         # 投票
│   │   │   ├── ForumModeratorController    # 版主中心
│   │   │   ├── ForumFriendLinkController   # 友情链接
│   │   │   ├── ForumCategoryApplyController# 板块申请
│   │   │   ├── ForumFeedController         # RSS/Atom/JSON Feed/OPML
│   │   │   ├── ForumCommonController       # 配置 / 验证码 / 上传 / 公告
│   │   │   ├── ForumUxController           # 关注流 / 热帖 / 相似帖
│   │   │   └── ForumBaseController         # 前台控制器基类
│   │   │
│   │   └── admin/                   # 🟥 后台 API 控制器（29 个）
│   │       ├── IndexController             # 后台首页
│   │       ├── CaptchaController           # 登录验证码
│   │       ├── EmployeeController          # 员工管理
│   │       ├── DepartmentController        # 部门管理
│   │       ├── RoleController              # 角色管理
│   │       ├── MenuController              # 菜单管理
│   │       ├── LoginLogController          # 登录日志
│   │       ├── OperationLogController      # 操作日志
│   │       ├── ConfigController            # 系统配置
│   │       ├── DatabaseController          # 数据库运维
│   │       ├── FileController              # 文件管理
│   │       ├── NoticeController            # 站内公告
│   │       ├── CommonController            # 后台公共接口
│   │       ├── ForumDashboardController    # 论坛仪表盘
│   │       ├── ForumConfigController       # 论坛全局配置
│   │       ├── ForumPageController         # 首页模块化配置
│   │       ├── ForumCategoryController     # 板块管理
│   │       ├── ForumCategoryApplyController# 板块申请审批
│   │       ├── ForumTagController          # 标签管理
│   │       ├── ForumFriendLinkController   # 友情链接管理
│   │       ├── ForumUserManageController   # 论坛用户管理
│   │       ├── ForumUserLevelController    # 等级 / 徽章
│   │       ├── ForumPostManageController   # 帖子管理 / 回收站
│   │       ├── ForumReplyManageController  # 回复管理
│   │       ├── ForumAuditQueueController   # 审核队列
│   │       ├── ForumReportController       # 举报处理
│   │       ├── ForumSensitiveWordController# 敏感词库
│   │       ├── ForumModeratorController    # 版主配置
│   │       └── ForumNewbieTaskController   # 新手任务配置
│   │
│   ├── middleware/                  # CORS · 维护模式
│   ├── model/                       # 数据模型（49 个 · 与数据表 1:1）
│   ├── service/                     # 业务服务（20 个）
│   │   ├── AuthService                     # 账号密码认证
│   │   ├── TokenService · ForumTokenService# JWT / 前后台双 Token
│   │   ├── OauthService                    # OAuth 登录
│   │   ├── MailService                     # SMTP 邮件
│   │   ├── UploadService                   # 文件上传（本地/OSS）
│   │   ├── FileSecurityService             # 文件类型 & 大小校验
│   │   ├── IpLocationService               # IP 归属地
│   │   ├── ForumConfigService              # 论坛动态配置
│   │   ├── ForumSanitizer                  # XSS / HTML 清洗
│   │   ├── ForumSensitiveWordService       # 敏感词过滤
│   │   ├── ForumPublishGuard               # 发帖频率 / 权限守卫
│   │   ├── ForumNotifyService              # 通知分发
│   │   ├── ForumExpService                 # 经验 / 积分变更
│   │   ├── ForumBadgeService               # 徽章判定
│   │   ├── ForumFeedService                # RSS/Atom 生成
│   │   ├── ForumPostFeatureService         # 精华 / 置顶 / 锁贴
│   │   ├── ForumModeratorService           # 版主权限判定
│   │   ├── ForumNewbieTaskService          # 新手任务进度
│   │   └── ForumUserPurgeService           # 用户清算
│   ├── BaseController.php           # 全局控制器基类
│   ├── common.php                   # 全局辅助函数
│   ├── ExceptionHandle.php          # 全局异常处理
│   └── event.php · provider.php     # 事件 / 服务容器
│
├── 📂 route/
│   ├── api.php                      # 前台论坛 API + Feed 路由
│   └── admin.php                    # 后台管理 API 路由
│
├── 📂 config/                       # ThinkPHP 官方配置 + admin_tools 自定义
├── 📂 public/                       # 🌍 Web 入口（站点根目录指向此处）
│   ├── index.php                    # 入口文件
│   ├── install.php                  # 安装向导入口
│   ├── nginx.htaccess               # Nginx 重写规则示例
│   └── storage/                     # 用户上传目录（需可写）
│
├── 📂 install/                      # 🧙 一键安装向导
│   ├── Installer.php                # 安装逻辑
│   ├── env.tpl                      # .env 模板
│   ├── sql/
│   │   ├── schema.sql               # 数据表结构（50 张表）
│   │   └── seed.sql                 # 初始化种子数据
│   └── steps/                       # 分步骤 UI
│
├── 📂 extend/                       # 第三方扩展 / 自定义类库
├── 📂 vendor/                       # Composer 依赖
├── 📂 runtime/                      # 缓存 / 日志 / Session（需可写，不入库）
│
├── 📂 论坛前端代码/                    # Vue 3 论坛前台（44 页面）
├── 📂 后台前端代码/                    # Vue 3 管理后台（31 页面）
│
├── 📄 composer.json                 # 后端依赖清单
├── 📄 think                         # ThinkPHP 命令行入口
├── 📄 部署文档.md                     # 上线部署详细手册
├── 📄 LICENSE                       # MIT License
└── 📄 README.md                     # 本文档
```

---

## 🎯 核心能力

<table>
<tr>
<td width="18%" align="center"><b>🔑 认证</b></td>
<td>账号密码 · 邮箱验证码 · OAuth（GitHub / Gitee 预留） · 邀请码注册 · 找回密码 · JWT Token 双端复用 · Token 自动续期</td>
</tr>
<tr>
<td align="center"><b>💬 内容</b></td>
<td>主题帖（普通 / 问答 / 投票 / 悬赏） · 多级回复 · @提及 · 标签 · 板块 · 精华 / 置顶 / 锁贴 · 匿名帖 · 附件收费</td>
</tr>
<tr>
<td align="center"><b>🤝 互动</b></td>
<td>点赞 · 收藏 · 关注（用户 / 板块 / 标签） · 私信 · 系统通知 · 浏览历史 · 关注流 Feed · 相似帖推荐</td>
</tr>
<tr>
<td align="center"><b>🎲 玩法</b></td>
<td>积分 · 经验 · 等级 · 徽章 · 新手任务 · 每日签到 · 排行榜 · 抽奖 · 红包 · 竞拍 · 附件购买 · 打赏</td>
</tr>
<tr>
<td align="center"><b>🛡 审核</b></td>
<td>敏感词库 · 审核队列（先审后发/先发后审可切换） · 举报处理 · 回收站 · 批量操作 · 板块申请审批 · 版主中心</td>
</tr>
<tr>
<td align="center"><b>📢 运营</b></td>
<td>数据仪表盘（ECharts） · 板块 / 标签管理 · 首页模块化配置 · 页面级 CMS · 友情链接 · 站内公告 · RSS / Atom / JSON Feed / OPML</td>
</tr>
<tr>
<td align="center"><b>⚙ 系统</b></td>
<td>员工 · 部门 · 职级 · 角色 · 菜单 · 功能权限（RBAC） · 登录日志 · 操作日志 · 数据库备份/优化 · 缓存清理 · 维护模式</td>
</tr>
</table>

---

## 🗄 数据库约定

### 基础约定

| 项目 | 约定 |
| :--- | :--- |
| **表前缀** | `ca_` |
| **表数量** | 50 张 |
| **字符集** | `utf8mb4` / `utf8mb4_unicode_ci` |
| **命名风格** | 全部蛇形；`ca_forum_*` = 论坛业务，`ca_employee_*` = 后台员工，其余为通用系统表 |
| **主键** | `id INT AUTO_INCREMENT` |
| **时间字段** | `created_at` / `updated_at`；部分表额外含 `read_at` / `expire_at` / `deleted_at` 等 |
| **软删除** | 部分表采用 `deleted_at IS NULL` 判定 |

### 分组一览

#### 👥 系统与员工（8 张）

`ca_config` · `ca_department` · `ca_employee` · `ca_employee_login_log`
· `ca_employee_operation_log` · `ca_role` · `ca_role_func` · `ca_func`
· `ca_menu` · `ca_notice`（其中 `notice/menu` 视口径可跨组）

#### 📁 文件与附件（2 张）

`ca_file` · `ca_file_group`

#### 💬 论坛核心（6 张）

`ca_forum_user` · `ca_forum_user_oauth` · `ca_forum_post` · `ca_forum_reply`
· `ca_forum_category` · `ca_forum_tag` · `ca_forum_post_tag`

#### 🤝 互动与关注（7 张）

`ca_forum_like` · `ca_forum_favorite` · `ca_forum_follow`
· `ca_forum_view_history` · `ca_forum_message` · `ca_forum_message_thread`
· `ca_forum_notification` · `ca_forum_notification_setting`

#### 🎲 玩法扩展（14 张）

`ca_forum_post_purchase` · `ca_forum_post_attachment` · `ca_forum_post_attachment_purchase`
· `ca_forum_post_auction` · `ca_forum_post_auction_bid`
· `ca_forum_post_lottery` · `ca_forum_post_lottery_condition` · `ca_forum_post_lottery_participant` · `ca_forum_post_lottery_prize`
· `ca_forum_post_red_packet` · `ca_forum_post_red_packet_claim`
· `ca_forum_post_jackpot`
· `ca_forum_poll_option` · `ca_forum_poll_vote`

#### 📢 运营配置（6 张）

`ca_forum_config` · `ca_forum_page` · `ca_forum_page_module`
· `ca_forum_friend_link` · `ca_forum_category_apply` · `ca_forum_category_moderator`

#### 🛡 审核治理（4 张）

`ca_forum_report` · `ca_forum_checkin` · `ca_forum_newbie_task_record`
（敏感词与审核策略存储于 `ca_forum_config`）

> 🌱 初始化数据均从 `install/sql/schema.sql` 与 `install/sql/seed.sql` 导入，
> 安装向导自动执行，无需手工建库。

---

## 🧭 API 与路由约定

### 路径规范

| 类型 | 前缀 | 方法 | 说明 |
| :--- | :--- | :---: | :--- |
| **前台业务** | `/api/forum/front/*` | `POST` | 论坛所有业务接口 |
| **前台鉴权** | `/api/forum/front/auth/*` | `POST` | 登录 / 注册 / me / 刷新 / OAuth |
| **后台业务** | `/api/*`（详见 `route/admin.php`） | `POST` | 管理端接口 |
| **Feed 订阅** | `/feed/*` | `GET` | 供 RSS 客户端使用 |
| **OAuth 回调** | `/oauth/:provider/callback` | `GET` | 第三方登录回跳 |

### 前台接口分组（部分示例）

| 分组 | 接口示例 |
| :--- | :--- |
| **鉴权** | `auth/login` · `auth/register` · `auth/me` · `auth/refresh` · `auth/reset_password` · `auth/oauth_url` |
| **帖子** | `post/list` · `post/detail` · `post/create` · `post/update` · `post/delete` · `post/like` · `post/favorite` · `post/follow` · `post/purchase` |
| **玩法** | `post/lottery_join` · `post/lottery_draw` · `post/red_packet_claim` · `post/auction_bid` · `post/attachment_purchase` · `post/poll_vote` |
| **回复** | `reply/list` · `reply/create` · `reply/delete` · `reply/like` · `reply/best` · `reply/my` |
| **板块** | `category/tree` · `category/detail` · `category/posts` · `category/follow` |
| **标签** | `tag/list` · `tag/hot` · `tag/detail` · `tag/posts` · `tag/follow` |
| **用户** | `user/profile` · `user/posts` · `user/replies` · `user/update_profile` · `user/change_password` |
| **私信** | `message/threads` · `message/messages` · `message/send` |
| **通知** | `notification/list` · `notification/read` |
| **搜索** | `search/index` · `search/suggest` |
| **首页** | `home/index` · `home/sidebar` · `home/stats` |
| **通用** | `common/config` · `common/captcha` · `common/init` · `common/notices` · `common/upload` |

### Feed 订阅入口

| 路径 | 内容 |
| :--- | :--- |
| `/feed/rss.xml` | 全站最新帖子（RSS 2.0） |
| `/feed/atom.xml` | 全站最新帖子（Atom） |
| `/feed/json` | 全站最新帖子（JSON Feed） |
| `/feed/hot.xml` | 热门帖子 |
| `/feed/essence.xml` | 精华帖 |
| `/feed/replies.xml` | 最新回复 |
| `/feed/category/:id.xml` | 单个板块 |
| `/feed/tag/:id.xml` | 单个标签 |
| `/feed/user/:id.xml` | 某用户主贴 |
| `/feed/post/:id/replies.xml` | 某帖子回复流 |
| `/feed/search.xml` | 搜索结果 |
| `/feed/directory.json` | Feed 目录索引 |
| `/feed/opml.xml` | OPML 订阅包 |

### 鉴权机制

- 前台请求带 `Authorization: Bearer <forumToken>`，由 `ForumTokenService` 校验
- 后台请求带 `Authorization: Bearer <adminToken>`，由 `TokenService` 校验
- 权限（登录态 / 版主 / 员工 / RBAC 功能码）由控制器内部校验
- 未鉴权返回 `401`，无权限返回 `403`

---

## 🚢 部署指南

生产部署通常涉及**三个域名**：

| 角色 | 示例域名 | 静态 / 动态 |
| :--- | :--- | :--- |
| 后端 API | `api.example.com` | PHP-FPM |
| 论坛前端 | `forum.example.com` | 静态 dist |
| 后台前端 | `admin.example.com` | 静态 dist |

完整 Nginx 配置、SSL、CORS、前端 `VITE_API_BASE_URL` 修改流程等请见
👉 **[部署文档.md](./部署文档.md)**。

### ✅ 部署自检清单

- [ ] 站点根目录指向 `public/`，**不是**项目根目录
- [ ] `.env` 已生成，`[APP] CORS_ALLOWED_ORIGINS` 填入前端 / 后台的真实域名（用逗号分隔，末尾无 `/`）
- [ ] 前端 `.env.production` 的 `VITE_API_BASE_URL` 已改为真实后端 API 域名
- [ ] `论坛前端代码/dist`、`后台前端代码/dist` 已上传至各自的静态站点根目录
- [ ] `runtime/`、`public/storage/` 属主为 Web 用户（`www-data` / `www`）且**可写**
- [ ] 安装完成后，`install/`、`public/install.php`、`public/install/` 已**删除或禁用**
- [ ] MySQL 数据库编码为 `utf8mb4 / utf8mb4_unicode_ci`
- [ ] 后台首次登录已使用向导中设置的超级管理员账号密码
- [ ] 如需上传附件到 OSS / 又拍 / 七牛，已在「后台 → 系统设置」填入 AK/SK
- [ ] 若开启邮件功能，已在「后台 → 系统设置」配置 SMTP
- [ ] 生产环境 `.env` 里 `APP_DEBUG = false`

### 🔒 安全加固建议

- Nginx 层拒绝对 `runtime/`、`.env`、`.git`、`install/` 的直接访问
- 生产环境务必开启 HTTPS，并把 `SameSite=Lax` 与 `Secure` 用于所有 Cookie
- 后台管理域名 `admin.example.com` 建议加 IP 白名单或独立 CDN
- 数据库账号使用最小权限，禁止 `SUPER / FILE`
- 定期使用后台「数据库备份」下载全量 `.sql`，并异地保存

---

## 🧪 常用运维命令

```bash
# 清理 ThinkPHP 缓存
php think clear

# 查看所有已注册的路由
php think route:list

# 手动运行队列 / 定时（若已启用）
php think schedule:run

# 检查所有 PHP 文件语法
find app route config public -name "*.php" -type f -exec php -l {} \;
```

```powershell
# PowerShell 版本
Get-ChildItem app,route,config,public -Recurse -File -Filter *.php |
  ForEach-Object { php -l $_.FullName }
```

---

## 🤝 开发协作

### 分支约定

- `main`：稳定分支，可随时部署
- `develop`：开发主线
- `feature/<name>`：新功能开发
- `fix/<name>`：Bug 修复
- `hotfix/<name>`：紧急上线补丁

### 提交规范（推荐 Conventional Commits）

```
feat(post):     新增悬赏帖竞拍出价接口
fix(auth):      修复 OAuth 回调 state 未校验导致的登录绕过
refactor(feed): 拆分 RSS 生成逻辑至 ForumFeedService
docs(readme):   更新部署自检清单
chore(deps):    升级 ThinkPHP 至 6.1.5
```

### 代码风格

- **PHP**：遵循 PSR-12，控制器薄、Service 厚，禁止在 Controller 里写 SQL
- **Vue**：`<script setup>` + Composition API，避免 mixin
- **命名**：文件名与类名保持一致，避免自动加载失败
- **注释**：公共 Service / 复杂算法必须写 PHPDoc / JSDoc

### 提交前自检

```bash
# 后端 PHP 语法体检
php -l <改动的文件>

# 前端构建冒烟
npm --prefix 论坛前端代码 run build
npm --prefix 后台前端代码 run build
```

### 新增功能的推荐流程

1. **建表**：在 `install/sql/schema.sql` 追加建表语句 + 种子数据
2. **建 Model**：`app/model/` 下新建，与表 1:1 对应
3. **写 Service**：把业务逻辑封装到 `app/service/`
4. **加 Controller**：`app/controller/api/` 或 `admin/` 下写薄控制器
5. **注册路由**：在 `route/api.php` 或 `route/admin.php` 加一行
6. **前端接入**：`src/api/xxx.js` 加接口，`src/views/` 加页面，`src/router/` 加路由

---

## ❓ 常见问题

#### Q1：前端页面能打开，但接口全 CORS 报错？

检查 `.env` 里 `[APP]` 段的 `CORS_ALLOWED_ORIGINS` 是否包含前端访问用的**完整 Origin**
（含 `https://` 与端口，末尾不带 `/`）。多条用英文逗号分隔。

#### Q2：改了 `.env.production` 后前端依然请求旧域名？

Vite 只在 `npm run build` 时把环境变量烘焙进 `dist`，改完必须**重新 build 并上传**。

#### Q3：站点根路径 302 重定向到 `install.php`？

说明 `.env` 或 `runtime/install.lock` 缺失。要么走完安装向导，
要么把之前备份的 `.env` + `runtime/install.lock` 恢复回来。

#### Q4：安装向导报「PDO 扩展未加载」或「目录不可写」？

- 用 `php -m` 检查缺失的扩展；
- 给 `runtime/`、`public/storage/` 添加 Web 用户写权限：
  ```bash
  chown -R www-data:www-data runtime public/storage
  chmod -R 755 runtime public/storage
  ```

#### Q5：怎么修改后台超级管理员密码？

登录后台 → **系统管理 → 员工管理**，找到自己账户后点「重置密码」。
如果密码丢失且无法登录，可直接在数据库 `ca_employee` 表用
`password_hash('新密码', PASSWORD_DEFAULT)` 生成的字符串覆写 `password` 字段。

#### Q6：上传的图片能显示，但重启后 404 了？

检查 `public/storage/` 是否被误清空；若使用 Docker，`public/storage/` 与 `runtime/`
必须**挂载卷持久化**。生产建议直接上传到 OSS / 又拍 / 七牛。

#### Q7：如何切换「先审后发」和「先发后审」？

登录后台 → **论坛运营 → 论坛配置 → 内容审核策略**。
支持按板块级别覆盖全局策略。

#### Q8：RSS / Atom 能同时提供吗？我要给不同客户端不同格式。

支持。全站最新帖同时提供：
- RSS 2.0：`/feed/rss.xml`
- Atom：`/feed/atom.xml`
- JSON Feed：`/feed/json`

板块、标签、用户、单帖回复流均有对应入口，详见 [API 与路由约定](#-api-与路由约定)。

#### Q9：可以只跑后端 + 论坛前端，不部署后台前端吗？

可以。后台前端是**独立静态站点**，可选部署。
如果不部署，需要通过数据库或后端脚手架命令直接维护配置。
建议至少内网部署一份，用于内容审核。

#### Q10：能不能改表前缀？

可以，但**必须在安装前**修改：编辑 `install/env.tpl` 里的 `DB_PREFIX`
以及 `install/sql/schema.sql` 中所有 `ca_` 前缀。不建议安装后再改。

---

## 🗺 Roadmap

- [ ] 移动端 App（Uni-app 或 React Native）
- [ ] 支持多语言 i18n
- [ ] Docker Compose 一键部署
- [ ] AI 辅助内容审核（接入 OpenAI / 通义千问）
- [ ] 帖子全文检索接入 Meilisearch / Elasticsearch
- [ ] 消息队列化（RabbitMQ / Redis）
- [ ] WebSocket 实时通知与私信
- [ ] 帖子 Markdown 双写与导出

---

## 📜 许可协议

本项目基于 [**MIT License**](./LICENSE) 开源，你可以自由地：

- ✅ 用于商业项目、二次开发、衍生作品
- ✅ 复制、修改、发布、再授权
- ✅ 私有部署与销售

**唯一要求**：请在你分发的副本中保留 [LICENSE](./LICENSE) 文件中的原始版权声明。

---

## 🙏 致谢

Candy BBS 站在众多优秀开源项目的肩膀上，特别感谢：

- [ThinkPHP](https://www.thinkphp.cn/) — 简单快速的 PHP 框架
- [Vue.js](https://vuejs.org/) — 渐进式 JavaScript 框架
- [Vite](https://vitejs.dev/) — 下一代前端构建工具
- [Element Plus](https://element-plus.org/) — 基于 Vue 3 的组件库
- [Pinia](https://pinia.vuejs.org/) — Vue 官方推荐的状态管理
- [wangEditor](https://www.wangeditor.com/) · [Tiptap](https://tiptap.dev/) — 富文本编辑器
- [ECharts](https://echarts.apache.org/) — 数据可视化
- [Tailwind CSS](https://tailwindcss.com/) — 原子化 CSS 框架

---

<div align="center">

_如果 Candy BBS 帮到了你，欢迎 ⭐ Star 或告诉我们你的使用场景_

**Made with ❤ by Candy BBS Team · Happy Coding! 🍬**

</div>