# TiDB Example - Java JDBC

## Initial database and table

Use [dbinit.sql](src/main/resources/dbinit.sql) to create `bank` database and `accounts` table.

```sql
SET sql_safe_updates = FALSE;

USE mysql;
DROP DATABASE IF EXISTS bank;
CREATE DATABASE IF NOT EXISTS bank;

USE bank;

CREATE TABLE accounts (
    `id` VARCHAR(36),
    `balance` INTEGER,
	PRIMARY KEY (`id`)
);
```

## Install maven

If you have configured `Maven`, skip this part.

To install Maven on macOS, run the following command:

```brew install maven```

To install Maven on a Debian-based Linux distribution like Ubuntu:

```apt-get install maven```

To install Maven on a Red Hat-based Linux distribution like Fedora:

```dnf install maven```

For other ways to install Maven, see its official [documentation](https://maven.apache.org/install.html).

## Build 

Note: It will taken sooooo long when you first time run it, must be more patience.

```mvn clean package```

## Run

Run the jar with dependencies:

```java -jar target/tidb-example-java-jdbc-0.0.1-jar-with-dependencies.jar```

And then, you will see the result of example:

```shell
cheese@CheesedeMacBook-Pro tidb-example-java-jdbc % java -jar target/tidb-example-java-jdbc-0.0.1-jar-with-dependencies.jar

[updateAccounts]:
    'com.mysql.cj.jdbc.ClientPreparedStatement: INSERT INTO accounts (id, balance) VALUES ('4eda0277-1da1-47eb-86fe-530b61fe6f00', 250)'

[updateAccounts]:
    'com.mysql.cj.jdbc.ClientPreparedStatement: INSERT INTO accounts (id, balance) VALUES ('76995b64-bf94-4d1c-b06f-3184820e50a2', 1000)'
ExampleDataDAO.updateAccounts:
    => 2 total updated accounts
main:
    => Account balances at time '18:21:16.519458':
    ID 1 => $1000
    ID 2 => $250

[transferFunds]:
    'com.mysql.cj.jdbc.ClientPreparedStatement: INSERT INTO accounts (id, balance) VALUES ('76995b64-bf94-4d1c-b06f-3184820e50a2', (( SELECT balance FROM accounts WHERE id = '76995b64-bf94-4d1c-b06f-3184820e50a2' ) - 100 )), ('4eda0277-1da1-47eb-86fe-530b61fe6f00', (( SELECT balance FROM accounts WHERE id = '4eda0277-1da1-47eb-86fe-530b61fe6f00' ) + 100 )) ON DUPLICATE KEY UPDATE balance = VALUES(balance)'
ExampleDataDAO.transferFunds:
    => $100 transferred between accounts 76995b64-bf94-4d1c-b06f-3184820e50a2 and 4eda0277-1da1-47eb-86fe-530b61fe6f00, 4 rows updated
main:
    => Account balances at time '18:21:16.571599':
    ID 1 => $900
    ID 2 => $350

ExampleDataDAO.bulkInsertRandomAccountData:
    'com.mysql.cj.jdbc.ClientPreparedStatement: INSERT INTO accounts (id, balance) VALUES ('aa1a5526-9413-4e6f-bc2c-61e1c707ee55', 832767234)'
    => 100 row(s) updated in this batch

ExampleDataDAO.bulkInsertRandomAccountData:
    'com.mysql.cj.jdbc.ClientPreparedStatement: INSERT INTO accounts (id, balance) VALUES ('bee22fe2-befb-4dc1-8504-acdf746dc5ea', 18439597)'
    => 100 row(s) updated in this batch

ExampleDataDAO.bulkInsertRandomAccountData:
    'com.mysql.cj.jdbc.ClientPreparedStatement: INSERT INTO accounts (id, balance) VALUES ('84ce1dd1-eefa-482e-bd93-802a0b02dbb0', 340197694)'
    => 100 row(s) updated in this batch

ExampleDataDAO.bulkInsertRandomAccountData:
    'com.mysql.cj.jdbc.ClientPreparedStatement: INSERT INTO accounts (id, balance) VALUES ('5575e17b-99f0-45a1-807e-f9abc00d06cf', 443655887)'
    => 100 row(s) updated in this batch

ExampleDataDAO.bulkInsertRandomAccountData:
    'com.mysql.cj.jdbc.ClientPreparedStatement: INSERT INTO accounts (id, balance) VALUES ('6a78223a-69e7-4785-ad32-719429a1eb2d', 727708267)'
    => 100 row(s) updated in this batch

ExampleDataDAO.bulkInsertRandomAccountData:
    => finished, 500 total rows inserted

[readAccounts]:
    'com.mysql.cj.jdbc.ClientPreparedStatement: SELECT id, balance FROM accounts LIMIT 10'
    id       => 46d16a7f-addf-4398-98a6-7fb07365fd9e
    balance  =>        900
    id       => 4dab9a27-a595-4ef3-bd8e-999b888ef2a5
    balance  =>        350
    id       => d5993a6f-86d2-490a-8531-2b67b62ee0cf
    balance  =>  462064494
    id       => 13bd7757-f06c-4bfb-a1a7-a15985761197
    balance  =>  739003150
    id       => 650c1b9e-2bb1-4405-9823-f37fafabc61a
    balance  =>  275945148
    id       => 825549e6-d4fd-437d-9930-a87714a0b566
    balance  =>  851495285
    id       => b596fcc2-f142-4bbf-8634-f0446b1e57b1
    balance  =>  337337199
    id       => c9b0adec-4be2-4537-b93b-72df8992d3b1
    balance  =>  243802065
    id       => 5f56eea3-a2e1-47c6-8ba3-ee5ba08ffc65
    balance  =>  719219129
    id       => 91cb1d34-e2d9-4f17-ae3e-33090d459cce
    balance  =>    7478440
```