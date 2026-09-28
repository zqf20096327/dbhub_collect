# FastAPI AI Starter

一个生产就绪的 FastAPI 项目模板，集成 Celery 异步任务、PostgreSQL/pgvector 和 Redis，适合构建 AI 应用。

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.135+-green.svg)
![Celery](https://img.shields.io/badge/Celery-5.6+-orange.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 特性

- **服务工厂架构** - 基于工厂模式的依赖注入系统，自动管理服务生命周期
- **异步全栈** - FastAPI + SQLModel 异步 ORM + Celery 任务队列
- **AI 就绪** - PostgreSQL + pgvector 扩展，支持向量存储和搜索
- **JWT 认证** - 完整的用户认证系统，密码 bcrypt 加密
- **自动迁移** - Alembic 数据库迁移，应用启动时自动执行
- **容器化部署** - Docker Compose + Nginx + Supervisord

## 技术栈

| 类别 | 技术 |
|------|------|
| Web 框架 | FastAPI, Starlette |
| ORM | SQLModel (Pydantic + SQLAlchemy) |
| 任务队列 | Celery + Redis |
| 数据库 | PostgreSQL 16 + pgvector |
| 包管理 | UV |
| 代码质量 | Ruff, MyPy, Pre-commit |
| 日志 | Loguru |

## 快速开始

### 环境要求

- Python 3.12+
- Docker & Docker Compose

### 安装

```bash
# 克隆项目
git clone https://github.com/your-username/fastapi-ai-starter.git
cd fastapi-ai-starter

# 安装 UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# 安装依赖
uv sync

# 配置环境变量
cp .env.example .env
```

### 启动服务

**Docker Compose（推荐）**

```bash
docker-compose up -d
```

**本地开发**

```bash
# 启动数据库和 Redis
docker-compose up -d pgvector redis

# 启动应用
uv run main.py

# 启动 Celery（可选）
uv run celery -A celery_tasks worker --loglevel=INFO
uv run celery -A celery_tasks beat --loglevel=INFO
```

访问 http://localhost:8000/docs 查看 API 文档。

## 项目结构

```
app/
├── api/v1/              # API 路由
├── services/            # 服务层
│   ├── base.py          # 服务基类
│   ├── manager.py       # 服务管理器（单例）
│   ├── factory.py       # 服务工厂
│   ├── deps.py          # 依赖注入函数
│   ├── database/        # 数据库服务
│   │   └── models/      # SQLModel 模型
│   ├── auth/            # 认证服务
│   └── settings/        # 配置服务
├── logging/             # 日志配置
└── main.py              # FastAPI 应用入口

celery_tasks/            # Celery 任务
├── celery.py            # Celery 应用
├── celeryconfig.py      # 配置
└── workers/             # 任务定义

alembic/                 # 数据库迁移
scripts/                 # 辅助脚本
```

## 开发指南

### 数据库迁移

```bash
./scripts/migration.sh "描述"   # 生成迁移
./scripts/migrate.sh            # 应用迁移
```

### 添加新服务

1. 在 `app/services/<name>/` 创建模块
2. 实现 `service.py`（继承 `Service`）和 `factory.py`（继承 `ServiceFactory`)
3. 在 `ServiceType` 枚举中添加类型
4. ServiceManager 自动发现并注册

### 添加 API 路由

1. 在 `app/api/v1/` 创建路由文件
2. 在 `app/api/router.py` 中注册

### 添加 Celery 任务

1. 在 `celery_tasks/workers/` 创建任务
2. 在 `celeryconfig.py` 的 `include` 列表注册

### 代码检查

```bash
uv run ruff check .
uv run ruff format .
uv run mypy .
pre-commit run --all-files
```

## 环境变量

| 变量 | 说明 |
|------|------|
| `ENVIRONMENT` | 运行环境 |
| `DATABASE_URL` | 数据库连接 URL |
| `JWT_SECRET` | JWT 密钥 |

## 架构说明

### 服务工厂模式

项目使用服务工厂模式管理依赖：

- `ServiceManager` - 单例管理器，负责服务注册和创建
- `ServiceFactory` - 工厂基类，自动推断服务依赖关系
- `Service` - 服务基类，定义统一接口

服务通过依赖注入使用：

```python
from app.services.deps import get_db_service, injectable_session_scope

# 获取服务实例
db = get_db_service()

# 在 API 中注入 session
async def endpoint(session: AsyncSession = Depends(injectable_session_scope)):
    ...
```

### 数据库 Session

应用启动时自动执行 Alembic 迁移。使用 `injectable_session_scope` 获取 session，自动处理提交和回滚。

## License

MIT