# dm8-verify

`dm8-verify` 是 P2 数据基线与一致性校验 Demo。它把证据标记为 `SOURCE`、`DATABASE`、`FIXTURE` 或 `RESTORED`，以避免把本地合成文件结果误写成 DM8 恢复成功。

## 环境与安装

需要 Python 3.10 或更高版本，仅使用标准库。开发模式可直接运行：

```bash
cd /srv/dm8-lab/dev
PYTHONPATH=src python3 -m dm8_verify.cli --help
```

也可在项目虚拟环境中安装：

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
```

## CLI

采集本地源文件（不会修改源文件）：

```bash
PYTHONPATH=src python3 -m dm8_verify.cli collect-source \
  --input /srv/dm8-lab/fixtures/hr/data \
  --config config/tables.json \
  --manifest /srv/dm8-lab/fixtures/hr/source_manifest.json \
  --output outputs/source-before
```

比较两个基线：

```bash
PYTHONPATH=src python3 -m dm8_verify.cli compare \
  --before outputs/source-before/baseline.json \
  --after outputs/source-after/baseline.json \
  --output outputs/comparison
```

运行完整离线演示：

```bash
PYTHONPATH=src python3 -m dm8_verify.cli demo --output outputs/p2-demo
```

`demo` 会执行相同 SOURCE 的 PASS 比较、行数/摘要异常的 FAIL 比较，以及缺失摘要的 INCOMPLETE 比较。它不连接 DM8。

## 输出与摘要规则

每个基线目录包含 `baseline.json` 和 `tables.csv`。基线记录 `schema_version`、`fingerprint_version`、`run_id`、采集时间、来源类型、输入文件 SHA-256、逐表行数、主键摘要、数据摘要、DDL 结构/约束和采集错误。

数据通过 UTF-8、固定列顺序和类型规范化后做 SHA-256 多重集摘要；因此输入行顺序变化不会改变结果。NULL 使用显式标记并区别于空字符串，日期使用 ISO 格式，DECIMAL 固定到声明的小数位。主键在临时 SQLite 文件中去重，避免将全部键保留在内存。

比较器会检查行数、主键摘要、数据摘要、列/约束/索引元数据和采集错误。只有所有配置项都采集且通过时才返回 `PASS`。来源类型不兼容、摘要缺失或版本不兼容返回 `INCOMPLETE`；发现差异返回 `FAIL`。

验证等级：`ROW_COUNT` 只比较逐表记录数；`DATA_ONLY` 比较记录数、已采集的主键摘要和数据摘要，并检查采集错误；`FULL` 还强制要求列元数据、约束、索引和聚合统计。未采集的必需证据一律为 `INCOMPLETE`，因此 `ROW_COUNT` 或 `DATA_ONLY` 结果不能表述为完整一致性。

退出码：`0` 全部通过，`1` 发现差异，`2` 输入或采集错误，`3` 证据不足。

## DM8 在线适配层

`collect-db` 使用只读 `SELECT` 结果和显式标记解析 disql 输出：

```bash
export DM8_VERIFY_PASSWORD='由安全凭据注入'
PYTHONPATH=src python3 -m dm8_verify.cli collect-db \
  --db-config config/db.json \
  --output outputs/database-before
```

恢复目标采集时增加 `--source-type RESTORED`，用于和恢复前 `DATABASE` 基线配对。

配置文件应只保存主机、端口、服务名、用户名、`password_env` 和 `disql_path`，不要保存密码。当前没有可用 DM8 客体连接，因此在线采集未联调；目录中的 SQL 模板也不应在未核对 DM8 版本系统视图前直接执行。

密码经 stdin 送给 `/nolog` 会话，不出现在 disql 命令行、日志或子进程环境中；为避免连接语法注入，密码仅支持安全字符集。

密码字符受安全连接语法限制；密码经 stdin 送给 `/nolog` 会话，不出现在 disql 命令行、日志或子进程环境中。

## 测试与限制

运行测试：

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

P2 已验证 SOURCE 离线采集、重复摘要、输入顺序变化、字段/主键/行数/聚合变化检测、结构和约束差异、缺失证据、非法输入及 disql 标记解析。DM8 目录元数据、真实数据库查询和 `DATABASE -> RESTORED` 恢复验收仍待 P1 环境恢复后联调。

P3/P4 可直接复用 `baseline.json` 作为备份前和恢复后输入：备份/恢复流程负责生成 `DATABASE` 或 `RESTORED` 基线，本工具负责比较和报告，不执行备份、恢复、主备切换或故障接管。
