# dm-r2dbc

> 达梦数据库原生响应式 R2DBC 驱动 — 基于 Netty 异步 I/O + ezorm 方言支持

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Java](https://img.shields.io/badge/Java-8+-green.svg)](https://openjdk.org)
[![Status](https://img.shields.io/badge/Status-Experimental-orange.svg)](https://github.com)

---

## 项目简介

**dm-r2dbc** 是达梦数据库（DM8）的原生响应式 R2DBC 驱动，采用**混合架构**设计：

- **网络传输层**：基于 Netty 实现真正的异步非阻塞 I/O，替代 JDBC 驱动默认的阻塞式 Socket
- **ORM 方言层**：完整实现 ezorm（hsweb-easy-orm-rdb）达梦方言，支持 Spring Data R2DBC 开箱即用

### 为什么需要这个项目？

| 对比项 | 官方 JDBC | 官方 R2DBC (桥接) | **dm-r2dbc** |
|--------|-----------|-------------------|-------------|
| 网络层 | 阻塞 Socket | 阻塞 Socket | **Netty 异步 I/O** |
| 真正异步 | ❌ | ❌ (伪异步) | ✅ |
| 协议复用 | — | — | **复用 JDBC 驱动** |
| ezorm 方言 | ❌ | ❌ | ✅ |
| Spring Data R2DBC | ❌ | ⚠️ 基础 | ✅ 完整 |

---

## 核心特性

### 🚀 原生响应式驱动

- 完整实现 R2DBC SPI 1.0.0 接口（`ConnectionFactory` / `Connection` / `Statement` / `Result` / `Row`）
- Netty EventLoop 驱动网络 I/O，`Schedulers.boundedElastic()` 隔离阻塞调用
- 支持事务（begin / commit / rollback / savepoint）
- 支持批量执行、参数绑定、自增主键返回
- 支持 CLOB / BLOB 大字段流式读写
- 支持命名参数绑定（`bind(String, Object)`），通过达梦 `DmdbParameterMetaData.getParameterName()` 获取参数名映射
- 支持存储过程调用（`CallableStatement`），包括 OUT / INOUT 参数注册与获取

### 🗣️ ezorm 达梦方言

完整实现 ezorm RDB 方言体系，可直接在 hsweb 4.x / 5.x 框架中使用：

| 方言组件 | 类名 | 说明 |
|---------|------|------|
| 方言定义 | `DmDialect` | 达梦 SQL 方言，标识符引用、类型映射 |
| 分页 | `DmPaginator` | 原生 `LIMIT ? OFFSET ?` 语法 |
| 建表 | `DmCreateTableSqlBuilder` | 达梦建表语法 |
| 修改表 | `DmAlterTableSqlBuilder` | 独立实现 ALTER TABLE |
| 插入 | `DmInsertSqlBuilder` | INSERT 语法，委托 Oracle 实现 |
| 批量更新插入 | `DmBatchUpsertOperator` | MERGE INTO 语法（达梦原生支持） |
| 索引解析 | `DmIndexMetadataParser` | 系统视图解析索引元数据 |
| 表元数据解析 | `DmTableMetadataParser` | 系统视图解析表结构 |
| 枚举位运算 | `DmEnumInFragmentBuilder` | IN / NOT IN 枚举位运算 |
| 异常翻译 (R2DBC) | `DmR2DBCExceptionTranslation` | R2DBC 异常 → ezorm 标准异常 |
| 异常翻译 (JDBC) | `DmJdbcExceptionTranslation` | JDBC 异常 → ezorm 标准异常 |
| Schema 元数据 | `DmSchemaMetadata` | 达梦 Schema 注册与特性管理 |

### 🛡️ 异常翻译体系

将达梦数据库错误码翻译为 ezorm 标准异常，覆盖 **13 个常见错误码**：

| 达梦错误码 | 含义 | 翻译为 |
|-----------|------|--------|
| -6602, -6610, -6611, -6612, 23505 | 唯一约束违反 | `DuplicateKeyException(false)` |
| -6608 | 主键约束违反 | `DuplicateKeyException(true)` |
| -6609 | 非空约束违反 | `DmConstraintViolationException(NOT_NULL)` |
| -6607 | 外键/引用约束违反 | `DmConstraintViolationException(FOREIGN_KEY)` |
| -6603 | CHECK 约束违反 | `DmConstraintViolationException(CHECK)` |
| -6407, -6004 | 锁超时 | `DmLockTimeoutException` |
| -6001, -6007 | 连接异常 | `DmConnectionException` |
| -104 | 表不存在 | `DmObjectNotFoundException` |
| -6103 | 除零错误 | `DmDataException` |
| -7046 | SELECT INTO 多行 | `DmDataException` |

> R2DBC 和 JDBC 两个通道均已增强，并支持递归 cause 链查找。

---

## 快速开始

### 1. 添加依赖

```xml
<dependency>
    <groupId>org.dameng</groupId>
    <artifactId>dm-r2dbc</artifactId>
    <version>1.0-SNAPSHOT</version>
</dependency>
```

> 需要达梦 JDBC 驱动 `DmJdbcDriver8:8.1.3.62` 在 classpath 中。

### 2. 编程式使用

```java
import io.r2dbc.spi.ConnectionFactories;
import io.r2dbc.spi.ConnectionFactoryOptions;

import static io.r2dbc.spi.ConnectionFactoryOptions.*;

ConnectionFactoryOptions options = ConnectionFactoryOptions.builder()
    .option(DRIVER, "dm")
    .option(HOST, "localhost")
    .option(PORT, 5236)
    .option(USER, "SYSDBA")
    .option(PASSWORD, "Admin123")
    .build();

ConnectionFactory factory = ConnectionFactories.get(options);

Mono.from(factory.create())
    .flatMap(conn ->
        Mono.from(conn.createStatement("SELECT ID, NAME FROM USERS WHERE ID = ?")
                .bind(0, 1)
                .execute())
            .flatMapMany(result -> result.map((row, meta) ->
                new User(row.get(0, Long.class), row.get(1, String.class))))
            .then(Mono.from(conn.close()))
    )
    .subscribe();
```

### 3. 连接字符串方式

```java
ConnectionFactory factory = ConnectionFactories.get(
    "r2dbc:dm://SYSDBA:Admin123@localhost:5236"
);
```

### 4. Spring WebFlux 集成

```yaml
spring:
  r2dbc:
    url: r2dbc:dm://localhost:5236
    username: SYSDBA
    password: Admin123
```

### 5. 事务使用

```java
Mono.from(factory.create())
    .flatMap(conn ->
        conn.beginTransaction()
            .then(/* 执行 SQL */)
            .then(conn.commitTransaction())
            .onErrorResume(e -> conn.rollbackTransaction().then(Mono.error(e)))
            .then(Mono.from(conn.close()))
    )
    .subscribe();
```

### 6. 命名参数绑定

达梦 JDBC 驱动支持通过 `ParameterMetaData.getParameterName()` 获取参数名，本驱动利用此特性实现命名参数绑定：

```java
Mono.from(factory.create())
    .flatMap(conn ->
        Mono.from(conn.createStatement("SELECT ID, NAME FROM USERS WHERE ID = :id AND NAME = :name")
                .bind("id", 1)          // 通过参数名绑定
                .bind("name", "admin")  // 大小写不敏感
                .execute())
            .flatMapMany(result -> result.map((row, meta) ->
                new User(row.get(0, Long.class), row.get(1, String.class))))
            .then(Mono.from(conn.close()))
    )
    .subscribe();
```

> 参数名来源于达梦 `DmdbParameterMetaData.getParameterName()`，支持大小写不敏感匹配。如果无法获取参数名，则回退到位置索引（`"1"`, `"2"`, ...）。

### 7. 存储过程调用（OUT / INOUT 参数）

本驱动自动识别 `{CALL ...}` 和 `{?= CALL ...}` 语法的 SQL，创建 `DmCallableStatement`：

```java
Mono.from(factory.create())
    .flatMap(conn -> {
        DmCallableStatement cstmt = ((DmConnection) conn)
            .createCallableStatement("{CALL ADD_USER(?, ?, ?)}");

        cstmt.bind(0, "admin")                          // IN 参数
             .bind(1, "password")                        // IN 参数
             .registerOutParameter(2, Types.VARCHAR);    // OUT/INOUT 参数

        return Mono.from(cstmt.execute())
            .flatMapMany(result ->
                result.flatMap(segment -> {
                    if (segment instanceof Result.OutSegment) {
                        OutParameters outParams = ((Result.OutSegment) segment).outParameters();
                        String outValue = outParams.get(0, String.class);
                        return Mono.just(outValue);
                    }
                    return Mono.empty();
                })
            )
            .then(Mono.from(conn.close()));
    })
    .subscribe();
```

> `registerOutParameter(index, sqlType)` 使用 R2DBC 的 0-based 索引（JDBC 内部自动 +1 转换）。支持通过 `OutParameters.get(name, type)` 按参数名获取输出值。

---

## 连接选项

| 选项 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `HOST` | String | localhost | 数据库主机 |
| `PORT` | Integer | 5236 | 数据库端口 |
| `USER` | String | 必填 | 用户名 |
| `PASSWORD` | String | 必填 | 密码 |
| `DATABASE` | String | null | 数据库/Schema |
| `schema` | String | null | Schema (同 DATABASE) |
| `ssl` | Boolean | false | SSL 连接 |
| `autoCommit` | Boolean | true | 自动提交 |
| `connectTimeout` | Integer | 5000 | 连接超时 (ms) |
| `socketTimeout` | Integer | 0 | Socket 超时 (ms) |

---

## 数据类型支持

| 达梦类型 | Java 类型 | 状态 |
|---------|----------|------|
| INT / INTEGER / BIGINT | Long | ✅ |
| SMALLINT / TINYINT | Integer | ✅ |
| FLOAT / DOUBLE | Double | ✅ |
| DECIMAL / NUMBER | BigDecimal | ✅ |
| CHAR / VARCHAR | String | ✅ |
| CLOB / TEXT | String | ✅ |
| BLOB | byte[] | ✅ |
| DATE | LocalDate | ✅ |
| TIME | LocalTime | ✅ |
| TIMESTAMP / DATETIME | LocalDateTime | ✅ |
| TIMESTAMP WITH TIME ZONE | OffsetDateTime | ✅ |
| BOOLEAN | Boolean | ✅ |
| VARBINARY | byte[] | ✅ |
| BIT | Boolean | ⚠️ 转换可能丢失精度 |
| XML | String | ⚠️ 作为 CLOB 读取 |
| ARRAY / STRUCT / REF CURSOR | — | ❌ |

---

## 架构概览

```
┌──────────────────────────────────────────────────┐
│            应用层 (Spring WebFlux / hsweb)        │
├──────────────────────────────────────────────────┤
│         R2DBC SPI (io.r2dbc.spi)                 │
├──────────────────────────────────────────────────┤
│         dm-r2dbc 驱动层                           │
│  ┌────────────────────────────────────────────┐  │
│  │  R2DBC API 适配层                           │  │
│  │  DmConnection / DmStatement / DmResult     │  │
│  ├────────────────────────────────────────────┤  │
│  │  ezorm 方言层                               │  │
│  │  DmDialect / DmPaginator / DmSchemaMeta... │  │
│  ├────────────────────────────────────────────┤  │
│  │  协议编解码层 (复用 JDBC 驱动)               │  │
│  ├────────────────────────────────────────────┤  │
│  │  Netty 异步传输层 (替换阻塞 Socket)          │  │
│  │  DmNettyTransport / DmNettyResponsePipeline │  │
│  └────────────────────────────────────────────┘  │
├──────────────────────────────────────────────────┤
│         达梦数据库服务端 (TCP 5236)               │
└──────────────────────────────────────────────────┘
```

---

## 项目结构

```
dm-r2dbc/
├── src/main/java/org/dameng/r2dbc/
│   ├── DmConnection.java              # R2DBC Connection 实现
│   ├── DmStatement.java               # R2DBC Statement 实现（支持命名参数绑定）
│   ├── DmCallableStatement.java       # R2DBC 存储过程调用（OUT/INOUT 参数）
│   ├── DmResult.java                  # R2DBC Result 实现
│   ├── DmRow.java                     # R2DBC Row 实现
│   ├── DmBatch.java                   # R2DBC Batch 实现
│   ├── DmConnectionFactory.java       # R2DBC ConnectionFactory 实现
│   ├── DmConnectionFactoryProvider.java  # R2DBC SPI 入口
│   ├── DmR2dbcException.java          # 达梦 R2DBC 异常定义
│   ├── transport/
│   │   ├── DmNettyTransport.java      # Netty 异步传输实现
│   │   └── DmNettyResponsePipeline.java  # Netty 响应处理管线
│   └── dialect/                       # ezorm 方言层
│       ├── DmDialect.java             # 方言定义
│       ├── DmSchemaMetadata.java      # Schema 元数据
│       ├── DmPaginator.java           # 分页 (LIMIT/OFFSET)
│       ├── DmCreateTableSqlBuilder.java   # 建表
│       ├── DmAlterTableSqlBuilder.java    # 修改表
│       ├── DmInsertSqlBuilder.java        # 插入
│       ├── DmBatchUpsertOperator.java     # 批量更新插入 (MERGE INTO)
│       ├── DmIndexMetadataParser.java     # 索引元数据解析
│       ├── DmTableMetadataParser.java     # 表元数据解析
│       ├── DmEnumInFragmentBuilder.java   # 枚举位运算
│       ├── DmR2DBCExceptionTranslation.java  # R2DBC 异常翻译
│       ├── DmJdbcExceptionTranslation.java   # JDBC 异常翻译
│       ├── DmConstraintViolationException.java  # 约束违反异常
│       ├── DmLockTimeoutException.java         # 锁超时异常
│       ├── DmConnectionException.java          # 连接异常
│       ├── DmObjectNotFoundException.java      # 对象不存在异常
│       └── DmDataException.java                # 数据异常
└── src/main/resources/
    └── META-INF/services/
        └── io.r2dbc.spi.ConnectionFactoryProvider
```

---

## 兼容性说明

### 达梦兼容模式

达梦数据库支持 Oracle、MySQL、PostgreSQL 三种兼容模式。本驱动核心特性在各模式下均可用：

| 特性 | Oracle 兼容 | MySQL 兼容 | PG 兼容 |
|------|:---------:|:--------:|:-----:|
| LIMIT/OFFSET 分页 | ✅ | ✅ | ✅ |
| MERGE INTO | ✅ | ✅ | ✅ |
| 系统视图 (all_indexes 等) | ✅ | ✅ | ✅ |
| 唯一约束错误码 (-6602) | ✅ | ✅ | ✅ |
| SQL 标准错误码 (23505) | ✅ | ✅ | ✅ |

### 版本要求

- **达梦数据库**：DM8+
- **JDBC 驱动**：DmJdbcDriver8 8.1.3.62（版本锁定，反射注入依赖内部字段名）
- **Java**：8+
- **Reactor**：3.6.6+
- **Netty**：4.1.112+

---

## 已知限制

### 达梦数据库本身限制

| 限制 | 说明 |
|------|------|
| ARRAY / STRUCT | 达梦对复合类型支持有限，本驱动暂不支持 |

### 其他限制

| 限制 | 说明 |
|------|------|
| 反射注入 | 替换 JDBC 驱动内部传输字段，依赖特定版本 (8.1.3.62) |
| 连接池 | 需上层集成 `r2dbc-pool` |

---

## ⚠️ 免责声明

本项目**仅供技术研究与学习**，不建议直接用于生产环境。

- 本项目复用达梦官方 JDBC 驱动的公开传输接口，通过反射将默认阻塞式 Socket 替换为 Netty 异步传输
- 使用本项目所产生的一切风险由使用者自行承担

---

## 详细设计

完整的技术设计文档请参阅 [TECHNICAL_DESIGN.md](TECHNICAL_DESIGN.md)，包含：

- 架构分层设计与线程模型
- 反射注入传输层机制
- Buffer 生命周期管理
- 协议交互流程
- 性能基准测试方案
- 后续优化方向（异步读取优化、连接池适配等）

---

## License

Apache License 2.0