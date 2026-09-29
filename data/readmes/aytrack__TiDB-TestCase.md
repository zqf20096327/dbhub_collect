# TiDB-TestCase
学习TiDB，编写相关测试用例

根据自己学习理解，将PD功能点分为以下5类：
- PD集群管理
- 调度
- 元数据管理
- config
- namespace管理

## 各模块介绍

### PD集群管理
Placement Driver (简称 PD) 是整个集群的管理模块，是一个集群，通过 Raft 协议保持数据的一致性，内部集成etcd。此部分主要用于验证PD集群上各节点的管理及PD Server配置信息。

### 调度
region是调度的基本单元，此部分PD通过创建scheduler来生成operator，对tikv上的region产生影响。

### 元数据管理
PD是无状态的，所有相关TiKV的数据都是TiKV自己上报，PD进行相关的记录。此处主要验证PD对上报数据的处理与查询。

### config
PD集群运行中全局或者namespace相关配置，影响scheduler等触发条件。

### namespace管理
namespace相关操作，影响TiKV数据的调度。


## 已完成
- PD集群管理
- 调度

## TODO
- 元数据管理
- config
- namespace管理