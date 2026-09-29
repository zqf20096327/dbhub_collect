# tpcds-kit

The official TPC-DS tools can be found at [tpc.org](http://www.tpc.org/tpc_documents_current_versions/current_specifications.asp).

This tpcds-kit is ported from [gregrahn/tpcds-kit](https://github.com/gregrahn/tpcds-kit), thanks to [gregrahn](https://github.com/gregrahn), this version is based on v2.7.0 and has been modified to:
* Allow compilation under macOS (commit [2ec45c5](https://github.com/gregrahn/tpcds-kit/commit/2ec45c5ed97cc860819ee630770231eac738097c))
* Address obvious query template bugs like
  * https://github.com/gregrahn/tpcds-kit/issues/30
  * https://github.com/gregrahn/tpcds-kit/issues/31
  * https://github.com/gregrahn/tpcds-kit/issues/33

## 1. Setup

### 1.1 install required development tools

Make sure the required development tools are installed:

- Ubuntu: `sudo apt-get install gcc make flex bison byacc git`
- CentOS/RHEL: `sudo yum install gcc make flex bison byacc git`
- MacOS: `xcode-select --install`

### 1.2 clone the code

`git clone https://github.com/huaj1101/tidb-tpcds-kit.git`

### 1.3 build

- Linux: `cd tools && make OS=LINUX -j8 && cd -`
- MacOS: `cd tools && make OS=MACOS -j8 && cd -`

## 2. Data generation

Data generation is done via `dsdgen`:
```sh
# "-sc" is used to specify the volume of data to generate in GB.
cd tools && ./dsdgen -sc 100 -f && cd -
```

## 3. Load Data
```sh
mysql -h 192.168.6.128 -P 4000 -u root -p123 -D test -e "drop database if exists tpcds;"
mysql -h 192.168.6.128 -P 4000 -u root -p123 -D test -e "create database tpcds;"
mysql -h 192.168.6.128 -P 4000 -u root -p123 -D tpcds < tools/tpcds.sql
./load_data.sh
```


## 4. prepare work before query

mysql -h 192.168.6.128 -P 4000 -u root -p123 -D tpcds < tools/analyze_tables.sql
mysql -h 192.168.6.128 -P 4000 -u root -p123 -D tpcds < tools/set_variables.sql

## 5. Run Queries

Sample queries from the 100GB scale factor can be found in the `queries/` directory.  The `query-templates/` directory contains the Apache Impala TPC-DS query templates which can be used with `dsqgen` (found in the official TPC-DS tools) to generate queries for other scale factors or to generate more queries with different substitution variables.
