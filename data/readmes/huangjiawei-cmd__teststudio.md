# TestStudio — 学生管理系统原型

一个现代化的学生管理系统开源原型，采用 **Vue 3 + Spring Boot 3 + MyBatis** 构建，提供学生、课程、成绩、考勤、仪表盘和系统设置等核心页面，并内置 H2 演示数据以降低本地启动门槛。

> 当前版本定位为 UI / 构建链路 / API 原型验证，不是生产级校园管理系统。完整 RBAC、真实成绩录入、高并发选课、Redis、批量导入导出等能力仍在路线图中。

## 项目亮点

- macOS 风格桌面化 UI：毛玻璃窗口、侧栏、Dock、状态栏
- 学生管理：学生档案、筛选、状态标签和编辑入口
- 课程管理：课程卡片、教师、学分、容量和剩余名额
- 成绩分析：GPA、及格率、优秀率、趋势和学业预警
- 考勤事务：今日考勤、迟到、旷课、请假与审批信息
- 仪表盘：学生/教师/课程统计、院系分布、趋势和待办事项
- 系统设置：角色、字典、日志、定时任务、院系专业和备份入口
- 双数据库模式：默认 H2 内存库快速演示，同时提供 MySQL 8 初始化 SQL

## 技术栈

### Frontend

- Vue 3
- Vite 5
- Vue Router
- Pinia

### Backend

- Java 17
- Spring Boot 3.2
- MyBatis
- Maven
- H2（默认演示）
- MySQL 8（可选）

## 项目结构

```text
teststudio/
├── frontend/        Vue 3 前端
│   ├── src/
│   └── package.json
├── backend/         Spring Boot API
│   ├── src/
│   └── pom.xml
├── database/        MySQL 示例 DDL
├── requirements.md  需求摘要
├── BUILD_REPORT.md  构建验证记录
└── README.md
```

## 快速开始

### 环境要求

- Node.js 18+
- npm 9+
- Java 17+
- Maven 3.8+

### 1. 启动后端

```bash
cd backend
mvn spring-boot:run
```

默认使用 H2 内存数据库，无需提前安装 MySQL。

后端默认地址：

```text
http://localhost:8080
```

示例 API：

```text
GET http://localhost:8080/api/dashboard/summary
```

### 2. 启动前端

新开一个终端：

```bash
cd frontend
npm install
npm run dev
```

然后访问 Vite 输出的本地地址，通常是：

```text
http://localhost:5173
```

> 前端依赖不会提交到 Git 仓库。首次运行必须先执行 `npm install`。

## 构建

### Frontend

```bash
cd frontend
npm install
npm run build
```

构建产物位于 `frontend/dist/`。

### Backend

```bash
cd backend
mvn -DskipTests package
```

构建产物位于 `backend/target/`。

## 使用 MySQL

项目默认使用 H2 方便快速演示。如果需要切换到 MySQL：

1. 创建 MySQL 8 数据库。
2. 执行 `database/mysql-schema.sql`。
3. 根据本地环境修改 `backend/src/main/resources/application-mysql.yml`。
4. 使用对应 Spring Profile 启动后端。

请不要把真实数据库密码、Token 或其他密钥提交到仓库。

## 当前验证状态

本项目已完成以下构建验证：

- 前端生产构建：通过
- Spring Boot Maven 打包：通过
- 后端 H2 启动：通过
- `GET /api/dashboard/summary`：返回成功

更详细的验证记录见 [`BUILD_REPORT.md`](BUILD_REPORT.md)。

## 路线图

- [ ] 完整学生信息 CRUD 与分页查询
- [ ] 课程与选课业务闭环
- [ ] 成绩录入、统计与导出
- [ ] RBAC 权限体系
- [ ] Excel 导入导出
- [ ] Redis 缓存和高并发选课保护
- [ ] MySQL 完整数据模型与迁移
- [ ] 前后端自动化测试
- [ ] Docker Compose 一键运行
- [ ] CI 构建与检查

## 贡献

欢迎 Issue、Bug Report、功能建议和 Pull Request。提交代码前请阅读 [`CONTRIBUTING.md`](CONTRIBUTING.md)。

## 安全

发现安全问题时，请不要在公开 Issue 中粘贴凭据、Token、生产数据或其他敏感信息。具体建议见 [`SECURITY.md`](SECURITY.md)。

## License

本项目采用 [MIT License](LICENSE)。

