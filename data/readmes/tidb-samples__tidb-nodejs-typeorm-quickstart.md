# Connect to TiDB with ORM framework TypeORM

[![Language](https://img.shields.io/badge/Language-TypeScript-3178c6.svg)](https://nodejs.org/en)
[![Driver](https://img.shields.io/badge/ORM-TypeORM-fe0902.svg)](https://typeorm.io/)

The following guide will show you how to connect to the TiDB cluster with Node.js ORM framework [TypeORM](https://typeorm.io/) and perform basic SQL operations like create, read, update, and delete.

> **Note**
>
> TiDB is a MySQL-compatible database, which means you can connect to a TiDB cluster in your application using the familiar driver/ORM framework from the MySQL ecosystem.
>
> The only difference is that if you connect to a TiDB Serverless cluster with public endpoint, you **MUST** [enable TLS connection on TypeORM](#4-set-up-the-environment-variables).

## Prerequisites

To complete this guide, you need:

- [Node.js](https://nodejs.org/en) >= 16.x installed on your machine
- [Git](https://git-scm.com/downloads) installed on your machine
- A TiDB cluster running

**If you don't have a TiDB cluster yet, please create one with one of the following methods:**

1. (**Recommend**) [Start up a TiDB Serverless cluster](https://tidbcloud.com/free-trial?utm_source=github&utm_medium=quickstart) instantly with a few clicks on TiDB Cloud.
2. [Start up a TiDB Playground cluster](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster) with TiUP CLI on your local machine.

## Getting started

This section demonstrates how to run the sample application code and connect to TiDB with Node.js ORM framework [TypeORM](https://www.typeORM.io/).

### Step 1. Clone the repository

Run the following command to clone the sample code locally：

```shell
git clone https://github.com/tidb-samples/tidb-nodejs-typeorm-quickstart.git
cd tidb-nodejs-typeorm-quickstart
```

### Step 2. Install dependencies

Run the following command to install the dependencies (including the `typeorm` and `mysql2` package) required by the sample code：

```shell
npm install
```

<details>
<summary><b>Install dependencies to existing project</b></summary>

For your existing project, run the following command to install the packages:

- `typeorm`: The ORM framework for Node.js.
- `mysql2`: The MySQL driver for Node.js. (You can also use `mysql` as the driver)
- `dotenv`: The package to load environment variables from `.env` file.
- `decimal.js`: The package to handle decimal numbers.

```shell
npm install typeorm mysql2 dotenv decimal.js --save
```

- `@types/node`: The package to provide TypeScript type definitions for Node.js.
- `ts-node`: The package to execute TypeScript code directly without compiling.
- `typescript`: The package to compile TypeScript code to JavaScript.

```shell
npm install @types/node ts-node typescript --save-dev
```

</details>

### Step 3. Provide connection parameters

<details open>
<summary><b>(Option 1) TiDB Serverless</b></summary>

1. Navigate to the [Clusters](https://tidbcloud.com/console/clusters) page, and then click the name of your target cluster to go to its overview page.
2. Click **Connect** in the upper-right corner.
3. In the connection dialog, select `General` from the **Connect With** dropdown and keep the default setting of the **Endpoint Type** as `Public`.
4. If you have not set a password yet, click **Create password** to generate a random password.

    <div align="center">
        <picture>
            <source media="(prefers-color-scheme: dark)" srcset="./static/images/tidb-cloud-connect-dialog-dark-theme.png" width="600">
            <img alt="The connection dialog of TiDB Serverless" src="./static/images/tidb-cloud-connect-dialog-light-theme.png" width="600">
        </picture>
        <div><i>The connection dialog of TiDB Serverless</i></div>
    </div>

5. Make a copy of the `.env.example` file to the `.env` file:

   ```shell
   cp .env.example .env
   ```

6. Edit the `.env` file, copy the connection parameters on the connection dialog, and replace the corresponding placeholders `{}`. The example configuration is as follows:

    ```dotenv
    TIDB_HOST={host}
    TIDB_PORT=4000
    TIDB_USER={user}
    TIDB_PASSWORD={password}
    TIDB_DATABASE=test
    TIDB_ENABLE_SSL=true
    ```

   > **Note**
   >
   > Modify `TIDB_ENABLE_SSL` to `true` to enable a TLS connection. (Required for public endpoint)

</details>

<details>
<summary><b>(Option 2) TiDB Dedicated</b></summary>

You can obtain the database connection parameters on [TiDB Cloud's Web Console](https://tidbcloud.com/console) through the following steps:

1. Navigate to the [Clusters](https://tidbcloud.com/console/clusters) page, and then click the name of your target cluster to go to its overview page.
2. Click **Connect** in the upper-right corner. A connection dialog is displayed.
3. Click **Allow Access from Anywhere**, and then click **Download TiDB cluster CA** to download the CA certificate.
4. Select `General` from the **Connect With** dropdown and select `Public` from the **Endpoint Type** dropdown.
5. Run the following command to copy `.env.example` and rename it to `.env`:

    ```shell
    cp .env.example .env
    ```

6. Edit the `.env` file, copy the connection parameters on the connection dialog, and replace the corresponding placeholders `{}`. The example configuration is as follows:

    ```dotenv
    TIDB_HOST={host}
    TIDB_PORT=4000
    TIDB_USER={user}
    TIDB_PASSWORD={password}
    TIDB_DATABASE=test
    TIDB_ENABLE_SSL=true
    TIDB_CA_PATH=/path/to/ca.pem
    ```

   > **Note**
   >
   > Modify `TIDB_ENABLE_SSL` to `true` to enable a TLS connection and using `TIDB_CA_PATH` to specify the file path of CA certificate downloaded from the connection dialog.

</details>

<details>
<summary><b>(Option 3) TiDB Self-Hosted</b></summary>

1. Make a copy of the `.env.example` file to the `.env` file.

   ```shell
   cp .env.example .env
   ```

2. Replace the placeholders for `<host>`, `<user>`, and `<password>` with the connection parameters of your TiDB cluster.

    ```dotenv
    TIDB_HOST=<host>
    TIDB_PORT=4000
    TIDB_USER=<user>
    TIDB_PASSWORD=<password>
    TIDB_DATABASE=test
    # TIDB_ENABLE_SSL=true
    # TIDB_CA_PATH=/path/to/ca.pem
    ```

   The TiDB Self-Hosted cluster using non-encrypted connection between TiDB's server and clients by default.

   If you want to enable TLS connection, please uncomment the `TIDB_ENABLE_SSL` and `TIDB_CA_PATH` options and specify the file path of CA certificate defined with [`ssl-ca`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#ssl-ca) option.

</details>

### Step 4. Create the database schema

Run following command to invoke TypeORM CLI] to initialize the database with the SQL statements written in the [migration files](src/migrations):

```shell
npm run migration:run
```

<details>
<summary><b>Expected execution output</b></summary>

The following SQL statements create a `players` table and a `profiles` table, and the two tables are associated through foreign keys.

```
query: SELECT VERSION() AS `version`
query: SELECT * FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_SCHEMA` = 'test' AND `TABLE_NAME` = 'migrations'
query: CREATE TABLE `migrations` (`id` int NOT NULL AUTO_INCREMENT, `timestamp` bigint NOT NULL, `name` varchar(255) NOT NULL, PRIMARY KEY (`id`)) ENGINE=InnoDB
query: SELECT * FROM `test`.`migrations` `migrations` ORDER BY `id` DESC
0 migrations are already loaded in the database.
1 migrations were found in the source code.
1 migrations are new migrations must be executed.
query: START TRANSACTION
query: CREATE TABLE `profiles` (`player_id` int NOT NULL, `biography` text NOT NULL, PRIMARY KEY (`player_id`)) ENGINE=InnoDB
query: CREATE TABLE `players` (`id` int NOT NULL AUTO_INCREMENT, `name` varchar(50) NOT NULL, `coins` decimal NOT NULL, `goods` int NOT NULL, `created_at` datetime NOT NULL, `profilePlayerId` int NULL, UNIQUE INDEX `uk_players_on_name` (`name`), UNIQUE INDEX `REL_b9666644b90ccc5065993425ef` (`profilePlayerId`), PRIMARY KEY (`id`)) ENGINE=InnoDB
query: ALTER TABLE `players` ADD CONSTRAINT `fk_profiles_on_player_id` FOREIGN KEY (`profilePlayerId`) REFERENCES `profiles`(`player_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
query: INSERT INTO `test`.`migrations`(`timestamp`, `name`) VALUES (?, ?) -- PARAMETERS: [1693814724825,"Init1693814724825"]
Migration Init1693814724825 has been  executed successfully.
query: COMMIT
```

</details>

The migration files are generated based on the entities defined in [`src/entities`](src/entities) folder. To learn how to define entities in TypeORM, please check the [Entities](https://typeorm.io/entities) documentation.

### Step 5. Run the sample code

Run the following command to execute the sample code:

```shell
npm start
```

**Expected execution output**

If the connection is successful, the terminal will output the version of the TiDB cluster as follows:

```
🔌 Connected to TiDB cluster! (TiDB version: 5.7.25-TiDB-v7.1.0)
🆕 Created a new player with ID 2.
ℹ️ Got Player 2: Player { id: 2, coins: 100, goods: 100 }
🔢 Added 50 coins and 50 goods to player 2, now player 2 has 100 coins and 150 goods.
🚮 Deleted 1 player data.
```

## Sample code snippets

### Connect with connection options

The following code establish a connection to TiDB with options defined in environment variables:

```typescript
// src/dataSource.ts

// Load environment variables from .env file to process.env.
require('dotenv').config();

export const AppDataSource = new DataSource({
  type: "mysql",
  host: process.env.TIDB_HOST || '127.0.0.1',
  port: process.env.TIDB_PORT ? Number(process.env.TIDB_PORT) : 4000,
  username: process.env.TIDB_USER || 'root',
  password: process.env.TIDB_PASSWORD || '',
  database: process.env.TIDB_DATABASE || 'test',
  ssl: process.env.TIDB_ENABLE_SSL === 'true' ? {
    minVersion: 'TLSv1.2',
    ca: process.env.TIDB_CA_PATH ? fs.readFileSync(process.env.TIDB_CA_PATH) : undefined
  } : null,
  synchronize: process.env.NODE_ENV === 'development',
  logging: false,
  entities: [Player, Profile],
  migrations: [__dirname + "/migrations/**/*{.ts,.js}"],
});
```

> **Note**
>
> For TiDB Serverless, you MUST enable TLS connection when using public endpoint. In this sample code, please set up the environment variable `TIDB_ENABLE_SSL` in the `.env` file to `true`.
> 
> However, you **don't** have to specify an SSL CA certificate via `TIDB_CA_PATH`, because Node.js uses the built-in [Mozilla CA certificate](https://wiki.mozilla.org/CA/Included_Certificates) by default, which is trusted by TiDB Serverless.

### Insert data

The following query creates a single `Player` record, and returns the created `player` object, which contains the `id` field that is automatically generated by TiDB:

```typescript
const player = new Player('Alice', 100, 100);
await this.dataSource.manager.save(player);
```

For more information, refer to [Insert data](https://docs.pingcap.com/tidbcloud/dev-guide-insert-data).

### Query data

The following query returns a single `Player` object with ID 101 or `null` if no record is found:

```typescript
const player: Player | null = await this.dataSource.manager.findOneBy(Player, {
  id: id
});
```

For more information, refer to the [Query data](https://docs.pingcap.com/tidbcloud/dev-guide-get-data-from-single-table).

### Update data

The following query adds 50 goods to the `Player` with ID 101:

```typescript
const player = await this.dataSource.manager.findOneBy(Player, {
  id: 101
});
player.goods += 50;
await this.dataSource.manager.save(player);
```

For more information, refer to [Update data](https://docs.pingcap.com/tidbcloud/dev-guide-update-data).

### Delete data

The following query deletes the `Player` with ID 101:

```typescript
await this.dataSource.manager.delete(Player, {
  id: 101
});
```

For more information, refer to [Delete data](https://docs.pingcap.com/tidbcloud/dev-guide-delete-data).

### Execute raw queries

The following query executes a raw SQL query and returns the version of the TiDB cluster:

```typescript
const rows = await dataSource.query('SELECT VERSION() AS tidb_version;');
console.log(rows[0]['tidb_version']);
```

For more information, refer to the documentation of TypeORM [DataSource API](https://typeorm.io/data-source-api).

## Best practices

### Foreign key constraint

Using foreign key constraints can add checks on the database side to ensure the [referential integrity](https://en.wikipedia.org/wiki/Referential_integrity) of data, but they might lead to serious performance issues when there is a large amount of data.

You can control whether foreign key constraints are created when constructing relationships between entities by using the `createForeignKeyConstraints` option (default `true`).

```typescript
@Entity()
export class ActionLog {
    @PrimaryColumn()
    id: number

    @ManyToOne((type) => Person, {
        createForeignKeyConstraints: false,
    })
    person: Person
}
```

For more information, refer to the [TypeORM FAQ](https://typeorm.io/relations-faq#avoid-foreign-key-constraint-creation) and [FOREIGN KEY constraints](https://docs.pingcap.com/tidbcloud/foreign-key#foreign-key-constraints).

## What's next

- Learn more about TypeORM from the [documentation](https://typeorm.io/#/).
- Explore the real-time analytics feature on the [TiDB Cloud Playground](https://play.tidbcloud.com/real-time-analytics).
- Read the [TiDB Developer Guide](https://docs.pingcap.com/tidbcloud/dev-guide-overview) to learn more details about application development with TiDB.
  - [HTAP Queries](https://docs.pingcap.com/tidbcloud/dev-guide-hybrid-oltp-and-olap-queries)
  - [Transaction](https://docs.pingcap.com/tidbcloud/dev-guide-transaction-overview)
  - [Optimizing SQL Performance](https://docs.pingcap.com/tidbcloud/dev-guide-optimize-sql-overview)
