<div align="center">

# OntoOS · 企业本体智能平台

**把企业的数据、知识、流程与 AI 统一在一个语义层上**

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![React](https://img.shields.io/badge/React_18-TypeScript-61dafb.svg)]()
[![Hono](https://img.shields.io/badge/Hono-API_server-e36002.svg)]()
[![SQLite](https://img.shields.io/badge/SQLite-Drizzle_ORM-003b57.svg)]()
[![Tests](https://img.shields.io/badge/smoke-204/204_passing-2ea44f.svg)]()

**42 个应用 · 全栈真实落库 · 一条命令启动 · 零外部依赖**

[快速开始](#快速开始) · [功能矩阵](#功能矩阵42-个应用) · [架构](#架构) · [验证资产](#测试与验证资产)

</div>

---

OntoOS 是一个开源的企业本体（Ontology）智能平台：把业务实体建模为**对象、链接、动作**的统一本体，在其上运转知识检索、交互分析、AI 助手（含 ChatBI 对话出图）、审批治理与自动化。所有页面均读写真实数据库，无 mock 演示态。

![平台仪表盘](docs/screenshots/overview.png)

## 为什么是本体

传统系统按应用割裂数据：CRM 一份客户、ERP 一份客户、工单系统又一份。OntoOS 把它们收敛为**同一个语义层**——

- **对象（Object）**：客户、设备、工单、订单……由类型定义动态生成表格列与表单
- **链接（Link）**：对象间的业务关系，构成可探索的关系图谱
- **动作（Action）**：校验 → 审批 → 写回 → 留痕的可治理变更
- **AI 原生**：智能助手基于本体调用 22 种工具，查数、出图、执行动作全程受权限与语义层约束

## 核心能力一览

### 1 · 本体建模与对象工作台

定义对象类型（属性/枚举/校验）、链接类型、动作、函数与业务术语；对象浏览器按类型定义动态生成列与表单，支持实例增删改查、关联管理、保存的探索、对象集比较、派生属性与场景分支。

| 本体管理器 | 对象浏览器 |
|---|---|
| ![本体管理器](docs/screenshots/ontology-manager.png) | ![对象浏览器](docs/screenshots/object-explorer.png) |

### 2 · 关系图谱与知识检索

关系图谱按链接实例渲染对象网络，支持聚焦、展开与业务仿真；知识库支持文档入库 → 解析分块 → 向量化，检索采用 **BM25 + 向量双路召回 + RRF 融合**，结果可溯源到具体分块。

| 关系图谱 | 知识检索（命中高亮 + 来源溯源） |
|---|---|
| ![关系图谱](docs/screenshots/graph.png) | ![知识检索](docs/screenshots/knowledge-search.png) |

### 3 · 交互分析与调度优化

探索分析：维度分组聚合真实对象，柱图/饼图/明细表联动，支持日期分桶与时间范围；调度优化内置约束求解引擎（产线/批次/优先级/工时冲突检测），甘特视图一键应用排程。

| 探索分析 | 调度优化（甘特 + 冲突检测） |
|---|---|
| ![探索分析](docs/screenshots/contour.png) | ![调度优化](docs/screenshots/scheduling.png) |

### 4 · 智能助手：对话式操作平台（含 ChatBI）

侧滑助手常驻全站，双引擎（LLM function-calling / 本地规则降级），**22 个工具**覆盖导航、对象查询、动作执行、知识检索、分组统计、函数/管道/排程、治理扫描、审批决策等；语义层守卫确保只按**认证过的业务口径**回答，无覆盖则明确拒答。

ChatBI 对话内出图并**自动选择图表形态**：时间趋势 → 折线图、枚举占比 → 饼图、排行 → 条形图、二维交叉 → **热力矩阵**；支持 **TOP-N**（"停机时长 TOP5 设备"）、**环比/同比**（自动推导对比窗口，给出本期/上期值与增减百分比）、**多维交叉**（"各设备类型的状态分布"、"按月看各状态订单金额"），双引擎均可解析这些问法。问题模糊（如"统计一下"）或字段不存在时，助手会**主动反问澄清**并给出可点选项，点击即继续——不瞎猜口径。

| ChatBI 分组聚合（条形图） | ChatBI 月度趋势（折线图） |
|---|---|
| ![智能助手 ChatBI](docs/screenshots/aip-chatbi.png) | ![智能助手趋势](docs/screenshots/aip-chatbi-trend.png) |
| **ChatBI 二维交叉（热力矩阵）** | |
| ![AIP 交叉分析](docs/screenshots/aip-chatbi-cross.png) | |

### 5 · 治理闭环与实现进度

动作引擎校验→审批分流→写回→全量审计；安全与标记提供脱敏规则、敏感扫描与生命周期策略。42 个应用的实现状态以 `src/config/status.ts` 为单一事实来源，站内「实现进度」页实时同步——**不虚标任何状态**。

| 登录 | 实现进度（42 应用总表） |
|---|---|
| ![登录](docs/screenshots/login.png) | ![实现进度](docs/screenshots/roadmap.png) |

## 快速开始

**前置要求**：Node.js 22+（推荐 22 LTS）。

> **Windows 用户注意**：`better-sqlite3` 是原生模块，若无预编译包会回退源码编译，需要
> **Visual Studio Build Tools**（勾选「使用 C++ 的桌面开发」）与 Python 3。
> 若 `npm install` 报 `gyp ERR! find VS`，请先安装上述工具，或改用 WSL / Docker 运行
> （Docker 可完全绕过此问题，见 [部署手册](./docs/DEPLOYMENT.md)）。

```bash
git clone https://github.com/dengzhh/ontology-platform.git && cd ontology-platform
npm install              # 首次
npm run db:migrate       # 初始化数据库（data/ontoos.db，幂等）
npm run seed             # 写入演示数据（星辰智造集团 + 个人生活模板包）
npm run dev              # 一条命令启动全栈：前端 http://localhost:5174 + API :5000
```

**默认账号**：`chen.xingye / ontos@2026`（平台管理员；另有维修工程师/计划员/审计员演示账号，登录页可一键填入）

**可选：一键装载全功能验证数据**（幂等，120 项断言）

```bash
python demo-data/build_external_db.py   # 生成独立外部 SQLite 演示库（4 表 / 120 行）
node demo-data/load.mjs                 # 期望：通过 120/120
```

装载后按 `demo-data/FEATURE-MATRIX.md` 的 42 页验证矩阵逐页体验。清理验证数据：`node demo-data/load.mjs --clean`。

<details>
<summary><b>生产部署与常用脚本</b></summary>

**生产部署（单端口：API + 前端静态同进程）**

```bash
npm ci && npm run build:all   # 前端 → dist/，服务端 → dist-server/（CommonJS）
export ONTOOS_SECRET="$(openssl rand -base64 32)"       # 密钥加密主密钥，必须备份保管
export ONTOOS_JWT_SECRET="$(openssl rand -base64 32)"   # 登录令牌签名密钥，生产必填
export NODE_ENV=production
npm run start             # 纯 node 运行，不依赖 tsx：http://localhost:5000
```

**Docker（推荐，二选一）**

```bash
# 方式一：直接拉取官方构建的镜像（免构建，支持 amd64/arm64，约 654MB）
# 空库首次启动会自动写入演示数据，直接登录即可，无需手动初始化
docker run -d --name ontoos \
  -e ONTOOS_SECRET="$(openssl rand -base64 32)" \
  -e ONTOOS_JWT_SECRET="$(openssl rand -base64 32)" \
  -p 5000:5000 -v ontoos-data:/app/data \
  ghcr.io/dengzhh/ontology-platform:latest

# 方式二：本地构建
docker compose up -d --build
```

- 默认账号：`chen.xingye / ontos@2026`（首启自动创建）
- 正式部署接真实数据时，加 `-e AUTO_SEED=false` 关闭演示数据自动写入
- 镜像地址：`ghcr.io/dengzhh/ontology-platform`（标签：`latest`、`v1.2.3`、`sha-xxxxxxx`）

**备份与恢复（VACUUM INTO 在线快照，不必停服）**

```bash
npm run backup            # 备份 + integrity_check 校验，保留最近 14 份
npm run backup:list       # 列出备份
npm run restore -- data/backups/ontoos-YYYYMMDD-HHmmss.db   # 恢复（需先停服）
```

详见 [部署手册](./docs/DEPLOYMENT.md)（含反向代理、systemd、安全上线检查清单、数据处理与合规说明）。

| 脚本 | 说明 |
|---|---|
| `npm run dev` | 开发：前端(vite) + API(tsx watch) 双进程热更新 |
| `npm run start` | 生产：单进程托管 API 与前端产物 |
| `npm run build` | 前端类型检查 + 产物构建（dist/） |
| `npm run build:server` | 服务端编译为 CommonJS（dist-server/，生产启动用） |
| `npm run build:all` | 前后端一次性构建 |
| `npm run typecheck:server` | 服务端类型检查 |
| `npm run backup` | 在线备份 + 完整性校验 |
| `npm run smoke` | 全站 API 黑盒冒烟（204 项断言，零依赖） |
| `npm run db:migrate` | 幂等建表 + 空间地基回填 |
| `npm run seed` | 重置并写入演示数据 |

</details>

> **多空间提示**：平台为多空间行级隔离架构（组织/个人/家庭），演示数据分布在组织空间「星辰智造集团」与个人空间，顶栏可切换。

## 功能矩阵（42 个应用）

| 域 | 应用 |
|---|---|
| **概览** | 应用中心（Launcher）、平台仪表盘 |
| **数据** | 数据连接（外部 SQLite/CSV/JSON 文件源真实探测与同步）、管道构建、代码仓库、数据集、数据血缘（缩放拓扑 + 影响分析） |
| **本体** | 本体管理器（对象/链接/动作/函数/接口/业务术语六 Tab）、对象浏览器、对象视图、关系图谱、规则引擎、流程编排、调度优化（本地求解引擎）、时序与告警 |
| **知识** | 知识库（入库/分块/向量化）、知识检索（BM25+向量 RRF）、知识抽取（LLM 候选 → 审核 → 落地为本体类型） |
| **分析** | 探索分析、联动分析、路径分析、地理空间、智能报告、智能表格（单元格写回本体 + 审计） |
| **应用** | 应用搭建、自动化引擎、岗位工作区、应用市场 |
| **AIP** | 工作流编排（可视化节点编排 + undo/redo + 连线控制 + 画布缩放 + **6 个开箱即用预设工作流**：设备健康分诊/工单紧急分流/订单金额分级/文档归类/文档智能分析/LLM 归因；**预览运行 → 确认 → 真实落库**：生成工单对象/通知/待审批单，离线模板不依赖 AI 网关）、智能体构建、**文档分析**（选文档→AI 分析→带上下文多轮追问，AI 网关失败保留草稿可重试）、模型管理、模型评估、开发者工具（API 密钥真实鉴权） |
| **治理** | 审批中心、审计日志、安全与标记（脱敏规则/敏感扫描/生命周期） |
| **管理** | 用户与权限、实现进度、控制面板（SMTP/AI/嵌入/视觉配置 + 真实用量）、识别模板、部署发布（本地编排状态机） |

**全局能力**：Ctrl+K 命令面板 · 通知中心 · 顶栏扫描录入（视觉/文本双通道识别，购物小票/发票/订单）· 多空间模板包与导出导入 · JWT + API 密钥双鉴权 · 业务术语/认证指标语义层 · 游标分页与事务批量导入（10 万行级实测毫秒响应）

## 架构

```
┌────────────────────────── 前端 React 18 + Vite + TailwindCSS ──────────────────────────┐
│  42 应用页面 · PageShell 骨架 · Ctrl+K 命令面板 · AIP Assist 侧滑助手 · 扫描录入        │
└──────────────────────────────────────┬─────────────────────────────────────────────────┘
                                       │ fetch（JWT + x-space-id）
┌──────────────────────────────────────▼─────────────────────────────────────────────────┐
│                              Hono API 服务（28 个路由组）                                │
│  对象/本体 │ 动作引擎+审批 │ 知识(分块/向量/BM25+RRF) │ 聚合分析 │ 时序 │ 调度求解        │
│  函数沙箱(node:vm) │ 自动化规则 │ 治理(审计/标记/脱敏) │ AI 网关(OpenAI 兼容, 可降级)     │
│  多空间行级隔离（org/personal/family · resolveSpace · 角色权限）                         │
└──────────────────────────────────────┬─────────────────────────────────────────────────┘
                                       │ Drizzle ORM（SQL 下推 + 热点索引 + 游标分页）
                            ┌──────────▼──────────┐        ┌──────────────────────┐
                            │ SQLite（better-sqlite3）│        │ 外部源（SQLite/CSV/JSON，│
                            │ 51 张表 · 单文件零运维  │        │ 路径白名单只读）        │
                            └─────────────────────┘        └──────────────────────┘
```

| 层 | 选型 | 说明 |
|---|---|---|
| 前端 | React 18 · TypeScript(strict) · Vite 5 · TailwindCSS · recharts · lucide-react | 42 页全 live，页面状态单一事实来源 `status.ts` |
| 后端 | Hono · @hono/node-server · Drizzle ORM | 28 路由组，`server/routes/*` 分域挂载 |
| 数据 | better-sqlite3（单文件） | 幂等迁移；升级路径：PostgreSQL（Drizzle 换方言） |
| 认证 | JWT(HS256) + bcryptjs + API 密钥（SHA-256） | 多空间行级隔离；升级路径：OIDC/LDAP/SSO |
| 知识 | BM25 + 向量余弦 + RRF 融合 | embedding 远程模型 + 本地哈希降级 |
| AI | OpenAI 兼容网关（端点/密钥/模型存库，服务端代理） | 未配置时本地规则引擎降级，功能可用 |
| 函数 | node:vm 沙箱 | 版本/发布/回滚/测试运行 |

**目录结构**

```
src/
├── config/nav.ts              # 42 应用路由/图标/能力域
├── config/status.ts           # ★ 页面状态单一事实来源（live/partial/mock）
├── components/layout          # 顶栏、侧栏、命令面板、AIP Assist、扫描录入
├── components/ui | canvas     # PageShell、DataTable、图谱/甘特/地图/电子表格画布
├── pages/                     # 42 个应用页面（按域分目录）
└── lib/                       # api（JWT+空间头）、useApi、文件解析
server/
├── index.ts                   # 28 个路由组挂载
├── routes/ · engine/          # 业务 API · 动作/检索/向量/沙箱/语义层/外部源引擎
├── templates/packs.ts         # 演示模板包
└── migrate.ts · seed.ts       # 幂等迁移 / 演示数据
shared/ai-tools.ts             # 前后端共享的 22 个 AI 工具契约
tests/ · demo-data/            # 冒烟/契约/清单/E2E 剧本/扫描素材 · 验证数据装载
```

## 测试与验证资产

| 资产 | 规模 | 说明 |
|---|---|---|
| `tests/smoke.mjs` | **204 项断言全绿** | 零依赖黑盒：登录 → 60+ 读端点 → 写闭环 → 权限 → 外部源 → ChatBI → 函数沙箱 → 分页/批量 |
| `demo-data/load.mjs` | **118 项幂等装载** | 一键生成验证全部功能的数据集（含外部库构建） |
| `demo-data/stress.mjs` | **10 万行基准** | 事务灌入 726ms、索引列表 0.3ms、count 5.4ms，自动清理 |
| `demo-data/FEATURE-MATRIX.md` | 42 页矩阵 | 每页功能 ↔ 验证数据 ↔ 体验步骤 |
| `tests/checklist.md` / `e2e-scenarios.md` | 42 页清单 / 10 剧本 | 人工验收与业务闭环走查 |
| `tests/fixtures/` | 24 个素材 | 小票/发票/订单/快递 + PDF/Word/CSV/TXT + 边界异常 |

## 已实现深度（节选）

- **动作·审批·审计闭环**：动作引擎校验 → 审批分流 → 写回 → 全量留痕；自动化规则支持 condition 表达式与 create/update/delete/link 效果
- **语义层**：业务术语 + 同义词 → 本体属性映射，人工认证后 AIP/Agent 按认证口径回答，无覆盖明确拒答（不猜测）
- **函数沙箱**：node:vm 隔离执行、版本管理、发布/回滚、测试输入输出
- **数据规模**：热点列索引 + SQL 下推 + 游标分页（limit 上限 200）+ 事务批量导入（`POST /objects/bulk`）
- **外部数据源**：独立 SQLite 库与 CSV/JSON/TXT/MD 文件源，真实连通性探测 → 表预览 → 同步为本体对象（路径白名单只读）
- **调度求解**：本地启发式引擎（约束/冲突/建议/应用真实落库）；部署发布 为本地编排状态机（晋升/回滚/冻结窗口）——两者均在页面如实标注能力边界，不假装外部系统

## 路线图

- ✅ **v1.0.0（当前）**：42 应用全 live；智能助手 22 工具 + ChatBI（趋势/环比同比/TOP-N/交叉/主动澄清）；语义层；多空间；外部数据源；10 万行级性能验证
- ✅ **v1.1.0 生产就绪**：单端口生产部署（Docker / systemd）· 备份与恢复演练 · 登录防爆破 + 分级限流 · JWT 令牌服务端吊销（登出/自助改密/管理员重置/停用即失效）· 用户自助修改密码· 密钥静态加密（AES-256-GCM）· 安全响应头/CSP/HSTS · 结构化日志与前端异常上报 · GitHub Actions CI
- 🔜 计划中：PostgreSQL/pgvector 适配 · OIDC/SSO · 流式时序采集 · 更多数据连接器（PG/MySQL/Kafka）· 查询管道实时掩码 · 对象存储 V2

## 说明

- 演示数据为虚构企业「星辰智造集团」与个人生活模板包；`src/mocks/*` 仅供 seed 使用，页面运行时一律走 API
- 所有文案为简体中文；开发规范见 [CONVENTIONS.md](./CONVENTIONS.md)
- **完整技术文档**：[docs/TECHNICAL-GUIDE.md](./docs/TECHNICAL-GUIDE.md) —— 42 个模块逐个说明「功能 / 实现原理 / 能力边界 / 验证方式」，含 29 张真实截图、架构分层、横切能力与边界总表
- **项目状态报告**：[docs/PROJECT-STATUS.md](./docs/PROJECT-STATUS.md) —— 完成度评估、分域评分、遗漏任务清单与下一步路线图
- **部署手册**：[docs/DEPLOYMENT.md](./docs/DEPLOYMENT.md) —— Docker/systemd 部署、备份恢复演练、安全上线检查清单、数据处理与合规说明、监控告警接入、套餐配额管理
- **PG 迁移手册**：[docs/PG-MIGRATION.md](./docs/PG-MIGRATION.md) —— 迁移触发条件、工作量评估、导出桥用法、五阶段操作步骤
- **用户手册**：[docs/USER-GUIDE.md](./docs/USER-GUIDE.md) —— 面向业务使用者的上手路径、日常工作流与常见问题
- 本项目单进程零运维设计，适合本地部署、私有化交付与二次开发

<div align="center">

**OntoOS v1.0.0** · 如果这个项目对你有帮助，欢迎 Star ⭐

</div>
