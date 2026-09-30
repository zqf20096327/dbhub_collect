# SQL Converter 工具

## 简介

SQL Converter 是一款用于跨数据库SQL语句转换的Java工具，支持多种主流数据库类型（MySQL、Oracle、Dameng等），可将源数据库的SQL语句转换为目标数据库兼容的语法格式。适用于数据迁移、跨数据库开发等场景。

## 功能特性

- **多数据库支持** 支持 MySQL、Oracle、Dameng 等数据库类型互转
- **SQL类型识别** 自动区分 DML（INSERT/UPDATE/DELETE）和 DDL（CREATE/ALTER/DROP/TRUNCATE/COMMENT）
- **异构DDL转换** 提取表结构元数据，生成目标数据库兼容的DDL
- **配置灵活** 支持大小写敏感、目标库命名规则等高级配置
- **统一接口** 提供简洁的API接口，快速集成到Java项目

## 使用说明

### 1. 核心转换接口

```java
public static List<String> convertSql(
    String sql, 
    DataBaseType sourceDBType, 
    DataBaseType targetDBType,
    String targetSchema, 
    String targetTable, 
    HashMap<String,String> config
) throws Exception
```

**参数说明**

| 参数         | 类型                   | 必选 | 说明                                          |
| ------------ | ---------------------- | ---- | --------------------------------------------- |
| sql          | String                 | 是   | 原始SQL语句                                   |
| sourceDBType | DataBaseType           | 是   | 源数据库类型（枚举值：MYSQL/ORACLE/DAMENG等） |
| targetDBType | DataBaseType           | 是   | 目标数据库类型                                |
| targetSchema | String                 | 是   | 目标模式名（如Oracle的Schema）                |
| targetTable  | String                 | 是   | 目标表名                                      |
| config       | HashMap<String,String> | 否   | 高级配置参数（见下方配置说明）                |

**返回值** 返回转换后的SQL语句列表（可能包含多条语句）

### 2. 通过模板生成CREATE语句

```java
public static List<String> convertCreateByTable(
    Template template, 
    String sourceDBType, 
    String targetDBType, 
    String targetSchema, 
    String targetTable, 
    HashMap<String,String> config
) throws Exception
```

适用于从预定义的表结构模板生成DDL

### 3. SQL类型识别接口

```java


public static SQLType getTypeBySQL(String sql, String sourceDBType) throws Exception
```

**返回值** 返回SQLType枚举：DML/CREATE/ALTER/DROP/TRUNCATE/COMMENT

## 配置参数

通过`config` HashMap传递高级参数：

| 参数键            | 示例值  | 说明                                                         |
| ----------------- | ------- | ------------------------------------------------------------ |
| caseSensitive     | "true"  | 是否启用大小写敏感（默认false）                              |
| targetDefaultCase | "upper" | caseSensitive为false时设置目标库标识符默认大小写规则（upper/lower） |

示例配置：

```
JavaHashMap<String, String> config = new HashMap<>();
config.put("caseSensitive", "true");
config.put("targetDefaultCase", "upper");
```

## 使用示例

### 示例1：转换CREATE语句

```java
String sql = "CREATE TABLE `test`.`employees` (\n" +
        "    `id` INT PRIMARY KEY AUTO_INCREMENT COMMENT '员工唯一ID',\n" +
        "    `Name` VARCHAR(50) NOT NULL COMMENT '员工姓名',\n" +
        "    `department` VARCHAR(50) DEFAULT '未分配' COMMENT '所属部门',\n" +
        "    `saLary` DECIMAL(10,2) NOT NULL DEFAULT 0 COMMENT '工资',\n" +
        "    `hire_Date` DATE DEFAULT (CURRENT_DATE) COMMENT '入职日期',\n" +
        "    `eMail` VARCHAR(100) COMMENT '邮箱（允许空）'\n" +
        ") COMMENT '员工信息表';";
HashMap<String, String> config = new HashMap<>();
config.put("caseSensitive", "false");

List<String> converted = SQLConverter.convertSql(
    sql, 
    DataBaseType.MYSQL, 
    DataBaseType.ORACLE, 
    "DXP", 
    "LGY_TEST_SOURCE", 
    config
);

// 输出结果示例：
CREATE TABLE "DXP"."LGY_TEST_SOURCE" (
  "ID" INT NOT NULL,
"NAME" VARCHAR2(50)  NOT NULL,
"DEPARTMENT" VARCHAR2(50)  DEFAULT '未分配',
"SALARY" NUMBER(10,2) DEFAULT 0 NOT NULL,
"HIRE_DATE" DATE DEFAULT CURRENT_DATE,
"EMAIL" VARCHAR2(100) , 
PRIMARY KEY ("ID")
 );

COMMENT ON TABLE "DXP"."LGY_TEST_SOURCE" IS '员工信息表';
COMMENT ON COLUMN "DXP"."LGY_TEST_SOURCE"."ID" IS '员工唯一ID';
COMMENT ON COLUMN "DXP"."LGY_TEST_SOURCE"."NAME" IS '员工姓名';
COMMENT ON COLUMN "DXP"."LGY_TEST_SOURCE"."DEPARTMENT" IS '所属部门';
COMMENT ON COLUMN "DXP"."LGY_TEST_SOURCE"."SALARY" IS '工资';
COMMENT ON COLUMN "DXP"."LGY_TEST_SOURCE"."HIRE_DATE" IS '入职日期';
COMMENT ON COLUMN "DXP"."LGY_TEST_SOURCE"."EMAIL" IS '邮箱（允许空）';
```

### 示例2：识别SQL类型

```java
SQLType type = SQLConverter.getTypeBySQL(
    "TRUNCATE TABLE orders", 
    "MYSQL"
);
// 返回 SQLType.TRUNCATE
```

## 注意事项

1. **DDL转换限制** 部分数据库特有的DDL语法（如存储过程）可能无法完全转换
2. **异常处理** 遇到无法解析的语法会抛出Exception，建议使用try-catch块捕获



# SQL Converter Tool

## Introduction

SQL Converter is a Java-based tool for cross-database SQL statement conversion. It supports multiple mainstream database types (MySQL, Oracle, Dameng, etc.), enabling the transformation of SQL statements from a source database into syntax compatible with target databases. Ideal for data migration and cross-database development scenarios.

## Features

- **Multi-Database Support**: Bidirectional conversion between MySQL, Oracle, Dameng, and other databases
- **SQL Type Recognition**: Automatically distinguishes DML (INSERT/UPDATE/DELETE) and DDL (CREATE/ALTER/DROP/TRUNCATE/COMMENT)
- **Heterogeneous DDL Conversion**: Extracts table structure metadata and generates target-database-compatible DDL
- **Flexible Configuration**: Supports advanced settings like case sensitivity and target database naming conventions
- **Unified API**: Provides clean Java API interfaces for seamless integration into projects

## Usage Guide

### 1. Core Conversion Interface

```java
public static List<String> convertSql(
    String sql, 
    DataBaseType sourceDBType, 
    DataBaseType targetDBType,
    String targetSchema, 
    String targetTable, 
    HashMap<String,String> config
) throws Exception
```

**Parameters**

| Parameter    | Type                   | Required | Description                                           |
| ------------ | ---------------------- | -------- | ----------------------------------------------------- |
| sql          | String                 | Yes      | Original SQL statement                                |
| sourceDBType | DataBaseType           | Yes      | Source database type (enum: MYSQL/ORACLE/DAMENG/etc.) |
| targetDBType | DataBaseType           | Yes      | Target database type                                  |
| targetSchema | String                 | Yes      | Target schema name (e.g., Oracle's Schema)            |
| targetTable  | String                 | Yes      | Target table name                                     |
| config       | HashMap<String,String> | No       | Advanced configuration parameters (see below)         |

**Return Value** List of converted SQL statements (may contain multiple statements)

### 2. Generate CREATE Statements from Template

```java
public static List<String> convertCreateByTable(
    Template template, 
    String sourceDBType, 
    String targetDBType, 
    String targetSchema, 
    String targetTable, 
    HashMap<String,String> config
) throws Exception
```

Designed for generating DDL from predefined table structure templates.

### 3. SQL Type Recognition Interface

```java
public static SQLType getTypeBySQL(String sql, String sourceDBType) throws Exception
```

**Return Value** SQLType enum: DML/CREATE/ALTER/DROP/TRUNCATE/COMMENT

## Configuration Parameters

Configure via `config` HashMap:

| Key               | Example | Description                                                  |
| ----------------- | ------- | ------------------------------------------------------------ |
| caseSensitive     | "true"  | Enable case sensitivity (default: false)                     |
| targetDefaultCase | "upper" | Default case rule when caseSensitive=false (options: "upper"/"lower") |

Example configuration:

```
JavaHashMap<String, String> config = new HashMap<>();
config.put("caseSensitive", "true");
config.put("targetDefaultCase", "upper");
```

## Examples

### Example 1: Convert CREATE Statement

```java
String sql = "CREATE TABLE `test`.`employees` (\n" +
        "    `id` INT PRIMARY KEY AUTO_INCREMENT COMMENT 'Employee ID',\n" +
        "    `Name` VARCHAR(50) NOT NULL COMMENT 'Employee name',\n" +
        "    `department` VARCHAR(50) DEFAULT 'Unassigned' COMMENT 'Department',\n" +
        "    `saLary` DECIMAL(10,2) NOT NULL DEFAULT 0 COMMENT 'Salary',\n" +
        "    `hire_Date` DATE DEFAULT (CURRENT_DATE) COMMENT 'Hire date',\n" +
        "    `eMail` VARCHAR(100) COMMENT 'Email (nullable)'\n" +
        ") COMMENT 'Employee information table';";
HashMap<String, String> config = new HashMap<>();
config.put("caseSensitive", "false");

List<String> converted = SQLConverter.convertSql(
    sql, 
    DataBaseType.MYSQL, 
    DataBaseType.ORACLE, 
    "DXP", 
    "LGY_TEST_SOURCE", 
    config
);

/* Output:
CREATE TABLE "DXP"."LGY_TEST_SOURCE" (
  "ID" INT NOT NULL,
  "NAME" VARCHAR2(50) NOT NULL,
  "DEPARTMENT" VARCHAR2(50) DEFAULT 'Unassigned',
  "SALARY" NUMBER(10,2) DEFAULT 0 NOT NULL,
  "HIRE_DATE" DATE DEFAULT CURRENT_DATE,
  "EMAIL" VARCHAR2(100), 
  PRIMARY KEY ("ID")
);

COMMENT ON TABLE "DXP"."LGY_TEST_SOURCE" IS 'Employee information table';
COMMENT ON COLUMN "DXP"."LGY_TEST_SOURCE"."ID" IS 'Employee ID';
COMMENT ON COLUMN "DXP"."LGY_TEST_SOURCE"."NAME" IS 'Employee name';
COMMENT ON COLUMN "DXP"."LGY_TEST_SOURCE"."DEPARTMENT" IS 'Department';
COMMENT ON COLUMN "DXP"."LGY_TEST_SOURCE"."SALARY" IS 'Salary';
COMMENT ON COLUMN "DXP"."LGY_TEST_SOURCE"."HIRE_DATE" IS 'Hire date';
COMMENT ON COLUMN "DXP"."LGY_TEST_SOURCE"."EMAIL" IS 'Email (nullable)';
*/
```

### Example 2: Identify SQL Type

```java
SQLType type = SQLConverter.getTypeBySQL(
    "TRUNCATE TABLE orders", 
    "MYSQL"
);
// Returns SQLType.TRUNCATE
```

## Notes

1. **DDL Conversion Limits**: Some database-specific DDL syntax (e.g., stored procedures) may not be fully convertible
2. **Error Handling**: Unparsable syntax will throw an Exception – recommend using try-catch blocks