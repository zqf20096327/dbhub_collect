
-- build and run 
mvn clean install -DskipTests
sudo docker-compose build
sudo docker-compose up

-- 问题
TiDB 官方镜像当前不支持 docker-compose 传递环境变量：environment，所以样例使用default value




-- 外部部署方式参考
-- install tidb
sudo docker pull pingcap/tidb
mkdir -p /home/pi314/run/tidb/data
sudo docker run --name tidb-server -d -v /home/pi314/run/tidb/data:/tmp/tidb -p 4000:4000 -p 10080:10080 pingcap/tidb:latest

-- test
curl http://localhost:10080/status

mysql -h 127.0.0.1 -P 4000 -u root -D test --prompt="tidb> "


-- create db
CREATE DATABASE demo CHARACTER SET utf8 COLLATE utf8_general_ci;
CREATE USER 'demo'@'%' IDENTIFIED BY 'demo';
GRANT ALL PRIVILEGES ON demo.* TO 'demo'@'%';
FLUSH PRIVILEGES;

use demo;
create table users(`name` varchar(100), `age` bigint(20));

go get github.com/go-sql-driver/mysql
       


 --client-urls="http://0.0.0.0:2379" \
 --advertise-client-urls="http://192.168.1.101:2379" \