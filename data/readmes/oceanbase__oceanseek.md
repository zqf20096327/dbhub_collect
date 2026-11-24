<p align="center">
    <a href="https://github.com/oceanbase/oceanseek">
        <img alt="OceanBase Logo" src="images/logo.svg" width="50%" />
    </a>
</p>

<p align="center">
    <a href="https://www.oceanbase.com/docs/oceanseek">
        <img alt="Chinese doc" src="https://img.shields.io/badge/文档-简体中文-blue" />
    </a>
    <a href="https://en.oceanbase.com/docs/oceanseek">
        <img alt="English doc" src="https://img.shields.io/badge/docs-English-blue" />
    </a>
    <a href="https://github.com/oceanbase/oceanseek/commits/master">
        <img alt="last commit" src="https://img.shields.io/github/last-commit/oceanbase/oceanseek/master" />
    </a>
    <a href="https://github.com/oceanbase/oceanseek">
        <img alt="stars" src="https://img.shields.io/badge/dynamic/json?color=blue&label=stars&query=stargazers_count&url=https%3A%2F%2Fapi.github.com%2Frepos%2Foceanbase%2Foceanseek" />
    </a>
    <a href="https://github.com/oceanbase/oceanseek/blob/master/LICENSE">
        <img alt="license" src="https://img.shields.io/badge/license-Apache--2.0-blue" />
    </a>
</p>

<p align="center">
    <a href="https://discord.gg/74cF8vbNEs">
        <img alt="Support" src="https://img.shields.io/badge/Discord-Join%20Oceanbase-brightgreen?logo=discord" />
    </a>
    <a href="https://stackoverflow.com/questions/tagged/oceanbase">
        <img alt="Stack Overflow" src="https://img.shields.io/badge/Stack-Stack%20Overflow-brightgreen?logo=stackoverflow" />
    </a>
</p>

English | [中文版](README_CN.md) | [日本語版](README_JA.md)

**OceanSeek** is the open-source distribution of the OceanBase AI database.

OceanSeek is a next-generation distributed database with multi-modal convergence and integrated lake-repository architecture, separating storage and computation. Built on OceanBase's large-scale, production-proven distributed platform, it caters to AI applications, agent data management, multimodal data processing, RAG/semantic search, and lake repository analysis. It unifies various data models, including relational, wide table, vector, JSON, text, and spatial models, under a single set of transaction, permission, version, and lifecycle mechanisms.

Architecturally, OceanSeek decouples the traditional database's computation, logging, and storage capabilities into three independently evolving layers. Each layer has clear responsibilities and can be extended independently, collectively providing high-performance, highly available, low-cost, and elastically scalable database services. The key benefits of this architecture are: the compute layer can be deployed with a single replica, while data persistence is independently guaranteed by three Paxos replicas of the LogService, achieving high availability with RPO=0, while maintaining the linear scalability of the compute layer—eliminating the need to incur the cost of multiple replicas at the compute layer for reliability.

# Key Features

- **Multi-Model Integration**: Natively supports relational tables, wide tables, vectors, JSON documents, text, spatial data, arrays/mappings, and other data types. A single table can simultaneously contain structured columns, JSON columns, vector columns, and text columns, and queries can cross data types. Each type has a matching index acceleration path: secondary index, vector index (HNSW/IVF), JSON index, multi-value index, full-text index (BM25), GIS index, and search index.

- **Hybrid Search**: Vector + Full-text + Scalar search, unstructured + semi-structured + structured data; a single SQL statement completes multi-path retrieval; built-in fusion ranking algorithms such as RRF, MINMAX_NORMALIZER, and WEIGHT_SUM.

- **Native Agent**: Provides five layers of isolation: tenant-level, database-level, namespace-level, table-level, and row/column-level, supporting data isolation for millions/tens of millions of agents; supports single SQL statement for memory-based retrieval; Fork Table/Database uses Copy-on-Write to achieve second-level data sandboxing, sharing baseline data, isolating incremental changes, and discarding failed attempts without polluting production data.

- **RAG Pipeline in DB**: Document parsing, document segmentation, text vectorization, index building, hybrid search, fusion ranking, and model inference are all completed within the library. AI functions are provided, supporting AI operators extended via Python UDFs. Documents are added to the database, and answers are retrieved without transferring data between multiple systems.

- **Real-time Data Warehouse:** Enables integrated stream and batch processing, supporting both high-frequency real-time writes and large-volume batch imports; supports incremental/full refresh materialized views; flexible definition of row-based, column-based, and mixed row-column storage; vectorized execution engine and native MPP execute in parallel.

- **Lake-Warehouse-Repository Integration:** Based on the same data, metadata, and SQL semantics, it simultaneously meets the low cost of a lake, the analytical capabilities of a warehouse, and the transactional requirements of a repository. Supports Iceberg/Hive/Paimon integration, Parquet/ORC/CSV adaptation, and synchronizes database table information to HMS via CatalogSync for unified metadata management.

- **Storage-Compute Separation:** Compute, logs, and storage are deployed and scaled independently; compute nodes are stateless, allowing for elastic scaling without data migration; hot data is cached on local SSDs, while cold data is stored in object storage, with the system automatically identifying access frequency and migrating accordingly.

- **Low Cost:** Maintaining data compression capabilities equivalent to OceanBase, compute nodes support single-replica deployment to reduce computational costs; shared data storage in object storage reduces storage costs.

- **MySQL/KV Compatibility:** Supports both MySQL and KV modes (OBKV-Table, OBKV-HBase), utilizing the ODP and MySQL ecosystem drivers, as well as toolchains such as OCP, ODC, and OMS.

- **Open Ecosystem:** Supports S3 protocol object storage, Iceberg/Paimon open table formats, and a unified catalog, reducing data replication, format conversion, and system locking.

For more information, please refer to [OceanBase AI Product](https://www.oceanbase.com/product/ai-database)

# Quick Start

For more information, please refer to [Quick Start Guide to OceanSeek](https://open.oceanbase.com/oceanseek-quickstart).

**Prerequisites**: OceanSeek uses object storage as the persistent foundation for all data. Before deployment, you need to prepare an object storage system that is **S3 protocol compatible**, and create **data buckets** and **log buckets** (heterogeneous media are acceptable, and they can be configured independently). The object storage system must meet four requirements: S3 compatibility, high availability, access credential rotation, and adjustable bandwidth.

## 🐳 Start with docker

The OceanSeek instance can be launched with a single click in a Docker Compose environment using the [docker image](https://github.com/oceanbase/docker-images/tree/main/oceanseek). For detailed usage instructions, please refer to the documentation [docker quick start](https://open.oceanbase.com/oceanseek-quickstart).

## ☸️ Start with Kubernetes

You can use [ob-operator](https://github.com/oceanbase/ob-operator) to quickly deploy and manage OceanSeek instances in a Kubernetes environment. For specific usage instructions, please refer to the documentation [ob-operator quick start](https://open.oceanbase.com/oceanseek-quickstart).

# Case study

OceanBase serves over 2,000 clients across various industries, including financial services, telecommunications, retail, and internet. OceanSeek shares the same distributed infrastructure as OceanBase.

For more detailed information, please refer to [Customer Cases](https://www.oceanbase.com/customer).

# System architecture

[System Architecture Introduction](https://docs.oceanbase.com/oceanbase-ai-database/system-architecture)

# Contributing

Community contributions are highly welcome. For development, compilation, and local execution instructions, please refer to the [Development and Build Guide](docs/docs/en/build-and-run.md). Before submitting an Issue or PR, it is recommended to read the code style guide and submission conventions.

# License

OceanSeek is licensed under the Apache License, Version 2.0. See the [LICENSE](LICENSE) file for more info.

# Community

Join the OceanBase community via:

* [Discord](https://discord.gg/74cF8vbNEs): Best for: asking questions, sharing feedback, getting the latest news, and connecting with other OceanBase users.
* [GitHub Issues](https://github.com/oceanbase/oceanseek/issues): Best for: addressing bugs encountered while using OceanBase, as well as submitting feature proposals.
* [Chinese User Forum](https://ask.oceanbase.com/): Only for Chinese users, best for: asking questions, sharing feedback, getting the latest news, and connecting with other OceanBase users.
* WeChat Group (Add the assistant with WeChat ID: OBCE666): Only for Chinese users, best for: getting the latest news and connecting with other OceanBase users.
