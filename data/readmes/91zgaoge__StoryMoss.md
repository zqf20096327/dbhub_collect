<p align="center">
  <img src="docs/images/logo.png" alt="StoryMoss 草苔" width="140" />
</p>

<h1 align="center">StoryMoss · 草苔</h1>

<p align="center">
  🌿 <strong>越写越懂的 AI 小说创作桌面应用</strong><br/>
  幕后管理故事资产，幕前沉浸式写作，AI 在需要时随行辅助
</p>

<p align="center">
  <a href="./CHANGELOG.md"><img alt="Version" src="https://img.shields.io/badge/version-v0.99.13-gold"></a>
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

### v0.99.13 · 切章保存不再误丢稿 / 更新检查不再假报错（日志巡检）

- **问题**：v0.99.10 日志包（11-17～11-22）里 27 条 ERROR 集中在两处。第一，10 次「正文已被另一窗口更新，拒绝用旧快照覆盖」的保存冲突，全部发生在切章后 10–50ms，冲突对象都是**上一章**——上一章在途保存被换成新章的 CAS 基线，后端正确拒绝、前端却误报「另一窗口已更新」并停止重试，切章前最后几次编辑因此丢失。第二，12 次「检查更新失败」+3 次「安装更新失败」：本机 GitHub 源不可达、官网已明确返回「无更新」，但旧裁决把「任一源失败」整体升级成更新失败，用户每次启动都看到报错。
- **结果**：CAS 基线改为「按 scene 绑定 + 保存入口同步捕获」，跨 scene 不发送指纹、在途保存不再覆盖新章基线；视觉空稿（`<p></p>` 等）直接跳过写入，避免把前端基线写成空稿后永久冲突。更新检查改为「有源成功给出确定结果即采用」，另一源失败只附 `warning` 诊断日志；所有源都失败才报错。新增 8 条回归测试（Rust 4 / 前端 4）。

### v0.99.12 · 续写训练真机复盘（日志保留 / 主角识别 / 修订直出 / 探针收敛）

- **问题**：11-22 的 10 章训练（报告 `aa70a919`）编审判 6 章修订，但报告写「0 章真正修订、7 章判修订但修订未完成」——修订只要 tool_loop 正常结束就记账，模型没写黑板也算完成；v0.99.11 重跑时单章修订 prompt 约 30k 字符（15k tokens），24 分钟仍未完成。同日重启后当日 tracing 从新进程第一行开始：日志保留条件写反，启动时删掉刚写入的日志、留下 7 天前旧文件。确定性 cast 兜底把出场最早的「大波浪卷女人」当成角色表第一项，旧 roster 便标成主角；brief 里「我/主角/周成」并存，编审把主角姓名判成配角。记忆探针仍报 `蓝漆铁/黄铜钥/邵先生/传呼机/冷库门`。
- **结果**：日志保留改为「早于 7 天才删」，当日 tracing 不再丢失；主角只按原文自称句式（我叫X/以X身份/X自报/自称X）识别，并把「我/主角/阴脉先生」合并到权威姓名，roster 不再假定第一项是主角；训练批量修订跳过 ReAct，用完整正文 + 逐条问题直出并校验「与首稿不同、≥300 字」，写回后再走第二轮 gate（round-2 也跟随直连 JSON）——修订完成才记账；LeadWriter 单章草稿写入上限 2 次，第二稿成功写入即采用，避免单章 9 稿轮询；首稿裁决 pass、修订稿变 revise 时回退首稿；探针改为长串优先 + 称谓/器物收尾过滤；写作红线新增「禁止不是…而是…排比/比喻堆叠、每章至少一次配角互动、主角身份统一」。新增 6 条回归测试。

### v0.99.11 · 模型调度止血（撞额度重试 + reasoning_effort + 冷却兜底）

- **问题**：本机 11-22 实机对账确认三处调度缺陷：writer 只申请 8192 输出，推理模型 CoT 吃满后 `content` 为空（`finish_reason=length`），连续 8 次空正文最终被当成主创熔断；`LlmProfile.reasoning_effort` 字段存在但从未发送给 API，JSON/抽取任务一直按默认 high 思考；`candidate_count=1` 时一次空正文就把唯一候选冷却 10 分钟，后续请求直接报「所有候选模型都因连续空正文进入冷却」。
- **结果**：适配器解析 `finish_reason` 与 `reasoning_tokens`，空正文撞 `length` 时把 `max_tokens` ×4（封顶 32768）重试一次；打通 `reasoning_effort`（profile 显式值优先，JSON/结构化任务默认 low，未声明 reasoning 的端点不发送）；全部候选冷却时恢复候选兜底而非硬失败；keepalive 与 pre-call 探测 5s/4 tokens → 30s/64 tokens，空正文告警 60s 节流。新增 7 条回归测试。

### v0.99.10 · 训练报告/标题落库/记忆探针收尾（日志巡检）

- **问题**：11-21 两轮真机 10 章训练（v0.99.9）第二轮总分升到 0.86、承接 9.9，但报告出现「0 章质检降级（编辑审计未完成，已放行保产出）」自相矛盾；第一轮第 12/13 章自动取名因 `database is locked` 失败、标题缺失；记忆探针仍把 `宏达投/达投资`（白名单长词窗口碎片）、`条案上/像是有/缕青烟`（方位/虚词窗口）误报为新专名。
- **结果**：降级说明只在确有降级时出现；章节标题写回改用 Immediate 事务，WAL 下不再因 BUSY_SNAPSHOT 绕过 `busy_timeout`。记忆探针按白名单子串与重叠窗口合并，并过滤方位收尾/虚词窗口。新增 1 条回归测试并扩充质量门文案断言。

### v0.99.9 · 训练报告与编审裁决健壮性（日志巡检）

- **问题**：11-20 真机 10 章训练总分 0.70、承接 9.1、编审 10/10 可用，但仍有 2 章质检降级；日志显示模型返回合法 JSON 却被判解析失败——`suggestions` 被模型写成对象数组而解析器只接受字符串；报告把诊断维度「原书差距」当短板并注入空修正；记忆探针误报跨词垃圾专名、线索只显示内部 ID。
- **结果**：`EditorVerdict` 宽容解析（对象 suggestions / 字符串分值 / null 维度不再拖垮整份裁决）；诊断维度不再进入短板与下一轮指令；记忆探针输出可读线索描述并过滤跨词边界噪声。新增 6 条回归测试。

### v0.99.8 · 章节标题统一（中文数字解析 + 第二章 铜钱与脚印）

- **问题**：历史库/训练沙盒同时存在 `第 134 章`、`第12章`、`香炉边的银镯与铜钱` 等混合标题；中文数字无法解析门禁章号，自动取名只写裸标题，展示层混用。
- **结果**：新增章节标题纯函数与中文数字转换；`parse_chapter_number` 支持阿拉伯/中文/空格/带后缀；训练源章标题从正文首行恢复；自动取名写「第二章 雨夜叩门」；幕前统一展示「第二章 铜钱与脚印」；V164 迁移归一旧库标题。新增 10 条回归测试。

### v0.99.7 · 续写训练真机复盘修复（编辑审计/门禁记录/deadline/资产）

- **问题**：v0.99.6 真机 10 章训练总分 0.683（承接 8.89、情节 7.0），但 9/10 章质检降级、10 章只有 1 行门禁记录；编辑审计 tool_loop 连续解析失败，Ds10/deepseek-v4 CoT-only 空正文、Qwren GPU OOM；run deadline 10×240s+120s 在第 17 章撞线；进度日志每章「0 字」；聚合漏世界观/角色。
- **结果**：训练编辑审计直连 JSON（带参照资产 + CoT JSON 提取，成功跳过 tool_loop）；失败门禁统一落 `editor_gate_records`；批量 deadline 600s/章+600s、上限 4h；`chapter_chars` 显示真实字数；世界观/角色用逐章事实与 grounded cast 确定性兜底；编审第三次短采样 + 换路由。新增 6 条回归测试。

### v0.99.6 · 批量/训练 trace 终态收尾（日志巡检）

- **问题**：续写训练/批量续写的 trace 在任务结束后仍显示 `running`（11-17 的 250 步、11-18 的 530 步训练 trace，1 天后仍未收尾）；v0.96.1 的 trace 收尾只覆盖创世/续写/单角色。
- **结果**：批量路径按结果与取消标记写入 completed/failed/cancelled，与 run 终态一致；新增 1 条三态回归测试。

### v0.99.5 · 用量统计与功能使用页签修复（日志巡检）

- **问题**：用量统计查询 `llm_calls.cost`，但该表从未有 `cost` 列，数据洞察页每次加载都报 `no such column: cost`；功能使用页签调用的 `get_feature_usage_stats` 命令后端从未注册，恒报 `Command not found`（均来自 v0.99.0 真机日志）。
- **结果**：统计 SQL 只聚合次数与 token（金额字段保留恒 0），`'global'` 恢复跨故事汇总语义；补齐并注册 `get_feature_usage_stats` 命令（默认 30 天、限幅 1–365）；新增 4 条回归测试。

### v0.99.4 · 官网 Release 保留策略 5→3（修复 552 Disk full）

- **问题**：v0.99.2 三平台构建成功，但 `upload-to-website` 在 macOS 更新包 `.sig` 报 `552 Disk full`；retentio