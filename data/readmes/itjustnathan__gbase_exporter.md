# GBase Exporter

GBase Exporter 是专为南大通用数据库（**GBase 8a MPP 集群** 与 **GBase 8s 事务型数据库**）设计的统一 Prometheus 监控指标采集器。

参考并借鉴了 `mysqld_exporter` 的生产级架构风格与设计理念，编译出的**统一二进制可执行文件名为 `gbase_exporter`**，内部具备数据库引擎全自动探测能力，无需针对 8a 和 8s 维护不同的采集器程序。

---

## 核心特性

- **内部自动确认 8a / 8s**：
  - 采集器启动后，内部通过轻量级数据库版本指纹探测器（`SELECT @@version, @@version_comment`）自动判断后端内核是 **GBase 8a** 还是 **GBase 8s**。
  - **GBase 8a 场景**：自动采集分布式集群与分片同步指标（`gclusterdb` 系统库），8s 专有采集器自动静默跳过。
  - **GBase 8s 场景**：自动激活 8s 专有高可用（HDR/SDS/RSS）、DBSpace 存储与 Chunk 状态采集（`sysmaster` 系统库），自动跳过 8a 分布式元数据视图，彻底杜绝 SQL 语法不兼容报错。
- **保留人工控制权**：采集器默认启用自适应采集，同时支持通过 `--collector.gbase8s` 与 `--no-collector.gbase8s` 进行人为显式开关控制。
- **全静态单文件二进制**：采用 `CGO_ENABLED=0` 静态链接编译，绝无外部动态链接库依赖（不依赖任何本地 `libgci`、`libclntsh` 安装路径或 `LD_LIBRARY_PATH`）。
- **现代 Prometheus 生态规范**：
  - 集成 `prometheus/common/version`，支持 `--version` 输出详细构建元数据。
  - 集成 `prometheus/exporter-toolkit/web`，原生支持 IPv4 / IPv6（如 `[::]:9115`）双栈监听及 TLS。
  - 采用 INI 格式配置文件（`--config.file=gbase.conf`），支持指定连接池参数与连接超时。

---

## 编译与分发

### 统一构建脚本 (`build.sh`)
通过项目根目录下的 `build.sh` 可一键完成静态编译：
```bash
chmod +x build.sh
./build.sh
```

编译产物位于 `build/` 目录：
- `build/gbase_exporter`: 默认 Linux 架构可执行二进制
- `build/gbase_exporter_linux_amd64`: Linux x86_64 静态独立二进制
- `build/gbase_exporter_linux_arm64`: Linux aarch64 静态独立二进制

---

## 配置文件说明 (`gbase.conf`)

采集器支持通过 `--config.file` 指定连接参数，配置文件采用标准 INI 格式：

```ini
[client]
# engine 默认为 auto (自动探测 8a 或 8s)，亦可显式指定为 8a 或 8s
engine = auto
host = 127.0.0.1
port = 5258
user = monitor_user
password = monitor_pwd
database = gclusterdb
timeout = 10s
# 可选；默认值如下。程序启动时读取一次，不会在每次抓取时重复读取。
license_key_path = /opt/GBase/Server/bin/license.key
```

---

## 启动与运行选项

```bash
# 查看使用帮助
./gbase_exporter --help

# 查看版本信息
./gbase_exporter --version

# 使用配置文件启动并监听 IPv6/IPv4 端口（默认内部自动确认 8a / 8s 并全自动采集）
./gbase_exporter --config.file=gbase.conf --web.listen-address="[::]:9115"

# 人为显式关闭 8s 采集器
./gbase_exporter --no-collector.gbase8s
```

---

## HTTP 请求安全认证 (authMiddleware)

对标 `mysqld_exporter` 项目中的安全鉴权机制，`gbase_exporter` 提供了 `authMiddleware` 鉴权中间件保护。通过启动参数 `--scrape.enable-auth` 控制是否启用（默认关闭 `false`）。启用后将对 `/` 根路径与 `/metrics` 监控采集路径进行签名认证。

### 1. 认证机制
客户端（或 Prometheus 抓取端）发起请求时必须携带以下 URL Query 参数：
- `timestamp`: 当前请求的 Unix 时间戳字符串（例如 `1726700000`）。
- `token`: 基于密钥与时间戳生成的 SHA-256 动态签名摘要（截取前 16 位十六进制字符）。

### 2. Token 生成算法
```text
key = "prometheus"
secret = key + timestamp
hash = sha256(secret)
token = hex(hash)[0:16]
```

### 3. 请求示例
- **通过 curl 请求指标**：
  ```bash
  TS=$(date +%s)
  TOKEN=$(echo -n "prometheus${TS}" | sha256sum | cut -c 1-16)
  curl "http://127.0.0.1:9115/metrics?timestamp=${TS}&token=${TOKEN}"
  ```
- **Prometheus `scrape_configs` 配置示例**：
  ```yaml
  scrape_configs:
    - job_name: "gbase_exporter"
      metrics_path: "/metrics"
      params:
        timestamp: ["1726700000"]
        token: ["7a6568f590dab55c"]
      static_configs:
        - targets: ["11.1.1.11:9115"]
  ```

---

## 监控指标清单与说明

### 1. 引擎自适应与采集器状态

| 指标名称 | 类型 | 说明与标签 |
| :--- | :--- | :--- |
| `gbase_up` | Gauge | 当前被监控数据库节点实例存活状态（1=正常可用，0=连接断开/异常） |
| `gbase_database_engine_info` | Gauge | 自动识别的目标数据库内核信息，包含标签 `engine`（"8a"/"8s"）、`product`（"gbase8a"/"gbase8s"）、`version`、`version_comment` |
| `gbase_scrape_collector_success` | Gauge | 各子采集模块执行状态（1=成功，0=失败），标签：`collector` |
| `gbase_scrape_collector_duration_seconds` | Gauge | 各子采集模块抓取耗时（秒），标签：`collector` |
| `gbase_license_remaining_days` | Gauge | GBase License 剩余自然日，标签：`start_time`、`end_time`。`-2` 表示未配置、文件不存在、不可读或无法解析；`-1` 表示已过期；`0` 表示当天到期；正整数表示剩余天数。数据在程序启动时从 `license_key_path` 读取并保存在内存中。 |

### 2. 集群/节点健康类指标 (`--collector.cluster`)
| 指标名称 (Metric Name) | 类型 | 标签 (Labels) | 含义说明 | 数据来源 |
| :--- | :--- | :--- | :--- | :--- |
| `gbase_cluster_node_online` | Gauge | `node_ip`, `role` | 8a 集群节点在线状态 (1=在线, 0=离线) | `gclusterdb.cluster_nodes` |
| `gbase_cluster_node_sync_status` | Gauge | `node_ip` | 8a 节点数据副本同步状态 (1=已同步, 0=未同步) | `gclusterdb.cluster_nodes` |
| `gbase_cluster_segment_pending_sync` | Gauge | - | 当前集群待同步/不同步的分片副本总数 | `gclusterdb.cluster_nodes` |
| `gbase_cluster_service_alive` | Gauge | `service_name` | 集群核心守护进程存活状态 (1=存活, 0=异常) | 进程与端口可用性探测 |
| `gbase_cluster_node_data_size_gb` | Gauge | `node_ip` | 各数据节点所存储的数据总量 (GB) | `gbase.table_distribution` 聚合 |
| `gbase_cluster_nodes_total` | Gauge | `role` | 按角色统计的集群总节点数 (coordinator/data) | `gclusterdb.cluster_nodes` |
| `gbase_cluster_inter_node_communication_status` | Gauge | - | 节点间内部通信与心跳状态 (1=正常, 0=异常) | 内部网络与通信错误探测 |

---

### 3. 主机与引擎资源类指标 (`--collector.resources`)
| 指标名称 (Metric Name) | 类型 | 标签 (Labels) | 含义说明 | 数据来源 |
| :--- | :--- | :--- | :--- | :--- |
| `gbase_resources_cpu_usage_ratio` | Gauge | - | 系统整体 CPU 使用率 (0.0 ~ 1.0) | 系统状态 / `/proc/stat` |
| `gbase_resources_memory_usage_ratio` | Gauge | - | 系统物理内存使用率 (0.0 ~ 1.0) | 系统内存 / `/proc/meminfo` |
| `gbase_resources_load1` | Gauge | - | 系统 1 分钟平均负载 Load | 系统运行队列 |
| `gbase_resources_load5` | Gauge | - | 系统 5 分钟平均负载 Load | 系统运行队列 |
| `gbase_resources_load15` | Gauge | - | 系统 15 分钟平均负载 Load | 系统运行队列 |
| `gbase_resources_disk_usage_ratio` | Gauge | `mount_point` | 数据目录所在磁盘使用率 (0.0 ~ 1.0) | `Statfs` 磁盘文件系统 |
| `gbase_resources_disk_iowait_ratio` | Gauge | - | 磁盘 I/O 等待比率 (0.0 ~ 1.0) | `/proc/diskstats` 等待时间 |
| `gbase_resources_network_receive_bytes_total` | Counter | - | 网络接收总流量 (字节) | `Bytes_received` / 网卡状态 |
| `gbase_resources_network_transmit_bytes_total` | Counter | - | 网络发送总流量 (字节) | `Bytes_sent` / 网卡状态 |
| `gbase_resources_network_packets_dropped_total` | Counter | `direction` (rx/tx) | 网络接口丢包累计次数 | 系统网络接口计数 |
| `gbase_resources_network_retransmitted_segments_total` | Counter | - | TCP 协议段重传累计次数 | `/proc/net/snmp` |

---

### 4. 数据库运行与并发类指标 (`--collector.activity`)
| 指标名称 (Metric Name) | 类型 | 标签 (Labels) | 含义说明 | 数据来源 |
| :--- | :--- | :--- | :--- | :--- |
| `gbase_activity_connections_current` | Gauge | - | 当前客户端总连接会话数 | `information_schema.processlist` |
| `gbase_activity_active_queries` | Gauge | - | 正在执行 SQL 的活跃会话数 (排除休眠连接) | `processlist` 过滤 Command |
| `gbase_activity_slow_queries_total` | Counter | - | 数据库慢查询累计发生总次数 | `GLOBAL STATUS: Slow_queries` |
| `gbase_activity_failed_queries_total` | Counter | - | 执行失败/异常退出的 SQL 计数 | `Aborted_clients` 状态累积 |
| `gbase_activity_loader_job_state` | Gauge | `job_id`, `state` | 数据批量加载/导入任务运行状态 | `gclusterdb.cluster_loader_status` |
| `gbase_activity_lock_waits` | Gauge | - | 当前数据库锁等待与任务堆积数 | `Table_locks_waited` / 锁视图 |

---

### 5. 存储与容量空间类指标 (`--collector.storage`)
| 指标名称 (Metric Name) | 类型 | 标签 (Labels) | 含义说明 | 数据来源 |
| :--- | :--- | :--- | :--- | :--- |
| `gbase_storage_table_data_bytes` | Gauge | `schema_name`, `table_name` | 表数据所占用的存储容量 (字节) | `information_schema.tables` |
| `gbase_storage_table_index_bytes` | Gauge | `schema_name`, `table_name` | 表索引所占用的存储容量 (字节) | `information_schema.tables` |
| `gbase_storage_table_rows` | Gauge | `schema_name`, `table_name` | 表中记录估算总行数 | `information_schema.tables` |
| `gbase_storage_node_data_skewness_ratio` | Gauge | - | 集群数据倾斜系数 (最大节点容量 / 平均容量比) | `table_distribution` 计算 |
| `gbase_storage_directory_usage_bytes` | Gauge | `dir_type` (temp/log) | 临时目录与日志目录磁盘空间占用 (字节) | 存储空间统计 |
| `gbase_storage_backup_space_remaining_bytes` | Gauge | - | 备份目录或备份介质剩余可用空间 (字节) | 备份存储池状态 |

---

### 6. 稳定性与事件类指标 (`--collector.stability`)
| 指标名称 (Metric Name) | 类型 | 标签 (Labels) | 含义说明 | 数据来源 |
| :--- | :--- | :--- | :--- | :--- |
| `gbase_stability_uptime_seconds` | Counter | - | 数据库实例自上次启动以来的运行时长 (秒) | `GLOBAL STATUS: Uptime` |
| `gbase_stability_last_restart_timestamp` | Gauge | - | 数据库最近一次启动的 Unix 时间戳 (秒) | 启动时间换算 |
| `gbase_stability_error_logs_total` | Counter | `log_level` (error/fatal) | 数据库错误/致命异常日志出现次数 | 日志状态监控 |
| `gbase_stability_failover_events_total` | Counter | - | 集群节点故障切换与主从恢复累计事件数 | 高可用切换事件审计 |
| `gbase_stability_alarm_flapping_status` | Gauge | - | 监控指标告警抖动状态 (1=持续抖动, 0=正常稳定) | 波动率窗口算法 |

---

### 7. GBase 8s 专有高可用与存储指标 (`--collector.gbase8s`)
| 指标名称 (Metric Name) | 类型 | 标签 (Labels) | 含义说明 | 数据来源 |
| :--- | :--- | :--- | :--- | :--- |
| `gbase_cluster_node_active` | Gauge | `engine`, `node_name` | GBase 8s HDR/SDS/RSS 集群节点活跃状态 (1=活跃, 0=异常) | `sysha_node` / 复制状态 |
| `gbase_cluster_node_role` | Gauge | `engine`, `node_name`, `role` | GBase 8s 节点集群角色 (primary/hdr/sds/rss) | 集群拓扑视图 |
| `gbase_replication_lag_seconds` | Gauge | `engine`, `channel` | 8s 主备同步复制延迟时长 (秒) | `sysha_node` 延迟比对 |
| `gbase_replication_state` | Gauge | `engine`, `channel`, `state` | 主从复制通道状态 (1=正常同步, 0=异常) | 高可用同步状态 |
| `gbase_sessions_total` | Gauge | `engine` | 8s 当前连接的总会话数 | `sysmaster:syssessions` |
| `gbase_active_sessions` | Gauge | `engine` | 8s 正在执行非挂起事务的活跃会话数 | `syssessions (is_asleep=0)` |
| `gbase_lock_waits_total` | Counter | `engine` | 自实例启动以来发生的锁等待累积次数 | `sysmaster:sysprofile (lockwts)` |
| `gbase_deadlocks_total` | Counter | `engine` | 自实例启动以来发生的死锁总次数 | `sysmaster:sysprofile (deadlks)` |
| `gbase_dbspace_pages_total` | Gauge | `engine`, `dbspace_name` | DBSpace 逻辑存储空间的总页数 | `sysmaster:sysdbspaces` |
| `gbase_dbspace_pages_free` | Gauge | `engine`, `dbspace_name` | DBSpace 逻辑存储空间的剩余空闲页数 | `sysmaster:syschunks` 聚合 |
| `gbase_chunk_offline` | Gauge | `engine`, `chunk_num`, `dbspace_name` | 物理数据文件 Chunk 离线状态 (1=离线故障, 0=在线正常) | `sysmaster:syschunks` |
| `gbase_instance_boot_timestamp_seconds` | Gauge | `engine` | 8s 实例启动时的 Unix 时间戳 | `sysmaster:sysprofile (boot_time)` |
| `gbase_isreads_total` | Counter | `engine` | 物理磁盘与缓存读操作总次数 | `sysmaster:sysprofile (isreads)` |
| `gbase_iswrites_total` | Counter | `engine` | 物理磁盘写操作总次数 | `sysmaster:sysprofile (iswrites)` |

---

## 告警规则配置

项目在 `rules/gbase_alerts.yml` 中提供了生产级 Prometheus Alertmanager 告警规则，覆盖采集器可用性、8a 集群节点健康、8s 专有高可用与 Chunk 状态、查询运行、资源水位、数据倾斜等 20 组关键监控告警规则。

在 Prometheus 配置文件中引入即可生效：
```yaml
rule_files:
  - "/path/to/gbase_exporter/rules/gbase_alerts.yml"
```
