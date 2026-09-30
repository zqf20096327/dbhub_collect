# 数据库文档生成工具

基于 Java Swing 的数据库表结构文档生成工具，支持 MySQL、SQL Server、PostgreSQL 及达梦、人大金仓、openGauss 等国产数据库。可导出 Word/HTML/PDF 三种格式，支持表与字段级勾选筛选。JDBC 提取元数据，Apache POI 生成 Word，Freemarker 渲染 HTML，OpenHTMLtoPDF 转 PDF。jpackage 打包为免安装便携 EXE，自带 JRE，国产数据库驱动放入 drivers 目录自动加载。

## 技术栈

Java 17 / Swing / JDBC / Apache POI / Freemarker / OpenHTMLtoPDF / Maven

## 快速开始

```bash
mvn clean package -DskipTests
java -jar target/db-doc-generator.jar
```

打包便携 EXE：

```bash
jlink --module-path $JAVA_HOME/jmods \
  --add-modules java.base,java.desktop,java.sql,java.naming,java.net.http \
  --output target/jre --strip-debug --compress=2

jpackage --type app-image --name DatabaseDocGenerator \
  --input target --main-jar db-doc-generator.jar \
  --main-class com.dbdoc.Launcher --runtime-image target/jre --dest target/dist
```

## 目录结构

```
db-doc-generator/
├── src/main/java/com/dbdoc/
│   ├── controller/    # Swing 主界面
│   ├── datasource/    # JDBC 驱动加载
│   ├── generator/     # Word/HTML/PDF 生成器
│   ├── model/         # 数据模型
│   └── service/       # 元数据提取与导出服务
├── src/main/resources/templates/  # Freemarker 模板
└── pom.xml
```

## 功能特性

- 多数据库：MySQL、SQL Server、PostgreSQL、达梦、人大金仓、openGauss
- 多格式：Word（.docx）、HTML、PDF
- 可勾选：表级、字段级筛选导出
- 可扩展：索引、外键、表注释、概览页
- 便携化：免安装 EXE，自带 JRE
