# EasyDameng

[English](README_EN.md) | 简体中文

EasyDameng 是一个基于 JavaFX 的达梦数据库桌面客户端，提供连接管理、数据库对象维护、SQL 查询、数据导入导出、数据传输和数据库转储等功能。

后续更新  
https://github.com/oyzh1994/easyshell  

## 功能特性

- 管理多个达梦数据库连接，并维护连接配置。
- 浏览和管理架构、表、视图、索引、外键、触发器、函数及存储过程。
- 查看表结构、对象定义和数据库信息，支持常用 DDL 操作。
- 提供 SQL 查询与结果集编辑能力，并集成查询和代码生成工具。
- 支持 CSV、TXT、JSON、XML、Excel、SQL 等格式的数据导入、导出和转储。
- 支持在两个达梦数据库之间传输表结构、数据、视图、函数、存储过程和触发器。
- 提供 JavaFX 工作区、标签页、事件总线、国际化、主题和终端能力。

## 项目结构

| 目录 | 说明 |
|---|---|
| `cn.oyzh.easydameng.dameng` | 达梦客户端、SQL 生成、元数据、查询和数据库对象模型 |
| `cn.oyzh.easydameng.data` | 数据导入、导出、转储和数据传输 |
| `cn.oyzh.easydameng.controller` | 窗口和业务控制器 |
| `cn.oyzh.easydameng.fx` | JavaFX 控件和界面适配组件 |
| `cn.oyzh.easydameng.tabs` | 主工作区、查询、对象设计和终端标签页 |
| `cn.oyzh.easydameng.store` | 本地设置与数据存取 |
| `cn.oyzh.easydameng.terminal` | 终端集成 |

## 环境要求

- JDK 25
- Maven 3.9 或更高版本
- 达梦 JDBC 驱动 `DmJdbcDriver18.jar`

## 构建

达梦 JDBC 驱动通常需要先安装到本地 Maven 仓库：

```bash
mvn install:install-file \
  -Dfile=DmJdbcDriver18.jar \
  -DgroupId=com.dameng \
  -DartifactId=DmJdbcDriver18 \
  -Dversion=8.1.3.140 \
  -Dpackaging=jar
```

安装依赖工程并构建 EasyDameng：

```bash
mvn clean install -DskipTests
```

开发调试可从 IDE 运行以下任一入口类：

- `cn.oyzh.easydameng.EasyDamengApp`
- `cn.oyzh.easydameng.EasyDamengBootstrap`

运行测试：

```bash
mvn test
```

## 依赖工程

- [`base`](https://gitee.com/oyzh1994/base)：通用工具、事件、国际化、存储、SSH、打包等基础模块。
- [`fx-base`](https://gitee.com/oyzh1994/fx-base)：JavaFX UI、数据库、终端、富文本等扩展模块。

## 注意事项

- 请确认终端中的 `java -version` 为 JDK 25，否则 Maven 可能报告 `invalid target release: 25`。
- 数据导入、转储和传输操作可能修改或覆盖目标数据库，请在执行前确认目标环境并做好备份。
- 本地连接配置和应用设置由项目存储模块管理，请妥善保护包含凭据的数据。

## 许可证

项目包含 `APACHE-LICENSE-2.0.txt` 和 `MIT-LICENSE.txt`，使用前请查看相应许可条款。
