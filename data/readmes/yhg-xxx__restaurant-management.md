# 餐饮管理系统 restaurant-management

基于 **Spring Boot 3 + Vue 3 + openGauss** 的前后端分离餐饮管理系统，数据库采用国产开源数据库 openGauss，通过官方 JDBC 驱动接入。覆盖登录、桌台、菜品、点单、后厨制作、销售报表与图片上传等完整业务链路。

## 技术栈

| 层次 | 技术 |
| --- | --- |
| 后端 | Java 17、Spring Boot 3.5.3、Spring Data JPA / Hibernate、Hutool、Maven |
| 数据库 | openGauss，驱动 `org.opengauss:opengauss-jdbc:3.0.0`（`org.opengauss.Driver`） |
| 前端 | Vue 3、Vite 7、Vue Router 4、Element Plus、Axios、ECharts |
| 服务端口 | 后端 `8080`，前端 `5173`（Vite 默认） |

## 目录结构

```
restaurant-management/
├── restaurant-b/                 # 后端 Spring Boot 工程
│   ├── pom.xml
│   └── src/main/
│       ├── java/com/example/
│       │   ├── controller/       # REST 接口
│       │   ├── entity/           # JPA 实体（与数据库表一一对应）
│       │   ├── repository/       # 数据访问层
│       │   ├── dto/              # 请求 / 响应对象
│       │   ├── config/           # CORS 等配置
│       │   └── exception/        # 全局异常处理
│       └── resources/
│           ├── application.yaml              # 主配置（不含任何真实凭据）
│           └── application-local.yaml.example  # 本地配置模板
├── restaurant-f/                 # 前端 Vue 3 工程
│   └── src/
│       ├── components/           # 各业务页面
│       ├── router.js             # 路由
│       └── main.js               # axios baseURL 等全局配置
├── uploads/                      # 运行时上传的图片（不纳入版本管理）
└── .gitignore
```

## 功能模块

| 模块 | 说明 |
| --- | --- |
| 登录与个人信息 | 用户登录、资料查看、修改密码 |
| 桌台管理 | 桌台状态维护 |
| 菜品管理 | 菜品与分类维护、图片上传 |
| 订单管理 | 开单、加菜、订单明细与状态流转 |
| 菜品制作 | 后厨看板 |
| 销售报表 | 菜品销量排行、时段热力、分类销售额等（ECharts） |

## 快速开始

### 1. 准备数据库

创建 openGauss 数据库（示例中库名为 `rest`），并**按 `entity/` 下的实体定义预先建表**。项目使用 `spring.jpa.hibernate.ddl-auto: validate`，只校验不建表，且仓库中不含建表 SQL 脚本。涉及的表：

`categories`、`dishes`、`orders`、`order_details`、`tables`、`users`、`dish_sales`、`hourly_sales`

### 2. 配置连接

仓库中的 `application.yaml` 不含真实凭据，数据源通过占位符读取：

```
DB_URL       例如 jdbc:opengauss://localhost:5432/rest
DB_USER      数据库用户名
DB_PASSWORD  数据库密码
```

两种本地配置方式，任选其一：

- **本地配置文件（推荐）**：复制 `application-local.yaml.example` 为 `restaurant-b/src/main/resources/application-local.yaml`，填入真实值。该文件已被 `.gitignore` 忽略，不会提交。项目默认激活 `local` profile，放好后直接启动即可。
- **环境变量**：设置 `DB_URL` / `DB_USER` / `DB_PASSWORD`，环境变量优先级最高。若不想激活 `local` profile，可用 `SPRING_PROFILES_ACTIVE` 覆盖。

### 3. 启动后端

```bash
cd restaurant-b
mvn spring-boot:run
```

后端监听 `http://localhost:8080`。

### 4. 启动前端

```bash
cd restaurant-f
npm install
npm run dev
```

浏览器打开 `http://localhost:5173`（构建生产包用 `npm run build`）。

## 配置注意事项

- **跨域**：`CorsConfig.java` 只允许来源 `http://localhost:5173`；更换前端端口需同步修改。
- **接口地址**：`restaurant-f/src/main.js` 中 `axios.defaults.baseURL` 写死为 `http://localhost:8080`，部署到别处需要改成可配置项。
- **图片上传**：文件保存到启动目录下的 `uploads/`（运行时自动创建，单文件上限 5MB）；`FileUploadController` 返回的下载 URL 中 `localhost:8080` 为硬编码，远程部署需调整。
- **凭据安全**：请勿把真实密码、内网地址写进 `application.yaml`；只允许放进被忽略的 `application-local.yaml` 或环境变量。

## REST 接口概览

| 路径前缀 | 用途 |
| --- | --- |
| `/api/auth` | 登录认证 |
| `/api/users` | 用户与个人信息 |
| `/api/categories` | 菜品分类 |
| `/api/dishes` | 菜品管理 |
| `/api/tables` | 桌台管理 |
| `/api/orders` | 订单与明细 |
| `/api/sales` | 销售统计与报表数据 |
| `/api/files` | 图片上传与下载 |

## 说明

本项目为学习 / 课程实践用途，数据库表结构未随仓库提供，需要按实体类自行创建。欢迎按需扩展建表脚本、Docker 部署配置与单元测试。
