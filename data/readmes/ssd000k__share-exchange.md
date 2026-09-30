# 共享交换平台

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-%E6%BA%90%E7%AB%AF-4479A1?logo=mysql&logoColor=white)
![GBase 8s](https://img.shields.io/badge/GBase%208s-%E7%9B%AE%E6%A0%87%E7%AB%AF-FF6F00)

把 **MySQL 的表同步到 GBase 8s** 的可视化平台：配置数据源 → 勾选源表 → 生成任务 → 执行，全程有实时进度、速率、预计剩余时间和结构化日志。

```
D:\code\share-exchange\
├── run.py                    启动入口
├── start.bat                 Windows 一键启动
├── requirements.txt
├── backend\
│   ├── config.py             路径与默认参数
│   ├── database.py           平台元数据库（SQLite）
│   ├── models.py             数据源/任务/运行/日志/错误 模型
│   ├── mapping.py            MySQL → GBase 8s 类型映射 + DDL 生成
│   ├── engine.py             同步执行引擎
│   ├── runtime.py            实时状态 + SSE 事件总线 + 取消信号
│   ├── drivers\
│   │   ├── base.py           读写连接器抽象
│   │   ├── mysql.py          MySQL 读取器（服务端游标，大表安全）
│   │   └── gbase8s.py        GBase 8s 写入器（ODBC / JDBC / 原生）
│   └── api\
│       ├── datasources.py    数据源 CRUD、连通性自检、表结构浏览
│       ├── tasks.py          任务 CRUD、批量生成、DDL 预览、执行
│       └── runs.py           运行记录、日志、SSE、取消、驾驶舱
├── frontend\                 单页界面（原生 JS，无构建步骤）
└── data\
    ├── platform.db           平台元数据库
    └── logs\run_<id>.log     每次执行的完整日志
```

## 启动

```bat
start.bat
```

或手工：

```bash
.venv\Scripts\python.exe run.py --host 127.0.0.1 --port 8080
```

打开 <http://127.0.0.1:8080/>。接口文档在 `/api/docs`。

## 使用流程

1. **数据源** → 新建两个：一个 MySQL（源），一个 GBase 8s（目标）。填完点「测试连接」。
2. **同步任务** → 「从源表生成任务」→ 选源/目标数据源 → 读表清单 → 勾选表 → 生成。
3. 任务列表里点「运行」，或勾选多个后「批量运行」。
4. **实时监控** 看进度条、速率、剩余时间，可随时取消。
5. **运行记录** → 「详情」查看结构化日志、执行的建表语句、失败样本，可下载日志文件。

## GBase 8s 连接要点（2026-09-16 对真实服务器实测修订）

本机已注册 `GBase ODBC DRIVER (64-bit)`，通道选 **odbc** 即可，**不需要 JDK、不需要配置 setnet32**。

### 连接串里 `Server=` 和 `Protocol=` 缺一不可

这是踩过坑的地方。DSN-less 连接串必须同时带上这两个属性，否则连不上：

| 连接串 | 结果 |
|---|---|
| `Server=` + `Host=` + `Service=` + `Protocol=onsoctcp` | ✅ 正常工作 |
| **缺 `Server=`** | ❌ `-11060 General error` |
| **缺 `Protocol=`** | ❌ `-25555 Server xxx is not listed as a dbserver name in sqlhosts` |

平台会自动拼成这个形态（与 GBase 官方 `ConnectTest.exe` 一致），你不用手写：

```
DRIVER={GBase ODBC DRIVER (64-bit)};Server=<服务名>;Host=<主机>;Service=<端口>;
Protocol=onsoctcp;Database=<库>;UID=<用户>;PWD=<密码>;
```

- **端口**填页面的「端口」字段，平台写成 `Service=`（写 `PORT=` 会被驱动拒收，报 `-11005`）。
- **服务名**：直连模式下仅作标识，**可任意填**，留空自动用 `gbasedbt`。
- `CLIENT_LOCALE` / `DB_LOCALE` 可选，填了就成对写（如 `zh_cn.utf8`）。

### 看到 `-11060` 怎么判断

`-11060` 是驱动对"会话没建起来"的笼统包装，**瞬间返回且不发网络包**。
它不是"网络不通"，恰恰是连接串缺属性的典型症状。区分方法：

- 用 `socket` 直连一下 IP:9088。TCP **能通**却仍报 `-11060` → 是连接串/客户端问题
- TCP 不通 → 才是网络、防火墙或数据库服务没启动

平台会把常见错误码翻译成中文提示一并返回（`-11060` / `-25555` / `-951` / `-908` / `-329` / `-23101` …），
不用再去猜错误号。

### 备选：JDBC 通道

完全绕开 Client-SDK，只要 JDK + 一个 `gbasedbtjdbc_*.jar`。驱动包平台会自动搜索
（含 GBase DataStudio 的 `drivers` 目录），也可在「附加连接参数」里用 `jdbc_jar` 指定绝对路径。
ODBC 有异常时切到 **jdbc** 即可，两者报错都会给出同样的中文诊断。

### 一键「深度诊断」

数据源弹窗里除了「测试连接」，还有一个 **深度诊断** 按钮（仅 GBase 类型可见）。
它按「由外到内」的顺序逐层检查，最后给一句"卡在哪一层"的结论：

```
网络可达  →  所选通道(ODBC/JDBC)  →  客户端注册表  →  连接串与必需属性  →  实际建连
```

比「测试连接」多出来的价值在于**定位**：GBase 的报错太笼统（`-11060` 既可能是连接串写错、
也可能是客户端没装好），而网络不通时又会被误判成连接串问题。分层之后一眼能看出卡在哪。
两个实现细节：

- **网络层已经失败就跳过实际建连** —— 结果必然是失败，而驱动自己还要再等 20 秒。
- 报告里的连接串按 `PWD=` 属性打码，不是按密码值做字符串替换。
  （后者有个坑：密码只有一个字符时，`(64-bit)` 会被改成 `(64-***it)`。）

另外，「连接串 / 必需属性」这两层刻意**不依赖驱动探测结果**：探测不到 ODBC 驱动时，
按默认驱动名 `GBase ODBC DRIVER (64-bit)` 照样把连接串摆出来、照样校验必需属性
——否则客户端没装好（最需要这份报告）的机器，反而看不到这两层。

对应接口：`POST /api/datasources/diagnose`（传参数，不落库）、
`POST /api/datasources/{id}/diagnose`（用已保存的数据源）。

> 补充：`INFORMIXSQLHOSTS` / `GBASEDBTSQLHOSTS` 环境变量 GBase ODBC 驱动**不认**；
> setnet32 的配置实际存在 `HKCU\SOFTWARE\GBasedbt\`（`SqlHosts` / `Environment` / `netrc`）下，
> 但本平台走直连，**不依赖这些配置**。

ODBC 驱动位数必须与 Python 位数一致（本平台为 64 位）。

## 类型映射规则

GBase 8s 内核源自 Informix，与 MySQL 有几处必须转换的地方：

| MySQL | GBase 8s | 说明 |
|---|---|---|
| `tinyint` / `smallint` | `SMALLINT` | 8s 无 TINYINT |
| `int` / `mediumint` | `INTEGER` | |
| `bigint` | `BIGINT` | |
| `float` | `SMALLFLOAT` | 4 字节 |
| `double` | `FLOAT` | 8 字节（与 MySQL 相反） |
| `decimal(p,s)` | `DECIMAL(p,s)` | 精度上限 32 |
| `varchar(n)`，n ≤ 255 | `VARCHAR(n)` | |
| `varchar(n)`，n > 255 | `LVARCHAR(n)` | **关键**：8s 的 VARCHAR 上限 255 |
| `text` / `json` | `TEXT` | |
| `blob` / `binary` | `BLOB` | |
| `datetime` / `timestamp` | `DATETIME YEAR TO SECOND` | 8s 用粒度语法 |
| `time` | `DATETIME HOUR TO SECOND` | |
| `date` | `DATE` | |
| `year` | `SMALLINT` | |

标识符处理：MySQL 保留字（`desc`、`index`、`show`、`position` 等）在 GBase 8s 里同样是保留字，
平台会自动加双引号。表名统一转为小写（GBase 8s 的默认行为）。

## 同步模式与写入模式

**同步模式**
- `全量`：每次读整表。
- `增量`：指定水位列（如 `update_time`、`id`），只同步大于上次水位的数据，执行成功后自动更新水位。

**写入模式**
- `追加`：直接 INSERT。
- `覆盖`：先清空目标表再写。
- `更新插入`：按源表主键先 UPDATE 未命中则 INSERT（GBase 8s 没有 `ON DUPLICATE KEY`，用两步法实现）。
- `重建表`：DROP 后重建再写。表结构每次都按源表重新生成，所以在 GBase 侧手工加的
  索引/权限/注释不会保留；若目标表已被视图或存储过程引用，DROP 会失败 —— 这种情况改用「覆盖」。

建表时若目标表不存在会自动创建（GBase 8s 不支持 `CREATE TABLE IF NOT EXISTS`，
平台通过查 `systables` 判断存在性）。

> **「自动建表」与「重建表」同时开启时会怎样？**
> 目标表原本不存在 → 先自动建表，然后**跳过重建**（刚新建的结构就已经是源表结构，
> 再建一次是多余的）。目标表原本就存在 → 正常走 DROP + 重建。
> 这两条分支都有测试覆盖（`test_engine_guards.py` 的 `[8]` 组）。

## 性能相关

- 读 MySQL 用服务端游标（`SSDictCursor`），按 `batch_size` 分批取，不会一次性把大表读进内存。
- 写 GBase 8s 用 `executemany`，并尝试开启 `fast_executemany`。
- 最多 4 个任务并行（改 `SE_MAX_CONCURRENT_RUNS` 环境变量可调整）。
- 单批失败不会立刻中断，累计失败超过 3 个批次才终止，失败样本记录在运行详情里（最多 20 条）。

## 运行状态说明

| 状态 | 含义 |
|---|---|
| `成功` | 所有批次都写入成功 |
| **`部分成功`** | 有批次失败但有数据写入 —— 失败行数会单独统计，**不计入成功率**，请查看「失败样本」 |
| `失败` | 连接或首批写入就失败，没有数据落库 |
| `已取消` | 用户中途取消，已写入的行保留 |

## 标识符一致性（重要设计约束）

GBase 8s 里**未加引号的标识符按小写存储，加引号的标识符大小写敏感**。
所以如果建表时写 `"Desc"`、插入时写 `"desc"`，引擎会当成两个不同的列，运行期才报「列不存在」。

平台的对策是：所有标识符（DDL、INSERT、UPDATE、WHERE、表名、schema）
**只能经过 `mapping.gbase_ident()` 这一个函数**，它统一先转小写再决定是否加引号。
代码里不再直接调用 `quote_gbase()` 拼 SQL —— `tests/test_engine.py` 会校验这一点。

## 自检脚本

```bash
tests\run_all.bat                 # 一键跑全部
```

| 脚本 | 覆盖内容 |
|---|---|
| `tests/test_gbase_writer.py` | 写入器 SQL 生成：DDL/INSERT 标识符一致性、upsert 两步法、TRUNCATE 回退、取值转换、类型映射 |
| `tests/test_engine.py` | 水位字面量转换、SQL 注入防护、状态语义、标识符单一入口（源码级）、**被外键引用的主键必须防复用（数据模型级）** |
| `tests/test_engine_guards.py` | 并发提交保护、重启后收尾中断运行、**删除运行记录后遗留日志的清理（防止日志寄生于复用 id 的新运行）**、同步后对账、**批量建任务的重复/覆盖处理（回归：曾返回 500）**、**重建表模式下「表不存在」与「表已存在」两条分支（回归：新表首跑必失败）** |
| `tests/test_gbase_odbc_conn.py` | **ODBC 连接串必须含 `Server=`/`Host=`/`Service=`/`Protocol=`**、`Server` 缺省值、DSN 模式、locale 成对规则、错误码翻译、密码打码、分层体检结构、**诊断报告在无驱动环境下不丢层**、**报错瘦身（ODBC 重复段 / JDBC 堆栈与内嵌类名）** |
| `tests/render_smoke.js` | 用最小 DOM 桩在 Node 里真跑前端脚本，校验 6 个页面渲染 + 5 个弹窗表单 + 运行详情 + **深度诊断报告的渲染（结论/建议/分层步骤/耗时/详情转义）** |

改完代码建议都跑一遍。这些测试**都不需要真实 GBase 服务器**。

## 注意

- 数据源的密码以明文存在平台自己的 SQLite（`data/platform.db`）里，这是同步工具正常工作的前提。
  该文件不要提交到代码仓库，也不要随意分享。
- 「覆盖」和「重建表」会删除目标表数据，首次使用建议先拿 1~2 张小表试跑。
- 建任务时会校验两端类型（源必须 MySQL、目标必须 GBase 8s、不能选同一个数据源），
  配置错误在提交时就会拦下来，不会拖到运行期。
- 批量建任务（`POST /api/tasks/batch`）对已存在的任务默认**跳过**；
  带 `overwrite: true` 时是「**就地覆盖已有任务的配置**」，不是删掉重建 ——
  这样该任务的运行历史不会失去归属。返回值里 `created` / `updated` / `skipped`
  三个计数分开给出。
- **被外键引用的主键一律开启 `AUTOINCREMENT`**（`se_datasource` / `se_sync_task` / `se_sync_run`）。
  这一点很关键 —— SQLite 默认会复用被删除的 id，而运行日志、失败明细、任务→运行
  都是按 id 关联的；一旦某条记录被删却留下关联行，复用同一 id 的新记录就会把旧数据
  当成自己的显示出来（表现为运行详情里混进别的任务的日志）。叶子表
  （`se_run_log` / `se_run_error`）没有被任何外键指向，其 id 复用无害，故不加。
  规则由 `tests/test_engine.py` 的 `[5]` 组自动守住。
- 另外服务启动时会调用 `engine.purge_stale_logs()` 兜底清理两类脏行：
  `run_id` 已不存在的孤儿行，以及时间早于该运行开始时刻的越界行。
- **老库注意**：`sqlite_autoincrement` 只在建表时生效，已存在的表不会因此改变。
  对 2026-09-16 之前创建的 `platform.db`，防复用靠上面两条兜底；如需彻底获得
  `AUTOINCREMENT`，需要重建该表（本平台未自动做，避免擅自动用户数据）。
