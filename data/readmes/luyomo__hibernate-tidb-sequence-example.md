* hibernate-tidb-sequence-example
  | Software       | Version |
  |----------------+---------|
  | JAVA           |     1.8 |
  | hibernate-core |  5.2.11 |
Please check the source code how to prepare the java code for TiDB sequence. [[https://github.com/luyomo/hibernate-tidb-sequence-example/blob/main/src/main/java/com/pingcap/hibernate/Example.java][Example.java]]

* Run the example
** Setup TiDB cluster
 #+BEGIN_SRC
MySQL [mysql]> create database hibernate_seq_on_tidb;
MySQL [mysql]> use hibernate_seq_on_tidb;
MySQL [hibernate_seq_on_tidb]> CREATE SEQUENCE orderid_seq INCREMENT 1 MINVALUE 1 MAXVALUE 10000 START 1 CACHE 1 CYCLE;
MySQL [hibernate_seq_on_tidb]> CREATE SEQUENCE userid_seq  INCREMENT 1 MINVALUE 1 MAXVALUE 10000 START 1 CACHE 1 CYCLE;
 #+END_SRC
** Download this source code
#+BEGIN_SRC
user@workstation:/tmp$ git clone https://github.com/luyomo/hibernate-tidb-sequence-example.git
user@workstation:/tmp$ cd hibernate-tidb-sequence-example
#+END_SRC
** Replace the DB conntion in the config file [[https://github.com/luyomo/hibernate-tidb-sequence-example/blob/main/src/main/resources/hibernate.properties][hibernate.properties]]
 #+BEGIN_SRC
user@workstation:/tmp/hibernate-tidb-sequence-example$ more src/main/resources/hibernate.properties
 hibernate.dialect org.hibernate.dialect.TiDB4Dialect
 hibernate.connection.driver_class com.mysql.jdbc.Driver
 hibernate.connection.url jdbc:mysql://127.0.0.1:4000/hibernate_example      <<- Replace the connection string(The name in this example is hibernate_seq_on_tidb)
 hibernate.connection.username root                                          <<- User to connect to TiDB
 hibernate.connection.password                                               <<- Password to connect to TiDB
 
 hibernate.id.new_generator_mappings false
 hibernate.globally_quoted_identifiers true
 # hibernate.globally_quoted_identifiers_skip_column_definitions true
 # hibernate.auto_quote_keyword true
 
 hibernate.hbm2ddl.auto update
 #+END_SRC

** Install the JAVA 8
** Run the example application
#+BEGIN_SRC
user@workstation:/tmp/hibernate-tidb-sequence-example$ ./gradlew run

> Task :run
Nov 05, 2021 3:28:48 AM org.hibernate.Version logVersion
INFO: HHH000412: Hibernate Core {5.2.11.Final}
... ... ...
BUILD SUCCESSFUL in 3s
3 actionable tasks: 2 executed, 1 from cache
#+END_SRC
** Table/Data confirmation
#+BEGIN_SRC
MySQL [hibernate_seq_on_tidb]> show tables;
+---------------------------------+
| Tables_in_hibernate_seq_on_tidb |
+---------------------------------+
| Example$Order                   |
| Example$User                    |
| orderid_seq                     |
| userid_seq                      |
+---------------------------------+
4 rows in set (0.001 sec)
MySQL [hibernate_seq_on_tidb]> select * from Example$User;
+--------+--------+--------+
| userId | gender | name   |
+--------+--------+--------+
|     50 |      0 | Tommas |
|     51 |      0 | Jack   |
+--------+--------+--------+
2 rows in set (0.006 sec)
MySQL [hibernate_seq_on_tidb]> select * from Example$Order;
+---------+-------+--------+
| orderId | price | userId |
+---------+-------+--------+
|      50 |   500 |     50 |
|      51 |   200 |     50 |
+---------+-------+--------+
2 rows in set (0.007 sec)
#+END_SRC

* Note
  [[https://github.com/bb7133/tidb-hibernate-example][tidb-hibernate-example]] - Customized the source code to show TiDB sequence in the hibernate orm
