# LifyMIS08 — 高校宿舍管理系统

> 08组 · 数据库系统课程设计 · Spring Boot + Thymeleaf + openGauss

## 技术栈

| 层级 | 技术 |
|------|------|
| 框架 | Spring Boot 2.7.6 |
| 模板引擎 | Thymeleaf |
| 数据库 | openGauss (PG 9.2 兼容) |
| 数据库访问 | Spring JDBC (JdbcTemplate) |
| 连接池 | HikariCP |
| 前端 | Bootstrap 5.3 + Bootstrap Icons |
| 构建工具 | Maven |
| JDK | Java 8+ |

## 功能模块

| 模块 | 功能 |
|------|------|
| 🏠 控制台 | 统计卡片、卫生排名、入住率、楼栋综合统计 |
| 👤 学生管理 | CRUD + 搜索 + 住宿状态联动 |
| 🏢 楼栋管理 | CRUD |
| 🛏️ 宿舍管理 | CRUD + 查看入住学生 |
| 👨‍💼 管理员管理 | CRUD + 楼栋关联 |
| 🔑 住宿管理 | 入住 / 退宿 / 转宿（调用存储过程） |
| ⚡ 电费管理 | 生成电费单 / 缴费（含存储过程） |
| 🔧 报修管理 | 提交报修 / 处理 / 状态跟踪 |
| 🧹 卫生管理 | 检查记录 / 排名 |
| 📋 综合登记 | 晚归 / 借钥匙 / 访客 / 寄存 |

## 数据库设计

- **11 张表**：Student, Building, Dormitory, Manager, LiveIn, ElectricFee, Payment, Repair, Hygiene, Register, OperationLog
- **6 个视图**：住宿视图、入住率视图、卫生排名视图、报修统计视图、欠费视图、当月电费视图
- **6 个触发器**：自动更新入住人数、宿舍状态、电费计算、缴费标记等
- **6 个存储函数**：入住、退宿、转宿、批量生成电费、缴费、楼栋统计

## 快速开始

### 1. 配置数据库

设置环境变量（不要在配置文件中硬编码密码）：

```bash
export DB_URL=jdbc:postgresql://your_host:26000/lifymis08
export DB_USERNAME=your_username
export DB_PASSWORD=your_password
```

> Windows (CMD): `set DB_URL=...`  
> IDEA: Run → Edit Configurations → Environment variables

### 2. 初始化数据库

在 openGauss 中依次执行：
1. `LifyMIS08_建表脚本.sql`
2. `LifyMIS08_触发器存储过程.sql`

### 3. 启动应用

```bash
mvn spring-boot:run
```

访问 http://localhost:8080

## 项目结构

```
src/main/java/com/lify/mis08/
├── DormitoryApplication.java    # 启动类
├── config/WebConfig.java        # MVC 配置
├── controller/                  # 12 个 Controller
│   ├── IndexController.java     # 首页仪表盘
│   ├── StudentController.java   # 学生 CRUD
│   ├── BuildingController.java  # 楼栋 CRUD
│   ├── DormitoryController.java # 宿舍 CRUD
│   ├── ManagerController.java   # 管理员 CRUD
│   ├── LiveInController.java    # 住宿管理（含存储过程）
│   ├── ElectricFeeController.java # 电费管理
│   ├── PaymentController.java   # 缴费管理
│   ├── RepairController.java    # 报修管理
│   ├── HygieneController.java   # 卫生管理
│   ├── RegisterController.java  # 综合登记
│   └── LoginController.java     # 登录页
└── entity/                      # 10 个实体类
```

## License

Course project — for educational purposes.
