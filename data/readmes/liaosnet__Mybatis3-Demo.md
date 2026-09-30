# Mybatis-Demo 
Mybatis  
连接 GBase 8s数据库测试示例，包含简单的CRUD及分页查询。  

### 使用到的环境  
IDEA + Maven  
JDK-1.8  
Mybatis-3.4.5  
GBase 8s  
JDBC驱动2.0.1a2_2  
 
### 源代码结构  
```text
/src/main/java/
|- /com/gbasedbt/mybatis/Student.java
|- /com/gbasedbt/mybatis/StudentMapper.java
|- /com/gbasedbt/mybatis/StudentText.java
/src/main/resource 
|- db.properties
|- mybatis-config.xml
|- StudentMapper.xml
```

### 各配置文件说明  
1，db.properties  
> 数据库连接配置文件  

2，mybatis-config.xml  
> mybatis配置文件  

3，StudentMapper.xml
> Student映射文件  

详情见文档说明
