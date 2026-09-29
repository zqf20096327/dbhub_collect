# PolarDB PostgreSQL 技能库

PolarDB PostgreSQL 数据库管理和优化技能集合。

## 技能列表

| 技能 | 说明 | 状态 |
|------|------|------|
| [routine-check](skills/routine-check/) | 日常巡检、健康检查 | ✅ 可用 |
| [performance-tuning](skills/performance-tuning/) | 性能调优、SQL优化 | ✅ 可用 |
| [slow-query](skills/slow-query/) | 慢查询诊断与优化 | ✅ 可用 |
| [polardb-pg-openapi](skills/polardb-pg-openapi/) | PolarDB OpenAPI 管理与运维 | ✅ 可用 |
| [polardb-pg-gawr](skills/polardb-pg-gawr/) | GAWR 历史监控数据分析 | ✅ 可用 |

## 快速开始

```bash
# 连接数据库执行巡检
psql -h host -U user -d database -f skills/routine-check/queries/db-basic.sql
```

## 项目结构

```
polardb-pg-skills/
├── skills/                       # 技能目录
│   ├── routine-check/            # 日常巡检
│   │   ├── SKILL.md             # 技能定义
│   │   └── queries/             # SQL 查询
│   ├── performance-tuning/       # 性能调优
│   │   ├── SKILL.md
│   │   └── queries/
│   ├── slow-query/              # 慢查询诊断
│   │   ├── SKILL.md
│   │   └── queries/
│   ├── polardb-pg-openapi/       # PolarDB OpenAPI
│   │   ├── SKILL.md
│   │   ├── scripts/             # Python 脚本
│   │   └── references/          # 参考文档
│   └── polardb-pg-gawr/          # GAWR 历史监控数据分析
│       ├── SKILL.md
│       └── queries/
├── shared/                       # 共享资源
│   ├── thresholds.md            # 通用阈值
│   └── templates/               # SQL 模板
└── CLAUDE.md                    # Claude Code 指南
```

## 技能详情

### routine-check (日常巡检)

数据库健康检查和日常巡检，包含:
- 数据库概览 (版本、大小、事务ID年龄)
- 表统计 (死元组、Vacuum 状态)
- 索引分析 (使用率、冗余索引)
- 连接状态 (空闲事务、长查询)
- 复制状态 (延迟、WAL 状态)
- 配置审查

### performance-tuning (性能调优)

SQL 性能优化和调优建议，包含:
- 查询分析 (慢查询识别)
- 索引优化 (建议、效率分析)
- 缓存分析 (缓冲区命中率)
- 锁分析 (等待、阻塞)
- 内存调优

### slow-query (慢查询诊断)

系统性的慢 SQL 分析和优化，包含:
- 慢查询检测 (pg_stat_statements、auto_explain)
- 统计信息分析
- 执行计划分析
- Join 优化
- 索引优化建议
- 配置调优

### polardb-pg-openapi (OpenAPI 管理)

通过阿里云 OpenAPI 管理 PolarDB PostgreSQL，包含:
- 集群生命周期管理
- 参数配置
- 状态查询
- API 元数据发现

### polardb-pg-gawr (GAWR 历史监控分析)

基于 PolarDB GAWR 系统的历史监控数据分析，通过直连实例数据库查询，包含:
- 资源使用趋势 (CPU / 内存 / IO / 文件系统)
- 数据库性能 (TPS/QPS、连接数、缓存命中率、等待事件)
- 复制与延迟 (PolarDB 特有的并行回放延迟)
- SQL 分析 (Top SQL 历史快照)
- 存储空间 (WAL / 表大小 / 事务 ID 年龄)
- 异常事件 (ERROR / FATAL / OOM / Core dump)

## 许可证

MIT
