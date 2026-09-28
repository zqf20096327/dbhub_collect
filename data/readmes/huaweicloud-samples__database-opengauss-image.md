<p align="center">
  <h1 align="center">openGauss Database</h1>
  <p align="center">
    <strong>English</strong> | <a href="README_ZH.md"><strong>简体中文</strong></a>
  </p>

## Table of Contents

- [Repository Introduction](#project-introduction)
- [Prerequisites](#prerequisites)
- [Image Description](#image-description)
- [Get Help](#get-help)
- [How to Contribute](#how-to-contribute)

## Project Introduction
[openGauss](https://gitcode.com/opengauss/openGauss-server) is an open-source relational database management system with enterprise-level features such as multi-core high performance, full-link security, and intelligent operation and maintenance.

### **Core Features:**

**High Performance**

openGauss breaks through the bottleneck of multi-core CPUs, achieving 1.5 million tpmC on two Kunpeng 128-core processors, and the Memory-Optimized Table (MOT) engine reaches 3.5 million tpmC.

**Data Partitioning**

Key data structures shared by internal threads are partitioned to reduce lock access conflicts. For example, CLOG uses partition optimization to resolve the ClogControlLock bottleneck.

**NUMA-Aware Kernel Data Structures**

Key data structures are allocated in a NUMA-aware manner to reduce cross-CPU access. For instance, the global PGPROC array is divided into multiple parts based on the number of NUMA Nodes, with memory allocated on corresponding NUMA Nodes. This resolves the ProcArrayLock bottleneck.

**Core Binding Optimization**

Network interrupts and background business threads are bound to different cores to avoid performance instability caused by thread migration between cores.

**ARM Instruction Optimization**

Optimizations are made using ARM's atomic operation LSE to achieve efficient atomic operations on critical mutex variables.

**SQL BY PASS**

Simplifies CPU execution overhead by optimizing the SQL execution process through SQL BY PASS.

**High Reliability**

In normal business load scenarios, RTO is less than 10 seconds, reducing business unavailability time caused by node failures.

**Parallel Recovery**

When host logs are transmitted to the standby, the standby writes logs to disk while sending them to redo recovery distribution threads. The distribution threads dispatch logs to multiple parallel recovery threads based on log types and data pages operated on, ensuring the standby's redo speed keeps up with the host's log generation speed. This keeps the standby in a ready state, enabling instant failover.

**MOT Engine (Beta Release)**

The Memory-Optimized Table (MOT) storage engine is optimized for multi-core and large-memory environments, offering high OLTP performance and resource utilization. MOT data and indexes are entirely stored in memory, with NUMA-aware execution, latch contention elimination algorithms, and query JIT native compilation, providing low-latency data access and efficient transaction execution. For more details, refer to the [MOT Engine Documentation](https://opengauss.org/en/docs/2.0.0/docs/Developerguide/Memory-Table-Characteristics.html).

**Security**

openGauss supports comprehensive database security capabilities such as account management, authentication, password complexity checks, account locking, permission management and verification, transmission encryption, and operation auditing to ensure business compliance with security requirements.

**Easy Operation and Maintenance**

openGauss integrates AI algorithms to reduce database maintenance burdens.

- **SQL Prediction**

openGauss encodes historical performance data, trains models using deep learning, and supports SQL execution time prediction.

- **SQL Diagnoser**

openGauss supports a SQL statement diagnoser to detect slow queries in advance.

- **Automatic Parameter Tuning**

openGauss automatically adjusts database parameters using machine learning methods, improving tuning efficiency and reducing the cost of correct parameter configuration.

The open-source image product [**openGauss Database**](https://marketplace.huaweicloud.com/intl/hidden/contents/0c9e040c-c78c-4f9f-9dae-5f0ae5650a1c) provided by this project comes pre-installed with openGauss and its related runtime environment, along with deployment templates. Follow the user guide to enjoy an efficient "out-of-the-box" experience!

> **System Requirements:**
> - CPU: 2GHz or higher
> - RAM: 4GB or larger
> - Disk: At least 40GB

## Prerequisites
[Register a Huawei account and activate Huawei Cloud](https://support.huaweicloud.com/usermanual-account/account_id_001.html)

## Image Description

| Image Specification                                                                                            | Feature Description                                      | Notes |
|-------------------------------------------------------------------------------------------------------------|----------------------------------------------------------|-------|
| [opengauss-7.0.0-RC1-kunpeng](https://github.com/HuaweiCloudDeveloper/opengauss-image/tree/opengauss-7.0.0-RC1-kunpeng) | Installed and deployed based on Kunpeng server + Huawei Cloud EulerOS 2.0 64bit |       |

## Get Help
- For more questions, contact us via [issues](https://github.com/HuaweiCloudDeveloper/opengauss-image/issues) or the service support of the specified product in the Huawei Cloud Marketplace.
- Other open-source images can be found in [open-source-image-repos](https://github.com/HuaweiCloudDeveloper/open-source-image-repos)

## How to Contribute
- Fork this repository and submit a pull request
- Synchronously update README.md based on your open-source image information
