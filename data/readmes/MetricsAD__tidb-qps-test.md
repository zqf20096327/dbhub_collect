### Tidb 测试

```bash
# 打包镜像
docker build -t 409951699/tidb-test:1.0.0 .

# 推送到Docker hub
docker push 409951699/tidb-test:1.0.0
 
# 集群创建Cronjob
kubectl apply -f cronjob.yml


```