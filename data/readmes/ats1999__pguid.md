# pguid

A PostgreSQL extension that generates distributed, globally unique 64-bit identifiers using a Snowflake-like ID generation algorithm.

## Overview

**pguid** is a high-performance PostgreSQL extension written in C that generates unique, sortable identifiers suitable for distributed systems. It combines a timestamp, node ID, and sequence number to create 64-bit integers that are both globally unique and time-ordered.

## Features

- **Distributed ID Generation**: Supports multiple nodes (up to 1024) generating IDs independently
- **Time-Ordered IDs**: IDs are sortable by timestamp, making them efficient for database indexing
- **High Throughput**: Generates up to 4096 IDs per millisecond per node
- **Thread-Safe**: Uses PostgreSQL's lightweight locks (LWLock) for safe concurrent access
- **Custom Epoch**: Configurable epoch (defaults to Jan 1, 2024) to extend ID validity
- **Zero Configuration**: Works out of the box with optional node ID configuration

## ID Structure

64-bit ID layout:
```
[Timestamp (41 bits) | Node ID (10 bits) | Sequence (12 bits)]
[        41         |        10         |        12         ]
```

- **Timestamp**: Milliseconds since custom epoch (Jan 1, 2024)
- **Node ID**: Identifier for the generating node (0-1023)
- **Sequence**: Incremental counter for IDs generated in the same millisecond (0-4095)

### Limits

- Time range: ~2200+ years from epoch
- Max nodes: 1024
- Max IDs per second: ~4.1 million

## Installation

### From Source

1. Ensure PostgreSQL development files are installed:
   ```bash
   # macOS (Homebrew)
   brew install postgresql

   # Ubuntu/Debian
   sudo apt-get install postgresql-server-dev-15
   ```

2. Build and install:
   ```bash
   make
   make install
   ```

3. Create the extension in your database:
   ```sql
   CREATE EXTENSION pguid;
   ```

## Usage

### Basic ID Generation

```sql
-- Generate a new ID
SELECT pguid();
       pguid
---------------------
 369098147652968448
(1 row)

-- Use in a table
CREATE TABLE users (
    id BIGINT DEFAULT pguid() PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE TABLE

INSERT INTO users (name) VALUES ('Alice');
INSERT 0 1

INSERT INTO users (name) VALUES ('Bob');
INSERT 0 1

SELECT * FROM users;
 id                  | name  |         created_at
---------------------+-------+----------------------------
 369098147652968448  | Alice | 2026-03-29 10:30:15.123456
 369098147656162944  | Bob   | 2026-03-29 10:30:15.234567
(2 rows)
```

### Configuration

Configure the node ID to ensure uniqueness across multiple PostgreSQL instances:

```sql
-- Set in postgresql.conf
pguid.node_id = 1
```

Then restart PostgreSQL. The node ID must be set before the extension generates its first ID, as it's stored in shared memory.

```sql
-- Verify configuration
SHOW pguid.node_id;
```

## Architecture

### Shared Memory State

The extension maintains shared state across all PostgreSQL processes:

```c
typedef struct {
    int64 last_ts;      // Last generated timestamp
    uint16 seq;         // Sequence counter for current millisecond
    LWLock lock;        // Lightweight lock for synchronization
} pguid_state;
```

### Thread Safety

- All ID generation is protected by a lightweight lock (`LWLockAcquire`)
- The sequence counter resets when the timestamp advances
- If the sequence overflows, the timestamp is incremented

## Building & Development

### Requirements

- PostgreSQL 10+
- C compiler (gcc/clang)
- PostgreSQL development headers

### Build Commands

```bash
# Build the extension
make

# Install to PostgreSQL
make install

# Create a test database and load the extension
createdb pguid_test
psql pguid_test -c "CREATE EXTENSION pguid;"

# Test it
psql pguid_test -c "SELECT pguid(), pguid(), pguid();"
```

### Files

- `pguid.c` - Main C extension code
- `pguid.control` - PostgreSQL extension metadata
- `pguid--1.0.sql` - SQL function definitions
- `Makefile` - Build configuration
- `build.sh` - Build script

## Performance

Each call to `pguid()` acquires a lightweight lock for a very short duration, making it suitable for high-throughput environments. The function typically completes in microseconds.

## License

This project is provided as-is. Check the repository for license information.