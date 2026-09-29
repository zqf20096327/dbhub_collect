# chaos-ob

OceanBase 单机应急演练 / 混沌注入工具（Go）。不依赖 K8s / Chaos Mesh。

支持 **MySQL 租户** 与 **Oracle 租户**，用 `--duration` 控制每个场景持续时长。  
SQL 场景语句内带标记 `/* CHAOSOB:<场景名> emergency-drill */`，便于在会话、慢 SQL、审计里定位。

> 网络丢包/延迟（`tc netem`）暂未纳入。  
> 已在 **OceanBase 3.2.3** 与 **4.2.1.11** Oracle 租户上实机验证（见 `docs/TEST_REPORT.md`）。

### Oracle 事务 / 锁演练说明（3.x / 4.x 通用）

`database/sql` 的 `BeginTx` + `obconnector-go` 在部分版本上**经常无法真正挂起事务**（语句像自动提交），导致锁等待/死锁演练失效。  
当前实现统一为：

1. 独立 `sql.Conn`
2. 显式 `BEGIN`（并尝试 `SET AUTOCOMMIT=0`）
3. 关键用 `SELECT ... FOR UPDATE` 再 `UPDATE`

版本差异（均算演练成功）：

| 版本 | `deadlock` | `lock-wait` |
|------|------------|-------------|
| 3.2.3 | 常出 `mutual_block`；`ORA-00060` 不一定及时 | waiter 可长时间阻塞 |
| 4.2.x | 较易打出死锁中止信号 | waiter 常约 10s 后报 `ORA-30006`（等待超时），仍算锁等待成功 |

---

## 1. 编译

环境：Go 1.22+（开发机用过 1.25）。

```bash
cd chaos-ob

# 若 go proxy / sumdb 拉取 obconnector-go 失败，可临时：
export GOSUMDB=off
export GOPROXY=https://mirrors.aliyun.com/goproxy/,https://proxy.golang.org,direct

# 本机二进制
make build
# 或
go build -o bin/chaos-ob ./cmd/chaos-ob

# 交叉编译到 Linux x86_64（拷到 OB/OCP 机器）
make linux
# 或
GOOS=linux GOARCH=amd64 go build -o bin/chaos-ob-linux-amd64 ./cmd/chaos-ob
```

产物：

| 文件 | 说明 |
|------|------|
| `bin/chaos-ob` | 当前 OS 可执行文件 |
| `bin/chaos-ob-linux-amd64` | Linux 服务器用 |

依赖：

- MySQL 模式：`github.com/go-sql-driver/mysql`
- Oracle 模式：`github.com/helingjun/obconnector-go`（Oracle 租户握手）

---

## 2. 配置

```bash
cp config.example.yaml config.yaml
# 编辑连接信息
```

Oracle 示例（obclient）：

```bash
# 3.x
obclient -h172.16.104.28 -P2883 -uJAMES@oboracle#obv3 -p'***' -Ac
# 4.x
obclient -h172.16.104.23 -P2883 -uJAMES@sdq_oracle#obcluster -p'***'
```

```yaml
database:
  host: "172.16.104.23"
  port: 2883
  user: "JAMES@sdq_oracle#obcluster"
  password: "****"
  database: ""
  timeout_sec: 30
  mode: "oracle"          # oracle | mysql

defaults:
  duration: 60s
  concurrency: 8
  rows: 100000
  hold: 120s

host:
  clog_path: "/data/ob/clog"
  clog_reserve_gib: 1
  observer_process: "observer"
  io_path: "/data/ob/clog"   # io-stress 目录
```

密码也可用：`OB_PASSWORD`。未传 `-c` 且存在 `./config.yaml` 时自动加载。  
多环境可维护多份配置（如 `config.yaml` / `config.v4.yaml`），用 `-c` 或 `CFG=` 指定。

---

## 3. 一键安全回归（推荐）

排除：`clog-fill` / `coredump` / `kill-observer` / `standby-lag` / 网络。

```bash
cd /soft/chaos   # 或本仓库根目录
chmod +x scripts/run_safe_tests.sh

# 默认读 config.yaml；测 4.x 时：
CFG=config.v4.yaml ./scripts/run_safe_tests.sh

# 日志: test-safe-run.log  汇总: test-result.tsv
```

---

## 4. 命令速查

```bash
./bin/chaos-ob list
./bin/chaos-ob help
./bin/chaos-ob run <scenario> -c config.yaml --duration 10m [...]
```

| 参数 | 含义 |
|------|------|
| `-c` | 配置文件 |
| `--mode oracle\|mysql` | 租户模式 |
| `--duration` | 演练窗口（所有场景） |
| `--concurrency` | 并发 / 连接数 |
| `--rows` | large-tx 上限；slow-query-flood 灌数据量 |
| `--io-path` | io-stress 写目录 |
| `--kill-mode term\|kill` | kill-observer：优雅 / 强杀 |
| `--observer-pid` | 指定单个 observer PID（杀进程 / 冻副本） |
| `-H -P -u -p -D` | 覆盖连接 |

危险场景确认词：

```text
--allow-danger --confirm FILL      # clog-fill
--allow-danger --confirm COREDUMP  # coredump
--allow-danger --confirm KILL      # kill-observer
--allow-danger --confirm FREEZE    # standby-lag
```

---

## 5. 场景一览（考核方向）

### SQL / 会话类

| 场景 | 做什么 | 标记 / 考什么 |
|------|--------|----------------|
| `cpu-sql` | 高 CPU + 慢报表 | `CHAOSOB:cpu-sql` · 杀慢 SQL、限流 |
| `slow-query-flood` | 灌数后并发重 JOIN/扫表 | `CHAOSOB:slow-query-flood` · 慢 SQL、执行计划 |
| `large-tx` | 大事务 INSERT 不提交 | `CHAOSOB:large-tx` · 大事务/undo |
| `long-tx` | 长事务不提交（附带行锁） | `CHAOSOB:long-tx` · 长事务 |
| `lock-wait` | A 持锁 + B 持续等待 | `CHAOSOB:lock-wait` · 查锁、杀阻塞源 |
| `deadlock` | 订单↔库存交叉死锁 | `CHAOSOB:deadlock` · 死锁日志 |
| `conn-storm` | 大量会话挂住 | `CHAOSOB:conn-storm` · 连接打满、限流 |

### 主机 / 进程类（通常需与 OB 同机、root）

| 场景 | 做什么 | 考什么 |
|------|--------|--------|
| `cpu-burn` | 主机 CPU 忙等 | OS CPU、是否误判成 SQL |
| `io-stress` | 指定目录反复写+fsync | 慢盘、IO hang |
| `clog-fill` | 灌满 clog 盘 | 盘满告警与清理 |
| `coredump` | SIGABRT → core | core 收集、重启 |
| `kill-observer` | SIGTERM / SIGKILL | 进程消失与拉起 |
| `standby-lag` | SIGSTOP 冻结 observer | 副本延迟（多副本请用 `--observer-pid` 冻 follower） |

---

## 6. 演练示例

```bash
# 连接打满
./bin/chaos-ob run conn-storm -c config.yaml --duration 5m --concurrency 200

# 慢 SQL 洪水（先灌约 5000 行，可用 --rows 调整）
./bin/chaos-ob run slow-query-flood -c config.yaml --duration 10m --concurrency 16 --rows 8000

# 磁盘 IO
./bin/chaos-ob run io-stress --duration 5m --concurrency 8 --io-path /data/ob/clog

# 杀进程（优雅 / 强杀）
./bin/chaos-ob run kill-observer --duration 5m --kill-mode term --allow-danger --confirm KILL
./bin/chaos-ob run kill-observer --duration 5m --kill-mode kill --allow-danger --confirm KILL

# 冻副本（多副本时强烈建议指定 follower PID）
./bin/chaos-ob run standby-lag --duration 3m --observer-pid 12345 --allow-danger --confirm FREEZE

# 原有 SQL 场景
./bin/chaos-ob run cpu-sql   -c config.yaml --duration 15m --concurrency 16
./bin/chaos-ob run large-tx  -c config.yaml --duration 10m
./bin/chaos-ob run long-tx   -c config.yaml --duration 10m
./bin/chaos-ob run lock-wait -c config.yaml --duration 5m
./bin/chaos-ob run deadlock  -c config.yaml --duration 5m
```

演练表：`chaos_emg_customer` / `chaos_emg_order` / `chaos_emg_order_item` / `chaos_emg_inventory`。

---

## 7. long-tx vs lock-wait

| | `long-tx` | `lock-wait` |
|--|-----------|-------------|
| 目标 | 未提交事务挂很久 | 故意制造持续锁等待 |
| 现象 | 单会话 open transaction | A 持锁 + 多个 B 卡住 |
| 行锁 | 有（副作用） | 专项目标 |

---

## 8. 排查提示

```sql
SELECT * FROM GV$OB_PROCESSLIST WHERE INFO LIKE '%CHAOSOB%';
-- MySQL 模式也可用：SHOW FULL PROCESSLIST;
```

搜：`CHAOSOB:cpu-sql` / `slow-query-flood` / `large-tx` / `long-tx` / `lock-wait` / `deadlock` / `conn-storm`。

---

## 9. 注意

- **仅测试环境**。`clog-fill` / `coredump` / `kill-observer` / `standby-lag` 可能导致实例或副本异常。
- `standby-lag` 在单机 all-in-one 上意义有限；多副本请冻 **follower**，勿误冻唯一 leader 除非考切主。
- Oracle 租户必须 `mode: oracle`。
- Ctrl-C 会结束场景并尽量清理（如 io-stress 文件、standby-lag 的 SIGCONT）。

---

## 10. 目录结构

```text
chaos-ob/
├── cmd/chaos-ob/
├── internal/
│   ├── config/
│   ├── db/
│   ├── dialect/
│   ├── host/
│   └── scenario/
├── config.example.yaml
├── Makefile
└── README.md
```
