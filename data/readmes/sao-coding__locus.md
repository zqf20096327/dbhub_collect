<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset=".github/assets/logo-dark.svg">
    <img src=".github/assets/logo.svg" alt="Locus" width="360">
  </picture>
</p>

<p align="center">
  <a href="../../releases"><img alt="Release" src="https://img.shields.io/github/v/release/sao-coding/locus?include_prereleases"></a>
  <a href="../../actions/workflows/ci.yml"><img alt="CI" src="https://img.shields.io/github/actions/workflow/status/sao-coding/locus/ci.yml?branch=main&label=CI"></a>
  <img alt="Windows 10 and 11" src="https://img.shields.io/badge/Windows-10%20%7C%2011-0078D4">
  <a href="LICENSE"><img alt="License: AGPL-3.0" src="https://img.shields.io/badge/license-AGPL--3.0-blue"></a>
</p>

<p align="center"><b>English</b> · <a href="README.zh-CN.md">简体中文</a> · <a href="README.zh-TW.md">繁體中文</a></p>

# Locus

A database client for Windows that stays smooth. GPU-rendered, written in Rust, one small exe.

Locus talks to MySQL / MariaDB, PostgreSQL, SQLite, Redis, Oracle and SQL Server. Results stream into the
grid while the query is still running, and cancelling really stops the query on the server.

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset=".github/assets/screenshots/hero-dark.png">
    <img src=".github/assets/screenshots/hero-light.png" alt="Locus running a query over 300,000 rows" width="900">
  </picture>
</p>

<table>
  <tr>
    <td width="50%">
      <picture>
        <source media="(prefers-color-scheme: dark)" srcset=".github/assets/screenshots/prod-dark.png">
        <img src=".github/assets/screenshots/prod-light.png" alt="A Production connection blocks a write until it is unlocked">
      </picture>
    </td>
    <td width="50%">
      <picture>
        <source media="(prefers-color-scheme: dark)" srcset=".github/assets/screenshots/split-dark.png">
        <img src=".github/assets/screenshots/split-light.png" alt="Two query panes side by side">
      </picture>
    </td>
  </tr>
</table>

## Why Locus

- **It does not freeze.** Big results stream into a virtualized grid. A slow query or a huge
  table does not block typing, scrolling or switching tabs.
- **It is careful with production.** A connection marked Production is read-only by default.
  Writes need a timed unlock, every writing statement asks for its own confirmation, and each
  one lands in an audit log. The gate classifies the statement text; functions called by a `SELECT` are not checked for side effects, except known built-ins (`nextval`, `pg_terminate_backend`, `GET_LOCK` ...).
- **It stays out of your way.** One window, vertical tabs, split panes, and a command palette
  for everything else.

## Features

**Workspace**
- Spaces: group connections and tabs, each with its own color
- Vertical tabs; split the work area into up to 4 panes (`Ctrl+Shift+M` zooms one temporarily)
- Command palette (`Ctrl+K`), query history, light / dark / system theme, English, 简体中文 and 繁體中文

**Connections**
- MySQL / MariaDB, PostgreSQL, SQLite and Redis connect directly from Rust; Oracle and SQL Server go through
  a small Go helper (`sidecar.exe`, built into `locus.exe`)
- SSH tunnels; passwords are stored in the Windows Credential Manager
- Production protection: read-only by default, timed unlock, audit log

**Query**
- SQL editor with syntax highlighting, find / replace, formatting, completion, and JOIN
  suggestions taken from foreign keys
- Query parameters, saved queries and snippets
- Auto-commit or manual transactions with Commit / Rollback
- Execution plans

**Results**
- Streaming grid, server-side cancel, filters, selection statistics
- Follow a foreign key to the referenced row
- Edit cells in place; changes are applied inside a transaction
- Value viewer: text, JSON tree, hex, image

**Objects**
- Object tree with paging and server-side search
- Table structure tab, relationship diagram
- Source and compile for stored procedures, functions, triggers and Oracle packages

**Import and export**
- Import CSV and Excel
- Export CSV, xlsx, JSON, SQL INSERT, Markdown and HTML, including streaming the full result
  from the server

**Administration**
- Server activity: sessions, kill a query, server variables
- Redis: key browser, a viewer for each value type, command window

## Performance

<p align="center">
  <img src=".github/assets/compare-load.gif" alt="Locus (left) and DBeaver (right) loading 1,000,000 rows" width="900">
</p>

Loading a 1,000,000-row, 12-column table with `SELECT *`, Locus on the left, DBeaver 26.0.5 on the
right. Locus shows rows while they are still arriving and lets you stop the query; the GIF is
real time.

| | Locus | DBeaver |
|---|---|---|
| Load time, 1,000,000 rows | 1.5 to 1.7 s (3 runs) | 2.9 s (1 run; a second run failed with a driver error) |
| Memory when idle | about 100 MB | about 340 MB |
| Memory right after the load | about 360 MB | about 1.3 GB (peak 1.4 GB) |
| Memory after closing the result | about 107 MB, within seconds | about 1.37 GB, not released |

How it was measured: Intel Core i5-14400F, 15.8 GB RAM, Windows 11, MariaDB 11.8.5 on the same
machine over 127.0.0.1, no TLS. Locus is the release build with the per-tab row limit off (a separate 1,000,000-row memory cap, set in Settings, still applies; this table has exactly that many rows). DBeaver uses its
default 1 GB heap with the fetch size raised to 1,000,000 (its default is 200), so it loads
everything at once. Memory is the process's private memory sampled about once a second. The
two programs were measured in separate sessions, and DBeaver only once, so read the DBeaver
column as one observation, not a benchmark. Locus is not always faster: on a 100,000-row
result both were done in under a second.

## Install

Download from [Releases](../../releases) and either run the installer
`locus-<version>-windows-x64-setup.exe` (per user, no admin, with a Start menu entry and an
uninstaller) or run the portable `locus-<version>-windows-x64.exe`, one file with nothing to
install. Oracle and SQL Server support is built in, no extra file needed: the first Oracle or SQL Server
connection unpacks a small helper into `%LOCALAPPDATA%\Locus\sidecar\`.

The builds are not code-signed, so SmartScreen may warn the first time. To check a download:

```powershell
# compare with the .sha256 file on the release page
Get-FileHash .\locus-<version>-windows-x64.exe -Algorithm SHA256

# build provenance, with the GitHub CLI
gh attestation verify .\locus-<version>-windows-x64.exe --repo sao-coding/locus

# minisign signature (the key is also in minisign.pub)
minisign -Vm .\locus-<version>-windows-x64.exe -P RWRDNREpYa8EZ59rUGsAnTVNIMjNfUWhciyq6SgS2MpNZvMGj0yVAZ0s
```

Settings, saved connections and history live in `%APPDATA%\Locus`. Delete the folder to reset. The
Oracle helper is the only file outside it (`%LOCALAPPDATA%\Locus\sidecar\`); delete that folder too
to remove everything.

About once a day Locus asks GitHub whether a newer release exists (only `User-Agent: Locus/<version>`
is sent) and shows it in the status bar. A new version is downloaded in the background and installed
only when you pick Restart and update; it is installed only if its minisign signature is from the
key in `minisign.pub`. A Scoop install is left to `scoop update`. Both are switched in Settings › About.

## Keyboard

| Keys | Action |
|---|---|
| `Ctrl+K` / `Ctrl+Shift+P` | Command palette |
| `Ctrl+Enter` / `Ctrl+Shift+Enter` | Run the statement at the cursor / the whole script |
| `Ctrl+E` | Explain the statement at the cursor |
| `Ctrl+S` | Save query |
| `Ctrl+T` / `Ctrl+W` | New tab / close tab |
| `Ctrl+\` / `Ctrl+Shift+\` | Split right / split down |
| `Ctrl+Shift+M` | Zoom the current pane |
| `Ctrl+1…9` | Switch Space |
| `Ctrl+B` / `Ctrl+J` | Sidebar / right panel |
| `Ctrl+Shift+E` | Export the result |
| `Ctrl+,` | Settings |

Settings has the full list.

## FAQ

**Which Windows versions work?** Windows 10 and 11, 64-bit.

**Which databases?** MySQL, MariaDB, PostgreSQL, SQLite, Redis, Oracle and SQL Server. There is no
ClickHouse or MongoDB support.

**Does Oracle need an Oracle client?** No. The helper uses a pure-Go driver
([go-ora](https://github.com/sijms/go-ora)), and is built into `locus.exe`, so there is nothing to
install. It is unpacked to `%LOCALAPPDATA%\Locus\sidecar\` on the first Oracle connection.

**Is my password sent anywhere?** No. See [Privacy](#privacy).

## Reporting a problem

Open an [issue](../../issues/new/choose). Say which database and version you connect to, and
what you did. Never paste passwords or connection strings. For a security problem, see
[SECURITY.md](SECURITY.md) and do not open a public issue.

## Building from source

You need Windows, a recent stable Rust, and Go (for the Oracle helper).

```powershell
cargo build --release -p app       # target\release\locus.exe
.\sidecar\build.ps1                # sidecar\bin\sidecar.exe
cargo test --workspace --lib --bins
```

Do not regenerate `Cargo.lock`: `gpui-kit` is a snapshot and a fresh resolve breaks the build.
More in [CONTRIBUTING.md](CONTRIBUTING.md). A map of the source is in [docs/README.md](docs/README.md).

## Privacy

Locus has no telemetry, no account, no update check and no network traffic of its own. It only
connects to the databases and SSH hosts you configure. Passwords go to the Windows Credential
Manager, never to a file. Query history and audit logs stay in `%APPDATA%\Locus` on your
machine, and result data is never written there. The only other file Locus writes is the Oracle
helper in `%LOCALAPPDATA%\Locus\sidecar\`.

## Acknowledgements

- [GPUI](https://www.gpui.rs/) and `gpui-kit` for the UI
- [Arc](https://arc.net) for the idea behind Spaces and vertical tabs

The licenses of all bundled components are in [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md).

## License

[AGPL-3.0](LICENSE).
