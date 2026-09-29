# tidb-mad-k8s

### deploy tidb-monitor
``` yaml
# external-configMap
kubectl apply -f external-configMap.yaml -n tidb-cluster

# external-rules
kubectl apply -f external-rules.yaml -n tidb-cluster

# tidb-monitor
kubectl apply -f tidb-monitor.yaml -n tidb-cluster
```

### deploy prometheus-anomaly-detector
``` yaml
# deployment
kubectl apply -f k8s-deployment-tidb.yaml -n tidb-cluster

# service
kubectl apply -f k8s-service-tidb.yaml -n tidb-cluster
```