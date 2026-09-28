<p align="center">
  <h1 align="center">TiDB distributed NewSQL database</h1>
  <p align="center">
    <a href="README.md"><strong>English</strong></a> | <strong>简体中文</strong>
  </p>
</p>

## Table of Contents

- [Repository Introduction](#repository-introduction)
- [Prerequisites](#prerequisites)
- [Image Specifications](#image-specifications)
- [Getting Help](#getting-help)
- [How to Contribute](#how-to-contribute)

## Repository Introduction
‌[TiDB‌](https://github.com/pingcap/tidb) TiDB is an open-source distributed NewSQL database developed by PingCAP and has become a graduate project of Cloud Native Computing Foundation (CNCF) (the same level as Kubernetes and Prometheus). It combines the usability of traditional relational databases (such as MySQL) and the scalability of NoSQL databases. It is suitable for online transaction processing (OLTP) and online analytical processing (OLAP) scenarios with high concurrency and massive data.

**Core Features:**
1. Distributed architecture: TiDB uses a distributed architecture that separates computing and storage. The computing layer (TiDB Server) is responsible for SQL parsing and execution, the storage layer (TiKV) implements data HA based on the Raft protocol, and the scheduling layer (PD) is responsible for global metadata management and load balancing. Supports horizontal expansion to process PB-level data and millions of QPS.
2. High compatibility with MySQL: Compatible with MySQL 5.7 protocols and common syntax (such as JOIN, transaction, and window functions), mainstream ORM frameworks, and MySQL ecosystem tools (such as mysqldump and Navicat). Applications can be migrated without reconstruction, reducing service switchover costs.
3. Elastic horizontal expansion: TiKV or TiDB nodes are dynamically added to implement linear expansion of storage or computing capabilities. The expansion process is transparent to services. Automatic sharding (region) and load balancing are supported to avoid hotspot issues and are applicable to fast-growing service scenarios.
4. Strong consistency transactions: Implement distributed ACID transactions based on the Percolator model, support optimistic lock and pessimistic lock modes, and provide snapshot isolation (SI) and read committed (RC) isolation levels. Two-phase commit (2PC) ensures cross-node transaction consistency.
5. Real-time HTAP capability: The row-column hybrid storage engine TiFlash is used to implement real-time analysis and processing (OLAP). The TiKV (row-store) and TiFlash (column-store) collaborative computing is supported. The same data serves both TP (transaction processing) and AP (analysis) scenarios. Avoid ETL delays.
6. High availability and automatic recovery: Data is stored in multiple copies (three copies by default) by region. Automatic failover is implemented based on the Raft protocol. The failure of a single node does not affect data availability. The PD supports leader election, preventing single points of failure (SPOFs) of cluster management components.
7. Cloud native design: Supports Kubernetes deployment (TiDB Operator) and provides automatic O&M capabilities (scaling, upgrade, and backup). The storage layer supports local SSDs or cloud disks and is deeply integrated with cloud platforms such as AWS and GCP, which is suitable for hybrid cloud scenarios.
8. Enterprise-level monitoring and diagnosis: The built-in Prometheus+Grafana monitoring system provides visualized cluster health and performance indicators (such as latency and QPS). The TiDB Dashboard is integrated to support SQL performance analysis, slow query diagnosis, and real-time topology viewing.
9. Multi-tenant and resource isolation: The Resource Control feature is used to isolate CPU and I/O resources. Resource quotas (RUs) can be allocated by service to avoid resource contention in multi-tenant scenarios.
10. Open ecosystem and open source: Fully open-source (Apache 2.0), compatible with MySQL ecosystem tools (such as Binlog synchronization and CDC), supports integration with big data systems such as Spark and Flink, and provides data migration tool chains such as TiDB Data Migration (DM).

This project offers pre-configured [**`TiDB-Distributed NewSQL database`**](https://marketplace.huaweicloud.com/intl/hidden/contents/5fd701f5-4063-4045-a2c5-e6e5b15a2c25)，images with TiDB and its runtime environment pre-installed, along with deployment templates. Follow the guide to enjoy an "out-of-the-box" experience.

**Architecture Design:**

![](./images/img.png)

> **System Requirements:**
> - CPU: 4vCPUs or higher
> - RAM: 16GB or more
> - Disk: At least 50GB

## Prerequisites
[Register a Huawei account and activate Huawei Cloud](https://support.huaweicloud.com/usermanual-account/account_id_001.html)

## Image Specifications

| Image Version          | Description | Notes |
|------------------------| --- | --- |
| [TiDB8.5.1-arm-v1.0](https://github.com/HuaweiCloudDeveloper/tidb-image/tree/TiDB8.5.1-arm-v1.0?tab=readme-ov-file) | Deployed on Kunpeng servers with Huawei Cloud EulerOS 2.0 64bit |  |

## Getting Help
- Submit an [issue](https://github.com/HuaweiCloudDeveloper/tidb-image/issues)
- Contact Huawei Cloud Marketplace product support

## How to Contribute
- Fork this repository and submit a merge request.
- Update README.md synchronously based on your open-source mirror information.