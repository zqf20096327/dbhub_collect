# DeepFMT 信创版后端

## 概述

Spring Boot 3 + openGauss 信创合规后端，服务 DeepFMT 诊疗系统。

## 技术栈

| 组件 | 技术 |
|------|------|
| 框架 | Spring Boot 3.2 |
| 数据库 | openGauss 5（PostgreSQL兼容）|
| 认证 | JWT（HS256，24小时）|
| 加密 | 国密SM4 CBC模式（bouncycastle）|
| AI | 通义千问（阿里云百炼）|

## 环境变量

| 变量 | 必填 | 说明 |
|------|------|------|
| DB_HOST | 是 | openGauss数据库地址 |
| DB_PORT | 否 | 端口，默认5432 |
| DB_NAME | 否 | 数据库名，默认deepfmt |
| DB_USER | 是 | 数据库用户名 |
| DB_PASSWORD | 是 | 数据库密码 |
| JWT_SECRET | 是 | JWT签名密钥（≥32字符）|
| SM4_KEY | 是 | SM4加密密钥（32字符hex，16字节）|
| QWEN_API_KEY | 是 | 通义千问API Key |

## 启动

```bash
# 1. 初始化openGauss数据库（执行schema）
psql -h $DB_HOST -U $DB_USER -d $DB_NAME -f init.sql

# 2. 构建
./mvnw clean package -DskipTests

# 3. 启动
java -jar target/deepfmt-xinchuang-backend-1.0.0.jar
```

## API列表

### 认证
- POST /api/v1/auth/login — 手机号密码登录
- POST /api/v1/auth/logout — 退出登录
- GET  /api/v1/auth/me — 当前用户信息

### 患者数据（需JWT）
- GET  /api/v1/users/me — 获取我的信息
- PUT  /api/v1/users/me — 更新我的信息
- GET  /api/v1/followup/templates — 获取问卷模板
- GET  /api/v1/followup/records — 获取随访记录
- POST /api/v1/followup/records — 提交随访
- GET  /api/v1/medicine — 获取用药列表
- POST /api/v1/medicine — 添加用药
- PUT  /api/v1/medicine/{id} — 更新用药
- DELETE /api/v1/medicine/{id} — 删除用药
- GET  /api/v1/reports — 获取检查报告

### 管理员
- GET  /api/v1/admin/audit — 查询审计日志
- GET  /api/v1/admin/audit/export — 导出合规报告

### AI
- POST /api/v1/ai/chat — FMT科普问答
- POST /api/v1/ai/interpret-report — 检查报告解读

## 数据库Schema

详见：/workspace/projects/deepfmt-xinchuang/docs/openGauss-schema.md

## 目录结构

```
src/main/java/com/deepfmt/
├── DeepFmtApplication.java
├── config/SecurityConfig.java
├── controller/AuthController.java
├── controller/AuditController.java
├── service/AuthService.java
├── service/AuditService.java
├── entity/FmtUser.java
├── entity/FmtAuditLog.java
├── repository/UserRepository.java
├── repository/AuditLogRepository.java
├── dto/ApiResponse.java
├── dto/LoginRequest.java
├── dto/LoginResponse.java
├── security/JwtTokenProvider.java
├── security/JwtAuthFilter.java
└── encrypt/Sm4Util.java
```
