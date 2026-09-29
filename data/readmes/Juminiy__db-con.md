# TiDB 

## OLTP & OLAP 

在开始TiDB之前，先了解何为OLAP，何为OLTP

[OLTP VS OLAP](https://www.stitchdata.com/resources/oltp-vs-olap)，[分布式数据库开发者大会](https://open.oceanbase.com/dc2021)

账本：记账，转账，算账

### OLTP：事务型操作

适合：记账，转账，area：付款交易，信用卡，支票

重点在于：快速处理事务，快速读写改，事务失败也要保证数据完整性。

### OLAP：分析型操作

适合：算账，area：历史数据查询，分析，商业统筹，趋势分析

强调：快速查询响应，将数据转换为信息价值，事务失败不会对客户造成影响，会延迟商业判断力和准确性

### ETL：join OLTP to OLAP

将数据从多个OLTP数据库转换到OLAP的操作：Extract，Transform，Load，从数据源加载数据到数据目标位置，仓库称为数据仓库或者数据湖，既然能称为数据湖，海量数据的大小要达到一定规模(PB,EP级别)

oltp要满足一致性和正确性，是一个基础；分析型则对企业有了更高的要求

oltp是操作型的，olap是信息型的，他们无论从物理存储和使用特征来看的差别都很大，所以同时做到两者对于ddb(distributed database)的开发者来说非常挑战

|                         | OLTP                                                         | OLAP                                                         |
| ----------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| **Characteristics**     | 处理大规模小型事务(行存)                                     | 大量列存数据的复杂查询                                       |
| **Query types**         | Simple standardized queries                                  | Complex queries                                              |
| **Operations**          | Based on INSERT, UPDATE, DELETE commands                     | Based on SELECT commands to aggregate data for reporting     |
| **Response time**       | Milliseconds                                                 | Seconds, minutes, or hours depending on the amount of data to process |
| **Design**              | 行业分类：手工业，零售业，银行金融                           | 特定主题的：存货，销售，市场营销                             |
| **Source**              | Transactions                                                 | Aggregated data from transactions                            |
| **Purpose**             | 实时控制运行重要的商业金融操作（快，准）                     | 计划，解决问题，制定决策，发现隐藏价值(狠)                   |
| **Data updates**        | Short, fast updates initiated by user                        | Data periodically refreshed with scheduled, long-running batch jobs |
| **Space requirements**  | Generally small if historical data is archived               | Generally large due to aggregating large datasets            |
| **Backup and recovery** | Regular backups required to ensure business continuity and meet legal and governance requirements | Lost data can be reloaded from OLTP database as needed in lieu of regular backups |
| **Productivity**        | Increases productivity of end users                          | Increases productivity of business managers, data analysts, and executives |
| **Data view**           | Lists day-to-day business transactions                       | Multi-dimensional view of enterprise data                    |
| **User examples**       | Customer-facing personnel, clerks, online shoppers           | Knowledge workers such as data analysts, business analysts, and executives |
| **Database design**     | Normalized databases for efficiency                          | Denormalized databases for analysis                          |

## Intro

### Character

NewSQL型分布式数据库，`distributed`&`database`

支持同时在线联机事务处理和在线分析处理的混合负载，兼容MySQL协议(可移植)，强一致，高可用

- OLTP 在线事务处理，OLAP 在线分析处理，同时做到两者（HTAP），这对于分布式数据库非常挑战


- 水平扩展：对比传统事务型集中数据库更加方便运维


- 协议兼容：对于已有的业务不需要做任何改动，不需要修改连接客户端和原有业务代码


- 分布式事务：数据的存在方式用独定结构做了调整


- 云原生：支持公有云，私有云，混合云，使用TiKV作为底层存储


- 最小ETL：HTAP混合负载，不再需要Extracted，Transformed，Loaded


- 高可用：使用Raft一致性算法保证高可用


### Devlop

灵感来源：Google Spanner论文

thanks开源作品：GolevelDB,BoltDB,RocksDB

同类产品：AntFincial的OceanBase ，TPC-C跑分 World No.1。最新的report中，黄东旭认为TiDB跑分接近OceanBase或者有超越

## Start

运维工具：TiUP

运维工作，部署，启动，关闭，销毁，弹性扩缩容，升级版本

TiUP Playground

Linux推荐发行版：CentOS7.3+

操作环境：CentOS8 vultr cloud server within public-ip ，2vCPU 4G RAM（内存与CPU过小容易爆炸）

````bash
curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
source ${your_shell_profile}
 
# 查看网卡
ip addr 
# 默认下载最新版本的TｉＤＢ组件
tiup playground
# help
tiup playground --help
#　或者指定组件，指定网卡，外部访问
tiup playground v5.4.0 --db 2 --pd 3 --kv 3 --host "[pub-ip]"

# 浏览器查看各种监控面板

# 连接shell交互式客户端
tiup client
# 或者mysql-shell交互式客户端
mysql --host 127.0.0.1 --port 4000 -u root

#清理集群
tiup clean --all
````

tidb playground 集群组件有：

- PD
- TiDB Engine
  - mysql connect : 4001 4000
- TiKV Engine
- TiFlash Engine
- Monitor System
  - Prometheus：9090
  - Grafana：3000
- Web Dashboard：2379/dashboard

## HTAP

OLTP:行存储引擎TiKV，OLAP:列存储引擎TiFlash

- OLTP的TiKV与OLAP的TiFlash同时存在，自动同步，强一致
- TiKV满足ACID分布式事务接口，TiFlash从TiKV实时复制数据，保证强一致
- 数据隔离：按需隔离部署，解决资源隔离问题
- 数据计算：计算引擎v5.0引入MPP，允许节点数据交换，提供高性能，高吞吐的SQL算法

````bash
# 压力工具
tiup install bench
# 生成数据
tiup bench tpch --sf=1 prepare --host "149.28.88.142"
# 查看生成的数据
SELECT CONCAT(table_schema,'.',table_name) AS 'Table Name', table_rows AS 'Number of Rows', CONCAT(ROUND(data_length/(1024*1024*1024),4),'G') AS 'Data Size', CONCAT(ROUND(index_length/(1024*1024*1024),4),'G') AS 'Index Size', CONCAT(ROUND((data_length+index_length)/(1024*1024*1024),4),'G') AS'Total'FROM information_schema.TABLES WHERE table_schema LIKE 'test';

# 只用TiKV的行存查询
SELECT
    l_orderkey,
    SUM(
        l_extendedprice * (1 - l_discount)
    ) AS revenue,
    o_orderdate,
    o_shippriority
FROM
    customer,
    orders,
    lineitem
WHERE
    c_mktsegment = 'BUILDING'
AND c_custkey = o_custkey
AND l_orderkey = o_orderkey
AND o_orderdate < DATE '1996-01-01'
AND l_shipdate > DATE '1996-02-01'
GROUP BY
    l_orderkey,
    o_orderdate,
    o_shippriority
ORDER BY
    revenue DESC,
    o_orderdate
limit 10;

# 同步到TiFlash列存
ALTER TABLE test.customer SET TIFLASH REPLICA 1;
ALTER TABLE test.orders SET TIFLASH REPLICA 1;
ALTER TABLE test.lineitem SET TIFLASH REPLICA 1;

# HTAP分析 可以对比两次分析结果
explain analyze SELECT
    l_orderkey,
    SUM(
        l_extendedprice * (1 - l_discount)
    ) AS revenue,
    o_orderdate,
    o_shippriority
FROM
    customer,
    orders,
    lineitem
WHERE
    c_mktsegment = 'BUILDING'
AND c_custkey = o_custkey
AND l_orderkey = o_orderkey
AND o_orderdate < DATE '1996-01-01'
AND l_shipdate > DATE '1996-02-01'
GROUP BY
    l_orderkey,
    o_orderdate,
    o_shippriority
ORDER BY
    revenue DESC,
    o_orderdate
limit 10;
````

## Env Dev Prod

我们来看一下TiDB集群的最低的环境配置要求：

### 开发及测试环境

| **组件** | **CPU** | **内存** | **本地存储** | **网络** | **实例数量(最低要求)** |
| :------- | :------ | :------- | :----------- | :------- | :--------------------- |
| TiDB     | 8 核+   | 16 GB+   | 无特殊要求   | 千兆网卡 | 1（可与 PD 同机器）    |
| PD       | 4 核+   | 8 GB+    | SAS, 200 GB+ | 千兆网卡 | 1（可与 TiDB 同机器）  |
| TiKV     | 8 核+   | 32 GB+   | SSD, 200 GB+ | 千兆网卡 | 3                      |
| TiFlash  | 32 核+  | 64 GB+   | SSD, 200 GB+ | 千兆网卡 | 1                      |
| TiCDC    | 8 核+   | 16 GB+   | SAS, 200 GB+ | 千兆网卡 | 1                      |

### 生产环境

| **组件** | **CPU** | **内存** | **硬盘类型**   | **网络**             | **实例数量(最低要求)** |
| :------- | :------ | :------- | :------------- | :------------------- | :--------------------- |
| TiDB     | 16 核+  | 32 GB+   | SAS            | 万兆网卡（2 块最佳） | 2                      |
| PD       | 4核+    | 8 GB+    | SSD            | 万兆网卡（2 块最佳） | 3                      |
| TiKV     | 16 核+  | 32 GB+   | SSD            | 万兆网卡（2 块最佳） | 3                      |
| TiFlash  | 48 核+  | 128 GB+  | 1 or more SSDs | 万兆网卡（2 块最佳） | 2                      |
| TiCDC    | 16 核+  | 64 GB+   | SSD            | 万兆网卡（2 块最佳） | 2                      |
| 监控     | 8 核+   | 16 GB+   | SAS            | 千兆网卡             | 1                      |

直接劝退！

# Cassandra

机器，两台1vCPU 2G RAM Ubuntu 20.04LTS

一键install docker

````bash
# !/bin/bash 
# sh dk-in.sh
sudo apt-get remove docker docker-engine docker.io containerd runc
sudo apt-get update
sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
    
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
docker --version
````



install in docker

````bash
docker pull cassandra:latest

# 可以使用一台机器两个容器，或者两台不同的机器的两个容器
# 两台机器组成一个集群

# can-1
docker run --name "can-1" -d -e CASSANDRA_BROADCAST_ADDRESS=[can-1-ip] -p 7000:7000 cassandra
# can-2 
docker run --name "can-2" -d -e CASSANDRA_BROADCAST_ADDRESS=[can-2-ip] -p 7000:7000 -e CASSANDRA_SEEDS=[can-1-ip] cassandra

# bash shell interact 
# 进入两个can实例创造keyspace
docker exec -it cass_cluster cqlsh
````

golang连接

[GoCQL](https://github.com/gocql/gocql)

````bash
go get github.com/gocql/gocql
````

