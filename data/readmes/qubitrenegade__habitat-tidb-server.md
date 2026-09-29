# Habitat package: tidb

## Description

[TiDB](https://github.com/pingcap/tidb) built with Habitat.  Depends on [TiKV](https://github.com/qubitrenegade/habitat-tidb-tikv-server) and [PD](https://github.com/qubitrenegade/habitat-tidb-pd-server).  Refer to the [TiDB Documentation](https://www.pingcap.com/docs/) for information about tuning and architechture.

## Usage

### Minimum requirements:

* PD    - 3
* TiKV  - 1
* TiDB  - 1

### Running in local containers for development:

(The following assumes no more than one container already running locally)

#### Start PD

Run the following three times, omit the `-d` to run the container in the foreground and print logs to STDOUT.

```
docker run -d --rm qbrd/pd --peer 172.17.0.3 --peer 172.17.0.5 --topology leader
```

#### Start TiKV

Run the following 1 or 3+ times.  If run once, omit the `--topology leader`

```
docker run --rm --ulimit nofile=82920:82920 --memory-swappiness 0 \
  --sysctl ipv4.tcp_syncookies=0 --sysctl net.core.somaxconn=32768 \
  qbrd/tikv --bind pd:pd.default --peer 172.17.0.3 --peer 172.17.0.5 \
  --topology leader
```

#### Start TiDB

```
docker run --rm qbr/tidb --bind pd:pd.default --peer 172.17.0.3 --peer 172.17.0.5
```

#### Connect to the Databse

Depending on what the IP of the TiDB container is:

```
mysql -h 172.17.0.9 -P 4000
```

(no username or password was required... which might be bad...)
