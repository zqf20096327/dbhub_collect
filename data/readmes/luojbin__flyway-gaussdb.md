# Flyway GaussDB扩展插件

这个插件为Flyway提供了GaussDB数据库的支持，特别是适配不同的GaussDB模式类型。

## 支持的GaussDB模式

目前支持以下四种GaussDB模式：

1. **集中式MySQL B模式** (`gaussdb_centralized_mysql_b`)
2. **集中式MySQL M模式** (`gaussdb_centralized_mysql_m`)
3. **分布式MySQL B模式** (`gaussdb_distributed_mysql_b`)
4. **分布式MySQL M模式** (`gaussdb_distributed_mysql_m`)

> **注意**：当前仅在集中式MySQL M模式中测试通过，其他三种模式暂未完全适配与测试，使用时可能存在兼容性问题。

## 代码结构说明

本扩展采用工厂模式设计，将不同GaussDB模式的实现拆分为独立的类

- **`CompatibleModeEnum`**：兼容模式枚举类，定义了所有兼容模式
- **`CompatibleModeHandler`**：抽象接口，定义了所有需要根据模式实现不同行为的方法
- **`CompatibleModeHandlerFactory`**：工厂类，负责创建和管理不同模式的实现实例
- **兼容模式实现类**：
  - **MySQL兼容模式**
    - `AbstractMysqlHandler`：Mysql 抽象基类，提供各个 Mysql 模式的默认实现，减少重复代码
    - `CentralizedMySQLMHandler`：集中式MySQL M模式的实现, 继承 AbstractMysqlHandler
    - `CentralizedMySQLBHandler`：集中式MySQL B模式的实现, 继承 AbstractMysqlHandler
    - `DistributedMySQLMHandler`：分布式MySQL M模式的实现, 继承 AbstractMysqlHandler
    - `DistributedMySQLBHandler`：分布式MySQL B模式的实现, 继承 AbstractMysqlHandler
  - **Oracle兼容模式**
    - 暂未提供任何 Oracle 兼容模式的实现类

### 扩展新模式的步骤

要扩展新的GaussDB模式支持，只需：

1. 在`CompatibleModeEnum`枚举中添加新模式
2. 创建一个`CompatibleModeHandler`的实现类, 重写需要自定义的方法
3. 在`CompatibleModeFactory`中注册新的实现类

这种设计使得代码更加清晰、可维护，同时便于后续添加新的模式支持。

## 配置方法

### 通过配置文件设置模式

在`flyway.conf`文件中添加：

```properties
# 可以设置为 CompatibleModeEnum 中定义的类型
flyway.gaussdb.compatibleMode=gaussdb_centralized_mysql_m
```

### 通过环境变量设置模式

```bash
# Windows
set FLYWAY_GAUSSDB_COMPATIBLE_MODE=gaussdb_centralized_mysql_m

# Unix/Linux
FLYWAY_GAUSSDB_COMPATIBLE_MODE=gaussdb_centralized_mysql_m
```

### 通过Java API设置模式

```java
Flyway flyway = Flyway.configure()
    .dataSource(url, user, password)
    .configuration(Collections.singletonMap("flyway.gaussdb.compatibleMode", "gaussdb_centralized_mysql_m"))
    .load();
```

### 通过命令行参数设置模式

```bash
flyway -url=jdbc:gaussdb://localhost:8000/test -user=admin -password=password -flyway.gaussdb.compatibleMode=gaussdb_centralized_mysql_m migrate
```

## 模式特性

### MySQL 模式（所有支持的模式）

- 表创建使用MySQL风格的语法（VARCHAR, BOOLEAN等类型）
- 支持#注释
- 分隔符更改在单个语句之后仍然有效
- 使用反引号作为标识符引号

## 事务锁定配置

除了模式配置外，还可以配置事务锁定行为：

```properties
# 是否使用事务锁定（默认为false）
flyway.gaussdb.transactional.lock=false
```

## 使用说明

1. **Maven依赖**：

```xml
<dependency>
    <groupId>org.flywaydb</groupId>
    <artifactId>flyway-gaussdb</artifactId>
    <version>当前版本</version>
</dependency>
```

2. **基本使用**：

```java
// 基本使用
Flyway flyway = Flyway.configure()
    .dataSource("jdbc:gaussdb://localhost:54321/database", "username", "password")
    .configuration(Collections.singletonMap("flyway.gaussdb.compatibleMode", "gaussdb_centralized_mysql_m"))
    .load();

// 执行迁移
flyway.migrate();
```

## 注意事项

1. 确保使用正确的JDBC驱动程序
2. 不同模式下的SQL语法可能有所不同，请注意编写兼容的SQL脚本
3. 对于分布式模式，可能需要特别注意表的分布策略

## TODO项目

以下是待实现的功能：

- [ ] 完善`gaussdb_centralized_mysql_b`模式的适配
- [ ] 完善`gaussdb_distributed_mysql_m`模式的适配
- [ ] 完善`gaussdb_distributed_mysql_b`模式的适配
- [ ] 针对分布式模式优化连接处理
- [ ] 为不同模式添加更详细的文档说明