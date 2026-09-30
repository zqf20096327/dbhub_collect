# dmR

dmR是为在Linux下使用R语言进行达梦数据库操作、兼容ROracle接口的R语言工具包

## 兼容版本

| R版本   | DBI版本 | dmR版本 |
| ------- | ------- | ------- |
| 3.3.0 + | 1.0.0 + | 1.2.0 + |

## 主要功能

- 连接达梦数据库
- 执行SQL语句

## 安装dmR包（安装RDameng）

dmR包(RDameng包)在安装使用前源码目录下文件需要经过设置，然后打包使用。

### 1、环境安装

安装R与DBI。

### 2、通过源码安装注意事项

获取dmR源码，需要确认configure文件具有执行权限，如果configure不具备执行权限，需要在打包前设置，执行权限设置完成后打包成压缩包，该压缩包才是安装包，例如：

```shell
unzip dmR-1.2.0.zip 
mv dmR-1.2.0 RDameng
cd RDameng/
chmod +x configure
chmod +x cleanup 
cd ..
tar  -zcvf RDameng-1.2.0.tar.gz RDameng
```

### 3、开始安装

RDameng包安装有两种方式，可以根据情况自由选择安装方式。

在运行安装命令前，首要的准备工作是设置LD_LIBRARY_PATH包含libdmdci.so路径，例如当libdmdci.so在路径/path/to/libdmdci下时，运行命令:

```shell
export LD_LIBRARY_PATH=/path/to/libdmdci:$LD_LIBRARY_PATH
```

或者

```shell
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/path/to/libdmdci
```

#### 3.1、方式一

通过设置环境变量DM_HOME进行编译。

设置环境变量$DM_HOME用于编译，例如DM_HOME=/opt/dmdbms时，文件结构即包含内容要求的示例如下：

```shell
/opt/dmdbms
├── include
│   ├── DCI1.h
│   └── DCI.h
├── bin
│   └── libdmdci.so
```

设置DM_HOME环境变量，示例如下：

```shell
export DM_HOME=/opt/dmdbms
```

设置DM_HOME后，可运行以下安装命令：

```shell
R CMD INSTALL /path/to/RDameng-1.2.0.tar.gz
```

#### 3.2、方式二

通过设置--configure-args编译参数--with-dci-lib和--with-dci-inc进行编译。

--with-dci-lib需要指定包含libdmdci.so的绝对路径，--with-dci-inc需要指定包含头文件DCI.h和DCI1.h的绝对路径，文件结构示例：

```shell
Directory
├── dci_inc
│   ├── DCI1.h
│   └── DCI.h
├── dci_libs
│   └── libdmdci.so
```

确认libdmdci.so和头文件准备完毕后，再运行设置--configure-args编译参数方式的 RDameng 安装命令，示例如下：

```shell
R CMD INSTALL --configure-args='--with-dci-lib=/path/to/dci_libs --with-dci-inc=/path/to/dci_inc'  /path/to/RDameng-1.2.0.tar.gz
```



运行安装命令后，看到如下信息即表示安装成功：

```shell
*** installing help indices

** building package indices

** testing if installed package can be loaded

\* DONE (RDameng)
```

检查 RDameng 是否成功安装，如下所示：

```R
library(DBI)
library(RDameng)
```

若安装成功，llibrary(RDameng)加载后应无警告或异常信息，若出现如下信息：

```shell
package or namespace load failed for ‘RDameng’ in dyn.load(file, DLLpath = DLLpath, ...): 

无法载入共享目标对象‘/path/to/R/R-3.x.x/library/RDameng/libs/RDameng.so’：:

libdmdci.so: 无法打开共享对象文件: 没有那个文件或目录
```

则需要检查 LD_LIBRARY_PATH 设置是否指定了 DM DCI 库（libdmdci.so）的位置，例如

```shell
echo $LD_LIBRARY_PATH
```

libdmdci.so可在[达梦数据官网下载中心](https://www.dameng.com/list_103.html&amp)获取。

## 开始使用

RDameng 包正确安装后，可运行如下 R 脚本，连接 DM 数据库，执行简单 SQL 语句,测试 RDameng 加载情况，脚本如下：

```R
library(DBI)
library(RDameng)
dmdrv <- dbDriver("Dm")

#IP 地址
dmHost <-"127.0.0.1"
#数据库服务名称
dmServerName <- "DmServiceDMSERVER"
#用户名
dmUserName <-"SYSDBA"
#密码
dmPassword <-"Hust4400_DBA"
#拼写 TNS 字符串，达梦数据库默认端口 5236
dmconnect.string<-paste("(DESCRIPTION=(ADDRESS=(PROTOCOL=tcp)(HOST=",dmHost,")(PORT=5236))(CO
NNECT_DATA=(SERVICE_NAME=", dmServerName, ")))", sep = "")
#连接达梦数据库
dmCon <- dbConnect(dmdrv,username = dmUserName, password = dmPassword,dbname = dmconnect.string )
#执行 SQL 语句
dbGetQuery(dmCon, paste("create table RTEST_TABLE(COLUMN_1 varchar2(50)) "))
dbGetQuery(dmCon, paste("insert into RTEST_TABLE values('Hello DM server') "))
dbGetQuery(dmCon, paste("select * from RTEST_TABLE ") )
```

执行结果：

```shell
COLUMN_1

1 Hello DM server 
```
