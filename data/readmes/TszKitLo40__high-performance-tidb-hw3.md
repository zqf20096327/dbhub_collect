# High Performance Tidb hw3
## Deployment
The experiment is conducted with Tencent cloud cvm, the deployment is listed in the following form.
|component       |hardware                       |number                        
|----------------|-------------------------------|-----------------------------|
|tidb            |8core, 16G SAS                 |1                            |
|pd.             |8core, 16G SAS                 |1 (deployed with tidb server)                       |
|tikv            |8core, 32G SSD                 |3                            |

## Workload
32 tables in the database, 1000000 records in each tables.
![workload](https://github.com/TszKitLo40/high-performance-tidb-hw3/blob/master/workload.png)

## Tikv flame graph
![flame](https://github.com/TszKitLo40/high-performance-tidb-hw3/blob/master/flame.png)

The io block of _sendmsg is high. Maybe something can be done on it.

Issue link
[https://github.com/tikv/tikv/issues/8547](https://github.com/tikv/tikv/issues/8547)
