<p align="center">
  <img src="docs/screenshots/social-banner.png" alt="HireSignal — private, local job-search engine for technical roles" width="100%">
</p>

# HireSignal Personal Edition

[![CI](https://github.com/vinaygiri/hiresignal-personal/actions/workflows/ci.yml/badge.svg)](https://github.com/vinaygiri/hiresignal-personal/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
![Next.js 15](https://img.shields.io/badge/Next.js-15-black?logo=next.js)
![TypeScript](https://img.shields.io/badge/TypeScript-blue?logo=typescript&logoColor=white)
![LLM: Ollama or any provider](https://img.shields.io/badge/LLM-Ollama%20%C2%B7%20Gemini%20%C2%B7%20OpenAI-4c8bf5)
![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)

> **Your private, local job-search engine for technical roles** — semantic résumé matching, AI
> fit-scoring, company due-diligence, and assisted apply (it fills the form; you press Submit).
> Runs on your machine, for free.

![HireSignal demo](docs/screenshots/demo.gif)

> 📖 **New here?** The [**User Manual**](docs/USER-MANUAL.md) covers the whole workflow — first run,
> how the fit score is built (and its limits), what applying actually does, expected timings, and
> what to do when a free LLM quota runs out.

A single-user, localhost job-search tool for **software, engineering, architecture, data, and DevOps
roles** (healthcare-IT first, but it works across industries). It ingests jobs from ATS APIs, job
boards, and **company career pages**, matches them against your résumé with vector search, keeps the
list **fresh and valid** (dead/expired jobs are auto-retired), rates the best fits with an LLM, and
assists you through applying. Runs entirely on your machine.

> **Scope — technical roles only.** HireSignal is built for engineering/technical jobs. Non-technical
> postings (sales, marketing, recruiting, HR, etc.) are filtered out on broad sources and heavily
> down-ranked everywhere else. Seniority is **adaptive to your résumé**: it keeps senior/architect
> roles by default, and includes junior/entry-level *technical* roles when your résumé is early-career.

## Table of contents

- [Features](#features)
- [Screens](#screens)
- **[Full user manual](docs/USER-MANUAL.md)** — day-to-day guide, scoring explained, timings
- **[What's new in v1.0.0](docs/RELEASE-v1.0.0.md)** — measured before/after, and what changed about applying
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [First run](#first-run-walkthrough)
- [Daily usage](#daily-usage)
- [Scripts](#scripts)
- [Configuration](#configuration-envlocal)
- [Tech stack](#tech-stack)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [Cost](#cost)
- [Responsible use](#responsible-use)
- [License](#license)

## Features

- **Hybrid matching, scored 0-100** — meaning (vector search via sqlite-vec) *and* wording (BM25),
  fused by rank, then combined with **skill overlap against your résumé** (25%), the AI's verdict
  (25%) and context (10%). Your career targets are hard constraints, not hints: a deal-breaker caps
  a job at 15. Every row shows *why* it scored what it did — problems first.
- **37,000 company boards, searchable** — `npm run sync:directory`, then find any company by name in
  `/import` and pull its whole board. 14 ATS platforms are supported via their public APIs.
- **AI evaluation & company briefs** — per-job fit scoring plus recession-resilience due-diligence
  (financials, layoffs, culture, legitimacy).
- **Freshness & validity engine** — ingestion isn't append-only; stale/delisted jobs and dead links
  are auto-retired so the list stays genuine.
- **Assisted apply** — opens the real application form in a visible browser, fills the standard
  fields, attaches your résumé and cover letter, and hands off to you to review and click Submit.
  It never submits on your behalf. Boards that need a login (LinkedIn, Lever, Indeed) show a plain
  "Apply on company site" link instead. *No ATS offers applicants a submission API — Greenhouse's
  requires an employer key (HTTP 401 without one) and Ashby's is behind reCAPTCHA — so assisted
  apply is the only honest automation, and it's the one that works.*
- **Company intelligence** — Levels.fyi compensation, AmbitionBox (India) ratings, and layoff history,
  cached per company.
- **Multi-résumé library** — keep several résumés (e.g. generic + specialized) and switch the active one.
- **Local & private** — one SQLite file on your machine; no account, no cloud storage.
- **Bring any LLM** — Ollama by default; or Gemini, OpenAI, Groq, Anthropic. Embeddings run locally or
  in the cloud, so you can run **without Ollama** entirely.

## Screens

![Matches dashboard](docs/screenshots/dashboard.png)
*Two-pane matches — a scored job list with Place / fit / role filters and applied badges on the left, and the AI evaluation, company brief, and apply options for the selected job on the right.*

<p align="center">
  <img src="docs/screenshots/job-detail.png" width="48%" alt="Job detail — AI evaluation and company brief" />
  <img src="docs/screenshots/company-finder.png" width="48%" alt="Find a company — search ~37,000 career boards by name" />
</p>
<p align="center">
  <img src="docs/screenshots/settings.png" width="48%" alt="Settings — chat providers and the embeddings card" />
  <img src="docs/screenshots/guide.png" width="48%" alt="Built-in user guide" />
</p>

## Prerequisites

- Node.js 18+ (tested on 20/24)
- **Embeddings** power the whole matching engine. By default they run on **local Ollama** — free,
  CPU-only, no GPU (`nomic-embed-text` is ~275 MB):

```bash
ollama pull nomic-embed-text    # embeddings (required unless you use a cloud embedding provider)
ollama pull llama3.2            # optional: local chat fallback
```

**No Ollama? You can run entirely on the cloud.** Point embeddings at Gemini or OpenAI by setting
`EMBEDDING_PROVIDER` + a key in `.env.local` (see **Configuration**). The chat LLM (résumé parsing,
role suggestions, evaluations, cover letters) also defaults to Ollama but can use any provider —
see **LLM provider**. So the minimum is just **HireSignal + one LLM source** (Ollama *or* a cloud key).

## Setup

```bash
npm install
cp .env.example .env.local     # edit if you want a non-default LLM or knobs
ollama serve                   # make sure Ollama is running
```

## First run (walkthrough)

1. **Start the app:** `npm run dev` → open http://localhost:3000
2. **Upload your résumé:** go to `/profile`, drop your PDF (optionally give it a label like
   "Healthcare" or "Generic"). It's parsed + embedded, becomes the **active** résumé, and the app
   **auto-suggests target roles** from it.
   - **Multiple résumés:** upload more than one (e.g. a generic and a healthcare-specific version).
     The **Resume library** on `/profile` lets you switch which is active or delete one. The active
     résumé drives matching, evaluations, and generated documents; switching recomputes your matches.
3. **Pick your roles:** on `/profile`, the "Recommended from your résumé" chips are all on by
   default — deselect any you don't want, or hit **Regenerate**, then **Save**. These roles drive
   which jobs get hunted and rank matching titles higher.
4. **Get jobs + make them matchable — run the full daily loop:**
   ```bash
   npm run daily
   ```
   This runs, in order: ingest all sources → discover company career pages → embed → prune stale →
   verify links → evaluate the top matches. **The first run is the long one — see timing below.**
5. **View your matches:** http://localhost:3000 — fresh, validated, rated best-fits with badges.

> **⏱️ Heads-up — the first sync can take a while (often ~1–3+ hours).** This is expected, not a hang.
> The slow step is **embedding**: on local Ollama it's CPU-bound (~1–1.5 jobs/sec, no GPU), so
> thousands of freshly-ingested jobs take hours to embed. A **cloud embedding provider** (see
> *Configuration → Embeddings*) is dramatically faster. It runs in the background — leave it going;
> the sidebar shows live step progress and a running job counter, and you can keep browsing.
> **Rating** the top matches is also LLM-quota-sensitive and paced. Later syncs are far quicker —
> they only embed *new* jobs.
>
> Separately, the shipped database may contain old/stale postings; pruning retires anything not
> re-seen at its source, so the first run replaces them with fresh jobs. Prefer a clean start?
> `npm run db:reset` then `npm run daily`.

## Daily usage

**In the app (recommended):** click **Sync** in the sidebar.
- **Quick** (the Sync button): re-embed the backlog, prune stale/dead, verify links, re-rate the top
  matches. No scraping. Usually a minute or two — but longer if a lot of jobs still need embedding.
- **Full** (the ▾ menu → "Full sync"): also fetches new jobs from all sources + discovers company
  pages, then embeds them. **Duration scales with how many new jobs are found** — a few minutes for a
  small delta, but **potentially an hour or more** on the first run or when many new jobs need
  embedding on CPU Ollama (cloud embeddings are far faster). Launches headless browsers; shows live
  step progress + job counter; cancellable anytime, and it survives you browsing around.

The sidebar shows "last synced" + how many jobs are active/rated. Matches refresh automatically when
a sync finishes.

**From the terminal** (equivalent to a Full sync) — still available for automation:

```bash
npm run daily
```

Then browse matches at http://localhost:3000. The dashboard is a **two-pane** view: pick a job on the
left, its full match / AI evaluation / company brief / apply options load on the right. Apply manually
or use **Open & autofill** to have the form filled for you before you submit it yourself.

### Add a company's whole job board

**Easiest — search 37,000 boards.** Run `npm run sync:directory` once (~7 MB), then open
`/import` → **Find a company**, type a name, and click **Add & pull**. Each result arrives *with*
its board URL, so there is no careers-URL hunting. It seeds the company for future syncs and can
pull the board immediately.

> A result badged **"loose match"** is a substring guess, not a hit — searching "Elevance" also
> surfaces "Relevance AI". Check the name and ATS before adding.

**Other ways:** paste a company name or careers URL into `/import` → "Discover from career page",
or add lines to `scripts/data/companies.txt` and run `npm run discover && npm run embed`.

**14 ATS platforms are pulled via their public APIs** — every one verified against a live board:

| | | |
|---|---|---|
| Greenhouse | Lever | Ashby |
| SmartRecruiters | Recruitee | Workday |
| Workable | Breezy HR | Pinpoint |
| BambooHR | Personio | Teamtailor |
| Rippling | Manatal | |

**Workday needs a URL, not a name** — a pull requires the tenant, data-centre host and site, none of
which can be derived from a company name. The directory supplies all three for 3,530 Workday
employers; otherwise paste the `something.wdNN.myworkdayjobs.com/Site` URL from their job board.

Anything on another ATS falls back to a page crawl, which recovers little on large corporate sites
and says so rather than importing navigation links as jobs.

## Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start the app on http://localhost:3000 |
| `npm run daily` | **Full loop:** ingest:all → discover → embed → prune → verify:links → evaluate:top |
| `npm run ingest:all` | Pull all job-board/ATS sources |
| `npm run discover` | Pull company career pages listed in `scripts/data/companies.txt` |
| `npm run embed` | Generate embeddings for jobs missing them |
| `npm run reembed` | Re-embed everything **in place** after switching embedding provider (keeps applications/tracker/résumés; `-- --dry` previews) |
| `npm run prune` | Retire stale (`STALE_DAYS`) / dead-link jobs |
| `npm run verify:links` | HTTP-check the top matches; expire dead links |
| `npm run evaluate:top` | LLM-evaluate the top `MATCH_LIMIT` matches |
| `npm run sync:directory` | Download the ~37k company career-board directory (one time, ~7 MB) |
| `npm test` | Run the Vitest suite (90 tests) |
| `npm run test-apply` | Dry-run auto-apply smoke test (no real submit) |
| `npm run test-freeway` | Live smoke test of the Freeway LLM gateway |
| `npm run backup` | Back up the database |
| `npm run build` / `npm run start` | Production build / serve |
| `npm run db:reset` | Delete the database and start fresh |

Individual ingest sources also exist: `ingest` (Greenhouse + Lever), `ingest:hn`, `ingest:remote`,
`ingest:ashby`, `ingest:himalayas`, `ingest:wwr`, `ingest:4dayweek`, `ingest:linkedin`,
`ingest:hirist`, `ingest:jobspy`, `ingest:layoffs`.

> `ingest:naukri` exists but returns nothing — Naukri blocks automated access (a browser request
> gets "Access Denied"). Getting past that would mean defeating bot protection, so it is left as-is.

## Configuration (`.env.local`)

| Var | Default | Purpose |
|-----|---------|---------|
| `MATCH_LIMIT` | `30` | How many best-fit matches to show/cache/auto-evaluate (set 20–50) |
| `STALE_DAYS` | `21` | Retire jobs not re-seen at their source for this many days |
| `LINK_RECHECK_HOURS` | `24` | How often `verify:links` re-checks a URL |

**Chat LLM provider:** defaults to local Ollama (free, private). Set `GEMINI_API_KEY` (free tier,
1500 req/day) for materially better quality, or configure any provider (OpenAI, Anthropic, Groq,
etc.) in the app at `/settings`. Chat has a built-in fallback chain (rotates keys, then Ollama) so
a rate-limited provider degrades instead of failing.

**Embeddings provider (the matching engine):** defaults to Ollama. To run without Ollama, set these
in `.env.local`:

| Var | Default | Purpose |
|-----|---------|---------|
| `EMBEDDING_PROVIDER` | `ollama` | `ollama` \| `gemini` \| `openai` \| `openai-compatible` |
| `EMBEDDING_MODEL` | per-provider | e.g. `nomic-embed-text` / `text-embedding-004` / `text-embedding-3-small` |
| `EMBEDDING_API_KEY` | — | cloud key (falls back to `GEMINI_API_KEY` / `OPENAI_API_KEY`) |
| `EMBEDDING_BASE_URL` | per-provider | required for `openai-compatible` |

The active provider is shown in `/settings`. ⚠️ **All embeddings in one DB must use the same model.**
Changing the provider on an existing DB means re-embedding — use `npm run reembed` (in place, keeps
your data) rather than `npm run db:reset`. The app **refuses** to mix embedding spaces with a clear
message. Embeddings on Ollama have no quota; a cloud embedding key can hit a daily cap (embedding
pauses until reset). See `.env.example` for all options.

**Optional — [Freeway](./docs/freeway.md):** if you want quota-proof **chat** across ~20 free
providers (auto-routing, key rotation, fallback), point HireSignal's chat at your local Freeway
gateway as an `openai-compatible` provider. Freeway is a chat gateway only; embeddings stay on
Ollama or a direct key. Fully optional — HireSignal never depends on it.

## Tech stack

- **App:** Next.js 14 (App Router), TypeScript, Tailwind CSS
- **Storage:** SQLite (better-sqlite3) + [sqlite-vec](https://github.com/asg017/sqlite-vec) for on-device vector search
- **Embeddings:** Ollama (`nomic-embed-text`) by default, or Gemini / OpenAI
- **Chat LLM:** any provider — Ollama, Gemini, OpenAI, Groq, Anthropic (configured in-app)
- **Automation:** Playwright (career-page discovery, form autofill, PDF rendering)

## Troubleshooting

**Résumé upload fails or hangs** — this is almost always the embedding provider. The error message
names which one and what went wrong.
- **On Ollama (default):** make sure it's running and responsive — `curl http://127.0.0.1:11434/api/tags`.
  If it hangs, the process is stuck — restart it (quit the tray app / kill `ollama.exe`, then reopen).
  **Use `127.0.0.1`, not `localhost`, in `OLLAMA_BASE_URL`** (on Windows `localhost` can resolve to
  IPv6 `::1` and flake against Ollama — the #1 cause). Ensure the model is pulled:
  `ollama pull nomic-embed-text`.
- **On a cloud embedding provider:** check `EMBEDDING_API_KEY` is valid and you haven't hit the
  daily/rate limit (embedding pauses until it resets).
- Very long résumés are auto-truncated to fit the embedder's context, and transient errors retry
  automatically — neither is a failure cause.

**"Embedding provider mismatch" / matches look wrong after changing `EMBEDDING_PROVIDER`** — a DB's
embeddings must all use one model. Re-embed in place with `npm run reembed` (keeps your applications,
tracker, and résumés), or set the provider back to what it was. `/settings` shows the active provider
and flags a mismatch.

**Rating / generation slow or failing (quota)** — your cloud chat key likely hit its daily limit.
Add another provider in `/settings` (the chat fallback chain rotates automatically), run "Rate top
matches" when quota resets, or route chat through [Freeway](./docs/freeway.md) for automatic
multi-provider failover.

## Contributing

Contributions are welcome — new job sources, matching improvements, bug fixes, and docs. See
[CONTRIBUTING.md](./CONTRIBUTING.md) for the dev setup and guidelines, and please follow the
[Code of Conduct](./CODE_OF_CONDUCT.md). Security issues? See [SECURITY.md](./SECURITY.md).

## Cost

**$0** on local Ollama — no API keys, no billing. Optional hosted LLMs (Gemini free tier, Groq free
tier) keep it free too; paid providers are strictly opt-in.

## Responsible use

HireSignal is a **single-user, localhost personal tool**. It has no authentication and stores one
person's profile, résumés, and applications — do **not** deploy it as a public/multi-user service.

By using it you agree that:

- **You are responsible for complying with the Terms of Service** of every site it accesses
  (LinkedIn, Naukri, Greenhouse, Ashby, Lever, Levels.fyi, AmbitionBox, Layoffs.fyi, company career
  pages, etc.). Some sites prohibit automated access or rate-limit aggressively. Scrape only what
  you're permitted to, and keep the built-in polite delays.
- **You are the one who submits.** HireSignal fills the form in a visible browser and stops; it
  never clicks Submit. Read what it filled before you send it — the résumé, the cover letter and
  every screening answer are your words once submitted, and you are accountable for them. Keep the
  rate limits, and never let it answer a question you would not answer yourself.
- **Keep your data private.** Your résumé PDFs, the SQLite database (`data/`), and `.env.local`
  (API keys) are gitignored and must never be committed or shared.
- The software is provided "as is", without warranty (see LICENSE). Job data comes from third-party
  sources and may be incomplete, stale, or wrong — verify before acting.

## License

[MIT](./LICENSE) © 2026 [vinaygiri](https://github.com/vinaygiri)
