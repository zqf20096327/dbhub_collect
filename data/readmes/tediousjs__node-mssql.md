# node-mssql

**Microsoft SQL Server client for Node.js**

[![NPM Version][npm-image]][npm-url] [![NPM Downloads][downloads-image]][downloads-url]

Supported TDS drivers:

- [Tedious][tedious-url] (pure JavaScript - Windows/macOS/Linux, default)
- [MSNodeSQLv8][msnodesqlv8-url] (Microsoft / Contributors Node V8 Driver for Node.js for SQL Server, v2.4.8-v6 native - Windows or Linux/macOS 64 bits only)

## Installation

### Tedious driver (default)

```
npm install mssql
```

### MSNodeSQLv8 driver (optional)

```
npm install mssql msnodesqlv8
```

msnodesqlv8 6 needs Node.js 22 or later. On an older Node.js, install msnodesqlv8 5 (`npm install mssql msnodesqlv8@5`). With msnodesqlv8 6, use its latest release, 6.2.1 or later: 6.0.0 to 6.2.0 keep hold of the connection of a stream that is paused after it is cancelled.

## SQL Server prerequisites

This package requires TCP/IP to connect to SQL Server, and you may need to enable this in your installation.

## Short Example: Use Connect String

```javascript
const sql = require('mssql')

(async () => {
    try {
        // make sure that any items are correctly URL encoded in the connection string
        await sql.connect('Server=localhost,1433;Database=database;User Id=username;Password=password;Encrypt=true')
        const result = await sql.query`select * from mytable where id = ${value}`
        console.dir(result)
    } catch (err) {
        // ... error checks
    }
})()
```

If you're on Windows Azure, add `?encrypt=true` to your connection string. See [docs](#configuration) to learn more.

Parts of the connection URI should be correctly URL encoded so that the URI can be parsed correctly.

## Longer Example: Connect via Config Object

Assuming you have set the appropriate environment variables, you can construct a config object as follows:

```javascript
const sql = require('mssql')

const sqlConfig = {
  user: process.env.DB_USER,
  password: process.env.DB_PWD,
  database: process.env.DB_NAME,
  server: 'localhost',
  pool: {
    max: 10,
    min: 0,
    idleTimeoutMillis: 30000
  },
  options: {
    encrypt: true, // for azure
    trustServerCertificate: false // change to true for local dev / self-signed certs
  }
}

(async () => {
 try {
  // make sure that any items are correctly URL encoded in the connection string
  await sql.connect(sqlConfig)
  const result = await sql.query`select * from mytable where id = ${value}`
  console.dir(result)
 } catch (err) {
  // ... error checks
 }
})()
```

## Windows Authentication Example Using MSNodeSQLv8

```javascript
const sql = require('mssql/msnodesqlv8');

const config = {
  server: "MyServer",
  database: "MyDatabase",
  options: {
    trustedConnection: true, // Set to true if using Windows Authentication
    trustServerCertificate: true, // Set to true if using self-signed certificates
  },
  // driver: "ODBC Driver 18 for SQL Server", // Uncomment to use specific driver
};

(async () => {
  try {
    await sql.connect(config);
    const result = await sql.query`select TOP 10 * from MyTable`;
    console.dir(result);
  } catch (err) {
    console.error(err);
  }
})();
```

## Documentation

### Examples

* [Async/Await](#asyncawait)
* [Promises](#promises)
* [ES6 Tagged template literals](#es6-tagged-template-literals)
* [Callbacks](#callbacks)
* [Streaming](#streaming)
* [Connection Pools](#connection-pools)

### Configuration

* [General](#general-same-for-all-drivers)
* [Formats](#formats)

### Drivers

* [Tedious](#tedious)
* [MSNodeSQLv8](#msnodesqlv8)

### Connections

* [Pool Management](#pool-management)
* [Connection Validation](#connection-validation)
* [ConnectionPool](#connections-1)
* [connect](#connect-callback)
* [close](#close)
* [Pool properties](#pool-properties)
* [parseConnectionString](#connectionpoolparseconnectionstring-connectionstring)

### Requests

* [Request](#request)
* [execute](#execute-procedure-callback)
* [input](#input-name-type-value)
* [output](#output-name-type-value)
* [replaceInp

[...截断...]

ut](#replaceinput-name-type-value-1)
* [replaceOutput](#replaceoutput-name-type-value)
* [toReadableStream](#toReadableStream)
* [pipe](#pipe-stream)
* [query](#query-command-callback)
* [batch](#batch-batch-callback)
* [bulk](#bulk-table-options-callback)
* [cancel](#cancel)

### Identifier rules

* [Parameter names](#parameter-names)
* [Column names](#column-names)
* [Type names and sizes](#type-names-and-sizes)
* [Procedure names](#procedure-names)

### Transactions

* [Transaction](#transaction)
* [begin](#begin-isolationlevel-callback)
* [commit](#commit-callback)
* [rollback](#rollback-callback)

### Prepared Statements

* [PreparedStatement](#prepared-statement)
* [input](#input-name-type)
* [output](#output-name-type)
* [prepare](#prepare-statement-callback)
* [execute](#execute-values-callback)
* [unprepare](#unprepare-callback)

### Other

* [CLI](#cli)
* [Geography and Geometry](#geography-and-geometry)
* [Table-Valued Parameter](#table-valued-parameter-tvp)
* [Response Schema](#response-schema)
* [Affected Rows](#affected-rows)
* [JSON support](#json-support)
* [Handling Duplicate Column Names](#handling-duplicate-column-names)
* [Errors](#errors)
* [Informational messages](#informational-messages)
* [Metadata](#metadata)
* [Data Types](#data-types)
* [SQL injection](#sql-injection)
* [Diagnostics Channel](#diagnostics-channel)
* [Contributing](https://github.com/tediousjs/node-mssql/wiki/Contributing)
* [11.x to 12.x changes](#11x-to-12x-changes)
* [10.x to 11.x changes](#10x-to-11x-changes)
* [9.x to 10.x changes](#9x-to-10x-changes)
* [8.x to 9.x changes](#8x-to-9x-changes)
* [7.x to 8.x changes](#7x-to-8x-changes)
* [6.x to 7.x changes](#6x-to-7x-changes)
* [5.x to 6.x changes](#5x-to-6x-changes)
* [4.x to 5.x changes](#4x-to-5x-changes)
* [3.x to 4.x changes](#3x-to-4x-changes)
* [3.x Documentation](https://github.com/tediousjs/node-mssql/blob/1893969195045a250f0fdeeb2de7f30dcf6689ad/README.md)

## Examples

### Config

```javascript
const config = {
    user: '...',
    password: '...',
    server: 'localhost', // You can use 'localhost\\instance' to connect to named instance
    database: '...',
}
```


### Async/Await

```javascript
const sql = require('mssql')

(async function () {
    try {
        let pool = await sql.connect(config)
        let result1 = await pool.request()
            .input('input_parameter', sql.Int, value)
            .query('select * from mytable where id = @input_parameter')

        console.dir(result1)

        // Stored procedure

        let result2 = await pool.request()
            .input('input_parameter', sql.Int, value)
            .output('output_parameter', sql.VarChar(50))
            .execute('procedure_name')

        console.dir(result2)
    } catch (err) {
        // ... error checks
    }
})()

sql.on('error', err => {
    // ... error handler
})
```

### Promises

#### Queries

```javascript
const sql = require('mssql')

sql.on('error', err => {
    // ... error handler
})

sql.connect(config).then(pool => {
    // Query

    return pool.request()
        .input('input_parameter', sql.Int, value)
        .query('select * from mytable where id = @input_parameter')
}).then(result => {
    console.dir(result)
}).catch(err => {
  // ... error checks
});
```

#### Stored procedures

```js
const sql = require('mssql')

sql.on('error', err => {
    // ... error handler
})

sql.connect(config).then(pool => {

    // Stored procedure

    return pool.request()
        .input('input_parameter', sql.Int, value)
        .output('output_parameter', sql.VarChar(50))
        .execute('procedure_name')
}).then(result => {
    console.dir(result)
}).catch(err => {
    // ... error checks
})
```

Native Promise is used by default. You can easily change this with `sql.Promise = require('myownpromisepackage')`.

### ES6 Tagged template literals

```javascript
const sql = require('mssql')

sql.connect(config).then(() => {
    return sql.query`select * from mytable where id = ${value