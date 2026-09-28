# ob_recoverydelete
**注意** 这个只是根据个人对 OceanBase 的维护经验而开发使用的小工具，不是官方出品的，其只在本人内部环境对一些误操作进行过旧数据捞回来作为回退参考。



### 使用方法

首先在 OB 里找到 DELETE 语句操作的时间点。

```sql
select * from gv$sql where sql_text like "%delete%" order by gmt_modified;
```

在所在分区的主副本找到对应时间段的 clog，使用 OceanBase 自带的工具反序列化。

```shell
ob_admin clog_tool dump_all 1788 1789 1790 1791 1792 1793 1794 > /tmp/clog.dump_all.log
```

通过分区 TID 来过滤日志。

```shell
cd /tmp/
grep ${table_id} clog.dump_all.log > ${table_id}.all.dump
```

最后提取旧的数据。

```shell
python ob_recoverydelete.py ${table_id}.all.dump > /tmp/raw_sql.log
```

如果要方便导入，需要再加工一下，这里使用 REPLACE INTO 或 INSERT INTO 作插入方式。

```shell
sed -i 's/"NULL"/NULL/g' /tmp/raw_sql.log
sed -i 's/^/REPLACE INTO db_name.tb_name VALUES/g' /tmp/raw_sql.log
```

