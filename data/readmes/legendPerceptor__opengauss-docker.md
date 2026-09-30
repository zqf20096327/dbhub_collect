# OpenGauss Docker

使用 Docker 运行 OpenGauss 数据库。

## 快速开始

```bash
# 1. 复制环境配置
cp .env.example .env
# 编辑 .env 设置密码

# 2. 启动数据库
docker-compose up -d

# 3. 连接测试
docker exec -it opengauss-db gsql -U gaussdb -W YourPassword123!
```

## 默认配置

- 端口: 5432
- 用户: gaussdb
- 密码: 见 .env 文件
