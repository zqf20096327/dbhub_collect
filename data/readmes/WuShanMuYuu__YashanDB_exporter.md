# YashanDB Exporter

[![Go Version](https://img.shields.io/badge/go-%3E%3D1.18-blue)](https://golang.org/)
[![License](https://img.shields.io/badge/license-Apache%202.0-green)](LICENSE)

一款专为 [YashanDB](https://www.yashandb.com/) 打造的 Prometheus 监控导出工具，提供全面的数据库监控指标采集能力。

YashanDB 是深圳崖山科技有限公司研发的一款国产数据库管理系统，具有 Oracle 兼容特性。本 Exporter 针对 YashanDB 的系统视图进行了深度适配和优化。

## 功能特性

- **单目标/多目标监控** - 支持单实例和多实例监控模式
- **SQL 指纹分析** - 支持 SQL 语句归一化，便于分析慢查询模式
- **Web UI 管理** - 内置 Web 界面，支持配置在线编辑和 SQL 指纹查看
- **标准化指标** - 内置 DBA 标准监控指标配置，开箱即用
- **Prometheus 集成** - 完美兼容 Prometheus 生态

## 监控指标概览

### 一、实例状态监控
| 指标名称 | 类型 | 说明 |
|---------|------|------|
| `yashandb_up` | Gauge | 数据库是否在线 (1=在线, 0=离线) |
| `yashandb_database_value` | Gauge | 数据库基本信息（名称、日志模式、打开模式等） |
| `yashandb_instance_value` | Gauge | 实例状态信息（实例名、主机名、版本等） |

### 二、会话与进程监控
| 指标名称 | 类型 | 说明 |
|---------|------|------|
| `yashandb_session_count_count` | Gauge | 按状态和类型统计的会话数量 |
| `yashandb_session_user_count` | Gauge | 按用户名统计的连接数 |
| `yashandb_process_count` | Gauge | 进程总数 |
| `yashandb_active_session_count` | Gauge | 活跃会话数（按用户名和等待分类统计） |

### 三、SQL 性能监控
| 指标名称 | 类型 | 说明 |
|---------|------|------|
| `yashandb_slow_sql_*` | Gauge/Counter | 慢 SQL 监控（执行时间 > 1秒），支持 SQL 指纹 |
| `yashandb_high_freq_sql_*` | Gauge/Counter | 高频 SQL 监控（执行次数 > 100） |
| `yashandb_sql_count_count` | Gauge | SQL 缓存区语句数量 |

### 四、系统资源统计
| 指标名称 | 类型 | 说明 |
|---------|------|------|
| `yashandb_sysstat_commits` | Counter | 事务提交次数 |
| `yashandb_sysstat_rollbacks` | Counter | 事务回滚次数 |
| `yashandb_sysstat_disk_reads` | Counter | 磁盘读取次数 |
| `yashandb_sysstat_disk_writes` | Counter | 磁盘写入次数 |
| `yashandb_sysstat_disk_read_time` | Counter | 磁盘读取时间 |
| `yashandb_sysstat_disk_write_time` | Counter | 磁盘写入时间 |

### 五、存储监控
| 指标名称 | 类型 | 说明 |
|---------|------|------|
| `yashandb_tablespace_info_count` | Gauge | 表空间信息（名称、类型、状态） |
| `yashandb_datafile_count_count` | Gauge | 数据文件数量 |
| `yashandb_datafile_count_total_mb` | Gauge | 数据文件总大小（MB） |

### 六、锁与等待事件
| 指标名称 | 类型 | 说明 |
|---------|------|------|
| `yashandb_lock_count` | Gauge | 锁统计（按锁模式和请求类型） |
| `yashandb_lock_wait_count` | Gauge | 锁等待数量 |
| `yashandb_session_wait_count` | Gauge | 会话等待事件统计 |

## 安装与构建

### 前置依赖

1. **YashanDB C 驱动** - Go 驱动依赖 C 驱动库 `libyascli.so`

```bash
# 检查 C 驱动是否安装
ls ~/.yashandb/client/lib/libyascli.so

# 如未安装，请参考 YashanDB 官方文档安装 C 驱动
```

2. **Go 环境** - 需要 Go 1.18 或更高版本

### 从源码构建

```bash
# 克隆仓库
git clone https://gitee.com/junluoyu/yashan-db_exporter.git
cd yashan-db_exporter

# 设置 CGO 环境变量（指向 C 驱动库）
export CGO_CFLAGS="-I$HOME/.yashandb/client/include"
export CGO_LDFLAGS="-L$HOME/.yashandb/client/lib -lyascli"
export LD_LIBRARY_PATH=$HOME/.yashandb/client/lib:$LD_LIBRARY_PATH

# 构建
make build
# 或
go build -o yashandb_exporter .

# 验证编译结果
./yashandb_exporter --version
```

### Docker 构建

```bash
# 构建镜像
docker build -t yashandb-exporter:latest .

# 运行容器
docker run -d \
  -p 9166:9166 \
  -e DATA_SOURCE_NAME="sys/password@yashandb-host:1688" \
  yashandb-exporter:latest
```

## 使用方法

### 1. 配置数据库连接

设置环境变量指定数据库连接信息：

```bash
export DATA_SOURCE_NAME="sys/password@yashandb-host:1688"
```

DSN 格式：`用户名/密码@主机:端口`

示例：
```bash
# 本地连接
export DATA_SOURCE_NAME="sys/yashan123@localhost:1688"

# 远程连接
export DATA_SOURCE_NAME="sys/mypassword@192.168.1.100:1688"
```

### 2. 启动 Exporter

```bash
# 使用默认配置启动
./yashandb_exporter

# 指定端口和配置文件
./yashandb_exporter \
  --web.listen-address=:9166 \
  --default.metrics=./default-metrics.toml

# 启用多目标监控模式
export ENABLE_MULTI_TARGET=true
./yashandb_exporter
```

### 3. 验证运行状态

```bash
# 查看指标
curl http://localhost:9166/metrics

# 访问 Web UI
# http://localhost:9166/ui/
```

## 配置文件说明

### default-metrics.toml

默认监控指标配置文件，包含 8 大类、15 个指标组的监控配置：

| 分类 | 指标组 | 说明 |
|------|--------|------|
| 实例状态 | up, database, instance | 数据库在线状态、基本信息、实例状态 |
| 会话进程 | session_count, session_user, process, active_session | 会话统计、用户连接、进程数、活跃会话 |
| SQL 监控 | slow_sql, high_freq_sql, sql_count | 慢 SQL、高频 SQL、SQL 缓存数量 |
| 系统资源 | sysstat | 提交/回滚次数、磁盘读写统计 |
| 表空间 | tablespace_info | 表空间信息和状态 |
| 数据文件 | datafile_count | 数据文件数量和总大小 |
| 锁监控 | lock, lock_wait | 锁统计和锁等待 |
| 等待事件 | session_wait | 会话等待事件统计 |

### 慢 SQL 监控配置

```toml
[[metric]]
context = "slow_sql"
labels = [ "sql_id" ]
metricsdesc = { 
    elapsed_sec = "执行时间(秒)", 
    cpu_sec = "CPU时间(秒)", 
    executions = "执行次数", 
    buffer_gets = "逻辑读", 
    disk_reads = "物理读", 
    rows_processed = "处理行数" 
}
metricstype = { 
    elapsed_sec = "gauge", 
    cpu_sec = "gauge", 
    executions = "counter", 
    buffer_gets = "counter", 
    disk_reads = "counter", 
    rows_processed = "counter" 
}
sql_fingerprint = true
request = "SELECT sql_id, ROUND(elapsed_time / 1000000, 2) as elapsed_sec, ROUND(cpu_time / 1000000, 2) as cpu_sec, executions, buffer_gets, disk_reads, rows_processed FROM v$sql WHERE elapsed_time / 1000000 > 1 AND executions > 0 ORDER BY elapsed_time DESC FETCH FIRST 20 ROWS ONLY"
ignorezeroresult = true
```

### 自定义指标

可创建自定义指标文件（TOML 或 YAML 格式）：

```toml
[[metric]]
context = "my_custom_metric"
labels = [ "label1", "label2" ]
metricsdesc = { value = "描述信息" }
request = "SELECT col1 as label1, col2 as label2, col3 as value FROM my_table"
```

加载自定义指标：
```bash
./yashandb_exporter --custom.metrics /path/to/custom-metrics.toml
```

## 多目标监控模式

启用多目标模式，支持同时监控多个 YashanDB 实例：

```bash
# 启用多目标模式
export ENABLE_MULTI_TARGET=true

# 配置目标文件 targets.json
```

`targets.json` 示例：
```json
[
  {
    "name": "yashandb-prod-01",
    "dsn": "sys/password@192.168.1.10:1688",
    "labels": {
      "env": "production",
      "datacenter": "dc1"
    },
    "enabled": true
  },
  {
    "name": "yashandb-prod-02",
    "dsn": "sys/password@192.168.1.11:1688",
    "labels": {
      "env": "production", 
      "datacenter": "dc2"
    },
    "enabled": true
  }
]
```

多目标模式下访问：
```bash
# 查询特定目标
curl http://localhost:9166/metrics?target=yashandb-prod-01
```

## Web UI 功能

Exporter 内置 Web UI 管理界面，默认地址：`http://localhost:9166/ui/`

功能包括：
- **指标浏览** - 实时查看采集的数据库指标
- **配置编辑** - 在线编辑 `default-metrics.toml` 配置文件
- **SQL 指纹** - 查看归一化后的 SQL 指纹统计
- **目标管理**（多目标模式）- 管理监控目标

## 系统服务配置

使用 systemd 管理 Exporter 服务：

```bash
# 复制服务文件
sudo cp systemd-example/yashandb_exporter.service /etc/systemd/system/

# 编辑配置
sudo systemctl edit yashandb_exporter
```

编辑内容示例：
```ini
[Service]
Environment="DATA_SOURCE_NAME=sys/password@localhost:1688"
Environment="LD_LIBRARY_PATH=/root/.yashandb/client/lib"
ExecStart=/usr/local/bin/yashandb_exporter \
  --default.metrics=/etc/yashandb_exporter/default-metrics.toml \
  --web.listen-address=:9166
```

启动服务：
```bash
sudo systemctl daemon-reload
sudo systemctl enable yashandb_exporter
sudo systemctl start yashandb_exporter
```

## 监控用户权限配置

建议使用具有适当权限的数据库用户进行监控。最小权限要求：

```sql
-- 创建监控用户（可选，也可使用 sys 用户）
-- 授予必要的系统视图查询权限
GRANT SELECT ON v_$session TO monitor_user;
GRANT SELECT ON v_$process TO monitor_user;
GRANT SELECT ON v_$sysstat TO monitor_user;
GRANT SELECT ON v_$database TO monitor_user;
GRANT SELECT ON v_$instance TO monitor_user;
GRANT SELECT ON v_$sql TO monitor_user;
GRANT SELECT ON v_$tablespace TO monitor_user;
GRANT SELECT ON v_$datafile TO monitor_user;
GRANT SELECT ON v_$lock TO monitor_user;
```

## Prometheus 配置示例

在 `prometheus.yml` 中添加 scrape 配置：

```yaml
scrape_configs:
  - job_name: 'yashandb'
    static_configs:
      - targets: ['localhost:9166']
        labels:
          instance: 'yashandb-prod-01'
          
  # 多目标模式配置
  - job_name: 'yashandb-multi'
    static_configs:
      - targets: ['localhost:9166']
    params:
      target: ['yashandb-prod-01']
```

## 常用 PromQL 查询示例

```promql
# 数据库在线状态
yashandb_up

# 活跃会话数
sum(yashandb_session_count_count{status="ACTIVE"})

# 总会话数
sum(yashandb_session_count_count)

# 用户连接数排行
topk(5, yashandb_session_user_count)

# 慢 SQL 平均执行时间
avg(yashandb_slow_sql_elapsed_sec) by (sql_id)

# 磁盘读速率（每秒）
rate(yashandb_sysstat_disk_reads[5m])

# 事务提交速率
rate(yashandb_sysstat_commits[5m])

# 锁等待数量
yashandb_lock_wait_count

# 数据文件总大小
yashandb_datafile_count_total_mb
```

## 故障排查

### 连接失败

```
error pinging yashandb: YAS-02143 invalid username/password
```
- 检查 DSN 格式和凭据
- 确认用户未被锁定

```
error while loading shared libraries: libyascli.so.0
```
- 检查 C 驱动是否安装
- 设置 `LD_LIBRARY_PATH` 环境变量

### 指标采集失败

查看 Exporter 日志确认具体错误：
```bash
./yashandb_exporter --log.level=debug
```

常见原因：
- 监控用户权限不足
- SQL 语句与 YashanDB 版本不兼容
- 系统视图不存在

## 项目结构

```
yashan-db_exporter/
├── main.go                    # 主程序入口
├── go.mod / go.sum           # Go 依赖管理
├── default-metrics.toml      # 默认监控指标配置
├── start.sh                  # 启动脚本
├── Makefile                  # 构建脚本
├── Dockerfile                # Docker 构建
├── collector/                # 采集器模块
│   ├── collector.go          # 核心采集逻辑
│   ├── multi_target.go       # 多目标支持
│   ├── default_metrics.go    # 默认指标加载
│   └── sql_normalizer.go     # SQL 指纹归一化
├── webui/                    # Web UI 模块
│   ├── handler.go            # Web 处理器
│   └── static/index.html     # 前端页面
├── custom-metrics-example/   # 自定义指标示例
└── systemd-example/          # 系统服务配置示例
```

## 技术栈

- **Go 1.18+** - 主要开发语言
- **YashanDB Go Driver** - 数据库连接驱动
- **Prometheus Client** - 指标导出库
- **Gorilla Mux** - HTTP 路由

## 开源协议

Apache License 2.0

## 致谢

本项目架构参考了 [Oracle DB Exporter](https://github.com/iamseth/oracledb_exporter)，针对 YashanDB 进行了深度适配。

---

**注意**：本项目为 YashanDB 专版 Exporter，与 Oracle/MySQL Exporter 在指标命名和 SQL 语法上存在差异，请根据实际情况调整监控配置。
