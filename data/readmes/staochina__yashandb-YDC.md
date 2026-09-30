# yashandb-YDC

将 YashanDB YDC（`ydc-server`）打包为多架构 Docker 镜像，便于在 Linux amd64 / arm64 环境下一键部署与启动开发者控制台服务。

项目地址：https://github.com/staochina/yashandb-YDC
原始资源包下载 https://yashandb.com/download
原始资源产品说明文档 https://doc.yashandb.com/ydc/23.4/zh/Release-Note/Release-Notes.html

镜像：`staochina/yashandb-ydc:${TAG}`  
基础镜像：`ubuntu:26.04`  
默认端口：`9328`  
支持架构：`linux/amd64`、`linux/arm64`

## 构建并推送

多架构构建并推送到 Docker Hub：

```bash
docker buildx build --platform linux/amd64,linux/arm64 \
  -t staochina/yashandb-ydc:${TAG} --push .
```

仅构建当前主机架构：

```bash
docker build -t staochina/yashandb-ydc:${TAG} .
```

## 拉取并运行

```bash
docker pull staochina/yashandb-ydc:${TAG}
docker run -d --name yashandb -p 9328:9328 staochina/yashandb-ydc:${TAG}
```
