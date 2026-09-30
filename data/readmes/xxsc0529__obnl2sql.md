# OceanBase NL2SQL

<div align="center"><img width="100%" src="./assets/nl2sql360.png"></div>

> Fork of [NL2SQL360](https://github.com/HKUSTDial/NL2SQL360) — Powered by OceanBase Community

OceanBase NL2SQL 评测框架，支持 OceanBase（MySQL / Oracle 兼容模式）、SQLite、MySQL、PostgreSQL。

## 安装

要求 Python >= 3.8。

```bash
pip install obnl2sql
```

数据库驱动为可选依赖，按目标数据库安装：

```bash
pip install "obnl2sql[oceanbase]"   # OceanBase（pymysql + oracledb）
pip install "obnl2sql[mysql]"       # MySQL
pip install "obnl2sql[postgresql]"  # PostgreSQL
pip install "obnl2sql[all]"         # 全部驱动
```

SQLite 开箱即用，无需额外驱动。驱动缺失时会提示对应的安装命令。

或源码安装：

```bash
git clone https://github.com/oceanbase/obnl2sql.git
cd obnl2sql
pip install -e ".[oceanbase]"
```

```bash
obnl2sql version
```

## 快速开始

### 1. 准备数据

```
my_dataset/
├── dev.json          # 样本文件
├── tables.json       # 数据库 schema（可选）
└── database/
    └── my_db/
        └── my_db.sqlite
```

### 2. 导入数据集

```yaml
# dataset.yaml
core_dir: "./obnl2sql_cache"
core_name: "nl2sql"
sql_dialect: "SQLite"
dataset_name: "my_dataset"
dataset_dir: "data/my_dataset"
samples_file: "dev.json"
tables_file: "tables.json"
database_dir: "database"
question_key: "question"
sql_key: "query"
db_id_key: "db_id"
```

```bash
obnl2sql dataset dataset.yaml
```

### 3. 运行评测

```yaml
# evaluation.yaml
core_dir: "./obnl2sql_cache"
core_name: "nl2sql"
sql_dialect: "SQLite"
eval_name: "MyModel"
eval_dataset: "my_dataset"
eval_metrics: ["ex"]
pred_sqls_file: "predicted.sql"
```

```bash
obnl2sql evaluate evaluation.yaml
```

### 4. 生成报告

```yaml
# report.yaml
core_dir: "./obnl2sql_cache"
core_name: "nl2sql"
sql_dialect: "SQLite"
report_dataset: "my_dataset"
report_evaluation: ["MyModel"]
metric: ["ex"]
filter:
  - name: "JOIN"
    expression: "JOIN > 0"
save_path: "report.csv"
```

```bash
obnl2sql report report.yaml
```

## OceanBase 评测配置

OceanBase 用户名格式为 `用户名@租户名`（如 `root@test`、`sys@oracle_tenant`）。

### MySQL 兼容模式

```yaml
sql_dialect: "OceanBase-MySQL"
db_host: "127.0.0.1"
db_port: "2881"
db_user: "root@mysql_tenant"
db_password: "your_password"
# db_name 不设置 -> 每个样本按 db_id 路由到同名 schema（推荐多库数据集）
# db_name: "test_db"  # 显式设置则所有样本在单一 schema 上执行
```

### Oracle 兼容模式

```yaml
sql_dialect: "OceanBase-Oracle"
db_host: "127.0.0.1"
db_port: "2881"
db_name: "service_name"   # Oracle 模式下为 service name
db_user: "sys@oracle_tenant"
db_password: "your_password"
```

> 两种模式均需安装驱动：`pip install "obnl2sql[oceanbase]"`。

### db_id 路由（多库数据集）

BIRD 类数据集中每个样本属于一个数据库（由 `db_id` 标识）。**不设置 `db_name`
时**，框架自动把每个样本路由到与其 `db_id` 同名的 OceanBase schema 执行，
不同库中同名异构的表不会互相干扰。使用前需把各库的表结构和数据迁入对应
schema，完整步骤见实战文档。

## 支持的 SQL 方言

| 方言 | 默认端口 | 驱动安装 |
|------|------|------|
| `SQLite` | - | 内置，无需安装 |
| `MySQL` | 3306 | `pip install "obnl2sql[mysql]"` |
| `PostgreSQL` | 5432 | `pip install "obnl2sql[postgresql]"` |
| `OceanBase-MySQL` | 2881 | `pip install "obnl2sql[oceanbase]"` |
| `OceanBase-Oracle` | 2881 | `pip install "obnl2sql[oceanbase]"` |

## 评测指标

| 指标 | 代码 | 说明 |
|------|------|------|
| 执行准确率 | `ex` | 对比执行结果集 |
| 精确匹配 | `em` | 比较 SQL 结构 |
| 有效效率分数 | `ves` | 对比执行速度 |
| 基于奖励的 VES | `rves` | VES 升级版 |
| Soft-F1 分数 | `f1` | 部分重叠给部分分 |
| 问题方差测试 | `qvt` | 多条 SQL 一致性 |

## 文档与示例

- [OceanBase 评测实战指南（初学者版）](docs/oceanbase_evaluation.md)：从安装、数据迁移到 CLI / Python API 评测的完整手把手教程，附真实环境实测结果与排错 FAQ。
- CLI 配置示例：`examples/cli_examples/` 下的 `oceanbase/`、`bird/`、`spider/` 目录。
- Python API 示例：`examples/py_examples/`。

## 致谢

基于 [NL2SQL360](https://github.com/HKUSTDial/NL2SQL360) 二次开发，感谢原作者 Boyan Li 等。

论文：[The Dawn of Natural Language to SQL: Are We Fully Ready?](https://arxiv.org/abs/2406.01265) (VLDB'24)

## License

MIT License
