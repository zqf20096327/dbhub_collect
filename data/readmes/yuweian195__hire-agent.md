# HireAgent · 智能招聘筛选 Agent

[![CI](https://github.com/yuweian195/hire-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/yuweian195/hire-agent/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB)
![LangGraph](https://img.shields.io/badge/Agent-LangGraph-1C3C3C)
![FastAPI](https://img.shields.io/badge/API-FastAPI-009688)
![Java](https://img.shields.io/badge/Java-21-ED8B00)
![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.3-6DB33F)
![TypeScript](https://img.shields.io/badge/Frontend-TypeScript-3178C6)
![React](https://img.shields.io/badge/React-19-61DAFB)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B)

面向中小团队招聘场景的智能筛选与面试评估系统。覆盖简历解析、六维评分、人岗匹配、批量排名、面试回答评估和候选人流程管理；全流程由 LangGraph 状态图编排，并保留每个节点的执行轨迹。

<p align="center"><a href="docs/screenshots/workbench.png"><img src="docs/screenshots/workbench.png" alt="HireAgent 工作台" width="900"></a></p>

<p align="center"><a href="docs/screenshots/interview-evaluation.png"><img src="docs/screenshots/interview-evaluation.png" alt="面试评估" width="900"></a></p>

<p align="center"><a href="docs/screenshots/pipeline-board.png"><img src="docs/screenshots/pipeline-board.png" alt="TypeScript 招聘看板" width="900"></a></p>

<p align="center"><a href="docs/screenshots/workbench.png">查看工作台原图</a> · <a href="docs/screenshots/interview-evaluation.png">查看面试评估原图</a> · <a href="docs/screenshots/pipeline-board.png">查看招聘看板原图</a></p>

> 仓库内简历与岗位均为合成样本，用于可复现的工程评估；接入真实数据时请替换 `data/` 目录，并遵守候选人隐私与数据合规要求。

## 技术栈

| 层 | 技术 |
|---|---|
| Agent / API | Python 3.11、FastAPI、LangGraph |
| 前端 | TypeScript 5、React 19、Vite、Streamlit |
| 企业集成 | Java 21、Spring Boot 3、H2 |
| 存储 | SQLite（WAL 模式） |

## 业务背景

招聘初筛的真实问题不是“能不能调通大模型”，而是三件事：

1. **结果要可解释**：HR 需要知道 8.2 分是怎么来的，而不是一个黑盒结论。
2. **流程要可审计**：同一份简历重复筛选，结论应该稳定；敏感条件（性别、年龄、婚育）不能进入评分。
3. **能力要可落地**：解析、评分、匹配、面试题生成要能串成一条链路，而不是散落的 prompt。

HireAgent 把这条链路做成一个完整的单机服务：规则负责可解释的数值，LLM 负责语言理解与表达，二者解耦。

## 核心能力

- **简历解析**：支持 PDF / DOCX / TXT / Markdown，抽取姓名、联系方式、学历、院校层次、工作年限、技能、项目与工作经历。
- **六维评分**：学历、经验、技能、项目、稳定性、潜力，权重固定、结果确定，单份简历毫秒级完成。
- **人岗匹配**：必备技能命中率、加分技能、经验年限、学历要求综合计算匹配度，并给出缺口说明。
- **条件路由**：`≥ 8.0` 推荐并生成面试题；`6.0–8.0` 待定；`< 6.0` 淘汰。路由逻辑在 LangGraph 条件边中显式表达。
- **JD 合规检查**：识别性别、年龄、第一学历、婚育、户籍等歧视性条件，并从评分依据中剔除。
- **面试题生成**：围绕候选人已命中技能、缺失技能和项目经历生成技术题、项目题、行为题、场景题与岗位理解题。
- **面试回答评估**：按相关性、深度、结构、表达四个维度逐题评分，输出通过/待定/不通过、优势、风险与追问建议。
- **批量筛选与排名**：一次导入多份简历，按综合评分排名并导出 CSV，适合校招/社招批量初筛。
- **候选人流程管理**：支持初筛、面试中、Offer、已淘汰、人才库五种状态，记录可回溯。
- **报告导出**：筛选报告与面试报告均可导出 Markdown，便于归档和面试评审。
- **可选的 LLM 增强**：兼容 OpenAI / DeepSeek / 通义等 OpenAI-compatible 接口；未配置 Key 时自动使用离线规则模式。
- **Java ATS 集成**：Spring Boot 3 + H2 管理岗位、候选人与筛选记录，Python Agent 通过 HTTP 接入；未配置时自动回退本地数据。
- **TypeScript 招聘看板**：React + Vite 五列 Kanban，展示候选人流程、评分与详情，支持推进/退回阶段。
- **完整工程化**：FastAPI、Streamlit、SQLite、Java Spring Boot、pytest、JUnit、Ruff、Docker Compose、GitHub Actions。

## 架构

<p align="center"><a href="docs/diagrams/architecture.svg"><img src="docs/diagrams/architecture.svg" alt="architecture" width="960"></a></p>

## Agent 工作流

<p align="center"><a href="docs/diagrams/workflow.svg"><img src="docs/diagrams/workflow.svg" alt="workflow" width="960"></a></p>

每个节点都会记录耗时与摘要，工作台中可以直接展开“Agent 执行轨迹”查看。

面试评估使用独立的 LangGraph 子图：

<p align="center"><a href="docs/diagrams/interview-workflow.svg"><img src="docs/diagrams/interview-workflow.svg" alt="interview-workflow" width="960"></a></p>

单题评分维度：相关性 35%、深度 30%、结构 20%、表达 15%。默认 `≥ 7.5 通过 / ≥ 6.0 待定`，可通过环境变量调整。

## 评分模型

| 维度 | 权重 | 计算依据 |
|---|---:|---|
| 学历背景 | 15% | 最高学历、院校层次（985/211）、是否满足岗位学历要求 |
| 工作经验 | 25% | 工作年限与岗位最低年限的比值，分段映射到 1–10 分 |
| 技能匹配 | 25% | 必备技能命中率 75% + 加分技能命中率 25%，必备命中率过低时封顶 |
| 项目质量 | 15% | 项目数量 + 主导/架构/重构/高并发/落地等深度信号 |
| 稳定性 | 10% | 工作经历段数与平均单段年限，跳槽频繁扣分 |
| 成长潜力 | 10% | 学历、院校、AI 相关技能、开源/专利/团队信号、当前职级 |

总分 = Σ（维度得分 × 权重）。阈值默认 `推荐 8.0 / 待定 6.0`，可通过环境变量调整。

岗位 JSON 可以覆盖默认权重，例如 `"weights": {"skills": 0.35, "experience": 0.2, "projects": 0.2}`，系统会自动归一化；未提供时使用默认六维权重。默认 `REDACT_PII=true`，发送给 LLM 的内容使用“候选人”而不是真实姓名，联系方式不会进入 Prompt。

## 快速开始

```bash
# 1. 创建环境
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# 2. 安装
pip install -e ".[dev]"

# 3. 启动工作台
streamlit run ui/streamlit_app.py
```

浏览器打开 `http://localhost:8501`，左侧选择岗位、载入示例简历，点击“开始筛选”。

也可以单独启动 API：

```bash
uvicorn app.main:app --reload
```

- Swagger：`http://127.0.0.1:8000/docs`
- 健康检查：`GET /health`

TypeScript 招聘看板：

```bash
cd web
npm install
npm run build
cd ..
python scripts/seed_demo.py
uvicorn app.main:app --reload
```

打开 `http://127.0.0.1:8000/board/`。开发模式：`cd web && npm run dev`（默认连接 `http://127.0.0.1:8000`）。

## Java ATS 集成服务（可选）

`ats-service/` 是一个独立的 Java Spring Boot 3 服务，负责岗位、候选人和筛选记录的持久化，使用 H2 文件数据库。它模拟企业招聘系统中的 ATS 集成层：

```bash
cd ats-service
mvn spring-boot:run
# 服务地址 http://127.0.0.1:8080
```

Python 侧配置 `ATS_BASE_URL` 后，会优先从 Java 服务加载岗位，并在筛选完成后回写结果：

```bash
ATS_BASE_URL=http://127.0.0.1:8080 uvicorn app.main:app --reload
```

Java 服务不可用时自动回退到 `data/jobs` 与本地 SQLite，不影响主链路。接口包括：

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/api/jobs` | 岗位列表 |
| POST | `/api/candidates` | 创建候选人 |
| POST | `/api/screenings` | 写入筛选结果 |
| PATCH | `/api/screenings/{id}/stage` | 更新候选人流程状态 |
| GET | `/api/health` | Java 服务健康检查 |

`docker compose up --build` 会同时启动 Java ATS（8080）、API（8000）与工作台（8501）。

## 配置真实 LLM（可选）

复制 `.env.example` 为 `.env`，填入任意 OpenAI-compatible 服务：

```dotenv
LLM_API_KEY=sk-xxx
LLM_BASE_URL=https://api.deepseek.com/v1
LLM_MODEL=deepseek-chat
```

配置后，**评语、面试题与面试反馈**会由 LLM 生成；**筛选与面试分数仍然由规则计算**，保证可复现、可测试。未配置 Key 或调用失败时，自动回退到离线模板。

## API 示例

```bash
curl -X POST http://127.0.0.1:8000/screen \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "张伟\n工作年限：6 年\n技能：Java、Spring Cloud、MySQL、Redis",
    "job_id": "java-senior"
  }'
```

响应包含：

```json
{
  "candidate_name": "张伟",
  "total_score": 9.13,
  "recommendation": "recommend",
  "dimension_scores": ["...六维评分..."],
  "skill_match": {"matched": ["..."], "missing": ["..."]},
  "job_match": {"overall_rate": 0.98},
  "compliance": {"passed": true, "issues": []},
  "questions": ["...5 道面试题..."],
  "trace": ["...9 个节点..."]
}
```

其他接口：

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/health` | 服务状态、LLM 模式、岗位数量 |
| GET | `/jobs` | 岗位列表 |
| POST | `/screen` | 文本简历筛选 |
| POST | `/screen/upload` | 文件上传筛选（PDF/DOCX/TXT） |
| POST | `/screen/batch` | 批量筛选并返回排名 |
| GET | `/screenings` | 最近筛选记录 |
| GET | `/screenings/{id}` | 单条筛选详情 |
| GET | `/screenings/{id}/report` | 导出筛选报告（Markdown） |
| PATCH | `/screenings/{id}/stage` | 更新候选人流程状态 |
| POST | `/interview/evaluate` | 面试回答评估 |
| GET | `/interviews` | 最近面试报告 |
| GET | `/interview/{id}` | 单份面试报告 |
| GET | `/interview/{id}/report` | 导出面试报告（Markdown） |

## 评估结果

评估集包含 5 份合成简历、2 个岗位，覆盖推荐 / 待定 / 淘汰三档。完整报告见 [`reports/evaluation.md`](reports/evaluation.md)。

| 指标 | 结果 |
|---|---|
| 决策准确率 | **5/5（100%）** |
| 分数区间命中 | **5/5（100%）** |
| 平均单份耗时 | **12 ms** |
| P95 耗时 | **27 ms** |

```bash
python scripts/evaluate.py
```

> 评估标签按岗位要求人工标注，分数区间用于检查评分量级是否合理；这不是大规模基准测试。

## 目录结构

```text
hire-agent/
├── app/
│   ├── main.py                # FastAPI 入口
│   ├── config.py              # pydantic-settings 配置
│   ├── schemas.py             # API / 工作流共享模型
│   ├── db.py                  # SQLite 仓储
│   ├── graph/
│   │   ├── state.py           # 筛选状态定义
│   │   ├── nodes.py           # 9 个筛选节点
│   │   ├── workflow.py        # 筛选图构建
│   │   ├── interview_state.py # 面试评估状态
│   │   ├── interview_nodes.py # 5 个面试评估节点
│   │   └── interview_workflow.py
│   ├── tools/
│   │   ├── resume_parser.py   # PDF/DOCX/TXT 解析与结构化
│   │   ├── skill_matcher.py   # 技能库与匹配
│   │   ├── scorer.py          # 六维评分
│   │   ├── jd_matcher.py      # 人岗匹配
│   │   ├── compliance.py      # JD 合规检查
│   │   ├── question_generator.py
│   │   └── answer_evaluator.py # 面试回答四维评分
│   ├── llm/
│   │   ├── client.py          # OpenAI-compatible 客户端 + 降级
│   │   └── prompts.py
│   ├── integrations/
│   │   └── ats_client.py      # Java ATS 客户端（可选）
│   └── services/
│       ├── screening.py       # 筛选业务编排
│       ├── interview.py       # 面试评估编排
│       └── reporting.py       # Markdown 报告导出
├── ui/streamlit_app.py        # 招聘工作台（筛选/批量/面试/候选人/岗位）
├── data/
│   ├── jobs/                  # 岗位 JD
│   ├── resumes/               # 合成简历
│   ├── interviews/            # 面试问答样本
│   └── fixtures/              # 评估标签
├── scripts/
│   ├── evaluate.py            # 离线评估
│   ├── batch_screen.py        # 批量筛选 CLI
│   └── seed_demo.py           # 生成看板示例数据
├── ats-service/               # Java Spring Boot ATS 集成服务
│   ├── src/main/java/...      # 岗位 / 候选人 / 筛选记录 API
│   ├── src/test/java/...      # MockMvc 接口测试
│   ├── pom.xml
│   └── Dockerfile
├── web/                       # TypeScript + React 招聘看板
│   ├── src/App.tsx
│   ├── src/api.ts
│   ├── src/styles.css
│   └── package.json
├── tests/                     # 26 个 Python 测试
├── reports/
│   ├── evaluation.md
│   └── batch_results.csv
├── Dockerfile
├── docker-compose.yml
└── .github/workflows/ci.yml
```

## 测试与 CI

```bash
pytest -q
ruff check app ui tests scripts
```

GitHub Actions 在每次 push / PR 时执行 Ruff、pytest、Java ATS 的 Maven 测试，以及 TypeScript 看板构建（共 26 个 Python 测试 + 5 个 Java 测试）。

## 设计取舍

- **数值用规则，语言用 LLM**：筛选评分与面试评分都必须稳定、可解释、可单测；LLM 只负责评语、面试题与反馈。这样既保留大模型的语言能力，又避免“同样回答两次评分不同”。
- **先做技能词典，不先上向量检索**：技能匹配需要可审计的命中/缺失列表；向量召回适合保留到 JD 语义匹配阶段再引入。
- **SQLite 而不是 PostgreSQL**：单机工作台足够，部署成本低；仓储层已隔离，替换数据库不影响业务流程。
- **Python Agent + Java ATS**：Python 负责 Agent、评分与工作流，Java Spring Boot 负责企业 ATS 集成；HTTP 解耦，Java 不可用时自动回退本地数据。
- **默认离线可跑**：没有 API Key 也能完成完整筛选、面试评估与测试，降低部署门槛，也方便 CI。
- **单机交付**：SQLite 单机版本开箱即用，仓储层已隔离；需要多租户或鉴权时可按部署环境替换，不影响现有主链路。

## 项目状态

当前版本为完整可运行的实现：Python Agent 负责简历解析、六维评分、批量排名与面试评估；Java Spring Boot ATS 服务负责岗位、候选人与筛选记录；TypeScript 招聘看板负责流程展示与推进。三套构建与 CI 均已通过，仓库中的功能可直接运行。

## 工程边界

- 评估集为 5 份合成简历与 2 个岗位，指标用于评分回归检查，不代表真实招聘场景的泛化能力。
- 当前交付为单机 SQLite + 同步链路，面向单团队部署；多租户、异步队列属于不同部署形态。
- LLM 只参与评语、面试题与面试反馈；生产使用需补充 token/延迟监控与 Prompt 版本管理。

## 说明

HireAgent 面向中小团队招聘场景，提供从简历初筛到面试评估的完整本地实现：规则评分保证可解释与可复现，LLM 仅用于语言增强。

仓库内简历、岗位与评估标签均为合成数据，用于可复现的工程评估；接入生产数据时请替换 `data/` 目录，并遵守候选人隐私与数据合规要求。欢迎通过 Issue 交流评分模型与 Agent 工作流的设计。
