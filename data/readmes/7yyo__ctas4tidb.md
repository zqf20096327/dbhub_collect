# ctas4tidb

A client that adds CTAS capability to TIDB.

## Usage
```shell
java -jar ctas4tidb.jar -uroot -P4000 -h127.0.0.1 -Dtest
```
```sql
➜  Desktop java -jar ctas4tidb.jar -uroot -P4000 -h127.0.0.1 -Dtest

Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 526998750
Server version: 8.0.11-TiDB-v8.5.0 TiDB Server (Apache License 2.0) Community Edition, MySQL 8.0 compatible

Copyright (c) 2000, 2024, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> CREATE TABLE customer_order_analysis AS
> SELECT c.customer_id,
>        c.customer_name,
>        c.city,
>        c.country,
>        COUNT(DISTINCT o.order_id)                                     AS total_orders,
>        SUM(o.total_amount)                                            AS total_amount,
>        AVG(o.total_amount)                                            AS avg_order_amount,
>        MAX(p.price)                                                   AS max_product_price,
>        (SELECT p2.product_name
>         FROM order_items oi2
>                  JOIN products p2 ON oi2.product_id = p2.product_id
>         WHERE oi2.order_id IN (SELECT o3.order_id
>                                FROM orders o3
>                                WHERE o3.customer_id = c.customer_id)
>         ORDER BY p2.price DESC
>         LIMIT 1)                                                      AS most_expensive_product,
>        (SELECT GROUP_CONCAT(DISTINCT p3.category ORDER BY p3.category)
>         FROM order_items oi3
>                  JOIN products p3 ON oi3.product_id = p3.product_id
>         WHERE oi3.order_id IN (SELECT o4.order_id
>                                FROM orders o4
>                                WHERE o4.customer_id = c.customer_id)) AS product_categories
> FROM customers c
>          LEFT JOIN
>      orders o ON c.customer_id = o.customer_id
>          LEFT JOIN
>      order_items oi ON o.order_id = oi.order_id
>          LEFT JOIN
>      products p ON oi.product_id = p.product_id
> GROUP BY c.customer_id, c.customer_name, c.city, c.country;

Query OK, 3 rows affected (0.2 sec)

mysql> 
```

## help
```sql
➜  Desktop java -jar ctas4tidb.jar -help
usage: ctas4tidb-cli
 -D,--database <arg>   Database name to use for connection (default: test)
 -h,--host <arg>       Connect to host (default: 127.0.0.1)
 -help,--help          Print this help message.
 -p,--password <arg>   Password to use when connecting to server
 -P,--port <arg>       Port number to use for connection (default: 4000)
 -u,--user <arg>       User for login if not current user (default: root)
```