<p align="center">
  <img src="docs/assets/yarix-banner.svg" alt="Yarix banner" width="100%">
  <br />
  <br />
  <img src="docs/assets/yarix-logo.svg" alt="Yarix logo" width="104" height="104">
</p>

<h1 align="center">Yarix</h1>

<p align="center"><strong>Discord moderation powered by native YARA rules, Anti-Spam, Honeypot, and OCR.</strong></p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.11+">
  <img src="https://img.shields.io/badge/license-MIT-111827?style=for-the-badge" alt="MIT License">
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20Linux-C97A12?style=for-the-badge" alt="Windows and Linux">
  <img src="https://img.shields.io/badge/storage-SQLite-0F172A?style=for-the-badge" alt="SQLite">
</p>

<p align="center">
  <a href="#installation"><strong>Install</strong></a> |
  <a href="#configuration"><strong>Configure</strong></a> |
  <a href="#ocr-flow"><strong>OCR Flow</strong></a> |
  <a href="SECURITY.md"><strong>Security Guide</strong></a>
</p>

<p align="center">
  Yarix is a standalone Discord moderation bot built around custom YARA rules, repeated-message detection, OCR-assisted image analysis, and SQLite-backed moderation state.
</p>

<p align="center">
  It is designed as a configurable moderation engine, not as a fixed detection pack. You define the rules, actions, thresholds, and guild-wide behavior that fit your server.
</p>

## Overview

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Docker](#docker)
- [Configuration](#configuration)
- [Discord Setup](#discord-setup)
- [Rule Modes](#rule-modes)
- [OCR Flow](#ocr-flow)
- [Honeypot](#honeypot)
- [Project Structure](#project-structure)
- [Development](#development)
- [Troubleshooting](#troubleshooting)
- [Security Guide](#security-guide)

## Features

- Native YARA-based message detection
- Per-rule configuration for actions and moderation stage
- Anti-Spam gating for repeated same-message behavior
- OCR-backed advanced analysis for repeated image campaigns
- Honeypot trap channel with timeout, ban, or quarantine
- Exempt roles
- Member moderation overview
- Quarantine release command
- Components V2 based moderation panels and embeds
- SQLite database with schema bootstrap and migrations
- Human-readable or structured runtime logging
- Optional Docker deployment

## Requirements

Supported platforms:

- Windows
- Linux, including Debian and Ubuntu

Python:

- Python `3.11` or newer

Main dependencies:

- `discord.py`
- `yara-python`
- `rapidocr-onnxruntime`
- `Pillow`
- `aiosqlite`
- `structlog`
- `pydantic`
- `pydantic-settings`
- `python-dotenv`

Optional development tools:

- `pytest`
- `pytest-asyncio`
- `ruff`

## Installation

### 1. Create a virtual environment

Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Linux:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

If `3.12` is not available, use the Python version you have installed as long as it is `3.11+`.

### 2. Install Yarix

```bash
python -m pip install --upgrade pip
python -m pip install -e .
```

For development tools:

```bash
python -m pip install -e .[dev]
```

### 3. Prepare configuration

Copy `.env.example` to `.env`.

Required:

```env
YARIX_DISCORD_TOKEN=your_bot_token
```

Recommended for testing:

```env
YARIX_COMMAND_GUILD_ID=your_test_server_id
```

### 4. Start the bot

```bash
python -m yarix
```

Expected startup includes a line like:

```text
Connected to Discord as Yarix#8123 (application_id=...)
```

## Docker

Docker is optional. Yarix can still be run directly on the host exactly as before.

Included files:

- `Dockerfile`
- `compose.yml`
- `.dockerignore`

### Docker Compose

1. Copy `.env.example` to `.env`
2. Fill in at least:

```env
YARIX_DISCORD_TOKEN=your_bot_token
```

3. Start the container:

```bash
docker compose up -d --build
```

4. View logs:

```bash
docker compose logs -f
```

5. Stop it:

```bash
docker compose down
```

### Direct Docker

Build:

```bash
docker build -t yarix .
```

Run:

```bash
docker run -d \
  --name yarix \
  --restart unless-stopped \
  --env-file .env \
  -v "$(pwd)/data:/app/data" \
  yarix
```

Notes:

- Mount `./data` so the SQLite database and runtime logs survive container restarts.
- The container uses the same `.env` keys as the direct host setup.
- Docker support is additive only. Nothing about the normal local or VPS setup changes.

## Configuration

Yarix reads runtime configuration from `.env`.

Core keys:

```env
YARIX_DISCORD_TOKEN=
YARIX_APPLICATION_ID=
YARIX_COMMAND_GUILD_ID=
YARIX_DATABASE_PATH=data/yarix.sqlite3
YARIX_RUNTIME_LOG_PATH=data/logs/yarix.log
YARIX_LOG_LEVEL=INFO
YARIX_MODERATION_CONSOLE_LOG_MODE=complex
```

### Logging

```env
YARIX_LOG_LEVEL=INFO
YARIX_MODERATION_CONSOLE_LOG_MODE=complex
YARIX_RUNTIME_LOG_PATH=data/logs/yarix.log
```

`YARIX_LOG_LEVEL` controls general application logging.

Available values:

- `INFO`
- `WARNING`
- `ERROR`

`YARIX_MODERATION_CONSOLE_LOG_MODE` controls moderation-flow console output.

Available values:

- `off`
- `simple`
- `complex`

`simple` is usually the best day-to-day choice.

Example `simple` output:

```text
[01:53:11.409 28.06.2026] Queue: OCR job queued (1 waiting)
[01:53:11.409 28.06.2026] Dispatcher: selected worker 0 (1 queued)
[01:53:11.409 28.06.2026] Worker 0: accepted queued OCR job
[01:53:11.637 28.06.2026] Worker 0: started OCR for 4 grouped messages
```

`YARIX_COMMAND_GUILD_ID` is only a fast-sync target for slash commands during development or controlled deployment. It does not control moderation scope or OCR capacity.

### Detection patterns and supported files

```env
YARIX_URL_DETECTION_PATTERN=https?://
YARIX_INVITE_DETECTION_PATTERN=(?:https?://)?(?:www\.)?(?:discord\.gg|discord(?:app)?\.com/invite)/[A-Za-z0-9-]+
YARIX_SUPPORTED_IMAGE_MIME_PREFIXES=image/
YARIX_SUPPORTED_IMAGE_EXTENSIONS=.png,.jpg,.jpeg,.gif,.webp,.bmp
YARIX_SUPPORTED_VIDEO_EXTENSIONS=.mp4,.mov,.webm,.avi,.mkv
YARIX_SUPPORTED_ARCHIVE_EXTENSIONS=.zip,.rar,.7z,.tar,.gz
```

### OCR worker and backend limits

```env
YARIX_OCR_GLOBAL_MAX_WORKERS=2
YARIX_OCR_PER_GUILD_MAX_WORKERS=1
YARIX_OCR_MAX_ATTACHMENT_TIMEOUTS_PER_JOB=1
YARIX_OCR_INTRA_OP_THREADS=2
YARIX_OCR_INTER_OP_THREADS=1
```

Meaning:

- `YARIX_OCR_GLOBAL_MAX_WORKERS`
  total OCR job concurrency for the full bot process
- `YARIX_OCR_PER_GUILD_MAX_WORKERS`
  OCR concurrency cap for one Discord guild
- `YARIX_OCR_MAX_ATTACHMENT_TIMEOUTS_PER_JOB`
  aborts one OCR cluster after this many per-attachment timeouts
- `YARIX_OCR_INTRA_OP_THREADS`
  how much CPU one OCR runtime may use for a single operation
- `YARIX_OCR_INTER_OP_THREADS`
  how much internal OCR parallelism one OCR runtime may use

Recommended CPU OCR starting point:

```env
YARIX_OCR_GLOBAL_MAX_WORKERS=2
YARIX_OCR_PER_GUILD_MAX_WORKERS=1
YARIX_OCR_MAX_ATTACHMENT_TIMEOUTS_PER_JOB=1
YARIX_OCR_INTRA_OP_THREADS=2
YARIX_OCR_INTER_OP_THREADS=1
```

Tuning guidance:

- keep `INTER=1` unless benchmarking proves otherwise
- raise `INTRA` before raising `INTER`
- reduce worker count before assuming OCR needs more parallelism

### Emoji configuration

Yarix supports custom emoji references through `.env`.

```env
YARIX_EMOJI_PIN=<:pin:...>
YARIX_EMOJI_TIMEOUT=<:timeout:...>
YARIX_EMOJI_TRASH=<:trash:...>
YARIX_EMOJI_LIST=<:list:...>
YARIX_EMOJI_INFO=<:info:...>
YARIX_EMOJI_BAN=<:ban:...>
YARIX_EMOJI_SETTINGS=<:settings:...>
YARIX_EMOJI_ALERT=<:alert:...>
YARIX_EMOJI_HONEY=<:honey:...>
```

If a custom emoji is not configured, Yarix falls back to the default value in `config.py`.

## First Startup Behavior

On first run Yarix will:

- create the SQLite database if it does not exist
- create missing tables
- run migrations
- sync slash commands

You do not need to create the database manually.

## Discord Setup

Recommended first-run flow:

1. Open `/automod panel`
2. Configure the log channel
3. Configure exempt roles if needed
4. Configure Honeypot if you want trap-channel moderation
5. Open `/rules panel`
6. Import your YARA rules
7. Configure or confirm each rule's mode and actions

Main commands:

- `/automod panel`
- `/rules panel`
- `/rules import-file`
- `/view`
- `/quarantine-lift`

### OAuth scopes

Use these scopes when generating the invite URL:

- `bot`
- `applications.commands`

### Bot permissions

Recommended base permissions:

- `View Channels`
- `Send Messages`
- `Embed Links`
- `Attach Files`
- `Read Message History`
- `Manage Messages`

Required when you use specific features:

- `Moderate Members`
  Needed for timeouts from rules, Anti-Spam, and Honeypot.
- `Ban Members`
  Needed if Honeypot or a rule should ban users.
- `Manage Roles`
  Needed for quarantine role assignment, quarantine role creation, and quarantine release.
- `Mention Everyone`
  Not required. Leave this disabled.
- `Administrator`
  Not required. Do not grant it unless you intentionally want full trust.

Practical recommendation:

- Place Yarix's role above the roles it may timeout or assign quarantine to.
- If you use the managed quarantine role, keep Yarix above that role as well.
- If logs or Honeypot actions do not work, check both channel overwrites and role hierarchy first.

## Rule Modes

### Immediate

Matches the message and acts right away.

### Anti-Spam

Only acts after repeated same-message behavior is detected.

### Advanced Signal

Does not directly punish. It contributes OCR risk for suspicious repeated image campaigns.

### Advanced Detect

Runs on OCR output after advanced analysis has already started.

## OCR Flow

Yarix's OCR pipeline works like this:

1. Normal message handling runs first
2. Immediate rules may act immediately
3. Anti-Spam may trigger on repeated same-message behavior
4. Advanced signal rules add risk to suspicious repeated image campaigns
5. Mature suspicious candidates are grouped into OCR jobs by content-based candidate key
6. OCR jobs are placed into the guild OCR queue
7. The dispatcher assigns queued jobs to free worker slots
8. OCR scans supported images inside that job
9. OCR text is fed into advanced-detect YARA rules
10. Matching OCR-detect rules apply actions

Important notes:

- OCR uses `rapidocr-onnxruntime`
- OCR timeout is configured through the Discord AutoMod panel
- worker and backend thread limits come from `.env`
- one OCR job scans its own images sequentially
- different suspicious image sets from the same user become separate OCR jobs
- identical suspicious content is grouped into one OCR job
- if a cluster reaches the configured attachment-timeout limit, Yarix aborts the rest of that cluster

### OCR Tuning

Recommended tuning order:

1. keep worker counts conservative
2. increase OCR timeout if heavier images are simply too slow
3. increase `INTRA` if one OCR worker needs more CPU
4. only benchmark `INTER > 1` after the stable path is known

## Honeypot

The Honeypot system is a trap channel.

When a user posts in the configured Honeypot channel, Yarix can:

- delete the Honeypot message
- remove matching messages from the same user in other channels
- apply the configured punishment
- send a DM notice if possible
- log the event

Available Honeypot actions:

- timeout
- ban
- quarantine role

If `quarantine` is used, Yarix can:

- use an existing role
- create a managed quarantine role
- keep one appeal channel visible for quarantined users

## Database

Default database path:

```text
data/yarix.sqlite3
```

Relevant files:

- [src/yarix/db/schema.sql](src/yarix/db/schema.sql)
- [src/yarix/db/migrations.py](src/yarix/db/migrations.py)
- [src/yarix/db/repository.py](src/yarix/db/repository.py)

## Runtime Logs

Yarix writes:

- normal application output to the console
- runtime console output to the configured log file path

Default runtime log file:

```text
data/logs/yarix.log
```

## Project Structure

Important files and folders:

- [src/yarix/bot.py](src/yarix/bot.py) - bot startup and Discord event flow
- [src/yarix/cogs/admin.py](src/yarix/cogs/admin.py) - panels and slash commands
- [src/yarix/moderation.py](src/yarix/moderation.py) - moderation pipeline and action flow
- [src/yarix/components_v2.py](src/yarix/components_v2.py) - Components V2 layouts
- [src/yarix/ocr_engine.py](src/yarix/ocr_engine.py) - OCR wrapper
- [src/yarix/pipeline.py](src/yarix/pipeline.py) - attachment analysis pipeline
- [src/yarix/yara_engine.py](src/yarix/yara_engine.py) - YARA validation and matching
- [examples](examples) - example assets, images, and bundled rule references

## Development

Run tests:

```bash
pytest
```

Lint with Ruff:

```bash
ruff check .
```

## Minimal Setup Checklist

1. Install Python `3.11+`
2. Create and activate `.venv`
3. Run `python -m pip install -e .`
4. Copy `.env.example` to `.env`
5. Set `YARIX_DISCORD_TOKEN`
6. Start the bot with `python -m yarix`
7. Open `/automod panel`
8. Set the log channel
9. Open `/rules import-file` or `/rules panel`
10. Import and configure your rules

## Troubleshooting

### `python -m yarix` says `No module named yarix`

The project is not installed into the active virtual environment.

Run:

```bash
python -m pip install -e .
```

### OCR times out

The configured OCR timeout is too low for the machine or image batch.

Increase the OCR timeout from the advanced-analysis panel and test again.

### Commands do not appear

Make sure:

- the bot is running
- slash commands synced successfully on startup
- `YARIX_COMMAND_GUILD_ID` is set correctly for test-guild sync

### Database did not exist

That is normal on a fresh installation. Yarix creates it automatically on first startup.

## Security Guide

For Yarix-specific YARA rule design, supported externals, import presets, and rule-writing guidance, see [SECURITY.md](SECURITY.md).
