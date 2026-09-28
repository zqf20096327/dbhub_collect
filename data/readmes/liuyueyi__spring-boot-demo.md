# Spring-Boot-Demo

<a href="https://spring.hhui.top" target="_blank">
    <img src="https://img.shields.io/badge/-微信关注“一灰灰blog”公众号-orange.svg" alt="#" align="right">
</a>


[![Build Status](https://travis-ci.org/liuyueyi/spring-boot-demo.svg?branch=master)](https://travis-ci.org/liuyueyi/spring-boot-demo)
[![Average time to resolve an issue](http://isitmaintained.com/badge/resolution/liuyueyi/spring-boot-demo.svg)](http://isitmaintained.com/project/liuyueyi/spring-boot-demo "Average time to resolve an issue")
[![Percentage of issues still open](http://isitmaintained.com/badge/open/liuyueyi/spring-boot-demo.svg)](http://isitmaintained.com/project/liuyueyi/spring-boot-demo "Percentage of issues still open")

> SpringBoot + SpringCloud + SpringSecurity学习过程中的源码汇总，沉淀记录下学习历程


<bold style="color:red">
说明：Spring系列教程现已根据专栏方式进行收集整理，更便于系统学习，详情查看: [一灰灰的Spring系列专栏](https://hhui.top/spring/)</bold>

欢迎关注公众号 `一灰灰blog` 更多干货持续分享

![QrCode](https://spring.hhui.top/spring-blog/imgs/info/info.png)

## 0. 项目说明

如果想在本机使用这个项目的demo，下面有一些注意事项

环境要求

```bash
java: jdk1.8
maven: 3.2+
spring boot: 2.2.1.RELEASE
ide: IDEA/Eclipse/NetBeans随意

## 不同项目的环境依赖，请以项目对应的博文要求为准
db: mongodb + mysql + redis + solr + elasticsearch
中间件: promotheus + grafana + kibana + rabbitmq
```

IDEA插件

```bash
# 必须
lombok

# 推荐
maven helper: 查看依赖树的好工具（排除依赖冲突非常棒）
Free MyBatis plugin: mybatis的mapper与xml跳转比较方便
Mybatis log Plugin：日志
CodeGlance: 类似sublimetext 右边的快速预览框
Rainbow Brackets: 不同层级的括号颜色不一样
```

## 1. 知识点图谱

所有博文集中发布在个人博客网站 ： [一灰灰Blog-Spring](http://spring.hhui.top/)

大致规划的内容包括以下章节，希望能用<del>半年到一年(严重超期)</del>的时间完成....

### I. [基础篇](http://spring.hhui.top/spring-blog/categories/SpringBoot/基础篇/)

- [x] [配置相关](http://spring.hhui.top/spring-blog/tags/Config/)
- [x] [Bean相关](http://spring.hhui.top/spring-blog/tags/Bean/)
- [x] [日志相关](http://spring.hhui.top//spring-blog/tags/Log/)
- [x] [AOP相关](http://spring.hhui.top//spring-blog/tags/AOP/)
- [x] [SPEL](https://spring.hhui.top/spring-blog/tags/SpEL/)
- [x] [事件通知机制](https://spring.hhui.top/spring-blog/tags/EventListener/)

### II. 高级篇

- [x] [db读写](http://spring.hhui.top/spring-blog/tags/DB/)
    - [x] 基本配置，数据源，多数据源
    - [x] [jdbcTemplate](http://spring.hhui.top/spring-blog/tags/JdbcTemplate/)
    - [x] [jpa](http://spring.hhui.top/spring-blog/tags/JPA/)
        - 项目工程： [spring-boot/102-jpa](spring-boot/102-jpa)
    - [x] mybatis
      -
      项目工程:  [spring-boot/103-mybatis-xml](spring-boot/103-mybatis-xml) , [spring-boot/104-mybatis-noxml](spring-boot/104-mybatis-noxml)
    - [x] mybatis plus
        - 项目工程: [spring-boot/105-mybatis-plus](spring-boot/105-mybatis-plus)
    - [x] [Jooq](http://spring.hhui.top/spring-blog/tags/Jooq/)
      -
      项目工程: [spring-boot/108-jooq-curd](spring-boot/108-jooq-curd), [spring-boot/108-jooq-mysql](spring-boot/108-jooq-mysql)
- [ ] influxdb 时序数据库
  -
  项目工程: [spring-boot/130-influxdb](spring-boot/130-influxdb) ,  [spring-boot/131-influxdb-java](spring-boot/131-influxdb-java)
- [ ] [Mongo](http://spring.hhui.top/spring-blog/tags/Mongo/)
    - [x] 项目工程
        - 基础环境 [spring-boot/110-mongo-basic](spring-boot/110-mongo-basic)
        - mongoTemplate使用姿势 [spring-boot/111-mongo-template](spring-boot/111-mongo-template)
    - [x] 
      系列博文：[分类: MongoDB | 一灰灰Blog](https://spring.hhui.top/spring-blog/categories/SpringBoot/DB%E7%B3%BB%E5%88%97/MongoDB/)
- [x] [Redis读写](http://spring.hhui.top/spring-blog/tags/Redis/)
    - [x] 项目工程：
        - 基本环境构建 [spring-boot/120-redis-config](spring-boot/120-redis-config)
        - jedis环境构建  [spring-boot/121-redis-jedis-config](spring-boot/121-redis-jedis-config)
        - redisTemplate使用姿势 [spring-boot/122-redis-template](spring-boot/122-redis-template)
        - lettuce环境构建 [spring-boot/123-redis-lettuce-config](spring-boot/123-redis-lettuce-config)
        - redis集群实例工程 [spring-boot/124-redis-cluster](spring-boot/124-redis-cluster)
        - 排行榜应用实例工程 [spring-case/120-redis-ranklist](spring-case/120-redis-ranklist)
        - 站点统计应用实例工程 [spring-case/124-redis-site

[...截断...]

count](spring-case/124-redis-sitecount)
    - [x] 
      系列博文： [分类: Redis | 一灰灰Blog](https://spring.hhui.top/spring-blog/categories/SpringBoot/DB%E7%B3%BB%E5%88%97/Redis/)
- [ ] MemCache
- [] 内存缓存
    - [x] Caffiene
      -
      项目工程： [spring-boot/500-cache-caffeine](spring-boot/500-cache-caffeine) ， [spring-boot/501-cache-caffeine-special](spring-boot/501-cache-caffeine-special)
      -
      关联博文： [分类: Caffiene | 一灰灰Blog](https://spring.hhui.top/spring-blog/categories/SpringBoot/%E4%B8%AD%E9%97%B4%E4%BB%B6/Caffiene/)
    - [ ] Guava
- [ ] InfluxDb
    - [x] 项目工程：[spring-boot/130-influxdb](spring-boot/130-influxdb)
    - [InfluxDB系列博文](https://blog.hhui.top/hexblog/categories/DB/InfluxDB/)
- [x] SpringCache
    - [x] 项目工程：[spring-boot/125-cache-ano](spring-boot/125-cache-ano)
- [ ] 定时器
- [x] 搜索 ES
    - [x] 项目工程: [spring-boot/142-search-es](spring-boot/142-search-es)
    - [x] [ES系列博文](https://spring.hhui.top/spring-blog/tags/ElasticSearch/)
- [x] 搜索 [Solr](http://spring.hhui.top/spring-blog/tags/Solr/)
    - [x] 项目工程：[spring-boot/140-search-solr](spring-boot/140-search-solr)
    - [x] [基本环境搭建](http://spring.hhui.top/spring-blog/2019/05/10/190510-SpringBoot%E9%AB%98%E7%BA%A7%E7%AF%87%E6%90%9C%E7%B4%A2%E4%B9%8BSolr%E7%8E%AF%E5%A2%83%E6%90%AD%E5%BB%BA%E4%B8%8E%E7%AE%80%E5%8D%95%E6%B5%8B%E8%AF%95/)
    - [x] [新增与修改使用说明](http://spring.hhui.top/spring-blog/2019/05/26/190526-SpringBoot%E9%AB%98%E7%BA%A7%E7%AF%87%E6%90%9C%E7%B4%A2Solr%E4%B9%8B%E6%96%87%E6%A1%A3%E6%96%B0%E5%A2%9E%E4%B8%8E%E4%BF%AE%E6%94%B9%E4%BD%BF%E7%94%A8%E5%A7%BF%E5%8A%BF/)

### III. MVC篇

- [x] 过滤器
    - [x] 项目工程:
        - 基本使用姿势：[spring-boot/210-web-filter](spring-boot/210-web-filter)
        - filter优先级: [spring-boot/210-web-filter-order](spring-boot/210-web-filter-order)
- [x] 拦截器
    - [x] 项目工程：[spring-boot/213-web-interceptor](spring-boot/213-web-interceptor)
    - [x] 基本使用姿势: [拦截器](https://spring.hhui.top/spring-blog/tags/Interceptor/)
- [x] Get/Post/Put/Delete等http方法支持
- [x] 参数绑定(get/post参数解析，自定义参数解析器)
    - [x] 项目工程: [spring-boot/202-web-params](spring-boot/202-web-params)
    - [x] [请求参数解析姿势大全](http://spring.hhui.top/spring-blog/tags/%E8%AF%B7%E6%B1%82%E5%8F%82%E6%95%B0/)
- [x] 返回相关
    - [x] 数据返回
        - 项目:[spring-boot/207-web-response](spring-boot/207-web-response)
        - [返回数据姿势大全](http://spring.hhui.top/spring-blog/tags/%E8%BF%94%E5%9B%9E%E6%95%B0%E6%8D%AE/)
    - [x] 视图绑定,
      -
      项目: [spring-boot/204-web-freemaker](spring-boot/204-web-freemaker) | [spring-boot/204-web-thymeleaf](spring-boot/205-web-thymeleaf) [spring-boot/204-web-beetl](spring-boot/206-web-beetl)
        - [spring & 模板引擎构建web项目](http://spring.hhui.top/spring-blog/tags/%E6%A8%A1%E6%9D%BF%E5%BC%95%E6%93%8E/)
    - 返回头
- [x] 异常处理
- [ ] 安全相关(SQL/XSS等注入)
- [ ] 跨域处理
- [ ] WebSocket
    - [x] [websocket基础](http://spring.hhui.top/spring-blog/tags/WebSocket/)
- [ ] reactive
    - [ ] [webflux](https://spring.hhui.top/spring-blog/tags/WebFlux/)

### IV. SpringCloud篇

- [ ] 注册中心
- [ ] 配置中心
- [ ] 网关路由
- [ ] 负载均衡
- [ ] 熔断器
- [ ] 链路监控
- [ ] 安全模块
- [ ] oauth
- [ ] admin

### V. 源码篇

- [ ] 扩展点
    - [x] [项目](spring-extention/)
    - [x] [Spring扩展点专栏](https://spring.hhui.top/spring-blog/categories/Spring%E6%BA%90%E7%A0%81/%E6%89%A9%E5%B1%95%E7%82%B9/)

### VI. 项目说明

<details><summary> 项目说明 </summary>

| 项目                                                                                                                                                                              | 说明                                     | 知识点                                                                                   | 
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------|---------------------------------------------------------------------------------------|
| **SpringBoot**                                                             