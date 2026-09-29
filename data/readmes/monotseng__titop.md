# TiTop

[English](README_EN.md) | **简体中文**

TiTop 是一个面向 TiDB 集群的轻量级实时终端监控工具，交互体验参考 `oratop`。它直接查询 Prometheus，并可选连接 TiDB SQL 端口，在一个终端中集中展示集群负载、节点状态、TiKV 请求、线程池 CPU、SQL 类型和活跃会话。

TiTop 适合日常巡检、故障现场观察、压测监控和远程终端使用。Prometheus 是必需数据源；TiDB 数据库账号是可选项，仅在需要活跃会话、长事务和组件间 TLS 状态时使用。

> [!IMPORTANT]
> TiDB 数据库账号并非必需。启用 SQL 增强功能时，只需使用能够读取所需诊断系统表的最小权限专用账号，无需授予任何业务数据读写权限或管理权限。

## 功能概览

- 集群活动：QPS、事务完成速率（TPS）、P99、连接数、活跃数、错误率及 TiDB/TiKV/PD 在线节点数。
- 当前异常：长查询、长事务和 TiDB 组件间 TLS 状态。
- 节点视图：角色、状态、版本、运行时间、QPS、连接、CPU、RSS、主机内存及 TiKV 读写命令速率。
- TiKV 请求：OPS、平均延迟、P99 延迟和每秒累计时间负载。
- TiKV 线程池：Unified Read、Raft Store、Async Apply、gRPC Poll、Storage Read 和 GC Worker CPU。
- SQL 类型：DML/事务、DDL、管理和其他操作四栏展示。
- 活跃会话：实例、连接 ID、短 `DIGEST_ID`、用户、来源、数据库、Command、State、执行时间、当前摘要窗口统计、内存、磁盘临时空间及 SQL 文本。
- 交互刷新：页面切换、暂停、手动刷新、纯文本和单次快照。

## 环境要求

- Linux：交互式终端依赖 Linux TTY；其他平台可以使用 `--once` 或 `--plain`。
- Go 1.23 或更高版本：仅从源码构建时需要。
- 网络连通性：运行 TiTop 的主机需要访问 Prometheus HTTP API。
- 可选 SQL 连通性：使用 `-u/-p` 时，需要访问自动发现的 `4000` 端口或 `--mysql-address`。

默认情况下 TiTop 从 Prometheus 返回的 UP TiDB 实例中提取主机，并使用 `4000` 作为这些 TiDB 主机的 SQL 端口。若自动发现的 TiDB 主机统一监听其他 SQL 端口，例如 `4400`，使用 `-P 4400`。

`-P/--port` 只作用于自动发现的 TiDB 主机。若实际连接入口是 F5、VIP、代理或 Kubernetes Service，应使用包含入口端口的完整地址，例如 `--mysql-address f5.example.com:6000`。这里 TiDB 后端仍可能监听 `4000`，但 TiTop 连接的是 F5 暴露的 `6000`。由于 `--mysql-address` 已包含端口，不能与 `-P/--port` 同时使用。

## 快速开始

### 仅使用 Prometheus

```bash
./titop --prometheus 10.0.0.10:9090
```

省略协议时自动使用 HTTP。以下写法等价：

```bash
./titop -m 10.0.0.10:9090
./titop -m http://10.0.0.10:9090
```

可在地址前指定用于页面展示的集群名：

```bash
./titop -m production@http://10.0.0.10:9090
```

未指定集群名时显示 `unknown`。集群名仅用于展示；共享 Prometheus 可另外传入 `--cluster-label production`，为所有 TiDB 指标添加 `tidb_cluster="production"` 过滤条件。

### 启用 SQL 增强功能

```bash
./titop -m production@10.0.0.10:9090 -u monitor -p 'password'
```

为避免密码进入 shell 历史和进程参数，推荐使用环境变量：

```bash
export TITOP_PROMETHEUS=production@http://10.0.0.10:9090
export TITOP_MYSQL_USER=monitor
export TITOP_MYSQL_PASSWORD='password'
./titop
```

集群要求加密 SQL 连接时，可指定自定义地址和 CA：

```bash
./titop -m production@10.0.0.10:9090 -u monitor \
  --mysql-address tidb.example.com:4000 --mysql-tls \
  --mysql-tls-ca /etc/titop/ca.pem --mysql-tls-server-name tidb.example.com
```

`-u` 和 `-p` 必须同时提供。数据库账号需要能够读取以下系统表：

- `INFORMATION_SCHEMA.CLUSTER_PROCESSLIST`
- `INFORMATION_SCHEMA.CLUSTER_STATEMENTS_SUMMARY`
- `INFORMATION_SCHEMA.CLUSTER_TIDB_TRX`
- `INFORMATION_SCHEMA.CLUSTER_CONFIG`

> [!WARNING]
> **不要使用 `root` 用户或其他高权限管理账号运行 TiTop。** 请创建专用的只读监控账号，避免因凭据泄露、误操作或工具运行环境被入侵而危及整个集群。

要查看其他用户的活跃会话，TiDB 还要求账号拥有全局 `PROCESS` 权限；没有该权限时，`CLUSTER_PROCESSLIST` 通常只返回当前账号自己的会话，可能使 `LONG QUERY` 错误显示为零。实际所需权限会因 TiDB 版本和集群安全策略而异。请遵循最小权限原则，不要授予 `SUPER`、DDL、DML、用户管理或授权管理权限，并验证该账号不能修改业务数据或集群配置。

## 命令行参数

| 参数 | 默认值 | 说明 |
| --- | ---: | --- |
| `--prometheus` | `TITOP_PROMETHEUS` | `[cluster@]Prometheus地址`，支持 URL 或 `IP:端口` |
| `-m` | 同上 | `--prometheus` 的简写 |
| `-u` / `--user` | `TITOP_MYSQL_USER` | TiDB SQL 用户名 |
| `-p` / `--password` | `TITOP_MYSQL_PASSWORD` | TiDB SQL 密码 |
| `-P` / `--port` | `TITOP_MYSQL_PORT` 或 `4000` | 自动发现 TiDB 主机使用的 SQL 端口 |
| `--mysql-address` | 自动发现 `:4000` | 逗号分隔的 TiDB SQL `host:port` 地址 |
| `--mysql-tls` | `false` | 启用 TiDB SQL TLS |
| `--mysql-tls-ca` | `TITOP_MYSQL_TLS_CA` | SQL TLS CA PEM 文件 |
| `--mysql-tls-server-name` | `TITOP_MYSQL_TLS_SERVER_NAME` | SQL TLS 证书服务器名 |
| `--cluster-label` | `TITOP_CLUSTER_LABEL` | 过滤 Prometheus 的 `tidb_cluster` 标签 |
| `--output` | `text` | 输出格式：`text` 或 `json`；JSON 自动单次退出 |
| `--interval` | `5s` | 自动刷新间隔，最小 1 秒 |
| `--timeout` | `4s` | 单轮 Prometheus/SQL 查询超时 |
| `--long-query-threshold` | `10s` | 当前长查询判定阈值 |
| `--long-txn-threshold` | `1m` | 当前长事务判定阈值 |
| `--high-qps` | `50000` | 高 QPS 阈值 |
| `--high-tps` | `5000` | 高 TPS 阈值 |
| `--once` | `false` | 输出一次快照后退出 |
| `--plain` | `false` | 不清屏、不读取交互按键 |
| `--no-color` | `false` | 禁用 ANSI 颜色 |
| `--version` | - | 显示版本并退出 |

SQL 地址示例：

```bash
# 直连自动发现的 TiDB 节点，节点 SQL 端口统一为 4000
titop -m prometheus.example.com:9090 -u root -p 'password' -P 4000

# 通过 F5 的 6000 端口连接（后端 TiDB 端口可以是 4000）
titop -m prometheus.example.com:9090 -u root -p 'password' \
  --mysql-address f5.example.com:6000
```

也可以设置 `NO_COLOR=1` 禁用颜色。

## 交互按键

| 按键 | 功能 |
| --- | --- |
| `i` | TiDB、TiKV、PD 全部节点 |
| `k` | TiKV 线程池 CPU |
| `s` | SQL 类型和活跃会话 |
| `l` | Schema Load 性能面板 |
| `o` | 切换 Schema Overview/KV |
| `w` | TiKV 请求耗时 |
| `e` | 采集错误和陈旧指标详情 |
| `p` | 暂停或继续刷新 |
| `Space` | 立即刷新 |
| `h` / `?` | 打开或关闭帮助 |
| `q` | 退出 |

## 页面说明

### Cluster Activity

第一行展示集群总体吞吐、延迟、连接、错误率、节点数和组件版本。`QPS(1m)` 是全部 SQL 语句执行速率；`TPS(1m)` 来自 `tidb_session_transaction_duration_seconds_count{scope="general"}`，表示业务作用域事务完成事件的速率，不保证只包含成功提交事务，因此不等同于业务提交量。两者都是 Prometheus 最近一分钟的 rate 平滑值，与 Schema Load 按标题中实际 `INTERVAL` 计算的短周期 QPS 口径不同，不要求两者严格相等。TiDB、TiKV 和 PD 所有节点版本一致时，`VERSION` 显示绿色版本号；检测到多个版本时显示红色 `MIXED`；版本指标不完整时显示默认色 `N/A`。第二行展示依赖 SQL 连接的诊断状态：

- `LONG QUERY`：`CLUSTER_PROCESSLIST` 中非 Sleep 且运行时间达到阈值的会话数量。
- `LONG TXN`：`CLUSTER_TIDB_TRX` 中持续时间达到阈值的事务数量。
- `CLUSTER TLS CFG`：通过 `CLUSTER_CONFIG` 检查 TiDB、TiKV 和 PD 的组件间 TLS 路径配置。它与 TiTop 自身的 `--mysql-tls` 传输加密相互独立，也不验证文件、证书有效期或实际连接状态。

TLS 状态含义：

| 状态 | 颜色 | 含义 |
| --- | --- | --- |
| `CONFIGURED` | 绿色 | 所有 TiDB、TiKV、PD 实例的 CA、证书和私钥路径均非空 |
| `EMPTY` | 红色 | 所有相关配置均为空 |
| `INCONSISTENT` | 黄色 | 组件或实例间配置不一致，或证书配置不完整 |
| `UNKNOWN` | 黄色 | 查询成功，但没有返回足够配置项 |
| `N/A` | 默认色 | 未提供 SQL 凭据、连接失败或查询失败 |

### All Cluster Nodes

节点按 DOWN 优先、CPU 降序排列。QPS 仅适用于 TiDB，因此 TiKV 和 PD 节点显示 `-`。`READ CMD/s` 和 `WRITE CMD/s` 来源于 `tikv_storage_command_total`，表示按类型归类的 TiKV storage command 次数；它们不是 key 数、SQL 数、事务数或物理磁盘 IOPS。

CPU 以单核为 100%：多线程进程可能超过 100%。RSS/HOST% 依赖 node_exporter 的主机内存指标；无法匹配主机时显示 `-`。

### TiKV Thread Pool CPU

线程池 CPU 使用 TiDB Dashboard 风格的明确 PromQL，从 `tikv_thread_cpu_seconds_total` 计算一分钟速率并按实例求和。例如 Unified Read：

```promql
sum(rate(tikv_thread_cpu_seconds_total{name=~"unified_read_po.*"}[1m])) by (instance)
```

显示值是线程池累计 CPU 核占用比例，而不是主机 CPU 百分比：`100%` 约等于持续占用一个 CPU 核，`400%` 约等于四个 CPU 核。

### SQL Types

该区域始终从 Prometheus 的 `tidb_executor_statement_total` 获取 SQL 类型 QPS，并按以下四类展示：

- DML / TXN
- DDL
- ADMIN
- OTHER

SQL 页面不会重复展示 TOP 5 TiKV Request，以便为 SQL 信息保留更多空间。

### Active SQL Sessions

提供 SQL 凭据后，TiTop 查询 `CLUSTER_PROCESSLIST`，并以实例和 digest 关联当前 `CLUSTER_STATEMENTS_SUMMARY` 窗口。`WIN EXEC` 和 `WIN AVG` 分别表示该 digest 在当前 Statement Summary 窗口中的累计执行次数和加权平均延迟；窗口长度由 TiDB 的 `tidb_stmt_summary_refresh_interval` 控制，它们不是最近十分钟的滚动统计。页面最多显示 30 个非 Sleep 会话，按执行时间降序排列。

`DIGEST_ID` 是由 TiDB 原始 digest 再次生成的 13 位稳定短标识，使用体验类似 Oracle SQL ID，但不与 Oracle SQL ID 等价。TiDB 原始 digest 和完整 SQL 文本都比较长，在有限宽度的终端中直接展示会挤压其他关键列；`DIGEST_ID` 可以用较短的固定宽度快速对照多个活跃会话。

相同的 TiDB digest 始终得到相同的 `DIGEST_ID`。当两条 SQL 文本看起来非常相似时，可以先通过 `DIGEST_ID` 判断它们是否属于同一个 TiDB digest；不同 `DIGEST_ID` 表示原始 digest 一定不同。由于 `DIGEST_ID` 是截短后的标识，理论上仍存在极低的哈希碰撞可能，因此它适合终端快速识别和关联，不应替代 TiDB 原始 digest 作为审计或程序判断依据。需要严格确认时，应查询并比较完整的原始 digest。

会话内存达到 100 MiB，或磁盘临时空间达到 1 GiB 时，会话连接 ID 加粗标红。TiDB 偶尔可能返回无符号下溢的异常 MEM/DISK 值；TiTop 会将超出有效整数范围的值按零处理，避免整页查询失败。

### Schema Load

提供 SQL 凭据后，按 `l` 可打开 Schema Load 面板。TiTop 从 `CLUSTER_STATEMENTS_SUMMARY` 读取集群各 TiDB 实例的累计计数，并结合 `CLUSTER_STATEMENTS_SUMMARY_HISTORY` 衔接 summary 刷新窗口。为避免 TiTop 自身诊断 SQL 污染结果，面板排除 `information_schema`。数据先按实例、Schema 和 summary 窗口聚合，再通过相邻快照差值计算最近刷新区间的负载，默认按 `TIME LOAD` 降序显示 Top 20 Schema。空 Schema 保持显示为 `(none)`，表示执行 SQL 时没有选定默认 Schema。

按 `o` 可在两个子视图间切换：

- `SCHEMA LOAD / OVERVIEW`：展示总体 QPS、写 QPS、延迟、时间负载、错误、Keys、影响行数及资源消耗，按 `TIME LOAD` 排序。
- `SCHEMA LOAD / KV`：展示 `TOTAL KEYS/s`、`PROC KEYS/s`、`MVCC AMP`、`COP TASK/s`、`COP/EXEC`、`BACKOFF/s`、`WRITE KEYS/s`、`WRITE SIZE/s` 和 `TXN RETRY/s`，按 `TOTAL KEYS/s` 排序。

`MVCC AMP` 为区间 `TOTAL KEYS / PROC KEYS`，用于观察 MVCC 读取放大；`COP/EXEC` 表示平均每次 SQL 执行产生的 Coprocessor Task 数量。

KV 子视图颜色阈值：`MVCC AMP` 达到 `2x` 显示黄色、达到 `10x` 显示红色；`COP/EXEC` 达到 `100` 显示黄色、达到 `1000` 显示红色；`BACKOFF/s` 和 `TXN RETRY/s` 大于零显示黄色，分别达到 `10/s` 和 `1/s` 时显示红色。其余吞吐量指标默认显示绿色。这些阈值用于快速观察，不等同于告警策略。

- 面板全部指标采用标题中 `INTERVAL` 标明的最近一次有效采样区间，不使用 TiTop 进程运行期累计值。
- `QPS` 是全部 SQL 执行速率；`WRITE QPS` 是 `INSERT`、`UPDATE`、`DELETE` 和 `REPLACE` 的执行速率。它比按默认 Schema 归属 `COMMIT` 得出的近似 TPS 更可靠。
- `AVG LAT` 是区间加权平均延迟；`TIME LOAD` 是 Schema 总执行时间除以区间时长，`1.00s/s` 约等于持续消耗一个执行时间核。
- `ERR/s` 和 `ERR%` 分别表示每秒错误数和区间错误比例；`PROC KEYS/s`、`WRITE KEYS/s` 和 `AFFECT ROWS/s` 为区间增量除以实际采样时长。
- 第一次采集只建立基线，下一次刷新开始显示负载。计数器回退、TiDB 重启或 summary 清空时不会产生负增量，并显示 `RESET DETECTED`。
- `AVG MEM/EXEC` 和 `AVG DISK/EXEC` 是区间内按执行次数加权的平均单次 SQL 内存及临时磁盘用量，不是吞吐或当前占用。

#### Schema QPS 与 Cluster QPS

Cluster Activity 的 `QPS(1m)` 来自 Prometheus `tidb_executor_statement_total` 最近一分钟的 rate，用于观察整个 TiDB 集群的总体 SQL 吞吐。Schema Load 的 `QPS` 则来自 `CLUSTER_STATEMENTS_SUMMARY` 相邻快照的 `EXEC_COUNT` 差值，再除以标题中的实际 `INTERVAL`。两者的数据源、时间窗口和统计口径均不相同，因此各 Schema QPS 相加后不要求等于 Cluster QPS。

> [!IMPORTANT]
> **Schema QPS 只能作为 Schema 相对活跃度和负载趋势的参考，不是准确、完整的 Schema 请求计量。** `SCHEMA_NAME` 表示 SQL 执行时连接所选定的默认 Schema，并不一定是 SQL 实际访问对象所在的 Schema；跨 Schema SQL 也无法按真实访问比例拆分。

Schema QPS 还可能受到以下因素影响：

- Schema QPS 使用几秒钟的实际采样区间，而 Cluster QPS 是一分钟平滑值。
- Statement Summary 可能因容量限制淘汰 digest，造成统计缺失。
- TiDB 重启、Summary 清空、窗口切换或采集失败可能导致区间数据不完整。
- `tidb_stmt_summary_internal_query` 等配置会影响哪些 SQL 进入 Statement Summary。
- 没有选择默认 Schema 的 SQL 会归入 `(none)`，即使它通过完整限定名访问了某个业务 Schema。

因此，应使用 Cluster QPS 判断集群总体吞吐，使用 Schema QPS 比较当前哪些默认 Schema 相对更活跃；容量规划、计费、审计或需要精确请求量时，不应使用 Schema QPS 作为唯一依据。

`TIME LOAD` 的计算方式为：

```text
TIME LOAD = 区间内 SQL 总执行时间 / 实际采样时长
```

例如采样时间为 10 秒，某 Schema 的 SQL 总执行时间增量为 50 秒，则 `TIME LOAD` 为 `5.00s/s`，表示该 Schema 在该区间平均产生了约 5 个并发数据库时间单位。它包含 CPU 执行以及锁、TiKV RPC、Coprocessor、网络、磁盘和事务提交等等待时间，因此不是 CPU 使用率。

| 现象 | 建议理解 |
| --- | --- |
| `TIME LOAD` 高、QPS 高、`AVG LAT` 正常 | 通常是高吞吐业务负载，不一定异常 |
| `TIME LOAD` 高、`AVG LAT` 高 | 关注慢 SQL、锁等待或下游延迟 |
| `TIME LOAD` 高、`ERR%` 高 | 关注 SQL 执行错误 |
| `TIME LOAD` 高、`MVCC AMP` 高 | 关注 MVCC 历史版本读取放大 |
| `TIME LOAD` 高、`COP/EXEC` 高 | 单次 SQL 可能扫描大量 Region |
| `TIME LOAD` 高、`BACKOFF/s` 高 | 关注锁冲突、Region 或 RPC 重试 |
| `WRITE QPS`、`WRITE SIZE/s` 高 | 该 Schema 当前写入负载较高 |

因此 `TIME LOAD` 适合用作 Top Schema 的默认排序和排查入口，但不能单独证明某个 Schema 存在性能异常，应结合 Overview 和 KV 子视图共同判断。

Statement Summary 可能因 `tidb_stmt_summary_max_stmt_count` 限制而淘汰 digest，因此该面板适合实时性能观察，不应作为审计级精确统计。

## 颜色和阈值

- P99：达到 200 ms 显示黄色，达到 1 s 显示红色。
- 节点 CPU：达到 70% 显示黄色，达到 90% 显示红色。
- QPS/TPS：达到高负载阈值显示黄色；如果同时发生 P99 ≥ 1 s、执行错误或任一 TiDB CPU ≥ 90%，显示红色。
- 长查询/长事务：当前数量大于零显示红色。
- 节点状态：UP 绿色、DOWN 红色、未知状态黄色。
- Active Session ID：内存或磁盘临时空间超过阈值时显示红色。

这些颜色用于快速观察，不等同于完整告警策略。生产环境仍应使用 Prometheus Alertmanager 等系统配置持续告警。

## 构建

代码按职责拆分：`main.go` 仅负责启动，`config.go` 负责 CLI 配置，`app.go` 管理刷新生命周期，`render_text.go` 与 `render_format.go` 负责终端展示，`output_json.go` 维护 JSON 输出契约，`sql_collector.go` 协调 SQL 诊断采集。Prometheus、TiDB SQL 和终端能力位于各自的 `internal` 包中。

```bash
make test
make vet
make build
```

仓库包含 GitHub Actions CI；push 和 pull request 会在 Go 1.23 与当前稳定版上运行格式、测试、覆盖率和 `go vet` 检查，并执行 race detector、Staticcheck、govulncheck 及跨平台构建验证。

本机构建产物位于 `bin/titop`。

构建 Linux、macOS 和 Windows release：

```bash
make release
```

产物：

```text
release/titop-linux-arm64
release/titop-linux-amd64
release/titop-darwin-arm64
release/titop-darwin-amd64
release/titop-windows-amd64.exe
release/checksums.txt
```

覆盖版本号：

```bash
make release VERSION=0.9.0
```

## 单次输出和脚本使用

```bash
./titop -m 10.0.0.10:9090 --once --no-color
./titop -m 10.0.0.10:9090 --plain --no-color
```

`--once` 在 Prometheus 或 SQL 增强查询出现错误时以非零状态退出。`--output json` 可供脚本、巡检和 CI 使用。JSON 顶层的 `schema_version` 表示输出契约版本；`snapshot.Availability` 可用于区分真实零值和无数据指标，`snapshot.Stale` 则标记使用缓存值的指标及其采集时间。

推送 `v*` Git tag 时，发布工作流会通过 GoReleaser 创建多平台归档、SHA-256 校验和及 GitHub Release。默认版本来自 `git describe`，也可通过 `make release VERSION=...` 覆盖。

## 已知限制

- Prometheus 当前不支持 Basic Auth、Bearer Token、客户端证书或自定义 CA。
- 不同 TiDB/TiKV 版本可能缺少个别指标或系统表；独立查询失败不会影响其他 Prometheus 指标。
- 集群展示名仍不自动充当标签过滤器；共享 Prometheus 请显式传入 `--cluster-label`。

## 故障排查

### Prometheus URL 无效

确认地址包含正确的主机和端口。`IP:端口` 会自动补充 `http://`，HTTPS 地址必须明确写出 `https://`。

### SQL 页面显示连接错误

确认：

1. Prometheus 返回了 UP 状态的 TiDB 实例。
2. 运行 TiTop 的主机能访问自动发现的 `4000` 端口或 `--mysql-address`。
3. 用户名、密码和系统表权限正确。
4. 集群要求 TLS 时已配置 `--mysql-tls`、CA 和正确的服务器名。

### 指标为零或页面底部出现 WARN

按 `e` 查看具体错误和最后成功采样时间。TiTop 会保留失败指标的最近成功值，并对陈旧数据进行标记。

### 终端颜色或布局异常

使用 `--no-color` 排除 ANSI 颜色影响，并增大终端宽度。重定向输出时推荐同时使用 `--plain --no-color`。

## 项目结构

```text
cmd/titop/             CLI、交互循环和终端渲染
internal/monitor/      PromQL 定义、并发采集和快照聚合
internal/prometheus/   Prometheus HTTP API 客户端
internal/tidbsql/      TiDB SQL 连接和诊断查询
internal/terminal/     TTY 原始模式和终端宽度
```

## 与 oratop 的差异

Oracle 的 ASH 和等待事件无法直接映射到 TiDB Prometheus 指标。TiTop 当前以 TiKV 请求累计耗时作为等待压力的近似视图，并在提供 SQL 凭据时使用 TiDB 集群系统表展示当前活跃 SQL 和事务状态。

## Roadmap

- Prometheus Basic Auth、Bearer Token、mTLS 和自定义 CA。
- TiKV 热点、Region、Raft、磁盘和 PD 调度视图。
- 交互式排序、过滤和可配置会话资源阈值。

## License

TiTop 采用 [Apache License 2.0](LICENSE) 开源。第三方依赖的许可证信息请参阅 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
