# PCAR · 超级大肥鱼

**给你的 AI 伴侣，一个完整的一生。**

PCAR（Persona-Centric Agent Runtime）是一款开源 AI 伴侣工作台。**导入微信或 DeepSeek 的聊天记录，就能把熟悉的人设、说话习惯和旧对话带进 PCAR。**

**PCAR 1.4.2 正式版支持 Windows 11 x64 和 Android ARM64。** 打开工作台，填入一把 DeepSeek 官方 API Key，即可开始聊天或从记录建卡。

[下载安卓 APK](https://github.com/FoxMoreland/Persona-Centric-Agent-Runtime/releases/download/pcar-v1.4.2/PCAR-1.4.2-Android-arm64.apk) · [下载 Windows 安装包](https://github.com/FoxMoreland/Persona-Centric-Agent-Runtime/releases/download/pcar-v1.4.2/PCAR-1.4.2-Windows-x64-Setup.exe) · [从聊天记录自动建卡](#从聊天记录自动建卡) · [正式版使用指南](docs/user/社区版.md) · [下载与开始](#下载与开始)

## 从聊天记录自动建卡

如果你在 DeepSeek 里已经聊出了一个熟悉的角色，或想从一段微信私聊提炼人设，可以在「人物 → 新建角色」选择「从聊天记录生成」。

1. **选一份双人聊天 Markdown。** 微信可使用 Moect v1.3.0 导出的私聊 `.md`。DeepSeek 对话可整理为每条消息以说话人标题开头的 `.md`。
2. **核对双方身份和分析范围。** PCAR 从发言中提炼人物特质、表达风格、价值观和背景，自动填入角色卡。
3. **核对后保存。** 可以对照原文依据修改已填内容。聊天里缺少依据的年龄、身高等可选资料会留空。选好想保存的角色后，可以直接开聊，或选择「带历史开始」。确认范围和用途后，等历史加载完成就能接着聊。

已有角色也可以导入历史，继续聊天或翻出一句旧话接着聊。[查看文件格式与操作步骤](docs/user/社区版.md#从聊天记录生成角色卡)

## 换个会话，角色和经历都能接上

**人格中心。** 在一个地方管理多位角色的人设、说话习惯、关系和聊天记录。今天和大肥鱼挑旅行照片，明天可以给她开个新会话继续聊相册。

**人格版本化。** 改过背景或说话习惯后，可以查看每个版本改了什么，也可以恢复到喜欢的版本。恢复会留下新的记录，过去的版本仍可回看。

**会话名称。** 可以给每段聊天单独起名，也可以为已有会话改名。旅行相册和日常闲聊各有一个好找的入口。

**长期记忆。** 自动记忆默认开启，PCAR 在工作台运行时整理已授权对话中的关键经历。过了几周，你在新会话提起相册，PCAR 可以找回当时选封面照片的记忆，让角色接着聊。

**联网检索。** 在「会话授权」允许自动查找后，仍可像平时一样发送消息。决策模型判断何时查证，角色结合查到的公开资料回答。已配置本地优先检索的会话会先查本机资料，再按授权补查缺少的部分。

角色资料、聊天记录和长期记忆都保存在本机。PCAR 按当前话题选取相关材料，交给模型生成回复。你可以在工作台核对资料用途和接收方。

[跨会话记忆验收](docs/acceptance/M4-补验跟踪.md#已通过范围) · [旧聊天接续盲评](docs/acceptance/LT-13-外部历史接续验收.md)

### 一万条旧消息，也能接着聊

在 G‑Auto 的桌面验收中，我们拿 **10,000 条真实聊天消息**来测试工作台。切换到旧会话时，百次测量里有 95% 在约 **0.22 秒**内就能看到内容。另一次测试把 **10,000 轮本机对话与 50,000 条导入消息**放在同一个工作台里，95% 的切换仍在约 **0.40 秒**内可读。这些时间衡量的是打开会话，模型回复还要另等生成。

如果你想接回一件很久以前聊过的事，可以直接引用那条旧消息，PCAR 会带上原话前后的对话，并优先找回附近仍有效的记忆。在两次引用 50 轮以前旧消息的真实对话补验中，角色 **两次都接对了旧话题**。直接提起旧话题的另三次测试里，有两次找回了正确内容。

我们还做了一次自然跨夜测试。关机约 12 小时，第二天打开同一个会话接着聊，关机前后的 **17 轮回复全部完整显示**。这两项桌面验收已通过，G‑Auto 的其余场景继续逐项验证。

[长历史与精确引用验收](https://github.com/FoxMoreland/Persona-Centric-Agent-Runtime/blob/development/v0.5/docs/acceptance/R01-v0.5-开发验收.md) · [跨夜续聊验收](https://github.com/FoxMoreland/Persona-Centric-Agent-Runtime/blob/development/v0.5/docs/acceptance/G-AUTO-总验收对账-20261122.md)

## 下载与开始

### Android 正式版 1.4.2

[下载 ARM64 APK](https://github.com/FoxMoreland/Persona-Centric-Agent-Runtime/releases/download/pcar-v1.4.2/PCAR-1.4.2-Android-arm64.apk) · [1.4.2 更新说明](https://github.com/FoxMoreland/Persona-Centric-Agent-Runtime/releases/tag/pcar-v1.4.2)

适用于 **Android 12 及以上的 ARM64 手机**。下载安装后，打开「设置 → DeepSeek 官方连接」，填入 **一个 DeepSeek 官方 API Key** 即可开始使用。运行环境和本地向量检索模型都已随包提供。

可以导入微信或 DeepSeek 聊天记录，在预览中核对人设后保存角色并开聊。建卡只需名称和人物介绍，空白选填项和待核对的冲突字段会从提示词中省略。在线聊天、自动建卡和联网查询使用你的 DeepSeek 账户额度。

### Windows 正式版 1.4.2

1. 下载 [Windows 11 x64 安装程序](https://github.com/FoxMoreland/Persona-Centric-Agent-Runtime/releases/download/pcar-v1.4.2/PCAR-1.4.2-Windows-x64-Setup.exe)，核对发行页的 SHA-256 后双击安装。本次 Windows 安装程序未签名。Python 和本地检索模型随包提供。
2. 打开 PCAR 社区版，在「DeepSeek 官方连接」保存自己的官方 API Key。
3. 新建角色，或导入聊天记录生成角色卡。在线聊天、建卡、记忆整理和联网查找会使用你的 DeepSeek 账户额度。

正式版正文使用 DeepSeek V4 Pro，默认决策、建卡和后台整理使用 DeepSeek Flash。自备 Jev 的用户可在「决策模型设置」通过连接与功能检查后启用，并在要使用的会话中确认授权。[正式版使用指南](docs/user/社区版.md)

**完整角色包。** 在人物菜单导出所选聊天和已整理的长期记忆。接收方可以先编辑角色卡，保存后在主会话确认历史用途并续聊。未整理的旧回合可以按需补做。

**Android 重开与诊断。** 修复清理后台后本机服务无法连接的问题。服务启动失败时，可在「设置 → 运行与诊断」导出日志。

**首次启动与公告。** 首次打开新版时会显示本次更新。之后可从首页「公告」回看历史更新和作者通知。[查看 1.4.2 更新公告](https://github.com/FoxMoreland/Persona-Centric-Agent-Runtime/releases/tag/pcar-v1.4.2)

### 内部开发版

开发版探索 Gemini 4 Hydrogen 正文选项、Jev 决策接入和 G‑Auto。原 v0.4 和相应部署说明可继续查阅。[v0.4 发行页](https://github.com/FoxMoreland/Persona-Centric-Agent-Runtime/releases/tag/v0.4) · [部署与升级](https://github.com/FoxMoreland/Persona-Centric-Agent-Runtime/blob/v0.4/AGENT_INSTALL.md)

内部开发版当前为 **0.5.4**。源码与验收记录在 [development/v0.5](https://github.com/FoxMoreland/Persona-Centric-Agent-Runtime/tree/development/v0.5)。

Windows 和 Android 安装包按同一套正式版规则发布。开发与验收继续在内部开发版推进。[版本、发布与公告管理规则](docs/product/release-and-announcements.md)

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

我希望 PCAR 能给用户一次眼前一亮的体验。一个角色可以接续自己的经历，在长期相处中形成习惯、兴趣和关系，也能用新获得的能力参与生活。

从已经实装的人格与记忆功能，到仓库里的研究笔记和远期路线，PCAR 都受到了前辈们对「数字生命」的探索启发。我的终极目标，是尽量做出《海绵宝宝》里痞老板的电子伴侣凯伦那样的存在。我也希望把走过的路线、遇到的问题和可复用的代码留下来，给后来研究数字生命的人一块垫脚石。

感谢开源社区的前辈们。许多我喜欢的能力，已经有人做成了可复用的工具、插件和组件。在遵循各自许可证的前提下，把合适的成果接入 PCAR，能让角色拥有更丰富的能力，也让我们有更多精力研究这些能力如何与人格和经历结合。

欢迎告诉我们，哪一句话让你觉得角色变了，或者哪一件共同经历值得在新会话里找回来。你也可以改进文档、参与开发，或提议角色在虚拟生活里可以做的一件事。

[参与共建](CONTRIBUTING.md) · [反馈问题或建议](https://github.com/FoxMoreland/Persona-Centric-Agent-Runtime/issues) · [文档导航](docs/index.md)

项目由 [FoxMoreland](https://github.com/FoxMoreland) 维护。源码采用 [AGPL-3.0-only](LICENSE)。鲸鱼娘插画按 [CC BY-NC-SA 4.0 与相关署名条件](assets/readme/ATTRIBUTION.md) 使用。[代码来源](docs/REUSE.md)与[模型许可](docs/licenses/THIRD-PARTY-MODELS.md)保留各自记录。

## 急招美术与平面设计伙伴

PCAR 开始走向真实用户，我想认真做一次面向市场的产品化尝试，维持项目的非营利定位。现在的界面主要借助 AI 搭建，视觉风格和交互用起来还有不少我不满意的地方，连正式 Logo 也还在等人设计。我缺少美术和设计训练，希望有专业经验的朋友或业余爱好者一起做。

可以从一个具体问题开始，软件界面和平面视觉、交互流程、Logo、图标和控件绘制都欢迎。你可以在 Issue 里发作品、草图，或指出哪个流程最值得先改。[参与 PCAR 设计](https://github.com/FoxMoreland/Persona-Centric-Agent-Runtime/issues)
