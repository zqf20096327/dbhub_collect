# Canal-Dameng 同步工具

基于 Canal 1.1.8 实现的 MySQL 到达梦数据库的同步工具，支持全量同步和增量同步，具备断点续传功能。

## 功能特性

- ✅ **全量同步**：支持 MySQL 表结构和数据的全量迁移到达梦数据库
- ✅ **增量同步**：基于 Canal 实时同步 MySQL binlog 变更到达梦数据库
- ✅ **断点续传**：服务重启后自动恢复同步位置，不丢失数据
- ✅ **并行同步**：支持多表并行同步，可配置并行数量
- ✅ **单表顺序**：单表内的数据变更按顺序处理，保证数据一致性
- ✅ **单库点对点**：单库到单库的同步模式

## 系统要求

- JDK 1.8+
- Maven 3.6+
- MySQL 5.1.x / 5.5.x / 5.6.x / 5.7.x / 8.0.x
- 达梦数据库 8.x
- Canal Server 1.1.8

## 快速开始

### 1. 配置 Canal Server

确保 Canal Server 已启动并配置好 MySQL 数据源。

**使用 Docker 快速部署（推荐）：**

```bash
# 1. 配置 MySQL binlog（参考 docs/mysql-binlog-setup.md）
# 2. 编辑 canal-server/conf/example/instance.properties 配置 MySQL 连接信息
# 3. 运行部署脚本（脚本位于 scripts 目录）
cd scripts
./deploy-canal.sh        # Linux/Mac
# 或
deploy-canal.bat          # Windows (使用 Docker Compose)

# Windows 快速启动（直接使用 Docker 命令）
run-canal-windows.ps1     # PowerShell
run-canal-windows.cmd     # CMD

# 或使用 Docker Compose
docker-compose up -d
```

详细部署文档请参考：[Canal Server 部署文档](docs/canal-deployment.md)

### 2. 配置应用

> **配置优先级**：环境变量 > `application.properties` > 默认值。  
> 即使挂载了外部配置目录中的 `application.properties`，也会被同名环境变量覆盖。  
> 环境变量同时支持两种命名：`sync.tables`（原始 key）或 `SYNC_TABLES`（推荐）。
> 外部配置目录不再写死，可用 `SYNC_CONFIG_DIR` 或 JVM 参数 `-Dsync.config.dir=...` 指定。

编辑 `src/main/resources/application.properties`：

```properties
# Canal 配置
canal.host=127.0.0.1
canal.port=11111
canal.destination=example
canal.username=
canal.password=

# MySQL 源数据库配置
mysql.host=127.0.0.1
mysql.port=3306
mysql.database=test
mysql.username=root
mysql.password=root

# 达梦数据库配置
dameng.host=127.0.0.1
dameng.port=5236
dameng.database=DAMENG
dameng.username=SYSDBA
dameng.password=SYSDBA

# 同步配置
sync.parallelTables=5          # 并行同步的表数量
sync.batchSize=1000           # 批量处理大小
sync.checkpoint.dir=./checkpoint  # 检查点保存目录
sync.enableFullSync=true      # 是否启用全量同步

# 需要同步的表（多个表用逗号分隔，为空则同步所有表）
sync.tables=
```

#### Docker Compose 仅用 environment 配置（推荐）

```yaml
services:
  sync-service:
    image: canal-dameng-sync:latest
    environment:
      CANAL_HOST: canal-server
      CANAL_PORT: "11111"
      CANAL_DESTINATION: example
      MYSQL_HOST: mysql
      MYSQL_PORT: "3306"
      MYSQL_DATABASE: demo
      MYSQL_USERNAME: root
      MYSQL_PASSWORD: root
      DAMENG_HOST: dm
      DAMENG_PORT: "5236"
      DAMENG_DATABASE: DAMENG
      DAMENG_USERNAME: SYSDBA
      DAMENG_PASSWORD: SYSDBA
      SYNC_TABLES: user,order,order_item
      SYNC_FULL_EXECUTION_MODE: two_phase_no_fk
      SYNC_TABLE_DEPENDENCIES_XML: table-dependencies.xml
      SYNC_CONFIG_DIR: /opt/sync-config
    volumes:
      - ./sync-config:/opt/sync-config:ro
```

> 提示：`SYNC_TABLE_DEPENDENCIES_XML` 指向的 XML 需位于 `SYNC_CONFIG_DIR` 或绝对路径可访问位置。

### 3. 编译打包

```bash
mvn clean package
```

### 4. 运行

```bash
java -jar target/canal-dameng-sync-1.0.0.jar
```

## 配置说明

### Canal 配置

- `canal.host`: Canal Server 地址
- `canal.port`: Canal Server 端口（默认 11111）
- `canal.destination`: Canal 实例名称
- `canal.username`: Canal 用户名（可选）
- `canal.password`: Canal 密码（可选）
- `canal.batchSize`: 每次拉取的 binlog 数量
- `canal.subscribe`: 订阅规则（正则表达式）

### MySQL 配置

- `mysql.host`: MySQL 服务器地址
- `mysql.port`: MySQL 端口（默认 3306）
- `mysql.database`: 数据库名
- `mysql.username`: 用户名
- `mysql.password`: 密码
- `mysql.initialSize`: 连接池初始大小
- `mysql.maxActive`: 连接池最大连接数

### 达梦数据库配置

- `dameng.host`: 达梦数据库服务器地址
- `dameng.port`: 达梦数据库端口（默认 5236）
- `dameng.database`: 数据库名
- `dameng.username`: 用户名
- `dameng.password`: 密码
- `dameng.initialSize`: 连接池初始大小
- `dameng.maxActive`: 连接池最大连接数

### 同步配置

- `sync.parallelTables`: 并行同步的表数量（默认 5）
- `sync.batchSize`: 批量处理大小（默认 1000）
- `sync.checkpoint.dir`: 检查点保存目录（默认 ./checkpoint）
- `sync.enableFullSync`: 是否启用全量同步（默认 true）
- `sync.tables`: 需要同步的表列表，多个表用逗号分隔，为空则同步所有表

## 工作原理

### 全量同步

1. 获取 MySQL 表的 CREATE TABLE 语句
2. 转换 MySQL DDL 到达梦 DDL 格式
3. 在达梦数据库中创建表结构
4. 分批读取 MySQL 表数据并插入到达梦数据库

### 增量同步

1. 连接 Canal Server，订阅 binlog 变更
2. 解析 binlog 事件（INSERT/UPDATE/DELETE）
3. 根据事件类型执行相应的 DML 操作到达梦数据库
4. 定期保存检查点（binlog 文件名和位置）

### 断点续传

- 检查点保存在 `checkpoint/checkpoint.json` 文件中
- 服务启动时自动加载检查点，从上次位置继续同步
- 每次处理完一批数据后更新检查点

### 并行处理

- 使用线程池管理多表并行同步
- 每个表有独立的增量同步服务
- 单表内的数据变更按顺序处理，保证一致性

## 注意事项

1. **表结构转换**：MySQL 和达梦数据库的 DDL 语法有差异，工具会进行基本转换，但复杂场景可能需要手动调整。

2. **主键要求**：UPDATE 和 DELETE 操作需要主键，如果表没有主键，这些操作可能失败。

3. **数据类型映射**：部分 MySQL 数据类型需要手动映射到达梦数据库类型。

4. **性能优化**：
   - 根据实际情况调整 `sync.parallelTables` 参数
   - 调整 `sync.batchSize` 以平衡性能和内存使用
   - 确保 Canal Server 和数据库服务器有足够的资源

5. **监控和日志**：建议配置日志级别为 INFO 或 DEBUG，便于排查问题。

## 故障排查

### 日志文件

应用运行时会生成以下日志文件：

#### 1. 所有日志（包含 INFO/DEBUG/ERROR）
- **当前日志**：`logs/sync.log`
- **历史日志**：`logs/sync.yyyy-MM-dd.log`（按天滚动，保留30天）

#### 2. 错误和警告日志（推荐查看）
- **当前日志**：`logs/sync-error.log`（只记录 WARN 和 ERROR 级别）
- **历史日志**：`logs/sync-error.yyyy-MM-dd.log`（按天滚动，保留90天）
- **特点**：
  - 只包含错误和警告，便于快速定位问题
  - 包含完整异常堆栈信息
  - 保留时间更长（90天）

#### 3. 控制台输出
- 所有日志同时输出到控制台

#### 查看失败日志

**快速查看最新错误：**
```bash
# Windows PowerShell
Get-Content logs\sync-error.log -Tail 50

# Linux/Mac
tail -f logs/sync-error.log
```

**搜索特定表的错误：**
```bash
# Windows PowerShell
Select-String -Path "logs\sync-error*.log" -Pattern "tableName"

# Linux/Mac
grep "tableName" logs/sync-error*.log
```

**过滤所有错误日志：**
```bash
# Windows PowerShell
Select-String -Path "logs\sync*.log" -Pattern "ERROR"

# Linux/Mac
grep -r "ERROR" logs/
```

#### 记录的失败场景

1. **拉取 Canal 数据失败**
   - 日志内容：`拉取 Canal 数据失败: {tableName}`
   - 可能原因：Canal Server 连接问题、网络问题、binlog 解析错误

2. **处理数据变更失败**
   - 日志内容：`处理数据变更失败: {tableName}`
   - 可能原因：达梦数据库连接问题、SQL 执行错误、数据类型转换失败

### 检查点文件

检查点文件位于 `checkpoint/checkpoint.json`，格式如下：

```json
{
  "table1": {
    "binlogFile": "mysql-bin.000001",
    "binlogPosition": 12345,
    "updateTime": 1234567890
  }
}
```

### 常见问题

1. **连接失败**：检查 Canal Server 和数据库连接配置
2. **同步延迟**：检查 Canal Server 性能，调整 batchSize
3. **数据不一致**：检查主键配置，确保表有主键
4. **DDL 转换失败**：手动检查并调整表结构

## 开发

### 项目结构

```
canal-dameng-sync/
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/tddq/sync/
│   │   │       ├── config/          # 配置类
│   │   │       ├── sync/            # 同步服务
│   │   │       ├── util/            # 工具类
│   │   │       └── SyncApplication.java  # 主类
│   │   └── resources/
│   │       └── application.properties    # 配置文件
│   └── test/
├── pom.xml
└── README.md
```

### 依赖说明

- Canal Client 1.1.8：Canal 客户端
- MySQL Connector：MySQL 数据库驱动
- DmJdbcDriver18：达梦数据库驱动
- Druid：数据库连接池
- FastJSON：JSON 处理
- Logback：日志框架

## 许可证

Apache License 2.0

## 参考

- [Canal 官方文档](https://github.com/alibaba/canal)
- [Canal Client 示例](https://github.com/alibaba/canal/wiki/ClientExample)
- [达梦数据库文档](https://www.dameng.com/)

