# *If you just want to level up to Spring Boot 4 with Hibernate 7 then follow this [repo](https://github.com/AnghelLeonard/Hibernate-SpringBoot-4)*

[![Tweet](https://img.shields.io/twitter/url/http/shields.io.svg?style=social)](https://twitter.com/intent/tweet?text=Collection%20of%20best%20practices%20for%20Java%20persistence%20performance%20in%20Spring%20Boot%20applications&url=https://github.com/AnghelLeonard/Hibernate-SpringBoot&hashtags=springdata,hibernate,jpa,springboot)

# Best Performance Practices Hibernate 5/6 & Spring Boot 2

<table>
     <tr><td><b>If you need a deep dive into the performance recipes exposed in this repository then I am sure that you will love my book "Spring Boot Persistence Best Practices"</b></td><td><b>If you need a hand of tips and illustrations of 100+ Java persistence performance issues then "Java Persistence Performance Illustrated Guide" is for you.</b></td></tr>
     <tr><td>
<a href="https://www.apress.com/us/book/9781484256251"><p align="left"><img src="https://github.com/AnghelLeonard/Hibernate-SpringBoot/blob/master/Spring%20Boot%20Persistence%20Best%20Practices.jpg" height="500" width="450"/></p></a>
</td><td>
<a href="https://leanpub.com/java-persistence-performance-illustrated-guide"><p align="right"><img src="https://github.com/AnghelLeonard/Hibernate-SpringBoot/blob/master/Java%20Persistence%20Performance%20Illustrated%20Guide.jpg" height="500" width="450"/></p></a>
</td></tr></table>

**Hibernate & Spring Boot Samples**

1. **[How To Store UTC Timezone In MySQL](https://github.com/AnghelLeonard/Hibernate/tree/master/HibernateSpringBootUTCTimezone)**

**Description:** This application is a sample of how to store date, time, and timestamps in UTC time zone. The second setting, `useLegacyDatetimeCode` is needed only for MySQL. Otherwise, set only `hibernate.jdbc.time_zone`.

**Key points:**
- `spring.jpa.properties.hibernate.jdbc.time_zone=UTC`
- `spring.datasource.url=jdbc:mysql://localhost:3306/screenshotdb?useLegacyDatetimeCode=false`
     
-----------------------------------------------------------------------------------------------------------------------    

2. **[View Binding/Extracted Params Via Log4J 2](https://github.com/AnghelLeonard/Hibernate-SpringBoot/tree/master/HibernateSpringBootLog4j2ViewBindingParameters)**

**Description:** View the prepared statement binding/extracted parameters via Log4J 2 logger setting.

**Key points:**
- for Maven, in `pom.xml`, exclude Spring Boot's Default Logging
- for Maven, in `pom.xml`, Add Log4j 2 Dependency
- in `log4j2.xml` add, `<Logger name="org.hibernate.type.descriptor.sql" level="trace"/>`
   
**Output example:**
![](https://github.com/AnghelLeonard/Hibernate-SpringBoot/blob/master/HibernateSpringBootLog4j2ViewBindingParameters/log4j2%20display%20binding%20and%20extracted%20parameters.png)

-----------------------------------------------------------------------------------------------------------------------    

3. **[How To View Query Details Via DataSource-Proxy Library](https://github.com/AnghelLeonard/Hibernate-SpringBoot/tree/master/HibernateSpringBootDataSourceProxy)**

**Description:** View the query details (query type, binding parameters, batch size, execution time, etc) via **[DataSource-Proxy](https://github.com/ttddyy/datasource-proxy)**

**Key points:**
- for Maven, add in `pom.xml` the `datasource-proxy` dependency
- create an bean post processor to intercept the `DataSource` bean
- wrap the `DataSource` bean via `ProxyFactory` and an implementation of `MethodInterceptor`

**Output example:**\
![](https://github.com/AnghelLeonard/Hibernate-SpringBoot/blob/master/HibernateSpringBootDataSourceProxy/query%20details%20via%20datasource-proxy.png)

-----------------------------------------------------------------------------------------------------------------------    

4. **[Batch Inserts via `saveAll(Iterable<S> entities)` in MySQL](https://github.com/AnghelLeonard/Hibernate-SpringBoot/tree/master/HibernateSprin

[...截断...]

gBootBatchInsertsJpaRepository)**

**Description:** Batch inserts via `SimpleJpaRepository#saveAll(Iterable<S> entities)` method in MySQL

**Key points:**
- in `application.properties` set `spring.jpa.properties.hibernate.jdbc.batch_size`
- in `application.properties` set `spring.jpa.properties.hibernate.generate_statistics` (just to check that batching is working)
- in `application.properties` set JDBC URL with `rewriteBatchedStatements=true` (optimization for MySQL)
- in `application.properties` set JDBC URL with `cachePrepStmts=true` (enable caching and is useful if you decide to set `prepStmtCacheSize`, `prepStmtCacheSqlLimit`, etc as well; without this setting the cache is disabled)
- in `application.properties` set JDBC URL with `useServerPrepStmts=true` (this way you switch to server-side prepared statements (may lead to signnificant performance boost))
- in case of using a parent-child relationship with cascade persist (e.g. one-to-many, many-to-many) then consider to set up `spring.jpa.properties.hibernate.order_inserts=true` to optimize the batching by ordering inserts
- in entity, use the [assigned generator](https://vladmihalcea.com/how-to-combine-the-hibernate-assigned-generator-with-a-sequence-or-an-identity-column/) since MySQL `IDENTITY` will cause insert batching to be disabled
- in entity, add `@Version` property to avoid extra-`SELECT` statements fired before batching (also prevent lost updates in multi-request transactions). Extra-`SELECT` statements are the effect of using `merge()` instead of `persist()`; behind the scene, `saveAll()` uses `save()`, which in case of non-new entities (entities that have IDs) will call `merge()`, which instruct Hibernate to fire a `SELECT` statement to make sure that there is no record in the database having the same identifier
- pay attention on the amount of inserts passed to `saveAll()` to not "overwhelm" the Persistence Context; normally the `EntityManager` should be flushed and cleared from time to time, but during the `saveAll()` execution you simply cannot do that, so if in `saveAll()` there is a list with a high amount of data, all that data will hit the Persistence Context (1st Level Cache) and will remain in memory until the flush time; using relatively small amount of data should be ok (in this example, each batch of 30 entities run in a separate transaction and Persistent Context)
- the `saveAll()` method return a `List<S>` containing the persisted entities; each persisted entity is added into this list; if you just don't need this `List` then it is created for nothing
- if is not needed, then ensure that Second Level Cache is disabled via `spring.jpa.properties.hibernate.cache.use_second_level_cache=false`

-----------------------------------------------------------------------------------------------------------------------    

5. **[Batch Inserts Via EntityManager (MySQL)](https://github.com/AnghelLeonard/Hibernate-SpringBoot/tree/master/HibernateSpringBootBatchInsertsEntityManager)**

**Description:** This application is a sample of batching inserts via `EntityManager` in MySQL. This way you can easily control the `flush()` and `clear()` cycles of the Persistence Context (1st Level Cache) inside the current transaction. This is not possible via Spring Boot, `saveAll(Iterable<S> entities)`, since this method executes a single flush per transaction. Another advantage is that you can call `persist()` instead of `merge()` - this is used behind the scene by the SpringBoot `saveAll(Iterable<S> entities)` and `save(S entity)`.

If you want to execute a batch per transaction (recommended) then check this [example](https://github.com/AnghelLeonard/Hibernate-SpringBoot/tree/master/HibernateSpringBootBatchInsertsEntityManagerBatchPerTransaction).

**Key points:**
- in `application.properties` set `spring.jpa.properties.hibernate.jdbc.batch_size`
- in `application.properties` set `spring.jpa.properties.hibernate.generate_statistics` (just to check that batching is work