# 测试方法

## 测试环境
压力机：AWS EC2     
规格：c5.4xlarge 16vCPU, 32 GiB 
OS：Ubuntu

数据库：TiDB    
Tier Type: Delicated Tier   
Region: Singapore   
TiDB: 1 Node, 4 vCPU, 16 GiB    
TiKV: 3 Nodes, 4 vCPU 16 GiB, 500GiB Storage    







## 测试工具
|工具名称|描述|版本号|
|:-|:-|:-|
|Sysbench|Sysbench是一款基于LuaJIT的，模块化多线程基准测试工具，常用于数据库基准测试。通过内置的数据库测试模型，采用多线程并发操作来评估数据库的性能.|1.0.18


## EC2 sysbench 环境安装
```shell
wget https://codeload.github.com/akopytov/sysbench/zip/refs/tags/1.0.18
apt-get update
sudo apt install -y autoconf libtool vim unzip mysql-server pkg-config libmysqlclient-dev make
unzip 1.0.18
cd sysbench-1.0.18
./autogen.sh
./configure
sudo make -j
sudo make install
```

## 测试步骤
### 须知
请根据实际信息，替换线程并发数、连接IP、连接端口、用户名称与用户密码。

性能测试数据（包含SQL语句）都由sysbench工具自动生成。

压测机ECS与实例在同一可用区。

为了使sysbench 在大并发场景(512, 1000)正常运行，需要将参数 max_prepared_stmt_count 调大，建议改为 1048576（过多的prepare语句会占用大量内存空间进而导致OOM，4U16G规格该值建议设置为400000）。

为了提升sysbench压测的性能，建议检查以下参数并修改(以下参数修改并不影响产品功能及可靠性)并重启实例。

log_bin: OFF    


```shell
#user默认root 端口默认4000 hostname相应替换
mysql -u root -P 4000 -h <your host> -p -e "create database sbtest"

mysql -u root -P 4000 -h <your host> -p -e "show global variables like 'max_prepared_stmt_count'"

mysql -u root -P 4000 -h <your host> -p -e "set global max_prepared_stmt_count=1048576"

mysql -u root -P 4000 -h <your host> -p -e "show global variables like '%log%bin%'"
#检查log bin是否关闭

mysql -u root -P 4000 -h <your host> -p -e "set global log_bin=OFF"

mysql -u root -P 4000 -h <your host> -p -e "set global sql_log_bin=OFF"
```

## 压测指令（可用以下脚本生成）
```python
#用来生成压测指令的脚本：
host='your host' #替换
port=4000 #TiDB默认4000端口
user='root'
password='password of TiDB' #替换，TiDB的密码在创建Cluster之后要去Security选项里面先设置才有，默认是没有密码且不可用密码登录的
thread_num=128 #线程数，替换

def prepare():
    return f'sysbench --db-driver=mysql --mysql-host={host} --mysql-port={port} --mysql-user={user} --mysql-password={password} --mysql-db=sbtest --table_size=25000 --tables=250 --threads={thread_num} oltp_common prepare'

def write_only(): #只写
    return f'sysbench --db-driver=mysql --mysql-host={host} --mysql-port={port} --mysql-user={user} --mysql-password={password} --mysql-db=sbtest --table_size=25000 --tables=250 --time=600 --threads={thread_num} --percentile=95 --report-interval=1 oltp_write_only run'

def read_only(): #只读
    return f'sysbench --db-driver=mysql --mysql-host={host} --mysql-port={port} --mysql-user={user} --mysql-password={password} --mysql-db=sbtest --table_size=25000 --tables=250 --time=600 --range_selects=0 --skip-trx=1 --threads={thread_num} --percentile=95 --report-interval=1 oltp_read_only run'

def read_write(): #读写
    return f'sysbench --db-driver=mysql --mysql-host={host} --mysql-port={port} --mysql-user={user} --mysql-password={password} --mysql-db=sbtest --table_size=25000 --tables=250 --time=600 --threads={thread_num} --percentile=95 --report-interval=1 oltp_read_write run'

def cleanup():
    return f'sysbench --db-driver=mysql --mysql-host={host} --mysql-port={port} --mysql-user={user} --mysql-password={password} --mysql-db=sbtest --table_size=25000 --tables=250 --threads={thread_num} oltp_common cleanup'


if __name__ == '__main__':
    print(prepare()+'\n')
    print(read_only()+'\n') #替换此处的函数来切换只读，只写和读写
    print(cleanup()+'\n')
```
### 只写性能测试
导入数据。执行以下命令，创建测试数据库“sbtest”。    
```shell
mysql -u<user>-P <port> -h <host> -p -e "create database sbtest"
```

执行以下命令，将测试背景数据导入至“sbtest”数据库。  
```shell
sysbench --db-driver=mysql --mysql-host=<host> --mysql-port=<port> --mysql-user=<user> --mysql-password=<password> --mysql-db=sbtest --table_size=25000 --tables=250 --threads=<thread_num> oltp_common prepare
```

执行以下命令，测试性能。测试过程将持续10分钟。  
```shell
sysbench --db-driver=mysql --mysql-host=<host> --mysql-port=<port> --mysql-user=<user> --mysql-password=<password> --mysql-db=sbtest --table_size=25000 --tables=250 --time=600 --threads=<thread_num> --percentile=95 --report-interval=1 oltp_write_only run
```

执行以下命令，清理数据。    
```shell
sysbench --db-driver=mysql --mysql-host=<host> --mysql-port=<port> --mysql-user=<user> --mysql-password=<password> --mysql-db=sbtest --table_size=25000 --tables=250 --threads=<thread_num> oltp_common cleanup
```
### 只读性能测试
导入数据。执行以下命令，创建测试数据库“sbtest”。    
```shell
mysql -u<user> -P<port> -h<host> -p -e "create database sbtest"
```

执行以下命令，将测试背景数据导入至“sbtest”数据库。  
```shell
sysbench --db-driver=mysql --mysql-host=<host> --mysql-port=<port> --mysql-user=<user> --mysql-password=<password> --mysql-db=sbtest --table_size=25000 --tables=250 --threads=<thread_num> oltp_common prepare
```

执行以下命令，测试纯读性能，测试过程将持续10分钟。  
```shell
sysbench --db-driver=mysql --mysql-host=<host> --mysql-port=<port> --mysql-user=<user> --mysql-password=<password> --mysql-db=sbtest --table_size=25000 --tables=250 --time=600 --range_selects=0 --skip-trx=1 --threads=<thread_num> --percentile=95 --report-interval=1 oltp_read_only run
```

执行以下命令，清理数据。    
```shell
sysbench --db-driver=mysql --mysql-host=<host> --mysql-port=<port> --mysql-user=<user> --mysql-password=<password> --mysql-db=sbtest --table_size=25000 --tables=250 --threads=<thread_num> oltp_common cleanup
```

### 读写混合性能测试
导入数据。执行以下命令，创建测试数据库“sbtest”。    
```shell
mysql -u<user> -P<port> -h <host> -p -e "create database sbtest"
```

执行以下命令，将测试背景数据导入至“sbtest”数据库。  
```shell
sysbench --db-driver=mysql --mysql-host=<host> --mysql-port=<port> --mysql-user=<user> --mysql-password=<password> --mysql-db=sbtest --table_size=250000 --tables=25 --threads=<thread_num> oltp_common prepare
```
执行以下命令，测试读写混合性能，测试过程将持续10分钟。  
```shell
sysbench --db-driver=mysql --mysql-host=<host> --mysql-port=<port> --mysql-user=<user> --mysql-password=<password> --mysql-db=sbtest --table_size=250000 --tables=25 --time=600 --threads=<thread_num> --percentile=95 --report-interval=1 oltp_read_write run
```

执行以下命令，清理数据。    
```shell
sysbench --db-driver=mysql --mysql-host=<host> --mysql-port=<port> --mysql-user=<user> --mysql-password=<password> --mysql-db=sbtest --table_size=250000 --tables=25 --threads=<thread_num> oltp_common cleanup
```


## 测试指标
TPS：Transaction Per Second，数据库每秒执⾏的事务数。   
QPS：Query Per Second，数据库每秒执⾏的SQL语句数，包含insert、select、update、delete等。

注：ECS测试GaussDB部分参考华为云白皮书：https://support.huaweicloud.com/intl/zh-cn/pwp-gaussdb/gaussdb_pwp_0002.html
## 测试结果参考
![avatar](image.png)
使用AWS的EC2作为压力机来测试时，当线程过大时，prepare指令报错如图：
![avatar](EC2-TiDB-error.png)
使用华为云的ECS作为压力机来测试时，连接TiDB，当线程过大时，prepare指令报错如图：
![avatar](ECS-TiDB-error.png)
