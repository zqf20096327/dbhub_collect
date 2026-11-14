# LawAgent · 法律 RAG 与合同审查

[![CI](https://github.com/yuweian195/law-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/yuweian195/law-agent/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB)
![RAG](https://img.shields.io/badge/RAG-BM25-6B4F2A)
![LangGraph](https://img.shields.io/badge/Agent-LangGraph-1C3C3C)
![FastAPI](https://img.shields.io/badge/API-FastAPI-009688)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B)
![TypeScript](https://img.shields.io/badge/Frontend-TypeScript-3178C6)
![React](https://img.shields.io/badge/React-19-61DAFB)

面向劳动争议与合同审查场景的本地法律助手。输入一个法律问题或一份合同，系统会检索本地法条、给出带引用的意见、扫描条款风险，并在可计算时给出金额测算。

项目重点不是“让大模型自由发挥”，而是把 **检索、规则、计算、引用** 串成一条可审计的链路：结论必须能落到具体法条，金额必须能展示计算过程。

<p align="center"><a href="docs/screenshots/legal-opinion.png"><img src="docs/screenshots/legal-opinion.png" alt="法律意见书" width="900"></a></p>

<p align="center"><a href="docs/screenshots/contract-review.png"><img src="docs/screenshots/contract-review.png" alt="合同审查意见书" width="900"></a></p>

<p align="center"><a href="docs/screenshots/contract-console.png"><img src="docs/screenshots/contract-console.png" alt="TypeScript 合同审查控制台" width="900"></a></p>

<p align="center"><a href="docs/screenshots/legal-opinion.png">查看法律意见书原图</a> · <a href="docs/screenshots/contract-review.png">查看合同审查原图</a> · <a href="docs/screenshots/contract-console.png">查看 TypeScript 控制台原图</a></p>

> 仓库内法条为条文节选，合同与问题均为合成样本，用于工程评估；不构成正式法律意见。

## 技术栈

| 层 | 技术 |
|---|---|
| Agent / API | Python 3.11、FastAPI、LangGraph |
| 检索 | BM25 + 中文同义扩展 |
| 前端 | TypeScript 5、React 19、Vite、Streamlit |
| 存储 | SQLite（WAL 模式） |

## 业务背景

法律咨询和合同审查有两个硬约束：

1. **不能编法条**：回答必须能定位到具体法律、具体条文，否则对用户没有价值，甚至有风险。
2. **不能只给结论**：合同风险要说明“哪一条、为什么有风险、依据是什么、怎么改”；赔偿金额要给出计算过程。

LawAgent 的做法：

- 本地法条库 + BM25 检索，回答只引用检索到的条文；
- 规则引擎负责合同风险识别，LLM 只负责组织语言；
- 金额计算由独立计算器完成，结果附带公式与假设；
- 所有问答与审查记录落库，可回溯。

## 核心能力

- **法条 RAG**：33 条劳动法、劳动合同法、社会保险法、民法典合同编条文，中文字符二元组 BM25 检索，标题/标签加权。
- **带引用的法律问答**：识别解除补偿、试用期、竞业限制、服务期、社保、加班、违约金等意图，输出结论、分析、法条索引。
- **金额测算**：经济补偿 N、违法解除 2N、未提前通知 N+1，展示年限折算、公式和假设。
- **合同风险审查**：条款拆分、规则扫描、风险等级、修改建议、法条依据。
- **风险规则**：试用期超限、试用期工资低于 80%、服务期违约金无培训依据、竞业限制无补偿/超两年、随时解除、不缴社保、加班费包干、单方调岗、最终解释权、违约金过高、自动续约。
- **引用守卫**：检索不到高相关法条时，不生成确定性结论，提示补充事实或咨询律师。
- **TypeScript 合同审查控制台**：React + Vite 案卷索引与审查意见阅读器，逐条展示风险、修改建议和法条依据。
- **完整工程化**：FastAPI、Streamlit、SQLite、TypeScript、pytest、Ruff、Docker Compose、GitHub Actions。

## 架构

<p align="center"><a href="docs/diagrams/architecture.svg"><img src="docs/diagrams/architecture.svg" alt="architecture" width="960"></a></p>

## 工作流

### 法律问答

<p align="center"><a href="docs/diagrams/qa-workflow.svg"><img src="docs/diagrams/qa-workflow.svg" alt="qa-workflow" width="960"></a></p>

### 合同审查

<p align="center"><a href="docs/diagrams/review-workflow.svg"><img src="docs/diagrams/review-workflow.svg" alt="review-workflow" width="960"></a></p>

每个节点记录耗时与摘要，工作台可以展开“检索与生成轨迹”查看。

## 法条库

| 来源 | 条数 | 覆盖内容 |
|---|---:|---|
| 中华人民共和国劳动合同法 | 22 | 书面合同、试用期、服务期、竞业限制、解除、经济补偿、赔偿金 |
| 中华人民共和国劳动法 | 1 | 加班工资标准 |
| 中华人民共和国社会保险法 | 1 | 社保登记 |
| 中华人民共和国民法典（合同编） | 9 | 合同成立、格式条款、违约责任、违约金调整 |
| 合计 | 33 | 劳动争议与合同审查核心条文 |

检索实现：

- 中文字符二元组 + ASCII 词元，避免额外分词依赖；
- BM25（k1=1.5，b=0.75）；
- 标题命中 +0.35、标签命中 +0.20；
- 查询同义扩展：辞退/开除/劝退/被优化/N+1/社保/竞业协议等口语表达映射到法条术语；
- 返回相关度与覆盖率，供引用守卫判断。

## 合同风险规则

| 规则 | 风险 | 触发条件 | 依据 |
|---|---|---|---|
| `probation_limit` | 高 | 试用期超过合同期限对应上限 | 劳动合同法第 19 条 |
| `probation_salary` | 高 | 试用期工资低于约定工资 80% | 劳动合同法第 20 条 |
| `service_period_penalty` | 高 | 服务期违约金但无培训费用依据 | 劳动合同法第 22 条 |
| `non_compete_compensation` | 高 | 竞业限制未约定按月补偿 | 劳动合同法第 23 条 |
| `non_compete_term` | 高 | 竞业限制超过 2 年 | 劳动合同法第 24 条 |
| `unilateral_termination` | 高 | 随时解除且不承担补偿 | 劳动合同法第 48、87 条 |
| `social_insurance` | 高 | 不缴社保或员工自行承担 | 社会保险法第 58 条 |
| `overtime_pay` | 高 | 加班费包干/不支付 | 劳动法第 44 条 |
| `unilateral_change` | 中 | 单方调岗调薪 | 劳动合同法第 35 条 |
| `liquidated_damages` | 中 | 违约金比例可能过高 | 民法典第 585 条 |
| `final_interpretation` | 中 | 最终解释权条款 | 民法典第 496、497 条 |
| `auto_renewal` | 中 | 自动续约无退出机制 | 民法典第 496、509 条 |

风险评分：高风险 30 分/项、中风险 10 分/项，累计封顶 100；分数越高风险越大。

## 金额测算

| 场景 | 公式 |
|---|---|
| 协商解除 / 经济性裁员 | N × 月工资 |
| 违法解除 | 2N × 月工资 |
| 未提前 30 日通知 | N × 月工资 + 1 个月工资 |

N 的折算：每满一年计 1 个月；六个月以上不满一年按 1 年；不满六个月计 0.5 个月。

测算假设会随结果一起返回：月工资按解除前 12 个月平均工资、未考虑当地社平工资三倍封顶与 12 年上限、未包含未休年假/加班费/未签合同二倍工资等其他请求。

## 评估结果

评估集：15 个法律问题、3 份合成合同，其中包含“被辞退”“被优化”“N+1”“竞业协议不给钱”等口语化表达。完整报告见 [`reports/evaluation.md`](reports/evaluation.md)。

| 模块 | 指标 | 结果 |
|---|---|---:|
| 法条检索（纯 BM25） | Recall@3 | 93% |
| 法条检索（BM25 + 同义扩展） | Recall@3 | **100%** |
| 法条检索 | MRR | **0.867** |
| 合同规则 | Precision | **100%** |
| 合同规则 | Recall | **100%** |
| 法律问答 | 意图准确率 | **100%** |
| 法律问答 | 法条引用 Recall@3 | **100%** |
| 法律问答 | 金额计算准确率 | **100%** |
| 法律问答 | 平均耗时 | **7 ms** |

```bash
python scripts/evaluate.py
```

> 评估集规模较小，指标用于回归检查与量级参考，不构成法律意见，也不代表真实案件表现。

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

单独启动 API：

```bash
uvicorn app.main:app --reload
```

- Swagger：`http://127.0.0.1:8000/docs`
- 健康检查：`GET /health`

TypeScript 合同审查控制台：

```bash
cd web
npm install
npm run build
cd ..
python scripts/seed_demo.py
uvicorn app.main:app --reload
```

打开 `http://127.0.0.1:8000/console/`。开发模式：`cd web && npm run dev`（默认连接 `http://127.0.0.1:8000`）。

## 配置 LLM（可选）

复制 `.env.example` 为 `.env`：

```dotenv
LLM_API_KEY=sk-xxx
LLM_BASE_URL=https://api.deepseek.com/v1
LLM_MODEL=deepseek-chat
```

配置后，LLM 负责组织法律意见与审查结论的措辞；**检索、引用、风险规则和金额计算仍由本地逻辑完成**。未配置 Key 时使用确定性模板，全部功能可离线运行。

## API

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/health` | 服务状态、法条数量、LLM 模式 |
| GET | `/laws/search?q=&top_k=` | 法条检索 |
| POST | `/qa` | 法律问答 |
| GET | `/qa/history` | 咨询记录 |
| GET | `/qa/{id}` | 单条咨询 |
| GET | `/qa/{id}/report` | 导出法律意见书（Markdown） |
| POST | `/contract/review` | 合同审查 |
| POST | `/contract/review/upload` | 上传合同审查（PDF/DOCX/TXT） |
| GET | `/reviews` | 审查记录 |
| GET | `/reviews/{id}` | 单条审查 |
| GET | `/reviews/{id}/report` | 导出审查意见书（Markdown） |

示例：

```bash
curl -X POST http://127.0.0.1:8000/qa \
  -H "Content-Type: application/json" \
  -d '{"question":"公司违法解除劳动合同，工作3年2个月，月薪2万，能拿多少赔偿？"}'
```

## 目录结构

```text
law-agent/
├── app/
│   ├── main.py                 # FastAPI
│   ├── config.py
│   ├── schemas.py
│   ├── db.py                   # SQLite 仓储
│   ├── rag/
│   │   ├── corpus.py           # 法条 JSONL 加载
│   │   ├── tokenizer.py        # 中文二元组分词
│   │   ├── bm25.py             # BM25
│   │   └── retriever.py        # 检索 + 标题/标签加权
│   ├── graph/
│   │   ├── qa_state.py
│   │   ├── qa_nodes.py
│   │   ├── qa_workflow.py
│   │   ├── review_state.py
│   │   ├── review_nodes.py
│   │   └── review_workflow.py
│   ├── tools/
│   │   ├── contract_parser.py  # 合同/条款拆分
│   │   ├── risk_rules.py       # 风险规则
│   │   ├── question_parser.py  # 意图与事实抽取
│   │   ├── compensation.py     # 经济补偿/赔偿金
│   │   └── legal_answer.py     # 模板化法律意见
│   ├── llm/                    # 可选语言增强
│   └── services/
│       ├── qa.py
│       ├── review.py
│       ├── law.py
│       └── reporting.py
├── ui/streamlit_app.py         # 法律意见书风格工作台
├── data/
│   ├── laws/                   # 法条库
│   ├── contracts/              # 合成合同
│   ├── qa/                     # 评估问题
│   └── fixtures/               # 规则标签
├── scripts/
│   ├── evaluate.py
│   └── seed_demo.py
├── web/                        # TypeScript + React 合同审查控制台
│   ├── src/App.tsx
│   ├── src/api.ts
│   ├── src/styles.css
│   └── package.json
├── tests/                      # 24 个 Python 测试
├── reports/evaluation.md
├── docs/architecture.md
├── Dockerfile
├── docker-compose.yml
└── .github/workflows/ci.yml
```

## 设计取舍

- **BM25 而不是向量检索**：法条是短文本、术语稳定，BM25 可解释、零外部依赖、毫秒级；当前版本不引入额外嵌入模型，保持部署轻量。
- **规则识别风险，LLM 只组织语言**：风险判断必须可复现、可测试；LLM 不参与“有没有风险”的判定，也不生成法条编号。
- **引用守卫**：检索结果不足时不硬答，避免编造法条；所有回答附带免责声明。
- **法条库可替换**：JSONL 格式覆盖劳动争议与合同审查高频条文；替换为完整法规库时，检索与引用接口不变。
- **SQLite 单机存储**：便于本地部署与单机运行；仓储层已隔离，替换 PostgreSQL 不影响业务逻辑。

## 项目状态

当前版本为完整可运行的实现：Python 服务负责法条检索、带引用的问答、金额测算与合同审查；TypeScript 控制台负责案卷索引与审查意见阅读。两套构建与 CI 均已通过，仓库中的功能可直接运行。

## 工程边界

- 评估集为 15 个合成问题与 3 份合成合同，指标用于检索/规则回归检查，不代表真实案件泛化能力。
- 当前交付为单机 SQLite + 同步链路；生产使用需接入完整法规库、地域/时效元数据与权限控制。
- LLM 只参与意见措辞；生产使用需补充 token/延迟监控、Prompt 版本管理与人工复核闭环。

## 说明

仓库内法条为条文节选，合同、问题与评估标签均为合成数据，用于可复现的工程评估；接入真实业务数据前请替换 `data/` 目录，并遵守数据合规与律师执业规范。

本项目不提供正式法律意见。具体案件请咨询执业律师，并以劳动仲裁或法院认定为准。
