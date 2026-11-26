# Flyway GaussDB 商业版适配器

本项目为 Flyway 8.5.13 提供华为 GaussDB 商业版适配，支持 JDK 8。Flyway 通过 Java SPI 自动加载适配器，使用 `jdbc:gaussdb:` 识别连接，复用 PostgreSQL 迁移方言，并按 GaussDB 规则处理 JDBC 兼容版本和会话角色恢复。

## 模块

| Maven 坐标 | 用途 |
| --- | --- |
| `org.rdlinux:flyway-gaussdb:0.1.1` | Flyway 核心适配器，支持直接使用 Flyway Java API。 |
| `org.rdlinux:flyway-gaussdb-spring-boot-starter:0.1.1` | Spring Boot 2.7 自动配置，传递引入核心适配器，并补齐 GaussDB 的迁移目录占位符。 |

## 构建和接入

在仓库根目录使用 JDK 8 和 Maven 3.9.2 或以上版本构建两个模块。

```bash
mvn clean install
```

应用需在运行时提供与目标数据库匹配的华为 JDBC 驱动 `com.huawei.gaussdb.jdbc.Driver`，并提供自己的迁移 SQL。

### Spring Boot 2.7

在已配置 JDBC 数据源和 Flyway 的 Spring Boot 应用中引入自动配置模块。

```xml
<dependency>
    <groupId>org.rdlinux</groupId>
    <artifactId>flyway-gaussdb-spring-boot-starter</artifactId>
    <version>0.1.1</version>
</dependency>
```

当 Flyway 的实际迁移数据源使用 `jdbc:gaussdb:` 时，自动配置将 `{vendor}` 解析为 `gaussdb`。显式目录也可以直接使用。

```yaml
spring:
  datasource:
    driver-class-name: com.huawei.gaussdb.jdbc.Driver
    url: ${GAUSSDB_JDBC_URL}
    username: ${GAUSSDB_USERNAME}
    password: ${GAUSSDB_PASSWORD}
  flyway:
    locations: "classpath:db/migration/{vendor}"
```

### Flyway Java API

直接使用 Flyway 时引入核心适配器。

```xml
<dependency>
    <groupId>org.rdlinux</groupId>
    <artifactId>flyway-gaussdb</artifactId>
    <version>0.1.1</version>
</dependency>
```

通过 `Flyway.configure().dataSource(jdbcUrl, username, password).locations("classpath:db/migration/gaussdb").load().migrate()` 运行迁移。

核心适配器依赖 Flyway 8.5.13 的内部数据库接口，升级 Flyway 时需重新验证。核心插件的真库验证覆盖华为 GaussDB 的 A 兼容模式。Spring Boot 自动配置的兼容基线是 2.7.18。