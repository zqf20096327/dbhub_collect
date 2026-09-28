# TiDB Serverless Node.js & Sequelize Quickstart

![Static Badge](https://img.shields.io/badge/-TypeScript-white?logo=typescript)
![Static Badge](https://img.shields.io/badge/Node.js-%20%3E%3D%2018-%20?logo=nodedotjs)
![Static Badge](https://img.shields.io/badge/ORM-Sequelize-blue?logo=sequelize)

This is a quickstart project for using TiDB Serverless with Node.js, Sequelize and TypeScript.

- Driver: [MySQL2](https://github.com/sidorares/node-mysql2)
- ORM: [Sequelize](https://sequelize.org/)
- Language: [TypeScript](https://www.typescriptlang.org/)

## Prerequisites

- [TiDB Serverless cluster](https://www.pingcap.com/tidb-serverless/)
- [Node.js](https://nodejs.org/en/) >= 18.0.0
- [Yarn](https://yarnpkg.com/) >= 1.22.0

## Development

### 1. Connect to TiDB Serverless

> Note:
>
> If you choose self-hosted TiDB, you should set the `TIDB_ENABLE_SSL` environment variable to `false`, and set the `CA_PATH` environment variable empty. Or remove the `TIDB_ENABLE_SSL` and `CA_PATH` in `.env` file.

Refer to [src/lib/tidb.ts](src/lib/tidb.ts).

```typescript
import { Sequelize } from 'sequelize';
import { readFileSync } from 'fs';

export function initSequelize() {
  return new Sequelize({
    dialect: 'mysql',
    host: process.env.TIDB_HOST || 'localhost',
    port: Number(process.env.TIDB_PORT) || 4000,
    username: process.env.TIDB_USER || 'root',
    password: process.env.TIDB_PASSWORD || '',
    database: process.env.TIDB_DB_NAME || 'test',
    dialectOptions: {
      ssl:
        process.env?.TIDB_ENABLE_SSL === 'true'
          ? {
              minVersion: 'TLSv1.2',
              rejectUnauthorized: true,
              ca: process.env.TIDB_CA_PATH
                ? readFileSync(process.env.TIDB_CA_PATH)
                : undefined,
            }
          : null,
    },
  });
}

export async function getSequelize() {
  if (!sequelize) {
    sequelize = initSequelize();
    try {
      await sequelize.authenticate();
      logger.info('Connection has been established successfully.');
    } catch (error) {
      logger.error('Unable to connect to the database:');
      logger.error(error);
      throw error;
    }
  }
  return sequelize;
}
```

### 2. Define a model

Refer to [src/lib/model.ts](src/lib/model.ts).

```typescript
export function getPlayersModel(sequelize: Sequelize) {
  // CREATE TABLE players (
  //     `id` INT(11) NOT NULL AUTO_INCREMENT COMMENT 'The unique ID of the player.',
  //     `coins` INT(11) COMMENT 'The number of coins that the player had.',
  //     `goods` INT(11) COMMENT 'The number of goods that the player had.',
  //     PRIMARY KEY (`id`)
  // );
  Players.init(
    {
      // Model attributes are defined here
      id: {
        type: DataTypes.INTEGER,
        allowNull: false,
        autoIncrement: true,
        primaryKey: true,
        comment: 'The unique ID of the player.',
      },
      coins: {
        type: DataTypes.INTEGER,
        allowNull: false,
        comment: 'The number of coins that the player had.',
      },
      goods: {
        type: DataTypes.INTEGER,
        allowNull: false,
        comment: 'The number of goods that the player had.',
      },
    },
    {
      // Other model options go here
      sequelize, // We need to pass the connection instance
      modelName: 'players', // We need to choose the model name
    }
  );
  return Players;
}
```

### 3. Sync Model and Create Table

This creates the table, dropping it first if it already existed.

Refer to [src/app.ts#L21](src/app.ts#L21).

```typescript
await playersModel.sync({ force: true });
```

### 4. CRUD operations

#### 4.1 Create

Refer to [src/app.ts#L42](src/app.ts#L42).

```typescript
const newPlayer = await playersModel.create({
  id: 6,
  coins: 600,
  goods: 600,
});
logger.info('Created a new player.');
logger.info(newPlayer.toJSON());
```

#### 4.2 Read

Refer to [src/app.ts#L52](src/app.ts#L52).

```typescript
const allPlayersWithCoinsGreaterThan300 = await playersModel.findAll({
  where: {
    coins: {
      [Op.gt]: 300,
    },
  },
});
logger.info('Read all players with coins > 300.');
logger.info(allPlayersWithCoinsGreaterThan300.map((p) => p.toJSON()));
```

#### 4.3 Update

Refer to [src/app.ts#L64](src/app.ts#L64).

```typescript
await newPlayer.update({ coins: 700, goods: 700 });
logger.info('Updated the new player.');
logger.info(newPlayer.toJSON());
```

#### 4.4 Delete

Refer to [src/app.ts#L70](src/app.ts#L70).

```typescript
await newPlayer.destroy();
const deletedNewPlayer = await playersModel.findByPk(6);
logger.info('Deleted the new player.');
logger.info(deletedNewPlayer?.toJSON());
```

## Run the project locally

1. Clone the project

```bash
git clone git@github.com:tidb-samples/tidb-nodejs-sequelize-quickstart.git
cd tidb-nodejs-sequelize-quickstart
```

2. Install dependencies

```bash
yarn
```

3. Create a `.env` file from `.env.example` and fill in the environment variables

```bash
cp .env.example .env

# .env file
# TIDB_HOST='{gateway-region}.aws.tidbcloud.com'
# TIDB_PORT='4000'
# TIDB_USER='{prefix}.root'
# TIDB_PASSWORD='{password}'
# TIDB_DB_NAME='test'
# TIDB_CA_PATH='{path/to/ca.pem}'
```

4. Run the project locally

```bash
yarn start
```

If everything goes well, you will see the output like this:

<details>
  <summary>Click to expand the details</summary>

```bash
INFO (app/10117): Getting sequelize instance...
Executing (default): SELECT 1+1 AS result
Executing (default): DROP TABLE IF EXISTS `players`;
INFO (lib/tidb/10117): Connection has been established successfully.
INFO (app/10117): Got sequelize instance.
INFO (app/10117): Getting players model...
INFO (app/10117): Got players model.
INFO (app/10117): Syncing players model...
INFO (app/10117): This creates the table, dropping it first if it already existed
Executing (default): CREATE TABLE IF NOT EXISTS `players` (`id` INTEGER NOT NULL auto_increment  COMMENT 'The unique ID of the player.', `coins` INTEGER NOT NULL COMMENT 'The number of coins that the player had.', `goods` INTEGER NOT NULL COMMENT 'The number of goods that the player had.', `createdAt` DATETIME NOT NULL, `updatedAt` DATETIME NOT NULL, PRIMARY KEY (`id`)) ENGINE=InnoDB;
Executing (default): SHOW INDEX FROM `players`
Executing (default): INSERT INTO `players` (`id`,`coins`,`goods`,`createdAt`,`updatedAt`) VALUES (1,100,100,'2023-08-31 09:10:11','2023-08-31 09:10:11'),(2,200,200,'2023-08-31 09:10:11','2023-08-31 09:10:11'),(3,300,300,'2023-08-31 09:10:11','2023-08-31 09:10:11'),(4,400,400,'2023-08-31 09:10:11','2023-08-31 09:10:11'),(5,500,500,'2023-08-31 09:10:11','2023-08-31 09:10:11');
Executing (default): INSERT INTO `players` (`id`,`coins`,`goods`,`createdAt`,`updatedAt`) VALUES (?,?,?,?,?);
INFO (app/10117): Synced players model.
INFO (app/10117): Initializing players model with some data...
INFO (app/10117): Initialized players model with some data.
INFO (app/10117): Creating a new player...
Executing (default): SELECT `id`, `coins`, `goods`, `createdAt`, `updatedAt` FROM `players` AS `players` WHERE `players`.`coins` > 300;
Executing (default): UPDATE `players` SET `coins`=?,`goods`=?,`updatedAt`=? WHERE `id` = ?
INFO (app/10117): Created a new player.
INFO (app/10117):
    id: 6
    coins: 600
    goods: 600
    updatedAt: "2023-08-31T09:10:11.686Z"
    createdAt: "2023-08-31T09:10:11.686Z"
INFO (app/10117): Reading all players with coins > 300...
INFO (app/10117): Read all players with coins > 300.
INFO (app/10117):
    0: {
      "id": 4,
      "coins": 400,
      "goods": 400,
      "createdAt": "2023-08-31T09:10:11.000Z",
      "updatedAt": "2023-08-31T09:10:11.000Z"
    }
    1: {
      "id": 5,
      "coins": 500,
      "goods": 500,
      "createdAt": "2023-08-31T09:10:11.000Z",
      "updatedAt": "2023-08-31T09:10:11.000Z"
    }
    2: {
      "id": 6,
      "coins": 600,
      "goods": 600,
      "createdAt": "2023-08-31T09:10:11.000Z",
      "updatedAt": "2023-08-31T09:10:11.000Z"
    }
INFO (app/10117): Updating the new player...
Executing (default): DELETE FROM `players` WHERE `id` = 6
INFO (app/10117): Updated the new player.
INFO (app/10117):
    id: 6
    coins: 700
    goods: 700
    updatedAt: "2023-08-31T09:10:12.359Z"
    createdAt: "2023-08-31T09:10:11.686Z"
INFO (app/10117): Deleting the new player...
Executing (default): SELECT `id`, `coins`, `goods`, `createdAt`, `updatedAt` FROM `players` AS `players` WHERE `players`.`id` = 6;
INFO (app/10117): Deleted the new player.
INFO (app/10117):
INFO (app/10117): Closing sequelize instance...
INFO (app/10117): Closed sequelize instance.
INFO (app/10117): Done.
✨  Done in 9.87s.
```

</details>
