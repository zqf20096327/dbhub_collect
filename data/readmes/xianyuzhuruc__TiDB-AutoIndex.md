TiDB可用的[AutoIndex](https://github.com/zhouxh19/autoindex)，将与opengauss交互的语法修改为了tidb可用的语法，TiDB部署文件见`TiDB_deployment`文件夹，采用docker compose部署。

AutoIndex 执行命令：
```bash
python index_advisor_workload.py 34000 tpch --db-host 127.0.0.1 -U root workload.sql --schema tpch  --show-detail
```

