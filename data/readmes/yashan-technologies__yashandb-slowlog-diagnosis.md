# Yashan Slow Diagnosis | 慢SQL分析诊断工具

## 简介

适用于崖山数据库的慢SQL日志解析工具，能够解析并分析崖山数据库的慢SQL日志，帮助DBA对崖山数据库进行性能调优。

## 特性

- 解析慢SQL日志文件
- 根据时间段筛选慢SQL
- 根据执行时间等字段对慢SQL进行排序
- 根据SQLID，SQL text等搜索慢SQL

## 快速上手

### 命令介绍

```shell
bash # ./yaslowdiag -h
Usage: yaslowdiag

yaslowdiag is a slow sql diagnosis tool of YashanDB.

Flags:
  -h, --help                                 Show context-sensitive help.
  -v, --version                              Show version.
  -c, --config="./config/yaslowdiag.toml"    Configuration file.
  -f, --file=STRING                          The slow sql file path
  -r, --range=STRING                         The time range of the check, such as '1M', '1d', '1h', '1m'. If <range> is given, <start> and <end> will be discard.
  -s, --start=STRING                         The start datetime of the check, such as 'yyyy-MM-dd', 'yyyy-MM-dd-hh', 'yyyy-MM-dd-hh-mm'
  -e, --end=STRING                           The end timestamp of the check, such as 'yyyy-MM-dd', 'yyyy-MM-dd-hh', 'yyyy-MM-dd-hh-mm', default value is current datetime.
      --search=STRING                        The search keyword
```

- -r，-s， -e用于指定日志时间范围。全部为空时默认检查365天内的慢SQL信息。
- -f 用于指定崖山数据库慢日志文件的路径。
- --search 用于指定要搜索的关键字。



### 最佳实践

```shell
# 分析/tmp/slow.log中365天内的慢日志数据
./yaslowdiag -f /tmp/slow.log

# 分析/tmp/slow.log中30天内的慢日志数据
./yaslowdiag -f /tmp/slow.log -r 30d

# 分析/tmp/slow.log中2024-07-30 到2024-08-20的慢日志数据
./yaslowdiag -f /tmp/slow.log  -s 2024-07-30 -e 2024-08-20

# 分析/tmp/slow.log 中包含select * from v$instance;的慢日志数据
./yaslowdiag -f /tmp/slow.log --search 'select * from v$instance;'

```




