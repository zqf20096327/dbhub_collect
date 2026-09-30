# openGauss外键约束实验环境

## 项目结构
```
openGauss实验/
├── docker-compose.yml          # Docker Compose配置
├── Dockerfile                  # Docker镜像配置
├── start.bat                   # 启动数据库
├── stop.bat                    # 停止数据库
├── connect.bat                 # 连接数据库
└── data/                       # 数据库数据目录
```

## 快速开始

### 1. 启动数据库
```bash
start.bat
```

### 2. 连接数据库
使用DBeaver或其他PostgreSQL客户端：
- 主机：localhost
- 端口：5432
- 用户名：gaussdb
- 密码：Enmo@123
- 数据库：postgres

### 3. 编写实验脚本
在数据库客户端中编写您自己的外键约束实验脚本

## 实验要求
- 定义2张表间的无级联modification、有级联modification的外键关联
- 判断当增/删/改一张表中的主键、外键值时，DBMS的反应

## 停止数据库
```bash
stop.bat
```
