# Test-TiKV


### 测试概览
* 通过4台阿里云主机部署没有TiDB的集群，使用go-ycsb对集群进行raw insert测试，同时使用perf监测工具对当前TiKV中的执行进程进行record，然后对perf.data进行分析，并绘制函数调用图、火焰图和timechart图，尽可能全面的对TiKV进行性能分析。
### 测试环境
| 阿里云主机   | 私有ip   | CPU核心数目   | 内存大小   | 硬盘   | 角色   | 网络   | 
|:----|:----|:----|:----|:----|:----|:----|
| node001   | 172.31.197.172   | 8   | 32G   | 40G的SSD系统盘+200G的SSD数据盘   | PD、中控机、go-ycsb   | 1.2g网   | 
| node002   | 172.31.197.173   | 8   | 32G   | 40G的SSD系统盘+200G的SSD数据盘   | TiKV、perf监控   | 1.2g网   | 
| node003   | 172.31.197.175   | 8   | 32G   | 40G的SSD系统盘+200G的SSD数据盘   | TiKV   | 1.2g网   | 
| node004   | 172.31.197.174   | 8   | 32G   | 40G的SSD系统盘+200G的SSD数据盘   | TiKV   | 1.2g网   | 

### 测试内容及结果
* 测试命令：./bin/go-ycsb load tikv -p tikv.pd=172.31.197.172:2379 -p tikv.type=raw -P workloads/workloada
* 其中修改了workloada的记录数，为10W
* 测试流程：
  * 在go-ycsb机子上执行上述命令
  * 在某一台TiKV上得到tikv的pid，并用perf脚本进行record和绘制结果图
* 结果输出：
```
***************** properties *****************
"dotransactions"="false"
"scanproportion"="0"
"insertproportion"="0"
"updateproportion"="0.5"
"requestdistribution"="zipfian"
"recordcount"="100000"
"workload"="core"
"tikv.pd"="172.31.197.172:2379"
"readallfields"="true"
"readproportion"="0.5"
"operationcount"="100000"
"tikv.type"="raw"
**********************************************
INSERT - Takes(s): 10.0, Count: 42991, OPS: 4316.9, Avg(us): 23131, Min(us): 6147, Max(us): 526428, 95th(us): 48000, 99th(us): 72000
INSERT - Takes(s): 20.0, Count: 99892, OPS: 5004.9, Avg(us): 19937, Min(us): 6147, Max(us): 526428, 95th(us): 43000, 99th(us): 63000
Run finished, takes 20.236090571s
INSERT - Takes(s): 20.2, Count: 100000, OPS: 4952.2, Avg(us): 19936, Min(us): 5231, Max(us): 526428, 95th(us): 43000, 99th(us): 63000

```

### 结果分析与改进：
* 测试得到insert的avg吞吐量是4758 OPS，avg延时是21ms
* 测试过程中发现TiKV的CPU利用率在10%左右，内存利用率也很低，只有百分之几，可见go-ycsb对集群的测试并未达到集群的瓶颈。
* 可以通过增加go-ycsb的测试线程来增加压力，还可以增加多态go-ycsb服务器进行测试，尽量是CPU、内存或者是网络达到极限，就可以找到测试情况下集群的瓶颈所在了。
### 对火焰图的分析
![图片](https://github.com/LXC-viso/Test-TiKV/blob/master/img/fire.png)
* 火焰图：就是对函数调用栈的CPU时间的图形化展示。下面的函数调用上面的函数，最上面的调用是程序的瓶颈所在，优化它们可以提高程序性能。
* 从上图可以看到，时间花在了apply_worker、grpc-server-0、raftstore-4这三个调用上了：
  * apply_worker和raftstore-4两个调用中socksdb的write调用占了很多时间，这应该是等待IO耗时造成的。
  * grpc-server-0调用中比较耗时的是start-thread调用，其中调用了grpcio的异步io----poll，和io多路复用epoll；
* 最上面耗时的操作一般是lock和io操作，如_raw_spin_unlock_irqrestore和protobuf::stream::CodedInputStream::read_tag_unpack等顶层调用。如果过多的锁等待io的话，就会使程序的性能下降
### 对timechart图分析
![图片](https://github.com/LXC-viso/Test-TiKV/blob/master/img/timechart1.png)
![图片](https://github.com/LXC-viso/Test-TiKV/blob/master/img/timechart2.png)
* 可以发现，8个CPU核都没充分使用，大多时候都是idle状态。raftstore和jbd2/vdb大多数时间处于等待io状态，CPU抖动和io抖动都比较严重。
### 函数调用图的分析
![图片](https://github.com/LXC-viso/Test-TiKV/blob/master/img/func_call1.png)

![图片](https://github.com/LXC-viso/Test-TiKV/blob/master/img/func_call2.png)
* 这是对这段时间内调用时间的占用分析图，图很大，只贴了一部分，对应火焰图可以发现哪些函数耗时较多。
### 总结
* 通过阿里云服务器对TiKV集群进行了raw insert的测试，发现单台go-ycsb并不能测出TiKV的瓶颈，需要增加线程和测试服务器。同时发现TiKV作为存储层的一些性能瓶颈，主要集中在锁的等待和io上了，CPU并不是其瓶颈。TiKV是负责TiDB存储层的服务，需要保证能提供高性能、高并发、高吞吐的服务，应尽可能地优化。



