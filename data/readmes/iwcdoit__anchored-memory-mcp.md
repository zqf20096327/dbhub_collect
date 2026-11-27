# Anchored Memory MCP — 基于代码锚点的 AI 研发记忆库

![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![MCP Streamable HTTP](https://img.shields.io/badge/MCP-Streamable_HTTP-2563EB)
![SQLite FTS5 + sqlite-vec](https://img.shields.io/badge/SQLite-FTS5_%2B_sqlite--vec-003B57?logo=sqlite&logoColor=white)
![Embedding](https://img.shields.io/badge/BGE-bge--small--zh--v1.5-F59E0B)
![MkDocs Material](https://img.shields.io/badge/MkDocs-Material-526CFE?logo=materialformkdocs&logoColor=white)

面向 **Claude Code、Codex、Cursor** 等多工具与团队协同开发场景的轻量化研发记忆与上下文管理服务。日常用 AI 辅助研发时，排障经验和业务设计往往散落在单次对话里——换个会话就“失忆”，换个工具就不互通，写成静态文档又容易在代码重构后过期误导。本项目将**项目公共规范**随 Git 仓库版本化共享，将**跨会话的排障与设计笔记**沉淀到统一的 MCP 记忆服务中；每篇笔记直接关联真实的源码路径、核心方法与排查验证步骤，让 AI 下次遇到同类问题时能直接顺着笔记定位代码并核对逻辑是否变更，同时支持在网页端实时查阅。

![一图看懂 AI Coding 研发记忆库](docs/assets/anchored-memory-comic.svg)

---

## 核心设计：轻量化按需加载与活体记忆自愈

在多微服务研发场景下，多个独立的业务 Git 仓库共享同一个 Basic Memory MCP 服务。系统围绕**「轻量化、零额外工具轮次、负 Token 开销」**设计以下四步工作流：

### 第一步：项目级配置挂载 MCP 服务
各业务子仓库根目录通过客户端配置文件（.mcp.json、.codex/config.toml、.cursor/mcp.json）统一接入共享的 Streamable HTTP MCP 服务端（:8000/mcp）。日常普通编码任务零 MCP 调用、零额外 Token 消耗。

### 第二步：自动读取子项目 AGENTS.md 入口与底部钩子
AI 进入具体微服务仓库时，仅加载该项目根目录下的精简 **AGENTS.md**（**CLAUDE.md** 仅一行 @AGENTS.md 引用同一事实源），获取模块划分与构建测试命令，并通过文件末尾的钩子接管按需加载策略：

```markdown
# Agent Instructions (位于各子项目 AGENTS.md 底部)
Read and follow .ai/AI_CONTEXT.md and .ai/MEMORY_POLICY.md before starting work.
Apply any more-specific AGENTS.md files within their directory scope.
```

### 第三步：本地静态规范按需路由（由 .ai/AI_CONTEXT.md 控制）
禁止 AI 递归预加载整个 docs 目录，仅按当前任务类型按需读取 docs/development/conventions.md（开发规约）、docs/architecture/（模块边界）、docs/adr/（架构决策）或 docs/tasks/（长任务追踪）。

### 第四步：远端记忆按需读写、内联锚点校验与 Playbook 自愈（由 .ai/MEMORY_POLICY.md 与 Skills 控制）
多个微服务物理共用同一记忆库，逻辑上通过 **repository** 元数据隔离。每篇笔记仅用约 70 Tokens 绑定 **代码锚点（Code Anchors）** 与 **可执行剧本（Playbook）**，帮 Agent 省去 3~5 轮全仓 grep/find 盲搜（单次排障净省数万 Input Tokens）：

- **按需混合检索与内联锚点核验（memory-continue，零额外脚本轮次）**：
  仅在排查疑难故障或跨会话续接时，按 repository 过滤执行 BM25 + BGE 中文向量混合检索。AI 读回笔记后，直接顺着笔记的 **code_paths** 打开目标源码文件，在读代码的同时顺手核对 **code_symbols**（类名#方法名/常量）是否完好（对话内零额外脚本调用；同时服务端提供 coding_memory.drift 供离线/CI 零 Token 批量巡检三级漂移状态：**CLEAN** 零漂移 / **MODIFIED_SAFE** 符号完好 / **DRIFTED** 高危漂移）。

- **可执行剧本直达（Playbook）**：
  笔记内置标准化 Playbook 章节，直接向 AI 提供精确的验证路径，杜绝盲猜试错：
  - **[probe] 只读诊断探针**：遇到同类症状时可直接复用的日志检索式或参数化只读排查 SQL。
  - **[verify] 回归验证命令**：精确到测试类的最小回归单测命令（如 mvn test -Dtest=xxxTest）。

- **查重合成与四态自愈闭环（memory-capture / memory-notes）**：
  写入前先调 search_notes 查重，同主题原地合成覆写（拒绝碎片化追加），按 projects/&lt;repository&gt;/&lt;memory_type&gt;/ 归档为 6 类标准笔记（incident / debugging / solution / pitfall / practice / task-context），形成四态自愈闭环：
  **draft**（排查草稿） $\rightarrow$ **verified**（已验证并绑定代码锚点） $\rightarrow$ **stale**（源码重构触发锚点漂移，经 Playbook 复核并刷新 commit 后自愈回 verified） / **promoted**（沉淀为长期架构红线反哺写入 Git 仓库的 ADR 或开发规约）。

**活体记忆笔记结构示例：**

```markdown
---
title: 热点账户行锁超时排查
repository: pay-ledger
memory_type: troubleshooting
status: verified
commit: 8f3a1c2
code_paths: [pay-ledger-server/src/main/java/com/pay/ledger/account/HotAccountShardingService.java]
code_symbols: [HotAccountShardingService#routeSubAccount, ERR_ACCOUNT_LOCK_TIMEOUT]
---

# 热点账户行锁超时排查
...(根因与拆分归集方案)...

## Observations
- [root_cause] 同一平台收益账户高峰期集中并发写入，单行锁串行等待占满连接池。
- [fix] 按峰值冗余拆分子账户，订单号 Hash 取模路由分散写压力，配合定时任务异步归集。

## Playbook
- [probe] 检索近 15 分钟行锁超时日志：error_code="ERR_ACCOUNT_LOCK_TIMEOUT"
- [verify] 运行热点子账户路由与归集单测：mvn -pl pay-ledger-server test -Dtest=HotAccountShardingServiceTest

## Relations
- relates_to [[交易终态事件驱动编排规范]]
```

---

## 快速启动服务端

### 方式一：Docker Compose（推荐）

支持 Linux x86_64 / ARM64 及 Apple Silicon。首次启动自动缓存约 96 MB 的轻量级 bge-small-zh-v1.5 权重并初始化示例笔记。

```bash
docker compose up --build --wait --wait-timeout 420
docker compose ps
```

| 服务组件 | 默认地址 | 职责说明 |
| :--- | :--- | :--- |
| **Basic Memory MCP** | http://localhost:8000/mcp | 供 Claude Code / Codex / Cursor 按需检索、读取、写入笔记 |
| **MkDocs 知识站** | http://localhost:8088/ | 人类浏览器实时查阅同一批 Markdown 笔记 |
| **BGE 中文向量服务** | 容器内 http://embedding:8001/v1 | 本地轻量 CPU 推理生成 512 维 L2 归一化中文向量 |

### 方式二：本机直接运行（无 Docker，基于 uv）

```bash
uv sync --locked --managed-python --python 3.12
uv run --locked python -m coding_memory local
```

### 离线锚点巡检与端到端冒烟验证

```bash
# 离线/CI 批量校验笔记的 Code Anchors 与 Playbook 契约（可传 --repo-dir 对比业务仓库源码漂移，零 Token 消耗）
python3 -m coding_memory.drift --require-contract

# 校验 MCP 握手、三路混合检索 (text/vector/hybrid) 与 MkDocs 实时发布闭环
python3 -m coding_memory.verify --write-check
```

---

## 业务仓库轻量化接入模板

将 examples/client-project/ 复制到业务微服务仓库根目录即可完成接入：

```text
your-service-repo/
├── AGENTS.md                           # 子项目模块结构、构建命令与底部 .ai 钩子入口
├── CLAUDE.md                           # 单行 @AGENTS.md 引用，保持多工具单一事实源
├── .mcp.json                           # Claude Code MCP 接入配置 (:8000/mcp)
├── .codex/config.toml                  # Codex CLI MCP 接入配置
├── .cursor/mcp.json                    # Cursor MCP 接入配置
├── .ai/
│   ├── AI_CONTEXT.md                   # 本地 docs/ (conventions / adr / tasks) 按需路由规则
│   ├── MEMORY_POLICY.md                # 轻量化内联锚点核验、Playbook、6 大分类与四态自愈策略
│   └── scripts/get-developer-context.sh# 写入时辅助提取 Git repository / branch / commit 元数据
└── .agents/skills/
    ├── memory-continue/SKILL.md        # 按需混合检索、直达 code_paths 内联核验与 Playbook 诊断
    ├── memory-capture/SKILL.md         # 查重原地合成与 stale 笔记自愈刷新指引
    └── memory-notes/SKILL.md           # Code Anchors + Observations + Playbook + Relations 规范
```

---

## 服务端仓库结构

```text
.
├── compose.yaml                 # Docker Compose 三服务编排 (embedding / memory / site)
├── Dockerfile                   # 多阶段 uv 构建镜像
├── mkdocs.yml                   # Material for MkDocs 中文知识站配置
├── pyproject.toml               # Python 3.12 依赖分组定义 (memory / embedding / site)
├── coding_memory/
│   ├── config.py                # 核心运行时配置与目录映射 (RuntimeConfig)
│   ├── encoder.py               # FastAPI OpenAI 兼容轻量向量服务 (BAAI/bge-small-zh-v1.5)
│   ├── drift.py                 # 离线/CI 三级代码锚点漂移巡检与可执行 Playbook 解析引擎
│   ├── __main__.py              # 服务统一入口与本机多进程编排器
│   └── verify.py                # 锚点契约 + MCP Streamable HTTP + 混合检索端到端验证
├── examples/
│   ├── client-project/          # 业务仓库轻量化分层接入脚手架 (AGENTS.md + .ai/ + 3 Skills)
│   └── notes/                   # 含代码锚点与 Playbook 的示例研发笔记
└── docs/
    └── assets/anchored-memory-comic.svg # 四格漫画与全链路架构图
```

## 许可证

MIT License
