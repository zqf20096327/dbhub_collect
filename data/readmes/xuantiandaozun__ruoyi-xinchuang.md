# XCRuoYi

面向信创环境的管理后台。操作员使用的仍是用户、部门、角色、菜单、字典、参数、日志和系统监控；数据库按达梦 DM8 编写，而不是只换一个 JDBC 驱动。

基于 [RuoYi-Vue](https://gitee.com/y_project/RuoYi-Vue)（MIT）的改造思路，包名与模块独立。Powered by RuoYi。

## 界面

本机达梦上的管理端：登录、工作台、用户和角色。

| 登录 | 工作台 |
|:---:|:---:|
| ![登录](docs/images/login.jpg) | ![工作台](docs/images/workbench.jpg) |

| 用户 | 角色 |
|:---:|:---:|
| ![用户](docs/images/user.jpg) | ![角色](docs/images/role.jpg) |

操作过程：

![登录到用户、角色与日志](docs/images/demo.gif)

## 能做什么

- 在达梦上使用熟悉的用户 / 部门 / 角色 / 菜单权限模型
- 按支持矩阵核对 JDK、数据库、操作系统是否可进现场
- 同一套代码可打 `jar`（内嵌 Tomcat）或 `war`（预留东方通）

开源范围是适配能力与这套管理后台，不包含行业业务模块，也不包含在线代码生成器。边界见 [开源与商业](docs/boundaries.md)。

## 技术栈

| 项 | 选择 |
|---|---|
| JDK | 开发 11；现场使用毕昇 / Dragonwell / 麒麟 JDK |
| 后端 | Spring Boot 2.7.18 |
| ORM | MyBatis-Plus |
| 前端 | Vue 3 + Element Plus |
| 数据库 | 达梦 DM8（主线） |
| 运行 | `jar` + 内嵌 Tomcat；可打 `war` |

已验证与未验证的组合以 [支持矩阵](docs/support-matrix.md) 为准，不要把「进行中」当成已支持。

## 当前状态

本机达梦上已能登录，用户 / 部门 / 角色 / 菜单 / 字典 / 参数 / 日志 / 系统监控与权限、分页已点验。开源版不提供 Docker Compose 和麒麟冒烟；现场实施前请先对照支持矩阵。

## 环境要求

- JDK 11、Maven 3.8+
- Node.js 18+
- 达梦 DM8 实例（需自行准备；驱动使用现场 `drivers/jdbc` 下与库同系列的 jar，本机开发包为 `DmJdbcDriver8`）

达梦实例参数、JDBC 与 SCHEMA 约定见 [达梦约定](docs/dameng.md)。开发 JDK 不要写入交付清单，现场换国产 JDK。

## 初始化数据库

1. 用 SYSDBA 创建业务用户 `XC_ADMIN`（与 SCHEMA 同名），不要让应用使用 SYSDBA。
2. 用该用户执行 `sql/dm8/xc_admin.sql`。
3. 需要清空重导时，先执行 `sql/dm8/drop.sql`。

步骤与授权示例见 [sql/dm8/README.md](sql/dm8/README.md)。

导入后的默认管理员为 `admin` / `admin123`，请立即修改。

## 启动

```bash
# 后端（默认 dm profile）
mvn -pl xc-admin -am package
java -jar xc-admin/target/xc-admin-0.1.0-SNAPSHOT.jar

# 前端
cd xc-ui
npm install
npm run dev
```

- 管理端开发地址：http://localhost:5173
- 后端默认：http://localhost:8080

数据源见 `xc-admin/src/main/resources/application-dm.yml`。密码使用环境变量或已忽略的 `xc-admin/application-local.yml`，不要提交到仓库。`spring.profiles.active` 使用 `dm,local`（`local` 必须在后）。

## 文档

| 文档 | 内容 |
|---|---|
| [文档目录](docs/README.md) | 全部文档索引 |
| [支持矩阵](docs/support-matrix.md) | 已验证 / 进行中 / 不支持 |
| [达梦约定](docs/dameng.md) | 实例、JDBC、主键、SCHEMA |
| [SQL 方言](docs/sql-dialect.md) | 禁止的 MySQL 写法与替换 |
| [部署](docs/deploy.md) | 开发机 jar、WAR / TongWeb |
| [踩坑清单](docs/pitfalls.md) | 驱动、大小写、分页、字体 |
| [架构](docs/architecture.md) | 模块与适配层 |
| [开源边界](docs/boundaries.md) | 开源范围与定制范围 |

## 开源与定制

本仓库源码以 MIT 发布。Issue 用于可复现的缺陷、脚本导入失败和文档错误。

达梦或金仓整库迁移、麒麟 / 统信实施、东方通部署、国密与驻场等不在开源范围内，见 [开源边界](docs/boundaries.md)。

## 许可证

[MIT](LICENSE)。第三方与若依归属见 [NOTICE](NOTICE)。达梦数据库与 JDBC 驱动版权归达梦公司，使用须遵守其许可；本仓库不提供安装介质。
