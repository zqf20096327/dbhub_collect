## linux安装过程
    tar -jxf openGauss-Server-6.0.0-CentOS7-x86_64.tar.bz2 -C /opt/software/openGau
    
    sh install.sh  -w "1qaz2wsx3EDC" -p 5432 &&source ~/.bashrc


## 重启openGauss
    启动
    gs_ctl start -D /opt/software/openGauss/data/single_node -Z single_node

    暂停
    gs_ctl stop -D /opt/software/openGauss/data/single_node -Z single_node
    
    重启
    gs_ctl restart -D /opt/software/openGauss/data/single_node -Z single_node

    查看数据库主节点的端口号
    cat /opt/software/openGauss/data/single_node/postgresql.conf | grep port


## 连接openGauss
    gsql -h localhost -p 5432 -U openGauss -d school
    
    gs_ctl query -D /opt/software/openGauss/data/single_node

## 创建新用户
# 连接到 openGauss 数据库
gsql -h localhost -p 5432 -U gaussdb -d your_database

# 创建新用户
CREATE USER cas WITH PASSWORD '1qaz2wsx3EDC' CREATEDB CREATEROLE;

# 授予权限
GRANT ALL PRIVILEGES ON DATABASE school TO cas;

# 退出当前会话
\q

# 以新用户身份连接
gsql -h 192.168.122.1 -p 5432 -U cas -d school


# 重置密码
ALTER USER openGauss WITH PASSWORD '1qaz2wsx3EDC';

# 配置远程连接
vi $HOME/openGauss/data/single_node/postgresql.conf
# 修改如下
listen_addresses = '*'
port = 5432
max_connections = 200
password_encryption_type = 0 # 开启远程连接必须设置为0

# 用户解锁
ALTER USER cas ACCOUNT UNLOCK;
ALTER USER cas WITH PASSWORD '11223344';

# 关闭防火墙
sudo systemctl stop firewalld
sudo systemctl disable firewalld

## 外部访问更改配置
### 1、更改ph_hbg.conf
    # "local" is for Unix domain socket connections only
    local   all             all                                     trust
    # IPv4 local connections:
    host    all             all            0.0.0.0/0                sha256
    # IPv6 local connections:
    host    all             all             ::/0                 sha256

### 2、更改postgresql.conf
    listen_addresses = '*' 