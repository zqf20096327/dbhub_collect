# 学生选课管理系统

[English](README.en.md)

基于 Spring Boot、Thymeleaf、Layui、MyBatis 与 openGauss 实现的学生选课管理系统。系统采用服务端渲染页面，提供管理员、教师和学生三类角色的选课业务流程；邮件验证码注册与学生 AI 助手为可选功能。

> 本仓库只开源前端页面、后端业务代码、MyBatis 数据库接口与无数据建表脚本。不包含生产数据库、历史用户数据、默认可登录账号、服务器地址、部署记录、SSH 私钥、Cookie、邮箱授权码或 AI 密钥。

## 系统预览

以下截图来自本地历史演示环境，仅用于展示页面效果；截图中的姓名、课程、账号和统计数字均不随仓库提供，也不能用于登录。

| 管理员：课程管理 | 管理员：公告管理 |
| --- | --- |
| ![管理员课程管理](docs/images/table1-local-admin-course.png) | ![管理员公告管理](docs/images/coursefix-local-information-final.png) |

| 学生：选课中心 | 教师：课程信息 |
| --- | --- |
| ![学生选课中心](docs/images/table1-local-student-courseCase.png) | ![教师课程信息](docs/images/teacher-course-card-local-desktop.png) |

## 功能简介

### 管理员

- 菜单与角色权限管理。
- 学院、教师、学生和课程信息管理。
- 课程学年、课程容量、授课教师、上课时间与地点维护。
- 首页公告的发布、编辑与删除。
- 对教师、学生和课程数据进行分页查询、编辑与删除。

### 教师

- 查看本人授课课程及课程详情。
- 查看选修某门课程的学生。
- 录入和修改学生成绩、学分备注。
- 查看课程、选课与成绩相关统计信息。
- 查看个人资料。

### 学生

- 注册、登录和邮箱验证码验证。
- 浏览可选课程，按学院、课程类别和关键词筛选。
- 执行选课、退课，查看已选课程。
- 查看个人选课与成绩统计、个人资料。
- 使用可选的 AI 学业助手查询本人课程与选课信息。

## 技术栈

| 层次 | 使用技术 |
| --- | --- |
| 后端 | Java 11、Spring Boot 2.2、Spring MVC |
| 数据访问 | MyBatis、PageHelper、openGauss JDBC |
| 前端 | Thymeleaf、Layui、原生 JavaScript、CSS |
| 数据库 | openGauss 5.x |
| 可选服务 | SMTP 邮件验证码、DeepSeek 兼容 Chat Completions API |

## 项目结构与前后端接口

本项目不是前后端分离项目：Thymeleaf 模板负责渲染页面，页面通过 Ajax 调用同一 Spring Boot 服务中的 JSON 接口。接口实现集中在 `src/main/java/com/kzl/controller/`，页面位于 `src/main/resources/templates/`，对应的 Mapper SQL 位于 `src/main/resources/mybatis/`。

| 业务模块 | 页面与接口前缀 | 主要能力 |
| --- | --- | --- |
| 登录与会话 | `/`、`/manage/login`、`/teacher/login`、`/student/login`、`/logout` | 三类角色登录、退出、登录后跳转 |
| 注册 | `/register`、`/register/studentRegister`、`/register/teacherRegister`、`/common/email/sendCode` | 学生/教师注册、邮箱验证码发送与校验 |
| 管理端 | `/manage/**` | 菜单、学院、公告、教师、学生、角色的页面和 CRUD 接口 |
| 课程管理 | `/course/**` | 课程、课程学年、授课教师、选课容量的查询和维护 |
| 教师端 | `/teacher/**` | 课程列表、学生名单、成绩维护、统计、个人资料 |
| 学生端 | `/student/**` | 选课中心、选课/退课、已选课程、统计、个人资料 |
| AI 助手（可选） | `/student/ai/chat`、`/student/ai/history`、`/student/ai/conversation` | 当前登录学生的课程上下文问答与会话记录 |

接口返回统一使用 `com.kzl.util.Result`。需要登录的接口依赖服务端 Session；使用浏览器或其他客户端调用时应保留登录请求返回的 `JSESSIONID` Cookie。

## 数据库接口

数据库访问接口位于 `src/main/java/com/kzl/dao/`，每个接口对应 `src/main/resources/mybatis/` 下的 XML 映射文件。连接信息只来自环境变量，不会写入源代码。

| 数据表 | 对应 Mapper | 用途 |
| --- | --- | --- |
| `manage_user`、`teacher`、`student` | `LoginMapper`、`ManageMapper`、`RegisterMapper` | 三类用户的登录、注册与资料维护 |
| `role`、`menu`、`role_menu_rel` | `ManageMapper` | 角色、菜单与权限关系 |
| `college`、`information` | `ManageMapper` | 学院信息与公告 |
| `course`、`course_academic_year` | `CourseMapper`、`StudentMapper`、`TeacherMapper` | 课程、学年与教师授课信息 |
| `student_course_rel` | `StudentMapper`、`TeacherMapper` | 学生选课、退课与成绩记录 |
| `email_verify_code` | `EmailVerifyCodeMapper` | 注册邮箱验证码 |
| `student_ai_conversation`、`student_ai_message` | `StudentAiMapper` | AI 助手会话及消息记录 |

完整空库表结构见 [sql/openGauss_schema.sql](sql/openGauss_schema.sql)。该脚本只有 `CREATE TABLE`、`CREATE INDEX`，不含任何 `INSERT`、账号、密码或个人数据，也不会删除既有表。

### 初始化说明

1. 创建一个空的 openGauss 数据库，例如 `oasys`。
2. 使用数据库管理员或具有建表权限的账号执行建表脚本：

```bash
gsql -h localhost -p 26000 -U your_database_user -d oasys -f sql/openGauss_schema.sql
```

3. 本仓库不附带种子数据。要完成登录和完整业务演示，请自行编写初始化脚本创建首个管理员、学院、角色、菜单、用户、课程和学年数据；首个管理员创建完成后，再通过管理端继续维护这些数据。

## 配置

复制 [.env.example](.env.example) 中的变量名称，在系统环境变量、IDE Run Configuration 或部署平台中填写实际值。`.env` 文件仅是参考格式，Spring Boot 默认不会自动读取它。

### 必填：数据库

| 环境变量 | 示例 | 说明 |
| --- | --- | --- |
| `DB_URL` | `jdbc:postgresql://localhost:26000/oasys` | openGauss JDBC 地址 |
| `DB_USERNAME` | `your_database_user` | 数据库用户名 |
| `DB_PASSWORD` | `your_database_password` | 数据库密码 |
| `SERVER_PORT` | `8088` | 可选，Web 服务端口 |

PowerShell 示例：

```powershell
$env:DB_URL = 'jdbc:postgresql://localhost:26000/oasys'
$env:DB_USERNAME = 'your_database_user'
$env:DB_PASSWORD = 'your_database_password'
$env:SERVER_PORT = '8088'
```

### 可选：邮件与 AI

| 功能 | 变量 | 说明 |
| --- | --- | --- |
| 邮箱验证码 | `MAIL_HOST`、`MAIL_PORT`、`MAIL_USERNAME`、`MAIL_PASSWORD`、`MAIL_PROTOCOL` | SMTP 服务及邮箱授权码 |
| AI 助手 | `DEEPSEEK_BASE_URL`、`DEEPSEEK_MODEL`、`DEEPSEEK_API_KEY` | 兼容 Chat Completions 的服务地址、模型和密钥 |

未配置 AI 密钥时，AI 接口会返回“服务尚未配置”；未配置邮件服务时，邮箱验证码发送会失败，但不影响其他已配置的系统功能。

## 本地启动

### 1. 准备环境

- JDK 11
- Maven 3.6 或更高版本
- openGauss 5.x，并完成上面的建库建表和环境变量配置

### 2. 构建并运行

```bash
mvn clean package -DskipTests
java -jar target/springboot-student.jar
```

浏览器打开：`http://localhost:8088/`。

如端口冲突，设置 `SERVER_PORT`，或直接追加参数：

```bash
java -jar target/springboot-student.jar --server.port=18088
```


## 许可证

本项目沿用 [木兰宽松许可证，第 2 版](LICENSE)。
