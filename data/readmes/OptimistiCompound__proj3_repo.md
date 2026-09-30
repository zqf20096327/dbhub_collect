# 数据库基准测试——比较分析openGauss 与 PostgreSQL

## 项目介绍

openGauss 是华为开发的开源关系型数据库管理系统（RDBMS），旨在为企业级应用提供支持，基于 PostgreSQL 进行开发，并进行了一些高性能、可靠性和安全性的增强。openGauss 被宣称尤其适用于复杂的数据密集型场景，例如金融系统、电信、以及大规模的电子商务平台。

然而，openGauss 是否如其所说的那样优秀？本项目旨在探索并评估这个问题。通过与 PostgreSQL 的比较，全面分析 openGauss 的优劣，并为其应用场景提供更多的数据支持。

> 本项目为南方科技大学`CS213 数据库原理（H）`课程项目

> 本项目对两个数据库的比较基于本地环境，且笔者没有对两个数据库进行调优，只是保证两者在Baseline接近的情形下进行对比测试。文档的写作目的在于通过课程项目学习更多数据库的知识，了解更多技术内幕。

## 文件结构

```
.
├──	Join
├──	QPS
|   ├── dataSource
|   |    ├── cities.csv
|   |    ├── cities.sql
├──	Autovacuum_update_delete
├── Cluster
├── README.md
├── Project 3 Benchmarking openGauss Against PostgreSQL A Comparative Analysis.pdf
```
请对照Project 3 Benchmarking openGauss Against PostgreSQL A Comparative Analysis.pdf中的说明查看本仓库。

## 环境依赖

### 使用docker进行部署数据库

#### 拉取镜像

```shell
docker pull docker.1panel.live/enmotech/opengauss:3.0.0
docker pull docker.1panel.live/ubuntu/postgres:14-22.04_beta
```

opengauss推荐使用3.0.0版本，更高的版本可能导致包依赖问题

#### 运行镜像

##### opengauss：

```shell
docker pull docker.1panel.live/enmotech/opengauss:3.1.1 docker pull docker.1panel.live/ubuntu/postgres:14-22.04_beta docker run --name project3-opengauss --privileged=true \ -d -e GS_PASSWORD= \ -v :/var/lib/opengauss -u root \ -p 15432:5432 \ docker.1panel.live/enmotech/opengauss:3.0.0
```

>  <GS_PASSWORD>：opengauss Docker 实例的密码
>
> openGauss 密码复杂度要求：密码长度必须至少为 8 个字符，并且必须包含大写字母、小写字母、数字和特殊字符。如果无法访问容器，请使用 `docker logs <container_id>` 命令检查密码是否有效。
> 持久化目录：存储 opengauss 数据库文件的本地目录。
> 请修改这些选项并在本地终端中运行命令。
>
> 如果部署在本地服务器上，则 URL 为 localhost（如果部署在其他服务器上，请使用该服务器的 IP 地址）。

执行后，opengauss 将在您的计算机上运行，并监听 15432 端口。
您可以使用与 PostgreSQL 兼容的驱动程序进行连接。
用户名为：gaussdb，密码由您自行配置。



##### postgres：

```shell
docker run -d \
 --name project3-postgres \
 -e POSTGRES_USER=postgres
 -e POSTGRES_PASSWORD=<!!!your db password!!!> \
 -e POSTGRES_DB=postgres
 -e PGDATA=/var/lib/postgresql/data/pgdata \
 -p 5432:5432 \
 -v <!!!persist directory!!!>:/var/lib/postgresql/data \
 docker.1panel.live/ubuntu/postgres:14-22.04_beta
```

>  <POSTGRES_PASSWORD>：Postgresql Docker 实例的密码
>
>  不需要复杂密码
>  PGDATA：存储 PostgreSQL 数据库文件的本地目录

 执行后，Postgres 将在您的计算机上运行，并监听 15432 端口。
 您可以使用 Postgres 驱动程序进行连接。
 用户名为：postgres，密码由您自行配置。
