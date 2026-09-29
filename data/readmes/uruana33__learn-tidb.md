# learn-tidb



练习1:

使得 TiDB 启动事务时，能打印出一个 “hello transaction” 的 日志



由文章：三篇文章了解 TiDB 技术内幕 - 说计算，可知事务相关逻辑应该在kv层。

改动代码：

github.com/pingcap/tidb/store/tikv/kv.go:281

```golang
func (s *tikvStore) Begin() (kv.Transaction, error) {
	txn, err := newTiKVTxn(s)
	if err != nil {
		return nil, errors.Trace(err)
	}
	logutil.Logger(context.Background()).Info("on tikvStore, hello transaction")
	return txn, nil
}

```



过程记录：

1.pd安装(Placement Driver)

```shell
git clone https://github.com/pingcap/pd
cd pd
make build

# start
./pd-server
```



2.tikv安装

docker方式：

```shell
$ git clone https://github.com/pingcap/tidb-docker-compose.git
$ cd tidb-docker-compose && docker-compose pull # Get the latest Docker images
$ docker-compose up -d
$ mysql -h 127.0.0.1 -P 4000 -u root
```



```shell
export HostIP="127.0.0.1"
docker run -d -p 2379:2379 -p 2380:2380 --name pd pingcap/pd \
          --name="pd" \
          --data-dir="pd" \
          --client-urls="http://0.0.0.0:2379" \
          --advertise-client-urls="http://${HostIP}:2379" \
          --peer-urls="http://0.0.0.0:2380" \
          --advertise-peer-urls="http://${HostIP}:2380" \
          --log-file=pd.log
 
 
docker run -d --name tikv1 \
-p 20160:20160 \
pingcap/tikv:latest \
--addr="0.0.0.0:20160" \
--advertise-addr="${HostIP}:20160" \
--data-dir="/data/tikv" \
--pd="${HostIP}:2379"
 
docker run -d --name tikv2 \
-p 20162:20160 \
pingcap/tikv:latest \
--addr="0.0.0.0:20160" \
--advertise-addr="${HostIP}:20162" \
--data-dir="/data/tikv" \
--pd="${HostIP}:2379"
 
docker run -d --name tikv3 \
-p 20163:20160 \
pingcap/tikv:latest \
--addr="0.0.0.0:20160" \
--advertise-addr="${HostIP}:20163" \
--data-dir="/data/tikv" \
--pd="${HostIP}:2379"
 
 
docker run -d --name tikv4 \
-p 20164:20160 \
pingcap/tikv:latest \
--addr="0.0.0.0:20160" \
--advertise-addr="${HostIP}:20164" \
--data-dir="/data/tikv" \
--pd="${HostIP}:2379"
```



3.tidb安装

```shell
git clone https://github.com/pingcap/tidb.git $GOPATH/src/github.com/pingcap/tidb
cd $GOPATH/src/github.com/pingcap/tidb
make

./tidb-server --store=tikv --path="127.0.0.1:2379" --log-file=tidb.log

```



4.使用mysql客户端

Host:localhost

Port:4000

Username: root

Passed: 空