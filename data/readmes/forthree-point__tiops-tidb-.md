# TiOps

TiOps 是一个轻量级、可私有化部署的 TiDB 多集群运维平台。它把集群总览、会话管理、
SQL Binding、常用运维、健康巡检、自动告警和每日报告集中在同一个 Web 界面中，
适合 DBA 和 TiDB 运维团队统一管理多套集群。

项目使用 Python 内置 HTTP Server，仅依赖 `PyMySQL`，无需额外的 Web 框架和管理数据库。
功能与代码架构说明见 [CLAUDE.md](CLAUDE.md)。

## 适用场景

- 同时管理开发、测试、预生产和生产环境中的多套 TiDB 集群。
- 希望减少在 TiDB、PD、Grafana、Prometheus 与命令行之间反复切换。
- 需要快速定位慢 SQL、异常会话、资源瓶颈、CDC/Drainer 延迟等常见问题。
- 需要在内网或隔离网络中部署一套轻量、可审计、数据不出域的运维工具。
- 希望通过统一巡检标准生成每日健康报告，降低重复性人工检查成本。

## 主要功能

| 模块 | 功能 |
|---|---|
| 多集群总览 | 统一管理多套 TiDB 集群，查看集群状态，快速跳转 PD、Grafana、TiDB Status 和 Prometheus |
| 会话管理 | 查看当前连接与 SQL，支持单会话、分组、批量 Kill，以及按条件循环 Kill |
| SQL Binding | 查看、创建和删除 TiDB Plan Binding，辅助处理执行计划不稳定问题 |
| 一键运维 | 查看 Binlog 状态、执行 Binlog Recover、查看参数、表容量与 TiKV Labels |
| 巡检中心 | 集中检查 TiKV 运行时长、CDC、Drainer、磁盘、CPU、内存、I/O、网络、长 SQL 和集群参数 |
| 每日报告 | 跨集群并发采集 12 项健康指标，自动评级并生成可下载的巡检报告 |
| 自动告警 | 后台定时检查磁盘、CDC、TiKV 和长 SQL，支持页面查看、手动刷新和自定义阈值 |
| 可视化设置 | 在页面中添加、修改、删除集群并配置巡检阈值，修改后即时生效 |
| Web 主题 | 支持跟随系统、深色和浅色三种模式，登录页和功能页均可切换 |
| AI SQL 优化入口 | 配置 ChatGPT、DeepSeek、Qwen、Kimi 或内部大模型网页，首页一键跳转 |
| 登录与安全 | 支持门户账号登录和 HttpOnly Session，集群地址与数据库密码加密落盘 |

## 技术特点

- 纯 Python 服务：基于 `ThreadingHTTPServer` 和 Mixin 路由组织，部署简单。
- 跨集群并发：使用线程池并发查询 TiDB SQL、Status API 和 Prometheus。
- 无额外管理库：集群配置与巡检配置使用本地 JSON，告警状态保存在进程内存中。
- 敏感信息保护：使用 OpenSSL AES-256-CBC 加密，密钥与代码分离存放。
- 自适应界面：默认跟随操作系统颜色模式，也可手动锁定深色或浅色主题。
- 可配置启停：通过 `.env`、`setup.sh`、`star.sh` 和 `stop.sh` 完成环境初始化与服务管理。

> 安全提示：会话 Kill、Binding 变更和 Binlog Recover 会修改集群状态。
> 建议使用专用低权限数据库账号，并只在受信任网络中部署本系统。

## 运行要求

- Linux 或其他兼容 Bash 的系统
- Python 3.8 或更高版本
- OpenSSL
- `sudo` 或 root 权限（用于初始化 `/etc/tidb-portal/portal.key`）
- 能够访问 TiDB SQL 端口、组件 Status API 和 Prometheus 的网络

## 快速安装

服务器可以访问 GitHub 和 Python 软件源时，可按下面的完整流程安装：

```bash
# 1. 下载代码
git clone https://github.com/forthree-point/tiops-tidb-.git
cd tiops-tidb-

# 2. 初始化 Python 环境、依赖、配置文件和本机密钥
chmod +x setup.sh star.sh stop.sh setup_key.sh
./setup.sh

# 3. 修改 Web 登录账号、密码和监听地址
vi .env

# 4. 后台启动
./star.sh
```

`.env` 推荐配置：

```dotenv
# 允许其他机器访问时使用 0.0.0.0；仅本机访问可使用 127.0.0.1
PORTAL_HOST=0.0.0.0
PORTAL_PORT=8888
PORTAL_USERNAME=tiops_admin
PORTAL_PASSWORD=replace-with-a-long-random-password
PORTAL_SESSION_TTL=28800

# 可选：公开示例集群的默认 TiDB 账号；也可以登录后在设置页面添加集群
TIDB_USER=change-me
TIDB_PASSWORD=change-me
```

启动成功后，在浏览器访问：

```text
http://<服务器实际 IP 或域名>:8888/
```

> `PORTAL_HOST=0.0.0.0` 表示监听服务器所有网卡，不是浏览器访问地址。
> 云服务器还需要在安全组和系统防火墙中放行所配置的端口。

## 安装前检查

先检查服务器已经安装的 Python。TiOps 要求 Python 3.8 或更高版本，推荐使用
Python 3.11 或 3.12。查看常见安装位置：

```bash
ls -l /usr/bin/python* /usr/local/bin/python* 2>/dev/null
```

也可以直接打印所有可识别版本：

```bash
for py in python3 python3.14 python3.13 python3.12 python3.11 python3.10 python3.9 python3.8; do
    if command -v "$py" >/dev/null 2>&1; then
        printf '%-12s %s\n' "$py" "$("$py" --version 2>&1)"
    fi
done

openssl version
```

不要为了运行 TiOps 修改系统 `/usr/bin/python3` 软链接。`setup.sh` 会自动寻找
可用的 Python 3.8～3.14，并在项目目录创建独立的 `.venv`。进入项目目录后，
如果希望明确指定：

```bash
PYTHON_BIN=python3.11 ./setup.sh
```

## 获取代码

服务器能够访问 GitHub 时：

```bash
git clone https://github.com/forthree-point/tiops-tidb-.git
cd tiops-tidb-
```

国内网络也可以从 Gitee 获取：

```bash
git clone https://gitee.com/guanguanglei/tiops-tidb.git
cd tiops-tidb
```

没有 Git 或不能访问外网时，在其他机器下载项目 ZIP，上传到服务器后执行：

```bash
unzip tiops-tidb--main.zip
cd tiops-tidb--main
```

## 初始化环境

```bash
chmod +x setup.sh star.sh stop.sh setup_key.sh
./setup.sh
```

典型输出如下，实际 Python 路径和项目目录以服务器环境为准：

```text
[setup] 使用 Python：/usr/bin/python3.11（Python 3.11.x）
[setup] 创建 Python 虚拟环境：/path/to/tiops-tidb-/.venv
[setup] 未检测到 PyMySQL，尝试从 Python 软件源安装
[setup] 已创建 .env，启动前请修改其中的账号密码
[setup] 初始化本机密钥
[setup] 密钥初始化完成：/etc/tidb-portal/portal.key
[setup] 检查 Python 模块和项目语法
[setup] 环境初始化完成
```

`setup.sh` 会检查环境、创建虚拟环境、准备 PyMySQL、生成 `.env`，并为当前
部署环境创建独立密钥。已经存在的 `.env` 和 `/etc/tidb-portal/portal.key`
不会被覆盖。

如果所选 Python 已安装 `PyMySQL`，安装脚本会让 `.venv` 继承并复用，不访问外网。
只有未检测到该模块时才会通过 `pip` 安装。无外网服务器可使用系统软件源、内网
pip 镜像或离线 wheel 提前安装 PyMySQL。

### 内网离线安装 PyMySQL

如果服务器无法访问 Python 软件源，可在一台能够联网、且 Python 版本和服务器一致
的机器上下载 wheel：

```bash
mkdir tiops-wheels
python3 -m pip download --only-binary=:all: \
    --dest tiops-wheels "PyMySQL>=1.0,<2.0"
```

把 `tiops-wheels` 目录上传到服务器的项目目录，然后执行：

```bash
PYTHON_BIN=python3.11 ./setup.sh
.venv/bin/python -m pip install --no-index \
    --find-links ./tiops-wheels "PyMySQL>=1.0,<2.0"
./setup.sh
```

如果服务器的系统 Python 已经能够执行 `import pymysql`，直接运行 `./setup.sh`
即可；脚本会创建可复用系统模块的虚拟环境，不需要联网下载。

## 配置与启动

编辑 `.env`，至少替换门户账号密码：

```bash
vi .env
```

```dotenv
PORTAL_HOST=0.0.0.0
PORTAL_PORT=8888
PORTAL_USERNAME=tiops_admin
PORTAL_PASSWORD=replace-with-a-long-random-password
PORTAL_SESSION_TTL=28800
```

`PORTAL_HOST` 是服务监听地址，不是浏览器访问地址。云服务器通常使用
`0.0.0.0` 监听，再通过 `http://<服务器IP>:8888/` 访问。不要在示例或公开文档
中填写真实公网 IP、账号或密码。

启动服务：

```bash
./star.sh
```

典型启动输出：

```text
[star] 服务已启动，PID=<进程号>
[star] 监听地址：http://0.0.0.0:8888
[star] 运行日志：/path/to/tiops-tidb-/nohup.out
```

登录后进入「设置 → 集群管理」，将公开示例集群替换为自己的 TiDB 集群配置。

### Web 主题与背景

登录页右上角和登录后的顶部导航栏都提供主题选择：

- `跟随系统`：根据操作系统的深色/浅色设置自动切换。
- `深色`：固定使用 TiOps 深色科技风背景。
- `浅色`：固定使用高对比度浅色背景。

主题选择保存在当前浏览器的本地存储中，刷新页面后仍会保留。更换浏览器、
使用无痕模式或清理站点数据后，需要重新选择。

`app.py` 会在导入业务模块前自动读取项目目录中的 `.env`，因此也可以直接运行：

```bash
.venv/bin/python app.py
```

### 从其他机器访问

如果程序运行在服务器上，而浏览器在另一台机器上，请修改 `.env`：

```dotenv
PORTAL_HOST=0.0.0.0
PORTAL_PORT=8887
```

重启后使用 `http://<服务器IP>:8887/` 访问。`0.0.0.0` 只用于服务监听，
浏览器地址中必须填写服务器的实际 IP 或域名。如果仍然无法访问，请依次检查：

```bash
# 确认进程正在运行
cat .portal.pid
ps -p "$(cat .portal.pid)"

# 确认端口已经监听
ss -lntp | grep 8887

# 查看启动错误
tail -n 100 nohup.out
tail -n 100 tidb_portal.log
```

还需要确认服务器防火墙、安全组或网络 ACL 已允许浏览器所在网络访问该端口。
生产环境建议通过 Nginx/Caddy 配置 HTTPS 和访问控制，不要直接向公网暴露管理端口。

### 停止、重启与查看日志

```bash
# 查看运行状态
cat .portal.pid
ps -p "$(cat .portal.pid)" -o pid,lstart,cmd

# 查看实时日志
tail -f nohup.out

# 停止服务（读取并校验 .portal.pid）
./stop.sh

# 确认进程退出后重新启动
./star.sh
```

`stop.sh` 会先确认 PID 属于当前项目的 `app.py`，再发送正常停止信号；如果进程
已经退出，则自动清理旧的 `.portal.pid`，避免误杀其他进程。

### 更新代码

更新前建议备份本机配置：

```bash
cp .env .env.backup
cp portal_config.json portal_config.json.backup 2>/dev/null || true
cp ai_optimizer_config.json ai_optimizer_config.json.backup 2>/dev/null || true
```

使用 Git 部署时，可拉取最新代码后重新执行初始化并重启：

```bash
git pull
./stop.sh
./setup.sh
./star.sh
```

使用 ZIP 离线更新时，不要覆盖或删除 `.env`、`portal_config.json`、
`ai_optimizer_config.json` 和 `/etc/tidb-portal/portal.key`。其中 JSON 配置依赖
原密钥解密；丢失密钥后，已有加密配置无法恢复。

## 一键巡检项目与阈值

一键巡检（每日报告，`daily_report.py`）对每个集群并发采集 **12 个项目**。每项判定
`normal / warning / danger / error / na`（`na` = 该集群无此组件，如未部署 CDC/Drainer）。
阈值常量集中在 [daily_report.py](daily_report.py) 顶部（`TH_*`）。

| # | 巡检项 | 采集源 | 警告(warning) | 严重(danger) |
|---|---|---|---|---|
| 1 | 集群状态 | SQL `cluster_info` | 任一节点 UPTIME < 24h（判为重启） | — |
| 2 | 磁盘空间 | Prometheus | 挂载点使用率 ≥ 80% | 任一挂载点 ≥ 90% |
| 3 | CPU 使用率 | Prometheus | 实例 ≥ 70% | 任一实例 ≥ 90% |
| 4 | 内存使用率 | Prometheus | 实例 ≥ 80% | 任一实例 ≥ 90% |
| 5 | I/O 负载 | Prometheus | 实例 ≥ 500 MB/s | 任一实例 ≥ 1000 MB/s（2×） |
| 6 | 网卡流量 | Prometheus | 实例 ≥ 900 MB/s（收+发，3 分钟均值） | 无（万兆卡上限 ~1250 MB/s，仅一档警告） |
| 7 | CDC 延时 | Prometheus | 延时 > 60 min 或 status ≠ 0 | status = 2（changefeed 需重搭）或延时 > 60 min |
| 8 | Drainer 延时 | Prometheus | 延时 > 60 min | 延时 > 240 min（4×） |
| 9 | 慢 SQL | SQL `cluster_processlist` + statements | 24h 内计划变异（同 digest max/min 延时 > 2×） | 有正在执行 > 30 min 的 SQL |
| 10 | 当前会话慢sql>5s | SQL `cluster_processlist` | TIME ≥ 5s 的会话数 > 10 | 会话数 > 30（3×） |
| 11 | QPS | Prometheus | 无阈值，同比展示 | 无阈值 |
| 12 | Duration P99 | Prometheus | 无阈值，同比展示 | 无阈值 |

> 说明：
> - 慢 SQL 第 10 项排除 `root / backup / query` 类账号。
> - 连接数（`collect_connections`，`PER_TIDB_MAX_CONN=500`）代码保留但**当前不参与巡检**，已被「当前会话慢sql>5s」替代。
> - 阈值改动只需改 [daily_report.py](daily_report.py) 顶部 `TH_*` 常量，判级逻辑在各 `collect_*` 函数内。

## 安全配置

### 敏感配置加密

公开的 `clusters.py` 只含文档专用示例地址，账号密码从环境变量读取。
设置页会把真实集群配置写入被 Git 忽略的 `portal_config.json`；其中地址、
密码以 `ENC(...)` 密文存放（openssl AES-256-CBC）。

- 密钥文件固化路径:**`/etc/tidb-portal/portal.key`**(权限 600,父目录 700),
  **不放进项目目录、不随代码上传分发**。
- 首次部署可一键初始化（已有密钥时不会覆盖）：

```bash
chmod +x setup_key.sh
./setup_key.sh
```

- 查找顺序:环境变量 `PORTAL_KEY_FILE` > `/etc/tidb-portal/portal.key` >
  `~/.tidb_portal.key`(旧位置,向后兼容,仅读取时回退)。
  这样密钥位置不依赖"谁启动服务、家目录在哪",适合多人 / 服务化部署。
- 常用命令(在项目目录执行):

```bash
python3 secret_store.py gen-key              # 生成密钥到固化路径(已存在则跳过)
python3 secret_store.py encrypt '新密码或地址' # 得到 ENC(...) 密文,粘贴进 clusters.py
python3 secret_store.py decrypt 'ENC(...)'   # 验证解密
python3 secret_store.py migrate              # 把 clusters.py 里的明文敏感字段批量加密
```

- 每个部署环境都应自行生成密钥，不要复制或共用开发环境的密钥。
- 密钥只需初始化一次，后续发版不需要更改。
- 改集群地址或密码流程:`encrypt` 生成新密文 → 替换 clusters.py 对应字段 → 重启;
  或直接用首页「设置 → 集群管理」页面改(明文输入、自动加密,免命令)。

### 设置中心(导航栏「设置」按钮)

- **集群管理** `/settings/clusters`:页面上添加新集群 / 修改地址、用户名、密码。
  密码框输入**明文**,保存时后端自动加密;编辑时密码留空 = 保持原值。
- **AI SQL 优化配置** `/settings/ai_optimizer`:配置首页 AI SQL Optimizer
  的显示名称和网页跳转地址，支持 ChatGPT、DeepSeek、Qwen、Kimi 官方入口
  或自定义内部大模型地址。可选 API Key 当前仅作后续 API 集成预留，不会放入
  跳转 URL 或发送到浏览器。
- 改动**即时生效**(内存热更新,无需重启),并持久化到 `portal_config.json`
  (集群地址与密码为 ENC 密文)。
- AI SQL Optimizer 配置单独保存在被 Git 忽略的
  `ai_optimizer_config.json`，模型地址和 API Key 均使用 `portal.key` 加密。
- **优先级**:存在 `portal_config.json` 时以它为准,clusters.py 内置配置仅作初始种子。
  部署新代码不会覆盖页面上做过的修改(JSON 不在 `rm -rf *.py` 清理范围);
  若要回到 clusters.py 内置配置,删除服务器上的 portal_config.json 再重启。

## 备注

- 服务无持久化：进程重启后告警清零，需等下一轮巡检调度（默认 4 小时）跑完才重新出现。
- 上线前建议本地 `python3 -m py_compile *.py` 或 `python3 app.py` 快速自检，避免语法错误导致启动失败。
