# TiDB Code RAG

TiDB 源代码的结构化知识库，通过 frozen snapshot 机制提供"即问即答"的 RAG 服务。

## 这是什么

一个预编译的 TiDB 源码知识库。不是每次从源码重新检索，而是**一次性编译、反复使用**——从 109 篇设计文档、23 篇 agents 文档、106 篇官方中文文档中系统性提炼了约 558KB 的结构化知识，涵盖 10 个子系统 + 15 个核心特性。

```
提问示例：
- "TiDB 的 Online DDL 怎么保证分布式 Schema 一致性？"
- "Skyline Pruning 和传统 CBO 索引选择有什么区别？"
- "Pipelined DML 的 flush 机制是怎么工作的？"
- "Resource Control 的 RU 怎么算？怎么限制写入速率？"
- "Stale Read 的 SafeTS 是怎么计算的？"
```

## 知识结构

```
wiki/
├── index.md                      # 总索引
├── architecture.md               # 顶层架构（组件图 + 4 条跨模块数据流）
│
├── subsystems/                   # 10 个子系统（主线）
│   ├── parser.md                 # 25KB — SQL 解析器，parser.y + AST 类型体系
│   ├── server.md                 # 27KB — MySQL 协议，连接管理，认证
│   ├── planner.md                # 39KB — 查询优化器，RBO + CBO + Plan Cache
│   ├── statistics.md             # 32KB — 直方图、CMSketch、Analyze 流程
│   ├── executor.md               # 26KB — Volcano 执行引擎、TiFlash 下推
│   ├── expression.md             # 24KB — 三层表达式体系、签名矩阵、向量化
│   ├── ddl.md                    # 41KB — DDL Job 生命周期、Reorg、Multi-Schema Change
│   ├── infoschema.md             # 35KB — v1/v2 双版本、SIEVE 缓存
│   ├── session-domain.md         # 28KB — Domain 协调、变量管理、资源管控
│   └── storage.md                # 31KB — TiKV 适配器、事务、DistSQL、TableCodec
│
└── features/                     # 15 个特性（辅线）
    ├── distributed-transaction.md  # 22KB — 乐观/悲观/Async Commit/1PC/2PC
    ├── mvcc-gc.md                  # 19KB — MVCC 原理、GC safepoint
    ├── stale-read.md               # 22KB — Stale Read、Follower Read、AS OF
    ├── query-optimization.md       # 18KB — RBO/CBO/Skyline/IndexMerge/Hint
    ├── plan-cache.md               # 13KB — Prepared/Non-Prepared 缓存、SPM
    ├── statistics-management.md    # 20KB — Analyze、Predicate Columns、Index Advisor
    ├── vectorized-execution.md     # 21KB — Chunk 模型、MPP、Spill
    ├── partition-table.md          # 13KB — Range/List/Hash/Key 分区
    ├── index-design.md             # 11KB — 聚簇索引、MV Index、Vector Index
    ├── charset-collation.md        # 11KB — UTF8MB4/GBK/GB18030
    ├── schema-features.md          # 16KB — TTL、Views、FK、Placement Rules
    ├── tiflash-htap.md             # 16KB — 列存引擎、MPP、Pipeline
    ├── resource-control.md         # 15KB — RU 调度、Resource Group、Runaway
    ├── distributed-framework.md    # 17KB — DXF、Global Sort
    └── security-rbac.md            # 16KB — RBAC、动态权限、日志脱敏
```

每个页面都包含 9 个标准段落：概述、原理/数据结构、关键流程、源码导航、配置与变量、设计决策与取舍(★)、使用场景与最佳实践、隐性知识/踩坑、参考链接。

## 怎么用

### 1. 启动 Expert Agent

```bash
cd ~/project/tidb-code-RAG

# 从冻结镜像 fork 并启动（首次约 3-5 分钟加载，后续秒级）
wiki/snapshot/snapshot.sh start
```

### 2. 提问

```bash
# 命令行
wiki/snapshot/snapshot.sh ask "TiDB 的 stale read 是怎么实现的？"
wiki/snapshot/snapshot.sh ask "Pipelined DML 和普通事务的区别？"

# 或在另一个 agent 中通过 ai send 调用
EXPERT_ID=$(cat wiki/snapshot/expert.id)
ai send --id "$EXPERT_ID" --wait --timeout 2m "你的问题"
```

### 3. 停止 / 清理

```bash
wiki/snapshot/snapshot.sh stop    # 停止（保留 session，可 resume）
wiki/snapshot/snapshot.sh clean   # 丢弃工作副本（下次重新 fork）
wiki/snapshot/snapshot.sh status  # 查看状态
```

### 4. 通过 Skill 调用（其他 Agent）

```bash
# 任何 agent 都可以通过 find_skill 发现并加载
find_skill("tidb")          # → 发现 tidb-rag skill
find_skill("tidb-rag", load=true)  # → 读取完整使用说明
```

### Snapshot 冻结机制

```
frozen/ (只读)              runtime/ (可变)
18条消息, 136KB              随提问增长
    │                           │
    │  start = cp               │  ask × N
    │ ──────────────►           │ ──────────► session 越来越大
    │                           │
    │  clean = rm               │
    │ ◄────────────────         │
    │                           │
    ▼                           ▼
  永远干净                    用脏了就扔
```

- **frozen/**：冻结的干净镜像，包含 wiki 加载完成时的上下文，永不修改
- **runtime/**：工作副本，每次 start 从 frozen 复制，提问会追加消息
- 用脏了就 `clean`，下次 start 重新 fork 出干净的

## 怎么维护和更新

### 更新 wiki 内容

当 TiDB 源码有重要更新时：

```bash
# 1. 拉取最新源码
git -C ~/project/tidb/.worktrees/sync pull

# 2. 查看哪些文件变更了
git -C ~/project/tidb/.worktrees/sync log --oneline --stat HEAD~50..HEAD

# 3. 评估影响的子系统（对照 wiki/subsystems/ 的文件索引）
#    例如 pkg/ddl/ 有变更 → 需要更新 ddl.md

# 4. 用 subagent 重新探索受影响的子系统
#    （参考下面的"构造方法"章节）

# 5. 重建 frozen snapshot
wiki/snapshot/snapshot.sh freeze

# 6. 重新开始使用
wiki/snapshot/snapshot.sh clean
wiki/snapshot/snapshot.sh start
```

### 更新周期

| 事件 | 操作 |
|------|------|
| 小修改（bug fix） | 不需要更新 |
| 功能迭代 | 更新对应的 subsystems/ 页面 + 相关 features/ 页面 |
| 新特性 | 新建 features/ 页面，更新 index.md |
| 大版本升级 | 全面更新所有页面 |

### 子系统 → 源码映射

| 子系统 | 源码包 | 新设计文档位置 |
|--------|--------|---------------|
| parser | `pkg/parser/` | `docs/design/` |
| planner | `pkg/planner/` | `docs/design/` + `docs/agents/planner/` |
| statistics | `pkg/statistics/` | `docs/design/` |
| executor | `pkg/executor/` | `docs/design/` + `docs/agents/executor/` |
| expression | `pkg/expression/` | `docs/design/` |
| ddl | `pkg/ddl/` | `docs/design/` + `docs/agents/ddl/` |
| infoschema | `pkg/infoschema/` | `docs/design/` |
| session-domain | `pkg/session/`, `pkg/domain/`, `pkg/sessionctx/` | `docs/design/` |
| server | `pkg/server/` | `docs/design/` |
| storage | `pkg/store/`, `pkg/kv/`, `pkg/distsql/` | `docs/design/` |

### 特性 → 官方文档映射

features/ 页面的内容来自 TiDB 官方中文文档：

```
~/project/docs-cn/    — 官方文档仓库
├── transaction-overview.md, optimistic-transaction.md, ...  → distributed-transaction.md
├── garbage-collection-*.md                                  → mvcc-gc.md
├── stale-read.md, follower-read.md, ...                     → stale-read.md
├── sql-optimization-*.md, cost-model.md, explain-*.md, ...  → query-optimization.md
├── statistics.md, extended-statistics.md, ...               → statistics-management.md
├── partitioned-table.md, partition-pruning.md, ...          → partition-table.md
├── tiflash/                                                 → tiflash-htap.md
└── ...
```

## 构造方法

这个 wiki 是按以下步骤分批构建的：

### 第一轮：子系统探索（v1）

用 5 个 subagent 并行探索 TiDB 源码，每个负责 1-2 个子系统：

| Subagent | 探索范围 | 输出 |
|----------|---------|------|
| 1 | Parser + Server | parser.md, server.md |
| 2 | Planner + Statistics | planner.md, statistics.md |
| 3 | Executor + Expression | executor.md, expression.md |
| 4 | DDL + InfoSchema | ddl.md, infoschema.md |
| 5 | Storage + KV + DistSQL | storage.md |

每个 subagent 的任务：
1. 读取源码核心文件（每个子系统 ≥ 10 个文件）
2. 读取 `docs/agents/` 下的已有文档
3. 输出标准 7 段格式的 wiki 页面

### 第二轮：设计文档整合（v2）

用 4 个 subagent 按主题分组阅读全部 109 篇设计文档：

| Subagent | 阅读范围 | 新增段落 |
|----------|---------|---------|
| A | 20 篇 Planner + 6 篇 Statistics + 3 篇 agents | 设计决策与取舍(★)、特性演进时间线 |
| B | 19 篇 DDL + 9 篇 agents | 同上 |
| C | 12 篇 Executor + 12 篇 Storage + 3 篇 agents | 同上 |
| D | 14 篇 Session + 7 篇 Parser + 10 篇杂项 | 同上 |

### 第三轮：特性辅线（v3）

用 4 个 subagent 阅读官方中文文档（docs-cn）的 106 篇文档：

| Subagent | 阅读范围 | 输出 |
|----------|---------|------|
| 1 | 17 篇事务 + 锁 + 隔离级别 | distributed-transaction, mvcc-gc, stale-read |
| 2 | 36 篇优化器 + 执行 + 统计 | query-optimization, plan-cache, statistics-management, vectorized-execution |
| 3 | 29 篇 DDL + Schema + 数据类型 | partition-table, index-design, charset-collation, schema-features |
| 4 | 24 篇 TiFlash + 资源管控 + 安全 | tiflash-htap, resource-control, distributed-framework, security-rbac |

### 通用 Subagent Prompt 模板

```
你是 TiDB 源码 wiki 的构建者。请探索以下子系统，输出结构化 wiki 页面。

## 探索范围
[列出需要阅读的源码目录、设计文档、agents 文档]

## 输出要求
写入文件 [路径]，包含以下段落：
1. 概述  2. 原理与架构  3. 源码导航  4. 配置与系统变量
5. 设计决策与取舍(★)  6. 使用场景与最佳实践  7. 常见问题/踩坑指南
8. 相关子系统(链接)  9. 参考
```

## 文件清单

```
~/project/tidb-code-RAG/
├── README.md                   # 本文件
├── SKILL.md                    # Agent skill 定义（符号链接到 ~/.ai/skills/tidb-rag/）
├── docs/
│   └── tidb-architecture-wiki.md  # 初始版本（已整合进 wiki/）
└── wiki/
    ├── index.md                # 索引
    ├── architecture.md         # 顶层架构
    ├── log.md                  # 更新日志
    ├── subsystems/             # 10 个子系统页面
    ├── features/               # 15 个特性页面
    └── snapshot/
        ├── frozen/             # 冻结镜像（只读）
        ├── runtime/            # 工作副本（可变）
        ├── bootstrap.md        # Agent 启动指令
        └── snapshot.sh         # 管理脚本（start/ask/stop/clean/freeze/reset/status）
```

## 依赖

- `ai` CLI（`ai serve/send/kill` 控制 agent 生命周期）
- `tmux`（agent 后台运行）
- TiDB 源码 worktree：`~/project/tidb/.worktrees/sync/`
- TiDB 官方文档：`~/project/docs-cn/`（特性页面参考）