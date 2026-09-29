# tidb-clickhouse
This tool helps migration ClickHouse table to TiDB

## Supported Features
- dump clickhouse table schema as DDL, [example](example_clickhouse_ddl.sql).
- convert clickhouse table schema as TiDB supported DDL, [example](example_tidb_ddl.sql).

## Data Type Mapping
|ClickHouse |TiDB             |
|-----------|-----------------|
|UInt8      |TINYINT UNSIGNED |
|Int8       |TINYINT          |
|UInt16     |SMALLINT UNSIGNED|
|Int16      |SMALLINT         |
|UInt32     |INT UNSIGNED     |
|Int32      |INT              |
|UInt64     |BIGINT UNSIGNED  |
|Int64      |BIGINT           |
|Float32    |FLOAT            |
|Float64    |DOUBLE           |
|Decimal    |DECIMAL          |
|DateTime   |DATETIME         |
|Date       |DATE             |
|FixedString|CHAR             |
|String     |VARCHAR          |
|Enum8      |ENUM             |
|Enum16     |ENUM             |
|Bool       |BOOLEAN          |
|JSON       |JSON             |

### String type Mapping
length: max(lengthUTF8())

|length| type                      |
|------|---------------------------|
|length == 0| char(255) or varchar(255) |
|lenght > 255| TEXT                      |
|lenght > 65535| MEDIUMTEXT                |
|lenght > 16777215| LONGTEXT                  |

 
## Requirements
- Python3.8

## How to Install
```shell
pip3 install -r requirements.txt
```

## How to Use
```shell
python3 main.py --help

python3 main.py dump-clickhouse-table-schema -h 127.0.0.1 -P 9000 -u default -p xx -d db1,db2

python3 main.py build-tidb-table-schema -h 127.0.0.1 -P 9000 -u default -p xxx -d db1,db2
```


