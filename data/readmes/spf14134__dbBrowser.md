# DB Browser - 数据库浏览器

一款全栈 Web 数据库管理工具，支持多数据库连接管理、SQL 查询编辑、Excel 导入导出和数据库对象浏览。

## 技术栈

- **后端**: Java 8 + Spring Boot 2.7.18 + Undertow + Spring Security + JWT
- **前端**: React 18 + Vite 5 + Ant Design 5
- **数据库**: H2（嵌入式文件数据库，存储连接配置和查询历史）
- **通信加密**: AES-CBC 加密前后端 API 通信
- **构建工具**: Maven + Vite

## 快速启动

### 后端

```bash
cd dbBrowser-backend
mvn spring-boot:run
# 或在 Windows 下使用
mvnw.cmd spring-boot:run
```

服务启动于 http://localhost:8080

### 前端（开发模式）

```bash
cd dbBrowser-frontend
npm install
npm run dev
```

前端开发服务器启动于 http://localhost:5173

### 构建完整 JAR 包

```bash
# 1. 构建前端
cd dbBrowser-frontend
npm install
npm run build

# 2. 将 dist/ 内容复制到后端静态资源目录
cp -r dist/* ../dbBrowser-backend/src/main/resources/static/

# 3. 构建后端 JAR
cd ../dbBrowser-backend
mvn package -DskipTests

# 4. 运行
java -jar target/db-browser-backend-1.0.0.jar
```

### 默认登录

- 用户名: `admin`
- 密码: `admin`

## 功能特性

- **多数据库连接管理**: 支持 MySQL、PostgreSQL、Oracle、SQL Server、达梦及自定义 JDBC 连接
- **动态驱动加载**: 通过上传 JAR 包动态加载 JDBC 驱动，自动扫描检测驱动类
- **SQL 查询编辑器**: 语法高亮、历史记录、结果分页展示
- **Excel 导入导出**: 基于 Apache POI 流式处理，支持大数据量导出
- **数据库元数据浏览**: 查看表结构、列信息、主键、外键、视图
- **AES 加密通信**: 前后端 API 全程加密，保障敏感信息安全
- **JWT 认证**: 无状态 Token 认证

## 项目结构

详见 [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md)。
