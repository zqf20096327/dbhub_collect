# ATTRIBUTION_PLAN v1.1 拆分清单（17 张任务卡）

> 2026-10-31 · 拆分原则：**每张卡 = AI 一个会话能独立做完并机器验收的量**。
> 2026-11-01 修订：+T0b（历史出池回流）/T2e（重写 unattr_judge 薄壳）两卡；T1c 不再碰 unattr_judge（已拍板废弃重写，不拉齐）；T1b 素材先落盘；T4a 加裁决人工抽检；T5a 加引擎单测 CI 收口；T1a 加词表人工过目+ports 声明性空口径。
> 整份方案给方向，任务卡给执行——做卡的 AI 不需要读全案。
> 台账用法：做完一张把 `[ ]` 改 `[x]` 并填提交号，支持断点续做。

## 任务卡七要素（每卡模板）

```
目标：一句话
输入：文件路径级素材（事实直接给，不让 AI 自己统计）
输出：文件路径级产物
边界：只许动哪些文件（白名单制，防越界）
验收：机器命令 + 期望数字（不是"我觉得做完了"）
防坑：本项目历史事故提炼的备注
依赖：前置卡号
```

## 卡总表（依赖拓扑排序）

| 批 | 卡 | 内容 | 规模 | 依赖 |
|---|---|---|---|---|
| 0 止血 | T0 | pool_core 出池闸门+审计日志 | S | — |
| 0 止血 | T0b | 历史已出池仓回流候选清单（止血≠回血） | S | T0 |
| 1 词表 | T1a | db_profiles 加 drivers/images/ports（17 库档案） | M | — |
| 1 词表 | T1b | 精确词档位机制+误伤反例用例 | S | T1a |
| 1 词表 | T1c | 词表派生层：三套硬编码归一 | M | T1a |
| 2 引擎 | T2a | attribution/ 包骨架+六型证据 schema | S | — |
| 2 引擎 | T2b | 匹配器（指纹×词表×topic 三规则）+单测 | M | T1a,T1b,T2a |
| 2 引擎 | T2c | quorum 投票+E-CI 消歧+单测 | M | T2b |
| 2 引擎 | T2d | 全池扫描 CLI（gap/status） | S | T2c |
| 2 引擎 | T2e | 重写 unattr_judge 薄壳（读 evidence+matcher，零网络） | S | T1c,T2b |
| 3 试点 | T3a | 试点清单生成（50+30+20+draft122） | S | T2d |
| 3 试点 | T3b | 人工复核表+命中率报告（人介入） | S | T3a |
| 4 回写 | T4a | 定点裁决 prompt+批量执行 | M | T3b 过 90% 闸 |
| 4 回写 | T4b | 回写器（立案写回+空适配打四类原因） | M | T4a |
| 4 回写 | T4c | 误杀复审 820 批 | S | T3b |
| 5 常态 | T5a | 增量挂钩+补全率报表进 CI | M | T4b |
| 5 常态 | T5b | release notes 复验触发 | S | T4b |
| 5 常态 | T5c | Gitee MVP 四库（独立失败域） | L | — （可提前并行） |

同批内并行；批间串行。T5c 无硬依赖，配额允许即可与第 2 批并行。

---

## 第 0 批 · 止血（先于一切）

### T0 出池闸门+审计日志 ｜✅ 2026-11-01 完成（提交号待填；10 用例绿+真实数据预演：9,269 圈定→920 准出/8,349 拦下）
- **目标**：pool_core 出池前先查"已侦查且无证据"，误杀仓（sqlc 式）不准踢出池
- **输入**：`pool_core` 现行 `_unlinked_fns` 逻辑（读通）；`state/unattr_verdicts.json` 台账
- **输出**：闸门函数 + `state/pool_exit_audit.json`（每次出池记录 fn/原因/当时证据状态）
- **边界**：只动 pool_core 相关文件与新增 audit 文件，不碰 interpret/collect
- **验收**：构造 3 个用例（真无关/没证据/已判 no_evidence）→ 只有第一类出池；audit 可查
- **防坑**：atomic_write 轮转三副本——写 audit 用同款机制勿裸写（[[atomic-write-rotation]]）
- **依据**：方案 §2.5

### T0b 历史出池回流候选（止血≠回血）
- **目标**：T0 只挡未来误杀；已出池的 sqlc 式仓要捞回——用快照历史差集生成回流候选清单
- **输入**：`lib/pool_history.py`（快照历史查询）；`state/unattr_verdicts.json`（当时证据状态）；dbhub_page 卡片清单
- **输出**：`state/pool_return_candidates.json`（fn/出池日期/当时状态/建议动作：overrides 签发 or 重扫 or 维持）
- **边界**：只读历史+产清单，**不直接改 pool**（回流动作走人工签发/重扫既有机制）
- **验收**：候选清单落盘且可查；与 10-09 桶剔名单（非流失口径）交叉注记区分"设计内剔除非误杀"
- **防坑**：消失仓≠流失（[[weekly-report-data]] 口径警告）；清单只建议不自动执行
- **依赖**：T0（闸门先行，回流仓不再被二次误杀）

## 第 1 批 · 词表地基（三卡可并行）

### T1a db_profiles 词表字段扩展 ｜✅ 2026-11-01 完成（提交号待填；新增词清单已呈用户）
- **目标**：每库档案加 `drivers`（依赖名）/`images`（镜像名）/`ports`，国产 4 库一次建全
- **输入**：`config/db_profiles.py` 现结构；10-30 文档的包名清单（GaussDB=huaweicloud-gaussdb 族、PolarDB=polardb-*/aliyun polardb20xx、YashanDB=yashandb、Dameng 补 DmJdbcDriver/DmProvider）；镜像名 pingcap/tidb、oceanbase/oceanbase、opengauss/opengauss
- **输出**：17 库档案三字段全量 + `validate` 增加词表一致性检查项
- **边界**：只动 db_profiles.py 与其 validate；**不动**任何消费方（接线是 T1c 的事）
- **验收**：`python -c "from config import db_profiles"` 通过；validate 全绿；17/17 库 `drivers∪drivers_exact` 与 `images` 非空（`ports` 允许声明性空：SQLite 嵌入式/云服务库无标准端口，notes 注明）；**新增词 diff 清单呈用户过目后才算过**（国产 4 库词无实测校准，10 分钟人工把关，防 T3b 才发现返工）
- **防坑**：精确词（pg）与子串词（psycopg）必须分字段标 `exact: true`，混在一起 T1b 会误伤

### T1b 精确词档位机制 ｜✅ 2026-11-01 完成（提交号待填；selftest 25/25 绿）
- **目标**：词表匹配支持两级——子串安全词与精确词（`==` 匹配）
- **输入**：T1a 字段结构；误伤反例集：`jsonwebtoken`/`pg-electron` 不得命中裸 pg、`@types/pg` 排除、`sqlite3` 在 package.json deps 与 devDeps 区分
- **输出**：`attribution/dep_match.py`（匹配函数：`@types/` 前缀排除、exact/子串两档、dev 降档标志）+ `attribution/fixtures/false_positives.json`（**误伤样本先落盘再写单测——契约先行**，正例+反例都带 expect 字段）+ `attribution/selftest_dep_match.py`（仿 selftest_evidence.py 手写断言风格，零网络）
- **验收**：反例用例全绿（含至少 10 条我从审计里挖的真实误伤样本）
- **依赖**：T1a 定字段结构

### T1c 三套词表归一 ｜✅ 2026-11-01 完成（提交号待填；readme 视图零 diff+db_scan 重跑 31,947 仓产物逐字节一致）
- **目标**：DEP_ALIAS/DIR_ALIAS 从 db_profiles 派生，消灭三套硬编码漂移
- **输入**：`interpret/unattr_judge.py` 的 E1/E3 表、db_scan 的 DB_VOCAB
- **输出**：`attribution/vocab.py` 派生层 + db_scan 改为 import（**unattr_judge 不碰**——由 T2e 整体重写，旧代码不再投入维护）
- **边界**：替换 db_scan 词表定义处，不改判定逻辑；**不动 interpret/unattr_judge.py**（11-01 决策：旧版废弃重写，工作区未推送改动由 T2e 吸收，不再"先拉齐"）
- **验收**：派生输出 vs 现表 diff 仅含 T1a 新增词（逐条人工过）；`python evidence/selftest_evidence.py` 绿；db_scan 重跑后提名量对比记录在案（扩词表→提名增加是预期收益）
- **防坑**：这是全链路最险的一卡——词表一变全线漂。diff 审查必须逐条人工过

## 第 2 批 · 引擎核心（链式：a→b→c→d）

### T2a attribution/ 包骨架
- **目标**：独立包，纯函数接口 `judge(evidence_pack) → verdict(+证据链+引擎版本)`，不碰网络不碰存储
- **输出**：`attribution/__init__.py`、`evidence_model.py`（六型证据统一 schema：`{型,库,票,出处,采集时间}`）、`api.py`（注意：六型中 rel_notes 在 T5b 前无数据源——schema 留空位是设计意图，勿因无源砍型）
- **验收**：schema 单测；空证据包 → 全空结论（不炸）
- **依据**：方案 §3.2 + 10-30 解耦五原则

### T2b 匹配器
- **目标**：指纹×词表×topic 三规则匹配，输出证据包
- **输入**：`state/evidence_cache_shards/`（31,884 仓，status=ok only）、pool.json topics、T1c 词表；topic 三规则（专有名才算/泛词排除 4,982/矛盾=互补进 recheck）
- **输出**：`attribution/matcher.py` + 单测
- **验收**：43 个 recheck 活案例（dep_only 清单）行为符合预期；nopCommerce 案例 topic(SQL Server) 与指纹不矛盾时输出"互补标记"而非冲突
- **防坑**：interp 分片键是 fn 哈希（值里带 fn）、evidence 键是 owner/repo——按 `rec["fn"]` 对齐；sha_mismatch 记录跳过

### T2c quorum 投票+E-CI 消歧
- **目标**：2/1/0.5 票制、≥2 票立案、E-CI 三规则（国产专属信号优先/纯国际不猜国产/双信号双标）
- **输出**：`attribution/quorum.py` + `rules_ci.py` + 单测
- **验收**：单测必须含实测活案例——`SSE-DZH/OceanBase` 纯 go-sql-driver 证据 → 判 MySQL 不判 OceanBase（国产）；加 oceanbase 镜像证据 → 双标 MySQL+OceanBase；单 topic（1 票）不立案
- **依据**：方案 §3.2/§3.4

### T2d 全池扫描 CLI
- **目标**：`attribution/scan.py --gap/--status`，全池离线跑出缺口报告
- **输出**：gap 报告（漏报/不完整/双源 strong 三清单，star 降序）+ 台账 `state/attribution_gap.json`
- **验收**：复现 10-31 实测数字 ±10%：匹配不到 ≥1,400 / 不完整 ≥1,300 / 双源 ≥700（词表已扩，数字只会更高）
- **防坑**：30,169 仓全量扫描注意内存——流式逐分片处理勿一次载入

### T2e 重写 unattr_judge（薄壳，零网络）
- **目标**：unattr_judge.py 推倒重写（名字不变）：读 evidence 分片 + attribution 词表/匹配，替代旧版自打 GitHub API 的侦查层（定时已因 Core 配额冲突暂定）
- **输入**：`state/evidence_cache_shards/`（31,884 仓）、T1c vocab、T2b matcher；旧版 10-29 未推送的 6 处口径修正（README 行号引证豁免/OOS 补 graal/testdata 弱路径/firm 收紧/--min-stars——重写前先 `git stash` 存档，口径融进新版）
- **输出**：新版 `interpret/unattr_judge.py`：圈范围（已解读无归属+未签发）→ 信号层（oos/edu/desc_pending/judged_no_support 口径不变）→ 证据层读取（按 `rec["fn"]` 对齐）→ matcher 判定 → 台账 `state/unattr_verdicts.json`（字段结构兼容，unattr_prescreen/T0 消费方不动）；旧 draft 122 名单先存档 `state/unattr_draft_122_archive.md`（T3a 素材）
- **边界**：只动 interpret/unattr_judge.py；CLI 兼容（--mode/--limit/--dry-run/--report-only/--min-stars 保留；--threads/--retry-errors 砍——无网络）
- **验收**：--dry-run 全量零网络跑通；金丝雀对拍：sqlmap 仍 draft≥6 库、sqlc 不再 ClickHouse 误报（testdata 弱路径）、SSE-DZH/OceanBase 判 MySQL 不判 OceanBase、duckdb/duckdb→oos、huihut/interview→edu；`python tools/unattr_prescreen.py` 能直接读新台账
- **防坑**：evidence 无记录的 fn → 新 status `pending_evidence`（进增量补采队列）；api_error/partial_scan 退役；写台账 atomic_write+LF
- **依赖**：T1c（词表）、T2b（匹配器——薄壳不自己造匹配逻辑）

## 第 3 批 · 试点（人介入，全方案第一个证伪点）

### T3a 试点清单生成
- **目标**：50 点名缺口（README 提名差 star 降序）+ 30 全空工具（eco=tool）+ 20 误杀候选（820 里 star 降序）+ draft 122 全量
- **输出**：`state/pilot_100.json` + markdown 复核表（每仓：证据卡+现判+建议判+留空人工栏）
- **验收**：四段名单无重叠、star 降序、证据卡字段完整

### T3b 人工复核+命中率报告（**人做，AI 不代填**）
- **产出**：命中率报告 → **准确率 ≥90% 才准进第 4 批；<90% 调词表回 T1a 重来，不硬推**
- **防坑**：[[interp-task-redesign]] 金标独立性教训——LLM 永不预填人工复核栏

## 第 4 批 · 裁决回写（过闸后）

### T4a 定点裁决
- **目标**：只问"该仓是否实际支持库 X"+ 附证据包（不重新全文解读，省 90% AI 费）
- **输入**：点名缺口 3,894 库位（README 提名差 3,283 + topics 差 611）
- **输出**：裁决结果 NDJSON `state/adjudications.ndjson`（幂等、断点续跑）
- **验收**：`python interpret/golden_eval.py --run --tag t4a` 对 base **不退步**（[[golden-eval-gate]] 金标 814 是一切 interpret 改动验收关）；烧完全量后**抽 50 条裁决人工过目**——golden_eval 管解读质量不管"是否支持库 X"的裁决对错，抽检过了才准进 T4b
- **防坑**：BudgetOut 原样 raise、仓边界收尾 exit 0（09-29 铁律）；烧 API 前先 `--limit 20` 冒烟

### T4b 回写器
- **目标**：quorum 立案结论写回 interp dbs；13,242 空适配全部打四类原因（真不涉及/范围外/证据不足/新仓未解读）
- **输出**：回写函数 + 空白态四类标注 + `state/attribution_writes.json` 台账（可回滚）
- **验收**：黑洞归零统计（13,242 → 100% 带原因）；golden_eval 对比不退；抽 20 条回写 diff 人工过
- **防坑**：只补空缺不改历史结论（方案铁律）；写分片用 touch(fn) 惯例（[[interp-cache-sharding]]）

### T4c 误杀复审批
- **目标**：820 个"提名过被 AI 否决"仓（sqlkata/postgis 级），star 降序重裁决
- **验收**：sqlkata 判回 5 库、postgis 判回 PostgreSQL（金丝雀案例必须过）

## 第 5 批 · 常态与专项（三卡并行）

### T5a 增量挂钩
- **目标**：每日跟 evidence incremental 同步判定；归属补全率报表进 CI summary；**attribution 各卡单测并入采集前置 selftest 链**——现在每夜绿门只有 `evidence/selftest_evidence.py`，引擎坏了要等下次全池扫描才发现
- **验收**：collect.yml 加一步，连续 3 晚报表落盘且不炸（CI 续跑教训 [[ci-resume-pitfalls]]）；attribution selftest 进 CI 后首晚绿

### T5b release notes 复验
- **目标**：release notes 命中 add/drop/support/deprecate+库名 → 触发该仓适配复验队列
- **验收**：构造 5 条合成 release note 单测全绿；真实仓冒烟 1 晚

### T5c Gitee MVP（可提前并行）
- **目标**：GoldenDB/GBase/YashanDB/TDSQL 四库，Gitee API v5 独立 token，平行池 `state/gitee_pool.ndjson` 不并入主池
- **验收**：独立失败域（Gitee 挂了主流程不受影响）；每晚 ≤500 仓封顶；四库生态清单落盘
- **防坑**：Gitee 限流 ~60/min 独立核算；README 内容有内容审查风险——输出脱敏（[[llm-paste-moderation]]）

---

## 怎么确保做卡的 AI 不遗漏、不出错（机制，非口号）

1. **卡自包含**：素材写到文件路径级，事实数字直接给——AI 不读全案、不自己统计（统计口径错是本项目最高频事故，今天审计就踩了 fn 哈希键的坑）
2. **验收是命令不是形容词**：每卡跑得出数字（selftest/golden_eval/diff 复现），"做完了"由机器说了算
3. **边界白名单制**：只许动列出的文件，越界即打回——防顺手改坏别处
4. **契约先行**：误伤反例集/活案例单测先写，实现对着用例跑（TDD）
5. **事实注入**：卡里的数字（1,468/3,894/96.7%）都是 10-31 实测，AI 拿来即用，重新统计=口径漂移之源
6. **每卡 1 PR 1 提交**：diff 可审、回滚单位小；脏工作区用 worktree+cherry-pick 推送法（[[attribution-evidence-layer]] 惯例）
7. **关键卡交叉复审**：T1c/T4b 两张高危卡完成后，由另一个会话只读复审再合（本项目两文档交叉审核有先例）
8. **台账断点续做**：本文件打勾+提交号，任何会话接手先读台账（CI 续跑事故教训）

## 批间闸门（推进纪律）

```
T0 ──→ T1(a∥b∥c) ──→ T2(a→b→c→d) ──→ T3(a→b 人工) ──≥90%?──→ T4(a→b→c) ──→ T5(∥)
                                                  │<90% 调词表回 T1 重来
```
- T3b 是全案第一个证伪点：不达标不硬推
- T4 前必须 T3 过闸——防"补全激进→误配上升"
- T2e 只依赖到 T2b，可与 T2c/T2d 并行
- 每卡完成即打勾+提交号，批次全绿才开下一批
