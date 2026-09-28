# 达梦数据库实践

**不喜欢就别用，既然自己能写的更好，就自己写。觉得没法用，请直接将此项目从您的设备中删除。** 请仔细查看各个脚本的用途，如果看不懂，**亦请直接将此项目从您的设备中删除**。遇到问题可以看[这里](./qa.md)，如果您遇到的问题不在其中，欢迎提出。

> TIPS:  
> 达梦启动需要时间，要等一会再连接。

## [QA](./qa.md)

一些开发问题，请看[这里](./qa.md)

## docker

### 官方docker

[官方 docker 下载](https://eco.dameng.com/download/)

[流程](https://eco.dameng.com/document/dm/zh-cn/start/dm-install-docker.html)如下

```bash
# load
docker load -i dm8_20220822_rev166351_x86_rh6_64_ctm.tar
# run
docker run -d -p 5236:5236 --restart=always --name dm8_01 --privileged=true -e PAGE_SIZE=16 -e LD_LIBRARY_PATH=/opt/dmdbms/bin -e INSTANCE_NAME=dm8_01 -v /data/dm8_01:/opt/dmdbms/data dm8_single:v8.1.2.128_ent_x86_64_ctm_pack4
# log
docker logs -f dm8_01
# start stop
docker stop dm8_01
docker start dm8_01
docker restart dm8_01
```

> 1. 如果使用 docker 容器里面的 disql，进入容器后，先执行 source /etc/profile 防止中文乱码。
> 2. 新版本 Docker 镜像中数据库默认用户名/密码为 SYSDBA/SYSDBA001。

```bash
# login
cd /opt/dmdbms/bin && ./disql SYSDBA/SYSDBA001@127.0.0.1:5236
cd $DM_HOME/bin && ./disql SYSDBA/SYSDBA001@127.0.0.1:5236

cd /opt/dmdbms/bin
./disql SYSDBA/SYSDBA001@127.0.0.1:5236
./disql test111/'"123456@@@"'@127.0.0.1:5236

# or
isql -v DM
```
