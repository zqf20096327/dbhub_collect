# 引言
本文向大家介绍最近参加 TiDB Hackathon 的一个赛题，如何让TiDB在云上更智能的运维。
# TiDB Hackathon RFC
Make TiDB on cloud more native and nb native .
# 作者
- [mikechengwei](https://github.com/mikechengwei) ，TiDB Operator Committer/Prometheus Operator Contributor.
- [caohe](https://github.com/caohe) ，现就职于字节，云原生爱好者。
- [devenzhou](https://github.com/devenzhou) ，现就职于同程，大数据资源组研发负责人。
- [tomatopunk](https://github.com/tomatopunk) ，现就职于同程，云原生爱好者。

# 项目介绍
解决当前TiDB在云上云原生方式运维的局限性，为TiDB在云上提供云原生场景下智能化运维手段，让TiDB在云上自动化运维的同时，也能智能的说话。

# 背景
当前 TiDB 基于 TiDB Operator 部署在 Kubernetes 上，基于云原生 StateFulSet Workload 部署和运行。基于此当前运维和管理有很多局限性，运维不够智能化，没有可观测性的界面了解云上集群状态和运维动作。
我们希望提供一个云上智能化运维解决方案,解决以下问题:
- 时刻保证最佳的运维方式变更。当前TiDB云原生实例更新策略采用Partition倒序更新的方式，没有考虑集群节点当前状态。存在PD节点类型leader迁移两次；TiKV倒序更新节点可能会让集群陷入一个更糟糕的情况，比如TiKV-0因资源问题Crash，应该优先处理TiKV-0节点。
- 解决异构集群的分区运维问题。当前异构集群是通过启动两个不同规格的TiDB负载组合成一个TiDB集群，虽然它们本身是一个集群，但是运维更新没有统一。  
- 让云上TiDB自动化运维的同时能够说话，为用户解决 Operator 自动化运维黑盒问题。当前云原生部署TiDB,没有一个可观测性的视图，查看当前集群状态和云上运维事件变更的信息。

# 项目设计
## 实现方式列举
云上智能化运维的前提是运维更新的策略可以自定义。TiDB采用`Statefulset`部署，要想做到自定义运维有两种改造方式:

1. 类似于 [ES 云原生项目](https://github.com/elastic/cloud-on-k8s),保留 `Statefulset` 的存储功能，基于`OnDelete` 的Update Policy，自定义一套运维更新策略。
2. `TiDB Workload` 直接管理Pod，我们不仅支持自定义运维更新策略，也可以将更多的功能集成进来，比如指定上下线节点的功能，原地升级等等功能。
   之前TiDB Operator 有很多尝试，我们自定义了一套 `AdvanceStatefulSet` 支持指定上下线功能，尝试集成 `OpenKruise` 框架支持原地升级功能，最终我们发现这些尝试都在加重 `TiDB Operator` 的复杂度。所以与其捆绑一堆项目，不如自研一个符合 TiDB 场景的 基础 CRD。

我们当前倾向于后者，将重构做到极致。

## 功能设计
基于上面第二种选择，我们需要通过 `TiDB` 直接管理 Pod。Workload 中需要实现已下功能:

1. StatefulSet 的 `volumeClaimTemplates` 功能。
2. StatefulSet 固定的 PodName 序号规则。   
3. Pod 自定义运维更新策略。
4. TiDB Workload 支持指定上下线节点。
5. 支持 Pod 的原地升级。

这里最难的就是要将管理 StatefulSet 的逻辑平滑切换到管理 Pod，这一点改动最大，也是最复杂的地方，需要考虑前后兼容性，之前 `TiDB Operator` 将 `TiDBMonitor` 从 `Deployment` 平滑迁移到 `Statefulset` 就遇到类似的问题。 

![平滑迁移](https://github.com/NbNative/RFC/blob/main/img/upgrade.png)

可观测性需要实现以下功能:

1. 制定标准的运维Event事件消息格式，采集事件消息。
2. 集群实时状态信息的开发。
3. Operator 运维事件消息和集群状态的联动设计。

![项目架构图](https://github.com/NbNative/RFC/blob/main/img/backend.png)

# 小结
我们会发现可观测性的概念也越来越火，因为我们在想方设法的找出分布式系统上云后的问题和Bug，这是一种被动的方式。
基础研发们利用 Kubernetes Operator 将复杂的分布式系统搬到云上之后确实带来了很多不确定性和复杂度，从外部黑盒的角度来验证和测试这些组件的稳定性是手段之一。但是我觉得我们更应该主动出击，做更适合存储类型的云原生载体。

