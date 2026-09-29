# FTP 到数据库同步服务（ftpflow）

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Java](https://img.shields.io/badge/Java-8%2B-orange.svg)](https://www.oracle.com/java/)
[![Build](https://img.shields.io/badge/build-Maven-blue.svg)](https://maven.apache.org/)

本项目用于定时轮询 FTP 目录，读取符合命名规则的业务数据文件，解析后按 `mapping.yaml` 配置写入 TDengine（时序历史数据）和 OceanBase（最新数据）。适用于工业/物联网场景下将 FTP 上落地的批量文本数据增量同步到数据库。

## 目录

- [当前能力](#当前能力)
- [技术栈](#技术栈)
- [环境要求](#环境要求)
- [快速开始](#快速开始)
- [处理流程](#处理流程)
- [文件格式](#文件格式)
- [映射配置](#映射配置)
- [配置文件](#配置文件)
- [构建与运行](#构建与运行)
- [日志](#日志)
- [运行产物](#运行产物)
- [贡献](#贡献)
- [许可证](#许可证)

## 技术栈

| 组件 | 说明 |
| --- | --- |
| Java 8 | 编译与运行目标版本 |
| Maven（maven-shade-plugin） | 构建可执行 fat jar |
| Apache Commons Net | FTP 客户端 |
| SnakeYAML | 解析 `mapping.yaml` |
| Gson | 读写 `checkpoint.json` |
| TDengine JDBC (TAOS-WS) | 写入时序历史数据 |
| MySQL Connector/J | 以 MySQL 兼容模式写入 OceanBase |
| SLF4J + Logback | 日志 |

## 环境要求

- JDK 8 及以上
- Maven 3.6+
- 一台可访问的 FTP 服务器
- TDengine 与/或 OceanBase 实例（按 `mapping.yaml` 中启用的目标库准备）

## 快速开始

```bash
# 1. 克隆
git clone <your-repo-url>
cd ftpflow

# 2. 配置：复制模板并按需修改（真实凭据请勿提交）
cp config.properties.example config.properties

# 3. 按真实库表结构核对 mapping.yaml

# 4. 打包
mvn -q -DskipTests package

# 5. 运行（config.properties 与 mapping.yaml 放在 jar 同级目录）
java -jar target/ftpflow-1.0.0.jar
```

> 应用会先加载打包进 jar 的默认 `config.properties`（示例值），再用 jar 同级目录下的 `config.properties` 覆盖同名配置项。详见 [配置文件](#配置文件)。

## 当前能力

- 按固定间隔依次轮询同一台 FTP 服务器上的多个远程目录。
- 只列出远程文件名，不把文件下载到本地临时目录。
- 处理文件名格式：

```text
xxx_yyy_yyyyMMddHHmmss.txt
```

- 使用文件名第二段 `yyy` 作为文件类型。
- 每个远程目录拥有独立的 checkpoint 命名空间，默认用目录名，可通过 `checkpointPrefix` 覆盖。
- 只处理时间戳大于当前 checkpoint 的文件。
- 每个远程目录每轮按时间戳排序后最多处理自己的 `batchSize` 个文件。
- 通过 FTP `InputStream` 直接读取并解析文件内容。
- 失败文件会记录到 `local.errorDir/error.log`。
- 根据 `mapping.yaml` 将解析结果写入 TDengine 和 OceanBase。
- 每个分组处理完后，将 checkpoint 推进到本轮该分组最大的文件时间戳。

## 暂不包含

- 自动建表。
- 本地下载归档。
- 失败文件内容归档。

## 处理流程

### 启动阶段

1. 加载配置：先读取 classpath 中打包的 `config.properties`，再用 jar 同级目录的同名文件覆盖同名配置项。
2. 解析 FTP 连接与目录列表：连接参数取全局 `ftp.host`（必填）、`ftp.port`、`ftp.username`、`ftp.password`、`ftp.passiveMode`、`ftp.encoding`。远程目录由 `ftp.remoteDirs` 逗号数组配置，按书写顺序轮询；目录名取路径最后一段（要求互不重复），作为目录 id 和默认 `checkpointPrefix`。每个目录可用 `ftp.<目录名>.batchSize`（兜底 10）、`ftp.<目录名>.checkpointPrefix`（默认目录名）、`ftp.<目录名>.minFileAgeSeconds`（回退全局 `ftp.minFileAgeSeconds`）单独覆盖。
3. 加载 checkpoint 文件（默认 `./checkpoint.json`）到内存。checkpoint 是一个 JSON 映射，键为 `checkpointPrefix:文件类型`，值为该组已处理的最大文件时间戳。文件不存在或损坏时从空 checkpoint 开始。
4. 加载 `mapping.yaml` 并构建 TDengine、OceanBase 写入器。映射文件缺失或非法会直接启动失败；数据库连接按需建立，启动时不连接。
5. 启动单线程调度器（非守护线程 `ftp-scheduler`），以 `schedule.intervalSeconds` 为间隔按固定延迟执行轮询：上一轮完全结束后再等待间隔时间，不会出现两轮重叠。
6. 注册 shutdown hook：收到退出信号时停止调度器并等待当前轮结束（最多 10 秒），随后断开所有 FTP 连接、关闭数据库连接，实现优雅停机。

### 每轮轮询（runCycle）

每轮串行遍历所有远程目录（每个目录独立建立一次 FTP 连接），单个目录异常只影响自己，不影响其他目录：

```text
runDirectoryCycle(directory)
  -> connect()          登录、进入被动模式、二进制传输、切换到 remoteDir
  -> listFileNames()    只列普通文件；跳过修改时间距当前不足 minFileAgeSeconds 的文件
                        （视为可能正在上传，留到下一轮）
  -> parseAndFilter()   文件名必须匹配 xxx_yyy_yyyyMMddHHmmss.txt，否则忽略；
                        取 yyy 作为文件类型（groupKey），14 位数字作为文件时间戳；
                        时间戳 <= checkpoint(checkpointPrefix:yyy) 的文件跳过；
                        剩余文件按时间戳升序排序，只保留前 batchSize 个（跨类型合计）
  -> 按文件类型分组
  -> processGroup()     每组内按时间戳升序逐个处理文件：
                          -> ftpClient.readFile()   通过 InputStream 流式读取，不落地本地
                          -> fileParser.parse()     解析文件内容（见下）
                          -> recordWriter.write()   路由写库（见下）
                          -> 任一步失败：写入 error.log 后继续处理组内下一个文件
                        整组处理完后，checkpoint 推进到本组本轮最大时间戳并立即落盘
  -> disconnect()       无论成功失败，finally 中断开连接
```

### 文件解析（FileParser）

文件整体结构为：`文件头 ~ 记录1 ~ 记录2 ~ ... ~ ||`

- 第一个 `~` 之前是文件头，之后每条记录以 `~` 结尾，整个文件以 `||` 结束，`||` 之后不允许出现其他内容。
- 字段以 `;` 分隔，解析后文件头字段命名为 `headerField1..N`，记录字段命名为 `boreholeField1..N`。
- 每条解析记录同时携带文件头字段和自身记录字段，供映射配置按源字段名取值。

### 写库路由（DatabaseRecordWriter）

1. 用文件类型（`yyy`）查找 `mapping.yaml` 中的类型配置。未配置的类型只记 warning 并视为处理成功，不阻塞该组 checkpoint 推进。
2. 类型配置中存在 `tdengine` 块时，`TDengineWriter` 使用 TDengine WebSocket JDBC 驱动写入历史数据：每个文件生成一条多子表批量 `INSERT`，通过 `USING 超级表 TAGS (...)` 自动建子表，时间戳列固定放在首列。
3. 类型配置中存在 `oceanbase` 块时，`OceanBaseWriter` 使用 MySQL 兼容 JDBC 驱动写入最新数据：每个文件生成一条多值 `INSERT ... ON DUPLICATE KEY UPDATE ...`，按 `uniqueKeyField` 做 upsert。
4. 两个目标库相互独立：TDengine 失败不影响继续尝试 OceanBase；任一目标失败，该文件整体记为失败文件。
5. 每次写入前用 `Connection.isValid(timeout)` 检查连接可用性，连接失效自动重连；写入失败时关闭当前连接，下次写入重建。

### 失败与 checkpoint 语义

- 单个文件解析或写库失败：追加记录到 `local.errorDir/error.log`（格式：`时间 | 文件名 | 原因`），本轮继续处理后续文件。
- 整组处理完后 checkpoint 仍会推进到组内最大时间戳，失败文件不会自动重试，需要根据 error.log 人工处理。
- checkpoint 每次更新都写盘，采用临时文件加原子重命名方式，进程中途被杀不会留下损坏的 JSON。

## 文件格式

文件名格式：

```text
xxx_yyy_yyyyMMddHHmmss.txt
```

示例：

```text
abc_MGSS_20260618120000.txt
```

其中：

- `abc`：文件来源或前缀。
- `MGSS`：文件类型，也是 `mapping.yaml` 中的类型键。
- `20260618120000`：文件时间戳，用于排序和 checkpoint 判断。

文件内容解析后会生成通用字段名：

- 文件头字段：`headerField1`、`headerField2`、...
- 明细记录字段：`boreholeField1`、`boreholeField2`、...

## 映射配置

业务写库规则放在 `mapping.yaml`，不写死在 Java 代码中。

当前启用的类型：

- `MGYL`：写入 OceanBase。
- `MGSS`：写入 TDengine 和 OceanBase。
- `HDWY`：写入 OceanBase。
- `WYSS`：写入 TDengine 和 OceanBase。
- `DBLC`：写入 OceanBase。
- `LCSS`：写入 TDengine 和 OceanBase。

投产前需要核对 `mapping.yaml` 中的表名、字段名和 source 对应关系与真实库表结构一致。

字段类型支持：

- `string`
- `int`
- `long`
- `decimal`
- `date`
- `datetime`

字段未配置 `type` 时默认按 `string` 处理；源文件中的空字段统一写入为 SQL `NULL`，不会在数字或时间解析时报错。

日期时间规则：

- `date` 支持 `yyyy-MM-dd` 和 `yyyyMMdd`。
- `datetime` 支持 `yyyy-MM-dd HH:mm:ss`、`yyyyMMddHHmmss`，也兼容带 `T` 分隔符的时间格式。

### TDengine 配置说明

TDengine 数据库由 `tdengine.url` 决定，`mapping.yaml` 不需要配置数据库名。

TDengine 映射必须包含：

- `table`：超级表名。
- `subtableSuffix`：用于拼接子表名后缀的目标列名。
- `timestampField`：时间戳目标列名。
- `tags`：TAG 字段，顺序需要和超级表 TAG 定义一致。
- `fields`：普通列字段，不包含 TAG。

### OceanBase 配置说明

OceanBase 映射必须包含：

- `database`：数据库名。
- `table`：表名。
- `uniqueKeyField`：用于 upsert 的唯一键或主键列名。
- `fields`：写入字段列表。

真实表结构中必须给 `uniqueKeyField` 对应列建立唯一键或主键，否则 `ON DUPLICATE KEY UPDATE` 不会按预期生效。

## 配置文件

应用启动时按以下顺序加载配置：

1. 先加载 classpath 中打包的 `config.properties`。
2. 如果应用以 jar 方式运行，并且 jar 同级目录存在 `config.properties`，再加载该外部文件覆盖同名配置。

当前应用不读取命令行参数。

主要配置项：

```properties
# FTP 服务器（全局唯一）
ftp.host=127.0.0.1
ftp.port=21
ftp.username=ftpuser
ftp.password=changeme
ftp.passiveMode=true
ftp.encoding=UTF-8
ftp.minFileAgeSeconds=60

# 调度
schedule.intervalSeconds=40

# 远程目录数组，逗号分隔，按书写顺序轮询
# 目录名取路径最后一段，作为目录 id 和默认 checkpointPrefix
ftp.remoteDirs=/site1,/site2,/site3

# 每目录可选覆盖：batchSize（兜底 10）、checkpointPrefix、minFileAgeSeconds
ftp.site1.batchSize=20
ftp.site2.batchSize=50
ftp.site3.batchSize=50

# 本地运行文件
local.errorDir=./runError
local.checkpointFile=./checkpoint.json
mapping.configFile=./mapping.yaml

# TDengine
tdengine.url=jdbc:TAOS-WS://127.0.0.1:6041/example_db
tdengine.user=root
tdengine.password=taosdata
tdengine.driverClass=com.taosdata.jdbc.ws.WebSocketDriver

# OceanBase
oceanbase.url=jdbc:mysql://127.0.0.1:2881/example_db?useSSL=false&serverTimezone=Asia/Shanghai
oceanbase.user=root@sys
oceanbase.password=changeme
oceanbase.driverClass=com.mysql.cj.jdbc.Driver
```

> 以上仅为示例值。实际部署时请在 jar 同级目录放置真实的 `config.properties` 覆盖，并妥善保管数据库/FTP 凭据，切勿提交到版本库。

## 构建与运行

编译目标为 Java 8。打包使用 maven-shade-plugin 生成包含全部依赖、可直接运行的 fat jar（主类 `com.ftpflow.FtpToDbApplication`）。

编译：

```bash
mvn -q -DskipTests compile
```

生产打包：

```bash
mvn -q -DskipTests package
```

运行：

```bash
java -jar target/ftpflow-1.0.0.jar
```

部署时注意相对路径的解析基准不同：`mapping.yaml`（`mapping.configFile`）相对 jar 所在目录解析；`checkpoint.json`、`runError/`、`logs/` 相对启动时的工作目录生成。建议在 jar 所在目录内启动，两者保持一致。

## 日志

日志由打包进 jar 的 `logback.xml` 控制：同时输出到控制台和 `logs/ftpflow.log`，文件按天滚动，保留 30 天，根日志级别为 `WARN`。

## 运行产物

以下文件或目录是运行期或构建期产物，默认不应提交：

- `target/`
- `logs/`
- `runError/`
- `checkpoint.json`
- `checkpoint.json.tmp`
- 外部覆盖用的 `/config.properties`

这些已在 `.gitignore` 中忽略。

## 贡献

欢迎通过 Issue 和 Pull Request 参与改进：

1. Fork 本仓库并创建特性分支（`git checkout -b feature/xxx`）。
2. 提交前确保 `mvn -DskipTests package` 可正常构建。
3. 不要在提交中包含任何真实的服务器地址、账号、密码或业务库表结构。
4. 发起 Pull Request，并在描述中说明变更动机与影响范围。

## 许可证

本项目基于 [MIT License](LICENSE) 开源。
