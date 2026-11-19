# db-branch

Instant database branches for MySQL and PostgreSQL, on your own servers.

Test a migration, let an AI agent loose, or give every pull request its own copy of the database. db-branch creates a copy-on-write branch of a large database in seconds, with nothing copied. Break it, reset it, throw it away. Built on ZFS clones, self-hosted, Apache-2.0.

**Status: Beta.** db-branch is usable today, but APIs and command-line details may still change before 1.0. It is an independent open-source project, built from scratch.

![Create a branch, drop a table, reset the branch, delete it](docs/assets/demo.gif)

## Try it

1. **In your browser, 0 minutes.** A live console demo runs entirely in the page (nothing real is created): <https://demo.db-branch.com/>
2. **On a Mac or Windows machine, about 2 minutes.** db-branch needs Linux and ZFS, so run it in an Ubuntu VM with [Multipass](https://multipass.run/). One command makes the VM, installs db-branch, initialises it on a file-backed ZFS pool and loads a small sample base, `shop` (MySQL 8.4):

   ```sh
   multipass launch 24.04 --name db-branch-eval --memory 4G --disk 30G --timeout 900 \
     --cloud-init https://raw.githubusercontent.com/db-branch/db-branch/main/scripts/eval-cloud-init.yaml
   multipass exec db-branch-eval -- cloud-init status --wait    # wait for the setup (about two minutes)
   multipass exec db-branch-eval -- cat /etc/motd               # console URL and sign-in (admin / admin), or what failed
   multipass shell db-branch-eval                               # then: sudo db-branch branch create try --base shop --ttl 1h --record
   ```

   On Windows (PowerShell or cmd), put the `multipass launch` command on one line and drop the `\`:

   ```powershell
   multipass launch 24.04 --name db-branch-eval --memory 4G --disk 30G --timeout 900 --cloud-init https://raw.githubusercontent.com/db-branch/db-branch/main/scripts/eval-cloud-init.yaml
   ```

   - The history module is turned on, and the paid modules run for 30 days without a key. `--record` records a branch so it can be restored to any point.
   - The pool is a file, so it is slower and not meant for real data. The first admin password is `admin`; the console asks for a new one at the first sign-in.
   - On Apple Silicon (and other arm64 machines) the setup downloads about 800 MB for MySQL, against 80 MB on Intel, because Oracle ships no minimal build for arm64. `--timeout 900` keeps `launch` from giving up on a slow connection.
   - If the setup fails, `/etc/motd` says so, and `sudo tail -n 30 /var/log/cloud-init-output.log` in the VM shows why.
   - Delete the VM with `multipass delete --purge db-branch-eval`.
3. **On your own Ubuntu server.** See [Install](#install).

## Use cases

- **AI agent sandboxes.** The built-in MCP server lets an LLM agent create a branch, run a risky query or migration on it, and delete the branch, so production data is never touched.
- **A database per pull request.** Each CI run or PR gets its own copy of a large database, ready in seconds, and removed by `--ttl` when it is no longer needed.
- **Version-upgrade checks.** Run a major-version upgrade (for example MySQL 8.0 to 8.4) on one branch first, with `branch upgrade --check-only` to see what it would run into, before touching the base.

## What it does

- **Branches in seconds.** On our own 3-node test cluster a PostgreSQL branch is ready in about 0.5 s and a MySQL branch in about 3 s, with 0 bytes copied at creation (copy-on-write).
- **Reset and expire.** `branch reset` returns a branch to its creation state; `--ttl` deletes it automatically.
- **Checkpoints.** `branch checkpoint` saves a running branch's state instantly; `branch restore` puts it back. Restoring replaces the current state, and every checkpoint you already have stays restorable.
- **Per-branch upgrades.** `branch upgrade` moves one branch to a newer MySQL or PostgreSQL version while the base and the other branches stay put. A checkpoint is saved first, and a failed upgrade rolls back by itself.
- **MySQL and PostgreSQL, several versions at once.** Engine runtimes are installed by version and can live side by side.
- **One interface everywhere.** CLI, REST API, web console and an MCP server (so LLM agents can create and query their own branches) all use the same API.
- **Single node or cluster.** A Raft cluster of VMs, with optional ProxySQL routing so applications keep one address.

## Web Console

![The branches page of the web console](docs/assets/branch-home.png)
![The branch graph of the web console, showing which branch comes from which base](docs/assets/branch-graph.png)

## Install

Requirements: Ubuntu 24.04 LTS or 26.04 LTS, and a ZFS pool (the `zfsutils-linux` package is installed as a dependency).

```sh
curl -fsSL https://apt.db-branch.com/db-branch.gpg | sudo tee /usr/share/keyrings/db-branch.gpg >/dev/null
echo "deb [signed-by=/usr/share/keyrings/db-branch.gpg] https://apt.db-branch.com stable main" | sudo tee /etc/apt/sources.list.d/db-branch.list
sudo apt update && sudo apt install db-branch
sudo db-branch init --pool <zpool>
```

The repository signing key fingerprint is `3F404C4E5D49FA653F8385692C6E89E341D4D7A5`. `db-branch init` prints the initial admin password once.

## First branch

```sh
db-branch runtime install postgres@18.6                                     # a database engine version
db-branch base create prod --runtime postgres@18.6 --dump prod.sql.gz       # a base: your data, loaded once
db-branch branch create feature-x --base prod --ttl 72h                     # a branch: instant, copy-on-write
db-branch branch dsn feature-x                                              # connection URL (includes the password)
db-branch branch checkpoint feature-x --name before-migration               # save the state (instant)
db-branch branch restore feature-x before-migration                         # go back to the saved state
db-branch branch reset feature-x                                            # discard every change
db-branch branch delete feature-x                                           # remove it
```

MySQL works the same way, for example `mysql@8.4.13`. List installable versions with `db-branch runtime available`. To try a version upgrade on one MySQL branch:

```sh
db-branch branch upgrade feature-x --runtime mysql@8.4.13 --check-only      # what would the upgrade run into?
db-branch branch upgrade feature-x --runtime mysql@8.4.13                   # move this branch only; a checkpoint is saved first
```

## How it works

A base is a ZFS dataset holding a loaded database. A branch is a ZFS clone of a base snapshot, so creating one copies nothing, and each branch runs its own database server on its own port. Optionally, ProxySQL routes client connections to the right branch by user name (or by a `/*db_branch='name'*/` query comment). Several nodes form a Raft cluster that shares bases, branches, settings and users.

## Editions

- **Core (this repository), Apache-2.0:** branches, bases, runtimes, clustering, CLI, API, web console, MCP, monitoring, notifications, anonymous (no sign-in) branches with limits, scheduled base refresh, backup of cluster state.
- **Free modules** in the same apt repository: `proxysql`, `greenmask`, `greenmask-mysql`, `anon` (routing and data masking).
- **Paid modules** (auth/SSO, audit, history, diff, FSx storage) are separate, closed-source packages, self-hosted and enabled with a license key (monthly or yearly). A governed masking workflow is planned as an opt-in beta and is not part of any plan yet. See [docs/modules.md](docs/modules.md) for the extension points they use.

There is no hosted or cloud version of db-branch.

## Documentation

- [docs/README.md](docs/README.md): index of the design and reference documents (written in Japanese)
- English user documentation: <https://db-branch.com/docs/>
- Website: <https://db-branch.com> (English), <https://db-branch.com/ja/> (Japanese)
- [api/openapi.yaml](api/openapi.yaml): machine-readable REST API definition
- [CHANGELOG.md](CHANGELOG.md)

## Contributing, security, support

- Contributions are welcome: see [CONTRIBUTING.md](CONTRIBUTING.md). Commits need a DCO sign-off (`git commit -s`).
- Security issues: see [SECURITY.md](SECURITY.md). Please use private vulnerability reporting, not public issues.
- Support: see [SUPPORT.md](SUPPORT.md). No support is promised; Issues are read when possible.
- Please follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## License

Apache-2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE).

## 日本語

db-branch は、ZFS クローンで MySQL / PostgreSQL のデータベースブランチを発行・リセット・破棄するツールです。現在は Beta で、1.0 までに API が変わる可能性があります。コアは Apache-2.0 で、有償モジュール（認証/SSO・監査・履歴・差分・FSx ストレージ）は別パッケージ（クローズドソース、セルフホスト、ライセンスキー）です。

Mac / Windows では、Multipass のコマンド1つで試せます: <https://db-branch.com/ja/docs/getting-started/#multipass-ですぐ試す>。日本語のサイトは <https://db-branch.com/ja/>、設計ドキュメントは [docs/](docs/) にあります（日本語）。
