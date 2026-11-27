# 达梦慢 SQL 优化报告系统

> 本文件是什么：项目总说明，面向人阅读。写清当前范围、依据、目录、运行命令、清洗/切块/标签规则、实际结果和已知限制。代码细节看 `src/knowledge/ingest.py` 和 `src/knowledge/retrieval.py` 的文件头。

武汉达梦 4-1 毕业设计项目。系统只生成“慢 SQL 优化报告草稿”：不连接生产库、不执行 SQL、不自动创建索引、不替代人工判断；证据不足时必须降级为“资料不足/需人工确认”。

当前完成的是 **1A v2：26 篇 DM SQL 优化案例 + 1 篇 DM9 手册样章的清洗、标题化、小块切分、父子块标注、角色/内容类型标注、标签与校验**。**1B 已在这批数据上跑通检索与 20 题基线评测**：bge-base-zh-v1.5 + Chroma + BM25/RRF，角色选子块、父块只补上下文；代码、20 题评测集和指标已提交，索引目录按约定不进 Git，结果仍等待人工验证。1B 的指标、失败明细和复现命令见 `README_1B.md`。

## 1. 依据

| 内容 | 依据 |
| --- | --- |
| 配置 `settings.yaml` + 不提交 `.env` | 实践计划书 §3(四) |
| 四类主题 | 实践计划书 §4(一) |
| 清洗、标题化、代码块/表格处理 | 实践计划书 §4(二) |
| 构建流程、统计项 | 实践计划书 §4(五) |
| 20 块人工抽看、变更记录 | 实践计划书 §4(六) |
| 小块检索 + 父块补上下文；检索块 128 token；重叠 0 最好 | DM-RAG 论文 §V（ICDE 2026） |
| `chunk_target_chars=200`、`chunk_max_chars=300`、`chunk_overlap_chars=0` | 论文 128 token 的中文工程换算：按 1 token≈1.5 汉字取 200 字，上限 300 字；字符数不是论文原话 |
| 角色（问题/原因/办法/验证/概念/步骤/参考/总结） | 本项目报告拼接约定：报告按“问题 → 证据 → 原因 → 办法 → 验证”组织，角色用于检索和查漏 |
| 父子块（`root_id` / `parent_id` / `chunk_index`） | DM-RAG 论文 §V 的层次切块与父块展开；父块不单独入库，运行时按 `parent_id` 还原 |
| `sentence-transformers`、`chromadb` 等检索依赖 | 实践计划书 表41 |
| `BAAI/bge-base-zh-v1.5`（不用 small） | 用户 2026-11-26 明确要求：small 太小，选 bge-base 或 Qwen embedding；本项目取 bge-base，768 维、512 token，查询指令按模型卡 |
| BM25 + 向量 + RRF、父块展开 | DM-RAG 论文 §V；RRF `k=60` 为论文/RRF 原论文常用值 |
| 20 题评测集、指标定义 | 本项目自建；题目来自 1A 语料实际章节，不是论文的 1,324 QA；指标计算见 `scripts/eval_retrieval.py` |
| 原始资料、索引目录不进 Git | 实践计划书 表41/§4；项目理解 表12 |

变更说明：实践计划书原定“200–400 块、单块 800 字、重叠 80”。1A v1 按该规则产出 296 块，但单块平均 859 字、最长 15,876 字，检索不精确。组会决定按 DM-RAG 论文改为“小块检索 + 父块补上下文”，块数不再是硬指标；本版实际 1,502 块。该变更记入 `CHANGELOG.md` 2026-11-26。

## 2. 目录

```text
config/
  settings.yaml          1A 路径/切块参数 + 1B 模型/召回/角色/父块参数
  tags.yaml              四类主题、操作符、参数、SQL 特征、角色、内容类型
src/knowledge/
  ingest.py              清洗、标题化、切块、父子块、角色、标签、统计
scripts/
  build_chunks.py        来源登记；清洗 + 切块 + 打标签
  check_chunks.py        校验、统计、生成 20 子块 + 10 父块抽看清单
  build_index.py         1B 建索引：Chroma 向量 + BM25 token + 元数据
  search.py              1B 单条查询 CLI（role/global）
  eval_retrieval.py      1B 20 题基线评测，写 eval_metrics.json + eval_report.md
tests/
  test_ingest.py         切块/父子块/角色/标签/元数据单元测试
  test_retrieval.py      1B 纯函数：角色推断、RRF、选案例、父块、证据
README_1B.md             1B 的指标、失败明细、复现命令和边界
data/
  raw/dm_cases/          26 篇案例原始 Markdown（不进 Git）
  raw/dm_docs/           1 篇手册样章（不进 Git）
  registry/sources.json  来源登记（可进 Git）
  interim/cleaned/       清洗后的 Markdown（不进 Git）
  processed/             chunks.jsonl、stats.json、spot_check_20.md（不进 Git）
  index/                 Chroma、BM25 token、索引元数据（不进 Git）
  eval/                  20 题、评测指标和报告（已提交；索引目录不进 Git）
  logs/                  构建告警、来源登记报告（不进 Git）
```

## 3. 环境与运行

实际验证环境：Windows + Python 3.12.3（实践计划书要求 Python 3.11+）。

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

把 26 篇案例放到 `data/raw/dm_cases/`，把手册样章放到 `data/raw/dm_docs/`（文件名保持原样），然后执行：

```bash
# 1. 扫描两个目录，登记来源、版本、H1 类型
python scripts/build_chunks.py --register-only

# 2. 清洗、切块、打标签
python scripts/build_chunks.py

# 3. 校验并生成 20 子块 + 10 父块人工抽看清单
python scripts/check_chunks.py

# 4. 单元测试
python -m pytest -q

# 5. 1B 建索引（首次或 chunks/tags/模型变化后加 --force）
python scripts/build_index.py --force

# 6. 1B 单条查询（人工看角色、父块上下文、证据）
python scripts/search.py --query "这条 SQL 为什么没走索引，应该怎么优化？"

# 7. 1B 20 题基线评测
python scripts/eval_retrieval.py
```

`requirements.txt` 固定 1A 的 `PyYAML`、`pytest`，以及 1B 实际安装的 `sentence-transformers`、`chromadb`、`jieba`、`rank-bm25` 版本；`torch` 由 sentence-transformers 传递安装，本机为 2.15.0+cpu。1B 的建库、查询、评测命令见 `README_1B.md`。

**1B 脚本必须从项目根目录运行。** Chroma 1.5.9 在 Windows 下用含中文的绝对路径建库/加载会失败；代码把 `data/index/chroma` 转成相对当前目录的 ASCII 路径，路径不在项目根目录下或含非 ASCII 字符时直接报错。原因和实测见 `README_1B.md` §4.2。

## 4. 清洗与切块规则

### 4.1 H1 分类

登记时把 H1 下的正文分为四类，避免把推广链接或代码误当摘要：

- `none`：H1 后直接是 H2。
- `boilerplate`：只有 `ps：`、公众号、推荐文章链接等推广内容；清洗时删除。
- `abstract`：真正的摘要/概述；即使不足 80 字也保留独立块。
- `content`：H1 下含代码或表格；按普通正文章节切块。

### 4.2 清洗与标题化

- 删除 H1 与第一个 H2 之间的推广正文、水平分割线。
- 把 4 空格缩进代码转换为三个反引号围栏；同一段缩进代码按内容拆成 `sql` 与 `text`（执行计划）。
- 代码中的 `--` 注释保留；注释不作为切块边界。
- 纯编号标题 `## 01` 若下一行是粗体标签（如 `**原始SQL**`），改成 `## 01 原始SQL`；无法自动补标题的写入告警，不猜测。
- 纯编号且没有正文的分组标题只作分组标记，不进入 `section_path`，由子标题承担语义。
- 清洗结果写入 `data/interim/cleaned/`，便于复核；`chunks.jsonl` 不手工编辑。

### 4.3 父子块

- **父块 = 文章里的一个标题节**，不单独切、不单独入库。父块编号 `parent_id = <source_id>-pNNN`，同一父块内子块按 `chunk_index` 从 1 连续编号。
- **子块 = 检索单位**：目标 200 字，单块不超过 300 字，生产参数不重叠。
- 检索命中子块后，用 `parent_id` 把同一节的子块按 `chunk_index` 拼回父块，作为上下文；父块不重复建索引。
- 父块只用于补上下文，不替代角色。角色在节一级确定，所以同一父块只有一个角色。

### 4.4 子块切分

- 正文：超过 300 字才按句号/问号/分号等自然边界切，目标 200 字；不足 80 字的短引导句先攒着，贴到后面的代码或表格上，避免“构造数据”四个字单独成块。
- 代码：
  - 短代码与前面的说明同块；超过 300 字按行拆段，每段重新带 ``` 围栏，标 `code_split`。
  - 单行本身超过预算时保留整行，标 `oversize_line`，不把一条 SQL/一行计划从中间切断。
  - 最后一段太短时先从上一段挪几行过来；仍不够且并回不超过 300 字才并回，不制造超长块。
  - 代码不按注释切，避免把一句 SQL 从注释处切断。
- 表格：超过 300 字才按行拆，每块重复表头；引导句和表标题只放第一块；单行超长保留整行，标 `table_row_oversize`。
- 短块合并：只在**同父块、同角色、同内容类型**内合并，合并后不超过 300 字；合不了的保留，标 `short_chunk`，交给校验和人工抽看。
- H1 真摘要即使不足 80 字也保持独立，不参与合并。

### 4.5 角色与内容类型

角色只看标题，按 `config/tags.yaml` 的顺序匹配，先命中先算：

- 案例：问题 / 原因 / 办法 / 验证 / 概念 / 步骤 / 总结；标题看不出时记“未分类”。
- 手册：步骤 / 参考 / 总结；其余默认“概念”，不把手册的“优化”硬当成案例的“办法”。
- H1 是文档标题，统一记“概念”。

内容类型判断“这一块包含什么”，顺序为：执行计划 → 统计输出 → SQL → 表格 → 命令 → 文字。
证据（执行计划/统计输出）用 `content_type` 表示，不占 `section_role`；这样“原因”节里贴一段执行计划，父块角色仍是“原因”，不会被计划块污染。

### 4.6 元数据与标签

`chunks.jsonl` 每块固定字段：

`chunk_id`、`root_id`、`parent_id`、`chunk_index`、`source_type`、`source_name`、`source_url`、`section_path`、`title`、`section_role`、`content_type`、`tags`、`version`、`text`。

标签规则、可复现，1A 不使用 LLM 打标签：

- 主题：执行计划 / 索引 / 统计信息 / SQL写法，允许多标签；没有命中时不虚构“其他”，进入 QC。
- 操作符：只从 `#` 开头的计划行抽取，多词操作符整体保留。
- 参数：精确匹配语料中实际出现的参数；表名、索引名不算。
- SQL 特征：`SELECT *`、前导模糊、函数包列、隐式转换、连接方式、子查询、分页、排序、绑定变量；只做显式文本/正则匹配。
- 标签顺序：主题 → 操作符 → 参数 → SQL 特征，去重。
- `config/tags.yaml` 只收语料中实际出现的词；新增词必须有语料出处。

## 5. 1A v2 实际结果（2026-11-26）

- 来源：27 个（26 篇案例 `case-001..026` + 1 篇手册样章 `doc-001`）。手册样章为 DM9 系统管理员手册第 22 章“查询优化”。
- 子块：**1,502 块**；父块：**240 个**；平均每父块 6.26 个子块。
- 长度：平均 211.9 字；最短 18 字，最长 594 字；p50 223，p90 287。
- 不足 80 字：39 块（2.6%），其中 9 块是 H1 摘要（按规则保留），30 块标 `short_chunk`。
- 超过 300 字：13 块（0.9%），原因是 9 个单行超长（执行计划/SQL）和 4 个超长表格行；均带 `oversize_line` / `table_row_oversize` 标记，没有把行从中间切断。
- 角色覆盖：问题 173、原因 20、办法 311、验证 152、概念 265、步骤 99、参考 1、总结 18、未分类 463。
- 内容类型：文字 278、SQL 465、执行计划 524、统计输出 53、表格 182。
- 主题覆盖（可多选）：执行计划 874、索引 200、统计信息 54、SQL写法 623。
- 质量标记：`code_split` 1,039 块（长代码/计划分段，属预期）；`short_chunk` 30 块。
- 重复文本：37 组、48 个多余块。均为原文重复（同一 SQL/计划在“问题SQL”和“问题验证”各出现一次，或手册重复示例），不是切块器重复。
- 校验：`check_chunks.py` **0 个错误**；`pytest` **30 个测试通过**。
- 人工抽看：`data/processed/spot_check_20.md`，含 20 个子块 + 10 组父块还原；**尚未完成人工勾选**。

已知限制（不掩盖）：

1. **父块可能很大**：最大的父块有 85 个子块、18,079 字（`doc-001-p024`，手册 22.6.2 自主修复；`case-018-p006` 也有 85 块）。1B 已按 `parent_window=2`、`parent_max_chars=1500`、`role_context_max_chars=1500` 做窗口和限长，且命中块先放、兄弟块后放；这样不会整段塞入，但超大父块仍只能读到命中块附近的一段。
2. **13 个超长块**是单行计划/单行表格行造成的，硬切会破坏语义；1B 按 `max_seq_length=512` 编码，1A 最长块 594 字，超长单行可能被模型截断，`oversize_line` / `table_row_oversize` 标记仍保留。
3. **463 个未分类（30.8%）**：标题里没有角色词（如“使用示例”“update语句”“in 查询与优化”）。它们仍可按文本检索，但不参与“问题/原因/办法/验证”查漏；本版没有为了凑角色硬扩充词典，是否补词等人工看 1B 失败题后再定。
4. **代码块大多是分段**（`code_split` 1,039）：子块单独看可能从 SQL/计划中间开始，必须配合父块展开使用；这正是“小块检索 + 父块补上下文”的代价。
5. **重复块**没有在 1A 删除：删掉会丢失“问题”或“验证”其中一种角色语境；计划在 1B 检索结果里按文本去重。

## 6. DM-RAG 公开语料的使用边界

论文和公开仓库的情况（2026-11-26 核对）：

- 论文：DM-RAG: Enhancing User Support in Dameng Databases with Retrieval-Augmented Generation，ICDE 2026，DOI `10.1109/ICDE65706.2026.00304`。
- 公开语料仓库：`https://github.com/johnnyhuangcs/Dameng_Corpus`，当前约 380 个 `.md` 文件，覆盖 `common_question`、`quick_start`、`app-dev`、`sql_development_guide`、`operations_guide`、`product_manual`。
- 仓库 README 写明：数据集归武汉达梦数据库股份有限公司所有；任何使用、复制、修改需事先取得书面许可；联系 `huangqiang@dameng.com`。
- 仓库里**没有**论文所说的 1,324 条 QA 对，也没有评测 JSON；论文声称的 QA 对需要向作者申请。
- 语料是 DM8 文档；本项目的案例是 DM8，手册样章是 DM9，版本字段已分开记录，不能混用。

建议的使用方式（未执行，先不动仓库）：

1. 先发邮件申请书面许可，说明只用于毕业设计、非商业、不对外分发；没有许可不下载入库。
2. 获许可后只取与慢 SQL 相关的目录（`product_manual` 的 SQL 优化/系统管理员、`sql_development_guide`、`operations_guide` 的性能诊断部分），不整库拷贝。
3. 原始文件继续放 `data/raw/` 且不进 Git，不把语料再分发；来源登记保留仓库 URL 和版本。
4. 1,324 条 QA 对单独向作者申请；拿到后只作为评测集，不混入知识库，避免“考题进题库”。

## 7. 1B 检索与基线（已完成，索引不入库）

2026-11-26 在 1A v2 的 1,502 个子块上跑通第一版基线：

- `BAAI/bge-base-zh-v1.5`（768 维、512 token）编码，Chroma 集合 `dm_slow_sql_v2` 持久化；BM25 用 jieba 精确模式 + `tags.yaml` 词表，`BM25Okapi(k1=1.5, b=0.75)`。
- dense 与 BM25 各取 50 个子块，在**子块级**用 RRF（`k=60`）融合；角色选子块、再选案例；父块只在选中后按 `parent_id` 展开补上下文，不建索引、不参与排序；证据按 `content_type=执行计划/统计输出` 单独取。
- 20 题自建基线：**CaseHit@1 95.0%**（19/20）、**RoleRecall@3 77.1%**（micro，27/35）、**RoleMRR@3 60.5%**（micro）、**RoleGoldCoverage 85.0%**、**EvidenceCoverage 85.7%**（14 题；q05/q09 的 gold 本身没有要求类型，按资料不足解释，可评估的 12 题为 100%）、**Global Recall@5 70.0%**。
- 工程校验：Chroma 1,502/1,502、BM25 1,502/1,502；`pytest` 52 通过；同题两次检索结果一致；构建后重开 Chroma 和新进程查询均通过。
- **不设质量通过线**。这些数是基线，用来讨论下一轮怎么提高；不代表已经达到验收标准。
- 已知问题：q19 在近义案例 case-012/case-021 之间选错；q13 的“手动收集”步骤没进 top3；q05/q09 是题目要求与 gold 资料不匹配；20 题规模小，doc-001 的 4 题共享 root，CaseHit 偏粗。详细解释、指标口径和复现命令见 `README_1B.md`。
- 限制：Chroma 1.5.9 在 Windows 上不能用含中文的绝对路径建库/加载，脚本必须从项目根目录运行；修复见 `chroma_relative_path()` 和 `README_1B.md` §4.2。

报告生成仍只输出草稿；资料不足时明确降级为“资料不足/需人工确认”。
