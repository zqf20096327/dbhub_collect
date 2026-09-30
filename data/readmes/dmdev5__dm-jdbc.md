# 达梦 JDBC

> 🌐 语言：[English](./README.en.md) | **简体中文**

达梦数据库 JDBC 驱动。本 JDBC 驱动通过标准 JDBC API 为 Java 应用程序提供数据库连接，支持 JDBC 规范，可自动注册到 DriverManager。

## 获取驱动
 您可以从 [Dameng 下载中心](https://www.dameng.com/download/index.html) 下载预编译的驱动（jar），或使用您惯用的依赖管理工具来引入：
### Maven 中央仓库
您可以在中央仓库（The Central Repository）中通过 GroupId 和 ArtifactId com.dameng:dm-jdbc 进行搜索.

```
<!-- 在 pom.xml 里加入下面这段依赖配置, -->
<!-- 将 LATEST 替换为您需要的具体版本号 -->

<dependency>
  <groupId>com.dameng</groupId>
  <artifactId>dm-jdbc</artifactId>
  <version>LATEST</version>
</dependency>
```
## 文档
欲了解更多信息，您可以阅读 [DM JDBC 编程指南](https://eco.dameng.com/document/dm/zh-cn/pm/jdbc-rogramming-guide.html)；如需通用的 JDBC 文档，请参阅 [The Java™ Tutorials](https://docs.oracle.com/javase/tutorial/jdbc/).

### 驱动类与数据源类

| 实现的接口 | 实现类 |
| -- | -- |
| java.sql.Driver |	dm.jdbc.driver.DmDriver |
| javax.sql.DataSource | dm.jdbc.driver.DmdbDataSource |
| javax.sql.ConnectionPoolDataSource |	dm.jdbc.driver.DmdbConnectionPoolDataSource |
| javax.sql.XADataSource |	dm.jdbc.driver..DmdbXADataSource |

### 构造连接串 URL
驱动支持以下形式的 JDBC URL:
```
jdbc:dm://
jdbc:dm://host
jdbc:dm://host:port
```
连接达梦数据库服务器的 JDBC URL 通用格式如下，其中方括号（[ ]）内的部分为可选项:
```
jdbc:dm://[host][:port][/schemaName][?propName1=propValue1] [&propName2=propValue2][&…]…
```
where:

- **jdbc:dm://** （必填）即子协议（sub‑protocol），为固定常量。
- **host** （可选）为要连接的服务器地址。可以是 DNS 名称或 IP 地址，本机连接可用 localhost 或 127.0.0.1。若要指定 IPv6 地址，host 参数须用方括号包起来（jdbc:dm://[::1]:5236）。默认为 localhost。
- **port** （可选）为 host 上监听的端口号。默认为 5236。

### 连接属性
见 [DM JDBC 编程指南](https://eco.dameng.com/document/dm/zh-cn/pm/jdbc-rogramming-guide.html#4.5.4%20DM%20%E6%89%A9%E5%B1%95%E8%BF%9E%E6%8E%A5%E5%B1%9E%E6%80%A7%E7%9A%84%E4%BD%BF%E7%94%A8)

## 社区
通过以下方式加入达梦社区：

- [论坛](https://eco.dameng.com/community/question/) 最适合：提问、反馈建议、获取最新动态，以及与其他 Dameng 用户交流。