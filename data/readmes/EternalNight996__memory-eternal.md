# 🧠 memory-eternal — 给 AI 装「第二大脑」

[![HOL Guard](https://img.shields.io/endpoint?url=https%3A%2F%2Fhol.org%2Fapi%2Fregistry%2Fbadges%2Fplugin%3Fslug%3Deternalnight996%252Fmemory-eternal%26metric%3Dtrust)](https://hol.org/registry/plugins/eternalnight996%2Fmemory-eternal)

<!-- 语言 / Language：本文件是**默认**（简体中文）README；英文镜像见 README.en.md。
     两份是**独立文件**、标题层级一一对应；改一处请同步另一处（新增一节要两边都加）。
     npm / DSH 插件市场默认展示本文件（中文）。 -->

<p align="center"><b>简体中文（默认）</b> · <a href="README.en.md">English</a></p>

<p align="center">
  <img src="https://img.shields.io/badge/DeepSeek%20Harness-plugin-3B82F6" alt="DSH plugin" />
  <img src="https://img.shields.io/npm/v/memory-eternal" alt="npm version" />
  <img src="https://img.shields.io/github/stars/EternalNight996/memory-eternal?style=flat" alt="GitHub stars" />
  <img src="https://img.shields.io/github/license/EternalNight996/memory-eternal" alt="license" />
  <a href="https://dsh.market/"><img src="https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-zh.svg" alt="DSH Market 收录" /></a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/EternalNight996/memory-eternal/main/assets/screen/memory-eternal.gif" width="880" alt="对话自动沉淀 + 图形化知识库 + 知识图谱（演示）" />
</p>

> **对话结束自动沉淀，跨会话不失忆；召回只取相关小块，省 token 少噪音。**
> 全自研、零第三方记忆框架、不改 DSH 源码、一个记忆库所有 Agent 共享，SQLite 持久存储，零外部依赖。

<p align="center"><strong>⭐ 觉得好用就点个 Star</strong>！ <br/><sub>DSH 一条命令：<code>dsh plugin --profile web add memory-eternal</code></sub></p>

<p align="center">
  <img src="https://raw.githubusercontent.com/EternalNight996/memory-eternal/main/assets/screen/memory-popup.png" width="32%" alt="记忆库弹窗：知识卡 / 检索 / 知识图谱" />
  <img src="https://raw.githubusercontent.com/EternalNight996/memory-eternal/main/assets/screen/memory-settings.png" width="32%" alt="DSH 设置 → 记忆：全部配置项" />
  <img src="https://raw.githubusercontent.com/EternalNight996/memory-eternal/main/assets/screen/memory-sidebar.png" width="32%" alt="侧边栏一键入口" />
</p>

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
cd ~/.dsh/profiles/web && pnpm add memory-eternal@0.9.6

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
dsh-memory connec

[...截断...]

t claude       # 写 ~/.claude/settings.json 的 SessionEnd hook → 会话结束自动沉淀
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
dsh-memory serve [--port 7999]       # 前台跑 web
dsh-memory open                      # ensure web 存活 + 开浏览器
dsh-memory watchdog [--port 7799]    # 看门狗保活 web（独立进程）
dsh-memory status [--json]           # 看常驻 watchdog：pid / 端口 / 版本 / 是否存活
                                     # 以及**端口上真正在服务的版本**（锁里的版本号只是 watchdog 自述）
dsh-memory stop [--port 7799]        # 停止常驻 watchdog（配置改动不会自动停；连它拉起的 web 一起停）
                                     # 停完会再问一次端口占用者，仍被占着就明确告警
dsh-memory restart [--port 7799]     # 停止并重起 watchdog（升级后换新版）
                                     # 按端口占用者兜底收掉锁里没登记的旧 web，起完自检端口上服务的版本
dsh-memory audit list [--status pending|rejected|approved|deleted|all] [--limit N] [--json]
                                     # 列出卡片；总数不受 --limit 影响，--limit 只限制显示条数（默认全部）
                                     # all = 审核队列（pending + rejected），不含 approved / deleted
dsh-memory audit approve <卡片路径...>              # 人工批量批准
dsh-memory audit reject <卡片路径...> --reason "..." # 人工批量驳回
```

单独装（不发 DSH）时 `dsh-memory` 命令来自 `npm i -g`。

---

## ⚙️ 服务自管理（白话）

**三个概念**，别搞混：

- **web server 怎么保活**（`autoWebMode`）→ `init`=DSH 启动时拉一次（默认）；`interval`=DSH 进程内定时探活自动拉起（0 额外内存）；`manual`=全手动只从 `dsh-memory open` 起。
- **看门狗进程**（`watchdogAutoSpawn`，默认开）→ 一个**独立** node 进程，DSH 退出了它也能拉起 web（约 +47 MB 内存）。只在要 7×24 保活时开。
- **版本漂移自愈**（`autoRestartOnDrift`，默认开）→ 常驻 web **比 DSH 活得久**：升级只换磁盘文件，端口上那个进程仍跑着启动时加载的旧代码（「启动 dsh 后运行中还是旧版本」就是这么来的）。开着它，DSH 激活时会**问端口上真正服务的版本**，与磁盘不一致就用新代码重启常驻实例；关掉则只告警，需要时在「插件信息」点**重启常驻实例**。
- **自动挂载 MCP**（`autoMcpSetup`，默认关）→ 是否自动把 MCP 写进 Claude Code/Codex/Cursor 配置。关 = 不碰你本机配置文件，需要时手动 `dsh-memory setup`。

**改这些**：记忆库左栏「记忆配置」（或 DSH 设置 → 记忆）→ 表格里改，点「保存配置」；`autoWebMode`/`watchdogAutoSpawn` 需重启 DSH 生效。

> ⚠️ **同端口不会因配置改动而自动替换（#19）**：看门狗是**独立进程且故意不杀**（多会话共用一个），所以
> 关闭 `watchdogAutoSpawn` **不会**停掉已经在跑的那个，改 `webCheckIntervalMs`/`webMaxRestart` 也不会生效。
> 要停止 / 换新版请显式执行 `dsh-memory stop [--port N]` 与 `dsh-memory restart [--port N]`（`stop` 会**连它拉起的 web 一起停**，不留占端口的孤儿）；
> `dsh-memory status` 会显示常驻实例的 pid、端口、启动时间与**版本是否落后于本机安装的包**，并单独报出**端口上真正服务的版本**
> （锁文件里的版本号只是 wa