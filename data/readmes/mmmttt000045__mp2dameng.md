# 达梦 DMDSC 两节点多写集群 — 自动化部署与测评

多写数据库综述测评项目的达梦部分：在一组 Linux 服务器上全自动部署 DM8 DMDSC
两节点共享存储多写集群（类 Oracle RAC），完成多写验证与 TPC-C 压测；并包含
[MP-Router](https://github.com/HuangDunD/MP-Router) 的达梦适配（db-type 3，DPI 接口）。

## 快速开始（服务器到位后）

```bash
# 1. 下载 DM8 开发版 x86 rh7_64 zip（https://www.dameng.com/list_103.html）放入 pkg/
# 2. 填 cluster.conf：节点 IP、SSH、4 块共享盘的 /dev/disk/by-id 路径、密码
vim cluster.conf

./deploy.sh --dry-run                    # 预览步骤
scripts/00_preflight.sh --rw-probe       # 预检（含共享盘读写一致性探测）
./deploy.sh                              # 00→06 全流程（约 20-40 分钟）
scripts/06_verify_multiwrite.sh --failover   # 可选：故障演练
scripts/07_benchmark.sh                  # 三组 TPC-C 对照压测
```

失败续跑：`./deploy.sh --from <步骤号>`；推倒重来：`scripts/teardown.sh`。

## 目录结构

| 路径 | 说明 |
|---|---|
| `cluster.conf` | 唯一配置入口（节点/磁盘/端口/密码/调优/压测参数） |
| `deploy.sh` | 总编排（00 预检 → 06 多写验证） |
| `lib/common.sh` | 公共库：SSH 封装、模板渲染、配置校验 |
| `scripts/0*.sh` | 各步骤驱动（控制机执行） |
| `scripts/remote/*.remote.sh` | 远端执行体（root，经 stdin 注入变量） |
| `scripts/teardown.sh` | 卸载并清盘（危险，需输入 WIPE 确认） |
| `templates/*.tpl` | 全部 DSC 配置模板（`{{VAR}}` 由 cluster.conf 渲染） |
| `benchmark/` | BenchmarkSQL 5.0 + 达梦 JDBC 压测（node0/node1/双节点三组对照） |
| `mprouter/` | MP-Router 达梦适配（代码改造 + `DM-INTEGRATION.md` 对照表） |
| `docs/RUNBOOK.md` | 每步等效手工命令（排障对照） |
| `pkg/` | 手工放置 DM8 安装包 |
| `logs/`、`.rendered/` | 运行日志 / 本地渲染产物（可随时删） |

## 关键前提

- 两台 x86_64 Linux（首选 CentOS/Rocky/openEuler/Kylin，Ubuntu 打警告可尝试），内存 ≥8G；
- 4 块**两节点同时可见的共享块设备**（SAN 多路径盘或云多写盘）：DCR ≥1G、VOTE ≥1G、REDO ≥20G、DATA ≥50G，无分区无文件系统；
- 控制机（本机）到两节点 SSH 免密（root 或免密 sudo）；两节点内网互通、时钟同步（差 <2s）；
- 密码只用字母数字（避开 disql/su 多层转义）。

## MP-Router 压测（达梦适配完成后）

```bash
# 构建（在装有达梦客户端的机器上；DM_HOME 指向 DM 安装目录即可启用 WITH_DM_DPI）
cd mprouter/MP-Router && cmake -S . -B build -DDM_HOME=/home/dmdba/dmdbms && cmake --build build -j
export LD_LIBRARY_PATH=/home/dmdba/dmdbms/bin:$LD_LIBRARY_PATH
./build/serve/test/dameng_test "host=<node0> port=5236 user=SYSDBA password=<pwd>"   # 冒烟
cd build
./serve/test/run --db-type 3 --workload smallbank \
  --db-connection "host=<node0> port=5236 user=SYSDBA password=<pwd>" \
  --db-connection "host=<node1> port=5236 user=SYSDBA password=<pwd>" \
  --system-mode 11    # 0=random 2=hash 11=MP-Router，三种对照
```

详见 `mprouter/DM-INTEGRATION.md`。改造后的源码在 `mprouter/MP-Router/`（上游 main@5ad2eb4），相对上游的差异见 `mprouter/dameng-port.patch`；
本机无客户端时用 `mprouter/build_check.sh`（mock 桩，docker 内）做编译验证——两种配置已通过。
