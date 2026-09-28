
# mysqltools 权威指南

官方微信公众平台 

![官方微信公众平台](docs/mp-wechat.jpg)

---

## 文档结构
- [概要](#概要)
  - [质量](#质量)
  - [效率](#效率)
  - [经济](#经济)
  - [技术介绍](#技术介绍)
- [安装mysqltools](#安装mysqltools)
  - [安装前的准备](#安装前的准备)
  - [下载并解压](#下载并解压)
  - [安装Python](#安装Python)
  - [安装ansible](#安装ansible)
  - [配置ansible和mysqltools](#配置ansible和mysqltools)
- [mysqltools快速开始](#mysqltools快速开始)
  - [mysqltools目录介绍](#mysqltools目录介绍)
  - [自动化mysql单实例安装](#自动化mysql单实例安装)
    - [进入mysql功能目录](#进入mysql功能目录)
    - [指定安装的目标主机](#指定安装的目标主机)
    - [执行自动化安装](#执行自动化安装)
  - [谈谈mysqltools如何实现高效](#谈谈mysqltools如何实现高效)
  - [谈谈mysqltools如何实现高质量](#谈谈mysqltools如何实现高质量)
- [赞助/交流/技术支持](#联系我)
- [mysql原生环境安装](#mysql原生环境安装)
  - [mysql单机](#mysql单机)
  - [mysql主从复制](#mysql主从复制)
  - [mysql多源复制](#mysql多源复制)
  - [mysql组复制](#mysql组复制)
  - [mysql小版本升级](#mysql小版本升级)
- [读写分离](#读写分离)
  - [mycat读写分离](#mycat读写分离)
- [高可用](#高可用)
  - [mha](#mha)
    - [环境规划](#环境规划)
    - [配置mha的一些前置备件](#配置mha的一些前置备件)
    - [配置ansible的hosts文件](#配置ansible的hosts文件)
    - [配置mysqltools中mha相关的配置项](#配置mysqltools中mha相关的配置项)
    - [配置mha的相关信息](#配置mha的相关信息)
    - [准备安装配置mha](#准备安装配置mha)
    - [安装配置mha](#安装配置mha)
    - [验证是否成功完成](#验证是否成功完成)
- [备份](#备份)
  - [mysqltools备份相关的实现细节](#mysqltools备份相关的实现细节)
  - [实施备份计划的前期准备](#实施备份计划的前期准备)
  - [配置备份](#配置备份)
  - [检查配置是否成功的几个点](#检查配置是否成功的几个点)
  - [注意事项](#注意事项)
- [巡检](#巡检)
  - [开发中]
- [监控](#监控)
  - [目前已经实现的监控项](#目前已经实现的监控项)
  - [监控项的人肉使用方法](#监控项的人肉使用方法)
  - [zabbix监控环境介绍](#zabbix监控环境介绍)
  - [zabbix监控环境安装规划](#zabbix监控环境安装规划)
  - [安装用于保存监控数据的mysql数据库](#安装用于保存监控数据的mysql数据库)
  - [改配置文件中zabbix_server_ip这个配置项](#改配置文件中zabbix_server_ip这个配置项)
  - [安装httpd](#安装httpd)
  - [安装zabbix服务端](#安装zabbix服务端)
  - [安装zabbix客户端](#安装zabbix客户端)
  - [通过mysqltools中给出的模板来监控mysql](#通过mysqltools中给出的模板来监控mysql)
  - [mysqltools中定义的MySQL的监控模板](#mysqltools中定义的MySQL的监控模板)
- [lnmp](#lnmp)
  - [安装mysql单机](#安装mysql单机)
  - [安装python](#安装python)
  - [安装nginx](#安装nginx)
  - [查看效果](#查看效果)

---

如果你使用 mysql-8.0 那么 https://github.com/Neeky/dbm-agent 在功能上会更加强大

---


## 概要

   总的来说mysqltools源自于工作、一个dba的日常大概包括 数据库安装，读写分离、高可用、负载均衡等环境的配置，
   数据库备份策略拟定与实施，数据库相关的监控，数据库优化，故障分析，也有可能参与到数据库建模，SQL的编写。
   
   这样我们就面临两个问题 1、**质量** 质量表现在解决问题的深度(类似问题还会再出现吗？) 2、**效率** 效率表现在你单位时间内解决问题的数量(安装一百个库的用时是一个库的100倍   吗？)； 通常这两个目标并不是互斥的，也就是说我们可以两个都做到。

   ---

1. ## 质量
   **KFC** vs **学校后街的蛋炒饭**

   KFC根据既定的流程生产每一个汉堡，假设这个流程下公众对汉堡给出的评分是80分，那么不管哪个KFC的店它生产出来的汉堡都稳定在80分；一段时间后它发现这个流程中可以改进的项，把汉堡的质量提升到81分，那么它就能做到所有的店里的汉堡都能打81分。

   学校后街的蛋炒饭 好不好吃这个事难说；因为好多事都影响到它，有可能老板今天心情不好，也有可能是今天客人太多他比较急，这些都会影响到炒饭的质量。有一次我要买两盒，由于去的比较晚，老板只有一个鸡蛋了，你没有猜错！ 他就只放了一个蛋，按常理是要一盒一个的。

   表面上看**KFC** 流程化生产的好处在于它的东西质量有保障，**最要命的是KFC只做加法，它可以不断提升自己，学校后街的蛋炒饭上周一，做的好吃，我们没办法确认那是不是超水平发挥，蛋炒饭质量的方差太大了。**

   
   **对于DBA来说可以专门针对自己的日常工作开发一款工具，这样做的好处有 1:)由于工具已经把流程固定下来了所以“产出的质量”有保证 2:)随着自己技术的进步自己工作的输出也可以稳步提高。**  **这样我们在质量这个目标上就只做加法了。**
   
   ---

2. ## 效率
   
   **流水线** vs **手工作坊**

   流水线相对于手工作坊，那是生产力的巨大提升。我为什么要说这个？因为在MySQL的使用中可能会遇到一些场景，比如说“分库分表”，“高可用+读写分离”；特别是前者通常就是一个MyCAT后面有好几十个分片，上百个MySQL实例(通常它们会为一个分片做一主两从并加上高可用)，装100+个MySQL今晚加班不？ 配100+个主从今晚加班不？ 不要忘记还要给它们加
   高可用呢？ 好吧这只是测试环境生产环境和测试环境是1:1的，那接下来几天加班不？ 对于生产通常还要加备份，监控那接下来几天加班不？

   **DBA的工具不应该只是能输出高质量的交付物，更应该要解放生产力----有批量管理的能力。**

   ---

3. ## 经济
   **mysqltools 是开源的&免费的&高质量的MySQL数据管理工具**

   ---

4. ## 技术介绍
   1、mysqltools的高质量源自于**蒋乐兴**也就是我写出来的高质量的playbook

   2、mysqltools的高效源自于**ansible**这个批量管理工具

   3、1 , 2 基本上解决了原生MySQL的环境(**单机**、**master -->slave**、**mysql-group-replication** 、**multi-source-replication**)的安装部署

   4、mysqltools在为MySQL做**高可用**时采用的是**MHA**这个方案，**读写分离用**的是**MyCAT**

   5、mysqltools在**备份**时支持到了 **xtrabackup**,**mysql enterprise backup**,**mysqldump**

   6、mysqltools在**监控**MySQL时用的是**zabbix**

   7、其它开源工具无法满足的功能通过自己编写程序实现。由于这个程序的许多功能是通用的，所以我把它单独了出来成为一个新的开源项目，这样它就与mysqltools解耦了。详见<a href="https://github.com/Neeky/mysqltools-python">mysqltools-python </a>

   mysqltools的定位是一个**集中化管理平台**你只要**在一台主机上安装好mysqltools就可以了**，其它主机作为被管理都的角色。由于mysqltools是基于**Python-3.x**开发
   出来的所以你的**主控机**上应该事先安装好python-3.x、还要安装上ansible。 好在mysqltools已经包含有所有**Python**和**ansi

[...截断...]

ble**所有的包。

   ---

## 安装mysqltools

   假设我们有如下一套环境、把**172.16.192.131**这台主机作为主控机.
   
   **角色**     | **ip地址**         | **系统版本**   |
   -----------:|:-------------------|--------------|
   主控机       | 172.16.192.131     |centos-7.4    |
   被控机       | 172.16.192.132     |centos-7.4    |
   ...         | ...                |centos-7.x    |

   ---

   1. ### 安装前的准备
      1): **你的主控机上要配置有yum**、因为mysqltools要源码编译安装Python-3.6.2、这就涉及gcc ... 等依赖
   
      2): **有主控机的root账号(安装软件时会用到)**
   
      3): **被控机上也要配置好yum**

      ---

   2. ### 下载并解压
      **mysqltools是开源在github上的、下载地址如下：https://github.com/Neeky/mysqltools/archive/master.zip** 
   
      linux可以直接执行如下命令完成下载并解压到/usr/local/
   
      ```bash
      cd /tmp/
      wget https://github.com/Neeky/mysqltools/archive/master.zip &
   
      ll -h /tmp/                                                                           
      -rwxr-xr-x. 1 root  root  194M 3月  23 11:52 master.zip
   
      unzip master.zip
   
      mv mysqltools-master /usr/local/mysqltools
      ```
   
      ---

   3. ### 安装Python
      **mysqltools包含了Python的自动化安装脚本、前提是yum已经可用**
   
      ```bash
      cd /usr/local/mysqltools/deploy/packages/python/
      bash install.sh
   
      ```
      安装成功后的最后几行输出如下：
      ```bash
      Collecting setuptools
      Collecting pip
      Installing collected packages: setuptools, pip
      Successfully installed pip-9.0.1 setuptools-28.8.0
      ```
   
      检查python3是否安装成功
      ```bash
      source /etc/profile
    
      python3 --version
      Python 3.6.2
      ```
   
      ---
   
   4. ### 安装ansible
      **ansible和它相关的依赖我都打包到mysqltools中了、也和上面安装python一样一行命令就行**
   
      ```bash
      source /etc/profile
      cd /usr/local/mysqltools/deploy/packages/ansible
      bash install.sh 
   
      ```
      安装成功后可以看到如下输出
      ```bash
      Using /usr/local/python-3.6.2/lib/python3.6/site-packages
      Finished processing dependencies for ansible==2.4.0.0
      ```
   
      ---

   5. ### 配置ansible和mysqltools
      1): **增加ansible的配置文件**

      ```bash
      # 增加ansible的配置文件
      mkdir -p /etc/ansible
      touch /etc/ansible/hosts
      ```
      /etc/ansible/hosts文件如下：
      ```
      host_131 ansible_user=root ansible_host=172.16.192.131
      host_132 ansible_user=root ansible_host=172.16.192.132
      ```

      ---

      2): **配置主控机与被控机之间的ssh信任**

      ```bash
      ssh-keygen
      ssh-copy-id root@172.16.192.131
      ssh-copy-id root@172.16.192.132
      ```
      命令输出大致如下：
      ```bash
      ssh-keygen # 一直回车就能生成钥匙对了
      Generating public/private rsa key pair.
      Enter file in which to save the key (/root/.ssh/id_rsa): 
      Enter passphrase (empty for no passphrase): 
      Enter same passphrase again: 
      Your identification has been saved in /root/.ssh/id_rsa.
      Your public key has been saved in /root/.ssh/id_rsa.pub.
      The key fingerprint is:
      SHA256:D9kR6/ehu5O99p/LRJlZWNqwZ0tzU4+jvPegq7j/Pq8 root@studio2018
      The keys randomart image is:
      +---[RSA 2048]----+
      |          .   . o|
      |           o   Oo|
      |          o   *+B|
      |         + o ..+X|
      |        S o + .* |
      |         o . +.. |
      |          . oo+. |
      |         .  ++=o.|
      |        ooo+EOo**|
      +----[SHA256]-----+
   
   
      ssh-copy-id root@172.16.192.131 # 回答yes、然后输入目标主机的root密码
      /usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/root/.ssh/id_rsa.pub"
      The authenticity of host '172.16.192.131 (172.16.192.131)' can't be established.
      ECDSA key fingerprint is SHA256:qdoqi3B2aqO3ssOIphwOiWLywSlAoflX2YH+LCG7T/E.
      ECDSA key fingerprint is MD5:8f:78:6e:20:ab:d0:2a:6b:c0:1a:e5:09:ac:82:7d:04.
      Are you sure you want to continue connecting (yes/no)? 
      root@172.16.192.131's password: 
      
      Number of key(s) added: 1
      
      Now try logging into the machine, with:   "ssh 'root@172.16.192.131'"
      and check to make sure that only the key(s) you wanted were added.
   
