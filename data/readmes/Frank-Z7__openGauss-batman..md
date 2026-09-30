openGauss-batman是一款前后端分离的数据库备份恢复管理软件。  
前端采用vue2框架进行开发，后端采用spring-boot套件。  
openGauss-batman的代码框架来源于开源的renren-fast，在其上进行了
大量的开发改造。  
batman缩写自Backup And resTore MANagement system中大写的英文字母。  


# 特点  
* 支持逻辑备份和物理备份
* 物理备份支持全量备份和增量备份
* 全量备份和增量备份均支持周期性备份
* 支持物理备份后恢复到指定的备份集

# 限制约束
* 单实例最多支持各一个物理全量备份和物理增量备份计划
* 备份命令采用SSH remote的方式执行
* 目前仅支持本地盘备份
* batman自身的数据存储使用PostgreSQL数据库，主要原因是由于PG良好的平台兼容性。
* node.js建议使用v14版本，在其它版本上前端代码可能会编译失败

# 使用说明
## 从源码启动
源码启动的方式需要用户自己配置好数据源，当前支持的数据库为PostgreSQL。
1、在数据库实例中创建batman数据库
2、修改backend/src/main/resources/application-prod.yml中的数据库的连接IP、用户名以及密码
3、进入backend目录，执行以下命令进行打包，
```shell
  mvn package
```
4、进入生成的target目录下，执行以下命令启动后端服务
```shell
  java -jar opengauss-batman.jar
```
5、切换到web目录,执行以下命令，启动前端服务
```shell
  sudo npm install -g serve
  npm run build:prod
  serve -s dist -p 8081
```
## 快速启动
  使用docker-compose快速打包体验。在batman目录下执行以下命令即可快速启动
  ```shell
  docker-compose up -d 
  ```
  启动成功后，在浏览器中输入127.0.0.1:8081即可进入管理系统


