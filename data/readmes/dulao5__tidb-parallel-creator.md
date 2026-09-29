# tidb-parallel-creator

Accelerate large-scale table creation in TiDB using its **Accelerated Table Creation** feature (v8.1 ~ v8.5).

This tool extracts `CREATE TABLE` statements from a MySQL `mysqldump` schema file and submits them in parallel using Go routines, achieving significantly faster table creation in TiDB — up to **140 QPS** in local testing.

## 🔍 Background

Since TiDB v8.1, the system variable [`tidb_enable_fast_create_table`](https://docs.pingcap.com/tidb/stable/accelerated-table-creation/) allows DDLs to be merged and committed in a single transaction to reduce overhead.

However, to take advantage of this feature, **all `CREATE TABLE` statements must be:**

- Submitted in the same schema (`CREATE TABLE ...`)
- Submitted **at the same time**
- Sent via independent sessions (parallel connections)

This makes it challenging to trigger fast path table creation using manual scripts or naive clients.

## 🚀 What This Tool Does

1. **Parses** a schema-only `mysqldump` file and extracts all `CREATE TABLE` statements.
2. **Splits** the statements into batches.
3. **Submits** each batch in parallel, using independent connections, within a controlled time window.
4. **Logs** the result of each statement.

## 📦 Installation

Clone the repository and build:

```bash
git clone https://github.com/dulao5/tidb-parallel-creator.git
cd tidb-parallel-creator
go build -o tidb-parallel-creator main.go
```

## ⚙️  Usage
```
tidb-parallel-creator \
  -u root \
  -h $offline_host \
  -p $pw \
  -P 4000 \
  -d $dbname \
  -j 50 \
  -f ~/schema.sql
```

