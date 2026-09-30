## 达梦数据库容器化

### 注意事项

- 为避免文件权限冲突，宿主机与容器内运行数据库的用户 UID/GID 必须保持一致。部署前，请在宿主机上创建用户及目录，并赋予正确的权限

### 准备素材

```sh
dm-docker/
├── Dockerfile              # 镜像构建模板
├── docker-compose.yml      # 部署模板（新增）
├── .dockerignore           # 构建忽略规则（新增）
├── Makefile                # 构建辅助
├── entrypoint.sh           # 容器启动脚本
├── generate_soft_xml.sh    # 静默安装配置生成
├── DMInstall.bin           # 达梦安装包（需自行放置）
├── dm.key                  # 授权文件（可选）
└── readme.md               # 说明文档
```

### 构建镜像

```sh
# 构建镜像（注意最后的 . 表示当前目录）
docker build -t dm8:mini .

# 查看构建结果
docker images | grep dm8

# 1. 查看镜像信息
docker inspect dm8:mini

# 2. 测试运行
docker run --rm dm8:mini /dmdbms/bin/dmserver --help

# 3. 查看环境变量
docker run --rm dm8:mini env | grep -E "DM_HOME|PATH|LD_LIBRARY_PATH"
```

### 宿主机配置

```sh
# 创建数据与归档目录
mkdir -p /dmdb/dm{data,arch,slog}

# 创建安装用户组（gid=1001）
groupadd -g 53321 -r dinstall

# 创建安装用户 dmdba（uid=1001），并指定默认目录
useradd -u 53321 -r -g dinstall -m -d /home/dmdba -s /bin/bash dmdba

# 授权目录访问权限
chown -R dmdba:dinstall  /dmdb
```

### 运行容器

```sh
docker run -d --name dm8 \
    --restart always \
    -u dmdba \
    --memory=8g \
    --cpus=4 \
    -p 5237:5236 \
    -e SYSDBA_PWD=SyspwDBA_137 \
    -e SYSAUDITOR_PWD=SyspwDBA_137 \
    -e EXTENT_SIZE=32 \
    -e PAGE_SIZE=16 \
    -e CHARSET=0 \
    -e CASE_SENSITIVE=1 \
    -e BLANK_PAD_MODE=0 \
    -e ARCH_FLAG=1 \
    -e ARCH_SPACE_LIMIT=10240 \
    -v /data/dmdb/dmdata:/dmdata \
    -v /data/dmdb/dmarch:/dmarch \
    -v /data/dmdb/dmslog:/dmslog \
    -v /host/dm.key:/dmdbms/bin/dm.key:ro \
    dm8:mini
    
    

```

#### 检查

```sh
# 查看日志
docker logs -f dm8

# 连接测试
docker exec -it dm8 /dmdbms/bin/disql SYSDBA/SyspwDBA_137@127.0.0.1:5236
docker exec -it dm8 /dmdbms/bin/disql SYSDBA/SyspwDBA_137@localhost:5236

# 查看容器状态
docker ps | grep dm8
docker exec dm8 ps aux | grep dmserver

# 健康检查
docker inspect dm8 --format='{{.State.Health.Status}}'

# 镜像信息
docker images dm8:mini --format '{{.Repository}}:{{.Tag}} {{.Size}}'
docker history dm8:mini --no-trunc --format 'table {{.Size}}\t{{.CreatedBy}}'
```



### 约束和制约因素

- 数据库实例名必须使用DMDB，禁止使用DAMENG
- 禁止启动和配置dmap 服务



## 附录

### 参考文档

- <https://eco.dameng.com/community/article/4c012830c0f24a04809f2be20a896323>
- <https://github.com/MacroSAN-Tech/sys-docker-image>

