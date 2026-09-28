# VideoServer
用作为个人学习linux服务器开发项目，简易视频点播服务器，实现对视频列表、用户信息的增删改查功能
### 服务端模块
服务端主要采用epoll网络IO并发模型和线程池（采用c语言pthread库编写）技术，负责视频列表数据的处理和储存，数据库采用sqlite3
### 客户端模块
客户端从服务端获取视频列表，调用了FFMpeg进行解码可以简单播放，视频数据从Live555服务器获取
### 压力测试模块
简单编写了压力测试端，短时内自动生成大量的连接到服务端，测试服务的处理能力
### 编译方式
***
大部分linux都能支持，需安装有sqlite3库，然后使用cmake工具进行源码编译：
```
mkdir build
cd build
cmake ..
make
``` 
执行生成的video_server、video_client程序