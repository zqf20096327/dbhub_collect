# 研途 ResearchFlow

面向大学生小组科研 / 课程项目的资料与进度工作台：把散落的资料、来源证据、任务状态和日期区间周报放在同一个中文界面里，减少「资料找不到、进度反复问、周报重复写」。

核心数据由 **OceanBase seekdb** 真实持久化。接入失败时接口返回明确的 `503 seekdb_unavailable`，不会用静态样例伪装成功。

- 线上站点（Qoder Sites）：<https://researchflow-beda1hy9p7c.qoder.website>
- 代码仓库：<https://github.com/kfccc29/researchflow-qoder-seekdb>
- 线上访问范围：**公开**。2026-10-28 经所有者确认改为任何人可访问，匿名请求返回 HTTP 200。
- 线上演示范围：**只读快照**。Qoder Sites 运行时不提供 seekdb 原生引擎，因此线上页面读取的是从本地真实数据库导出的静态快照；新增资料、修改任务状态等写入操作在线上被禁用。完整写入链路请在本机按下方步骤运行。

![桌面端概览](docs/assets/desktop-overview-1440.png)

## 功能

- **概览**：项目信息、资料/任务计数、整体完成度、最近资料与即将到期任务。
- **资料检索**：按标题、正文、标签、来源出处检索；结果返回命中字段、正文上下文片段和来源出处，支持唯一检索词验收。
- **资料录入**：标题、内容、标签、来源类型、来源出处写入 seekdb，返回数据库中的真实记录。
- **任务进度**：待开始 / 进行中 / 已完成 / 受阻四种状态，更新后写入任务表并追加 `activity_log` 操作日志。
- **日期区间周报**：确定性模板，区分已完成、进行中、风险、下一步；支持 JSON 与 Markdown，Markdown 可复制或下载。
- **集成与验证**：显示 seekdb 引擎版本、连接状态、本次进程的查询/写入计数，以及最近一次自动化验证结果。
- **响应式布局**：深色导航 + 温暖浅色内容 + 青绿色主色；已用 CDP 设备模拟验证 390px 真实移动端布局。

![移动端 390px 概览](docs/assets/mobile-overview-390.png)

## 技术栈

| 层 | 选型 |
| --- | --- |
| 前端 | React 19、Vite 6、TypeScript、原生 CSS、hash 路由 |
| API | Node.js 24 原生 `http`，ESM，无 Web 框架 |
| 数据库 | OceanBase seekdb 1.4.0（Docker 服务模式，MySQL 协议） |
| SDK | `seekdb@1.2.0`（官方 npm 包） |
| 发布 | Qoder Sites 静态托管 + 只读演示快照 |

## 快速开始

### 前置条件

- Node.js >= 20（实际验证环境为 Node v24.13.0）
- Docker Desktop 已启动
- 本机端口 `3001`（API）、`5173`（开发前端）、`12881`（seekdb 映射）可用
- npm 缓存已由 `.npmrc` 指向 `F:\DevCache\npm-cache`

### 1. 安装依赖

```bash
cd F:\OceanBase\Qorder
npm ci
```

`seekdb` 与 `@seekdb/default-embed` 固定为 `1.2.0`。不要升级到带 `workspace:*` 协议的新版本，否则 npm 会报 `EUNSUPPORTEDPROTOCOL`。

### 2. 启动 seekdb

```bash
npm run db:start
npm run db:status
```

首次启动会拉取 `oceanbase/seekdb:latest`，创建独立容器 `researchflow-seekdb` 和命名数据卷 `researchflow-seekdb-data`，等待 `SELECT VERSION()` 成功。实际验证得到的引擎版本为 `5.7.25-OceanBase seekdb-v1.4.0.0`，镜像摘要为 `sha256:4db4961869d554313520d6081fca29265ba6da6db7313311bd8acbed771a956b`。

> Windows 下不要改用目录 bind mount 挂载 seekdb 数据目录；实际测试会触发 seekdb block manager `errcode=-4009`。本项目使用 Docker 命名数据卷。

### 3. 启动开发环境

```bash
npm run dev
```

该命令同时启动：

- API：<http://127.0.0.1:3001>
- 前端：<http://127.0.0.1:5173>（`/api` 代理到 3001）

首次连接时，如果 `researchflow` 数据库或表不存在，服务会自动创建，并仅在空表时写入固定合成样例。已有数据不会被覆盖。

### 4. 生产式本地运行

```bash
npm run build
npm start
```

访问 <http://127.0.0.1:3001>。Node 服务同时提供 API 和 `dist` 静态文件；静态路由回退到 `index.html`。

### 5. 只读演示站点

```bash
npm run build:site
npm run preview
```

访问 <http://localhost:4173>。`build:site` 使用 `.env.demo` 中的 `VITE_DEMO=1`，把提交在 `web/src/demo/snapshot.json` 的真实导出快照打包为静态站点；写入按钮会被禁用并显示只读说明。

快照的重新导出需要本地 API 与 seekdb 处于运行状态，且数据库为规范种子状态（6 条资料、12 条任务、`task-003` 为进行中、验证结果通过）：

```bash
npm run demo:export
npm run build:site
```

## 配置

复制 `.env.example` 为 `.env` 后按需修改。默认值如下：

| 变量 | 默认值 | 说明 |
| --- | --- | --- |
| `PORT` | `3001` | HTTP API 端口 |
| `HOST` | `127.0.0.1` | 监听地址；默认仅本机 |
| `SEEKDB_HOST` | `127.0.0.1` | seekdb 主机 |
| `SEEKDB_PORT` | `12881` | Docker 映射到宿主机的端口 |
| `SEEKDB_USER` | `root` | seekdb 用户 |
| `SEEKDB_PASSWORD` | 空 | 本地隔离容器默认空密码；如修改需与容器一致 |
| `SEEKDB_DATABASE` | `researchflow` | 业务数据库名，仅允许字母、数字、下划线 |
| `DB_TIMEOUT_MS` | `6000` | 单次数据库操作超时 |

`.env` 已被 `.gitignore` 排除，不会进入仓库。`.env.example` 与 `.env.demo` 不包含凭证，可以提交。

## 架构与数据流

### 本地完整链路

```text
浏览器
  React 19 + Vite 6 + TypeScript
  hash 路由 /#/overview /#/sources /#/tasks /#/weekly /#/integration
        │  /api（开发时 Vite 代理，生产时同源）
        ▼
Node.js 24 原生 HTTP API（server/index.js）
  参数化 SQL、输入校验、统一错误映射
        │  seekdb npm SDK 1.2.0
        ▼
Docker 容器 researchflow-seekdb
  OceanBase seekdb 1.4.0（127.0.0.1:12881）
  命名数据卷 researchflow-seekdb-data
```

### 线上演示链路

```text
Qoder Sites 静态托管（dist/）
  只读快照 web/src/demo/snapshot.json
  前端在浏览器内完成检索与确定性周报重算
  写入操作被禁用，不连接任何线上数据库
```

Qoder Sites 支持静态文件与 Deno Edge Function，但无法运行 seekdb 原生引擎。我们没有伪造一个「在线 seekdb」：线上明确标注只读快照，完整写入只在本地真实 stack 中运行。

### 数据表

| 表 | 关键字段 | 用途 |
| --- | --- | --- |
| `sources` | `id`、`project_id`、`title`、`content`、`tags_json`、`source_type`、`source_ref`、`created_at`、`created_on` | 科研资料与来源 |
| `tasks` | `id`、`project_id`、`title`、`status`、`due_date`、`completed_on`、`completed_at`、`sort_order`、`updated_at` | 任务进度 |
| `activity_log` | `task_id`、`action`、`from_status`、`to_status`、`actor`、`at` | 任务状态变更审计 |

所有查询使用参数化 SQL。检索对标题、正文、标签 JSON、来源出处做 `LIKE` 匹配，并对 `%`、`_` 进行转义；命中正文时截取关键词前后各 52 个字符作为证据片段。DATE 列在 SELECT 时用 `DATE_FORMAT(..., '%Y-%m-%d')` 读取为无时区字符串，避免驱动把 DATE 解析成本地 `Date` 后产生跨时区偏移。

### API

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/meta` | 项目元信息与服务时间 |
| GET | `/api/health` | seekdb 连接、版本、延迟；失败返回 503 |
| GET | `/api/overview` | 统计、最近资料、即将到期任务、健康状态 |
| GET | `/api/sources?q=&tag=` | 资料检索，返回证据片段与空状态提示 |
| POST | `/api/sources` | 新增资料，成功返回 201 与数据库记录 |
| GET | `/api/tasks` | 任务列表 |
| PATCH | `/api/tasks/:id` | 更新任务状态并写操作日志 |
| GET | `/api/weekly?from=YYYY-MM-DD&to=YYYY-MM-DD` | 周报 JSON；`format=md` 返回 Markdown |
| GET | `/api/integration` | 引擎信息、进程内查询/写入计数、最近验证结果 |

### 错误语义

- `400 invalid_range`：周报日期非法、反向区间、不存在的日期或超过 366 天。
- `400 invalid_input` / `invalid_status`：输入不合法。
- `404 task_not_found` / `not_found`：资源不存在。
- `413 body_too_large`：请求体超过 512KB。
- `503 seekdb_unavailable`：数据库不可用。响应中带修复提示，且不返回任何回退条目。
- `500 internal_error`：未预期错误，记录堆栈并返回请求 ID。

### 周报确定性规则

模板版本为 `deterministic-v1`，不依赖大模型：

1. `done` 且 `completedOn` 落在区间内 → **已完成**。
2. `blocked` → **风险**。
3. 非 `done` 且截止日期早于或等于区间结束日 → **风险（逾期）**。
4. `in_progress` → **进行中**。
5. 其余 → **下一步**。
6. 按 `createdOn` 落在区间内统计**本期新增资料**。

日期统一使用 Asia/Shanghai 时区，周报区间最长 366 天。Markdown 中标注真实数据库名，避免把样例或快照误认为线上查询结果。

## 固定合成样例

样例项目为「夜间步行安全感 · 课程调研」，全部人物、路线与观察记录均为合成内容，不包含真实姓名、联系方式或可识别影像。

- 6 条资料、12 条任务，sprint 为 2026-10-19 至 2026-11-01。
- 初始状态：3 待开始 / 2 进行中 / 5 已完成 / 2 受阻，整体完成度 42%。
- 唯一检索词：`RF-UNIQ-NIGHT-07`，只出现在 `src-001` 正文中，用于证明检索来自真实数据库内容而非界面拼接。

## 自动化验证

```bash
npm run check   # TypeScript + 服务端语法检查
npm run verify  # 11 项真实集成验证
```

`npm run verify` 会：

- 连接真实 seekdb，读取 `VERSION()`，重建独立测试库 `researchflow_verify`；
- 动态分配空闲端口启动测试 API，不污染 3001 上的开发服务；
- 验证新增资料、唯一词检索、无结果、任务更新、周报、服务重启持久化；
- 通过直接写入数据库并读回，验证 DATE 边界值无时区偏移；
- 启动一个指向未监听端口的 API 实例，确认返回 503 而非伪造数据；
- 把结果写入 `docs/verification/latest.json` 与 `latest.md`，并按时间戳归档到 `docs/verification/runs/`。

### 最近一次真实结果（2026-10-27）

- 状态：**通过 11/11**
- 环境：Node v24.13.0 / win32-x64 / `seekdb@1.2.0`
- 引擎：`5.7.25-OceanBase seekdb-v1.4.0.0`
- 测试库：`researchflow_verify`（独立于演示库 `researchflow`）

| # | 检查 | 结果 | 关键证据 |
| --- | --- | --- | --- |
| 1 | seekdb 连接与独立测试数据库 | 通过 | 127.0.0.1:12881，测试库重建 |
| 2 | 启动测试 API 并检查健康状态 | 通过 | HTTP 200，6 资料 / 12 任务 |
| 3 | 固定样例与概览统计 | 通过 | 3/2/5/2，完成度 42% |
| 4 | 唯一词检索返回来源证据 | 通过 | `RF-UNIQ-NIGHT-07` → `src-001`，命中正文 |
| 5 | 新增资料写入并再次检索 | 通过 | POST 201，直接查库确认，检索命中 |
| 6 | 无结果检索返回明确空状态 | 通过 | 0 条 + 空状态提示 |
| 7 | 任务状态更新并记录日志 | 通过 | `task-003` 完成，`completed_on` 与 `activity_log` 写入 |
| 8 | 日期区间周报与 Markdown 导出 | 通过 | 固定/动态区间统计与 `format=md` |
| 9 | DATE 边界写入与读回 | 通过 | `2026-10-27` / `2024-02-29` / `2026-01-01` 无偏移 |
| 10 | 重启 API 后数据仍然存在 | 通过 | 新端口重启，资料/任务/周报保持 |
| 11 | seekdb 不可用时返回 503 | 通过 | `seekdb_unavailable`，无条目回退 |

完整输出：[docs/verification/latest.md](docs/verification/latest.md)、[docs/verification/latest.json](docs/verification/latest.json)。

第一轮验证曾在 2 个断言上失败，原因是测试预期与实际日期/动态区间规则不一致（直接查库返回的 `DATE` 对象未按上海时区格式化；动态区间把已逾期任务归入风险）。修正的是测试断言，不是为了让应用通过而篡改行为；失败记录保留在 `docs/verification/runs/verify-20261027-193056.*`。第二轮 10/10 记录为 `verify-20261027-193116.*`。独立复核提出 DATE 读取仍可能受运行时时区影响后，服务端改为 SQL `DATE_FORMAT` 返回无时区字符串，并新增第 9 项真实写入/读回边界断言；第三轮 11/11 记录为 `verify-20261027-194359.*`。

### 浏览器与响应式检查

- 在内置浏览器中实际执行：唯一词检索、新增资料、任务状态更新、周报生成与 Markdown 下载；新增/变更的测试数据随后清理，恢复规范种子状态。
- 浏览器导出的周报留档：[docs/verification/browser-weekly-2026-10-19_2026-10-25.md](docs/verification/browser-weekly-2026-10-19_2026-10-25.md)。
- 使用 Chrome DevTools Protocol `Emulation.setDeviceMetricsOverride` 验证 390×844：`documentScrollWidth = 390`，无横向溢出；导航五个入口全部可见。
- 桌面 1440px 截图与移动端截图见 `docs/assets/`。

## Qoder Sites 发布

- 最近更新时间：2026-10-27 19:45（Asia/Shanghai；DATE 映射修复后的第二次发布）
- 首次发布时间：2026-10-27 19:36（Asia/Shanghai）
- 平台状态：`published: true`、`committed: true`
- 站点地址：<https://researchflow-beda1hy9p7c.qoder.website>
- 访问范围：公开；2026-10-28 已验证匿名 HTTP 200，JS/CSS 的 SHA-256 与本地已验证构建一致。
- 发布内容：`dist/` 只读演示快照，未上传 `node_modules`、`.env`、源码映射或运行时数据库

发布使用 Qoder Sites 工具的 `prepare_site` → `get_publish_status` → `publish_site` 流程，构建产物为经过校验的静态文件。线上页面不执行 seekdb 查询，也不接受写入；这是平台运行时限制下的明确取舍，而不是把本地 API 冒充线上后端。

站点首次发布时为私密访问；2026-10-28 经所有者确认已调整为公开。匿名访问与构建一致性证据见 [docs/verification/public-site.json](docs/verification/public-site.json)。页面交互验证在本地同一构建上执行，未将 HTTP 可达性等同于生产环境全流程交互验证。

## 停止与数据保留

```bash
npm run db:stop      # 停止 seekdb 容器
npm run db:status    # 查看状态
npm run db:logs      # 查看最后 80 行日志
```

- 停止容器不会删除命名数据卷，下次 `npm run db:start` 会保留资料、任务和操作日志。
- 停止 Node 服务即可结束 API；开发模式下同时结束 Vite。
- 若要彻底删除本地数据（不可恢复），需显式删除容器与数据卷：

```bash
docker rm -f researchflow-seekdb
docker volume rm researchflow-seekdb-data
```

## 故障处理

| 现象 | 排查 |
| --- | --- |
| `/api/health` 返回 503 或 `seekdb_unavailable` | 运行 `npm run db:status`；确认 Docker Desktop 已启动；确认 12881 未被其他程序占用 |
| `npm run db:start` 等待超时 | 查看 `npm run db:logs`；首次拉取镜像可能较慢；确认容器名/端口未被占用 |
| seekdb 报 `errcode=-4009` | 不要使用 Windows 目录 bind mount，使用脚本创建的命名数据卷 |
| `EADDRINUSE` | 3001/5173/4173 被占用；先停止旧进程，或通过 `PORT` 修改 API 端口并同步 Vite 代理 |
| 页面提示「前端尚未构建」 | 运行 `npm run build`，或开发时使用 `npm run dev` |
| 线上页面出现登录页 | 当前应为公开；由所有者在 Sites 分享设置中检查是否仍为「任何人都可访问」 |
| 线上写入按钮不可用 | 预期行为：线上为只读快照；完整写入请本地运行 |
| 周报日期与预期差一天 | DATE/DATETIME 读取统一走 SQL `DATE_FORMAT` 或 Asia/Shanghai 格式化；不要用 `Date#toISOString()` 截取本地日期 |
| npm 报 `EUNSUPPORTEDPROTOCOL workspace:*` | 依赖必须锁定 `seekdb@1.2.0` 与 `@seekdb/default-embed@1.2.0` |
| Windows 上 seekdb 嵌入式绑定不可用 | 锁定版本的 JS bindings 不支持 win32-x64；本项目使用 Docker 服务模式 |

## 仓库结构

```text
.
├─ server/                 # Node HTTP API、seekdb 数据层、种子数据
│  ├─ config.js
│  ├─ db.js
│  ├─ index.js
│  ├─ repo.js
│  └─ seed.js
├─ shared/                 # 前端/后端共用的检索与周报逻辑
│  ├─ report.mjs
│  └─ search.mjs
├─ web/                    # React 前端与只读演示快照
│  └─ src/
├─ scripts/                # seekdb 生命周期、开发启动、验证、快照导出
├─ docs/
│  ├─ QODER_DEVELOPMENT.md # Qoder 开发记录
│  ├─ verification/        # 真实验证输出与归档
│  └─ assets/              # 桌面/移动端截图
├─ dist/                   # 构建产物（被 .gitignore 排除）
├─ PROJECT_BRIEF.md
├─ DELIVERY_AUDIT.md       # 独立核对记录
├─ SUBMISSION_CHECKLIST.md
└─ README.md
```

被排除的运行时内容：`.env`、`node_modules/`、`dist/`、`.data/`、`.run/`、日志、`.qoder.site` 描述文件、缓存与凭证。

## 安全与隐私

- 固定样例全部为合成内容，不读取其他项目、个人资料或凭证值。
- 数据库只监听 `127.0.0.1:12881`，API 默认只监听 `127.0.0.1:3001`。
- 参数化 SQL、输入长度与数据库名校验、512KB 请求体上限、CSP 与安全响应头。
- 仓库不包含 `.env`、密码、令牌、运行时数据或 `node_modules`。
- 线上只读快照来自合成样例数据库，不包含真实个人数据。

## 已知限制

1. **线上不是完整后端**：Qoder Sites 不能运行 seekdb，线上只能演示只读快照；新增资料和任务更新仅本地可用。
2. **生产环境验证范围**：已验证匿名访问及 JS/CSS 与本地构建一致；交互验证使用本地同一构建。
3. **无大模型**：周报使用确定性模板 `deterministic-v1`，不生成自由文本分析。
4. **单项目单用户**：未实现多用户权限、团队协作和文献自动解析。
5. **Docker 依赖**：本地完整功能需要 Docker Desktop 和可用端口；Windows 不支持该版本的 seekdb 嵌入式绑定。

## 开发记录与提交

- Qoder 开发记录：[docs/QODER_DEVELOPMENT.md](docs/QODER_DEVELOPMENT.md)
- 独立核对记录：[DELIVERY_AUDIT.md](DELIVERY_AUDIT.md)
- 提交清单：[SUBMISSION_CHECKLIST.md](SUBMISSION_CHECKLIST.md)
- 验证输出：[docs/verification/latest.md](docs/verification/latest.md)
