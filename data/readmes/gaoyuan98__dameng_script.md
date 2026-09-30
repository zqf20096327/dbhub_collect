# dameng_script

达梦数据库脚本仓库，目前主要收录 `DM_SQL_RPT`，用于按 `EXEC_ID` 汇总一次 SQL 执行的诊断信息。

## 目录结构

```text
.
├─ README.md
└─ DM_SQL_RPT
   ├─ DM_SQL_RPT_v1.0_sourcecode.sql
   └─ README.md
```

## DM_SQL_RPT 简介

`DM_SQL_RPT` 是一个 SQL 诊断包，围绕 `EXEC_ID` 输出一次执行相关的关键信息，主要包括：

- 表信息
- 索引信息
- 统计信息
- 执行计划
- ET 节点运行信息
- 缓存执行计划相关信息

## 快速使用

1. 在达梦数据库中执行 `DM_SQL_RPT/DM_SQL_RPT_v1.0_sourcecode.sql`
2. 获取需要分析的 SQL 对应 `EXEC_ID`
3. 调用总入口过程：

```sql
CALL DM_SQL_RPT.GET_ALL_INFO(11410);
```

## 相关文档

- 简版介绍和使用说明：`DM_SQL_RPT/README.md`
