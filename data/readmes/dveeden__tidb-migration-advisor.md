# TiDB Migration Checker

Checks queries to see which ones may not work with TiDB

## Usage

For a single query

```
$ ./tidb-migration-advisor -query 'SELECT 1 FOR UPDATE SKIP LOCKED'
```

For a file with multiple queries

```
./tidb-migration-advisor -file dump.sql
```

To fetch information from a server

```
./tidb-migration-advisor -dsn 'root@127.0.0.1:3306/test'
```

```
$ ./tidb-migration-advisor -h
Usage of ./tidb-migration-advisor:
  -dsn string
    	MySQL datasource name
  -error-only
    	only show reports with errors (only for lists of text reports)
  -file string
    	MySQL datasource name
  -format string
    	output format: json or text (default "json")
  -query string
    	query string
  -show-parsing-info
    	show query parsing details, like AST
```

## Example

```
$ ./tidb-migration-advisor -query 'CREATE TABLE t AS SELECT 1'
Query Compatibility Report:
{
  "query": "CREATE TABLE t AS SELECT 1",
  "table": {
    "schema": "",
    "table": ""
  },
  "query_restored": "CREATE TABLE `t` AS SELECT 1",
  "parser_error": "",
  "checker_errors": [
    "CREATE TABLE...SELECT is not supported"
  ],
  "advise": null
}
```

```
$ ./tidb-migration-advisor -query 'CREATE TABLE t AS SELECT 1' -format text
Query Compatibility Report:
----------------------------------------------------------------
Query: CREATE TABLE t AS SELECT 1
❌ Check error 0: CREATE TABLE...SELECT is not supported
```

## Related resources

- https://docs.pingcap.com/tidb/stable/mysql-compatibility/
- [MySQL 8.0 Compatibility](https://github.com/pingcap/tidb/issues/7968)
- https://docs.pingcap.com/tidb/stable/migrate-from-mariadb/

## Tested

- If query is parsed by the TiDB parser
- If any functions are known TiDB functions
- Various checks for statements and options that are parsed, but are known not to work.

## Not tested

- If table and column names actually exist.
- If arguments to a function are valid.
- Combination of charset and collation make sense
- Dependencies between operations for ALTER statements

## Development

### Resources

- https://pkg.go.dev/github.com/pingcap/tidb/pkg/parser
- https://pkg.go.dev/github.com/pingcap/tidb/pkg/parser/ast

### TODO & Ideas

- Add query source for MySQL binlog (DDL statements)
