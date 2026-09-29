# akka-persistence-tidb-sample

A sample application integrates akka-persistence and TiDB.

This application uses following akka features.

- akka-persistence-typed
- akka-persistence-jdbc
- akka-serialization-jackson

## Usage

### Start TiDB services

```
cd tidb-docker-compose
docker-compose up
```

### Create database

Connect to the TiDB with mysql client which is in `tispark-master` service.

````
cd tidb-docker-compose
docker-compose exec tispark-master mysql -h tidb -P 4000 -u root
````

Create a database.

```sql
CREATE DATABASE IF NOT EXISTS akka;
```

Switch to the database created in the previous step.

```sql
use akka;
```

Execute following SQL to create tables.

- [akka-persistence-jdbc/mysql-schema.sql at v4.0.0](https://github.com/akka/akka-persistence-jdbc/blob/v4.0.0/core/src/test/resources/schema/mysql/mysql-schema.sql)

### Start the application

```
sbt run
```

### Create a user

```
curl -X POST http://127.0.0.1:8080/users \
    -H 'Content-Type: application/json' \
    -d '{ "name": "test", "age": 28, "countryOfResidence": "japan"  }'
```

#### Get a user

```
curl -X GET http://127.0.0.1:8080/users/test
```

### Get all users

```
curl -X GET http://127.0.0.1:8080/users
```

### Delete a user

```
curl -X DELETE http://127.0.0.1:8080/users/test
```
