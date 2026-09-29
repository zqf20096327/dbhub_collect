# High Performance Tidb hw1
***
# Prerequisites

### Rust Installation
Installation guide https://www.rust-lang.org/tools/install
Tikv can only be complied using rust nightly version
Run the following command to use nightly version.
```sh
$ rustup default nightly
```
### Go Installation
Use brew to install go.
```sh
$ brew install go
```

# Building
### tidb
```sh
$ git clone https://github.com/TszKitLo40/tidb.git
$ cd tidb
$ make
```
### tikv
The binary file will be in the tikv/target/debug
```sh
$ git clone https://github.com/TszKitLo40/tikv.git
$ cd tikv
$ make build
```

### pd
```sh
$ git clone https://github.com/TszKitLo40/pd.git
$ cd pd
$ make
```

### Assignment
The code in [session.go](https://github.com/pingcap/tidb/blob/master/session/session.go) handles the session with client. In function NewTxn will start a new transaction. So I add code in this function which will write a log hello transaction
![code](https://github.com/TszKitLo40/high-performance-tidb-hw/blob/master/code.png) 

### Deploying the tidb cluster
1. Start tidb
    ```sh
    ./tidb/bin/tidb-server 
    ```
2. Start pd
    ```sh
    ./pd/bin/pd-server --name=pd1 \
                --data-dir=pd1 \
                --client-urls="http://127.0.0.1:2379" \
                --peer-urls="http://127.0.0.1:2380" \
                --initial-cluster="pd1=http://127.0.0.1:2380" \
                --log-file=pd1.log
    ```            
3. Start tikv cluster
    ```sh
    ./tikv/target/tikv-server --pd-endpoints="127.0.0.1:2379" \
                --addr="127.0.0.1:20160" \
                --data-dir=tikv1 \
                --log-file=tikv1.log

    ./tikv/target/tikv-server --pd-endpoints="127.0.0.1:2379" \
                --addr="127.0.0.1:20161" \
                --data-dir=tikv2 \
                --log-file=tikv2.log
    ./tikv/target/tikv-server --pd-endpoints="127.0.0.1:2379" \
                --addr="127.0.0.1:20162" \
                --data-dir=tikv3 \
                --log-file=tikv3.log
    ```     
4. Use mysql client to connect tidb and start a txn
    ```sh
    mysql --host 127.0.0.1 --port 4000 -u root
    $ START TRANSACTION;
    $ COMMIT;
    ```
    
### Runtime log
![log](https://github.com/TszKitLo40/high-performance-tidb-hw/blob/master/log.png) 
