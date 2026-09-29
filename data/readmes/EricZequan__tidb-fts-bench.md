# TiDB FTS Import and Benchmark

This repo contains a small Python workflow to load Wikipedia titles into TiDB
with a full-text index and run an FTS benchmark.

## Requirements

- Python 3.11+
- A running TiDB cluster (defaults: `127.0.0.1:4000`)
- `data_set/wiki-articles.json` (newline-delimited JSON, downloaded separately)

## Setup

```bash
python3 -m venv myenv
source myenv/bin/activate
pip3 install -r requirements.txt
```

## Download Dataset

For this tutorial, download the 5M+ English Wikipedia corpus here:
[wiki-articles.json (2.34 GB)](https://www.dropbox.com/s/wwnfnu441w1ec9p/wiki-articles.json.bz2?dl=0).
Store it under `data_set/` and decompress it:

```bash
wget -O data_set/wiki-articles.json.bz2 \
  "https://www.dropbox.com/s/wwnfnu441w1ec9p/wiki-articles.json.bz2?dl=1"
bunzip2 data_set/wiki-articles.json.bz2
```

## Import Data

The importer creates the target table with a full-text index and then inserts
data in batches. It also enables `TIDB_ENABLE_FULLTEXT_INDEX` globally, so the
connected user must have permission to set it.

```bash
python3 load_wiki_articles.py --host 127.0.0.1 --port 4000 --database test --truncate
```

Common options:
- `--table` to change the target table name (default: `stock_items`).
- `--limit N` to load only the first N rows for a quick smoke test.
- `--file data_set/wiki-articles.json` to use a custom dataset.
- `--truncate` to clear existing rows in the target table (destructive).

## Run the Benchmark

The benchmark executes `fts_match_word` queries against the target table and
prints QPS and latency percentiles.

```bash
python3 benchmark_fts.py --query "Bluetooth" --duration 30 --concurrency 8
```

Multiple concurrency levels (run sequentially, then print an average):

```bash
python3 benchmark_fts.py --query "Bluetooth" --concurrency 10,20,50 --duration 30
```

Count-only mode and query list file:

```bash
python3 benchmark_fts.py --mode count --query-file queries.txt --duration 60 --concurrency 8
```

Tips:
- Use `--query-pick round-robin` for a deterministic query order.
- Run `--help` on either script for the full parameter list and defaults.
