## PostgreSQL 与 openGauss 对比实验

**目录**

1. 简介

2. 实验环境

3. 实验结构

4. 参考资料

   

#### 1.简介

本文档记录了 PostgreSQL 和 openGauss 在性能、存储与索引、并发控制与事务处理以及安全性与可靠性方面的对比实验。通过一系列测试，旨在探讨两种数据库系统在不同应用场景下的表现。



#### 2.实验环境

- 硬件配置

  - CPU:  [01]: Intel64 Family 6 Model 186 Stepping 2 GenuineIntel ~2600 Mhz

  - 可用的物理内存:   5,759 MB

    物理内存总量:     16,109 MB

    虚拟内存: 最大值: 24,301 MB

    虚拟内存: 可用:   8,362 MB

- 软件环境

  - 操作系统: Microsoft Windows 11 家庭中文版

  - PostgreSQL 和 openGauss 都是拉的老师放的镜像

  - Java 版本: 17.0.12

    

#### 3.实验结构

#####  1.插入\查询（索引）等性能对比

- 数据插入测试

  - 生成并插入 10^6 行随机数据
  - 生成并插入 10^7 行随机数据

- 复杂查询测试

  并查看查询的PLAN

- 增加B-tree 索引，并测试其索引性能

##### 2.安全性与可靠性

- ACID 特性测试
  - 原子性 (Atomicity)
  - 一致性 (Consistency)
  - 持久性 (Durability)
  - 隔离性 (Isolation)

详细代码见console_gauss，console_gauss1，console_posgre

##### 3. 并发控制与事务处理

我只做了比较简单的测试吞吐量，并且我发现处理事务本身的效率对吞吐量的影响不是线性的，所以我让事务是

```sql
SELECT 1;
```

来避免对实验结果的影响。

实际上我先尝试了使用python来模拟多线程访问，但是我的py可能配置有问题，我总是下载不了数据库连接相关的包。

后面我只好使用java多线程模拟并发操作了，但是考虑到JAVA本身运行时间较长的原因，不能排除使用java会使结果偏差较大。

详细代码见OpenGaussConcurrencyTest.java，PostgreSQLConcurrencyTest.java

注意Java如果要连接数据库要先在`pom.xml`中添加以下依赖：

```java
<dependency>
    <groupId>org.postgresql</groupId>
    <artifactId>postgresql</artifactId>
    <version>42.6.0</version>
</dependency>
```



#### 4.参考资料

- PostgreSQL 官方文档: [PostgreSQL: Documentation](https://www.postgresql.org/docs/)

- openGauss 官方文档: [openGauss 技术架构.pptx](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Flearningvideo.obs.ap-southeast-1.myhuaweicloud.com%2FopenGauss%20%E6%8A%80%E6%9C%AF%E6%9E%B6%E6%9E%84.pptx&wdOrigin=BROWSELINK)

  



#### 



