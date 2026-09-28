# Flink 学习

麻烦路过的各位亲给这个项目点个 star，太不易了，写了这么多，算是对我坚持下来的一种鼓励吧！另外特别感谢 [JetBrains](https://jb.gg/OpenSourceSupport) 公司提供的免费全家桶工具，🙏🙏🙏！

![](http://zhisheng-blog.oss-cn-hangzhou.aliyuncs.com/img/2019-05-25-124027.jpg)

## Stargazers over time

![Stargazers over time](https://starchart.cc/zhisheng17/flink-learning.svg)

## 本项目结构

![](http://zhisheng-blog.oss-cn-hangzhou.aliyuncs.com/2020-01-11-064410.png)


## How to build

Maybe your Maven conf file `settings.xml` mirrors can add aliyun central mirror :

```xml
<mirror>
  <id>alimaven</id>
  <mirrorOf>central</mirrorOf>
  <name>aliyun maven</name>
  <url>https://maven.aliyun.com/repository/central</url>
</mirror>
```

then you can run the following command :

```
mvn clean package -Dmaven.test.skip=true
```

you can see following result if build success.

![](http://zhisheng-blog.oss-cn-hangzhou.aliyuncs.com/img/2019-09-27-121923.jpg)

## Flink 系统专栏

基于 Flink 1.9 讲解的专栏，涉及入门、概念、原理、实战、性能调优、系统案例的讲解。扫码下面专栏二维码可以订阅该专栏

![](http://zhisheng-blog.oss-cn-hangzhou.aliyuncs.com/img/2019-11-05-044731.jpg)

首发地址：[http://www.54tianzhisheng.cn/2019/11/15/flink-in-action/](http://www.54tianzhisheng.cn/2019/11/15/flink-in-action/)

专栏地址：[https://gitbook.cn/gitchat/column/5dad4a20669f843a1a37cb4f](https://gitbook.cn/gitchat/column/5dad4a20669f843a1a37cb4f)



## Change

**2022/02/26** 将自己 《Flink 实战与性能优化》专栏放在 GitHub，参见 books 目录

**2021/12/18** 将该项目的 Flink 版本升级至 1.14.2，如果有需要可以去老的分支查看。

**2021/08/15** 将该项目的 Flink 版本升级至 1.13.2，API 发生重大改变，所以代码结构也做了相应的调整（部分代码在 master 分支已经删除，同时将之前的代码切到 [feature/flink-1.10.0](https://github.com/zhisheng17/flink-learning/tree/feature/flink-1.10.0) 上了，如果有需要可以去老的分支查看）。

**2020/02/16** 将该项目的 Flink 版本升级至 1.10，该版本代码都是经过测试成功运行的，尽量以该版本作为参考，如果代码在你们集群测试不成功，麻烦检查 Flink 版本是否一致，或者是否有包冲突问题。 

**2019/09/06** 将该项目的 Flink 版本升级到 1.9.0，有一些变动，Flink 1.8.0 版本的代码经群里讨论保存在分支 [feature/flink-1.8.0](https://github.com/zhisheng17/flink-learning/tree/feature/flink-1.8.0) 以便部分同学需要。

**2019/06/08** 四本 Flink 书籍：

+ [Introduction_to_Apache_Flink_book.pdf]()    这本书比较薄，处于介绍阶段，国内有这本的翻译书籍

+ [Learning Apache Flink.pdf]()    这本书比较基础，初学的话可以多看看

+ [Stream Processing with Apache Flink.pdf]()    这本书是 Flink PMC 写的

+ [Streaming System.pdf]()  这本书评价不是一般的高

**2019/06/09** 新增流处理引擎相关的 Paper，在 paper 目录下：

+ [流处理引擎相关的 Paper](./paper/paper.md)

**【提示】**：关于书籍的下载，因版权问题，不方便提供，所以已经删除，需要的话可以切换到老分支去下载。

## 博客

1、[Flink 从0到1学习 —— Apache Flink 介绍](http://www.54tianzhisheng.cn/2018/10/13/flink-introduction/)

2、[Flink 从0到1学习 —— Mac 上搭建 Flink 1.6.0 环境并构建运行简单程序入门](http://www.54tianzhisheng.cn/2018/09/18/flink-install)

3、[Flink 从0到1学习 —— Flink 配置文件详解](http://www.54tianzhisheng.cn/2018/10/27/flink-config/)

4、[Flink 从0到1学习 —— Data Source 介绍](http://www.54tianzhisheng.cn/2018/10/28/flink-sources/)

5、[Flink 从0到1学习 —— 如何自定义 Data Source ？](http://www.54tianzhisheng.cn/2018/10/30/flink-create-source/)

6、[Flink 从0到1学习 —— Data Sink 介绍](http://www.54tianzhisheng.cn/2018/10/29/flink-sink/)

7、[Flink 从0到1学习 —— 如何自定义 Data Sink ？](http://www.54tianzhisheng.cn/2018/10/31/flink-create-sink/)

8、[Flink 从0到1学习 —— Flink Data transformation(转换)](http://www.54tianzhisheng.cn/2018/11/04/Flink-Data-transformation/)

9、[Flink 从0到1学习 —— 介绍 Flink 中的 Stream Windows](http://www.54tianzhisheng.cn/2018/12/08/Flink-Stream-Windows/)

10、[Flink 从0到1学习 —— Flink 中的几种 Time 详解](http://www.54tianzhisheng.cn/2018/12/11/Flink-time/)

11、[Flink 从0到1学习 —— Flink 读取 Kafka 数据写入到 ElasticSearch](http://www.54tianzhisheng.cn/2018/12/30/Flink-ElasticSearch-Sink/)

12、[Flink 从0到1学习 —— Flink 项目如何运行？](http://www.54tianzhisheng.cn/2019/01/05/Flink-run/)

13、[Flink 从0到1学习 —— Flink 读取 Kafka 数据写入到 Kafka](http://www.54tianzhisheng.cn/2019/01/06/Flink-Kafka-sink/)

14、[Flink 从0到1学习 —— Flink JobManager 高可用性配置](http://www.54tianzhisheng.cn/2019/01/13/Flink-JobManager-High-availability/)

15、[Flink 从0到1学习 —— Flink parallelism 和 Slot 介绍](http://www.54tianzhisheng.cn/2019/01/14/Flink-parallelism-slot/)

16、[Flink 从0到1学习 —— Flink 读取 Kafka 数据批量写入到 MySQL](http://www.54tianzhisheng.cn/2019/01/15/Flink

[...截断...]

-MySQL-sink/)

17、[Flink 从0到1学习 —— Flink 读取 Kafka 数据写入到 RabbitMQ](https://t.zsxq.com/uVbi2nq)

18、[Flink 从0到1学习 —— Flink 读取 Kafka 数据写入到 HBase](https://t.zsxq.com/zV7MnuJ)

19、[Flink 从0到1学习 —— Flink 读取 Kafka 数据写入到 HDFS](https://t.zsxq.com/zV7MnuJ)

20、[Flink 从0到1学习 —— Flink 读取 Kafka 数据写入到 Redis](https://t.zsxq.com/zV7MnuJ)

21、[Flink 从0到1学习 —— Flink 读取 Kafka 数据写入到 Cassandra](https://t.zsxq.com/uVbi2nq)

22、[Flink 从0到1学习 —— Flink 读取 Kafka 数据写入到 Flume](https://t.zsxq.com/zV7MnuJ)

23、[Flink 从0到1学习 —— Flink 读取 Kafka 数据写入到 InfluxDB](https://t.zsxq.com/zV7MnuJ)

24、[Flink 从0到1学习 —— Flink 读取 Kafka 数据写入到 RocketMQ](https://t.zsxq.com/zV7MnuJ)

25、[Flink 从0到1学习 —— 你上传的 jar 包藏到哪里去了](https://t.zsxq.com/uniY7mm)

26、[Flink 从0到1学习 —— 你的 Flink job 日志跑到哪里去了](https://t.zsxq.com/zV7MnuJ)


### Flink 源码项目结构

![](./pics/Flink-code.png)


## 学习资料

另外我自己整理了些 Flink 的学习资料，目前已经全部放到微信公众号了。
你可以加我的微信：**yuanblog_tzs**，然后回复关键字：**Flink** 即可无条件获取到，转载请联系本人获取授权，违者必究。

![](http://zhisheng-blog.oss-cn-hangzhou.aliyuncs.com/img/2019-09-17-143454.jpg)

更多私密资料请加入知识星球！

![](http://zhisheng-blog.oss-cn-hangzhou.aliyuncs.com/img/2019-07-23-124320.jpg)

有人要问知识星球里面更新什么内容？值得加入吗？

目前知识星球内已更新的系列文章：

### 大数据重磅炸弹

1、[《大数据重磅炸弹——实时计算引擎 Flink》开篇词](https://t.zsxq.com/fqfuVRR​)

2、[你公司到底需不需要引入实时计算引擎？](https://t.zsxq.com/emMBaQN​)

3、[一文让你彻底了解大数据实时计算框架 Flink](https://t.zsxq.com/eM3ZRf2) ​

4、[别再傻傻的分不清大数据框架Flink、Blink、Spark Streaming、Structured Streaming和Storm之间的区别了](https://t.zsxq.com/eAyRz7Y)​

5、[Flink 环境准备看这一篇就够了](https://t.zsxq.com/iaMJAe6​)  

6、[一文讲解从 Flink 环境安装到源码编译运行](https://t.zsxq.com/iaMJAe6​)

7、[通过 WordCount 程序教你快速入门上手 Flink](https://t.zsxq.com/eaIIiAm)  ​

8、[Flink 如何处理 Socket 数据及分析实现过程](https://t.zsxq.com/Vnq72jY​)  

9、[Flink job 如何在 Standalone、YARN、Mesos、K8S 上部署运行？](https://t.zsxq.com/BiyvFUZ​)

10、[Flink 数据转换必须熟悉的算子（Operator）](https://t.zsxq.com/fufUBiA)

11、[Flink 中 Processing Time、Event Time、Ingestion Time 对比及其使用场景分析](https://t.zsxq.com/r7aYB2V) 

12、[如何使用 Flink Window 及 Window 基本概念与实现原理](https://t.zsxq.com/byZbyrb)

13、[如何使用 DataStream API 来处理数据？](https://t.zsxq.com/VzNBi2r)

14、[Flink WaterMark 详解及结合 WaterMark 处理延迟数据](https://t.zsxq.com/Iub6IQf)

15、[基于 Apache Flink 的监控告警系统](https://t.zsxq.com/MniUnqb)

16、[数据仓库、数据库的对比介绍与实时数仓案例分享](https://t.zsxq.com/v7QzNZ3)

17、[使用 Prometheus Grafana 监控 Flink](https://t.zsxq.com/uRN3VfA)


### 源码系列

1、[Flink 源码解析 —— 源码编译运行](https://t.zsxq.com/UZfaYfE)

2、[Flink 源码解析 —— 项目结构一览](https://t.zsxq.com/zZZjaYf)

3、[Flink 源码解析—— local 模式启动流程](https://t.zsxq.com/zV7MnuJ)

4、[Flink 源码解析 —— standalonesession 模式启动流程](https://t.zsxq.com/QZVRZJA)

5、[Flink 源码解析 —— Standalone Session Cluster 启动流程深度分析之 Job Manager 启动](https://t.zsxq.com/u3fayvf)

6、[Flink 源码解析 —— Standalone Session Cluster 启动流程深度分析之 Task Manager 启动](https://t.zsxq.com/MnQRByb)

7、[Flink 源码解析 —— 分析 Batch WordCount 程序的执行过程](https://t.zsxq.com/YJ2Zrfi)

8、[Flink 源码解析 —— 分析 Streaming WordCount 程序的执行过程](https://t.zsxq.com/qnMFEUJ)

9、[Flink 源码解析 —— 如何获取 JobGraph？](https://t.zsxq.com/naaMf6y)

10、[Flink 源码解析 —— 如何获取 StreamGraph？](https://t.zsxq.com/qRFIm6I)

11、[Flink 源码解析 —— Flink JobManager 有什么作用？](https://t.zsxq.com/2VRrbuf)

12、[Flink 源码解析 —— Flink TaskManager 有什么作用？](https://t.zsxq.com/RZbu7yN)

13、[Flink 源码解析 —— JobManager 处理 SubmitJob 的过程](https://t.zsxq.com/zV7MnuJ)

14、[Flink 源码解析 —— TaskManager 处理 SubmitJob 的过程](https://t.zsxq.com/zV7MnuJ)

15、[Flink 源码解析 —— 深度解析 Flink Checkpoint 机制](https://t.zsxq.com/ynQNbeM)

16、[Flink 源码解析 —— 深度解析 Flink 序列化机制](https://t.zsxq.com/JaQfeMf)

17、[Flink 源码解析 —— 深度解析 Flink 是如何管理好内存的？](https://t.zsxq.com/zjQvjeM)

18、[Flink Metrics 源码解析 —— Flink-metrics-core](https://t.zsxq.com/Mnm2nI6)

19、[Flink Metrics 源码解析 —— Flink-metrics-datadog](https://t.zsxq.com/Mnm2nI6)

20、[Flink Metrics 源码解析 —— Flink-metrics-dropwizard](https://t.zsxq.com/Mnm2nI6)

21、[Flink Metrics 源码解析 —— Flink-metrics-graphite](https://t.zsxq.com/Mnm2nI6)

22、[Flink Metrics 源码解析 —— Flink-metrics-influxdb](https://t.zsxq.com/Mnm2nI6)

23、[Flink Metrics 源码解析 —— Flink-metrics-j