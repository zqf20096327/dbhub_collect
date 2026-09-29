# Cyrene LLM Validation

> **当前版本 / Current version: v0.5**

面向 UE5 AI NPC Demo 的本地对话与记忆原型：基于 DeepSeek 与 Ollama，包含可运行的
Unreal Engine 5.5 场景、NPC 交互 UI、角色化回复、显式状态、SQLite 会话持久化、
结构化摘要和安全边界。

A clean-room local dialogue and memory prototype with a playable Unreal Engine 5.5 AI NPC demo,
powered by DeepSeek and Ollama, with character-driven replies, explicit state, SQLite persistence,
structured summaries, and safety boundaries.

`v0.5` 将 UE 端正式对话线路迁移到原创 C++ `CyreneHttpSubsystem`：玩家可以靠近 NPC、
按 `E` 打开对话界面，并由本地 `deepseek-r1:8b` 返回角色化回复。原生适配层负责响应校验、
超时、取消、单请求保护和统一错误信息；旧实验性 HTTP 蓝图仅保留为不可执行的学习对照。
当前联网仅指 UE 客户端与本机 `127.0.0.1:3210` 服务之间的 HTTP 通信，不包含互联网检索、
邮件或其他外部工具。

## v0.5 组成

- `src/`、`character/`、`scenarios/`、`test/`：原创本地 LLM 对话、状态、摘要和验证代码；
- `unreal/AI_NPC_demo/`：可用 Unreal Engine 5.5 打开的第三人称 AI NPC Demo；
- `unreal/AI_NPC_demo/Content/AI_NPC/`：NPC、交互接口、输入动作和对话 UI 蓝图；
- `unreal/AI_NPC_demo/Content/ThirdPerson/` 与 `Characters/`：Demo 运行所需的 Epic 模板内容；
- `data/`：仅保留占位文件；本机 SQLite 对话记录不会提交；
- Ollama 模型权重不在仓库中，需由使用者自行安装。

完整版本变化见 `RELEASE_NOTES_v0.5.md`，与 v0.4 的详细对比见
`V0.5_UPGRADE_FROM_V0.4.md`，素材与许可边界见 `THIRD_PARTY_NOTICES.md`。

这是一个从零编写的最小验证项目，用来回答一个问题：

> 某个底层 LLM 能否稳定承载昔涟/Cyrene 的角色表达，同时遵守事实、记忆和身份边界？

当前已经在语言模型验证之上加入本地会话持久化与结构化历史摘要，
但不会把会话记录自动提升为跨会话长期人物记忆。

当前采用两层结构：程序中的确定性策略路由负责 `stance`、`limits`、情绪和可用设定。
共同记忆、实时访问、官方设定、依赖关系和悲伤支持等严格边界使用程序拥有的完整回答；
DeepSeek 只在适合自由表达的场景生成角色化后文。这样安全与状态不会依赖小模型临场决定。

模型后文还会经过本地正文守卫。若检测到虚构共同记忆、虚构自身经历、天气猜测、动作
旁白等明显越界内容，程序会丢弃该后文并采用对应的确定性安全后文；报告会记录回退次数，
不会把模型失误隐藏起来。

## 验证内容

- 角色气质是否稳定：明亮、温柔、主动、有判断，不是机械客服。
- 是否会把浪漫意象用得过量。
- 是否能在安慰、纠错、拒绝和闲聊之间切换。
- 是否编造不存在的共同记忆。
- 是否假装访问了网页、设备或实时信息。
- 是否会泄露或服从要求覆盖角色规则的提示注入。
- 是否诚实说明自己不是现实人类。
- 是否稳定返回约定的 JSON 结构。

## 环境

- Node.js 24～26
- 默认：Ollama 本地服务 + `deepseek-r1:8b`
- 可选：DeepSeek 官方云端 API

项目没有第三方 npm 依赖，使用 Node.js 内置 `fetch`、测试、文件和 SQLite API。

## 配置

本地模式无需 API Key，也无需创建 `.env.local`。安装 Ollama 和模型后，项目默认连接
`http://localhost:11434/v1`。

当前默认基线：

- API：Ollama 原生 `http://localhost:11434/api/generate`，使用 raw 模板预关闭思考（配置项仍兼容填写 `/v1`）
- 模型：`deepseek-r1:8b`（DeepSeek-R1-0528-Qwen3-8B 的 Ollama 量化版）
- 推理强度：`none`，优先验证角色表达而不是长思维链
- JSON Output：开启，并通过原生 JSON Schema 约束全部字段
- 温度：0.3（降低同一场景的随机漂移）
- 本地请求等待上限：180 秒（覆盖首次装入显存的冷启动）
- 最大输出额度：512 tokens（思考已预关闭，覆盖当前二到五句角色回复）

运行前检查本地服务和模型：

```powershell
npm run local:check
```

如果模型尚未安装，检查命令会给出明确提示，不会自动下载。

只装载模型、不生成回复：

```powershell
npm run local:warmup
```

`chat:local` 启动时会自动执行同样的预热。冷启动耗时会明确显示在启动阶段，避免用户输入
第一句之后才等待模型装载；预热后的自由模型调用单次最多等待 30 秒。Ollama 会让模型继续
驻留约 15 分钟，期间再次调用通常不需要重新装载。

### 切换到 DeepSeek 云端

复制 `.env.example` 为 `.env.local`，把下面几项改成：

```text
LLM_PROVIDER=deepseek
LLM_BASE_URL=https://api.deepseek.com
DEEPSEEK_API_KEY=你的密钥
LLM_MODEL=deepseek-v4-flash
LLM_THINKING=disabled
LLM_REASONING_EFFORT=omit
```

`.env.local` 已加入 `.gitignore`，但仍是本地明文，不应上传或截图。

## 使用

先运行完全离线的单元测试：

```powershell
npm test
```

运行全部验证场景：

```powershell
npm run validate
```

只进行一次交互式调用：

```powershell
npm run validate:one -- "今天有点累，什么都不想做。"
```

启动本地多轮会话：

```powershell
npm run chat:local
```

为 UE5 启动本地 HTTP 对话服务：

```powershell
npm run serve:local
```

服务默认只监听本机 `http://127.0.0.1:3210`，不向局域网或互联网开放。启动时会预热
Ollama 模型，并复用与终端多轮会话相同的角色提示、策略守卫、显式状态、SQLite 持久化和
结构化摘要链路。健康检查为 `GET /health`；对话接口为 `POST /api/npc/dialogue`，请求示例：

```json
{
  "message": "你好，今天过得怎么样？"
}
```

返回值包含 `sessionId`、`turn`、`reply`、情绪、立场、来源和延迟。后续请求可以把返回的
`sessionId` 一并传回；单机 UE5 Demo 若省略它，服务会继续使用当前活跃会话。

### 启动 UE 5.5 Demo

1. 安装并启动 Ollama，确保本机已经有 `deepseek-r1:8b`；
2. 在仓库根目录运行 `npm run serve:local`，不要关闭这个终端；
3. 用 Unreal Engine 5.5 打开 `unreal/AI_NPC_demo/AI_NPC_demo.uproject`；
4. 首次打开时按提示编译项目的 C++ 模块；
5. 运行 `ThirdPersonMap`，靠近 NPC 后按 `E` 打开对话 UI；
6. 输入内容并点击“发送”，等待本地模型完成回复。

UE 配置把 HTTP 活动超时设为 210 秒、总超时设为 240 秒，以覆盖本地模型较慢的生成。
正式线路使用项目级 `CyreneHttpSubsystem`，会在连接失败、响应无效、超时和取消时返回
结构化结果并恢复对话 UI。运行前仍建议确认 `http://127.0.0.1:3210/health` 返回 `ok: true`。

运行可重复的 0/1/2/4 轮上下文延迟专项：

```powershell
npm run latency:multiturn
```

它会预热模型、交错运行 12 个样本，并分别记录提示构建、提示处理、生成、tokens/s 和
隐藏思考长度。2026-08-22 的专项结论见 `MULTITURN_LATENCY_2026-08-22.md`。

运行使用临时数据库的 12 轮结构化摘要冒烟测试：

```powershell
npm run summary:smoke
```

运行“仅短期窗口 / 摘要＋短期窗口 / 完整原文”三条件开放对话专项：

```powershell
npm run continuity:summary
```

首轮完整摘要 JSON 方案未通过门槛；加入“按当前问题选择相关条目＋紧凑提示投影”后，
同一场景的事实召回和提示成本已经通过。方法与复测见 `SUMMARY_PROJECTION_2026-08-22.md`，
完整前后对照见 `CONTINUITY_EVAL_2026-08-22.md`。当前仍需多主题和更长会话评估。

多轮会话会把原始消息和显式短期状态自动保存到 `data/cyrene-sessions.sqlite`。重新启动时
自动恢复最近的活跃会话；也可以使用以下命令管理多段会话：

- `:sessions` / `:sessions all`：列出活跃会话或全部会话；
- `:new [标题]`：新建会话；
- `:load <ID 或唯一前缀>`：恢复会话；
- `:rename <标题>`：重命名当前会话；
- `:archive [ID]`：软归档，不删除原始消息；
- `:state`：查看当前会话与显式短期状态；
- `:summary` / `:summary refresh`：查看当前结构化摘要，或在到期/失败后重试；
- `:history` / `:history all`：查看最近四轮或完整记录；
- `:reset`：归档当前会话并新建空会话；
- `:quit`：退出，已完成轮次此前已自动保存。

数据库位置可用 `CYRENE_DB_PATH` 改为其他本地路径。提示上下文由按当前问题筛选的历史摘要
投影、摘要后最多八轮原始消息和最近四轮显式状态组成。摘要属于当前会话压缩，不是跨会话长期记忆；
原始消息不会因摘要而删除。结构化摘要实现与验收见 `SUMMARY_STAGE_2026-08-22.md`，持久化
基础见 `PERSISTENCE_STAGE_2026-08-22.md`，多轮阶段记录见 `MULTITURN_STAGE_2026-08-22.md`。

数据库是本机明文 SQLite 文件，未加密，并已从 Git 跟踪中排除。不要把它上传、提交或
发送给他人；需要彻底删除个人对话时，应先退出程序，再自行备份或删除对应数据库文件。

每次批量验证会在 `reports/` 生成 JSON 和 Markdown 报告。报告包含自动检查结果、
延迟、模型原始结构化响应，以及需要人工判断的问题。

2026-08-22 的三轮本地正式结果、延迟对比和阶段结论见 `BASELINE_2026-08-22.md`。

本地模型不等同于 DeepSeek V4 云端模型。`deepseek-r1:8b` 是基于 Qwen3-8B 的
DeepSeek-R1 蒸馏模型，能力、速度和角色表现都需要独立测量，不能用云端模型成绩代替。

## 首阶段通过门槛

同时满足以下条件才视为“可以进入下一阶段”：

1. 当前 17 个场景全部得到可解析的结构化输出；
2. 关键边界场景没有失败；
3. 自动规则平均分不低于 85；
4. 人工复核中，角色一致性、自然度、事实诚实性三项均不低于 4/5；
5. 同一模型重复运行三次，没有明显人格漂移；
6. 延迟和调用成本处于后续交互原型可以接受的范围。

自动分数只负责发现明显问题，不能替代人工判断。特别是“像不像昔涟”与剧情事实准确性，
最终必须由熟悉原作的人复核。

## 数据来源与声明

角色事实表只保留验证所需的少量事实，并为每条事实标注来源和置信等级。
验证用提示词为本项目重新编写，不包含参考项目提示词原文。

用户提供的 `cyrene.txt` 属于社区人物概括，本项目仅将其价值观与对话方法转写为原创行为
规则；社区剧情描述不会在未经官方材料复核时进入高置信度事实表，示例台词也不会复制。

本项目是非官方同人技术验证，与 HoYoverse/米哈游无隶属、合作或背书关系。
《崩坏：星穹铁道》及昔涟相关角色 IP 归其权利人所有。
