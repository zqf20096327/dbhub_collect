# Reindexer

[![GoDoc](https://godoc.org/github.com/Restream/reindexer?status.svg)](https://godoc.org/github.com/Restream/reindexer)
[![Build Status](https://github.com/Restream/reindexer/workflows/build/badge.svg?branch=master)](https://github.com/Restream/reindexer/actions)
[![Build Status](https://ci.appveyor.com/api/projects/status/yonpih8vx3acaj86?svg=true)](https://ci.appveyor.com/project/olegator77/reindexer)

**Reindexer** is an embeddable, in-memory, document-oriented database with a high-level Query builder interface.

Reindexer's goal is to provide fast search with complex queries. We at Restream weren't happy with Elasticsearch and created Reindexer as a more performant alternative.

The core is written in C++ and the application level API is in Go.

This document describes the Go connector and its API. For information about the Reindexer server and HTTP API, refer to the
[Reindexer documentation](cpp_src/readme.md).

# Table of contents:

- [Features](#features)
  - [Performance](#performance)
  - [Memory Consumption](#memory-consumption)
  - [Full text search](#full-text-search)
  - [Vector indexes (ANN/KNN)](#vector-indexes-annknn)
  - [Hybrid search](#hybrid-search)
  - [Disk Storage](#disk-storage)
  - [Replication](#replication)
  - [Sharding](#sharding)
- [Usage](#usage)
  - [SQL compatible interface](#sql-compatible-interface)
- [Installation](#installation)
  - [Installation for server mode](#installation-for-server-mode)
    - [Official docker image](#official-docker-image)
  - [Installation for embedded mode](#installation-for-embedded-mode)
    - [Prerequisites](#prerequisites)
    - [Get Reindexer using go.mod](#get-reindexer-using-gomod)
    - [Get Reindexer using go.mod and replace](#get-reindexer-using-gomod-and-replace)
    - [Get Reindexer for apps without go.mod (vendoring)](#get-reindexer-for-apps-without-gomod-vendoring)
    - [Get Reindexer using go.mod (vendoring)](#get-reindexer-using-gomod-vendoring)
- [Advanced Usage](#advanced-usage)
  - [Index Types and Their Capabilities](#index-types-and-their-capabilities)
    - [NULL-values filtration](#null-values-filtration)
  - [Nested Structs](#nested-structs)
  - [Sort](#sort)
    - [Forced sort](#forced-sort)
  - [Functions](#functions)
    - [flat_array_len(field_name)](#flat_array_lenfield_name)
    - [now(unit)](#nowunit)
  - [Counting](#counting)
  - [Text pattern search with LIKE condition](#text-pattern-search-with-like-condition)
  - [Update queries](#update-queries)
    - [Update queries with inner joins and subqueries](#update-queries-with-inner-joins-and-subqueries)
    - [Update field with object](#update-field-with-object)
    - [Remove field via update-query](#remove-field-via-update-query)
    - [Update array elements by indexes](#update-array-elements-by-indexes)
    - [Concatenate arrays](#concatenate-arrays)
    - [Remove array elements by values](#remove-array-elements-by-values)
  - [Delete queries](#delete-queries)
  - [Truncate queries](#truncate-queries)
  - [Transactions and batch update](#transactions-and-batch-update)
    - [Synchronous mode](#synchronous-mode)
    - [Async batch mode](#async-batch-mode)
    - [Transactions commit strategies](#transactions-commit-strategies)
    - [Implementation notes](#implementation-notes)
  - [Join](#join)
    - [Nested Join](#nested-join)
    - [Anti-join](#anti-join)
    - [Joinable interface](#joinable-interface)
  - [Subqueries (nested queries)](#subqueries-nested-queries)
  - [Complex Primary Keys and Composite Indexes](#complex-primary-keys-and-composite-indexes)
  - [Aggregations](#aggregations)
  - [Search in array fields](#search-in-array-fields)
    - [Search in array fields with matching indexes](#search-in-array-fields-with-matching-indexes)
    - [Search in array fields with matching indexes using grouping](#search-in-array-fields-with-matching-indexes-using-grouping)
      - [Query Execution Examples](#query-execution-examples)
    - [Grouped values extraction examples

[...截断...]

 for more complex cases](#grouped-values-extraction-examples-for-more-complex-cases)
  - [Atomic on update functions](#atomic-on-update-functions)
  - [Expire Data from Namespace by Setting TTL](#expire-data-from-namespace-by-setting-ttl)
  - [Direct JSON operations](#direct-json-operations)
    - [Upsert data in JSON format](#upsert-data-in-json-format)
    - [Get Query results in JSON format](#get-query-results-in-json-format)
  - [Using object cache](#using-object-cache)
    - [DeepCopy interface](#deepcopy-interface)
    - [Get shared objects from object cache (USE WITH CAUTION)](#get-shared-objects-from-object-cache-use-with-caution)
    - [Limit size of object cache](#limit-size-of-object-cache)
    - [Geometry](#geometry)
- [Events subscription](#events-subscription)
- [Logging, debug, profiling and tracing](#logging-debug-profiling-and-tracing)
  - [Turn on logger](#turn-on-logger)
  - [Slow actions logging](#slow-actions-logging)
  - [Debug queries](#debug-queries)
  - [Custom allocators support](#custom-allocators-support)
  - [Profiling](#profiling)
    - [Heap profiling](#heap-profiling)
    - [CPU profiling](#cpu-profiling)
    - [Known profiling issues](#known-profiling-issues)
  - [Tracing](#tracing)
- [Integration with other programming languages](#integration-with-other-programming-languages)
  - [Reindexer for python](#pyreindexer-for-python)
  - [Reindexer for java](#reindexer-for-java)
    - [Spring wrapper](#spring-wrapper)
  - [3rd party open source connectors](#3rd-party-open-source-connectors)
    - [PHP](#php)
    - [Rust](#rust)
    - [.NET](#net)
- [Limitations and known issues](#limitations-and-known-issues)
- [Getting help](#getting-help)
- [References](#references)

## Features

Key features:

- Sortable indices
- Aggregation queries
- Indices on array fields
- Complex primary keys
- Composite indices
- Join operations
- Full-text search
- Up to 256 indexes (255 user's index + 1 internal index) for each namespace
- ORM-like query interface
- SQL queries

### Performance

Performance has been our top priority from the start, and we think we managed to get it pretty good. Benchmarks show that Reindexer's performance is on par with a typical key-value database. On a single CPU core, we get:

- up to 500K queries/sec for queries `SELECT * FROM items WHERE id='?'`
- up to 50K queries/sec for queries `SELECT * FROM items WHERE year > 2010 AND name = 'string' AND id IN (....)`
- up to 20K queries/sec for queries `SELECT * FROM items WHERE year > 2010 AND name = 'string' JOIN subitems ON ...`

See benchmarking results and more details in [benchmarking repo](https://github.com/Restream/reindexer-benchmarks)

### Memory Consumption

Reindexer aims to consume as little memory as possible; most queries are processed without any memory allocation at all.

To achieve that, several optimizations are employed, both on the C++ and Go level:

- Documents and indices are stored in dense binary C++ structs, so they don't impose any load on Go's garbage collector.

- String duplicates are merged.

- Memory overhead is about 32 bytes per document + ≈4-16 bytes per each search index.

- There is an object cache on the Go level for deserialized documents produced after query execution. Future queries use pre-deserialized documents, which cuts repeated deserialization and allocation costs

- The Query interface uses `sync.Pool` for reusing internal structures and buffers.
  The combination of these technologies allows Reindexer to handle most queries without any allocations.

### Full text search

Reindexer has internal full text search engine. Full text search usage documentation and examples are [here](fulltext.md)

### Vector indexes (ANN/KNN)

Reindexer has internal k-nearest neighbors search engine. k-nearest neighbors search usage documentation and examples are [here](float_vector.md). For selective post-filtered pages on HNSW, see [streaming KNN](float_vector.md#streaming-knn-hnsw) (omit `k` and `radius`, use `LIMI