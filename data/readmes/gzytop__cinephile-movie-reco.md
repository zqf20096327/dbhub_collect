# Cinephile · Spring Boot 电影推荐系统

一个包含电影浏览、评分收藏、可解释推荐与后台管理的电影推荐站点。前后端分离，推荐结果附带匹配标签与自然语言理由。

> 完整需求见 [`PRD.md`](./PRD.md)（Draft v0.2）

## 项目截图

### 用户前台

**电影列表** — 12 部影片、按评分/年份/热度切换、标签芯片一键筛选、搜索框实时过滤。

![电影列表](docs/screenshots/01-movie-list.png)

**电影详情** — 大背景图 + 海报 + 星级评分（点星即评）+ 收藏按钮，底部按标签命中相关推荐。

![电影详情](docs/screenshots/02-movie-detail.png)

**为你推荐** — 顶部显示当前策略（冷启动兜底 / 标签偏好），偏好画像展示 top-6 权重标签，每张推荐卡片附有匹配度 % + 自然语言理由 + 命中标签。

![推荐页](docs/screenshots/03-recommendations.png)

### 后台管理

**数据看板** — 6 张 KPI 卡（电影总数 / 注册用户 / 日评分数 / 推荐点击率 / 覆盖率 / 冷启动占比）+ 近 7 天双色趋势柱状图 + 热门标签分布。

![后台看板](docs/screenshots/04-admin-dashboard.png)

**电影管理** — 表格化展示影片，含标签、评分、状态；顶部搜索按片名/导演过滤；右上「新增电影」弹窗支持全字段编辑。

![电影管理](docs/screenshots/05-admin-movies.png)

**推荐概览** — CTR 近 7 日趋势 + 覆盖率 KPI + 推荐调用日志表，可按策略（`tag-preference` / `cold-start-popular`）过滤。

![推荐概览](docs/screenshots/06-admin-reco-overview.png)

## 技术栈

**后端** — Java 21 · Spring Boot 3.3 · MyBatis-Plus 3.5 · MySQL 8 · Sa-Token 1.39 · BCrypt

**前端** — Vue 3 · TypeScript · Vite 5 · Pinia 2 · Vue Router 4 · Tailwind CSS 3 · lucide-vue-next

**测试** — PowerShell 接口 E2E（57 断言）+ Playwright 浏览器 E2E（7 场景）+ 自动截图生成

## 目录结构

```
Spring Boot 电影推荐系统/
├── PRD.md                    产品需求文档 (Draft v0.2)
├── docs/screenshots/         6 张交付截图（由 Playwright 自动生成）
├── server/                   Spring Boot 后端工程
│   ├── src/main/java/com/cinephile/
│   │   ├── config/           鉴权 / CORS / 分页 / 密码 encoder
│   │   ├── common/           统一响应 / 全局异常
│   │   ├── init/             启动种子数据（12 部电影 + 2 账号）
│   │   └── modules/          6 大业务模块
│   │       ├── auth/         注册 / 登录 / 退出
│   │       ├── user/         用户信息
│   │       ├── movie/        列表 / 详情 / 搜索 / 标签
│   │       ├── rating/       评分（含平均分聚合）
│   │       ├── favorite/     收藏
│   │       ├── recommendation/ 标签偏好 + 冷启动兜底 + 理由文案
│   │       └── admin/        KPI / 趋势 / 调用日志 / 电影维护
│   ├── e2e-test.ps1          端到端接口测试（PowerShell）
│   └── pom.xml
└── web/                      Vue 3 前端工程
    ├── src/
    │   ├── api/              后端 API 封装（http / auth / movies / ...）
    │   ├── router/           带鉴权守卫的路由
    │   ├── layouts/          Public / App / Admin / Blank
    │   ├── pages/            11 个页面
    │   ├── components/       MovieCard / RatingStars / ReasonCard / ...
    │   ├── stores/           Pinia（auth 登录态 / userActivity 行为缓存）
    │   ├── types/            与后端 VO 对齐的 TS 类型
    │   └── styles/main.css   Tailwind 入口
    ├── tests/e2e/            Playwright 浏览器测试
    │   ├── user-flow.spec.ts   7 项行为断言
    │   ├── screenshots.spec.ts 自动生成 6 张交付截图
    │   ├── global-teardown.ts  测试后自动清理数据库
    │   └── helpers.ts
    ├── playwright.config.ts
    └── package.json
```

## 使用教程

### 第 1 步 · 环境准备

需要的开发环境：

| 依赖 | 版本 | 说明 |
|------|------|------|
| JDK | 21+ | 后端运行时 |
| Maven | 3.9+ | 后端构建 |
| Node.js | 18+ | 前端构建 |
| MySQL | 8.0+ | 数据库 |

**Windows** 用户如果通过 phpStudy 装 MySQL，需先在 phpStudy 面板启动 MySQL 服务。

### 第 2 步 · 建库建表

```bash
# 建库
mysql -uroot -p123456 -e "CREATE DATABASE IF NOT EXISTS movie_reco DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

**建表**：DDL 完整版见 [`server/README.md`](./server/README.md#建表-ddl)，把里面那段 SQL 粘贴到 mysql CLI 执行即可。共 8 张表：

- `users` — 用户与角色（user / admin）
- `movies` — 影片元数据
- `movie_tags` — 电影 → 标签映射
- `ratings` — 用户评分（uk = user_id + movie_id）
- `favorites` — 用户收藏（uk = user_id + movie_id）
- `recommendation_logs` — 每次推荐调用
- `recommendation_items` — 该次推荐命中的具体电影
- `user_events` — 曝光/点击等通用事件表（预留）

### 第 3 步 · 启动后端

```bash
cd server
mvn -DskipTests package
java -jar target/movie-reco-server.jar
```

启动完成后监听 `http://localhost:8080`。**首次运行**会自动种入：

- 2 个账号：`admin@example.com / admin123`（管理员）、`liam@example.com / liam1234`（普通用户）
- 12 部电影 + 全部标签（星际穿越、教父、千与千寻、银翼杀手 2049 等）

### 第 4 步 · 启动前端

```bash
cd web
npm install
npm run dev
```

浏览器打开 `http://localhost:5173`。

### 第 5 步 · 体验完整链路

| 场景 | 操作步骤 |
|---|---|
| **登录 + 浏览** | 打开 `/login` → 填 `liam@example.com` / `liam1234` → 自动跳到 `/app/movies` |
| **筛选电影** | 顶栏搜索"科幻" **或** 点击「科幻」标签芯片 → 网格实时过滤 |
| **评分 + 收藏** | 点某张海报 → 详情页点星星（1-5 分）→ 点「收藏」按钮 → 立即生效 |
| **看推荐变化** | 评 3 部以上电影后，导航到「为你推荐」→ 策略从「冷启动兜底」切换到「标签偏好」，卡片附带理由 |
| **个人中心** | 顶栏点头像 → 查看评分/收藏/偏好画像 3 个 tab |
| **切换到管理员** | 打开 `/admin/login` → `admin@example.com` / `admin123` → 进入数据看板 |
| **新增电影** | 侧栏「电影管理」→ 「新增电影」→ 填写标题/年份/标签 → 保存 |
| **看推荐效果** | 侧栏「推荐概览」→ 查看 CTR 趋势、标签分布、调用日志（可按策略过滤） |

### 第 6 步 · 跑自动化测试（可选）

后端和前端都启动后：

```powershell
# 接口 E2E：57 项断言，覆盖两大场景
powershell -NoProfile -File server\e2e-test.ps1

# 浏览器 E2E：真实点击评分/收藏/后台切换
cd web
npm install                          # 首次跑需要
npx playwright install chromium      # 首次跑需要
npm run test:e2e

# 重新生成 6 张交付截图
npm run test:screenshots
```

两个测试脚本**运行完都会自动清理测试数据**，让数据库恢复到 12 部电影 + 2 账号的干净状态。

## 部署到线上（Vercel + Render + TiDB Cloud）

三家服务全部免费额度即可跑。目标架构：

```
[用户浏览器] ──▶ Vercel(全球 CDN, Vue SPA) ──▶ Render(Frankfurt, Spring Boot) ──▶ TiDB Cloud(Frankfurt, MySQL)
```

### A · TiDB Cloud（数据库）

1. 在 <https://tidbcloud.com> 建 **Starter** 集群，Region 建议 AWS Frankfurt / Tokyo / Singapore
2. 集群创建后 Connect → 复制 host / user / password / port（4000）
3. SQL Editor 里粘贴执行本仓库的 [`server/init.sql`](./server/init.sql)（建库 + 8 张表）

### B · 后端部署到 Render

1. 把整个仓库推到一个 **public GitHub repo**
2. <https://render.com> 登录后 **New → Web Service** 关联该 repo
3. 关键字段：
   - **Root Directory**：`server`
   - **Runtime**：Docker（自动识别 [`server/Dockerfile`](./server/Dockerfile)）
   - **Instance Type**：Free（512MB）
   - **Region**：Frankfurt（跟数据库同区，降延迟）
4. **Environment Variables**：
   | 键 | 值 |
   |---|---|
   | `DB_URL` | `jdbc:mysql://<host>:4000/movie_reco?sslMode=VERIFY_IDENTITY&enabledTLSProtocols=TLSv1.2,TLSv1.3&useUnicode=true&characterEncoding=utf8&serverTimezone=Asia/Shanghai` |
   | `DB_USERNAME` | TiDB 面板给的用户名，例如 `xxxxxxxx.root` |
   | `DB_PASSWORD` | TiDB 密码 |
   | `CORS_ALLOWED_ORIGINS` | 先填 `*`，拿到 Vercel 域名后改成精确值 |
5. Deploy。首次构建 5-8 分钟；启动日志出现 `Started MovieRecoApplication` 即成功
6. 记下 Render 分配的 URL，形如 `https://cinephile-server-xxxx.onrender.com`

> ⚠️ **Free 层 15 分钟无访问自动休眠**，冷启动约 30-60 秒。演示前先访问一下 `/api/movies` 唤醒。

### C · 前端部署到 Vercel

1. <https://vercel.com> 登录后 **Add New → Project** 关联同一个 repo
2. 关键字段：
   - **Root Directory**：`web`
   - **Framework Preset**：Vite（自动识别）
   - **Build Command**：`npm run build`
   - **Output Directory**：`dist`
3. **Environment Variables**：
   | 键 | 值 |
   |---|---|
   | `VITE_API_BASE` | 上一步 Render 的 URL，例如 `https://cinephile-server-xxxx.onrender.com` |
4. Deploy。1-2 分钟就绪，拿到域名如 `https://cinephile.vercel.app`

### D · 回填 CORS

拿到 Vercel 域名后，回 Render → Environment → 把 `CORS_ALLOWED_ORIGINS` 改成：

```
https://cinephile.vercel.app,https://*.vercel.app
```

保存后 Render 会自动重启。第二个通配是给 preview 分支用的。

### E · 演示前的检查清单

- [ ] 打开 Vercel 链接首页能加载
- [ ] 用 `liam@example.com / liam1234` 登录成功
- [ ] 电影列表 12 部海报正常显示（TMDB CDN）
- [ ] 评 3 部电影后推荐页从"冷启动"切换到"标签偏好"
- [ ] `admin@example.com / admin123` 能进 `/admin` 数据看板

### F · 线上账号（交付文档用）

| 角色 | 邮箱 | 密码 | 入口 |
|---|---|---|---|
| 普通用户 | `liam@example.com` | `liam1234` | `/login` |
| 管理员 | `admin@example.com` | `admin123` | `/admin/login` |

## 页面清单（对应 PRD 5.1 节，共 11 个页面）

| 入口 | 页面 | 路径 | 守卫 |
|------|------|------|------|
| 官网 | 首页 | `/` | 匿名 |
| 用户 | 登录 | `/login` | 匿名 |
| 用户 | 注册 | `/register` | 匿名 |
| 用户 | 电影列表 | `/app/movies` | 需登录 |
| 用户 | 电影详情 | `/app/movies/:id` | 需登录 |
| 用户 | 为你推荐 | `/app/recommendations` | 需登录 |
| 用户 | 个人中心 | `/app/me` | 需登录 |
| 后台 | 管理员登录 | `/admin/login` | 匿名 |
| 后台 | 数据看板 | `/admin` | 需 admin |
| 后台 | 电影管理 | `/admin/movies` | 需 admin |
| 后台 | 推荐概览 | `/admin/recommendations` | 需 admin |

## 推荐算法（PRD 第 7 节）

第一版为**可解释的标签偏好加权**，不上协同过滤/深度模型：

```text
pref[tag]   = Σ(rating × tagHit) / count(rating for tag)
score(movie)= Σ pref[tag] / (5 × movie.tag_count)   # 归一化到 [0,1]
reason      = top-2 matched tags
```

- **冷启动**（用户评分 &lt; 3 条）自动切换到「社区高分兜底」策略
- **已评分/已收藏**的电影会被过滤，避免重复推荐
- 每次推荐调用记录到 `recommendation_logs` + `recommendation_items` 两张表，供后台分析

## 关键设计决定

1. **单前端工程 vs 多入口** — PRD 定义了 `www.xxx.com / app.xxx.com / admin.xxx.com` 三个子域，实际工程上单前端通过 `/`、`/app/*`、`/admin/*` 三块路由承载，减少初期部署成本。
2. **推荐可解释** — 每条推荐返回 `score / reason / matchedTags`，前端 `ReasonCard` 组件把它们组合成"你近期给高分的科幻标签影片较多"这类自然语言。
3. **Sa-Token** — 前端登录后拿到 uuid 风格 token，写入 `localStorage`，后续请求自动带上；权限校验放在后端 `SaTokenConfig` 的路由拦截器里，管理员接口独立要求 `role = admin`。CORS 预检 OPTIONS 请求需在拦截器里 `stop()` 放行，否则浏览器跨域会被 401 拦掉。
4. **管理员单独登录入口** — 与用户 token 体系相同（同一张 `users` 表），但走独立的 `/admin/login` 页面，避免普通用户误入。

## 端到端测试

| 层级 | 工具 | 覆盖 | 位置 |
|------|------|------|------|
| **接口层** | PowerShell + REST | 完整 REST API 链路，57 项断言 | `server/e2e-test.ps1` |
| **浏览器层** | Playwright + Chromium | 真实点击评分/收藏、后台侧栏高亮、权限守卫，7 场景 | `web/tests/e2e/user-flow.spec.ts` |
| **截图生成** | Playwright + fullPage | 6 张交付截图 | `web/tests/e2e/screenshots.spec.ts` |

两个测试都带自动清理，跑完不留脏数据。

## 常见问题

**Q: 后端启动报 `Column 'created_at' cannot be null` 或字段找不到？**
A: 说明表结构没建全。用 [`server/README.md`](./server/README.md#建表-ddl) 里的完整 DDL 重新建一次表（`DROP TABLE` 后再 `CREATE`）。

**Q: 前端能打开但点评分/收藏没反应，控制台没报错？**
A: 检查是否 CORS 预检被拦。当前版本 `SaTokenConfig` 已在拦截器最前面用 `SaRouter.match(SaHttpMethod.OPTIONS).stop()` 放行 OPTIONS，如果自行改动过鉴权代码请保留这一行。

**Q: 推荐页一直显示"冷启动兜底"？**
A: 因为你当前用户评分数 &lt; 3。评满 3 部电影再刷新推荐页即可切换到「标签偏好」策略。

**Q: 后台看板 7 天趋势图空白？**
A: 今天还没有评分记录时会全 0。评几部电影再回来看即可。

## 已知未做（骨架 / MVP 阶段）

- 未做删除电影接口（只支持下架 = status offline）
- 未做点击事件上报，`recommendation_logs.clicked_count` 目前一直是 0
- 未做用户管理页
- 未做国际化、SSR、上线部署脚本

## 开发日志

- **v0.1** — PRD 起草 + 前端假数据骨架
- **v0.2** — PRD 修订（补注册页、管理员登录页、`user_events` / `recommendation_items` 两张表）
- **0.1.0** — 后端 6 大模块完成，接口 E2E 57/57 通过
- **前后端联调** — 前端接入真实 API，移除全部 mock 数据
- **0.1.1** — 修复 CORS 预检拦截 / 侧栏高亮 / 星星点击 / 趋势图渲染四个 UI bug；补 Playwright 浏览器 E2E + 自动截图 + 数据库自清理
