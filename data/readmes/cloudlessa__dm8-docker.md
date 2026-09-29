## 镜像说明

**构建版本：** dm8_20220822_rev166351_x86_rh6_64_ctm

**暴露端口：** 5236

### 环境变量

#### `DM8_SYSDBA_PWD`

> 初始用户sysdba,密码默认值`123456789`


#### docker镜像文件下载地址
> https://www.dameng.com/list_103.html

```
docker load -i dm8_20220822_rev166351_x86_rh6_64_ctm.tar

```

## 使用说明

> 下面的案例采用`docker-compose`部署，挂载了数据目录和授权文件，并暴露了端口出来，默认用户`sysdba`的密码设置为`123456789`

### docker-compose.yml

```
version: '3'
services:
  dm:
    image: "dm8_single:v8.1.2.128_ent_x86_64_ctm_pack4"
    build:
      context: ./
      dockerfile: Dockerfile
    restart: always
    container_name: dm8_single
    environment:
      - SYSDBA_PWD=123456789
    ports:
      - 5236:5236
    volumes:
      - 自己磁盘挂载目录/data:/home/dmdba/data
networks:
  default:
    external:
      name: cloudlessa
```

### 启动停止

- 启动

> ```sh
> docker-compose up -d
> ```

- 查看日志

>  ```sh
>  docker ps -a
>  docker logs 容器id
>  ```

> 如果出现如下日志则启动成功

```
Attaching to dm8_single

dm8_single | file dm.key not found, use default license!

dm8_single | License will expire on 2023-08-04

dm8_single | Normal of FAST

dm8_single | Normal of DEFAULT

dm8_single | Normal of RECYCLE

dm8_single | Normal of KEEP

dm8_single | Normal of ROLL

dm8_single |

dm8_single | log file path: /opt/dmdbms/data/DAMENG/DAMENG01.log

dm8_single |

dm8_single |

dm8_single | log file path: /opt/dmdbms/data/DAMENG/DAMENG02.log

dm8_single |

dm8_single | write to dir [/opt/dmdbms/data/DAMENG].

dm8_single | create dm database success. 2023-07-07 13:33:31

dm8_single | initdb V8

dm8_single | db version: 0x7000c

dm8_single | Init DM success!

dm8_single | Start DmAPService...

dm8_single | Starting DmAPService: [ OK ]

dm8_single | /opt/dmdbms/conf/dm.ini does not exist, use default dm.ini

dm8_single | Start DMSERVER success!

dm8_single | Dmserver is running.

dm8_single | DM Database is not OK, please wait...

dm8_single | DM Database is OK

dm8_single | Finished soft link DM current dm_DMSERVER_202307.log to dm_DMSERVER.log

dm8_single | * Starting periodic command scheduler cron

dm8_single | ...done.

dm8_single | 2023-07-07 13:33:53.913 [INFO] database P0000000048 T0000000000000000093 total 0 active crash trx, pseg_crash_trx_rollbacksys_only(0) begin ...

dm8_single | 2023-07-07 13:33:53.913 [INFO] database P0000000048 T0000000000000000093 pseg_crash_trx_rollback end, total 0 active crash trx, include 0 empty_trxs, 0 empty_pages which only need to delete mgr recs.

dm8_single | 2023-07-07 13:33:53.913 [INFO] database P0000000048 T0000000000000000093 pseg_crash_trx_rollback end

dm8_single | 2023-07-07 13:33:53.913 [INFO] database P0000000048 T0000000000000000093 hpc_clear_active_trx adjust n_crash_active_trx from 0 to 0.

dm8_single | 2023-07-07 13:33:53.914 [INFO] database P0000000048 T0000000000000000048 backup control file /opt/dmdbms/data/DAMENG/dm.ctl to file /opt/dmdbms/data/DAMENG/dm_20230707133353_913995.ctl

dm8_single | 2023-07-07 13:33:53.916 [INFO] database P0000000048 T0000000000000000048 backup control file /opt/dmdbms/data/DAMENG/dm.ctl to file /opt/dmdbms/data/DAMENG/ctl_bak/dm_20230707133353_914965.ctl succeed

dm8_single | 2023-07-07 13:33:53.916 [INFO] database P0000000048 T0000000000000000048 local instance name is DMSERVER, mode is NORMAL, status is OPEN.

dm8_single | 2023-07-07 13:33:53.916 [INFO] database P0000000048 T0000000000000000048 SYSTEM IS READY.
```

### 使用dbeaver 或者navicat 连接都可以
> 驱动在jdbc文件夹下
