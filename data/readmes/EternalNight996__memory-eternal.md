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
  <img src="https://img.shields.io/badge/release-v0.15.0-FF7A45" alt="v0.15.0" />
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

<p align="center">
  <img src="https://raw.githubusercontent.com/EternalNight996/memory-eternal/main/assets/screen/terminal.png" width="49%" alt="Web 内「终端版」：复制命令，进入完整 TUI 或 dsh-tui 原生 /audit" />
  <img src="https://raw.githubusercontent.com/EternalNight996/memory-eternal/main/assets/screen/tui-audit.png" width="49%" alt="终端原生待审：全选、批量批准/驳回、判词双栏" />
</p>
<p align="center">
  <img src="https://raw.githubusercontent.com/EternalNight996/memory-eternal/main/assets/screen/tui-reader.png" width="72%" alt="终端原生长文读卡器：目录、正文、相关记忆与滚动" />
</p>
<p align="center"><sub>▲ v0.14 新增：Web 内终端引导 · 终端原生审核（全选/批驳）· 长文读卡器</sub></p>

---

## 🧩 支持平台

| 平台 / 宿主 | Memory Atlas UI | 待审 / 批驳 | 知识星图 | 入口与状态 |
|---|---|---|---|---|
| **DSH 桌面版 / Web** | 完整内嵌 | ✅ | ✅ | 左栏「记忆」，已支持 |
| **任意终端（TUI）** | 终端原生 | ✅ 全选 / 批量批驳 | 连接簇 / 邻接表 | [`dsh-memory tui`](#-终端版tui)，免绝对路径 |
| **Orca** | 侧栏启动器 | Web 内完成 | Web 内完成 | 右栏「记忆」，[本版新增](orca-plugin/README.md) |
| **dsh-tui** | 原生 `/audit` + 完整 TUI | 原生场景 | 原生场景 | [本版新增](dsh-tui-plugin/README.md) |
| **Codex** | 浏览器打开 | Web 内完成 | Web 内完成 | [`memory-open` skill](skills/memory-open/SKILL.md)，本版新增 |
| **Claude Code** | 浏览器打开 / Pane | Web 内完成

[...截断...]

 | Web 内完成 | `/memory-eternal:memory-open`，本版新增 |
| **Cursor** | Webview 内嵌 | ✅ | ✅ | [扩展 Webview](cursor-extension/README.md)，本版新增 |
| **纯 Web** | 主实现 | ✅ | ✅ | `http://127.0.0.1:7999/` |

> 原则：**一套 Web UI 作为唯一真源**；能内嵌的宿主用 Webview，不能内嵌的宿主只做轻量启动器，不复制第二套 UI。所有入口打开同一版本，避免 DSH / Web 版本漂移。

---

## 🖥️ 终端版（TUI）

Web 不是唯一入口。终端版是同一套记忆库的**原生 TUI**，适合快速批卡、全选、长文阅读和低干扰工作流。

### 任意用户，一条命令

不需要克隆仓库、不需要 `cd`、不需要填写本机绝对路径：

```bash
npx -y -p memory-eternal dsh-memory tui
```

已经安装 `memory-eternal` 的机器：

```bash
dsh-memory tui          # 默认实时：记忆库/待审/星图/状态/回收站
dsh-memory tui --write  # 写入：允许真实批准/驳回
dsh-memory tui --demo   # 示例数据（无 API 时也可看效果）
```

`dsh-memory` 不在 PATH 时，直接用上面的 `npx` 命令；它会临时下载并运行当前 npm 版本。

> `tui` 子命令从 **0.14.1** 开始提供。旧版 `dsh-memory` 会显示帮助；升级：`npm i -g --force memory-eternal@0.15.0`。

### 终端版包含

| 页面 | 能力 |
|---|---|
| 记忆库 | 搜索、类型筛选、今日回看、读卡 |
| 待审 | 全选 / 反选、批量批准、批量驳回、判词 |
| 知识星图 | 连接簇、邻接表、相关卡片 |
| 运行状态 | 知识库、备份、版本、沉淀日志 |
| 回收站 | 恢复、彻底删除 |
| 设置 | 自动沉淀、失败提醒、审核、回收站保留、主题 |
| 读卡器 | 长文换行、目录、相关记忆、滚动 |

### 终端键位

| 键 | 作用 |
|---|---|
| `1–6` | 切换主页面 |
| `Tab` | 循环页面 |
| `↑↓` / `j k` | 移动 |
| `←→` / `t` | 切换类型 |
| `Space` | 多选 / 切换设置 |
| `s` / `Ctrl+A` | 全选 / 反选 |
| `a` | 批准当前或批量 |
| `r` | 驳回当前或批量；回收站里是恢复 |
| `d` | 回收站彻底删除 |
| `Enter` | 读卡 / 切换设置 |
| `L` | 直接打开长文读卡器 |
| `j k` / `PgUp` `PgDn` / `g G` | 读卡器滚动 / 翻页 / 首尾 |
| `/` | 搜索 |
| `Esc` | 返回 / 清空 |
| `?` | 帮助 |
| `q` | 退出 |

### 为什么 Web 不直接嵌 TUI

终端 TUI 依赖 alternate screen、原始键盘事件和字符网格，无法用 iframe 忠实嵌入。  
所以 Web 的「终端版」页面提供可复制命令和预览，真正运行时进入终端；dsh-tui 里则使用原生 `/audit` 场景。

### 限制

- 终端不渲染图片 / 二维码 / Canvas 星图；星图使用连接簇和邻接表。
- 长文、颜色和边框依赖终端字体；Windows 建议 Windows Terminal / VS Code 集成终端。
- 默认只读；真实批驳必须显式加 `--write`；示例数据用 `--demo`。

---

## ✨ 它到底解决什么问题

| 你遇到的 | 以前的做法 | 用了之后 |
| --- | --- | --- |
| 聊了 3 天的项目，新会话全忘 | 手动翻历史 / 重新解释一遍 | 每轮结束自动沉淀成卡，开工前 `memory_recall` 一句就回来 |
| 记忆塞进 prompt，token 爆掉 | 全量粘贴、越聊越贵 | 只召回相关的一小块（可配上限），省 token 也少噪音 |
| AI 写的东西不敢直接信 | 无法追溯、无法回滚 | 卡片带来源 / 时间 / 状态，先审后入，删除进回收站 |

- **看得见**：知识卡 / 图谱 / 健康概览 / 沉淀日志，四层可视化；
- **控得住**：审核模式（全部人工 / 仅高风险）、去重与矛盾扫描、批量合并、每日备份与一键恢复；
- **带得走**：知识库是本地 Markdown + SQLite，可 git 管理、可导出，不锁在插件里。

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
cd ~/.dsh/profiles/web && pnpm add memory-eternal@0.15.0

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

#