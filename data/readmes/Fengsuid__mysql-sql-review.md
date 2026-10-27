# mysql-sql-review：MySQL 兼容 SQL 审查助手

把 SQL 贴给 Agent，按“正确性 → 性能 → 安全 → 可维护性”逐项审查，得到分级问题表、语义等价的改写 SQL 和验证方法。适用于 MySQL 及 MySQL 兼容数据库，如 OceanBase MySQL 模式、seekdb、TiDB。

## 能做什么

- 找出会让**结果出错**的写法：AND/OR 优先级、`NOT IN` 遇到 NULL、`LEFT JOIN` 退化、时间边界、`LIMIT` 无排序等。
- 找出**性能隐患**：索引列上用函数、隐式类型转换、前导 `%` 模糊查询、深分页、`SELECT *`、大事务等。
- 提示**安全风险**：SQL 注入、无保护的 UPDATE/DELETE、锁表 DDL。
- 给出**改写 SQL**和用 `EXPLAIN` 自行验证的方法。缺少表结构或执行计划时明确写出前提，不编造耗时数据。

本 Skill 只做静态审查，不连接数据库，也不执行任何 SQL。

## 使用方法

1. 把 `mysql-sql-review` 文件夹（包含 `SKILL.md`）放到你所用 Agent 的 Skills 目录，或在支持 Skill 的平台导入。
2. 对 Agent 说“帮我审查这条 SQL”，并贴出 SQL。
3. 想要更准确的结论，可以一并提供：
   - 业务意图；
   - `SHOW CREATE TABLE` 的结果；
   - 大致数据量；
   - `EXPLAIN` 的输出。

## 使用示例

**输入**

> 帮我看看这条 SQL 有什么问题：
>
> ```sql
> SELECT * FROM orders
> WHERE DATE(created_at) = '2026-10-01' AND status = 1 OR user_id = 42
> ORDER BY id LIMIT 100000, 20;
> ```

**输出（节选）**

| # | 级别 | 问题 | 建议 |
| --- | --- | --- | --- |
| 1 | 严重 | `AND ... OR user_id = 42` 实际为 `(A AND B) OR C`，会返回 user_id = 42 的全部订单 | 按意图加括号，并请确认 |
| 2 | 警告 | `DATE(created_at)` 使该列索引无法直接使用 | 改为 `created_at >= '2026-10-01' AND created_at < '2026-10-02'` |
| 3 | 警告 | `LIMIT 100000, 20` 深分页 | 改为 `AND id > ? ... LIMIT 20` 游标分页 |
| 4 | 建议 | `SELECT *` | 只查需要的列 |

需确认：`status` 列的类型（若为字符串会发生隐式转换），以及条件组合的真实意图。

## 文件

- `SKILL.md`：Skill 本体，包含审查步骤、判定原则和输出格式。
- `README.md`：本说明。

## 许可证

MIT，见 `LICENSE`。
