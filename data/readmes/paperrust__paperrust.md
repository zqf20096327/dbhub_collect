# PaperRust

English · [Deutsch](README.de.md)

**A fast, lean document archive that works with your paperless-ngx data.**

PaperRust scans, recognises and files your documents and makes them searchable. It is a
re-implementation of [paperless-ngx](https://github.com/paperless-ngx/paperless-ngx) 3.4.2 in Rust:
it uses the **same database, the same files and the same REST API**, but runs as a single program
(`paperrust`) next to PostgreSQL – no Python, Redis, Celery, Tika or Gotenberg. You can switch from
paperless-ngx with one command (or one click in the desktop app), and there is a way back.

Website: <https://paperrust.org> · Documentation: [English](docs/user/en/README.md) ·
[Deutsch](docs/user/README.md) · Release notes 0.1.1: [English](docs/RELEASE-NOTES-0.1.1.en.md) ·
[Deutsch](docs/RELEASE-NOTES-0.1.1.md) (0.1.0: [English](docs/RELEASE-NOTES-0.1.0.en.md))

> [!IMPORTANT]
> **Status: 0.1.1, an early version.** PaperRust is young software. Read the
> [known limits](docs/RELEASE-NOTES-0.1.0.en.md#limits) and try it with a **copy** of your data first.
> The Windows installer is not code-signed yet.

## At a glance

Measured against paperless-ngx 3.4.2 on the same small arm64 board (NVIDIA Jetson Orin Nano), same
documents, same database – details and limits below:

- **17× faster consuming:** 230 documents in 1 min 46 s instead of 29 min 56 s.
- **Raspberry Pi 5:** 230 documents in 3 min 05 s instead of 27 min 07 s, with a twelfth of the processor
  time (100 instead of 1,253 CPU seconds) – [report](results/benchmark/2026-11-22-pi5/bericht.md) (German).
- **16× faster first start** (3.3 s instead of 53 s); a restart answers after 0.6 s instead of 34 s.
- **12–19× faster answers with several users at once** (median, 1–10 people, no errors) –
  [report](results/benchmark/2026-11-20-jetson/s2s3-rerun/bericht.md) (German).
- **One container instead of two, 0.65 GB instead of 3.5 GB** – no Python, Redis, Celery, Tika or
  Gotenberg. Starts with 74 MiB of memory (plus the database).
- **Your data stays as it is:** same database, same files, same REST API. Apps for paperless-ngx keep
  working, and [switching](#switching-from-paperless-ngx) takes a few commands – with a way back.

```sh
docker pull ghcr.io/paperrust/paperrust:0.1.1     # linux/amd64 + linux/arm64
```

## Why PaperRust?

Measured on 20 November 2026 on an NVIDIA Jetson Orin Nano (arm64, 6 cores, 8 GB RAM) in Docker, one
run per setup, 255 made-up documents. PaperRust (commit `e546b8f`) against paperless-ngx 3.4.2 in
its leanest setup (Valkey, no Tika/Gotenberg), both with PostgreSQL 17 and 4 cores each, both
cleaning and deskewing scans:

| | paperless-ngx 3.4.2 | PaperRust |
|---|---:|---:|
| First start until login is possible | 53.2 s | 3.3 s |
| Restart until the document list answers | 33.7 s | 0.57 s |
| Consume 230 documents (200 text PDFs, 30 scans) | 29 min 56 s | 1 min 46 s |
| One scan (1 page) until searchable | 25.8 s | 8.1 s |
| List/search while consuming (median / 95 %) | 150 / 187 ms | 10 / 32 ms |
| Memory freshly started (services + database) | 598 + 41 MiB | 74 + 64 MiB |
| Memory idle after consuming (services + database) | 702 + 49 MiB | 420 + 74 MiB |
| Docker images without PostgreSQL ¹ | 3.47 GB (2 containers) | 0.65 GB (1 container) |

¹ Measured on 18 November 2026 (commit `c97f15c`).

**Where PaperRust is worse:** its database uses more memory (74 instead of 49 MiB after consuming)
and more disk (logically 28.4 instead of 18.2 MB, the database volume 11 % more), and the memory peak
while consuming (800 MiB) is only slightly below paperless-ngx (838 MiB). Only one device and clean
test documents were measured in this table (Raspberry Pi 5: see above); do not over-interpret differences below about 10 %.

Full report with method and limits (German):
[results/benchmark/2026-11-20-jetson/bericht.md](results/benchmark/2026-11-20-jetson/bericht.md),
all tables: [tabellen.md](results/benchmark/2026-11-20-jetson/tabellen.md). Summary in English:
[release notes → Performance](docs/RELEASE-NOTES-0.1.0.en.md#performance).

## Features

- **One program instead of five services:** `paperrust serve --worker` is web server, worker,
  scheduler and consumption folder in one process; queue and cache live in PostgreSQL.
- **Drop-in compatible:** apps and scripts written for the paperless-ngx API keep working; all
  `PAPERLESS_*` variables keep their meaning (own settings use `PAPERRUST_*`).
- **Adding documents** from the consumption folder, upload, mailboxes, scanners (AirScan/eSCL scan
  button, scan to e-mail) and the REST API. PDF, images (including HEIC and multi-page TIFF), Office
  files (including old `.doc/.xls/.ppt`), e-mails.
- **Text recognition** with Tesseract, built-in cleaning and deskewing of scans, PDF/A archive files.
- **Organising and searching:** correspondents, document types, nested tags, storage paths, custom
  fields, ASNs, saved views, automatic matching, full-text search.
- **Automation:** workflows shown as a readable sentence, templates, dry run before applying,
  history ([automation](docs/user/en/automatik.md)).
- **Optional AI** (off by default; local with Ollama or OpenAI-compatible services): suggestions with
  a review list, custom fields, AI text recognition, chat, MCP server ([AI](docs/user/en/ai.md)).
- **PDF tools:** redaction, shrinking, convert to PDF, repair on ingest
  ([PDF tools](docs/user/en/pdf-tools.md)).
- **Ransomware protection:** read-only guard, encrypted versioned backups, integrity check
  ([ransomware](docs/user/en/ransomware.md)).
- **Own web UI** in 10 languages, with the classic paperless-ngx-style UI still selectable.
- **Users and permissions:** roles, groups, object permissions, two-factor login, OpenID Connect and
  other social logins.

## Installation

| Way | What you get | Guide |
|---|---|---|
| **Desktop app – Windows** (x64) | Installer with embedded PostgreSQL 17, Tesseract and PDFium; no server setup, no login on your own computer. **Not code-signed yet**, so Windows SmartScreen warns; compare the SHA-256 checksum. Code signing through the SignPath Foundation is planned. | [Desktop app](docs/user/en/installation.md#desktop) |
| **Desktop app – Linux** (x86_64) | Portable `tar.gz` with PostgreSQL 17, Tesseract (German, English) and PDFium. Needs glibc 2.36 or newer (Debian 12, Ubuntu 24.04, Fedora 37 or newer). Opens its own window when WebKitGTK 4.1 and libayatana-appindicator are installed, otherwise the browser. Do not run it as root. | [Linux package](docs/user/en/installation.md#desktop-linux) |
| **Desktop app – macOS** | Planned (needs a Mac and an Apple developer account). | – |
| **Docker / server** | Image from `docker/Dockerfile` for `linux/amd64` and `linux/arm64`, compose files in `docker/`. Same volumes, port and commands as the paperless-ngx image. | [Docker](docs/user/en/installation.md#docker) |
| **NAS** | Templates for Synology, UGREEN, Asustor (compose), Unraid (XML) and CasaOS in `docker/nas/` | [NAS](docs/user/en/installation.md#nas), [docker/nas/README.md](docker/nas/README.md) (German) |
| **From source** | `paperrust`, `paperrust-pdftool` and `paperrust-migrate-db`, plus PostgreSQL ≥ 14, Tesseract 5 and PDFium | [Building from source](docs/user/en/installation.md#build) |

Desktop installers and packages are attached to the
[GitHub releases](https://github.com/paperrust/paperrust/releases).

### Get the code

The `upstream/` git submodule (paperless-ngx v3.4.2, unmodified) is **required to build** – clone
with submodules:

```sh
git clone --recurse-submodules https://github.com/paperrust/paperrust.git
cd paperrust
# already cloned without submodules?  git submodule update --init
```

### Docker compose

The published image `ghcr.io/paperrust/paperrust` (tags `0.1.1`, `0.1`, `latest`; amd64 and arm64)
starts with PostgreSQL like this:

```sh
cd docker
mkdir -p consume export
# first set PAPERRUST_SECRET_KEY (and optionally PAPERRUST_ADMIN_USER/PASSWORD) in docker-compose.env
export PAPERRUST_IMAGE=ghcr.io/paperrust/paperrust:0.1.1
docker compose -f docker-compose.postgres.yml pull
docker compose -f docker-compose.postgres.yml up -d      # PaperRust + PostgreSQL 17
```

Without `PAPERRUST_IMAGE`, compose builds the image from this repository instead
(`docker compose -f docker-compose.postgres.yml build`).

The UI is then at <http://localhost:8000>. Other variants in `docker/`: slim configuration
(`docker-compose.slim.yml`), separate web/worker processes (`docker-compose.multiprocess.yml`),
switching from paperless-ngx (`docker-compose.migrate-from-paperless.yml`).

### Building from source

With a current stable Rust toolchain (selected by `rust-toolchain.toml`):

```sh
cargo build --release -p pl-server                                              # target/release/paperrust
cargo build --release -p pl-pdftools --features engine --bin paperrust-pdftool  # PDF tools, put next to paperrust
cargo build --release -p pl-dbmigrate                                           # paperrust-migrate-db (SQLite/MariaDB → PostgreSQL)
(cd frontend-light && pnpm install && pnpm build)                               # web UI → frontend-light/dist
```

Without `paperrust-pdftool` next to `paperrust`, redaction, shrinking, repair and Office→PDF are not
available. Database setup, configuration, static files and a systemd unit:
[Installation → server without Django](docs/user/en/installation.md#standalone).

## Switching from paperless-ngx

> **Please stay healthily sceptical.** PaperRust 0.1 is an early version. The core is thoroughly tested –
> but not with your documents. Before switching: make a **full backup** of paperless-ngx (export, or database
> and media folder), **try PaperRust with a copy first**, and only turn paperless-ngx off once everything is
> right. Don't migrate blindly. The way back to paperless-ngx stays open.


PaperRust takes over paperless-ngx 2.20 and 3.0–3.4.2 (also the newer tag-tree schema after 3.4.2)
with one command – `paperrust migrate --from <paperless folder | database URL | export>` – or with
"Switch from paperless-ngx" in the desktop app. Files, users with their passwords, permissions,
workflows and mail rules come along. PaperRust checks everything first (`--dry-run`), backs up an
existing database before changing it, and prints a comparison report at the end. SQLite and
MariaDB/MySQL databases are copied into PostgreSQL.

**The way back:** after the switch, paperless-ngx can no longer open the same database. Going back
works through the backup or an export in the paperless-ngx 3.4.2 format. If unsure, switch into a
**copy** (`--target`) and leave paperless-ngx untouched.

### Switching in a few commands (Docker with PostgreSQL)

```sh
# 1. back up (paperless-ngx stopped: docker compose down, then start only the database)
docker compose up -d db
docker compose exec db pg_dump -U paperless -Fc paperless > paperless-before.pgdump
# 2. in docker-compose.yml replace the paperless-ngx image with ghcr.io/paperrust/paperrust:0.1.1
#    (template: docker/docker-compose.migrate-from-paperless.yml) – keep volumes and PAPERLESS_SECRET_KEY
# 3. trial run: checks everything, changes nothing
docker compose run --rm webserver paperrust migrate --dry-run \
    --from "postgres://paperless:PASSWORD@db:5432/paperless" --media /usr/src/paperless/media
# 4. switch (same command without --dry-run), then start and sign in with your existing users
docker compose up -d
```

Want to leave the original untouched? Add `--target "postgres://paperless:PASSWORD@db:5432/paperrust"`
(an empty database) and PaperRust copies everything into it. Going back: restore
`paperless-before.pgdump` and put the paperless-ngx image back.

- Step by step: [English](docs/user/en/umstieg.md) · [Deutsch](docs/user/umstieg.md)
- In depth (same database, SQLite/MariaDB, export/import, going back):
  [English](docs/user/en/migration.md) · [Deutsch](docs/user/migration.md)

## Documentation

- User guide: [English](docs/user/en/README.md) · [Deutsch](docs/user/README.md) – installation,
  first steps, configuration, mail, scanners, workflows, AI, permissions, backup, security,
  troubleshooting. The same manual is built into the app (`/rs/docs/`).
- Release notes 0.1.0 with all known limits: [English](docs/RELEASE-NOTES-0.1.0.en.md) ·
  [Deutsch](docs/RELEASE-NOTES-0.1.0.md)
- For developers (mostly German): [architecture](docs/ARCHITECTURE.md), per-crate contracts with
  "Known differences" in [docs/contract/](docs/contract/), [following upstream](docs/UPSTREAM-SYNC.md),
  [release gate](docs/RELEASE-GATE.md).

## Status and limits

PaperRust 0.1.0 is the first version. Before the release it went through a 24-hour soak test under
mixed load without a single server error ([report](results/release/soak/2026-11-19-24h/BERICHT.md),
German) and an independent code security review with all findings fixed
([report](results/release/review/security-2026-11-19.md), German).

**How the core was tested:** about 2,100 automated tests (Windows and Linux arm64), API comparison
against a running paperless-ngx 3.4.2, load, concurrency and failure tests, a 24-hour soak test,
several hours of fuzzing, a full restore on a fresh system, and UI click tests in Chromium. What we
could not test ourselves (Safari, Firefox, Android, screen readers, real NAS devices, many real-world
document collections) is listed openly below. **This is where we need you:** if something does not
work, please [open an issue](https://github.com/paperrust/paperrust/issues) – every report helps
make PaperRust solid.

Main limits (full list in the [release notes](docs/RELEASE-NOTES-0.1.0.en.md#limits)):

- **PostgreSQL only** (14 or newer); SQLite/MariaDB are copied over when switching.
- The Windows installer is **not code-signed** yet; the Linux package is new (checked on fresh Ubuntu 24.04
  and Debian 12); no macOS app yet.
- Not specifically tested: Safari, Firefox, Android browsers, screen readers, real NAS devices.
- **Automatic matching** uses its own model and learns again after switching.
- Office files become simpler archive PDFs than with LibreOffice/Gotenberg; PDF/A is not confirmed
  with veraPDF.
- Fewer social-login providers (OpenID Connect, GitHub, GitLab, Google, Microsoft, Nextcloud,
  Discord, Gitea); no Django admin (`/admin/`).
- The UI has 10 languages; API error messages are in English only.
- Several integrations (Azure OCR, S3 backup, scanner hardware, OAuth mail, social-login providers)
  are covered by tests with simulated responses, not checked against the real services.

Reference version: paperless-ngx **v3.4.2** (`upstream/` submodule, never modified). API responses
are compared against a running paperless-ngx instance (`tests/parity/`); every accepted deviation is
written down as a "Known difference" in `docs/contract/*.md`.

## Contributing and security

- How to build, test and submit changes: [CONTRIBUTING.md](CONTRIBUTING.md)
- Reporting vulnerabilities (privately, not as an issue): [SECURITY.md](SECURITY.md)
- Code of conduct: [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

Please report bugs in PaperRust here, **not** to the paperless-ngx project.

## License and credits

PaperRust is licensed under the **GNU General Public License v3.0** (`GPL-3.0-only`), see
[LICENSE](LICENSE) and [NOTICE](NOTICE).

PaperRust is based on [paperless-ngx](https://github.com/paperless-ngx/paperless-ngx) (GPL-3.0,
© the paperless-ngx authors), which itself builds on paperless-ng and Paperless. Its business logic,
database schema and parts of the documentation come from there – many thanks to everyone who built
it. Third-party components and their licenses are listed in [NOTICE](NOTICE).

PaperRust is an independent project and is not affiliated with, endorsed by or supported by the
paperless-ngx project. "Rust" is a trademark of the Rust Foundation; PaperRust is not endorsed by the
Rust Foundation.
