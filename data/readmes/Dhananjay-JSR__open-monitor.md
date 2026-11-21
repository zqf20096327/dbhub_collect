# open-monitor

**Live demo:** [omon.dhananjaay.dev](https://omon.dhananjaay.dev) (sign in with `demo` / `demo`)

A self-hosted server that watches web searches or specific pages on a schedule, asks an LLM whether each new result matters for your goal, and sends what it keeps to a webhook. You bring the search provider and the LLM.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/dashboard-dark.png">
  <img alt="Open Monitor dashboard" src="docs/dashboard-light.png">
</picture>

```bash
curl -X POST http://localhost:8787/v1/monitors \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "AI infra funding",
    "targets": [{ "type": "search", "query": "ai infrastructure funding" }],
    "goal": "New funding rounds for GPU cloud and inference companies",
    "schedule": { "type": "interval", "interval": "1d" },
    "webhook": { "url": "https://agent.example.com/hooks/monitor" }
  }'
```

The response includes `webhook.secret` (`whsec_...`) once. The whole API is described in OpenAPI 3.1 at `/openapi.json`, which needs no key.

## Run it

### Node

Needs Node 24 or newer (it uses the built-in `node:sqlite`).

```bash
cp .env.example .env    # set API_KEY, plus a search provider and an LLM key, see below
npm start
```

It listens on port 8787, stores everything in `monitor.db`, and runs the scheduler once a minute.

### Docker Compose (full stack)

```bash
cp .env.example .env    # set API_KEY and LLM_API_KEY; search needs no key here
docker compose up -d
```

This starts three containers: the monitor on port 8787, [SearXNG](https://github.com/searxng/searxng) for search (so no Tavily key is needed), and [Lightpanda](https://github.com/lightpanda-io/browser) for pages that build their content with JavaScript. Data lives in the `data` volume. Change `secret_key` in `searxng/settings.yml` before you expose anything.

## Deploy

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/Dhananjay-JSR/open-monitor)
[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/deploy/open-monitor?referralCode=kxlF5H&utm_medium=integration&utm_source=template&utm_campaign=generic)

Any host that runs the `Dockerfile`, or the published image `ghcr.io/dhananjay-jsr/open-monitor`, works. Give it a persistent disk at `/data` (the SQLite file lives there), set the variables from [Configuration](#configuration), and set `TRUST_PROXY=1`, since these hosts sit behind a proxy that terminates HTTPS.

- **Railway:** the template builds the `Dockerfile` with a volume at `/data`, generates `API_KEY` and `SESSION_SECRET`, and asks for the LLM, Tavily and dashboard values.
- **Render:** the button reads `render.yaml`, which creates the web service with a 1 GB disk and generates `API_KEY` and `SESSION_SECRET`. Disks need a paid instance; on the free one the database is lost on every deploy and the service sleeps, so the scheduler stops too.

### Cloudflare Workers

```bash
wrangler d1 create open-monitor        # paste the id into wrangler.toml
wrangler secret put API_KEY            # and the other secrets listed in wrangler.toml
wrangler deploy
```

Storage is D1 and a cron trigger runs the scheduler every minute. `LLM_COMMAND` does not work on Workers.

### Hosts without a scheduler

Point any external cron at `POST /tick` with the API key. Calling it more often than needed is harmless.

## Configuration

Everything is an environment variable; `.env.example` lists them.

| Variable | What it does |
|---|---|
| `API_KEY` | Required. Clients send it as `Authorization: Bearer ...` |
| `LLM_API_KEY`, `LLM_BASE_URL`, `LLM_MODEL` | Judge over an OpenAI-compatible API. Defaults: OpenRouter, model `openrouter/free` |
| `LLM_COMMAND` | Judge with a local command instead (Node only) |
| `LLM_REQUESTS_PER_MINUTE` | Judge calls per minute, shared by every process. Default 20, `0` for no limit |
| `TAVILY_API_KEY` | Search with Tavily |
| `SEARXNG_URL` | Search with your own SearXNG. Wins if both are set |
| `BROWSER_WS_URL` | CDP websocket of a headless browser, for JavaScript-rendered pages |
| `DASHBOARD_USER`, `DASHBOARD_PASSWORD`, `SESSION_SECRET` | Turn the dashboard on (all three needed) |
| `OTEL_EXPORTER_OTLP_ENDPOINT`, `OTEL_EXPORTER_OTLP_HEADERS`, `OTEL_SERVICE_NAME` | Telemetry export |
| `TRUST_PROXY` | Behind a reverse proxy: trust `X-Forwarded-For`, `X-Forwarded-Proto` and `X-Forwarded-Host` |
| `ALLOW_PRIVATE_URLS` | Allow webhook and page URLs on localhost and private networks |
| `COST_PER_SEARCH_RUN`, `COST_PER_PAGE_FETCH` | Rates for `usage.cost`. Default 0 |
| `PORT`, `DB_PATH` | Default `8787` and `monitor.db` |

## The judge

Each candidate (a new search result, or a page diff) gets one LLM call that scores it from 0 to 1 against the monitor's `goal`. Scores at or above 0.5, or the target's `judge.threshold`, are kept. Without an LLM every run fails with `judge_failed`.

```bash
# OpenRouter, free models only (the default): a key is all it needs
LLM_API_KEY=sk-or-...

# any OpenAI-compatible API
LLM_BASE_URL=https://api.openai.com/v1
LLM_API_KEY=sk-...
LLM_MODEL=<a chat model your key can use>

# Ollama, fully local
LLM_BASE_URL=http://localhost:11434/v1
LLM_MODEL=<a model you have pulled>

# a command line tool: the prompt goes to stdin, the answer comes from stdout
LLM_COMMAND="claude -p"
```

`openrouter/free` routes each call to one of OpenRouter's free models. Free models allow 20 requests a minute (the default `LLM_REQUESTS_PER_MINUTE`) and 50 a day, or 1,000 a day once the account has bought credits. The per-minute count lives in the database, so every process shares it. On a 429 the judge waits for `Retry-After`; whatever is left unjudged is picked up by the next run.

## Search and pages

**Search monitors** run the query, keep up to `max_results` results, apply `include_domains` and `exclude_domains`, drop URLs the monitor has already judged, and send the rest to the judge. A new monitor's first run looks back over the past 7 days; each later run covers the time since the one before. Findings come newest first. Each URL is judged once, even if you change the goal later.

**Page monitors** fetch each URL, compare its text with the copy from the last run and send the unified diff (up to 24 KiB) to the judge. The first run only saves the page. For pages that render in the browser, set `BROWSER_WS_URL` to any CDP endpoint: Lightpanda (`lightpanda serve --host 127.0.0.1 --port 9222`), Chrome with `--remote-debugging-port`, or a hosted browser. `BROWSER_WS_HEADERS` (a JSON object) adds headers to the websocket request.

## Webhooks

Events are signed the [Standard Webhooks](https://www.standardwebhooks.com) way, so existing verification libraries work. By hand:

```js
import { createHmac, timingSafeEqual } from 'node:crypto'

function verify(rawBody, headers, secret) {
  const key = Buffer.from(secret.slice('whsec_'.length), 'base64')
  const signed = `${headers['webhook-id']}.${headers['webhook-timestamp']}.${rawBody}`
  const expected = Buffer.from(createHmac('sha256', key).update(signed).digest('base64'))
  // during a secret rotation two signatures arrive, separated by a space
  return headers['webhook-signature'].split(' ').some((entry) => {
    const given = Buffer.from(entry.split(',')[1] ?? '')
    return given.length === expected.length && timingSafeEqual(given, expected)
  })
}
```

- Events: `monitor.changes.detected` and `monitor.paused` by default, `monitor.run.completed` on request.
- A failed delivery is retried after 5 seconds, 5 minutes, 30 minutes, 2, 5 and 10 hours. Redirects count as failures. The monitor keeps running meanwhile; only an event that fails all 7 attempts pauses it with `pause_reason: webhook_failing`.
- After a secret change the old secret keeps signing alongside the new one for 24 hours.
- URLs on localhost or private addresses are refused unless `ALLOW_PRIVATE_URLS=1`. The check reads the hostname as written, so a public name that resolves to a private address is not caught.
- Every attempt is listed at `GET /v1/monitors/{id}/deliveries`.

## Dashboard

Set `DASHBOARD_USER`, `DASHBOARD_PASSWORD` and `SESSION_SECRET`, then open the server's root URL. Without all three, `/` returns 404.

- With no monitors yet it opens a three-step setup: pick an example, set the goal, schedule and webhook, then watch the first run.
- The main view is a feed of findings (search results, and page changes as before and after lines), findings per day, and failed runs or failing webhooks under "Needs attention". Monitors can be created, edited, run, paused and deleted there.
- The API page shows the base URL, copyable curl examples and a webhook verification snippet. "Copy for AGENTS.md" copies a short section an AI agent can follow to use the API.
- Logins are server-side sessions that last 12 hours. Five wrong passwords lock that username and IP for 15 minutes. Serve it over HTTPS so the session cookie is marked `Secure`.

## Telemetry

Set `OTEL_EXPORTER_OTLP_ENDPOINT` (and `OTEL_EXPORTER_OTLP_HEADERS`, url-encoded) to export traces, counters and logs over OTLP/HTTP with the official OpenTelemetry packages. Grafana Cloud's free tier works. Each run is one trace covering the search or page fetches, every judge call and every webhook attempt; outgoing webhooks carry a `traceparent` header, and a run's `trace_id` is in its JSON. Secrets, page content and search results are never exported, and only the host of a webhook URL is.

On Workers, Cloudflare's own tracing is off by default; uncomment `[observability]` in `wrangler.toml` to add it.

## Development

```bash
npm test
```

The tests need no network. To include the browser test, point it at a CDP browser and a page rendered by JavaScript:

```bash
TEST_BROWSER_WS_URL=ws://127.0.0.1:9222/ TEST_JS_PAGE_URL=http://127.0.0.1:8801/index.html npm test
```

## License

MIT, see [LICENSE](LICENSE).
