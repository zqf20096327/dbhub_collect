# 修改conf/config.yaml中数据库的地址和端口后重新编译生效
# 编译二进制服务
    CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build .
# 启动服务
    ./thingspanel-TDsql-pg

# build镜像
    docker build -t thingspanel-TDsql-pg:1.0.0 . 
    注意：如果需要修改配置文件内容，请修改后重新build镜像，配置文件中的数据库地址请填写能访问的地址
# 启动镜像
    docker run -it --name td -p 50052:50052 thingspanel-TDsql-pg:1.0.0


