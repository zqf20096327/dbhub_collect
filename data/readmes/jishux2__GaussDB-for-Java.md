### 编译运行
`javac -encoding utf-8 -cp .\opengaussjdbc.jar GaussDBDemo.java;java -cp ".;./opengaussjdbc.jar" GaussDBDemo`

### 注意事项
1. GaussDB是华为推出的一款基于PostgreSQL的企业级数据库产品。
2. 如果标识符（模式名、表名、字段名等）中含有大写字母，那么在命名和引用时都应该用引号括起来，以区分大小写（）。
3. 在`from`子句中使用子查询时，必须给子查询的结果关系起一个别名，否则PostgreSQL会报错；而GaussDB在这方面的要求类似于Oracle，即允许（以省略关键字`as`的方式）对子查询的结果命名，但不支持对此关系的属性更名。
4. GaussDB**不支持**`year`等时间/日期函数（使用时会报错：`year is supported only in B-format database`）。不过你可以用`year_part()`函数**提取**年份，或者用`between`运算符**筛选**时间范围。
5. 在SQL语句中，要用`.`符号来连接模式名和关系名，表示关系属于哪个模式。例如，`"Schema_ljh_zzh".UserInfo`表示UserInfo关系属于Schema_ljh_zzh模式。
6. 在ResultSet中，不能用别名来获取列的值，比如`f1.UID1`和`f2.UID1`。这些别名只对SQL语句有用，ResultSet中只认识原来的列名，也就是`UID1`。如果想用别名，可以在SQL语句中给查询的列起一个新名字，或者直接用列的序号来访问。