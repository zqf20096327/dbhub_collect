# tikv-test

This allows easy testing of tikv configuration.

```
# 1. Run kind cluster 6 worker nodes
# 2. install tikv operator 
# 3. install tikv-cluster from tikv-cluster.yaml
# 4. Deploy load generator, deployment can be scaled for more load

$ make all

```

