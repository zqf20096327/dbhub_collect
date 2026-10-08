# workbuddy-account-migrate

> WorkBuddy 数据搬家工具：**跨设备迁移**（家用电脑 ⇄ 办公电脑，两个账号也能把项目会话打包带走）+ **账号切换恢复**（切账号后对话记录、记忆、连接器一键找回）。
>
> Move your WorkBuddy data: **carry project sessions across computers** (home ⇄ office, two accounts) + **recover everything after switching accounts** (conversations, memory, connectors).

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform: macOS | Windows | Linux](https://img.shields.io/badge/Platform-macOS%20%7C%20Windows%20%7C%20Linux-blue.svg)](https://github.com/xiaoliuzhuan666/workbuddy-account-migrate)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)
[![Version 1.7.0](https://img.shields.io/badge/Version-1.7.0-brightgreen.svg)](https://github.com/xiaoliuzhuan666/workbuddy-account-migrate)

**[English](#english) | [中文](#chinese)**

---

<h2 id="chinese">中文</h2>

### ⭐ 核心功能

| | 功能 | 解决什么场景 |
|:--|:---|:---|
| ⭐ | **跨设备项目迁移**<br>`migrate_project.py`（v1.7 新增） | **家用电脑和办公电脑各一个账号，两地交替做同一个项目**——项目会话打包成单个文件带走，向导模式输序号 + 拖文件，三步完成 |
| 🔄 | **整账号迁移**<br>`migrate.py` | 切换账号 / 重新登录后，对话记录、长期记忆、MCP 连接器全部"消失"——一键合并恢复可见 |
| 💬 | **单对话跨版本迁移**<br>`migrate_session.py` | 只想把某一个对话从国内版搬到国际版（或反向），不动其他数据 |

**三个脚本都支持无参数运行进交互向导，全程不需要知道 user_id。**

跨设备迁移三步走（这是本工具的招牌场景）：

```
电脑A（账号A）                                电脑B（账号B）
┌─────────────────────┐                  ┌─────────────────────┐
│ 项目A · 77 个会话    │  ① 导出（选1）   │                     │
│ 正文/工具结果/任务/  │ ────────────────→│  包出现在桌面        │
│ 工作区记忆           │  包自动放桌面     │  ③ 导入（选2）       │
└─────────────────────┘                  │  选包 → 拖入项目路径  │
        │                                └─────────────────────┘
        │ ② 传输：AirDrop / U盘 / scp / 网盘           │
        └─────────────────────────────────────────────→
                                           自动改写账号 + 项目路径
                                           会话全部归来 ✅
```

- 🔁 **同一个包反复导入不出双份**——"两地交替工作"来回带的底气
- 🧳 工作区记忆（`{项目}/.workbuddy/`）一起带走
- 💻 macOS ⇄ Windows 路径风格自动重映射（盘符、分隔符、中文路径）
- 🛡️ 导入前自动备份，`--rollback` 一键还原

### 你是不是遇到了这个问题？

WorkBuddy 切换账号 / 重新登录 / 换了腾讯云身份后，**之前的对话记录全没了**？长期记忆、MCP 连接器配置也看不到了？

**数据其实没丢**——它们还在磁盘上，只是 WorkBuddy 用 `user_id` 做了账号隔离，新账号的 UI 看不到旧账号的数据。

本工具一键把旧账号的数据合并到当前登录账号，**对话记录、记忆、连接器全部恢复可见**。

```
切换账号前：                       切换账号后：
┌──────────────────┐              ┌──────────────────┐
│  账号 A           │              │  账号 B           │
│  26 个对话 ✅     │    ──→      │  26 个对话 ❌     │ ← UI 看不到了
│  13KB 记忆 ✅     │              │  13KB 记忆 ❌     │ ← 文件还在磁盘上
│  17 个 MCP ✅     │              │  17 个 MCP ❌     │
└──────────────────┘              └──────────────────┘
                                         │
                                    运行迁移脚本
                                         │
                                         ▼
                                  ┌──────────────────┐
                                  │  账号 B           │
                                  │  26 个对话 ✅     │ ← 合并到当前账号
                                  │  13KB 记忆 ✅     │ ← 追加去重
                                  │  17 个 MCP ✅     │ ← 深度合并
                                  └──────────────────┘
```

### 功能特性

| 特性 | 说明 |
|:---|:---|
| ✅ 交互式向导 | 运行即用，列出所有账号，手动选择目标/源账号，无需知道 user_id |
| ✅ 跨平台路径适配 | v1.4：storage.json 路径自动适配 macOS / Windows / Linux |
| ✅ 国内版 / 国际版 | 交互式向导可选版本，或 `--intl` 参数指定国际版（`~/.workbuddy-ai`） |
| ✅ Session 对话记录迁移 | 修改 SQLite 数据库中的 `user_id` 字段，对话记录全部回归 |
| ✅ Memory 长期记忆合并 | 追加式去重合并，不会丢失当前账号已有记忆 |
| ✅ Connector MCP 连接器合并 | JSON 深度合并，目标账号已有配置保留不动 |
| ✅ 自动备份 + 回滚 | 迁移前自动备份数据库、记忆、连接器，支持一键回滚 |
| ✅ WAL 安全处理 | 迁移前后执行 SQLite checkpoint，确保数据持久化 |
| ✅ 登录态权威识别 | v1.6.3：以 `account-snapshot.json` 的 `primary.uid`（客户端真实登录态，**左侧面板按它过滤**）为权威，`storage.json` 降为兜底；两来源不一致时强烈提示显式传 `--target` |
| ✅ 迁移结果验证 | v1.3：UPDATE 后验证源 user_id 归零，确认迁移成功 |
| ✅ 云端通道映射重置 | v1.6.3：清掉旧账号的 `edge-sync` 映射行，对话按新账号通道重新上传（回滚自动还原）；`--keep-cloud-mapping` 可关闭 |
| 🧰 强制重登辅助脚本 | `scripts/force-relogin.sh`：客户端反复自动登录到错账号时逼它弹登录界面（附带实测局限说明） |


[...截断...]

| ✅ 零依赖 | 仅需 Python 3.8+，无第三方包 |

### 快速开始

```bash
git clone https://github.com/xiaoliuzhuan666/workbuddy-account-migrate.git
cd workbuddy-account-migrate
python3 scripts/migrate.py
```

> 受限 shell / 沙箱环境里 `git clone` 可能报「目标路径已存在」，改用 tarball：
> ```bash
> mkdir -p workbuddy-account-migrate && cd workbuddy-account-migrate
> curl -sSL https://codeload.github.com/xiaoliuzhuan666/workbuddy-account-migrate/tar.gz/refs/heads/main \
>   | tar xz --strip-components=1
> ```

运行效果：

```
======================================================================
WorkBuddy 版本选择
======================================================================

  1. 国内版（数据目录 ~/.workbuddy）
  2. 国际版（数据目录 ~/.workbuddy-ai）

请选择 WorkBuddy 版本（输入序号，默认 1）:
```

选择版本后进入账号选择：

```
======================================================================
WorkBuddy 账号迁移向导
======================================================================

请选择迁移方向：先选【目标账号】（接收数据），再选【源账号】（被迁移）

  序号   user_id                                  Sessions     Memory   Connectors
  ------------------------------------------------------------------------
  1      abc12345-6789-...                              18     13.0KB  17mcp/6conn
  2      def67890-1234-...                               7      5.1KB  17mcp/4conn

请选择【目标账号】（接收数据的账号，输入序号）: 1
```

输入序号即可，全程不需要知道 user_id。

**其他模式：**

```bash
# 仅诊断 — 查看所有账号数据分布
python3 scripts/migrate.py --diagnose

# 指定源账号迁移（高级用户）
python3 scripts/migrate.py --source <USER_ID>

# 显式指定目标账号（不依赖当前登录态推断，v1.4 新增）
python3 scripts/migrate.py --source <USER_ID> --target <USER_ID>

# 国际版（数据目录 ~/.workbuddy-ai）
python3 scripts/migrate.py --intl
python3 scripts/migrate.py --intl --diagnose
python3 scripts/migrate.py --intl --source <USER_ID>

# 显式指定数据目录（优先级高于 --intl）
python3 scripts/migrate.py --dir ~/.workbuddy-ai

# 进程检测"查不出来"时按「客户端已关闭」谨慎继续
#   与 --force 的区别：真检测到客户端仍在运行时，它照样拦截
python3 scripts/migrate.py --assume-clients-closed

# 回滚到指定备份
python3 scripts/migrate.py --rollback <TAG>

# 迁移完成后自动重启 WorkBuddy 客户端（macOS），会话列表立即刷新
python3 scripts/migrate.py --source <USER_ID> --yes --restart
```

> **国内版 vs 国际版**：目录结构完全一致，区别在于**数据目录位置**与**登录态来源**：
>
> | | 国内版 | 国际版 |
> |:---|:---|:---|
> | 数据目录 | `~/.workbuddy/` | `~/.workbuddy-ai/` |
> | 登录态权威来源 | 目录内 `storage/skeleton/account-snapshot.json` → `primary.uid`（平台 `storage.json` → `genie.userId` 仅兜底） | 目录内 `storage/skeleton/account-snapshot.json` → `primary.uid`（**不读**平台 `storage.json`） |
>
> 因此同一台机器上装了两个版本时，脚本会按**数据目录**决定读哪份登录态：
> 指向国际版目录时不会去读国内版的 `storage.json`（否则会把国际版数据迁到一个国际版里不存在的账号下）。
> **目录优先级**：`--dir` > `--intl` > 自动探测（`~/.workbuddy-ai` 存在且非空时判为国际版，否则国内版）。交互式向导还会让你确认一次版本。

### 备份目录布局

> ⚠️ v1.6 起**单对话迁移**的备份挪到了 `migrate_backups/session/` 子目录，
> 与 `scripts/migrate.py` 的整账号备份（直接放 `migrate_backups/` 根下）分开——
> 两者的 `meta.json` 格式不同，混在一个目录里会让 `--backups` 列出、
> `--rollback` 撞上 `KeyError`。
>
> | 路径 | 内容 | 回滚命令 |
> |:---|:---|:---|
> | `~/.workbuddy/migrate_backups/<TAG>/` | 整账号备份 | `scripts/migrate.py --rollback <TAG>` |
> | `~/.workbuddy/migrate_backups/session/<TAG>/` | 单对话备份 | `scripts/migrate_session.py --rollback <TAG>` |
>
> **旧位置的单对话备份仍然能被 `--backups` / `--rollback` 找到**（两个目录都会扫），
> 但如果外部脚本里硬编码了备份路径，请注意这次布局变化。
>
> `--backup-dir`（**只有 `migrate_session.py` 有这个参数**，`migrate.py` 没有）
> 的语义是「**额外**加入一个搜索根」而不是「限定只搜它」：
> 新建的备份写进 `<指定目录>/session/`（同样套一层命名空间，避免你把自定义目录
> 指向 `migrate_backups` 时和整账号备份挤在一起），查找 / 回滚时仍会回退扫描
> 上面两个标准目录——命中的备份不在你指定的目录里时，脚本会显式告警，
> 避免误滚了不相干的旧备份。

### 退出码

下表三个脚本共用，但 **`3` 只有 `migrate.py` 会产生**（整账号迁移才有"源账号空"这个概念；
另两个脚本遇到源/目标版本目录没数据时是 `1`）。

| 退出码 | 含义 |
|:---:|:---|
| `0` | 确实迁移 / 回滚了东西 |
| `1` | 出错（含：`migrate_session.py` 的源/目标版本目录里根本没有库 = 版本选错） |
| `2` | 「客户端必须关闭」检测拦截（检测到客户端仍在运行，或检测不可信且未给 `--force` / `--assume-clients-closed`） |
| `3` | **仅 `migrate.py`**：无数据可迁，本次未做任何改动。涵盖两种情况——源账号确实没有 session / memory / connector；或源有数据但与目标完全一致、合并后没有任何新增内容 |

> ⚠️ 自动化脚本不要把「退出码 0」当成「一定迁了东西」，也不要把「3」当成失败：
> 它表示本次没有产生任何改动。判读建议：`0` → 成功，`3` → 跳过，其他 → 失败。
>
> ⚠️ **破坏性变更**：v1.6.1 之前，源账号没数据时 `migrate.py` 返回 `0`。
> 如果你在 CI / 自动化里按 `rc