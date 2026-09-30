# opengauss-serverless-demo测试运行
## 前期准备
参考openGauss的环境准备

## rust依赖安装
$ curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf | sh

## HTTP服务器配置
HTTP服务器用于节点间的通信。

所有节点，包括执行节点（运行执行器），调度节点（负责解析SQL和提供数据），都要运行HTTP服务器，每个服务器的配置都相同
### HTTP服务器配置修改
进入storage_server目录打开**src/main.rs**
修改HTTP服务器的ip和端口，默认为本地ip和8080端口启动
- 修改DB_NAME为sql查询的数据库名称
- 修改DB_USER为sql查询的用户名
- 修改DB_PORT为数据库server启动的端口（默认是5432）
- 修改STORAGE_DIR为openGauss数据目录路径：每个节点都应挂载相同的数据，用于模拟共享存储的数据
- 监听所有本地 IPv4 网络接口上的 8080 端口，充当服务器
  `let addr = SocketAddr::from(([0, 0, 0, 0], 8080));`

### HTTP服务器启动

在storage_server目录运行 
  `cargo run`

## openGauss节点配置

每个节点都应挂载相同的数据，用于模拟共享存储的数据

### 执行节点配置
执行节点只处理执行器相关逻辑。
在src/gausskernel/storage/cstore/custorage.cpp修改下面代码的"localhost:8080"为存储服
务器ip和开放端口，用以从存储服务器取数据。
    
    httplib::Client client("localhost:8080");

### 调度节点配置
存储节点负责解析SQL和存储数据。

在src/gausskernel/process/tcop/postgres.cpp中修改下面代码的"localhost:8080"为执行节点的ip和开放端口，用以向执行节点发送物理计划。
    
    httplib::Client client("localhost:8080");

### 编译

    cmake .. -DENABLE_MULTIPLE_NODES=OFF -DENABLE_THREAD_SAFETY=ON -DENABLE_READLINE=ON -DENABLE_MOT=ON -DENABLE_OPENEULER_MAJOR=ON -DUSE_ONNX=OFF


### 启动数据库server
每个节点都要启动数据库

    gs_ctl start -D 数据目录路径 -Z single_node -l logfile

### 创建数据库
参考openGauss的步骤创建TPC-H数据库，加载数据

### 执行query

    gsql -d 数据库名称 -p 5432 -U 用户名称 -f simple_query.sql


