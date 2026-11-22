# PCAR · 超级大肥鱼

**给你的 AI 伴侣，一个完整的一生。**

PCAR（Persona-Centric Agent Runtime）是一款开源桌面 AI 伴侣工作台。**导入微信或 DeepSeek 的聊天记录，就能把熟悉的人设、说话习惯和旧对话带进 PCAR。**

**社区版 1.0 支持 Windows 11 x64 一键安装。** 打开工作台，填入一把 DeepSeek 官方 API Key，即可开始聊天或从记录建卡。

[下载社区版 1.0](https://github.com/FoxMoreland/Persona-Centric-Agent-Runtime/releases/tag/community-v1.0.0) · [从聊天记录自动建卡](#从聊天记录自动建卡) · [社区版使用指南](docs/user/社区版.md) · [下载与开始](#下载与开始)

## 从聊天记录自动建卡

如果你在 DeepSeek 里已经聊出了一个熟悉的角色，或想从一段微信私聊提炼人设，可以在「人物 → 新建角色」选择「从聊天记录生成」。

1. **选一份双人聊天 Markdown。** 微信可使用 Moect v1.3.0 导出的私聊 `.md`。DeepSeek 对话可整理为每条消息以说话人标题开头的 `.md`。
2. **核对双方身份和分析范围。** PCAR 从发言中提炼人物特质、表达风格、价值观和背景，自动填入角色卡。
3. **核对后保存。** 可以对照原文依据修改已填内容。聊天里缺少依据的年龄、身高等可选资料会留空。选好想保存的角色后，可以直接开聊，或选择「带历史开始」接上原来的对话。

已有角色也可以导入历史，继续聊天或翻出一句旧话接着聊。[查看文件格式与操作步骤](docs/user/社区版.md#从聊天记录生成角色卡)

## 换个会话，角色和经历都能接上

**人格中心。** 在一个地方管理多位角色的人设、说话习惯、关系和聊天记录。今天和大肥鱼挑旅行照片，明天可以给她开个新会话继续聊相册。

**人格版本化。** 改过背景或说话习惯后，可以查看每个版本改了什么，也可以恢复到喜欢的版本。恢复会留下新的记录，过去的版本仍可回看。

**长期记忆。** 为角色开启自动记忆后，PCAR 在工作台运行时从聊天中整理关键经历。过了几周，你在新会话提起相册，PCAR 可以找回当时选封面照片的记忆，让角色接着聊。

**联网检索。** 聊到需要查证的公开信息，可以在会话授权范围内发起联网查找，并让角色结合查到的资料回答。已配置本地优先检索的会话会先查本机资料，再按授权补查缺少的部分。

角色资料、聊天记录和长期记忆都保存在本机。PCAR 按当前话题选取相关材料，交给模型生成回复。你可以在工作台核对资料用途和接收方。

[跨会话记忆验收](docs/acceptance/M4-补验跟踪.md#已通过范围) · [旧聊天接续盲评](docs/acceptance/LT-13-外部历史接续验收.md)

## 下载与开始

### 社区版 1.0

1. 在[社区版 1.0 发行页](https://github.com/FoxMoreland/Persona-Centric-Agent-Runtime/releases/tag/community-v1.0.0)下载 Windows 11 x64 安装程序，双击安装。Python 和本地检索模型随包提供。
2. 打开 PCAR 社区版，在「DeepSeek 官方连接」保存自己的官方 API Key。
3. 新建角色，或导入聊天记录生成角色卡。在线聊天、建卡、记忆整理和联网查找会使用你的 DeepSeek 账户额度。

社区版正文使用 DeepSeek V4 Pro，决策、建卡、后台整理和联网取材使用 DeepSeek V4.1 Flash。[社区版使用指南](docs/user/社区版.md)

### 主版本 v0.4

主版本提供 Gemini 4 Hydrogen 正文选项和 Jev 决策接入，沿用 Agent 辅助部署，可从 v0.3 原机升级。[v0.4 发行页](https://github.com/FoxMoreland/Persona-Centric-Agent-Runtime/releases/tag/v0.4) · [部署与升级](https://github.com/FoxMoreland/Persona-Centric-Agent-Runtime/blob/v0.4/AGENT_INSTALL.md)

社区版与主版本并行发行，分别提供安装入口和数据目录。

## 远期愿景

![社区鲸鱼娘在窗边翻开相册，身旁的书信与书本象征过去的经历和未来的日常](assets/readme/superfish-vision.webp)

*愿景插画，依据社区鲸鱼娘设定进行 AI 辅助二创。[形象来源与署名](assets/readme/ATTRIBUTION.md)。*

### 她有自己的时间

在 PCAR 的远期设想里，大肥鱼醒来时，昨天读到一半的书还摊在桌上。你去忙自己的事，她可以读完那一章、试着照料一盆植物，也可以睡个午觉。等你回来，她有了自己的事想和你聊。

我们想把聊天里的连续性延伸到日常生活。读到了哪一页、窗边的植物什么时候浇过水、明天有什么安排，都能在下次醒来时接着做。

<img src="assets/readme/continuity-concept.png" width="720" alt="设计方向：同一个人格连接身份与关系、过去的经历、关切与计划、生活状态及未完成的事情">

*设计方向 · 同一个人格如何接续自己的经历、关系和计划。*

### 在经历中，成为自己

她试着照料一盆植物，记下哪扇窗的光线合适，第二天想起给它换个位置。这样的经历可以改变她下一次的选择。

![远期生活设想，按从左到右、从上到下阅读：鲸鱼娘醒来、独自阅读与记笔记、分享照料植物的发现、夜间休息](assets/readme/daily-life-vision.webp)

*远期生活设想 · 醒来、独处、重逢、休息。*

虚拟生活是 PCAR 的远期方向。我们想让角色参与活动、看到行动的结果、回顾自己的经历，慢慢形成兴趣和习惯。

休息也算进日常。远期设计里，角色睡觉时暂停模型调用，醒来再看留言、继续手头的事。全天在线由独立的云端方案探索。学习工具、制作技能和维护自身能力也在远期路线中。

[完整产品路线](docs/product/roadmap.md) · [数字人格与虚拟生活研究](docs/long-term/README.md)

## 一起把这段人生做出来

PCAR 目前主要围绕 DeepSeek 开发，也从 DSH 等开源社区的插件与互动实践中学习。

欢迎告诉我们，哪一句话让你觉得角色变了，或者哪一件共同经历值得在新会话里找回来。你也可以改进文档、参与开发，或提议角色在虚拟生活里可以做的一件事。

[参与共建](CONTRIBUTING.md) · [反馈问题或建议](https://github.com/FoxMoreland/Persona-Centric-Agent-Runtime/issues) · [文档导航](docs/index.md)

项目由 [FoxMoreland](https://github.com/FoxMoreland) 维护。源码采用 [AGPL-3.0-only](LICENSE)。鲸鱼娘插画按 [CC BY-NC-SA 4.0 与相关署名条件](assets/readme/ATTRIBUTION.md) 使用。[代码来源](docs/REUSE.md)与[模型许可](docs/licenses/THIRD-PARTY-MODELS.md)保留各自记录。
