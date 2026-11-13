# Antigravity Token Monitor

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Zero Dependencies](https://img.shields.io/badge/Backend-Python%203%20Stdlib-green.svg)](#architecture)
[![macOS App](https://img.shields.io/badge/macOS-Cocoa%20%2B%20WKWebView-black.svg)](#native-macos-app)

A **zero-dependency, local-first, real-time Token & API Value Monitoring Dashboard** for Google Antigravity — available both as a standalone **native macOS Desktop + Menu Bar App** (`AntigravityTokenMonitor.app`) and a **cross-platform Web UI** (`http://127.0.0.1:18923`).

---

## Features

- **Real-Time Incremental Telemetry (`<1ms` cached scan)**
  - Directly reads `~/.gemini/antigravity/conversations/*.db` (including live `-wal` pages) and `conversation_summaries.db` in **read-only** SQLite URI mode (`?mode=ro`).
  - Tracks `(mtime_ns, size)` across both `.db` and `.db-wal` files so unchanged sessions are skipped cleanly while active conversations update within milliseconds.
  - Displays active windows (`5m`) and live 15-minute burn rates (`tok/min` and `$/hr`).
- **Time Windows & Adaptive Trend Granularity**
  - Built-in presets: `近 7 天 (last_7d)`, `本周一 (since_monday)`, `今日 (today)`, `近 24 小时 (last_24h)`, `近 5 小时 (last_5h)`, `近 1 小时 (last_1h)`, `全部历史 (all_time)`, and `自定义区间 (custom)`.
  - Automatically switches trend chart aggregation between `daily`, `hourly`, `15m`, and `5m` buckets depending on the selected span, with interactive hover tooltips.
- **Multi-Dimensional Pricing & Currency**
  - Switch live across **4 valuation modes**: Promo + Cache (`promo`), Official Standard + Cache (`std`), Promo Without Cache Equivalent (`nc_promo`), and Standard Without Cache Equivalent (`nc_std`), plus `generate_image` unit accounting.
  - Instant `$ USD` / `¥ CNY` toggle with editable exchange rate and timezone selector (`Local` / `UTC+8` / `UTC+0` / `UTC-8`).
- **Rich Visual Analytics & Exports**
  - 4 KPI summary cards (with value-change flash feedback), toggleable Model Distribution Donut Chart (Tokens vs API Cost), 4-part Cost Breakdown stacked bar & pricing ladder, sortable Full-Precision Model Table, Root Window Ranking, and Latest 30 Live Call Feed with search filter.
  - Export full reports to **CSV** (`/api/export.csv`) or save a **PNG Snapshot** directly to Desktop.
- **100% Self-Contained & Private**
  - Pure Python 3 standard library backend (`monitor_server.py`) and zero-CDN embedded HTML/CSS/SVG/JS frontend (`index.html`). No npm, no pip packages, no external network calls, and zero telemetry ever leaves your machine.

---

## Quick Start

### Option 1: Web Dashboard (macOS / Linux / Windows)

Requires only **Python 3.8+**:

```bash
git clone https://github.com/STARKTANG108/antigravity-token-monitor.git
cd antigravity-token-monitor
python3 monitor_server.py --host 127.0.0.1 --port 18923
```

Open **http://127.0.0.1:18923** in any browser.

### Option 2: Native macOS Desktop + Menu Bar App

Requires **macOS 12+** with Xcode Command Line Tools (`swiftc`):

```bash
git clone https://github.com/STARKTANG108/antigravity-token-monitor.git
cd antigravity-token-monitor
chmod +x build.sh
./build.sh
```

This builds and launches `/Applications/AntigravityTokenMonitor.app`, featuring:
- Resizable dark `WKWebView` dashboard window (`1480×920`, stays alive in the background when closed)
- Compact Menu Bar item (`🪙 $...`) with optional icon-only mode, live 7-day / today / burn-rate summary, Always-on-Top toggle, native Desktop PNG snapshot (`WKWebView.takeSnapshot` + `NSSavePanel`), CSV export, and Launch at Login (`~/Library/LaunchAgents/com.antigravity.tokenmonitor.plist`)
- Managed local `monitor_server.py` subprocess on `http://127.0.0.1:18923`

---

## Project Structure

```text
.
├── monitor_server.py      # Python 3 stdlib SQLite WAL reader + HTTP/JSON/CSV API server
├── index.html             # Self-contained dark telemetry dashboard UI (HTML/CSS/JS/SVG)
├── TokenMonitorApp.swift  # Native macOS Cocoa + WebKit + NSStatusBar wrapper app
├── build.sh               # App bundle + vector icon + codesign build script
├── LICENSE                # MIT License
└── README.md
```

---

## HTTP API Reference

| Endpoint | Description |
| --- | --- |
| `GET /` | Serves the real-time dashboard UI (`index.html`) |
| `GET /api/health` | Health check returning `{"ok":true}` |
| `GET /api/stats?preset=last_7d&tz=local` | Aggregated telemetry JSON (`meta`, `summary`, `models`, `trend`, `windows`, `recent_calls`). Supports `preset` (`last_7d`, `since_reset`, `since_monday`, `today`, `last_24h`, `last_5h`, `last_1h`, `all_time`, `custom`), `start`, `end` (ISO-8601), and `tz` (`local` or numeric UTC offset). |
| `GET /api/export.csv?...` | Downloads a UTF-8 BOM CSV summary matching the active query parameters |

### Optional Environment Variable

- `ANTIGRAVITY_RESET_AT`: ISO-8601 start timestamp used when calling `/api/stats?preset=since_reset` (falls back to current week Monday `00:00` if unset).

---

## Customizing Model Mappings & Pricing

Antigravity stores serialized protobuf call metadata (`gen_metadata` and `steps`) in local SQLite files. Model IDs (`ENUM_TO_NAME`), per-million token rates (`PRICING`), colors (`MODEL_COLORS`), and image generation fee (`IMAGE_GEN_UNIT_COST`) can all be adjusted directly at the top of `monitor_server.py`.

---

## Privacy

- All database connections open local files strictly with `?mode=ro` (`sqlite3` read-only URI mode).
- Neither `monitor_server.py` nor `AntigravityTokenMonitor.app` modifies Antigravity databases or transmits usage logs anywhere outside `127.0.0.1`.

---

## License

Released under the [MIT License](LICENSE).
