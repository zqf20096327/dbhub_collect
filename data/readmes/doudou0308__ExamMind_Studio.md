# ExamMind Studio · 知衡

**AI 题库与智能考试平台 | Spring Boot + Vue 3 + DeepSeek**

基于 **Spring Boot + Vue 3 + MySQL** 的前后端分离考试系统，支持题库管理、在线考试、遗传算法组卷，以及 DeepSeek 辅助出题与学习分析。

这是一个可本地运行的 **Java 课程设计 / 数据库课程设计参考项目**，围绕“题库与考试系统”“在线考试系统”“智能组卷系统”实现管理员与学生两类角色的业务流程。适合学习 Spring Boot + Vue 前后端分离、JDBC 数据访问、遗传算法自动组卷、AI 出题及错题分析。

**English:** An AI-assisted online examination and question bank system built with Spring Boot, Vue 3 and MySQL. It includes genetic algorithm based test paper generation, DeepSeek question generation, wrong-answer analysis and student learning reports.

公开仓库只提供源码、空数据库表结构和项目说明，不包含真实学生资料、考试成绩、个人报告或原始提交包。课程设计的需求与代码对照见 [课程设计参考](docs/course-design.md)，架构与接口入口见 [系统设计](docs/architecture.md)。

## 🖼️ Demo / Screenshots

以下截图由项目原有 Vue 页面渲染，使用专门编写的虚构题目、演示账号和模拟成绩；不连接真实数据库或 DeepSeek，不代表真实 AI 响应。目前没有公开在线 Demo，可按下方步骤本地启动完整系统。

### 管理员题库管理

支持分类筛选、题目维护和 AI 出题入口。

![Spring Boot Vue 题库管理系统：题目列表、分类筛选与 AI 出题入口](docs/screenshots/question-management.png)

### 考试管理

管理考试状态、查看成绩与区分度，并导出 Excel。

![在线考试系统管理员界面：考试发布、状态管理、成绩分析与 Excel 导出](docs/screenshots/exam-management.png)

### 学生学习面板

展示待参加考试、错题本、学习统计与历次成绩趋势。

![学生在线考试界面：模拟考试、错题本、学习统计与成绩趋势](docs/screenshots/student-dashboard.png)

截图数据和复现步骤见 [截图说明](docs/screenshots/README.md)。

## 功能

| 角色 | 功能 |
| --- | --- |
| 管理员 | 题目增删改查、分类筛选、分页查询、学生管理与密码重置 |
| 管理员 | 手动选题、遗传算法自动组卷、考试发布与结束、答卷查看 |
| 管理员 | 题目区分度分析、Excel 成绩导出、AI 出题与题库知识 Wiki |
| 学生 | 限时答题、交卷与自动判分、历史答卷与成绩统计 |
| 学生 | 自主练习、错题筛选、AI 错题解析、已掌握标记与恢复 |
| 学生 | 个人知识图谱、掌握度展示、AI 学习周报 |

AI 功能需要自行配置 DeepSeek 密钥并承担相应 API 费用。不配置密钥时，题库与考试等基础功能仍可使用，AI 请求会提示未配置。

## 技术栈与结构

后端使用 Java 17、Spring Boot 2.7.18、JDBC、Druid 和 Apache POI；前端使用 Vue 3、TypeScript 和 Vite 5；数据库使用 MySQL 8。

```text
.
├── exam_web/
│   ├── backend/
│   │   ├── pom.xml
│   │   └── src/
│   │       ├── main/java/com/exam/
│   │       │   ├── config/        # 认证、权限与异常处理
│   │       │   ├── controller/    # REST API
│   │       │   ├── dao/           # JDBC 数据访问
│   │       │   ├── model/         # 实体模型
│   │       │   ├── service/       # AI 调用与判分
│   │       │   └── util/          # 数据库工具与遗传算法
│   │       ├── main/resources/    # 环境变量配置、空表初始化脚本
│   │       └── test/              # 配置与本地 HTTP 调用测试
│   └── frontend/                  # 页面、API 封装与全局状态
├── scripts/check_publication.py   # 公开文件检查
└── .github/workflows/ci.yml       # 后端、前端与脱敏检查
```

遗传算法默认使用 20 个个体、30 代进化、20% 精英保留和 10% 变异率，结合目标平均难度与分类覆盖评价试卷组合。个人“知识图谱”以知识点统计及 AI 生成的卡片呈现，未使用图数据库。

## 快速启动

### 1. 准备环境

- JDK 17，并确保 `JAVA_HOME` 指向该版本。
- Maven 3.8+。
- Node.js 20+ 与 npm。
- MySQL 8.0；使用有建库、建表和读写权限的开发数据库账号。

```sh
git clone https://github.com/doudou0308/ExamMind_Studio.git
cd ExamMind_Studio
```

### 2. 配置并启动后端

所有口令和 API Key 通过环境变量提供：

| 变量 | 默认值 | 用途 |
| --- | --- | --- |
| `DB_URL` | 本机 3306 端口的 `exam_web` 数据库 | JDBC URL，默认允许自动创建数据库 |
| `DB_USERNAME` | `root` | MySQL 用户名，建议替换为开发专用账号 |
| `DB_PASSWORD` | 空 | MySQL 密码，按本机环境设置 |
| `BOOTSTRAP_ADMIN_PASSWORD` | 空 | 新数据库初始化管理员时必填，至少 12 位 |
| `DEEPSEEK_API_KEY` | 空 | 可选，启用 AI 功能 |
| `DEEPSEEK_BASE_URL` | `https://api.deepseek.com` | 服务根地址，代码追加 `/v1/chat/completions` |
| `SERVER_PORT` | `8081` | 后端端口，变更时同步修改前端代理 |

PowerShell 示例，请替换示例口令：

```powershell
$env:DB_USERNAME = 'your_database_user'
$env:DB_PASSWORD = 'replace-with-your-database-password'
$env:BOOTSTRAP_ADMIN_PASSWORD = 'replace-with-a-unique-admin-password'
# 如需 AI 功能，再设置 $env:DEEPSEEK_API_KEY
Set-Location exam_web/backend
mvn spring-boot:run
```

macOS / Linux 示例：

```sh
export DB_USERNAME='your_database_user'
export DB_PASSWORD='replace-with-your-database-password'
export BOOTSTRAP_ADMIN_PASSWORD='replace-with-a-unique-admin-password'
cd exam_web/backend
mvn spring-boot:run
```

首次启动自动创建 9 张业务表，并在尚无 `admin` 账号时创建管理员；已有账号不会被覆盖。系统不自动创建学生或成绩数据，请登录管理员后添加测试学生。`BOOTSTRAP_ADMIN_PASSWORD` 不负责重置已有管理员密码。

表结构见 [init.sql](exam_web/backend/src/main/resources/init.sql)，仅包含建库建表语句，没有个人数据或账号种子。

如需文件配置，可自行在 `exam_web/backend/config/` 下创建 `application-local.yml` 并通过 Spring 的 local profile 启用（例如 `mvn spring-boot:run -Dspring-boot.run.profiles=local`）；该文件被 Git 忽略。Spring Boot 不会自动读取根目录 `.env`。

### 3. 启动前端

在新终端中，从仓库根目录执行：

```sh
cd exam_web/frontend
npm ci
npm run dev
```

访问 **http://localhost:3001**，使用 `admin` 和首次初始化时设置的密码登录。前端开发服务器将 `/api` 代理到 http://localhost:8081。管理员创建学生后，学生可从登录页选择账号，首次登录需要修改初始密码。

## 构建与验证

```sh
# 仓库根目录：扫描已纳入 Git 的文件
python scripts/check_publication.py

# 后端：编译、单元测试与打包，不访问真实数据库或 AI 服务
cd exam_web/backend
mvn verify
# 生成 target/exam-web-backend-1.0.0.jar

# 前端
cd ../frontend
npm ci
npm run build
```

CI 分别运行公开文件扫描、后端验证与前端构建。前端当前 `build` 是 Vite 构建，不包含独立 TypeScript 类型检查。数据库集成、完整考试流程与真实 AI 响应需在自行配置的开发环境验证。

## 数据与部署说明

- 仓库不携带真实姓名、学号、考试记录、成绩、个人文档和历史 ZIP。依赖目录、编译产物、IDE 配置及本地配置也被排除。
- 运行产生的数据保存在使用者自己的数据库中；本仓库不会同步原作者的本地数据库。
- AI 分析会将选中的题目及相关答题信息发送至配置的服务，请使用合成测试数据，或先按实际需要完成去标识处理。
- 当前实现面向课程学习：密码仍使用 MD5；学生创建/重置采用固定初始口令，Token 存在服务端内存且没有到期机制，登录页可读取学生名单，跨域配置较宽。正式部署前应改用现代密码哈希、短期会话及更严格的访问控制，详见 [SECURITY.md](SECURITY.md)。

## 常见问题

**能作为“题库与考试系统”或“在线考试系统”课程设计的学习参考吗？**

可以参考需求拆分、9 张业务表、前后端接口和角色流程，并根据自己的课程要求设计与验证扩展。项目更详细的功能范围与阅读顺序见 [课程设计参考](docs/course-design.md)。

**自动组卷使用什么算法？AI 出题和组卷是一回事吗？**

自动组卷可使用遗传算法，从已有题库中选择接近目标难度和分类要求的题目；AI 出题调用 DeepSeek 生成新的题目。这两个流程由不同模块实现。

**没有 DeepSeek Key 可以运行吗？需要 Redis 或 Docker 吗？**

基础题库和考试功能不依赖 AI Key；当前项目运行不要求 Redis 或 Docker。AI 出题、错题解析、知识 Wiki 与周报需要另外配置 DeepSeek。

**这是编程题在线判题系统（OJ）吗？**

本项目围绕题库与考试业务，不提供编程代码沙箱或 Java/C 代码编译判题；选择仓库时请按实际需求区分。

## 许可证

采用 [MIT License](LICENSE)。欢迎通过 Issue 反馈问题或提交 Pull Request。
