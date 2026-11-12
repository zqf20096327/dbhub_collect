# 第六届 OceanBase 数据库大赛 · 赛题一：部署 seekdb

本仓库记录赛题一的部署过程与验证结果。

## 一、环境

| 项目 | 内容 |
|---|---|
| 操作系统 | Kali Linux 2026.2（VMware 虚拟机） |
| 容器 | Docker |
| seekdb 版本 | latest（`oceanbase/seekdb`） |
| 端口 | 2881 |

## 二、部署过程

### 1. 尝试一：官方安装脚本（失败）

```bash
curl -fsSL https://obbusiness-private.oss-cn-shanghai.aliyuncs.com/download-center/opensource/seekdb/seekdb_install.sh | sudo bash
sudo systemctl start seekdb
```

结果：`Unit seekdb.service not found`——安装脚本不支持 Kali（Debian 衍生版但不在支持列表内），未生成 systemd 服务。

### 2. 尝试二：Docker Hub 直连（失败）

```bash
sudo docker run -d -p 2881:2881 --name seekdb oceanbase/seekdb
```

结果：`dial tcp 157.240.12.35:443: connect: connection refused`，无法访问 Docker Hub。

### 3. 尝试三：国内镜像源（成功）

```bash
sudo docker pull docker.m.daocloud.io/oceanbase/seekdb
sudo docker tag docker.m.daocloud.io/oceanbase/seekdb oceanbase/seekdb
sudo docker run -d -p 2881:2881 --name seekdb oceanbase/seekdb
```

首次拉取因网络重置中断（`connection reset by peer`），重试后成功（已下载的层会缓存，不会从零开始）。

## 三、验证

容器状态：

```bash
sudo docker ps
```

```
CONTAINER ID   IMAGE             STATUS         PORTS                    NAMES
8318bafeab1a   oceanbase/seekdb  Up ...         0.0.0.0:2881->2881/tcp   seekdb
```

数据库连通性：

```bash
sudo docker exec seekdb mysql -uroot -h127.0.0.1 -P2881 -e "select 1"
```

返回 `1`，说明实例正常运行、可连接并执行 SQL。

## 四、遥测 ID

遥测文件位于容器内：

```
/var/lib/seekdb/run/telemetry.json
```

读取方式：

```bash
sudo docker exec seekdb cat /var/lib/seekdb/run/telemetry.json
```

> 遥测 ID 已单独提交至大赛提测平台，不在本仓库中公开。

## 五、遇到的问题与解决

| 问题 | 原因 | 解决 |
|---|---|---|
| `externally-managed-environment` | Kali 系统 Python 受 PEP 668 保护 | 不使用 `pip install` 安装服务端；改用 Docker 部署 |
| `Unit seekdb.service not found` | 安装脚本不支持 Kali | 改用 Docker |
| Docker Hub 连接被拒 | 网络不可达 | 换国内镜像源 |
| 拉取中断 `connection reset by peer` | 网络抖动 | 重试（层缓存续传） |

## 六、结论

seekdb 在 Kali + Docker 环境下部署成功，实例运行正常，可通过 MySQL 协议连接并执行 SQL。
