# 阻止 Codex 毁了你的电脑 🛑💾

> Codex（ChatGPT 桌面版）会在后台以每分钟数十次的频率向 `~/.codex/logs_2.sqlite` 写入 TRACE/DEBUG/INFO 日志，持续消耗 SSD 写入寿命（TBW）。极端情况下 **21 天可产生约 37TB 写入量**。这个 skill 用一条 SQLite trigger 从源头掐断所有日志写入，让 WAL 归零、写入量为零。

## 背景

### 问题是怎样的

Codex 桌面版在运行期间，会通过 Rust 的 tracing 机制不断向 `~/.codex/logs_2.sqlite`（SQLite 数据库）写入日志：

- **日志级别**：DEBUG、INFO、TRACE、WARN、ERROR
- **写入频率**：平均每分钟 53 次写入（约 3,200 次/小时、77,000 次/天）
- **TRACE 日志**：占约 15%，对普通用户毫无价值，纯粹是调试级别的内容
- **自动清理**：Codex 会定期删除旧日志（只保留最近 ~11 天），但这意味着 99.3% 的写入是"写了就删"——纯粹的 SSD 寿命浪费

### 为什么伤 SSD

SQLite 的写入放大效应使实际磁盘写入远大于日志数据本身：

| 因素 | 说明 |
|------|------|
| 数据页写入 | 每条记录写入 4KB 数据页 |
| 索引更新 | logs 表有 4 个索引，每次 INSERT 都要更新 |
| WAL 日志 | Write-Ahead Log 先写 WAL，再 checkpoint 回主库 |
| checkpoint 重写 | WAL 合并回主库时产生二次写入 |
| 删除 + 碎片 | 删除旧记录产生 freelist 碎片，VACUUM 重写整个文件 |

实测数据显示，72 天累计 555 万次写入，实际 SSD 磁盘写入量估算在 **11~19 GB** 之间。极端高负载场景（如网络断连导致频繁重连重试）下可达 **21 天 37TB**。

### 解决方案

在 `logs_2.sqlite` 上安装一个 SQLite **BEFORE INSERT trigger**：

```sql
CREATE TRIGGER block_all_log_inserts
BEFORE INSERT ON logs
FOR EACH ROW
BEGIN
    SELECT RAISE(IGNORE);
END;
```

当 Codex 尝试 INSERT 日志时，trigger 执行 `RAISE(IGNORE)`，静默丢弃这条 INSERT——**不写数据页、不写 WAL、不写索引**，从源头消除写入。

配合 **launchd 守护进程**，每 5 分钟自检 trigger 是否存在，防止 Codex 升级/重启后 trigger 丢失。

## 安装

### 前提条件

- macOS（已安装 Codex / ChatGPT 桌面版）
- `~/.codex/logs_2.sqlite` 文件存在（即 Codex 已运行过至少一次）

### 方式一：手动安装（推荐）

```bash
# 1. 克隆仓库
git clone https://github.com/songlanglang/codex-log-blocker.git
cd codex-log-blocker

# 2. 将 skill 复制到 Codex skills 目录
mkdir -p ~/.codex/skills/codex-log-blocker
cp SKILL.md ~/.codex/skills/codex-log-blocker/
cp -r scripts ~/.codex/skills/codex-log-blocker/

# 3. 安装拦截 trigger
bash ~/.codex/skills/codex-log-blocker/scripts/block_log_writes.sh install

# 4. 安装 launchd 守护进程（防 trigger 丢失）
bash ~/.codex/skills/codex-log-blocker/scripts/block_log_writes.sh install-daemon

# 5. 验证
bash ~/.codex/skills/codex-log-blocker/scripts/block_log_writes.sh verify
```

### 方式二：让 Codex / AI 助手自动安装

在 Codex 或任何支持 skill 的 AI 助手中说：

> "帮我装一下 codex-log-blocker 这个 skill，阻止 Codex 高频写日志烧 SSD"

如果 skill 已安装到 `~/.codex/skills/`，AI 会自动读取 SKILL.md 并执行安装流程。

## 使用

安装后无需任何操作，拦截在后台自动运行。

### 查看状态

```bash
bash ~/.codex/skills/codex-log-blocker/scripts/block_log_writes.sh status
```

输出示例：
```
=== Codex 日志写盘状态 ===

数据库文件:
  路径:      /Users/you/.codex/logs_2.sqlite
  大小:      29M
  创建时间:  Jul 12 14:16:31 2026

拦截 Trigger:
  状态: 已安装 (trigger 存在)

LaunchAgent 守护进程:
  状态: 已加载并运行

历史写入估算:
  历史总写入次数:    5550150
  已被自动清理:      5520928 条 (99.4%)
  实际磁盘写入估算:  11.05 GB ~ 18.42 GB (含 SQLite 写入放大)
```

### 验证拦截效果

```bash
bash ~/.codex/skills/codex-log-blocker/scripts/block_log_writes.sh verify
```

会进行 30 秒持续监控，确认 MAX(id)、COUNT、WAL 大小全部零增长。

### 恢复日志记录

如果需要排查 Codex 问题（比如需要看 TRACE 日志），临时恢复：

```bash
bash ~/.codex/skills/codex-log-blocker/scripts/block_log_writes.sh uninstall
```

排查完毕后重新安装：

```bash
bash ~/.codex/skills/codex-log-blocker/scripts/block_log_writes.sh install
bash ~/.codex/skills/codex-log-blocker/scripts/block_log_writes.sh install-daemon
```

## 命令一览

| 命令 | 说明 |
|------|------|
| `install` | 安装 trigger + VACUUM 回收碎片空间 |
| `install-daemon` | 安装 launchd 守护进程（每 5 分钟自检 trigger） |
| `verify` | 验证拦截是否生效（30 秒监控） |
| `status` | 查看当前状态和历史写入量 |
| `uninstall` | 卸载所有组件，恢复日志记录 |

## 拦截效果

| 指标 | 拦截前 | 拦截后 |
|------|--------|--------|
| MAX(id) | 持续增长（555 万+） | 冻结不变 |
| COUNT(*) | 随自动清理波动 | 冻结不变 |
| WAL 文件大小 | 0~数 MB 波动 | 永久 0 字节 |
| 写入频率 | ~53 次/分钟 | 0 次/分钟 |
| DB 修改时间 | 每秒更新 | 停在安装时刻 |

## 工作原理

```
Codex 进程
    │
    ▼
INSERT INTO logs (...)          ← Codex 的 Rust tracing 机制
    │
    ▼
BEFORE INSERT trigger           ← 本 skill 安装的拦截器
    │
    ▼
RAISE(IGNORE)                   ← 静默丢弃，不报错
    │
    ▼
不写数据页 ✗
不写 WAL ✗
不写索引 ✗
磁盘 I/O = 0 ✅
```

### 持久化保障

| 层级 | 措施 | 说明 |
|------|------|------|
| 第一层 | trigger 写入主库 | 已 checkpoint 到主库文件，持久存在 |
| 第二层 | `~/.codex/ensure_log_blocker.sh` | 自检脚本，检查 trigger 是否存在 |
| 第三层 | LaunchAgent | 每 5 分钟自动运行自检脚本，trigger 丢了就重建 |

## FAQ

**Q: 会不会影响 Codex 正常使用？**

不会。trigger 只拦截 `logs_2.sqlite` 的 `logs` 表写入。Codex 的会话记录存储在 `sessions/` 目录的 jsonl 文件中，线程历史存储在 `thread_history_1.sqlite` 中，都不受影响。

**Q: Codex 升级后 trigger 会不会丢？**

有可能。Codex 升级时可能重建数据库。launchd 守护进程每 5 分钟自检一次，最多 5 分钟内自动恢复拦截。已在测试中验证：删除 trigger → 自检脚本自动重建 → 拦截仍然有效。

**Q: RAISE(IGNORE) 会不会写 WAL？**

不会。手动测试确认：触发 `RAISE(IGNORE)` 后 WAL 大小保持 0 字节。SQLite 在 `RAISE(IGNORE)` 时不产生任何数据页或 WAL 写入。

**Q: 之前已经被写入的 SSD 寿命能恢复吗？**

不能。SSD 的 TBW（Total Bytes Written）是不可逆的。安装这个 skill 只能防止进一步的损耗，不能修复已有的损耗。所以越早安装越好。

## License

MIT
