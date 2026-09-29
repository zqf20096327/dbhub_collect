# BurpQL

AI-optimized query engine for Burp Suite Pro HTTP traffic data. Ingests Burp XML exports into a fast, searchable SQLite database with a REST API designed for AI agent consumption.

## Why BurpQL?

The Portswigger MCP tool lets AI agents interact with Burp Suite, but searching through thousands of requests/responses is inefficient and overloads context windows. BurpQL fills this gap by providing:

- **Dual full-text search** — Porter stemming for word search + trigram indexing for substring search
- **Metadata-first API** — Returns URL/method/status by default, bodies only on demand
- **Token budget control** — Truncation and result limits on every endpoint
- **Persistent project storage** — Query past projects without re-ingesting

## Quick Start

### Local

```bash
# Install
uv sync

# Ingest a Burp XML export and start the API
uv run burpql myproject export.xml

# API is now running at http://localhost:8888
# Swagger docs at http://localhost:8888/docs
```

### Docker

```bash
# Build
docker compose build

# Ingest and serve (mounts CWD for XML files, ~/.burpql for persistent data)
docker compose run burpql myproject export.xml

# Or serve an existing project
docker compose up
```

### Exporting from Burp Suite

1. In Burp Suite Pro, go to **Proxy > HTTP history** (or **Target > Site map**)
2. Select the items you want to export (Ctrl+A for all)
3. Right-click > **Save items** (or **Export selected items**)
4. Save as XML format

## CLI

```bash
burpql                          # List available projects
burpql <project-name>           # Serve existing project API
burpql <project-name> <file>    # Ingest XML then serve API
```

Project databases are stored at `~/.burpql/<project-name>.db` and persist across runs.

## API Reference

All endpoints return JSON. Bodies are excluded by default — use `include_bodies=true` to include them.

### Search

| Endpoint | Description |
|----------|-------------|
| `GET /search?q=<term>` | Word search with porter stemming ("cache" matches "cached", "caching") |
| `GET /grep?q=<string>` | Substring search via trigram index (finds any substring in any field) |

Both accept: `max_results`, `include_bodies`, `truncate_at`

### Browse

| Endpoint | Description |
|----------|-------------|
| `GET /requests` | Filtered listing (filters: `host`, `method`, `status`, `content_type`, `path_contains`) |
| `GET /requests/{id}` | Single request with full detail |
| `GET /hosts` | Unique hosts with request counts |
| `GET /endpoints` | Unique method+path combinations |
| `GET /parameters` | URL query parameters with counts and examples |
| `GET /stats` | Summary statistics |
| `GET /headers?name=<header>` | Search for specific HTTP headers |

### Common Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `max_results` | 50-100 | Maximum results to return |
| `include_bodies` | false | Include request/response headers and bodies |
| `truncate_at` | 2000 | Truncate body fields at N characters (0 = no truncation) |
| `offset` | 0 | Pagination offset (on `/requests`) |

## Architecture

- **SQLite + FTS5** — Portable, fast, zero-config database
- **Porter tokenizer** — Word-level search with stemming
- **Trigram tokenizer** — Character-level substring search at index speed
- **FastAPI** — Async API with auto-generated Swagger docs
- **lxml iterparse** — Memory-efficient XML parsing for large exports

## AI Agent Skill

BurpQL includes a Claude skill (`skill/`) with a self-contained Python search tool that wraps the REST API. This avoids curl/jq shell escaping issues that commonly break AI agent terminal interactions.

To install the skill:

```bash
cp -r skill/ ~/.claude/skills/BurpQL/
```

The skill teaches AI agents:
- When to use BurpQL and when to use Portswigger MCP instead
- How to search with the Python tool (no curl needed)
- Token budget management and progressive detail patterns
- Security-focused reconnaissance workflows

## Development

```bash
make dev        # Install all dependencies
make lint       # Check linting
make format     # Auto-format code
make test       # Run tests
```
