# test-oceanbase-ora

通过 Docker 在 Linux 服务器上快速启动 OceanBase 社区版 4.3.x LTS，并自动创建 **Oracle 兼容模式** 租户、业务用户和示例表，用于测试与验证 Oracle 兼容能力。

- 单容器、单机部署，仅用于测试，不要用于生产。
- 一条 `./run.sh` 完成拉镜像、启动容器、等待就绪、创建 Oracle 租户与初始化数据。
- 数据与 obd 配置持久化在工程内的 `volumes/` 目录，第二次运行会自动加载原数据。
- 容器时区固定为 Asia/Shanghai。

## 目录结构

```
.
├── conf/ob.env          # 全部可配置参数（镜像、端口、密码、资源规格、网络等）
├── sql/                 # 初始化 SQL 模板（占位符由 run.sh 渲染）
├── volumes/
│   ├── data/ob/         # 映射到容器 /root/ob：observer 数据、clog、日志
│   └── conf/obd/cluster # 映射到容器 /root/.obd/cluster：obd 集群配置
├── run.sh               # 启动容器并完成初始化
├── stop.sh              # 停止容器
├── log.sh               # 查看实时日志
└── test.sh              # 验证租户、用户、示例数据与时区
```

## 环境要求

| 项目 | 要求 |
| --- | --- |
| 操作系统 | Linux（x86_64 或 ARM64） |
| Docker | 已安装并运行，当前用户有执行 docker 的权限（或使用 sudo） |
| 内存 | 建议 16GB 及以上；最低 8GB 时需调小 `conf/ob.env` 中的资源参数 |
| 磁盘 | 建议 30GB 及以上可用空间 |
| 端口 | `HOST_PORT`（默认 2881）未被占用 |
| 网络 | 能访问 Docker Hub；不可达时可改用 quay.io / ghcr.io 镜像地址或提前导入镜像 |

首次启动容器并完成初始化约需 3~6 分钟，`./run.sh` 会阻塞等待并自动初始化。

## 快速开始

将工程放到服务器后，在工程根目录执行：

```bash
chmod +x ./*.sh
./run.sh
```

看到类似输出即表示初始化完成：

```
[2026-01-01 10:00:00] 初始化完成。
...
  容器时间：2026-01-01 10:00:00 CST (+0800)
执行 ./test.sh 可自动验证数据库状态。
```

随后执行验证：

```bash
./test.sh
```

## 访问方式

**统一使用「宿主机 IP + 暴露端口」访问，不需要关心容器内部 IP。**

1. 获取宿主机 IP：

   ```bash
   hostname -I
   # 或
   ip addr
   ```

2. 确认端口映射：

   ```bash
   docker ps --filter name=oceanbase-ora
   ```

3. 确保服务器防火墙放行 `HOST_PORT`（默认 2881），并确认从客户端可连通：

   ```bash
   nc -vz <HOST_IP> 2881
   ```

### 使用 obclient 连接

以下 `<HOST_IP>` 替换为服务器 IP，密码与 `conf/ob.env` 一致。

sys 租户（集群管理）：

```bash
obclient -h<HOST_IP> -P2881 -uroot@sys -proot123456 -Doceanbase -A
```

Oracle 租户管理员（租户名 `ora_tenant`）：

```bash
obclient -h<HOST_IP> -P2881 -usys@ora_tenant -poracle123456 -A
```

Oracle 业务用户：

```bash
obclient -h<HOST_IP> -P2881 -uappuser@ora_tenant -papp123456 -A
```

如果客户端机器没有安装 obclient，也可以进入容器连接：

```bash
docker exec -it oceanbase-ora obclient -h127.0.0.1 -P2881 -uappuser@ora_tenant -papp123456 -A
```

### 使用 JDBC 连接

使用 OceanBase JDBC 驱动（`oceanbase-client`），URL 形如：

```
jdbc:oceanbase://<HOST_IP>:2881/
```

- Oracle 租户业务用户：用户名 `appuser@ora_tenant`，密码 `app123456`
- Oracle 租户管理员：用户名 `sys@ora_tenant`，密码 `oracle123456`
- sys 租户：用户名 `root@sys`，密码 `root123456`

## 日常管理

| 命令 | 说明 |
| --- | --- |
| `./run.sh` | 启动容器并完成初始化（容器已存在时复用或启动） |
| `./run.sh --no-init` | 仅启动容器，不等待、不初始化 |
| `./log.sh` | 实时查看容器日志（最近 200 行） |
| `./test.sh` | 验证时区、Oracle 租户、业务用户与示例表 |
| `./stop.sh` | 停止容器，保留容器与数据 |
| `./stop.sh --purge` | 停止并删除容器，`volumes/` 数据仍保留 |

### 第二次及以后运行

```bash
./run.sh
```

- 容器未删除：自动 `docker start` 复用，数据保留。
- 容器已 `--purge` 删除：重新创建容器，挂载同一 `volumes/`，obd 检测到已有配置后直接启动原集群，数据保留。
- 初始化步骤是幂等的：已存在的资源单元、资源池、租户、用户、示例表会自动跳过；若修改了 `ORA_CPU`，脚本会自动调整已有 `ora_unit` 的 CPU。
- 镜像自带的 test 租户默认会占用 sys 租户之外的剩余 CPU，`run.sh` 会将其 `MAX_CPU` 自动限制为 `TEST_TENANT_MAX_CPU`（默认 1），为 Oracle 租户释放资源。
- 集群日志盘不足时，`run.sh` 会自动执行 `ALTER SYSTEM SET log_disk_size` 扩容到 `OB_LOG_DISK_SIZE`，再创建资源池。

## 持久化说明

| 宿主机目录 | 容器目录 | 内容 |
| --- | --- | --- |
| `volumes/data/ob` | `/root/ob` | observer 数据文件、clog、运行日志 |
| `volumes/conf/obd/cluster` | `/root/.obd/cluster` | obd 集群部署配置（`config.yaml` 等） |

这两个目录必须同时保留。只保留数据目录会导致下次启动重新部署集群，只保留配置目录会丢失数据。

容器使用自定义网络与固定内部 IP（`172.31.254.10`），目的仅是让容器重建后 obd 配置中的地址仍然有效；用户访问始终走宿主机 IP 与端口映射。

如需彻底清空数据（谨慎操作）：

```bash
./stop.sh --purge
rm -rf volumes/data/ob/* volumes/conf/obd/cluster/*
```

## 主要配置项（conf/ob.env）

| 变量 | 默认值 | 说明 |
| --- | --- | --- |
| `OB_IMAGE` | `oceanbase/oceanbase-ce:4.3.5-lts` | 官方镜像，按需改为实际可用 tag |
| `CONTAINER_NAME` | `oceanbase-ora` | 容器名 |
| `HOST_PORT` | `2881` | 宿主机映射端口（对外访问端口） |
| `TZ` | `Asia/Shanghai` | 容器时区 |
| `DOCKER_NETWORK` | `oceanbase-ora-net` | 自定义网络名 |
| `NETWORK_SUBNET` | `172.31.254.0/24` | 网络子网，冲突时修改 |
| `CONTAINER_IP` | `172.31.254.10` | 固定容器内部 IP |
| `MODE` | `mini` | 镜像部署规格 |
| `OB_MEMORY_LIMIT` | `10G` | OceanBase 总内存 |
| `OB_SYSTEM_MEMORY` | `2G` | 系统预留内存 |
| `OB_DATAFILE_SIZE` | `5G` | 数据盘大小 |
| `OB_LOG_DISK_SIZE` | `10G` | 集群日志盘总容量；需容纳 sys 2G + test 2G + Oracle 2G，至少 6G |
| `OB_SYS_PASSWORD` | `root123456` | sys 租户 root 密码 |
| `OB_TENANT_NAME` | `test` | 镜像自带的 MySQL 模式租户名 |
| `OB_TENANT_MIN_CPU` / `OB_TENANT_MEMORY_SIZE` | `1` / `2G` | 自带租户规格（为 Oracle 租户预留资源） |
| `TEST_TENANT_MAX_CPU` | `1` | test 租户 CPU 上限，脚本启动时自动限制；设为 0 表示不限制 |
| `ORA_TENANT` | `ora_tenant` | Oracle 模式租户名 |
| `ORA_CPU` / `ORA_MEMORY` / `ORA_LOG_DISK` | `2` / `4G` / `2G` | Oracle 租户资源规格 |
| `ORA_SYS_PASSWORD` | `oracle123456` | Oracle 租户 sys 用户密码 |
| `APP_USER` / `APP_PASSWORD` | `appuser` / `app123456` | 示例业务用户 |
| `AUTO_INIT` | `true` | 是否自动初始化 |
| `BOOT_TIMEOUT` | `600` | 等待启动超时（秒） |

密码建议使用字母和数字，避免 `|`、`&`、`$` 等会被 sed/Shell 特殊处理的字符。

## 时区说明

- 容器启动时传入 `TZ=Asia/Shanghai`，并将宿主机 `/usr/share/zoneinfo/Asia/Shanghai` 挂载为容器 `/etc/localtime`。
- 初始化时在 sys 租户执行 `SET GLOBAL time_zone = '+08:00';`。
- 验证：

  ```bash
  docker exec oceanbase-ora date
  # 预期包含 CST 与 +0800

  docker exec -i oceanbase-ora obclient -h127.0.0.1 -P2881 -uroot@sys -proot123456 -A -Doceanbase \
    -e "SELECT @@time_zone;"
  # 预期输出 +08:00
  ```

## 常见问题

**1. 启动超时或初始化失败**

```bash
./log.sh
docker logs --tail 100 oceanbase-ora
```

常见原因是内存或 CPU 不足。可调小 `conf/ob.env` 中的 `OB_MEMORY_LIMIT`、`OB_SYSTEM_MEMORY`、`OB_TENANT_MEMORY_SIZE`、`ORA_MEMORY`，确保宿主机内存大于 `OB_MEMORY_LIMIT`。

如果日志出现 `CPU resource not enough`，说明 zone 内 CPU 已被占满。`run.sh` 会先将 test 租户的 `MAX_CPU` 限制为 `TEST_TENANT_MAX_CPU`（默认 1）；若仍不足，可继续调小 `ORA_CPU`（如 `1`）。也可手动查看与调整：

```bash
# 注意 SQL 中的 $ 需要使用单引号，避免 Shell 展开
docker exec oceanbase-ora obclient -h127.0.0.1 -P2881 -uroot@sys -proot123456 -A -Doceanbase \
  -e 'SELECT SVR_IP, ZONE, CPU_CAPACITY, CPU_ASSIGNED FROM oceanbase.GV$OB_SERVERS;'

docker exec oceanbase-ora obclient -h127.0.0.1 -P2881 -uroot@sys -proot123456 -A -Doceanbase \
  -e "SELECT NAME, MAX_CPU, MIN_CPU, MEMORY_SIZE FROM oceanbase.DBA_OB_UNIT_CONFIGS;"
```

手动释放 test 租户 CPU（unit 名称以上述查询结果为准）：

```sql
ALTER RESOURCE UNIT test_unit MAX_CPU = 1, MIN_CPU = 1;
```

如仍无法创建资源池，可删除默认 test 租户（谨慎操作，删除后需等待资源回收）：

```sql
DROP TENANT test;
```

如果日志出现 `LOG_DISK resource not enough`，说明集群日志盘容量不足。`sys` 2G + `test` 2G + Oracle 2G 合计至少需要 6G，`run.sh` 会自动检测并动态扩容：

```sql
ALTER SYSTEM SET log_disk_size = '10G';
```

验证：

```bash
docker exec oceanbase-ora obclient -h127.0.0.1 -P2881 -uroot@sys -proot123456 -A -Doceanbase \
  -e 'SELECT LOG_DISK_CAPACITY, LOG_DISK_ASSIGNED FROM oceanbase.GV$OB_SERVERS;'
```

`log_disk_size` 的 `edit_level` 为 `DYNAMIC_EFFECTIVE`，无需重启容器。容器重启后 obd 可能按持久化配置恢复到旧值，`run.sh` 每次会重新检查并扩容。

**2. 端口 2881 被占用**

修改 `conf/ob.env` 的 `HOST_PORT`（例如 `2882`），重新执行 `./run.sh`。注意容器已存在时端口修改不会生效，需要 `./stop.sh --purge` 后重建。

**3. 网络子网冲突**

如果出现 `Pool overlaps with other one on this address space`，修改 `NETWORK_SUBNET` 与 `CONTAINER_IP` 后重试；或删除旧网络：

```bash
docker network rm oceanbase-ora-net
```

**4. 固定 IP 被占用**

报错 `Address already in use` 时，修改 `CONTAINER_IP` 为新地址后重建容器。

**5. 镜像 tag 不存在或拉取失败**

确认 Docker Hub 上可用的 4.3.x tag，并修改 `OB_IMAGE`。也可以改用：

```
quay.io/oceanbase/oceanbase-ce:4.3.5-lts
ghcr.io/oceanbase/oceanbase-ce:4.3.5-lts
```

**6. 脚本在 Windows 编辑后无法执行**

确保文件为 LF 行尾（工程已通过 `.gitattributes` 约束），并在服务器上执行：

```bash
chmod +x ./*.sh
# 或直接使用 bash
bash run.sh
```
