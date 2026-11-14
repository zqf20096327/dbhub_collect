# TelecomAgent · AIOps 告警压缩与根因定位

[![CI](https://github.com/yuweian195/telecom-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/yuweian195/telecom-agent/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB)
![AIOps](https://img.shields.io/badge/AIOps-Topology-0E7490)
![LangGraph](https://img.shields.io/badge/Agent-LangGraph-1C3C3C)
![FastAPI](https://img.shields.io/badge/API-FastAPI-009688)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B)
![TypeScript](https://img.shields.io/badge/Frontend-TypeScript-3178C6)
![React](https://img.shields.io/badge/React-19-61DAFB)

面向电信网络运维的告警分析 Agent。输入一天的原始告警，系统会按拓扑与时间窗压缩告警、定位根因、计算影响面、匹配历史案例并生成派单建议；低置信度事件自动转人工复核。

核心目标：把“几百条告警”变成“几起可处置的事件”，并且每一起来源、影响范围、判断依据都能追溯。

<p align="center"><a href="docs/screenshots/noc-overview.png"><img src="docs/screenshots/noc-overview.png" alt="NOC 值班总览" width="900"></a></p>

<p align="center"><a href="docs/screenshots/topology-view.png"><img src="docs/screenshots/topology-view.png" alt="拓扑视图" width="900"></a></p>

<p align="center"><a href="docs/screenshots/noc-live-feed.png"><img src="docs/screenshots/noc-live-feed.png" alt="实时告警流" width="900"></a></p>

<p align="center"><a href="docs/screenshots/noc-wallboard.png"><img src="docs/screenshots/noc-wallboard.png" alt="TypeScript NOC 大屏" width="900"></a></p>

<p align="center"><a href="docs/screenshots/noc-overview.png">查看 NOC 总览原图</a> · <a href="docs/screenshots/topology-view.png">查看拓扑视图原图</a> · <a href="docs/screenshots/noc-wallboard.png">查看 TypeScript 大屏原图</a> · <a href="docs/screenshots/noc-live-feed.png">查看实时告警流原图</a></p>

> 告警、拓扑与案例均为合成数据，用于工程评估；处置步骤需结合现场确认，不构成实际操作指令。

## 技术栈

| 层 | 技术 |
|---|---|
| Agent / API | Python 3.11、FastAPI、LangGraph |
| 前端 | TypeScript 5、React 19、Vite、Streamlit |
| 实时接入 | TypeScript / Node、WebSocket、批量转发 |
| 数据处理 | 拓扑关联、时间窗压缩、规则引擎 |
| 存储 | SQLite（WAL 模式） |

## 业务背景

网络运维的告警问题不是“告警不够多”，而是：

1. **告警风暴**：一根光缆中断可能触发几十条 OLT/基站告警，值班员看到的是噪声。
2. **根因难定位**：同一时间窗内多个网元告警，需要沿拓扑找上游根告警。
3. **处置要快且可审计**：派单前要说明影响了哪些网元、依据是什么、先做什么。

TelecomAgent 用“拓扑 + 时间窗 + 规则 + 案例”做压缩和定位，LLM 只负责组织值班摘要，不参与根因判定。

## 核心能力

- **拓扑感知压缩**：10 分钟时间窗内，按 CORE → TRANSPORT → OLT → BASE_STATION 的下游关系聚合告警。
- **根因定位**：识别光缆中断、电源故障、核心网信令过载、光路劣化、设备高温、配置变更等根因。
- **影响面计算**：基于拓扑 descendants 输出受影响网元与类型，区分根网元与下游。
- **置信度与人工复核**：低置信度或未归类的 P1/P2 事件自动进入人工复核分支。
- **案例检索**：按症状与根因类型匹配历史故障案例，返回处置步骤。
- **派单建议**：按严重度与时间排序，生成“先做什么”的处置清单。
- **NOC 值班台**：Streamlit 深色控制台，包含告警分析、拓扑视图、案例库与历史记录。
- **TypeScript NOC 大屏**：React + Vite 只读大屏，自动刷新最新分析结果，适合值班室展示。
- **实时告警流网关**：Node/TypeScript 持续消费 CSV 告警，批量调用 Python 分析，并通过 WebSocket 推送大屏。
- **完整工程化**：FastAPI、SQLite、pytest、Ruff、Docker Compose、GitHub Actions。

## 架构

<p align="center"><a href="docs/diagrams/architecture.svg"><img src="docs/diagrams/architecture.svg" alt="architecture" width="960"></a></p>

## 工作流

<p align="center"><a href="docs/diagrams/workflow.svg"><img src="docs/diagrams/workflow.svg" alt="workflow" width="960"></a></p>

每个节点记录耗时与摘要，控制台可以展开“分析轨迹”查看。

## 数据与拓扑

| 资产 | 规模 | 说明 |
|---|---:|---|
| 告警 | 223 条 | 3 起已标注根因事件 + 2 起光路劣化 + 1 起未归类 P1 + 4 组背景噪声 |
| 网元 | 83 个 | CORE / TRANSPORT / OLT / BASE_STATION 四层 |
| 拓扑边 | 81 条 | 核心→传输→OLT→基站 |
| 故障案例 | 6 条 | 光缆、电源、信令、光路、高温、配置变更 |

数据由 `scripts/generate_sample_data.py` 确定性生成，可直接替换为真实 CSV。

## 压缩算法

1. **时间窗**：默认 10 分钟，同一窗口内才做关联。
2. **根候选**：CORE / TRANSPORT / OLT 上的 P1/P2 告警，类型属于 `LINK_DOWN`、`LINK_DEGRADED`、`POWER_FAILURE`、`SIGNAL_OVERLOAD`、`HIGH_TEMPERATURE`、`CONFIG_CHANGE`。
3. **拓扑关联**：计算根候选的 descendants，把窗口内落在下游网元的告警归入同一事件。
4. **优先级**：按拓扑层级（CORE 优先）、严重度、时间排序；已归入事件的告警不重复分配。
5. **剩余告警**：P1/P2 进入“未归类/人工复核”；P3/P4 按告警类型聚合为背景噪声。
6. **压缩率**：`1 - 事件数 / 原始告警数`。

在当前样本上：223 条 → 10 起事件，压缩率 95.5%。

## 根因规则

| 根因 | 典型根告警 | 判断信号 | 处置方向 |
|---|---|---|---|
| 光缆中断 | TRANSPORT `LINK_DOWN` | 下游 OLT/基站批量退服、LOS、CRC 异常 | OTDR 定位、备用纤芯/环网倒换 |
| 电源故障 | OLT `POWER_FAILURE` | 市电中断、蓄电池放电、基站批量退服 | 确认市电、油机/应急电源 |
| 核心网信令过载 | CORE `SIGNAL_OVERLOAD` | CPU 高、SCTP 重传、呼叫失败 | 流控、排查呼叫风暴、扩容分流 |
| 光路劣化 | `LINK_DEGRADED` + CRC/误码 | 光功率下降、误码率上升 | 清洁/更换光模块、复测 |
| 设备高温 | `HIGH_TEMPERATURE` | 风扇异常、机房温度高 | 检查空调/风扇、降温 |
| 配置变更 | `CONFIG_CHANGE` | 变更后指标抖动/告警突增 | 核对变更单、必要时回滚 |
| 未归类 | P1/P2 无匹配规则 | 无明确根因信号 | 转人工复核 |

置信度由影响网元数、严重度、网元类型多样性、下游覆盖率、相似案例得分共同决定；低于阈值自动转人工。

## 案例检索

案例库为短文本症状签名，使用 **加权 Jaccard + 根因类型加成**：

- 症状/标签/标题分词后计算集合相似度；
- 根因类型完全匹配 +0.40；
- 根网元类型匹配 +0.10；
- 与拓扑规则互补，用于给出处置参考，不替代根因判断。

## 评估结果

评估集：223 条合成告警、83 个网元、6 条案例。完整报告见 [`reports/evaluation.md`](reports/evaluation.md)。

| 指标 | 结果 |
|---|---:|
| 告警压缩率 | **95.5%（223 → 10）** |
| 根因准确率 | **3/3（100%）** |
| 影响面平均召回 | **100%** |
| 案例检索 Recall@3 | **6/6（100%）** |
| 平均分析耗时 | **1 ms** |
| 低置信度转人工 | **是** |

```bash
python scripts/evaluate.py
```

> 评估集为合成数据，指标用于回归检查与量级参考，不代表真实网络环境。

## 快速开始

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -e ".[dev]"
streamlit run ui/streamlit_app.py
```

浏览器打开 `http://localhost:8501`。

TypeScript NOC 大屏：

```bash
cd web
npm install
npm run build
cd ..
python scripts/seed_demo.py
uvicorn app.main:app --reload
```

打开 `http://127.0.0.1:8000/wallboard/`。开发模式可运行 `npm run dev`（默认连接 `http://127.0.0.1:8000`）。

另开一个终端启动实时告警流网关：

```bash
cd gateway
npm install
npm run dev
```

网关会持续读取 `data/alarms/incident_day.csv`，每 20 条调用一次 `/ops/analyze`，并把结果通过 `ws://127.0.0.1:8081/ws/alarms` 推给大屏。

单独启动 API：

```bash
uvicorn app.main:app --reload
```

- Swagger：`http://127.0.0.1:8000/docs`
- 健康检查：`GET /health`

## 配置 LLM（可选）

复制 `.env.example` 为 `.env`：

```dotenv
LLM_API_KEY=sk-xxx
LLM_BASE_URL=https://api.deepseek.com/v1
LLM_MODEL=deepseek-chat
```

配置后，LLM 只负责生成值班摘要的措辞；**压缩、根因、影响面、派单与人工复核判断仍由本地逻辑完成**。未配置 Key 时使用确定性模板。

## API

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/health` | 服务状态、网元数、案例数 |
| GET | `/topology` | 网络拓扑 |
| GET | `/alarms/sample` | 样例告警 |
| GET | `/cases/search?cause=&q=&top_k=` | 故障案例检索 |
| POST | `/ops/analyze` | 分析告警（默认样例） |
| POST | `/ops/analyze/upload` | 上传 CSV 分析 |
| GET | `/ops/runs` | 分析记录 |
| GET | `/ops/runs/{id}` | 单次分析详情 |
| GET | `/ops/runs/{id}/report` | 导出 NOC 报告（Markdown） |

示例：

```bash
curl -X POST http://127.0.0.1:8000/ops/analyze \
  -H "Content-Type: application/json" \
  -d '{}'
```

## 目录结构

```text
telecom-agent/
├── app/
│   ├── main.py                 # FastAPI
│   ├── config.py
│   ├── schemas.py
│   ├── db.py                   # SQLite 仓储
│   ├── ops/
│   │   ├── alarms.py           # CSV 加载、去重、时间窗
│   │   ├── topology.py         # 拓扑图与 descendants
│   │   ├── compression.py      # 压缩、根因、置信度
│   │   ├── case_retriever.py   # 案例检索
│   │   └── runbooks.py         # 处置手册
│   ├── graph/
│   │   ├── ops_state.py
│   │   ├── ops_nodes.py
│   │   └── ops_workflow.py
│   ├── llm/                    # 可选值班摘要
│   └── services/
│       ├── ops.py
│       └── reporting.py
├── ui/streamlit_app.py         # NOC 值班台
├── data/
│   ├── alarms/                 # 合成告警 CSV
│   ├── topology/               # 网络拓扑
│   ├── cases/                  # 故障案例
│   └── fixtures/               # 评估标签
├── scripts/
│   ├── generate_sample_data.py
│   ├── evaluate.py
│   └── seed_demo.py
├── web/                        # TypeScript + React NOC 大屏
│   ├── src/App.tsx
│   ├── src/api.ts
│   ├── src/live.ts             # WebSocket 实时告警
│   ├── src/styles.css
│   └── package.json
├── gateway/                    # TypeScript / Node 实时告警网关
│   ├── src/server.ts
│   ├── package.json
│   └── Dockerfile
├── tests/                      # 21 个 Python 测试
├── reports/evaluation.md
├── docs/architecture.md
├── Dockerfile
├── docker-compose.yml
└── .github/workflows/ci.yml
```

## 设计取舍

- **拓扑规则优先，不做纯 LLM 诊断**：根因必须可复现、可解释；LLM 只写摘要，避免“模型编一个原因”。
- **先压缩再诊断**：直接在 223 条告警上做诊断既慢又噪声大；拓扑 + 时间窗先收敛到事件。
- **案例检索用 Jaccard 而非向量**：案例是短症状签名，Jaccard 可解释且零依赖；向量召回留给更大规模案例库。
- **低置信度必须转人工**：运维场景里“不确定”比“猜一个”更安全；未归类 P1/P2 自动进入复核。
- **双前端分工**：Streamlit 负责操作与调试，React/TypeScript 大屏负责值班室展示；两者共用 FastAPI。
- **SQLite 单机存储**：便于本地运行与部署；仓储层隔离，替换 PostgreSQL 不影响业务逻辑。

## 项目状态

当前版本为完整可运行的实现：Python 服务负责压缩、根因与派单；TypeScript/React 大屏负责展示；Node 网关负责实时告警接入与分析触发。三套构建与 CI 均已通过，仓库中的功能可直接运行。

## 工程边界

- 评估集为 223 条合成告警与 3 起标注事件，指标用于压缩与定位回归检查，不代表真实网络环境。
- 当前交付面向离线告警分析，使用静态拓扑；实时流式接入、动态拓扑与多故障并发拆簇属于生产集成范围。
- LLM 只生成值班摘要；生产使用需补充 token/延迟监控与告警反馈闭环。

## 说明

告警、拓扑、案例与标签均为合成数据，用于可复现的工程评估；接入真实网络数据前请替换 `data/` 目录，并遵守生产变更与安全规范。

本项目的处置步骤是通用建议，不构成对具体设备的操作指令；执行前需结合现场确认。
