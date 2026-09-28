# Awesome Big Data

[![Awesome](https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg)](https://github.com/sindresorhus/awesome)

A curated list of awesome big data frameworks, resources and other awesomeness. Inspired by <b><code>&nbsp;32706⭐</code></b> <b><code>&nbsp;&nbsp;5140🍴</code></b> [awesome-php](https://github.com/ziadoz/awesome-php)), <b><code>322629⭐</code></b> <b><code>&nbsp;28793🍴</code></b> [awesome-python](https://github.com/vinta/awesome-python)), <b><code>&nbsp;&nbsp;1265⭐</code></b> <b><code>&nbsp;&nbsp;&nbsp;174🍴</code></b> [awesome-ruby](https://github.com/Sdogruyol/awesome-ruby)), [hadoopecosystemtable](http://hadoopecosystemtable.github.io/) & [big-data](http://usefulstuff.io/big-data/).

Your contributions are always welcome!

- [Awesome Big Data](#awesome-big-data)
  - [RDBMS](#rdbms)
  - [Frameworks](#frameworks)
  - [Distributed Programming](#distributed-programming)
  - [Distributed Filesystem](#distributed-filesystem)
  - [Distributed Index](#distributed-index)
  - [Document Data Model](#document-data-model)
  - [Key Map Data Model](#key-map-data-model)
  - [Key-value Data Model](#key-value-data-model)
  - [Graph Data Model](#graph-data-model)
  - [Columnar Databases](#columnar-databases)
  - [NewSQL Databases](#newsql-databases)
  - [Time-Series Databases](#time-series-databases)
  - [Lakehouse Table Formats](#lakehouse-table-formats)
  - [SQL-like processing](#sql-like-processing)
  - [Vector Databases](#vector-databases)
  - [Data Ingestion](#data-ingestion)
  - [Data Quality and Observability](#data-quality-and-observability)
  - [Service Programming](#service-programming)
  - [Scheduling](#scheduling)
  - [Machine Learning](#machine-learning)
  - [Benchmarking](#benchmarking)
  - [Security](#security)
  - [System Deployment](#system-deployment)
  - [Applications](#applications)
  - [Search engine and framework](#search-engine-and-framework)
  - [MySQL forks and evolutions](#mysql-forks-and-evolutions)
  - [PostgreSQL forks and evolutions](#postgresql-forks-and-evolutions)
  - [Memcached forks and evolutions](#memcached-forks-and-evolutions)
  - [Embedded Databases](#embedded-databases)
  - [Business Intelligence](#business-intelligence)
  - [Data Visualization](#data-visualization)
  - [Internet of things and sensor data](#internet-of-things-and-sensor-data)
  - [Interesting Readings](#interesting-readings)
  - [Interesting Papers](#interesting-papers)
    - [2015 - 2016](#2015---2016)
    - [2013 - 2014](#2013---2014)
    - [2011 - 2012](#2011---2012)
    - [2001 - 2010](#2001---2010)
  - [Videos](#videos)
  - [Books](#books)
      - [Streaming](#streaming)
      - [Distributed systems](#distributed-systems)
      - [Graph Based approach](#graph-based-approach)
    - [Data Visualization](#data-visualization-1)
- [Other Awesome Lists](#other-awesome-lists)

## RDBMS
* 🌎 [MySQL](www.mysql.com/) The world's most popular open source database.
* 🌎 [PostgreSQL](www.postgresql.org/) The world's most advanced open source database.
* [Oracle Database](http://www.oracle.com/us/corporate/features/database-12c/index.html) - object-relational database management system.
* [Teradata](http://www.teradata.com/products-and-services/teradata-database/) - high-performance MPP data warehouse platform.

## Frameworks

* <b><code>&nbsp;&nbsp;1027⭐</code></b> <b><code>&nbsp;&nbsp;&nbsp;136🍴</code></b> [Bistro](https://github.com/facebook/bistro)) - general-purpose data processing engine for both batch and stream analytics. It is based on a novel data model, which represents data via *functions* and processes data via *column operations* as opposed to having only set operations in conventional approaches like MapReduce or SQL.
* 🌎 [IBM Streams](www.ibm.com/analytics/us/en/technology/stream-computing/) - platform for distributed processing and real-time analytics.  Integrates with many of the popular technologies in the Big Data ecosystem (Kafka, HDFS, Spark, etc.)
* [Ap

[...截断...]

ache Hadoop](http://hadoop.apache.org/) - framework for distributed processing. Integrates MapReduce (parallel processing), YARN (job scheduling) and HDFS (distributed file system).
* <b><code>&nbsp;&nbsp;&nbsp;284⭐</code></b> <b><code>&nbsp;&nbsp;&nbsp;&nbsp;33🍴</code></b> [Tigon](https://github.com/caskdata/tigon)) - High Throughput Real-time Stream Processing Framework.
* <b><code>&nbsp;&nbsp;2830⭐</code></b> <b><code>&nbsp;&nbsp;&nbsp;179🍴</code></b> [Numaflow](https://github.com/numaproj/numaflow)) - Kubernetes-native stream processing platform.
* [Pachyderm](http://pachyderm.io/) - Pachyderm is a data storage platform built on Docker and Kubernetes to provide reproducible data processing and analysis.
* <b><code>&nbsp;&nbsp;3735⭐</code></b> <b><code>&nbsp;&nbsp;&nbsp;330🍴</code></b> [Polyaxon](https://github.com/polyaxon/polyaxon)) - A platform for reproducible and scalable machine learning and deep learning.
* <b><code>&nbsp;&nbsp;&nbsp;421⭐</code></b> <b><code>&nbsp;&nbsp;&nbsp;356🍴</code></b> [Smooks](https://github.com/smooks/smooks)) - An extensible Java framework for building XML and non-XML (CSV, EDI, Java, etc...) streaming applications.

## Distributed Programming

* <b><code>&nbsp;&nbsp;&nbsp;435⭐</code></b> <b><code>&nbsp;&nbsp;&nbsp;&nbsp;85🍴</code></b> [AddThis Hydra](https://github.com/addthis/hydra)) - distributed data processing and storage system originally developed at AddThis.
* [AMPLab SIMR](http://databricks.github.io/simr/) - run Spark on Hadoop MapReduce v1.
* 🌎 [Apache APEX](apex.apache.org/) - a unified, enterprise platform for big data stream and batch processing.
* 🌎 [Apache Beam](beam.apache.org/) - an unified model and set of language-specific SDKs for defining and executing data processing workflows.
* [Apache Crunch](http://crunch.apache.org/) - a simple Java API for tasks like joining and data aggregation that are tedious to implement on plain MapReduce.
* [Apache DataFu](http://incubator.apache.org/projects/datafu.html) - collection of user-defined functions for Hadoop and Pig developed by LinkedIn.
* [Apache Flink](http://flink.apache.org/) - high-performance runtime, and automatic program optimization.
* 🌎 [Apache Gearpump](gearpump.github.io/gearpump/) - real-time big data streaming engine based on Akka.
* [Apache Gora](http://gora.apache.org/) - framework for in-memory data model and persistence.
* [Apache Hama](http://hama.apache.org/) - BSP (Bulk Synchronous Parallel) computing framework.
* 🌎 [Apache MapReduce](wiki.apache.org/hadoop/MapReduce/) - programming model for processing large data sets with a parallel, distributed algorithm on a cluster.
* 🌎 [Apache Pig](pig.apache.org/) - high level language to express data analysis programs for Hadoop.
* [Apache REEF](http://reef.apache.org/) - retainable evaluator execution framework to simplify and unify the lower layers of big data systems.
* [Apache S4](http://incubator.apache.org/projects/s4.html) - framework for stream processing, implementation of S4.
* [Apache Spark](http://spark.apache.org/) - framework for in-memory cluster computing.
* 🌎 [Apache Spark Streaming](spark.apache.org/docs/latest/streaming-programming-guide.html) - framework for stream processing, part of Spark.
* [Apache Storm](http://storm.apache.org) - framework for stream processing by Twitter also on YARN.
* [Apache Samza](http://samza.apache.org/) - stream processing framework, based on Kafka and YARN.
* [Apache Tez](http://tez.apache.org/) - application framework for executing a complex DAG (directed acyclic graph) of tasks, built on YARN.
* 🌎 [Apache Twill](incubator.apache.org/projects/twill.html) - abstraction over YARN that reduces the complexity of developing distributed applications.
* [Baidu Bigflow](http://bigflow.cloud/en/index.html) - an interface that allows for writing distributed computing programs providing lots of simple, flexible, powerful APIs to easily handle data of any scale.
* [Cascalog](http://cascalog.org/) - data processing and queryin