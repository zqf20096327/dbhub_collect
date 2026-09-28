[![](https://jitpack.io/v/Areeb-Gillani/vertx-boost-db.svg)](https://jitpack.io/#Areeb-Gillani/vertx-boost-db)
# vertx-boost-db
This project (BoostDB) provides easier ways to write code for a data-access layer. Keeping in mind the learning curve of vertx, this project is designed to be as close to the SpringData layer as possible. This project provides a multi-tenant approach to configuring multiple data sources using connection configuration.
# Background & Basics
### Vertx vs. Spring
Vertx is an event-driven toolkit backed by the Eclipse Foundation. It's a polyglot and is used for highly concurrent code writing. When compared to spring, people usually use hibernate or spring data. They are heavy with their own pros and cons. For instance, in hibernate, one can't bypass its L1 cache. Vertx on the other hand provides lightweight clients for most of the popular databases to get things going. This component covers MySQL, MSSQL, Postgres, Oracle, and DB2 (all built on Vert.x's unified `sqlclient`/`SqlTemplate` stack via `CrudRepository`), plus MongoDB and Cassandra (which have their own client families in Vert.x, so they get their own `MongoRepository`/`CassandraRepository` — see [Usage](#usage) below for why).
### Why Vertx?
When compared to Spring (Webflux or Boot), Vertx is exceptionally fast. In my performance testing, I found Vertex to be 75% faster than Spring. Techempower has also shared more interesting results on their site: https://www.techempower.com/benchmarks/#section=data-r22. Now considering this, if you want to develop a state-of-the art application with high throughput, one should go for vertx, as it is Java's fastest unopinionated framework available today (Techempower's results also back this statement).
### Basics of Vertx
Vertx, out of the box, provides SQL and NoSQL clients. Whereas those clients are event-driven, non-blocking, and have low overhead.
### Why BoostDB?
BoostDB helps you code in a very similar way to what you are used to in Spring. Just because the learning curve of vertx itself is a little tricky, it will also be a bit messy to arrange your code in the best possible way. This project helps you in the best possible way to write performance-efficient code without worrying about the bits and pieces of low-end code.
# Dependency
### Repository
#### build.gradle
```kotlin
allprojects {
        repositories {
            maven ("https://jitpack.io")
        }
    }
```
#### pom.xml
```xml
<repositories>
  ...
  <repository>
      <id>jitpack.io</id>
      <url>https://jitpack.io</url>
  </repository>
</repositories>
```
### Dependency
#### build.gradle
```kotlin
dependencies {
  implementation ("com.github.Areeb-Gillani:vertx-boost-db:2.1.1")
}
```
#### pom.xml
```xml
<dependencies>
  ...
	<dependency>
	    <groupId>com.github.Areeb-Gillani</groupId>
	    <artifactId>vertx-boost-db</artifactId>
	    <version>2.1.1</version>
	</dependency>
</dependencies>
```
# Config
One can add multiple connection configurations in this way, and upon creating the repository, please make sure you pass the right connection name so that if the connection is not available in the application, it will be created.

```json
{
  "dbConnections": {
    "Primary": {
      "dbName": "example_database",
      "dbHost":"localhost",
      "dbPort": 3306,
      "dbUsername": "root",
      "dbPassword": "password",
      "dbConnectionPoolSize": 10,
      "dbType": "MYSQL",
      "dbRetryCount": 5,
      "dbRetryInterval": 1000
    },
    "MySecondConnection": {
      "dbName": "example_database",
      "dbHost":"192.168.1.10",
      "dbPort": 1521,
      "dbUsername": "root",
      "dbPassword": "password",
      "serviceName":"o19c"
      "dbConnectionPoolSize": 10,
      "dbType": "ORACLE",
      "dbRetryCount": 5,
      "dbRetryInterval": 1000
    },
    "MyMongoConnection": {
      "dbName": "example_database",
      "dbHost": "localhost",
      "dbType": "MONGODB"
    },
    "MyCassandraConnection": {
      "dbName": "example_keyspace",
      "dbHost": "localhost",
      "dbType": "CASSANDRA"
    }
  }
}
```
`dbPort` can be omitted for any type above - it defaults to the vendor-conventional port (MySQL 3306, Postgres 5432, MSSQL 1433, Oracle 1521, DB2 50000, MongoDB 27017, Cassandra 9042). `dbUsername`/`dbPassword` can also be omitted for MongoDB and Cassandra (unauthenticated local/dev instances are common for both); every relational connection still requires a username.

# Usage
### Relational (MySQL, Postgres, MSSQL, Oracle, DB2)
These five share Vert.x's unified sqlclient stack, so they're all just CrudRepository. Its factory picks the right connection type from the dbType attribute in your connection configuration - you don't need a per-vendor repository class.

```java
@Repository("MyDbConfig")
public class DatabaseRepo extends CrudRepository<ExampleModel>{
   public DatabaseRepo (String connectionName, JsonObject config){
      super(connectionName, config);
   }
    //Write other db operations here your CRUD operations are already covered above 
}
```
VertxBoost's ([![](https://jitpack.io/v/Areeb-Gillani/vertx-boost.svg)](https://jitpack.io/#Areeb-Gillani/vertx-boost)) service class has been used in order to demo the usage
```java
@Service("SomeWorker")
public class ExampleService extends AbstractService {
    @Autowired
    DatabaseRepo repo;
    //Please code other related stuff here.
}
```
### MongoDB and Cassandra
Vert.x's Mongo and Cassandra clients are not part of the sqlclient family - no Pool, no SqlConnectOptions, no SqlTemplate/RowMapper. They're wrapped by MongoCrudRepository/CassandraCrudRepository instead. The verbs (save/update/delete/read/saveOrUpdate) match CrudRepository on purpose, but the parameters are native to each store - a JsonObject filter and collection name for Mongo, a CQL string with positional ? placeholders for Cassandra - rather than forced into the SQL-shaped signature.

```java
@Repository("MyMongoConnection")
public class MongoDatabaseRepo extends MongoCrudRepository<ExampleModel> {
    public MongoDatabaseRepo(String connectionName, JsonObject config) {
        super(connectionName, config);
    }
}
```
```java
@Repository("MyCassandraConnection")
public class CassandraDatabaseRepo extends CassandraCrudRepository<ExampleModel> {
    public CassandraDatabaseRepo(String connectionName, JsonObject config) {
        super(connectionName, config);
    }
}
```
Cassandra's read also takes a Function<Row, T> mapper you supply yourself - the driver has no built-in POJO mapping the way Mongo's JsonObject.mapTo() or SQL's codegen RowMapper do.

#### Note: Please include the specific client driver in your build.gradle in order to make this code work.
```kotlin
    dependencies{
          implementation ("io.vertx:vertx-mysql-client:5.1.5")
          // or vertx-pg-client / vertx-mssql-client / vertx-oracle-client / vertx-db2-client
          // or vertx-mongo-client / vertx-cassandra-client
    }
```
