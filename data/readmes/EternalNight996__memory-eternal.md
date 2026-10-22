# 🧠 memory-eternal — 给 AI 装「第二大脑」

[![HOL Guard](https://img.shields.io/endpoint?url=https%3A%2F%2Fhol.org%2Fapi%2Fregistry%2Fbadges%2Fplugin%3Fslug%3Deternalnight996%252Fmemory-eternal%26metric%3Dtrust)](https://hol.org/registry/plugins/eternalnight996%2Fmemory-eternal)

<!-- 语言 / Language：本文件是**默认**（简体中文）README；英文镜像见 README.en.md。
     两份是**独立文件**、标题层级一一对应；改一处请同步另一处（新增一节要两边都加）。
     npm / DSH 插件市场默认展示本文件（中文）。 -->

<p align="center">
  <img src="https://raw.githubusercontent.com/EternalNight996/memory-eternal/main/assets/icon.png" width="84" alt="memory-eternal" />
</p>

<p align="center">
  <b style="font-size:20px">Memory Atlas · 本地优先的 AI 记忆库</b><br/>
  <sub>自动沉淀 · 先审后入 · 知识星图 · 全 Agent 共享</sub>
</p>

<p align="center"><b>简体中文（默认）</b> · <a href="README.en.md">English</a></p>

<p align="center">
  <img src="https://img.shields.io/badge/DeepSeek%20Harness-plugin-3B82F6" alt="DSH plugin" />
  <img src="https://img.shields.io/npm/v/memory-eternal" alt="npm version" />
  <img src="https://img.shields.io/badge/release-v0.12.0-FF7A45" alt="v0.12.0" />
  <a href="https://eternalnight996.github.io/memory-eternal/"><img src="https://img.shields.io/badge/Live%20Demo-online-FF7A45" alt="Live demo" /></a>
  <img src="https://img.shields.io/github/stars/EternalNight996/memory-eternal?style=flat" alt="GitHub stars" />
  <img src="https://img.shields.io/github/license/EternalNight996/memory-eternal" alt="license" />
</p>

<p align="center">
  <a href="https://eternalnight996.github.io/memory-eternal/demo/"><img src="https://raw.githubusercontent.com/EternalNight996/memory-eternal/main/assets/screen/library.png" width="920" alt="Memory Atlas：记忆库、今日回看、知识卡与连接星图" /></a>
</p>
<p align="center"><sub>▲ Memory Atlas · 在线 Demo（示例数据）· <a href="https://eternalnight996.github.io/memory-eternal/demo/">点此打开</a></sub></p>

> **对话结束自动沉淀成知识卡，跨会话不失忆；召回只取相关小块，省 token 少噪音。**
> 全自研、零第三方记忆框架、不改 DSH 源码；一个记忆库所有 Agent 共享，SQLite 持久存储，零外部依赖。

<p align="center"><strong>⭐ 如果它帮你少解释了一遍上下文，点个 Star 就是最大的支持</strong><br/><sub>DSH 一条命令：<code>dsh plugin --profile desktop add memory-eternal</code></sub></p>

<p align="center"><a href="https://eternalnight996.github.io/memory-eternal/"><b>🌐 在线体验</b></a> · <a href="https://eternalnight996.github.io/memory-eternal/demo/"><b>打开记忆库 Demo</b></a> <sub>（示例数据，不用安装）</sub></p>

<p align="center">
  <img src="https://raw.githubusercontent.com/EternalNight996/memory-eternal/main/assets/screen/audit.png" width="32%" alt="待审：顶部类型条 + 队列 + 右侧判词栏" />
  <img src="https://raw.githubusercontent.com/EternalNight996/memory-eternal/main/assets/screen/graph.png" width="32%" alt="知识星图：按类型着色、连接簇图例、跨库聚合" />
  <img src="https://raw.githubusercontent.com/EternalNight996/memory-eternal/main/assets/screen/reader.png" width="32%" alt="读卡器：正文 + 右侧目录、标签与相关记忆" />
</p>

<p align="center"><sub>▲ 真实运行截图：待审判词 · 知识星图 · 读卡器</sub></p>

---

## 🧩 支持平台

| 平台 / 宿主 | Memory Atlas UI | 待审 / 批驳 | 知识星图 | 入口与状态 |
|---|---|---|---|---|
| **DSH 桌面版 / Web** | 完整内嵌 | ✅ | ✅ | 左栏「记忆」，已支持 |
| **Orca** | 侧栏启动器 | Web 内完成 | Web 内完成 | 右栏「记忆」，[本版新增](orca-plugin/README.md) |
| **dsh-tui** | 浏览器打开 | Web 内完成 | Web 内完成 | `/memory`，[本版新增](dsh-tui-plugin/README.md) |
| **Codex** | 浏览器打开 | Web 内完成 | Web 内完成 | [`memory-open` skill](skills/memory-open/SKILL.md)，本版新增 |
| **Claude Code** | 浏览器打开 / Pane | Web 内完成 | Web 内完成 | `/memory-eternal:memory-open`，本版新增 |
| **Cursor** | Webview 内嵌 | ✅ | ✅ | [扩展 Webview](cursor-extension/README.md)，本版新增 |
| **纯 Web** | 主实现 | ✅ | ✅ | `http://127.0.0.1:7999/` |

> 原则：**一套 Web UI 作为唯一真源**；能内嵌的宿主用 Webview，不能内嵌的宿主只做轻量启动器，不复制第二套 UI。所有入口打开同一版本，避免 DSH / Web 版本漂移。

---

## ✨ 它到底解决什么问题

| 你遇到的 | 以前的做法 | 用了之后 |
| --- | --- | --- |
| 聊了 3 天的项目，新会话全忘 | 手动翻历史 / 重新解释一遍 | 每轮结束自动沉淀成卡，开工前 `memory_recall` 一句就回来 |
| 记忆塞进 prompt，token 爆掉 | 全量粘贴、越聊越贵 | 只召回相关的一小块（可配上限），省 token 也少噪音 |
| AI 写的东西不敢直接信 | 无法追溯、无法回滚 | 卡片带来源 / 时间 / 状态，先审后入，删除进回收站 |

- **看得见**：知识卡 / 图谱 / 健康概览 / 沉淀日志，四层可视化；
- **控得住**：审核模式（全部人工 / 仅高风险）、去重与矛盾扫描、批量合并、每日备份与一键恢复；
- **带得走**：知识库是本地 Markdown + SQLite，可 git 管理、可导出，不锁在插

[...截断...]

件里。

---

## 🚀 五分钟上手

### 🟦 DeepSeek Harness（DSH）—— 重点

**装**（官方桌面版走插件市场，`dsh web` 用一条 CLI）：

```bash
# ① 官方 DeepSeek Harness 桌面版（推荐）：设置 → 插件 → 搜 memory-eternal 安装
#    等价 CLI（该壳的 profile 名就是 desktop）：
dsh plugin --profile desktop add memory-eternal

# ② dsh web（浏览器端）：
dsh plugin --profile web add memory-eternal

# 或在 profile（pnpm workspace）里直接更新。注意用 pnpm，npm install 会报 EUNSUPPORTEDPROTOCOL
cd ~/.dsh/profiles/web && pnpm add memory-eternal@latest

# 刚发新版时 @latest 可能被 pnpm 的最小发布年龄门槛/元数据缓存挡住（静默停在旧版）：
# 直接指定版本号最快，pnpm 会自动把它加进 workspace 的 minimumReleaseAgeExclude
cd ~/.dsh/profiles/web && pnpm add memory-eternal@0.12.0

# 验版本（应等于上面装的号），然后重启对应宿主生效
node -e "console.log(require('memory-eternal/package.json').version)"
```

#### 🖥️ 桌面版支持策略（先看这条）

- **优先、且只保证支持官方 DeepSeek Harness 桌面版**（官方 Electron 发行版，profile 名 `desktop`）。v0.9.4 → v0.9.6 三轮修复全部围绕它：0.1.7 设置服务换血、`schemastery 3.18.4` 的 volatile 活引用、以及窗口标题栏避让（`data-windows-titlebar`，避免全屏浮层压住最小化/最大化/关闭）。
- **作者自研的 `dsh-desktop`（`dsh-desktop-shell` / `dsh-ui-*` / `dsh-plugin-marketplace` 那一套）已停止维护**，不再作为支持目标 —— 官方桌面版已覆盖同样能力，继续维护两条壳只会分裂兼容性。注意它的 profile 依赖里还钉着已从 npm 撤下的 `dsh-desktop-shell@0.3.0`，会让 `pnpm install` 直接失败；**建议迁到官方桌面版，并从 profile 里删掉这套依赖**。
- 兼容矩阵（均已实测）：官方桌面版 `desktop` profile（schemastery **3.18.4**）＋ `dsh web` 的 `web` profile（schemastery **3.18.1**），两条路径共用同一份代码。

**重启宿主**后，三样东西立即生效：

| 效果 | 在哪看 |
|---|---|
| 自动沉淀知识卡 | 每轮对话结束自动发生，无需操作 |
| `memory_recall` 工具 | Agent 需要历史时自动调用 |
| 图形化界面 | 侧边栏底部「记忆」按钮 / 设置 → 记忆 |

**入口**：侧边栏底部「记忆」按钮 → 记忆库（左栏含 知识卡 / 知识图谱 / 用量 / **审核中心** / 回收中心 / **记忆配置**）；「DSH 设置 → 记忆」= 纯配置页。

**界面语言**：全套 UI 中英双语，跟随 **DSH 设置 → 语言** 实时切换（含知识卡 / 知识图谱 / 审核中心 / 新建卡模板）；浏览器直接访问 web 时跟随浏览器语言。

**改配置**：记忆库左栏「记忆配置」（或 DSH 设置 → 记忆）→ DSH 记忆配置 / 成本控制 / 自动审核配置 / 服务自管理，点「保存配置」即写入。`autoWebMode`/`watchdogAutoSpawn` 的改动需重启 DSH 生效；注意**已常驻的 watchdog 不会被配置改动自动停掉**，要停止或换新版请执行 `dsh-memory stop` / `dsh-memory restart`（见「服务自管理」）。

### 🟨 Claude Code

```bash
npm i -g memory-eternal     # 装 CLI + MCP（写 ~/.claude.json mcpServers.memory）
dsh-memory connect claude       # 写 ~/.claude/settings.json 的 SessionEnd hook → 会话结束自动沉淀
```

装完即用：会话里说「recall 一下数据库选型」→ 自动检索记忆；会话结束 → 自动沉淀进统一 `~/.dsh/memory-vault`（新卡 `pending` 待审核）。

### 🟧 Codex CLI / Cursor

```bash
npm i -g memory-eternal     # 装完自动写 Codex config.toml / Cursor mcp.json 的 mcpServers.memory
dsh-memory connect codex        # 写用户级 ~/.codex/hooks.json 的 Stop hook → 会话结束自动沉淀（含 Codex Desktop）
dsh-memory connect cursor       # 写 ~/.cursor/hooks.json 的 stop/sessionEnd hook → 自动沉淀
```

重启工具 → MCP 已在列表，会话里直接：`用 memory_recall 查一下项目历史决策`；会话结束自动沉淀进统一 `~/.dsh/memory-vault`（新卡 `pending` 待审核）。

> **三种 agent 同一套库**：全部写入 `~/.dsh/memory-vault`，每卡 `submittedBy` 区分作者（DeepSeek Harness / claude-code / codex / cursor），主库只显已审核、审核中心管新卡。

> **原生插件（可选，平台 Marketplace）**：仓库含 `.claude-plugin` / `.codex-plugin` / `.cursor-plugin` 清单，可 `claude /plugin marketplace add EternalNight996/memory-eternal` + `/plugin install`、`codex plugin marketplace add EternalNight996/memory-eternal` + `codex plugin add`、Cursor Settings→Plugins。`connect` 走用户级 hooks.json（更稳，不依赖 Marketplace 审核；Codex Desktop 也走这条）。

> **只保留本插件（卸载其它记忆插件，如 agentmemory）**：`dsh-memory` 只写自己的键（`mcpServers.memory` / 含 `capture.mjs` 的 hooks），不依赖、也不冲突任何其它记忆插件。卸载其它插件需在其自身配置层删除对应条目（如 Codex 的 `[marketplaces.*]` 与 `hooks.state.*`、其 `hooks.json` 事件、`~/.agentmemory` 数据目录）。



### 🟩 浏览器（不依赖任何 Agent）

```bash
dsh-memory open    # 起 web + 开浏览器（默认 http://127.0.0.1:7999）
```

统计 / 搜索 / 知识卡（增删改合并导入导出）/ 知识图谱，全在此。与 DSH 内嵌页同一份 UI，数据同步。

> **zcode（智谱）**：暂无原生 MCP，经社区 [zcode-open-bridge](https://github.com/tizerluo/zcode-open-bridge) 转 MCP 或用 CLI。

---

## 📖 命令速查

```bash
dsh-memory recall "数据库选型"       # 检索
dsh-memory capture "重要结论..."     # 手动沉淀（- 读 stdin）
dsh-memory sweep ~/.claude/projects  # 挖掘已有会话记录
dsh-memory setup [--dry-run]         # 重跑/预览自动挂载（幂等）
dsh-memory connect <claude|codex|cursor>  # 写会话结束自动沉淀 hook（用户级 hooks.json，含 Codex Desktop）
dsh-memory mcp                       # MCP stdio（挂任意 MCP 客户端）
dsh-memory serve [--port 7999]       