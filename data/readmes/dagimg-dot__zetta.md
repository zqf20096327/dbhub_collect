<div align="center">

<img src="assets/icon.svg" width="88" height="88" alt="">

<h1>zetta</h1>

<p><strong>A database explorer for Postgres and SQLite in one binary under 3 MB.</strong><br>
Browse and query in your browser, or run SQL from the shell.</p>

<p>
<a href="https://github.com/dagimg-dot/zetta/releases/latest"><img alt="Latest release" src="https://img.shields.io/github/v/release/dagimg-dot/zetta?style=flat-square&color=EA580C&label=release"></a>
<a href="https://github.com/dagimg-dot/zetta/releases"><img alt="GitHub downloads" src="https://img.shields.io/github/downloads/dagimg-dot/zetta/total?style=flat-square&logo=github&label=downloads&color=EA580C"></a>
<a href="https://hub.docker.com/r/workflowjd/zetta"><img alt="Docker pulls" src="https://img.shields.io/docker/pulls/workflowjd/zetta?style=flat-square&logo=docker&logoColor=white&label=docker%20pulls&color=EA580C"></a>
<a href="https://github.com/dagimg-dot/zetta/actions/workflows/ci.yml"><img alt="CI" src="https://img.shields.io/github/actions/workflow/status/dagimg-dot/zetta/ci.yml?branch=main&style=flat-square&label=ci"></a>
<a href="LICENSE"><img alt="MIT license" src="https://img.shields.io/badge/license-MIT-555?style=flat-square"></a>
</p>

<p>
<a href="https://tryzetta.netlify.app"><strong>Website</strong></a> ·
<a href="https://tryzetta.netlify.app/demo/"><strong>Live demo</strong></a> ·
<a href="#features">Features</a> ·
<a href="#install">Install</a> ·
<a href="#usage">Usage</a> ·
<a href="#docker">Docker</a> ·
<a href="#development">Development</a>
</p>

<img src="assets/screenshot-postgres.png" alt="zetta on Postgres: a filtered table, with the inspector following a foreign key" width="720">
<br><sub>Postgres: schemas, views and functions, a filtered and sorted table, and a foreign key followed in the inspector</sub>
<br><br>
<img src="assets/screenshot-sqlite.png" alt="zetta on SQLite: a query with its results and a formatted JSON value" width="720">
<br><sub>SQLite: a query in the SQL editor, its results, and a JSON value formatted in the inspector</sub>

</div>

## Features

| | |
|---|---|
| **Browse** | Every schema, table, view and function. A grid that pages through any table, with filters and sorting from a builder or your own `WHERE` and `ORDER BY`. |
| **Inspect** | Each row formatted, JSON included, with foreign keys you can follow. Each table's structure, indexes, triggers, DDL and relationships. |
| **Query** | A SQL editor with highlighting and completion. It runs the statement at the caret, the selection or the whole script, and asks before anything that destroys data. |
| **Share** | Every view lives in the URL. Copy cells and rows as CSV, TSV, JSON or Markdown, or save them as a file. |
| **Shell** | `zetta query` prints a table, CSV or JSON, and `zetta tables` lists what is there. Completions for bash, zsh and fish. |
| **Safe** | Listens on `127.0.0.1` with a fresh token each run, and refuses other hosts and origins. `--read-only` is enforced in the database adapter, not the UI. Passwords never reach a log. |
| **Small** | One binary with the UI embedded, its own Postgres client with TLS, and SQLite compiled in. No libpq, no OpenSSL. |

## Install

**Linux and macOS**

```sh
curl -fsSL https://raw.githubusercontent.com/dagimg-dot/zetta/main/install.sh | sh
```

The script picks the build for your system, checks it against the release's `SHA256SUMS` and installs `zetta` to `/usr/local/bin`, or `~/.local/bin` when that is not writable. Set `ZETTA_VERSION` to pin a release or `ZETTA_INSTALL_DIR` to choose the directory.

**Arch Linux**, from the `zetta-bin` PKGBUILD in this repository (with bash, zsh and fish completions):

```sh
git clone --depth 1 https://github.com/dagimg-dot/zetta
cd zetta/packaging/aur/zetta-bin && makepkg -si
```

**Manual download** from the [latest release](https://github.com/dagimg-dot/zetta/releases/latest):

| Platform | Archive |
|---|---|
| macOS, Apple Silicon | `zetta-<version>-macos-aarch64.tar.gz` |
| Linux, x86_64 | `zetta-<version>-linux-x86_64.tar.gz` |
| Linux, arm64 | `zetta-<version>-linux-aarch64.tar.gz` |
| Windows, x64 | `zetta-<version>-windows-x86_64.zip` |
| Windows, arm64 | `zetta-<version>-windows-aarch64.zip` |

On macOS, clear the download quarantine of a manual download once with `xattr -d com.apple.quarantine zetta`.

**Docker:** `docker pull workflowjd/zetta`, then see [Docker](#docker).

**From source** with Zig 0.16.0 and bun:

```sh
cd web && bun install && cd ..
zig build -Doptimize=ReleaseSafe    # the binary is zig-out/bin/zetta
```

## Usage

```sh
zetta ./app.db                                    # browse a SQLite file
zetta postgres://me@localhost/app --read-only     # browse Postgres without writes
zetta query app.db 'select * from users limit 5'  # print a result
zetta query postgres://me@localhost/app -f csv < report.sql > report.csv
zetta tables app.db                               # list schemas and tables
```

`zetta` prints a URL with a one-time token and opens it in your browser, on port 1993 or the next free one. A database is a `postgres://` URL, a Postgres keyword string (`host=... dbname=...`) or a SQLite file. Set `DATABASE_URL` instead of passing it to keep a password out of the process list. `zetta <command> --help` lists every option, and every flag also has an environment variable.

## Docker

```sh
export ZETTA_TOKEN=$(openssl rand -hex 16)

# Postgres
docker run --rm -p 127.0.0.1:1993:1993 -e ZETTA_TOKEN \
  -e DATABASE_URL=postgres://user:password@db:5432/app workflowjd/zetta

# A SQLite file in the current directory
docker run --rm -p 127.0.0.1:1993:1993 -e ZETTA_TOKEN \
  --user "$(id -u):$(id -g)" -v "$PWD:/data" workflowjd/zetta serve /data/app.db
```

Then open `http://localhost:1993/?token=$ZETTA_TOKEN`. Inside the container zetta listens on all interfaces, so it needs `ZETTA_TOKEN` (16 to 64 letters and digits). It serves plain HTTP, so keep the port on `127.0.0.1` unless a TLS proxy is in front. `--user` lets the container open a file you own.

The image is a static binary on `scratch` for amd64 and arm64, also published as `ghcr.io/dagimg-dot/zetta`. `latest` is the newest release and `edge` follows `main`.

### Docker Compose

Add zetta beside the database your project already runs:

```yaml
services:
  db:
    image: postgres:17
    environment:
      POSTGRES_PASSWORD: postgres

  zetta:
    image: workflowjd/zetta
    ports: ["127.0.0.1:1993:1993"]
    environment:
      ZETTA_TOKEN: ${ZETTA_TOKEN:?set ZETTA_TOKEN in .env}
      DATABASE_URL: postgres://postgres:postgres@db:5432/postgres
    depends_on: [db]
```

Put `ZETTA_TOKEN=` and the output of `openssl rand -hex 16` in `.env`, run `docker compose up`, and open the link `docker compose logs zetta` prints. In the image zetta keeps trying the database for 30 seconds while it starts, so it needs no health check; `ZETTA_WAIT` changes how long. Add `ZETTA_READ_ONLY: "true"` to browse a shared database without writes. For SQLite, mount the file's folder and pass `command: ["serve", "/data/app.db"]`, with `user:` set to your own uid and gid.

<details>
<summary><strong>Postgres support</strong></summary>

<br>

- URLs and keyword strings parsed as libpq does, `PG*` environment variables and `~/.pgpass`
- SCRAM-SHA-256, MD5, cleartext password and trust
- Every `sslmode` from `disable` to `verify-full`, with `sslrootcert=<file>` or the system store
- TCP, IPv6 and Unix sockets
- Not supported: channel binding, client certificates, Kerberos, multiple hosts and `COPY FROM STDIN`

`--read-only` opens SQLite read-only. On Postgres it runs each statement in a read-only transaction and refuses `DO` and `CALL`. For a hard guarantee, connect as a read-only role.

</details>

## Development

```sh
zig build check            # format check and full build
zig build test             # unit tests and the adapter suite
cd web && bun run check    # types, lint and UI tests
cd web && bun run dev      # UI dev server, proxies /api to zetta on port 1993
```

`ZETTA_TEST_PG_URL=postgres://... zig build test test-oracle -Dpg-oracle=true` also runs the suite on Postgres and compares it with libpq, and `dev/pg-matrix.sh` covers auth, TLS and sslmode against real servers in Docker.

zetta is in early development. Issues and pull requests are welcome.

## License

[MIT](LICENSE). The binary also carries SQLite (public domain), solid-js and Ark UI (MIT), and the Lexend and Source Code Pro fonts (SIL Open Font License 1.1).
