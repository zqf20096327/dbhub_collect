# GaussDB 源码知识工程 2.4.0

源码、用户手册、历史特性名称、`compile_commands.json` → **模块 / 功能特性 / 主干流程学习计划** → 当前 Agent 与原生子 Agent 研究 → 实际审阅 → SQLite 知识库、Wiki 与开发 / 测试 / review / 运维前置知识。

**[直接在 Claude 使用](CLAUDE-START.md) · [迁移与完整命令](MIGRATE-GAUSSDB.md) · [技术设计](docs/DESIGN-2.4.md) · [实测结果](docs/VALIDATION-2.4.md)**

## 最短使用路径

准备 Python 3.12、Git、已有 Claude Code 和完整工程。发行 ZIP 带 Python 核心依赖的离线 wheels；源码、模型、认证、Claude 和调用图不打包。

将 `paths.example.json` 复制为 `local/paths.json`，填写 source、manual、features、compile_db、home。设计文档和 ECS 图可选。Linux 编译路径与 Windows 源码路径不同，用 path_maps 映射；未定位项保留。

在 Claude 中粘贴，只改工程和配置路径：

```text
请读取 E:/kb/engine/skills/gauss-knowledge/SKILL.md。
工程 E:/kb/engine；配置 E:/kb/engine/local/paths.json。
先生成并展示全仓计划。然后按我选的模块开始学习，多个模块用当前宿主原生 Agent 并行。
沿用工程证据、租约和研究/知识两阶段审阅，最后导出 Wiki 和四角色知识查询。
不要另起 Claude、模型 API 或全仓 TU 解析。
```

也可安装入口后使用 `/gauss-knowledge`。初始规划不调用模型，实际理解代码由当前 Agent 执行。没有原生子 Agent 的宿主使用串行流程。

## 输出

| 产物 | 位置和含义 |
| --- | --- |
| 模块功能课程 | `home/curriculum/index.html`、`PLAN.md`、`PLAN.json`、`WORK-PACKAGES.csv`；可筛选、调整、选模块 |
| 全仓责任与覆盖 | `home/whole/PLAN.json`、`COVERAGE.csv`；包括无调用边、无历史特性名的文件 |
| 构建输入账 | `home/setup/inputs/inputs-*/manifest.json`；保留特性原始行、编译上下文、宏、路径映射及未定位项 |
| 权威知识 | `home/knowledge.sqlite3`、冻结原文 `blobs/`、知识修订 `wiki.git/` |
| 已审 Wiki | `home/wiki/index.html`；同一修订的 Markdown、HTML、`knowledge.json` 和四角色视图 |
| Agent 输入 | `ask` / MCP `get_context`；包含条件、源码证据、影响、角色必需内容和未知 |

SQLite 是权威记录，Wiki 是同一已审知识的阅读投影。初始计划、未审草稿和调用图不会自动成为已审 Wiki。

## 学习流程

1. 冻结输入，登记领域、模块、特性候选、公共机制和主干流程，按行为线索及文件/字节预算生成工作包候选。
2. 用户选择模块，Agent 完整盘点范围，结合源码确认或调整功能课程。初始目录和文件名分组不冒充已确认特性树。
3. 按机制研究，包内用有界阅读计划和局部 SCC 后序，保留环内成员、跨文件边、未编译代码与宏分支。
4. 提交正文及覆盖解释，经实际研究审阅和知识审阅后入库。就绪模块可以深入，不必等全仓盘点完。
5. 用四角色查询、实现解释账、跨模块契约及覆盖验收暴露缺口，继续补学。知识内容变化使旧覆盖失效。

**函数、TU、调用边、阅读区间不会各建一项任务。** 物理区间只检查遗漏，要关联行为、条件、状态、消费者、清理、测试依据和实质知识。全文读取、标签和一句摘要不能关闭解释覆盖；语义正确性仍需实际审阅。

## ECS 与多人

`compile_commands.json` 在 Windows 只登记上下文，不执行命令。本工程自带 `ecs.sh`、GCC 插件和 Clang 产图程序；需实际 Linux 构建环境及对应编译器/生成头。`K graph-job` 生成交接脚本。原始 CDB 用于 ECS；`compile_commands.inventory.json` 只作本机盘点。

已有 ECS 图配置 `index_db`、`run_id`、`graph_storage: reference`，协调端只读挂接一次。不同服务器用 `team assign --kit` → `team open` → 学习 → `team export` → `team receive` → 中央审阅 → `team feedback/sync`。模块包保留课程、实现覆盖、前置知识和真实子 Agent 身份，不手工合并 SQLite，不要求每人复制全仓图。

同一工作区的 `batch` 返回独立子会话、原生租约和实际宿主 Agent ID 续接信息。协调端规划续学任务再同步给成员；成员本地调整课程需先协调。完整命令见迁移手册。

## 验证边界

公开 openGauss 全仓实测：2,380 个 CPP、2,412 个历史编译上下文、537 个模块、3,667 个工作包候选，初始 559 个任务，全部 CPP 有课程归属。手册仅一页样例、历史特性仅验证样例，不能当作完整产品材料。实测提交及学习范围见[验证报告](docs/VALIDATION-2.4.md)。

公司专有 GaussDB 的目录、构建及知识正确性需在目标版本验收。升级工程不会自动批准旧知识。论文依据见[调研设计](docs/plans/module-feature-learning-redesign-20261108.md)，实现对应见[技术设计](docs/DESIGN-2.4.md)。
