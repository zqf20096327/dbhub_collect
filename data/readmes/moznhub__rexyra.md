# Rexyra

[![CI](https://github.com/moznhub/rexyra/actions/workflows/ci.yml/badge.svg)](https://github.com/moznhub/rexyra/actions/workflows/ci.yml)
[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](#licence)

A Redis-compatible in-memory data server for Windows, written in Rust.

Rexyra speaks the Redis protocol (RESP2 and RESP3) and implements 201 Redis commands, so existing Redis tools and client libraries can talk to it. It runs as a single native Windows executable: no WSL, no Docker, no runtime to install.

## Highlights

- **Redis-compatible.** Strings, hashes (with Redis 7.4's expiry of single fields), lists, sets, sorted sets, bitmaps, expiry, transactions, blocking commands, Pub/Sub, Lua scripting and functions. Replies and error messages are checked against Redis 7.4.
- **Durable, and interchangeable with Redis.** RDB snapshots and an append-only file in Redis's own formats: Redis loads Rexyra's files and Rexyra loads Redis's.
- **Background saves without `fork`.** A point-in-time snapshot is written while commands keep running. Measured under load, throughput during a save is within a few percent of normal.
- **Memory limit and eviction.** `maxmemory` with the eight Redis eviction policies, measured against what the process has actually allocated.
- **Access control.** Passwords, ACL users with command, category and key-pattern rules, and protected mode.
- **Written in Rust**, with no `unsafe` code in the project itself. Scripting embeds the standard Lua 5.1 interpreter.

## Status

**Version 1.0**, the first stable release. From 1.0 on, version numbers follow [Semantic Versioning](https://semver.org/): within 1.x, what is listed under [Versions and compatibility](#versions-and-compatibility) does not change in an incompatible way.

How it is tested, on every change:

- about 650 tests of its own;
- five client libraries, two versions of each: StackExchange.Redis, redis-py, Jedis, Lettuce and go-redis (see [clients](clients/README.md));
- the installer, on a clean Windows machine: installed, restarted, upgraded (from a build of the same code and from the latest published release), and removed.

Behaviour is compared with Redis 7.4 command by command, and the comparisons are kept as tools that can be run again. Before each release, a six-hour soak test runs a mixed workload with every reply checked and a client that uses client-side caching ([results](docs/benchmarks/soak/README.md)).

Rexyra is new. It has not yet run in production anywhere we know of, so try it with your own workload before relying on it.

It is a **single-instance** server: replication, cluster mode, streams, modules and TLS are not implemented. See [what differs from Redis](docs/COMPATIBILITY.md) and the [roadmap](docs/ROADMAP.md).

## Versions and compatibility

Within 1.x:

- **Commands** keep replying as documented: as Redis 7.4 does, apart from the differences listed in [COMPATIBILITY.md](docs/COMPATIBILITY.md). A change that brings a reply closer to Redis's counts as a fix, and is listed in the [changelog](CHANGELOG.md).
- **Settings and command-line options** keep their names and meaning. None is removed; a new one has a default that leaves behaviour as it was.
- **Data files**: a snapshot or append-only file written by a 1.x version loads in every later 1.x version. Files stay in Redis's formats, loadable by Redis 7.4.
- **The Windows service** keeps its name (`Rexyra`), its account (`LocalService`) and its folders, and an upgrade keeps the settings and the data.

Not covered: the wording of log lines and of `INFO` fields that Redis does not have, performance figures, and the tools in [tools](tools).

Security fixes are made for the latest 1.x version; see [SECURITY.md](SECURITY.md).

## Quick start

**Install it as a service.** Download `rexyra-vX.Y.Z-windows-x86_64.msi` from the [releases page](https://github.com/moznhub/rexyra/releases) and run it. Setup asks for the folder and the port, then installs Rexyra as a Windows service that starts with the machine. See [Running as a Windows service](#running-as-a-windows-service).

**Or just run it.** Download `rexyra-vX.Y.Z-windows-x86_64.zip` from the same page, unzip it and start the server in a terminal. It is one self-contained executable for 64-bit Windows 10 and 11; nothing else needs installing.

```powershell
.\rexyra-server.exe --port 6379
```

Neither download is code-signed, so Windows SmartScreen may ask for confirmation the first time. Each release lists SHA-256 checksums you can compare with `Get-FileHash`.

**Or build from source.** You need [Rust](https://rustup.rs/) (stable, MSVC toolchain) and the Visual Studio Build Tools with the C++ workload, which compiles the bundled Lua interpreter.

```powershell
git clone https://github.com/moznhub/rexyra.git
cd rexyra
cargo build --release
target\release\rexyra-server.exe --port 6379
```

Then use any Redis client:

```powershell
redis-cli -p 6379 ping
redis-cli -p 6379 set greeting hello
redis-cli -p 6379 get greeting
```

## Configuration

Options are given on the command line, in a `redis.conf`-style file passed as the first argument, or both (the command line wins):

```powershell
rexyra-server.exe rexyra.conf --port 7000
```

| Option | Meaning | Default |
|---|---|---|
| `--bind`, `--port` | Address and port to listen on | `127.0.0.1`, `6379` |
| `--requirepass` | Password clients must give with `AUTH` | none |
| `--protected-mode` | Without a password, accept only local connections | `yes` |
| `--dir`, `--dbfilename` | Where the snapshot is kept. The folder must exist: as in Redis, the server will not start without it. | `.`, `dump.rdb` |
| `--logfile` | File the log is written to | standard error |
| `--logfile-max-size`, `--logfile-max-files` | Size at which the log file is started afresh, and how many earlier ones (`rexyra.1.log`, ...) are kept; `0` never rolls it | `100mb`, `5` |
| `--save` | Automatic snapshots, as `seconds changes` pairs | `3600 1 300 100 60 10000` |
| `--appendonly`, `--appendfsync` | The append-only file and when it is forced to disk | `no`, `everysec` |
| `--maxmemory`, `--maxmemory-policy` | Memory limit and what to evict at the limit | none, `noeviction` |
| `--notify-keyspace-events` | Keyspace notifications to publish, in Redis's letters (`KEA` for all); see [COMPATIBILITY.md](docs/COMPATIBILITY.md#keyspace-notifications) | none |
| `--tracking-table-max-keys` | The most keys client-side caching (`CLIENT TRACKING`) remembers before it invalidates some; `0` for no limit | `1000000` |
| `--databases`, `--maxclients` | Number of databases and of simultaneous clients | `16`, `10000` |

Run `rexyra-server.exe --help` for the full list. Many settings can also be changed while the server runs with `CONFIG SET`, and `CONFIG REWRITE` saves them, with any users made with `ACL SETUSER`, to the configuration file for the next start. Directives in a configuration file that Rexyra does not support are skipped with a warning, so an existing `redis.conf` is a reasonable starting point.

## Running as a Windows service

The installer (`.msi`) sets this up for you: it puts the program in the folder you choose, writes a configuration file with the port you choose, and installs and starts a service called **Rexyra**. The service runs under the low-privilege `LocalService` account, starts with Windows, is restarted if it crashes, and saves its data when it is stopped or the machine shuts down.

| | |
|---|---|
| `C:\Program Files\Rexyra\` | The program |
| `C:\ProgramData\Rexyra\rexyra.conf` | The settings; edit and restart the service to change them |
| `C:\ProgramData\Rexyra\data\` | The data files |
| `C:\ProgramData\Rexyra\logs\rexyra.log` | The log, with up to five earlier files of 100 MB each beside it |

For a scripted install:

```powershell
msiexec /i rexyra-vX.Y.Z-windows-x86_64.msi /qn PORT=6380 INSTALLFOLDER="D:\Rexyra"
```

**[docs/WINDOWS-SERVICE.md](docs/WINDOWS-SERVICE.md)** covers the rest: upgrading and removing, what is kept when the service stops, opening the port to other machines, and setting the service up by hand with `rexyra-server.exe --service`.

## Supported commands

| Group | Commands |
|-------|----------|
| Connection | `PING` `ECHO` `HELLO` `AUTH` `SELECT` `QUIT` `RESET` `CLIENT` (`ID`, `GETNAME`, `SETNAME`, `SETINFO`, `LIST`, `INFO`, `KILL`, `UNBLOCK`, `NO-EVICT`, `NO-TOUCH`, and for client-side caching `TRACKING`, `CACHING`, `GETREDIR`, `TRACKINGINFO`) |
| Server | `COMMAND` (`COUNT`, `LIST`, `INFO`, `DOCS`, `GETKEYS`, `GETKEYSANDFLAGS`) `DBSIZE` `SWAPDB` `FLUSHDB` `FLUSHALL` `INFO` `CONFIG` (`GET`, `SET`, `RESETSTAT`) `SLOWLOG` (`GET`, `LEN`, `RESET`) `MEMORY` (`USAGE`) `ACL` (`SETUSER`, `GETUSER`, `DELUSER`, `LIST`, `USERS`, `WHOAMI`, `CAT`, `GENPASS`, `DRYRUN`) `TIME` `SAVE` `LASTSAVE` `SHUTDOWN` `BGSAVE` `BGREWRITEAOF` `DEBUG` (`PANIC`, `SET-ACTIVE-EXPIRE`) |
| Pub/Sub | `SUBSCRIBE` `UNSUBSCRIBE` `PSUBSCRIBE` `PUNSUBSCRIBE` `SSUBSCRIBE` `SUNSUBSCRIBE` `PUBLISH` `SPUBLISH` `PUBSUB` (`CHANNELS`, `NUMSUB`, `NUMPAT`, `SHARDCHANNELS`, `SHARDNUMSUB`, `HELP`), and keyspace notifications (`notify-keyspace-events`) |
| Transactions | `MULTI` `EXEC` `DISCARD` `WATCH` `UNWATCH` |
| Scripting | `EVAL` `EVALSHA` `EVAL_RO` `EVALSHA_RO` `SCRIPT` (`LOAD`, `EXISTS`, `FLUSH`, `KILL`) `FCALL` `FCALL_RO` `FUNCTION` (`LOAD`, `DELETE`, `FLUSH`, `LIST`, `STATS`, `KILL`, `DUMP`, `RESTORE`) |
| Keys | `DEL` `UNLINK` `EXISTS` `TOUCH` `TYPE` `RENAME` `RENAMENX` `COPY` `MOVE` `KEYS` `SCAN` `RANDOMKEY` `SORT` `SORT_RO` `DUMP` `RESTORE` `OBJECT` (`ENCODING`, `REFCOUNT`, `IDLETIME`, `FREQ`) |
| Expiry | `EXPIRE` `PEXPIRE` `EXPIREAT` `PEXPIREAT` `TTL` `PTTL` `EXPIRETIME` `PEXPIRETIME` `PERSIST` |
| Strings | `GET` `SET` `SETNX` `SETEX` `PSETEX` `GETSET` `GETDEL` `GETEX` `MGET` `MSET` `MSETNX` `INCR` `DECR` `INCRBY` `DECRBY` `INCRBYFLOAT` `APPEND` `STRLEN` `GETRANGE` `SUBSTR` `SETRANGE` `LCS` |
| Bitmaps | `SETBIT` `GETBIT` `BITCOUNT` `BITPOS` `BITOP` `BITFIELD` `BITFIELD_RO` |
| Hashes | `HSET` `HMSET` `HSETNX` `HGET` `HMGET` `HDEL` `HGETALL` `HKEYS` `HVALS` `HLEN` `HEXISTS` `HSTRLEN` `HINCRBY` `HINCRBYFLOAT` `HSCAN` `HRANDFIELD` `HEXPIRE` `HPEXPIRE` `HEXPIREAT` `HPEXPIREAT` `HTTL` `HPTTL` `HEXPIRETIME` `HPEXPIRETIME` `HPERSIST` |
| Lists | `LPUSH` `RPUSH` `LPUSHX` `RPUSHX` `LPOP` `RPOP` `LMPOP` `LMOVE` `RPOPLPUSH` `BLPOP` `BRPOP` `BLMPOP` `BLMOVE` `BRPOPLPUSH` `LLEN` `LRANGE` `LINDEX` `LPOS` `LSET` `LINSERT` `LREM` `LTRIM` |
| Sets | `SADD` `SREM` `SCARD` `SISMEMBER` `SMISMEMBER` `SMEMBERS` `SMOVE` `SPOP` `SRANDMEMBER` `SSCAN` `SINTER` `SUNION` `SDIFF` `SINTERSTORE` `SUNIONSTORE` `SDIFFSTORE` `SINTERCARD` |
| Sorted sets | `ZADD` `ZINCRBY` `ZREM` `ZCARD` `ZSCORE` `ZMSCORE` `ZRANK` `ZREVRANK` `ZCOUNT` `ZLEXCOUNT` `ZRANGE` `ZREVRANGE` `ZRANGEBYSCORE` `ZREVRANGEBYSCORE` `ZRANGEBYLEX` `ZREVRANGEBYLEX` `ZRANGESTORE` `ZREMRANGEBYRANK` `ZREMRANGEBYSCORE` `ZREMRANGEBYLEX` `ZPOPMIN` `ZPOPMAX` `ZMPOP` `BZPOPMIN` `BZPOPMAX` `BZMPOP` `ZUNION` `ZINTER` `ZDIFF` `ZUNIONSTORE` `ZINTERSTORE` `ZDIFFSTORE` `ZINTERCARD` `ZSCAN` `ZRANDMEMBER` |

## Compatibility

For the commands above, Rexyra is meant to be indistinguishable from Redis 7.x to a client. Where it is not, the difference is listed in [docs/COMPATIBILITY.md](docs/COMPATIBILITY.md), together with the details of persistence, the memory limit and access control. A few to know about up front:

- No replication, cluster mode, streams or TLS.
- Users created with `ACL SETUSER` are not saved; put the ones that must survive a restart in the configuration file.
- `SCAN` cursors are valid but not numerically the same as Redis's.
- Snapshots and append-only files written by Redis older than 7.0, or containing streams or module data, are refused with a message saying why.

If you find a difference that is not documented, that is a bug worth reporting.

## Performance

No comparison with Redis or any other server has been made yet. What has been measured, on one desktop machine (Ryzen 9 7900X, NVMe disk, Windows 11) with 50 connections sending `GET` and `SET` of 1 KB values without pipelining:

- about 115,000 commands per second, with a 99th-percentile latency of 0.8 ms;
- during a background save, throughput 2–7 % lower and the 99th percentile unchanged, including with 100 MB strings in the keyspace and with a deliberately slowed disk;
- with hashes of a million fields and lists of two million elements in the keyspace, no pause longer than 2 ms for other clients during a save;
- a snapshot of a million 1 KB keys written in about 2 seconds when idle and about 3 seconds under that load.

The method, raw results and the tool that produced them are in [docs/benchmarks](docs/benchmarks/bgsave) and [tools/rexyra-bench](tools/rexyra-bench).

## Building and testing

```powershell
cargo build --release
cargo test --workspace
cargo clippy --workspace --all-targets -- -D warnings
cargo fmt --all -- --check
```

Fuzzing the protocol parser needs a nightly toolchain and [cargo-fuzz](https://github.com/rust-fuzz/cargo-fuzz):

```powershell
cargo +nightly fuzz run request
cargo +nightly fuzz run frame
```

## Project layout

| Path | Contents |
|---|---|
| `crates/resp` | RESP2/RESP3 parser, decoder and encoder (no I/O) |
| `crates/engine` | The keyspace: hash table, databases, value types, expiry (no I/O, no clock) |
| `crates/persist` | The RDB snapshot format: writer, reader, checksum |
| `crates/commands` | Command table and handlers, persistence, eviction, scripting, users and permissions |
| `crates/server` | Networking, the command-execution thread, configuration, the `rexyra-server` binary |
| `tools/rexyra-bench` | Load generator for measuring background saves under traffic, and the throughput of single commands |
| `tools/rexyra-keyevents` | Records the keyspace notifications a script of commands produces, to compare with Redis |
| `fuzz` | cargo-fuzz targets for the protocol crate |
| `docs` | Compatibility notes, roadmap, design notes, benchmarks |

One thread executes every command and owns the data; network I/O runs on a Tokio runtime and hands requests to it. How a consistent snapshot is taken without `fork` is described in [docs/design/snapshot-without-fork.md](docs/design/snapshot-without-fork.md).

## Contributing

Contributions are welcome, and the most useful one is simple: tell us where Rexyra behaves differently from Redis. Bug reports, tests with real client libraries, missing commands and documentation fixes are all appreciated.

Start with [CONTRIBUTING.md](CONTRIBUTING.md); it explains how to set up, what a pull request needs, and how the code is organised. The [roadmap](docs/ROADMAP.md) lists what is not done. Everyone taking part is expected to follow the [Code of Conduct](CODE_OF_CONDUCT.md).

Please report security problems privately, as described in [SECURITY.md](SECURITY.md).

## Licence

Licensed under the [Apache License, Version 2.0](LICENSE).

The libraries it is built with keep their own licences, which are mostly MIT or Apache-2.0; their notices are in `THIRD-PARTY-NOTICES.txt` in each download.

Unless you state otherwise, any contribution you submit for inclusion in Rexyra is licensed under the Apache License, Version 2.0, without additional terms.

## Trademark notice

Rexyra is an independent project. Redis is a trademark of Redis Ltd. Rexyra is not affiliated with, endorsed by or sponsored by Redis Ltd.; the name is used here only to describe compatibility.
