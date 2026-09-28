# MarketCalls Terminal

A free, open-source stock market terminal that runs entirely on your own
computer. It gives you a Zerodha Kite-style dark dashboard with live-ish
quotes, TradingView-style candlestick charts, technical indicators, trend
analysis, and NIFTY 50 market breadth - all powered by free Yahoo Finance
data. No broker account, no API keys, no sign-up.

![MarketCalls Terminal](screenshots/dashboard.png)

This is a research and charting tool only. It does not place orders and it
is not investment advice.

## What you get

- **Watchlist** with live prices, day change, and mini sparkline charts,
  refreshed every few seconds. Add or remove any NSE stock or index.
- **Charts** for any symbol with 5m / 15m / 1H / Daily / Weekly / Monthly
  timeframes and range presets from 5 days to 5 years.
- **Indicators** you can toggle on and off live: SMA, EMA (20/50/200),
  Bollinger Bands, Supertrend, VWAP, RSI, MACD, ADX, and ATR.
- **Trend panel** that scores every watchlist symbol from -100 to +100 and
  tells you exactly why (price vs EMAs, RSI zone, MACD, ADX strength).
- **Top movers and market breadth** for the NIFTY 50 universe: gainers,
  losers, most active, advance/decline, and % of stocks above key EMAs.
- **Quick search** with Ctrl+K (or /) to switch charts or add symbols.

## Before you start

You need two things installed:

| Tool | What it is | Get it |
|---|---|---|
| **uv** | A fast Python package manager (installs Python for you too) | see below |
| **Node.js 20+** | JavaScript runtime for the frontend | [nodejs.org](https://nodejs.org) |

### Install uv

**macOS / Linux** (paste in Terminal):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows** (paste in PowerShell):

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Close and reopen your terminal afterwards, then check it works:

```bash
uv --version
```

## Setup (one time)

The app has two parts: a Python **backend** (fetches market data) and a
React **frontend** (the dashboard you see). You will run them in two
separate terminal windows. The commands below are the same on macOS and
Windows.

### 1. Get the code

```bash
git clone https://github.com/marketcalls/trading-terminal.git
cd trading-terminal
```

(No git? Click "Code > Download ZIP" on GitHub and unzip it instead.)

### 2. Set up the backend

```bash
cd backend
uv venv
uv pip install -r requirements.txt
```

`uv venv` creates an isolated Python environment in a `.venv` folder, and
`uv pip install` puts all the required packages into it. If you don't have
Python installed, uv downloads it for you automatically.

### 3. Set up the frontend

Open a second terminal:

```bash
cd trading-terminal/frontend
npm install
```

## Run it (every time)

**Terminal 1 - backend:**

```bash
cd trading-terminal/backend
uv run uvicorn app.main:app --host 127.0.0.1 --port 8000
```

`uv run` automatically uses the `.venv` you created - no need to activate
anything.

**Terminal 2 - frontend:**

```bash
cd trading-terminal/frontend
npm run dev
```

Now open **http://127.0.0.1:5173** in your browser. You should see the
terminal with a NIFTY 50 chart and a pre-loaded watchlist.

## How to use it

- **Switch charts**: click any watchlist row, or press `Ctrl+K` (macOS:
  `Cmd+K`) or `/` and search.
- **Add a stock**: press `Ctrl+K`, type a name or NSE symbol (e.g.
  `RELIANCE` or `TATASTEEL`), and pick "Add". Plain symbols are treated as
  NSE; indices use Yahoo tickers like `^NSEI` (NIFTY 50).
- **Remove a stock**: hover over its watchlist row and click the X.
- **Change timeframe**: use the `5m 15m 1H D W M` buttons above the chart;
  the second group (5D-5Y) controls how much history is loaded.
- **Indicators**: click the toolbar buttons (SMA 20, EMA 50, RSI, MACD...)
  to add or remove them live. RSI/MACD/ADX/ATR open their own panes below
  the price chart. VWAP works on intraday timeframes only.
- **Right panel**: Trend (tap a row to see the "why" behind the score),
  Top Movers (click a stock to chart it), and Breadth.

## Configuration (optional)

Defaults work out of the box. To change them, edit `backend/.env`:
poll interval, cache lifetimes, database path, and the default watchlist
are all configurable. The NIFTY 50 scan universe is a simple editable list
in `backend/app/symbols.py`.

## API reference

The backend is a regular REST API you can also use directly:

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/health` | liveness check |
| GET/POST | `/api/watchlist` | list / add symbol |
| DELETE | `/api/watchlist/{id}` | remove symbol |
| GET | `/api/quotes?symbols=A,B` | batch LTP, change %, sparkline |
| GET | `/api/chart/{symbol}?interval=1d&range=6mo` | OHLCV bars |
| GET | `/api/chart/{symbol}/indicators?names=EMA20,RSI14` | indicator series |
| GET | `/api/analysis/trend/{symbol}` | trend score + signals |
| GET | `/api/analysis/trend/watchlist` | trend for all watchlist symbols |
| GET | `/api/analysis/top-movers?type=gainers` | universe movers scan |
| GET | `/api/analysis/breadth` | advance/decline and EMA breadth |

Interactive API docs are at http://127.0.0.1:8000/docs while the backend
is running.

## Troubleshooting

- **"No data found for XYZ.NS"** - the symbol doesn't exist on Yahoo
  Finance (typo, or the ticker changed after a corporate action).
- **TA-Lib fails to install** - recent versions install cleanly from pip
  wheels. On macOS, if it still fails, run `brew install ta-lib` first and
  retry `uv pip install -r requirements.txt`.
- **Port already in use** - something else is on 8000 or 5173. Stop it, or
  change the port (`--port 8001` for the backend; update the proxy target
  in `frontend/vite.config.ts` to match).
- **Charts look stale** - Yahoo data is delayed and the app caches
  aggressively (quotes 15s, bars 5min, universe scan 3min) to respect rate
  limits. This is by design; don't poll faster.
- **Blank page in the browser** - make sure BOTH terminals are running and
  you opened http://127.0.0.1:5173 (not :8000).

## Tech stack

FastAPI, yfinance, TA-Lib, SQLite (sqlmodel) on the backend; React 19,
Vite, TailwindCSS, shadcn/ui, lightweight-charts v5, TanStack Query, and
zustand on the frontend.

## Disclaimer

Market data comes from Yahoo Finance via the yfinance library, is delayed,
and may be inaccurate. This software is for education and research only and
is not investment advice.
