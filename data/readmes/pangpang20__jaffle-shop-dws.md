# The Jaffle Shop For GaussDB(DWS)

这个DEMO项目将展示如何使用dbt-core和dbt-gaussdbdws插件来开发一个数据仓库项目。支持华为GaussDB(DWS)。


##  前提条件

- 华为云GaussDB(DWS)的账号密码及其连接信息。
- 具备linux基本操作能力。
- 具备dbt-core的基本使用能力。

## 部署项目
提供两种方式部署项目：

- 克隆项目到本地，然后安装插件使用
- 使用docker部署，在容器中运行项目，好处是无需安装插件，直接运行即可


## 克隆项目到本地运行项目
### 安装插件

git的安装和github配置请参考[基于EulerOS配置GitHub](https://bbs.huaweicloud.com/blogs/441850)

在自己的工作目录克隆项目，比如: /opt
```bash
# 克隆项目
git clone git@github.com:pangpang20/jaffle-shop-dws.git
cd jaffle-shop-dws
```

在项目根目录下执行以下命令安装插件
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m pip install dbt-core dbt-gaussdbdws
```
如果安装报错提示http2协议错误，请使用以下命令：
```bash
git config --global http.version HTTP/1.1
```

查看版本信息
```bash
dbt --version
pip show dbt-core dbt-gaussdbdws

```

更新插件（可选）
```bash
pip install --upgrade dbt-gaussdbdws
```

### 配置项目
#### 创建数据库和用户（可选）
GaussDB中创建用户和数据库，参考SQL：
```sql
CREATE USER dbt_user WITH PASSWORD 'Dbtuser@123';
GRANT ALL PRIVILEGES to dbt_user;
CREATE DATABASE dbt_test OWNER = "dbt_user" TEMPLATE = "template0" ENCODING = 'UTF8'   CONNECTION LIMIT = -1;
```


#### 修改profiles.yml
```bash
cp sample-profiles.yml profiles.yml
vi profiles.yml
jaffle_shop:
  target: dev_dws
  outputs:
    dev_dws:
      type: gaussdbdws
      host: xx.xx.xx.xx
      user: dbt_user
      password: Dbtuser@123
      port: 8000
      dbname: dbt_test
      schema: jaffle_shop  # 如果这里有修改，下一步的dbt_project.yml也要同步修改
      threads: 4

```

#### 修改dbt_project.yml（可选）
修改dbt_project.yml中的profile，schema为 profiles.yml中的值：
```bash
profile: jaffle_shop
+schema: jaffle_shop
```
DEMO中已经配置好了，如果不一致，请参考上面修改。

参数`gaussdb_type` ,默认为1，主要区分是否有系统表`pg_matviews`,如果存在，设置为1。一般DWS集群版本为8.x，需要设置为0，9.x设置为1。

### 测试连接
使用下面的命令测试连接
```bash
dbt debug
```
如果连接成功，会输出类似下面的信息：
```bash
... ...
03:28:45    profiles.yml file [OK found and valid]
03:28:45    dbt_project.yml file [OK found and valid]
03:28:45  Required dependencies:
03:28:45   - git [OK found]

03:28:45  Connection:
03:28:45    host: 123.xx.xx.53
03:28:45    port: 8000
03:28:45    user: dbt_user
03:28:45    database: dbt_test
03:28:45    schema: jaffle_shop
03:28:45    connect_timeout: 10
03:28:45    role: None
03:28:45    search_path: None
03:28:45    keepalives_idle: 0
03:28:45    sslmode: None
03:28:45    sslcert: None
03:28:45    sslkey: None
03:28:45    sslrootcert: None
03:28:45    application_name: dbt
03:28:45    retries: 3
03:28:45  Registered adapter: gaussdbdws=1.0.1
03:28:45    Connection test: [OK connection ok]

03:28:45  All checks passed!
```

如果输出下面的信息，说明GaussDB的参数`password_encryption_type`为2，用户密码加密默认保存方式为SHA256，需要修改为1，同时支持MD5和SHA256的兼容模式。
```bash

connection to server at "xx.xx.xx.xx", port 8000 failed: none of the server's SASL authentication mechanisms are supported
```
原因是原生的psycopg2不支持SHA256的加密方式，只支持MD5。
下面提供两个途径实现修改：
- 方法一：联系GaussDB技术支持，修改参数`password_encryption_type`为1。
- 方法二：参考下面的方法，使用GaussDB提供的psycopg2替换原生psycopg2。
  ```bash
    # 华为云官网获取驱动包
    wget -O /tmp/GaussDB_driver.zip https://dbs-download.obs.cn-north-1.myhuaweicloud.com/GaussDB/1730887196055/GaussDB_driver.zip

    # 解压下载的文件
    unzip /tmp/GaussDB_driver.zip -d /tmp/ && rm -rf /tmp/GaussDB_driver.zip

    # 复制驱动到临时目录
    \cp /tmp/GaussDB_driver/Centralized/Hce2_arm_64/GaussDB-Kernel_505.2.0_Hce_64bit_Python.tar.gz /tmp/

    # 解压版本对应驱动包
    tar -zxvf /tmp/GaussDB-Kernel_505.2.0_Hce_64bit_Python.tar.gz -C /tmp/ && rm -rf /tmp/GaussDB-Kernel_505.2.0_Hce_64bit_Python.tar.gz

    # 卸载原生psycopg2
    pip uninstall -y $(pip list | grep psycopg2 | awk '{print $1}')


    # 将 psycopg2 复制到 python 安装目录下的 site-packages 文件夹下
    \cp /tmp/psycopg2 $(python3 -c 'import site; print(site.getsitepackages()[0])') -r

    # 修改 psycopg2 目录权限为 755
    chmod 755 $(python3 -c 'import site; print(site.getsitepackages()[0])')/psycopg2 -R

    # 将 psycopg2 目录添加到环境变量 $PYTHONPATH，并使之生效
    echo 'export PYTHONPATH="${PYTHONPATH}:$(python3 -c '\''import site; print(site.getsitepackages()[0])'\'')"' >> .venv/bin/activate

    # 对于非数据库用户，需要将解压后的 lib 目录，配置在 LD_LIBRARY_PATH 中
    echo 'export LD_LIBRARY_PATH="/tmp/lib:$LD_LIBRARY_PATH"' >> .venv/bin/activate

    # 激活虚拟环境,使之生效
    source .venv/bin/activate

    # 测试是否可以使用 psycopg2,没有报错即可
    (.venv) [root@ecs-euleros-dev ~]# python3
    Python 3.9.9 (main, Jun 19 2024, 02:50:21)
    [GCC 10.3.1] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import psycopg2
    >>> exit()
  ```
重新执行上面的测试连接命令，如果成功，说明psycopg2已经替换成功了。
### 安装依赖


```bash
# 安装依赖
dpt deps

# 修改文件中的关键字postgresql为gaussdbdws，因为依赖包中的dbt_packages/dbt_date还不支持gaussdb，需要替换
grep -rl postgresql | grep -E "\.py$|\.sql$|\.toml$|\.md$" | xargs sed -i 's/postgresql/gaussdbdws/g'
grep -rl postgres_ | grep -E "\.py$|\.sql$|\.toml$|\.md$" | xargs sed -i 's/postgres_/gaussdbdws_/g'

```

### 运行项目
前提条件：
- 数据库中已创建好schema为`jaffle_shop`
- 已经存在stg_开头的表



执行 `dbt run` 来运行项目,将stg开头的表经过数据清洗转换后加载结果表。
```bash
# 运行项目
dbt run

# 或者可以开启Debug模式，在运行过程中打印生成的每个 SQL 查询语句
dbt run -d --print
```
运行成功会得到如下输出：
```bash
... ...
11:40:54  Finished running 7 table models in 0 hours 0 minutes and 2.81 seconds (2.81s).
11:40:54  Command end result
11:40:54
11:40:54  Completed successfully
11:40:54
11:40:54  Done. PASS=7 WARN=0 ERROR=0 SKIP=0 TOTAL=7
11:40:54  Resource report: {"command_name": "run", "command_success": true, "command_wall_clock_time": 9.665491, "process_in_blocks": "0", "process_kernel_time": 0.303831, "process_mem_max_rss": "116404", "process_out_blocks": "5280", "process_user_time": 10.275382}
11:40:54  Command `dbt run` succeeded at 19:40:54.741590 after 9.67 seconds
11:40:54  Sending event: {'category': 'dbt', 'action': 'invocation', 'label': 'end', 'context': [<snowplow_tracker.self_describing_json.SelfDescribingJson object at 0xffffa04fcdf0>, <snowplow_tracker.self_describing_json.SelfDescribingJson object at 0xffff9fe34520>, <snowplow_tracker.self_describing_json.SelfDescribingJson object at 0xffff9eff5700>]}
11:40:54  Flushing usage events
```

在GaussDB中查看数据：
```sql
ANALYZE jaffle_shop.customers;
ANALYZE jaffle_shop.order_items;
ANALYZE jaffle_shop.orders;
ANALYZE jaffle_shop.products;
ANALYZE jaffle_shop.locations;
ANALYZE jaffle_shop.supplies;
ANALYZE jaffle_shop.metricflow_time_spine;

SELECT
    relname AS table_name,
    reltuples::BIGINT AS table_row_count
FROM
    pg_class c
JOIN
    pg_namespace n ON c.relnamespace = n.oid
WHERE
    n.nspname = 'jaffle_shop'
    AND c.relkind = 'r'
    AND c.relname not like 'stg%'
ORDER BY
    table_name;

```


输出结果：
| table_name            | table_row_count |
|-----------------------|-----------------|
| customers             | 934             |
| locations             | 5               |
| metricflow_time_spine | 3651            |
| order_items           | 90899           |
| orders                | 61947           |
| products              | 9               |
| supplies              | 64              |

至此，dbt core的jaffle-shop-dws项目已经运行成功。


## 基于Docker运行项目
### 前提条件

- docker,git已经安装
- 具备docker命令使用能力
- 已经添加 SSH 密钥到 GitHub
- 克隆项目到本地（基于ARM架构），如果是x86架构，请修改Dockerfile中的FROM指令

docker安装请参考[基于EulerOS部署Docker](https://bbs.huaweicloud.com/blogs/441849)

```bash
# 克隆项目
git clone git@github.com:pangpang20/jaffle-shop-dws.git

# 构建镜像
docker build -t jaffle-shop-dws:1.0.0  .

# 查看镜像
docker images

# 运行镜像，并进入容器(修改参数为实际的值)
docker run -it -e DB_HOST=xx.xx.xx.xx -e DB_PORT=xxx -e DB_USER=xxx -e DB_PASS=xxxx -e DB_NAME=xxxx -e DB_SCHEMA=xx --name jaffle-shop-dws  jaffle-shop-dws:1.0.0


# 如果是不带参数运行，则进入容器后需要修改profiles.yml
docker run -it --name jaffle-shop-dws  jaffle-shop-dws:1.0.0

```

### 测试连接

使用下面的命令测试连接

```bash
# 激活虚拟环境
source .venv/bin/activate

# 测试连接
dbt debug
```

如果连接成功，会输出类似下面的信息：
```bash
... ...
12:22:34  Connection:
12:22:34    host: 192.xx.xx.205
12:22:34    port: 8000
12:22:34    user: dbadmin
12:22:34    database: gaussdb
12:22:34    schema: jaffle_shop
12:22:34    connect_timeout: 10
12:22:34    role: None
12:22:34    search_path: None
12:22:34    keepalives_idle: 0
12:22:34    sslmode: None
12:22:34    sslcert: None
12:22:34    sslkey: None
12:22:34    sslrootcert: None
12:22:34    application_name: dbt
12:22:34    retries: 3
12:22:34  Registered adapter: gaussdbdws=1.0.1
12:22:34    Connection test: [OK connection ok]

12:22:34  All checks passed!
```


### 运行项目

执行 `dbt run` 来运行项目,将stg开头的表经过数据清洗转换后加载结果表。

```bash
# 运行项目
dbt run

# 或者可以开启Debug模式，在运行过程中打印生成的每个 SQL 查询语句
dbt run -d --print
```
运行成功会得到如下输出：
```bash
... ...
12:23:32  Finished running 7 table models in 0 hours 0 minutes and 3.03 seconds (3.03s).
12:23:32  Command end result
12:23:32
12:23:32  Completed successfully
12:23:32
12:23:32  Done. PASS=7 WARN=0 ERROR=0 SKIP=0 TOTAL=7
12:23:32  Resource report: {"command_name": "run", "command_success": true, "command_wall_clock_time": 8.262636, "process_in_blocks": "0", "process_kernel_time": 0.187725, "process_mem_max_rss": "118952", "process_out_blocks": "5280", "process_user_time": 7.825792}
12:23:32  Command `dbt run` succeeded at 12:23:32.384375 after 8.26 seconds
12:23:32  Sending event: {'category': 'dbt', 'action': 'invocation', 'label': 'end', 'context': [<snowplow_tracker.self_describing_json.SelfDescribingJson object at 0xffffa77aeb90>, <snowplow_tracker.self_describing_json.SelfDescribingJson object at 0xffffa6a66530>, <snowplow_tracker.self_describing_json.SelfDescribingJson object at 0xffffa50bf160>]}
12:23:32  Flushing usage events

# 退出容器
exit

```

在GaussDB中查看数据：
```sql
ANALYZE jaffle_shop.customers;
ANALYZE jaffle_shop.order_items;
ANALYZE jaffle_shop.orders;
ANALYZE jaffle_shop.products;
ANALYZE jaffle_shop.locations;
ANALYZE jaffle_shop.supplies;
ANALYZE jaffle_shop.metricflow_time_spine;

SELECT
    relname AS table_name,
    reltuples::BIGINT AS table_row_count
FROM
    pg_class c
JOIN
    pg_namespace n ON c.relnamespace = n.oid
WHERE
    n.nspname = 'jaffle_shop'
    AND c.relkind = 'r'
    AND c.relname not like 'stg%'
ORDER BY
    table_name;

```


输出结果：
| table_name            | table_row_count |
|-----------------------|-----------------|
| customers             | 934             |
| locations             | 5               |
| metricflow_time_spine | 3651            |
| order_items           | 90899           |
| orders                | 61947           |
| products              | 9               |
| supplies              | 64              |

至此，dbt core的jaffle-shop-dws项目已经运行成功。
