# dmtop

<p align="center">
  <img src="docs/images/dmtop-logo.png" width="560" alt="dmtop logo">
</p>

**Dameng Database Real-Time Performance TUI**

**达梦数据库实时性能诊断工具**

`dmtop` 是一个使用 Go 编写的 DM8 本机实时性能诊断工具。它把 Linux 主机压力、
数据库活动、会话线程、SQL 和阻塞链组织在同一个终端界面中，用于快速回答：

- 当前压力来自 CPU、内存、磁盘还是网络；
- 哪个数据库会话和 Linux 线程正在消耗 CPU；
- 哪条 SQL 正在执行，完整 SQL 和执行计划是什么；
- 哪个会话阻塞了哪个会话，根阻塞者是谁；
- 解析、计划缓存、提交同步和锁等待是否出现异常。

**当前版本：v0.2.2 · 主题：SQL Throughput & Transaction Diagnosis**

![Go](https://img.shields.io/badge/Go-1.24+-00ADD8?logo=go)
![DM](https://img.shields.io/badge/Database-DM8-1f6feb)
![Platform](https://img.shields.io/badge/Platform-Linux-lightgrey?logo=linux)
![License](https://img.shields.io/badge/License-MIT-2ea44f)

> `dmtop` 是面向当前故障的轻量诊断工具，不是数据库巡检、监控平台或 AWR 替代品。
> 它不部署 Agent、不启动 `disql`、不长期保存监控数据。为保证 OS 与数据库证据属于
> 同一台机器，推荐并默认按“在 DM 数据库主机本地运行”理解所有指标。

------

## 项目定位

`dmtop` 将数据库动态视图和 Linux `/proc` 的相邻采样汇总为一份实时证据快照：

```text
 Linux /proc                         DM8 dynamic views
 CPU / memory / disk / network       V$SESSIONS / V$SYSSTAT / V$TRXWAIT / ...
              |                                  |
              +----------------+-----------------+
                               |
                               v
                       Interval Snapshot
                               |
                 +-------------+-------------+
                 |             |             |
                 v             v             v
                OS            DB          PROCESS
                                               |
                                      +--------+--------+
                                      |                 |
                                      v                 v
                                  SQL Detail       LOCK CHAIN
```

工具追求的是“小、快、证据直接”：进入数据库主机后运行一个二进制文件，先看全局压力，
再沿 `PROCESS -> SID/TID -> SQL/PLAN/BLOCKER` 下钻，不需要预先部署监控服务。

------

## 主界面

<p align="center">
  <img src="docs/images/dmtop-main.png" width="1200" alt="dmtop 主界面">
</p>

界面使用连续的经典 TUI 表格，逻辑宽度随终端收缩，宽终端封顶 132 列；80×24
仍可使用。反色标题栏保持等宽，主界面不显示常驻快捷键帮助行。

| 区域 | 作用 | 主要证据 |
| --- | --- | --- |
| DATABASE | 确认目标身份 | 模式、状态、数据库名、实例名、数据库运行时间、归档状态 |
| OPERATING SYSTEM PERFORMANCE | 判断主机瓶颈 | CPU、负载、内存、Swap、磁盘吞吐/延迟、网络收发 |
| DATABASE PERFORMANCE | 判断数据库负载类型 | 会话、事务、STMT/s、CURSOR/s、TPS、逻辑/物理 IO、Redo、缓存、解析、计划、锁与提交延迟 |
| PROCESS | 定位责任会话 | SID、Linux TID、区间 CPU、AGE、事务号、DML/锁计数、用户、客户端和 SQL |
| LOCK CHAIN | 展示实时阻塞关系 | `ROOT BLOCKER -> WAITER`、锁类型/模式、对象和等待时长；无阻塞时不占屏幕 |

界面图由真实渲染器生成，避免文档与实际输出漂移。重新生成：

```bash
go run ./cmd/_mockup
```

------

## 核心能力

- **本机 OS 诊断**：直接读取 `/proc`，展示 CPU user/system/idle/iowait、1/5/15 分钟
  load、内存与 Swap、最热磁盘的 util/await/IOPS/吞吐，以及网络 RX/TX。
- **数据库活动总览**：从 `V$SYSSTAT`、`V$SESSIONS`、`V$TRX`、内存池和缓存视图计算
  STMT/s、CURSOR/s、TPS、逻辑/物理读写、Redo、Parse、Hard Parse、Parser Error、Plan Hit、Redo Sync、
  Lock Wait 和 Deadlock 等证据。
- **会话到操作系统线程**：`V$SESSIONS.THRD_ID` 直接显示为 `TID`，与
  `top -H -p <dmserver-pid>`、`ps -L` 对齐；会话 `%CPU` 优先来自对应 Linux 线程。
- **实时 PROCESS 排行**：保留 ACTIVE、IDLE 与 IDLE-TX 用户会话，按当前采样区间 CPU 降序，
  最多 20 行；CPU 采用绿/黄/红分级，IDLE 绿色，具有 DML、持锁或阻塞链证据的空闲事务以
  黄色 `IDLE-TX` 显示，并关联 `TRX_ID`、`DML_CNT` 与 `LOCK_CNT`。
- **直观阻塞链**：基于 `V$TRXWAIT` 的真实 `WAIT_FOR_ID` 关系，按
  `ROOT BLOCKER -> WAITER` 方向展开多级链，并关联双方 SID、TID、用户、锁对象和时长；
  DDL 锁同时展示 `V$LOCK.LTYPE/LMODE`，例如 `OBJECT/X`。
- **长 SQL 与长事务提示**：当前请求、或 dmtop 连续观察到有 DML/持锁证据的空闲事务
  达到 30 秒后，分别输出 `LONG SQL`、`LONG TX`。长 SQL 包含 SID、TID、AGE、CPU、WAIT 和 `CUR_SQLSTR`；
  长事务包含事务号、观测年龄下限、DML 与锁计数。
- **三层 SQL 证据**：PROCESS 详情同时展示 `V$SESSIONS.SQL_TEXT`、`CUR_SQLSTR` 和
  按需获取的 `SF_GET_SESSION_SQL(SID)`，适合从存储过程调用下钻到内部热点 SQL。
- **SQL RT / SQL CUM**：NOW 使用相邻采样差值定位当前重 SQL；CUM 使用游标累计值发现
  长期重 SQL。两者按 `SQL_ID` 聚合并独立排序。
- **交互式执行计划**：按 `x` 输入 `SQL_TEXT_ID`，从 `V$SQLTEXT` 按 `SQL_NTH` 拼接
  完整 SQL，显示 `FULL SQL` 和 `SQL PLAN`；计划页支持滚动。
- **安全会话关闭**：按 `k` 输入数据库 SID，重新展示目标证据并要求 `y` 确认后才调用
  `SP_CLOSE_SESSION(SID)`；拒绝关闭 dmtop 自身连接和内部会话。
- **按需 ENV 信息**：参数、库规模、对象数量、表空间和 Hot-Lock 热点只在进入 ENV
  子屏时查询，不增加日常刷新负担。
- **版本兼容降级**：启动时查询 `V$DYNAMIC_TABLES` 与 `V$DYNAMIC_TABLE_COLUMNS`；缺少
  视图或字段时选择兼容 SQL 或让单项显示 `N/A`/`-`，不会因一个字段缺失清空 PROCESS。
- **原生驱动与安全口令**：只使用达梦原生 Go 驱动和 `database/sql`；密码通过终端隐藏
  输入、受控环境变量或标准输入提供，拒绝命令行明文密码。

------

## 指标语义

所有指标先区分时间语义，再进入界面：

| 语义 | 定义 | 用途 |
| --- | --- | --- |
| NOW / RT | 相邻两次采样之间的增量或速率 | 当前故障定位；首帧显示 `warming up` |
| CUM | 实例启动或 SQL 游标创建以来的累计值 | 长期重 SQL 与累计资源消耗 |
| ENV | 参数、规模、对象、表空间等按需信息 | 环境核对，不参与每轮采样 |
| `N/A` | 数据源查询失败或当前版本不支持 | 与“查询成功但没有记录”严格区分 |
| `-` | 该状态下不适用或无法可靠计算 | 不使用猜测值冒充精确指标 |

### OS 指标

| 指标 | 口径 |
| --- | --- |
| CPU states | `/proc/stat` 相邻采样得到的 user/system/idle/iowait 百分比 |
| load avg | `/proc/loadavg` 的 1/5/15 分钟负载 |
| Memory / Swap | `/proc/meminfo` 的使用、空闲与缓存空间 |
| Disk util / await | `/proc/diskstats` 相邻采样的设备忙碌率和平均 IO 等待 |
| RIO/WIO、RMB/WMB | 磁盘每秒读写次数和 MiB 吞吐 |
| RX/TX | 非 loopback 网卡每秒接收和发送字节数 |

### DB 指标

| 指标 | 口径与注意事项 |
| --- | --- |
| sessions / active / idle | `V$SESSIONS` 当前快照，排除 dmtop 自身会话 |
| rw trx | `V$TRX` 中具有 DML、持锁或参与阻塞链证据的事务数；只读空闲会话的 `V$TRX` 行不计入 |
| AAS~ | 当前采样时刻 ACTIVE 会话数，是近似快照，不冒充 ASH 平均值 |
| STMT/s | `V$SYSSTAT` 中 SELECT、INSERT、UPDATE、DELETE 及对应 `in pl/sql` 计数的区间增量之和；扣除每轮 dmtop 查询数的估算开销，可观察存储过程内部 SQL 吞吐 |
| CURSOR/s | SQL RT 在采样区间观察到的可见游标执行次数，已排除 dmtop 查询；不等同于数据库全局 QPS |
| TPS / UCPS | `V$SYSSTAT` 相邻采样的事务与用户提交速率 |
| LIO / PRD / PWR / REDO | 逻辑读、物理读、物理写和 Redo 生成速率 |
| HIT / MEM_POOL / SORT_MEM | 缓冲命中率、内存池使用量和排序内存指标 |
| PARSE / HARD / PERR / PLANHIT | 解析、硬解析、解析错误和计划缓存效率 |
| SYNC / LOCKMS/s / DEADLOCK | 单次提交同步延迟、`V$SYSSTAT` 区间锁等待毫秒率和区间新增死锁；`LOCKMS/s` 不是当前 waiter 数 |
| STATE | `ACTIVE` 表示当前正在执行；`IDLE-TX` 表示空闲且有 DML、持锁或阻塞链证据；其余空闲会话显示 `IDLE` |
| AGE | ACTIVE 时为当前时间减 `LAST_RECV_TIME`，表示当前请求年龄；IDLE-TX 时为 dmtop 连续观察到可诊断事务的时间下限并显示 `>=`；IDLE 显示 `-` |
| TRX_ID / DML_CNT / LOCK_CNT | 可诊断事务号，以及 `V$TRX` 的插入、删除、更新合计和锁计数；只读无锁且未参与阻塞时显示 `-` |
| %CPU | 对应 TID 在本采样区间消耗的单核百分比，与 `top -H` 口径一致 |

> 对存储过程调用，ACTIVE `AGE` 表示整个 `CALL` 请求持续时间；内部单条 SQL 需要进入
> PROCESS 详情查看 `CUR_SQLSTR`。行锁的精确等待时长以 LOCK CHAIN 的
> `V$TRXWAIT.WAIT_TIME` 为准。DM8 在这里没有提供可跨版本依赖的事务开始时间，
> 因此 IDLE-TX 的 `AGE >=...` 是从 dmtop 首次看到该事务开始计算的下限，不是假定的精确年龄。

### SQL RT 与 SQL PATTERN

`SQL RT` 展示本采样区间的 SQL 强度：`EXEC/s` 是执行频率，`LIO/s` 是逻辑读速率，
`LIO/EX` 是单次执行逻辑读，`HARD/s` 是硬解析速率，`CPU%` 优先取 SQL 所属会话 TID 的
Linux 线程 CPU。按 `s` 进入该面板。

`SQL PATTERN` 将字符串和数字常量归一化为 `?`。例如：

```sql
SELECT * FROM T WHERE ID=123;
SELECT * FROM T WHERE ID=456;
```

会聚合为：

```sql
SELECT * FROM T WHERE ID = ?
```

面板按模板展示 `VARIANTS/s`、`HARD/s`、`EXEC/s`、`CPU%`，并关联主要来源的 USER、
APPNAME、CLNT_HOST 和 CLNT_IP。按 `p` 或数字 `5` 进入该面板。`VARIANTS/s` 表示本区间
首次观察到的不同 SQL 文本/游标变体速率。短于采样间隔且已从 `V$SQL_STAT` 消失的 SQL
无法逐条保留；当模板样本与全局硬解析风暴证据一致时，界面使用 `~` 标记按 `V$SYSSTAT`
估算的变体/硬解析速率，而不会把估算值冒充精确游标计数。

部分 DM8 版本不会在 `V$SQL_STAT` 中逐条暴露 `EXECUTE IMMEDIATE` 生成的内层 SQL，而是把
硬解析次数记录在外层 PL/SQL 游标上。遇到这种情况，dmtop 会从外层字符串拼接表达式提取
内层 SQL 模板，并以实测 `HARD_PARSE_CNT` 估算字面量变体数；`VARIANTS/s` 前仍用 `~` 明确
标识估算语义，`HARD/s` 则保持数据库记录的区间增量。

当 `STMT/s` 很高而 `CURSOR/s` 很低时，SQL 可能位于存储过程内部，或游标生命周期短于
采样间隔；界面会给出 `INTERNAL SQL` 提示。当 `HARD/s` 与模板 `VARIANTS/s` 同时升高时，
界面会给出 `LITERAL SQL` 提示并显示来源。部分 DM8 版本的 `plan total count` 不覆盖全部
动态 SQL；若它与硬解析速率矛盾，`PLANHIT` 显示 `N/A`。

------

## 适用场景

| 场景 | dmtop 提供的定位路径 |
| --- | --- |
| CPU 突然升高 | OS CPU/load → PROCESS `%CPU`/TID → Enter 查看内部 SQL |
| 行锁或 DDL 阻塞 | DB trx waits/LOCKMS/s → LOCK CHAIN 根阻塞者 → `TID`/`OBJECT/X` → SID/TID/SQL |
| 磁盘延迟 | OS util/await/RIO/WIO → DB PRD/PWR/REDO/SYNC |
| 提交变慢 | DB SYNC → 本机 disk await → 判断本地磁盘或同步主备链路 |
| 解析压力 | PARSE/HARD/HARD%/PERR → SQL RT/CUM 与计划缓存命中率 |
| 长 SQL | `LONG SQL` → PROCESS ACTIVE/AGE → CUR_SQLSTR → SQL_TEXT_ID/FULL SQL/SQL PLAN |
| 长时间未提交 | `LONG TX` → PROCESS IDLE-TX/AGE → TRX_ID/DML_CNT/LOCK_CNT → SID/TID/SQL |
| 会话异常 | PROCESS 客户端信息 → Enter 核实 → `k` 安全关闭 SID |
| 版本字段差异 | 启动能力检测 → 兼容 SQL → 单项 `N/A`/`-` 降级 |

不适合的场景：跨主机集中监控、长期趋势、告警、巡检报表和历史回放。这些需求应使用
Exporter/Prometheus 等持续监控体系，而不是扩大 dmtop 的产品边界。

------

## 快速开始

### 1. 准备可执行文件

发布版 Linux 静态二进制运行时不依赖 `disql`、Go 工具链或外部 Agent。请根据
`uname -m` 的输出选择发布包：`x86_64` 使用 `amd64`，`aarch64` 使用 `arm64`。

Linux amd64：

```bash
tar -xzf dmtop-v0.2.2-linux-amd64.tar.gz
cd dmtop-v0.2.2-linux-amd64
chmod +x dmtop
sudo install -m 0755 dmtop /usr/local/bin/dmtop
```

Linux arm64：

```bash
tar -xzf dmtop-v0.2.2-linux-arm64.tar.gz
cd dmtop-v0.2.2-linux-arm64
chmod +x dmtop
sudo install -m 0755 dmtop /usr/local/bin/dmtop
```

如果当前用户没有 `sudo` 权限，可以跳过 `install`，直接在解压目录运行 `./dmtop`。

从源码构建时需要先准备用户自己的 DM Go 驱动，见[源码构建：准备 DM Go 驱动](#源码构建准备-dm-go-驱动)。

### 2. 在数据库主机运行

默认端口 5236：

```bash
./dmtop SYSDBA
```

指定主机和非默认端口：

```bash
./dmtop SYSDBA@127.0.0.1:5237
```

程序会在终端中隐藏输入密码。主界面首次采样的速率项显示 `warming up`，下一轮开始
展示真实区间值。

### 3. 批处理取证

```bash
DMTOP_PASSWORD='由秘密管理系统注入' ./dmtop SYSDBA -c 2 -b

# 或从标准输入读取一行密码
printf '%s\n' "$PASSWORD" | ./dmtop SYSDBA -password-stdin -c 2 -b
```

批处理与交互模式复用同一套主界面、指标语义和兼容降级逻辑，适合重定向保存现场快照，
不会再出现批处理与 TUI 口径不一致的问题。

> 不支持 `USER/PASSWORD` 命令行形式，避免密码进入 shell history 和进程列表。

------

## 交互操作

主界面不常驻显示快捷键帮助；按 `h` 可在程序内查看，完整操作如下：

| 按键 | 操作 |
| --- | --- |
| `m` | 返回 PROCESS |
| `s` / `S` | 打开 SQL RT / SQL CUM |
| `p` / `5` | 打开 SQL PATTERN |
| `Tab` / `←` / `→` | 在 PROCESS、SQL RT、SQL CUM、SQL PATTERN 间切换 |
| `↑` / `↓` / `j` | 移动选中行 |
| `PgUp` / `PgDn` | 按页滚动 |
| `Enter` | 查看选中会话或 SQL 的详细证据 |
| `x` | 输入 `SQL_TEXT_ID`，查看完整 SQL 与执行计划 |
| `k` | 输入数据库 SID，核实并关闭会话 |
| `e` | 打开 ENV 按需信息 |
| `o` | 切换 SQL RT/CUM 排序 |
| `i` | 修改刷新间隔 |
| `/` / `c` | 设置 / 清除会话过滤条件 |
| `f` | 冻结 / 恢复刷新 |
| `h` | 打开帮助页 |
| `q` | 返回或退出 |

`k` 使用数据库 SID，不能输入 Linux TID。不要在操作系统中直接 `kill -9` 达梦线程。

------

## 常用参数

完整参数使用 `dmtop -h` 查看：

| 参数 | 说明 | 默认值 |
| --- | --- | --- |
| `USER[@HOST[:PORT]]` | 位置连接参数 | — |
| `-user` / `-host` / `-port` | 拆分连接参数 | — / `127.0.0.1` / `5236` |
| `-i` | 刷新间隔，秒 | `2` |
| `-connect-timeout` | 数据库连接超时 | `10s` |
| `-query-timeout` | 单条采集查询超时 | `5s` |
| `-session-detail-top` | PROCESS 最大采集行数，最多 20 | `20` |
| `-b` / `-c N` | 批处理模式 / 迭代次数 | 关 / 持续 |
| `-o` | 将批处理输出写入文件 | — |
| `-password-stdin` | 从标准输入读取密码 | 关 |
| `-no-os` | 禁用本机 OS 指标 | 关 |
| `-no-color` | 禁用 ANSI 配色 | 关 |
| `-debug` | 输出查询耗时和可选查询错误 | 关 |
| `-dsn-options` | 原生驱动 DSN 查询参数 | — |

连接信息也可通过 `DMTOP_USER`、`DMTOP_HOST`、`DMTOP_PORT` 和 `DMTOP_PASSWORD`
提供。密码环境变量只适合由受控服务或秘密管理系统注入。

------

## 源码构建：准备 DM Go 驱动

DM Go 驱动由使用者从自己的 DM 安装目录或官方下载包提供，不属于本仓库，也不适用
本项目的 MIT 许可证。

`scripts/setup-dm-go-driver.sh` 仅供从源码构建 dmtop 时使用：它把用户自行取得的
DM Go 驱动复制到 Git 忽略的 `.deps/dm`，以满足 `go.mod` 中的本地模块引用。直接下载
GitHub Release 中预编译二进制的用户不需要运行此脚本，也不需要另外安装 DM SDK。

在 Linux 开发或构建主机执行：

```bash
sh ./scripts/setup-dm-go-driver.sh /opt/dmdbms

# 也可直接传官方 go-YYYYMMDD.zip
sh ./scripts/setup-dm-go-driver.sh /path/to/go-YYYYMMDD.zip
```

脚本会定位或解压驱动、验证 `dm/go.mod` 和模块名，并在替换已有 `.deps/dm` 前创建时间戳
备份。不要把 `.deps` 或官方驱动提交到仓库。

------

## 构建与测试

```bash
go test ./...
go vet ./...
go build ./...
```

Linux amd64 静态构建：

```bash
GOOS=linux GOARCH=amd64 CGO_ENABLED=0 \
  go build -trimpath -ldflags "-s -w" \
  -o bin/dmtop-linux-amd64 ./cmd/dmtop
```

ARM64 主机将 `GOARCH` 改为 `arm64`。

------

## 兼容性与权限

- 支持 DM8；不同补丁版本的动态视图字段存在差异，dmtop 会先做能力检测再选择查询。
- 推荐在 Linux 数据库主机本地运行。异机连接虽然可以建立，但 OS 指标属于 dmtop
  所在机，因此不应作为远程数据库主机证据。
- 查看完整诊断证据需要能够查询相关 `V$` 视图和系统函数；当前测试与开发通常使用
  `SYSDBA`。最小权限授权脚本仍在后续路线中。
- `k` 关闭会话额外需要执行 `SP_CLOSE_SESSION` 的权限。
- 官方驱动 DSN 对部分特殊字符有限制；dmtop 会在连接前拒绝无法无歧义表达的凭据。

------

## 实现原则

- 数据库访问只使用达梦原生 Go 驱动和标准 `database/sql`，不执行外部命令。
- 连接池最多 1 条连接；每轮 SELECT 在同一采样事务中执行并回滚，避免监控查询污染 TPS。
- 每轮对 `V$SESSIONS`、`V$TRXWAIT`、`V$TRX` 和 `V$SQL_STAT` 各只扫描一次；摘要计数与
  PROCESS/SQL 资源值由同一批结果派生。
- 主界面不周期采集 EVENT；当前线程等待仅复用 `V$THREADS.WAIT_STATUS`，阻塞关系以
  `V$TRXWAIT` 明细为准。
- NOW 指标由相邻采样计算；首帧和数据源失败不会伪装成精确的 0。
- 监控 SQL 带 `/*dmtop*/` 标记，并通过会话 ID 与标记双重排除自身。
- SQL RT `%CPU` 优先使用 `/proc/<pid>/task/<tid>/stat`；DM 时间统计不可用时明确降级。
- 主界面只展示快速定位需要的证据，环境信息和完整 SQL 均按需查询。

------

## 目录结构

```text
cmd/dmtop/          CLI 入口、连接和刷新循环
cmd/_mockup/        使用真实渲染器生成 README 示例图
internal/config/    参数与安全输入
internal/conn/      达梦原生 database/sql 适配层
internal/collect/   能力检测、查询编排和相邻采样
internal/host/      Linux /proc 指标采集
internal/model/     领域快照与证据模型
internal/render/    80/132 列 TUI 与批处理渲染
internal/tui/       Bubble Tea 交互、下钻与会话关闭
scripts/            本地 DM SDK 安装脚本
```

------

## 迭代路线

| 版本 | 目标 |
| --- | --- |
| `v0.1.0` | 首个版本控制基线，建立 TUI、数据库/OS 采集和诊断链路 |
| `v0.2.0` | 原生驱动唯一后端；指标口径、兼容降级、OS/DB 仪表板、PROCESS 与阻塞链 |
| `v0.2.1` | 合并周期查询、移除 EVENT 采集、统一 TUI/批处理口径并降低监控开销 |
| `v0.2.2` | 真实语句吞吐、SQL 模板归一化、长 SQL/长事务与 DDL 锁诊断 |
| `v0.3.0` | `dmtop doctor`、最小权限脚本、JSONL/CSV 取证输出 |

------

## 延伸文档

- [需求与产品边界](docs/需求文档.md)
- [界面原型](docs/界面原型.md)
- [oratop 字段与达梦口径对照](docs/oratop字段-达梦对照与诊断.md)
- [达梦原生 Go 驱动评估](docs/原生Go驱动评估.md)
- [调度器锁争用案例](docs/案例-调度器锁争用.md)

------

## License

`dmtop` 使用 [MIT License](LICENSE)。

达梦原生 Go 驱动由用户单独提供，仍受其自身许可证约束，不包含在本项目 MIT 授权范围内。
