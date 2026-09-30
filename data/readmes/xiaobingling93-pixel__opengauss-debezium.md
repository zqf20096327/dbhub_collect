# debezium

## 介绍
Debezium是一个开源项目，为捕获数据更改(change data capture,CDC)提供了一个低延迟的流式处理平台。

本仓库初始代码来源于Debezium v1.8.1.Final版本

[Debezium v1.8.1.Final](https://github.com/debezium/debezium/tree/v1.8.1.Final)

本仓库构建的目的是为了借助于debezium（需要做一定的适配）和kafka开源组件，构建基于openGauss的在线迁移系统。

在线迁移工具详情请参考

[oracle在线迁移工具](https://gitcode.com/opengauss/openGauss-tools-onlineMigration)

[迁移校验工具管理portal](https://gitcode.com/opengauss/openGauss-migration-portal)

更多debezium介绍和构建过程请参考

[debezium介绍](https://gitcode.com/opengauss/debezium/blob/master/README_ZH.md)

## 迁移插件下载
当前Debezium mysql connector和Debezium opengauss connector作为openGauss数据迁移平台的组件，可在[官网下载页面](https://opengauss.org/zh/download/)的openGauss Tools部分下载各版本的发布包。
- replicate-mysql2openGauss
基于Debezium mysql connector构建，支持对MySQL增量数据的同步

- replicate-openGauss2mysql
基于Debezium opengauss connector构建，支持对openGauss全量数据和增量数据的同步

获取软件包后，需对其完整性进行校验，操作步骤如下：

1. 计算下载包的sha256值（以replicate-mysql2openGauss_6.0.0为例，其他版本操作相同）
~~~
sha256sum replicate-mysql2openGauss-6.0.0.tar.gz
~~~

2. 在[官网下载页面](https://opengauss.org/zh/download/)的openGauss Tools部分中复制对应软件包的sha256值，与步骤1计算出的sha256值做对比，如果一致则可以确认下载下来的包是完整的，否则需要重新下载。

## 构建Debezium

### 软件依赖

使用Debezium代码库并在本地配置它需要以下软件：

- [Git](https://gitcode.com/link?target=https%3A%2F%2Fgit-scm.com) 2.2.1 or later
- JDK 11 or later, e.g. [OpenJDK](https://gitcode.com/link?target=http%3A%2F%2Fopenjdk.java.net%2Fprojects%2Fjdk%2F)
- [Apache Maven](https://gitcode.com/link?target=https%3A%2F%2Fmaven.apache.org%2Findex.html) 3.6.3 or later

有关平台上的安装说明，请参阅上面的链接。您可以通过以下指令查看安装版本

```
git --version
java -version
mvn -version
```

### Debezium oracle connector

构建Debezium oracle connector，需手动下载xstream.jar包，并用如下命令安装至本地maven仓库，详情请参考[Debezium oracle connector](https://gitcode.com/opengauss/debezium/tree/master/debezium-connector-oracle)

```
mvn install:install-file -DgroupId=com.oracle.instantclient -DartifactId=xstreams -Dversion=21.1.0.0 -Dpackaging=jar -Dfile=xstreams.jar
```

### Debezium mysql connector

原始debezium mysql connector基于开源组件mysql-binlog-connector-java的0.25.4版本读取binlog，并串行解析为event事件，我们对该开源软件进行修改，可用于支持并行解析event事件，以提高debezium mysql connector 作为source端的性能。

对应的patch文件为[mysql-binlog-connector-java-0.25.4.patch](https://gitcode.com/opengauss/debezium/tree/master/debezium-connector-mysql/patch/mysql-binlog-connector-java-0.25.4.patch),并在配置文件中增加参数parallel.parse.event参数控制是否启用并行解析event功能，默认为true，表示启用并行解析能力。

同时针对debezium mysql connector，我们也增加sink端能力，可支持数据在openGauss端按照事务粒度并行回放，用于构建完整的端到端的迁移能力（mysql -> openGauss）。

构建Debezium mysql connector, 需应用patch文件，可利用一键式构建脚本[build.sh](https://gitcode.com/opengauss/debezium/tree/master/build.sh)快速编译Debezium mysql connector，编译的压缩包的位置为：

```
debezium-connector-mysql/target/debezium-connector-mysql-1.8.1.Final-plugin.tar.gz
```

### Debezium opengauss connector

我们基于原始的debezium开源软件的debezium postgresql connector，新增了debezium opengauss connector，支持抽取openGauss的逻辑日志，将其存入kafka的topic中。同时，我们增加了debezium opengauss connector的sink端能力，能够抽取kafka的日志并完成数据的回放，以实现对数据dml操作的反向迁移能力（openGauss -> mysql, openGauss -> PostgreSQL）.
编译debezium后，可以得到反向迁移工具的压缩包，压缩包的位置为：

```
debezium-connector-openngauss/target/debezium-connector-opengauss-1.8.1.Final-plugin.tar.gz
```

### Debezium postgres connector

基于原始的debezium开源软件的debezium postgresql connector，支持抽取postgresql的逻辑日志，将其存入kafka的topic中。同时，我们增加了debezium postgres connector 全量迁移和sink端能力，全量迁移支持抽取postgresql端全量数据和对象，并将对应消息存入kafka中。增量迁移通过抽取postgresql的逻辑日志并存入kafka中。sink端能够抽取kafka的日志并完成数据的回放，以实现对数据的全量和增量迁移能力（PostgreSQL -> openGauss）.
编译debezium后，可以得到PostgreSQL迁移工具的压缩包，压缩包的位置为：

```
debezium-connector-postgres/target/debezium-connector-postgres-1.8.1.Final-plugin.tar.gz
```

### 构建命令

```
mvn clean package -P quick,skip-integration-tests,oracle,jdk11,assembly,xstream,xstream-dependency,skip-tests -Dgpg.skip -Dmaven.test.skip=true -Denforcer.skip=true
```

## Debezium mysql connector

### 新增功能介绍

原始的debezium mysql connector作为source端，可用于捕获数据变更并存入kafka。现新增如下功能点：

- Source端支持并行解析event事件；
- Source端支持自定义配置快照点；
- 配置gtid_mode=on，source端支持解析last_committed和

[...截断...]

sequence_number字段，并存入kafka；
- 基于Debezium connector（Kafka Connect）框架，增加sink端能力，可用于从kafka抽取数据并在openGauss端按照事务粒度并行回放;
- 增加迁移进度上报功能，可用于读取数据迁移时延；
- 增加增量迁移断点续传功能，用户中断后基于断点重启后继续迁移；
- sink端增加按表并行回放的能力，并支持自定义参数控制按事务回放还是按表回放。

### 新增配置参数说明

#### Source端

(1) 启动类

```
connector.class=io.debezium.connector.mysql.MySqlConnector
```

(2) 配置文件示例

[mysql-source.properties](https://gitcode.com/opengauss/debezium/tree/master/debezium-connector-mysql/patch/mysql-source.properties)

(3) debezium原生参数含义请参考：

[debezium原生参数](https://debezium.io/documentation/reference/1.9/connectors/mysql.html)

(4) topic路由请参考：

[topic路由](https://debezium.io/documentation/reference/stable/transformations/topic-routing.html)

在线迁移方案严格保证事务的顺序性，因此将DDL和DML路由在kafka的一个topic下，且该topic的分区数只能为1(参数num.partitions=1)，从而保证source端推送到kafka，和sink端从kafka拉取数据都是严格保序的。

默认情况下，debezium mysql connector针对DDL，DML和事务创建独立的topic，且每个表为一个topic

事务topic需配置provide.transaction.metadata=true，才显式生成事务topic

topic命名规则为：

DDL topic名称：${database.server.name}

DML topic名称：${database.server.name}.db_name.table_name

事务topic名称：${database.server.name}.transaction

DDL，DML和事务topic名称均以${database.server.name}开头，因此以前缀方式去正则匹配合并topic，将DDL，DML和事务的
topic进行路由合并为一个topic，且该topic的分区数只能为1。

source端将数据推送至该topic下，同时sink端配置topics为合并后的topic，用于从kafka抽取数据，从而可保证事务的顺序。

DDL，DML和事务topic利用路由转发功能进行合并的配置如下：

Source端：
```
database.server.name=mysql_server

provide.transaction.metadata=true

transforms=route
transforms.route.type=org.apache.kafka.connect.transforms.RegexRouter
transforms.route.regex=^mysql_server(.*)
transforms.route.replacement=mysql_server_topic
```

Sink端：
```
topics=mysql_server_topic
```

(5) 新增配置参数说明

| 参数                             | 类型      | 参数说明                                                                                                                                                          |
|--------------------------------|---------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|
| snapshot.offset.binlog.filename | String  | 自定义配置快照点的binlog文件名                                                                                                                                            |
| snapshot.offset.binlog.position | String  | 自定义配置快照点的binlog位置                                                                                                                                             |
| snapshot.offset.gtid.set       | String  | 自定义配置快照点的Executed_Gtid_Set，需注意最大事务号需减1                                                                                                                        |
| parallel.parse.event           | boolean | 是否启用并行解析event能力，默认为true，表示启用并行解析能力                                                                                                                            |
| commit.process.while.running   | boolean | 是否开启迁移进度上报功能，默认为false，表示不开启该功能                                                                                                                                |
| source.process.file.path       | String  | 迁移进度文件输出路径，默认在迁移插件同一目录下，在迁移进度上报功能开启后起作用                                                                                                                       |
| commit.time.interval           | int     | 迁移进度上报的时间间隔，默认值为1，单位：秒，在迁移进度上报功能开启后起作用                                                                                                                        |
| create.count.info.path         | String  | 源端binlog日志的事务号输出路径，默认在迁移插件同一目录下，必须与sink端的该路径保持一致，用于和sink端交互获取总体同步时延                                                                                           |
| process.file.count.limit       | int     | 同一目录下文件数目限制，超过该数目工具会按时间从早到晚删除多余进度文件，默认为10                                                                                                                     |
| process.file.time.limit        | int     | 进度文件保存时间，超过该时间后工具会删除对应的进度文件，默认为168，单位：小时               