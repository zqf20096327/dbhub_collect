# openGauss 数据库实验平台

## 平台说明

基于 WSL2、Docker 和 openGauss 7.0.0-RC3 的数据库系统实验平台。  
实验数据库环境与原课设数据库环境完全隔离，互不影响。

## 固定配置

| 配置项 | 值 |
|--------|-----|
| 学号 | 2023217472 |
| 实验容器 | lab-opengauss |
| 实验镜像 | opengauss-lab:7.0.0-rc3-local |
| 实验端口 | 15433 |
| 实验数据库 | jwgl_2023217472 |
| 实验用户 | jwgl_user_2023217472 |
| 实验数据卷 | opengauss_lab_data |
| 课设容器 | qbank-opengauss |
| 课设端口 | 15432 |

## 首次使用

```bash
cd openGaussLab
chmod +x script/*.sh
./script/setup_env.sh
./script/lab.sh init
./script/lab.sh status
./script/lab.sh verify
```

## 日常命令

```bash
./script/lab.sh start          # 启动实验容器
./script/lab.sh stop           # 停止实验容器
./script/lab.sh status         # 查看平台状态
./script/lab.sh connect-lab    # 以实验用户连接数据库
./script/lab.sh connect-admin  # 以管理员连接数据库
```

## 数据库管理

| 命令 | 作用 | 风险 |
|------|------|------|
| `init` | 创建/启动容器，初始化用户和数据库 | 低，可重复执行 |
| `drop` | 删除实验数据库和用户 | 中，实验数据丢失 |
| `reset` | drop + init + verify 一键重置 | 中，实验数据丢失 |
| `destroy` | 删除实验容器和数据卷 | 高，全部实验环境不可恢复 |

## 执行 SQL

普通模式（实验用户）：

```bash
./script/lab.sh run-sql experiments/01_database_table/01_create.sql
./script/lab.sh run-experiment experiments/01_database_table
```

管理员模式：

```bash
./script/lab.sh run-sql --admin experiments/05_user_permission/01_create_user.sql
./script/lab.sh run-experiment --admin experiments/05_user_permission
```

## 安全边界

**严禁**对 `qbank-opengauss`、端口 `15432` 和数据库 `qbank_db` 执行任何实验操作。

本平台的全部写操作仅发生在 `lab-opengauss` 容器内的 `jwgl_2023217472` 数据库中。

## DBeaver

平台通过 `verify` 命令验收后，再配置 DBeaver Community 连接 `127.0.0.1:15433`。

## 目录结构

```text
openGaussLab/
├── README.md
├── experiments/          # 实验 SQL 脚本
├── logs/                 # SQL 执行日志
└── script/
    ├── common.sh         # 公共模块
    ├── setup_env.sh      # 密码配置
    ├── lab.sh            # 主管理入口
    └── .env.example      # 密码配置模板
```
