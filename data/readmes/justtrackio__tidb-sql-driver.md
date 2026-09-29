# tidb-sql-driver
This library is a thin wrapper around the official mysql sql driver for Golang: https://github.com/go-sql-driver/mysql. \
It contains additional functionality which is special to TiDB (https://docs.pingcap.com/tidb/stable/overview) and not 
covered by MySQL. 

### transactions with causal consistency
TiDB supports transactions with causal consistency (https://docs.pingcap.com/tidb/stable/transaction-overview#causal-consistency)
which is not supported by MySQL. Causal consistency can be enabled via the additional parameter `tidb_txn_causal`.

### additional parameters
*Parameters are case-sensitive!*

Notice that any of `true`, `TRUE`, `True` or `1` is accepted to stand for a true boolean value. Not surprisingly, false can be specified as any of: `false`, `FALSE`, `False` or `0`.

##### `tidb_txn_causal`

```
Type:           bool
Valid Values:   true, false
Default:        false
```

`tidb_txn_causal=true` enables transactions being executed with causal consistency 
(https://docs.pingcap.com/tidb/stable/transaction-overview#causal-consistency). This is a driver global setting, and can't
be changed on starting individual transactions.

