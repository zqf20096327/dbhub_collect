# Network Monitor

Local dashboard for monitoring network targets (ICMP ping, TCP port, HTTP/HTTPS).

## Run on Windows

From the project root in CMD:

```bat
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
py main.py
```

Then open <http://127.0.0.1:8000>. Tests: `py -m unittest discover -s tests -t .`

On Linux, ping without special privileges needs an appropriate `net.ipv4.ping_group_range`.

## Windows executable (no Python required)

On **one Windows machine that has Python**, build once, then copy the output folder to other machines:

```bat
build_windows.bat
```

Output is in `dist\NetMonitor\`. Copy that entire folder and run `NetMonitor.exe`.

- Browser opens automatically (`http://127.0.0.1:8000`)
- `config\` and `data\` are created next to the exe (settings and database)
- To stop: close the console window or press `Ctrl+C`
- If antivirus flags it: common PyInstaller false positive; exclude the folder or build on that machine yourself

> **Note:** Building a Windows exe only works on Windows (PyInstaller targets the host platform). You cannot build a Windows exe from Linux/macOS.

## Features

- Statuses: up / unstable / down (down after consecutive failures, not a single lost packet)
- Tile background is a latency bar chart (PingPlotter-style: green/yellow/orange by latency, red = loss); click a tile for details, stats (avg, min, max, jitter, loss), and charts
- Persistent up/down events and per-minute stats in SQLite (`data/`), 24h trend chart and 24h CSV report
- Browser notifications + sound, optional Telegram alerts
- Search, filter, sort, add/edit/delete, CSV import and export
- Import PingPlotter text exports (File → Export to Text File, format «1 column per hop, 1 row per sample» with sample times) — final hop is added and latency history is loaded
- Import modes: add new only, add + update duplicates, or full replace
- Configurable log retention, packet-loss and latency threshold alerts, down re-alert cooldown, per-target mute
- Fullscreen mode for groups and targets only

## Appearance (themes and graphs)

- **18 themes** (10 night, 8 day) plus *Auto (system)*: Midnight, OLED Black (pure #000 for OLED screens), Graphite, Deep Ocean, Matrix, Amethyst, Ember, Sunset, Nord, Solar Dark / Daylight, Paper, Mint, Sky, Lavender, Solar Light, Rosé, Mono.
  Pick one from the **Theme** button (works in fullscreen too), from Settings → Appearance, or press **T** / **Shift+T** to cycle. The choice is remembered per browser.
- **Tile graph styles** (Settings → Appearance): Bars, Area, Line, Heat strip, Dots. All are coloured by latency (green / yellow / orange, red = loss) using the theme palette.
- **History window** (the ↗ button on a tile): live 5 min, 1 h, 6 h, 24 h, 7 d, 30 d; Area / Line / Bars; hover tooltip; min–max envelope; packet-loss chart; latency distribution.
- Palettes live in one place: the `THEMES` array at the top of `app/ui/static/app.js` — add a line there to create your own theme.

## Multiple browser tabs, multiple groups

Each browser tab can show different groups. Click **Groups for this tab…**, select groups, then **Apply to this tab** or **Open in new tab**.
Selection is stored in the URL and is bookmarkable, e.g.:

```
http://127.0.0.1:8000/?g=Core%20network&g=DNS
```

In a tab with fixed groups, search, filter, and alerts apply only to those groups.
A tab without `g` parameters paginates with `groups_per_window` and receives alerts for all groups.

## CSV format

Columns: `id,name,host,group,type,port,muted` — only `name,host,group` are required.
`type` is one of `icmp` (default), `tcp` (with `port`), or `http` (full `https://…` URL in `host`).
`muted=1` disables alerts for that target.

## Keeping the app light

- Checks are scheduled on a heap; first due times are staggered across the ping interval so targets never all fire at once.
- Fixed worker count (`max_concurrent_pings`) and a bounded queue; if the system falls behind, checks do not pile up.
- Down targets are checked every `down_ping_interval_seconds`, not every second.
- Base stats are kept incrementally (O(1)); the database is written in batches every 30 seconds.
- The browser only receives visible groups (`groups_per_window`, max `targets_per_group` targets) via SSE and updates the DOM in place; a hidden tab (without alerts) closes the connection.

## Settings (`config/settings.json`)

| Key | Meaning |
|---|---|
| `ping_interval_seconds`, `ping_timeout_seconds` | Check interval and timeout |
| `down_ping_interval_seconds`, `down_after_failures` | Interval for down targets; failures until “down” |
| `max_concurrent_pings`, `max_targets` | Concurrency and target cap |
| `history_seconds` | In-memory history length |
| `groups_per_window`, `targets_per_group` | Groups and targets shown per page |
| `ui_push_seconds`, `sparkline_points` | UI refresh; tile bar count (default 60; 0 = off) |
| `db_enabled`, `retention_days` | Persistent storage and retention |
| `alert_loss_pct`, `alert_loss_minutes` | Packet-loss alert threshold (0 = off) |
| `alert_latency_ms`, `alert_latency_minutes` | High-latency alert threshold (0 = off) |
| `alert_down_cooldown_seconds` | Re-alert interval while still down (0 = once) |
| `telegram_bot_token`, `telegram_chat_id` | Telegram alerts (empty = off) |
| `web_host`, `web_port`, `allowed_hosts` | Server bind; for LAN access set `web_host` to `0.0.0.0` and list allowed hosts (or `"*"`) |

Out-of-range or invalid values are corrected instead of crashing, and logged.

## Security

Server binds to `127.0.0.1` by default. `Host` header (anti DNS-rebinding) and `Origin` on mutating requests (anti CSRF) are checked. There is no authentication; if you expose it on a network, put it behind a reverse proxy with a password.
