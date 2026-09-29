# High Performance Tidb hw2
## Deployment
![deployment](https://github.com/TszKitLo40/high-performance-tidb-hw2/blob/master/deployment.png)
The experiment is conducted with Tencent cloud cvm, the deployment is listed in the following form.
|component       |hardware                       |number                        
|----------------|-------------------------------|-----------------------------|
|tidb            |8core, 16G SAS                 |1                            |
|pd.             |8core, 16G SAS                 |1 (deployed with tidb server)                       |
|tikv            |8core, 32G SSD                 |3                            |
I just use the default config of to run the tidb cluster with the tiup tool.

## Experiment
### sysbench
#### point select
QPS is around 6k.
![Result](https://github.com/TszKitLo40/high-performance-tidb-hw2/blob/master/sysbench/point_select/sysbench_point_select.png)
![qps](https://github.com/TszKitLo40/high-performance-tidb-hw2/blob/master/sysbench/point_select/sysbench_point_select_qps.png)
![latency](https://github.com/TszKitLo40/high-performance-tidb-hw2/blob/master/sysbench/point_select/sysbench_latency.png)
![cpu](https://github.com/TszKitLo40/high-performance-tidb-hw2/blob/master/sysbench/point_select/tikv_cpu_point_select_sysbench.png)
![tikv qps](https://github.com/TszKitLo40/high-performance-tidb-hw2/blob/master/sysbench/point_select/tikv_point_select_qps_sysbench.png)
![grpc](https://github.com/TszKitLo40/high-performance-tidb-hw2/blob/master/sysbench/point_select/grpc_point_select.png)

#### update index
QPS is around 2.5k
![result](https://github.com/TszKitLo40/high-performance-tidb-hw2/blob/master/sysbench/update_index/update_index.png)
![qps](https://github.com/TszKitLo40/high-performance-tidb-hw2/blob/master/sysbench/update_index/qps.png)
![tidb latency](https://github.com/TszKitLo40/high-performance-tidb-hw2/blob/master/sysbench/update_index/latency.png)
![tikv cpu](https://github.com/TszKitLo40/high-performance-tidb-hw2/blob/master/sysbench/update_index/cpu.png)
![tikv qps](https://github.com/TszKitLo40/high-performance-tidb-hw2/blob/master/sysbench/update_index/tikv_qps.png)
![grpc](https://github.com/TszKitLo40/high-performance-tidb-hw2/blob/master/sysbench/update_index/grpc.png)
#### read only
QPS is around 20k
![result](https://github.com/TszKitLo40/high-performance-tidb-hw2/blob/master/sysbench/read_only/read_only.png)
![qps](https://github.com/TszKitLo40/high-performance-tidb-hw2/blob/master/sysbench/read_only/qps.png)
![latency](https://github.com/TszKitLo40/high-performance-tidb-hw2/blob/master/sysbench/read_only/latency.png)
![cpu](https://github.com/TszKitLo40/high-performance-tidb-hw2/blob/master/sysbench/read_only/cpu.png)
![tikv](https://github.com/TszKitLo40/high-performance-tidb-hw2/blob/master/sysbench/read_only/tikv_qps.png)
![grpc](https://github.com/TszKitLo40/high-performance-tidb-hw2/blob/master/sysbench/read_only/grpc.png)
### ycsb
QPS is around 50k
![ycsb](https://github.com/TszKitLo40/high-performance-tidb-hw2/blob/master/ycsb/ycsb.png)
![qps](https://github.com/TszKitLo40/high-performance-tidb-hw2/blob/master/ycsb/qps.png)
![latency](https://github.com/TszKitLo40/high-performance-tidb-hw2/blob/master/ycsb/latency.png)
![cpu](https://github.com/TszKitLo40/high-performance-tidb-hw2/blob/master/ycsb/cpu.png)
![tikv](https://github.com/TszKitLo40/high-performance-tidb-hw2/blob/master/ycsb/tikv_qps.png)
![grpc](https://github.com/TszKitLo40/high-performance-tidb-hw2/blob/master/ycsb/grpc.png)
### tpcc
![tpcc](https://github.com/TszKitLo40/high-performance-tidb-hw2/blob/master/tpc/tpcc/tpcc.png)
### tpch
![tpch](https://github.com/TszKitLo40/high-performance-tidb-hw2/blob/master/tpc/tpch/tpch)

## Bottleneck
I think the bottleneck should be in tikv. The cpu usage is not very high in tikv.

