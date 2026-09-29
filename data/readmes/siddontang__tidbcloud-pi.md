# TiDB Cloud for Pi

A [Pi package](https://pi.dev/docs/latest/packages) that gives Pi explicit tools for [TiDB Cloud CLI (`ti`)](https://github.com/tidbcloud/ti-cli):

- `tidb_cloud_db` manages TiDB Cloud Starter clusters and branches, prepares SQL users, formats connection strings, and executes one SQL statement.
- `tidb_cloud_fs` manages TiDB Cloud Filesystems, files, mounts, layers, and filesystem tokens.
- `/tidb-cloud status` checks whether the `ti` binary is available.

The extension invokes `ti` with an argv array rather than a shell command. It blocks credentials in tool arguments, gates mutations and secret-bearing output, propagates cancellation and timeouts, and follows Pi's 50 KiB / 2,000-line output limit.

## Requirements

- Pi 0.84.2 or newer (Node.js 22.19 or newer)
- `ti` 0.2.3 or newer
- A configured TiDB Cloud profile, or the relevant `TI_*` / `TIDB_CLOUD_*` environment variables

Install `ti` on macOS or Linux:

```sh
curl -fsSL https://github.com/tidbcloud/ti-cli/releases/latest/download/install.sh | sh -s -- --yes
export PATH="$HOME/.ti/bin:$PATH"
ti configure
```

## Install the Pi package

From GitHub:

```sh
pi install git:github.com/siddontang/tidbcloud-pi
```

For local development:

```sh
npm install
pi install /absolute/path/to/tidbcloud-pi
```

Run `/tidb-cloud status` inside Pi to verify the integration.

If `ti` is not on `PATH`, set `TI_CLI_PATH` to the absolute binary path before starting Pi:

```sh
export TI_CLI_PATH="$HOME/.ti/bin/ti"
pi
```

## Usage

Ask Pi naturally, for example:

```text
List my Starter database clusters in aws-us-west-2.
Run SELECT CURRENT_TIMESTAMP using the read-only user on cluster <id>.
List files under /workspace in filesystem <id>.
Copy /workspace/report.json from TiDB Cloud Filesystem to stdout.
```

The tools accept a `command` plus a verbatim `args` array. The model can inspect any supported CLI command by selecting it and passing `args: ["--help"]` before constructing an operation.

State-changing commands require `confirm: true`; in interactive mode Pi also displays a confirmation dialog. A supported `--dry-run` bypasses the mutation gate. SQL execution is treated as state-changing unless `--read-only` is explicit—this plugin never guesses privilege from SQL text.

Commands that return a database connection string or one-time filesystem token require `reveal_secrets: true` and, in interactive mode, another visible confirmation. These values become part of Pi's session history. Prefer `execute-sql-statement` and `ti`'s local credential store when the raw credential is unnecessary.

Never pass these flags through either tool:

- `--fs-token`
- `--tidb-cloud-public-key`
- `--tidb-cloud-private-key`

The plugin rejects them because Pi persists tool arguments. Supply secrets through environment variables or `ti configure` instead.

## Database support

`tidb_cloud_db` supports the complete `ti db` workflow for TiDB Cloud Starter:

- Create, list, describe, update, and delete Starter clusters.
- Create, list, describe, and delete cluster branches.
- Prepare locally managed `read_only`, `read_write`, and `admin` SQL users.
- Execute exactly one SQL statement per tool call over HTTPS or MySQL transport.
- Generate MySQL, JDBC, Go SQL driver, SQLAlchemy, or dotenv connection strings.

TiDB Cloud Essential, Premium, and Dedicated clusters are not accepted by the current `ti db` implementation. Commands that create a cluster must explicitly use `--db-cluster-type starter`.

Ask Pi to provision a database and prepare SQL access:

```text
Create a Starter database cluster named agent-demo, wait until it is ACTIVE,
then prepare its SQL users. Use --dry-run first and show me the plan before
running the confirmed mutation.
```

For an existing cluster, use explicit database privileges:

```text
On cluster <cluster-id>, create database app with the admin role, create a
table using a separate SQL call, insert two rows with the read-write role,
then query them with the read-only role.
```

Each `execute-sql-statement` invocation accepts one SQL statement. Pi must use separate tool calls for `CREATE DATABASE`, `CREATE TABLE`, `INSERT`, and `SELECT`. The plugin never infers privilege from SQL text:

- `--read-only` queries do not require mutation confirmation.
- `--read-write` and `--admin` SQL require `confirm: true`.
- Control-plane mutations support `--dry-run` when the underlying `ti` command declares it.

Prefer `execute-sql-statement`, which keeps locally managed passwords out of the model context. If an application needs a raw connection string, ask Pi to run `format-db-connection-string` with `reveal_secrets: true`. The returned credential becomes part of Pi's session history and must be handled as a secret.

### Database and Filesystem workflow

Pi can orchestrate Filesystem data into TiDB without exposing credentials. There is no implicit server-side import: Pi reads the remote object, validates or transforms it, and sends an explicit SQL statement through `tidb_cloud_db`.

```text
Write a CSV locally, upload it to Filesystem <filesystem-id>, read it back,
create database import_demo and table imported_rows on Starter cluster
<cluster-id>, insert the validated CSV rows with the read-write role, and
query the final rows with the read-only role. Never print credentials or
tokens, and use only tidb_cloud_fs and tidb_cloud_db for cloud operations.
```

The reverse flow works the same way: query TiDB, write the returned rows to a local file, then upload that file with `tidb_cloud_fs copy-file`.

## Filesystem support

An existing Filesystem can be accessed without a full TiDB Cloud profile:

```sh
export TI_FS_TOKEN="<scoped-or-owner-token>"
export TI_REGION_CODE="aws-us-east-1"
pi
```

Use a path-scoped token with only the operations the agent needs. Before refreshing, disabling, or deleting a token used by a local mount, drain and unmount that Filesystem.

## Development

```sh
npm install
npm run check
npm pack --dry-run
pi -e ./extensions/tidb-cloud.ts
```

`npm run check` runs strict TypeScript checking, unit tests, and a smoke test that loads both tools and executes real `ti db <command> --help` and `ti fs <command> --help` paths without cloud credentials or mutations.

## Security model

Pi packages execute with the permissions of the user who starts Pi. Review package source before installation. This extension narrows command construction and adds safety gates, but `ti` still has access to the configured TiDB Cloud account and local filesystem. Use least-privilege API keys, scoped Filesystem tokens, `--read-only`, and `--dry-run` where possible.
