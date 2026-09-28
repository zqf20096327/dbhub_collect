# 方言比较小站 - 后端 API

[![FastAPI](https://img.shields.io/badge/FastAPI-0.116.1-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-2.0.1-brightgreen.svg)](CHANGELOG.md)

访问网站：[方音圖鑒 - dialects.yzup.top](https://dialects.yzup.top/)

---

## 协作入口

如果你准备和当前仓库协作，尤其是准备在 `app/tools/` 目录下新增工具模块、复用文件与任务基础设施、或理解工具模块应当如何统一挂载，请优先阅读：

- [Tools 模块开发与接入指南](docs/implementation/tools/module_development_guide.md)

这份文档已经按当前代码重新整理，重点说明了：

- 如何在 `app/tools/` 下新增一个新的工具模块
- [`app/tools/file_manager.py`](app/tools/file_manager.py) 的每个核心函数如何使用
- [`app/tools/task_manager.py`](app/tools/task_manager.py) 的每个核心函数如何使用
- 工具模块的路由应该在哪里注册
- 为什么所有工具模块现在都应统一在 [`app/tools/__init__.py`](app/tools/__init__.py) 挂载
- `praat` 这类复杂模块在目录结构上可以更复杂，但挂载方式也必须和普通工具一致

如果你是前后端协作者，想快速了解“新增工具模块需要改哪些文件、要配哪些路由、有哪些约束和注意事项”，建议先看这份文档，再动手改代码。

---

## 📖 项目概述

**方言比较小站** 是一个基于 **FastAPI** 的高性能后端系统，专注于汉语方言数据的查询、分析和可视化。该项目为方言学术研究、语言学习和文化传承提供强大的数据支持平台。

### 🎯 核心特性

- 🔍 **中古音韵查询系统** - 按中古地位整理汉字读音，支持音位反查中古来源
- 📊 **音韵分类矩阵** - 声母-韵母-汉字交叉表，支持多维度音韵特征分类
- 🔎 **查字查调功能** - 根据汉字查询各方言点读音，支持声调查询和对比
- 🗺️ **地理信息服务** - 方言点坐标查询、区域划分、批量匹配
- 🎙️ **Praat 声学分析** - 音频声学参数提取、音高分析、共鸣峰检测、声调轮廓
- 👤 **完整用户系统** - JWT 认证、权限管理、活动追踪、多数据库权限隔离
- 🛠️ **专业工具集** - 粤拼转 IPA、数据校验、文件合并等实用工具
- 💾 **自定义数据管理** - 用户可添加和管理自己的方言数据
- 📈 **三层缓存架构** - Redis 缓存（用户、权限）+ 内存缓存（方言数据）
- 🔐 **安全可靠** - bcrypt 密码加密、Token 刷新、API 限流、权限控制
- 🏘️ **VillagesML 机器学习系统** ⭐ - 广东省 285,860 条自然村地名分析，7 大模块（字符、语义、空间、模式、区域、ML 计算），50+ API 端点，100% 数据库覆盖
- 📊 **管理员分析系统** ⭐ - 用户行为分析、RFM 分析、异常检测、排行榜系统、会话监控、设备追踪

---

## 📊 项目统计

> [!NOTE]
> 本节已按 **2026-03-27** 当前仓库与 `data/*.db` 实际内容重新整理。  
> 其中“路由数量”按源码中的 FastAPI / APIRouter 装饰器扫描统计，“数据库数量/表数”按当前本地 `data/` 目录快照统计；后续若继续扩展模块或数据库，请同步更新本节。

| 指标 | 当前数值 | 统计口径 |
|------|------|------|
| **Python 文件数** | 298 个 | 扫描仓库内 `.py` 文件，已排除 `.venv` 与 `__pycache__` |
| **Python 代码行数** | 52,133 行 | 按当前仓库 Python 文件逐个计行 |
| **HTTP 路由声明数** | 282 个 | 按 `@router.get/post/...`、`@app.get/post/...` 装饰器统计 |
| **依赖包数量** | 66 个 | 按 `requirements.txt` 的有效依赖行统计 |
| **SQLite 数据库文件数** | 13 个 | 按 `data/*.db` 统计，包含 0 字节占位库 |
| **SQLite 表总数** | 103 个 | 按所有 `.db` 中非 `sqlite_%` 表累加 |
| **当前版本** | 2.0.1 | README 当前维护版本号 |
| **最后更新** | 2026-03-27 | 本节最后核对日期 |

### 路由规模拆分（按源码目录统计）

| 模块 | 路由数 |
|------|------|
| `app/routes/core` | 16 |
| `app/routes/geo` | 7 |
| `app/routes/user` | 11 |
| `app/routes/auth.py` | 9 |
| `app/routes/index.py` | 9 |
| `app/routes/admin` | 68 |
| `app/routes/logging` | 14 |
| `app/sql` | 14 |
| `app/tools` | 27 |
| `app/villagesML` | 107 |

### 当前数据库文件概览

| 数据库 | 表数 | 说明 |
|------|------|------|
| `auth.db` | 8 | 用户、会话、usage、登录日志等 |
| `logs.db` | 5 | 访问统计、HTML 访问、关键词、诊断事件等 |
| `characters.db` | 6 | 中古音、字符位置、上古音等核心查询数据 |
| `dialects_admin.db` | 1 | 管理侧方言数据 |
| `dialects_user.db` | 1 | 用户侧方言数据 |
| `query_admin.db` | 1 | 管理侧查询表 |
| `query_user.db` | 1 | 用户侧查询表 |
| `supplements.db` | 9 | 用户补充数据、自定义分区等 |
| `villages.db` | 68 | VillagesML 预计算结果与分析表 |
| `yubao.db` | 2 | 语保相关数据 |
| `yc_spoken.db` | 1 | 语料/口语相关数据 |
| `query.db` | 0 | 当前为空占位库 |
| `query_dialects.db` | 0 | 当前为空占位库 |

---

## 🔗 相关仓库

- **[预处理字表](https://github.com/jengzang/dialects-build)**
  [![dialects-build](https://img.shields.io/badge/Repo-dialects--build-ff69b4?logo=github&logoColor=white&style=for-the-badge)](https://github.com/jengzang/dialects-build)
  方言数据预处理仓库，负责原始数据的清洗、转换和优化。

- **[前端代码](https://github.com/jengzang/dialects-js-frontend)**
  [![dialects-vue-frontend](https://img.shields.io/badge/Repo-dialects--js--frontend-0088ff?logo=github&logoColor=white&style=for-the-badge)](https://github.com/jengzang/dialects-js-frontend)
  前端界面，基于 Vue 框架和原生 JavaScript。

---

## 🚀 快速开始

### 环境要求

- Python 3.12+
- Redis 7.0+ (可选，用于缓存)
- SQLite 3.35+ (内置)
- FFmpeg (Praat 声学分析必需)

### 1. 克隆项目

```bash
git clone https://github.com/jengz

[...截断...]

ang/backend-fastapi.git
cd backend-fastapi
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量（可选）

创建 `.env` 文件：

```env
# 运行模式
RUN_TYPE=MINE  # MINE(开发) / EXE(打包) / WEB(生产)

# Redis 配置（可选）
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=

# JWT 配置
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=30
```

### 4. 启动服务

```bash
# 开发模式（单进程，自动重载）
python run.py

# 生产模式（主应用 3 workers，承接除新 GIS / Cluster 之外的主流量）
gunicorn -c gunicorn_main.py app.entrypoints.main_app:app

# 独立 GIS worker（/api/gis/**）
gunicorn -c gunicorn_gis.py app.entrypoints.gis_app:app

# 独立 Cluster worker（/api/tools/cluster/**）
gunicorn -c gunicorn_cluster.py app.entrypoints.cluster_app:app
```

说明：
- `5000`：主应用入口（保留主页、老 geo、主查询、普通 tools、villages 等）
- `5001`：仅承接 `/api/gis/**`
- `5002`：仅承接 `/api/tools/cluster/**`
- 这三套 gunicorn 需要由你现有的进程管理/转发层分别启动并按路径分流；后端代码本身不再把新 GIS 与 cluster 挂在主应用里。

| 短參數 | 長參數 | 類型 | 可選值 | 默認值 | 功能描述                                      |
| :--- | :--- | :--- | :--- | :--- |:------------------------------------------|
| `-r` | `--run` | `string` | `WEB`, `EXE`, `MINE` | `WEB` | 指定運行模式，WEB为部署模式；MINE是跑在局域网的；EXE是打包为独立程序的。 |
| `-close` | `--close-browser` | `flag` | - | `False` | 禁止自動打開瀏覽器。如果不加此參數，程序啟動後會嘗試調用系統默認瀏覽器。      |

服务启动后访问：
- **API 文档**：http://localhost:5000/docs
- **备用文档**：http://localhost:5000/redoc
- **主页**：http://localhost:5000/

---

## 🏗️ 系统架构

### 架构图

```
┌──────────────────────────────────────────────────────────────────────┐
│                       FastAPI 应用入口（app/main.py）                │
│      create_app() + lifespan() + Uvicorn / Gunicorn Worker          │
└──────────────────────────────┬───────────────────────────────────────┘
                               │
                               V
┌──────────────────────────────────────────────────────────────────────┐
│                           生命周期启动层                             │
│  run_process_startup()                                               │
│  - 初始化 SQLite 连接池                                               │
│  - 检查 supplements.db / logs.db 结构                                │
│  - 自动创建 logs.db 诊断表                                            │
│  - 清理旧工具临时目录                                                 │
│  - 预热方言缓存                                                       │
└──────────────────────────────┬───────────────────────────────────────┘
                               │
                               V
┌──────────────────────────────────────────────────────────────────────┐
│                              中间件层                                │
│  - RequestLogMiddleware                                              │
│    - auth.db usage/detail 记录                                       │
│    - logs.db hourly/daily 统计                                       │
│    - API 诊断事件（error / slow / MINE 全量模式）                    │
│  - GZipMiddleware                                                    │
│  - CORSMiddleware                                                    │
│  - EXE 模式请求期打印抑制中间件                                      │
└──────────────────────────────┬───────────────────────────────────────┘
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
          V                    V                    V
┌─────────────────┐  ┌──────────────────────┐  ┌────────────────────────┐
│ 认证与用户层     │  │ 核心业务路由层        │  │ 扩展业务路由层          │
│ /auth            │  │ /api, /sql, /logs    │  │ /admin, /user,         │
│ JWT / Session    │  │ phonology / geo /    │  │ /api/tools, /api/      │
│ Refresh Token    │  │ compare / search     │  │ villages/*             │
└─────────────────┘  │ SQL API / logs API    │  └────────────────────────┘
                     └────────────┬───────────┘
                                  │
                                  V
┌─────────────────────────────────────────────────────────