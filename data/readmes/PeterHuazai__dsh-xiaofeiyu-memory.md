# 小肥鱼记忆库 · dsh-xiaofeiyu-memory

> 给 AI 一个会遗忘、会分区、还会被监督的长期记忆。

这是一个 **DeepSeek Harness（DSH）插件**，也是一套可以独立运行的本地记忆库：
多轮长对话里最容易出问题的两件事 ——「记住不该混的」和「忘掉不该记的」—— 它都做了工程化处理。

> 作者说明：这是**非人工智能专业的学生**拿 DeepSeek Harness 写着玩的插件。功能是真的能跑（129 个自动化测试全绿），
> 但设计上一定还有不少幼稚和可以改进的地方，欢迎大家指正和评价，不喜也勿喷 🙏

---

## 它解决什么问题

| 长对话里的老毛病 | 这里的做法 |
| --- | --- |
| 不同项目的记忆互相串味 | **分区隔离**：一个话题一个分区，`recall` 必须带分区，跨分区查询在代码层被拒绝 |
| 什么都存，越存越慢、越存越乱 | **遗忘曲线**：`retention = exp(-Δt / stability)`，用上就变牢、不用就衰减，低到阈值转休眠/归档，主干永远不睡 |
| 上下文太长 → 反复读同一堆东西 → 命中率掉 → 开始胡说 | **守卫 + 审查**：上下文压力/命中率/重复读取/陈旧占比四项打分，到线就 `warn`/`block`，并给出「只按主干作答」的指令 |
| 找不到上次那条结论 | **两段式召回**：`index` 只给前 90 字（省 token），真要用再取全文；再加向量余弦 + DeepSeek 语义指纹兜住「换了个说法」 |
| 不知道记忆到底好不好用 | **实时看板**：命中率趋势、每条的记忆曲线、每个分区的记忆板块，图表可交互、可导出导入、参数可在线微调 |
| 库坏了全丢 | **多重保险**：SQLite 主库 + JSONL 影子日志（可从日志重建）+ 定时备份 + 完整性校验 + 回收站 + 汇报可恢复 |

## 三个核心机制（一句话版）

1. **分区（partition）**：所有数据的根作用域。`remember / recall / search / audit` 全部按分区走，
   `item_link` 也禁止跨分区连接（会直接抛「分区不可混用」）。
2. **遗忘曲线（forgetting curve）**：每条记忆有自己的 `stability`（稳定度，单位天）。
   - 被召回且回填 `used: true` → `stability *= (1 + growth)`，越用越牢；
   - 回填 `used: false` → 衰减更快；
   - `retention < forgetThreshold` → 转 `dormant`（休眠，可被显式召回），`< archiveThreshold` → `archived`；
   - `pinned` 或 `importance >= trunkImportance` 的条目**永不休眠** —— 这就是「保留主干」。
3. **守卫（guard）**：`score = 0.45*上下文压力 + 0.25*(1-命中率) + 0.2*重复读取 + 0.1*陈旧占比`，
   并且有**硬阈值**：上下文 token 越过 `contextWarnTokens` 直接 warn，越过 `contextBlockTokens` 直接 block（不靠分数加权碰运气）。

## 安装

### 作为 DSH 插件

```bash
# 发布到市场后：
dsh plugin --profile web add dsh-xiaofeiyu-memory

# 本地开发：
dsh plugin --profile web add link:G:/华仔的小肥余专属工作区/xiaofeiyu-memory
```

装上之后会多出 13 个原生工具（`xfy_memory_*`），数据默认落在 `~/.dsh/xiaofeiyu-memory/data`，
路径可以在插件配置 `root` 里改，也可以用环境变量 `XFY_MEMORY_ROOT`。

### 作为独立命令行 / 服务（不装插件也能用）

```bash
git clone https://github.com/PeterHuazai/dsh-xiaofeiyu-memory.git
cd dsh-xiaofeiyu-memory
npm install          # 只有 sqlite-vec 两个可选依赖
node src/server.mjs  # 看板：http://127.0.0.1:8787/

node src/cli.mjs partition add --name myproject --title "我的项目"
node src/cli.mjs task start --partition myproject --title "今天要做什么"
node src/cli.mjs recall --partition myproject "关键词" --detail index
node src/cli.mjs remember --partition myproject --title "结论" --body "依据与边界" --importance 4
node src/cli.mjs task end <taskId> --summary "一句话结果" --md "## 做了什么
## 结论
## 遗留"
```

## 13 个插件工具

| 工具 | 干什么 |
| --- | --- |
| `xfy_memory_recall` | 分区内召回这次最该看的几条（词面 + 向量 + 衰减 + 重要度），返回 `eventId` |
| `xfy_memory_remember` | 写一条长期结论（同内容自动去重） |
| `xfy_memory_search` | 全量翻找 + 分页 + 排序，只给片段（想起关键词但记不清内容时用） |
| `xfy_memory_feedback` | 回填「用上了没有」——命中率和遗忘曲线的唯一信号来源 |
| `xfy_memory_guard` | 上下文压力/命中率/重复读取/陈旧占比 → `ok`/`warn`/`block` + 处置指令 |
| `xfy_memory_audit` | 记忆体检报告（陈旧、膨胀、低命中、无主干、任务泄漏、备份过期…） |
| `xfy_memory_digest` | 这段时间学到什么、用上什么、什么在冷掉（含每日桶） |
| `xfy_memory_health` | 库结构体检 + 可选安全修复（补向量、删悬空关联） |
| `xfy_memory_dedupe` | 找重复条目，只给建议不自动合并 |
| `xfy_memory_summarize` | 把散记忆归纳成一条钉住的主干，旧主干用 `superseded_by` 取代 |
| `xfy_memory_link` | 条目关联（结论↔依据），同分区硬校验 |
| `xfy_memory_explain` | 解释这条为什么被召回 / 为什么快忘了（打分逐项拆开） |
| `xfy_memory_task` | 任务闸门：`start` 建会话并返回主干；`end` 必须写汇报文档 |

## 看板

![看板](docs/screenshots/dashboard-dark.png)

`node src/server.mjs` 之后打开 <http://127.0.0.1:8787/>，单文件、无外网请求、随时能离线用：

- 分区概览、记忆条目表、**记忆曲线**（悬停看某一天、点图例隐藏序列）
- **命中率趋势**（点柱子筛当天事件）、守卫事件、审查结论
- 回收站、参数微调（25+ 项，改完立即生效）、导入导出、汇报文档（可删/可恢复/可彻底清理）
- 向量索引面板（后端、覆盖数、语义指纹状态）、多模态描述面板（批量给图片写描述）
- **检索与自检**面板（库内检索 / 摘要 / 体检 / 查重 / 归纳主干），条目里点「为什么」看打分拆解

![检索与自检](docs/screenshots/tools-dark.png)
- 检索与自检面板（search / digest / health / dedupe / summarize / explain 的图形入口）

## 目录结构

```
index.js            插件 host 半端（注册 xfy_memory_* 工具）
lib/hostdeps.mjs    从宿主树里取 schemastery / defineTool，取不到就本地等价实现
cordis.patch.yml    插件挂载点
src/db.mjs          SQLite schema + 影子日志 + 备份 + 配置
src/engine.mjs      分词、遗忘曲线、remember/recall/feedback、休眠清理、附件
src/vector.mjs      本地哈希向量 + 语义指纹 + 三后端探测 + ANN
src/guard.mjs       守卫打分与审查（含记录软删/恢复/清空）
src/harness.mjs     DSH 历史会话扫描与导入（多帧 zstd、一项目一分区）
src/tasks.mjs       任务闸门、汇报写删恢复、导入导出、参数夹紧
src/vision.mjs      多模态描述（可选视觉模型）
src/tools.mjs       search/digest/explain/link/expand/pin/health/dedupe/summarize
src/server.mjs      HTTP API + 静态看板
src/cli.mjs         命令行
web/index.html      看板（单文件内联）
tests/run-tests.mjs 129 个断言
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
| `guard.contextWarnTokens` / `contextBlockTokens` | 120000 / 200000 | 硬阈值 |
| `vector.vectorWeight` / `vectorFloor` / `fpWeight` | 0.6 / 0.15 / 1.5 | 向量融合与语义指纹权重 |
| `lifecycle.recycleDays` | 30 | 回收站保留天数 |

## 已知边界（不吹牛）

- **DeepSeek 官方 API 没有 embeddings 端点**（只有 chat/completions 与 FIM），所以向量是「本地哈希打底 + DeepSeek 生成语义指纹」。
  想要真 embedding 请把 `vector.provider` 指向任意 OpenAI 兼容的 `/v1/embeddings`。
- `sqlite-vec` / `qdrant` 只是**探测位**：装了 sqlite-vec 扩展就会用它做 ANN，否则退回暴力向量扫描（几千条量级完全够）。
- 多模态默认关闭（`multimodal.vision.enabled=false`），需要你自己给一个 OpenAI 兼容的视觉端点；不配也不会报错，只是图片没有描述、召回不到。
- 看板是给本地单人用的，没有登录鉴权，别直接暴露到公网。

## 测试

```bash
node tests/run-tests.mjs    # 通过 129 / 失败 0
node tests/plugin-smoke.mjs # 插件形态冒烟：13 个工具真实注册并逐个调用（11 项全 PASS）
```

覆盖：分区隔离、去重、index/full 两种召回、遗忘曲线与反馈、守卫硬阈值、汇报写删恢复清理、导入导出、
影子日志重建、附件与描述、向量惰性补齐、语义指纹、HTTP 集成、CLI 回归，以及 8 个新工具的边界（跨分区拒绝、悬空关联修复…）。

## License

MIT
