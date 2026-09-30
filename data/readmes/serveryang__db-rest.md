
# DB REST API (Rust + JNI + JDBC)

🚀 一个使用Rust编写的高性能REST API服务，通过JNI调用JDBC驱动连接MySQL、PostgreSQL、SQLite、达梦8等数据库。
将数据库表直接映射成RESTful接口来操作。同时可当成数据库客户端来使用。

## 🗃️ JDBC 驱动管理（Maven 方式）

本项目推荐使用 Maven 管理 JDBC 驱动 JAR 文件，统一下载到 `jdbc-drivers` 目录，便于配置和升级。

1. 在项目根目录的 `pom.xml` 中声明所需的 JDBC 驱动依赖。
2. 运行以下命令将所有 JAR 下载到 `jdbc-drivers` 文件夹：

   ```sh
   rm -f jdbc-drivers/*.jar;  mvn dependency:copy-dependencies -DoutputDirectory=jdbc-drivers -DexcludeTransitive=true
   ```

   查看db.driver.class
   ```sh
   jar tf jdbc-drivers/ShenTong/oscarJDBC.jar | grep Driver.class
   ```

3. 在配置文件中引用 JAR 路径（支持绝对或相对路径），如：

   ```
   db.driver.path=jdbc-drivers/mysql-connector-java-8.0.29.jar
   ```

> `jdbc-drivers` 目录仅需存放 JAR 文件，无需包含 Java 源码或编译产物。

## ✨ 特性

- **高性能**: Rust编写，内存安全，零成本抽象
- **数据库支持**: MySQL 5.x/8.x 和 PostgreSQL
- **易于扩展**: 支持任何JDBC驱动
- **配置灵活**: 多种预设配置，支持Properties文件
- **双工作模式**:
  - 🌐 **REST API模式**: 标准的RESTful HTTP服务
  - 💻 **CLI模式**: 命令行SQL执行工具
- **内存占用小**: 优化版本仅约52MB内存占用
- **线程优化**: 从99个线程减少到14个线程
- **完整调试支持**: VS Code调试配置和SQL日志记录

## 📁 项目结构

```
db-rest/
├── jdbc-drivers/                      # JDBC驱动JAR目录（由Maven统一管理）
├── configs/                           # 配置文件目录
│   ├── db-rest-mysql.properties      # mysql数据库连接配置
│   ├── db-rest-dm8.properties        # 达梦8数据库连接配置
│   └── db-rest-production.properties # 生产环境配置
├── docs/                              # 文档目录
│   ├── CONFIG_GUIDE.md                # 配置指南
│   ├── PERFORMANCE_CONFIG.md          # 性能优化说明
│   ├── VSCODE_DEBUG_GUIDE.md          # VS Code调试指南
│   └── FORMATTING.md                  # 代码格式规范
├── src/                               # 源代码
├── .vscode/                           # VS Code配置
└── README.md
```

## 📋 系统要求

- Linux系统 (已测试Ubuntu/CentOS)
- Java Runtime Environment (JRE) 8+
- JDBC驱动JAR文件

## 🛠️ 快速开始

### 1. 准备JDBC驱动

推荐使用Maven统一下载（见上文“JDBC驱动管理”），或手动下载：

```bash
# MySQL驱动 (已提供)
jdbc-drivers/mysql-connector-java-8.0.29.jar

# PostgreSQL驱动 (如需要)
wget https://jdbc.postgresql.org/download/postgresql-42.7.1.jar -O jdbc-drivers/postgresql-42.7.1.jar
```

### 2. 选择配置文件

`configs/` 目录下支持以下配置文件，可根据实际场景选择：

```
# MySQL数据库开发/测试环境
./target/debug/db-rest --conf configs/mysql.properties

# 达梦8数据库开发/测试环境 (已替换)
./target/debug/db-rest --conf configs/mysql.properties

# 生产环境高性能配置
./target/debug/db-rest --conf configs/production.properties

# 其他数据库或自定义配置可参考上述模板自行添加
```

```

### 3. 编译运行

```bash
cargo clippy --fix --allow-dirty --allow-staged

cargo build --release

# 运行
./target/debug/db-rest --conf configs/mysql.properties
```

## 🌐 API 接口

### 获取所有学生

```bash
GET /api/students
```

### 获取指定学生

```bash
GET /api/students/{id}
```

### 创建学生

```bash
POST /api/students
Content-Type: application/json

{
  "name": "张三",
  "address": "北京市海淀区",
  "age": 20,
  "email": "zhangsan@example.com",
  "phone": "13800138001"
}
```

### 更新学生信息

```bash
PUT /api/students/{id}
Content-Type: application/json

{
  "name": "李四",
  "address": "上海市浦东新区",
  "age": 22,
  "email": "lisi@example.com",
  "phone": "13800138002"
}
```

### 删除学生

```bash
DELETE /api/students/{id}
```

## 📊 工作模式

db-rest 支持两种工作模式：

### 🌐 REST API 模式 (默认)

启动HTTP服务器，提供RESTful API接口：

```bash
# 使用调试配置启动
./target/debug/db-rest --conf configs/debug.properties

# 使用生产配置启动  
./target/debug/db-rest --conf configs/production.properties
```

# 使用生产配置启动

./target/debug/db-rest --conf configs/mysql.properties

直接执行SQL语句，适用于数据库管理、批处理等场景：

```bash
# 用于检测数据库登录账号是否正确。登录成功返回sucess，失败则打印错误信息。
./target/debug/db-rest --conf configs/mysql.properties --run-as-cli --check-account
success

./target/debug/db-rest --conf configs/test-invalid-mysql.properties --run-as-cli --check-account
Exception in thread "Thread-0" java.sql.SQLException: Access denied for user 'invalid_user'@'172.24.0.1' (using password: YES)
        at com.mysql.cj.jdbc.exceptions.SQLError.createSQLException(SQLError.java:129)
        at com.mysql.cj.jdbc.exceptions.SQLExceptionsMapping.translateException(SQLExceptionsMapping.java:122)
        at com.mysql.cj.jdbc.ConnectionImpl.createNewIO(ConnectionImpl.java:828)
        at com.mysql.cj.jdbc.ConnectionImpl.<init>(ConnectionImpl.java:448)
        at com.mysql.cj.jdbc.ConnectionImpl.getInstance(ConnectionImpl.java:241)
        at com.mysql.cj.jdbc.NonRegisteringDriver.connect(NonRegisteringDriver.java:198)
Error: Failed to connect via driver: Java exception was thrown

# 从文件执行SQL, create `classicmodels`
./target/debug/db-rest --conf configs/mysql.properties --run-as-cli --sql-file data/mysql/sample.sql
./target/debug/db-rest --conf configs/mysql.properties --run-as-cli --sql-file=data/mysql/sample.sql
./target/debug/db-rest --conf configs/mysql.properties --run-as-cli --sql-file data/mysql/sample-describe.sql

# 执行单条SQL语句
./target/debug/db-rest --conf configs/mysql.properties --run-as-cli --sql "select * from classicmodels.orders;"

# 支持通过命令行形式来传递参数，从而覆盖properties配置文件中的默认值。
# 参数与properties中的一样，不需要添加--了。
./target/debug/db-rest --conf configs/mysql.properties --run-as-cli --check-account db.username=admin db.password="Root__123"

```

#### CLI 模式特性

- ✅ **智能SQL类型检测**: 自动识别SELECT/INSERT/UPDATE/DELETE等语句类型
- ✅ **格式化输出**: JSON格式美化显示查询结果
- ✅ **错误处理**: 详细的错误信息和适当的退出代码
- ✅ **注释支持**: 支持SQL文件中的`--`注释
- ✅ **日志配置**: 继承配置文件中的日志设置
- ✅ **性能统计**: 显示SQL执行时间和影响行数

## 📊 REST API 使用示例

启动服务后，可以使用curl进行测试：

```bash
# 获取所有学生
curl -X GET http://localhost:8080/api/students

# 创建学生
curl -X POST http://localhost:8080/api/students \
  -H "Content-Type: application/json" \
  -d '{"name":"测试学生","address":"深圳市南山区","age":21,"email":"test@example.com","phone":"13800138888"}'

# 获取学生
curl -X GET http://localhost:8080/api/students/1

# 更新学生
curl -X PUT http://localhost:8080/api/students/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"更新学生","address":"杭州市西湖区","age":23,"email":"updated@example.com","phone":"13800139999"}'

# 删除学生
curl -X DELETE http://localhost:8080/api/students/1
```

## 🔧 配置参数说明

| 参数                | 说明                | 示例                             |
| ------------------- | ------------------- | -------------------------------- |
| `db.driver.type`    | 数据库类型          | mysql, postgresql                |
| `db.driver.path`    | JDBC驱动JAR路径     | /opt/jdbc-drivers/mysql/...      |
| `db.driver.class`   | JDBC驱动类名 (可选) | com.mysql.jdbc.Driver            |
| `db.url`            | 数据库连接URL       | jdbc:mysql://localhost:3306/test |
| `db.username`       | 数据库用户名        | root                             |
| `db.password`       | 数据库密码          | password                         |
| `db.maxConnections` | 最大连接数          | 10                               |
| `server.host`       | 服务器监听地址      | 0.0.0.0                          |
| `server.port`       | 服务器监听端口      | 8080                             |

## 🚀 性能特点

- **启动时间**: < 1秒
- **内存占用**: ~8MB
- **响应时间**: < 10ms (本地数据库)
- **并发支持**: 支持数千并发连接

## � 文档

- [📖 配置指南](docs/CONFIG_GUIDE.md) - 详细的配置参数说明
- [⚡ 性能优化配置](docs/PERFORMANCE_CONFIG.md) - 性能优化详解
- [🐛 VS Code调试指南](docs/VSCODE_DEBUG_GUIDE.md) - 开发环境配置
- [📐 代码格式规范](docs/FORMATTING.md) - 代码格式要求

## �🔮 扩展支持

支持任何JDBC兼容的数据库，只需：

1. 下载对应的JDBC驱动JAR文件
2. 修改配置文件中的驱动路径和连接参数
3. 重启服务

已测试的数据库：

- ✅ MySQL 5.7/8.0
- ✅ PostgreSQL 12+
- 🔄 Oracle (理论支持)
- 🔄 SQL Server (理论支持)

## 📊 性能数据

| 配置类型   | 线程数 | 内存占用 | 适用场景      |
| ---------- | ------ | -------- | ------------- |
| 优化配置   | 14个   | ~52MB    | 开发/小型部署 |
| 多线程配置 | 19个   | ~64MB    | 测试/中等负载 |
| 生产配置   | 23+个  | ~128MB+  | 生产/高并发   |
| 原始版本   | 99个   | ~72MB    | -             |

## 📝 注意事项

1. 确保Java环境已正确安装
2. JDBC驱动JAR文件路径必须可访问
3. 数据库连接参数必须正确
4. 使用现有的demo数据库中的students表
5. students表结构包含：id, name, address, age, email, phone, create_at, update_at

## 🐛 故障排除

### 常见问题

1. **JVM初始化失败**: 检查Java环境和JDBC驱动路径
2. **数据库连接失败**: 检查数据库服务状态和连接参数
3. **权限问题**: 确保应用有访问JDBC驱动文件的权限

### 日志查看

服务启动时会输出详细日志：

```
JVM initialized with classpath: /opt/jdbc-drivers/mysql/...
✅ JDBC Driver loaded: com.mysql.jdbc.Driver
✅ Database connection test successful: jdbc:mysql://...
✅ Database schema initialized
🚀 DB REST API (Rust + JNI + JDBC) 启动成功!
```

## 📄 许可证

MIT License
