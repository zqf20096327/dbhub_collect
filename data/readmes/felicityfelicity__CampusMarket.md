# Campus Market 校园二手物品交易网站

基于 openGauss 数据库的校园二手商品交易系统

## 技术栈

### 前端

- Vue 3 (Composition API)
- Axios
- 原生 CSS (亚马逊风格)

### 后端

- Flask (Python Web 框架)
- SQLAlchemy (ORM)
- psycopg2 (数据库适配器)

### 数据库

- **openGauss 5.0.0** (华为开源企业级数据库)
- 兼容 PostgreSQL 协议
- 支持触发器、视图、存储过程

## 系统架构

```
┌─────────────┐     HTTP      ┌─────────────┐     SQL       ┌─────────────┐
│   Vue 3     │ ◄──────────► │   Flask     │ ◄──────────► │  openGauss  │
│  Frontend   │   REST API    │   Backend   │  SQLAlchemy   │  Database   │
│  (5174)     │               │   (5001)    │               │   (5432)    │
└─────────────┘               └─────────────┘               └─────────────┘
```

- **在线演示**：http://localhost:5173
- **后端 API**：http://localhost:5001/api
- **数据库端口**：localhost:5432
