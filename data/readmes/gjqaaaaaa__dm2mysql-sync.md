# dm2mysql-sync

A small, dependency-light CLI for **incremental data sync between SQL databases** —
originally built to move data from **Dameng (达梦)** into **MySQL** on a schedule,
but generic enough to sync between any two SQLAlchemy-supported engines
(MySQL, PostgreSQL, SQLite, Dameng, …).

## Why

Nightly/monthly ETL jobs usually need "only the rows that changed since last run".
`dm2mysql-sync` does exactly that:

- **Watermark-based incremental sync** — tracks the max value of a column
  (e.g. `updated_at` or an auto-increment `id`) and only pulls rows newer than it.
- **Upsert on primary key** — existing rows are updated, new rows inserted.
- **Resumable** — the last watermark is persisted to a JSON state file, so a
  crashed run can be re-run safely.
- **Config-driven** — connections and tables come from a YAML file; **no
  credentials are ever hard-coded** (use env vars / SQLAlchemy URLs).
- **`--dry-run`** — validate config and connectors before touching data.

## Install

```bash
pip install -e ".[dev]"      # editable install + pytest
```

## Quick start

```bash
export TGT_USER=root TGT_PASS=secret
cp examples/config.example.yaml config.yaml
# edit config.yaml (set source/target URLs and tables)
dm2mysql-sync -c config.yaml
dm2mysql-sync -c config.yaml --dry-run   # validate only
```

`config.yaml`:

```yaml
source:
  url: "dameng://"                      # built from DM_* env vars
  table: "credit_records"
target:
  url: "mysql+pymysql://${TGT_USER}:${TGT_PASS}@localhost:3306/target_db"
  table: "credit_records"
watermark_column: "updated_at"
primary_key: "id"
batch_size: 2000
mode: "incremental"                     # or "full"
```

## Dameng (达梦) support

This repo does **not** bundle the proprietary Dameng driver. To enable it:

1. Install the driver for your licensed Dameng distribution
   (e.g. `pip install sqlalchemy-dm`).
2. Provide secrets via env vars — never commit them:
   `DM_HOST`, `DM_PORT` (default `5236`), `DM_USER`, `DM_PASSWORD`, `DM_DB`.
3. Use `source.url: "dameng://"` in your config.

The exact dialect URL form lives in `src/dm2mysql_sync/connectors/dameng.py`
and can be adjusted to match your driver.

## How it works

1. On the first run (no saved watermark) it pulls everything, ordered by the
   watermark column, in pages of `batch_size`.
2. Each page is upserted into the target by primary key; the running max
   watermark is tracked.
3. The max watermark is written to `state_file`.
4. On the next run only rows with `watermark > last_watermark` are pulled.

Switch `mode: "full"` to ignore the watermark and re-sync everything.

## Development

```bash
pytest                 # runs the SQLite-based end-to-end tests
```

## Author

Jianqiang Gong (贡建强)

## License

MIT
