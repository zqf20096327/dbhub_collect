# Flink CDC Connector for Dameng Database

This repository contains a standalone Flink CDC Connector for Dameng Database (DM), implemented based on Flink CDC 3.0 Source API and Dameng LogMiner mechanism.

## Features
- **Snapshot Phase**: Parallel chunk reading of historical data (JDBC-based).
- **Incremental Phase**: Uses `DBMS_LOGMNR` to read archiving logs for real-time changes.
- **Failover Recovery**: Resume from specific SCN.
- **Table API Support**: Implements `DynamicTableSourceFactory` for SQL usage.
- **Source**: `DamengSource` (CDC) and `DamengDynamicTableSource` (SQL).
- **Sink**: `DamengSink` (JDBC).

## Prerequisites
Before using this connector, ensure your Dameng Database is configured correctly:

1. **Archive Log Mode**: The database must be in ARCHIVELOG mode.
   ```sql
   ALTER DATABASE MOUNT;
   ALTER DATABASE ARCHIVELOG;
   ALTER DATABASE OPEN;
   ```
2. **Supplemental Log**: Enable supplemental logging for all columns (minimal requirement) or specific tables.
   ```sql
   ALTER DATABASE ADD SUPPLEMENTAL LOG DATA (ALL) COLUMNS;
   ```
3. **Privileges**: The connecting user requires:
   - `SELECT ANY dictionary`
   - `EXECUTE ON DBMS_LOGMNR`
   - `SELECT ANY TRANSACTION`
   - `SELECT ON V$LOGMNR_CONTENTS`

## Key Design Decisions
1. **Direct LogMiner Integration**: Unlike the official Oracle connector which uses Debezium, this connector directly manages `DBMS_LOGMNR` sessions within the Flink `SplitReader`.
2. **LogMiner Parsing**: The connector parses `SQL_REDO` from `V$LOGMNR_CONTENTS`. This is a simplified parser adapting to Dameng's SQL dialect.
3. **Data Types**:
   - `DATETIME` maps to Flink `TIMESTAMP(0)`.
   - Identifiers are handled as Case-Sensitive (quoted) by default.

## Usage

### SQL Interface
```sql
CREATE TABLE my_table (
  id INT,
  name STRING,
  PRIMARY KEY (id) NOT ENFORCED
) WITH (
  'connector' = 'dameng-cdc',
  'hostname' = 'localhost',
  'port' = '5236',
  'username' = 'SYSDBA',
  'password' = 'SYSDBA',
  'database-name' = 'DAMENG',
  'table-name' = 'SCHEMA.TABLE'
);
```

### Source (DataStream / Source API)
```java
DamengSource<String> source = new DamengSourceBuilder<String>()
    .hostname("localhost")
    .port(5236)
    .username("SYSDBA")
    .password("SYSDBA")
    .databaseList("DAMENG")
    .tableList("SCHEMA.TABLE")
    .build();
```

## Comparisons with MySQL CDC
- **Mechanism**: MySQL uses Binlog (File position); Dameng uses LogMiner (SCN).
- **Performance**: LogMiner is heavier than Binlog reading; `fetchSize` should be tuned.
- **Consistency**: Dameng uses `READ COMMITTED` by default; LogMiner ensures committed data only.
