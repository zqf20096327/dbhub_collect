# SqlBranch

**Writable, full-size SQL Server database branches in seconds, for development, tests and AI agents.**

[![NuGet](https://img.shields.io/nuget/v/SqlBranch.svg?label=SqlBranch)](https://www.nuget.org/packages/SqlBranch)
[![NuGet](https://img.shields.io/nuget/v/SqlBranch.Testing.svg?label=SqlBranch.Testing)](https://www.nuget.org/packages/SqlBranch.Testing)
[![.NET 10](https://img.shields.io/badge/.NET-10-512BD4)](https://dotnet.microsoft.com/download/dotnet/10.0)
[![CI](https://github.com/vuglll/SqlBranch/actions/workflows/ci.yml/badge.svg?branch=dev)](https://github.com/vuglll/SqlBranch/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

Restore your production-sized backup **once**. Then give every developer, every pull request, every test and every AI agent its own writable copy of it in about two seconds, using almost no extra disk.

> **50 GB database → new writable branch in ~0.4 s** (clone) / ~2.5 s end-to-end `branch create`, on x86-64 Linux.
> This assumes the image already exists. Building the image is a one-time full restore that takes minutes or more (see [Building an image](#building-an-image)).

![SqlBranch demo: init, a 50.78 GiB image, then a branch created in about 3.5 s, listed with 288 KiB of own data, connected and removed](https://raw.githubusercontent.com/vuglll/SqlBranch/dev/docs/demo.gif)

<sub>Replay of a recorded session on x86-64 Linux with a 50.78 GiB StackOverflow2013 image. `branch create` runs at its real speed; `init` and the one-time `image build` are sped up, with their real durations shown.</sub>

## How it works in 30 seconds

1. **One full copy per machine.** On a developer laptop, a CI runner or a
   test server, restore a backup **once** into an *image*. Run your masking
   scripts before the image is sealed, so no branch ever sees real personal
   data.
2. **Branches share that copy.** A branch is a copy-on-write clone of the
   image's files (XFS reflink): it shares the image's blocks on disk, so
   creating one copies only metadata. A block is copied only when the branch
   writes to it. That is why a branch of a 50 GB database takes about 0.4 s
   and about 300 KB, whatever the size.
3. **One engine, many databases.** Each branch is attached as its own
   database on one SQL Server Developer container that SqlBranch manages.

SqlBranch never connects to your production server or its replicas: it works
from a backup file you already have. Timings are measured up to 50 GB.

> **Status: 0.2, early release.** Branching, images from backups and scripts,
> and the `SqlBranch.Testing` package are released. Cloud backup URLs, image
> export and import, and BACPAC builds are included as **preview**: they are
> not yet verified against real cloud accounts. The plan is in
> [docs/roadmap.md](docs/roadmap.md).

> ⚠️ **Development and testing only. Never use SqlBranch for production data.**
> It runs SQL Server Developer edition, which is not licensed for production
> use. The engine's `sa` password is stored in a file in the pool, and the
> engine listens on `127.0.0.1` only.

## Why

- **Stop sharing one dev database.** Everyone gets their own, with real data volume and real query plans.
- **Real integration tests.** Each test gets a private, full-size database: no mocks, no tiny seed scripts, no cleanup code.
- **Safe playground for AI agents.** Let an agent run migrations and destructive queries on a branch; throw it away or `reset` it.
- **Reproduce production issues** against production-sized data without touching production.

### Test migrations on real data

A migration that passes on an empty database or a 20-row seed can still fail
in production:

- adding a `NOT NULL` column fails because old rows hold NULLs,
- a new unique index fails because the data already has duplicates,
- a column change rewrites a 50-million-row table and holds a lock for 40 minutes.

You only see that on real data. Give each pull request a branch of last
night's production image (masked with `--post-script`) and run the migration
there in CI:

```sh
sqlbranch branch create pr-142 --from prod-masked --ephemeral --ttl 2h   # a full copy, in seconds
dotnet ef database update --connection "$(sqlbranch branch conn pr-142 --quiet)"
sqlbranch branch rm pr-142
```

### SqlBranch vs Testcontainers

They solve different problems, and they work well together.

| | [Testcontainers](https://dotnet.testcontainers.org/) | SqlBranch |
|---|---|---|
| What a test gets | A new SQL Server container, usually per test class or run, with an empty database | A branch of a prebuilt image on one long-running engine |
| Schema and data | You create them in every run (migrations, seed scripts) | Built once into the image: a backup, SQL scripts or a BACPAC |
| Cost of a 50 GB database | A restore in every run | One restore; each branch then takes seconds and almost no disk |
| Best for | Small schemas, empty or small seeded databases | Realistic data volume and query plans, slow migrations or seed |

Neon and Databricks Lakebase offer branching for Postgres as cloud services;
SqlBranch brings the same idea to SQL Server, on your own machines.

If an empty database plus EF migrations and a small seed is all your tests
need, Testcontainers is a fine choice. When the migrations get slow or the
tests need real data, build the image once:

```sh
dotnet ef migrations script --idempotent -o db/001_schema.sql
sqlbranch image build app --from-scripts db
```

and each test starts from that schema without running the migrations again.

## Requirements

SqlBranch runs SQL Server in a **Docker** container that it creates and manages. Besides the .NET tool, everything it makes lives in Docker and in its storage pool.

- **Docker**: Docker Engine on Linux, or Docker Desktop or Colima on macOS. The Docker daemon must be running, and your user must be able to run `docker` commands.
- **.NET 10 SDK** to install the tool and use `SqlBranch.Testing`.
- **Disk space** for the image, roughly the size of your restored database, plus room for the backup while the image builds. Thin branches add almost nothing on top of that.

Run `sqlbranch doctor` to check your setup.

## Quick start

```sh
dotnet tool install --global SqlBranch

sqlbranch init                                       # set up the pool and engine
sqlbranch image build prod-masked --from-bak ./prod.bak --post-script mask.sql   # slow, one-time: restore, then mask
sqlbranch branch create feature-123 --from prod-masked                         # fast: seconds, every time after that
sqlbranch branch conn feature-123                    # prints the connection string
```

Done with it? `sqlbranch branch reset feature-123` to start over, or `sqlbranch branch rm feature-123`.

`mask.sql` is your own script that overwrites personal data (emails, names,
phone numbers) before the image is sealed; see
[Building and masking with SQL scripts](docs/images.md#building-and-masking-with-sql-scripts).
Leave out `--post-script` only when the backup holds no personal data.

The backup must be a full, single-file backup made by a SQL Server no newer
than the engine's. `init` can take a minute the first time, because it pulls
the SQL Server image. The pool SqlBranch creates is 60 GB by default; for a
bigger database set `SQLBRANCH_POOL_SIZE` before `init`: the backup sits in
the pool while the image is built, so a 50 GB database built from a 15 GB
backup needs about `80GB`. To run from a checkout instead of the tool, use
`dotnet run --project src/SqlBranch.Cli --` where the commands say `sqlbranch`.

`sqlbranch branch list` shows every branch and how much data it has changed.
`branch conn` is the only command whose output contains the engine password:
do not paste it into a log or a chat. Every command takes `--format json` and
returns stable exit codes (0 success, 1 failed, 2 usage or configuration
error, 3 environment not ready); see [docs/cli-output.md](docs/cli-output.md).

Commands in detail: [docs/engine.md](docs/engine.md) (`init`, `status`,
`doctor`, `engine start|stop`, `teardown`), [docs/images.md](docs/images.md),
[docs/branches.md](docs/branches.md) and
[docs/configuration.md](docs/configuration.md) (flags, `SQLBRANCH_*` variables,
`.sqlbranch.yml`).

## Building an image

There are two costs to understand:

| Step | How often | Time |
|---|---|---|
| `image build` | Once per backup (for example weekly) | About as long as a normal `RESTORE DATABASE` of that backup, plus a short seal step |
| `branch create` | Every developer, pull request, test or agent | Seconds, regardless of database size |

`image build` is a full SQL Server restore, and you pay that cost once. After that, every branch is a clone of the image's files with no restore. How long the build takes depends on:

- **Backup size.** A compressed backup expands to its full data size on restore.
- **Disk throughput** of the pool, which is usually the limiting factor.
- **Where the backup lives.** A local `.bak` is fastest. A backup from a cloud URL (preview) is read from storage during the restore.
- **CPU and memory** given to Docker, especially on Docker Desktop for macOS.

For reference: a 14.8 GB compressed backup (StackOverflow2013) built a 50.8 GB image in about 2 minutes on an 8-vCPU x86-64 Linux server with local disk ([docs/research/2026-11-20-x86-64-release-gate-run.md](docs/research/2026-11-20-x86-64-release-gate-run.md)).

Tips:

- **Build images on a schedule, outside working hours** (nightly or weekly), and give them dated names like `prod-masked-2026-11-16`, so nobody waits on a restore.
- **Old images stay usable while a new one builds.** Existing branches aren't affected.
- **In CI, don't build the image on every run.** Build it once on a long-lived runner, or use image export and import (preview), and only run `branch create` per job.

Images can also be built from SQL scripts (`--from-scripts`) and from a BACPAC (`--from-bacpac`, preview); see [docs/images.md](docs/images.md).

## Use it in tests

```sh
dotnet add package SqlBranch.Testing
```

Your test machine or CI runner needs Docker and the `sqlbranch` tool to build the image once. GitHub Actions `ubuntu-latest` runners already have Docker. Build an image (for example `sqlbranch image build shop --from-scripts db`), and give each test its own private database with one line:

```csharp
[Fact]
public async Task ConnectionOpensThePrivateDatabase()
{
    await using var db = await SqlBranchDatabase.CreateAsync("shop");
    await using var connection = new SqlConnection(db.ConnectionString);
    await connection.OpenAsync();
    Assert.Equal(db.Name, connection.Database);
}
```

The snippet needs `using SqlBranch.Testing;` and `using Microsoft.Data.SqlClient;`.

The branch is dropped when the test disposes it. The connection string contains
the engine password, so keep it out of test output. NUnit, MSTest and parallel
tests are covered in [docs/testing.md](docs/testing.md); runnable projects are
under `samples/`.

## Concepts

| Term | Meaning |
|---|---|
| **Pool** | Storage that can clone files without copying them: a directory on a reflink file system, or an XFS file that SqlBranch creates and mounts itself |
| **Engine** | One SQL Server Developer container that SqlBranch creates and owns, with the pool mounted at `/pool` |
| **Image** | A sealed, read-only set of database files, built once from a full backup |
| **Branch** | A writable database whose files are clones of an image, so changes never reach the image or another branch |

## Thin mode and copy mode

Every command that creates files reports the clone mode of the pool:

- **thin.** The pool can share blocks. A branch is a set of clones of the
  image's files and costs almost no disk until it writes. Creating one does not
  depend on the database's size. On Linux without a reflink directory, and on
  Docker Desktop for macOS, `init` creates an XFS file and mounts it itself,
  which needs permission to run a privileged helper container.
- **copy.** The pool cannot share blocks, so every branch is a full copy of the
  image and takes as long and as much disk as the copy does. `init` falls back
  to this when it cannot make a thin pool, says why, and exits 0. Set
  `requireThin: true` to refuse copies later: in copy mode, `branch create`
  without `--copy` and `branch reset` then exit 3 with `thin_required`
  before creating any file.

`sqlbranch branch create <name> --copy` makes a full copy even on a thin pool.
Use it for benchmarks (see below).

## The first-write cost (gate G2)

A thin branch shares blocks with its image. By default XFS unshares 128 KiB
around every written 8 KiB page, and SqlBranch sets a smaller copy-on-write
hint on the branches folder to roughly halve that. Measured on x86-64 Linux
(gate G2 of the spike, see
[docs/research/spike-results.md](docs/research/spike-results.md)): updating
every tenth row of a large table on a branch of a 50 GB image took about 5
times as long as on a full copy (about 4.5 times with the smaller hint), and
unshared 12 to 28 GB. A second pass of the same updates was just as slow,
because the branch's files were left in millions of pieces. Inserts cost the
same on a branch as on a copy. That run used a pool file on another file
system; on a dedicated XFS disk the cost may be lower.

So:

- Thin branches are for development, tests and CI, where a branch lives
  minutes to days and is reset often. A reset gives a fresh, unfragmented
  clone.
- For sustained write-heavy work and for benchmarks, create the branch with
  `--copy`. The setup is in the benchmark section of
  [docs/branches.md](docs/branches.md).
- `sqlbranch branch list` shows each branch's own changed data, so a branch that
  has drifted far from its image is visible.

## Benchmark of branch creation

`tools/bench/clone-bench.sh <image> [count] [prefix]` creates five branches
(or `count`) from an existing image, prints how long each took and how much the
pool grew, and removes only the branches it made. It runs the `sqlbranch` on
your PATH, or the command in the `SQLBRANCH` variable. Point that at the built
binary, not `dotnet run`, which adds build-check and startup time to every
create and skews the numbers:

```sh
tools/bench/clone-bench.sh shop
SQLBRANCH="dotnet src/SqlBranch.Cli/bin/Release/net10.0/sqlbranch.dll" tools/bench/clone-bench.sh shop 10 try
```

## Tear it all down

```sh
sqlbranch teardown --force
```

removes everything SqlBranch created: every database on the engine (branches
and any database you made there), the engine container, the pool folders, and
the managed pool file or the `sqlbranch-pool` volume. Without `--force` it
removes nothing and exits 2. It lists what it removed and what is left; if a
step fails, run it again. On a directory pool it deletes only SqlBranch's own
folders and the pool marker, and leaves other files in the directory alone.
Backups you kept in the pool's `import` folder are deleted too. See
[docs/engine.md](docs/engine.md).

## Limits

- **Full backups only,** in one file, without FILESTREAM or memory-optimized
  filegroups. A differential, log or striped backup is refused. The engine must
  be at least as new as the backup.
- **Development editions only.** `developer` by default; `standard-developer`
  and `enterprise-developer` (SQL Server 2025 and later) to match production's
  feature set.
- **One engine, one host, one user.** The pool's size is fixed when it is
  created (60 GB by default, `poolSize`) and cannot be resized in 0.1. A copy
  branch needs the image's full size free in the pool.
- **The engine image, edition, port and pool are fixed at the first `init`.**
  Changing them means `teardown --force` and a new `init`.
- **Crash debris is not cleaned up automatically.** `status` lists it. A branch
  made by a client that was killed is repaired with `branch reset` or removed
  with `branch rm`.
- **Windows without Docker and branch snapshots** are not part of 0.2 yet; see the
  [roadmap](docs/roadmap.md).
- A container has none of the resource limits of a managed service, so for
  Azure SQL Database trust only relative benchmark results.

## Platform support

| Platform | Status |
|---|---|
| Linux x86-64 with Docker | ✅ Supported. The SQL Server container image supports x86-64 Linux hosts only |
| macOS (Docker Desktop or Colima) | ✅ Works through the managed pool. On Apple Silicon the engine runs under emulation, which is slower and less reliable, and `init` warns about it |
| Windows (Docker Desktop / WSL2) | 🧪 Not verified yet; help wanted. The check is prepared in [docs/research/windows-check.md](docs/research/windows-check.md). If the managed pool cannot be mounted, `init` falls back to copy mode and says so |

On x86-64 Linux a 50 GB image branches in about 0.4 s, and
`sqlbranch branch create` takes 2.1 to 2.5 s
([docs/research/spike-results.md](docs/research/spike-results.md)).

## Contributing

Contributions are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) first:
every contributor signs the project's Contributor License Agreement before a
pull request can be merged. Report security issues privately as described in
[SECURITY.md](SECURITY.md).

## License

Apache-2.0. See [LICENSE](LICENSE).
