# oceanbase_perf_test

## Performance Test Result

### sysbench
1. Read Only overview (TPS)<br>

| ARCH                | taskset 100% CPU  | taskset %70 CPU    |
|---------------------|:-----------------:|-------------------:|
| SPR E0 (remote)     |68237 (total 192c )|60270               |
| ICX8360Y (remote)   |60348 (total 144c )|                    |
| SPR D0 (localhost)  |77359 (48c/s, 192c)|70253(40c/s, 160c)  |

2. Apple2Apple<br>

| ARCH                  |  32  |  40  |  48  |  56  |  64  |  72  |  80  |  88  |  96  |
|-----------------------|:----:|-----:|-----:|-----:|-----:|-----:|-----:|-----:|-----:|
| SPR E0 (remote)       |30756 |38904 |46451 |54203 |60829 |65108 |70253 |67386 |68747 |
| ICX8360Y(remote)      |26440 |33434 |40185 |46707 |53565 |60348 |      |      |      |
| SPRvsICX8360Y(SPEEDUP)|1.16  |1.16  |1.16  |1.16  |1.14  |1.08  |      |      |      |



## OS setting

### Configure Networking Queue
* ethtool -L $eth1 combined $cnt (设置网卡eth1的quque数为cnt)
* ethtool -l ens11f0np0 (查看修改是否成功)

### task set
1. 查看CPU 核数
 *. numactl -H
2. bind 所有 CPU
 * taskset -a -pc 0-223 166023 (166023是进程号)
3. bind 一半 CPU
 * taskset -a -pc 0-39,112-151,56-105,168-207 166023

### 修改/etc/sysctl.conf
vi /etc/sysctl.conf<br>
<br>
fs.file-max = 1000000 <br>
fs.aio-max-nr = 1048576 <br>
kernel.core_uses_pid = 1<br>
net.core.netdev_max_backlog = 262144<br>
net.core.rmem_default = 8388608<br>
net.core.rmem_max = 16777216<br>
net.core.somaxconn = 32769<br>
net.core.wmem_default = 8388608<br>
net.core.wmem_max = 16777216<br>
net.ipv4.tcp_max_syn_backlog = 262144<br>
net.ipv4.tcp_rmem = 4096 87380 4194304<br>
net.ipv4.tcp_sack = 1<br>
net.ipv4.tcp_keepalive_intvl = 20<br>
net.ipv4.tcp_keepalive_probes = 3<br>
net.ipv4.tcp_keepalive_time = 60<br>
net.ipv4.tcp_fin_timeout = 5<br>
net.ipv4.tcp_synack_retries = 2<br>
net.ipv4.tcp_timestamps = 1<br>
net.ipv4.tcp_tw_reuse = 1<br>
net.ipv4.tcp_max_tw_buckets = 262144<br>
net.ipv4.ip_local_reserved_ports = 5050,5258,5288,6666,6268<br>
net.ipv4.tcp_syncookies = 0<br>
net.ipv4.tcp_window_scaling = 1<br>
net.ipv4.tcp_wmem = 4096 16384 4194304<br>
net.nf_conntrack_max = 1200000<br>
net.netfilter.nf_conntrack_max = 1200000<br>
vm.vfs_cache_pressure = 1024<br>
vm.swappiness = 0<br>
vm.overcommit_memory = 1<br>
vm.zone_reclaim_mode = 0<br>
vm.max_map_count = 16471966<br>
vm.min_free_kbytes = 4194304<br>
<br>
sysctl -p
### ulimit
ulimit -n 655350<br>


## Oceanbase reousrce configuration
<br>
创建资源单元<br>
* SPR: create resource unit sysbench_unit max_cpu 144, max_memory '60G', max_iops 128, max_disk_size 53687091200, max_session_num 64, MIN_CPU=144, MIN_MEMORY='60G', MIN_IOPS=128;<br>
* ICX: create resource unit sysbench_unit max_cpu 130, max_memory '60G', max_iops 128, max_disk_size 33687091200, max_session_num 64, MIN_CPU=130, MIN_MEMORY='60G', MIN_IOPS=128;
<br>
创建资源池<br>
create resource pool sysbench_pool unit = 'sysbench_unit', unit_num = 1, zone_list=('zone1');<br>
创建租户<br>
create tenant sysbench_tenant resource_pool_list=('sysbench_pool'), charset=utf8mb4, replica_num=1, zone_list('zone1'), primary_zone=RANDOM, locality='F@zone1' set variables ob_compatibility_mode='mysql', ob_tcp_invited_nodes='%';<br>
<br>
alter system set enable_auto_leader_switch=false;<br>
alter system set enable_one_phase_commit=false;<br>
alter system set weak_read_version_refresh_interval='5s';<br>
alter system set system_memory ='30G';<br>
alter system set syslog_level='PERF';<br>
alter system set max_syslog_file_count=100;<br>
alter system set enable_syslog_recycle='True';<br>
alter system set trace_log_slow_query_watermark='10s';<br>
alter system set large_query_threshold='1s';<br>
alter system set clog_sync_time_warn_threshold='2000ms';<br>
alter system set syslog_io_bandwidth_limit='10M';<br>
alter system set enable_sql_audit=false;<br>
alter system set enable_perf_event=false; <br>
alter system set clog_max_unconfirmed_log_count=5000;<br>
alter system set memory_chunk_cache_size ='16G';<br>
alter system set autoinc_cache_refresh_interval='86400s';<br>
alter system set cpu_quota_concurrency=2;<br>
alter system set enable_early_lock_release=false tenant=all;<br>
alter system set  default_compress_func = 'lz4_1.0';<br>
<br>
把日志聚合，减小网络开销，提高并发读<br>
alter system set _clog_aggregation_buffer_amount=4;<br>
alter system set _flush_clog_aggregation_buffer_timeout='1ms';<br>
set global ob_timestamp_service='GTS';<br>
set global autocommit=ON;<br>
set global ob_query_timeout=36000000000;<br>
set global ob_trx_timeout=36000000000;<br>
set global max_allowed_packet=67108864;<br>
set global ob_sql_work_area_percentage=100;<br>
<br>
/*
parallel_max_servers推荐设置为测试租户分配的resource unit cpu数的10倍
如测试租户使用的unit配置为：create resource unit $unit_name max_cpu 26
那么该值设置为260
parallel_server_target推荐设置为parallel_max_servers * 机器数*0.8
那么该值为260*3*0.8=624
*/<br>
set global parallel_max_servers=1440;<br>
set global parallel_servers_target=1152;<br>

/* change it when number of total core > 64 */<br>
alter system set net_thread_count = 36;<br>

ALTER SYSTEM SET _ob_enable_prepared_statement=TRUE;

mysql -uroot -P3881 -h127.0.0.1

## Test script
1. cd /data02/ob_data/spr_test;numactl --cpunodebind=0 /mnt/nvme4/xtang/oceanbase-master/build_release/src/observer/observer r '127.0.0.1:3882:3881' -o __min_full_resource_pool_memory=268435456,memory_limit='80G',system_memory='4G',datafile_disk_percentage=10,enable_syslog_recycle=True,max_syslog_file_count=4 -z 'zone1' -p 3881 -P 3882 -c 1 -d '/data02/ob_data/spr_test/store' -i 'lo' -l 'ERROR' -- exited code 0
2. ../sysbench oltp_read_only.lua --mysql-host=127.0.0.1 --mysql-port=3881 --mysql-db=test --mysql-user=root@sysbench_tenant --table_size=1000000 --tables=30 --threads=64 --report-interval=10 --time=600 run


## Limit CPU and LLC usage
<br>
Here is an example of adjusting LLC size:<br>
#set a policy of using 2 ways of LLC:  <br>
pqos -e "llc:1=0x0003"<br>
<br>
#associate core with policy: <br> 
pqos -a "llc:1=0-3,48-51,24-27,72-75;"<br>
<br>
#reset to default: <br>
pqos -R<br>
<br>
#query how may associative ways of llc: <br>
getconf -a|grep CACHE<br>

## 配置无需密码远程登录

按以下步骤设置无密码 SSH 登录：<br>
<br>
在中控机器上运行以下命令查看密钥是否存在：<br>
ls ~/.ssh/id_rsa.pub<br>
如果密钥已经存在，则无需生成新的密钥。<br>
<br>
#1.（可选）在中控机器上运行以下命令生成 SSH 公钥和私钥：<br>
ssh-keygen -t rsa<br>

#2.在中控机器上运行以下命令将第一步生成的公钥上传至目标服务器的 .ssh 文件夹：<br>
scp /root/.ssh/id_rsa.pub root@<server_ip>:/root/.ssh/<br>
<br>
#3.在目标机器上运行以下命令，将中控机器传入的公钥写到 authorized_keys：<br>
cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys<br>
<br>
#4.在中控机器上运行以下命令登录目标机器：<br>
ssh root@<server_ip><br>
<br>
重复步骤，为每台机器设置无密码登录 SSH。<br>

## Config LLC
调整SPR/ICX核数、频率为相同值，测试在不同核数下的Scaling情况：<br>
<br>
a)	调整核数方法：<br>
Enable core:<br>
for i in {16..111}; do echo 1 > /sys/devices/system/cpu/cpu$i/online; done<br>
disable core:<br>
for i in {16..111}; do echo 0 > /sys/devices/system/cpu/cpu$i/online; done<br>
<br>
b)	固定主频方法：<br>
for i in {16..111}; echo 2700000 > /sys/devices/system/cpu/cpu$i/cpufreq/scaling_max_freq; done //我一般固定到2.7GHz<br>
<br>
<br>
c)	调整L3 Cache的大小：<br>
每一代CPU Per core 的L3大小一般是固定的，如果减少了CPU的核数，就需要相应地减少L3 Cache的大小。减少L3 Cache大小是通过减少L3 associative way的数量来实现。<br>

距离来说，对于ICX, L3 associative way 是12， per core L3的大小是1.5MB, 38核的ICX就是57MB。 如果要把它变为16核的，那么就需要相应调整L3的大小为： (16/38) *12，然后四舍五入得5，5就是5个1，即11111，16进制是001F，所以llc:1=0x001F。<br>
下面是设置需要用到的相关命令：<br>
set a policy:  pqos -e "llc:1=0x0003"  //per way per bit, it means to use 2 ways (11)<br>
associate core with policy: pqos -a "llc:1=0-3,48-51,24-27,72-75;"<br>
reset CAT:  pqos -R<br>
query how may associative ways of llc: getconf -a|grep CACHE<br>
query size of each cache: lshw -C memory<br>

d)	调整uncore frequency<br>
由于不同核数的功耗是不同的，这会影响uncore的频率，所以在测试core scaling时，一般还需要固定uncore frequency，<br>
pcm-msr.x  -a 0x620 -w 0x1414 //这个命令是设置为2.0GHz,<br>

## Resource

https://intel.sharepoint.com/sites/ProcessorCounterMonitor-internal \

