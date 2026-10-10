
# Altinity Backup for ClickHouse®

[![Build](https://github.com/Altinity/clickhouse-backup/actions/workflows/build.yaml/badge.svg?branch=master)](https://github.com/Altinity/clickhouse-backup/actions/workflows/build.yaml)
[![GoDoc](https://godoc.org/github.com/Altinity/clickhouse-backup?status.svg)](http://godoc.org/github.com/Altinity/clickhouse-backup)
[![Telegram](https://img.shields.io/badge/telegram-join%20chat-3796cd.svg)](https://t.me/clickhousebackup)
[![Docker Image](https://img.shields.io/docker/pulls/altinity/clickhouse-backup.svg)](https://hub.docker.com/r/altinity/clickhouse-backup)
[![Downloads](https://img.shields.io/github/downloads/Altinity/clickhouse-backup/total.svg)](http://github.com/Altinity/clickhouse-backup/releases)
[![Coverage Status](https://coveralls.io/repos/github/Altinity/clickhouse-backup/badge.svg)](https://coveralls.io/github/Altinity/clickhouse-backup)
<a href="https://altinity.com/slack">
  <img src="https://img.shields.io/static/v1?logo=slack&logoColor=959DA5&label=Slack&labelColor=333a41&message=join%20conversation&color=3AC358" alt="AltinityDB Slack" />
</a>

A tool for easy backup and restore utility for ClickHouse databases with support for many cloud and non-cloud storage types.

### Don't run `clickhouse-backup` remotely
During backup and restore data, `clickhouse-backup` requires access to the same files as `clickhouse-server` in `/var/lib/clickhouse` folders.
For that reason, it's required to run `clickhouse-backup` on the same host or same Kubernetes Pod or the neighbor container on the same host where `clickhouse-server` ran.
**WARNING** You can backup and restore only schema when connect to remote `clickhouse-server` hosts.

## Features

- Easy creating and restoring backups of all or specific tables
- Efficient storing of multiple backups on the file system
- Uploading and downloading with streaming compression
- Works with AWS, GCS, Azure, Tencent COS, FTP, SFTP
- **Support for Atomic Database Engine**
- **Support for Replicated Database Engine**
- **Support for multi disks installations**
- **Support for custom remote storage types via `rclone`, `kopia`, `restic`, `rsync` etc**
- **Support for incremental backups on remote storage**
- **Support for custom SQL disks declared as `SETTINGS disk = disk(...)`** (ClickHouse 23.2+, tested from 24.8)

## Limitations

- ClickHouse above 1.1.54394 is supported
- Only MergeTree family tables engines (more table types for `clickhouse-server` 22.7+ and `USE_EMBEDDED_BACKUP_RESTORE=true`)

## Community

Altinity Backup for ClickHouse is a community effort sponsored by Altinity. The best way to reach us or ask questions is:

* Join the [Altinity Slack](https://altinity.com/slack) - Chat with the developers and other users
* Log an [issue on GitHub](https://github.com/Altinity/clickhouse-backup/issues) - Ask questions, log bugs and feature requests

## Support 

Altinity is the primary maintainer of clickhouse-backup. We offer a range of software and 
services related to ClickHouse. 

- [Official website](https://altinity.com/) - Get a high level overview of Altinity and our offerings.
- [Altinity.Cloud](https://altinity.com/cloud-database/) - Run ClickHouse in our cloud or yours.
- [Altinity Support](https://altinity.com/support/) - Get Enterprise-class support for ClickHouse.
- [Slack](https://altinity.com/slack) - Talk directly with ClickHouse users and Altinity devs.
- [Contact us](https://hubs.la/Q020sH3Z0) - Contact Altinity with your questions or issues.
- [Free consultation](https://hubs.la/Q020sHkv0) - Get a free consultation with a ClickHouse expert today.

## Installation

Download the latest binary from the [releases](https://github.com/Altinity/clickhouse-backup/releases) page and decompress with:

```shell
tar -zxvf clickhouse-backup.tar.gz
```

Use the official tiny Docker image and run it on a host with `clickhouse-server` installed:

```shell
docker run -u $(id -u clickhouse) --rm -it --network host -v "/var/lib/clickhouse:/

[...截断...]

var/lib/clickhouse" \
   -e CLICKHOUSE_PASSWORD="password" \
   -e S3_BUCKET="clickhouse-backup" \
   -e S3_ACCESS_KEY="access_key" \
   -e S3_SECRET_KEY="secret" \
   altinity/clickhouse-backup --help
```

Build from the sources (required go 1.21+):

```shell
GO111MODULE=on go install github.com/Altinity/clickhouse-backup/v2/cmd/clickhouse-backup@latest
```

## Brief description of how clickhouse-backup works

Data files are immutable in the `clickhouse-server`.
During a backup operation, `clickhouse-backup` creates file system hard links to existing `clickhouse-server` data parts via executing the `ALTER TABLE ... FREEZE` query.
During the restore operation, `clickhouse-backup` copies the hard links to the `detached` folder and executes the `ALTER TABLE ... ATTACH PART` query for each data part and each table in the backup.
A more detailed description is available here: https://www.youtube.com/watch?v=megsNh9Q-dw

## Signal handling

One-shot CLI commands (`create`, `upload`, `download`, `restore`, `delete`, `create_remote`, `restore_remote`, `watch`, ...):
- the first `SIGINT` (Ctrl+C) or `SIGTERM` cancels the running command: it unwinds, removes the shadow directories it froze (`FREEZE ... WITH NAME <uuid>`) and exits with a non-zero code; a `create` interrupted this way keeps its incomplete local backup directory, `clean_local_broken` or `backups_to_keep_local` retention removes it
- the second `SIGINT`/`SIGTERM` exits immediately without waiting for the cleanup to finish
- `SIGKILL` (including OOM kill and pod eviction) can't be handled, the frozen shadow of the table processed at that moment stays behind; every `FREEZE` is recorded in `<backup_name>/freezes.tmp` before it is executed, so the next `clean`, `delete local`, `clean_local_broken` or retention run unfreezes it, see `clean` for details

`server` mode:
- `SIGTERM` cancels all running commands (same as `POST /backup/kill` for each of them), removes their pid files and stops the API server; in Kubernetes make sure `terminationGracePeriodSeconds` covers the shadow cleanup of a big table, otherwise the following `SIGKILL` leaves it for the next `clean`
- `SIGHUP` reloads the config and restarts the API server, running commands are canceled the same way as via `POST /restart`

## Logging

All log messages go to stderr. stdout only carries the command output (`list`, `tables`, `print-config`, ...), so it can be piped to other tools, e.g. `clickhouse-backup list remote --format json | jq`.
To keep the log in a file, redirect stderr as well:

```shell
clickhouse-backup create_remote my_backup >> clickhouse-backup.log 2>&1
```

`docker logs` and `kubectl logs` show only the output of the container's main process, e.g. `clickhouse-backup server` in a sidecar container.
A command started with `docker exec` or `kubectl exec` writes its log to the exec session, so it doesn't appear in the container log.
To get it there, run the command through the [API](#api), e.g. `POST /backup/create_remote` or `INSERT INTO system.backup_actions`: the server executes it in its own process.

Use `log_level` / `LOG_LEVEL` to change the verbosity.

## Default Config File

By default, the config file is located at `/etc/clickhouse-backup/config.yml`, but it can be redefined via the `CLICKHOUSE_BACKUP_CONFIG` environment variable or via `--config` command line parameter.
All options can be overwritten via environment variables.
Use `clickhouse-backup default-config` to print the default config.

## Configurable Parameters

Use `clickhouse-backup print-config` to print the current config.
Environment variables can override each config parameter defined in the config file. Their names should be UPPERCASE, and exact names are provided after the comment character `#.`
The following values are not defaults; they explain what each config parameter with an example.

```yaml
general:
  remote_storage: none           # REMOTE_STORAGE, choice from: `azblob`,`gcs`,`s3`, etc; if `none` then `upload` and `