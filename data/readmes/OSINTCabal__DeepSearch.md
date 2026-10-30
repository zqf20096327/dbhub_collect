# DeepSearch

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Code Style: PEP 8](https://img.shields.io/badge/code%20style-PEP%208-blue.svg)](https://peps.python.org/pep-0008/)
[![Version](https://img.shields.io/badge/version-1.0-green.svg)]()

**Created by OSINTCabal**

**DeepSearch** is a terminal wrapper for the [DeepSeek Search & Fetch API](https://api-docs.deepseek.com/guides/search/). It features a beautiful animated terminal UI, ddgr-style paginated search with lazy API loading, an interactive single-key navigation system, a built-in SQLite database, and local page fetching via curl/wget — all in your terminal. No emojis.

> **Lazy loading:** The API is called only when you navigate to a new page. Going back to previous pages uses cached results with zero extra API calls. This keeps costs down and browsing instant.

---

## Screenshot

![DeepSearch Main Menu](docs/screenshot.png)

---

## Example Output

### Paginated Search (ddgr-style, default)

```
╭──────────────────────────────────────────────────────────────────────────╮
│  DeepSearch   python tutorial    10/50 results    Result 3/10            │
│  ████░░░░░░░░░░░░░░░░  6%                                                │
╰──────────────────────────────────────────────────────────────────────────╯

  ↑ 3 more above

  >   3  1.60  ***- Python Tutorial - W3Schools
       W3Schools  |  w3schools.com/python/  |  2026-01-15
       Python is a popular programming language. ...

    4  1.45  **-- Python for Beginners
       Real Python  |  realpython.com/python-beginner  |  2026-01-10
       Learn Python from scratch with hands-on tutorials...

  ↓ 7 more below  |  40 not yet loaded (scroll to fetch)

────────────────────────────────────────────────────────────────────────────────
  [↑↓] scroll  [PgUp/PgDn] page  [Enter] expand  [wheel] scroll  |  [n]ext [p]rev
  [f]irst [l]ast  |  [#] expand  [o]# fetch  [b]# browser  [c]# copy  [d]#
  download  |  [r]esearch [s]ave [?]help [q]uit
```

### Full Display Mode (`--no-paginate`)

```
────────────────────────  RESULTS FOR: python tutorial  ────────────────────────
╭─────────────────── RESULT STATISTICS - 10 RESULTS CAPTURED ───────────────────╮
│  Total Results:  10                                                           │
│  Score Range:    1.21 - 1.83  (avg 1.52)                                      │
│  Authority:      ****x2  ***-x3  **--x3  *---x2                               │
│  Date Range:     2025-03-09 to 2026-01-15                                     │
│  Top Sites:      w3schools.com (3), realpython.com (2), github.com (2)        │
╰───────────────────────────────────────────────────────────────────────────────╯
```

### Database Browser

```
──────────────────────────────────  DATABASE  ──────────────────────────────────
╭─────────────────────────────────────┬────────────────────────────────────────╮
│ Total Searches                      │ 36                                     │
│ Total Results Stored                │ 331                                    │
│ Total Fetches                       │ 12                                     │
│ Total Chars Fetched                 │ 10,868                                 │
│ Date Range                          │ 2026-10-21 to 2026-10-22               │
╰─────────────────────────────────────┴────────────────────────────────────────╯
```

---

## Features

| Mode | Description |
|------|-------------|
| **Web Search** | ddgr-style paginated search with lazy API loading (default). Results are fetched from the API only when you navigate to a new page. Single-key navigation with arrow keys, mouse wheel, and vim-style keys. |
| **Full Display** | All results displayed at once with relevance scores, authority tiers, snippets, AI summaries, and field availability indicators (`--no-paginate`). |
| **Fetch URL** | Fetch any web page and render the full content as Markdown. API or local (curl/wget with `--local`). |
| **Batch Search** | Run multiple search queries from a file with concurrent workers. Progress bar, summary table, saves to JSON + Markdown. |
| **Batch Fetch** | Fetch multiple URLs from a file with concurrent workers. |
| **Database** | Browse saved searches and fetches in SQLite. Search, stats, export, clear. |
| **Settings** | View API key status, endpoints, rate limits, pricing. |
| **Setup** | Reconfigure API key (stored in `~/.deepsearch_config.json`). |

### Key Capabilities

- **Lazy API loading** — API called only when scrolling to new pages, never on cached pages
- **Single-key navigation** — Arrow keys, mouse wheel, PgUp/PgDn, Home/End, vim keys (j/k), all without pressing Enter
- **Animated terminal UI** — Two-tone ASCII banner, typewriter tagline, animated rules, smooth Live-based scroll view
- **SQLite database** — Every search and fetch auto-saved to `~/.deepsearch.db`
- **Search history** — Recent queries shown before interactive prompts
- **Terminal height awareness** — Viewport auto-adjusts to fit your terminal
- **Windows support** — Arrow keys, PgUp/PgDn, Home/End work via msvcrt scan code mapping
- **Key buffering** — Fast typists won't lose keystrokes; unconsumed keys are buffered and replayed
- **Non-TTY fallback** — Piped/redirected output automatically uses full display mode
- **JSON output** — Raw JSON for scripting (`--json`)
- **Save to file** — Export results to JSON (`-o FILE`)

---

## Installation

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- A [DeepSeek API key](https://platform.deepseek.com) (get one at platform.deepseek.com)

### Install from Source

```bash
# Clone the repository
git clone <local-path>/deepsearch-cli.git
cd deepsearch-cli

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### First Run

```bash
# Run the setup wizard to save your API key
python deepsearch.py setup

# Or just run it — first run triggers setup automatically
python deepsearch.py
```

Your API key is saved to `~/.deepsearch_config.json` with owner-only permissions.

---

## Usage Examples

### Interactive Mode (Recommended)

```bash
# Launch the interactive menu — animated banner, then pick a mode
python deepsearch.py
```

### Web Search

```bash
# Paginated ddgr-style search (default, lazy loading)
python deepsearch.py search "AI news"

# Custom page size and result count
python deepsearch.py search "AI news" --count 30 --page-size 5

# Full display mode (all results at once, no pagination)
python deepsearch.py search "DeepSeek V4 release" --count 10 --no-paginate

# Include full page content in results
python deepsearch.py search "python rich library" --count 3 --content --no-paginate

# Raw JSON output (for scripts)
python deepsearch.py --json search "AI news" --count 3

# Save results to file
python deepsearch.py search "AI news" -o results.json
```

### Fetch URL

```bash
# Fetch a URL via DeepSeek API
python deepsearch.py fetch "https://example.com/article"

# Fetch a URL locally (curl/wget, no API cost)
python deepsearch.py fetch "https://example.com" --local

# JSON output
python deepsearch.py --json fetch "https://example.com"
```

### Batch Operations

```bash
# Batch search from a file (one query per line)
python deepsearch.py batch-search queries.txt --count 5 --verbose

# Batch fetch from a file (one URL per line)
python deepsearch.py batch-fetch urls.txt --qps 3
```

### Database

```bash
# Browse saved data
python deepsearch.py db recent 20
python deepsearch.py db search "python"
python deepsearch.py db fetches 10
python deepsearch.py db stats
python deepsearch.py db result 42
python deepsearch.py db export backup.json
python deepsearch.py db clear
```

### Global Flags

```bash
# Disable animations (fast, script-friendly)
python deepsearch.py --no-anim search "query"

# Skip the banner
python deepsearch.py --no-banner search "query"

# Override API key
python deepsearch.py --key sk-... search "query"

# Reset saved key and reconfigure
python deepsearch.py --reset
```

---

## Paginated Search Navigation

Results are fetched lazily — the API is called only when you scroll near the end of loaded results. Scrolling back uses cached results with zero extra API calls.

### Scrolling

| Key | Action |
|-----|--------|
| `↑` / `↓` | Scroll up / down (1 result at a time) |
| Mouse wheel | Scroll up / down (3 results at a time) |
| PgUp / PgDn / `←` / `→` | Jump by one viewport |
| Enter | Expand the result under the cursor |

### Jump

| Key | Action |
|-----|--------|
| `n` / Space / `j` | Page down |
| `p` / `k` | Page up |
| `f` / Home | First result |
| `l` / End | Last result |

### Result Actions (use with a number 1-N)

| Key | Action |
|-----|--------|
| `<#>` or `e <#>` | Expand result (full summary + content) |
| `o <#>` | Fetch result URL in DeepSearch |
| `b <#>` | Open result URL in browser |
| `c <#>` | Copy result URL to clipboard |
| `d <#>` | Download result page (curl/wget) |

### Other

| Key | Action |
|-----|--------|
| `r` | Research (new search query) |
| `s` | Save all results to JSON |
| `?` | Navigation help |
| `q` | Quit back to menu |
| Ctrl+C | Quit immediately |

---

## Query Operators

The DeepSeek Search API supports these operators:

| Operator | Description | Example |
|----------|-------------|---------|
| `site:` | Restrict to a site | `DeepSeek site:github.com` |
| `site: OR` | Multiple sites | `DeepSeek site:github.com OR site:huggingface.co` |
| `-site:` | Exclude a site | `DeepSeek -site:example.com` |
| `-` | Exclude a term | `DeepSeek -advertisement` |
| `-"..."` | Exclude a phrase | `DeepSeek -"release notes"` |
| `"..."` | Exact phrase match | `DeepSeek "exact phrase"` |
| `lang:` | Language filter | `DeepSeek lang:zh,en` |
| `after:` | After date | `DeepSeek after:2025-01-01` |
| `before:` | Before date | `DeepSeek before:2026-06-01` |

---

## Configuration

Your API key is saved to `~/.deepsearch_config.json` after first-run setup.

**Resolution order:**
1. `--key` command-line argument
2. `DEEPSEEK_API_KEY` environment variable
3. `.env` file in the project directory
4. `~/.deepsearch_config.json` (saved by setup wizard)

### Pricing

| Service | Price |
|---------|-------|
| Search | $0.75 / 1,000 requests |
| Fetch | $0.75 / 1,000 requests |

### Rate Limits

| Service | QPS Limit |
|---------|-----------|
| Search | 100 QPS |
| Fetch | 25 QPS |

---

## Database

All searches and fetches are automatically saved to `~/.deepsearch.db` (SQLite).

| Command | Description |
|---------|-------------|
| `db recent [N]` | Show last N searches (default 10) |
| `db search "pattern"` | Search saved queries |
| `db fetches [N]` | Show last N fetches (default 10) |
| `db stats` | Show database statistics |
| `db result ID` | Show a specific result by ID |
| `db export FILE` | Export database to JSON |
| `db clear` | Delete all data |

---

## Terminal Compatibility

- **Auto viewport sizing** — The paginated view automatically adjusts the number of visible results to fit your terminal height
- **Non-TTY fallback** — Piped/redirected output automatically uses full display mode (no pagination)
- **Mouse support** — Scroll wheel and click support via SGR mouse reporting (Unix terminals)
- **Windows support** — Arrow keys, PgUp/PgDn, Home/End work via msvcrt scan code mapping
- **Key buffering** — Fast typists won't lose keystrokes; unconsumed keys are buffered and replayed

---

## Requirements

```
rich>=13.0.0
requests>=2.28.0
python-dotenv>=1.0.0
beautifulsoup4>=4.12.0
```

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

**Created by OSINTCabal**
