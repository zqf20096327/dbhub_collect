# Branch DB

<img src="./assets/Branch-DB-LOGO-orange.png" width=300 height=300 style="border-radius: 8px"/>

**Branch DB** is a lightweight, high-performance, and simple key-value database built in C++. It offers in-memory and on-disk persistence for storing and retrieving data efficiently. This project aims to provide a basic yet powerful storage engine to experiment with low-level database concepts.

## Sneak Peek in 60 Seconds ( Click to watch )
[![Watch the demo](https://img.youtube.com/vi/20eKOlHn814/maxresdefault.jpg)](https://www.youtube.com/watch?v=20eKOlHn814)
[Watch Video on Youtube](https://www.youtube.com/watch?v=20eKOlHn814)

## High Level Architecture
<img src="./assets/branchdb_architecture.png"  style="border-radius: 8px"/>

## Features

- **Key-Value Store:** Efficient storage and retrieval of key-value pairs using std::unordered_map as the core in-memory data structure.
- **Persistence:** Supports on-disk storage with `WAL` **( Write Ahead Logging )** for durability.
- **Serialization:** Efficient custom binary format for encoding and decoding data
- **Concurrency:** Reader-Writer locks for thread-safe operations
- **TTL:** Support for setting expiry times on keys, with automatic background cleanup of expired entries.
- **LRU ( Least Recently Used ) Cache:** Evicting least used keys, when LRU cache capacity hits.
- **API/CLI Support:** Basic command-line interface for interacting with the database

### ✅ In Scope:

- Basic key-value data storage engine
- On-disk persistence via Write Ahead Logging
- Data serialization/deserialization logic
- Safe concurrent access (read/write locks)
- Simple CLI interface for basic operations
- Clear documentation and open-source release
- LRU ( Least Recently Used ) Cache

## Architecture

Branch DB is designed with a minimalistic architecture to focus on core database principles like storage, concurrency and durability. The system consists of the following components:

1. **Storage Engine** – Manages in-memory and on-disk data storage.
2. **Concurrency Layer** – Implements thread-safety with read-write locks.
3. **Persistence Layer** – Ensures durability by writing data to disk via log files.
4. **TTL Manager** – A background thread that periodically scans for and removes expired keys.
5. **Compact Logging** - Log file is compacted automatically when the `FLUSH` command is executed.
6. **Multi-User Architecture** - Supports multiple databases within a single instance (e.g., `staging`, `production`).
7. **Authentication** - Built-in security to control and verify user access.

---

# Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Prerequisites

You'll need the following tools installed on your system to get started:

- **C++ Toolchain:** A C++ compiler (like `g++` or `clang++`) and `CMake` (version 3.10 or higher).
- **Boost C++ Libraries:** Your project relies on Boost libraries, specifically `Boost.Asio`. Currently using: `1_88_0`
- **Docker:** To build and run the containerized version of the database.
- **Node.js & npm:** To use and develop the client SDK.

# 1. Server Setup

You have two options for running the database server. For production use, the Docker container is highly recommended. And even faster building.

### Option A: Local Development Build

This method compiles and runs the server directly on your machine.

1. Clone the repository:

```
git clone https://github.com/ChandanKhamitkar/BranchDB.git
cd BranchDB
```

2. Install prerequisites

#### Windows (manual installation):
- Install [CMake](https://cmake.org/download/)
- Download and extract [Boost](https://www.boost.org/users/download/), e.g. `C:/local/boost_1_88_0`

#### Linux (Ubuntu/Debian):
```
brew install cmake boost
```

#### macOS (using Homebrew):
```
sudo apt update
sudo apt install cmake build-essential libboost-all-dev
```

3. Build the Project:
#### You can either manually build:
```
mkdir build
cd build
cmake ..
cmake --build .
cd Debug
```

4. Run the BranchDB

```
on Windows
./BranchDB.exe

on Mac
./BranchDB
```

### OR
# Or, use the universal run script that handles build and execution automatically:

```
# Linux/macOS
./branchdb-run.sh

# Windows (CMD)
branchdb-run.cmd

# Windows (PowerShell)
.\branchdb-run.ps1
```

### Option B: Docker Container - Self Containerization

This method builds a self-contained Docker image of your database, which can be run anywhere.

1. Build the Docker Image:

```
docker build -t branchdb-image .
```

2. Run the Container: This command runs the server and exposes it on port 1981.

```
docker run -p 1981:1981 branchdb-image
```

### Option 3: Pulling Docker Image (Recommended)

This method directly pull the image, no need of any Repository Cloning and Manual Building.

1. Pull the image:

```
docker pull chandankhamitkar/branchdb
```

2. Run the Container

#### 2.1 General Approach

```
docker run -p 1981:1981 chandankhamitkar/branchdb
```

#### 2.2 To make sure data is not lost when the container is stopped ( Recommended )

```
docker run -p 1981:1981 -v mydata:/app/data chandankhamitkar/branchdb
```

---

# 2. Client SDK

Once the server is running (either locally or in a Docker container), you can use the Node.js lightweight client SDK to interact with it.

Follow this: [🔗BranchDB Client SDK](https://www.npmjs.com/package/branchdb-client)


## OR
# Connect via `CLI`
```
telnet localhost 1981

or

nc localhost 1981
```
# Commands

| Method                           | Description                                       |
| -------------------------------- | ------------------------------------------------- |
| `SET <key> <value> EX <seconds>` | Sets a key-value as provided & expiry [optional]. |
| `GET <key>`                      | Retrieves the value for a given key.              |
| `DEL <key>`                      | Deletes a key-value pair.                         |
| `EXISTS <key>`                   | Checks if a key exists.                           |
| `TTL <key>`                      | Returns the remaining time to live for a key.     |
| `EXPIRE <key> EX <seconds>`      | Sets a new TTL for an existing key.               |
| `PERSIST <key>`                  | Removes the TTL from a key.                       |
| `GETALL`                         | Returns a list of all keys in the database.       |
| `FLUSH FORCE`                    | Deletes all keys from the database.               |

# License 📄

This project is licensed under the `Apache-2.0 License`. See the [LICENSE](https://github.com/ChandanKhamitkar/BranchDB/blob/main/LICENSE) file for more.

# Author

- **Khamitkar Sai Chandan**
