## 这是达梦数据库版的nacos,基于nacos2.4.3源码改造,适配达梦数据库8

jdk8 maven3.8.1
在项目根目录下运行以下命令
```shell
     mvn -Prelease-nacos -Dmaven.test.skip=true -Dpmd.skip=true -Drat.skip=true -Dcheckstyle.skip=true clean install -U
```
构建成功在distribution模块的target目录下生成达梦版的nacos-server-2.4.3.zip

参考文章：[点击这里跳到我的博客](https://blog.csdn.net/pky86676022/article/details/137726884)

docker版的如下：
```shell
        docker pull --platform=linux/amd64 pkyit/nacos:2.4.3-dm8 # 拉取x86架构镜像
        
        docker pull --platform=linux/arm64 pkyit/nacos:2.4.3-dm8 # 拉取arm64架构镜像
```

记得挂载配置文件
```shell
docker run -d --name=nacos-dm -e MODE=standalone \
 -v /root/application.properties:/home/nacos/conf/application.properties \
  -p 8848:8848 -p 9848:9848 \
   pkyit/nacos:2.4.3-dm8
```