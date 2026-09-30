# 🧭 OceanBase Local Playground

> A reproducible, Docker-based OceanBase single-node environment for Windows + WSL2 users, designed for SQL practice, tenant operations, and competition training.
> 一个可复现的、基于 Docker 的 OceanBase 单机环境，面向 Windows + WSL2 用户，用于 SQL 练习、租户操作与比赛训练。

[English](README.md) | [简体中文](README.zh-CN.md)

---

## ✨ Vision / 项目愿景

Setting up OceanBase locally on Windows is harder than it should be.

Running `observer` natively inside WSL2 frequently fails at bootstrap time with low-level RPC timeouts (`-4012`, `-4653`) caused by WSL2's virtualized clock and scheduling behavior. This project documents a working path that avoids those problems entirely: **run OceanBase in Docker Desktop (WSL2 backend)**.

The goal is a **10-minute, reproducible local OceanBase environment** for learners, competitors, and developers who just want to write SQL — not fight the platform.

在 Windows 上本地搭建 OceanBase 比想象中要难。

在 WSL2 中直接运行 `observer`，经常在 bootstrap 阶段因为 WSL2 的虚拟化时钟与调度问题，出现底层 RPC 超时（`-4012`、`-4653`），永远无法完成初始化。本项目记录了一条能完全绕开这些问题的可行路径：**在 Docker Desktop（WSL2 后端）中运行 OceanBase**。

目标是提供一个**10 分钟可复现的本地 OceanBase 环境**，让学习者、参赛者、开发者专注于写 SQL，而不是和平台搏斗。

---

## 🚀 Features / 当前功能

| Feature | Status | Notes |
|---|---|---|
| Docker-based OceanBase single node | ✅ Implemented | One `docker run` command |
| Windows + WSL2 support | ✅ Verified | Tested on Windows 10.0.22631 |
| OceanBase CE 4.4.2.1 | ✅ Verified | Pulled from `oceanbase/oceanbase-ce:latest` |
| sys tenant connection | ✅ Verified | `root@sys`, port `2881` |
| Basic DDL / DML workflow | ✅ Verified | `create database` / `insert` / `select` |
| Grafana / Prometheus / obproxy / obagent | ❌ Not included | Not required for single-node practice |
| Native WSL2 (non-Docker) deployment | ❌ Not recommended | See "Why not WSL2 native" below |

---

## 📦 Installation / 安装方式

### Prerequisites / 环境要求

| Item | Requirement |
|---|---|
| OS | Windows 10 / 11 |
| Docker | Docker Desktop with WSL2 backend |
| Memory | ≥ 8 GB (observer uses 6 GB `memory_limit`) |
| Disk | ≥ 20 GB free (image + data + logs) |
| CPU | 4+ cores (8 recommended) |

### Step 1 — Install Docker Desktop / 安装 Docker Desktop

1. Open https://www.docker.com/products/docker-desktop/
2. Download **Download for Windows - AMD64**
3. During installation, **check "Use WSL 2 based engine"**
4. Restart Windows after installation

Verify:
powershell

docker version
docker ps

Step 2 — Pull the OceanBase image / 拉取 OceanBase 镜像
docker pull oceanbase/oceanbase-ce:latest

Step 3 — Start the container / 启动容器
docker run -d --name obce `
  -p 2881:2881 `
  -p 2882:2882 `
  -e MODE=mini `
  -e OB_MEMORY_LIMIT=6G `
  -e OB_SYSTEM_MEMORY=1G `
  -e OB_DATAFILE_SIZE=2G `
  -e OB_LOG_DISK_SIZE=14G `
  oceanbase/oceanbase-ce:latest

Or as a single line:
docker run -d --name obce -p 2881:2881 -p 2882:2882 -e MODE=mini -e OB_MEMORY_LIMIT=6G -e OB_SYSTEM_MEMORY=1G -e OB_DATAFILE_SIZE=2G -e OB_LOG_DISK_SIZE=14G oceanbase/oceanbase-ce:latest

Step 4 — Wait for initialization / 等待初始化
docker logs -f obce

First startup takes about 1–5 minutes. Wait until you see:
oceanbase bootstrap ok
obshell bootstrap ok

Note: bootstrap ok does not mean the SQL port is immediately ready. Wait another 1–3 minutes before connecting.

Step 5 — Connect / 连接
docker exec -it obce obclient -h127.0.0.1 -P2881 -uroot@sys -Doceanbase -A

Expected welcome output:

Welcome to the OceanBase.  Commands end with ; or \g.
Your OceanBase connection id is ...
Server version: OceanBase_CE 4.4.2.1 ...
obclient(root@sys)[oceanbase]>

🧪 Testing / 测试方式
After connecting, run the following SQL to verify the environment:
select version();

show databases;

create database test;
use test;

create table t1(id int primary key, name varchar(20));
insert into t1 values (1, 'miku'), (2, 'oceanbase');
select * from t1;

Expected result:
+----+-----------+
| id | name      |
+----+-----------+
|  1 | miku      |
|  2 | oceanbase |
+----+-----------+
2 rows in set (0.001 sec)
If this returns without error, the environment is fully functional.

📖 Documentation / 相关文档
Document	Purpose
README.md	English entry point
README.zh-CN.md	Chinese entry point
docs/WSL2-NATIVE-FAILURE.zh-CN.md	Record of the failed native WSL2 deployment (planned)
docs/TROUBLESHOOTING.zh-CN.md	Common issues and fixes (planned)

中文提醒：

默认账号 root@sys 无密码，仅适合本地练习环境，请勿将 2881 端口暴露到公网；

容器默认把 2881、2882 绑定到 0.0.0.0，在不可信网络中请改为 127.0.0.1；

docker rm -f obce 会彻底删除容器内所有数据，请先备份；

请勿提交任何 .env、密钥或生成凭据到本仓库；

本项目仅用于学习与比赛训练，请遵守 Docker、OceanBase 及网络服务商的条款。

🧱 Why not WSL2 native? / 为什么不用 WSL2 原生部署
Attempting a native obd deployment inside WSL2 leads to the following symptoms:

text
[errcode=-4012] OB_TIMEOUT
[errcode=-4653] OB_LOCATION_NOT_EXIST
[errcode=-4389] timer task too much delay in priority queue
observer listens on port 2881, but obclient connections always time out, and bootstrap never completes.

Root cause: WSL2's virtualized clock and CPU scheduling are not stable enough for OceanBase's internal timer/heartbeat mechanism, even after tuning vm.max_map_count, fs.aio-max-nr, and ulimit.

Why Docker works: Docker Desktop's WSL2 backend provides additional compatibility for clocks, AIO, and scheduling. The official oceanbase/oceanbase-ce image is already tuned for container environments.













