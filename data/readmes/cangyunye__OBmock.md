# OBmock — OceanBase 双租户（MySQL/Oracle）开发测试桩

单二进制内嵌 SQL 引擎，用 **MySQL 线协议**模拟 OceanBase 的 MySQL 租户与 Oracle 租户，
供日常开发/CI 快速测试。行为基准取自真 OB 企业版实测（`docs/baseline.md`）。

```
                      ┌─ MySQL 协议 listener ─→ MySQL 租户桩（标准 MySQL 驱动直连无感）
OBmock 单二进制进程 ──┤                └─→ Oracle 租户桩（Oracle 方言 SQL + OBE 错误码）
   Go + SQLite         （协议面 100% 对齐真 OB——TNS 线路经实证真库不接受，无需实现）
```

## 为什么是这个架构（调研结论）

- OB 社区版无 Oracle 租户（企业版专属），企业版有 180 天试用 License
- OB 服务端单端口**实际只接受 MySQL 线协议**（ojdbc TNS 直连被真库 ORA-17904 拒绝；obconnector-j 源码 internal/com 全为 MySQL 协议类）+ 驱动白名单（mock 默认宽松放行）
- **真 OB 会识别驱动**：普通 MySQL 驱动连 Oracle 租户被拒（`1235: Oracle tenant for current client driver is not supported`）——mock 默认**宽松模式**放行一切 MySQL 协议客户端，比真 OB 更适合测试
- Oracle 官方纯 thin 驱动（python-oracledb thin / go-ora）连真 OB Oracle 租户也不支持，明确不做

## CI

`.github/workflows/ci.yml`：单元测试、mock 启动、三语言包装自测、obcheck 自校一键执行；
双跑对比（需真 OB）留 self-hosted runner 挂载位（`vars.OB_REAL_RUNNER` 启用）。

## 兼容性预检（obcheck）

```bash
go build -o obcheck ./cmd/obcheck
./obcheck path/to/sql/          # 扫描目录，[error] 标记 mock 不支持特性
./obcheck -json -v path/ > report.json
```

15 条规则三级分级（error=mock 必报错 / warn=真库支持需注意 / info），迁移前预检应用 SQL。

## 测试容器包装（一行启动）

```python
# Python（containers/python/obmock_container.py）
from obmock_container import ObMock
with ObMock(password="test123") as m:
    conn = pymysql.connect(**m.connect_kwargs("sys@oratest"))
```

```go
// Go（containers/go/obmock_testkit.go）
m := obmocktestkit.Start(t)   // t 为 *testing.T，失败自动回收
defer m.Stop()
db, _ := sql.Open("mysql", m.DSN("sys@oratest"))
```

```rust
// Rust（containers/rust/，Drop 自动回收）
let mut mock = obmock_testkit::ObMock::start()?;
let mut conn = mock.conn()?;
```

四语言包装均含自验证测试（连接→建表→序列→GET_DDL→错误码断言→回收）。

## 快速开始

```bash
# 源码运行
go build -o bin/oracle-sim ./cmd/oracle-sim
./bin/oracle-sim -listen 0.0.0.0:13306 -data ./data -password secret

# Docker
docker build -t obmock .
docker run -d -p 13306:13306 -v obmock-data:/data obmock

# 连接（用户名格式与真 OB 完全一致：user@tenant）
obclient -h127.0.0.1 -P13306 -usys@oratest -psecret -A
```

Oracle 方言 SQL 原样发送：

```sql
CREATE TABLE demo_t (id NUMBER PRIMARY KEY, name VARCHAR2(50), amt NUMBER(10,2));
INSERT INTO demo_t (id, name) VALUES (demo_seq.NEXTVAL, 'x');
SELECT rownum, id, NVL(name, '(null)') FROM demo_t WHERE ROWNUM <= 10;
SELECT DECODE(id, 1, 'one', 2, 'two', 'other') FROM demo_t;
SELECT column_name, data_type, column_id FROM user_tab_columns WHERE table_name = 'DEMO_T' ORDER BY column_id;
-- 错误码：OBE-00942 table or view 'SYS.XXX' does not exist
```

## 四语言示例（全部实测通过）

| 语言 | 驱动 | 位置 | 状态 |
|---|---|---|---|
| Go | go-sql-driver/mysql | `examples/go` | ✅ 含事务回滚 |
| Python | PyMySQL | `examples/python/smoke.py` | ✅ |
| Java | mysql-connector-j **+ OceanBase Connector/J 双驱动** | `examples/java` | ✅ OB 官方驱动直连 mock 验证通过 |
| Rust | mysql crate | `examples/rust` | ✅ |

## 配置参数

| 参数 | 默认 | 说明 |
|---|---|---|
| `-listen` | `0.0.0.0:13306` | MySQL 协议监听地址 |
| `-data` | `./data` | SQLite 数据目录（每租户一个 .db 文件） |
| `-password` | 空 | 统一开发密码（客户端须一致；空=客户端发空密码） |
| `-oracle-tenants` | `oratest,sim_oracle` | Oracle 模式租户列表 |
| `-mysql-tenants` | `obmysql,sim_mysql,test` | MySQL 模式租户列表 |
| `-default-tenant` | `sim_mysql` | 用户名未带 `@tenant` 时的默认租户 |
| `-version-string` | `5.7.25-OceanBase-v4.4.2.2-mock` | 握手包版本串 |
| 环境变量 `OBMOCK_LOG_SQL` | - | 非空时打印进站 SQL（排障用） |

租户名建议与真 OB 一致，这样测试代码在 mock 与真库之间只需换 host/port。

## 已支持（P0 清单，对照详细计划）

**会话**：`user@tenant` 解析、SET/SHOW VARIABLES、autocommit 语义（Oracle 线默认手动提交）、
server-side PREPARE、START TRANSACTION/BEGIN/COMMIT/ROLLBACK/SAVEPOINT、DDL 隐式提交

**DDL**：NUMBER(p,s)/VARCHAR2/CHAR/DATE(含时分秒)/TIMESTAMP/CLOB/BLOB/RAW 类型映射、
CREATE TABLE（PK/UNIQUE/FK/CHECK/DEFAULT）、CREATE INDEX、CREATE OR REPLACE VIEW、CTAS、
CREATE/DROP SEQUENCE（NEXTVAL/CURRVAL 会话语义）、TRUNCATE、ALTER ADD/DROP/RENAME COLUMN、
COMMENT ON、未加引号标识符大写、分区表语法降级+警告

**DML**：ROWNUM 两大分页模式、OFFSET..FETCH、JOIN 全家、UNION/MINUS/INTERSECT、子查询/EXISTS/IN、
WITH CTE、CASE、DECODE/NVL/NVL2、''=NULL 语义、序列赋值、SELECT FOR UPDATE 剥离

**函数**：TO_CHAR/TO_DATE/TO_TIMESTAMP/TO_NUMBER（Oracle 格式串解析）、ADD_MONTHS/MONTHS_BETWEEN/LAST_DAY、
TRUNC、SUBSTR/INSTR（Oracle 参数语义）、REGEXP_LIKE/REPLACE/SUBSTR、CHR/ASCII、LISTAGG→GROUP_CONCAT、
窗口函数直通、IFNULL 原生；第二批 50+：CONCAT/CONCAT_WS/CHAR_LENGTH/LEFT/RIGHT/LOCATE/SUBSTRING_INDEX/
INITCAP/REPEAT/REVERSE、DATEDIFF/TIMESTAMPDIFF/TIMESTAMPADD/EXTRACT/DATE_FORMAT、GREATEST/LEAST/IF/ISNULL/
LNNVL/SIGN/LN/LOG 族、聚合统计族 STD/STDDEV/VARIANCE（自定义聚合）、JSON 最小集（VALUE/QUERY/EXISTS/ARRAY/
OBJECT/VALID）、DATE_ADD INTERVAL、APPROX_COUNT_DISTINCT、FORMAT/ELT/FIELD/FIND_IN_SET/BIN/CONV/MD5/CRC32/
SPLIT_PART/URL 编解码/TO_BASE64/INT2IP 等

**数据校验**：INSERT 字面量校验 NUMBER(p,s) 整数位溢出（OBE-01438）、VARCHAR2/CHAR 字节超长
（OBE-01401，BYTE 语义含多字节字符）、TO_DATE 失败（OBE-01843）

**仿真**：OBE 错误码（00942/00001/01400/01722/01476/02291/00900/08002/00439/01438/01401/01843…）、
OBPK_ 风格约束名、user_/all_/dba_ 数据字典全对象（表/列/视图/索引/序列/约束/同义词/存储过程源码/触发器）、
DUAL、v$version banner（对齐 4.4.2.2 基线）、version()/@@version 返回对应版本、Hint 吞析、`@@系统变量` 探测响应

**Oracle 线专项**：ROWID 伪列、SYS_GUID/USER/UID、TO_CHAR 数字格式串（9/0/,/./$）、
NLS_DATE_FORMAT 驱动 DATE 列显示（SYSDATE→15-NOV-26，表列同样生效）、同义词 SQL 解析（链式+JOIN 位置）、
**CONNECT BY 层次查询 → WITH RECURSIVE**（含 LEVEL 伪列与 **SYS_CONNECT_BY_PATH** 路径列）、
DBMS_LOB.SUBSTR/GETLENGTH/INSTR、ARG_MAX/ARG_MIN/GROUPING 聚合、
**MERGE INTO**（含 USING 子查询源，UPDATE+INSERT 两语句翻译）、**INSERT ALL** 多目标展开、
**DBMS_OUTPUT** 会话缓冲（PUT_LINE/GET_LINE）、ANALYTIC 窗口框架（ROWS/RANGE BETWEEN 直通）、
**分区子句元数据**（USER_PART_TABLES）、autocommit=off 手动提交、''=NULL、DDL 隐式提交

**错误码体系**：00942/00904/00955/00947/00913/00001/01400/01401/01438/01722/01843/01476/02291/00900/08002/00439/00600…
（01400 消息含 "表"."列"，01438 含 NUMBER(p,s) 详情，00904 含列名）

**元数据查询**（两租户线）：

| 对象 | Oracle 线（user_/all_/dba_） | MySQL 线 |
|---|---|---|
| 表/列/视图/索引/序列 | ✅ TABLES/TAB_COLUMNS/VIEWS/INDEXES/SEQUENCES | ✅ information_schema.tables/columns/statistics + SHOW TABLES/DESC |
| 约束 | ✅ CONSTRAINTS/CONS_COLUMNS（P/U/R/C 真实数据，含自动命名 OB_C_*） | ⚠️ SHOW CREATE TABLE |
| 存储过程/函数/包 | ✅ 元数据+源码可查（USER_SOURCE/PROCEDURES/OBJECTS），**调用显式报 OBE-00439（不执行 PL/SQL）** | — |
| 触发器 | ✅ TRIGGERS（触发时机/事件/基表/源码） | — |
| 同义词 | ✅ CREATE/DROP SYNONYM + SYNONYMS（含 @dblink 解析） | — |
| 对象汇总 | ✅ USER_OBJECTS/ALL_OBJECTS/CAT 全类型 | — |

说明：代码类对象（存储过程/函数/包/触发器）在 mock 中是**元数据级支持**——DDL 建对象、存源码、
字典可查（Flyway 等迁移工具的"建对象→校验"流程可跑通），但调用执行明确报错不编译 PL/SQL。

## 已知妥协（对照真 OB 的偏差）

- SQLite 单写者：并发写场景失真（开发测试够用）
- 表达式列头为"Oracle 派生规则"近似（大写+去空格，字面量内保留原样）
- PL/SQL：存储过程/函数/包/触发器**元数据级支持**（建对象/查源码/查字典可跑），调用执行不支持（明确报错）；CONNECT BY/MERGE 不支持
- 序列值进程内存态，重启后回到 CREATE SEQUENCE 时的持久化值
- 同义词仅元数据：SQL 中按同义词名解析底层对象未实现
- 日期结果以 ISO 文本返回（NLS_DATE_FORMAT 显示格式化为 P2）

## 路线图

- ~~Phase 2 TNS listener~~：**经实证取消**（ojdbc 直连真库 ORA-17904，真库不接受 TNS 协议；细节见 docs/verification-report.md §二d），
  让 ojdbc / obconnector-J Oracle 模式 / cx_Oracle+libobci 直连
- **Phase 1.5**：SHOW/DESC/information_schema 全家、Flyway/MyBatis Generator 兼容验证
- **持续**：`tests/goldensql` 对照回归（mock vs WSL 真 OB 企业版实例）

## 目录结构

```
cmd/oracle-sim/          入口
internal/dialect/        Oracle→SQLite 方言翻译（tokenizer+重写 pass+函数注册+序列注册表）
internal/engine/sqlite/  内嵌存储（modernc.org/sqlite 纯 Go、会话事务、元数据、错误映射）
internal/server/mysql/   MySQL 线协议 listener（go-mysql server 包适配）
internal/session/        user@tenant 会话/租户模式/变量
internal/errcode/        OBE/ORA 错误码体系
tests/baseline/          Phase 0 真库探测脚本（可重放）
tests/smoke/             冒烟 SQL 套件
docs/baseline.md         行为基准（真 OB 实测）
examples/{go,python,java,rust}/  四语言示例
```
