# TiDB Row Inserter
Simple python script that inserts rows into TiDB. Useful for benchmarking TiDB's CDC performance

It has 2 write modes
1. SINGLE which writes once and exits
2. CONTINOUS which writes as long as the process lives

Comes with [Dockerfile](./Dockerfile) and 2 manifests
1. [K8s CronJob Manifest](./k8s/CronJob.yaml) suited for the SINGLE write mode
2. [K8s Deployment Manifest](./k8s/Deployment.yaml) suited for the DEPLOYMENT write mode
