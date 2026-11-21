# 轻享图文

> 项目名暂定「轻享图文」，后续可能改名。  
> 《JAVA框架技术(一)》小组课程项目：SSM 企业级 CMS + UGC 图文社区。

## 文档

| 文档 | 内容 |
|---|---|
| [产品需求与业务说明书](docs/产品需求与业务说明书.md) | M1 范围、角色、业务规则、验收场景 |
| [开发规范](docs/开发规范.md) | SSM 技术基线、六表 RBAC、AOP 权限、增量开发、质量门禁 |
| [接口文档](docs/接口文档.md) | REST API、请求响应、错误码、模块归属 |
| [模块划分与分工](docs/模块划分与分工.md) | 三人模块、全流程交付物、增量顺序与核对触发 |
| [UIUX-小红书](docs/UIUX-小红书.md) | 小红书 Web 设计 DNA、令牌、布局、组件 |
| [开发文档模板](docs/开发文档-模板.md) | 每人开发文档的固定结构 |
| [扩展脑暴](docs/扩展脑暴.md) | M2/M3 推荐、深色主题、治理方向 |

## 三人模块

| 成员 | 模块 | 核心表 |
|---|---|---|
| A | 账号、权限与治理 | `sys_user` / `sys_role` / `sys_permission` / `operation_log` / `notification` |
| B | 内容、分类与审核 | `article` / `category` |
| C | 互动、关注与分发 | `article_like` / `article_favorite` / `comment` / `user_follow` / `reader_feedback` |

每人独立负责一个模块，从需求、库表、接口、后端、JSP、测试到文档完整走一遍；完成后必须提交 `docs/开发文档-成员X.md`。

## 开发模式：增量开发

- 每个增量是一个**可运行、可测试、可演示**的垂直切片：表 + 接口 + 页面 + 测试 + 文档。
- 按依赖顺序切片，**不设固定周期**：切片 1 骨架/CRUD；切片 2 状态机/审核/评论/关注；切片 3 页面/联调/通知；切片 4 测试/答辩。
- **触发式核对**：切片完成、契约变更、合并前、跨模块阻塞、答辩前，跑一次全量 `mvn clean test` + 主链路演示。
- `main` 始终保持可启动；不提交 stub、TODO、假数据；没做完不合 `main`。
- 每个增量结束更新自己的 `docs/开发文档-成员X.md`「增量记录」。

## 仓库协作

- 远端：<https://github.com/JFT-Group/QingXiangTuWen>
- 组员上手教程（clone / push / PR，不需要 gh CLI）：[Git 协作图](docs/guide/git-clone-push.png)
- 集成分支：`main`
- 个人分支：`feat/a-*`、`feat/b-*`、`feat/c-*`
- 合并前：`git pull --rebase origin main`；禁止 force push `main`
- 共享文件（`pom.xml`、`config/**`、`Result`、`app.css`、`接口文档.md`）由 owner 合并，其他人提 PR

## 技术基线

JDK 17 + Spring 5.3.31 + Spring MVC + MyBatis 3.5.15 + MyBatis-Plus 3.5.5 + MySQL + JSP/JSTL + Tomcat 9 + Maven war。

工程骨架复用 MonaHub 的 SSM 全注解三件套；**UI/UX 按小红书 Web 浅色设计 DNA**，不再沿用 MonaHub 视觉。

## 快速开始

```bash
mvn -B clean test
mvn -B -Prun package cargo:run
# http://127.0.0.1:18080/qingxiang/
```

首次运行前：依次执行 `sql/01_core.sql`、`sql/02_content.sql`、`sql/04_seed.sql`、
`sql/04_seed_b.sql`、`sql/05_creator_permissions.sql`；复制
`src/main/resources/common/db.properties.example` 为 `db.properties` 并填本机 MySQL 密码。

### 用 IDEA 运行（组员机器）

本项目是标准 Maven war，IDEA 的 Tomcat 只是另一种启动方式。**不要和本机 `cargo:run` 同时开**，两者抢 18080 和同一个 context。

前置：JDK 17、**Tomcat 9.0.x**（不能用 10/11，jakarta 不兼容）、MySQL 已初始化。

**IDEA Ultimate（有 Tomcat 集成）**

1. 打开项目根目录（`pom.xml`），等 Maven 导入完成。
2. `Project Structure` → SDK 选 JDK 17，Language level 17。
3. `Run` → `Edit Configurations` → `+` → `Tomcat Server` → `Local`。
4. `Application server` 指向 Tomcat 9.0.86 的安装目录；HTTP port 用 `18080`。
5. `Deployment` → `+` → `Artifact` → `qingxiang:war exploded`；Application context 填 `/qingxiang`。
6. 启动后访问 `http://127.0.0.1:18080/qingxiang/`。

没有 `qingxiang:war exploded` 时：`Project Structure` → `Artifacts` → `+` → `Web Application: Exploded` → `From Modules` → 选 `qingxiang`。

**IDEA Community（没有 Tomcat 集成）**

- 推荐直接用 `mvn -Prun cargo:run`（与本机脚本同一套），IDEA 只负责写代码；或
- 装 `Smart Tomcat` 插件：Tomcat home 选 9.0.86，Context path `/qingxiang`，部署模块选 `qingxiang`。

端口可以改成 8080，但文档、截图、curl 统一按 18080；JSP 页面同源访问不受端口影响。

## 课程约束

- 六张核心表 + 物理外键/索引；Spring AOP 接口权限；MyBatis-Plus 高级特性；RESTful + ApiFox。
- 保留 AI 交互与修改痕迹；禁止复制完整 AI 项目或开源项目。
