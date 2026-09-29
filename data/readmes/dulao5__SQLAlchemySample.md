# TiDB/TiFlash SQLAlchemy Stock Management PoC

This project is a Proof of Concept (PoC) for a lock-free stock management solution using Python, SQLAlchemy, and TiDB/TiFlash.

## Requirements

- Python 3.8+
- A running TiDB instance (local or remote)
  - eg. `tiup playground v8.5.3 --tiflash 1`

## Setup

1.  **Create a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure database connection:**
    Update the `DATABASE_URI` in `database.py` if your TiDB connection details are different from the default (`mysql+mysqlconnector://root:@127.0.0.1:4000/test`).

4.  **Initialize the database:**
    This command will create the tables, set up TiFlash replicas, and insert initial data.
    ```bash
    python app.py setup-db
    ```
    **Note:** Creating TiFlash replicas can take a few minutes. You can monitor the progress with the following SQL command:
    ```sql
    SELECT AVAILABLE, PROGRESS FROM INFORMATION_SCHEMA.TIFLASH_REPLICA WHERE TABLE_NAME IN ('stock_moves', 'stock_moves_history');
    ```
    Wait until `AVAILABLE` is `1` for both tables before proceeding.

## Usage

The application provides a command-line interface to perform stock operations.

### Add Stock (Inbound)

```bash
# Add 10 units of item 101
python app.py add-stock --item-id 101 --quantity 10 --date 2025-09-20
```

### Get Current Stock

```bash
# Get the current stock level for item 101
python app.py get-stock --item-id 101 --date 2025-09-20
```

### Remove Stock (Outbound)

There are two ways to handle outbound stock movements.

1.  **With Application-Side Check:**
    The application first checks the available stock and then proceeds with the removal if the stock is sufficient.
    ```bash
    # Try to remove 20 units of item 101
    python app.py remove-stock-check --item-id 101 --quantity 20 --date 2025-09-20
    ```

2.  **With Database-Side Check:**
    A single `INSERT ... SELECT ... WHERE` query attempts the stock removal only if the condition (sufficient stock) is met. This is an atomic and non-locking approach.
    ```bash
    # Try to remove 10 units of item 101, will only succeed if stock is >= 10
    python app.py remove-stock-atomic --item-id 101 --quantity 10 --date 2025-09-20
    ```

### View Daily Movements

This command uses TiFlash to read the `stock_moves` table and show the sum of movements for the current day.
```bash
python app.py daily-summary
```

### Run End-of-Day Batch

This command simulates a daily batch process. It calculates the closing stock for a given day from `stock_moves` (read from TiFlash) and upserts it into the `stock_moves_history` table.
```bash
# Run batch for today's date
python app.py run-batch --date $(date +%Y-%m-%d)

# Run batch for a specific date
python app.py run-batch --date 2025-09-19
```


## Scenario of testing

This scenario demonstrates how to handle stock movements after a daily batch has been processed.

0. **Prepare data**
```
python app.py setup-db

python app.py get-stock --item-id 101 --date 2025-09-19 # Calculated stock for item 101 on 2025-09-19: 100
python app.py add-stock --item-id 101 --date 2025-09-19 --quantity 25
python app.py get-stock --item-id 101 --date 2025-09-19 # Calculated stock for item 101 on 2025-09-19: 125
python app.py remove-stock-check --item-id 101 --quantity 30 --date 2025-09-19 # Successfully removed 30 units from item 101 on 2025-09-19.

python app.py remove-stock-check --item-id 101 --quantity 100 --date 2025-09-19
# Current stock is 95. Trying to remove 100.
# Failed to remove stock: Insufficient stock. Available: 95, Required: 100.
python app.py get-stock --item-id 101 --date 2025-09-19
# Calculated stock for item 101: 95

python app.py remove-stock-atomic --item-id 101 --quantity 15 --date 2025-09-19
# Successfully removed 15 units from item 101 (atomic).
python app.py get-stock --item-id 101 --date 2025-09-19
# Calculated stock for item 101: 80
```

1.  **Run the batch for the first day (e.g., 2025-09-19).**
    Assume the total stock movement for item 101 on this day resulted in a final stock of 80.
    ```bash
    python app.py run-batch --date 2025-09-19
    ```
    You can verify this in the database:
    ```sql
    SELECT * FROM test.stock_moves_history WHERE item_id = 101 AND date = '2025-09-19';
    -- Expect sum_stock_increment = 80
    ```

2.  **Check the stock on the next day (2025-09-20).**
    The stock should be equal to the previous day's closing balance.
    ```bash
    python app.py get-stock --item-id 101 --date 2025-09-20
    ```
    Expected output: `Calculated stock for item 101 on 2025-09-20: 80`

3.  **Add new stock on the second day.**
    Let's add 10 more units.
    ```bash
    python app.py add-stock --item-id 101 --quantity 10 --date 2025-09-20
    ```
    Expected output: `Successfully added 10 units to item 101 on 2025-09-20.`

4.  **Verify the final stock on the second day.**
    The stock should now be the previous day's balance plus the new addition (80 + 10).
    ```bash
    python app.py get-stock --item-id 101 --date 2025-09-20
    ```
    Expected output: `Calculated stock for item 101 on 2025-09-20: 90`

```


## confirm the plan of OLTP sql
```
mysql> select * from items;
+---------+-----------+-----------------------+
| item_id | item_code | name                  |
+---------+-----------+-----------------------+
|     101 | SAKE-101  | 純米大吟醸 720ml      |
+---------+-----------+-----------------------+
1 row in set (0.00 sec)

mysql> select * from stock_moves;
+----------------+---------+-----------------+------------+---------------------+
| stock_moves_id | item_id | stock_increment | date       | updated_at          |
+----------------+---------+-----------------+------------+---------------------+
|              1 |     101 |             100 | 2025-09-19 | 2025-09-19 11:45:47 |
|              2 |     101 |              25 | 2025-09-19 | 2025-09-19 11:48:20 |
|              3 |     101 |             -30 | 2025-09-19 | 2025-09-19 11:49:22 |
|              4 |     101 |             -15 | 2025-09-19 | 0000-00-00 00:00:00 |
|              6 |     101 |              10 | 2025-09-20 | 2025-09-19 12:37:19 |
+----------------+---------+-----------------+------------+---------------------+
5 rows in set (0.00 sec)

mysql> select * from stock_moves_history;
+---------+---------------------+------------+---------------------+
| item_id | sum_stock_increment | date       | updated_at          |
+---------+---------------------+------------+---------------------+
|     101 |                  80 | 2025-09-19 | 0000-00-00 00:00:00 |
+---------+---------------------+------------+---------------------+
1 row in set (0.00 sec)

mysql> explain analyze SELECT     IFNULL((SELECT sum_stock_increment FROM stock_moves_history WHERE item_id = 101 AND date = '2025-09-19'), 0)     +     IFNULL((SELECT SUM(stock_increment) FROM stock_moves WHERE item_id = 101 AND date = '2025-09-20'), 0) AS stock_total_count;
+--------------------+---------+---------+------+---------------+-----------------------------------------------------+---------------+---------+------+
| id                 | estRows | actRows | task | access object | execution info                                      | operator info | memory  | disk |
+--------------------+---------+---------+------+---------------+-----------------------------------------------------+---------------+---------+------+
| Projection_55      | 1.00    | 1       | root |               | time:3.79µs, loops:2, RU:0.995562, Concurrency:OFF  | 90->Column#27 | 0 Bytes | N/A  |
| └─TableDual_56     | 1.00    | 1       | root |               | time:584ns, loops:2                                 | rows:1        | N/A     | N/A  |
+--------------------+---------+---------+------+---------------+-----------------------------------------------------+---------------+---------+------+
2 rows in set (0.00 sec)

mysql> explain analyze SELECT sum_stock_increment FROM stock_moves_history WHERE item_id = 101 AND date = '2025-09-19';
+-------------+---------+---------+------+-------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+--------+------+
| id          | estRows | actRows | task | access object                                                     | execution info                                                                                                                                                                                                                                                                                                                                   | operator info | memory | disk |
+-------------+---------+---------+------+-------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+--------+------+
| Point_Get_1 | 1.00    | 1       | root | table:stock_moves_history, clustered index:PRIMARY(item_id, date) | time:555.4µs, loops:2, RU:0.506249, Get:{num_rpc:1, total_time:501.9µs}, time_detail: {total_process_time: 91.5µs, total_wait_time: 70.2µs, total_kv_read_wall_time: 165.4µs, tikv_wall_time: 234.5µs}, scan_detail: {total_process_keys: 1, total_process_keys_size: 50, total_keys: 1, get_snapshot_time: 25.5µs, rocksdb: {block: {}}}        |               | N/A    | N/A  |
+-------------+---------+---------+------+-------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+--------+------+
1 row in set (0.00 sec)

mysql> explain analyze SELECT SUM(stock_increment) FROM stock_moves WHERE item_id = 101 AND date = '2025-09-20';
+-----------------------------+---------+---------+-----------+-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------+-----------+------+
| id                          | estRows | actRows | task      | access object     | execution info                                                                                                                                                                                                                                                                                                    | operator info                                                           | memory    | disk |
+-----------------------------+---------+---------+-----------+-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------+-----------+------+
| StreamAgg_12                | 1.00    | 1       | root      |                   | time:659.9µs, loops:2, RU:0.493368                                                                                                                                                                                                                                                                                | funcs:sum(Column#11)->Column#6                                          | 1.45 KB   | N/A  |
| └─Projection_32             | 0.00    | 1       | root      |                   | time:657.2µs, loops:2, Concurrency:OFF                                                                                                                                                                                                                                                                            | cast(test.stock_moves.stock_increment, decimal(10,0) BINARY)->Column#11 | 1.11 KB   | N/A  |
|   └─TableReader_18          | 0.00    | 1       | root      |                   | time:650.5µs, loops:2, cop_task: {num: 1, max: 596.2µs, proc_keys: 1, tot_proc: 52.1µs, tot_wait: 147.5µs, copr_cache_hit_ratio: 0.00, build_task_duration: 7.63µs, max_distsql_concurrency: 1}, rpc_info:{Cop:{num_rpc:1, total_time:582.1µs}}                                                                   | data:TableRangeScan_17                                                  | 305 Bytes | N/A  |
|     └─TableRangeScan_17     | 0.00    | 1       | cop[tikv] | table:stock_moves | tikv_task:{time:0s, loops:1}, scan_detail: {total_process_keys: 1, total_process_keys_size: 66, total_keys: 2, get_snapshot_time: 126.4µs, rocksdb: {delete_skipped_count: 1, key_skipped_count: 1, block: {}}}, time_detail: {total_process_time: 52.1µs, total_wait_time: 147.5µs, tikv_wall_time: 326.2µs}     | range:[2025-09-20 101,2025-09-20 101], keep order:false, stats:pseudo   | N/A       | N/A  |
+-----------------------------+---------+---------+-----------+-------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------+-----------+------+
4 rows in set (0.00 sec)

explain 
INSERT INTO stock_moves_history (item_id, date, sum_stock_increment) 
SELECT /*+ READ_FROM_STORAGE(TIFLASH[sm]) */
    sm.item_id,
    '2025-09-19' AS date,
    IFNULL((
        SELECT /*+ READ_FROM_STORAGE(TIFLASH[h]) */ h.sum_stock_increment
        FROM stock_moves_history h
        WHERE h.item_id = sm.item_id
        AND h.date = '2025-09-19'
    ), 0) + IFNULL(SUM(sm.stock_increment), 0) AS closing_d
FROM stock_moves sm 
WHERE sm.date = '2025-09-19'
GROUP BY sm.item_id
ON DUPLICATE KEY UPDATE
sum_stock_increment = VALUES(sum_stock_increment),
updated_at = CURRENT_TIMESTAMP;

+---------------------------------------------+---------+--------------+---------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| id                                          | estRows | task         | access object | operator info                                                                                                                                                               |
+---------------------------------------------+---------+--------------+---------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Insert_1                                    | N/A     | root         |               | N/A                                                                                                                                                                         |
| └─TableReader_77                            | 1.00    | root         |               | MppVersion: 2, data:ExchangeSender_76                                                                                                                                       |
|   └─ExchangeSender_76                       | 1.00    | mpp[tiflash] |               | ExchangeType: PassThrough                                                                                                                                                   |
|     └─Projection_14                         | 1.00    | mpp[tiflash] |               | test.stock_moves.item_id, 2025-09-19->Column#17, plus(cast(ifnull(test.stock_moves_history.sum_stock_increment, 0), decimal(20,0) BINARY), ifnull(Column#16, 0))->Column#23 |
|       └─Projection_75                       | 1.00    | mpp[tiflash] |               | Column#16, test.stock_moves.item_id, test.stock_moves_history.sum_stock_increment                                                                                           |
|         └─HashJoin_74                       | 1.00    | mpp[tiflash] |               | left outer join, equal:[eq(test.stock_moves.item_id, test.stock_moves_history.item_id)]                                                                                     |
|           ├─ExchangeReceiver_34(Build)      | 0.00    | mpp[tiflash] |               |                                                                                                                                                                             |
|           │ └─ExchangeSender_33             | 0.00    | mpp[tiflash] |               | ExchangeType: Broadcast, Compression: FAST                                                                                                                                  |
|           │   └─Selection_32                | 0.00    | mpp[tiflash] |               | eq(test.stock_moves_history.date, 2025-09-19 00:00:00.000000)                                                                                                               |
|           │     └─TableFullScan_31          | 1.00    | mpp[tiflash] | table:h       | pushed down filter:empty, keep order:false, stats:partial[date:unInitialized]                                                                                               |
|           └─Projection_25(Probe)            | 1.00    | mpp[tiflash] |               | Column#16, test.stock_moves.item_id                                                                                                                                         |
|             └─HashAgg_20                    | 1.00    | mpp[tiflash] |               | group by:Column#33, funcs:sum(Column#32)->Column#16, funcs:firstrow(Column#33)->test.stock_moves.item_id, stream_count: 8                                                   |
|               └─Projection_78               | 0.01    | mpp[tiflash] |               | cast(test.stock_moves.stock_increment, decimal(10,0) BINARY)->Column#32, test.stock_moves.item_id->Column#33, stream_count: 8                                               |
|                 └─ExchangeReceiver_24       | 0.01    | mpp[tiflash] |               | stream_count: 8                                                                                                                                                             |
|                   └─ExchangeSender_23       | 0.01    | mpp[tiflash] |               | ExchangeType: HashPartition, Compression: FAST, Hash Cols: [name: test.stock_moves.item_id, collate: binary], stream_count: 8                                               |
|                     └─TableRangeScan_22     | 0.01    | mpp[tiflash] | table:sm      | range:[2025-09-19,2025-09-19], keep order:false, stats:partial[date:unInitialized]                                                                                          |
+---------------------------------------------+---------+--------------+---------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
16 rows in set (0.04 sec)

```