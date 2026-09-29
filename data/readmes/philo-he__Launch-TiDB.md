This repository mainly includes the source code of Pd, TiKV and TiDB for building shared libraries.

## Build prerequisite

1. build Rocksdb.

   run build_rocksdb.sh

2. install Golang (1.5+ version).

   https://golang.org/dl/

   Suppose ${GO_HOME} is the path where golang is installed. Please set ${GO_HOME}/bin/ in $PATH.
   If ${GO_HOME} is not under /usr/local/, please set $GOROOT: export GOROOT=${GO_HOME}.

3. install Rust. Only the nightly version is valid.

   https://www.rust-lang.org/en-US/other-installers.html

## Support SSM project

  To enable TiDB in SSM (https://github.com/Intel-bigdata/SSM.git), you should run build_shared_libs.sh to generate three files with .so suffix under lib/ directory in this project.

  After build is completed, you should put libpd.so, libtikv.so and libtidb.so into {SSM_HOME}/lib.
  The libtikv.so is dynamically linked to librocksdb.so.5.6. So you should also build rocksdb as build prerequisite section guides on each host where TiKV is deployed.

## Run demo

  Run compile.sh to compile the java code and run start.sh to start tidb.

## Deployment tips

1. unset http_proxy and https_proxy.

2. Options for PD, TiKV and TiDB.

   The client-urls option for pd must be a http address and a hostname is not valid.
   The addr option for tikv should be an ip address without starting with http.
   The pd option for tikv and the path option for tidb can be either a hostname or an ip address.
   In the cluster situation, the client-url option for pd and the addr option for tikv should not be 127.0.0.1.

   Here is an example.

   For Pd server, --name=pd --data-dir=pd --client-urls="http://192.168.150.104:2379" --peer-urls="http://192.168.150.104:2380" --log-file=pd.log

   For Tikv server, --pd="192.168.150.104:2379" --addr="192.168.150.109:20160"  --data-dir=tikv --log-file=tikv.log

   For Tidb server, --store=tikv --path="192.168.150.104:2379" --log-file=tidb.log
