# nacos+xxljob with oceanbase

> use oceanbase as nacos+xxljob mysql storage



## How to Running

* init database

```code
mysql-schema-m.sql and xxljob-m.sql
```

## Some Notes

oceanbase currently  only support  `OceanBase`  Engine some sql will contains 

`ENGINE=InnoDB` this will cause exception, we can delete this