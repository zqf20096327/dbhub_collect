# tidb-High-performance-work
tidb高性能

## 一 work1源码编译部署tidb,并修改源码,在事务开启处打印 hello transaction
### 1先安装go环境和rust环境,参见网上资料
go版本是<br>
![](https://github.com/gaokunnanjing/tidb-High-performance-work/blob/master/work1_images/go%E7%89%88%E6%9C%AC_20200816102905.png)<br>
https://www.rust-lang.org/en-US/other-installers.html<br>
注意选择nightly版本下载安装，
将url中的www.rust-lang.org替换成mirrors.ustc.edu.cn/rust-static会更快<br>
rust版本是<br>
![](https://github.com/gaokunnanjing/tidb-High-performance-work/blob/master/work1_images/rust%E7%89%88%E6%9C%AC_20200816103346.png)<br>

.bashrc 环境变量配置<br>
![](https://github.com/gaokunnanjing/tidb-High-performance-work/blob/master/work1_images/%E7%8E%AF%E5%A2%83%E5%8F%98%E9%87%8F_20200816103913.png)

### 2下载tidb,pd和tikv源代码
git clone https://github.com/tikv/tikv.git<br>
git clone https://github.com/pingcap/pd.git<br>
git clone https://github.com/pingcap/tidb.git<br>
放置在一个单独的文件夹下<br>
![](https://github.com/gaokunnanjing/tidb-High-performance-work/blob/master/work1_images/%E6%BA%90%E7%A0%81%E6%96%87%E4%BB%B6%E5%A4%B9_20200816120706.png)

### 3编译tidb,pd和tikv
进入tidb和pd相应文件夹,里面有Makefile,直接make<br>
tikv需要使用 cargo build<br>
![](https://github.com/gaokunnanjing/tidb-High-performance-work/blob/master/work1_images/%E7%BC%96%E8%AF%91pd_20200816104932.png)<br>
![](https://github.com/gaokunnanjing/tidb-High-performance-work/blob/master/work1_images/%E7%BC%96%E8%AF%91tidb_20200816105123.png)<br>
![](https://github.com/gaokunnanjing/tidb-High-performance-work/blob/master/work1_images/%E7%BC%96%E8%AF%91tikv_20200816105251.png)<br>
中间遇到一个问题<br>
![](https://github.com/gaokunnanjing/tidb-High-performance-work/blob/master/work1_images/tikv%E7%BC%96%E8%AF%91%E5%87%BA%E9%94%99_20200816105349.png)<br>
根据百度方法,命令行输入下面语句解决<br>
cargo rustc -- -C link-arg=-nostartfiles<br>
![](https://github.com/gaokunnanjing/tidb-High-performance-work/blob/master/work1_images/%E7%BC%96%E8%AF%91tikv%E6%88%90%E5%8A%9F_20200816105948.png)
编译成功之后,会生成下面的可执行程序<br>
![](https://github.com/gaokunnanjing/tidb-High-performance-work/blob/master/work1_images/tidb%E5%8F%AF%E6%89%A7%E8%A1%8C_20200816120749.png)<br>
![](https://github.com/gaokunnanjing/tidb-High-performance-work/blob/master/work1_images/tikv%E5%8F%AF%E6%89%A7%E8%A1%8C_20200816121036.png)<br>
![](https://github.com/gaokunnanjing/tidb-High-performance-work/blob/master/work1_images/pd%E5%8F%AF%E6%89%A7%E8%A1%8C_20200816120829.png)<br>

### 4单机部署与测试
首先进入相应文件夹,按顺序启动 pd,tikv和tidb<br>
启动pd-server<br>
./bin/pd-server --name=pd1 \
--data-dir=pd1 \
--client-urls="http://127.0.0.1:2379" \
--log-file=pd.log

启动三个KV进程<br>
./tikv-server --pd="127.0.0.1:2379" \
--addr="127.0.0.1:20160" \
--data-dir=tikv1 \
--log-file=tikv1.log

.tikv-server --pd="127.0.0.1:2379" \
--addr="127.0.0.1:20161" \
--data-dir=tikv2 \
--log-file=tikv2.log

./tikv-server --pd="127.0.0.1:2379" \
--addr="127.0.0.1:20162" \
--data-dir=tikv3 \
--log-file=tikv3.log

启动tidb<br>
./bin/tidb-server --store=tikv \
--path="127.0.0.1:2379" \
--log-file=tidb.log


使用 netstat -lntp查看是否启动成功<br>
然后使用 mysql client进行连接<br>
mysql -h 127.0.0.1 -P 4000 -u root -D test
![](https://github.com/gaokunnanjing/tidb-High-performance-work/blob/master/work1_images/%E8%BF%9E%E6%8E%A5%E6%B5%8B%E8%AF%95_20200816111642.png)<br>
至此,源码安装部署成功 <br>
### 5修改源代码,重新部署,使得开启事务时打印 hello transaction
修改conn.go文件 dispatch函数<br>
![](https://github.com/gaokunnanjing/tidb-High-performance-work/blob/master/work1_images/1_20200816141356.png)<br>
重新编译,启动部署后,执行sql,运行结果<br>
![](https://github.com/gaokunnanjing/tidb-High-performance-work/blob/master/work1_images/3_20200816141118.png)<br>
![](https://github.com/gaokunnanjing/tidb-High-performance-work/blob/master/work1_images/2_20200816141237.png)<br>


