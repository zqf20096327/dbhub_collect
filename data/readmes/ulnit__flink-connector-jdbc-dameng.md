# Flink Connector JDBC Dameng

Apache Flink 的达梦数据库 JDBC 连接器，支持 Flink 1.20.x 版本。

## 概述

该连接器为 Apache Flink 提供了与达梦数据库的集成能力，支持：

- 读取达梦数据库中的数据
- 向达梦数据库写入数据
- 支持批处理和流处理模式
- 支持 Upsert 操作（MERGE 语句）
- 完整的数据类型映射
- 优化的性能配置

## 系统要求

- Apache Flink 1.20.2+
- 达梦数据库 8.x
- Java 17+
- Maven 3.6+

## 安装与构建

### 1. 克隆项目

```bash
git clone <repository-url>
cd flink-connector-jdbc-dameng
```

### 2. 构建项目

```bash
mvn clean install
```

构建成功后会生成 `target/flink-connector-jdbc-dameng-1.0-SNAPSHOT.jar` 文件。

### 3. 部署到 Flink

将生成的 JAR 文件复制到 Flink 的 `lib` 目录：

```bash
cp target/flink-connector-jdbc-dameng-1.0-SNAPSHOT.jar $FLINK_HOME/lib/
```

## 依赖配置

### Maven 依赖

在你的项目中添加以下依赖：

```xml
<dependency>
    <groupId>org.apache.flink</groupId>
    <artifactId>flink-connector-jdbc-dameng</artifactId>
    <version>1.0-SNAPSHOT</version>
</dependency>
```

## 使用方法

### 1. 数据库连接配置

```java
import org.apache.flink.connector.jdbc.JdbcConnectionOptions;
import org.apache.flink.connector.jdbc.JdbcExecutionOptions;
import org.apache.flink.connector.jdbc.JdbcSink;

// JDBC 连接配置
JdbcConnectionOptions connectionOptions = new JdbcConnectionOptions.JdbcConnectionOptionsBuilder()
    .withUrl("jdbc:dm://localhost:5236/DAMENG")
    .withDriverName("dm.jdbc.driver.DmDriver")
    .withUsername("SYSDBA")
    .withPassword("SYSDBA")
    .build();

// 执行参数配置
JdbcExecutionOptions executionOptions = JdbcExecutionOptions.builder()
    .withBatchSize(1000)
    .withBatchIntervalMs(200)
    .withMaxRetries(5)
    .build();
```

### 2. 从达梦数据库读取数据

#### Table API 方式

```java
import org.apache.flink.table.api.EnvironmentSettings;
import org.apache.flink.table.api.TableEnvironment;

// 创建 Table Environment
EnvironmentSettings settings = EnvironmentSettings.newInstance()
    .inStreamingMode()
    .build();
TableEnvironment tableEnv = TableEnvironment.create(settings);

// 创建达梦数据库表连接
tableEnv.executeSql(
    "CREATE TABLE dameng_source (" +
    "  id BIGINT," +
    "  name STRING," +
    "  age INT," +
    "  salary DECIMAL(10,2)," +
    "  create_time TIMESTAMP(3)" +
    ") WITH (" +
    "  'connector' = 'jdbc'," +
    "  'url' = 'jdbc:dm://localhost:5236/DAMENG'," +
    "  'table-name' = 'users'," +
    "  'username' = 'SYSDBA'," +
    "  'password' = 'SYSDBA'," +
    "  'driver' = 'dm.jdbc.driver.DmDriver'" +
    ")"
);

// 查询数据
Table result = tableEnv.sqlQuery("SELECT * FROM dameng_source WHERE age > 25");
```

#### DataStream API 方式

```java
import org.apache.flink.connector.jdbc.JdbcSource;
import org.apache.flink.api.common.typeinfo.TypeInformation;
import org.apache.flink.types.Row;

// 创建 JDBC Source
JdbcSource<Row> jdbcSource = JdbcSource.<Row>builder()
    .setDBUrl("jdbc:dm://localhost:5236/DAMENG")
    .setDrivername("dm.jdbc.driver.DmDriver")
    .setUsername("SYSDBA")
    .setPassword("SYSDBA")
    .setQuery("SELECT id, name, age, salary FROM users")
    .setTypeInformation(TypeInformation.of(Row.class))
    .build();

// 添加到数据流
DataStream<Row> dataStream = env.fromSource(jdbcSource, WatermarkStrategy.noWatermarks(), "DamengSource");
```

### 3. 向达梦数据库写入数据

#### Table API 方式

```java
// 创建目标表
tableEnv.executeSql(
    "CREATE TABLE dameng_sink (" +
    "  id BIGINT," +
    "  name STRING," +
    "  age INT," +
    "  salary DECIMAL(10,2)," +
    "  create_time TIMESTAMP(3)" +
    ") WITH (" +
    "  'connector' = 'jdbc'," +
    "  'url' = 'jdbc:dm://localhost:5236/DAMENG'," +
    "  'table-name' = 'users_copy'," +
    "  'username' = 'SYSDBA'," +
    "  'password' = 'SYSDBA'," +
    "  'driver' = 'dm.jdbc.driver.DmDriver'" +
    ")"
);

// 插入数据
tableEnv.executeSql("INSERT INTO dameng_sink SELECT * FROM dameng_source");
```

#### DataStream API 方式

```java
// 创建 JDBC Sink
dataStream.addSink(JdbcSink.sink(
    "INSERT INTO users_copy (id, name, age, salary) VALUES (?, ?, ?, ?)",
    (statement, row) -> {
        statement.setLong(1, row.getFieldAs(0));
        statement.setString(2, row.getFieldAs(1));
        statement.setInt(3, row.getFieldAs(2));
        statement.setBigDecimal(4, row.getFieldAs(3));
    },
    executionOptions,
    connectionOptions
));
```

### 4. Upsert 操作

```java
// 使用 MERGE 语句进行 Upsert 操作
tableEnv.executeSql(
    "CREATE TABLE dameng_upsert (" +
    "  id BIGINT," +
    "  name STRING," +
    "  age INT," +
    "  salary DECIMAL(10,2)," +
    "  PRIMARY KEY (id) NOT ENFORCED" +
    ") WITH (" +
    "  'connector' = 'jdbc'," +
    "  'url' = 'jdbc:dm://localhost:5236/DAMENG'," +
    "  'table-name' = 'users'," +
    "  'username' = 'SYSDBA'," +
    "  'password' = 'SYSDBA'," +
    "  'driver' = 'dm.jdbc.driver.DmDriver'" +
    ")"
);

// 执行 Upsert
tableEnv.executeSql("INSERT INTO dameng_upsert SELECT * FROM source_table");
```

## 数据类型映射

| 达梦数据类型 | Flink 数据类型 | Java 类型 |
|------------|---------------|-----------|
| TINYINT | TINYINT | Byte |
| SMALLINT | SMALLINT | Short |
| INT | INT | Integer |
| BIGINT | BIGINT | Long |
| REAL | FLOAT | Float |
| DOUBLE | DOUBLE | Double |
| DECIMAL(p,s) | DECIMAL(p,s) | BigDecimal |
| CHAR(n) | CHAR(n) | String |
| VARCHAR(n) | VARCHAR(n) | String |
| TEXT | STRING | String |
| BINARY | BINARY | byte[] |
| VARBINARY | VARBINARY | byte[] |
| BLOB | BYTES | byte[] |
| CLOB | STRING | String |
| DATE | DATE | LocalDate |
| TIME | TIME | LocalTime |
| TIMESTAMP | TIMESTAMP | LocalDateTime |
| BOOLEAN | BOOLEAN | Boolean |

## 配置选项

### JDBC 连接选项

| 参数 | 类型 | 必需 | 默认值 | 描述 |
|------|------|------|-------|------|
| connector | String | 是 | 无 | 连接器类型，必须为 'jdbc' |
| url | String | 是 | 无 | JDBC 数据库 URL |
| table-name | String | 是 | 无 | 数据库表名 |
| driver | String | 否 | dm.jdbc.driver.DmDriver | JDBC 驱动类名 |
| username | String | 否 | 无 | 数据库用户名 |
| password | String | 否 | 无 | 数据库密码 |
| connection.max-retry-timeout | Duration | 否 | 60s | 连接超时时间 |

### 读取选项

| 参数 | 类型 | 必需 | 默认值 | 描述 |
|------|------|------|-------|------|
| scan.partition.column | String | 否 | 无 | 分区列名 |
| scan.partition.num | Integer | 否 | 无 | 分区数量 |
| scan.partition.lower-bound | Long | 否 | 无 | 分区下界 |
| scan.partition.upper-bound | Long | 否 | 无 | 分区上界 |
| scan.fetch-size | Integer | 否 | 0 | 每次获取的行数 |

### 写入选项

| 参数 | 类型 | 必需 | 默认值 | 描述 |
|------|------|------|-------|------|
| sink.buffer-flush.max-rows | Integer | 否 | 100 | 批量写入的最大行数 |
| sink.buffer-flush.interval | Duration | 否 | 1s | 刷新间隔 |
| sink.max-retries | Integer | 否 | 3 | 最大重试次数 |
| sink.parallelism | Integer | 否 | 无 | 写入并行度 |

## 性能优化

### 1. 批量写入优化

```java
JdbcExecutionOptions executionOptions = JdbcExecutionOptions.builder()
    .withBatchSize(5000)        // 增加批量大小
    .withBatchIntervalMs(1000)  // 设置合适的刷新间隔
    .withMaxRetries(3)          // 设置重试次数
    .build();
```

### 2. 连接池配置

```java
JdbcConnectionOptions connectionOptions = new JdbcConnectionOptions.JdbcConnectionOptionsBuilder()
    .withUrl("jdbc:dm://localhost:5236/DAMENG?useServerPrepStmts=false&rewriteBatchedStatements=true")
    .withDriverName("dm.jdbc.driver.DmDriver")
    .withUsername("SYSDBA")
    .withPassword("SYSDBA")
    .build();
```

### 3. 分区读取

```sql
CREATE TABLE dameng_source (
  id BIGINT,
  name STRING,
  age INT,
  salary DECIMAL(10,2)
) WITH (
  'connector' = 'jdbc',
  'url' = 'jdbc:dm://localhost:5236/DAMENG',
  'table-name' = 'users',
  'username' = 'SYSDBA',
  'password' = 'SYSDBA',
  'driver' = 'dm.jdbc.driver.DmDriver',
  'scan.partition.column' = 'id',
  'scan.partition.num' = '4',
  'scan.partition.lower-bound' = '1',
  'scan.partition.upper-bound' = '100000'
)
```

## 常见问题

### 1. 驱动未找到

确保达梦 JDBC 驱动 JAR 包在 Flink 的 classpath 中：

```bash
cp DmJdbcDriver11-8.1.4.41033.jar $FLINK_HOME/lib/
```

### 2. 连接超时

调整连接超时参数：

```java
.withUrl("jdbc:dm://localhost:5236/DAMENG?connectTimeout=60000&socketTimeout=60000")
```

### 3. 字符编码问题

在连接 URL 中指定字符集：

```java
.withUrl("jdbc:dm://localhost:5236/DAMENG?characterEncoding=utf8")
```

### 4. 事务隔离级别

```java
.withUrl("jdbc:dm://localhost:5236/DAMENG?defaultTransactionIsolation=2")
```

## 示例项目

完整的示例代码可以参考 `src/test/java` 目录下的测试用例。

### 简单的流处理示例

```java
public class DamengFlinkExample {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        
        // 设置检查点
        env.enableCheckpointing(5000);
        
        // JDBC 连接配置
        JdbcConnectionOptions connectionOptions = new JdbcConnectionOptions.JdbcConnectionOptionsBuilder()
            .withUrl("jdbc:dm://localhost:5236/DAMENG")
            .withDriverName("dm.jdbc.driver.DmDriver")
            .withUsername("SYSDBA")
            .withPassword("SYSDBA")
            .build();
        
        // 执行选项
        JdbcExecutionOptions executionOptions = JdbcExecutionOptions.builder()
            .withBatchSize(1000)
            .withBatchIntervalMs(200)
            .withMaxRetries(5)
            .build();
        
        // 从达梦数据库读取数据
        JdbcSource<Row> source = JdbcSource.<Row>builder()
            .setDBUrl("jdbc:dm://localhost:5236/DAMENG")
            .setDrivername("dm.jdbc.driver.DmDriver")
            .setUsername("SYSDBA")
            .setPassword("SYSDBA")
            .setQuery("SELECT id, name, age FROM users WHERE id > ?")
            .setParameterTypes(Types.INTEGER)
            .setParameters(100)
            .setTypeInformation(TypeInformation.of(Row.class))
            .build();
        
        // 处理数据流
        DataStream<Row> dataStream = env.fromSource(source, WatermarkStrategy.noWatermarks(), "DamengSource")
            .map(row -> {
                // 数据处理逻辑
                return Row.of(row.getField(0), row.getField(1), (Integer)row.getField(2) + 1);
            });
        
        // 写入到达梦数据库
        dataStream.addSink(JdbcSink.sink(
            "INSERT INTO users_processed (id, name, age) VALUES (?, ?, ?)",
            (statement, row) -> {
                statement.setLong(1, (Long) row.getField(0));
                statement.setString(2, (String) row.getField(1));
                statement.setInt(3, (Integer) row.getField(2));
            },
            executionOptions,
            connectionOptions
        ));
        
        // 执行作业
        env.execute("Dameng Flink Example");
    }
}
```

## 版本说明

- **1.0-SNAPSHOT**: 初始版本，支持基本的读写操作和 Upsert 功能

## 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 许可证

本项目采用 Apache License 2.0 许可证。详情请参阅 [LICENSE](LICENSE) 文件。

## 联系方式

如有问题或建议，请提交 Issue 或联系项目维护者。