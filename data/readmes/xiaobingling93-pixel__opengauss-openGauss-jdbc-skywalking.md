# openGauss-jdbc-skywalking

#### 介绍
该文基于Skywalking 8.5.0

8.5.0源码：https://archive.apache.org/dist/skywalking/8.5.0/apache-skywalking-apm-8.5.0-src.tgz

安装介质：https://archive.apache.org/dist/skywalking/8.5.0/apache-skywalking-apm-es7-8.5.0.tar.gz

安装手册原文： https://skywalking.apache.org/docs/main/v8.5.0/readme/

#### UI 安装教程
解压apache-skywalking-apm-es7-8.5.0.tar.gz 包后，UI已经包含在里面；
使用/bin/webappService.sh(.bat) 来运行；
##### 配置
配置文件在webapp/webapp.yml
```
server:
  port: 8080

collector:
  path: /graphql
  ribbon:
    ReadTimeout: 10000
    # 多个地址使用,(逗号分隔)
    listOfServers: 10.2.34.1:12800,10.2.34.2:12800
```


#### Agent 安装教程

1.  Sky8.5 Agent 支持JDK8以上版本， 1.8以下版本不再支持；
2.  解压apache-skywalking-apm-es7-8.5.0.tar.gz 介质包后 找到agent 目录；
3.  在config/agent.config配置文件中，设置agent.service_name 服务名称，可以是任何英文字符；
4.  在config/agent.config配置文件中，设置collector.backend_service 服务端地址，默认为127.0.0.1:11800
5.  将-javaagent:/path/to/skywalking-package/agent/skywalking-agent.jar 加入到你的应用启动参数中；

Agent 介质包目录
```
+-- agent
    +-- activations
         apm-toolkit-log4j-1.x-activation.jar
         apm-toolkit-log4j-2.x-activation.jar
         apm-toolkit-logback-1.x-activation.jar
         ...
    +-- config
         agent.config  
    +-- plugins
         apm-dubbo-plugin.jar
         apm-feign-default-http-9.x.jar
         apm-httpClient-4.x-plugin.jar
         .....
    +-- optional-plugins
         apm-gson-2.x-plugin.jar
         .....
    +-- bootstrap-plugins
         jdk-http-plugin.jar
         .....
    +-- logs
    skywalking-agent.jar
```

    
#### Postgresql 对 openGauss-jdbc监控支持

OpenGauss数据库采用了与Postgresql相同的驱动方式，Skywalking 中已经对Postgresql做了支持，但是在新的Driver中官方提供的插件包存在部分不兼容情况，对此作了部分修正，将https://gitee.com/gitee_652781429/openGauss-jdbc-skywalking.git 中提供openGauss-jdbc-skywalking/ apm-postgresql-8.x-plugin-8.5.0.jar包进行替换，替换文件agent/plugin/目录下即可；



##### 修正说明
openGauss-jdbc-skywalking/postgresql-8.x-plugin为修正代码模块；
修正代码 
postgresql-8.x-plugin/src/main/java/org/apache/skywalking/apm/plugin/jdbc/postgresql/CreateStatementInterceptor.java

原：

```
    @Override
    public Object afterMethod(EnhancedInstance objInst, Method method, Object[] allArguments, Class<?>[] argumentsTypes,
                              Object ret) throws Throwable {

        if (ret instanceof EnhancedInstance) {
            ConnectionInfo connectInfo = (ConnectionInfo) objInst.getSkyWalkingDynamicField();
            ((EnhancedInstance) ret).setSkyWalkingDynamicField(new StatementEnhanceInfos(connectInfo, "", "Statement"));
        }

        return ret;
    }
```

修正后：

```
    @Override
    public Object afterMethod(EnhancedInstance objInst, Method method, Object[] allArguments, Class<?>[] argumentsTypes,
                              Object ret) throws Throwable {

        if (ret instanceof EnhancedInstance) {
            ConnectionInfo connectInfo = (ConnectionInfo) objInst.getSkyWalkingDynamicField();
			//修正代码
            if (connectInfo == null && objInst instanceof PgConnection) {
                PgConnection conn = (PgConnection) objInst;
                String url = conn.getURL();
                connectInfo = URLParser.parser(url);
            }
            ((EnhancedInstance) ret).setSkyWalkingDynamicField(new StatementEnhanceInfos(connectInfo, "", "Statement"));
        }

        return ret;
    }
```

#### OpenGauss-jdbc监控支持

基于openGauss-connector-jdbc-2.0.1 驱动，增加 opengauss-2.x-plugin 插件；

将openGauss-jdbc-skywalking/ compile包下：
apm-jdbc-commons-8.5.0.jar替换原 agent/plugins/apm-jdbc-commons-8.5.0.jar
opengauss-2.x-plugin-8.5.0.jar 放到 agent/plugins/下

skywalking-agent.jar 更新 agent/下的 skywalking-agent.jar 

同时更新 component-libraries.yml 到 /apache-skywalking/config/component-libraries.yml

#### 使用说明

请参照：https://skywalking.apache.org/docs/main/v8.5.0/en/ui/readme/

#### 参与贡献

1.  Fork 本仓库 https://gitee.com/opengauss/openGauss-jdbc-skywalking



