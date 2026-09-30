# GaussDB 前后端分离 Web 应用

基于 Flask + PySpark 后端和 Vue.js + Element UI 前端的完整 Web 应用系统。

## 技术栈

- **后端**: Python Flask + PySpark
- **前端**: Vue.js 3 + Element Plus
- **数据库**: GaussDB (兼容 PostgreSQL 协议)
- **容器化**: Docker + Docker Compose
- **大数据处理**: Apache Spark (PySpark)

## 项目结构

```
gaussdb-webapp/
├── backend/
│   ├── app.py                 # Flask 主应用
│   ├── gaussdb_config.py      # GaussDB 配置类
│   ├── spark_connector.py     # Spark 连接器
│   ├── requirements.txt       # Python 依赖
│   └── Dockerfile             # 后端容器镜像
├── frontend/
│   ├── src/
│   │   ├── main.js            # Vue 应用入口
│   │   ├── App.vue            # 主应用组件
│   │   ├── router/            # 路由配置
│   │   ├── services/         # API 服务
│   │   └── components/       # Vue 组件
│   │       ├── UserManagement.vue
│   │       ├── ProductManagement.vue
│   │       ├── OrderManagement.vue
│   │       └── SalesAnalytics.vue
│   ├── package.json          # 前端依赖
│   ├── vite.config.js        # Vite 配置
│   ├── nginx.conf            # Nginx 配置
│   └── Dockerfile            # 前端容器镜像
├── docker-compose.yml        # 容器编排配置
├── init.sql                  # 数据库初始化脚本
└── README.md                 # 项目文档
```

## 功能特性

### 1. 用户管理
- 用户列表查看（使用 Spark 读取）
- 用户创建（姓名、邮箱、年龄）

### 2. 产品管理
- 产品列表查看（使用 Spark 读取）
- 产品创建（名称、价格、分类、库存）

### 3. 订单管理
- 订单列表查看（使用 Spark 读取）
- 订单创建（自动计算总价）

### 4. 销售分析
- 产品销售统计（订单数、总销量、总收入、平均订单金额）
- 用户消费统计（订单数、总消费）
- 使用 Spark 进行复杂聚合分析

## 环境配置

### 数据库配置

项目支持两种环境配置：

1. **本地虚拟机环境**（一主二备）
   - 默认配置在 `gaussdb_config.py` 的 `LOCAL_CONFIG`
   - 地址: `192.168.126.101:26000`
   - 用户: `yu`
   - 数据库: `postgres`

2. **云开发者空间**（伪分布式）
   - 默认配置在 `gaussdb_config.py` 的 `CLOUD_CONFIG`
   - 地址: `localhost:5432`

### 环境变量

可通过环境变量覆盖配置：

```bash
# 本地环境配置（默认）
GAUSSDB_HOST=192.168.126.101
GAUSSDB_PORT=26000
GAUSSDB_DB=postgres
GAUSSDB_USER=yu
GAUSSDB_PASSWORD=gauss@666

# 运行环境
ENVIRONMENT=local  # 默认使用本地环境，或 cloud

# 云环境配置示例
# GAUSSDB_HOST=localhost
# GAUSSDB_PORT=5432
# GAUSSDB_DB=clouddb
# GAUSSDB_USER=cloud_user
# GAUSSDB_PASSWORD=CloudPassword123!
# ENVIRONMENT=cloud
```

## 快速开始

### 方式一：Docker Compose 一键部署（推荐）

```bash
# 构建并启动所有服务
docker-compose up -d --build

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

启动后访问：
- **前端**: http://localhost
- **后端API**: http://localhost:5000/api/health
- **数据库**: 192.168.126.101:26000 (本地环境) 或 localhost:5432 (云环境)

### 方式二：本地开发运行

#### 后端开发

```bash
cd backend
pip install -r requirements.txt

# 设置环境变量（可选，默认使用本地配置）
export ENVIRONMENT=local
export GAUSSDB_HOST=192.168.126.101
export GAUSSDB_PORT=26000
export GAUSSDB_DB=postgres
export GAUSSDB_USER=yu
export GAUSSDB_PASSWORD=gauss@666

# 启动 Flask 应用
D:\anaconda\envs\MS\python.exe app.py
```

后端运行在: http://localhost:5000

#### 前端开发

```bash
cd frontend
npm install
npm run dev
```

前端开发服务器运行在: http://localhost:3000

## 数据库初始化

数据库表结构在 `init.sql` 中定义：

- **users**: 用户表（id, name, email, age, created_at）
- **products**: 产品表（id, name, price, category, stock_quantity, created_at）
- **orders**: 订单表（id, user_id, product_id, quantity, total_price, order_date）

使用 Docker Compose 时，数据库会自动初始化。手动初始化：

```bash
# 本地环境
psql -h 192.168.126.101 -p 26000 -U yu -d postgres -f init.sql

# 云环境
psql -h localhost -U cloud_user -d clouddb -f init.sql
```

## API 接口文档

### 健康检查
```
GET /api/health
```

### 用户管理
```
GET  /api/users          # 获取用户列表（Spark 读取）
POST /api/users          # 创建新用户
```

### 产品管理
```
GET  /api/products       # 获取产品列表（Spark 读取）
POST /api/products       # 创建新产品
```

### 订单管理
```
GET  /api/orders         # 获取订单列表（Spark 读取）
POST /api/orders         # 创建新订单
```

### 数据分析
```
GET /api/analytics/sales  # 销售数据分析（Spark 聚合）
GET /api/analytics/users  # 用户数据分析（Spark 聚合）
```

## Spark 集成说明

项目使用 PySpark 进行大数据处理：

1. **数据读取**: 使用 Spark JDBC 连接器从 GaussDB 读取数据
2. **数据写入**: 使用 Spark JDBC 连接器写入数据到 GaussDB
3. **数据分析**: 使用 Spark SQL 进行复杂聚合分析

Spark 配置：
- 执行器内存: 1GB
- 驱动内存: 1GB
- JDBC 驱动: PostgreSQL JDBC Driver (兼容 GaussDB)

## 部署说明

### 生产环境部署建议

1. **数据库连接**: 使用专用数据库用户，设置最小权限
2. **环境变量**: 使用 `.env` 文件或容器编排工具管理敏感信息
3. **Spark 集群**: 生产环境建议使用独立的 Spark 集群，而非本地模式
4. **Nginx 配置**: 根据实际需求调整 Nginx 配置（HTTPS、负载均衡等）
5. **监控日志**: 配置日志收集和监控系统

### 连接外部 GaussDB

如果已有部署好的 GaussDB 实例，修改 `docker-compose.yml`：

```yaml
services:
  backend:
    environment:
      - GAUSSDB_HOST=your-gaussdb-host
      - GAUSSDB_PORT=your-port
      - GAUSSDB_DB=your-database
      - GAUSSDB_USER=your-user
      - GAUSSDB_PASSWORD=your-password
```

然后移除或注释掉 `gaussdb` 服务。

## 常见问题

### 1. Spark 连接失败

- 确保 JDBC 驱动已下载到 `/opt/spark/jars/`
- 检查数据库连接参数是否正确
- 查看后端日志获取详细错误信息

### 2. 前端无法连接后端

- 检查 `nginx.conf` 中的代理配置
- 确保后端服务正常运行
- 检查 CORS 配置

### 3. 数据库连接失败

- 验证数据库服务是否运行
- 检查连接参数（主机、端口、用户名、密码）
- 确认网络连通性（容器网络或宿主机网络）

## 项目总结

本项目实现了：

✅ **前后端分离架构**: Flask 后端 + Vue.js 前端  
✅ **完整的 UI 界面**: 每个前端元素都有对应的后台处理逻辑  
✅ **GaussDB 数据库读写**: 使用 SQLAlchemy 和 Spark JDBC  
✅ **Spark 大数据框架集成**: 数据读取、写入和复杂分析  
✅ **容器化部署**: Docker + Docker Compose 一键部署  
✅ **完整的 CRUD 操作**: 用户、产品、订单管理  
✅ **数据分析功能**: 销售统计和用户分析  

## 许可证

本项目仅用于学习和实验目的。
