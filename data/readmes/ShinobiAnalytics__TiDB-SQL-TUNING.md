# TRAINING TIDB SQL TUNING - LABS HANDS ON
================================================================================================

# TiDB SQL Tuning Lab 1: Clustered and Non-Clustered Indexes
## Module 1: Best Practices For Clustered Indexes
In this module, you will create clustered indexes for primary key tables and configure related settings to prevent data insertion hotspots.

## Tasks
- Created a table named orders1 by a given DDL. The table will have a high concurrency of insertions by the application design.
- Identify any potential performance issues that may arise with table orders1.
- Recreate the orders1 table to ensure it includes a clustered index for the primary key.
- Perform multiple data insertions into the orders1 table and analyze the resulting data distribution.
## Step 1. Log in to the remote Linux
## Step 2. Connect to database test
```
mysql -h ${HOST_DB1_PRIVATE_IP} --port 4000 -u root
```
```
USE test;
```
> **sample output**
> ```
> Database changed
> ```

### Step 3. Observe the table definition of orders1, point out the potential performance problem
- The table definition is shown below, click the Explain with AI button to get more information.
```
CREATE TABLE orders1 (
 id INT UNSIGNED AUTO_INCREMENT NOT NULL,
 code VARCHAR(30) NOT NULL,
 order_no VARCHAR(200) NOT NULL DEFAULT '', 
 status INT NOT NULL,
 cancel_flag INT DEFAULT NULL,
 create_user VARCHAR(50) DEFAULT NULL,
 update_user VARCHAR(50) DEFAULT NULL,
 create_time DATETIME DEFAULT NULL, 
 update_time DATETIME DEFAULT NULL,
 PRIMARY KEY (id) 
);
```
- The table orders1 utilizes AUTO_INCREMENT for its primary key. It is advisable to replace AUTO_INCREMENT with AUTO_RANDOM to prevent hotspot issues that may arise from sequential data insertion.

- Considering the expected large volume of data insertion, it is recommended to preemptively partition the table by splitting the TiKV regions during the initial table creation.

### Step 4. Recreate table orders1 as per the best practice
- Create the orders1 table, since we need to use AUTO_RANDOM instead of AUTO_INCREMENT, the id column needs to be changed from INT type to BIGINT type.

```
DROP TABLE orders1;
CREATE TABLE orders1 
( id BIGINT unsigned AUTO_RANDOM NOT NULL,
  code VARCHAR(30) NOT NULL,
  order_no VARCHAR(200) NOT NULL DEFAULT '', 
  status INT NOT NULL,
  cancel_flag INT DEFAULT NULL,
  create_user VARCHAR(50) DEFAULT NULL,
  update_user VARCHAR(50) DEFAULT NULL,
  create_time DATETIME DEFAULT NULL, 
  update_time DATETIME DEFAULT NULL,
  PRIMARY KEY (id) CLUSTERED
);
SHOW CREATE TABLE orders1\G
```

> **sample output**
> ```
> *************************** 1. row ***************************
>Table: orders1
>Create Table: CREATE TABLE `orders1` (
>  `id` BIGINT unsigned NOT NULL /*T![auto_rand] AUTO_RANDOM(5) */,
>  `code` VARCHAR(30) NOT NULL,
>  `order_no` VARCHAR(200) NOT NULL DEFAULT '',
>  `status` INT NOT NULL,
>  `cancel_flag` INT(4) DEFAULT NULL,
>  `create_user` VARCHAR(50) DEFAULT NULL,
>  `update_user` VARCHAR(50) DEFAULT NULL,
>  `create_time` DATETIME DEFAULT NULL,
>  `update_time` DATETIME DEFAULT NULL,
>  PRIMARY KEY (`id`) /*T![clustered_index] CLUSTERED */
>) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
>1 row in set (0.01 sec)
> ```

- Check the Region distribution of the orders1 table.

```
SHOW TABLE orders1 REGIONS\G
```
> **sample output**
> ```
> *************************** 1. row ***************************
>              REGION_ID: 34
>              START_KEY: t_94_
>                END_KEY: t_281474976710649_
>              LEADER_ID: 139
>        LEADER_STORE_ID: 2
>                  PEERS: 35, 139, 186
>             SCATTERING: 0
>          WRITTEN_BYTES: 273
>             READ_BYTES: 0
>   APPROXIMATE_SIZE(MB): 1
>       APPROXIMATE_KEYS: 0
> SCHEDULING_CONSTRAINTS: 
>       SCHEDULING_STATE: 
> 1 row in set (0.01 sec)
> ```

- Split orders1 table into multiple TiKV regions.

```
SPLIT TABLE orders1 BETWEEN(0) AND (922337203685477580

[...截断...]

7) REGIONS 16;
SHOW TABLE orders1 REGIONS\G
```

> **sample output**
> ```
> +--------------------+----------------------+
>| TOTAL_SPLIT_REGION | SCATTER_FINISH_RATIO |
>+--------------------+----------------------+
>|                 15 |                    1 |
>+--------------------+----------------------+
>1 row in set (0.48 sec)
>*************************** 1. row ***************************
>             REGION_ID: 244
>             START_KEY: t_94_
>               END_KEY: t_94_r_576460752303423487
>             LEADER_ID: 246
>       LEADER_STORE_ID: 2
>                 PEERS: 245, 246, 247
>            SCATTERING: 0
>         WRITTEN_BYTES: 39
>            READ_BYTES: 0
>  APPROXIMATE_SIZE(MB): 1
>      APPROXIMATE_KEYS: 0
>SCHEDULING_CONSTRAINTS: 
>      SCHEDULING_STATE: 
>*************************** 2. row ***************************
>             REGION_ID: 248
>             START_KEY: t_94_r_576460752303423487
>               END_KEY: t_94_r_1152921504606846974
>             LEADER_ID: 251
>       LEADER_STORE_ID: 5
>                 PEERS: 249, 250, 251
>            SCATTERING: 0
>         WRITTEN_BYTES: 39
>            READ_BYTES: 0
>  APPROXIMATE_SIZE(MB): 1
>      APPROXIMATE_KEYS: 0
>SCHEDULING_CONSTRAINTS: 
>      SCHEDULING_STATE: 
>... ...
>*************************** 16. row ***************************
>             REGION_ID: 34
>             START_KEY: t_94_r_8646911284551352305
>               END_KEY: t_281474976710649_
>             LEADER_ID: 139
>       LEADER_STORE_ID: 2
>                 PEERS: 35, 139, 186
>            SCATTERING: 0
>         WRITTEN_BYTES: 0
>            READ_BYTES: 0
>  APPROXIMATE_SIZE(MB): 1
>      APPROXIMATE_KEYS: 0
>SCHEDULING_CONSTRAINTS: 
>      SCHEDULING_STATE: 
>16 rows in set (0.08 sec)
> ```

### Step 5. Insert data into the orders1 table five times

```
BEGIN;
INSERT INTO orders1 (code, status) VALUES (SUBSTRING(MD5(RAND()),1,20), FLOOR(RAND()*10));
INSERT INTO orders1 (code, status) VALUES (SUBSTRING(MD5(RAND()),1,20), FLOOR(RAND()*10));
INSERT INTO orders1 (code, status) VALUES (SUBSTRING(MD5(RAND()),1,20), FLOOR(RAND()*10));
INSERT INTO orders1 (code, status) VALUES (SUBSTRING(MD5(RAND()),1,20), FLOOR(RAND()*10));
INSERT INTO orders1 (code, status) VALUES (SUBSTRING(MD5(RAND()),1,20), FLOOR(RAND()*10));
COMMIT;
```

> **sample output**
> ```
> Query OK, 0 rows affected (0.00 sec)
> ```

```
SELECT id, code, status FROM orders1 ORDER BY id;
```
> **sample output**
> ```
> +---------------------+----------------------+--------+
>| id                  | code                 | status |
>+---------------------+----------------------+--------+
>| 1152921504606846977 | b1f55f9268fb31cec7f5 |      0 |
>| 1152921504606846978 | c3fd54abaab48504539a |      3 |
>| 1152921504606846979 | 92c1b99e02e4e646b0b5 |      0 |
>| 1152921504606846980 | 67af6b9ceb8e758c5794 |      9 |
>| 1152921504606846981 | ed834b9ef841a67d8edb |      8 |
>+---------------------+----------------------+--------+
>5 rows in set (0.01 sec)
> ```

- Although the AUTO_RANDOM attribute has been specified for the primary key in the orders1 table, the generated primary key values are still continuous.

### Step 6. TRUNCATE the data in the orders1 table and insert new data
- Note that, after TRUNCATE, there will only be 1 region left in the orders1 table, so it needs to be split manually.
```
TRUNCATE TABLE orders1;
SPLIT TABLE orders1 BETWEEN(0) AND (9223372036854775807) REGIONS 16;
```
> **sample output**
> ```
> +--------------------+----------------------+
>| TOTAL_SPLIT_REGION | SCATTER_FINISH_RATIO |
>+--------------------+----------------------+
>|                 15 |                    1 |
>+--------------------+----------------------+
>1 row in set (0.06 sec)
> ```
```
INSERT INTO orders1(code, status) VALUES(SUBSTRING(MD5(RAND()),1,20), FLOOR(RAND()*10)), \
(SUBSTRING(MD5(RAND()),1,20), FLOOR(RAND()*10)), (SUBSTRING(MD5(RAND()),1,20), FLOOR(RAND()*10)), \
(SUBSTRING(MD5(RAND()),1,20), FLOOR(RAND(