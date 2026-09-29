# tidb-example-python

[![CI Workflow](https://github.com/pingcap-inc/tidb-example-python/actions/workflows/ci.yml/badge.svg)](https://github.com/pingcap-inc/tidb-example-python/actions/workflows/ci.yml)

English | [中文](/README-zh.md)

**tidb-example-python** is a sample project written by PingCAP for Python to connect to [TiDB](https://docs.pingcap.com/tidb/stable). You can find the following examples here.

**Driver**

- [PyMySQL](/pymysql_example.py) example
- [mysqlclient](/mysqlclient_example.py) example
- [mysql-connector-python](/mysql_connector_python_example.py) example

**ORM**

- [SQLAlchemy](/sqlalchemy_example.py) example
- [peewee](/peewee_example.py) example

**Framework**

- [Django](/django_example) example

**Scenario**

- [Serverless Tier connection](/serverless_tier_example.py) example
- [Butch delete](/batch_delete.py) example
- [Butch update](/batch_update.py) example
- [Avoid write skew](/write_skew_example.py) example
- [Optimistic and pessimistic transaction](/txn_example.py) example

## Dependcies

- [TiDB](https://docs.pingcap.com/tidb/stable)
- [mycli](https://www.mycli.net/)
- [Python 3.6+](https://www.python.org/)

## Run

### Run the Whole ORM and Driver Test

```bash
make test
```

### Run the particular test

Using run the `peewee_example.py` script as an example:

1. Install dependcy.

    ```bash
    pip install -r requirement.txt
    ```

2. Initial the table.

    ```bash
    mycli --host 127.0.0.1 --port 4000 -u root --no-warn < player_init.sql
    ```

3. Run the script.

    ```bash
    python3 peewee_example.py
    ```