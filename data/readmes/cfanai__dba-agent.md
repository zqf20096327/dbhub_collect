# DBA-Agent

**本地优先的数据库诊断与治理 Agent** · 只读默认 · 动作可审计 · 结果可复现

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](./LICENSE)

---

## 这是什么

DBA-Agent 不是一个"会聊天的数据库助手"。它是一套**受治理约束的数据库诊断 Agent**，
按以下五层结构建造：

```
Agent 决策大脑  +  版本化能力包  +  确定性执行器  +  独立审计 Agent  +  证据链
```

核心设计取舍只有一句话：**用可审计性换自由度**。

它**刻意不使用自由的 Function Calling / 自由 SQL 生成**——因为那会让"Agent 到底做了什么"
变得无法复核。取而代之的是：

- 模型只做两件事：**从闭集里选能力**、**输出受 schema 约束的结构化结果**；
- 真正碰数据库的动作全部由**确定性执行器**完成，逐条可列、可复跑；
- 每个动作都有 **fail-closed 停止条件**（如 `database_write_requested`、`generic_sql_requested`）。

## 快速了解它的规模

| 维度 | 现状 |
| --- | --- |
| 注册能力包 | **100 个**（`project_capability_catalog.v1.json`），每个含版本号、执行器入口、证据 schema、恢复分支、停止条件与 SHA-256 实现指纹 |
| 数据库覆盖 | MySQL、PostgreSQL、Oracle、达梦 DM8、KES、openGauss、TiDB、OceanBase、Redis、MongoDB、Elasticsearch，另有跨引擎能力 |
| 审计模型 | 内置异构审计 Agent（`granite3.2:8b`，本地 Ollama），支持 `strict` / `standard` / `rapid` 三档，覆盖 `plan` / `checkpoint` / `full_event` / `training` / `retest` 五个阶段 |
| 工作台 | 本地 Vue 单页应用，会话绑定 + 单源校验（Host / Origin / 会话令牌三重校验） |
| 离线检索 | 内置 MCP 离线文档库（SQLite FTS5 词法检索，带 provenance 溯源） |

## 一个可复现的端到端例子

**MySQL 慢 SQL 只读闭环**（`Q1` 场景），经工作台页面真实跑通的完整链路：

```
preflight   → READY_FOR_AUDIT_CHECKPOINT   （建立真实 TLS 会话、核验身份与只读链路）
plan_audit  → audit_checkpoint             （内部独立审计 Agent 出判并留回执）
capture     → captured                     （performance_schema 只读摘要采集）
archive     → archived                     （生成 7 态状态清单并归档）
```

归档回执里的关键字段：

- `status = READONLY_CLOSURE_ARCHIVED`
- `executor_invoked = false`、`writing_or_repair_executed = false` —— **全程零写入**
- `capture.digest_text_hash` —— 按 digest 指纹归一的 TOP SQL 指纹
- 7 态状态清单：`preflight → agent_selected → audit_checkpoint → running →
  monitoring_observed → safe_stop_or_complete → archived`
- 每个阶段的证据文件都带 SHA-256，可逐层回溯

## 设计原则

1. **只读默认。** 诊断链路不写数据库；修复需要另外的授权门。
2. **证据优先于结论。** 事实来自确定性采集，模型只负责解释与编排。
3. **失败即停。** 命中停止条件就停，不猜、不重试、不兜底。
4. **审计独立。** 行动 Agent 与审计 Agent 分离，审计在计划阶段就介入。
5. **本地优先。** 可在无公网环境下运行；对外连接必须显式授权且限定目标。

## 已知边界（重要，请先读这一段）

本项目在文档中坚持区分**"已实现并测试"与"已在真实环境验证通过"**，绝不混用。当前明确**未**做到：

- **工作台闭环目前只对 `Q1` 场景开放。** `Q2`–`Q6` 能通过预检，但闭环路由当前硬绑定 `Q1`。
- **工作台路径不含任何修复动作。** 建索引、更新统计信息、清理等写操作不在只读闭环内。
- **Agent 学习状态为 `NOT_PROVEN`。** 有产品能力证据，但没有"模型自主学会"的证明。
- **不主张企业生产就绪。** 当前是个人实验室范围的验证。
- 部分能力的状态是 `IMPLEMENTED_TESTED`（已实现并测试），不是 `LIVE_PASS`（真实环境通过）。
- 实验室三台 MySQL 目标是**克隆体**（共享同一 server_uuid 与服务器证书），
  因此"三目标"在证据独立性意义上并非三个独立实例。

> 把这些写清楚，比写成"全面支持多数据库、生产可用"更接近本项目真正想表达的东西。

## 目录结构

```
src/dba_agent/          能力包、确定性执行器、Agent、审计、工作台服务端
  ├─ agents/            行动 / 审计 Agent、上下文构建、输出校验
  ├─ deployment/        各数据库的部署与诊断执行器
  ├─ analysis/          离线静态检查器（SQL 风险、结构、索引、日志分类等）
  ├─ workbench/         本地工作台 HTTP 服务
  └─ mcp_offline/       MCP 离线文档库与 FTS5 检索
tests/                  测试套件
schemas/                证据与请求的 JSON Schema
workbench/phase10_vue/  工作台前端
docs/                   规范、任务回执与审计记录
tools/                  运维与验证脚本
```

## 快速开始

### Windows：双击即用

下载后**双击仓库根目录的 `start.bat`** 即可。它会自动完成：

1. 检查 Python（需要 3.10+，缺了会给出安装提示）
2. 首次运行创建虚拟环境并安装依赖
3. 首次运行生成工作台本地账号，并把登录密码显示在窗口里
4. 启动工作台并自动打开浏览器

首次运行约 2–3 分钟（在装依赖），之后每次启动都是秒开。关闭窗口即停止服务。

### 其他平台：命令行

```bash
# 1) 安装依赖
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt     # Windows: .venv\Scripts\python.exe

# 2) 首次运行：创建本地工作台账号（只需一次）
#    会提示设置密码，只保存校验子，不保存明文
.venv/bin/python tools/bootstrap_workbench_root_auth.py

# 3) 启动工作台
PYTHONPATH=src .venv/bin/python tools/serve_phase10_workbench.py --port 17865
```

然后浏览器打开 `http://127.0.0.1:17865/`，用 `root` 和刚才设置的密码登录。

> **启动模式说明**
>
> - 默认是 **`demo` 模式**：页面、能力目录、离线知识库都能用，
>   但**不会连接任何真实数据库**。
> - 要连接真实目标需要显式启用 **`live` 模式**：准备离线 vendor 的 `asyncssh` 运行时、
>   本地凭据录入、目标登记，并用 `--runtime-receipt <回执路径>` 启动。
>   这套配置目前只在个人实验环境验证过，尚未提供开箱即用的一键配置。
> - 想让内置审计 Agent 出判断，需要本机安装 [Ollama](https://ollama.com)
>   并准备 `granite3.2:8b`（审计）与 `qwen3:8b`（执行）两个模型。
>   未安装时工作台仍可启动，只有涉及模型判断的阶段不可用。

### 依赖说明

核心依赖只有 `pymysql` 与 `cryptography`。`asyncssh` 由项目**离线 vendor**
（不使用包索引安装），仅 live 模式需要。请参见 `requirements.txt` 中的注释。

## 免责声明

本项目面向**已获授权的个人实验环境**。使用者须自行确保对目标数据库拥有合法授权。
项目默认只读，但"只读"不等于"无风险"——在生产环境使用前请自行评估。

## 许可证

GNU Affero General Public License v3.0（AGPL-3.0），详见 [LICENSE](./LICENSE)。

简单说：你可以自由使用、修改、分发；但如果你把它改造成对外提供服务的产品，
**必须同样以 AGPL 开源你的修改**。如需闭源商用，需要单独的商业授权。
