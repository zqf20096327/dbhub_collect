# Multi-Database Test Framework

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Java](https://img.shields.io/badge/Java-8%2B-orange.svg)](https://www.oracle.com/java/)
[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-Compatible-brightgreen.svg)](https://spring.io/projects/spring-boot)

一个轻量级的多数据库测试框架，帮助开发者在多个数据库上运行相同的测试逻辑，避免重复的测试代码。

## ✨ 特性

- 🔄 **支持 MySQL 和 OceanBase** - 开箱即用的多数据库支持
- 🐳 **TestContainers 集成** - 自动管理数据库容器生命周期
- ⚡ **动态数据源切换** - 无需重启 Spring 容器即可切换数据库
- 📜 **自定义 SQL 初始化** - 支持数据库特定的初始化脚本
- 🔧 **Spring Boot 兼容** - 完全兼容 Spring Boot 和 MyBatis-Plus
- 💾 **内存优化** - 同一时间只运行一个数据库容器，节省资源
- 🎯 **零配置** - 最小化配置，专注测试逻辑
- 🚀 **高度可扩展** - 使用设计模式，轻松扩展新数据库类型

## 🚀 快速开始

### 添加依赖

在你的测试模块的 `build.gradle` 中添加：

```gradle
dependencies {
    testImplementation 'com.brianxiadong:multi-database-test-framework:1.0.0'
    testImplementation 'org.testcontainers:mysql'
    testImplementation 'org.testcontainers:junit-jupiter'
    testImplementation 'com.oceanbase:oceanbase-client'
}
```

### 创建初始化脚本

在 `src/test/resources/` 目录下创建数据库初始化脚本：

**init-mysql.sql**
```sql
-- MySQL 初始化脚本
CREATE TABLE IF NOT EXISTS user_info (
    id VARCHAR(255) NOT NULL PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(200),
    created_at BIGINT
);
```

**init-oceanbase.sql**
```sql
-- OceanBase 初始化脚本  
CREATE TABLE IF NOT EXISTS user_info (
    id VARCHAR(255) NOT NULL PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(200),
    created_at BIGINT
);
```

### 方式一：使用兼容接口（推荐用于迁移）

```java
@SpringBootTest(classes = YourTestApplication.class)
@Import(MultiDbHelper.TestDataSourceConfiguration.class)
class UserRepositoryMultiDbTest {

    @Autowired
    private UserRepository userRepository;

    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        MultiDbHelper.configureProperties(registry);
    }

    @Test
    void testUserOperationsOnAllDatabases() {
        MultiDbTestRunner.runMultiDbTest(
            "init-mysql.sql",      // MySQL 初始化脚本
            "init-oceanbase.sql",  // OceanBase 初始化脚本
            (dbInfo) -> {          // 测试逻辑
                performUserTests(dbInfo);
            }
        );
    }
    
    private void performUserTests(DatabaseInfo dbInfo) {
        System.out.println("测试数据库: " + dbInfo.getName());
        
        // 你的测试逻辑...
        // userRepository.save(user);
        // assertEquals(expected, actual);
        
        System.out.println("✓ " + dbInfo.getName() + " 测试通过");
    }
}
```

### 方式二：使用新配置接口（推荐）

```java
@Test
void testWithNewConfigApi() {
    DatabaseTestConfig config = DatabaseTestConfig.create()
        .withInitScript(DatabaseType.MYSQL, "init-mysql.sql")
        .withInitScript(DatabaseType.OCEANBASE, "init-oceanbase.sql");
    
    MultiDbTestRunner.runMultiDbTest(config, (dbInfo) -> {
        performUserTests(dbInfo);
    });
}
```

### 方式三：单独测试某个数据库

```java
@Test
void testMySQLOnly() {
    MultiDbTestRunner.runSingleDbTest(
        DatabaseType.MYSQL, 
        "init-mysql.sql", 
        (dbInfo) -> {
            performUserTests(dbInfo);
        }
    );
}
```

## 🏗️ 架构设计

### 核心组件

- **`DatabaseType`** - 数据库类型枚举，定义支持的数据库
- **`DatabaseInfo`** - 数据库连接信息封装
- **`DatabaseHandler`** - 数据库操作接口，定义统一的数据库操作规范
- **`AbstractDatabaseHandler`** - 抽象基类，提供通用的脚本执行逻辑
- **`DatabaseHandlerFactory`** - 工厂模式，根据类型创建对应的处理器
- **`DatabaseTestConfig`** - 测试配置类，支持灵活的配置管理
- **`MultiDbTestRunner`** - 核心测试执行器，协调各组件完成测试流程
- **`SwitchableDataSource`** - 动态数据源，支持运行时切换
- **`MultiDbHelper`** - Spring Boot 集成助手

### 设计模式应用

- **策略模式**: `DatabaseHandler` 接口及其实现类
- **工厂模式**: `DatabaseHandlerFactory` 创建不同的数据库处理器
- **模板方法模式**: `AbstractDatabaseHandler` 提供通用流程框架
- **建造者模式**: `DatabaseTestConfig` 支持链式配置

### 工作原理

1. **配置解析** - 解析用户配置，确定要测试的数据库类型和初始化脚本
2. **处理器创建** - 使用工厂模式创建对应的数据库处理器
3. **容器管理** - 各处理器负责启动和管理自己的数据库容器
4. **数据源切换** - 使用 `SwitchableDataSource` 动态切换数据库连接
5. **脚本执行** - 执行数据库特定的初始化脚本
6. **测试执行** - 在配置的数据库上依次运行测试逻辑
7. **资源清理** - 测试完成后自动清理容器资源

## 📋 系统要求

- **JDK**: 8 或更高版本
- **Docker**: 确保 Docker 环境正常运行（TestContainers 需要）
- **Spring Boot**: 2.x 或 3.x
- **构建工具**: Gradle 或 Maven

## 📚 详细配置

### 数据库驱动依赖

```gradle
dependencies {
    // MySQL
    testImplementation 'com.mysql:mysql-connector-j'
    
    // OceanBase
    testImplementation 'com.alipay.oceanbase:oceanbase-client'
}
```

### 初始化脚本规范

- 脚本中的注释行（以 `--` 开头）会被自动过滤
- 支持多行 SQL 语句
- 建议使用 `IF NOT EXISTS` 避免重复创建

## ⚡ 性能优化

- **容器复用**: 同一时间只运行一个数据库容器
- **连接池**: 使用 HikariCP 连接池优化数据库连接
- **快速启动**: MySQL 容器通常在 10-20 秒内启动完成
- **内存管理**: OceanBase 容器启动较慢但功能更强大

## 🔧 扩展支持

### 扩展新数据库类型

框架使用设计模式确保高度可扩展性，添加新数据库类型只需要几个步骤：

#### 1. 添加数据库类型枚举

```java
// 在 DatabaseType.java 中添加
POSTGRESQL("PostgreSQL", "org.postgresql.Driver", "postgres:13");
```

#### 2. 实现数据库处理器

```java
public class PostgreSQLHandler extends AbstractDatabaseHandler {
    private PostgreSQLContainer<?> container;
    
    @Override
    public DatabaseInfo startContainer() throws Exception {
        container = new PostgreSQLContainer<>(DatabaseType.POSTGRESQL.getDefaultDockerImage())
                .withDatabaseName("security")
                .withUsername("postgres")
                .withPassword("password");
        container.start();
        
        return new DatabaseInfo(
                DatabaseType.POSTGRESQL,
                container.getJdbcUrl(),
                container.getUsername(),
                container.getPassword()
        );
    }
    
    @Override
    public void stopContainer() {
        if (container != null && container.isRunning()) {
            container.stop();
        }
    }
    
    @Override
    public boolean isRunning() {
        return container != null && container.isRunning();
    }
}
```

#### 3. 更新工厂类

```java
// 在 DatabaseHandlerFactory.java 中添加
case POSTGRESQL:
    return new PostgreSQLHandler();
```

#### 4. 使用新数据库

```java
DatabaseTestConfig config = DatabaseTestConfig.create()
    .withInitScript(DatabaseType.POSTGRESQL, "init-postgresql.sql");

MultiDbTestRunner.runMultiDbTest(config, testLogic);
```

## 📝 更新日志

### v1.0.0
- 初始版本发布
- 支持 MySQL 和 OceanBase
- 实现动态数据源切换
- TestContainers 集成
- 设计模式重构，提升扩展性
- 新增配置化API

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本项目
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的修改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 👨‍💻 作者

**brianxiadong** - [GitHub](https://github.com/brianxiadong)

---

如果这个项目对你有帮助，请给个 ⭐️ 支持一下！ 

![CodeRabbit Pull Request Reviews](https://img.shields.io/coderabbit/prs/github/brianxiadong/multi-database-test-framework?utm_source=oss&utm_medium=github&utm_campaign=brianxiadong%2Fmulti-database-test-framework&labelColor=171717&color=FF570A&link=https%3A%2F%2Fcoderabbit.ai&label=CodeRabbit+Reviews)
