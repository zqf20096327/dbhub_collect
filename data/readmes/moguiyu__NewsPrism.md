# NewsPrism

NewsPrism is a self-hosted news analysis tool built around one idea: the same event, read from many directions, gets you closer to what actually happened.

It collects the same stories from 46 sources across 12 countries and languages, groups them by real-world event, and surfaces how different outlets — state media, independent press, tech reporters, regional correspondents — choose to frame the same facts. The daily report is a Chinese digest designed for readers who want calibrated perspective, not just headlines.

```text
Collect articles  ->  Tag + dedup  ->  Cluster events  ->  Assess quality  ->  Summarize angles  ->  Render HTML / publish
```

This public repository supports both self-hosting with Docker and local development from source.

Current major release: `v0.6.3`.

## Highlights

- Groups the same event across multiple sources and shows how each outlet frames it differently — state media, independent press, regional correspondents, tech reporters
- Active perspective-seeking: if a major story is missing a regional voice, the pipeline searches for it and adds it to the cluster
- LLM-driven event clustering (single API call) groups articles by real-world event identity, not just topic overlap; falls back to embedding-based clustering automatically
- LLM multi-dimensional impact evaluation ranks stories by real-world consequence — scope, severity, novelty, actor influence, decision relevance, feelgood — blended with a cross-source signal under calibrated weights (no keyword matching)
- Self-evolving selection: editor 👍/👎 feedback nudges the impact weights weekly and distills a persistent editorial-policy memo back into the scoring prompt
- **State Media Matrix ownership gate**: every source is independently classified (7 tiers); state-controlled outlets are blocked from covering another country's 内政 (domestic governance only — disasters, diplomacy, trade, and war are excluded) while independent and public-service media retain full standing
- Keyword-free storyline grouping with a coherence gate, plus compact cross-day timelines for developing topics
- Batch summarisation processes all stories in one LLM call (~36 s → ~10 s per publish cycle)
- Multilingual collection across Chinese, English, Japanese, Korean, Russian, Polish, Dutch, and more
- Dedicated `今日好消息` / Good News lane derived from the same impact evaluation's feelgood dimension
- WIRED-inspired static HTML reports with system/light/dark modes and self-hosted fonts
- Per-task LLM routing: name your providers once (DeepSeek, OpenRouter, any OpenAI-compatible endpoint), then pick a provider and model for each pipeline step, with a default and a fallback
- LAN settings page: see provider balances, the Telegram check, and every setting with where it comes from and whether the running services have picked it up; log in to edit and changes apply within about a minute, no restart
- CLI entrypoints for collection, publish, replay, and scheduler runs

## Architecture

```text
newsprism/
├── types.py          Shared dataclasses and typed records
├── config.py         YAML + environment loader
├── repo/             SQLite persistence
├── service/          collect, dedup, cluster (LLM + embedding fallback), impact eval, storyline, calibrate, summarize
└── runtime/          schedule, render, publish, feedback poll, admin portal, settings page
```

Layer rule: `types -> config -> repo -> service -> runtime`. Higher layers must not be imported downward.

## Self-Host With Docker

NewsPrism supports a single-server Docker Compose deployment with published GHCR images. The default install path only needs `docker-compose.yml` and `.env`; it does not require a local `Dockerfile` or a full repo checkout.

```bash
# Download docker-compose.yml and .env.example from this repo into an empty directory
cp .env.example .env
# Fill in at least LITELLM_API_KEY, LITELLM_MODEL, LITELLM_BASE_URL, REPORT_BASE_URL

# Start the published images
docker compose up -d

# Optional: trigger the first run immediately instead of waiting for cron
docker compose exec newsprism python -m newsprism once
```

The default stack includes:

- `newsprism`: scheduler and pipeline worker
- `web`: static report server on `http://localhost:8080`
- [`NewsNow`](https://github.com/ourongxing/newsnow): optional-but-recommended helper for difficult Chinese sources

The default image-based install uses the config and templates bundled inside the `newsprism` image. If you want editable host-side `config/`, `templates/`, or nginx config files, use the contributor/source-build stack in `docker-compose.dev.yml`. For Chinese-source coverage, NewsPrism works best with the self-hosted [`NewsNow`](https://github.com/ourongxing/newsnow) proxy enabled.

Full server install, update, backup, and customization guidance lives in `docs/deploy-docker.md`.

### Settings page (optional, source-build stack)

`docker-compose.dev.yml` adds `newsprism-settings`, a small web page for running the installation from a browser on your home network:

- an overview of each service (applied or pending), LLM provider balances, Tavily usage, and a live Telegram check
- every setting with its value (secrets masked), where it comes from (`store`, `.env`, `config.yaml`, or a default), and whether it is applied
- after logging in, edit forms for providers, per-task models, search keys, delivery, schedule, and site URLs

Edits are saved to `settings-store/settings.json`, which keeps revisions and an audit log. The scheduler reloads it between jobs, so changes apply within about a minute without a restart. For any key in the store, the store wins over `.env`.

```bash
# One-time: copy the current .env / compose / config.yaml values into the store
docker compose -f docker-compose.dev.yml exec newsprism-settings python -m newsprism settings import

# Set the admin password (viewing works without one; editing needs it)
docker compose -f docker-compose.dev.yml exec -it newsprism-settings python -m newsprism settings set-password
```

The page only answers LAN clients and is bound to one host IP (`SETTINGS_BIND_IP`, never `0.0.0.0`). Don't put it behind a public reverse proxy.

### Demo copy on Cloudflare Pages (optional)

`scripts/publish_demo_site.py` publishes a noindex copy of the public reports to a Cloudflare Pages project (for example `newsprism.pages.dev`). It builds a staging tree from `output/` (never the private `staging`, `shadow` or `verify-*` folders), rewrites the canonical hostname to the demo one, and uploads it with wrangler in a throwaway Node container. `output/` is not modified.

```bash
# Credentials live outside the repo, mode 600 (CLOUDFLARE_API_TOKEN needs Account > Cloudflare Pages > Edit)
python3 scripts/publish_demo_site.py --build-only   # build and report, upload nothing
python3 scripts/publish_demo_site.py --dry-run      # also print the upload command
python3 scripts/publish_demo_site.py                # upload (--project, --days, --to-base-url available)
```

Run it from cron shortly after the daily publish. The credentials file defaults to `~/.config/newsprism/cloudflare-pages.env`.

## Develop Locally

```bash
git clone https://github.com/moguiyu/NewsPrism.git
cd NewsPrism

python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .[dev]

cp .env.example .env
# Fill in at least LITELLM_API_KEY, LITELLM_MODEL, and LITELLM_BASE_URL

python -m newsprism collect
python -m newsprism once
```

Optional helper services:

- `docker compose -f docker-compose.dev.yml up -d newsnow` starts a local [`NewsNow`](https://github.com/ourongxing/newsnow) proxy for harder Chinese sources.
- `docker compose -f docker-compose.dev.yml up -d web` serves generated HTML reports from `http://localhost:8080`.

## Environment Variables

Required for summarization:

| Variable | Purpose |
|---|---|
| `LITELLM_API_KEY` | API key for your OpenAI-compatible LLM provider |
| `LITELLM_MODEL` | LiteLLM model identifier used for story summaries |
| `LITELLM_BASE_URL` | Provider base URL |
| `REPORT_BASE_URL` | Public or local base URL used in rendered report links |

Optional:

| Variable | Purpose |
|---|---|
| `EVALUATOR_MODEL` | Separate model for active-search evaluation |
| `NEWSNOW_BASE_URL` | External `newsnow` endpoint if not using the bundled compose service |
| `TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID` | Telegram publishing |
| `TAVILY_API_KEY` / `BRIGHTDATA_API_KEY` | Active search providers |
| `X_BEARER_TOKEN` / `YOUTUBE_API_KEY` | Official social fallback providers |
| `SCHEDULE_TIMEZONE` | Override scheduler timezone without editing YAML |
| `SETTINGS_BIND_IP` / `SETTINGS_PORT` | Host LAN IP and port for the settings page (default port `8085`) |
| `SETTINGS_UID` / `SETTINGS_GID` | Host user/group the settings page runs as (must read `.env` and write `settings-store/`) |
| `SETTINGS_LOW_BALANCE` | Balance below which a provider is flagged red on the settings page |

Once the settings store exists, the keys it holds (LLM providers and models, search keys, Telegram, schedule, site URLs) are managed on the settings page; editing them in `.env` no longer has any effect. `.env` still provides bootstrap values such as paths, ports, and the `SETTINGS_*` variables.

## Customization

Self-hosters are expected to customize the installation through files, not Python code.

For the default image-based install, those files live inside the container image. Use `docker-compose.dev.yml` from a repo checkout if you want to edit `config/`, `templates/`, or `config/nginx.conf` directly on the host.

| Surface | What you can change |
|---|---|
| `.env` | provider keys, public report URL, scheduler timezone, optional integrations |
| settings page / `settings-store/settings.json` | LLM providers and per-task models, search keys, Telegram, schedule, site URLs (source-build stack; wins over `.env` once imported) |
| `config/config.yaml` | schedule, source list, clustering thresholds, dedup rules, storyline coherence, English report toggle, active-search behavior |
| `config/editorial-values.yaml` | impact dimension weights, status floors, positive-lane thresholds, source tier scores |
| `config/style-guide.md` | editorial prompt and no-fabrication rules used by the summarizer |
| `templates/report-template.html` | HTML branding and presentation |

Common examples:

- disable sources by setting `enabled: false` under `sources:`
- enable the English report toggle under `output.english.enabled`
- edit `schedule.collect_cron` and `schedule.publish_cron`
- adjust selection by editing impact weights / status floors in `config/editorial-values.yaml`, or send 👍/👎 feedback and let weekly calibration tune them
- set `clustering.use_llm_clustering: false` to use embedding-only clustering (no LLM API call for clustering)

## CLI Commands

| Command | Purpose |
|---|---|
| `python -m newsprism collect` | Fetch and store fresh articles |
| `python -m newsprism publish` | Cluster and publish the current report |
| `python -m newsprism once` | Run collection and publish in one pass |
| `python -m newsprism replay --date YYYY-MM-DD` | Rebuild one report date from its saved article set |
| `python -m newsprism run` | Start the long-running scheduler |
| `python -m newsprism feedback add\|list\|poll` | Record editor 👍/👎 on a cluster, list recent feedback, or poll Telegram |
| `python -m newsprism calibrate run\|show\|reset` | Run weight calibration + policy distillation, inspect, or reset to seeds |
| `python -m newsprism portal --host 127.0.0.1 --port 8081` | Run the local admin quality portal (inspect selection + give structured feedback) |
| `python -m newsprism settings --host-root /host` | Run the LAN settings page |
| `python -m newsprism settings import [--force]` | One-time import of `.env` / compose / `config.yaml` values into the settings store |
| `python -m newsprism settings set-password` | Set the settings-page admin password |

## Testing and Packaging

```bash
pytest
python -m build
```

The default test suite is designed to run without private infrastructure or deployment secrets.

## Configuration Surface

Most behavior is file-based:

| File | Purpose |
|---|---|
| `config/config.yaml` | Sources, schedules, thresholds, storyline/hot-topic behavior |
| `config/editorial-values.yaml` | Impact dimension weights, status floors, positive-lane thresholds, source tier scores |
| `config/style-guide.md` | Editorial prompt and no-fabrication constraints |
| `settings-store/settings.json` | Operator settings edited on the settings page (providers, models, keys, schedule, site) |

## Project Docs

| Topic | File |
|---|---|
| Contributing process | `CONTRIBUTING.md` |
| Security reporting | `SECURITY.md` |

## Acknowledgements

NewsPrism is an independent project inspired by [TrendRadar](https://github.com/sansan0/TrendRadar). Thanks to the TrendRadar project and its author/community for the inspiration.

NewsPrism also relies on the self-hosted [NewsNow](https://github.com/ourongxing/newsnow) project for stronger coverage of difficult Chinese news sources. Thanks to that project and its author for making that workflow practical.

Development assistance for recent quality, deployment, and release work was provided by [Claude Code](https://claude.ai/claude-code) (Anthropic).

## Deployment Notes

- Supported public deployment target: one Linux server with Docker Compose
- Default self-hosting path uses published GHCR images; no local source checkout is required
- Persistence lives in `data/`, `output/`, `settings-store/` (source-build stack), and the Hugging Face cache volume
- SQLite is intended for single-host use; this repo does not target clustered multi-writer deployments
- For public internet exposure, run a reverse proxy with HTTPS in front of the `web` service and set `REPORT_BASE_URL` accordingly
- Some source coverage, especially difficult Chinese sites, is materially better when [`NewsNow`](https://github.com/ourongxing/newsnow) is enabled

## License

Released under the MIT License. See `LICENSE`.
