# Data_IndexQuote_Mootdx

## 1. Project Overview

本项目用于同步 mootdx 指数行情数据至 OceanBase `datademands.IndexQuote_Mootdx`。

当前同步对象：

| Field           | Value                    |
| --------------- | ------------------------ |
| IndexInnerCode  | 2749411                  |
| IndexCode       | 880009                   |
| Source          | mootdx                   |
| Target Database | OceanBase`datademands` |
| Target Table    | `IndexQuote_Mootdx`    |

数据来源为 mootdx 标准市场指数接口：

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market="std", quiet=True)
df = client.index(
    symbol="880009",
    frequency=9,
    start=0,
    offset=800,
)
```

已验证接口情况：

- `client.index(...)` 可获取 `880009` 指数日线数据。
- 当前使用 `index` 接口返回数据作为 mootdx 可获取范围内全量。

## 2. Repository Structure

项目结构对齐生产参考项目格式：

Data_IndexQuote_Mootdx/
├── README.md
├── manifest.json
├── main.py
├── core.py
├── function.py
├── rawdata.json
├── update_database.json
├── corecode/
│   ├── up_indexquote_mootdx.py
│   └── up_indexquote_mootdx_check.py
└── create_tables/
    ├── IndexQuote_Mootdx_sqlserver.sql
    ├── IndexQuote_Mootdx_ob.sql
    └── migration-report.md

核心文件说明：

| File                                             | Description                                              |
| ------------------------------------------------ | -------------------------------------------------------- |
| `main.py`                                      | 统一程序入口，处理命令行参数并调用`core.main`          |
| `core.py`                                      | 核心协调器，管理完整数据处理流程                         |
| `function.py`                                  | 数据库操作工具库，包含数据库连接、upsert、结果回查等函数 |
| `corecode/up_indexquote_mootdx.py`             | mootdx 数据拉取与字段清洗                                |
| `corecode/up_indexquote_mootdx_check.py`       | 数据质量检查                                             |
| `create_table/IndexQuote_Mootdx_sqlserver.sql` | SQL Server 风格源 DDL                                    |
| `create_table/IndexQuote_Mootdx_ob.sql`        | OceanBase 建表 DDL                                       |
| `create_table/migration-report.md`             | DDL 转换报告                                             |
| `manifest.json`                                | gaea/生产调度配置                                        |

## 3. Table DDL

表结构由 SQL Server DDL 转换为 OceanBase MySQL mode。

转换命令示例：

```bash
python3 scripts/sqlserver_to_oceanbase.py \
  create_table/IndexQuote_Mootdx_sqlserver.sql \
  -o create_table/IndexQuote_Mootdx_ob.sql \
  --profile smartquant \
  --add-column-group \
  --current-database SmartQuant \
  --report create_table/migration-report.md
```

目标表：

```text
datademands.IndexQuote_Mootdx
```

主键：

```text
IndexInnerCode + IndexCode + TradingDay
```

字段设计原则：

- 尽量保留 mootdx 原生字段。
- 新增必要管理字段：`IndexInnerCode`、`IndexCode`、`TradingDay`、`Source`、`UpdateTime`。
- `TradingDay` 用作交易日期和主键字段。
- `DateTime` 保留 mootdx 原始 `datetime` 字段。
- `TradingDay` 类型为 `date`，`DateTime` 类型为 `datetime`。

OceanBase DDL：

```sql
CREATE TABLE `IndexQuote_Mootdx` (
  `IndexInnerCode` int(11) NOT NULL,
  `IndexCode` varchar(20) NOT NULL,
  `TradingDay` date NOT NULL,
  `Open` decimal(20,4) DEFAULT NULL,
  `Close` decimal(20,4) DEFAULT NULL,
  `High` decimal(20,4) DEFAULT NULL,
  `Low` decimal(20,4) DEFAULT NULL,
  `Vol` decimal(24,4) DEFAULT NULL,
  `Amount` decimal(24,4) DEFAULT NULL,
  `Year` int(11) DEFAULT NULL,
  `Month` int(11) DEFAULT NULL,
  `Day` int(11) DEFAULT NULL,
  `Hour` int(11) DEFAULT NULL,
  `Minute` int(11) DEFAULT NULL,
  `DateTime` datetime DEFAULT NULL,
  `UpCount` int(11) DEFAULT NULL,
  `DownCount` int(11) DEFAULT NULL,
  `Volume` decimal(24,4) DEFAULT NULL,
  `Source` varchar(32) DEFAULT NULL,
  `UpdateTime` datetime DEFAULT NULL,
  PRIMARY KEY (`IndexInnerCode`, `IndexCode`, `TradingDay`)
) WITH COLUMN GROUP(all columns, each column);
```

## 4. Field Mapping

字段说明：

| Field              | Description                     |
| ------------------ | ------------------------------- |
| `IndexInnerCode` | 指数内码，当前固定为`2749411` |
| `IndexCode`      | 指数代码，当前固定为`880009`  |
| `TradingDay`     | 交易日期，用于主键              |
| `Open`           | mootdx 原生字段`open`         |
| `Close`          | mootdx 原生字段`close`        |
| `High`           | mootdx 原生字段`high`         |
| `Low`            | mootdx 原生字段`low`          |
| `Vol`            | mootdx 原生字段`vol`          |
| `Amount`         | mootdx 原生字段`amount`       |
| `Year`           | mootdx 原生字段`year`         |
| `Month`          | mootdx 原生字段`month`        |
| `Day`            | mootdx 原生字段`day`          |
| `Hour`           | mootdx 原生字段`hour`         |
| `Minute`         | mootdx 原生字段`minute`       |
| `DateTime`       | mootdx 原生字段`datetime`     |
| `UpCount`        | mootdx 原生字段`up_count`     |
| `DownCount`      | mootdx 原生字段`down_count`   |
| `Volume`         | mootdx 原生字段`volume`       |
| `Source`         | 数据来源，当前为`mootdx`      |
| `UpdateTime`     | 入库更新时间                    |

字段映射：

| mootdx Field   | OceanBase Field |
| -------------- | --------------- |
| `open`       | `Open`        |
| `close`      | `Close`       |
| `high`       | `High`        |
| `low`        | `Low`         |
| `vol`        | `Vol`         |
| `amount`     | `Amount`      |
| `year`       | `Year`        |
| `month`      | `Month`       |
| `day`        | `Day`         |
| `hour`       | `Hour`        |
| `minute`     | `Minute`      |
| `datetime`   | `DateTime`    |
| `up_count`   | `UpCount`     |
| `down_count` | `DownCount`   |
| `volume`     | `Volume`      |

补充字段：

| Field              | Value / Logic                       |
| ------------------ | ----------------------------------- |
| `IndexInnerCode` | 固定为`2749411`                   |
| `IndexCode`      | 固定为`880009`                    |
| `TradingDay`     | 由 mootdx`datetime` 转为 `date` |
| `Source`         | 固定为`mootdx`                    |
| `UpdateTime`     | 入库时写入当前时间                  |

## 5. Runtime Config

### rawdata.json

`rawdata.json` 保留统一入口参数格式。当前项目数据源为 mootdx 外部接口，不依赖数据库源表。

### update_database.json

`update_database.json` 用于写入 OceanBase `datademands`。

配置 key 按生产参考项目使用 `smartquant_ob`：

```json
{
  "smartquant_ob": {
    "type": "oceanbase",
    "host": "host",
    "port": "2883",
    "database": "datademands",
    "user": "user",
    "password": "password",
    "charset": "utf8mb4"
  }
}
```

## 6. Gaea Schedule

`manifest.json` 中的主要调度配置：

```json
{
  "dag_id": "Data_IndexQuote_Mootdx_0100",
  "start_time": "0100",
  "day_delay": 1,
  "check_dependency": 0,
  "insert_database": 1,
  "worker_image": "python:3.9"
}
```

说明：

- gaea 系统时间为 UTC。
- `start_time = 0100` 表示 UTC 01:00，对应北京时间 09:00。
- `day_delay = 1` 表示传入前一个自然日作为 `-d` 参数。
- 当前项目不依赖上游数据库表，`dependencies` 为空，`check_dependency = 0`。
- 当前项目会写入 OceanBase，`insert_database = 1`。

由于 mootdx 在盘中可能返回当天临时日线，代码会按 runner date 过滤：

```text
TradingDay <= runner date
```

例如北京时间 `2026-07-08 09:00` 运行时，gaea 传入：

```text
-d 2026-07-07
```

即使 mootdx 返回 `2026-07-08` 盘中数据，代码也只写入：

```text
TradingDay <= 2026-07-07
```

避免写入当天未完成数据。

## 7. Run

安装依赖：

```bash
pip install -U tdxpy mootdx pandas sqlalchemy pymysql click
```

正式运行：

```bash
python main.py -d 2026-07-07 -r rawdata.json -u update_database.json
```

调试运行：

```bash
python main.py -d 2026-07-07 -r rawdata.json -u update_database.json --debug
```

dry run：

```bash
python main.py -d 2026-07-07 -r rawdata.json -u update_database.json --dry-run
```

命令行参数：

| Parameter         | Description                       |
| ----------------- | --------------------------------- |
| `-d, --date`    | runner date，格式为`YYYY-MM-DD` |
| `-r, --rawdata` | 数据库读取配置文件路径            |
| `-c, --config`  | 项目配置文件路径                  |
| `-u, --update`  | 数据库写入配置文件路径            |
| `--debug`       | 打印调试信息                      |
| `--dry-run`     | 只检查入口，不执行实际同步        |

## 8. Update Logic

日更逻辑：

1. 每次运行从 mootdx 拉取当前可获取的 `880009` 全量日线。
2. 按 mootdx 原生字段清洗。
3. 补充 `IndexInnerCode`、`IndexCode`、`TradingDay`、`Source`。
4. 按 runner date 过滤 `TradingDay <= date`，避免写入当天盘中临时数据。
5. 检查主键、价格字段和 OHLC 关系。
6. 使用 `IndexInnerCode + IndexCode + TradingDay` 执行 upsert。
7. 重复运行不会重复插入。

## 9. Validation

OceanBase 回查：

```sql
SELECT COUNT(*) AS row_count,
       MIN(`TradingDay`) AS start_day,
       MAX(`TradingDay`) AS end_day
FROM IndexQuote_Mootdx
WHERE IndexInnerCode = 2749411
  AND IndexCode = '880009';
```

查看最新数据：

```sql
SELECT *
FROM IndexQuote_Mootdx
WHERE IndexInnerCode = 2749411
  AND IndexCode = '880009'
ORDER BY `TradingDay` DESC
LIMIT 10;
```

重复运行校验：

```bash
python main.py -d 2026-07-07 -r rawdata.json -u update_database.json
python main.py -d 2026-07-07 -r rawdata.json -u update_database.json
```

再次查询行数，确认不会重复插入。
