# GBase 8s Prometheus Exporter

基于 **GBase 8s 官方 JDBC 驱动**（Maven 中央仓库 `com.gbasedbt:jdbc`）和 **Prometheus Java Client** 编写的数据库监控导出器，暴露 `/metrics` 端点供 Prometheus 抓取。

## 特性

- **三档分频采集**，避免"为了监控数据库反而打爆数据库"：
  - **fast（默认 10s）**：连接 / QPS / TPS / CPU / IO / 锁 —— 8 次轻量查询
  - **normal（默认 60s）**：事务 / 表空间 / 日志 / 缓冲池 / 高可用 / 网络 —— 9 次查询
  - **slow（默认 300s）**：数据库对象统计（各库表数）
- 抓取 `/metrics` 时只读缓存，响应快、不压数据库
- 单指标查询容错：某一项查询失败不影响其他指标，连接失败体现在 `gbase8s_up` / `gbase8s_query_up`
- 指标命名对齐监控大盘规格（`gbase8s_connections/qps/tps/cpu_usage/io_*` 等）
- 单文件 fat jar，`java -jar` 直接运行；配置支持 spring 风格键名，可复用现有 Spring 配置

## 构建

```bash
mvn -q package -DskipTests
# 产物：target/gbase8s-exporter.jar
```

## 运行

```bash
# 方式一：读取同目录 application.properties
java -jar target/gbase8s-exporter.jar

# 方式二：命令行参数覆盖（优先级最高）
java -jar target/gbase8s-exporter.jar -Ddb.url="jdbc:gbasedbt-sqli://host:port/db:GBASEDBTSERVER=xxx" -Ddb.user=gbasedbt -Ddb.password=xxx -Dhttp.port=9090
```

配置优先级：**系统属性(-D) > 环境变量 > application.properties > 默认值**

| 配置项 | 环境变量 | 默认值 | 说明 |
|---|---|---|---|
| `db.url` / `spring.datasource.url` | `G8S_URL` | 由 host/port 拼装 | 完整 JDBC URL |
| `db.host` / `db.port` / `db.name` | `G8S_HOST`/`G8S_PORT`/`G8S_DB` | `127.0.0.1`/`9088`/`sysmaster` | 未给 URL 时拼装用 |
| `db.server` | `G8S_SERVER` | 空 | 拼装时附加 `:GBASEDBTSERVER=` |
| `db.user` / `spring.datasource.username` | `G8S_USER` | `gbasedbt` | 用户名 |
| `db.password` / `spring.datasource.password` | `G8S_PASSWORD` | 空 | 密码 |
| `scrape.interval.fast` | `G8S_FAST_INTERVAL` | `10` | 高频指标间隔（秒） |
| `scrape.interval.normal` | `G8S_NORMAL_INTERVAL` | `60` | 中频指标间隔（秒），兼容旧键 `scrape.interval` |
| `scrape.interval.slow` | `G8S_SLOW_INTERVAL` | `300` | 低频指标间隔（秒） |
| `http.port` | `G8S_HTTP_PORT` | `9090` | 抓取端口 |

## 指标（按 6 类监控组织）

## 指标（按监控大盘规格命名，分三档采集）

> fast=10s / normal=60s / slow=300s。`gbase8s_profile{stat}` 为累计值需 `rate()`；
> QPS/TPS/CPU/IO 等已由 exporter 后台直接算好速率，大盘直接用。

### fast 档（高频，8 次查询）
| 指标 | 说明 |
|---|---|
| `gbase8s_up` / `gbase8s_query_up` | 实例存活 / 最近查询是否成功 |
| `gbase8s_connections` | 当前连接数（= `gbase8s_sessions` 兼容别名） |
| `gbase8s_connections_max` | 最大连接数（= `gbase8s_max_connections`） |
| `gbase8s_connections_usage` | 连接使用率（= `gbase8s_connections_used_ratio`） |
| `gbase8s_qps` | 每秒读写删改操作数（isreads/iswrites/isrewrites/isdeletes 增量） |
| `gbase8s_tps` | 每秒事务数（iscommits/isrollbacks 增量） |
| `gbase8s_lock_waits` | 当前锁等待数（syslcktab.wtlist） |
| `gbase8s_lock_wait_time` | 当前最长锁等待（秒，sysrstcb.lkwaittime） |
| `gbase8s_deadlocks` | 死锁累计（sysprofile.deadlks） |
| `gbase8s_cpu_usage` | 数据库 CPU 利用率（0..1，VP CPU 速率 / VP 数） |
| `gbase8s_io_latency` | 综合 IO 延迟（秒，读写延迟取较大值） |
| `gbase8s_io_utilization` | IO 利用率（0..1，chunk IO 时间占比） |
| `gbase8s_vp_count` / `gbase8s_vp_cpu_seconds_total{class}` | 虚拟处理器数与 CPU（单位秒） |
| `gbase8s_locks` / `gbase8s_chunk_reads_total` / `gbase8s_chunk_writes_total` 等 | 锁数量、磁盘 IO 累计（IOPS 用 `rate()`） |
| `gbase8s_uptime_seconds` / `gbase8s_info{version}` / `gbase8s_last_scrape_error` / `gbase8s_scrape_duration_seconds` | 运行时长/版本/采集健康 |
| `gbase8s_profile{stat}` | sysprofile 白名单累计计数（`isreads`/`iswrites`/`isrewrites`/`isdeletes`/`iscommits`/`isrollbacks`/`ovtrans`/`lockreqs`/`lockwts`/`deadlks`/`lktouts`/`ovlock`/`bufreads`/`bufwrites`/`latchwts`/`ckptwts`/`numckpts`/`disksorts`/`num_ready`/`num_cpu_ready`） |

### normal 档（中频，9 次查询）
| 指标 | 说明 |
|---|---|
| `gbase8s_active_transactions` / `gbase8s_long_transactions` | 活跃/长事务数（systxptab） |
| `gbase8s_databases` | 数据库总数 |
| `gbase8s_dbspace_size_bytes{dbspace}` / `gbase8s_dbspace_free_bytes{dbspace}` | 表空间总/空闲空间 |
| `gbase8s_disk_usage{dbspace}` | 表空间使用率（0..1，= 1 - free/size） |
| `gbase8s_logical_log_pages_total/used` / `gbase8s_physical_log_pages_total/used` | 逻辑/物理日志空间（页） |
| `gbase8s_bufferpool_size_bytes` / `gbase8s_bufferpool_bufwaits_total` / `gbase8s_bufferpool_hit_ratio` | 缓冲池大小/等待/命中率 |
| `gbase8s_network_receive_bytes_total` / `gbase8s_network_send_bytes_total` | 网络收发累计（速率用 `rate()`） |
| `gbase8s_ha_type` / `gbase8s_ha_info{role}` | 主备/集群状态（sysha_type，0=无复制） |

### slow 档（低频，数据库对象统计）
| 指标 | 说明 |
|---|---|
| `gbase8s_tables{db}` | 各库用户表数（每 5 分钟一次，逐库切换查询） |

### 无法实现（受 GBase 8s 限制，采集不到）

| 大盘期望指标 | 无法实现原因 |
|---|---|
| 查询延迟 P50/P95/P99（`gbase8s_query_latency*`） | GBase 8s 无全局查询延迟统计，需启用 `SQLTRACE` 后由 trace 数据计算；当前 trace 未启用 |
| 慢查询统计 / Top SQL / SQL 统计 | 同上，需 DBA 在 `onconfig` 启用 SQLTRACE（`syssqltrace_info.sqlseen` 当前为 null） |
| 复制状态 / 复制延迟 | `sysha_lagtime` 仅在 HDR/RSS 复制启用时有意义；本次实测 `sysha_type=0`（未启用复制） |
| 连接错误/中止计数 | sysmaster 无对应计数器 |
| 锁等待明细/等待时长分布 | `syslocks` 虚拟表在锁竞争场景下查询会长时间阻塞（实测卡至超时），仅能提供锁数量（syslcktab）与最长等待（sysrstcb） |
| 实例共享内存总使用率 | `sysshmem` 查询报"不支持编码或代码集"，无可靠来源；可用缓冲池近似 |
| 引擎内部指标（InnoDB 风格行操作/页明细） | GBase 8s 无 InnoDB 引擎，缓冲池/日志/IO 已有对应替代 |

> ⚠️ 逻辑日志告警提示：本次实测 `gbase8s_logical_log_pages_used/total ≈ 97.8%`，
> 逻辑日志写满会阻塞数据库写入，请优先处理日志备份。

## 已知限制与设计说明

- GBase 8s 不支持 Informix 风格跨库语法（`sysmaster:table`），采集器通过 `DATABASE sysmaster` 语句切换系统监控库查询指标。
- `sysmaster:syslocks` 虚拟表在服务器锁竞争/长事务场景下查询会长时间阻塞（实测 `SELECT COUNT(*)` 与 `SELECT FIRST 5` 均卡住直至超时），因此**实时锁数量从 `syslcktab` 读取（独立 5s 超时保护）**，锁类累计指标（lockreqs/lockwts/deadlks 等）从 `sysprofile` 读取。
- 采集连接自动去除 URL 中的 `sqlmode=oracle` 参数：实测 oracle 兼容模式下部分系统表查询会卡住；去除后连接语义与登录信息不变。
- 所有指标查询带 15 秒超时（`setQueryTimeout`，锁表查询 5 秒），单项失败记为 -1（表/库统计）或跳过，不影响 `gbase8s_up`；连接失败时 `gbase8s_up=0` 且清空全部指标。

## Prometheus 抓取配置

```yaml
scrape_configs:
  - job_name: gbase8s
    static_configs:
      - targets: ['<exporter-host>:9090']
```

## 告警规则与 Grafana 看板

仓库内置开箱即用的告警与看板文件：

| 文件 | 说明 |
|---|---|
| `prometheus/gbase8s_alerts.yml` | 15 条告警，按 6 类组织：**可用性**（宕机/采集错误）、**连接**（使用率 >80%/95%）、**性能**（命中率<90%、VP CPU>80%、QPS 骤降）、**资源**（IO 延迟高）、**锁/事务**（锁>5000、死锁、**长事务 critical**）、**存储**（表空间 85%/95%、逻辑日志 85% critical、物理日志 85%） |
| `grafana/gbase8s_dashboard.json` | 33 面板（含 6 个分组行）**6 大盘**：①总览（状态/连接/QPS/TPS/CPU/IO/版本）②性能（QPS/TPS/SQL 明细/命中率）③资源（CPU/IOPS/IO 延迟/IO 利用率/网络/缓冲池）④事务与锁（活跃/长事务、锁/锁等待/死锁）⑤存储（表空间/逻辑日志/物理日志/各库表数）⑥高可用（主备状态/Primary/Secondary/运行时长） |

使用方式：

```yaml
# Prometheus（prometheus.yml 中追加）
rule_files:
  - /etc/prometheus/gbase8s_alerts.yml

scrape_configs:
  - job_name: gbase8s
    static_configs:
      - targets: ['<exporter-host>:19090']
```

```bash
# Grafana：导入 grafana/gbase8s_dashboard.json（Dashboards → Import → Upload JSON），
# 数据源选择你的 Prometheus，dbspace 变量会自动下拉。
```

> ⚠️ 告警阈值基于本次实测环境设定（连接 300/锁 5000 等），请按业务规模调整；
> `GBase8sPhysicalLogUsageHigh` 的物理日志总容量按实际 `onconfig.PHYSFILE` 调整分母。

## 说明

- 指标查询走 `sysmaster` 系统监控库（`syssessions`/`sysdatabases`/`sysprofile`/`sysshmvals`/`syslcktab`/`sysrstcb`/`systxptab`/`sysdbstab`/`syschktab_fast`/`sysbufpool`/`syslogfil`/`sysplog`/`sysnetworkio`/`sysha_type`/`sysvplst`），需要连接账号具备相应权限；某项查询无权限时该项为 `-1`。
- 三档采集各自独立线程与独立连接，fast 档失败反映在 `gbase8s_up`/`gbase8s_query_up`；normal/slow 档失败仅记录日志，不影响可用性指标。
- 数据库标识符与 URL 参数（如 `DB_LOCALE=zh_CN.utf8`）在连接属性中自动附带，连接建立即符合中文环境。
