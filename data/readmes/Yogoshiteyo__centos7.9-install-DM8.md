# centos7安装达梦8（DM8）数据库
## 1. 基础信息
    操作系统：centos7.9
    DB Version: 0x7000c
    安装包：https://download.dameng.com/eco/adapter/DM8/202401END/dm8_20240116_x86_rh7_64.zip
## 2. 创建安装用户
### 2.1 不建议使用root用户直接安装，所以创建一个安装用户
```bash
groupadd  dinstall
useradd  -g dinstall -m -d /home/dmdba -s /bin/bash dmdba
echo "password" | passwd "dmdba" --stdin
mkdir -p /data/dm8
chown -R dmdba.dinstall /data/dm8
```
### 2.2 镜像挂载
```bash
cd /home/dmdba
mkdir tmp
unzip dm8_20240116_x86_rh7_64.zip
mount dm8_20240116_x86_rh7_64.iso /home/dmdba/tmp/
```
### 2.3 切换到dmdba用户设置环境变量
```bash
su - dmdba
echo 'export DM_HOME="/data/dm8"' >> ~/.bash_profile
echo 'export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/data/dm8/bin"' >> ~/.bash_profile
echo 'export PATH=$PATH:$DM_HOME/bin:$DM_HOME/tool' >> ~/.bash_profile
source .bash_profile
```
### 2.4 进入安装目录安装
```bash
cd /home/dmdba/tmp/
./DMInstall.bin -i
```
请选择安装语言 [1]:```1```

是否输入Key文件路径? (Y/y:是 N/n:否) [Y/y]:```n```

是否设置时区? (Y/y:是 N/n:否) [Y/y]:```y```

请选择时区 [21]:```21```

请选择安装类型的数字序号 [1 典型安装]:```1```

请选择安装目录 [/home/dmdba/dmdbms]:```/data/dm8```

是否确认安装路径(/data/dm8)? (Y/y:是 N/n:否)  [Y/y]:```y```

是否确认安装? (Y/y:是 N/n:否):```y```

请以root系统用户执行命令:
/data/dm8/script/root/root_installer.sh
### 2.5 安装DmAPService服务
```bash
exit
/data/dm8/script/root/root_installer.sh
```
移动 /data/dm8/bin/dm_svc.conf 到/etc目录
```bash
cd /data/dm8/script/root/
./dm_service_installer.sh -t dmap
```
创建服务(DmAPService)完成
### 2.6 初始化数据库
```bash
su - dmdba
/data/dm8/bin/dminit PATH=/data/dm8/data
```
### 2.7 安装DmServiceDMSERVER实例
```bash
exit
/data/dm8/script/root/dm_service_installer.sh -t dmserver -dm_ini /data/dm8/data/DAMENG/dm.ini -p DMSERVER
```
创建服务(DmServiceDMSERVER)完成
```bash
systemctl start DmServiceDMSERVER
systemctl status DmAPService.service
systemctl status DmServiceDMSERVER
```
