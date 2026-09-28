# SawitDB (Go Version)

![SawitDB Banner](https://github.com/WowoEngine/SawitDB/raw/main/docs/sawitdb.jpg)

<div align="center">

[![Docs](https://img.shields.io/badge/Docs-Read%20Now-blue?style=for-the-badge&logo=googledocs)](https://wowoengine.github.io/SawitDB/)
[![Go Report Card](https://goreportcard.com/badge/github.com/WowoEngine/SawitDB-Go?style=for-the-badge)](https://goreportcard.com/report/github.com/WowoEngine/SawitDB-Go)
[![Node.js Version](https://img.shields.io/badge/Node.js%20Version-Visit%20Repo-green?style=for-the-badge&logo=nodedotjs)](https://github.com/WowoEngine/SawitDB)
[![PHP Version](https://img.shields.io/badge/PHP%20Version-Visit%20Repo-purple?style=for-the-badge&logo=php)](https://github.com/WowoEngine/SawitDB-PHP)

</div>

**SawitDB (Go)** is the high-performance Golang implementation of SawitDB. It aims to provide near-native speeds while maintaining full compatibility with the `.sawit` binary format used by the Node.js and PHP versions.

**🚨 Emergency: Aceh Flood Relief**
Please support our brothers and sisters in Aceh.

[![Kitabisa](https://img.shields.io/badge/Kitabisa-Bantu%20Aceh-blue?style=flat&logo=heart)](https://kitabisa.com/campaign/donasipedulibanjiraceh)

## Features (v2.5.0)

- **Paged Architecture**: Data is stored in 4096-byte binary pages.
- **Object Caching (New)**: Implements Page-Level Object Caching for high-speed reads (bypassing JSON parse for hot pages).
- **Hash Joins (New)**: Optimized `JOIN` operations (O(M+N)) for massive performance gains on relations.
- **Persistent Indexes (New)**: Indexes are now automatically persisted in `_indexes` system table and restored on load.
- **Query Cache (New)**: LRU Cache for parsed queries to reduce CPU overhead.
- **Concurrency**: Goroutine-safe server implementation.
- **Network Support**: Client-Server architecture using TCP.

## Installation

```bash
go get github.com/WowoEngine/SawitDB-Go
```

## Quick Start (CLI)

Build the CLI tool:

```bash
go build -o sawit-cli.exe ./cmd/cli
./sawit-cli
```

Inside the interactive shell:
```sql
MASUK WILAYAH my_plantation
LAHAN trees
TANAM KE trees (id, type) BIBIT (1, 'Dura')
PANEN * DARI trees
```

## Quick Start (Server)

```bash
go run cmd/sawit-server/main.go
# Or build
go build -o sawit-server.exe ./cmd/sawit-server
./sawit-server
```

The server will start on `0.0.0.0:7878` by default.

## Usage (Embedded)

You can use the Engine directly in your Go applications.

```go
package main

import (
	"fmt"
	"github.com/WowoEngine/SawitDB-Go/internal/engine"
)

func main() {
	db, _ := engine.NewSawitDB("./data/plantation.sawit")
	defer db.Close()

	// AQL
	db.Query("LAHAN trees", nil)
	db.Query("TANAM KE trees (id, type) BIBIT (1, 'Dura')", nil)

	// Fetch
	res, _ := db.Query("PANEN * DARI trees DIMANA type='Dura'", nil)
	fmt.Println(res)
}
```

## Architecture Details

- **pkg/engine**: Core Database Engine logic.
- **pkg/storage**: Pager and File I/O.
- **pkg/parser**: Query Parser (AQL/SQL).
- **pkg/index**: B-Tree Index implementation.
- **pkg/server**: TCP Server implementation.

## Full Feature Comparison

| Feature | Tani Edition (AQL) | Generic SQL (Standard) | Notes |
|---------|-------------------|------------------------|-------|
| **Create DB** | `BUKA WILAYAH [db]` | `CREATE DATABASE [db]` | Creates `.sawit` in data/ |
| **Use DB** | `MASUK WILAYAH [db]` | `USE [db]` | Switch context |
| **Show DBs** | `LIHAT WILAYAH` | `SHOW DATABASES` | Lists available DBs |
| **Create Table** | `LAHAN [table]` | `CREATE TABLE [table]` | Schema-less creation |
| **Show Tables** | `LIHAT LAHAN` | `SHOW TABLES` | Lists tables in DB |
| **Drop Table** | `BAKAR LAHAN [table]` | `DROP TABLE [table]` | Deletes table & data |
| **Insert** | `TANAM KE [table] ... BIBIT (...)` | `INSERT INTO [table] (...) VALUES (...)` | Auto-ID if omitted |
| **Select** | `PANEN ... DARI [table] DIMANA ...` | `SELECT ... FROM [table] WHERE ...` | Supports Projection |
| **Join** | `... GABUNG [tbl] PADA ...` | `... JOIN [tbl] ON ...` | Hash/Nested Loop |
| **Update** | `PUPUK [table] DENGAN ... DIMANA ...` | `UPDATE [table] SET ... WHERE ...` | Atomic update |
| **Delete** | `GUSUR DARI [table] DIMANA ...` | `DELETE FROM [table] WHERE ...` | Row-level deletion |
| **Index** | `INDEKS [table] PADA [field]` | `CREATE INDEX ON [table] (field)` | B-Tree Indexing |
| **Count** | `HITUNG COUNT(*) DARI [table]` | `SELECT COUNT(*) FROM [table]` (via HITUNG) | Aggregation |

## License

MIT License