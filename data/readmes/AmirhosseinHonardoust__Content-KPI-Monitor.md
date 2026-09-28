# Mini Content KPI Monitor (SQL + Python + Streamlit)

A compact, production‑quality analytics project for tracking **content performance**.  
It ingests a single CSV of daily metrics into **SQLite**, computes KPIs in a SQL view, and serves a **Streamlit** dashboard to explore **CTR**, **Conversion Rate**, **Dwell Time**, and **Bounce Rate** with filtering and drill‑downs.

---

## Highlights
- **Simple data model** (`content_daily`) with a **derived SQL view** `v_content_kpi` that calculates `ctr` and `conversion_rate`.
- **One‑command ETL** from CSV → SQLite (idempotent, safe upserts).
- **Streamlit dashboard** with:
  - KPI tiles
  - CTR trend over time
  - Conversion Rate by category
  - Top content table (sortable, filterable)
- **Future‑proofed UI**: `st.plotly_chart(..., config=...)` (no deprecated args).

---

## Architecture
```
CSV  ──▶  Python ETL  ──▶  SQLite (content_daily, v_content_kpi)  ──▶  Streamlit app
```

**Folders**
```
mini-content-kpi/
├─ app/
│  └─ streamlit_app.py        # Dashboard (Streamlit + Plotly)
├─ data/
│  ├─ raw_metrics.csv         # Input CSV (can be regenerated)
│  └─ content_kpi.db          # SQLite database (created by ETL)
├─ sql/
│  └─ schema.sql              # Table + view definitions
├─ src/
│  ├─ generate_sample.py      # Generates example CSV
│  └─ ingest_and_export.py    # ETL: CSV → SQLite
└─ requirements.txt
```

---

## Data Model & KPIs

**Table: `content_daily`**
- `date` (YYYY‑MM‑DD), `content_id`, `title`, `category`
- `impressions` (int), `clicks` (int), `conversions` (int)
- `avg_dwell_sec` (float), `bounce_rate` (0 – 1)

**View: `v_content_kpi`** (defined in `sql/schema.sql`)
```sql
SELECT
  date, content_id, title, category,
  impressions, clicks, conversions, avg_dwell_sec, bounce_rate,
  CASE WHEN impressions > 0 THEN 1.0 * clicks / impressions ELSE 0 END AS ctr,
  CASE WHEN clicks > 0 THEN 1.0 * conversions / clicks ELSE 0 END AS conversion_rate
FROM content_daily;
```
**Formulas**
- **CTR** = `clicks / impressions`
- **Conversion Rate (CR)** = `conversions / clicks`

---

## Quickstart

### 1) Create & activate a virtual env
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
# source .venv/bin/activate
```

### 2) Install dependencies
```bash
pip install -r requirements.txt
```

### 3) Generate example data (optional)
```bash
python src/generate_sample.py
```
Creates `data/raw_metrics.csv` for 30 days across a few demo articles.

### 4) Ingest CSV → SQLite
```bash
python src/ingest_and_export.py --csv data/raw_metrics.csv --db data/content_kpi.db --schema sql/schema.sql
```

### 5) Launch the dashboard
```bash
streamlit run app/streamlit_app.py
```
Open the URL shown in the terminal (usually `http://localhost:8501`).

---

## Dashboard Guide

### KPI Tiles
- **Impressions**, **Clicks**, **Conversions**, **Avg Dwell (s)**, **Bounce Rate**  
- CTR and CR deltas are annotated alongside Clicks/Conversions.

### CTR Over Time (line)
- Tracks daily CTR under current filters (date range, category, title search).  
- Useful for spotting spikes and dips; investigate content around peaks.

### Conversion Rate by Category (bar)
- Compares mean CR by category to prioritize content themes.

### Top Content (table)
- Sorted by CTR. Includes CR, dwell time, bounce.  
- Use sidebar filters to narrow by date range or category.

---

### Dashboard Preview

#### Full Dashboard Overview
<img width="1341" height="513" alt="Screenshot 2025-10-28 at 09-50-40 Content KPI Monitor" src="https://github.com/user-attachments/assets/c145b79f-9538-4dbe-9045-2f70d4605205" />

---

#### Top Content Table
<img width="1021" height="424" alt="Screenshot 2025-10-28 at 09-49-58 Content KPI Monitor" src="https://github.com/user-attachments/assets/f0e5d6fe-e3d1-451c-b44f-757be77b15b9" />

---

## CSV Format (required header)
File path: `data/raw_metrics.csv`
```csv
date,content_id,title,category,impressions,clicks,conversions,avg_dwell_sec,bounce_rate
2025-10-01,A101,"10 Tips to Brew Coffee",Lifestyle,1200,180,25,42,0.38
```
- `bounce_rate` is a fraction (e.g., `0.38` = 38%).

---

## CLI Reference

### Generate sample data
```bash
python src/generate_sample.py
```

### Ingest any CSV into SQLite
```bash
python src/ingest_and_export.py   --csv data/raw_metrics.csv   --db data/content_kpi.db   --schema sql/schema.sql
```

**Behavior**
- Safely **replaces** rows for the same `(date, content_id)` (idempotent).  
- Validates numerics and fills non‑parsable values with 0 to keep the pipeline robust.

---

## Validation & Troubleshooting

- **No data in dashboard?** Ensure you ran the ETL step and `data/content_kpi.db` exists.
- **Deprecation warnings?** Already mitigated: we do not use `use_container_width` or other deprecated kwargs. If you add new charts, pass only `config=...`.
- **Wrong CTR/CR values?** Confirm the CSV has integer `impressions`, `clicks`, `conversions` and that `bounce_rate` is 0–1, not 0–100.

---

## Exporting / Sharing
- Use Streamlit’s “⋮” menu on each chart to **download PNG** or data.
- To export the view for BI tools:
  ```python
  # Example: dump v_content_kpi to CSV
  import sqlite3, pandas as pd
  con = sqlite3.connect("data/content_kpi.db")
  df = pd.read_sql_query("SELECT * FROM v_content_kpi", con)
  df.to_csv("data/kpi_export.csv", index=False)
  con.close()
  ```

---

## Roadmap
- Segmentation (device/source/region)
- Content cohort retention
- Uplift / A/B test summaries
- Anomaly detection on CTR/CR
- Auto‑email/PDF weekly report
