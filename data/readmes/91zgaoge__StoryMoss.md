<p align="center">
  <img src="docs/images/logo.png" alt="StoryMoss 草苔" width="140" />
</p>

<h1 align="center">StoryMoss · 草苔</h1>

<p align="center">
  🌿 <strong>越写越懂的 AI 小说创作桌面应用</strong><br/>
  幕后管理故事资产，幕前沉浸式写作，AI 在需要时随行辅助
</p>

<p align="center">
  <a href="./CHANGELOG.md"><img alt="Version" src="https://img.shields.io/badge/version-v0.99.8-gold"></a>
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

> 完整变更日志见 [`CHANGEL

[...截断...]

OG.md`](./CHANGELOG.md)。

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

- **问题**：v0.99.2 三平台构建成功，但 `upload-to-website` 在 macOS 更新包 `.sig` 报 `552 Disk full`；retention=5、服务器正好 5 版，清理「nothing to clean up」，官网 latest.json 停在 0.99.1。
- **结果**：上传脚本默认 `RELEASE_RETENTION_COUNT` 5→3，Cleanup Releases keep 默认 5→3；Cleanup keep=3 已释放空间，v0.99.2 上传重跑，后续 v0.99.3/v0.99.4 按新策略上传。

### v0.99.3 · 训练 compact/blind/probes + brief 预览 + 模型 GPU 诊断

- **问题**：v0.99.2 的 P1/P2 剩余项——本地模型没有 compact 提示词模式、训练页没有盲测开关、资产摘要阶段没有逐章进度、人物/线索/地点/新专名探针未接入报告、摘要缓存无 TTL、报告详情看不到模型实际收到的《前情提要》、模型页不显示 GPU 实测 prompt 上限。
- **结果**：新增 compact prompt（预算 6000/brief 2200/ledger 600/progress 900）、训练页盲测/紧凑勾选、资产逐章进度（35→40）+日志心跳、记忆探针（人物留存/线索未推进/地点跳切/疑似新专名）、V163 摘要缓存 30 天 TTL、`training_get_story_brief` 报告详情预览、`ModelHealthReport.prompt_limit_tokens` 模型页诊断。

### v0.99.2 · 续写训练资产分阶段 + 网关容量路由 + 进度/评分口径

- **问题**：v0.99.1 真机报告 0.63（承接 7.2）证明长程记忆有效，但资产重建仍失败——单次 26k prompt/8192 tokens 下 deepseek-v4 三次 CoT-only（content 空）、Qwren127 GPU OOM（16,781 tokens 需 9,439MB，仅 3,387MB）；brief 只剩 2042 字首尾摘要/0 白名单/0 cast；147 次 writer 调用 55 次失败；确定性摘要漏第 142 章 81% 的邵卫江；编审把原书后续差距误判为承接断裂；任务 40% 停 45 分钟。
- **结果**：资产重建改为「逐章小 prompt（并发 3、V163 缓存）→ 聚合 brief（只喂结构化摘要）」；JSON mode 补全 reasoning 截断 JSON；GPU OOM 学习模型 prompt 上限并按大小跳过本地小模型；确定性事件摘要（首句+中段冲突/引号/专名句+尾句）；批内每章 progress/log/heartbeat；judge 分列「承接（沙盒）」与「原书差距 reference_gap」；blind 反馈模式过滤真实后续节点。

### v0.99.1 · 续写训练长程记忆（前情提要 + 本批账本 + 设定白名单）

- **问题**：v0.99.0 后 10 章训练仍 0.40（承接 3.1、情节 3.3），编审结论「缺乏长程记忆与逻辑连贯性」；11-17 那轮资产重建成功（10 条逐章梗概都在库里）也只有 0.24（承接 1.2）——数据生成了，但没进 writer/planner 的 prompt。
- **根因**：writer 进度块只读最近 3 章正文末 220 字，第 11 章后 `scene_outcomes` 更把上下文整体替换成 3 条 outcome；planner 只读 3 条梗概，1400 字承接锚点又在 3200 字 directive 之外被截掉；资产重建失败时通用兜底用「正文头 600 + 尾 1800」生成「第 134 章单章回顾 + 下一拍规划」，截到 1200 字冒充故事大纲。
- **结果**：新增《前情提要》（逐章事实/未结线索/人物当前态/设定白名单），protected 全量注入 writer、planner 与编审；进度块改为全量逐章梗概 + outcomes 补充；批次维护滚动账本（第 n 章看到第 11..n-1 章实际发生了什么）；训练路径跳过 `ensure_story_outline` 伪大纲；通用大纲兜底改逐章摘要归纳并拒绝执行规划；红线引用白名单与未结线索。

### v0.99.0 · 续写训练「跨章复制/原地踏步」根修

- **问题**：10 章训练报告中第 14–17、20 章整段复制上一章，剧情原地踏步，文风漂移并自创「引魂蛆/骨刺」等玄幻设定。
- **根因**：并行批量中修订轮熔断后，兜底取稿按「黑板任意最新稿」取到了下一章；第 n 章被装配成第 n+1 章正文，相邻章因此字节相同（13/14、16/17、19/20），draft 11/15/18 从未落库。报告里的承接断裂大多是这条错位链，不是模型幻觉。
- **结果**：兜底取稿与修订兜底都只接受本章草稿；训练新增 5 条写作红线（设定/语体/推进/承接/设定白名单）、资产重建逐章梗概首尾兜底、跨章复制判「不可用」、质量门逐章单一归类；正文首行章名统一裁掉。

### v0.98.9 · 修复任务进度与执行日志显示不一致

- **问题**：任务详情头部进度已到 40%，展开的「执行日志」最新一条仍停在「进度 5%」；续写训练页的「最新日志」同样不刷新。
- **根因**：任务列表每 5 秒轮询，日志查询却只在任务完成/失败/取消时刷新；运行中的 `task-progress` 事件没有前端消费者，日志面板一直停留在展开时刻。
- **结果**：每个进度事件同时刷新任务列表与对应日志，日志随 5% → 20% → 30% → 40% 等阶段实时推进，并与头部进度、更新时间一致。

### v0.98.8 · 修复日志自动上传提议从未触发（三处日志布局不匹配）

- **问题定位**：官网日志包列表连续多日为空，本机在 11-11 手动上传后不再出现新包；排查发现自动提议从未执行到打包——诊断日志写