# Zero-TiDB
Zero-TiDB

# 1. 概述
## 1.1. 简介
  TiDB 是 PingCAP 公司自主设计、研发的开源分布式关系型数据库，是一款同时支持在线事务处理与在线分析处理 (Hybrid Transactional and Analytical Processing, HTAP) 
的融合型分布式数据库产品，具备水平扩容或者缩容、金融级高可用、实时 HTAP、云原生的分布式数据库、兼容 MySQL 协议和 MySQL 生态等重要特性。
目标是为用户提供一站式 OLTP (Online Transactional Processing)、OLAP (Online Analytical Processing)、HTAP 解决方案。
TiDB 适合高可用、强一致要求较高、数据规模较大等各种应用场景。
## 1.2. 特性
1. 一键水平扩缩容得益于 TiDB 存储计算分离的架构的设计，可按需对计算、存储分别进行在线扩容或者缩容，扩容或者缩容过程中对应用运维人员透明。
2. 金融级高可用数据采用多副本存储，数据副本通过 Multi-Raft 协议同步事务日志，多数派写入成功事务才能提交，确保数据强一致性且少数副本发生故障时不影响数据的可用性。可按需配置副本地理位置、副本数量等策略，满足不同容灾级别的要求。
3. 实时 HTAP提供行存储引擎 TiKV、列存储引擎 TiFlash 两款存储引擎，TiFlash 通过 Multi-Raft Learner 协议实时从 TiKV 复制数据，确保行存储引擎 TiKV 和列存储引擎 TiFlash 之间的数据强一致。TiKV、TiFlash 可按需部署在不同的机器，解决 HTAP 资源隔离的问题。
4. 云原生的分布式数据库专为云而设计的分布式数据库，通过 TiDB Operator 可在公有云、私有云、混合云中实现部署工具化、自动化。
5. 兼容 MySQL 协议和 MySQL 生态兼容 MySQL 协议、MySQL 常用的功能、MySQL 生态，应用无需或者修改少量代码即可从 MySQL 迁移到 TiDB。提供丰富的数据迁移工具帮助应用便捷完成数据迁移。
## 1.3. 适用
1. 原业务的 MySQL 的业务遇到单机容量或者性能瓶颈时，可以考虑使用 TiDB 无缝替换 MySQL。TiDB 可以提供如下特性：
   - 吞吐量、存储和计算能力的水平扩展
   - 水平伸缩时不停服务
   - 强一致性分布式 ACID 事务
2. 大数据量下，MySQL 复杂查询很慢。
3. 大数据量下，数据增长很快，接近单机处理的极限，不想分库分表或者使用数据库中间件等对业务侵入性较大、对业务有约束的 Sharding 方案。
4. 大数据量下，有高并发实时写入、实时查询、实时统计分析的需求。
5. 有分布式事务、多数据中心的数据 100% 强一致性、auto-failover 的高可用的需求。
## 1.4. 不适用
1. 单机 MySQL 能满足的场景也用不到 TiDB。
2. 数据条数少于 5000w 的场景下通常用不到 TiDB，TiDB 是为大规模的数据场景设计的。
3. 如果你的应用数据量小（所有数据千万级别行以下），且没有高可用、强一致性或者多数据中心复制等要求，那么就不适合使用 TiDB。

# 2. 功能

# 3. 使用

## 3.1 Docker安装
### 3.1.1. pull images
```shell
#第一种
docker pull xuxuclassmate/tidb
#第二种
docker pull pingcap/tidb
```

### 3.1.2. start tidb
```shell
docker run --name tidb -d --privileged=true -p 4000:4000 xuxuclassmate/tidb

```

### 3.1.3. use mysql client to connect tidb
```shell
mysql -h 127.0.0.1 -P 3306 -u root
```

### 3.1.4. init data

```shell
CREATE DATABASE zero;

CREATE USER 'zero'@'%' IDENTIFIED BY 'zero';
GRANT ALL PRIVILEGES ON demo.* TO 'zero'@'%';
FLUSH PRIVILEGES;

use mysql
update user set authentication_string = password('root@123') where User = 'root';
FLUSH PRIVILEGES;

CREATE TABLE `system_user` (
 `id` int(11) NOT NULL AUTO_INCREMENT,
 `username` varchar(100) DEFAULT NULL,
 `age` int(11) DEFAULT NULL,
 PRIMARY KEY (`id`)
) ENGINE=InnoDB;
  
INSERT INTO zero.`system_user`(id, name, age)VALUES(1, 'jack', 18);
INSERT INTO zero.`system_user`(id, name, age)VALUES(2, 'alyssa', 19);
```

## 3.2. 直接使用


# 4. 其他

# 5. 参考