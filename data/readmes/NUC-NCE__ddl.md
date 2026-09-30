# DDL Checker

[English](./README_en.md) | 中文

DDL 校验工具用于比对 Oracle 与 GaussDB 数据库的表结构定义是否一致。

## 功能特性

- 表空间比对
- 表结构（列定义）比对
- 主键比对
- 索引比对
- 支持 CLI 命令行调用
- 支持 SDK 编程调用

## 快速开始

### CLI 方式

```bash
# 编译打包
mvn package

# 运行校验
java -jar target/ddl-checker-1.0.0.jar -c config.json -t tables.txt -o result.txt
```

### SDK 方式

```xml
<!-- 父项目 pom.xml -->
<dependency>
    <groupId>com.datacheck</groupId>
    <artifactId>ddl-checker</artifactId>
    <version>1.0.0</version>
    <exclusions>
        <exclusion>
            <groupId>org.postgresql</groupId>
            <artifactId>postgresql</artifactId>
        </exclusion>
    </exclusions>
</dependency>

<!-- 添加自定义 Gauss 驱动 -->
<dependency>
    <groupId>com.huawei.gauss</groupId>
    <artifactId>gaussjdbc</artifactId>
    <version>3.0.0</version>
</dependency>
```

```java
import com.datacheck.sdk.*;
import com.datacheck.sdk.config.*;
import com.datacheck.model.*;

List<String> tables = Arrays.asList("EMPLOYEE", "DEPARTMENT");

DdlCompareResult result = DdlComparatorBuilder.builder()
    .oracle()
        .jdbcUrl("jdbc:oracle:thin:@localhost:1521:orcl")
        .username("scott")
        .password("tiger")
    .gauss()
        .jdbcUrl("jdbc:postgresql://localhost:5432/dbname")
        .username("gauss")
        .password("gauss")
    .options()
        .compareTablespace(true)
        .compareIndex(true)
        .comparePrimaryKey(true)
        .compareColumn(true)
        .threadCount(4)
    .buildAndCompare(tables);

// 获取汇总
System.out.println(result.getSummary());

// 获取差异详情
for (DdlDifference diff : result.getAllDifferences()) {
    System.out.println(diff.getMessage());
}
```

## 配置文件

`config.json`:

```json
{
  "oracle": {
    "jdbcUrl": "jdbc:oracle:thin:@localhost:1521:orcl",
    "username": "scott",
    "password": "tiger"
  },
  "gauss": {
    "jdbcUrl": "jdbc:postgresql://localhost:5432/dbname",
    "username": "gauss",
    "password": "gauss"
  },
  "options": {
    "compareTablespace": true,
    "compareIndex": true,
    "comparePrimaryKey": true,
    "compareColumn": true
  },
  "threadCount": 4,
  "outputDir": "./output"
}
```

## 表名列表

`tables.txt`:

```
EMPLOYEE
DEPARTMENT
SALARY
```

每行一个表名，`#` 开头的行为注释。

## CLI 参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| -c, --config | 配置文件路径 | config.json |
| -t, --tables | 表名列表文件 | tables.txt |
| -o, --output | 输出文件路径 | 控制台输出 |
| -h, --help | 显示帮助 | - |
| -v, --version | 显示版本 | - |

## 输出示例

```
========================================
DDL Compare Report
========================================
Generated: 2026-03-15 12:00:00

Summary:
----------------------------------------
Total Tables: 3
Matched: 1
Tables with Differences: 2
Total Differences: 5

Detailed Differences:
----------------------------------------

Table: EMPLOYEE
  [DIFFERENT] Table: EMPLOYEE, COLUMN_TYPE: SALARY | Oracle=NUMBER(10,2) vs Gauss=NUMERIC
  [DIFFERENT] Table: EMPLOYEE, COLUMN_NULLABLE: HIRE_DATE | Oracle=NULL vs Gauss=NOT NULL

Table: DEPARTMENT
  [ORACLE_ONLY] Table: DEPARTMENT, INDEX: IDX_DEPT_NAME
```

## 返回码

- 0: 校验完成，无差异
- 1: 校验完成，存在差异
- 2: 数据库连接错误
- 3: IO 错误
- 4: 其他错误

## 驱动说明

项目中的 JDBC 驱动已标记为 `optional`，打包时默认排除。父项目可引入自定义版本：

- Oracle: `com.oracle.database.jdbc:ojdbc8`
- GaussDB: `com.huawei.gauss:gaussjdbc` 或使用 PostgreSQL 兼容驱动
