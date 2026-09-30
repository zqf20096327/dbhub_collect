# Spawned JupyterHub 🚀

<div align="center">

[![Docker](https://img.shields.io/badge/docker-20.10%2B-blue?logo=docker)](https://www.docker.com/)
[![JupyterHub](https://img.shields.io/badge/jupyterhub-5.4.3-orange?logo=jupyter)](https://jupyter.org/hub)
[![PostgreSQL](https://img.shields.io/badge/postgresql-15%2B-blue?logo=postgresql)](https://www.postgresql.org/)
[![GaussDB](https://img.shields.io/badge/GaussDB-ready-blue)](https://www.huaweicloud.com/product/gaussdb.html)
[![Vertica](https://img.shields.io/badge/Vertica-ready-green)](https://www.vertica.com/)
[![Maxcompute](https://img.shields.io/badge/ODPS-ready-orange)](https://www.aliyun.com/product/maxcompute)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

**企业级 JupyterHub 多用户部署方案 · Docker 容器化 · HTTPS 加密 · 预集成 GaussDB/PostgreSQL/Vertica/Maxcompute 等多种数据库客户端**

[English](#english) | [中文](#chinese)

</div>

---

## <a name="chinese"></a>🇨🇳 中文介绍

### 📖 项目简介

`Spawned-Jupyterhub` 是一个企业级的 JupyterHub 多用户部署方案，基于 Docker 容器化技术，提供完整的用户认证、SSL 加密和多种企业级数据库客户端集成。特别适合需要连接 GaussDB（华为高斯数据库）、Vertica、ODPS（阿里云 MaxCompute）等数据平台的数据科学团队。

### ✨ 核心特性

#### 🔐 安全与认证
- HTTPS 加密访问，支持自定义 SSL 证书
- JupyterHub 5.4.3 官方稳定版
- 管理员用户预配置
- 完整的用户权限管理

#### 🐳 Docker 容器化
- 一键 Docker Compose 部署
- Docker-in-Docker 支持，动态生成用户容器
- 独立数据卷持久化存储
- 自定义 Docker 网络 `jupyterhub-network`

#### 🗄️ 企业级数据库集成

通过环境变量预配置以下数据库客户端连接：

| 数据库 | 类型 | 配置支持 |
|--------|------|----------|
| **GaussDB** | 华为高斯数据库 | Host, Port, DBName, User, Password |
| **Vertica** | 分析型数据库 | Host, Port, DBName, User, Password |
| **ODPS** | 阿里云 MaxCompute | Access ID, Access Key, Project, Endpoint |
| **PostgreSQL** | 关系型数据库 | 可通过 Notebook 镜像扩展 |

#### 🌏 本地化配置
- 默认时区 Asia/Shanghai
- 中文环境优化
- 完整的 .env 配置示例
- 支持自定义 Notebook 镜像

### 📋 环境要求

- Docker 20.10+
- Docker Compose 2.0+
- OpenSSL（用于生成 SSL 证书）
- 操作系统：Linux、macOS 或 WSL2

### 🚀 快速开始

#### 1. 克隆仓库

```bash
git clone https://github.com/zhongsheng-chen/Spawned-Jupyterhub.git
cd Spawned-Jupyterhub
```

#### 2. 配置环境变量

```bash
# 从示例文件创建配置
cp .env.example .env

# 编辑 .env 文件，修改必要的配置
vim .env
```

**.env 主要配置项：**

```env
# JupyterHub 配置
JUPYTERHUB_ADMIN=admin
DOCKER_NETWORK_NAME=jupyterhub-network
DOCKER_NOTEBOOK_IMAGE=jupyter/datascience-notebook:latest
DOCKER_NOTEBOOK_DIR=/home/jovyan/work
TZ=Asia/Shanghai

# GaussDB 连接配置
GAUSSDB_HOST=localhost
GAUSSDB_PORT=5432
GAUSSDB_DBNAME=gaussdb
GAUSSDB_USER=gaussdb
GAUSSDB_PASSWORD=password

# Vertica 连接配置
VERTICA_HOST=localhost
VERTICA_PORT=5433
VERTICA_DBNAME=vertica
VERTICA_USER=vertica
VERTICA_PASSWORD=password

# ODPS (MaxCompute) 连接配置
ODPS_ACCESS_ID=<your-access-id>
ODPS_ACCESS_KEY=<your-access-key>
ODPS_PROJECT=<your-project>
ODPS_ENDPOINT=<your-endpoint>
```

#### 3. 创建 Docker 网络

```bash
# 创建 JupyterHub 专用的 Docker 网络
docker network create jupyterhub-network
```

#### 4. 启动服务

```bash
# 使用完整配置启动（包含数据库）
docker-compose -f docker-compose.yml -f docker-compose.db.yml up -d

# 或仅启动 JupyterHub（如使用外部数据库）
docker-compose up -d
```

#### 5. 访问 JupyterHub

打开浏览器访问：`http://localhost:8000`

使用管理员账号登录：
- 用户名：`admin`
- 密码：在 `.env` 中设置的密码

### 📁 项目结构

```text
Spawned-Jupyterhub/
├── docker-compose.yml            # 主 Docker Compose 配置
├── docker-compose.db.yml         # 数据库服务配置，用于用户状态持久化
├── .env                          # 环境变量配置
├── .env.example                  # 环境变量示例
├── .gitignore                    # Git 忽略配置
├── config/                       # 配置文件目录
│   └── jupyterhub_config.py      # JupyterHub 主配置文件
├── ssl/                          # SSL 证书目录
    ├── jupyterhub.crt            # SSL 证书
    └── jupyterhub.key            # SSL 私钥

```

### 🔧 服务管理

#### 启动/停止服务

```bash
# 后台启动
docker-compose up -d

# 查看日志
docker-compose logs -f

# 查看服务状态
docker-compose ps

# 停止服务
docker-compose down

# 重启服务
docker-compose restart
```

#### 数据卷管理

```bash
# 查看数据卷
docker volume ls

# 备份数据卷
docker run --rm -v jupyterhub-data:/data -v $(pwd):/backup alpine tar czf /backup/jupyterhub-data-backup.tar.gz -C /data .

# 恢复数据卷
docker run --rm -v jupyterhub-data:/data -v $(pwd):/backup alpine tar xzf /backup/jupyterhub-data-backup.tar.gz -C /data
```

### 🔌 数据库客户端使用

#### GaussDB 连接示例（Python）

```python
import psycopg2
import os

# 从环境变量读取配置
conn = psycopg2.connect(
    host=os.environ.get('GAUSSDB_HOST', 'localhost'),
    port=os.environ.get('GAUSSDB_PORT', '5432'),
    dbname=os.environ.get('GAUSSDB_DBNAME', 'gaussdb'),
    user=os.environ.get('GAUSSDB_USER', 'gaussdb'),
    password=os.environ.get('GAUSSDB_PASSWORD', 'password')
)

cursor = conn.cursor()
cursor.execute('SELECT version()')
print(cursor.fetchone())
```

#### Vertica 连接示例（Python）

```python
import vertica_python
import os

conn_info = {
    'host': os.environ.get('VERTICA_HOST', 'localhost'),
    'port': int(os.environ.get('VERTICA_PORT', '5433')),
    'database': os.environ.get('VERTICA_DBNAME', 'vertica'),
    'user': os.environ.get('VERTICA_USER', 'vertica'),
    'password': os.environ.get('VERTICA_PASSWORD', 'password'),
}

with vertica_python.connect(**conn_info) as conn:
    cur = conn.cursor()
    cur.execute('SELECT version()')
    print(cur.fetchone())
```

#### ODPS (MaxCompute) 连接示例（Python）

```python
from odps import ODPS
import os

o = ODPS(
    access_id=os.environ.get('ODPS_ACCESS_ID'),
    secret_access_key=os.environ.get('ODPS_ACCESS_KEY'),
    project=os.environ.get('ODPS_PROJECT'),
    endpoint=os.environ.get('ODPS_ENDPOINT')
)

# 列出所有表
for table in o.list_tables():
    print(table.name)
```

### 🔒 SSL 证书配置

#### 生成自签名证书（测试环境）

```bash
cd ssl
openssl req -x509 -newkey rsa:4096 -keyout jupyterhub.key -out jupyterhub.crt -days 365 -nodes
```

#### 配置 Let's Encrypt 证书（生产环境）

```bash
# 安装 certbot
sudo apt-get install certbot

# 获取证书
sudo certbot certonly --standalone -d your-domain.com

# 复制证书
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem ssl/jupyterhub.crt
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem ssl/jupyterhub.key
```

### 📊 监控与维护

#### 健康检查

```bash
# 检查 JupyterHub API 状态
curl http://localhost:8000/hub/api/status

# 查看容器资源使用
docker stats
```

#### 日志管理

```bash
# 实时查看日志
docker-compose logs -f

# 查看最近100行日志
docker-compose logs --tail=100

# 将日志保存到文件
docker-compose logs > jupyterhub-logs.txt
```

### ⚠️ 常见问题

#### Q1: Docker 套接字权限错误
**A:** 确保 Docker 套接字权限正确：
```bash
# 将用户添加到 docker 组
sudo usermod -aG docker $USER
# 重新登录或执行
newgrp docker
```

#### Q2: 网络不存在错误
**A:** 创建所需的 Docker 网络：
```bash
docker network create jupyterhub-network
```

#### Q3: 无法连接到 GaussDB/Vertica
**A:** 检查环境变量配置和网络连通性：
```bash
# 检查环境变量是否正确加载
docker exec jupyterhub env | grep -E "GAUSSDB|VERTICA|ODPS"

# 测试数据库连接
docker exec jupyterhub ping <database-host>
```

#### Q4: 用户无法启动 Notebook
**A:** 检查 Notebook 镜像是否存在：
```bash
# 拉取指定的 Notebook 镜像
docker pull ${DOCKER_NOTEBOOK_IMAGE}
```

### 🚢 生产环境部署建议

1. **使用正式 SSL 证书**（Let's Encrypt 或商业证书）
2. **配置外部 PostgreSQL 数据库**（使用 docker-compose.db.yml）
3. **启用资源限制**：
   ```yaml
   services:
     hub:
       deploy:
         resources:
           limits:
             memory: 2G
   ```
4. **设置定期备份**：
   ```bash
   # 添加 crontab 任务
   0 2 * * * cd /path/to/Spawned-Jupyterhub && ./backup.sh
   ```
5. **使用反向代理**（Nginx/Traefik）处理 SSL  termination
6. **配置日志轮转**和监控告警

### 🤝 贡献指南

欢迎贡献！您可以通过以下方式参与：

1. 🍴 Fork 本仓库
2. 🌿 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 💾 提交您的修改 (`git commit -m 'Add some AmazingFeature'`)
4. 📤 推送到分支 (`git push origin feature/AmazingFeature`)
5. 🔍 提交 Pull Request

### 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

### 📞 联系方式

- **作者**: zhongsheng-chen
- **GitHub**: [@zhongsheng-chen](https://github.com/zhongsheng-chen)
- **项目链接**: [https://github.com/zhongsheng-chen/Spawned-Jupyterhub](https://github.com/zhongsheng-chen/Spawned-Jupyterhub)

### 🙏 致谢

- [JupyterHub](https://github.com/jupyterhub/jupyterhub) - 多用户 Jupyter 笔记本服务器
- [Docker](https://www.docker.com/) - 容器化平台
- [GaussDB](https://www.huaweicloud.com/product/gaussdb.html) - 华为高斯数据库
- [Vertica](https://www.vertica.com/) - 分析型数据库
- [MaxCompute](https://www.aliyun.com/product/odps) - 阿里云大数据计算服务

---

## <a name="english"></a>🇬🇧 English Introduction

### 📖 Project Overview

`Spawned-Jupyterhub` is an enterprise-grade multi-user JupyterHub deployment solution based on Docker containerization technology. It provides complete user authentication, SSL encryption, and integration with various enterprise database clients, especially suitable for data science teams that need to connect to GaussDB, Vertica, ODPS (Alibaba Cloud MaxCompute) and other data platforms.

### ✨ Key Features

#### 🔐 Security & Authentication
- HTTPS encrypted access with custom SSL certificates
- Official JupyterHub 5.4.3 stable version
- Pre-configured admin user
- Complete user permission management

#### 🐳 Docker Containerization
- One-click Docker Compose deployment
- Docker-in-Docker support for dynamic user containers
- Persistent data volume
- Custom Docker network `jupyterhub-network`

#### 🗄️ Enterprise Database Integration

Pre-configured database clients via environment variables:

| Database | Type | Configuration Support |
|----------|------|----------------------|
| **GaussDB** | Huawei Gauss Database | Host, Port, DBName, User, Password |
| **Vertica** | Analytical Database | Host, Port, DBName, User, Password |
| **ODPS** | Alibaba MaxCompute | Access ID, Access Key, Project, Endpoint |
| **PostgreSQL** | Relational Database | Extensible via Notebook images |

For detailed configuration and usage instructions, please refer to the [Chinese documentation](#chinese) above.

---

<div align="center">
Made with ❤️ by zhongsheng-chen
</div>