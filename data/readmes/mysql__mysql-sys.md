# The MySQL sys schema

A collection of views, functions and procedures to help MySQL administrators get insight in to MySQL Database usage.

There are install files available for 5.6 and 5.7 respectively. To load these, you must position yourself within the directory that you downloaded to, as these top level files SOURCE individual files that are shared across versions in most cases (though not all).

## Installation

The objects should all be created as the root user (but run with the privileges of the invoker).

For instance if you download to /tmp/mysql-sys/, and want to install the 5.6 version you should:

    cd /tmp/mysql-sys/
    mysql -u root -p < ./sys_56.sql

Or if you would like to log in to the client, and install the 5.7 version:

    cd /tmp/mysql-sys/
    mysql -u root -p 
    SOURCE ./sys_57.sql

Alternatively, you could just choose to load individual files based on your needs, but beware, certain objects have dependencies on other objects. You will need to ensure that these are also loaded.

### Generating a single SQL file

There is bash script within the root of the branch directory, called `generate_sql_file.sh`, that allows you to create a single SQL file from the branch.

This includes substitution parameters for the MySQL user to use, and whether to include or exclude `SET sql_log_bin` commands from the scripts. This is particularly useful for installations such as Amazon RDS, which do not have the root@localhost user, or disallow setting sql_log_bin.

When run, this outputs a file named such as `sys_<sys_version>_<mysql_version_identifier>_inline.sql`, i.e. `sys_1.2.0_56_inline.sql` is sys version 1.2.0, built for MySQL 5.6.

#### Options

* v: The version of MySQL to build the sys schema for, either '56' or '57'
* b: Whether to omit any lines that deal with sql_log_bin (useful for RDS)
* u: The user to set as the owner of the objects (useful for RDS)
* m: Whether to generate a mysql_install_db / mysqld --initialize formatted file

#### Examples

Generate a MySQL 5.7 SQL file that uses the 'mark'@'localhost' user:

    ./generate_sql_file.sh -v 57 -u "'mark'@'localhost'"

Generate a MySQL 5.6 SQL file for RDS:

    ./generate_sql_file.sh -v 56 -b -u CURRENT_USER

Generate a MySQL 5.7 bootstrap file:

    ./generate_sql_file.sh -v 57 -m

## Overview of objects

### Tables

#### sys_config

##### Description

Holds configuration options for the sys schema. This is a persistent table (using the `InnoDB` storage engine), with the configuration persisting across upgrades (new options are added with `INSERT IGNORE`). 

The table also has two related triggers, which maintain the user that `INSERTs` or `UPDATEs` the configuration - `sys_config_insert_set_user` and `sys_config_update_set_user` respectively.

Its structure is as follows:

```SQL
+----------+--------------+------+-----+-------------------+-----------------------------+
| Field    | Type         | Null | Key | Default           | Extra                       |
+----------+--------------+------+-----+-------------------+-----------------------------+
| variable | varchar(128) | NO   | PRI | NULL              |                             |
| value    | varchar(128) | YES  |     | NULL              |                             |
| set_time | timestamp    | NO   |     | CURRENT_TIMESTAMP | on update CURRENT_TIMESTAMP |
| set_by   | varchar(128) | YES  |     | NULL              |                             |
+----------+--------------+------+-----+-------------------+-----------------------------+
```

Note, when functions check for configuration options, they first check whether a similar named user variable exists with a value, and if this is not set then pull the configuration option from this table in to that named user variable. This is done for performance reasons (to not continually `SELECT` from the table), however this comes with the side effect that once inited, the values last with the session, somewhat like how session variables are init

[...截断...]

ed from global variables. If the values within this table are changed, they will not take effect until the user logs in again.

##### Options included

| Variable                             | Default Value | Description                                                                    |
| ------------------------------------ | ------------- | ------------------------------------------------------------------------------ |
| statement_truncate_len               | 64            | Sets the size to truncate statements to, for the `format_statement()` function. |
| statement_performance_analyzer.limit | 100           | The maximum number of rows to include for the views that does not have a built-in limit (e.g. the 95th percentile view). If not set the limit is 100. |
| statement_performance_analyzer.view  | NULL          | Used together with the 'custom' view. If the value contains a space, it is considered a query, otherwise it must be an existing view querying the performance_schema.events_statements_summary_by_digest table. |
| diagnostics.allow_i_s_tables         | OFF           | Specifies whether it is allowed to do table scan queries on information_schema.TABLES for the `diagnostics` procedure. |
| diagnostics.include_raw              | OFF           | Set to 'ON' to include the raw data (e.g. the original output of "SELECT * FROM sys.metrics") for the `diagnostics` procedure.|
| ps_thread_trx_info.max_length        | 65535         | Sets the maximum output length for JSON object output by the `ps_thread_trx_info()` function. |

### Views

Many of the views in the sys schema have both a command line user friendly format output, as well as tooling friendly versions of any view that contains formatted output duplicated as an x$ table.

The examples below show output for only the formatted views, and note where there is an x$ counterpart available.

#### host_summary / x$host_summary

##### Description

Summarizes statement activity, file IO and connections by host.

When the host found is NULL, it is assumed to be a "background" thread.

##### Structures (5.7)

```SQL
mysql> desc host_summary;
+------------------------+---------------+------+-----+---------+-------+
| Field                  | Type          | Null | Key | Default | Extra |
+------------------------+---------------+------+-----+---------+-------+
| host                   | varchar(60)   | YES  |     | NULL    |       |
| statements             | decimal(64,0) | YES  |     | NULL    |       |
| statement_latency      | text          | YES  |     | NULL    |       |
| statement_avg_latency  | text          | YES  |     | NULL    |       |
| table_scans            | decimal(65,0) | YES  |     | NULL    |       |
| file_ios               | decimal(64,0) | YES  |     | NULL    |       |
| file_io_latency        | text          | YES  |     | NULL    |       |
| current_connections    | decimal(41,0) | YES  |     | NULL    |       |
| total_connections      | decimal(41,0) | YES  |     | NULL    |       |
| unique_users           | bigint(21)    | NO   |     | 0       |       |
| current_memory         | text          | YES  |     | NULL    |       |
| total_memory_allocated | text          | YES  |     | NULL    |       |
+------------------------+---------------+------+-----+---------+-------+
12 rows in set (0.15 sec)

mysql> desc x$host_summary;
+------------------------+---------------+------+-----+---------+-------+
| Field                  | Type          | Null | Key | Default | Extra |
+------------------------+---------------+------+-----+---------+-------+
| host                   | varchar(60)   | YES  |     | NULL    |       |
| statements             | decimal(64,0) | YES  |     | NULL    |       |
| statement_latency      | decimal(64,0) | YES  |     | NULL    |       |
| statement_avg_latency  | decimal(65,4) | YES  |     | NULL    |       |
| table_scans            | decimal(65,0) | YES  |     | NULL    |       |
| file_ios               | decimal(