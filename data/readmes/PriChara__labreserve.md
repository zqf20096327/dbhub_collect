# LabReserve 校园实验设备预约与借还管理系统

Web 数据库课程项目：Vue 3 + TypeScript → Nginx → Spring Boot/JDBC → 真实 openGauss 6.0.2。

前端与后端分别封装为 Docker 服务，数据库运行在 openEuler 虚拟机中。后端采用模块化单体结构，支持通过 Compose 运行多个相同后端实例。

## 源码与提交材料

源码仓库：<https://github.com/PriChara/labreserve>。点击 **Code → Download ZIP** 可下载完整源码，或使用 `git clone https://github.com/PriChara/labreserve.git`。

仓库包含前端与后端源码、两个 Dockerfile、`compose.yaml`、数据库建表脚本、初始化与验证脚本、测试结果及截图。提交内容和复现步骤见 [源码交付说明](docs/submission.md)。

## 运行已有部署

1. 启动本地虚拟机 `D:\VirtualMachines\openGauss6.0.2\openEuler.vmx`。
2. 使用课程环境中的 omm 用户登录虚拟机，执行 `gs_om -t start`。数据库端口为 26000。
3. 在项目根目录执行：

```powershell
docker compose up -d --wait
```

打开 <http://127.0.0.1:8088>。默认只绑定本机端口。

演示账号：`admin`（管理员：张鹤闻）、`teacher`（教师：李四）、`student`（学生：张三）、`student2`（学生：王五）。管理员显示姓名按项目开发者要求设置，其他姓名为通用模拟姓名；账号及业务记录用于课程演示。首次初始化时密码由 `.env` 中 `DEMO_PASSWORD` 决定，当前演示密码为 `DemoLab@2026`。

关闭应用：`docker compose down`。该命令不停止虚拟机、不删除 openGauss 数据。数据库与应用生命周期独立。

## 在另一台机器快速部署

准备 Docker 与可访问的 openGauss 6.0.2 数据库，复制项目源码或发行包。

```powershell
# 有离线镜像包时，直接导入，不需要安装 Java、Node.js 或 Maven。
docker load -i artifacts/labreserve-images.tar
Copy-Item .env.example .env
# 编辑 .env，填入实际数据库地址、端口和应用账号密码。
docker compose up -d --no-build --wait
```

数据库准备分为两种情况：

- 使用本项目的虚拟机副本：数据库与账号已经存在，使用对应的 `.env`，无需再次初始化。
- 使用其他新的 openGauss 实例：创建 **PG 兼容模式**数据库，执行 `database/01-schema.sql` 并配置权限。课程虚拟机可使用下面的初始化脚本。

新的课程虚拟机环境初始化：

```powershell
python -m pip install -r scripts/requirements.txt
python scripts/init_database.py --trust-first-use
```

脚本交互读取 omm SSH 密码。数据库密码随机生成，只保存在忽略版本控制的 `.env`。再次运行脚本不会覆盖业务数据；已有数据库兼容模式不为 PG 时会停止并保留原库。只给应用账号配置 VMware 指定子网的 SHA-256 认证。

虚拟机的 host-only 网卡必须能够被应用宿主机访问。其他机器的 VMware 子网、数据库地址可能不同，需要相应调整 `.env` 和 `pg_hba.conf`。不能将应用连接地址写成虚拟机外部客户端自己的 `localhost`。

## 从源码构建

先准备可访问的 openGauss 6.0.2 数据库，并按上文完成 PG 兼容模式建库、建表和应用账号权限配置。首次下载源码后执行：

```powershell
Copy-Item .env.example .env
# 编辑 .env，填写当前环境的 DB_HOST、DB_PORT、DB_USER 和 DB_PASSWORD。
docker compose up -d --build --wait
```

构建阶段在容器内使用 Maven、Java 17 和 Node.js 24，运行阶段仅保留 JRE 与 Nginx。后端使用普通用户运行，数据库端口不会由 Compose 额外发布。

开发模式：在一个终端执行 `./scripts/dev.ps1`，在另一个终端进入 `frontend` 执行 `npm ci`、`npm run dev`。浏览器入口为 <http://127.0.0.1:5173>，前端开发服务将 `/api` 转发到本地后端 8080。开发脚本为本项目选择 Java 17，不修改系统 Java 设置。

## 功能与边界

- 学生：查看设备与占用时段、提交预约、查看和取消自己的待审批/已批准预约。
- 教师：审核他人的预约、办理领用与归还、查看预约和借用情况。
- 管理员：教师功能，以及添加设备、登记/结束维修、查看审计与数据库状态。
- 同一物理设备的重叠预约不能同时成功，待审批预约也占用时段。
- 预约范围：未来 30 天，同一天 08:00—22:00，每次 30 分钟至 8 小时。
- 领用范围：开始前 30 分钟至结束时间之间；上一笔借用未归还时不能再次领用。
- 设备有未完成借用或未来待处理/已批准预约时，不能进入维修。
- 审批、领用、归还、取消和审计记录均在数据库事务中处理。

## 验证与实验依据

```powershell
python tests/integration.py --base http://127.0.0.1:8088 --cleanup-password-stdin
python scripts/verify_database.py
```

集成测试从 HTTP 接口验证真实数据库行为，覆盖登录、越权、注入、参数校验、重复状态转换、维修与 8 请求并发预约。提供 omm SSH 密码后，仅清理本次创建的 IT- 测试设备和关联记录，保留演示数据。`--cleanup-password-stdin` 表示从标准输入读取该密码；不提供此参数则保留测试记录。

数据库验证脚本检查约束、权限和事务回滚；在临时表上用 10 万行模拟记录比较查询计划，并在全新临时数据库中恢复逻辑备份，比较 12 张表的行数与内容指纹。脚本会删除自己创建的恢复验证库，备份保存在 `artifacts/backups`。

结果文件：`artifacts/test-results.json`、`artifacts/database-verification.json`、`artifacts/query-plans.txt`。性能结果是本机上的小规模合成实验，不能直接解释为生产环境容量。

## 多实例部署

```powershell
docker compose up -d --scale backend=2 --force-recreate --wait
```

Nginx 在启动时解析后端服务地址，会使用同一服务的多个实例。增加/减少实例后重新创建前端以刷新地址。会话保存在数据库，预约互斥依赖数据库行锁，因此不会依赖单个实例的内存锁。

恢复默认：`docker compose up -d --scale backend=1 --force-recreate --wait`。

`python tests/deployment.py` 可验证两个实例均收到请求，然后重建为一个实例，核对原会话和业务记录仍然一致。本次已有镜像的重建恢复健康实测为约28秒，该数值不包含首次下载与构建时间。

## 小组分工与技术说明

张鹤闻负责数据库设计、JDBC 数据访问、事务与并发控制及部署集成；徐阳光负责需求分析、前端页面与交互及界面验收；刘睿航负责总体设计、后端认证与业务接口、接口测试及后端容器配置。技术说明见 `docs/architecture.md`、`docs/database.md`、`docs/api.md`。

## 已知限制

当前是课程演示规模，预约列表单次最多返回 200 条，审计返回最近 100 条。未提供注册、账号管理、消息通知、审批超时自动释放或主备故障切换。教师权限按全局角色划分，尚未限制到实验室。演示部署为本机 HTTP，使用真实数据或网络发布前应增加 HTTPS、修改演示账号、设置 `COOKIE_SECURE=true` 并重新评估访问范围。应用密码使用 BCrypt，数据库账号使用 SHA-256 网络认证；当前 JDBC 连接没有启用 TLS。

## 环境问题记录

- openGauss 默认数据库兼容模式不一定为 PG。本环境默认 A 模式，将空字符串视为 NULL，因此项目建库必须显式指定 `DBCOMPATIBILITY 'PG'`。
- Maven 中的 `org.opengauss:opengauss-jdbc:6.0.0` 包含 `org.postgresql.Driver`，使用 `jdbc:postgresql:` URL。它仍然是 openGauss 官方 JDBC 包，服务器通过 `version()` 实际核验为 openGauss。
- 本机 Maven 默认 Java 8，项目需要 Java 17；开发脚本单独设置进程环境。
- Windows Java NIO 临时 Unix 域套接字路径曾导致启动失败；开发脚本使用本机原生临时目录解决。Linux Docker 运行不需要该参数。
- Docker 原容器代理地址失效，已通过 Docker Desktop 设置修正为本机正在运行的 HTTP/HTTPS 代理。网络环境不同的机器应使用自己的有效代理配置。
