# 制作在Apple芯片下运行达梦数据库的docker镜像
### 注意点
1. Apple的芯片是Arm架构，需要下载Arm的达梦数据库安装文件
2. 用户与权限：按照实际目录修改
3. 安装配置文件：修改实际安装目录，按需配置参数
4. 入口脚本：修改实际安装目录
### 具体过程
1. 拉取ubuntu22镜像
2. 下载达梦安装文件，操作系统：麒麟10SP1，cpu：飞腾920
3. 宿主的用户与权限
```
sudo dscl . -create /Groups/dmdba
sudo dscl . -create /Groups/dmdba PrimaryGroupID 1001

sudo dscl . -create /Users/dmdba UniqueID 1001
sudo dscl . -create /Users/dmdba PrimaryGroupID 1001
sudo dscl . -create /Users/dmdba NFSHomeDirectory /dm具体目录/home
sudo dscl . -create /Users/dmdba UserShell /bin/bash
sudo dscl . -passwd /Users/dmdba password123
sudo chown 1001:1001 /Users/dm的具体目录/home

如果权限有问题，可以通过界面操作
dm/home目录->显示简介->共享与权限：给docker运行用户添加读写权限
```
4. 宿主机目录结构
```
dm
|-install
	|-DMInstanll.bin
	|-dm_init.xml
	|-entrypoint.sh
|-home
	|-dbdata
```
### 安装完成
1. ubuntu的root密码:password123
2. 达梦的密码:Dameng123
3. 容器中数据库安装位置 :/home/dmdba/dmdbms
4. 宿主目录:dm/home/dbdata
