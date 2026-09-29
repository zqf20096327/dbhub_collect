# OpenMES · 通用制造执行系统

面向**离散制造全制程**的通用制造执行系统（MES），覆盖：来料 → 零件加工 → 部件装配 → 表面处理 → 总装 → 检测 → 打标 → 包装 → 成品入库 → 出库发货。
支持**多产线（每产线独立工艺路线）**、**按 BOM 分车型/配置**、**单件序列号追溯**、**工位防错（Poka-yoke）**、
**按部门职责的权限矩阵**、简单 ERP（内置测试用，接口可替换真实 ERP）。

> 内置演示数据取自**汽车座椅滑轨行业**样例（厂区/产线/物料/客户均为虚构），仅用于功能演示；生产环境可导入任意行业 EBOM 与主数据。

> **开源协议：Apache License 2.0**（详见 [LICENSE](./LICENSE)）。
> 本仓库内置**完整演示数据库**（`mes.db`，含 8 个车型配置 BOM、库存、工单、单件与历史数据），
> **clone 后即可启动体验**，无需 Node 环境（前端构建产物已包含在 `backend/static`）。

---

## 界面预览

| 登录页 | 生产大屏（实时数据） |
|---|---|
| ![登录页](docs/screenshots/01-login.png) | ![生产大屏](docs/screenshots/02-production-board.png) |

| 物料主数据 | 生产工单 |
|---|---|
| ![物料主数据](docs/screenshots/03-materials.png) | ![生产工单](docs/screenshots/04-production-orders.png) |

| 综合分析报表 | 成本核算 |
|---|---|
| ![综合分析报表](docs/screenshots/05-report-board.png) | ![成本核算](docs/screenshots/06-cost-rollup.png) |

---

## 一、快速启动

### 方式 A：Windows 一键启动（已内置构建产物，无需 Node）

```
run.bat
```

打开 http://127.0.0.1:8001 ，登录任意演示账号（见下方账号表）。

### 方式 B：手动启动（任意平台）

```bash
python -m venv .venv
.venv\Scripts\activate            # Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8001 --app-dir .
```

> 说明：`backend/static` 已包含最新前端构建产物，clone 即跑；若修改了前端源码，需 `cd frontend && npm install && npm run build` 重新构建（构建产物输出到 `backend/static`）。

### 演示账号

| 账号 | 角色 | 初始密码 | 职责 |
|---|---|---|---|
| `admin` | 系统管理员 | admin123 | 全功能 + 系统管理 |
| `dev` | 开发部 | 123456 | BOM/车型配置/产品信息/关键件定义 |
| `sales` | 营业部 | 123456 | 客户订单、客户归属、跟单看工单/排产 |
| `tech` | 生产技术部 | 123456 | 工艺/设备/内外制/制造成本、计划并行 |
| `mfg` | 制造部 | 123456 | 生产执行/车间管理 |
| `quality` | 质量部 | 123456 | 检验/不良/追溯/关键件追加 |
| `purchase` | 采购部 | 123456 | 采购、采购单价维护 |
| `logistics` | 物流部 | 123456 | 计划/进销存/发货/库位/安全库存 |
| `finance` | 财务部 | 123456 | 成本（全见只读）、采购单/工单只读 |
| `gm` | 工厂总经理 | 123456 | **全局只读** + 成本全见 |
| `planner`/`warehouse` | 计划员/仓管（兼容） | 123456 | 计划/仓储 |

> ⚠️ **正式使用前必须**：修改所有默认口令；设置环境变量 `MES_SECRET` 为长随机串（JWT 签名密钥，默认值仅用于开发演示）。

## 二、功能总览（阶段 0-10 全部完成）

| 模块 | 说明 |
|---|---|
| 组织与资源 | 工厂/车间/产线/工位/设备，工位含防错标记；部门按「车间 + 职能部门」划分 |
| 主数据 | 物料（EBOM 自动抽取，含所属车型列、共用件多车型展示）、供应商、厂内部门、客户、车型、配置列、工艺路线（每产线独立，工序绑工位/防错物料） |
| BOM 管理 | 标准模板下载、导入时录入车型名称 + 必选客户 + 多选 sheet、按配置展开 BOM 树、物料需求展开、损耗率 |
| 计划/ERP | 销售订单 → 生产工单 → MRP 缺料 → 采购 → 收货；缺料汇总；库存齐套（净需求口径：总成库存先抵扣 → 逐层抵扣 → 共用件跨配置合并统一抵扣）；简单 ERP 契约可替换 |
| 生产执行 | 工单开工生成序列号、工位作业（防错扫码核对 + 报工）、单件正/反追溯（含设备参数曲线）、单件管理、工序任务卡 |
| 仓储物流 | 库存余额、流水台账（统一留痕）、出入库/调拨/盘点、批次 FIFO/有效期、库位容量、工单发料、完工自动入成品仓 |
| 设备采集 | 设备 OEE 看板（实时模拟采集）、状态控制、事件日志、OEE 趋势、MTBF/MTTR、停机分析 |
| 质量管理 | 检验计划（CC/SC 关键特性）、检验单（IQC/IPQC/FQC）、首件/巡检、SPC（CPK）、不良柏拉图、不良与返工闭环、质量追溯报告 |
| 看板报表 | 生产大屏（实时刷新）、Andon 安灯闭环、报表中心（产量/不良/OEE/采购到货 Excel 导出）、产量报表与 KPI |
| 页面规整 + 权限矩阵（阶段十） | 左侧导航按部门职责组织（10 组）并按角色显隐；物料主数据**字段级**数据维护责任；关键件**记录级**主权（开发定义/质量追加，交叉不可删减）；工单**发放执行人**；追溯分级（质量全权限/制造技术仅产线相关）；成本分级查看（总成/采购/制造成本分角色） |

## 三、端到端演练（验收）

```
.venv\Scripts\python.exe -X utf8 backend\test_e2e.py
```

覆盖：销售订单→生产工单→MRP→（缺料则采购收货+IQC）→工单发料→开工→8 工序
（不良+返工 / 防错拦截·放行 / 测量）→完工→FQC→成品自动入库→正追溯→报表导出。

## 四、技术栈与目录

- 后端：Python 3.11 + FastAPI + SQLAlchemy + SQLite（`mes.db`，可 `MES_DB_PATH` 覆盖）
- 前端：Vue3 + Vite + Element Plus + ECharts（构建产物 → `backend/static`）
- 认证：JWT + PBKDF2；报表导出：openpyxl

```
slide-rail-mes/
├── run.bat                 # Windows 一键启动（建 venv/装依赖/启动）
├── LICENSE                 # Apache-2.0
├── requirements.txt
├── mes.db                  # SQLite 演示库（首次启动自动建；已含完整演示数据）
├── backend/
│   ├── main.py             # FastAPI 入口（API + 静态托管 + 采集模拟器）
│   ├── auth.py             # JWT + 密码哈希
│   ├── roles.py            # 统一角色/部门常量与模块权限集合（阶段十）
│   ├── seed.py             # 种子数据 + 建表 + 列迁移
│   ├── routers/            # auth org master bom plan mfg warehouse equipment quality reporting cost tools
│   ├── test_*.py           # 各阶段验收脚本 + test_e2e.py
│   └── static/             # 前端构建产物（clone 即跑）
├── frontend/               # Vue3 源码（npm run build → backend/static）
├── bom/EBOM模版.xlsx       # 标准 EBOM 导入模板
├── deploy/                 # 部署件：Nginx 配置、NSSM Windows 服务安装/卸载、启停脚本
└── docs/                   # 00-roadmap + 01~11 各阶段文档（部署/用户手册/权限矩阵）
```

## 五、主要 API（前缀 /api）

```
POST /api/auth/login
GET  /api/org/factories | lines | stations | equipment
GET  /api/master/materials | suppliers | customers | vehicle-models | bom-configs | routings
POST /api/bom/preview | import          GET /api/bom/headers/{id}/tree?config_id=&root_part_no=
POST /api/plan/sales-orders | /{sid}/generate    GET /api/plan/shortage-summary
POST /api/plan/purchase-orders | /{pid}/receive
POST /api/mfg/production-orders/{id}/start       GET /api/mfg/trace/{serial}
POST /api/mfg/units/{id}/poka-check | /report
POST /api/master/material/{mid}/key-part         # 关键件记录级（开发/质量）
GET  /api/wh/stock | /transactions | /batches    POST /api/wh/in|out|transfer|inventory
GET  /api/equipment/monitor | /oee-summary
POST /api/quality/inspections | /units/{id}/rework
GET  /api/cost/rollup                            # 成本分级（按角色屏蔽字段）
GET  /api/dash/overview | /api/andon | /api/export/*(xlsx)
```

## 六、开发

```bash
# 前端热更新（需后端 :8001 已启动）
cd frontend && npm run dev   # http://127.0.0.1:5173 （/api 代理到 8001）

# 重新构建前端
cd frontend && npm run build
```

## 七、部署（正式环境）

- 完整部署 / Nginx / Windows 服务（NSSM）/ 上线前检查：见 `docs/09-stage9-deployment.md`
- 用户手册（含角色权限）：见 `docs/用户手册.md`
- 页面与权限矩阵：见 `docs/11-page-governance.md`

## 八、路线图

见 `docs/00-roadmap.md`（9 阶段）。阶段 0-9 全部完成（2026-08-27）；阶段十（页面规整 + 部门权限矩阵）已完成。
后续规划：Windows 安装程序封装、多版本授权（基础版/企业版）、网络访问控制等（见 `docs/10-optimization-roadmap.md`）。
