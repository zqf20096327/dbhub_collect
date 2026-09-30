# flink-sql-connector-tdsql-cdc
详情参考我的博客：[https://blog.csdn.net/qq_20042935/article/details/133858359](https://blog.csdn.net/qq_20042935/article/details/133858359)

基于flink-sql-connector-mysql-cdc二次开发的腾讯tdsql cdc connectors

相关maven命令如下:

```bash
## 打包命令
mvn clean package  -Dfile.encoding=UTF-8 -Dmaven.test.skip=true  -f pom.xml
## 查询依赖关系
mvn dependency:tree 
```
