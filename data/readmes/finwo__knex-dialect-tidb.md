# @finwo/knex-tidb

TiDB dialect for Knex.js. Extends MySQL2 with no behavioral changes; purely an identity marker so upstream code can distinguish `tidb` from `mysql` / `mysql2`.

## Why

TiDB speaks the MySQL wire protocol but diverges on certain DDL operations. This package provides a dedicated `tidb` dialect so upstream code can identify the client and apply targeted overrides, without polluting the generic mysql2 path.

No custom query compiler, table compiler, column compiler, or transaction class is needed; all behavior is inherited from MySQL2.

## Usage

```js
const Knex = require('knex');
const Client_TiDB = require('@finwo/knex-tidb');

const knex = Knex({
  client: Client_TiDB,
  connection: {
    host: 'localhost',
    user: 'root',
    password: '',
    database: 'mydb',
  },
});
```

## Verification

- `knex.client.constructor.name` returns `'Client_TiDB'`
- `knex.client.driverName` returns `'tidb'`
- All MySQL2 query generation behavior is inherited

## Requirements

- Node.js 16+
- Knex ^3.0.0 (peer dependency)
