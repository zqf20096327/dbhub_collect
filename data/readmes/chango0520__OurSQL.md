# 学生管理系统 (Student Management System)

基于 **Vue 3 + Django REST Framework + openGauss** 的全栈学生信息管理系统，实现学生、教师、课程、成绩四大核心模块的增删改查，并提供成绩统计分析、挂科预警、排名计算等数据算法功能。

---

## 目录

- [技术栈](#技术栈)
- [系统功能总览](#系统功能总览)
- [项目结构](#项目结构)
- [数据库设计](#数据库设计)
- [后端 API 接口](#后端-api-接口)
- [算法模块](#算法模块)
- [前端页面及路由](#前端页面及路由)
- [快速启动](#快速启动)
- [开发说明](#开发说明)

---

## 技术栈

| 层级 | 技术 | 版本 |
|---|---|---|
| **前端框架** | Vue 3 (Composition API) | ^3.5 |
| **前端路由** | Vue Router | ^5.0 |
| **HTTP 请求** | Axios | ^1.18 |
| **构建工具** | Vite | ^8.0 |
| **后端框架** | Django | 5.2 |
| **API 框架** | Django REST Framework | 3.17 |
| **数据库** | openGauss (PostgreSQL 兼容模式) | — |
| **数据库适配** | 自定义 `db_backends.opengauss` | — |
| **科学计算** | NumPy | ^2.2 |
| **跨域支持** | django-cors-headers | ^4.9 |
| **筛选支持** | django-filter | ^25.2 |

---

## 系统功能总览

### 1. 基础数据管理（CRUD）

| 模块 | 功能 |
|---|---|
| **学生管理** | 增删改查学生信息（学号、姓名、性别、出生日期、班级、学院、入学年份、联系电话），支持分页、关键词搜索（姓名/学号）、多条件筛选（学院/班级/性别/入学年份） |
| **教师管理** | 增删改查教师信息（工号、姓名、性别、职称、学院、电话、邮箱），支持分页、搜索、筛选（学院/职称/性别） |
| **课程管理** | 增删改查课程信息（课程号、课程名、学分、学时、授课教师、开课学期），支持分页、搜索、筛选（授课教师/学期） |
| **成绩管理** | 成绩录入、编辑、删除；一节课号/学号筛选查询。**特殊：同一学生同一课程只保留一条成绩**（`unique_together` 约束） |

### 2. 特色功能

| 功能 | 说明 |
|---|---|
| **批量成绩录入** | 选定课程后，一次性录入多名学生的成绩，已存在的自动更新 |
| **课程成绩统计** | 统计某课程的总人数、平均分、最高/低分、中位数、标准差、及格率、分数段分布及占比直方图 |
| **课程排名** | 某课程内所有学生排名（含百分位），支持取前 N 名 |
| **班级及格率** | 按班级统计各课程参考人数、及格人数、及格率、平均分及总体及格率 |
| **挂科预警** | 基于挂科学分评估风险等级（高/中/低），结果按挂科学分降序排列 |
| **GPA 计算** | 百分制→4.0 绩点转换及加权 GPA 计算 |
| **仪表盘** | 首页展示学生/教师/课程/成绩四类数据总数 + 快速入口链接 |

### 3. 前端设计风格

- **Editorial Minimalism（编辑极简主义）**
- 零第三方 UI 库（无 Element Plus），全部原生 HTML + CSS
- 无卡片、无阴影、无外边框，排版即设计
- 左导航 + 右内容区的双栏布局
- 页面切换淡入上浮动画

---

## 项目结构

```
student-management-system/
├── .gitignore                   # Git 忽略规则
├── README.md                    # 本文件
│
├── backend/                     # Django 后端
│   ├── manage.py                # Django 项目管理入口
│   ├── requirements.txt         # Python 依赖清单
│   ├── test.bat                 # Windows 快速测试脚本
│   ├── sms/                     # Django 项目配置
│   │   ├── settings.py          # 主配置 (openGauss)
│   │   ├── settings_test.py     # 测试配置 (SQLite)
│   │   ├── urls.py              # 全局路由
│   │   └── wsgi.py              # WSGI 入口
│   ├── apps/                    # Django 应用
│   │   ├── students/            # 学生管理
│   │   │   ├── models.py        # Student 模型
│   │   │   ├── serializers.py   # 序列化器（含校验）
│   │   │   ├── views.py         # StudentViewSet
│   │   │   ├── urls.py          # 路由注册
│   │   │   ├── stats.py         # 统一统计接口
│   │   │   └── tests.py         # 单元测试
│   │   ├── teachers/            # 教师管理
│   │   │   ├── models.py
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   └── urls.py
│   │   ├── courses/             # 课程管理
│   │   │   ├── models.py
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   └── urls.py
│   │   └── scores/              # 成绩管理
│   │       ├── models.py
│   │       ├── serializers.py   # (含批量录入序列化器)
│   │       ├── views.py         # (含批量/统计/预警/排名接口)
│   │       └── urls.py
│   ├── algorithm/               # 算法模块
│   │   ├── __init__.py          # 模块导出
│   │   ├── analysis.py          # 成绩统计 & 排名
│   │   ├── warning.py           # 挂科预警
│   │   └── utils.py             # GPA & 及格率工具
│   └── db_backends/             # 数据库后端适配
│       └── opengauss/
│           ├── __init__.py
│           └── base.py          # openGauss 适配器
│
└── frontend/                    # Vue 3 前端
    ├── index.html               # HTML 入口
    ├── vite.config.js           # Vite 配置
    ├── package.json             # NPM 依赖
    ├── eslint.config.js         # ESLint 配置
    ├── jsconfig.json            # JS 配置 (路径别名)
    ├── .editorconfig            # 编辑器规范
    ├── .gitattributes           # Git 属性
    ├── .oxlintrc.json           # Oxlint 配置
    ├── public/
    │   └── favicon.ico
    └── src/
        ├── main.js              # Vue 应用入口
        ├── App.vue              # 根组件 (布局 + 导航)
        ├── assets/
        │   └── main.css         # 全局样式 (设计令牌)
        ├── router/
        │   └── index.js         # 路由配置 (14 条路由)
        ├── api/                 # Axios API 封装
        │   ├── request.js       # 请求实例 (拦截器/错误处理)
        │   ├── student.js
        │   ├── teacher.js
        │   ├── course.js
        │   ├── score.js
        │   └── analysis.js      # 统计/预警/排名 API
        ├── components/          # 通用组件
        │   ├── SearchBar.vue
        │   ├── TablePagination.vue
        │   ├── Toast.js         # 通知组件
        │   └── ConfirmDialog.js # 确认弹窗
        ├── utils/
        │   ├── format.js        # 格式化工具
        │   └── validation.js    # 表单校验
        └── views/               # 页面组件
            ├── Dashboard.vue    # 仪表盘
            ├── student/
            │   ├── StudentList.vue
            │   └── StudentForm.vue
            ├── teacher/
            │   ├── TeacherList.vue
            │   └── TeacherForm.vue
            ├── course/
            │   ├── CourseList.vue
            │   └── CourseForm.vue
            ├── score/
            │   ├── ScoreList.vue
            │   ├── ScoreBatchInput.vue
            │   └── ScoreQuery.vue
            └── analysis/
                ├── CourseStats.vue     # 课程成绩统计
                ├── PassRate.vue        # 班级及格率
                └── WarningList.vue     # 挂科预警
```

---

## 数据库设计

### 实体关系

```
Student (1) ────< Score >──── (1) Course
                      │
                 (1) Teacher
```

一个学生可选多门课程 → `Score` 关联表；一门课程由一位教师授课。

### 表结构

#### `student` — 学生表

| 字段 | 类型 | 说明 |
|---|---|---|
| `stu_id` | VARCHAR(20) PK | 学号 |
| `name` | VARCHAR(50) | 姓名 |
| `gender` | CHAR(1) | `M` 男 / `F` 女 |
| `birth_date` | DATE | 出生日期 |
| `class_name` | VARCHAR(50) | 班级 |
| `college` | VARCHAR(100) | 学院 |
| `enroll_year` | INTEGER | 入学年份 |
| `phone` | VARCHAR(20) | 联系电话 |
| `created_at` | DATETIME | 创建时间 |
| `updated_at` | DATETIME | 更新时间 |

#### `teacher` — 教师表

| 字段 | 类型 | 说明 |
|---|---|---|
| `teacher_id` | VARCHAR(20) PK | 工号 |
| `name` | VARCHAR(50) | 姓名 |
| `gender` | CHAR(1) | 性别 |
| `title` | VARCHAR(50) | 职称（教授/副教授/讲师等） |
| `college` | VARCHAR(100) | 学院 |
| `phone` | VARCHAR(20) | 联系电话 |
| `email` | VARCHAR(100) | 邮箱 |
| `created_at` | DATETIME | 创建时间 |

#### `course` — 课程表

| 字段 | 类型 | 说明 |
|---|---|---|
| `course_id` | VARCHAR(20) PK | 课程号 |
| `course_name` | VARCHAR(100) | 课程名 |
| `credit` | DECIMAL(3,1) | 学分 |
| `hours` | INTEGER | 学时 |
| `teacher_id` | VARCHAR(20) FK → teacher | 授课教师 |
| `semester` | VARCHAR(20) | 开课学期 |
| `created_at` | DATETIME | 创建时间 |

#### `score` — 成绩表

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | AUTO PK | 自增主键 |
| `stu_id` | VARCHAR(20) FK → student | 学号 |
| `course_id` | VARCHAR(20) FK → course | 课程号 |
| `score` | DECIMAL(5,2) | 成绩（0–100） |
| `exam_date` | DATE | 考试日期 |
| `created_at` | DATETIME | 创建时间 |
| | UNIQUE(stu_id, course_id) | 同一学生同一课程仅一条记录 |

---

## 后端 API 接口

统一前缀：`/api/v1/`

统一响应格式：`{ "code": 200, "message": "success", "data": {...} }`

### 学生管理

| 方法 | 路径 | 说明 |
|---|---|---|
| `GET` | `/students/` | 学生列表（分页 `?page=1&page_size=10`，搜索 `?search=`，筛选 `?college=&class_name=&gender=&enroll_year=`，排序 `?ordering=stu_id`） |
| `GET` | `/students/{stu_id}/` | 单个学生详情 |
| `POST` | `/students/` | 新增学生（校验：学号≥6位，电话必须为数字） |
| `PUT` | `/students/{stu_id}/` | 全量更新 |
| `PATCH` | `/students/{stu_id}/` | 部分更新 |
| `DELETE` | `/students/{stu_id}/` | 删除学生 |
| `GET` | `/students/count/` | 学生总数 |

### 教师管理

| 方法 | 路径 | 说明 |
|---|---|---|
| `GET` | `/teachers/` | 教师列表（搜索 `?search=`，筛选 `?college=&title=&gender=`） |
| `GET` | `/teachers/{teacher_id}/` | 单个教师详情 |
| `POST` | `/teachers/` | 新增教师 |
| `PUT` | `/teachers/{teacher_id}/` | 全量更新 |
| `PATCH` | `/teachers/{teacher_id}/` | 部分更新 |
| `DELETE` | `/teachers/{teacher_id}/` | 删除教师 |
| `GET` | `/teachers/count/` | 教师总数 |

### 课程管理

| 方法 | 路径 | 说明 |
|---|---|---|
| `GET` | `/courses/` | 课程列表（搜索 `?search=`，筛选 `?teacher_id=&semester=`） |
| `GET` | `/courses/{course_id}/` | 单个课程详情 |
| `POST` | `/courses/` | 新增课程 |
| `PUT` | `/courses/{course_id}/` | 全量更新 |
| `PATCH` | `/courses/{course_id}/` | 部分更新 |
| `DELETE` | `/courses/{course_id}/` | 删除课程 |
| `GET` | `/courses/count/` | 课程总数 |

### 成绩管理

| 方法 | 路径 | 说明 |
|---|---|---|
| `GET` | `/scores/` | 成绩列表（筛选 `?stu_id=&course_id=`） |
| `POST` | `/scores/` | 录入一条成绩 |
| `PUT` | `/scores/{id}/` | 更新成绩 |
| `DELETE` | `/scores/{id}/` | 删除成绩 |
| `GET` | `/scores/count/` | 成绩记录总数 |

### 特色接口

| 方法 | 路径 | 说明 |
|---|---|---|
| `POST` | `/scores/batch/` | **批量录入** — 请求体 `{ "course_id": "...", "scores": [{"stu_id": "...", "score": "85.5"}, ...] }`。已存在的记录自动更新（`update_or_create`） |
| `GET` | `/scores/course-stats/{course_id}/` | **课程成绩统计** — 返回平均分、最高/低分、中位数、标准差、及格率、分数段分布及占比直方图 |
| `GET` | `/scores/ranking/{course_id}/` | **课程排名** — 所有学生排名及百分位，`?top_n=10` 取前 N 名 |
| `GET` | `/scores/pass-rate/` | **班级及格率** — 各课程及格率及总体及格率，`?class_name=计科2101` 筛选班级 |
| `GET` | `/scores/warning/` | **挂科预警** — `?threshold=60&min_credits=10` 控制及格线和风险阈值，返回高/中/低风险学生列表 |
| `GET` | `/stats/` | **统一统计** — 一次性返回学生/教师/课程/成绩四类数据总数（仪表盘使用） |

---

## 算法模块

`backend/algorithm/` 基于 NumPy 实现，与 API 接口解耦，可直接作为独立库使用。

### `analysis.py` — 成绩统计与排名

| 函数 | 说明 |
|---|---|
| `compute_course_stats(scores)` | 课程成绩分布统计：人数、平均分、最高/低分、中位数、标准差、及格率、五段分布及直方图 |
| `compute_rank(scores, target_stu_id)` | 单个学生在某课程中的排名及百分位 |
| `batch_compute_ranks(scores, top_n)` | 批量计算所有学生排名，可选仅返回前 N 名 |

### `warning.py` — 挂科预警

| 函数 | 说明 |
|---|---|
| `compute_warning(scores_with_credits, threshold, min_credits)` | 聚合所有学生挂科信息，按未通过学分划分风险等级：高（≥ `min_credits` 学分）、中（≥ `min_credits * 0.5` 学分）、低（其余），结果降序排列 |
| `compute_student_warning_detail(student_scores, threshold)` | 单个学生挂科详情及挂科占比 |

### `utils.py` — 工具函数

| 函数 | 说明 |
|---|---|
| `score_to_gpa(score)` | 百分制→4.0 绩点转换（90+ → 4.0, 80+ → 3.0, …） |
| `compute_gpa(scores_with_credits)` | 加权平均绩点（GPA）计算 |
| `compute_class_pass_rate(scores, threshold)` | 班级各课程及格率统计及总体及格率 |

---

## 前端页面及路由

| 路由 | 页面 | 功能 |
|---|---|---|
| `/` | **Dashboard** | 仪表盘 — 展示四类数据总数 + 快速入口 |
| `/students` | StudentList | 学生列表 — 分页表格 + 关键词搜索 + 学院筛选 |
| `/students/new` | StudentForm | 新增学生表单 |
| `/students/:id` | StudentForm | 编辑学生表单（props 传递学号） |
| `/teachers` | TeacherList | 教师列表 — 分页 + 搜索 + 筛选 |
| `/teachers/new` | TeacherForm | 新增教师 |
| `/teachers/:id` | TeacherForm | 编辑教师 |
| `/courses` | CourseList | 课程列表 — 分页 + 搜索 + 筛选 |
| `/courses/new` | CourseForm | 新增课程 |
| `/courses/:id` | CourseForm | 编辑课程 |
| `/scores` | ScoreList | 成绩列表 — 按学号/课程号筛选 |
| `/scores/batch` | ScoreBatchInput | 批量录入成绩 — 先选课程，再逐行录入 |
| `/scores/query` | ScoreQuery | 成绩高级查询 |
| `/analysis/course/:id` | CourseStats | 课程成绩统计 — 展示统计指标 + 分布直方图 |
| `/analysis/pass-rate` | PassRate | 班级及格率 — 按班级查看各课程及格率 |
| `/analysis/warning` | WarningList | 挂科预警 — 可调阈值，展示风险列表 |

### 前端 API 封装

`frontend/src/api/` 下的五个模块封装了全部后端接口：

- `request.js` — Axios 实例，配置 `baseURL: http://localhost:8000/api/v1/`，自动解包响应 `data`，统一错误处理（Toast 通知）
- `student.js` — `getStudents`, `getStudent`, `createStudent`, `updateStudent`, `patchStudent`, `deleteStudent`, `getStudentCount`
- `teacher.js` — `getTeachers`, `getTeacher`, `createTeacher`, `updateTeacher`, `patchTeacher`, `deleteTeacher`, `getTeacherCount`
- `course.js` — `getCourses`, `getCourse`, `createCourse`, `updateCourse`, `patchCourse`, `deleteCourse`, `getCourseCount`
- `score.js` — `getScores`, `createScore`, `updateScore`, `deleteScore`, `batchCreateScores`, `getScoreCount`
- `analysis.js` — `getStats`, `getCourseStats`, `getCourseRanking`, `getClassPassRate`, `getWarningList`

---

## 快速启动

### 前置要求

- Python ≥ 3.10
- Node.js ≥ 20.19
- openGauss 数据库（或 PostgreSQL）

### 1. 后端启动

```bash
# 进入后端目录
cd backend

# 安装依赖
pip install -r requirements.txt

# 修改 sms/settings.py 中的数据库配置
# ⚠ 将 DATABASES 改为你自己的 openGauss 连接信息

# 数据库迁移
python manage.py makemigrations
python manage.py migrate

# 启动开发服务器 (默认 :8000)
python manage.py runserver 0.0.0.0:8000
```

> **本地测试**：可使用 SQLite 快速验证功能。编辑 `sms/settings.py`，注释掉 openGauss 配置、取消注释 SQLite 配置即可。

### 2. 前端启动

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器 (默认 :5173)
npm run dev
```

### 3. 访问系统

打开浏览器访问 `http://localhost:5173`

---

## 开发说明

### openGauss 适配

`backend/db_backends/opengauss/base.py` 继承 Django 的 PostgreSQL 后端，通过重写 `check_database_version_supported()` 跳过版本检查（openGauss 版本号与 PostgreSQL 不同）。直接配置 `ENGINE: 'db_backends.opengauss'` 即可使用。

### 配置分离

- **`settings.py`** — 生产/开发配置（openGauss）
- **`settings_test.py`** — 测试环境配置（SQLite），配合 `test.bat` 脚本快速运行单元测试

### 单元测试

```bash
cd backend
python manage.py test --settings=sms.settings_test
```

涵盖 Student CRUD 和 Algorithm 统计接口的测试用例。

### 响应约定

所有 API 统一返回格式：

```json
{
  "code": 200,
  "message": "success",
  "data": { ... }
}
```

前端 `request.js` 的响应拦截器自动解包，业务代码直接拿到 `data` 内容。错误时拦截器自动弹出 Toast 通知。

### 前端设计原则

- **零第三方 UI 库** — 全部组件原生 HTML + CSS，减少依赖体积
- **Editorial Minimalism** — 去除装饰性容器，排版即设计
- **自建通知/弹窗** — `Toast.js` 和 `ConfirmDialog.js` 替代 Element Plus 的 `ElMessage` / `ElMessageBox`
- **`$route.fullPath` 作 key** — 确保路由间切换强制重新创建组件，避免表单页面不触发 `onMounted`
