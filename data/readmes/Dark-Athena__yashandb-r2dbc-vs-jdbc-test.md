# YashanDB JDBC vs R2DBC 性能测试

对比 YashanDB 数据库在 JDBC 和 R2DBC 两种驱动下的性能表现。

## 环境要求

- JDK 17+
- Maven 3.6+
- YashanDB 数据库实例

## 依赖说明

| 组件 | 版本 | 说明 |
|------|------|------|
| yashandb-jdbc | 1.9.24 | Maven Central |
| r2dbc-yashandb | 0.1.4 | [GitHub Releases](https://github.com/Dark-Athena/r2dbc-yashandb/releases) |
| HikariCP | 5.1.0 | JDBC 连接池 |
| r2dbc-pool | 1.0.1 | R2DBC 连接池 |
| Reactor Core | 3.6.0 | 响应式核心库 |

## 快速开始

### 1. 下载 R2DBC 驱动

```bash
mkdir -p libs
curl -L -o libs/r2dbc-yashandb-0.1.4.jar \
  https://github.com/Dark-Athena/r2dbc-yashandb/releases/download/v0.1.4/r2dbc-yashandb-0.1.4.jar
```

### 2. 配置数据库连接

编辑 `src/main/resources/application.properties`:

```properties
db.host=192.168.163.134
db.port=1688
db.username=sys
db.password=your_password
```

### 3. 运行测试

```bash
mvn compile exec:java
```

## 测试场景

| 场景 | 说明 |
|------|------|
| Simple Query | 单条查询 |
| Batch Query (1K/10K) | 批量查询 |
| Simple Insert | 单条插入 |
| Batch Insert (100) | 批量插入（使用 Statement.add()） |
| Concurrent Query (10/50) | 并发查询 |
| Concurrent Insert (10/50) | 并发插入 |
| Transaction | 多语句事务 |

## 测试结果示例

```
============================================================
Test: Batch Insert (100 rows) [R2DBC]
============================================================
Total Operations:    10
Successful:          10
Errors:              0 (0.00%)
Total Time:          1200.00 ms
------------------------------------------------------------
Throughput:          8.33 ops/sec
============================================================
```

## 性能对比结果

> 测试环境: YashanDB 23.2, JDK 17, 10 轮迭代

### 吞吐量对比 (ops/sec)

| 测试场景 | JDBC | R2DBC | 胜者 |
|---------|-----:|------:|:----:|
| Simple Query | 1127.96 | 1146.50 | R2DBC |
| Batch Query (1K rows) | - | - | 平局 |
| Batch Query (10K rows) | - | - | 平局 |
| Simple Insert | 1109.88 | 1139.64 | R2DBC |
| **Batch Insert (100 rows)** | **53.15** | **84.83** | **R2DBC** |
| Concurrent Query (10 threads) | 1109.88 | 1109.16 | 平局 |
| Concurrent Query (50 threads) | 2548.80 | 2588.96 | R2DBC |
| Concurrent Insert (10 threads) | 95.97 | 92.86 | JDBC |
| **Concurrent Insert (50 threads)** | **124.25** | **170.00** | **R2DBC** |
| Transaction | 3.25 | 3.23 | 平局 |

### 延迟对比 (ms)

| 测试场景 | JDBC Avg | R2DBC Avg | JDBC P95 | R2DBC P95 |
|---------|--------:|---------:|--------:|---------:|
| Simple Query | 88.67 | 87.22 | 93.48 | 92.41 |
| Batch Query (1K) | 201.60 | 194.81 | 213.05 | 206.93 |
| Batch Query (10K) | 878.61 | 863.48 | 920.68 | 912.70 |
| Simple Insert | 89.98 | 87.67 | 96.69 | 96.74 |
| Batch Insert (100) | 188.15 | 117.88 | 194.55 | 141.93 |
| Concurrent Insert (50) | 313.68 | 224.35 | 568.77 | 285.07 |

### 结论

| 统计 | 数量 |
|-----|-----:|
| JDBC 胜出 | 1 |
| R2DBC 胜出 | 4 |
| 平局 | 5 |

**关键发现:**
- R2DBC 基于 JDBC 桥接实现，大部分场景性能相近
- **批量插入**: R2DBC 使用 `Statement.add()` 比 JDBC 快 **60%**
- **高并发插入**: R2DBC 非阻塞 I/O 优势明显，吞吐量提升 **37%**
- 简单同步操作两者性能基本持平

**适用场景:**
- **JDBC**: 传统应用、简单 CRUD、低延迟要求
- **R2DBC**: 响应式应用、高并发场景、Spring WebFlux 集成

## 项目结构

```
├── libs/                          # R2DBC 驱动 jar
├── src/main/java/com/test/
│   ├── PerformanceTestApplication.java  # 主入口
│   ├── jdbc/
│   │   └── JdbcPerformanceTest.java     # JDBC 测试
│   ├── r2dbc/
│   │   └── R2dbcPerformanceTest.java    # R2DBC 测试
│   └── report/
│       └── ReportGenerator.java         # 报告生成
└── src/main/resources/
    └── application.properties           # 配置文件
```

## 注意事项

1. **R2DBC 事务提交**: r2dbc-yashandb v0.1.4 默认 `autoCommit=false`，需显式调用 `commitTransaction()`
2. **批量插入**: 使用 `Statement.add()` 实现批量绑定，驱动内部转换为 JDBC `executeBatch()`
3. **表隔离**: JDBC 和 R2DBC 使用独立表 (`PERF_TEST_JDBC` / `PERF_TEST_R2DBC`) 避免干扰

## License

MIT
