# tidb-autoid

This is a small utility to list up next values of _tidb_rowid/auto_increment/auto_random.
It is actually [`SHOW TABLE table NEXT_ROW_ID`](https://docs.pingcap.com/tidb/stable/sql-statement-show-table-next-rowid) for each table. 

## Usage

1. Rename `_env.playground` file to `.env` and modify environment values along with your TiDB environment. 
2. Run `autoids` command. It shows table name, autoid type, and next value of the autoid. 
