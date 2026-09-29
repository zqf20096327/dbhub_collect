# TiDB Hackathon 2022 Demo

## Redistributed Index

### Connection

```
mysql -h 172.16.4.99 -P 9025 -u root -Dtest --prompt="tidb> "

set tidb_broadcast_join_threshold_count=0;
set tidb_broadcast_join_threshold_size=0;
```

## Performance

### Connection

* Original

```
mysql -h 172.16.4.99 -P 9025 -u root -Dtpch_100_multi_key --prompt="tidb> "

set tidb_isolation_read_engines = 'tiflash';
set tidb_mpp_enable_redistributed_index=OFF;
```

* Optimized
```
mysql -h 172.16.4.99 -P 9025 -u root -Dtpch_100_multi_key --prompt="tidb(opt.)> "

set tidb_isolation_read_engines = 'tiflash';
set tidb_mpp_enable_redistributed_index=ON;
```
