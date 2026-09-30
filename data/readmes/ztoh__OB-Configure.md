搭建过程:
本项目为maven工程 + mysqldb,前提先配置好java/maven环境
1.执行init_sql_20130517.sql文件的语句在mysql上建表
2.修改obconfig-db.properties文件设置数据库连接属性
3.执行mvn clean package -Dmaven.test.skip命令
执行后为一个war包^_^