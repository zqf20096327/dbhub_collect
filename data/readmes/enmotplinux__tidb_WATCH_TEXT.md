# tidb_WATCH_TEXT

TiDB 拉黑SQL 工具 
支持拉黑 
查看 
解绑
##  环境
go 1.20


TiDB 版本 v7.5+
##  注意

1. 目前只支持 单条SQL  不支持 多条SQL


##  原理


https://docs.pingcap.com/zh/tidb/stable/tidb-resource-control#query-watch-%E8%AF%AD%E5%8F%A5%E8%AF%B4%E6%98%8E


## 使用方法
/*

 解绑：


 go run main.go Unbind --ip "127.0.0.1" --port 4000 --pid 6  id 是查询出来的


查询：


 go run main.go select  --ip "127.0.0.1" --port 4000 

 拉黑：


 go run main.go block  --ip "127.0.0.1" --port 4000  --sql "select * from test.t1" 


 go run main.go block --ip "127.0.0.1" --port 4000 --sql "select * from test.t1 limit 1"   
