# 基于CM模式的openGauss容器化方案设计



# 一、openGauss与CM介绍

openGauss作为一款企业级开源关系型数据库，具有高性能，高可用，高安全，易运维等特点。CM的加入，使openGauss集群在易运维，可靠性等方面进一步提升。CM（Cluster Manager）是一款集群资源管理软件。支持自定义资源监控，提供了数据库主备的状态监控、网络通信故障监控、文件系统故障监控、故障自动主备切换等能力。CM提供了丰富的集群管理能力，如集群、节点、实例级的启停，集群状态查询、选主、主备切换、日志管理等。本方案依托于社区的CM实现openGauss高可用能力，降低Operator直接集群管理的复杂度。



# 二、架构设计

![image-20230912110225056](img/image-20230912110225056.png) 

- openGaussCluster，声明自定义资源对象。Operator监听到create事件后会创建三种类型Pod。
  - openGauss为数据库节点，Primary为数据库主节点，Standby为数据库从节点
  - cms负责数据库选主等工作，pod数量为3
  - openGauss-export采集数据库监控指标，pod数量为1

- Backup-Recovery

  - 备份：在声明备份后，以job方式创建，启动一个客户端，连接需要备份的数据库服务，使用gs_probackup 执行全量物理备份，上传备份文件到备份服务器，输出全过程日志。

  - 恢复：以job方式创建，启动一个客户端，从备份服务器拉去备份文件，使用gs_probackup执行数据恢复，输出全过程日志。
- Fluentd。通过DaemonSet方式部署，调度到openGauss主机上，采集/data盘log日志。

# 三、功能列表

- 集群部署（支持一主多从、固定节点、固定IP）
- 主从切换
- 备份恢复
- 备机重建
- 节点驱逐

- 资源规格扩缩容
- 监控采集
- 日志采集
- 集群维护
- 集群释放  

 

# 四、关键能力实现

## 4.1 固定节点

​	固定节点即当DN节点的pod重新调度时，为保证数据不丢失需使pod调度至之前的宿主机上，主要实现基于调度器延迟调度和PV的节点亲和两个特性。

- 设置storageclass的volume绑定模式为WaitForFirstConsumer。

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
 name:  local-storage-test
provisioner: kubernetes.io/no-provisioner
reclaimPolicy: Delete
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
```

-   待pod调度后与PV绑定，将PV与当前的pod进行绑定，后续pod再次调度时调度器会参考PV所在的节点进行调度。


```yaml
nodeAffinity:
 required:
  nodeSelectorTerms:
  - matchExpressions:
    - key: kubernetes.io/hostname
      operator: In
      values:
      - ly-xjf-r020301-gyt
```

 

## 4.2 固定IP

​	固定IP即pod重启后为保证集群的拓扑关系，重启后的podIP与原来保持一致，主要实现基于calico-ipam固定IP能力，具体如下：

1. 采用calico插件自动分配pod IP
2. 利用operator list-watch 机制，在pod创建成功而后将pod ip回写至对应的pod的annotaions:"cni.projectcalico.org/ipAddrs":"[\"xx.xx.xx.xx\"]"；



## 4.3 备份恢复

​	备份恢复的具体能力是通过制作镜像实现的，对于备份恢复的结果显示主要做了以下内容：

1. 通过job实现单次备份或者单次恢复
2. 当job执行任务结束后，会被Operator监听到。之后Operator会去读取pod日志，根据pod日志的结尾字样来判断任务执行结果，并回显备份恢复的结果。



## 4.4 高可用能力

CM自身高可用能力。

- gauss保活机制。cm_agent每秒检查一次gauss进程，如果不存在拉起进程。如果进程僵死，杀死僵死进程，重新拉起。
- cm_agent保活机制。Om_monitor进程每秒检查一次cm_agent进程状态，如果不存在拉起进程，如果僵死，则杀死僵死进程，重新拉起。
- om_monitor保活机制。执行entrypoint.sh脚本，作为守护进程，每分钟检查一次om_monitor进程的状态，如果不存在，拉起进程，如果僵死，则杀死僵死进程，重新拉起。

CM高可用能力已覆盖大部分故障的场景，但依旧存在问题。

- 如何确保entrypoint.sh脚本的守护进程一直存在。
- Pod被删除后，不能自动恢复。
- Pod所在主机故障或者磁盘使用率超过阈值，集群状态异常，CM无法处理。

针对以上3种容器场景CM无法处理的问题，容器设计层面做出了一些处理。

- 将entrypoint.sh脚本做为主进程，如果entrypoint.sh不存在，则容器会自动重启（设置容器重启策略）。
- Operator监听pod的del事件，如果pod被del，则operator重新拉起pod。
- 对于pod所在主机无法满足的情况，通过节点驱逐功能解决。
- 增加健康探测机制
  - 设置operator的reconcile同步频率。每分钟对operator监听的资源对象进行健康检查并更新ogc.status，如果集群状态为异常，打印warning日志。可以使用组件对Waring日志采集进而触发集群状态异常告警。
  - 设置Readiness探针。Readiness探针会检测gauss进程是否存在，如果不存在，不做任何处理。如果存在，就会查询服务是否为Normal状态，如果不是Normal，则返回异常。Gauss容器添加Readiness探针后，每5秒执行一次，如果返回异常超过3次，则gauss容器状态变为Notready。此时会被operator监听到，并将集群状态标记为异常，打印warning日志。Waring日志会被采集并出发告警。
  - 设置Liveness探针。Liveness探针会检测gauss进程是否存在，如果不存在，则返回异常。对于使用cm_ctl stop的操作，则会跳过检测。Gauss容器添加Liveness探针后，每5秒执行一次，如果返回异常超过3次，则gauss容器会被重启。





# 五、安装

## 5.1 镜像构建

### 5.1.1 Operator镜像

下载operator代码
```markdown
git clone -b dev-20230620 https://gitee.com/youshouldnowme/openGauss-operator
```

生成exe文件
```markdown
set GOARCH=amd64
set GOOS=linux
set GO111MODULE=off
SET CGO_ENABLED=0
go build -a -o opengauss_operator cmd/main.go
```

Dockerfile
```markdown
FROM k8s-deploy/busybox:latest
ADD opengauss_operator /
ADD customConfig /customConfig
RUN chmod 111 opengauss_operator
```


根据Dockerfile，制作operator镜像
```markdown
docker build -t k8s-deploy/opengauss-operator:v5.0.0-20230930
```



### 5.1.2 openGauss镜像

```markdown
git clone -b dev-multidn https://gitee.com/wang-xinyu-7/openGauss-image
```



### 5.1.3 备份恢复镜像

```markdown
git clone -b backup-restore https://gitee.com/wang-xinyu-7/openGauss-image
```



### 5.1.4 openGauss-exporter镜像

```markdown
git clone https://gitee.com/opengauss/openGauss-prometheus-exporter
```



### 5.1.5 fluented镜像

```markdown
git clone https://github.com/fluent/fluentd
```

## 5.2 部署



### 5.2.1 部署CRD

部署ogc
```markdown
kubectl apply -f config\crd\bases\gaussdb.gaussdb.middleware.cmos.cn_opengaussbackuprecoveries.yaml
```

部署ogbr
```markdown
kubectl apply -f config\crd\bases\gaussdb.gaussdb.middleware.cmos.cn_opengaussclusters.yaml
```



### 5.2.2 部署Operator
使用deployment部署operator
```markdown
kubectl apply -f deploy/operator-deployment.yaml
```



### 5.2.3 部署openGauss集群

部署
```markdown
kubectl apply -f config\samples\gaussdb_v1_opengausscluster.yaml
```
查看集群
```markdown
kubectl get opengaussclusters.gaussdb.gaussdb.middleware.cmos.cn
```







 

# 六、使用手册

## 6.1 自定义资源CRD描述

### 6.1.1 openGaussCluster

| 属性名称           | 属性类型               | 属性说明                                                     |
| ------------------ | ---------------------- | ------------------------------------------------------------ |
| Architecture       | string                 | 部署架构。split表示cm与dn分离部署，merge表示cm与dn集成部署（暂不支持） |
| NetworkType        | string                 | 网络类型。overlay/underlay                                   |
| DataNodeNum        | *int32                 | DN节点数量                                                   |
| Maintenance        | bool                   | true：人工维护，false：operator维护                          |
| Images             | ContainerImage         | 镜像组。包含DN镜像、备份恢复镜像、监控采集镜像。             |
| DBResources        | ResourceList           | DN容器资源规格                                               |
| DBStorage          | DBStorageTemplate      | 存储模板                                                     |
| Ports              | *int32                 | 对外服务端口,overlay模式下指的是起始端口                     |
| BackRecovery       | BackRecoverySpec       | 备份恢复信息                                                 |
| Switchover         | SwitchoverMessage      | 主从切换信息                                                 |
| StandbyReconstruct | StandbyReconstructSpec | 备机重建信息                                                 |
| IsInit             | bool                   | 集群状态第一次变为Running后，进行初始化。初始化内容为创建gauss账号密码、权限设置。 |
| InstanceMigration  | InstanceMigrationSpec  | 节点驱逐信息                                                 |

 

### 6.1.2 openGaussBackupRecovery

| 属性名称   | 属性类型 | 属性说明                          |
| ---------- | -------- | --------------------------------- |
| Address    | string   | 备份服务器地址                    |
| Mode       | string   | 备份文件传输方式，目前只支持scp。 |
| Time       | string   | 定时备份时间                      |
| BackupFile | string   | 备份文件名称                      |



## 6.2 集群部署

部署

```
kubectl apply -f zhengxin-test.yaml
```

查看集群状态，当state为Running，表示集群状态正常，同时可以查看各节点信息以及主从关系

```
kubectl get ogc zhengxin-test -oyaml
```

![image-20230911152702794](img/image-20230911152702794.png)

## 6.3 服务对外访问

查看NodePort端口

```markdown
kubectl get service -n cmdb
```

查看pod所在主机IP，通过获取

```
kubectl get pod -n cmdb -owide  

kubectl describe node ${nodeName} | grep IP
```

通过客户端连接数据库服务

![image-20230911152902359](img/image-20230911152902359.png)





## 6.4 主从切换

查看当前主节点

```
kubectl get ogc zhengxin-test -oyaml
```

声明主从切换

```yaml
apiVersion: gaussdb.gaussdb.middleware.cmos.cn/v1
kind: OpenGaussCluster
metadata:
  name: zhengxin-test
  namespace: ${namespace}
spec:
.......
  # 主从切换
  switchover:
    targetMasterPod: zhengxin-test-0
    status: begin
```

查看主从切换结果

```
kubectl get ogc -n cmdb zhengxin-test -oyaml | grep -A 3 switchover
```

登录控制台，查看主从切换是否执行成功

```
kubectl exec -it -n cmdb zhengxin-test-0 bash

su - omm
cm_ctl query -Cv
```



## 6.5 单次备份

声明某个节点进行单次备份

```yaml
apiVersion: gaussdb.gaussdb.middleware.cmos.cn/v1
kind: OpenGaussCluster
metadata:
  name: zhengxin-test
  namespace: ${namespace}
spec:
.......
  backRecovery:
    transfer:
      address: 192.168.29.104
      mode: scp
    backups:
    - podName: zhengxin-test-0
      status: Create
```

查看备份状态详细信息

```
kubectl get ogc -n cmdb  zhengxin-test  -oyaml | grep -A 10 backRecovery
```

查看备份pod日志

```
kubectl logs -f -n cmdb ${podName}
```

备份完成后，登录备份服务器192.168.29.104，查看备份文件

```
ll /data/backups/${fileName}
```



## 6.6 定时备份

声明定时备份

```yaml
apiVersion: gaussdb.gaussdb.middleware.cmos.cn/v1
kind: OpenGaussCluster
metadata:
  name: zhengxin-test
  namespace: ${namespace}
spec:
.......
  backRecovery:
    cronBackupTime: 0 1 * * *
    transfer:
      address: 192.168.29.104
      mode: scp
```

查看定时备份cronjob

```markdown
kubectl get cronjob -n cmdb | grep zhengxin
```

在定时备份触发后，查看定时备份pod

```
kubectl get pod -n cmdb | grep zhengxin | grep cron
```

## 6.7 单次恢复

声明单次恢复

```yaml
apiVersion: gaussdb.gaussdb.middleware.cmos.cn/v1
kind: OpenGaussCluster
metadata:
  name: zhengxin-test
  namespace: ${namespace}
spec:
.......
  backRecovery:
    transfer:
      address: 192.168.29.104
      mode: scp
    recoveries:
    - podName: ${podName}
      backFileName: opengaussbk_xxx/RYLAxx
      status: Create
```

查看恢复状态详细信息

```
kubectl get ogc -n cmdb  zhengxin-test  -oyaml | grep -A 10 backRecovery
```

查看恢复pod日志

```
kubectl logs -f -n cmdb ${podName}
```

查看集群状态

```markdown
kubectl get ogc -n cmdb zhengxin-test -oyaml
```



## 6.8 备机重建

声明备机重建

```yaml
apiVersion: gaussdb.gaussdb.middleware.cmos.cn/v1
kind: OpenGaussCluster
metadata:
  name: opengausscluster-sample
  namespace: ${namespace}
spec:
.......
  standbyReconstruct:
    executeInstance: ${podName}
    problemInstance: ${podName}
    status: create
```

查看备机重建详细信息

```
kubectl get ogc -n cmdb  zhengxin-test -oyaml | grep -A 4 standbyReconstruct
```

当standbyReconstruct.status变为succeed，查看集群状态

```
kubectl get ogc -n cmdb  zhengxin-test -oyaml 
```



## 6.9 节点驱逐

声明节点驱逐

```yaml
apiVersion: gaussdb.gaussdb.middleware.cmos.cn/v1
kind: OpenGaussCluster
metadata:
  name: zhengxin-test
  namespace: ${namespace}
spec:
.......
  instanceMigration:
    instance: ${podName}
    status: create
```

查看节点驱逐详细信息

```
kubectl get ogc -n cmdb  zhengxin-test -oyaml | grep -A 3 instanceMigration
```

当instanceMigration.status变为succeed，查看集群状态，如果pod状态正常但集群状态异常，可以尝试进行备机重建或者单次恢复

```markdown
kubectl get ogc -n cmdb zhengxin-test -oyaml
```



## 6.10 资源规格扩缩容

声明资源规格调整

```yaml
apiVersion: gaussdb.gaussdb.middleware.cmos.cn/v1
kind: OpenGaussCluster
metadata:
  name: zhengxin-test
  namespace: ${namespace}
spec:
.......
  dbResources:
    limits:
      cpu: 5
      memory: 15Gi
    requests:
      cpu: 2
      memory: 2Gi
```

查看pod规格

```
kubectl get pod -n cmdb ${podName} -oyaml | grep -A 6 resources
```

查看集群状态

```markdown
kubectl get ogc -n cmdb zhengxin-test -oyaml
```



## 6.11 监控采集

集群状态正常后，就开始采集数据库监控指标，获取监控采集pod ip

```markdown
kubectl describe pod -n cmdb  zhengxin-test-exporter |  grep IP
```

查看采集指标

```
curl ${ip}:9187/metrics
```



## 6.12 日志采集

查询日志采集pod

```
kubectl get pod -n kube-system | grep fluentd
```

查看日志采集配置

```
kubectl get cm -n kube-system | grep fluentd
```

查看日志采集pod日志

```markdown
kubectl logs -f -n kube-system ${podName}
```

## 6.13 集群维护

集群维护声明

```yaml
apiVersion: gaussdb.gaussdb.middleware.cmos.cn/v1
kind: OpenGaussCluster
metadata:
  name: zhengxin-test
  namespace: ${namespace}
spec:
.......
  maintenance: true
```

此时再去声明主从切换、单次备份等内容，不再进行操作





## 6.14 集群释放

集群释放

```markdown
kubectl delete -f zhengxin-test.yaml
```

查看资源对象，已被删除

```
kubectl get ogc -n cmdb | grep zhengxin-test

kubectl get service -n cmdb  | grep zhengxin-test

kubectl get pvc -n cmdb  | grep zhengxin-test

kubectl get pod -n cmdb | grep zhengxin-test
```

查看持久化数据，数据被清理

```
ll /data/cmdb/zhengxin-test/
```



