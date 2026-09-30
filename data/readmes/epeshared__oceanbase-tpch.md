# oceanbase-tpch

## Oceanbase 4.0.0 配置
* tpch配置 https://www.oceanbase.com/docs/community-observer-cn-10000000000901377
* 租户配置 https://github.com/oceanbase/obdeploy/blob/master/docs/zh-CN/3.user-guide/3.obd-command/1.cluster-command-groups.md#obd-cluster-tenant-create

## oceanbase configuration for tpch
系统租户<br>
alter system set system_memory='15g';<br>
alter resource unit sys_unit_config max_memory='15g',min_memory='15g';<br>
alter system set enable_merge_by_turn= False;<br>
alter system set trace_log_slow_query_watermark='100s';<br>
alter system set max_kept_major_version_number=1;<br>
alter system set enable_sql_operator_dump=True;<br>
alter system set _hash_area_size='3g';<br>
alter system set memstore_limit_percentage=50;<br>
alter system set enable_rebalance=False;<br>
alter system set memory_chunk_cache_size='1g';<br>
alter system set minor_freeze_times=5;<br>
alter system set merge_thread_count=20;<br>
alter system set cache_wash_threshold='30g';<br>
alter system set syslog_level='PERF';<br>
alter system set max_syslog_file_count=100;<br>
alter system set enable_syslog_recycle='True';<br>

<br>
设置租户<br>
set global ob_sql_work_area_percentage=80;<br>
set global optimizer_use_sql_plan_baselines = true;<br>
set global optimizer_capture_sql_plan_baselines = true;<br>
alter system set ob_enable_batched_multi_statement='true';<br>
set global ob_query_timeout=36000000000;<br>
set global ob_trx_timeout=36000000000;<br>
set global max_allowed_packet=67108864;<br>

<br>
set global secure_file_priv="";<br>
grant file on *.* to tpch_100g_part;<br>

## load ddl
* cd to /path/to/TPC-H_Tools_v3.0.0/dbgen/load
* source /path/to/TPC-H_Tools_v3.0.0/dbgen/load/create_tpch_mysql_table_part.ddl
* python load.py

## queries
* cd to /path/to/TPC-H_Tools_v3.0.0/dbgen/queries
* ./tpch.sh
