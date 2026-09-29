# Gandalf-TiDB
It's built with TiDB and It shows that TiDB supports raw mysql protocal perfectly.

* ### 项目说明
本项目主要是用Java和Python脚本的方式访问TiDB。
测试的时候，Java使用的JDBC原生的数据库驱动，Python使用PyMySQL 0.8.0

以下是在本地搭建TiDB环境的过程以及可能遇到的问题。


* ### 下载Docker for Mac
下载完成后，双击Docker.dmg，安装Docker for Mac。

https://docs.docker.com/docker-for-mac/install/

* ### Docker Compose
Docker 编排服务

* ### 下载 tidb-docker-compose

```
cd /Users/lucas/tools
git clone https://github.com/pingcap/tidb-docker-compose.git
cd /Users/lucas/tools/tidb-docker-compose

``` 

* ### 拉取最新镜像

```$xslt
cd tidb-docker-compose && docker-compose pull # Get the latest Docker images
```

* ### 通过docker images可以看到pd，tikv，tidb的镜像已经被拉下来了
docker images

* ### 启动容器
守护进程的方式启动
```$xslt
docker-compose up -d

```

通过docker ps -a可以看到pd，tikv，tidb容器已经启动了，启动了3 个 PD，3 个 TiKV，1 个 TiDB。

* ### 访问集群

```$xslt
mysql --default-character-set=utf8 -h 127.0.0.1 -P 4000 -u root

```

可以看到TiDB已经启动了，我们通过mysql命令已经可以访问集群了


* ### 停止集群 或者 批量stop docker 进程
停止集群

```$xslt

docker-compose stop

```

批量stop

```$xslt

docker ps -a | awk '{print $1}'|xargs docker stop

```

* ### start command|启动命令

```$xslt
mysql --default-character-set=utf8 -h 127.0.0.1 -P 4000 -u root

```

- 注意：
    
    不加参数：--default-character-set=utf8，可能会遇到下面的错误：
    
    mysql ERROR 1105 (HY000): Unknown charset id 255