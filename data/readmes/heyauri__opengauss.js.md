# opengauss.js

[![npm version](https://img.shields.io/npm/v/opengauss.js.svg)](https://www.npmjs.com/package/opengauss.js)  
**Non-blocking OpenGauss/PostgreSQL client for Node.js with pure JavaScript implementation.**

**A hybrid database client that supports both OpenGauss and PostgreSQL connections simultaneously**, based on:
- [node-postgres@8.22.0](https://github.com/brianc/node-postgres)
- [openGauss-connector-nodejs](https://github.com/opengauss-mirror/openGauss-connector-nodejs)
- [pg-opengauss](https://github.com/whyour/pg-opengauss)

**Node.js version requirement**: >= 16.0.0

✅ ​**Key Features**  
- Dual-database support with type switching
- Compatibility with `Knex.js` and other query builders
- Native promise-based API
- Connection pooling support
- Enables smooth transition of existing Knex.js applications from PostgreSQL to OpenGauss with schema compatibility

## Installation
```bash
npm install opengauss.js
```

## Usage

### Basic Client Setup Configuration
```javascript
const { Client } = require("opengauss.js");

const client = new Client({
    user: 'dbuser',
    password: 'secretpassword',
    host: 'database.server.com',
    port: 3211,
    database: 'mydb',

    databaseType: 'openGauss'  // Options: 'openGauss' | 'postgres' | 'pg' (Default: 'openGauss')
});

await client.connect();

const res = await client.query('SELECT $1::text as message', ['Hello world!']);
console.log(res.rows[0].message);
await client.end();
```

### Connection Pool
```javascript
const { Pool } = require("opengauss.js");

const pool = new Pool({
    user: 'dbuser',
    password: 'secretpassword',
    host: 'database.server.com',
    port: 3211,
    database: 'mydb',
    databaseType: 'openGauss',
    max: 10,
    idleTimeoutMillis: 30000
});

const res = await pool.query('SELECT NOW()');
console.log(res.rows[0]);
await pool.end();
```

### Integration with Knex.js
Seamless replacement via npm alias:
```javascript
// package.json
{
    ...,
    "dependencies": {
        "pg": "npm:opengauss.js@^1.2.0"
    }
}
```

Knex configuration
```javascript
const knex = require('knex')({
  client: 'pg',
  connection: {
    databaseType: 'openGauss',  // Specify database type
    // ...other standard pg configurations
    host: '127.0.0.1',
    ...
  },
  version: "9.2"
});
```

## Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `user` | Database user | process.env.USER |
| `password` | Database password | null |
| `host` | Database host | localhost |
| `port` | Database port | 5432 |
| `database` | Database name | undefined |
| `databaseType` | Database type: `openGauss` \| `postgres` \| `pg` | openGauss |
| `connectionString` | Connection string | undefined |
| `ssl` | SSL configuration | false |
| `sslnegotiation` | SSL negotiation mode: `postgres` \| `direct` | undefined |
| `connectionTimeoutMillis` | Connection timeout in milliseconds | 0 |
| `query_timeout` | Query timeout in milliseconds | false |
| `statement_timeout` | Statement timeout in milliseconds | false |
| `lock_timeout` | Lock timeout in milliseconds | false |
| `keepAlive` | Enable keep-alive | false |
| `keepAliveInitialDelayMillis` | Initial delay for keep-alive | 0 |
| `scramMaxIterations` | Maximum SCRAM iterations | 100000 |
| `max` | Max pool connections | 10 |
| `idleTimeoutMillis` | Idle timeout in milliseconds | 30000 |

## API Exports

```javascript
const {
    Client,
    Pool,
    defaults,
    types,
    DatabaseError,
    escapeIdentifier,
    escapeLiteral,
    Result,
    utils,
    TypeOverrides,
    Connection
} = require("opengauss.js");
```

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

### Recent Changes (v1.2.0)
- Minimum Node.js version is now `16.0.0`
- Updated internal `pg-pool` to `3.14.0`
- Updated internal `pg-connection-string` to `2.14.0`
- Updated internal openGauss protocol files based on `pg-protocol` to `1.15.0`
- Files migrated to `pg@8.22.0`: connection-parameters.js, defaults.js, utils.js, query.js, result.js, crypto/sasl.js, crypto/utils.js, crypto/cert-signatures.js, opengauss/connection.js, postgres/connection.js
- Removed `lib/crypto/utils-webcrypto.js` & `lib/crypto/utils-legacy.js`
