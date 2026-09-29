# 📒 LedgerWise

**A bookkeeping & Excel-operations assistant for Virtual Assistants and bookkeepers.**

LedgerWise consolidates four legacy desktop scripts (double-entry bookkeeping, a
VLOOKUP-style merger, an Excel cleaner/pivoter, and a PDF/DOCX harvester) into a
single, modern, self-explanatory web app — built with **Streamlit**, **SQLite**
(SQLAlchemy), **Plotly**, and **pandas**.

> Designed for a non-developer end user: install once, run with one command, and
> everything is point-and-click with a dark, professional UI.

---

## ✨ Features

### Bookkeeping
- **Dashboard** — income/expense/net KPIs (month + fiscal YTD), trend & breakdown charts, recent activity, quick actions.
- **Journal Entries** — guided double-entry creation with a **live debit = credit** check, multi-line entries, edit/void/delete with an **audit trail**, and a **bulk entry** grid.
- **Chart of Accounts** — full CRUD, contra-account support, account numbering, Excel import/export. Seeded with a sensible default COA (migrated from the legacy script).
- **Reports** — Trial Balance, Income Statement (P&L), Balance Sheet, and Cash Flow, with preset/custom date ranges and **Excel + PDF export**.

### Excel & document tools (modernised legacy utilities)
- **Import Wizard** — drag-and-drop a CSV/Excel transaction list; auto-map columns, auto-categorize, detect duplicates, preview, then post to the ledger.
- **Merge** — *Key Join* (VLOOKUP-style, with SKU normalization) and *Stack* (append rows).
- **Clean & Pivot** — the "Standardizer" (date/status/money/name/ID/country fixers, each toggleable) plus an interactive pivot + chart builder.
- **Harvest** — extract tables from **PDF/DOCX** into a clean spreadsheet.

### 🤖 VA assistant tools
- **Transaction Categorizer** — keyword-rule suggestions for raw transactions; manage your own rules.
- **Anomaly Alerts** — flags duplicates, outliers, future-dated and unbalanced entries.
- **Month-End Checklist** — guided book-closing with progress tracking.
- **Quick Search** — full-text search across every journal line.

### Settings & data
- Company name, currency & symbol, date format, fiscal-year start, default cash account.
- **Backup/restore**: export everything to JSON, download the raw SQLite database, load demo data, or clear transactions.

---

## 🚀 Quick start

### Windows (one command)
```bat
run.bat
```
This creates a virtual environment in `.venv`, installs dependencies, and launches the app.

### macOS / Linux
```bash
./run.sh        # or:  make setup && make run
```

### Manual
```bash
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt   # Windows
# source .venv/bin/activate && pip install -r requirements.txt   # macOS/Linux
.venv\Scripts\python -m streamlit run app.py
```

Then open the URL Streamlit prints (default <http://localhost:8501>).

On first run the database is created automatically at `data/ledgerwise.db` and
seeded with a default Chart of Accounts, a month-end checklist, and categorizer
rules. Use **Settings → Data → Load sample data** to populate demo transactions.

---

## ⌨️ Keyboard shortcuts
`d` Dashboard · `n` New entry · `i` Import · `r` Reports · `/` Search
(ignored while typing in a field).

---

## ⚙️ Configuration

Copy `.env.example` to `.env` to override defaults:

| Variable | Purpose | Default |
|---|---|---|
| `LEDGERWISE_DATA_DIR` | Where the DB, logs, exports, backups live | `./data` |
| `LEDGERWISE_LOG_LEVEL` | `DEBUG`/`INFO`/`WARNING`/`ERROR` | `INFO` |

Runtime settings (company, currency, fiscal year…) are edited in-app and stored
in the database.

---

## 🗂️ Project structure

```
VA/
├── app.py                     # Streamlit entry point (navigation router)
├── requirements.txt           # dependencies
├── pyproject.toml             # packaging + tooling config
├── run.bat / run.sh / Makefile
├── .streamlit/config.toml     # dark theme
├── AUDIT_REPORT.md            # Phase 1 — legacy code audit
├── ARCHITECTURE.md            # Phase 2 — design
└── ledgerwise/
    ├── config.py              # paths & static defaults (pathlib)
    ├── logging_config.py      # rotating-file + console logging
    ├── core/                  # accounting domain (no UI)
    │   ├── accounts.py  journal.py  ledger.py  reports.py
    │   ├── categorizer.py  anomaly.py  search.py  checklist.py
    │   ├── periods.py  money.py
    ├── excel/                 # IO services
    │   ├── io_utils.py  importer.py  merger.py
    │   ├── cleaner.py  harvester.py  exporter.py
    ├── data/                  # persistence
    │   ├── models.py  database.py  seed.py  migrations.py  backup.py  schema.sql
    └── ui/                    # Streamlit layer
        ├── theme.py  components.py  state.py  nav.py
        └── pages/             # dashboard, journal, accounts, import_excel,
                               # reports, excel_tools, va_tools, settings
```

**Layering:** `ui → core/excel → data → foundation`. The domain (`core/`) is
Streamlit-free and unit-testable; the double-entry invariant lives only in
`core/journal.py`.

---

## 🔁 What happened to the old scripts?

See **`AUDIT_REPORT.md`** for a file-by-file audit and **`ARCHITECTURE.md`** for
the design. In short:

| Legacy script | Now lives in |
|---|---|
| `Excel_Bookkeeping.py` | `core/` accounting + Dashboard/Journal/Reports pages |
| `Excel_Merger_Connector.py` | `excel/merger.py` (Key Join + SKU cleaner) |
| `excel_cleaner.py` | `excel/cleaner.py` (Standardizer + Pivot) |
| `Excel_converter_Harvestor.py` | `excel/harvester.py` (generalised) |

The legacy flat-CSV storage is replaced by SQLite; `xlrd`-era Excel handling by
`openpyxl`/`XlsxWriter`; `print` debugging by `logging`; and hardcoded business
rules (SKU/status/country/name maps) became editable configuration.

---

## 🛠️ Tech stack
Streamlit · SQLAlchemy 2 (SQLite) · pandas · NumPy · Plotly · openpyxl ·
XlsxWriter · pypdf · python-docx · reportlab.

## 📄 License
MIT.
