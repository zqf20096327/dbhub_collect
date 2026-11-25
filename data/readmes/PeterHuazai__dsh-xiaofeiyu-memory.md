# 小肥鱼记忆库 · dsh-xiaofeiyu-memory

**中文** | [English](README.en.md)

> 给 AI 一个会遗忘、会分区、还会被监督的长期记忆。

这是一个 **DeepSeek Harness（DSH）插件**，也是一套可以独立运行的本地记忆库：
多轮长对话里最容易出问题的两件事 ——「记住不该混的」和「忘掉不该记的」—— 它都做了工程化处理。

> 作者说明：这是**非人工智能专业的学生**拿 DeepSeek Harness 写着玩的插件。功能是真的能跑（187 个自动化测试全绿），
> 但设计上一定还有不少幼稚和可以改进的地方，欢迎大家指正和评价，不喜也勿喷 🙏

---

## 它解决什么问题

| 长对话里的老毛病 | 这里的做法 |
| --- | --- |
| 不同项目的记忆互相串味 | **分区隔离**：一个话题一个分区，`recall` 必须带分区，跨分区查询在代码层被拒绝 |
| 什么都存，越存越慢、越存越乱 | **遗忘曲线**：`retention = exp(-Δt / stability)`，用上就变牢、不用就衰减，低到阈值转休眠/归档，主干永远不睡 |
| 上下文太长 → 反复读同一堆东西 → 命中率掉 → 开始胡说 | **守卫 + 审查**：上下文压力/命中率/重复读取/陈旧占比四项打分，到线就 `warn`/`block`，并给出「只按主干作答」的指令 |
| 守卫给了建议却不知道怎么执行 | **一键修复**：面板卡片 / `mem fix` 先出计划（5 步、带影响条数和预览），勾选后带 `confirm` 才真执行 |
| 细节记得太细，主干反而想不起来 | **三层记忆**：★主干 / ·场景 / 细节；`task end` 自动把结论并进主干、落一条场景；新会话第一轮自动注入主干速览 |
| 找不到上次那条结论 | **两段式召回 + token 预算**：`index` 只给前 90 字，`recall` 默认 1200 tokens 硬上限，超了先降级再丢尾部并告诉你丢了几条 |
| 不知道记忆到底好不好用 | **实时看板**：命中率趋势、每条的记忆曲线、每个分区的记忆板块，图表可交互、可导出导入、参数可在线微调 |
| 库坏了全丢 | **多重保险**：SQLite 主库 + JSONL 影子日志（可从日志重建）+ 定时备份 + 完整性校验 + 回收站 + 汇报可恢复 |
| 重要结论记得不如随手记的牢 | **FSRS 式自适应 + 主干强化**：命中降难度、拉长间隔，遗忘打折；主干有留存地板（默认 0.55）并可用 `reinforce` 追加强化 |

## 三个核心机制（一句话版）

1. **分区（partition）**：所有数据的根作用域。`remember / recall / search / audit` 全部按分区走，
   `item_link` 也禁止跨分区连接（会直接抛「分区不可混用」）。**读操作走严格分区**：名字打错就报
   `unknown partition`，不会偷偷建空分区；只有写入入口（`remember` / `task start` / `import`）才会自动化建。
2. **遗忘曲线（forgetting curve）**：每条记忆有自己的 `stability`（稳定度，单位天）。
   - 被召回且回填 `used: true` → `stability *= (1 + growth)`，越用越牢；
   - 回填 `used: false` → 衰减更快；
   - `retention < forgetThreshold` → 转 `dormant`（休眠，可被显式召回），`< archiveThreshold` → `archived`；
   - `pinned` 或 `importance >= trunkImportance` 的条目**永不休眠** —— 这就是「保留主干」。
3. **守卫（guard）**：`score = 0.45*上下文压力 + 0.25*(1-命中率) + 0.2*重复读取 + 0.1*陈旧占比`，
   并且有**硬阈值**：上下文 token 越过 `contextWarnTokens` 直接 warn，越过 `contextBlockTokens` 直接 block（不靠分数加权碰运气）。

再往上还有一层**闭环**：`task start` 给主干 → 干活时 `recall/feedback/guard` → `task end` 自动 consolidate（结论并主干 + 场景记忆）并清理休眠 → `mem daily` 出健康日报、`mem eval` 量化召回质量、`mem site` 导出静态站点。插件形态下 `agent/pre-step` 与 `agent/turn-stopping` 会自动替你跑守卫（写操作的自动清扫默认关闭）。

## v0.2 加了什么

- **三层记忆**：不新增列，用 `kind` + `pinned` + `importance` 推导 `layer`（trunk / scene / detail），老库零迁移；
  `mem trunk --digest` 给一段紧凑主干，`xfy_memory_trunk` 工具同源。
- **token 预算**：`recall` 有 `budget`（默认 `recall.budgetTokens = 1200`），超出时 `full → index` 降级、再丢尾部，
  返回里带 `totalTokens / budgetDropped / budgetDowngraded / layers`。
- **守卫一键修复**：`planFix` 出计划（sweep 休眠 / trunk 补主干 / backup 备份 / cleanup 清统计 / merge 合并近似），
  `applyFix` 必须带 `confirm: true`；面板是勾选式卡片，CLI 是 `mem fix`（默认只预览）+ `mem fix --apply`。
- **第一轮自动注入主干**：`agent/pre-step` 中间件在 `turn===1 && step===1` 时往 `decision.messages` 里塞一条
  `source.kind = 'xiaofeiyu-memory'` 的速览消息（约 100 tokens），第二轮起不再注入。开关是 `injectTrunk`。
- **脚手架不计入知识**：`task start` 写的「任务开启：…」条目不进召回候选、不进主干归档、不进合并候选
  （仍可用 `search` 翻到）。

## 安装

### 作为 DSH 插件

```bash
# 发布到市场后：
dsh plugin --profile web add dsh-xiaofeiyu-memory

# 本地开发：
dsh plugin --profile web add link:G:/华仔的小肥余专属工作区/xiaofeiyu-memory
```

装上之后会多出 **14 个原生工具**（`xfy_memory_*`），数据默认落在 `~/.dsh/xiaofeiyu-memory/data`，
路径可以在插件配置 `root` 里改，也可以用环境变量 `XFY_MEMORY_ROOT`。

宿主带 `webServer` 时插件还会挂 `/xfy-memory`（HTTP API + 看板静态页），并把 `lib/client.js` 作为**原生 React 面板**注册到右侧栏与会话头按钮——不需要额外开服务。两半端的细节见 [docs/DSH-PLUGIN.md](docs/DSH-PLUGIN.md)。

### 作为独立命令行 / 服务（不装插件也能用）

```bash
git clone https://github.com/PeterHuazai/dsh-xiaofeiyu-memory.git
cd dsh-xiaofeiyu-memory
npm install          # 只有 sqlite-vec 两个可选依赖
node src/server.mjs  # 看板：http://127.0.0.1:8787/

node src/cli.mjs partition add --name myproject --title "我的项目"
node src/cli.mjs task start --partition myproject --title "今天要做什么"
node src/cli.mjs recall --partition myproject "关键词" --detail index --budget 1200
node src/cli.mjs remember --partition myproject --title "结论" --body "依据与边界" --importance 4
node src/cli.mjs trunk --partition myproject --digest --max-tokens 200
node src/cli.mjs fix --partition myproject            # 先看计划
node src/cli.mjs fix --partition myproject --apply --step backup
node src/cli.mjs task end <taskId> --summary "一句话结果" --md "## 做了什么
## 结论
## 遗留"
```

## 14 个插件工具

| 工具 | 干什么 |
| --- | --- |
| `xfy_memory_recall` | 分区内召回这次最该看的几条（词面 + 向量 + 衰减 + 重要度），返回 `eventId`；带 `budget` token 上限 |
| `xfy_memory_remember` | 写一条长期结论（同内容自动去重）；`kind` 支持 `trunk` / `scene` |
| `xfy_memory_search` | 全量翻找 + 分页 + 排序，只给片段（想起关键词但记不清内容时用） |
| `xfy_memory_feedback` | 回填「用上了没有」——命中率和遗忘曲线的唯一信号来源 |
| `xfy_memory_guard` | 四项打分 → `ok`/`warn`/`block` + 处置指令；`plan: true` 出修复计划，`apply: true` + `confirm: true` 才执行 |
| `xfy_memory_trunk` | 主干速览（比 `recall` 更省，只记得大方向时用），按 token 预算截断并给层计数 |
| `xfy_memory_audit` | 记忆体检报告（陈旧、膨胀、低命中、无主干、任务泄漏、备份过期…） |
| `xfy_memory_digest` | 这段时间学到什么、用上什么、什么在冷掉（含每日桶） |
| `xfy_memory_health` | 库结构体检 + 可选安全修复（补向量、删悬空关联） |
| `xfy_memory_dedupe` | 找重复条目，只给建议不自动合并 |
| `xfy_memory_summarize` | 把散记忆归纳成一条钉住的主干，旧主干用 `superseded_by` 取代 |
| `xfy_memory_link` | 条目关联（结论↔依据），同分区硬校验 |
| `xfy_memory_explain` | 解释这条为什么被召回 / 为什么快忘了（打分逐项拆开） |
| `xfy_memory_task` | 任务闸门：`start` 建会话并返回主干；`end` 必须写汇报文档并自动 consolidate |

## 看板

![看板](docs/screenshots/dashboard-dark.png)

`node src/server.mjs` 之后打开 <http://127.0.0.1:8787/>，单文件、无外网请求、随时能离线用：

- 分区概览、记忆条目表（带**层**列：★主干 / ·场景 / 细节）、**记忆曲线**（悬停看某一天、点图例隐藏序列）
- **命中率趋势**（点柱子筛当天事件）、守卫事件、审查结论、**一键修复卡片**（出计划 → 勾选 → 执行）
- 回收站、参数微调（25+ 项，改完立即生效）、导入导出、汇报文档（可删/可恢复/可彻底清理）
- 向量索引面板（后端、覆盖数、语义指纹状态）、多模态描述面板（批量给图片写描述）
- **检索与自检**面板（库内检索 / 摘要 / 体检 / 查重 / 归纳主干），条目里点「为什么」看打分拆解

![检索与自检](docs/screenshots/tools-dark.png)
- 检索与自检面板（search / digest / health / dedupe / summarize / explain 的图形入口）

## 目录结构

```
index.js            插件 host 半端（14 个工具 + /xfy-memory 路由 + pre-step 中间件 + 第一轮注入）
lib/hostdeps.mjs    从宿主树里取 schemastery / defineTool，取不到就本地等价实现
lib/client.js       插件 client 半端：DSH 右侧栏原生 React 面板（__ModuleLoader__ 包裹）
cordis.patch.yml    插件挂载点
src/db.mjs          SQLite schema + 影子日志 + 备份 + 配置
src/engine.mjs      分词、遗忘曲线、remember/recall/feedback、三层判定、主干摘要、consolidate、休眠清理、附件
src/vector.mjs      本地哈希向量 + 语义指纹 + 三后端探测 + ANN
src/guard.mjs       守卫打分与审查、一键修复（planFix / applyFix）
src/harness.mjs     DSH 历史会话扫描与导入（多帧 zstd、一项目一分区）
src/tasks.mjs       任务闸门、汇报写删恢复、导入导出、参数夹紧
src/vision.mjs      多模态描述（可选视觉模型）
src/tools.mjs       search/digest/explain/link/expand/pin/health/dedupe/summarize
src/server.mjs      HTTP API + 静态看板
src/cli.mjs         命令行
web/index.html      看板（单文件内联）
docs/DSH-PLUGIN.md  插件形态说明（两半端、槽位、waterfall 契约、安装与验证）
tests/run-tests.mjs 187 个断言
```

## 参数（都能在看板里改，`updateConfig` 会按合理区间夹紧）

| 键 | 默认 | 含义 |
| --- | --- | --- |
| `curve.stabilityBaseDays` | 7 | 新记忆的初始稳定度（天） |
| `curve.forgetThreshold` | 0.25 | 低于它转休眠 |
| `curve.archiveThreshold` | 0.02 | 低于它转归档 |
| `curve.trunkImportance` | 4 | 重要度达到它永不休眠 |
| `recall.topK` / `minScore` | 8 / 0.12 | 召回条数与分数线 |
| `recall.detail` / `indexBodyChars` | index / 90 | 默认只给前 90 字正文（省 token） |
| `recall.budgetTokens` | 1200 | 单次召回的 token 硬上限 |
| `guard.contextWarnTokens` / `contextBlockTokens` | 120000 / 200000 | 硬阈值 |
| `vector.vectorWeight` / `vectorFloor` / `fpWeight` | 0.6 / 0.15 / 1.5 | 向量融合与语义指纹权重 |
| `curve.adaptive` | true | FSRS 式复习：命中降难度抬间隔，遗忘乘 0.45 |
| `curve.trunkFloor` / `trunkBoostGrowth` / `trunkBoostMax` | 0.55 / 1.35 / 4 | 主干留存地板与强化上限 |
| `maintain.cleanupDays` / `mergeThreshold` / `digestTokens` | 30 / 0.6 / 320 | 一键修复的清理窗口、合并阈值、主干摘要预算 |
| `injectTrunk`（插件配置） | true | 是否在新会话第一轮自动注入主干速览 |
| `lifecycle.recycleDays` | 30 | 回收站保留天数 |

## 已知边界（不吹牛）

- **DeepSeek 官方 API 没有 embeddings 端点**（只有 chat/completions 与 FIM），所以向量是「本地哈希打底 + DeepSeek 生成语义指纹」。
  想要真 embedding 请把 `vector.provider` 指向任意 OpenAI 兼容的 `/v1/embeddings`。
- `sqlite-vec` / `qdrant` 只是**探测位**：装了 sqlite-vec 扩展就会用它做 ANN，否则退回暴力向量扫描（几千条量级完全够）。
- 多模态默认关闭（`multimodal.vision.enabled=false`），需要你自己给一个 OpenAI 兼容的视觉端点；不配也不会报错，只是图片没有描述、召回不到。
- 看板是给本地单人用的，没有登录鉴权，别直接暴露到公网。

## 测试

```bash
node tests/run-tests.mjs            # 通过 187 / 失败 0
node tests/plugin-smoke.mjs         # 插件冒烟：14 个工具真实注册、预置修复计划、第一轮注入（26 项全 PASS）
node tests/client-panel.test.mjs    # 面板渲染与请求 URL（107 项断言）
node tests/cordis-waterfall.test.mjs # 真 cordis 库复现 waterfall 契约（5 项）
```

覆盖：分区隔离与严格分区、去重、index/full 两种召回、token 预算丢弃与降级、遗忘曲线与反馈、守卫硬阈值、
一键修复计划与确认、三层判定与主干摘要、consolidate 幂等、汇报写删恢复清理、导入导出、
影子日志重建、附件与描述、向量惰性补齐、语义指纹、HTTP 集成、CLI 回归、8 个工具的边界（跨分区拒绝、悬空关联修复…），
以及自适应曲线（主干地板 vs 普通指数、FSRS 复习、主干强化、曲线预测不破地板）、相近合并、收尾自动归档主干、检索评测、健康日报、静态站点导出。

## License

MIT
