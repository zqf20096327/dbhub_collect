# GlobalTemperatureSQL

**Query the Data. Understand the Climate.**

An interactive SQL-powered platform for exploring historical global temperature anomalies from
NASA GISTEMP v4 — a PostgreSQL/PostGIS database with **25 million gridded observations**, a
library of 78 SQL analyses, a measured indexing and partitioning study, a regression analysis of
El Niño and the warming trend with autocorrelation-robust uncertainty, a Streamlit app with
interactive maps and charts, and a secure SQL Playground.

![CI](https://github.com/zeynepsonmeez/global-temperature-sql/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.13-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-336791)
![PostGIS](https://img.shields.io/badge/PostGIS-3.6-5a8f29)
![Coverage](https://img.shields.io/badge/coverage-94%25-brightgreen)
![Ruff](https://img.shields.io/badge/lint-ruff-261230)
![SQLFluff](https://img.shields.io/badge/SQL-sqlfluff-c22e2e)
![License](https://img.shields.io/badge/license-MIT-green)
[![Kaggle dataset](https://img.shields.io/badge/Kaggle-dataset-20BEFF)](https://www.kaggle.com/datasets/zeynepsonmeez/global-and-country-temperature-anomalies-1880-2025)

![Home page: a slowly turning globe coloured by the warming of each latitude band](docs/images/home.png)

<table>
  <tr>
    <td width="50%"><img src="docs/images/explorer.png" alt="Climate Explorer: the global trend since 1880 with a 5-year moving average"><br><sub><b>Climate Explorer</b> — seven analyses, each with its SQL</sub></td>
    <td width="50%"><img src="docs/images/map.png" alt="Warming Map: warming rate by country, 1970–2025"><br><sub><b>Warming Map</b> — country trends from 25 M grid values in PostGIS</sub></td>
  </tr>
  <tr>
    <td width="50%"><img src="docs/images/drivers.png" alt="Climate Drivers: the ENSO index above global temperature"><br><sub><b>Climate Drivers</b> — ENSO, CO₂ and a regression model</sub></td>
    <td width="50%"><img src="docs/images/playground.png" alt="SQL Playground: sample queries, schema, editor and challenges"><br><sub><b>SQL Playground</b> — read-only SQL with a cost gate and 15 challenges</sub></td>
  </tr>
</table>

---

## Features

**Climate Explorer** — seven ready-made analyses with filters (year range, regions, month,
moving average): global trend, hottest years, decades, hemispheres, monthly heatmap,
record tracker and warming by latitude band. Every chart has a **"SQL behind this chart"**
panel and can be opened in the Playground with one click.

**Warming Map** — built on NASA's 2°×2° grid in PostGIS: a country choropleth of warming
rates for any period, the full grid for any year since 1880, and a side-by-side comparison of
up to five countries against the global mean. Country series are area-weighted from the grid cells inside
each border.

**Climate Drivers** — why does temperature go up and down from year to year? ENSO (El Niño /
La Niña) against global temperature, the lag between them, the warmest years before and after
removing ENSO, the breakpoint when warming accelerated, the Keeling CO₂ curve, and classical vs
Newey-West confidence intervals side by side. Methods: [`docs/METHODS.md`](docs/METHODS.md).

**SQL Playground** — write and run read-only SQL against the real database (including PostGIS
functions): schema browser, 78 sample queries (basic → advanced → spatial → drivers), result table with
timing, CSV export, quick charts, an EXPLAIN cost gate and 15 **challenges** checked automatically against a
reference query.

**Home** — a rotatable globe coloured by the warming of each latitude band, dataset facts and
headline findings computed live. Interface in **English and Turkish**; light theme by default,
dark theme in the menu.

## Findings

Computed by the queries in [`sql/`](sql/) on the NASA snapshot of 10 Nov 2026
(anomalies in °C relative to 1951–1980):

| Finding | Query |
|---|---|
| The 10 hottest years all occurred in **2015 or later**; 2024 is the hottest (+1.28 °C). | B2 |
| No month has been cooler than the 1951–1980 average since **September 1992**. | B8 |
| **41 consecutive months** at or above +1.0 °C (June 2023 – October 2026); the previous longest run was 7. | A10 |
| Global warming rate since 1970: **+0.20 °C per decade** (R² = 0.91), about 2.5× the long-term rate. | A6 |
| The **Arctic** (64°N–90°N) has warmed **3× faster** than the globe since 1970. | A7 |
| Since 1970, **land has warmed twice as fast as the ocean** (0.29 vs 0.15 °C per decade). | S6 |
| **Türkiye** has warmed **+0.44 °C per decade** since 1970 — 2.2× the global rate; 2024 was +2.57 °C. | S2, map |
| The hemisphere gap grew from 0.06 °C (1990s) to **0.61 °C** (2020s): the land-rich North warms faster. | I2 |
| Relative to 1880–1900, 2024 reached about +1.50 °C (a single year, not the Paris 20-year average). | I9 |
| El Niño is associated with **+0.09 °C per ONI unit**, three months later; adding ENSO raises R² from 0.83 to 0.87. | model |
| With ENSO removed, **2016 drops from the 4th to the 9th** warmest year; 2023–2025 stay on top. | D8 |
| Warming **accelerated around 1975** (approx. range 1971–1979): from 0.04 to **0.21 °C per decade**. | D9 |
| Autocorrelation makes the classical trend interval **half as wide as it should be** (Newey-West). | model |

## Performance study

How do you index 25 million rows that are queried by date (maps), by cell (local series) and
by country (spatial joins)? [`docs/PERFORMANCE.md`](docs/PERFORMANCE.md) measures five
strategies with `EXPLAIN (ANALYZE, BUFFERS)`:

| | No index | Best single index | Production design |
|---|---:|---:|---:|
| One month, all cells | 350 ms | 2.2 ms (B-tree date) | 2.4 ms |
| One cell, all months | 348 ms | 0.8 ms (B-tree cell, date) | 1.4 ms |
| One country, from the raw grid | 1,069 ms | 37 ms | 42 ms → **0.1 ms** with a materialized view |

Key lessons: column order decides which queries an index can serve; a **BRIN index** matches a
B-tree on date-ordered data at **1/4,000 of the size** (40 KB vs 169 MB); partitioning by decade
prunes date queries to one partition; pre-aggregation beats any index. The production design —
decade partitions + `(cell_id, obs_date)` primary key + BRIN + materialized views — is the only
one fast on every query shape.

## Statistical analysis

A regression of the monthly global anomaly on time and the lagged El Niño index (1970 onwards),
estimated with Newey-West standard errors because consecutive months are not independent
(residual autocorrelation 0.59), plus a two-segment breakpoint search on annual means.
Assumptions, every number and its limitations are written up in [`docs/METHODS.md`](docs/METHODS.md);
the results are described as associations, not attributions.

## Architecture

```text
 NASA GISTEMP CSV ─► download_data.py ─► clean_data.py ─► load_data.py ─┐
   (global, hemispheres, latitude bands; manifest with SHA-256)          │
                                                                         ▼
 NASA 2°x2° NetCDF ─┐                                     PostgreSQL 17 + PostGIS 3.6 (Docker)
 Natural Earth ─────┴► download_grid.py ─► load_grid.py ─►  public: monthly + zonal series
   (COPY 25M rows, constraints after load, spatial join)      grid_anomalies (partitioned by decade)
                                                              grid_cells, countries, cell_countries
                                                              materialized views (cell, country, trends)
 NOAA ONI + CO2 ─► load_drivers.py ─► run_models.py ───────►  enso_oni, co2_monthly, model_* tables
   (statsmodels: OLS + Newey-West, breakpoint profile)      playground: read-only views
                                                                         │
                          Streamlit app ── connects as gts_reader (read-only role) ◄─┘
                           ├─ Home · Climate Explorer · Warming Map · Climate Drivers (Plotly)
                           └─ SQL Playground ── sql_guard (sqlglot) ── DB privileges + 3 s timeout
```

## Quick start

Requirements: Python 3.11+, Docker, ~3 GB free disk for the grid.

```bash
# 1. Python environment
python -m venv .venv
.venv\Scripts\activate                 # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt

# 2. Settings: copy and set your own passwords
cp .env.example .env

# 3. Database (PostgreSQL 17 + PostGIS on 127.0.0.1:5433)
docker compose up -d
python scripts/setup_database.py       # schemas + read-only role

# 4. Data
python scripts/clean_data.py           # global series (a NASA snapshot is committed)
python scripts/load_data.py
python scripts/download_grid.py        # grid + country borders (~29 MB download)
python scripts/load_grid.py            # ~25M rows, about a minute
python scripts/load_drivers.py         # ENSO and CO2 (committed NOAA snapshots)
python scripts/run_models.py           # regression, ENSO-adjusted series, breakpoint

# 5. Run
streamlit run app/main.py              # http://localhost:8501
pytest                                 # 558 test cases
python scripts/benchmark.py            # optional: re-run the performance study
python scripts/export_kaggle.py        # optional: analysis-ready files for Kaggle in data/kaggle/
```

**Run the app in Docker instead** (after step 4 — the pipeline writes the data, the container
only reads it through the read-only role):

```bash
docker compose --profile app up -d --build   # http://localhost:8501
```

**Development setup** — linters, git hooks and coverage:

```bash
pip install -r requirements-dev.txt
pre-commit install                     # ruff, sqlfluff and file checks before every commit
pytest --cov                           # coverage of app/ and scripts/
```

## Database

| Object | Rows | Description |
|---|---:|---|
| `datasets` | 2 | One row per downloaded snapshot (data versioning) |
| `regions` | 14 | Global, hemispheres and 11 latitude bands with their bounds |
| `monthly_anomalies` | 5,286 | GLB / NH / SH monthly; PK `(dataset_id, region_id, year, month)` |
| `zonal_annual_anomalies` | 1,606 | Latitude bands, annual |
| `grid_cells` | 16,200 | 2°×2° cell polygons with exact spherical area weights |
| `grid_anomalies` | 25.4 M | Partitioned by decade; anomaly as lossless `SMALLINT` hundredths |
| `countries`, `cell_countries` | 242 / 8.3 k | Natural Earth borders and their overlap with every cell (km²) |
| `v_grid_annual`, `v_grid_trends`, `v_country_annual` | | Materialized aggregates for the app |
| `enso_oni`, `co2_monthly` | 921 / 824 | NOAA ONI (stored on the centre month) and Mauna Loa CO₂ |
| `model_results`, `model_enso_adjusted`, `model_breakpoints` | | Outputs of `run_models.py` |
| `playground.*` | | The only objects the app's read-only role can see |

Design notes and validation: [`docs/DATA.md`](docs/DATA.md). Among the checks: NASA's annual
values are recomputed in SQL and must match; the grid's area-weighted mean must reproduce
NASA's global series (mean difference 0.005 °C, r = 0.9999); stored grid values must equal
the NetCDF file exactly.

## SQL library

| File | Queries | Topics |
|---|---:|---|
| [`basic_queries.sql`](sql/basic_queries.sql) | 15 | SELECT, WHERE, ORDER BY, NULLS LAST, GROUP BY, HAVING, aggregates, LIKE |
| [`intermediate_queries.sql`](sql/intermediate_queries.sql) | 16 | CTEs, self-join, LEFT JOIN, subqueries, EXISTS, UNION ALL, CASE, FILTER, dates |
| [`advanced_queries.sql`](sql/advanced_queries.sql) | 22 | RANK / DENSE_RANK / ROW_NUMBER, LAG / LEAD, ROWS vs RANGE windows, NTILE, gaps-and-islands, LATERAL, ROLLUP, regr_slope, corr, percentile_cont |
| [`spatial_queries.sql`](sql/spatial_queries.sql) | 13 | Spatial joins, ST_Contains, KNN `<->`, ST_Area on geography, area weighting, DISTINCT ON |
| [`drivers_queries.sql`](sql/drivers_queries.sql) | 12 | Detrending with regr_slope / regr_intercept, lagged joins with make_interval, correlation over generated lags, growth rates |

Every query is commented, available in the Playground and runs in CI.

## Security

The Playground has two independent layers: a sqlglot-based validator and a PostgreSQL role that
can only read the playground views and PostGIS functions, cannot write or create anything, and
is stopped after 3 seconds. Between them, an **EXPLAIN cost gate** refuses queries whose planner
estimate is too high before they run, and results stream through a server-side cursor.
See [`docs/SECURITY.md`](docs/SECURITY.md).

## Code quality

- **ruff** lints all Python (pycodestyle, pyflakes, import order, bugbear, pyupgrade).
- **sqlfluff** lints the SQL library; the rules that are switched off are style choices,
  each justified in [`.sqlfluff`](.sqlfluff).
- **pre-commit** runs both plus file checks (large files, private keys, merge conflicts)
  before every commit; raw data files are excluded so their checksums never change.
- **Coverage** is measured across the whole pipeline: CI runs every pipeline script under
  `coverage run`, then the test suite, and fails below 85% (currently 94%).
- **Design decisions** are recorded as [architecture decision records](docs/adr/).

## Testing

| Suite | Tests | Covers |
|---|---:|---|
| `test_clean_data.py` | 13 | Parsing, `***` → NULL, long format, NASA J-D match, baseline check |
| `test_validation.py` | 7 | Every validation rule rejects the problem it is written for |
| `test_database.py` | 20 | Row counts, SQL annual mean = NASA J-D, constraints, keys, SQL library runs, planner statistics after loading |
| `test_grid.py` | 9 | Area weights, valid geometry, lossless storage, grid = NASA global mean, partition pruning |
| `test_findings.py` | 9 | Every claim in the Findings table above, recomputed from the database |
| `test_drivers.py` | 10 | ONI season mapping, NULL sentinels, model signs, Newey-West wider than classical |
| `test_run_models.py` | 5 | Newey-West bandwidth, breakpoint recovered from a synthetic series, lag alignment |
| `test_sql_guard.py` | 57 | 40 attack queries blocked; 12 harmless edge cases and all 78 library queries allowed |
| `test_reader_role.py` | 10 | Database-level protection without the validator |
| `test_errors.py` | 92 | Every library query run as the read-only role through the cost gate; expensive queries refused before running; plain error messages, timeout, streaming row limit |
| `test_queries.py` | 56 | Static checks on the app's SQL (placeholders) |
| `test_export_kaggle.py` | 2 | The Kaggle export writes every file, a description that matches it and valid metadata |
| `test_freshness.py` | 5 | The freshness check finds added and revised months and never touches the committed snapshot |
| `test_helpers.py` | 14 | SQL literal quoting, library numbering, psql command (password never on the command line) |
| `test_challenges.py` | 35 | Challenge references and the answer checker |
| `test_i18n.py` | 196 | Every text in EN and TR, matching placeholders, every key used in the code exists |
| `test_app.py` | 18 | Every page renders in both languages; the globe loads plotly.js locally; Playground runs and blocks queries |

**558 test cases from 109 test functions** — many are parametrised (for example one case per
translation key or per attack query).

GitHub Actions runs two jobs on every push: **lint** (ruff, sqlfluff) and **test**, which builds
the database on PostGIS, runs the whole pipeline under coverage (with the grid from 2015 only), then all
tests, and writes the coverage table to the job summary. On that subset the two tests that need
decades of grid data (land vs ocean warming, the country comparison) skip, so CI reports
556 passed and 2 skipped.

A second, scheduled workflow (**Data freshness**, on the 16th of each month or on demand)
checks whether NASA has published a newer GISTEMP release than the committed snapshot
(`scripts/check_freshness.py`). It is check-only: the snapshot stays frozen for
reproducibility. On a new release it loads the data into a throwaway database and re-runs the
README findings; the run turns red only when a finding no longer holds, which is the cue to
adopt the release and update the text.

## Project structure

```text
app/                Streamlit app (main.py, views/, sql_guard.py, queries.py, i18n.py, ...)
data/raw/           NASA series snapshot + manifests (grid files are downloaded)
data/processed/     cleaned CSVs (generated)
database/           schema.sql, spatial_schema.sql, drivers_schema.sql, roles.sql
docs/               DATA.md, METHODS.md, PERFORMANCE.md (+ benchmark_results.json), SECURITY.md
docs/adr/           architecture decision records
scripts/            download, clean, load, grid, drivers, models, setup, benchmark and export scripts
sql/                SQL analysis library
tests/              pytest suites
Dockerfile          image for the Streamlit app (docker compose --profile app)
requirements*.txt   app only / app + pipeline + tests / + dev tools
```
## AI Assistance

Much of the code, tests, and documentation was drafted with assistance from Claude Opus 5.5
(Anthropic). I defined the scope, made the design decisions, and reviewed and tested every
change; the results are verified by the automated test suite.

## Data sources and license

- NASA GISS Surface Temperature Analysis (GISTEMP v4), https://data.giss.nasa.gov/gistemp/ —
  GISTEMP Team, 2026: GISS Surface Temperature Analysis (GISTEMP), version 4. NASA Goddard
  Institute for Space Studies. Dataset accessed 2026-11-21.
- Natural Earth 1:50m Admin 0 Countries, v5.1.2 — public domain, https://www.naturalearthdata.com/
- NOAA Climate Prediction Center, Oceanic Niño Index — https://www.cpc.ncep.noaa.gov/
- NOAA Global Monitoring Laboratory, Mauna Loa CO₂ — https://gml.noaa.gov/ccgg/trends/

The analysis-ready files (country series, trends and the annual grid) are published as a Kaggle
dataset: https://www.kaggle.com/datasets/zeynepsonmeez/global-and-country-temperature-anomalies-1880-2025
(DOI: 10.34740/kaggle/dsv/22679721), produced by `scripts/export_kaggle.py`.

Code: MIT License © 2026 Zeynep Sönmez. The data is subject to its providers' terms.
