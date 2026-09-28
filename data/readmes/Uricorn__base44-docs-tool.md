# Base44 Documentation Tool (Deprecated)


## Update: Base44 has launched a MCP for their documentation now!
More details here:
https://docs.base44.com/developers/backend/overview/base44-docs-mcp

It performs much better than this, so this is no longer required.



___________________________________________________________________________________________________________

(The following is AI Slop - please use responsibly.)

> **Instant, local access to complete Base44 documentation with AI assistant integration**

A tool that scrapes, stores, and queries Base44 documentation locally using the official `llms.txt` index. Perfect for developers, AI assistants, and teams who need fast, reliable access to Base44 docs.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

## Quick Start

```bash
# Clone and setup
git clone https://github.com/uricorn/base44-docs-tool.git
cd base44-docs-tool
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
playwright install chromium

# Scrape the documentation
python3 base44_docs_scraper.py scrape --no-embeddings

# Start using immediately
./b44 search "Google login setup"
./b44 get "/Getting-Started/Quick-start-guide"
```

## Features

- **llms.txt-Based Discovery**: Uses Mintlify's official `llms.txt` index for reliable page discovery
- **Complete Documentation**: Auto-discovers and scrapes 100+ Base44 documentation pages
- **Local SQLite Storage**: Full-text search with metadata, versioning, and change detection  
- **Optional Semantic Search**: AI-powered semantic search using sentence transformers
- **Multiple Interfaces**: CLI, HTTP API, and convenience scripts
- **Progress Visibility**: Clear progress indicators and timeout handling

## Documentation Coverage

The scraper automatically discovers all pages from `https://docs.base44.com/llms.txt`:

| Section | Description |
|---------|-------------|
| **Account & Billing** | Plans, credits, workspace management |
| **Building Your App** | AI agents, chat modes, automations, design |
| **Community & Support** | Troubleshooting, support, privacy |
| **Developers** | CLI, SDK, API reference, code editor |
| **Enterprise** | SSO, workspace domains, app visibility |
| **Getting Started** | Quick start, prompts, templates, partners |
| **Integrations** | AI, Airtable, Slack, Stripe, Zapier, etc. |
| **Performance & SEO** | App optimization, search visibility |
| **Setting Up Your App** | Access, login, security, domains |

## Usage

### CLI Commands

```bash
# View documentation index without scraping
python3 base44_docs_scraper.py index

# Scrape all documentation (with progress indicator)
python3 base44_docs_scraper.py scrape

# Scrape without generating embeddings (faster)
python3 base44_docs_scraper.py scrape --no-embeddings

# Force re-scrape all pages
python3 base44_docs_scraper.py scrape --force

# Search documentation
python3 base44_docs_scraper.py search "authentication" --limit 5

# Get specific page
python3 base44_docs_scraper.py get "/Getting-Started/Quick-start-guide"

# View database stats
python3 base44_docs_scraper.py stats

# Start HTTP API server
python3 base44_docs_scraper.py serve --port 8000
```

### Convenience Script

```bash
./b44 search "backend functions"
./b44 get "/Integrations/Stripe-integration"
./b44 stats
```

### Search Options

```bash
# Search with section filter
python3 base44_docs_scraper.py search "backend" --section "Developers"

# Different output formats
python3 base44_docs_scraper.py search "Stripe" --format table   # Default
python3 base44_docs_scraper.py search "Stripe" --format json    # JSON output
python3 base44_docs_scraper.py search "Stripe" --format text    # Text list

# Page retrieval with formats
python3 base44_docs_scraper.py get "/Integrations/Resend-integration" --format markdown
```

### HTTP API

```bash
# Start server
python3 base44_docs_scraper.py serve --port 8000

# Endpoints:
# GET /search?q=<query>&limit=<limit>
# GET /stats
```

## How It Works

The scraper uses Mintlify's `llms.txt` file as the authoritative source for documentation pages:

1. **Discovery**: Fetches `https://docs.base44.com/llms.txt` to get all page URLs
2. **Scraping**: Uses Playwright to render each page and extract content
3. **Storage**: Saves to SQLite with content hashing for change detection
4. **Search**: Text-based search with optional semantic embeddings

## Troubleshooting

### Scraping hangs or times out
Each page has a 30-second timeout. If many pages fail, check your internet connection.

### Missing dependencies
```bash
pip install -r requirements.txt
playwright install chromium
```

### Database issues
Delete `base44_docs.db` and re-scrape:
```bash
rm base44_docs.db
python3 base44_docs_scraper.py scrape --force
```

## Project Structure

```
base44 docs/
├── base44_docs_scraper.py    # Main scraper & CLI
├── cursor_integration.py     # Cursor integration
├── quick_search.py           # Streamlined search
├── b44                       # Convenience script
├── requirements.txt          # Python dependencies
├── base44_docs.db            # SQLite database (auto-created)
└── README.md
```

## License

MIT License
