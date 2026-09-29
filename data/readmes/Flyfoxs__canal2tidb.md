# 一键启动
./main.sh

# 验证结果

```shell script
#在主库插入数据
mysql -h 127.0.0.1 -u root -proot -P 3306 -e "INSERT INTO test_db.test_kafka ( id ,  user_name  ) values (1, 'felix');"

#在从库检查数据
mysql -h 127.0.0.1 -u root -proot -P 3307 -e "select * from test_db.test_kafka"
```

 


# Sync RDB
https://github.com/alibaba/canal/wiki/Sync-RDB

# ClientAdapter
https://github.com/alibaba/canal/wiki/ClientAdapter


# 其他
1. ClientAdapt RDB 无法同步DDL 


# Download
https://github.com/alibaba/canal/releases/download/canal-1.1.4/canal.deployer-1.1.4.tar.gz
https://github.com/alibaba/canal/releases/download/canal-1.1.4/canal.adapter-1.1.4.tar.gz
