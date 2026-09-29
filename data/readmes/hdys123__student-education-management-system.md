# 学生教务管理系统

这是一个面向数据库课程设计场景的学生教务管理系统，使用 `openGauss` 作为数据库，后端使用 `Node.js + Express`，前端使用原生 `HTML / CSS / JavaScript`。系统围绕“院系、教师、学生、课程、教学安排、选课、成绩、报表”建立完整业务链路，并实现了基于角色的权限控制。

后端会直接托管前端静态页面，因此本项目启动后只需要访问一个地址即可使用完整系统。

```text
http://localhost:3000
```

## 技术栈

- 数据库：openGauss
- 后端：Node.js、Express、opengauss.js / pg
- 前端：原生 HTML、CSS、JavaScript
- 鉴权：JWT
- 本地调试：支持真实数据库模式和 mock 内存数据模式

## 项目结构

```text
student-education-management-system/
├─ backend/
│  ├─ sql/
│  │  ├─ schema.sql              # 数据库表结构
│  │  └─ seed.sql                # 初始数据
│  ├─ src/
│  │  ├─ app.js                  # Express 应用入口
│  │  ├─ server.js               # 服务启动入口
│  │  ├─ config/                 # 数据库配置
│  │  ├─ middleware/             # 鉴权、错误处理
│  │  ├─ mock/                   # MOCK_DB=true 时使用的内存数据服务
│  │  ├─ routes/                 # 各业务 API
│  │  ├─ scripts/                # 数据库初始化/迁移辅助脚本
│  │  └─ utils/                  # 通用工具
│  └─ package.json
├─ frontend/
│  ├─ index.html                 # 页面结构
│  ├─ styles.css                 # 页面样式
│  ├─ app.js                     # 前端业务逻辑
│  └─ package.json
├─ .gitignore
└─ README.md
```

## 核心功能

- 用户登录、注册、JWT 会话管理
- 系统管理员管理用户账号
- 教务管理员按所属学院管理本学院教师、学生、课程、教学安排和选课
- 院系信息查看与系统管理员维护
- 教师查看自己的任课安排，并查看选自己课程的学生
- 教师为自己课程中的学生录入成绩
- 学生查看自己的学籍、课程和成绩报表
- 教师、学生、课程、选课数据查询筛选
- 教师和学生批量导入
- 按班级批量选课
- CSV 导出
- 头像、个人资料和密码修改
- 中英文界面切换
- 侧边栏收起
- 角色化顶部导航
- 必填字段红色星号提示
- 统一错误提示、保存反馈、删除反馈和登录过期提示
- mock 模式下无需数据库也可演示主要流程

## 角色与权限

### system_admin：系统管理员

系统管理员负责平台级账号和基础院系信息维护。

可用模块：

- 总览
- 用户管理
- 院系管理
- 教师管理
- 学生管理
- 报表查询

主要权限：

- 创建、编辑、禁用、删除登录账号
- 创建、编辑、删除院系信息
- 查看教师、学生、报表
- 不直接负责课程、教学安排和选课业务

### academic_admin：教务管理员

教务管理员必须属于某一个学院，系统通过 `users.department_id` 保存其所属学院，并按该学院进行数据范围控制。

可用模块：

- 总览
- 院系管理
- 教师管理
- 学生管理
- 课程管理
- 教学安排
- 选课管理
- 报表查询

主要权限：

- 只能查看自己的学院信息，不能修改学院信息
- 只能查看和维护本学院教师
- 只能查看和维护本学院学生
- 只能查看和维护本学院课程
- 只能给本学院学生办理选课
- 支持班级批量选课
- 支持教师和学生批量导入
- 创建教师或学生时，如果没有填写初始密码，系统会默认使用教师编号或学号作为初始密码

### teacher：教师

教师只能访问与自己授课相关的数据。

可用模块：

- 总览
- 教师
- 学生
- 课程
- 教学安排
- 选课管理
- 报表查询

主要权限：

- 查看自己的教师档案
- 查看自己的教学安排
- 只能查看选了自己课程的学生
- 只能查看自己课程相关选课记录
- 只能给自己课程中的学生录入成绩
- 可以修改自己的账号资料和密码

### student：学生

学生只查看自己的数据，不能自行选课。

可用模块：

- 总览
- 学生
- 课程
- 报表查询

主要权限：

- 查看自己的学籍信息
- 查看课程信息
- 查看自己的成绩报表
- 可以修改自己的账号资料和密码
- 不能自行选课，选课只能由教务管理员操作

## 数据库设计概览

系统核心表如下：

- `departments`：院系信息
- `users`：登录账号、角色、联系方式、头像、状态、所属学院
- `teachers`：教师档案，与 `users` 一对一关联
- `students`：学生档案，与 `users` 一对一关联
- `courses`：课程信息
- `teaching_assignments`：课程任课安排
- `enrollments`：选课、成绩、修读状态

主要关系：

- 一个院系可以拥有多个教师、学生、课程
- 一个用户账号可以绑定一个教师档案或学生档案
- 一个课程可以配置多个教学安排
- 一个选课记录关联学生、课程，并可关联具体教学安排
- 教师查看学生时，通过 `enrollments -> teaching_assignments -> teachers` 限定为“选了自己课程的学生”

## 运行方式

### 1. 安装依赖

```powershell
cd .\backend
npm install
```

前端是静态页面，没有构建依赖。如果只做语法检查，可进入 `frontend` 执行：

```powershell
cd .\frontend
npm run check
```

### 2. 配置后端环境变量

在 `backend/.env` 中配置数据库连接。示例：

```env
PORT=3000
DB_HOST=127.0.0.1
DB_PORT=5432
DB_NAME=student_education_db
DB_USER=opengauss
DB_PASSWORD=your_password
DB_SSL=false
JWT_SECRET=replace_with_a_long_random_secret
MOCK_DB=false
```

如果暂时没有 openGauss，可设置：

```env
MOCK_DB=true
```

mock 模式下系统会使用内存数据，适合本地演示和前端调试。

### 3. 初始化数据库

先在 openGauss 中创建数据库：

```sql
CREATE DATABASE student_education_db;
```

然后执行建表和种子数据：

```powershell
gsql -d student_education_db -U gaussdb -W -f .\backend\sql\schema.sql
gsql -d student_education_db -U gaussdb -W -f .\backend\sql\seed.sql
```

也可以使用后端脚本：

```powershell
cd .\backend
npm run db:init
```

如果是从旧版本数据库升级，还可以执行：

```powershell
npm run db:ensure-scope
```

该脚本会补齐教务管理员学院字段相关结构与默认数据。

### 4. 启动服务

```powershell
cd .\backend
npm start
```

访问：

```text
http://localhost:3000
```

健康检查：

```text
http://localhost:3000/api/health
http://localhost:3000/api/health/db
```

当 `MOCK_DB=true` 时，`/api/health/db` 会返回 mock 模式信息。

## 初始账号

真实数据库种子数据中包含以下管理端账号：

```text
系统管理员：admin / Admin@123
教务管理员：academic / Academic@123
```

说明：

- `admin` 是系统管理员账号。
- `academic` 是教务管理员账号，默认绑定计算机学院。
- 教师和学生账号可通过注册页创建，也可由管理员在管理端创建。
- 教务管理员创建教师或学生时，如果没有填写密码，教师默认密码为教师编号，学生默认密码为学号。

## 质量检查命令

后端：

```powershell
cd .\backend
npm run check
```

前端：

```powershell
cd .\frontend
npm run check
```

目前检查内容主要是 JavaScript 语法检查，确保主要前后端文件都可以被 Node 正常解析。

## 待改进问题解决情况

以下问题来自 `C:\Users\30205\Desktop\数据库-待改进.docx`。目前均已处理。

| 序号 | 待改进问题 | 是否已解决 | 解决说明 |
| --- | --- | --- | --- |
| 1 | 应增加批量导入功能，如创建师生账号、某班级全部学生选课 | 已解决 | 已增加教师批量导入、学生批量导入、班级批量选课。前端支持粘贴 JSON、CSV/TSV 文本或选择 CSV/TSV 文件；后端逐行校验并返回成功/失败明细。班级批量选课会按班级名查找本学院学生并生成选课记录。 |
| 2 | 选课只能由教务管理员操作，学生无法自行选课 | 已解决 | 前端学生导航中不展示选课管理入口，后端选课新增、批量选课、删除接口只允许 `academic_admin`。学生只能查看自己的课程与成绩，不能提交选课操作。 |
| 3 | 教务管理员不应修改学院信息；应只能查看本学院师生、课程，即教务管理员应具有学院属性 | 已解决 | `users` 表增加 `department_id`，教务管理员账号绑定学院。后端通过 `departmentScope` 工具限制教师、学生、课程、教学安排、选课、报表等数据范围。院系编辑按钮只对系统管理员显示，教务管理员只能查看自己的学院。 |
| 4 | 教师应只能查看选自己课的学生 | 已解决 | 学生查询接口对教师角色增加关联过滤，只返回通过 `enrollments -> teaching_assignments -> teachers` 与当前教师关联的学生。mock 接口也实现了同样逻辑。 |
| 5 | 上方栏目应根据当前角色选择性展示 | 已解决 | 前端增加 `roleNavigation` 配置，不同角色只显示自己可用的功能模块。系统管理员、教务管理员、教师、学生的顶部模块均已区分。 |
| 6 | 必填字段要有红色星号 `*` | 已解决 | 前端表单渲染增加 `data-required-label` 标记，CSS 使用红色星号展示必填字段。登录、注册和动态业务表单均已覆盖主要必填项。 |
| 7 | 左边栏应可以收起 | 已解决 | 页面增加侧边栏收起按钮，收起状态保存到 `localStorage`，刷新后仍保留用户选择。移动端也做了适配。 |
| 8 | 若教务管理员在创建师生时没有设置初始密码，师生无法登录 | 已解决 | 后端创建教师时密码为空则默认使用教师编号，创建学生时密码为空则默认使用学号。前端表单也增加提示说明。mock 模式保持一致。 |
| 9 | 师生应可修改自己的密码 | 已解决 | 账号设置页支持所有登录角色修改个人资料和密码。新增“确认新密码”字段，两次输入不一致时前端阻止提交。后端 `/api/auth/me` 支持当前用户更新自己的密码。 |
| 10 | 部分文本表述不准确 | 已解决 | 已根据当前权限模型修正文案，例如院系仅系统管理员可修改、教务管理员仅管理本学院、教师只能处理自己课程等，避免界面说明和实际权限不一致。 |
| 11 | 部分英文在中文模式下无法译为中文 | 已解决 | 已补齐课程、选课、成绩、报表、表单字段、状态、角色、按钮、提示等多处翻译键，减少中文模式下的英文硬编码。 |

## 近期额外完善

除了 `docx` 中列出的问题，还进一步做了以下完善：

- 保存表单时禁用按钮，避免重复提交。
- 保存、删除、错误提示统一在模块操作区反馈，减少浏览器 `alert`。
- 登录过期时自动清除本地会话并提示重新登录。
- 网络异常时显示更友好的提示。
- 表格显示当前记录数。
- 表格和表单输出增加 HTML 转义，降低输入内容破坏页面的风险。
- 后端将数据库唯一键、外键、检查约束错误转换成更友好的业务提示。
- 选课时增加课程容量校验，防止超过课程容量。
- 选课时校验教学安排必须属于所选课程。
- 成绩录入限制成绩范围为 0 到 100，绩点范围为 0 到 5。
- 新增 `.gitignore`，忽略 `node_modules`、日志、环境变量等不应提交的文件。
- 增加 `npm run check` / `npm test`，便于交付前做基础检查。

## 主要接口说明

### 认证

- `POST /api/auth/login`：登录
- `POST /api/auth/register`：注册教师或学生账号
- `GET /api/auth/me`：获取当前用户信息
- `PUT /api/auth/me`：修改当前用户资料、头像和密码

### 用户与基础资料

- `GET /api/users`：系统管理员查询用户
- `POST /api/users`：系统管理员创建用户
- `PUT /api/users/:id`：系统管理员更新用户
- `DELETE /api/users/:id`：系统管理员删除用户
- `GET /api/departments`：查询院系
- `POST /api/departments`：系统管理员创建院系
- `PUT /api/departments/:id`：系统管理员更新院系
- `DELETE /api/departments/:id`：系统管理员删除院系

### 教师、学生、课程

- `GET /api/teachers`：查询教师
- `POST /api/teachers`：创建教师
- `POST /api/teachers/batch`：批量导入教师
- `GET /api/students`：查询学生
- `POST /api/students`：创建学生
- `POST /api/students/batch`：批量导入学生
- `GET /api/courses`：查询课程
- `POST /api/courses`：教务管理员创建本学院课程

### 教学安排、选课与成绩

- `GET /api/assignments`：查询教学安排
- `POST /api/assignments`：教务管理员创建教学安排
- `GET /api/enrollments`：查询选课记录
- `POST /api/enrollments`：教务管理员创建选课记录
- `POST /api/enrollments/batch`：教务管理员班级批量选课
- `PUT /api/enrollments/:id/score`：教务管理员或任课教师录入成绩
- `DELETE /api/enrollments/:id`：教务管理员删除选课记录

### 报表

- `GET /api/reports/student-scores`：学生成绩明细
- `GET /api/reports/course-selection`：课程选课统计
- `GET /api/dashboard`：首页统计
- `GET /api/lookups`：前端表单下拉数据

## 使用建议

推荐按以下顺序演示系统：

1. 使用 `admin / Admin@123` 登录，查看用户管理和院系管理。
2. 使用系统管理员创建或确认教务管理员账号已绑定学院。
3. 使用 `academic / Academic@123` 登录，创建本学院教师、学生、课程。
4. 创建教学安排，将课程分配给教师。
5. 使用选课管理为单个学生选课，或使用班级批量选课。
6. 使用教师账号登录，查看自己的教学安排和选自己课的学生。
7. 教师录入成绩。
8. 使用学生账号登录，查看自己的课程和成绩报表。

## 注意事项

- 真实数据库模式下，需要先保证 openGauss 服务可用，并正确配置 `backend/.env`。
- mock 模式数据保存在内存中，服务重启后会恢复初始 mock 数据。
- 教务管理员必须绑定学院，否则后端会拒绝其访问需要学院范围的数据。
- 删除院系、课程、教师、学生等记录时，如果已有业务数据关联，数据库外键可能阻止删除，系统会返回友好提示。
- 公开注册页仍支持教师和学生注册；管理端也支持管理员创建教师和学生账号。课程设计演示时可以根据需要选择其中一种账号创建方式。
