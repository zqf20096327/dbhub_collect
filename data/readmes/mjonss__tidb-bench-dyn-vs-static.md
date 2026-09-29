Misc configuration, script and results for benchmarking TiDB new tidb_partition_pruning_mode='dynamic' mode (vs old 'static' implementation).

I used a 1 node cluster having a single instance of each TiDB cluster components (TiDB, TiKV, PD, monitoring), see prune-bench.1-node.yaml, which I destroyed between HASH and RANGE partitioning.

I also used the latest sysbench, with a change to create the secondary index before loading the data (prepare/insert): https://github.com/mjonss/sysbench/tree/add-index-before-load

Checked the cluster config:
tiup cluster check prune-bench.1-node.yaml -i ~/.ssh/id_ed25519 -u mjadmin

And deployed with:
tiup cluster deploy prune-bench-1node nightly prune-bench.1-node.yaml -i ~/.ssh/id_ed25519 -u mjadmin

Fixed the tidb settings (setup-tidb-for-sysbench.sh):
mysql -h 192.168.2.62 -P 4000 -u root -e 'set global tidb_disable_txn_auto_retry = off'
mysql -h 192.168.2.62 -P 4000 -u root -e 'create database if not exists sbtest'
mysql -h 192.168.2.62 -P 4000 -u root -e 'set global tidb_partition_prune_mode = "dynamic"'

Tested for hash based partitioning with:
(date ; time ./src/sysbench --mysql-host=192.168.2.62 --mysql-port=4000 --mysql-user=root --tables=4 --table-size=1000000 --threads=64 --time=300 --report-interval=10 --create_secondary=before --create_table_options="PARTITION BY HASH (id) PARTITIONS 8" oltp_read_only prepare ; date ) > oltp.prepare.`date -Iseconds`
(date ; time ~/bench/sysbench/src/sysbench --config-file=./sysbench.conf oltp_read_only run ; date ) > oltp.run.dynamic.`date -Iseconds` 2>&1
# Changed the tidb_partition_prune_mode to 'static':
set global tidb_partition_prune_mode='dynamic';
# and verified it with a new connection
(date ; time ~/bench/sysbench/src/sysbench --config-file=./sysbench.conf oltp_read_only run ; date ) > oltp.run.static.`date -Iseconds` 2>&1


Cleaned the data before the next run:
tiup cluster clean prune-bench-1node --all
tiup cluster tiup cluster start prune-bench-1node
Tested for range based partitioning with:
(date ; time ./src/sysbench --mysql-host=192.168.2.62 --mysql-port=4000 --mysql-user=root --tables=4 --table-size=1000000 --threads=64 --time=300 --report-interval=10 --create_secondary=before --create_table_options="PARTITION BY RANGE (id) (PARTITION p0 values less than (125000), partition p125 values less than (250000), partition p250 values less than (375000), partition p375 values less than (500000), partition p500 values less than (625000), partition p625 values less than (750000), partition p750 values less than (875000), partition pMax values less than (MAXVALUE))" oltp_read_only prepare ; date ) > oltp.prepare.`date -Iseconds` 2>&1
(date ; time ~/bench/sysbench/src/sysbench --config-file=./sysbench.conf oltp_read_only run ; date ) > oltp.run.dynamic.`date -Iseconds` 2>&1
# Changed the tidb_partition_prune_mode to 'static':
set global tidb_partition_prune_mode='dynamic';
# and verified it with a new connection
(date ; time ~/bench/sysbench/src/sysbench --config-file=./sysbench.conf oltp_read_only run ; date ) > oltp.run.static.`date -Iseconds` 2>&1



Moving on to tpcc:
tiup cluster clean prune-bench-1node --all
tiup cluster start prune-bench-1node
sh ~/bench/setup-tidb-for-sysbench.sh








Older notes:
Considerations:
Try to focus on showing the difference:
if the performance difference is expected inside the optimizer/cpu based then run on RAM-disk (single node with RAM-disk is better to remove any network or disk IO) 
if the performance difference is expected during actual reading/writing then run in (Cluster will show the difference by adding network and disk IO latency. Be aware of small datasets will be affected by high cache hits in the TiKV/RocksDB code)

So for verifying the Plan cache, we can use one node cluster with RAM disk

Actually we can try both setups for all tests, to verify the above assumptions!
