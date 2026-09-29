# mysql/connector + TiDB python failover

- How to mysql failover in python
- Using TiDB
- Example python mysql connection failover

Scenario: You have at least 3 mysql nodes (or TiDB nodes as tested here)
and you randomly reboot them to simulate downtime.

It's confusing there's lots of python packages
for connecting to mysql. The 
https://pypi.org/project/mysql-connector-python/
package seems to be the only one which supports failover (is this correct?).

There are warnings that it's unstable if using in combination with sqlalchemy, but it's not clear how old those warnings are, pay attention to dates. 

This is an example of how to achieve failover


> NOTE: The 'failover' feature in mysql/connector as observed does *not* failover *after* a successful
  connection has been made, it is only during the `mysql.connector.connect` call that failover hosts
  are attempted (during the inital connection phase). It seems you have to teardown the connection
  and create a new one in order to benefit from the failover feature.

> NOTE: TiDB is an *implementation* of the Mysql protocol, it is not mysql- but can be used in the
same way. If has different design goals around high availability and the types of workloads it optmises
for. The automated failover of TiDB in combination with mysql/connector failover is a very interesting/useful
combination from an operations perspective (multi-master, without completly having to change database tooling.

## Testing


### What happends when first host is rebooted/goes down

The connector fails over in less than 1 seccond. 
TODO get more precise measurement.

Scenario: Rebook the currently connected database host:
```
Database host: 10.10.10.1 SELECT NOW() output: (datetime.datetime(2021, 12, 19, 14, 56),)
Database host: 10.10.10.1 SELECT NOW() output: (datetime.datetime(2021, 12, 19, 14, 56),)
Database host: 10.10.10.1 SELECT NOW() output: (datetime.datetime(2021, 12, 19, 14, 56, 1),)
Connection error: MySQL Connection not available.
Database host: 10.10.10.2 SELECT NOW() output: (datetime.datetime(2021, 12, 19, 14, 56, 2),)
Database host: 10.10.10.2 SELECT NOW() output: (datetime.datetime(2021, 12, 19, 14, 56, 3),)
```

> Note a reconnection has to take place using `mysql.connector.connect`,
  the connector does not failover the existing connection. (see `def connect_to_database`).

### What happens when **all** database hosts go down? 
Scenario: All datbase hosts restarted in error. Recovery time ~ 30 secconds.
```
Database host: 10.10.10.2 SELECT NOW() output: (datetime.datetime(2021, 12, 19, 15, 9, 27),)
Connection error: MySQL Connection not available.
Connection error: MySQL Connection not available.
Connection error: MySQL Connection not available.
Connection error: MySQL Connection not available.
Connection error: MySQL Connection not available.
Connection error: MySQL Connection not available.
Connection error: MySQL Connection not available.
Connection error: MySQL Connection not available.
Connection error: MySQL Connection not available.
Connection error: MySQL Connection not available.
Connection error: MySQL Connection not available.
Connection error: MySQL Connection not available.
Connection error: MySQL Connection not available.
Connection error: MySQL Connection not available.
Connection error: MySQL Connection not available.
Connection error: MySQL Connection not available.
Database host: 10.10.10.1 SELECT NOW() output: (datetime.datetime(2021, 12, 19, 15, 10, 17),)
```

Sometimes longer (dependant on leader election TiDB)


See also:

### Simplest example connecting to mysql database with python:
https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html

### What are all the connection options?

See https://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html

### How do I execute a simple query?

https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-select.html


## See also
https://stackoverflow.com/questions/21266171/how-to-configure-failover-in-sqlalchemy
