# Forkget

English · [简体中文](README.zh-CN.md)

Disposable database workspaces for applications and agents.

![Forkget comic: fork, test, diff, discard](doc/assets/intro-comic.svg)

Forkget creates isolated branches from a pinned snapshot of MySQL,
PostgreSQL or MongoDB. Connect through an admitted native client,
inspect typed changes, save a complete result and replay it against its retained
baseline. Branches have explicit permissions, row budgets and expiry.

Choose a version from [GitHub Releases](https://github.com/pterchan/ForkGet/releases)
and read its qualification status and known limitations. Use prereleases with
disposable, non-production data. The release page lists the source, Linux x86_64
binaries, Console and checksums available for that tag.

TiDB is outside the v0.1.1 release scope because of the unresolved concurrent
foreign-key integrity issue. See [known limitations](doc/limitations.md).

## Get started

1. [Build and run a local deployment](doc/install.md).
2. [Capture data, run an application and save its result](doc/workflow.md).
3. [Connect with a native client or SQLAlchemy](doc/connecting.md), or open the
   [Web Console](doc/console.md).
4. Read the [supported subset](doc/support-matrix.md), [limits](doc/limitations.md)
   and [security guide](doc/security.md) before choosing a workload.

```sh
forkget fork review-task --write
forkget status --id 42
# Wait until the branch is active, then connect and run your workload.
forkget diff --id 42 --output changes.json
forkget drop --id 42
```

Replace `42` with the immutable branch ID returned by `forkget fork`.

Omitting `--write` creates a read-only branch. Writable SQL branches materialize
native copies; their provisioning time and space grow with the snapshot.
MongoDB requires a separate client pool per branch. An exported result is not a
full backup and is never automatically merged into a production source.

A deployment has one proxy, a control service, metadata PostgreSQL and one
separately configured native serving engine. Keep the source database separate
from the serving database. The packaged Console shares the loopback control
origin; remote operators use an authenticated SSH tunnel. Database connections
verify TLS on both data hops.

## Operate and recover

- [Owner and operator commands](doc/cli.md)
- [Deployment settings and native roles](deploy/README.md)
- [Source backup accounts](doc/source-backup-roles.md)
- [Result retention and recovery](doc/recovery.md)
- [Audit delivery, coordinated upgrades and storage restore](doc/audit-recovery.md)
- [Storage and permission model](doc/architecture.md)

## Contribute

See [CONTRIBUTING.md](CONTRIBUTING.md) for a source build and focused checks.
The [changelog](CHANGELOG.md) records user-visible changes. Forkget uses the
[MIT license](LICENSE); dependencies and bundled tools retain their licenses.

## Support

[Donate with PayPal](https://www.paypal.com/ncp/payment/E22SDNFKMNVJ6).
100% of donations will be used to support the development of Forkget and Shift.
