# 🤖 LangChain Deep Agents 学习项目

> 以**课程式路线**循序渐进地学习 [LangChain Deep Agents](https://github.com/langchain-ai/deepagents) 框架(`deepagents`),每课一个可运行示例 + 中文注释讲解。

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-✓-1C3C3C)](https://github.com/langchain-ai/langchain)
[![deepagents](https://img.shields.io/badge/deepagents-✓-0C6E4D)](https://github.com/langchain-ai/deepagents)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/Pjk-llm/deepagents-learn)](https://github.com/Pjk-llm/deepagents-learn)
[![GitHub Forks](https://img.shields.io/github/forks/Pjk-llm/deepagents-learn)](https://github.com/Pjk-llm/deepagents-learn)

## 📚 课程一览

| 课程 | 目录 | 状态 | 内容 |
|---|---|---|---|
| **基础课程** | [`minimal-deepagent/`](minimal-deepagent/) | ✅ **已完成** | 第 0–11 课:最小智能体 → 工具设计 → 多轮对话 → 文件系统与权限 → Backend 持久化 → 长期记忆 → Skills → 多智能体 → HITL → 自定义中间件 → 生产化 |
| **进阶课程** | [`advanced-deepagent/`](advanced-deepagent/) | ✅ **已完成** | 两轨学习:① 各组件**使用原理**(`01-principles/`)② 各功能**详细示例**(`02-middlewares/`…`07-integration/`) |

### 进阶课程进度

| 轨道 | 进度 |
|---|---|
| **① 使用原理** `01-principles/` | p1 agent 循环与图结构 ✅ · p2 中间件模型(钩子/执行顺序/洋葱模型)✅ · p3 上下文工程 ✅ · p4 Backend 抽象 ✅ · p5 记忆系统 ✅ · p6 多智能体 ✅ · p7 结构化输出 ✅ · p8 持久化 ✅ |
| **② 详细示例** `02-…07-` | 19 中间件 ✅ · 9 Backend ✅ · 5 编排 ✅ · 3 结构化输出 ✅ · 6 生产化 ✅ · 3 集成 ✅ |

每个课程目录自带 `README.md`(启动方式)、`LEARNING_ROADMAP.md`(进度与要点)、`requirements.txt` 与独立 `.venv`,互不干扰。

## 🗂️ 项目结构

```text
deepagents-learn/
├── minimal-deepagent/          # ✅ 基础课程(第 0–11 课)
│   ├── agent.py                #    第 0 课:最小工具调用 agent
│   ├── lesson01_loop.py … lesson11_production.py
│   ├── README.md / LEARNING_ROADMAP.md / requirements.txt / .env.example
│   └── .venv/                  #    (不提交)
├── advanced-deepagent/         # ✅ 进阶课程
│   ├── 01-principles/          #    ① 使用原理
│   │   ├── p1-agent-loop/
│   │   └── p2-middleware-model/
│   ├── 02-middlewares/ … 07-integration/   #    ② 详细示例(19 中间件 / 9 Backend / 5 编排 / 3 结构化 / 6 生产化 / 3 集成)
│   └── README.md / LEARNING_ROADMAP.md / requirements.txt / .env.example
├── README.md
├── LICENSE                     # MIT
└── .gitignore
```

## ⚙️ 环境要求

- **Python 3.11+**(`deepagents` 要求 ≥3.11;3.12 / 3.13 均可)
- 一个 **DeepSeek API Key**(申请: <https://platform.deepseek.com>);也可换成任意 OpenAI 兼容模型,改 `model` 参数即可
- 各课程目录的依赖清单见各自的 `requirements.txt`

## 🚀 快速开始(以 minimal-deepagent 为例)

```bash
cd minimal-deepagent
python -m venv .venv
source .venv/Scripts/activate    # Windows (Git Bash)
# .venv/bin/activate             # Linux/macOS

pip install -r requirements.txt

cp .env.example .env             # 填入 DEEPSEEK_API_KEY,切勿提交 .env
python agent.py                  # 第 0 课:最小工具调用 agent
```

详细说明与分课目录见 [`minimal-deepagent/README.md`](minimal-deepagent/README.md)。

## 🧭 学习路线

每门课程在各自目录下维护 `LEARNING_ROADMAP.md`,记录进度与每课要点:

- **基础课程** → [`minimal-deepagent/LEARNING_ROADMAP.md`](minimal-deepagent/LEARNING_ROADMAP.md)
- **进阶课程** → [`advanced-deepagent/LEARNING_ROADMAP.md`](advanced-deepagent/LEARNING_ROADMAP.md)

## 📌 仓库约定

- `.env`(含 API Key)、`.venv/`、`__pycache__/`、`.idea/`、`workspace/` 一律不提交(见根目录 [`.gitignore`](.gitignore))。
- 每门课程一个独立子目录,自带 `requirements.txt` / `.env.example` / `.venv` / `README.md` / `LEARNING_ROADMAP.md`,互不共享环境。
- 提交使用 conventional 风格:基础课 `feat: 第N课 —— 主题`,进阶课 `feat: 进阶 mNN —— 主题`。

---

如果觉得这个项目对你有帮助,欢迎点个 **⭐ Star** 支持,也欢迎提 Issue / PR 一起完善。

## 📄 License

[MIT](LICENSE)
