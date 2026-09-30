# YashanDB Oracle 兼容修复插件

## 项目简介
实现 Oracle 到 YashanDB 兼容性问题的自动修复工具，帮助用户快速迁移 Oracle SQL 到 YashanDB。

## 核心功能

1. **语法兼容修复**：自动识别并转换 Oracle 特有语法到 YashanDB 兼容语法，包括函数、类型、语法结构等。
2. **复杂 SQL 支持**：支持存储过程、函数、触发器等复杂 SQL 结构的转换。
3. **模块化规则系统**：采用可扩展的规则系统，支持自定义转换规则。
4. **批量处理**：支持批量上传和处理多个 SQL 文件。
5. **错误自动诊断**：提供详细的错误信息和修复建议。

## 使用说明

### 编译和运行

1. **编译项目**：
   ```bash
   mvn clean package -DskipTests
   ```

2. **运行应用**：
   ```bash
   java -jar target/sql-fix-plugin-1.0.0.jar
   ```

3. **访问界面**：
   打开浏览器，访问 `http://localhost:8080`

### 依赖配置

- **Maven 依赖**：项目使用 Maven 管理依赖，主要依赖包括：
  - Spring Boot 3.2.4
  - ANTLR 4.13.1（用于 SQL 解析）
  - YashanDB JDBC 驱动 1.9.3

- **JDBC 驱动**：
  项目已包含 YashanDB JDBC 驱动，位于 `lib/yashandb-jdbc-1.9.3.jar`

## 技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| **ANTLR 4** | 4.13.1 | SQL 语法解析 — 基于 `OracleSql.g4` 语法文件自动生成词法分析器（Lexer）、语法分析器（Parser）和 AST 访问器（Visitor），支持完整的 Oracle SQL 语法树解析与遍历 |
| **Spring Boot** | 3.2.4 | Web 应用框架 — 提供 REST API、依赖注入、配置管理，驱动前端交互与后端服务 |
| **规则引擎**（自建） | — | 可插拔规则链系统 — 基于 `Rule` 接口定义统一的 `canApply` / `apply` 契约，通过 `SqlFixEngine` 按序编排 `TypeRule`、`FunctionRule`、`SyntaxRule` 等多条规则，支持动态注册自定义规则 |

> 规则引擎采用**责任链模式**：每条规则独立判断是否适用并执行转换，引擎按注册顺序依次调用，转换结果作为下一条规则的输入，形成可扩展的 SQL 修复流水线。

## 环境要求

- **JDK 版本**：JDK 17 或更高版本
- **YashanDB 版本**：YashanDB 2.0 或更高版本（用于验证 SQL 语法）
- **Maven 版本**：Maven 3.6 或更高版本（用于编译项目）
- **操作系统**：支持 Windows、Linux、macOS 等主流操作系统

## 功能使用

### 单个 SQL 转换
1. 在首页的 "SQL 语句转换" 输入框中输入 Oracle SQL 语句
2. 点击 "转换" 按钮
3. 查看转换结果和错误信息

### 批量文件处理
1. 在首页的 "批量文件处理" 区域点击 "选择文件"
2. 选择一个或多个 SQL 文件
3. 点击 "上传并转换" 按钮
4. 查看每个文件的转换结果

### 数据库连接测试
1. 在首页的 "数据库连接测试" 区域点击 "测试连接" 按钮
2. 查看连接状态和错误信息

## 项目结构

```
YashanDB/
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/yashan/sqlfix/       # 核心代码
│   │   ├── resources/
│   │   │   ├── antlr4/                  # ANTLR 语法文件
│   │   │   └── static/                  # 前端静态文件
│   └── test/
├── lib/                                 # 依赖库
│   └── yashandb-jdbc-1.9.3.jar          # YashanDB JDBC 驱动
├── target/                              # 编译输出目录
└── pom.xml                              # Maven 配置文件
```

## 核心模块

1. **SQL 解析器**：使用 ANTLR 4 解析 Oracle SQL 语句
2. **转换引擎**：基于规则系统和 AST 访问器实现 SQL 转换
3. **规则系统**：模块化的转换规则，支持类型、函数、语法等转换
4. **批处理服务**：处理多个 SQL 文件的批量转换
5. **验证服务**：验证转换后的 SQL 是否符合 YashanDB 语法

## 扩展开发

### 添加自定义转换规则

1. 实现 `com.yashan.sqlfix.core.rule.Rule` 接口
2. 在 `SqlFixEngine` 构造函数中添加自定义规则

```java
public SqlFixEngine() {
    // 初始化规则列表
    rules = new ArrayList<>();
    rules.add(new TypeRule());
    rules.add(new FunctionRule());
    rules.add(new SyntaxRule());
    // 添加自定义规则
    rules.add(new CustomRule());
}
```

### 扩展语法支持

修改 `src/main/resources/antlr4/OracleSql.g4` 文件，添加新的语法规则。

## 注意事项

1. 本插件主要针对 Oracle 到 YashanDB 的语法转换，不保证 100% 兼容所有 Oracle 特性
2. 对于复杂的存储过程和触发器，可能需要手动调整转换结果
3. 建议在生产环境使用前，对转换结果进行充分测试

## 版本历史

- v1.0.0：初始版本，支持基本 SQL 语句、存储过程、函数、触发器的转换

## 联系方式

如有问题或建议，请联系项目维护人员。