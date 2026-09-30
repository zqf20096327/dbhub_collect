# seata-samples-polardb

Spring Cloud Alibaba + Seata + Nacos + OpenFeign + MP

用于阿里云polardb使用PG和MySQL原生JDBC驱动的能力下，与当前的seata 1.6.1的兼容性的简单测试。

### 主要组件及其版本

|          组件          |      版本       |                  备注                  |
|:--------------------:|:-------------:|:------------------------------------:|
|        seata         |     1.6.1     |                                      |
| spring-cloud-alibaba | 2.2.6.RELEASE | 包含nacos client 1.4.2, 与seata 1.6.1适配 |
|     spring-cloud     | 2.2.6.RELEASE |           包含feign 10.10.1            |
|     spring-boot      | 2.3.2.RELEASE |                                      |
|      mysql-jdbc      |    8.0.28     |                                      |
|      postgresql      |    42.6.0     |                                      |
|     mybatis plus     |     3.4.0     |                                      |

### 主要服务及其版本

|      服务      |  版本   | 
|:------------:|:-----:|
| seata server | 1.6.1 | 
| nacos server | 1.4.2 |

### 测试

- [scripts](scripts)
- [test requests](test.http)