# Table of Contents

- [About the TiDB](#about-the-TiDB)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Authors](#authors)

## About the TiDB
Here’s a concise **About TiDB** section for your GitHub README:

TiDB is an **open-source, distributed SQL database** designed for **Hybrid Transactional and Analytical Processing (HTAP)** workloads. It is **MySQL-compatible**, offering **horizontal scalability**, **high availability**, and **strong consistency**.  

#### **Key Features:**  
- **Scalability** – Seamlessly scales out storage and compute resources.  
- **HTAP Support** – Combines **TiKV** (row-based) and **TiFlash** (columnar) storage engines.  
- **Cloud-Native** – Optimized for Kubernetes and cloud environments.  
- **High Availability** – Uses **Raft consensus** for fault tolerance.  
- **MySQL Compatibility** – Supports MySQL syntax and ecosystem tools.  

TiDB is ideal for **large-scale applications**, **real-time analytics**, and **cloud-native deployments**.  

For more details, visit the [TiDB documentation](https://docs.pingcap.com/tidb/stable/overview/) or [Wikipedia](https://en.wikipedia.org/wiki/TiDB). 🚀  

## Getting Started
This guide provides instructions for deploying **TiDB on AWS EKS** with a **multi-AZ worker node setup** consisting of 3 wokers. TLS is **enabled by default** and managed using **cert-manager**, ensuring secure communication across the cluster.

### Prerequisites
- An existing **AWS EKS cluster** with multi-AZ worker nodes.  
- Helm installed for managing Kubernetes resources.  
- Cert-manager deployed for automatic TLS certificate management.  

### Installation
1. Install cert-manager
    ```
    $ helm repo add jetstack https://charts.jetstack.io
    $ helm repo update

    $ helm install cert-manager jetstack/cert-manager \
        --namespace cert-manager \
        --create-namespace \
        --set installCRDs=true
    ```
2. Install TiDB Operator
    ```
    $ helm repo add pingcap https://charts.pingcap.org/
    $ helm repo update

    $ kubectl create namespace tidb-admin

    $ helm install tidb-operator pingcap/tidb-operator \
      --namespace tidb-admin \
      --set operatorImage=pingcap/tidb-operator:v1.6.1 \
      --set controllerManager.replicaCount=1 \
      --set scheduler.create=true \
      --set webhook.create=true \
      --set admissionWebhook.create=true
    ```
3. Install TiDB CRDs.
    ```
    $ kubectl apply -f crd.yaml
    ```
4. Install the Certificates.
    ```
    $ kubectl create ns tidb-cluster

    $ kubectl apply -f tidb-cluster-issure.yaml -n tidb-cluster
    $ kubectl apply -f cluster-client-secret.yaml -n tidb-cluster
    $ kubectl apply -f pd-cluster-secret.yaml-n tidb-cluster
    $ kubectl apply -f tidb-client-cert.yaml -n tidb-cluster
    $ kubectl apply -f tidb-cluster-secret.yaml -n tidb-cluster
    $ kubectl apply -f tidb-server-secret.yaml -n tidb-cluster
    $ kubectl apply -f tiflash-cluster-secret.yaml -n tidb-cluster
    $ kubectl apply -f tikv-cluster-secret.yaml -n tidb-cluster
    ```
5. Install the TiDB cluster
    ```
    $ kubectl apply -f mycluster-tls.yaml -n tidb-cluster
    ```
6. Verify the Installation
    ```
    kubectl  get pods -n tidb-cluster

    NAME                             READY   STATUS    RESTARTS   AGE
    tidb-discovery-74bddf459-l2m55   1/1     Running   0          43h
    tidb-pd-0                        1/1     Running   0          43h
    tidb-pd-1                        1/1     Running   0          43h
    tidb-pd-2                        1/1     Running   0          43h
    tidb-tidb-0                      2/2     Running   0          43h
    tidb-tidb-1                      2/2     Running   0          43h
    tidb-tidb-2                      2/2     Running   0          43h
    tidb-tiflash-0                   4/4     Running   0          43h
    tidb-tikv-0                      1/1     Running   0          43h
    tidb-tikv-1                      1/1     Running   0          43h
    tidb-tikv-2                      1/1     Running   0          43h
    ```
## Authors
- Hossein Tabatabaei
