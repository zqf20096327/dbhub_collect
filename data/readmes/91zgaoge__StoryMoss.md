<p align="center">
  <img src="docs/images/logo.png" alt="StoryMoss 草苔" width="140" />
</p>

<h1 align="center">StoryMoss · 草苔</h1>

<p align="center">
  🌿 <strong>越写越懂的 AI 小说创作桌面应用</strong><br/>
  幕后管理故事资产，幕前沉浸式写作，AI 在需要时随行辅助
</p>

<p align="center">
  <a href="./CHANGELOG.md"><img alt="Version" src="https://img.shields.io/badge/version-v0.99.27-gold"></a>
  <a href="./LICENSE"><img alt="License" src="https://img.shields.io/badge/license-ISC-blue.svg"></a>
  <a href="https://github.com/91zgaoge/StoryMoss/actions/workflows/build.yml"><img alt="Build" src="https://github.com/91zgaoge/StoryMoss/actions/workflows/build.yml/badge.svg"></a>
  <img alt="Platform" src="https://img.shields.io/badge/platform-macOS%20%7C%20Windows%20%7C%20Linux-lightgrey.svg">
  <img alt="Tauri" src="https://img.shields.io/badge/Tauri-2.4-orange.svg">
  <img alt="React" src="https://img.shields.io/badge/React-18-61dafb.svg">
  <img alt="Rust" src="https://img.shields.io/badge/Rust-1.95-dea584.svg">
</p>

---

## ✨ 核心特性

| | 特性 | 说明 |
| :---: | --- | --- |
| 🎬 | **双界面创作** | 幕前「墨纸」沉浸写作 + 幕后「机械」工作室管理，两套设计语言各得其所 |
| 🎛️ | **自适应幕后工作台** | 暗色主题、容器感知卡片与表单、独立面板滚动；800×600 到宽屏均无逐字竖排、固定限高裁切或悬浮遮挡 |
| 🤖 | **Agency 多代理创作** | 主创 / 管理 / 编辑审计三代理黑板并行协作，每章经 Gate v2 加权质量门（代码 0.2 / 规则 0.3 / 编辑 0.5，阈值 0.75）才交付；你的修改率作为独立信号回流 |
| 🗂️ | **语料资产** | 新闻 / 故事 / 概念 / 灵感 / 图片 / 链接 / 笔记按故事隔离；支持导入、AI 提炼、转为角色/世界观/伏笔草稿、交给导演调度 |
| 🎬 | **导演 Agent 与剧组对话** | 代理工作室三栏：导演统筹管理 / 编审 / 主创；子 agent 异步派发、心跳、租约、重试与审批；幕后可直接 @ 三个 agent |
| ⚡ | **分时介入架构** | 幕前续写走三角色主创、编辑审计后台化；划词改写仍可走完整质检——解开「质量与速度不可兼得」的根本矛盾 |
| 🧠 | **越写越懂你** | 持续学习：从创作事件观察模式 → 提炼 instinct → 确认后晋升为可复用技能；Tab 接受 / Esc 放弃还会回灌到每拍写作手法的选择（章法偏好） |
| 🧭 | **长篇记性与计划** | 续写前按需检索前文原文（【前文相关原文】只读块）；卷/弧中层计划（卷目标 / 卷末高潮 / 须兑现伏笔）；改稿后下游章纲标记待重规划、逐条勾选才落库——长篇不崩的四件套 |
| 🧪 | **判官一致率与文笔校准** | 「创作评估」按你的改动核对编辑的每条审查意见（判得准不准有数字）；文笔基线阈值经公版人类语料校准（`resources/voice_corpus/`） |
| 📝 | **PROBLEM 七元素** | 简单指令自动基于 Erik Bork 七元素增强为强力 Logline，驱动大纲与续写 |
| 🌍 | **资产强关联** | 世界观 / 故事大纲 / 场景大纲 / 用户指令四位一体显式调和，剧情不跑偏 |
| 🔄 | **资产回流** | 每章正文生成后自动提取角色 / 关系 / 世界观 / 大纲回流累积进资产库，手工编辑永不覆盖，续写越写越强关联 |
| 🔌 | **多模型适配** | OpenAI / Anthropic / Ollama / 本地 API，角色 × 任务模型路由 |
| 🔄 | **双源自动更新** | GitHub Releases 优先、官网备用；清单与下载网络故障自动换源，备用源限同一版本，签名验证始终启用 |
| 📚 | **全链路资产管理** | 角色 / 世界构建 / 场景 / 知识图谱 / 伏笔看板 / 叙事分析 / 拆书，AI 不「吃书」 |
| ❤️ | **情感回路** | 单拍强制「事件→评估→情绪变化→行动/台词→代价」因果链；批量续写按章生成 1–3 幕；关系张力账本、情感债务与读者面板；情感驱动情节，不是形容词 |
| 🧩 | **叙事契约** | 每拍先编译场契约（目标 / 具名阻力 / 转折 / 必须结果 / 情感链 / 字数），writer 按这一页写；gate 对具名阻力缺席、正文过短、契约无效硬拦截；幕后选中另一部小说即切换，生成中也不静默拒绝 |
| 🧵 | **多 write 并行** | 同一故事最多 3 个 write 任务并行；章号由数据库原子分配，Append 同章排队，资产补齐加租约，不抢号、不重复造资产 |
| 📌 | **固定语料** | 语料页「固定用于续写」后，素材以只读块进入单拍/批量 writer prompt（≤4 条、≤1200 字）；图片语料读取尺寸/摘要；deepseek-v4.1-flash 等视觉模型可读原图，作者可强制 AI 遵守/化用 |
| 🪪 | **姓名编译** | 创世角色名做重名 / 同用字 / 同姓扎堆 / 长度塌缩 / 模型陈词组合校验；常见姓可正常使用，但不再整组「林雪/沈夜/苏墨/顾寒」式二字塌缩 |

---

## 📸 界面预览

<p align="center">
  <img src="docs/images/frontstage-preview.png" alt="幕前写作界面" width="82%" />
</p>

<p align="center"><em>幕前 · 极简全屏写作，AI 输入栏随行辅助，文思模式主动给萤火提示</em></p>

<p align="center">
  <img src="docs/images/backstage-preview.png" alt="幕后工作室" width="82%" />
</p>

<p align="center"><em>幕后 · 故事 / 角色 / 世界构建 / 场景 / 知识图谱 / 代理工作室等全套资产管理</em></p>

---

## 🚀 安装与运行

### 下载预构建版本

访问官网 `https://storymoss.top` 或 GitHub Releases 页面，下载对应平台安装包后直接安装即可。

### 从源码运行

需要安装 [Node.js](https://nodejs.org/)（推荐 20 LTS）和 [Rust](https://rustup.rs/)。
仓库通过 `rust-toolchain.toml` 固定 Rust 版本为 **1.95.0**，`rustup` 会自动下载对应工具链。

```bash
# 1. 克隆仓库
git clone https://github.com/91zgaoge/StoryMoss.git
cd StoryMoss

# 2. 安装前端依赖
cd src-frontend && npm install

# 3. 安装 Tauri CLI 并运行桌面应用
cd ..
npm install -g @tauri-apps/cli
cargo tauri dev
```

> **注意**：`Cargo.lock` 已纳入版本控制。如需升级依赖，请在本地验证 `cargo clippy` / `cargo test` 通过后再提交。

### 仅运行前端（开发调试）

```bash
cd src-frontend
npm run dev
```

然后在浏览器打开 `http://localhost:5173/`。

### 构建官网落地页

```bash
cd landing
npm install
npm run build
```

构建产物位于 `landing/dist/`，可部署到任意静态托管服务。开发模式运行 `npm run dev`，测试运行 `npm run test`。

---

## 🆕 最新动态

> 完整变更日志见 [`CHANGE

[...截断...]

LOG.md`](./CHANGELOG.md)。

### v0.99.27 · 修复任务心跳与 finish 的落库竞态

- **问题**：v0.99.26 的 macOS CI 唯一失败用例暴露真实时序——任务心跳是 fire-and-forget，`finish` 可能先写完成状态，后到的心跳被 `WHERE status IN ('running','waiting')` 静默丢弃，`turn_count` 少计；历史 tag 构建的「reporter heartbeat flake」都是它。
- **结果**：`TaskReporter` 登记未落库的心跳，`finish` 先等待它们落库（每个上限 5s）再写完成状态；心跳仍不阻塞 LLM 调用。新增 8 次心跳后 finish 的确定性回归用例。Rust **2314/17**（+1）、tsc 0、Vitest **732/3**、Playwright **144/5**、fmt/clippy/guard/prettier 全绿。

### v0.99.26 · 日志巡检：后台保活探测降频 + 探测开销收敛

- **问题**：本机 v0.99.25 一天日志里 **15,584 次健康探测 vs 45 次真实生成**——10s 保活对所有模型无条件轮询（含付费远端 `deepseek-v4` 10,413 次），凌晨无人使用也每小时 ~1,000 次；tracing 86% 的行是探测，另有 3,324 次探测顺带重新读取 `AppConfig`（DB 忙时还会新建连接池）。
- **结果**：保活改为按模型节奏——闲置模型（2 分钟无真实生成）5 分钟一次、活跃模型 10s 一次，连续失败 ≥3 的死模型交给退避重试；探测提示词加 60s 缓存，不再每次查 SQLite/AppConfig。预计探测请求降到 1,000 次/天量级，日志里真实生成与错误更容易被发现。Rust **2313/17**（+5）、tsc 0、Vitest **732/3**、Playwright **144/5**、fmt/clippy/guard/prettier 全绿。

### v0.99.25 · 日志巡检：健康探测退避失效 + 自动上传旧错误误计

- **问题**：Windows v0.99.14 日志包显示，三个不可用模型跨 24 小时各被「退避重试」93–97 次且退避值恒为 30s——`probe_model` 对调用失败返回 `Ok(success=false)`，调度器只判 `Err`，把失败当成功并不断重置退避；同时 11-23 提议上传日志时称「20 条新错误」，实际全部来自 6–15 天前（`creative_workflow.log` 只追加，旧实现只按文件 mtime 过滤）。
- **结果**：调度器改按真实 `ProbeResult.success` 判定并按 30→60→…→3600s 指数退避；自动上传错误计数增加行级时间过滤（tracing `timestamp` / 工作流 `ts` / legacy 行首时间戳）；Step2 知识生成对枚举外关系类型（真机 `同门师兄妹`）降级为 `RelatedTo`，不再让整段 JSON 解析失败。Rust **2308/17**（+4）、tsc 0、Vitest **732/3**、Playwright **144/5**、fmt/clippy/guard/prettier 全绿。

### v0.99.24 · 训练报告通用规则提升层 + 生产回归探针

- **问题**：v0.99.23 已复用训练能力，但训练报告里的具体改进仍只回灌下一轮训练；具体书名/人名/情节不能跨故事搬运。
- **结果**：新增 `training_rules` 与 V165 `training_rule_promotions`，从报告维度均分/通用信号提取 8 类不含书名/人名/情节的规则，按 key 去重累计；生产 writer/修订/genesis/auto_write/gate 自动注入规则块，装配后 `[ProductionProbes]` 核对文风/AI 腔/主线/承接/推进/口吻/节奏/钩子；旧报告升级时幂等补齐。Rust **2304/17**（+5）、tsc 0、Vitest **732/3**、Playwright **144/5**、fmt/clippy/guard/prettier 全绿。

### v0.99.23 · 续写训练能力全量复用：创世/普通续写/导演/单章均启用

- **问题**：主线投影、原文语体样本/基线、前情提要（StoryBrief）、直连编审 gate 此前只在续写训练沙盒注入（训练执行器显式 `with_*`），普通创世与续写只拿到部分能力；训练出的质量改进无法进入真实创作路径。
- **结果**：新增生产复用层——从故事大纲/CHAPTER 合同/卷纲/Blueprint 派生故事主线，从前文 scene 抽语体样本/基线（无前文退到 StyleDNA/corpus），确定性构建前情提要；genesis fastpath、单章/批量/导演续写、修订、章纲、GateRunner/后台 QC 全部接入；生产默认直连编审 JSON；genesis 自动绑定题材推荐风格 DNA；自动续写/单角色 writer 任务也注入语体样本、前情提要、红线等章号无关能力；生产写作红线 9 条。批量主线只有首章用「下一节点」，后续章用合同/卷纲 beat。训练显式字段优先，不覆盖训练 LLM brief。Rust **2299/17**（+9）、tsc 0、Vitest **732/3**、Playwright **144/5**、fmt/clippy/guard/prettier 全绿。

### v0.99.22 · v0.99.21 真机验证：总分 0.734 / 口吻 7.11 / 原书差距 7.07

- **结果**：本机 10 章训练报告 `018e787e`（13:20–14:12）加权 **0.734**（历轮最高：v0.99.16 0.729、v0.99.20 0.689、v0.99.17 0.7175），style **7.01**、plot **7.67**、voice **7.11**、pacing **7.17**、hooks **7.28**，承接 8.9、`reference_gap` **7.07**（最初问题轮 2.9）；编审 **6 pass / 4 revise / 0 unavailable**，质量门 3 通过 / 7 修订 / 0 降级，主线探针 9/10 ✓；10 章全部落库 2.7–3.8k 字。承接近乎无缝、145/150/151 主线节点与真实章几乎逐一对应、148「妖孽，看我法宝」/151 碑线/152 身世落地。
- **仍未根治**：146 小梅诊室试探改村口跪求、149 玉碟敕神/宋辨经考据压成三件套、147 周成荤腔纯情化、148/152/153 偶发格言/预告腔；文风探针句长仍 9.6–14.0（原文 19.2）。下一轮按报告改进项继续。测试 **2290/17**（文档验证版，数量不变）、tsc 0、Vitest **732/3**、Playwright **144/5**、fmt/clippy/guard/prettier 全绿。

### v0.99.21 · 创作 effort 回滚 + 封顶空稿降 effort 重试 + 文风门禁建议化

- **问题**：v0.99.20 真机报告 `21b15629` 显示低 effort 让 10 章全部产出、编审 10/10 可用（上轮 8/10），但总分 **0.689**（上轮 0.7169）、style 6.75、voice 6.5（上轮 7.125）—— editor 判「黄玄然絮叨被削成短刀、陆尘音功能化、第一人称自嘲递减」。144 章 editor 原判 style 8/voice 8，确定性 style gate（句长 10.8<0.75×19.2）强制修订后报告 style 反而 6.5；空 content 仍在：writer 32768 封顶，`should_retry_truncated_empty` 因 `max_tokens < cap` 从未重试。
- **结果**：创作 effort 回滚（结构化仍 low）；空稿封顶时仍重试一次并临时降 `reasoning_effort=low`（首次保留原 effort）；文风/AI 腔 `style_issue` 改为建议性——只在 editor 已判 RevisionRequired 且 style<7 时并入 issues，不再强制改 pass。新增断言更新；Rust **2290/17**（数量不变）、tsc 0、Vitest **732/3**、Playwright **144/5**、fmt/clippy/guard/prettier 全绿。

### v0.99.20 · 推理模型创作调用默认 low：训练主创不再被 CoT 吃空

- **问题**：v0.99.19 真机训练启动段 12:05–12:08 连续 5 次 `agency_writer` 空 content——提示词约 37,899 tokens、completion 29,773–31,978 tokens、`finish_reason=le