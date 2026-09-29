# Open Terminal — Financial Research Platform

**Open Terminal** is a self-hosted financial research tool built for the individual investor. It connects directly to SEC filings, stock price data, and AI analysis to give you a Bloomberg-style interface without the Bloomberg price tag.

📺 **[Watch the Tutorial Video](https://youtu.be/B-LW_vZrOBY)**

---

## Table of Contents

1. [What It Does](#what-it-does)
2. [The Six Tabs](#the-six-tabs)
   - [Financials](#1-financials)
   - [Companies](#2-companies)
   - [Quadrant](#3-quadrant)
   - [AI Playground](#4-ai-playground)
   - [SQL Explorer](#5-sql-explorer)
3. [Data Sources](#data-sources)
4. [API Keys](#api-keys)
5. [Configuration](#configuration)
6. [Running the Server](#running-the-server)
7. [Architecture](#architecture)

---

## What It Does

Open Terminal pulls together three data streams into one interface:

- **SEC financial filings** — revenues, net income, assets, and dozens of other GAAP concepts, aggregated monthly going back years
- **Stock prices** — live via Polygon.io, or monthly averages from the built-in parquet archive when no key is provided
- **News with sentiment** — historical articles from Polygon with LLM-scored sentiment and reasoning, plus live articles for recent days

The data is pre-processed into a columnar parquet file and served through DuckDB in memory, so most queries return in milliseconds.

---

## The Six Tabs

### 1. Financials

The main research view. Select one or more tickers from the left sidebar, choose financial concepts (Revenue, Net Income, etc.), and a chart renders immediately.

**Price chart (top panel)**
- Loads live daily or monthly OHLC prices from Polygon when an API key is present
- Falls back to monthly average prices from the SEC parquet archive when no key is configured — labeled "Monthly avg (parquet)" in the chart header
- Supports Line and OHLC/Candlestick modes
- Multiple tickers are normalized to % change from period start for comparison

**Fundamentals chart (bottom panel)**
- Plots any combination of SEC financial concepts as line or bar charts
- Covers revenues, income, assets, liabilities, shares, market cap, and more
- Concepts can be filtered and searched in the left sidebar

**Merge mode**
Combines price and fundamentals onto a single dual-axis chart — price on the left axis, fundamentals on the right.

**Formulas tab**
Build custom metrics from existing concepts using Python-style arithmetic expressions. For example:

```
NetIncomeLoss / Revenues
```

Name it (e.g. "Profit Margin"), add it to your selection, and it plots alongside standard concepts. Formulas persist across sessions via localStorage.

**Data tab**
Shows the raw numbers behind the chart in a sortable table, with direct links to the original SEC filing for each data point.

**News tab**
Displays recent news articles for selected tickers. Each article shows:
- Title, publisher, date, and description
- Sentiment score (LLM-scored, range −10 to +10)
- Sentiment reason — hover over the score badge to see a one-sentence explanation of why the article received that score
- Relevance classification (Company Related vs. Industry Related)

When no Polygon API key is configured, a notice indicates that only historical parquet news is available.

---

### 2. Companies

A browseable directory of thousands of public companies, sourced from SEC CIK metadata and enriched with LLM-generated summaries and tags.

**Filtering**
- Keyword search across ticker, company name, sector tags, business summaries, and management discussion excerpts
- Tag chips let you filter by sector or theme (e.g. "semiconductors", "biotech")
- Results sort by relevance — exact ticker matches appear first

**Company cards** show:
- Business summary and company description
- Recent SEC filing date
- Current news with sentiment scores (same hover tooltip as the Financials tab)

**Use Displayed Tickers**
Once you have filtered down to the companies you want, click this button to add all currently visible companies to your active ticker selection — then proceed to Quadrant or Financials to compare them.

---

### 3. Quadrant

A scatter-plot view for comparing many companies across two financial dimensions simultaneously.

- Choose any two financial formulas for the X and Y axes (e.g. Net Income vs. Market Cap)
- Each dot is one company
- Optionally color dots by a third formula to visualize a category like profitability or leverage
- Click a dot or find a company in the legend to highlight it
- Drag-select a region of dots to isolate a subset — then keep only those companies in your active selection
- Log scale is on by default; toggle it off for linear comparison
- Optional regression line shows the trend across all plotted companies

This tab is the fastest way to screen a large universe of companies and find outliers.

---

### 4. AI Playground

A conversational interface backed by any model available on [OpenRouter](https://openrouter.ai), with full awareness of the financial database schema.

Ask plain-English questions like:
> "Show me the top growth stocks in the last five years with at least $50M in revenue"

The AI generates a SQL query against the `financial_data` table, executes it, and renders the result as a chart. You can then:

- **Use Displayed Tickers** — add the returned companies directly to your ticker selection
- **See Data Table** — send the query to the SQL Explorer tab for inspection or modification

The AI maintains conversation history so you can refine queries in follow-up messages. Supported models include GPT-4o, Claude, Gemini, and others via OpenRouter.

**Requires an OpenRouter API key** in the top bar.

---

### 5. SQL Explorer

Direct DuckDB query access to the underlying financial database for power users.

The main table is called `financial_data` and is in long/tall format:

| Column | Description |
|--------|-------------|
| `ticker` | Stock ticker symbol |
| `name` | Company name |
| `month_start_date` | First day of the reporting month |
| `concept` | GAAP concept name (e.g. `Revenues`, `NetIncomeLoss`) |
| `concept_label` | Human-readable label |
| `value` | Reported value |
| `stock_price_avg` | Monthly average stock price |
| `market_cap` | Estimated market cap for that month |
| `shares` | Share count |
| `annual_accessions` | Links to the SEC annual filing |
| `quarterly_accessions` | Links to the SEC quarterly filing |

**Tips:**
- Only `SELECT` queries are allowed
- Click any column name in the schema panel on the left to insert it into the editor
- `Ctrl+Enter` / `Cmd+Enter` runs the query
- Results are capped at 2,000 rows
- For multi-concept queries, join `financial_data` to itself filtering by `concept` — or ask the AI to write the query for you

---

## Data Sources

| Source | What it provides | Update frequency |
|--------|-----------------|-----------------|
| SEC EDGAR (via CIK) | Financial statements (GAAP concepts), filing metadata, company names | Weekly |
| Polygon.io | Live stock prices, news articles | Live (prices), Daily (news) |
| FRD (optional) | Minute-level and daily adjusted price history | On-demand |
| LLM (local Ollama or OpenRouter) | News sentiment scores, company descriptions, 10-K summaries | Weekly |

Financial data is pre-aggregated at the **month level** — each monthly value represents the most recently reported figure for that period, derived from both annual and quarterly filings.

---

## API Keys

Keys can be configured in `config.yaml` or entered directly in the top bar of the app. Keys entered in the UI are pre-filled from the server config and persist in the browser session.

| Key | Used for | Required? |
|-----|----------|-----------|
| **Polygon.io** | Live stock prices, live news articles | Optional — app works without it using parquet data |
| **OpenRouter** | AI Playground chat and query generation | Required for AI tab |

Without a Polygon key:
- Stock prices are served from the monthly parquet archive (labeled in the chart)
- News loads from the historical parquet; a notice indicates no live refresh

---

## Configuration

The server reads `config.yaml` in the working directory. All fields are optional and fall back to built-in defaults.

```yaml
app:
  name: Open Terminal

server:
  host: 0.0.0.0
  port: 3000
  debug: false

data:
  parquet_file: sec_filings_unified_monthly_top100.parquet
  meta_data_file: cik_metadata.parquet
  polygon_news_file: polygon_news.parquet
  load_mem_full: true     # load full parquet into RAM for fast queries

query:
  financials_row_limit: 5000
  sql_row_limit: 2000

api_keys:
  polygon: YOUR_POLYGON_KEY
  openrouter: YOUR_OPENROUTER_KEY

gate:
  enabled: false           # set true to require a math CAPTCHA on first visit
```

**`load_mem_full: true`** loads the entire parquet into a pandas DataFrame and registers it with DuckDB. This uses more RAM but makes all queries significantly faster. Set to `false` to let DuckDB query the file on disk directly (lower RAM, slower queries).

---

## Running the Server

**Requirements:** Python 3.10+, the packages in `requirements.txt`.

```bash
# Install dependencies
pip install -r requirements.txt

# Run with defaults (reads config.yaml in current directory)
python app.py

# Override port or config file
python app.py --port 8080 --config /path/to/config.yaml

# Production (gunicorn, 2 workers × 2 threads)
gunicorn --workers 2 --threads 2 --timeout 120 --bind 0.0.0.0:3000 app:app
```

The app serves at `http://localhost:3000` by default. If `gate.enabled: true` in config, new visitors must pass a simple arithmetic CAPTCHA before accessing the app.

---

## Architecture

```
Browser (script.js + styles.css)
        │
        │  REST / JSON
        ▼
Flask app (app.py)
        │
        ├── DuckDB (in-memory)  ←── financial_data parquet  (SEC + prices)
        ├── DuckDB (per-request) ←── polygon_news.parquet   (news + sentiment)
        ├── Polygon.io API       ←── live prices, live news
        └── OpenRouter API       ←── AI chart generation, chat
```

**Backend (app.py)**
- Flask with gunicorn in production
- DuckDB for in-memory SQL over parquet files
- A threading lock (`_duckdb_lock`) serializes all queries against the main financial table to keep DuckDB thread-safe
- News queries use independent DuckDB connections to avoid contention with the main lock

**Frontend (script.js)**
- Vanilla JavaScript — no framework
- Chart.js for line/bar/scatter charts
- Lightweight Charts (TradingView) for OHLC candlestick view
- Selections (tickers, concepts) persist in browser cookies across sessions
- Custom formulas persist in localStorage

**ETL pipeline (../src/)**
- Separate pipeline (run via `run_etl.sh`) pulls SEC data, Polygon news, and market cap
- Outputs parquet files that the Flask app reads at startup
- News sentiment is scored locally via Ollama (default: qwen3:8b) or any OpenRouter model
- Run `--classes A` daily for news, `--classes B` weekly for SEC financials
