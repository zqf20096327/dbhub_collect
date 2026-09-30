# YashanDB SQL 审计执行平台

## 项目简介

基于 Spring Boot + Vue 3 构建的企业级 SQL 审计执行平台，支持工单审批流程、多数据库统一执行、执行结果追踪等功能。

## 核心功能

### 1. 用户管理
- 用户注册/登录（JWT 认证）
- 角色权限控制（ADMIN/DBA/普通用户）
- 用户列表管理

### 2. 数据库配置管理
- 数据库连接配置（支持 YashanDB）
- 连接测试
- 加密存储敏感信息

### 3. 工单管理
- SQL 工单创建（支持多数据库选择）
- 富文本 SQL 编辑器
- 工单列表查看
- 工单详情与执行结果展示

### 4. 审批流程
- 提交工单后自动进入待审批状态
- ADMIN/DBA 角色可审批通过/拒绝
- 审批意见记录

### 5. SQL 执行
- 按工单顺序在多个数据库执行 SQL
- 失败策略配置（停止/继续）
- 实时执行结果记录
- 详细错误信息展示
- 执行日志持久化

### 6. 预约执行
- 支持预约指定时间执行
- 定时任务调度

## 技术栈

### 后端
- **框架**: Spring Boot 2.x
- **ORM**: MyBatis-Plus
- **认证**: Spring Security + JWT
- **数据库**: YashanDB
- **构建工具**: Maven

### 前端
- **框架**: Vue 3
- **UI 组件**: Element Plus
- **状态管理**: Pinia
- **路由**: Vue Router
- **富文本**: Vue Quill
- **构建工具**: Vite

## 项目结构

```
sql-audit-yashandb-java/
├── sql-audit-backend/      # 后端 Spring Boot 项目
│   ├── src/main/java/com/sqlaudit/
│   │   ├── config/         # 配置类（CORS、安全等）
│   │   ├── module/         # 业务模块
│   │   │   ├── auth/       # 认证模块
│   │   │   ├── user/       # 用户管理
│   │   │   ├── dbconfig/   # 数据库配置
│   │   │   ├── workorder/  # 工单管理
│   │   │   └── execution/  # SQL 执行
│   │   └── security/       # JWT 认证
│   └── pom.xml
│
├── sql-audit-frontend/     # 前端 Vue 3 项目
│   ├── src/
│   │   ├── views/          # 页面组件
│   │   ├── layout/         # 布局组件
│   │   ├── api/            # API 接口
│   │   ├── store/          # Pinia 状态
│   │   └── router/         # 路由配置
│   └── package.json
│
├── docker-compose.yml       # Docker 编排
└── README.md
```

## 快速开始

### 方式一：本地开发

#### 后端启动
```bash
cd sql-audit-backend
mvn clean package
java -jar target/sql-audit-backend.jar
```

#### 前端启动
```bash
cd sql-audit-frontend
npm install
npm run dev
```

访问: http://localhost:5173

### 方式二：Docker 部署

```bash
# 构建并启动
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止
docker-compose down
```

访问: http://localhost

## 默认账号

| 角色 | 用户名 | 密码 |
|------|--------|------|
| 管理员 | admin | admin123 |
| DBA | dba | dba123 |

## 核心流程

1. **创建工单**: 用户填写 SQL，选择目标数据库
2. **审批工单**: DBA/管理员审批通过或拒绝
3. **执行工单**: 审批通过后执行 SQL
4. **查看结果**: 查看每个数据库的执行结果和错误信息

## License

MIT
