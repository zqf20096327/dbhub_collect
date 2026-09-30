# 项目架构说明
### 1.架构模型：单体架构
### 2.架构特性：易维护、易部署
### 3.依赖中间件：dm8
### 4.采用ssh技术、支持 root 账户密码登录
### 5.部分操作采用ssh远程调用shell脚本方式
远程刷新设备脚本方式：修改 application.yml 中 manager.version 版本号，实现shell脚本自动更新升级
### 6.后端日志生成路径 /home/ncdb-admin/logs

# 启动说明
### 1.执行以下命令安装本地依赖
mvn install:install-file -Dfile=(项目根目录)\dm-framework\1.0.50\dm-framework-1.0.50.pom -DgroupId=com.dm.framework -DartifactId=dm-framework -Dversion=1.0.50 -Dpackaging=pom
### 2.连接数据源并执行根目录下doc中的sql（顺序为initDM.sql -> initDMData.sql -> initDM-DevEnv.sql(开发环境)
### 3.启动

# 部署说明 
### 1.将ncdb-admin-package.tar.gz 包上传到linux 任意路径 后执行 tar -zxvf ncdb-admin-package.tar.gz 解压
### 2.解压成功后会在当前目录下生成一个 ncdb-admin 文件夹
### 3.进入 ncdb-admin 文件夹
 --lib 文件夹 存放项目依赖的jar包
 --config 文件夹 存放项目的配置文件及shell 脚本等文件
  --config/application.yml 
 --config/license 文件夹 存放项目的license 文件