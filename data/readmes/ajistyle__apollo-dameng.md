## 本项目基于源项目修改：https://github.com/apolloconfig/apollo
### 使用方式
#### 代码可直接编译运行
#### 编译
```
cd apollo-dameng
./scripts/build.sh
```
#### 运行在docker环境中
```
Dockerfile分别在 apollo-adminservice、apollo-configservice、apollo-portal 的 src/main/docker 目录下
```

#### 运行在k8s环境中
```
yaml文件放在 ./scripts/k8s/目录下
部署步骤见：./scripts/README-K8S-DM-git.md
```
