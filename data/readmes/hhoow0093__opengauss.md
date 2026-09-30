# Opengauss overview

database forms are compromised into `digital data` and `analog data`. Monitor dan controlling database (DBMS).

## DBMS function
1. database definition
2. data manipulation
3. database opration management
4. interface and tools for convenient and effective database access
5. database creation and maintenance

[![Screenshot-2025-09-06-183735.png](https://i.postimg.cc/sf8cf1hT/Screenshot-2025-09-06-183735.png)](https://postimg.cc/F1ycDrGS)

[![Screenshot-2025-09-06-184129.png](https://i.postimg.cc/hG6LD5Jf/Screenshot-2025-09-06-184129.png)](https://postimg.cc/XZKGxxkb)

# Database installation and deployment
Open gauss is a relational database that uses client server single process multi thread architecture that supports standalone and one primary multi standby deployment.

> prerequisites : make sure openEuler 22.03 is installed in virtual box

## Steps to download opengauss
1. Update openEuler Package

```bash
sudo yum update -y
```

2. install necessary dependencies
```bash
sudo yum install -y wget tar bzip2 net-tools

sudo dnf update -y
sudo dnf remove NetworkManager -y
sudo dnf install NetworkManager -y
sudo dnf update -y

sudo dnf install -y gcc gcc-c++ make cmake bison flex \
readline readline-devel zlib zlib-devel \
libaio libaio-devel perl openldap-devel

sudo dnf install -y readline-devel libaio-devel
ldconfig -p | grep readline
ldconfig -p | grep aio

```

3. create dedicated user
```bash
sudo useradd omm
sudo passwd omm
sudo chown -R omm:omm /home/omm
```

4. login as user
```bash
su - omm
```

5. install the package
```bash
wget https://opengauss.obs.cn-south-1.myhuaweicloud.com/3.0.6/x86_openEuler/openGauss-3.0.6-openEuler-64bit.tar.bz2
tar -xvf openGauss-3.0.6-openEuler-64bit.tar.bz2
cd openGauss-3.0.6/simpleInstall
```

6. install openGauss
```bash
chmod +x install.sh
./install.sh -w Mypassword123
```

7. start database
```bash
gs_ctl start -D ~/data/single_node
```

8. stop database
```bash
gs_ctl stop -D ~/data/single_node -m fast
```

9. status database
```bash
gs_ctl status -D ~/data/single_node
```

10. connect gaussDB
```bash
gsql -d postgres -p 5432 -r
```

## usedul command in gaussDB

```sql
\l               -- list databases
\c demo          -- connect to demo DB
\dt              -- list tables
\q               -- quit gsql
\d tablename     -- describe table structure
\! clear         -- clear console in gsql
```




