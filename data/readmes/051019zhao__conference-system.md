# 会议管理系统(数据库课程大作业 · 第一类)

基于 **openGauss + Spring Boot 3 + Vue 3 + Element Plus** 的会议管理系统,支持三角色(管理员/评审专家/投稿作者)的完整投稿-评审-录用流程。

> 本项目用于本地课程演示。演示账号、数据库密码和 JWT 默认值均为公开示例；如部署到可被他人访问的环境，先通过环境变量更换这些值，并启用真实邮件发送。

## 功能清单(对照大作业要求)

| 模块 | 功能 |
|---|---|
| 前台 | 首页(会议信息+统计+开幕倒计时+**投稿截止倒计时**)、征文通知、专家介绍(**真实头像**)、主旨报告、会议日程、录用论文(论文集公示、公开下载主稿或终稿)、通知公告、资料下载 |
| 注册登录 | 邮箱验证码注册 → **管理员审核(通过/拒绝)后方可登录**、忘记密码(邮箱重置)、个人中心(资料/密码/**头像上传**)、JWT 会话(**每请求实时校验账号状态**) |
| 作者端 | **草稿→编辑(含附件替换)→正式投稿**、多作者可排序、PDF 主稿≤20MB(**扩展名+魔数双重校验**)、**附属资料(zip/rar/7z 压缩包等,可随投稿一起上传,版本化账本 paper_file)**、待初审可撤回、录用后站内提示及邮件通知、上传终稿(**投稿/终稿截止日期由后端强制**) |
| 管理端-论文 | 初审、退稿、手动/自动分配评审专家(**校验启用状态+回避投稿人+去重**)、终审、分页、CSV 导出 |
| 管理端-用户 | 创建账号、**注册审核**、编辑(主旨专家标记)、禁用、重置密码、分页 |
| 管理端-内容 | 专题/主旨报告/日程/通知/资料管理、会议信息编辑(**三个重要日期**)、ECharts 仪表盘 |
| 专家端 | 评审任务、下载论文、**五维评分评审表**(契合度/创新性/完整性/深度/表达,1-5 星)+ 总评 + 结论 + 期刊推荐 |
| 审计 | 应用层操作日志(20+ 类动作,含 IP)与数据库触发器状态日志**双链路审计** |
| **AI 增强** | **①AI 论文预审**(智谱 GLM,异步生成落库 `ai_analysis` 表,五维评分建议+终审倾向,仅评审专家/管理员可见,对作者保密,人机协同定位);**②智能会议助手**(前台聊天窗,数据库事实注入的轻量 RAG,回答会期/截止/专题/流程);未配置 Key 时优雅降级不影响其他功能 |
| 并发安全 | 论文状态流转与评审提交全部采用 **CAS 条件更新**(WHERE 带原状态,影响行数为 0 即拒绝) |
| 数据库亮点 | 15 表、视图、触发器、CHECK/唯一约束(含 `(paper_id, sort_no)` 作者序唯一)、事务、索引、string_agg、**BYTEA 头像大对象** |
| 工程质量 | 统一响应/全局异常、参数校验、JWT 与录用发布单元测试、**全流程自动化冒烟测试**(`node scripts/smoke-test.mjs`)、Git 版本管理 |

## 环境要求

- JDK 17（可设置 `JAVA_HOME`；Windows 脚本也会搜索用户目录中的 JDK 17）
- Node.js 18+
- Docker Desktop(跑 openGauss)
- Maven 3.6+（可来自 PATH、`MAVEN_HOME` 或 IntelliJ IDEA 自带版本）

## 启动步骤

### 1. 启动 openGauss（先启动 Docker Desktop）

**Windows：** 直接运行下一步的 `scripts/run-backend.cmd`，脚本会自动启动或复用已有 `opengauss` 容器并等待就绪。

**Git Bash/Linux：** 在项目根目录执行：

```bash
bash setup-opengauss.sh
```

脚本会自动:启动容器 → 等待就绪 → 确保业务库存在 → 打印连接信息。
(GS_DB 环境变量会在首次初始化时自动创建 `conference_db`。)

**手动启动全新容器：**

```bash
docker run --name opengauss --privileged=true -d \
  -e GS_PASSWORD=Gauss@123 \
  -p 5432:5432 \
  -v opengauss_data:/var/lib/opengauss \
  opengauss/opengauss:5.0.0

docker exec -it opengauss gsql -d postgres -c "CREATE DATABASE conference_db ENCODING 'UTF8';"
```

### 2. 启动后端(backend/)

**方式一(Windows):** 启动 Docker Desktop 后运行 `scripts/run-backend.cmd`（自动启动或复用数据库容器、检测 JDK 17 和 Maven；可先运行 `scripts/run-backend.cmd --check`，日志输出在终端）

**8080 端口无法使用时：** 运行 `scripts/run-backend-docker.cmd`，后端会在 Docker 中启动并映射到本机 `http://localhost:18080`。此方式仍需本机 JDK 17 和 Maven 打包，首次使用需下载 `eclipse-temurin:17-jre` 镜像。随后正常运行 `scripts/run-frontend.cmd`，它会自动把 `/api` 代理到容器后端。

**方式二(IDEA):** 打开 `backend` 目录,Project SDK 选 JDK 17,运行 `ConferenceApplication`

- 首次启动会**自动建表(schema.sql,含审计日志表)+ 写入演示数据**(账号见下表);
- 后端地址:http://localhost:8080

> 若 `org.opengauss:opengauss-jdbc:5.1.0-og` 拉取失败,依次尝试版本 `6.0.0-og`、`5.0.2`;仍失败则到 opengauss.org 下载 jar,放入 `backend/lib/` 并把 pom 中该依赖改为 system 作用域。

### 3. 启动前端(frontend/)

**方式一(Windows):** `scripts/run-frontend.cmd`（需要 Node.js 与 npm 在 PATH 中，首次运行自动执行 `npm ci`）

**方式二(命令行):**

```bash
cd frontend
npm install
npm run dev
```

访问:http://localhost:5173 (本机后端默认代理到 8080，运行 Docker 后端时自动代理到 18080)

## 演示账号(首次启动自动创建)

| 角色 | 用户名 | 密码 |
|---|---|---|
| 管理员 | admin | Admin@123 |
| 评审专家 | expert01(张伟,方向:数据库,数据挖掘,机器学习) | Expert@123 |
| 评审专家 | expert02(李静,方向:自然语言处理,信息检索,大模型) | Expert@123 |
| 评审专家 | expert03(王强,方向:计算机视觉,深度学习) | Expert@123 |
| 投稿作者 | author01(陈晨) | Author@123 |

**建议演示路线**:author01 登录投稿(关键词写"数据库,查询优化"以命中自动分配)→ admin 登录后台"论文管理"初审通过 → 自动分配(会匹配张伟)→ expert01 登录填写评审 → admin 终审录用 → author01 查看意见并上传终稿。

## 注册验证码说明

默认 `app.mail-enabled=false`(不真实发邮件):点击"发送验证码"后,验证码会**弹窗直接显示**(同时打印在后端日志),方便本地联调。上线真实邮件:在 `application.yml` 配置 QQ 邮箱 SMTP 授权码并置 `mail-enabled: true`。
终审录用后作者在“我的投稿”页可看到录用提示；录用邮件同样受 `app.mail-enabled` 控制。邮件未启用时仅记录日志，不会发送到作者邮箱。

## AI 功能配置(智谱 GLM-4-Flash,免费)

- API Key 放在 `scripts/local.env.cmd`(**已 gitignore,不会入库**),格式 `set AI_API_KEY=你的key`
- Key 在 [open.bigmodel.cn](https://open.bigmodel.cn) 免费申请;模型/超时可在 `application.yml` 的 `app.ai` 块调整
- 体验:前台右下角**智能助手**聊天窗;管理后台论文管理(外审中)→ **AI预审** 按钮,专家在论文详情查看预审报告
- 不配置 Key 时 AI 功能返回"AI 服务未配置"提示,系统其他功能完全不受影响

## 项目结构

```
conference-system/
├── README.md               本文件
├── 架构设计.md              架构 + 扩展指南(答辩/报告素材)
├── database/
│   └── 数据库设计说明.md    E-R/范式/状态机/触发器说明(报告素材)
├── backend/                 Spring Boot 3 + MyBatis(源码即交付物)
│   └── src/main/resources/schema.sql   建表脚本(自动执行,也可交报告)
└── frontend/                Vue 3 + Vite + Element Plus
```

## 常见问题

- **后端起不来提示连接失败**:确认 Docker 里 opengauss 容器在运行、`conference_db` 已创建、密码是 `Gauss@123`(与 yml 一致)。
- **Maven/npm 下载超时(ECONNREFUSED)**:检查本机 `HTTP_PROXY`、`HTTPS_PROXY` 和 Maven 代理设置；确认代理服务可用，或清除失效的代理变量。
- **Docker 拉镜像超时**:Docker Hub 国内直连不通,用镜像源拉取后改 tag:
  ```bash
  docker pull docker.1ms.run/opengauss/opengauss:5.0.0
  docker tag docker.1ms.run/opengauss/opengauss:5.0.0 opengauss/opengauss:5.0.0
  ```
- **上传 20MB 报错**:单文件上限为 20MB，yml 设为每文件 21MB、每请求 55MB。若仍报错检查 Nginx(如加代理)的 `client_max_body_size`。
- **SQL 日志**:后端控制台直接打印 MyBatis 执行的 SQL(答辩演示数据库操作时很有用)。
- **重置演示数据**:`docker exec -it opengauss gsql -d conference_db -U gaussdb -W Gauss@123 -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"` 后重启后端(会重新建表+写种子数据)。
- **进容器执行 gsql**(该镜像 gsql 不在默认 PATH):
  ```bash
  docker exec opengauss bash -c "export LD_LIBRARY_PATH=/usr/local/opengauss/lib; /usr/local/opengauss/bin/gsql -d conference_db -U gaussdb -W Gauss@123"
  ```

## 课程报告素材索引

- 需求分析 → 本 README 功能清单
- 数据库设计 → `database/数据库设计说明.md` + `backend/src/main/resources/schema.sql`
- 系统架构 → `架构设计.md`
- 测试 → `node scripts/smoke-test.mjs`(全流程自动化,截图/输出可用于报告"系统测试"章节);SQL 可用 Data Studio 执行并截图(EXPLAIN 验证索引)
