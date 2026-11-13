# 大学数据库管理系统（Docker 应用源码）

本项目是“数据库系统原理”课程实验 34 的 Web 三层架构应用，使用 Flask 提供页面和 JSON 接口，通过 psycopg2 访问 openGauss，并使用 Docker Compose 部署。

## 目录

```text
webapp-source/
├─ backend/
│  ├─ app.py              # 控制层与路由
│  ├─ service.py          # 业务逻辑与输入校验
│  ├─ dao.py              # 数据访问层
│  ├─ config.py           # 环境变量配置
│  ├─ templates/          # HTML 页面
│  ├─ static/             # 样式文件
│  ├─ Dockerfile
│  └─ requirements.txt
├─ sql/
│  ├─ create_db_tables.sql
│  └─ load_data.sql
├─ docker-compose.yml
├─ .env.example
└─ .gitignore
```

## 配置

复制环境变量示例并填写实际数据库信息：

```bash
cp .env.example .env
vi .env
```

`.env` 中需要填写：

```text
DB_HOST=数据库主机地址
DB_PORT=26000
DB_NAME=studentdb
DB_USER=student
DB_PASSWORD=数据库用户密码
APP_PORT=8080
```

`.env` 不会提交到 Git，也不应上传到公开仓库。

## 初始化数据库

使用 openGauss 的 `gsql` 执行：

```bash
gsql -d studentdb -p 26000 -r
\i sql/create_db_tables.sql
\i sql/load_data.sql
```

## Docker 部署

```bash
docker compose up -d --build
docker compose ps
curl http://127.0.0.1:8080/api/health
```

浏览器访问 `http://服务器IP:8080`。

停止服务：

```bash
docker compose down
```

## 页面与接口

| 方法 | 路径 | 功能 |
|---|---|---|
| GET | `/` | 首页 |
| GET | `/students` | 学生列表，支持 `?kw=` 搜索 |
| GET | `/students/<id>` | 学生详情及选课记录 |
| GET/POST | `/students/new` | 新增学生 |
| GET | `/courses` | 课程列表 |
| GET | `/stats` | 院系学生人数统计 |
| GET | `/api/students` | 学生 JSON 数据 |
| GET | `/api/health` | 数据库健康检查 |
