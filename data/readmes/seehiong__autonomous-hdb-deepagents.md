# 🏢 Autonomous HDB DeepAgents

**A Multi-Agent Geospatial + Resale-Price Intelligence System for Singapore HDB Search**

This project provides an **autonomous DeepAgent pipeline** that processes natural-language queries like:

- "Find flats near Bukit Batok MRT"
- "Show me 4-room flats in Toa Payoh under 500k"
- "HDB near MRT within 600m with good value picks"

and turns them into:
1. Intent extraction (town, MRT station, flat type, max price, radius)
2. MRT resolver (maps MRT → nearest HDB planning area)
3. Resale flat retrieval over the seed CSVs
4. Geospatial enrichment (nearest MRT, parks, walkability)
5. Distance formatting and correction
6. LLM-powered summaries

All orchestrated end-to-end via **DeepAgents + LangGraph**.

---

# 🌳 Project Structure

```text
autonomous-hdb-deepagents/
│
├── pyproject.toml
├── .env.example                # copy to .env
├── .dockerignore
├── README.md
│
├── src/
│   └── autonomous_hdb_deepagents/
│       │   └── __init__.py
│       │
│       ├── agent/
│       │   ├── __init__.py
│       │   ├── cli.py                 # CLI entrypoint (uv run -m autonomous_hdb_deepagents.agent.cli)
│       │   ├── deep_agent.py          # DeepAgent factory + LangGraph orchestration pipeline
│       │   ├── intent.py              # LLM-powered intent extraction
│       │   ├── mrt_resolver.py        # MRT → HDB-town resolver
│       │   ├── resale.py              # HDB resale query node
│       │   ├── mrt.py                 # Geospatial enrichment node
│       │   ├── summary.py             # LLM summary generation node
│       │   ├── state.py               # PipelineState (Pydantic)
│       │   ├── config.py              # loads .env
│       │   ├── tools.py               # tool loader (file-backed)
│       │   ├── local_store.py         # SQLite + geo scan over the seed CSVs
│       │   └── llm.py                 # Shared LLM instance (ChatOpenAI); endpoint/model from .env
│       │
│       ├── api/
│       │   ├── __init__.py
│       │   ├── api_server.py          # FastAPI server providing /health + /query
│       │   └── api_server_launch.py   # Dev launcher: uvicorn with --reload
│       │
│       └── ui/
│           ├── __init__.py
│           └── gradio_app.py          # Gradio full-screen chat UI with sample questions
│
├── notebook/
│   ├── deepagents-multi-agent.ipynb
│   ├── deepagents-sub-agent.ipynb
│   ├── deepagents-custom-model.ipynb
│   └── data-ingestion/
│       ├── hdb-existing-building.ipynb
│       ├── hdb-property-info.ipynb
│       ├── lta-mrt-exits.ipynb
│       ├── moe-sg-schools.ipynb
│       ├── npark-parks.ipynb
│       └── onemap-geocoding-cache.ipynb
│
├── db/
│   ├── refresh_data.py         # one entry point for all data refreshes
│   ├── refresh_resale_data.py  # top up the CSVs from data.gov.sg
│   ├── refresh_geodata.py      # rebuild MRT exits + parks from data.gov.sg
│   ├── geocode_schools.py      # fill school coordinates from OneMap
│   ├── onemap.py               # shared OneMap client (rate limiting + cache)
│   ├── datagov.py              # shared data.gov.sg client (poll-download)
│   └── init/
│       └── data/              # Preprocessed CSV/GeoJSON from notebooks
│          └── *.csv
│
├── tests/
│   ├── test_local_store.py    # data layer: parsing, distance, query semantics
│   ├── test_valuation.py      # forecast parity + comparability rule
│   └── test_pipeline.py       # resolve -> resale -> mrt -> valuation
│
├── start.sh
├── Dockerfile
└── docker-compose.yml
```

# 📚 Data Ingestion & Processing Notebooks

This project includes a set of **fully reproducible data-ingestion notebooks** located under:
```bash
notebook/data-ingestion/
```

These notebooks document how each official dataset from **data.gov.sg**, **LTA**, **MOE**, **NParks**, and **OneMap** was:
1. Downloaded (CSV/GeoJSON/API)
2. Cleaned
3. Transformed and normalized
4. Converted into flat CSV tables
5. Written to `db/init/data/`

These notebooks serve as **transparent documentation** of all preprocessing logic and allow anyone to **rebuild the entire dataset from scratch**.

## Included Notebooks

| Notebook                      | Purpose                                                                 |
|-------------------------------|-------------------------------------------------------------------------|
| hdb-existing-building.ipynb   | Extracts and processes HDB existing building geometries and metadata.   |
| hdb-property-info.ipynb       | Loads HDB property information dataset and formats it as CSV.|
| lta-mrt-exits.ipynb           | Processes official LTA MRT exit GeoJSON and creates table-ready geometries. |
| moe-sg-schools.ipynb          | Processes MOE schools master list (locations, categories, addresses).   |
| npark-parks.ipynb             | Loads NParks parks boundaries/points and normalizes names + coordinates.|
| onemap-geocoding-cache.ipynb  | Generates and caches OneMap coordinate lookups to speed up ingestion.   |

# ⚙️ Installation

## 1. Install dependencies

```powershell
uv sync
```

This installs only the base `dependencies` (what the app needs to run),
including `python-dotenv` — required so `.env` (LLM endpoint, model paths,
etc.) actually gets loaded; without it, settings there are silently ignored
and the app falls back to defaults, which looks like a routing bug rather
than a missing dependency. `pytest` lives in the `dev` optional-dependency
group, so running `uv sync` again after `uv run --extra dev pytest ...` will
remove it — that's `uv` reconciling the env back to the base spec, not a
broken install. Use `uv sync --extra dev` (or `uv run --extra dev ...`)
whenever you need the test tooling present.

## 2. Install in editable mode
```powershell
uv add --dev --editable .
```

Now you can import:
```python
import autonomous_hdb_deepagents
```

# ⚡ Pipeline Overview (DeepAgents + LangGraph)

## 1️⃣ intent_node

Extracts:
- town
- mrt_station
- flat_type
- max_price
- mrt_radius

## 2️⃣ mrt_resolve_node

- Calls `get-mrt-towns`
- Resolves `"BB" → "BUKIT BATOK"`
- Auto-sets `town` if missing

## 3️⃣ resale_node

Uses `list-hdb-flats` to fetch:
- block
- street
- price
- coordinates

Defaults:
- flat_type="4 ROOM"
- max_price=600000
- town="TOA PAYOH" (fallback)

## 4️⃣ mrt_node (Geospatial Enrichment)

Uses:
```text
geospatial-query
```

Adds:
- nearest mrt
- distance raw
- formatted distance (e.g., `"367m"`, `"1.1km"`)

The backend reports its own unit (`dist_unit`) rather than mrt_node
guessing from magnitude -- an earlier heuristic that read any value under
1000 as PostGIS degrees inflated honest metre values 1000x.

## 5️⃣ summary_node

Every per-flat figure is rendered in **Python**, not by the model:

```
| # | Block / Street | Sold | Listed | ML estimate | Gap | Verdict | MRT | Area | Floor | Lease | Model | PSF |
```

The model receives only this table plus portfolio-level context, and writes
prose that interprets it — it is told not to restate any figure and is given no
per-flat data to restate. A prompt is advice rather than a constraint, so the
reliable fix is to leave nothing to transcribe.

LLM produces:
- price range
- closest flats
- best value picks
- meaningful insights

## 6️⃣ DeepAgent Orchestrator

Graph:
```text
intent → mrt_resolve → resale → mrt → valuation → summary → END
```

# 🔧 Agent Tools

The pipeline calls three tools:

## 1. Resale lookup
```text
list-hdb-flats
```

## 2. MRT → HDB town mapping
```text
get-mrt-towns
```

## 3. Geospatial nearest-mrt search
```text
geospatial-query
```

Loaded via `agent/tools.py`, which serves them from `agent/local_store.py`:

```python
from autonomous_hdb_deepagents.agent.tools import load_tools
tools = await load_tools()
```

There is no database and no tool server. `local_store.py` reads the seed CSVs
in `db/init/data/` directly -- SQLite (standard library) for the relational
queries, and a brute-force scan for the geospatial ones.

# 🧪 Tests

```powershell
uv run --extra dev pytest tests/ -q
```

127 tests, ~22 s:

| File | Covers |
|:---|:---|
| `test_local_store.py` | coordinate parsing, distance maths, query semantics, seed-layer health |
| `test_valuation.py` | row parsing, forecast parity with the browser engine, the time-comparability rule |
| `test_pipeline.py` | resolve → resale → mrt → valuation end to end |
| `test_geocoding.py` | OneMap building verification and the same-postal guard |
| `test_intent.py` | price normalisation ("$900k" must not become 900) |

Tests needing the trained model skip automatically when the sibling
`hdb-price-predictor` checkout is absent, so a bare clone still runs the
suite.

# 🧠 Design Principles
  
✔ Fully modular agent layers  
✔ Clear separation of concerns  
✔ State management via Pydantic  
✔ LangGraph deterministic pipeline  
✔ DeepAgent orchestration wrapper  
✔ Supports CLI, FastAPI and Gradio entry points  
✔ Clean Python package for reuse  

# 🚀 Running Autonomous HDB DeepAgents

The agent has no database. It reads the seed CSVs in `db/init/data/` directly,
so there is nothing to provision, migrate or keep running alongside it.

```text
┌──────────────────────────┐
│      Docker Host         │
│                          │
│  ┌──────────────┐        │
│  │ Backend API  │        │
│  │ (FastAPI)    │        │
│  └──────────────┘        │
│            ▲             │
│            │             │
│  ┌──────────────┐        │
│  │  Gradio UI   │        │
│  └──────────────┘        │
│            ▲             │
│            │             │
│  ┌──────────────┐        │
│  │ db/init/data │◄───────┼── seed CSVs, read at startup (~4 s)
│  │ + models/    │◄───────┼── XGBoost model from hdb-price-predictor
│  └──────────────┘        │
└──────────────────────────┘
```

## 🖥️ 1. Run locally (no Docker)

```powershell
cp .env.example .env    # set your LLM endpoint or key
```

No paths to set beyond that: the seed CSVs live in this repo, and the
XGBoost model resolves to `../hdb-price-predictor/models` when both repos are
checked out side by side. To point elsewhere, set `HDB_MODELS_DIR` in `.env`.

Three ways to talk to the agent, all reading the same `.env`:

### CLI

```powershell
uv run -m autonomous_hdb_deepagents.agent.cli "Find flats near Bukit Panjang MRT"
```

<details>
<summary>Example output</summary>

```text
[INTENT] Parsed intent -> {'town': None, 'mrt_station': 'Bukit Panjang', 'flat_type': None, 'max_price': None, 'mrt_radius': None}
[MRT-RESOLVE] Resolving MRT station: Bukit Panjang
[MRT-RESOLVE] BP -> BUKIT PANJANG
[RESALE] Fetching 4 ROOM in BUKIT PANJANG <= 600000...
[RESALE] Retrieved 30 flats
[MRT] Enriching 30 flats (radius=800)
[MRT] Example: BT PANJANG RING RD -> BANKIT LRT STATION (162m)
[SUMMARY] Summarizing 30 flats

=== FINAL RESPONSE ===

### **Flats Near Bukit Panjang MRT: Summary**
...
```
</details>

### FastAPI

```powershell
uv run python src/autonomous_hdb_deepagents/api/api_server_launch.py
```

```powershell
curl http://localhost:8000/health

Invoke-RestMethod -Uri "http://localhost:8000/query" -Method Post `
  -Body '{"query":"Find flats near Bukit Batok MRT"}' `
  -ContentType "application/json"
```

`api_server_launch.py` runs with `--reload`, for local development; the
Dockerfile / `start.sh` path runs `uvicorn` directly without it.

### Gradio UI

```powershell
uv run python -m autonomous_hdb_deepagents.ui.gradio_app
```

```text
* Running on local URL:  http://0.0.0.0:7860
```

`0.0.0.0` (set in `gradio_app.py`'s `demo.launch(...)`) is a deliberate
choice, not a default you need to change: it binds every network interface,
so the UI is reachable from other machines on your LAN -- convenient if,
like the local-llama-server setup above, your model runs on a different box.
It also means anyone on that LAN can reach port 7860 with no authentication;
open http://localhost:7860 yourself, and if you don't want LAN-wide access,
change it to `server_name="127.0.0.1"` in `gradio_app.py`.

| Component | Port |
|-----------|------|
| FastAPI   | 8000 |
| Gradio UI | 7860 |

## 🐳 2. Run with Docker

```powershell
cp .env.example .env    # compose reads it via env_file
docker-compose up
```

- Gradio UI → http://localhost:7860
- FastAPI docs → http://localhost:8000/docs

`.dockerignore` keeps `.env`, `.venv`, the seed CSVs and the test suite out of
the build context — 483 MB down to 0.5 MB.

`build: .` means compose builds from the local Dockerfile; the
`seehiong/...` name is only a tag, so nothing is pulled or pushed. Push only
after the image works.

Verified: 2.16 GB image, ~277 MB resident with all 985k rows loaded, both
mounts read-only inside the container, and the same valuations as a host run.
A LAN llama-server in `HDB_LLM_BASE_URL` is reachable from the container.

The compose file mounts `db/init/data/` and the sibling repo's `models/`
read-only, so refreshing either is a restart rather than a rebuild.

### Using the published image

`docker-compose.yml`'s `build: .` means `docker-compose up` always builds
locally and never pulls from Docker Hub -- the `image:` line is only a tag
for the local build result. A public image is also published at
[`seehiong/autonomous-hdb-deepagents-backend`](https://hub.docker.com/r/seehiong/autonomous-hdb-deepagents-backend)
for anyone who wants to skip the build:

```powershell
docker pull seehiong/autonomous-hdb-deepagents-backend:latest
docker run --rm -p 8000:8000 -p 7860:7860 `
  --env-file .env `
  -v "$($PWD.Path)\db\init\data:/app/db/init/data:ro" `
  -v "$($PWD.Path)\..\hdb-price-predictor\models:/app/models:ro" `
  seehiong/autonomous-hdb-deepagents-backend:latest `
  bash /app/start.sh
```

Same mounts and `.env` as `docker-compose up` -- the image itself carries no
data or model, so both still need to be supplied at run time (a bare pull and
run without them gives you an app that starts but has nothing in
`/app/db/init/data` or `/app/models`). Building locally
(`docker-compose build`) is the more reliable path if you're actively
changing the code; the published tag only updates when someone pushes it, so
it can lag a fresh clone by however long since the last push.

## 📁 3. Configuration

Copy the example and edit:

```powershell
cp .env.example .env
```

`.env` is loaded at import time and is git-ignored. Real environment variables
win over it, so docker-compose and CI override without editing the file.

| Variable | Default | Purpose |
|:---|:---|:---|
| `OPENROUTER_API_KEY` | — | hosted LLM key; omit for a local server |
| `HDB_LLM_BASE_URL` | OpenRouter | any OpenAI-compatible endpoint |
| `HDB_LLM_MODEL` | `nvidia/nemotron-3.5-lightning:free` | model name or alias |
| `HDB_LLM_API_KEY` | falls back to `OPENROUTER_API_KEY` | key for a non-OpenRouter endpoint |
| `HDB_DATA_DIR` | `db/init/data` | seed CSVs the agent queries |
| `HDB_MODELS_DIR` | `../hdb-price-predictor/models` | XGBoost model + scaler |
| `HDB_RESALE_CSV` | sibling repo's fetched copy | source for `db/refresh_resale_data.py` |

### Using a local llama-server

A local model needs no key and is not rate limited, which suits a pipeline that
makes two LLM calls per query:

In `.env`:

```ini
HDB_LLM_BASE_URL=http://<host>:8081/v1
HDB_LLM_MODEL=<the --alias llama-server was started with>
```

```bash
llama-server-rocm --model ~/models/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-UD-Q4_K_XL.gguf \
  --alias nemotron-3.5-lightning --n-gpu-layers 99 --ctx-size 32768 \
  --flash-attn on --jinja --host 0.0.0.0 --port 8081
```

The model only writes prose — every figure in the answer is rendered in Python
(see below) — so a quantised local model is enough. Expect 2-4 minutes per
query on one GPU versus roughly 40 s via a hosted endpoint.

**Note on model choice.** Hosted free models are rate limited and can be
withdrawn without notice. If replies start failing, check
https://openrouter.ai/models and set `HDB_LLM_MODEL` to something current;
`amazon/nova-2-lite-v1` (paid, about $0.30/M input) is a reliable equivalent.

Resale CSVs are discovered by glob (`resale_flat_price_*.csv`), so adding a
file is enough -- no code change.

## ♻️ 4. Refreshing the data

One command checks everything and reports what is stale:

```powershell
uv run python db\refresh_data.py            # dry run
uv run python db\refresh_data.py --apply    # write changes
uv run python db\refresh_data.py --apply schools   # one stage only
```

Every stage is **dry-run by default** and **idempotent** -- re-running when
nothing is stale does nothing, and nothing is written without `--apply`.

| Stage | Source | What it does |
|:---|:---|:---|
| `resale` | data.gov.sg `d_8b84c4ee58e3cfc0ece0d773c8ca6abc` | adds months newer than the newest already present, to a per-year CSV |
| `geodata` | data.gov.sg -- LTA `d_b39d3a087...`, NParks `d_0542d48f0...`, MOE `d_688b934f8...` | rebuilds `mrt_exits.csv`, `sg_parks.csv`, `sg_schools.csv` |
| `schools` | OneMap | geocodes any school still missing coordinates |

**Stage order matters.** MOE publishes no coordinates, so `geodata` carries the
existing ones across by postal code and leaves relocated or newly added schools
blank; `schools` then fills those from OneMap. Running `refresh_data.py` with
no stage argument does both in that order.

### Command reference

Every script takes `--apply`; without it you get a dry run that reports what
would change.

| Command | What it does |
|:---|:---|
| `db\refresh_data.py` | all stages, in dependency order |
| `db\refresh_data.py resale\|geodata\|schools` | selected stages only |
| `db\refresh_resale_data.py` | resale months only (`--csv`, `--data-dir` to override paths) |
| `db\refresh_geodata.py [mrt\|parks\|schools]` | rebuild reference layers (`--force` to allow a sharp shrink) |
| `db\geocode_schools.py` | geocode schools missing coordinates (`--limit N` for a trial) |
| `db\geocode_schools.py --reverify` | re-check schools that already have coordinates |

A typical full refresh:

```powershell
# 1. pull new resale months into the sibling repo
uv run python ..\hdb-price-predictor\pipeline_public\01_fetch_data.py

# 2. see what is stale here
uv run python db\refresh_data.py

# 3. apply it
uv run python db\refresh_data.py --apply

# 4. confirm the data is sound
uv run --extra dev pytest tests/ -q
```

Then restart the agent. Step 4 matters: the suite checks that no seed CSV has
duplicate rows, that every school has coordinates (which fails if `geodata` ran
without `schools`), and that the two manually-corrected school positions
survived.

### Reference layers (`geodata`)

`mrt_exits.csv`, `sg_parks.csv` and `sg_schools.csv` are small and fully
published, so they are **rebuilt** from source rather than topped up:

```powershell
uv run python db\refresh_geodata.py                  # dry run: compare to current
uv run python db\refresh_geodata.py --apply          # rebuild every layer
uv run python db\refresh_geodata.py --apply schools  # one layer
```

data.gov.sg serves these two different ways, and which applies is a property of
the dataset rather than a choice:

| Layer | Endpoint |
|:---|:---|
| MRT exits, parks | **poll-download** -- file datasets, returns a signed S3 URL |
| Schools | **datastore_search** -- a table, fetched in sorted pages |

`db/datagov.py` handles both. It validates before returning -- JSON is parsed
before any write, and a datastore fetch checks the row count against the total
the API reports, so a short read cannot be written as a complete table -- and
backs off exponentially on HTTP 429 (these endpoints do rate limit).

A rebuild that would shrink a layer by more than 20% is **refused** unless
`--force` is passed, so an upstream outage returning a near-empty layer cannot
quietly gut the data.

Column layouts are preserved exactly, including the SVY21 `geom_3414` / `x` /
`y` columns, so the agent reads the result with no code change.

### Pulling genuinely new months

`refresh_data.py` reads the resale CSV that the sibling repo fetches. To get
new months from data.gov.sg first:

```powershell
uv run python ..\hdb-price-predictor\pipeline_public\01_fetch_data.py
uv run python db\refresh_data.py --apply
```

Then restart the agent -- resale CSVs are discovered by glob, so a new file
needs no code change.

### OneMap geocoding

`db/onemap.py` is a small client shared by the geocoding stages. It mirrors the
pacing the sibling repo uses to resolve 12,847 postal codes without being
blocked:

| Behaviour | Value | Why |
|:---|:---|:---|
| Delay between requests | 1.2 s | the pace the sibling pipeline has run at successfully |
| Retry on HTTP 429 | `1.2s x 2^attempt`, 3 attempts | exponential backoff rather than hammering |
| Cache | successes only | a rate-limited or interrupted run resumes by re-running |
| Checkpoint | every 250 lookups | an interrupted run keeps the work it did |

No API key is needed: OneMap's `/common/elastic/search` endpoint is public.
(Some OneMap endpoints do require a Bearer token -- `/public/revgeocode`
returns 401 without one -- but this one does not, and nothing here reads
credentials.)

Caches live beside the data as `db/init/data/.onemap_*_cache.json`. Deleting a
cache forces a full re-geocode; keeping it makes the next run instant.

**Rate-limit etiquette:** raising `ONEMAP_DELAY_S` to go faster is the wrong
lever -- the cache is what makes repeat runs fast. The full 337-school run
takes about 7 minutes once, then costs nothing.

### Geocoding schools directly

```powershell
uv run python db\geocode_schools.py                  # report what is missing
uv run python db\geocode_schools.py --apply          # geocode and write
uv run python db\geocode_schools.py --apply --limit 20     # small trial first
uv run python db\geocode_schools.py --apply --reverify     # re-check existing
```

Coordinates are written as `POINT (lon lat)` WKT into `geom_4326`, matching
`sg_parks.csv`, and results outside Singapore's bounds are rejected rather than
written.

**Every result is verified.** A postal-code lookup returns the *first* match
for that code, which is not always the school -- some campuses share a postal
code with a neighbouring institution:

| Postal | OneMap returns | Actual school | Error |
|:---|:---|:---|---:|
| 487012 | ALL SAINTS' CHURCH | Anglican High School | 108 m |
| 678117 | BOYS' TOWN | Assumption English School | 164 m |

When the building OneMap names does not look like the school, the school
**name** is searched instead, and the result is used only if it resolves to the
same postal code -- so a same-named school at a different site can never be
substituted. Both cases above are corrected automatically. `--reverify`
re-checks schools that already have coordinates, and rewrites only those that
actually move.

## ✅ 5. Confirming it works

### In UI:

You should be able to run:
```text
Find cheapest 5-room flats near Punggol MRT under 600k
```

# ⚠️ Known limitations

- **`list-hdb-flats` returns past transactions**, not current listings
  (`ORDER BY month DESC LIMIT 30`). For "what's on the market" questions this
  is the wrong dataset — it answers "what recently sold".
- **Private condo (URA) valuation is not integrated.** `condo_model.bst` needs
  `project_psf` / `street_psf` aggregates derived from URA caveats, which
  data.gov.sg does not publish; the sibling repo sources them from a Kaggle
  CC BY 4.0 redistribution or a URA API key. `_forecast_adjustment` would also
  need the segment-specific CCR/RCR/OCR growth rates in `condo_scaler.json`.
- **Outram Secondary is a split site** during its relocation (3 York Hill until
  2027, 48 Anchorvale Crescent from 2026). The data holds one coordinate per
  school and carries the new campus; nothing models two sites.
- **Startup re-parses ~985k CSV rows on every process start** (~4-5 s).
  Caching the built SQLite file on disk, keyed by the CSVs' mtimes, would make
  restarts near-instant. Paid once per process, not per query.
- **No parity fixture runs the valuation against `app.js` output directly.**
  `test_valuation.py` asserts the same *formula*, which catches drift in this
  port but not a change on the browser side.

# 📊 Data Sources & Citations

This project uses publicly available datasets from Singapore’s Housing & Development Board (HDB) provided via **data.gov.sg** under the Singapore Open Data Licence.

Please cite the following datasets if you use this project in research, reports, publications, or derivative works:

## APA Citations

- Housing & Development Board. (2016). Resale Flat Prices (Based on Approval Date), 1990–1999 (2024) [Dataset]. data.gov.sg.
Retrieved December 7, 2025, from https://data.gov.sg/datasets/d_ebc5ab87086db484f88045b47411ebc5/view

- Housing & Development Board. (2016). Resale Flat Prices (Based on Approval Date), 2000–Feb 2012 (2024) [Dataset]. data.gov.sg.
Retrieved December 7, 2025, from https://data.gov.sg/datasets/d_43f493c6c50d54243cc1eab0df142d6a/view

- Housing & Development Board. (2016). Resale Flat Prices (Based on Registration Date), From Mar 2012 to Dec 2014 (2024) [Dataset]. data.gov.sg.
Retrieved December 7, 2025, from https://data.gov.sg/datasets/d_2d5ff9ea31397b66239f245f57751537/view

- Housing & Development Board. (2017). Resale Flat Prices (Based on Registration Date), From Jan 2015 to Dec 2016 (2024) [Dataset]. data.gov.sg.
Retrieved December 7, 2025, from https://data.gov.sg/datasets/d_ea9ed51da2787afaf8e51f827c304208/view

- Housing & Development Board. (2021). Resale flat prices based on registration date from Jan-2017 onwards (2025) [Dataset]. data.gov.sg.
Retrieved December 7, 2025, from https://data.gov.sg/datasets/d_8b84c4ee58e3cfc0ece0d773c8ca6abc/view

- Housing & Development Board. (2018). HDB Property Information (2025) [Dataset]. data.gov.sg. Retrieved December 7, 2025 from https://data.gov.sg/datasets/d_17f5382f26140b1fdae0ba2ef6239d2f/view

- National Parks Board. (2023). Parks [Dataset]. data.gov.sg. Retrieved September 16, 2026 from https://data.gov.sg/datasets/d_0542d48f0991541706b58059381a6eca/view

- Ministry of Education. (2017). General information of schools [Dataset]. data.gov.sg. Retrieved September 16, 2026 from https://data.gov.sg/datasets/d_688b934f82c1059ed0a6993d2a829089/view

- Land Transport Authority. (2019). LTA MRT Station Exit (GEOJSON) [Dataset]. data.gov.sg. Retrieved September 16, 2026 from https://data.gov.sg/datasets/d_b39d3a0871985372d7e1637193335da5/view

- Singapore Land Authority. OneMap API. Retrieved September 16, 2026 from
  https://www.onemap.gov.sg/ — school coordinates in `sg_schools.csv` were
  geocoded from their postal codes via OneMap's public search endpoint
  (`db/geocode_schools.py`).

## 📘 Notes on Dataset Usage

- Data is provided under the **Singapore Open Data Licence**.
- Map data and geocoding results are from **OneMap, © Singapore Land
  Authority**, used under the
  [OneMap API terms](https://www.onemap.gov.sg/legal/opendatalicence.html).
- Users are permitted to **reuse, modify, and redistribute** these datasets.
- Proper **attribution must be given**, as included above.
- This project aggregates, normalizes, and enriches the datasets into flat CSV tables the agent queries directly.