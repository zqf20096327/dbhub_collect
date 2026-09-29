# tidb-code-reading
Note for understanding tidb code, include pd, tikv, tidb,tidb-dashboard





# pd

## main
pd/cmd/pd-server/main.go

传入一些serverBuilder用于提供api服务
创建server，调用server.run


## etcd start
pd/server/server.go
根据etcd的cfg把etcd创建好，更新集群的member成员信息，把创建好的etcd赋值给server的member成员，server的client也被创建好


## server start
pd/server/server.go

startServer initClusterID  从etcd存储里面读出clusterID  （此时etcd客户端已经有了？！）

startServer  --->  kv.NewEtcdKVBase  底层调用了连接etcd的客户端进行kv的一些操作 生成kvBase
            ---->  core.NewRegionStorage  使用levelDb读本地path的文件 生成regionStorage
            利用kvBase和regionStorage 生成server的成员storage


最后标记server started


## server 是怎么提供服务的
pd/server/api/server.go
createRouter--->newXXXHandler(service, render)  render用于帮助方便得写入json,xml,bytes,html等信息
createRouter会在创建server的时候被调用（serviceBuilder--->api.NewHandler---> createRouter）


## region api 相关操作
pd/server/api/region.go

pd-ctl提供了可以操作region的api



## etcd 底层支持的操作

包含的操作：
1. Load
2. LoadRange
3. Save
4. Remove
5. SlowLogTxn(mini事务)

