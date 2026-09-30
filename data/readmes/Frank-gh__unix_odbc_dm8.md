## [传送门](https://blog.csdn.net/xk_xx/article/details/104267525)
C++使用otl4通过unixodbc连接postgres
---
> 标题的信息量好大！是的，这不是心血来潮拿出来耍一耍的。这是改编自一个真实的项目。之前写过的连接数据库的应用也不算少了，但是用这么长的技术栈还真是头一回。
故事是这样的：**原有系统的数据库应用是基于OCI的，比较传统的架构，虽然OCI用起来不是那么方便，但是基本上在应用层使用的都是封装后的OCI接口，相对比较友好；后期使用了otl4，otl4用起来要比OCI/OCCI顺手些，主要是屏蔽掉了数据库的差异；最近要求将Oracle数据库换成GaussDB，经过简单的调研后，了解到GaussDB是基于postgres的分支进行研发的产品，所以理论上otl4是可以支持较小代价进行切换的，但是GaussDB的用户手册中明确告知对libpg支持不是很好，建议使用odbc的方式进行连接。所以就诞生了C++ + otl4 + unixodbc + postgres架构**

闲话说完了，开始整。。。

## 环境准备
需要准备的安装包（当然如果你可以直接接入公网可以直接选择apt，yum）
参考：[Ubuntu 安装 PostgreSQL](https://blog.csdn.net/xk_xx/article/details/105873881)

1. postgresql安装包：postgresql-12.2.tar.gz
2. unixodb安装包：unixODBC-2.3.7pre.tar
3. psql的odbc驱动：psqlodbc-12.01.0000.tar
4. otl4的头文件：otlv4_h2.zip
5. pgadmin：pgadmin4-4.21-x86.exe（可选）

以上的安装包到各种官网去down吧。

## 编译安装
- 系统环境
```bash
frank@LAPTOP-0OCJTGJR:~/software/postgresql-12.2$ uname -a
Linux LAPTOP-0OCJTGJR 4.4.0-18362-Microsoft #476-Microsoft Fri Nov 01 16:53:00 PST 2019 x86_64 x86_64 x86_64 GNU/Linux
frank@LAPTOP-0OCJTGJR:~/software/postgresql-12.2$ g++ -v
Using built-in specs.
COLLECT_GCC=g++
COLLECT_LTO_WRAPPER=/usr/lib/gcc/x86_64-linux-gnu/9/lto-wrapper
OFFLOAD_TARGET_NAMES=nvptx-none:hsa
OFFLOAD_TARGET_DEFAULT=1
Target: x86_64-linux-gnu
Configured with: ../src/configure -v --with-pkgversion='Ubuntu 9.2.1-9ubuntu2' --with-bugurl=file:///usr/share/doc/gcc-9/README.Bugs --enable-languages=c,ada,c++,go,brig,d,fortran,objc,obj-c++,gm2 --prefix=/usr --with-gcc-major-version-only --program-suffix=-9 --program-prefix=x86_64-linux-gnu- --enable-shared --enable-linker-build-id --libexecdir=/usr/lib --without-included-gettext --enable-threads=posix --libdir=/usr/lib --enable-nls --enable-bootstrap --enable-clocale=gnu --enable-libstdcxx-debug --enable-libstdcxx-time=yes --with-default-libstdcxx-abi=new --enable-gnu-unique-object --disable-vtable-verify --enable-plugin --enable-default-pie --with-system-zlib --with-target-system-zlib=auto --enable-multiarch --disable-werror --with-arch-32=i686 --with-abi=m64 --with-multilib-list=m32,m64,mx32 --enable-multilib --with-tune=generic --enable-offload-targets=nvptx-none,hsa --without-cuda-driver --enable-checking=release --build=x86_64-linux-gnu --host=x86_64-linux-gnu --target=x86_64-linux-gnu
Thread model: posix
gcc version 9.2.1 20191008 (Ubuntu 9.2.1-9ubuntu2)
frank@LAPTOP-0OCJTGJR:~/software/postgresql-12.2$
```
- 安装postgresql
```bash
./configure --prefix=/usr/local/pgsql --without-readline
# 需要注意的事`--without-readline`,readline这玩应儿呗淘汰了，
make
sudo make install
```

- 安装unixodbc
```bash
./configure --prefix=/usr/local/unixodbc
make
sudo make install
```

- 安装psql的odbc
```bash
./configure --prefix=/usr/local/psqlodbc --with-libpq=/usr/local/pgsql/ --with-unixodbc=/usr/local/unixodbc/
# --with-libpq pgsql的安装路径
# --with-unixodbc odbc安装路径

make
sudo make install
# 如果编译有问题看看是不是LD_LIBRARY_PATH的问题
# export LD_LIBRARY_PATH=/usr/local/unixodbc/lib:$LD_LIBRARY_PATH
```

## 配置

- 修改odbc配置
```bash
frank@LAPTOP-0OCJTGJR:/usr/local/unixodbc/etc$ pwd
/usr/local/unixodbc/etc
frank@LAPTOP-0OCJTGJR:/usr/local/unixodbc/etc$ ll
total 0
drwxr-xr-x 1 root root 512 May  5 13:18 ./
drwxr-xr-x 1 root root 512 May  5 12:55 ../
drwxr-xr-x 1 root root 512 May  5 12:55 ODBCDataSources/
-rw-r--r-- 1 root root 278 May  5 13:18 odbc.ini
-rw-r--r-- 1 root root 153 May  5 13:04 odbcinst.ini
```
`配置如下`
```bash
frank@LAPTOP-0OCJTGJR:/usr/local/unixodbc/etc$ cat odbc.ini
[pgsql]
Description=Test for PostgreSQL
Driver=PostgreSQL
Trace=Yes
TraceFile=sql.log
Database=postgres
Servername=localhost
UserName=postgres
Password=postgres
Port=5432
Protocol=6.4
ReadOnly=No
RowVersioning=No
ShowSystemTables=No
ShowOidColumn=No
FakeOidIndex=No
ConnSettings=
frank@LAPTOP-0OCJTGJR:/usr/local/unixodbc/etc$ cat odbcinst.ini
[PostgreSQL]
Description=PostgreSQL driver for Linux
Driver=/usr/local/psqlodbc/lib/psqlodbcw.so
Setup=/usr/local/psqlodbc/lib/psqlodbcw.so
UsageCount=1
```

## 验证
- 启动postgres
参考：[Ubuntu 安装 PostgreSQL](https://blog.csdn.net/xk_xx/article/details/105873881)
修改密码参考：[PostgreSQL忘记密码](https://blog.csdn.net/xk_xx/article/details/104876939)

- 运行pgadmin
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200506153722368.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3hrX3h4,size_16,color_FFFFFF,t_70)

表示postgres启动成功!


- 运行isql
创建软连接
```bash
frank@LAPTOP-0OCJTGJR:/lib64$ pwd
/lib64
frank@LAPTOP-0OCJTGJR:/lib64$ ll
total 0
drwxr-xr-x 1 root root 512 May  5 13:10 ./
drwxr-xr-x 1 root root 512 Apr 24 08:54 ../
lrwxrwxrwx 1 root root  32 Nov 29 22:19 ld-linux-x86-64.so.2 -> /lib/x86_64-linux-gnu/ld-2.30.so*
lrwxrwxrwx 1 root root  31 May  5 13:10 lipg.so.5 -> /usr/local/pgsql/lib/libpq.so.5
```
启动isql
```bash
frank@LAPTOP-0OCJTGJR:/usr/local/unixodbc/bin$ pwd
/usr/local/unixodbc/bin
frank@LAPTOP-0OCJTGJR:/usr/local/unixodbc/bin$ ./isql -v pgsql
+---------------------------------------+
| Connected!                            |
|                                       |
| sql-statement                         |
| help [tablename]                      |
| quit                                  |
|                                       |
+---------------------------------------+
SQL>
```
表示通过unixodbc可以连接pgsql了。


## 通过OTL4连接pgsql
- 数据库准备
```sql
-- Database: otlodbc

-- DROP DATABASE otlodbc;

CREATE DATABASE otlodbc
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'C.UTF-8'
    LC_CTYPE = 'C.UTF-8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

COMMENT ON DATABASE otlodbc
    IS 'otl4 for odbc';
    
-- SCHEMA: otluser

-- DROP SCHEMA otluser ;

CREATE SCHEMA otluser
    AUTHORIZATION postgres;
    
    
-- Table: otluser.company

-- DROP TABLE otluser.company;

CREATE TABLE otluser.company
(
    id integer NOT NULL,
    name character varying(20) COLLATE pg_catalog."default" NOT NULL,
    age integer NOT NULL,
    address character(25) COLLATE pg_catalog."default",
    salary numeric(18,2),
    CONSTRAINT company_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE otluser.company
    OWNER to postgres;
    
INSERT INTO otluser.COMPANY (ID,NAME,AGE,ADDRESS,SALARY) VALUES (1, 'Paul', 32, 'California', 20000.00);
```

- otlodbc.cpp
```c
#include <iostream>
using namespace std;
#include <stdio.h>
#include <string.h>
#include <stdlib.h>


#include <stdio.h>


#define OTL_ODBC // CompileOTL 4.0/ODBC  
#define OTL_ODBC_UNIX // uncomment this line if UnixODBC is used
//#define OTL_UNICODE // Compile OTL with Unicode    --->屏蔽 使用时中文显示乱码

#include "otlv4.h" // include the OTL 4.0 header file

otl_connect db; // connect object

void select()
{ 
    try{
        otl_stream ostream1(500, // buffer size
            "select * from otluser.company;",// SELECT statement
            db // connect object
            ); 
        // create select stream

        int id;
        int age;
        unsigned char name[255];
        unsigned char address[255];
        double salary;

        while(!ostream1.eof())
        { // while not end-of-data
            //ostream1>>id>>user>>name;
            ostream1>>id;
            ostream1>>name;
            ostream1>>age;
            ostream1>>address;
            ostream1>>salary;
            cout<<"id="<<id<<endl;
            cout<<"age="<<age<<endl;
            cout<<"name="<<name<<endl;
        }
    }
    catch(otl_exception& p)
    { // intercept OTL exceptions
        cout<<"otl_exception:"<<endl;
        cerr<<p.msg<<endl; // print out error message
        cerr<<p.stm_text<<endl; // print out SQL that caused the error
        cerr<<p.var_info<<endl; // print out the variable that caused the error
    }
}

int main()
{
    otl_connect::otl_initialize(); // initialize the database API environment
    try{
        db.rlogon("DSN=pgsql;UID=postgres;PWD=postgres;database=otlodbc"); // connect to the database
        select(); // select records from table
    }

    catch(otl_exception& p){ // intercept OTL exceptions
        cerr<<p.msg<<endl; // print out error message
        cerr<<p.stm_text<<endl; // print out SQL that caused the error
        cerr<<p.var_info<<endl; // print out the variable that caused the error
    }

    db.logoff(); // disconnect from the database

    return 0;

}
```

- CMakeLists.txt
```cmake
cmake_minimum_required (VERSION 2.6)
project (otlodbc)

set(CMAKE_CXX_FLAGS "-Wall")
set(CMAKE_CXX_FLAGS_DEBUG "-g3")
set(CMAKE_CXX_FLAGS_RELEASE "-O2")
set(CMAKE_BUILD_TYPE Debug)
include_directories(./)
include_directories(/usr/local/unixodbc/include)

add_executable(otlodbc otlodbc.cpp)
link_directories("/usr/local/psqlodbc/lib")
target_link_libraries(otlodbc /usr/local/psqlodbc/lib/psqlodbca.so)
```


- 运行结果
```bash
frank@LAPTOP-0OCJTGJR:~/project/database/build$ ./otlodbc 
id=1
age=32
name=Paul
```

