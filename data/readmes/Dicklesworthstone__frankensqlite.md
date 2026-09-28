<div align="center">
  <img src="site/spec-evolution/frankensqlite_illustration.webp" alt="FrankenSQLite — a Frankenstein monster building a database engine at his workbench">
</div>

<h1 align="center">FrankenSQLite</h1>

<p align="center">
  <strong>An independent ground-up Rust reimplementation of SQLite with page-level MVCC concurrent-writer support.</strong>
</p>

<p align="center">
  <a href="https://github.com/Dicklesworthstone/frankensqlite/actions/workflows/verification-gates.yml"><img src="https://img.shields.io/github/actions/workflow/status/Dicklesworthstone/frankensqlite/verification-gates.yml?branch=main&label=CI" alt="CI"></a>
  <a href="https://github.com/Dicklesworthstone/frankensqlite/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT%2BOpenAI%2FAnthropic%20Rider-blue.svg" alt="License: MIT+Rider"></a>
  <a href="https://www.rust-lang.org/"><img src="https://img.shields.io/badge/rust-nightly%20%7C%20edition%202024-orange.svg" alt="Rust"></a>
  <a href="https://github.com/Dicklesworthstone/frankensqlite"><img src="https://img.shields.io/badge/unsafe-only%20in%20VFS%20%2B%20C%20ABI-blue.svg" alt="unsafe only in VFS + C ABI"></a>
</p>

---

## TL;DR

**The Problem:** SQLite allows only one writer at a time. A single lock byte (`WAL_WRITE_LOCK` at `wal.c:3698`) serializes all writers. For write-heavy workloads, this bottleneck caps throughput regardless of how many cores you have. Torn writes and bit-flips can corrupt the database with no self-repair mechanism.

**The Solution:** FrankenSQLite reimplements SQLite from scratch in Rust, with a safe engine core and two architectural innovations:

1. **MVCC Concurrent Writers.** The single-writer lock is replaced with page-level Multi-Version Concurrency Control. Writers that touch different pages can overlap their page work, while commit validation and publication still contain coordinated sections. Serializable Snapshot Isolation (SSI) tracks write-skew dependencies by default. A safe write-merge ladder (intent replay + structured page patches) is present as dormant/tested implementation work but is not yet wired into the live commit path; current same-page base drift aborts and retries.

2. **RaptorQ Durability Research.** The workspace contains RaptorQ/ECS building blocks and partial native-mode integration. The live compatibility runtime does not yet justify a blanket self-healing or numeric durability claim; the native-mode sections below are design plus partial implementation and are gated on end-to-end recovery evidence.

The current runnable engine is already real, but still hybrid. Compatibility mode over standard SQLite files is the live runtime path today. Database text encodings UTF-8 (encoding 1) and UTF-16le/UTF-16be (encodings 2/3) are admitted for both reads and writes; UTF-16 support is newer than the long-verified UTF-8 surface, and attaching databases with mismatched encodings is rejected. Native mode / ECS sections below describe the longer-term design plus partial implementation work. See "Current Implementation Status" before treating every section as present-day behavior.

### Install the CLI

Linux and macOS:

```bash
curl -fsSL "https://raw.githubusercontent.com/Dicklesworthstone/frankensqlite/main/install.sh?$(date +%s)" | bash
```

Windows PowerShell:

```powershell
irm "https://raw.githubusercontent.com/Dicklesworthstone/frankensqlite/main/install.ps1?$([DateTime]::UtcNow.Ticks)" | iex
```

The installers select the native release artifact, require its SHA-256 entry,
authenticate the signed checksum manifest when `minisign` is available, and
run exact-version plus SQL smoke tests before reporting success. The Linux
artifacts are fully static so the same downloads work on glibc- and musl-based
distributions. Exact-version, air-gapped, custom-destination, source-build, and
post-install verification controls are documented by `install.sh --help` and
`Get-Help ./install.ps1 -Detailed`. Rust users can instead install the CLI

[...截断...]

 with
`cargo +nightly install fsqlite-cli --locked` (the workspace builds on the
dated nightly toolchain pinned in `rust-toolchain.toml`). Prebuilt installer support covers
v0.1.16-v0.1.17 and resumes with v0.2.0; v0.1.18-v0.1.19 did not publish native
signed artifact sets. When `minisign` is present, a missing or invalid
signature fails closed rather than silently downgrading authenticity.

### Why FrankenSQLite?

| Feature | C SQLite | FrankenSQLite |
|---------|----------|---------------|
| Concurrent writers | 1 (file-level lock) | Many by design (page-level MVCC with SSI); full concurrent-writer certification remains gated on the correctness gates below |
| Isolation level | SERIALIZABLE (by serializing) | SERIALIZABLE (SSI for concurrent mode) |
| Concurrent readers | Many (WAL; 5 read-mark slots by default) | Many (Compat: same 5 read-mark slots; Native: bounded by txn-slot capacity, no WAL-index cap) |
| Memory safety | Manual (C) | Core engine is safe Rust; `unsafe` is limited to `fsqlite-vfs` (mmap/shm) and the optional `fsqlite-c-api` shim (FFI) |
| Data races | Possible (careful C) | Prevented inside the Rust engine by ownership and type-system checks |
| File format | SQLite 3.x | SQLite 3.x layout; UTF-8 and UTF-16le/be text encodings are admitted for reads and writes, with parity verification deepest on the UTF-8 surface |
| Self-healing storage | No | Native file-backed connections can generate WAL repair symbols asynchronously; automatic FEC recovery is not wired to the compatibility WAL reader |
| Page-level encryption | No (commercial SEE extension) | Not currently available: the XChaCha20-Poly1305 DEK/KEK implementation exists in `fsqlite-pager`, but no `PRAGMA key`/`rekey` dispatch is wired into `Connection` |
| SQL dialect | Full | Large and growing subset; parser coverage exceeds full execution parity today |
| Extensions | FTS3/4/5, R-tree, JSON1, etc. | Extension crates are present; some runtime wiring is still in progress |
| Cross-process MVCC | No | Partial (shared-memory coordination, bounded by the measured harness scale) |
| Embedded, zero-config | Yes | Yes |

---

## Design Philosophy

### 1. Independent Reimplementation, Not a Translation

FrankenSQLite is not a C-to-Rust transpilation. It references the C source only for behavioral specification. Every function is written in idiomatic Rust, using the type system and ownership model rather than translating C idioms.

### 2. MVCC at Page Granularity

Page-level versioning sits at the right point in the complexity/concurrency tradeoff:

- **Row-level** (PostgreSQL-style) would break the file format and require VACUUM
- **Table-level** would conflict on every write to a shared table
- **Page-level** maps naturally to SQLite's B-tree structure. Writers to different leaf pages can perform page-version work concurrently. Commit publication still coordinates shared metadata, and transactions can also retry because of SSI dependencies or structural B-tree overlap.

### 3. Safe Rust Engine Core

Most of the workspace inherits `unsafe_code = "forbid"` from the root Cargo workspace lints, so the engine, pager, parser, VDBE, and surrounding Rust crates stay in safe Rust. Two crates override this locally: `fsqlite-vfs` (mmap and shared-memory regions require raw pointers) and the optional `fsqlite-c-api` (FFI boundary for a SQLite-compatible C ABI). If you use FrankenSQLite through the Rust crates or the CLI, you never need the C ABI shim at all. The design goal is to keep unsafe surface minimal and the engine itself in safe Rust.

### 4. File Format Compatibility Is Non-Negotiable

Compatibility with existing SQLite databases is a core goal of the current runtime. FrankenSQLite is built around standard `.db` plus rollback-journal/WAL files, and a major part of the harness exists to drive byte- and behavior-level parity against C SQLite. The runtime admits databases whose header declares encoding 1 (UTF-8) or encodings 2/3 (UTF-16le/UTF-16be) for both read