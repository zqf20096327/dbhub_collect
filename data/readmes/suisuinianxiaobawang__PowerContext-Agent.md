# PowerContext Agent

PowerContext Agent 是一个面向上下文工程、RAG 和工具调用的 Python 项目骨架。当前版本只实现可运行、可测试的基础组件，便于后续按赛题材料逐步加入真实业务逻辑。

## 与 PowerContext 赛题的对应关系

项目围绕大模型应用中的上下文组织问题预留了清晰模块。

- `src/agent` 负责规划、短期记忆和工具注册。
- `src/context` 负责上下文预算管理和知识检索。
- `src/database` 负责 OceanBase 连接配置。
- `configs` 保存不含密钥的运行参数。
- `tests` 用于验证基础行为，避免后续修改破坏已有能力。

具体比赛功能需要以官方赛题和数据为准。本仓库不预设评分规则，也不声明未经验证的效果。

## 系统架构

```text
用户请求
   |
   v
Agent Planner ---- Tool Registry
   |
   v
Context Manager ---- Conversation Memory
   |
   v
Retriever ---- Knowledge Base ---- OceanBase
```

## 如何运行

建议使用 Python 3.9 或更高版本。

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e .
python -m main --query "如何设计上下文管理模块"
pytest
```

OceanBase 连接参数通过环境变量提供。示例程序默认不会连接数据库。

```bash
export OCEANBASE_HOST=127.0.0.1
export OCEANBASE_PORT=2881
export OCEANBASE_USER=root@test
export OCEANBASE_PASSWORD=your_password
export OCEANBASE_DATABASE=test
```

## 后续开发计划

1. 阅读官方赛题材料并整理可验证的功能清单。
2. 接入真实模型服务和统一模型适配层。
3. 实现文档切分、向量化、召回和重排。
4. 接入 OceanBase，并建立可重复的数据导入流程。
5. 增加上下文压缩、记忆更新和工具调用评测。
6. 建立固定数据集、指标和自动化回归测试。

## 许可证

本项目采用 MIT License。参赛数据和第三方模型仍需遵守各自的许可要求。
