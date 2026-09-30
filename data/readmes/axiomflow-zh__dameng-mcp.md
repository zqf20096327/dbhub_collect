# 达梦数据库 MCP Server

> 使用 JDBC 连接达梦数据库，暴露为 MCP 工具，供 AI 编码助手直接查询。

## 新增优化

- JDBC statement 级查询超时（并保留 timer fallback）
- `describe_table` 现在包含主键 / 唯一约束 / 外键信息
- 新增 `dameng_health_check`
- 新增 `dameng_list_indexes`
- 新增 `dameng_list_procedures`
- 新增 `dameng_list_triggers`
- 新增 `dameng_list_synonyms`
- 增加 MCP `list_tools` 启动验证测试

## 快速开始

```bash
cd dameng-mcp
pip install -e .
cp .env.example .env
python -m dameng_mcp.server
```

## MCP 工具

| 工具 | 用途 |
|---|---|
| `dameng_query` | 执行只读 SQL |
| `dameng_list_schemas` | 列出 schema |
| `dameng_list_tables` | 列出表 |
| `dameng_describe_table` | 查看表结构、主键、唯一约束、外键 |
| `dameng_list_views` | 列出视图 |
| `dameng_list_indexes` | 查看指定表索引 |
| `dameng_list_procedures` | 列出过程对象（存储过程 / 函数 / 包） |
| `dameng_list_triggers` | 列出触发器 |
| `dameng_list_synonyms` | 列出同义词 |
| `dameng_explain` | 查看执行计划 |
| `dameng_health_check` | 检查连接健康与延迟 |

## 测试

```bash
pytest tests/ -v
```

真实数据库联调：

```bash
DM_TEST_HOST=... \
DM_TEST_PORT=5236 \
DM_TEST_DATABASE=... \
DM_TEST_USER=SYSDBA \
DM_TEST_PASSWORD=... \
DM_TEST_SCHEMA=... \
JAVA_HOME=... \
pytest tests/ -v
```
