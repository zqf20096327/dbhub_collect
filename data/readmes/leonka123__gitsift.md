# GitSift

**Find the repo before it is obvious.**

GitSift is an open-source radar for new and rising GitHub repositories. It reads the public
firehose, drops the forks, list repos and bought stars, ranks what is actually moving — and tells
you, in one paragraph, why it deserves ten minutes of your Saturday.

It runs on one Node process and a local SQLite file. No API keys, no external services, no
telemetry.

[![CI](https://img.shields.io/github/actions/workflow/status/leonka123/gitsift/ci.yml?branch=main&style=flat-square&label=CI)](https://github.com/leonka123/gitsift/actions/workflows/ci.yml)
[![MIT](https://img.shields.io/github/license/leonka123/gitsift?style=flat-square&color=2b1f18)](LICENSE)
[![Node 22+](https://img.shields.io/badge/node-22%2B-2b1f18?style=flat-square)](package.json)
[![No API keys](https://img.shields.io/badge/api%20keys-none-c03217?style=flat-square)](#quick-start)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-c03217?style=flat-square)](CONTRIBUTING.md)

![GitSift home page — an editorial radar with a signal-ranked ledger](docs/home-light.png)

## The problem with star leaderboards

GitHub Trending sorts by raw stars, which rewards the past. A five-year-old project with 80k stars
outranks a three-week-old tool adding 200 stars a day — and neither tells you whether the code is
real, maintained, or useful to what you are building.

GitSift ranks momentum, not magnitude:

| | GitHub Trending | GitSift |
| --- | --- | --- |
| Ranking input | total stars | stars/day, age, activity, quality prior |
| Star spikes | invisible | penalised by a bot score |
| Dead or archived projects | mixed in | filtered before scoring |
| "Why should I care?" | nothing | a factual reason and a weekend-sized build idea |
| Search | keywords | hybrid lexical + semantic, English and Russian |
| Code | closed | MIT, self-hostable, auditable |

The full formula is public, unit-tested and documented on the [method page](src/app/about/page.tsx)
and in [`src/lib/scoring.ts`](src/lib/scoring.ts).

## What is inside

- **Rising** — the live ledger, one row per repository, each with a percentile score on a
  five-step signal scale.
- **New** — repositories created in the last 7 / 30 / 90 days, ranked without long star history to
  lean on.
- **Hidden gems** — 20–900 stars, at least 1.5 stars/day, still small enough that the maintainer
  answers issues.
- **Semantic search** — describe the job, not the keyword. FTS5 + embeddings + reciprocal rank
  fusion, with English/Russian concept expansion.
- **Weekly issue** — twelve entries with "why now" and "weekend build" notes, published as RSS.
- **Public API** — the same data the pages use, no auth, cache-friendly.

<table>
  <tr>
    <td width="50%"><img src="docs/search-light.png" alt="Semantic search results for a self-hosted analytics tool" /></td>
    <td width="50%"><img src="docs/repo-light.png" alt="Repository page with signal percentile, star trajectory and similar repos" /></td>
  </tr>
  <tr>
    <td><em>Search by intent: “self-hosted analytics” → plausible/analytics, ClickHouse, langfuse.</em></td>
    <td><em>Every repository page shows the score, the trajectory and the neighbours.</em></td>
  </tr>
</table>

<details>
<summary><strong>Dark theme</strong></summary>

![GitSift home page in dark theme](docs/home-dark.png)

</details>

## Quick start

Requires **Node.js 22+**. Nothing else.

```bash
git clone https://github.com/leonka123/gitsift.git
cd gitsift
npm install
npm run dev
```

Open <http://localhost:3000>. On the first run GitSift loads the bundled **1,240-repository seed** —
real public metadata — scores it, writes summaries and embeddings, and builds the current issue.
That takes under a minute; the database is cached in `data/gitsift.db` afterwards.

![Mobile layout](docs/mobile-light.png)

> The seed is a snapshot, not a live mirror. Run `npm run ingest` to refresh from GitHub.

### Docker

```bash
docker build -t gitsift .
docker run --rm -p 3000:3000 -v gitsift-data:/app/data gitsift
```

The image seeds itself on first boot; the named volume keeps later ingests.

## How the ranking works

The raw score is a weighted sum of five signals, then converted to a percentile across the whole
index:

```text
raw = 0.50 · momentum      // log1p(stars_per_day · 7)
    + 0.16 · scale         // log10(stars + 1)
    + 0.14 · freshness     // 1 - age_days / 1100
    + 0.10 · activity      // 1 - days_since_push / 120
    + 0.24 · quality       // heuristic prior, 0..1

signal = percentile(raw × (0.55 + 0.45 · trust))   // 0..100
trust  = 1 - bot_score
```

A score of 99 means 99% of tracked repositories scored lower on the same day. The quality prior
looks at README length, license, tests, CI, release history and issue response; the bot score
penalises star spikes that do not match fork or contributor growth.

## Search

Two independent retrievals, fused with reciprocal rank fusion:

1. **Lexical** — SQLite FTS5 BM25 over names, descriptions, topics and README excerpts.
2. **Semantic** — cosine similarity over 384-dimensional embeddings.

Query terms are expanded with a small English/Russian concept dictionary before retrieval
(`src/lib/topics.ts`). With an LLM key configured, the top candidates are reranked and each result
gets a specific reason.

```bash
# English
curl "http://localhost:3000/api/search?q=self-hosted%20analytics&limit=5"

# Russian
curl "http://localhost:3000/api/search?q=инструмент%20для%20парсинга%20сайтов&limit=5"
```

The default embedding model is a zero-dependency lexical hash (`hash-384-v1`). It is fast, free and
offline; it will not understand a metaphor. Set `EMBEDDINGS_PROVIDER=openai` if that matters to you.

## Refresh from GitHub

```bash
cp .env.example .env
# GITHUB_TOKEN raises the API limit from 60/h to 5,000/h
npm run ingest
```

`npm run ingest` runs sixteen search queries, fetches READMEs for promising newcomers, records star
snapshots, recomputes signal, refreshes summaries and embeddings, and rebuilds the weekly issue.
Without a token it still works, just slowly.

Schedule it with the included GitHub Actions workflow (`.github/workflows/ingest.yml`), a cron job,
or any scheduler:

```bash
curl -X POST https://your-deployment.example/api/cron/ingest \
  -H "Authorization: Bearer $CRON_SECRET"
```

## Deploy

SQLite needs a persistent disk, so GitSift is not a good fit for stateless serverless platforms
without an external database. The included paths:

- **Docker** on any host with a volume (works on Fly.io, Railway, Render, a VPS).
- **Fly.io** with a volume — see [`fly.toml`](fly.toml) and [`docs/DEPLOY.md`](docs/DEPLOY.md).
- **A small VPS** with `npm run build && npm start` behind Caddy or nginx.

Set `NEXT_PUBLIC_SITE_URL` to the public origin (used for canonicals, sitemap, RSS and OG images)
and `CRON_SECRET` to a long random value before exposing the app.

## API

No auth, no keys, cache-friendly.

```bash
GET /api/repos?mode=rising&limit=12
GET /api/repos?mode=new&windowDays=30&language=Python&limit=12
GET /api/repos?mode=gems&minStars=50&topic=mcp
GET /api/search?q=self-hosted+analytics&limit=10&selfHosted=1
```

`mode` is `rising | new | gems | top`. Responses include the score, stars/day, topics, summary and
GitHub URL. The README body is omitted; its character count is included so clients can decide
whether to fetch it.

## Commands

| Command | What it does |
| --- | --- |
| `npm run dev` | Seed on first run, then start the dev server. |
| `npm run build` / `npm start` | Production build and server. |
| `npm run db:reset` | Wipe and rebuild the seeded database. |
| `npm run ingest` | Refresh repositories from GitHub. |
| `npm run pipeline` | ingest → score → summarize → embed → digest. |
| `npm run score` / `summarize` / `embed` / `digest` | Individual pipeline steps. |
| `npm run typecheck` / `npm test` | TypeScript and unit tests. |
| `node scripts/screenshots.mjs` | Visual QA with local Chrome or Edge. |

## Project structure

```text
src/
  app/                 routes, metadata, OG images, RSS, API
  components/          editorial UI primitives, repo rows, signal meter
  db/                  schema, migrations, typed queries
  lib/                 ingest, scoring, embeddings, search, LLM, digest
scripts/               seed, ingest, pipeline steps, visual QA
data/seed/repos.json   bundled 1,240-repository snapshot
docs/                  architecture, deployment, design direction
```

Read [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for the schema and pipeline details.

## Limitations

Honest list, because a ranking you cannot question is just another black box:

- Stars are a proxy for attention, and attention can be bought. The bot score catches clumsy
  spikes, not sophisticated campaigns.
- The index is young. Rankings improve as daily snapshots accumulate.
- Discovery queries impose thresholds (stars, recency, topics). Quiet projects below them stay
  invisible until they move.
- The default embedding is lexical, not neural.

## Roadmap

Shipped and planned work lives in [`docs/ROADMAP.md`](docs/ROADMAP.md). The short version: a hosted
demo, more snapshot history, saved searches, and broader topic coverage. Non-goals are listed too —
no paid placement, no bought stars, no login wall.

## Contributing

Issues and pull requests are welcome. Good first contributions:

- Add a topic alias or a Russian/English search expansion.
- Improve the anti-spam heuristic with a real failing example.
- Add a source query for an under-covered corner of the ecosystem.
- Improve accessibility or performance on a page you use.

Read [CONTRIBUTING.md](CONTRIBUTING.md) first. By participating you agree to the
[Code of Conduct](CODE_OF_CONDUCT.md).

If GitSift saves you an afternoon, **star the repo** — that is how the next person finds it.

## License

MIT. See [LICENSE](LICENSE).

GitSift is not affiliated with GitHub. Repository data comes from the public GitHub API; rankings are
opinionated and computed, not endorsed by maintainers.
