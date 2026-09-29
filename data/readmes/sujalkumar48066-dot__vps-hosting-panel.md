# VPS Hosting Panel (Telegram Bot)

A private-bot Telegram panel for hosting/selling VPS hosting subscriptions.
Runs on **TiDB Cloud** (multi-cluster mirroring, 5 clusters) or SQLite fallback.

## Security model
- The application is distributed as an **encrypted launcher** (`main.py`).
  Source (`.py`) files are NOT shipped. Decryption is gated by the
  `HOSTING_APP_KEY` secret: without it the process refuses to start.
- No credentials, tokens, or keys are committed to this repository.
- Secrets live only in deployment environment variables.

## Deploy on Render (blueprint)

1. Push this repo and create the service from `render.yaml`
   (or Dashboard → New → Blueprint).
2. In the Render dashboard, set these **secrets** for the service:
   - `HOSTING_APP_KEY` — the decryption key (required; bot refuses to run without it)
   - `HOSTING_BOT_TOKEN` — Telegram bot token from @BotFather
   - `HOSTING_OWNER_ID` — your Telegram user id
   - `HOSTING_TIDB_DSNS` — comma-separated TiDB DSN list (primary first)
   - optional: `HOSTING_SUB_LINK`, `HOST_URL`, `PORT`

`HOSTING_DB_DRIVER=tidb` and `HOSTING_DATA_DIR=/tmp/hosting_data` are set in
the blueprint already.

## Run locally

```bash
export HOSTING_APP_KEY=...        # same key used at build time
export HOSTING_BOT_TOKEN=...
export HOSTING_OWNER_ID=...
export HOSTING_DB_DRIVER=tidb
export HOSTING_TIDB_DSNS=mysql://...:4000/hostingdb,...
python main.py
```

## Build from source (owner only)
Source is rebuilt into `main.py` with a purpose-built bundler (`build_deploy.py`):
PBKDF2 keyed keystream → XOR + zlib + base85 per file, SHA-256 guarded key
check, self-extracting tempdir execution. Rebuild requires the source files and
produces a brand-new random `HOSTING_APP_KEY` each time.