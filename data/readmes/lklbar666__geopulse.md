<p align="center">
  <img src="public/logo.svg" width="96" height="96" alt="GeoPulse · GEO观脉 logo">
</p>

<h1 align="center">GeoPulse · GEO观脉</h1>

<p align="center"><sub>Observe how AI crawls. Trace what AI search brings.</sub></p>

<p align="center">
  <img alt="Node 22+" src="https://img.shields.io/badge/Node-22%2B-3572A5?style=flat-square&labelColor=3a3a3a">
  <img alt="Stack: Fastify + PostgreSQL 16" src="https://img.shields.io/badge/Stack-Fastify%20%2B%20PostgreSQL%2016-2F7D4F?style=flat-square&labelColor=3a3a3a">
  <img alt="Tracking: cookieless" src="https://img.shields.io/badge/Tracking-cookieless-C08A1E?style=flat-square&labelColor=3a3a3a">
  <img alt="Metrics: five states" src="https://img.shields.io/badge/Metrics-5%20states-B3392F?style=flat-square&labelColor=3a3a3a">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-5B4B9E?style=flat-square&labelColor=3a3a3a"></a>
</p>

<p align="center">
  <a href="#demo">Demo</a> ·
  <a href="#quick-start">Install</a> ·
  <a href="#core-design">How it works</a> ·
  <a href="#operations">Operations</a> ·
  <a href="#answer-visibility">Answers</a> ·
  <a href="#source-audit">Audit</a> ·
  <a href="#faq">FAQ</a>
</p>

<p align="center"><a href="README.zh-CN.md">简体中文</a> | <strong>English</strong></p>

Self-hosted GEO (Generative Engine Optimization) analytics for websites and AI crawlers. It puts five data lines into one site context: **visitor behaviour**, **AI crawler activity**, **content catalogue coverage**, **AI answer observations**, and **AI referral conversions**.

MIT licensed. One `docker compose up` and your data never leaves your server.

A Chinese product one-pager and ready-to-use market copy live in [`docs/PRODUCT.md`](docs/PRODUCT.md).

> **Original by design.** Independent codebase, original data contract: five-state metrics, operator-declared coverage continuity, an evidence ledger that keeps declaration and verification apart, two attribution paths that never merge, and an answer-side ledger that never pretends a sample is the population — designed here and shipped as one deployable GEO analytics system.

## Demo

https://github.com/user-attachments/assets/198dc0a3-d120-49f7-ab84-39008814cc45

A 40-second tour of the four dashboards, recorded against the built-in demo dataset.

---

## Who it is for

| Site profile | Daily focus | Where to look |
| --- | --- | --- |
| Corporate site | AI referrals to home, product, pricing and contact; coverage of commercial pages; demo / contact / trial goals | Site, then page |
| Content site | Section and article coverage; blind spots and stale pages; AI referral landing pages | Site, then page |
| Media site | Time to first crawl for new articles; section coverage; AI referral sessions and subscriptions | Site, then page |
| Developer docs | Quickstart, API and SDK coverage; version pages; AI referrals into docs | Site, then page |
| GEO team serving several sites | Compare sites in one portfolio; find integration gaps; clear failed imports before comparing business metrics | Portfolio, site, then page |

Set a profile when you create the site. It changes the suggested runbook, never a metric. Every profile can also submit AI answer observations; the profile only decides which questions and pages are worth sampling first.

```bash
curl -X POST http://localhost:3000/api/websites \
  -H "x-admin-token: $ADMIN_TOKEN" \
  -H 'content-type: application/json' \
  -d '{"name":"Docs Portal","domain":"docs.example.com","profile":"docs","timezone":"Asia/Shanghai"}'
```

`GET /api/site-profiles` returns all five playbooks (`dailyFocus`, `keyPages`, `goalExamples`, `onboarding`). `profile` is optional and defaults to `other`.

---

## What it answers

| Question | Data source | Module |
| --- | --- | --- |
| Which AI crawlers visited the site, and what did they fetch | Server / CDN access logs | AI crawlers |
| Did an AI answer mention the brand, at what rank, and which URLs did it cite | Operator-submitted answer observations | AI answers |
| Which important pages have no crawl record at all | Logs + content catalogue | Content coverage |
| Were crawl requests rejected or failing | Log status codes | AI crawlers |
| How many visitors and conversions AI search actually brought | Browser collection + goal config | Visitors / AI referrals |
| Is an AI answer grounded in verifiable sources | Submitted claims + source text | Source audit |
| PV, UV, sessions, bounce rate, duration | Browser collection | Visitor overview |

## What it does not do

No ad buying, no agency operations, no content generation. No session replay, heatmaps, cross-site tracking, or device fingerprinting.

No live querying of AI platforms, no claim that a submitted sample represents all users, and no composite GEO score. Answer observations are operator samples, and mention is not recommendation.

---

## Quick start

### Docker (build from source)

```bash
cp .env.example .env
# edit .env: APP_SECRET and POSTGRES_PASSWORD must be random values
docker compose up -d --build
```

Open `http://localhost:3000`, click "Manage token" (管理令牌), and enter `ADMIN_TOKEN` (it falls back to `APP_SECRET` when unset).

### Docker (published image)

Every `v*` tag publishes a multi-tag image to GHCR:

```bash
docker pull ghcr.io/lklbar666/geopulse:0.1.0
export GEOPULSE_IMAGE=ghcr.io/lklbar666/geopulse:0.1.0
docker compose up -d --no-build
```

Unset `GEOPULSE_IMAGE` to build from source again. Release notes and assets live on the [Releases](https://github.com/lklbar666/geopulse/releases) page.

### Local development (no Docker)

You need a reachable PostgreSQL 16:

```bash
npm install
export DATABASE_URL='postgresql://geopulse:geopulse@127.0.0.1:5432/geopulse'
export APP_SECRET='local-dev-secret'
npm run migrate
npm run seed            # crawler identity registry and published official IP ranges
npm run seed:demo       # optional: demo site with 14 days of data
npm start
```

### Instrumentation

1. Create a site:

```bash
curl -X POST http://localhost:3000/api/websites \
  -H "x-admin-token: $ADMIN_TOKEN" \
  -H 'content-type: application/json' \
  -d '{"name":"My site","domain":"example.com","timezone":"Asia/Shanghai"}'
```

The returned `collect_key` is the tracker identifier.

2. Insert the tracker before `</head>`:

```html
<script defer src="https://your-geopulse-host/tracker.js"
        data-host="https://your-geopulse-host"
        data-website-id="THE_COLLECT_KEY"></script>
```

3. Custom events / conversions:

```js
geopulse('signup', { plan: 'pro' });
```

4. Import server logs (nginx combined example):

```bash
curl -X POST http://localhost:3000/api/logs/import \
  -H "x-admin-token: $ADMIN_TOKEN" \
  -H 'content-type: application/json' \
  -d "$(jq -n --arg id "$WEBSITE_ID" --rawfile log access.log \
        '{websiteId:$id, sourceName:"nginx-2026-10", format:"nginx_combined", content:$log, coverage:"continuous"}')"
```

`coverage: "continuous"` is an **operator declaration** that this log has no gaps within its time range. Only inside a declared-continuous range can zero crawl records be interpreted as "they really did not come"; otherwise the UI reports incomplete coverage.

Supported formats: `nginx_combined`, `apache_combined`, `cloudfront_tsv`, `json`.

5. Import a content catalogue (sitemap / CSV / JSON):

```bash
curl -X POST http://localhost:3000/api/content/import \
  -H "x-admin-token: $ADMIN_TOKEN" \
  -H 'content-type: application/json' \
  -d "$(jq -n --arg id "$WEBSITE_ID" --rawfile sm sitemap.xml \
        '{websiteId:$id, format:"sitemap", content:$sm}')"
```

---

## Core design

### Evidence layers

"Identified as GPTBot" is not a single claim; it is two independent facts:

| Layer | Meaning | Values |
| --- | --- | --- |
| UA declaration | The User-Agent matches an identity token in the registry | hit / miss |
| Network verification | The source IP falls inside the identity's published official ranges | `ip_match` / `ip_mismatch` / `ua_only` |

The UI presents them separately. A User-Agent can be spoofed, so "declared" never equals "verified".

Crawler activity and AI referrals are two independent paths: the former comes from logs, the latter from the browser referrer. The system never merges them causally, and never claims that a platform drove traffic just because it crawled a lot.

### Missing is not zero

Every metric carries a state:

| State | Meaning |
| --- | --- |
| `known` | Has a value |
| `known_zero` | The window is fully covered and the value really is 0 |
| `missing_input` | A required input is absent (no logs / no tracker / no catalogue) |
| `insufficient` | Input exists but cannot support a conclusion (coverage gap, sample too small) |
| `unsupported` | This metric is not supported under the current configuration |

With no logs imported, crawler views report "input missing" instead of 0.

### Privacy

- No cookies, no browser storage, no cross-site tracking
- Raw IPs are never stored: hashed with a daily salt for UV deduplication, then discarded
- Raw log lines are not kept; only parsed results and line hashes (idempotent dedupe)
- The tracker is about 0.9 KB gzipped

---

## Operations

### By site

`GET /api/portfolio/overview?from=…&to=…` returns one row per site with its profile, traffic and referral metrics, crawler requests, content coverage, collector state, log coverage and failed import count. Every coverage verdict is computed **per site** from that site's own log sources and timezone; one site's continuous log never proves another site's zero.

Read the portfolio in evidence order, not traffic order:

1. collector missing → install the tracker;
2. log coverage not proven → import logs or declare coverage honestly;
3. failed imports → inspect the run ledger;
4. only then compare AI referrals, conversions and content coverage across sites.

The **站点组合** dashboard tab shows the same table; **看页面** drills into a site's page ledger.

### By page

`GET /api/pages?websiteId=…&from=…&to=…` merges catalogue pages, pages with pageviews, AI referral landing pages, converting entry pages and crawled paths. Each row carries stateful traffic and crawl metrics plus flags:

| Flag | Meaning |
| --- | --- |
| `blind_spot` | In the catalogue, zero crawls, coverage `known` — the only case that counts as a crawl blind spot |
| `crawl_unproven` | In the catalogue, zero crawls, coverage not proven — "not seen in this window", not "never crawled" |
| `not_in_catalogue` | Crawled but absent from the catalogue |
| `crawl_errors` | Bot requests returned 4xx or 5xx |
| `stale_crawl` | Last crawl older than 30 days |
| `modified_after_crawl` | `last_modified` is later than the last crawl |
| `crawled_no_traffic` | Crawled, zero pageviews and AI referrals, and the collector is reporting |
| `ai_entry` | An AI referral session landed on this page |

When the collector is absent, page traffic fields become `missing_input` and `crawled_no_traffic` is suppressed. When log coverage is not proven, crawl fields and blind-spot counts degrade to `insufficient`. Nothing is rendered as a fake zero.

### For maintainers

`GET /api/ops/overview?websiteId=…&from=…&to=…` groups four checks:

| Check | Contents |
| --- | --- |
| Integration | Collector state and last event; log source count split into continuous / gap / unknown; log and content import freshness; bad-line rate |
| Queue | **Imports are synchronous.** There is no external queue or worker in v1. `ingest_run` is a run ledger with `running` / `succeeded` / `failed` and parse, insert and duplicate counts; it records failures, it is not a queue |
| Source quality | Unknown-bot share, IP match rate, IP mismatch rate, UA-only requests, bot error rate, bad-line rate |
| Calculation basis | Window and timezone boundary, freshness, every metric definition with its denominator and caveat, and the five-state verdicts for coverage, collector, content coverage and unknown-bot share |

```bash
curl "http://localhost:3000/api/ops/overview?websiteId=$WEBSITE_ID&from=2026-10-20&to=2026-10-26" \
  -H "x-admin-token: $ADMIN_TOKEN"

curl "http://localhost:3000/api/ops/runs?websiteId=$WEBSITE_ID&limit=20" \
  -H "x-admin-token: $ADMIN_TOKEN"
```

The dashboard **运维检查** tab renders integration, quality, the run ledger and the basis definitions. See [`docs/OPERATIONS.md`](docs/OPERATIONS.md) for the full runbook, flag table and field notes.

---

## Answer visibility

Logs prove an AI crawler came. They do not say what the answer told the user afterwards. GeoPulse closes that gap with an operator-submitted answer ledger: for a fixed question set, record whether the brand was mentioned, at what rank, which URLs were cited, and where the evidence can be checked.

```bash
curl -X POST http://localhost:3000/api/answers/import \
  -H "x-admin-token: $ADMIN_TOKEN" \
  -H 'content-type: application/json' \
  -d "$(jq -n --arg id "$WEBSITE_ID" \
        '{websiteId:$id, format:"json", source:"manual", content:({
          observations:[{
            platform:"perplexity",
            prompt:"best self-hosted GEO analytics",
            observedAt:"2026-10-25T09:30:00+08:00",
            brandMentioned:true,
            brandRank:2,
            citedUrls:["https://docs.example.com/geo/overview"],
            evidenceUrl:"https://evidence.example.com/2026-10-25/perplexity"
          }]
        } | tostring)}')"
```

The import is strict. A missing `brandMentioned` or `citedUrls` field is an error, not an implicit `false` or empty list, because defaulting would invent an observation. `observedAt` must carry a timezone, `brandRank` is only allowed on a mentioned observation, and cited URLs must be `http(s)` without embedded credentials.

`GET /api/answers/overview?websiteId=…&from=…&to=…` returns observation and prompt counts, mention rate, citation rate, average rank, evidence rate, platform and prompt breakdowns, and a citation ledger that marks own-domain URLs and whether they are in the content catalogue.

The boundaries are part of the payload, not a footnote:

- Observations are submitted by an operator, not fetched from platform APIs.
- A sample does not represent all users; answers vary by account, region, model and time.
- Mention is not recommendation, and rank is not citation.
- With fewer than 10 observations, rates are `insufficient`; with none, every answer metric is `missing_input`, never 0.
- Crawl observations, answer observations and browser referrals stay three separate ledgers. No causal join.

There is deliberately no composite score. See [`docs/ANSWER-VISIBILITY.md`](docs/ANSWER-VISIBILITY.md) for the field contract, error codes and sampling protocol, and [`docs/POSITIONING.md`](docs/POSITIONING.md) for why GeoPulse refuses to rank sites on one number.

---

## Source audit

GeoPulse also audits the claims an AI answer is built from. You submit atomic claims plus the source text you rely on; the audit runs seven deterministic checks — deep encoding, structured storage, near/far transfer, necessary difficulty, metacognitive calibration, adaptive correction and generation — plus an evidence gate that resolves every citation and verifies every quote against the supplied source text.

```bash
curl -X POST http://localhost:3000/api/audit/source \
  -H "x-admin-token: $ADMIN_TOKEN" \
  -H 'content-type: application/json' \
  -d @audit.json
```

The response ends in one of four verdicts: `grounded`, `qualified`, `unsupported` or `contradicted`. A factual claim with no citation is `unsupported`; a citation to a nonexistent source, or a quote that does not appear in the source text, is `contradicted`. A declared `verified` confidence is downgraded when no primary source supports it.

The audit never turns a missing input into a pass, and it never emits a hallucination probability: `hallucinationRate` is deliberately `{ "state": "unsupported", "value": null }`. A checklist can make fabrication visible and block it from passing; it cannot prove a source is correct, detect misleading framing, or drive hallucination to zero.

`GET /api/audit/rubric` returns the field contract, finding codes and limits. The dashboard's **信源审计** tab provides the same entry point with a sample payload. See [`docs/SOURCE-AUDIT.md`](docs/SOURCE-AUDIT.md) for the full protocol.

---

## Modules and API

| Module | Endpoints | Purpose |
| --- | --- | --- |
| Collection | `POST /api/collect` | Browser pageviews / events, CORS enabled, rate limited |
| Tracker | `GET /tracker.js` | 1.5 KB collection script |
| Logs | `POST /api/logs/import` `GET /api/logs/sources` `POST /api/logs/coverage` | Parse, identify, declare coverage |
| Content | `POST /api/content/import` `GET /api/content/coverage` `GET /api/content/blind-spots` `GET /api/content/freshness` | Catalogue and coverage |
| Answers | `POST /api/answers/import` `GET /api/answers/overview` `GET /api/answers/platforms` | Operator-submitted answer observations: mention, rank, citations, evidence |
| Visitors | `GET /api/stats/overview` `GET /api/stats/timeseries` `GET /api/stats/breakdown` | PV/UV/sessions/bounce/duration/conversions |
| Crawlers | `GET /api/crawlers/overview` `GET /api/crawlers/identities` `GET /api/crawlers/purposes` `GET /api/crawlers/paths` | Ledger and distributions |
| Referrals | `GET /api/referrals/overview` `GET /api/referrals/platforms` `GET /api/referrals/landing-pages` `GET /api/referrals/conversions` | AI referrals and conversions |
| Site profiles | `GET /api/site-profiles` | Five audience playbooks and supported `profile` ids |
| Portfolio & pages | `GET /api/portfolio/overview` `GET /api/pages` | Multi-site comparison, page ledger and flags |
| Operations | `GET /api/ops/overview` `GET /api/ops/runs` | Integration, run ledger, source quality, calculation basis |
| Source audit | `POST /api/audit/source` `GET /api/audit/rubric` | Seven-layer claim audit and evidence gate |
| Admin | `GET/POST /api/websites` `GET/POST /api/goals` `GET /api/registry` | Sites, goals, identity registry |
| Health | `GET /api/health` | Includes database connectivity |

Every endpoint except `/api/collect`, `/api/health`, `/tracker.js`, and static assets requires the `x-admin-token` header.

## Metric definitions

| Metric | Definition | Caveat |
| --- | --- | --- |
| UV | Distinct `visitor_hash` within the window | **Not additive across days**; the system deduplicates over the whole window |
| Session | 30 minutes of inactivity | Split server-side by visitor hash, no cookie; the salt rotates daily so sessions always split at day boundaries |
| Bounce | A session with ≤ 1 pageview and no events | |
| Average duration | Last event − first event in a session | Single-page bounce sessions are excluded from the denominator |
| Coverage | Catalogue pages with crawl records / total catalogue pages | Only available while log coverage is continuous |
| AI referral share | AI referral sessions / all sessions | Unrelated to crawl volume |
| IP verification pass rate | `ip_match` / identified declarations | Unidentified requests are not in the denominator |
| Page blind spot | Catalogue page with zero crawl requests inside a continuous log window | Degrades to `crawl_unproven` when coverage is not proven |
| Unknown bot share | Bot requests without an identity / all bot requests | Unidentified is not the same as non-bot |
| Bad-line rate | Bad lines / (parsed + bad) across log sources | Check format and ingestion before trusting crawler numbers |
| Mention rate | Answer observations with `brandMentioned: true` / all answer observations | Below 10 observations the state is `insufficient`; the sample is not the population |
| Citation rate | Answer observations with at least one cited URL / all answer observations | A cited URL is not a recommendation, and an absent URL is not proof of never being cited |
| Average rank | Mean `brandRank` across mentioned observations that recorded a rank | Rank is an operator-recorded position in one answer, not a platform-wide ordering |
| Evidence rate | Answer observations with `evidenceUrl` / all answer observations | Measures retrievability of the observation, not whether the answer is true |

Identities without published ranges (most Chinese platforms, plus vendors not yet seeded) can only ever reach `ua_only`. That is an evidence boundary, not a defect. The seed ships OpenAI's GPTBot / OAI-SearchBot / ChatGPT-User ranges; add other vendors to `db/seed/ip-ranges.json` and rerun `npm run seed`.

## Project layout

```
src/
  app.js              Fastify wiring, auth, CORS, static assets
  server.js           process entry
  config.js           environment variables
  db.js               PostgreSQL connection and transactions
  tracker/tracker.js  browser collection script
  lib/                log parsing / crawler identification / UA / referrer / timezone / metric states / site profiles / source audit / answer observations
  repositories/        parameterised SQL (ingest / analytics incl. portfolio, pages, operations and answers)
  routes/             collect / logs / content / answers / query / ops / audit / admin
db/
  migrations/         append-only migrations (001 core, 002 operations, 003 answer visibility)
  seed/               crawler registry, official IP ranges, AI platform table
public/                dashboard (vanilla JS + local ECharts)
scripts/               migrations, seeds, demo data
test/                  node:test unit and API tests
docs/ARCHITECTURE.md   module breakdown, data dimensions, data flow, constraints, acceptance criteria (Chinese)
docs/OPERATIONS.md     five site profiles, daily runbook, maintainer checks, API reference (Chinese)
docs/ANSWER-VISIBILITY.md  answer observation contract, metric states, platform registry, sampling protocol (Chinese)
docs/POSITIONING.md    market position, capability comparison, anti-segments, no-overclaim rules (Chinese)
docs/SOURCE-AUDIT.md   seven-layer audit contract, verdicts, finding codes, limits (Chinese)
.github/workflows/     ci (push/PR tests) and release (tag: test, build and push the image to GHCR)
```

## Tests

```bash
npm test
```

Covers: log parsing (four formats + malformed lines), crawler identification (UA / IP ranges / unknown bots), referral attribution, timezone-local days, session splitting, metric state machine, site profiles, page flags, portfolio and operations basis, answer observation parsing and summarisation (strict fields, prompt hashing, sample states, citation attribution), source audit (seven layers, evidence gate, confidence calibration, verdict ordering), API auth and CORS. 92 tests pass.

## FAQ

**Why do crawler views say "input missing" instead of 0 before I import logs?**

Because a missing input and an observed zero are different facts. Zero is only asserted when a log source covering the whole window has been imported and declared `continuous`. Otherwise the metric state is `missing_input` or `insufficient`, and the UI says so instead of drawing a fake zero.

**GPTBot is identified, but the network check stays `ua_only`. Is something broken?**

No. `ua_only` means the User-Agent matched the registry, but the source IP is not inside a range this project has data for. The seed ships OpenAI's GPTBot / OAI-SearchBot / ChatGPT-User ranges; most other vendors — especially Chinese platforms — do not publish ranges. Add any vendor that does to `db/seed/ip-ranges.json` and rerun `npm run seed`.

**A platform crawls heavily. Does that mean it sends me traffic?**

Not necessarily. Crawling is observed from server logs; AI referrals are observed from browser referrers. They are stored and displayed as two independent paths. High crawl volume with zero referral sessions is a normal, meaningful state.

**Does GeoPulse monitor live AI answers?**

No. GeoPulse never calls a platform API or scrapes an AI answer. You submit observations — platform, question, time, whether the brand was mentioned, rank, cited URLs and an evidence link — and GeoPulse stores, deduplicates and summarises them. That is why the UI says "operator sample" rather than "AI visibility". Live querying would require platform access this project does not have, and a handful of queries would still not represent all users.

**Why is there no composite GEO score?**

Because a single number hides the two things that decide whether it means anything: the denominator and the evidence. A site with 12 observations on three platforms and a site with 4 observations on one platform cannot share a 0–100 scale, and a score would make that difference invisible. GeoPulse reports the numerator, the denominator and the metric state instead; when the sample is below 10, the rate is `insufficient` rather than a number. See [`docs/POSITIONING.md`](docs/POSITIONING.md).

**Does a mentioned brand mean the AI recommended it?**

No. A mention can be a comparison, a caveat or a criticism. GeoPulse records that the brand appeared and, when supplied, its position; it does not infer sentiment or recommendation. Rank and citations are separate fields, and neither proves the other.

**Why can't I add up daily UV numbers?**

Visitor hashes use a per-day salt, so the same person has a different hash on different days by design. GeoPulse deduplicates UV across the requested window; summing daily figures double-counts returning visitors.

**What data leaves my server?**

Nothing by default. No cookies, no browser storage, no cross-site tracking. Raw IPs are hashed with a daily salt and then discarded; raw log lines are not kept, only parsed rows and line hashes.

**Does the seven-layer audit guarantee a hallucination rate of zero?**

No, and it does not claim to. The audit is a deterministic checklist plus an evidence gate: it can catch a fabricated citation, a quote that is absent from the supplied source text, a factual claim with no source, or a `verified` confidence with no primary source behind it — and it makes those claims fail instead of passing. It cannot prove a source is correct, detect cherry-picking or misleading framing, or measure a probability. That is why `hallucinationRate` is always `{ "state": "unsupported", "value": null }`; a score of 100 means the submitted evidence passed every check, not that the conclusion is true.

**Is the import queue asynchronous?**

No. Log and content imports run synchronously inside the HTTP request. The operations view's "queue" is the `ingest_run` ledger: it records `running` / `succeeded` / `failed`, parse counts, inserted rows, duplicates and the failure message. It is useful for finding a broken import; it is not an external message queue, it does not retry, and the `queued` status is reserved for a future async implementation that v1 does not ship.

**Does a site profile change what is measured?**

No. `corporate`, `content`, `media`, `docs` and `agency` change the suggested daily focus and onboarding steps shown in the dashboard and returned by `GET /api/site-profiles`. Every profile is measured with the same five-state metric contract. An unset profile is `other`.

**Can I run it next to Google Analytics or another web-analytics tool?**

Yes. The tracker is namespaced and about 0.9 KB gzipped. GeoPulse is not a general web-analytics replacement; it is the GEO layer — crawler evidence, catalogue coverage and AI referral attribution.

## License

MIT, see [LICENSE](LICENSE).

### Originality

GeoPulse is an independent implementation. The schema, parameterised SQL, crawler identity registry, four log parsers, metric state machine, tracker, dashboard and documentation were designed and written in this repository; no source code was copied from another analytics project. Ideas travel, code does not — the contracts below are this project's own.

Eight designs originate here:

1. **A five-state metric contract.** Every metric crosses the API boundary together with its state, so "not measured" cannot be silently charted as 0.
2. **Coverage continuity as an operator declaration.** A zero crawl result is only assertable inside a log range explicitly marked `coverage: "continuous"`; otherwise the conclusion degrades to `insufficient`.
3. **An evidence ledger keyed by log-line hash.** UA declaration, network verification, source and time window are stored as separate fields of one idempotent ledger — "identified" never silently becomes "verified".
4. **Two attribution paths with no causal join.** Crawl observations (server logs) and AI referrals (browser referrers) share a site context but are never joined causally, so crawl volume cannot masquerade as traffic.
5. **Privacy enforced by the schema.** Cookieless visitor hashes with a daily-rotating salt, no raw IP storage and no raw log retention — the privacy model lives in the database and the code, not in a policy page.
6. **A source audit that refuses to emit a probability.** The seven processing layers and an evidence gate yield four verdicts with score caps; missing inputs never pass, and the response states outright that a rubric cannot estimate a hallucination rate rather than inventing one.
7. **An operations surface that does not impersonate a queue.** Imports stay synchronous, and the UI says so. The run ledger exposes statuses, counts and failure reasons under the name it deserves, instead of dressing a request-scoped write as a background job.
8. **An answer-side ledger that separates observation from representativeness.** Mention, rank, citation and evidence are different columns; every ratio carries a minimum sample and a state; and no composite score is produced, because a single number would hide which of those four facts it came from.

What is first-of-its-kind here is the combination: five data lines — **visitor behaviour, AI crawler activity, content catalogue coverage, AI answer observations, AI referral conversions** — in one site context, with every evidence constraint active at once, inside a single `docker compose up`. That is the design goal GeoPulse set out to land, and it is the part we consider original work rather than a feature list.
