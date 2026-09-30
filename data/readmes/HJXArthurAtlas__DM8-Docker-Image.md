# DM8 Docker Image

[达梦数据库 DM8](https://www.dameng.com/) 的 Docker 镜像，基于 `centos:7.9.2009`，通过预置应答文件实现静默安装与初始化，构建即得到可直接运行的数据库镜像。

## 前置条件

达梦 DM8 安装包受授权限制，无法随源码分发，需自行下载：

1. 从[达梦官网](https://www.dameng.com/list_103.html)下载 **Linux x86_64** 版本的安装文件 `DMInstall.bin`；
2. 将 `DMInstall.bin` 放入项目根目录的 `.init/` 下：

```
.
├── .init/
│   ├── DMInstall.bin   # 自行下载，不入库
│   └── run.txt         # 静默安装应答文件
├── Dockerfile
└── LICENSE
```

## 构建镜像

```bash
docker build -t dm8:latest .
```

安装过程完全无人值守，`dminit` 会按下方环境变量初始化实例 `DAMENG` 并删除安装包，最终镜像内只有数据库程序与数据文件。

## 构建参数（ENV）

以下参数在 **构建阶段** 生效，用于 `dminit` 初始化实例；构建后修改不生效：

| 变量 | 默认值 | 说明 |
| --- | --- | --- |
| `SYSDBA_PWD` | `SYSDBA001` | SYSDBA 用户密码 |
| `SYSAUDITOR_PWD` | `SYSAUDITOR001` | SYSAUDITOR 用户密码 |
| `CASE_SENSITIVE` | `1` | 大小写敏感（1 敏感，0 不敏感） |
| `CHARSET` | `1` | 字符集（0 GB18030，1 UTF-8，2 EUC-KR） |
| `PAGE_SIZE` | `8` | 页大小（KB） |
| `EXTENT_SIZE` | `16` | 簇大小（KB） |

构建时覆盖示例：

```bash
docker build --build-arg SYSDBA_PWD=YourPwd@123 -t dm8:latest .
```

> 若需通过 `--build-arg` 覆盖，请先在 Dockerfile 中为对应变量增加 `ARG` 声明。

## 运行容器

DM8 默认监听端口 **5236**：

```bash
docker run -d --name dm8 \
  -p 5236:5236 \
  -v dm8-data:/opt/dmdbms/data \
  dm8:latest
```

数据目录为 `/opt/dmdbms/data`，建议挂载卷持久化。

## 连接验证

```bash
# 进入容器使用 disql
docker exec -it dm8 /opt/dmdbms/bin/disql SYSDBA/SYSDBA001@localhost:5236

# 或用任意 DM 客户端 / JDBC 连接
# jdbc:dm://<host>:5236
```

## 环境说明

- 运行用户：`dmdba`（属组 `dinstall`），安装目录 `/opt/dmdbms`
- 启动命令：`dmserver path=/opt/dmdbms/data/DAMENG/dm.ini`
- 基础镜像 CentOS 7 已停止维护，仅建议用于开发测试

## License

[木兰宽松许可证 第2版 (Mulan PSL v2)](./LICENSE)
