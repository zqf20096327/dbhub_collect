# tidb-px
Running tidb backed by Portworx volumes

## Installing portworx
Refer to https://docs.portworx.com/portworx-install-with-kubernetes/

For this doc, Portworx was installed on AKS using: https://docs.portworx.com/portworx-install-with-kubernetes/cloud/azure/aks/


## Installing tidb

### Install helm
```
curl https://raw.githubusercontent.com/kubernetes/helm/master/scripts/get | bash
kubectl apply -f https://raw.githubusercontent.com/pingcap/tidb-operator/master/manifests/tiller-rbac.yaml && helm init --service-account=tiller --upgrade
helm list
```

Verify:
```
kubectl get po -n kube-system -l name=tiller
```

Initialize pingcap helm repo:
```
helm init --upgrade
helm repo add pingcap https://charts.pingcap.org/
helm search pingcap -l
```


### Install TiDB Operator
Create the crd:
```
wget https://raw.githubusercontent.com/pingcap/tidb-operator/master/manifests/crd.yaml
kubectl apply -f crd.yaml
kubectl get crd tidbclusters.pingcap.com
```

Deploy the operator:
```
mkdir tidb-operator
cd tidb-operator/
helm inspect values pingcap/tidb-operator --version=v1.0.6  > values-tidb-operator.yaml
helm install pingcap/tidb-operator --name=tidb-operator --namespace=tidb-admin --version=v1.0.6 -f values-tidb-operator.yaml
kubectl -n tidb-admin get pods
```


### Create Portworx StorageClasses
Create the storageClass below:
```
kind: StorageClass
apiVersion: storage.k8s.io/v1beta1
metadata:
 name: px-db
provisioner: kubernetes.io/portworx-volume
allowVolumeExpansion: true
parameters:
 repl: "3"
 priority_io: "high"
 io_profile: "db"
```

### Deploy the cluster
```
kubectl create ns tidb-cluster
kubectl create secret generic tidb-secret --from-literal=root=password  --namespace=tidb-cluster
helm inspect values pingcap/tidb-cluster --version=v1.0.6 > values-tidb-cluster.yaml
sed -i 's/local-storage/px-db/g' values-tidb-cluster.yaml

helm install pingcap/tidb-cluster --name=tidb-cluster --namespace=tidb-cluster --version=v1.0.6 -f values-tidb-cluster.yaml
```

Verify:
```
# kubectl get pods -n tidb-cluster
NAME                                      READY   STATUS    RESTARTS   AGE
tidb-cluster-discovery-7c954cf9b5-rq749   1/1     Running   0          39s
tidb-cluster-monitor-78f88b7568-fmj2z     3/3     Running   0          39s
tidb-cluster-pd-0                         1/1     Running   0          39s
tidb-cluster-pd-1                         1/1     Running   0          39s
tidb-cluster-pd-2                         1/1     Running   0          39s

# kubectl get pvc -A
NAMESPACE      NAME                   STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
tidb-cluster   pd-tidb-cluster-pd-0   Bound    pvc-b05fe801-4c70-11ea-bb94-000c297fd2ae   1Gi        RWO            px-db          30s
tidb-cluster   pd-tidb-cluster-pd-1   Bound    pvc-b0630d3e-4c70-11ea-bb94-000c297fd2ae   1Gi        RWO            px-db          30s
tidb-cluster   pd-tidb-cluster-pd-2   Bound    pvc-b0646e21-4c70-11ea-bb94-000c297fd2ae   1Gi        RWO            px-db          30s
```

## Load test tidb

### Launch sysbench client
```
kubectl run -it --rm sysbench-client --image=perconalab/sysbench:latest --restart=Never -- bash
```

### Initialization
```
sysbench \
  --mysql-host=tidb-cluster-tidb.tidb-cluster \
  --mysql-port=4000 \
  --mysql-user=root \
  --mysql-password=password \
  --mysql-db=sbtest \
  --time=600 \
  --threads=16 \
  --report-interval=10 \
  --db-driver=mysql \
  --rand-type=uniform \
  --rand-seed=$RANDOM \
  --tables=16 \
  --table-size=10000000 \
  oltp_common \
  prepare
  ```

### Warm up
```
sysbench \
  --mysql-host=tidb-cluster-tidb.tidb-cluster \
  --mysql-port=4000 \
  --mysql-user=root \
  --mysql-password=password \
  --mysql-db=sbtest \
  --time=600 \
  --threads=16 \
  --report-interval=10 \
  --db-driver=mysql \
  --rand-type=uniform \
  --rand-seed=$RANDOM \
  --tables=16 \
  --table-size=10000000 \
  oltp_common \
  prewarm
```

### Pressure test
```
sysbench \
  --mysql-host=tidb-cluster-tidb.tidb-cluster \
  --mysql-port=4000 \
  --mysql-user=root \
  --mysql-password=password \
  --mysql-db=sbtest \
  --time=600 \
  --threads=<threads> \
  --report-interval=10 \
  --db-driver=mysql \
  --rand-type=uniform \
  --rand-seed=$RANDOM \
  --tables=16 \
  --table-size=10000000 \
  <test> \
  run
```
*NOTE:* <test> is the test case of sysbench. In this test, `oltp_point_select`, `oltp_update_index`, `oltp_update_no_index`, and `oltp_read_write` are chosen as <test>.
