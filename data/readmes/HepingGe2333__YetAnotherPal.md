# YetAnotherPal（Yap）

[English](README.en.md) · **简体中文**

YetAnotherPal（Yap）是一个 Android + iOS 的 AI 陪伴应用：把「人格」建模成长期存在的联系人，而不是一组可调的聊天参数。两端共享同一套数据模型、同一套行为约定和同一份备份文件；应用显示名为 **Yap**。

[![GitHub](https://img.shields.io/badge/GitHub-HepingGe2333%2FYetAnotherPal-181717.svg?logo=github)](https://github.com/HepingGe2333/YetAnotherPal)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](https://github.com/HepingGe2333/YetAnotherPal/blob/main/LICENSE)
[![Platform](https://img.shields.io/badge/platform-Android%208.0%2B%20%7C%20iOS%2016%2B-lightgrey.svg)](https://github.com/HepingGe2333/YetAnotherPal#架构与技术栈)
[![Tests](https://img.shields.io/badge/tests-1414%20Android%20%7C%201625%20iOS%20%7C%2090%20agentcore%20%7C%20358%20agentd-brightgreen.svg)](https://github.com/HepingGe2333/YetAnotherPal#构建与测试)
[![CI](https://github.com/HepingGe2333/YetAnotherPal/actions/workflows/ci.yml/badge.svg)](https://github.com/HepingGe2333/YetAnotherPal/actions/workflows/ci.yml)

## 项目状态

| 项 | 值 |
| --- | --- |
| 版本 | `0.13.0`（内测，`0.x` 体系；版本策略与发版流程见 [CONTRIBUTING.md](CONTRIBUTING.md#版本号与发版)） |
| 数据库 schema | v13（消息按 200 条一块；人格带世界预设/话风/当前活动；两端版本号对齐） |
| 备份格式 | v5（`format = "myfriend.backup"`、`formatVersion = 5`，图片/头像、搜索 provider、世界预设与话风随备份走；v1–v4 仍可读）。格式名为历史兼容保留，产品名已改为 YetAnotherPal（Yap） |
| 构建号 | Android `versionCode` 与 iOS `CURRENT_PROJECT_VERSION` 保持相等 |
| 单元测试 | Android 2018 条（193 类）+ 56 条 instrumented、`:agentcore` 90 条、`:agentd` 556 条、iOS 2049 条（`swift test`）+ 16 条 App-hosted |
| 持续集成 | GitHub Actions：Linux 跑 Android / `:agentcore` / `:agentd`，macOS 跑 `swift test` + iOS `build-for-testing` |

## 特性概览

| 领域 | 已实现的能力 |
| --- | --- |
| 首页 | 联系人列表：头像、名字、最后一条消息、时间、未读数；一人一段会话 |
| 检索 | 聊天记录全文检索：摘要高亮、按人格与时间过滤、**逐区块扫描且没有候选上限**、点结果跳回该消息并高亮（两端语义一致，契约在 `spec/search/`） |
| 聊天 | SSE 流式、停止生成、Markdown / 代码块 / LaTeX、图片消息（每条最多 4 张）、长按菜单（复制 / 编辑重发 / 重新生成 / 删除）、链接识别与内置浏览器 |
| 已读与沉默 | `messages.readAt` 已读回执；`defer_reply` 允许模型本轮不回，界面只显示「已读」；被睡眠静默时，聊天页在输入框上方说清楚原因 |
| 睡眠 | **默认不睡**（睡眠是可选功能，在人格编辑里打开）；打开后人格自主睡觉、睡前免打扰（由模型决定）、30 分钟窗口内的唤醒阈值（新建/种子人格默认 3 条） |
| 表情包 | 压缩 GIF 表情：导入自动压到 ≤512KB/320px/60 帧，独立表情面板；模型可发送/制作/收藏（`sticker` 工具），服务端模式走媒体上传 |
| 语音与视频 | 按住录音（AAC 16kHz ≤5 分钟）、选视频（≤2 分钟/64MB）；模型可 `listen/watch` 真实听到声音、看到关键帧；不支持时明确报错 |
| 人格 | 结构化字段（性格 / 喜欢的事 / 行为方式 / 成长经历 / 个人设定）+ 行为参数（主动程度、记性、抽取频率、睡眠）、提示词全文编辑、版本快照、人格演化提案、人设卡 |
| 头像 | 人格头像与用户头像；采样压缩后存本地，统一渲染，不进备份 |
| 长期记忆 | 自动抽取、生命周期（ACTIVE / DORMANT / ARCHIVED）、分量衰减、每日整理、`recall` 三档检索、回忆重构 |
| 检索 | 中文二元组倒排索引 + 本地 384 维哈希嵌入余弦重排（`local-hash-v1`，离线、零依赖） |
| 长会话 | 历史按 **200 条一块**存储，首屏只读最新一块、向上/向下各加载一块；更早的内容另压成滚动摘要，原文不删 |
| 主动行为 | 30 秒心跳（先降后升的冲动曲线，三小时封顶）、主动唤醒规则；是否开口由模型决定 |
| 在线状态 | Presence：平静 / 发呆 / 在写东西等，以及「睡着了 · 08:00 醒」 |
| 工具 | `think` / `remember` / `recall` / `set_mood` / `set_quiet_hours` / `web_search` / `web_fetch` / `update_persona` / `defer_reply`；两端均有真实执行器 |
| 模型接入 | 任意 OpenAI 兼容服务：多套配置、Base URL / Key / 模型 / 自定义 Headers、连通性测试、推理参数；Gemini 与 Claude 原生适配已预留 |
| 用量 | 只统计 token（本月总量、按用途、按人排行）；没有金额、额度或拦截 |
| 并发 | 全局 LLM 并发闸 3，后台最多占 2 位，聊天保底 1 位 |
| 备份 | 导出 / 导入（合并 / 替换 / 预览），**头像与聊天图片随备份走**（限额内），两端同一 JSON 契约；API Key 永不进备份 |
| 外观 | 浅色 / 深色 / 跟随系统、主题色、字号、气泡样式、聊天背景、动画与触感开关 |
| 语言 | 中文（默认）与英文，跟随系统语言；没有应用内语言开关（见 [docs/I18N.md](docs/I18N.md)） |

两端并非逐项完全对等；平台限制与 iOS 仍缺的能力以 [docs/IOS-PARITY.md](docs/IOS-PARITY.md) 为准。

## 设计立场

项目的大部分取舍来自同一条约束：**界面面对的是一个联系人，不是一台可调参的机器人。** 记忆开关、回复节奏、每日主动次数、月度额度这类旋钮被刻意移除，相关决定交给人格字段与模型（`defer_reply`、睡眠与唤醒阈值、`proactiveLevel` 等）。这条立场写进了 [docs/design/roadmap-1.9.md](docs/design/roadmap-1.9.md) 的规格与删除清单，并在 [CONTRIBUTING.md](CONTRIBUTING.md) 里作为评审约束；架构层面的取舍见 [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)。

几处容易被当成「缺失功能」的取舍：

- **只有 token 统计**：没有金额、额度与拦截；`costMicroUsd` 只在库里留列，界面不展示。
- **远程决策服务默认关闭**：两端默认在本机算决策（零网络）；需要时可把 `agentd` 跑在自己的机器上，用构建开关/环境变量切过去，失败自动回退本机。
- **发布包不发明文 HTTP**：Release 构建关闭明文，只允许 HTTPS（iOS 额外放行局域网明文）；调试包不受影响。
- **模型写的内容不翻译**：界面文案跟随系统语言，但模型写出的话（心情理由、记忆正文、人格简介）保持它当时写下的语言。

## 架构与技术栈

| 层 | Android | iOS |
| --- | --- | --- |
| 语言与 UI | Kotlin 2.0.21、Jetpack Compose（BOM 2024.12.01）、Material 3 | Swift 5.9、SwiftUI（iOS 16.0+） |
| 依赖注入 / 装配 | Hilt 2.52 | 手写依赖装配（`ios/YetAnotherPal/App`） |
| 持久化 | Room 2.6.1（schema v10，导出 `app/schemas/`）、DataStore | 系统 `SQLite3`（表结构对齐 v10）、`UserDefaults` |
| 后台任务 | WorkManager 2.10、前台服务（`specialUse`）、开机恢复 | `BGAppRefreshTask` / `BGProcessingTask`（系统择机调度） |
| 网络 | OkHttp 4.12（SSE）、kotlinx.serialization 1.7.3 | `URLSession`（SSE）、`Codable` |
| 密钥 | Keystore 加密后写入 DataStore | Keychain（模拟器无 entitlement 时回退到调试兜底） |
| 最低版本 | Android 8.0（`minSdk 26`）、`targetSdk 35`、JDK 17 | iOS 16.0、Xcode 16+ |
| 测试 | JUnit4 + kotlinx-coroutines-test；迁移测试在 `androidTest` | XCTest（`ios/YapKit` 本地 SPM 包，macOS 上直接跑） |
| Agent 决策 | 共享 `:agentcore`（Kotlin/JVM，唯一实现） | 契约对齐的 Swift 实现；可切换远程 `agentd` |

跨端契约（三处必须一致）：

1. **数据库**：iOS 的 `SQLiteStore` 表名与列名逐字对齐 Room 导出的 `10.json`，两端 schema 都是 v10；
2. **备份**：两端 `BackupCodec` 与 `fixtures/backup/` 的 v1 / v2 样本互读，任何一端改格式而另一端没跟就会红；
3. **Agent 核心**：`spec/agent-core/cases/*.json` 是与语言无关的用例，Android 与 iOS 各有一条测试读同一批文件，喂给各自的领域实现（睡眠判定、`defer_reply`、主动上限、心跳、记忆衰减、工具参数夹取）。

决策层只有一份实现：`agentcore/`（`:agentcore`，零第三方依赖）被 `:app` 与 `agentd/` 同时依赖。`agentd/` 在此之上加一层 HTTP（仅 JDK `com.sun.net.httpserver`），暴露 `GET /health` 与四个核心接口（`sleep-decision` / `defer-plan` / `proactive-cap` / `tool-args`）。两端客户端都通过 `AgentCoreClient` 抽象接入：**默认走进程内/本机实现**（零网络），可按构建开关或环境变量切到远程服务，失败自动回退——没有用户可见设置项。

## 目录结构

```
.
├── app/                    Android 应用（Kotlin · Compose · Hilt · Room · WorkManager）
│   ├── schemas/            Room 导出的历史 schema（迁移测试的依据）
│   └── src/main/java/com/yap/app/
│       ├── data/           Room 实体 / DAO / 迁移 / 仓库 / DataStore / Keystore
│       ├── domain/         纯算法：记忆生命周期、心情、心跳、链接识别、向量、备份编解码…
│       ├── network/        OpenAI 兼容 SSE（多模态）+ 并发闸 + 用量
│       ├── service/        前台服务、开机恢复、自主循环控制
│       ├── ui/             components / screens / theme
│       └── util/           时间、LaTeX、媒体压缩与持久化、通知
├── ios/                    iOS 16+ 应用
│   ├── YapKit/             与 UI 无关的 SPM 包（Domain / Data / Net / Backup / Chat / Services），可 swift test
│   ├── YetAnotherPal/      SwiftUI 层（App / Views / Resources 本地化资源）
│   └── YetAnotherPal.xcodeproj  部署目标 16.0，无第三方依赖
├── agentcore/              共享 agent 决策层（纯 Kotlin/JVM，零依赖；:app 与 :agentd 都依赖它）
├── agentd/                 独立 agent 核心服务（Kotlin/JVM，HTTP，基于 :agentcore）
├── spec/agent-core/cases/  跨端 agent 契约用例（JSON，两端测试共读）
├── harness/                零依赖 Node.js 参考服务（OpenAI 兼容 mock，含工具与心跳分支）
├── fixtures/backup/        跨端备份黄金样本（v1 只读样例 + v2 契约）
├── docs/                   架构、对齐、更新记录、版本规则、i18n 说明
└── gradle/                 Gradle Wrapper
```

## 获取源码

```bash
git clone https://github.com/HepingGe2333/YetAnotherPal.git
cd YetAnotherPal
```

仓库：<https://github.com/HepingGe2333/YetAnotherPal>。旧仓库地址会由 GitHub 重定向到新地址。

## 构建与测试

**Android**（JDK 17、Android SDK Platform 35）：

```bash
echo "sdk.dir=$HOME/Library/Android/sdk" > local.properties   # 指向本机 SDK，此文件不进仓库
./gradlew :app:testDebugUnitTest :app:assembleDebug
adb install -r app/build/outputs/apk/debug/app-debug.apk
```

迁移测试（`app/src/androidTest`）需要模拟器或真机：

```bash
./gradlew :app:connectedDebugAndroidTest
```

**iOS**（Xcode 16+，部署目标 iOS 16.0，零第三方依赖）：

```bash
cd ios/YapKit && swift test --disable-sandbox      # 纯逻辑，macOS 上秒级
cd ios && xcodebuild -project YetAnotherPal.xcodeproj -scheme YetAnotherPal \
  -sdk iphonesimulator -destination 'platform=iOS Simulator,name=iPhone 17 Pro' build
```

构建产物：Android 在 `app/build/outputs/apk/debug/app-debug.apk`；iOS 在 `ios/.build/DerivedData/Build/Products/Debug-iphonesimulator/YetAnotherPal.app`。`dist/` 里的历史 APK 与 `docs/screenshots/` 下的截图是本地资料，文件名不随品牌改名重写；`dist/` 不进仓库。

**本地联调参考服务**（无需真实 API Key 即可走通全链路）：

```bash
node harness/server.mjs        # http://127.0.0.1:8787/v1 ，模型 ID 填 yap-reference
```

参考服务认得 `remember` / `recall` / `set_mood` / `web_search` / `yap-wake` / `defer_reply` / 记忆抽取 / 记忆整理 / 历史压缩等分支；`[chat]` 日志会打印 `systemChars` 与本轮使用的工具，便于核对人格与记忆是否真的随 `system` 注入。

## 文档

完整索引见 [docs/README.md](docs/README.md)。最常看的几份：

| 文档 | 内容 |
| --- | --- |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) · [EN](docs/ARCHITECTURE.en.md) | 分层、数据流、跨端契约、agent 核心的三种形态 |
| [docs/I18N.md](docs/I18N.md) · [EN](docs/I18N.en.md) | 双语方案、资源位置、新增文案规则 |
| [docs/CHANGELOG.md](docs/CHANGELOG.md) · [EN](docs/CHANGELOG.en.md) | 每个版本的实际变更 |
| [docs/IOS-PARITY.md](docs/IOS-PARITY.md) | 两端哪些必须一致、哪些受平台限制 |
| [docs/audits/](docs/audits/README.md) | 独立审计记录与已接受的取舍 |
| [docs/design/](docs/design/roadmap-1.9.md) | 历史设计记录（0.9.0 之前的行为规格，供追溯） |
| [CONTRIBUTING.md](CONTRIBUTING.md) · [EN](CONTRIBUTING.en.md) | 环境、代码风格、提交规范、发版流程 |

## 已知限制

- **iOS 后台不完全实时**：`BGAppRefreshTask` / `BGProcessingTask` 由系统择机调度，后台心跳与每日整理可能延后；
  回到前台时按错过的时间补算一次。这是 iOS 平台约束，不是可配置项。
- **检索每翻一页都会重新走一遍历史区块**：这是「没有候选上限、也不使用 offset」的代价——首屏很快，但历史越长、
  翻到越后面的页越慢；峰值内存仍然只有「一块 + 一页」。
- **来回长时间浏览会累积已加载区块**：向上/向下加载的块会留在窗口里（为了让读写区间连续），会话重新打开才回收。
- **区块不做重平衡**：极端删除后可能出现只有几条消息的块，块编号会出现空洞（分页按块表跳过空洞）。
- **备份里的图片有上限**：总量 128 MiB、单张 8 MiB，只带 JPEG / PNG / WebP；超出或格式不支持时**跳过并明确告警**，
  GIF / HEIC / 视频不随备份走。
- **大库检索有性能上限**：无候选上限的代价是「每翻一页重扫历史区块」，10 万条量级的实测数字与结论见
  [docs/performance.md](docs/performance.md)。

## 贡献与许可

提交改动前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)（[English](CONTRIBUTING.en.md)）。最低要求：两端单测通过；涉及数据结构时 schema、迁移、迁移测试与 fixtures 同步改；不提交密钥、`local.properties`、`dist/` 或截图。

License：[Apache-2.0](LICENSE) © 2026 Heping_Ge2333 (hpg2333)。提交贡献即表示同意以同一协议授权。

仓库：[HepingGe2333/YetAnotherPal](https://github.com/HepingGe2333/YetAnotherPal) · 问题：[Issues](https://github.com/HepingGe2333/YetAnotherPal/issues) · 合并请求：[Pull requests](https://github.com/HepingGe2333/YetAnotherPal/pulls)
