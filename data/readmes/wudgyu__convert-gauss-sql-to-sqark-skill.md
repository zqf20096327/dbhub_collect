# gauss2spark

把一个 **openGauss（DBCOMPATIBILITY = PG）SQL 文件**端到端转换为 **Spark SQL 4.2.0**，
并让每一步都可审计、可追溯：每条语句为什么这样转、依据哪条规则、哪里必须人工确认，
都落在固定字段的记录里，而不是只给一个转换后的文件。

三条必须先知道的性质：

1. **默认阻断**。只有低风险、确定性的转换自动放行；其余一律进入审批清单，未确认完不出最终 SQL。
2. **可追溯，但不可复现**。同一输入两次运行可能得到不同结果——转换由模型按规则库完成，不是编译器。
3. **只做过静态校验**。当前校验档位是 `static-only`：结构检查与方言扫描，结果**未经真实数据执行验证**。

## 适用范围

| 项 | 值 |
|---|---|
| 源方言 | openGauss，`DBCOMPATIBILITY = PG` |
| 目标方言 | Spark SQL **4.2.0**（唯一测试覆盖版本，其他版本不承诺正确性） |
| 语句范围 | SELECT、常用 DML/DDL、`COMMENT ON`、`SHOW`、`EXPLAIN` 等 |
| 明确不支持 | PL 块（`DO` / `FUNCTION` / `PROCEDURE` / `TRIGGER`）、psql 元命令 |
| 编码 | 自动探测：BOM → UTF-8 → UTF-16LE → GB18030 → ISO-8859-1 兜底，实际编码记在 `split_summary.json` |
| 大文件 | 超过 200 行或 20 条语句时走分片路径，否则整个文件直通模型 |
| 落点存储 | 不绑定，不生成 `USING`、`TBLPROPERTIES` 等落点相关子句 |

## 工作架构

```
输入 SQL 文件
   │
   ├─ g2s split ──────────► statements.jsonl（切分、编号、偏移、sha256）
   │
   ├─ gauss2spark-analyze ─► 01_analysis.jsonl（分类、风险、档位、规则路由）
   ├─ gauss2spark-convert ─► 02_conversion.jsonl（改写 + 决策链）
   ├─ gauss2spark-review  ─► 03_review.jsonl（独立复核 findings）
   ├─ gauss2spark-fix     ─► 04_fix.jsonl（按 findings 修复，最多 2 轮）
   │
   ├─ g2s check    ─► 契约校验（字段、枚举、规则 id、阶段完整性）
   ├─ g2s gate     ─► 档位统计 + 审批比对，决定放行与否
   └─ g2s assemble ─► 05_final.sql、06_process-log.md、07_audit-report.md、
                      08_report.html、run_manifest.json
```

职责划分是这个设计的核心：

- **确定性工具**（Java，`g2s-core`）只做机械可判定的事：切分、编号、契约校验、闸门计算、产物组装，不做任何语义判断。
- **模型**（六个 skill）做语义判断：识别、改写、复核、修复。
- **规则库**（YAML）是模型的知识来源，不是可执行代码。

## 目录结构

```
gauss2spark-skill/
├── g2s                 工具入口（bash 包装脚本，调用 tools/bin/g2s-core.jar）
├── skills/             六个 SKILL（纯 Markdown，可安装到各 CLI 宿主）
├── contracts/          工作流契约与产物契约（节点顺序、放行规则、字段级定义）
├── checklist/          Spark 4.2.0 行为基线 + 静默语义漂移检查清单
├── rules/              规则库（YAML）+ 机器可读索引 index.json
├── tools/              g2s-core（零依赖内核）、g2s-spark（可选适配器）、构建脚本
├── adapters/           跨 CLI 的技能安装脚本与宿主技能目录表
├── validation/         Spark 基线探针（重跑实测结论用）
├── tests/              契约校验、规则校验、切分器回归、端到端回归
├── docs/               设计文档与使用说明
└── runs/               每次运行的产物目录（不入库）
```

六个 skill 各司其职：`gauss2spark`（编排）、`gauss2spark-analyze`（分析）、
`gauss2spark-convert`（转换）、`gauss2spark-review`（审核）、`gauss2spark-fix`（纠错）、
`gauss2spark-rules`（规则库维护）。它们**必须与仓库一并使用**：skill 正文里的
`contracts/`、`rules/`、`checklist/` 一律按仓库根解析，不支持把单个 skill 拷到别处。

## 档位与闸门

每条语句在分析阶段被定为一档，档位直接决定闸门行为：

| 档位 | 含义 | 闸门行为 |
|---|---|---|
| `auto` | 确定性转换、低风险 | 自动放行 |
| `confirm` | 可转换，但语义有偏差或依赖前置条件 | 阻断，需人工确认 |
| `blocked` | 无法转换 | 阻断，必须人工改写 |

闸门规则：只有 `auto` 自动放行；任一 `confirm` / `blocked` 语句缺少审批记录时，
**不产出最终 SQL**，退出码 3，并输出待处理清单。人工确认有三种处置，
一律记入 `approvals.jsonl` 并带确认人与时间：

- `accept-converted`：接受转换结果
- `use-manual`：改用人工补写的 SQL（该 SQL 同样进入最终文件，审计报告标注来源为人工）
- `exclude`：排除该语句

只有显式传 `--allow-partial` 才产出残缺版本，文件头带醒目警示。
同一构造在多条语句中重复出现时（例如 `DEFAULT nextval(...)`），按构造一次性确认，
不逐条询问。

## 快速开始

环境要求：JDK 17+（运行工具）、Python 3.9+ 与 PyYAML（仅规则库与 Skill 校验）。
工具构建产物不入库，首次使用先构建——只需 JDK，不联网：

```bash
tools/build.sh
```

```bash
# 1. 建立本次运行的工作目录
RUN=runs/$(date -u +%Y%m%dT%H%M%S)-your_input
mkdir -p "$RUN"
cp your_input.sql "$RUN/00_input.sql"

# 2. 切分，得到语句清单与路由判定
./g2s split --in "$RUN/00_input.sql" --out "$RUN"

# 3. 依次执行四个节点（在 CLI 中以 skill 方式调用）
#    analyze → convert → review →（审核要求修复时）fix
#    也可以直接以编排 skill 驱动整条链路：$gauss2spark <文件>

# 4. 契约校验与闸门
./g2s check --run "$RUN"
./g2s gate  --run "$RUN"          # 放行 0，未放行 3

# 5. 放行后组装产物（校验档位必须如实填写）
./g2s assemble --run "$RUN" \
    --model-host <宿主> --model-name <模型> --verification-tier static-only
```

## 产物清单

每个 run 目录的固定产物（字段定义见 `contracts/artifact-contract.md`）：

| 文件 | 内容 | 是否总有 |
|---|---|---|
| `00_input.sql` | 输入快照 | 是 |
| `statements.jsonl` | 切分结果：编号、类型、行号、sha256、原文 | 是 |
| `01_analysis.jsonl` | 分类、特征、档位、风险、命中规则 | 是 |
| `02_conversion.jsonl` | 改写结果 + 决策链（语义、策略、备选方案、风险、证据） | 是 |
| `03_review.jsonl` | 独立复核意见与 findings | 是 |
| `04_fix.jsonl` | 纠错记录（按 finding 逐条回应） | 审核要求修复时 |
| `approvals.jsonl` | 人工确认记录 | 有 confirm/blocked 时 |
| `05_final.sql` | 最终 SQL（含原文注释） | 仅闸门放行时 |
| `06_process-log.md` | 转换过程文档（逐句决策链） | 组装时 |
| `07_audit-report.md` | 审计报告（统计、阻断清单、人工确认、校验档位声明） | 组装时 |
| `08_report.html` | 自包含对照报告，浏览器直接打开 | 组装时 |
| `run_manifest.json` | 运行清单：输入 sha256、规则集 sha256、闸门统计、校验档位 | 组装时 |
| `trace.jsonl` | 追加式事件流 | 组装时 |

`02_conversion.jsonl` 这类机器可读记录**永远全量**，文档简写不会丢记录。
过程文档刻意不导出原始思维链：不可复现、无法校验的东西构不成审计证据，
需要的是"决策依据可复查"。

## 规则库

规则是结构化 YAML，分主题按需加载（渐进披露），不是一股脑塞进上下文：

| 文件 | 主题 |
|---|---|
| `rules/core/010-type-mapping.yaml` | 类型名映射（三处语法位置共用） |
| `rules/core/020-ordering-null.yaml` | 排序与 NULL 位置（头号语义漂移项） |
| `rules/core/030-null-semantics.yaml` | NULL 语义差异函数 |
| `rules/core/040-scalar-functions.yaml` | 标量函数映射 |
| `rules/core/050-datetime-format.yaml` | 日期时间与格式串 token |
| `rules/core/060-ddl.yaml` | DDL 对象与表属性 |
| `rules/unsupported.yaml` | 语句级不支持清单（权威，判 blocked 前必比对） |

增删改查走 `gauss2spark-rules` skill，改完需要：

```bash
python3 tools/gen_rule_index.py    # 重新生成 rules/index.json（Java 侧只读 JSON）
python3 tests/validate_rules.py    # 校验规则结构与索引一致性
```

所有规则结论都必须有实测依据，出处是 `checklist/spark-4.2.0-baseline.md`；
规则与该文件冲突时以基线为准。

## 跨 CLI 安装

六个 skill 是纯 Markdown，符合通用 Agent Skills 规范。用符号链接安装（不是复制，
复制会让 skill 内的仓库根相对引用失效）：

```bash
adapters/install.sh --target claude        # 或 codex
adapters/install.sh --target opencode --dir <实际技能目录>
adapters/install.sh --target claude --dry-run
adapters/install.sh --target claude --uninstall
```

宿主技能目录表在 `adapters/targets.yaml`。目前只有 `claude` 与 `codex` 的目录约定
**经过实测**；`opencode`、`trae`、`codebuddy` 未实测，脚本会要求显式提供 `--dir`。
仓库必须保留在原地，并把仓库根暴露给工具（`export G2S_HOME=<仓库根>`）。

## 校验与测试

```bash
tests/run_all.sh
```

依次执行：构建工具 → 规则库校验 → Skill 结构校验 → 切分器回归 → 端到端回归。
端到端回归用的是预制记录，验证的是工具链与闸门行为，**不是**模型在真实语料上的表现。

每次运行必须记录校验档位，审计报告中如实声明：

| 档位 | 含义 |
|---|---|
| `static-only` | 仅结构检查与方言扫描（当前实际档位） |
| `syntax-parse` | 已用 Spark 4.2.0 解析器验证语法 |
| `explain-checked` | 已对转换结果执行 EXPLAIN 校验（需要 schema） |

## 已知限制

1. **Spark 接入未实现**：`g2s-spark` 适配器只有目录骨架，校验档位只到 `static-only`，转换结果的语法未被 Spark 4.2.0 解析器验证过。这是当前最大缺口。
2. **真实模型端到端演练尚未执行**：现有端到端回归用的是预制记录。
3. **PL 块的启发式切分路径没有测试覆盖**：现有语料的 PL 块都带美元引用。
4. **非 4.2.0 的 Spark 版本未验证**，包括 4.0.x 与 4.1.x 的差异。
5. **数万行的大文件未做实测**，阈值与内存表现待验证。
6. **opencode / trae / codebuddy 的技能目录约定未实测**。

## 文档索引

- 设计与决策记录：[docs/01-设计文档.md](docs/01-设计文档.md)（含 D1–D10 决策、待验证清单、演进路线）
- 使用说明：[docs/02-使用说明文档.md](docs/02-使用说明文档.md)
- 工作流契约：[contracts/workflow.md](contracts/workflow.md)
- 产物契约：[contracts/artifact-contract.md](contracts/artifact-contract.md)
- Spark 4.2.0 行为基线：[checklist/spark-4.2.0-baseline.md](checklist/spark-4.2.0-baseline.md)
- 语义漂移检查清单：[checklist/semantic-drift-checklist.md](checklist/semantic-drift-checklist.md)

## 需求来源

本项目源于以下需求，原文保留：

```text
写一个把一个GaussDB语法的**sql文件（由多个sql语句构成，各个sql语句之间用;分割。每个sql中有回车换行符，而且会有注释。）**，的GaussDB的sql语句转换成Spark SQL语法的SQL语句的skill工作流。
工作流至少需要包括：sql分析->sql转换->sql审核->sql纠错，几个部分；

要求：
(0) 注意：该工作流的每个节点都要写成一个SKILL，转换规则可以是一个单独的SKILL
(1) SKILL可以支持在opencode，或trae，codebuddy等CLI中运行；
(2) 转换规则可以配置，可以增删改查
(3) 需要产出设计文档、使用说明文档和思考过程的文档，整个过程可审计，可追溯。
(4) 界面没有要求，要是有页面，当然更好。
(5) 转换过程中需要有过程文档，也就是能看到大模型是如何转换的。
```

需求在讨论中还有几处澄清，落实结果如下（决策记录见
[docs/01-设计文档.md](docs/01-设计文档.md) §12）：

| 澄清 | 落实 |
|---|---|
| 暂只支持 openGauss，默认 PG | 源方言固定为 openGauss（PG），使用说明显著声明 |
| 目标是标准 Spark SQL，不绑定落点存储形态 | 不生成 `USING` / `TBLPROPERTIES` 等子句 |
| 不能只有 SELECT/DML，PL 块可暂不支持 | 覆盖常用 DDL 与命令；PL 块与元命令一律阻断 |
| 暂无 Spark 环境，仅做语法处理 | 校验档位为 `static-only`，如实声明未经执行验证 |
| 兼容单文件几万行 | 超过 200 行或 20 条语句走分片路径 |
| 默认阻断并要求人工确认 | 只有 `auto` 自动放行，其余进审批清单 |
| 降低外部依赖 | 自建工具改用 Java（复用 JVM，不新增运行时），`g2s-core` 零第三方依赖 |
| 转换主体交给模型，工具只保证描述准确 | 模型按规则库改写，工具只做切分、校验、闸门与组装 |
| 目标 Spark 版本先暂定 4.x | 冻结为实测覆盖的 4.2.0，其他版本不承诺正确性 |
| 过程文档即转换时输出的中间过程 | `02_conversion.jsonl` 固定字段记录决策链，并产出 `06_process-log.md` |
| 界面非必需，有更好 | 附带自包含 HTML 对照报告 `08_report.html` |
