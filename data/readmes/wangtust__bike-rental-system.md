# 骑行云 Bike Cloud — 公共自行车租赁管理与 OceanBase 数据库实验平台

西安交通大学《数据库前沿技术》小作业，选课序号 **21 → 21 % 10 = 1**，业务场景：**城市公共自行车租赁管理系统**。

✅ 完整的 Next.js 管理页面、FastAPI REST API、OceanBase MySQL 数据模型及 SQL；✅ 登录、用户与卡片 CRUD、车辆管理、租赁/归还、充值及历史记录；✅ 实验室索引性能展示，批量造数、JOIN / 高并发 / CRUD / 逻辑备份与恢复脚本；✅ B+ 树、冲突可串行性判别、Paxos 教学模拟的独立实现和自动化测试。

> 这是**用于课程学习的本地开发项目**，包含演示账户和随机模拟业务数据，**不是生产级共享单车平台**，也没有接入真实支付/真实硬件。请勿将默认密码暴露到公网。

## 目录

```text
bike-rental-system/
├── frontend/          # Next.js 16 + React 19 + 自定义响应式管理后台
├── backend/           # FastAPI + SQLAlchemy + PyMySQL + JWT
├── database/          # OceanBase 建表、SQL 查询、在线结构变更
├── scripts/           # CRUD、10 万级数据、性能、并发、逻辑备份/恢复
├── algorithms/        # B+ 树、散列索引、冲突可串行性、Paxos
├── docs/              # E-R 图、关系模式与说明
├── report/            # 实验报告目录草稿
├── compose.yml        # OceanBase + API + Next.js
└── start_local.sh     # 低内存轻量预览脚本（SQLite）
```

## 方案 A：最快在本机跑通（SQLite 预览，推荐先试）

前置：**Python 3.10+、Node.js 20+、npm**。无需安装数据库，后端自动生成 `backend/bike_rental.db` 并插入演示数据。适合内存只有 8GB 的 Mac 本机查看页面、体验租车流程。

**一条命令（macOS/Linux）**：

```bash
cd bike-rental-system
bash start_local.sh
```

或者分开启动，方便看报错：

**终端一：启动 API**

```bash
cd bike-rental-system/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

**终端二：启动前端**

```bash
cd bike-rental-system/frontend
npm install
npm run dev
```

打开：
- **前端：http://localhost:3000**
- **Swagger API：http://localhost:8000/docs**
- **健康检查：http://localhost:8000/api/health**

演示管理员账号：`admin`，密码：`admin123`。首次启动会生成 **13 个用户、12 张卡、24 辆自行车、12 个充值终端、30 笔历史租赁以及 19 笔历史充值**。支持登录、管理表单、充值、租车/还车、查询历史等。

**提示**：SQLite 不支持 OceanBase 的真正行级锁，不可用来提交课程中关于 OceanBase 并发一致性的实验证据。SQLite 只是快速预览前后端的开发模式；**正式作业必须切换 OceanBase**。

## 方案 B：OceanBase 真正数据库模式（用于课程实验）

需要 Docker Desktop / Docker Engine、足够的磁盘和内存。建议在 **x86_64 Linux、16GB+ RAM、至少 20GB 空闲 SSD** 上运行。OceanBase 的 Docker 镜像比较重，8GB Mac 可能因 Docker 虚拟机内存不足或架构兼容性而无法稳定启动。官方镜像及文档：
- https://github.com/oceanbase/docker-images/tree/main/oceanbase-ce
- https://en.oceanbase.com/quickstart

```bash
cd bike-rental-system
cp .env.example .env
# 根据需要修改 .env 中的密码密钥（此例仅限本机使用）
docker compose -f compose.yml up --build
```

镜像初次部署和租户初始化可能需要数分钟。后端启动时会自动等待数据库，创建 `bike_rental` 数据库、6 张表，并插入演示数据。不要因前端先出现页面就误以为后端已经准备就绪；观察 `docker compose -f compose.yml logs -f oceanbase backend`。

- OceanBase SQL：`127.0.0.1:2881`
- 租户账户：`root@test`，密码：`.env` 中的 `OB_TENANT_PASSWORD`（默认演示值 `obpass123`）
- 数据库：`bike_rental`
- API：`http://localhost:8000/docs`
- 前端：`http://localhost:3000`

Docker 模式不需要在宿主机执行 `database/schema.sql`，后端第一次启动时已经自动建表；该 SQL 文件供课程报告及手动验证使用。**本仓库不会自动删除持久化数据库卷**。

若镜像拉取失败，可按 OceanBase 官方文档尝试其他官方仓库镜像；若本机资源不足，建议用 SQLite 预览功能，然后在实验室 Linux 主机上做真正 OceanBase 测试。

## 按老师要求运行数据库实验

### 本机已有 OceanBase / seekdb（不使用 Docker）

本机已配置的 seekdb 使用 `127.0.0.1:2881`、`root`、空密码。
先启动数据库（若已运行则跳过）：

```bash
launchctl bootstrap gui/$(id -u) /Users/shuai/Downloads/seekdb-deployment/ai.seekdb.local.plist
```

项目根目录的 `.env` 配置 `DATABASE_URL`、`JWT_SECRET`、`ADMIN_PASSWORD` 和
`CORS_ORIGINS`，其中本机连接串为：

```dotenv
DATABASE_URL=mysql+pymysql://root@127.0.0.1:2881/bike_rental?charset=utf8mb4
CORS_ORIGINS=http://localhost:3001,http://127.0.0.1:3001
```

首次安装依赖（需要 Python 3.10+，本机使用 Homebrew Python 3.12）：

```bash
/opt/homebrew/bin/python3.12 -m venv backend/.venv
backend/.venv/bin/python -m pip install -r backend/requirements.txt
(cd frontend && npm install)
```

然后从项目根目录启动：

```bash
bash start_ob_local.sh
```

前端地址为 `http://localhost:3001`（避开其他项目占用的 3000），API 文档为
`http://localhost:8000/docs`。按 Ctrl+C 停止前后端，数据库独立运行。
后端自动创建 `bike_rental` 数据库及业务表，无需手动导入 SQL。
此连接使用 seekdb；课程是否接受 seekdb 作为 OceanBase 实验环境，应按课程要求确认。

命令统一从 **项目根目录** 执行。建议先启动后端产生演示数据库，再执行脚本；若连 OceanBase，命令需指定和 Docker 容器不同的**主机端口**连接串：

```bash
# 本机 OceanBase 密码如包含特殊字符需要 URL 编码
export DATABASE_URL='mysql+pymysql://root%40test:obpass123@127.0.0.1:2881/bike_rental?charset=utf8mb4'
# 如在 root 目录使用 backend 的虚拟环境：
source backend/.venv/bin/activate

# 1. 每表 >=10 条插入数据、每表各 1 次更新和删除（完成后清理）
python scripts/crud_tests.py

# 2. 生成 6 个关联表各 100000 条新数据，总计 600000+ 条
# 注意：大数据操作请用专用实验库；占用空间和运行时间明显增加
python scripts/generate_data.py --rows 100000

# 3. 复杂多表 JOIN / GROUP BY 性能测试，结果保存为 JSON
python scripts/run_benchmarks.py

# 4. 散列 vs B+ 树 vs 顺序扫描算法性能比较
python scripts/hash_benchmark.py

# 5. OceanBase 并发租同一辆车（SQLite 模式会直接拒绝此测试）
python scripts/concurrency_benchmark.py --clients 10
python scripts/concurrency_benchmark.py --clients 50
python scripts/concurrency_benchmark.py --clients 100

# 6. 逻辑转储、恢复到一个独立的 SQLite 数据库及行数验证
# 大规模数据时先减少数据量（这个脚本按全库导出 JSON）
python scripts/backup_restore.py
```

手工 SQL：

```text
database/schema.sql            六表建表代码
database/crud_examples.sql       简单 INSERT / UPDATE / DELETE / JOIN 示例
database/online_migration.sql   ALTER TABLE / 结构与外键校验
```

其中索引实验也可以在前端「数据库实验室」中点击运行，比较使用和忽略 `(card_id, rented_at)` 索引的查询延迟。**小数据下的性能对比不具备统计意义，必须用大量数据并重复计时**。

## 独立算法测试

```bash
cd bike-rental-system
source backend/.venv/bin/activate
python -m pytest algorithms backend/tests -v
python algorithms/bplus_tree/bplus_tree.py
python algorithms/serializability/serializability.py
python algorithms/paxos/paxos.py
```

- **B+ 树**：支持查找、插入、叶子/内部节点分裂、删除、借位/合并、范围查询与不变量验证。
- **冲突可串行性判别**：构建事务优先图，对读写冲突建立有向边，拓扑排序判断能否串行化。
- **Paxos**：只模拟 Single-Decree Paxos 的 Prepare/Promise/Accept、过半数与已接受值继承。它不模拟网络持久化、多实例日志复制，不是生产级 Paxos。
- **散列索引**：Python 字典抽象的算法演示；不是声称 OceanBase 提供 `USING HASH` 的二级索引。

## 前端功能

1. 登录与用户管理：管理员/用户、实名认证字段、修改和删除保护；
2. 射频卡：开卡、余额查询、状态维护/挂失；
3. 自行车：车辆状态、停放位置、维护；
4. 租赁：选卡 + 选车、原子租借、归还扣费、历史列表；
5. 充值：选择有效卡和终端，事务安全地增加余额并插入流水；
6. 看板：累计业务数据、车辆情况、近七天租赁数；
7. 实验室：运行索引对比、查看查询计划、定位其他实验脚本。

**默认计费规则是自行扩展的演示设定**：前 30 分钟免费，超出后每开始 30 分钟收费 ¥1。可编辑 `backend/app/services.py`。若还车余额不足，系统拒绝结算直至充值；租车需要卡片余额大于 0。

## 常见问题

- **前端打开后请求失败**：先打开 `http://localhost:8000/api/health`；若不通，检查后端错误和端口占用。
- **第一次启动前端 npm 下载慢**：先确认 Node 版本和 npm registry 网络可用。
- **OceanBase 一直无法连接**：查看 `docker compose logs oceanbase` 是否显示 `boot success!`，检查镜像、RAM、CPU 架构和 2881 端口。
- **原数据要恢复**：不要随意删除 Docker volume。备份脚本是教学用应用级 JSON 快照 + 独立 SQLite 恢复，不能替代 OceanBase 生产级备份恢复工具。
- **索引查询无明显收益**：初始化数据只有几十条，先执行批量造数，再查看执行计划。
- **需要重置 SQLite 数据**：关闭后端、删除 `backend/bike_rental.db`，再启动即可重新初始化。
- **仅允许本机访问**：Docker Compose 端口绑定 127.0.0.1；不要原样部署公网。

## 作业完整性说明

该项目交付的是**可运行源代码、SQL、实验执行工具及文档**，不是已经在用户 OceanBase 环境中运行并截图的最终实验报告。正式提交时需要你自己在 OceanBase 上运行至少 10 万级关联数据、保存查询计划与高并发数据，截图验证在线变更和恢复，再在报告中分析结果。参考 `report/REPORT_OUTLINE.md`。
