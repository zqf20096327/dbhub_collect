# 客户跟踪管理系统

基于 **Vue 3 + Flask + openGauss** 的客户跟踪管理课设项目，支持客户、联系人、需求、跟踪记录的全流程管理，以及用户权限、操作日志、数据导入导出与备份恢复。

## 功能概览

- 用户登录与基于角色的权限控制（管理员 / 普通用户）
- 客户、联系人、需求、跟踪记录的增删改查
- 仪表盘数据统计与可视化
- Excel 导入导出
- 数据备份与恢复
- 操作日志查询

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Vue 3、Vue Router、Vite、Axios、Bootstrap、ECharts |
| 后端 | Flask、Flask-CORS、PyJWT、APScheduler |
| 数据库 | openGauss（兼容 PostgreSQL 协议，使用 psycopg2） |

## 目录结构

```text
客户跟踪管理系统/
├── backend/                 # Flask 后端
│   ├── app.py               # 应用入口
│   ├── config.py            # 配置（优先读取环境变量 / .env）
│   ├── gunicorn_config.py   # 生产环境 Gunicorn 配置
│   ├── models/              # 数据模型
│   ├── routes/              # API 路由
│   ├── utils/               # 数据库、鉴权、日志等工具
│   ├── tests/               # 接口测试
│   └── requirements.txt
├── frontend/                # Vue 前端
│   ├── src/
│   ├── vite.config.js       # 开发代理：/api -> 127.0.0.1:5000
│   └── package.json
├── create_tables.sql        # 建表脚本
├── insert_data2.sql         # 示例数据
├── .env.example             # 环境变量模板
└── README.md
```

## 环境要求

- Python 3.8+
- Node.js 18+（推荐）
- openGauss（或兼容的 PostgreSQL）

## 快速开始

### 1. 配置数据库

1. 在 openGauss 中创建数据库（例如 `customer_tracking`）
2. 执行建表与示例数据脚本：

```bash
# 按你的实际客户端工具执行，例如 gsql / psql
gsql -d customer_tracking -f create_tables.sql
gsql -d customer_tracking -f insert_data2.sql
```

### 2. 配置环境变量

```bash
cp .env.example .env
```

编辑 `.env`，填写数据库主机、端口、库名、用户名和密码。**不要把真实密码提交到 Git。**

也可将 `.env` 放在 `backend/` 目录下，后端同样会自动加载。

### 3. 启动后端

```bash
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS / Linux
# source .venv/bin/activate

pip install -r requirements.txt
python app.py
```

默认监听：`http://127.0.0.1:5000`

健康检查：`GET /api/health`  
数据库连通性：`GET /api/test/db`

### 4. 启动前端

```bash
cd frontend
npm install
npm run dev
```

默认访问：`http://127.0.0.1:3000`

开发模式下，前端通过 **相对路径 `/api`** 访问后端；Vite 会将 `/api` 代理到 `http://127.0.0.1:5000`，无需再写死服务器 IP。

如需自定义 API 地址，可在前端目录创建 `.env`：

```env
VITE_API_BASE_URL=/api
# 或直连后端：
# VITE_API_BASE_URL=http://127.0.0.1:5000/api
```

### 5. 生产构建（可选）

```bash
cd frontend
npm run build
```

产物在 `frontend/dist/`。后端可用 Gunicorn：

```bash
cd backend
mkdir -p logs
gunicorn -c gunicorn_config.py app:app
```

## 默认说明

- 后端 CORS 已开启，便于本地前后端分离开发
- 数据库连接、密钥等敏感信息请只放在本地 `.env` 中
- 本仓库已去掉原部署环境中的绝对服务器地址，统一改为相对路径 `/api`

## 主要 API 前缀

- `/api/auth` 登录认证
- `/api/customers` 客户
- `/api/contacts` 联系人
- `/api/requirements` 需求
- `/api/tracking` 跟踪记录
- `/api/users` 用户管理
- `/api/logs` 操作日志
- `/api/backup` 备份恢复
- `/api/export`、`/api/import` 导入导出

## 许可证

仅用于课程设计与学习交流。
