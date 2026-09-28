# 高校教务管理系统

数据库课程设计项目，基于 **Qt 6.8.3 + openGauss/GaussDB** 的桌面端教务管理系统。

## 关于本项目

本项目是 **2025-2026-3 数据库系统课程设计** 的课程作业，实现了一个完整的高校教务管理系统（ChenjhMIS）。系统采用 Qt 6.8.3 开发桌面客户端，通过 QPSQL 驱动直连 openGauss/GaussDB 数据库，支持学生、教师、管理员三种角色的登录与操作。

- **数据库设计**：包含学生、教师、课程、学院、专业、班级、地区、学期、开课、选课成绩等核心表，以及视图、索引、触发器、存储过程等数据库对象
- **创新点**：基于角色的权限控制、成绩修改留痕日志、存储过程统一成绩录入入口、触发器自动维护学生已修学分
- **界面设计**：Fusion 风格 + QSS 自定义样式，蓝白教务主题，支持中文字段筛选

## 技术栈

| 类别 | 技术 |
|------|------|
| 前端框架 | Qt 6.8.3 Widgets (MinGW 64-bit) |
| 编程语言 | C++17 |
| 数据库 | openGauss / GaussDB |
| 数据库驱动 | QPSQL |
| 构建工具 | qmake + mingw32-make |
| 界面方案 | Fusion 风格 + QSS 样式表 |

## 功能概览

系统支持三种角色登录，不同角色拥有不同功能权限：

### 学生端
- 查看个人基本信息
- 成绩分析（课程学分、成绩、等级、是否及格、绩点、学分绩点）
- 个人排名查看
- 学业预警

### 教师端
- 查看本人任课课程
- 成绩录入与修改（通过存储过程 `proc_Chenjh_Innov_RecordGrade11`）
- 课程统计（通过存储过程 `proc_Chenjh_Innov_CourseStatistics11`）
- 查看成绩修改日志

### 管理员端
- 维护 13 张基础数据表（学生、教师、课程、学院、专业、班级、地区、学期等）
- 用户账号管理（创建、重置密码、启用/停用）
- 查看全部统计视图和业务视图
- 重算学生已修学分

## 项目结构

```
数据库课程设计/
├── ChenjhQtMIS/               # Qt 主程序
│   ├── src/                   # 源代码
│   │   ├── main.cpp           # 程序入口
│   │   ├── MainWindow.*       # 主窗口（导航 + 页面容器）
│   │   ├── LoginDialog.*      # 登录窗口
│   │   ├── ConnectionDialog.* # 数据库连接配置
│   │   ├── DatabaseManager.*  # 数据库连接管理（单例）
│   │   ├── AuthService.*      # 认证服务
│   │   ├── TablePage.*        # 通用 CRUD 表维护页
│   │   ├── QueryPage.*        # 只读查询视图页
│   │   ├── GradeEntryPage.*   # 教师成绩录入页
│   │   ├── AccountPage.*      # 管理员用户管理页
│   │   └── ...
│   ├── sql/                   # SQL 脚本
│   ├── resources/             # 图标资源
│   ├── ui-demos/              # UI 原型（HTML 静态方案）
│   ├── tests/                 # 单元测试
│   ├── release/               # 编译发布目录（含可执行文件）
│   └── ChenjhQtMIS.pro        # qmake 项目文件
```

## 构建与运行

### 环境要求

- Qt 6.8.3（MinGW 64-bit）
- PostgreSQL/openGauss 客户端库（`libpq.dll`）
- Windows 10/11

### 构建

```powershell
cd ChenjhQtMIS
$env:PATH='D:\Qt\Tools\mingw1310_64\bin;D:\Qt\6.8.3\mingw_64\bin;' + $env:PATH
& 'D:\Qt\6.8.3\mingw_64\bin\qmake.exe' ChenjhQtMIS.pro
& 'D:\Qt\Tools\mingw1310_64\bin\mingw32-make.exe'
```

生成的可执行文件位于 `ChenjhQtMIS/release/ChenjhQtMIS.exe`。

### 发布打包

```powershell
cd ChenjhQtMIS
powershell -NoProfile -ExecutionPolicy Bypass -File .\deploy-release.ps1
```

打包后位于 `ChenjhQtMIS/dist/ChenjhQtMIS/ChenjhQtMIS.exe`，可直接双击运行。

### 从脚本启动（自动补齐运行库路径）

```powershell
cd ChenjhQtMIS
powershell -NoProfile -ExecutionPolicy Bypass -File .\run-ChenjhQtMIS.ps1
```

### 运行测试

```powershell
cd ChenjhQtMIS
$env:PATH='D:\Qt\Tools\mingw1310_64\bin;D:\Qt\6.8.3\mingw_64\bin;' + $env:PATH
cd tests
& 'D:\Qt\6.8.3\mingw_64\bin\qmake.exe' tests.pro
& 'D:\Qt\Tools\mingw1310_64\bin\mingw32-make.exe'
cd ..
.\tests\release\tst_core.exe
```

## 数据库连接

启动程序后会先进入数据库连接配置窗口。默认连接参数如下：

| 参数 | 默认值 |
|------|--------|
| 主机 | 192.168.174.128 |
| 端口 | 26000 |
| 数据库 | ChenjhMIS11 |
| 用户名 | cjh_mis11 |
| Schema | cjh_mis11 |
| 密码 | CourseDesign@2026#11 |

连接成功后配置会被记住，下次启动自动连接；连接失败则弹出配置窗口。

## 默认账号

首次登录时程序会自动创建账号表并补齐默认账号：

| 角色 | 用户名 | 密码 |
|------|--------|------|
| 管理员 | admin | admin123 |
| 学生 | 学号 | 123456 |
| 教师 | 教师编号 | 123456 |

也可手动执行 `ChenjhQtMIS/sql/09_app_accounts.sql` 创建账号表和初始账号。

## 数据库能力对象

- `Chenjh_V_GradeAnalysis11`：成绩自动派生视图，显示是否及格、绩点、学分绩点
- `Chenjh_V_StudentRank11`：学生综合排名视图
- `Chenjh_V_AcademicWarning11`：学业预警视图
- `Chenjh_GradeChangeLogs11`：成绩修改日志表
- `Chenjh_CourseStatisticsResult11`：课程统计结果表
- `proc_Chenjh_Innov_RecordGrade11`：教师成绩录入存储过程
- `proc_Chenjh_Innov_CourseStatistics11`：课程统计存储过程
- 触发器自动维护学生已修学分（`cjh_TotalCredits11`）
