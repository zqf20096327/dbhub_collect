# Hacker News Search

Full-text search over the entire Hacker News corpus (~49M stories, comments, jobs and polls), served live from [Neon Lakebase Postgres](https://neon.com) with BM25 ranking. Every keystroke is a query against Postgres, and the UI is styled to feel like a search box bolted onto news.ycombinator.com.

## Design notes

- **[Next.js 16](https://nextjs.org)**: App Router, React Server Components, streaming SSR. Every page ships its shell (masthead, search box) instantly and streams the data through a React `<Suspense>` boundary keyed by the query, so navigating shows a skeleton right away instead of freezing on the previous results. The match count is a second, nested boundary that fills in after the results.
- **[Neon Lakebase Postgres](https://neon.com)** over the `@neondatabase/serverless` HTTP driver. Each request is a stateless SQL-over-HTTP round trip with no connection pool. The compute is pinned (see [`neon.ts`](neon.ts)) so there is no scale-to-zero cold start on the first query.
- **Postgres is the search engine.** `lakebase_text` with a `lakebase_bm25` index does corpus-aware BM25 ranking inside the database.
- **Per-type partial BM25 indexes.** The corpus is 85% comments, so a single shared BM25 index is a trap: it scores only its top `lakebase_bm25.default_limit` candidates (1000 by default) and _then_ applies the `type` filter, silently dropping most stories and nearly all jobs before you see them. Each searchable type gets its own **partial** index whose predicate matches the query's `WHERE` clause:

  ```sql
  CREATE INDEX items_story_bm25   ON items USING lakebase_bm25 (search_tsv) WHERE type = 'story'   AND NOT deleted AND NOT dead;
  CREATE INDEX items_comment_bm25 ON items USING lakebase_bm25 (search_tsv) WHERE type = 'comment' AND NOT deleted AND NOT dead;
  CREATE INDEX items_job_bm25     ON items USING lakebase_bm25 (search_tsv) WHERE type = 'job'     AND NOT deleted AND NOT dead;
  ```

  Ranking and counting now run over the requested type alone, so results are complete and correctly ordered at any page. `all` and the long-tail types (poll, pollopt) fall back to the full-corpus `items_search_bm25` index. The candidate limit is set per query inside a transaction, big enough to cover the page being read and opened to the cap when a residual `by`/`since` filter runs afterward.

- **Plans are steered, not left to the estimate.** Postgres estimates a multi-word match as if the words were independent. For correlated words that is badly wrong: `show hn` is estimated at 3,461 stories and is really 217,290. Left alone, the planner then picks a plan built for a tiny match set and reads every real match (3.6s). So each query shape pins its plan with `SET LOCAL` and a shape the estimate cannot flip:
  - **relevance** reads the top candidates off the BM25 index in a subquery with no `@@` filter (so the planner sees "top N of every story"), then filters them. If that leaves the page short (a rare AND, a phrase), the matches are few by definition, so they are collected through GIN and ranked exactly.
  - **date / points** walk the newest (or top-scored) rows through a btree and filter, bounded to ~20,000 rows, and fall back to GIN plus a sort when the walk comes up short.
- **Exact match counts from GIN alone.** Partial GIN indexes mirror the partial BM25 ones (`items_story_gin`, `items_job_gin`, `items_poll_gin`, plus `items_live_gin` over every live row). A bitmap scan of one reports how many row pointers it produced, which for a partial index over the query's own predicate is the exact number of matches, found without reading the heap. `countMatches` reads that number from `EXPLAIN ANALYZE` of a one-row probe: `show hn` counts 217,290 stories in ~70ms. Comments are live minus story, job and poll. Phrases, negations and `by`/`since` filters need the heap, so they keep the old race between a bounded exact count and the planner estimate. Rows changed since the last VACUUM still have index entries, so `items` is tuned to autovacuum every 20,000 changed rows instead of the default 20% of the table.
- **Typo tolerance.** `search_terms` is a lexicon of story-title words with their document counts (`npm run db:lexicon`, ~1 min), trigram-indexed, with `fuzzystrmatch` for edit distance. A query word gets a suggestion within 1 edit (up to 5 letters), 2 (up to 7) or 3 (8 or more), where swapping two neighbouring letters counts as one edit, and only when the suggestion is at least 50x more common, so rare but real words are left alone. No results as typed means the correction is searched instead ("Showing results for postgres. Search instead for postgers"). Otherwise the page offers "Did you mean …?".
- **Stopword-only queries** such as `to be or not to be` have an empty tsquery, because `search_tsv` indexes none of those words. They match the phrase in titles through the trigram index instead.
- **[Drizzle](https://orm.drizzle.team)** for the schema and migrations, **[Tailwind v4](https://tailwindcss.com)** for styling.

See [`src/lib/queries.ts`](src/lib/queries.ts) for the query builder and [`src/app/page.tsx`](src/app/page.tsx) for the streaming boundaries.

## Deployment

Deployed on Vercel in `cle1` (Cleveland), next to the Neon compute in `us-east-2`, to keep the SQL-over-HTTP round trip short. The Neon compute is pinned (see [`neon.ts`](neon.ts)) so the first query after an idle period is not paying a cold start. The dominant cost drivers are the pinned Neon compute (no scale-to-zero) and the hourly Vercel cron function, not per-request query load.

Set `DATABASE_URL_UNPOOLED` to the direct Neon connection string and `CRON_SECRET` to a random value (`openssl rand -hex 32`). Vercel sends the secret as `Authorization: Bearer …` on scheduled cron calls, which the sync route requires. Env vars are baked at build time, so redeploy after changing them.

## Local dev

1. **Install and configure.**

   ```bash
   npm install
   cp .env.example .env   # fill in DATABASE_URL_UNPOOLED
   ```

2. **Create the schema and load the corpus.** The seed streams the [ClickHouse Hacker News dataset](https://clickhouse.com/docs/get-started/sample-datasets/hacker-news) straight into Postgres with parallel `COPY`, then builds the indexes. BM25 indexes are opt-in because they are large:

   ```bash
   npm run db:migrate           # extensions + tables + btree/trigram indexes
   npm run db:seed -- --bm25    # download, COPY, generated column, all indexes
   ```

   Useful seed flags: `--streams=8`, `--batch=20000`, `--limit=100000` (small sample), `--skip-download`, `--skip-unzip`.

3. **(Optional) Warm the cache** so the first queries are fast after a restart:

   ```bash
   npm run db:prewarm
   ```

4. **Run it.**

   ```bash
   npm run dev
   ```

### Scripts

| Command                          | Purpose                                                              |
| -------------------------------- | -------------------------------------------------------------------- |
| `npm run dev` / `build`          | Next.js dev server / production build                                |
| `npm run typecheck`              | `tsc --noEmit`                                                       |
| `npm run db:generate`            | Regenerate Drizzle migrations from `src/db/schema.ts`                |
| `npm run db:migrate`             | Apply extensions + `items` and `sync_state` tables                   |
| `npm run db:seed`                | Bulk-load the HN dump (add `--bm25` to build search indexes)         |
| `npm run db:backfill`            | Two-phase (fetch to disk, then load) backfill of the 2021-to-now gap |
| `npm run db:prewarm`             | `pg_prewarm` the table and every index                               |
| `npm run db:lexicon`             | Rebuild the `search_terms` typo lexicon from story titles            |
| `tsx scripts/inspect-indexes.ts` | Dump table columns, extensions, and index sizes                      |

## Staying live

The seed dump stops around late 2021 (item id ~28.7M) while Hacker News is past 49M. A Vercel cron ([`vercel.json`](vercel.json), hourly) pulls from the official [HN Firebase API](https://github.com/HackerNews/API) to keep the corpus current.

- **`GET /api/cron/sync`** ([`route`](src/app/api/cron/sync/route.ts), [`lib`](src/lib/hn-sync.ts)) fetches item ids concurrently, maps them to the `items` schema, and upserts them in parameterized multi-row batches. The generated `search_tsv` column re-indexes automatically, so new rows are searchable the moment they land.
- **`mode=latest`** (the default) refreshes the newest window ending at the current max item id, so today's stories and comments appear right away and their scores and comment counts stay fresh.
- **`mode=backfill`** walks a separate forward cursor from where the seed ended, closing the 2021-to-now gap a batch at a time. Point a second cron or a manual request at `/api/cron/sync?mode=backfill` to fill history slowly while staying live.

Each run is bounded by a wall-clock budget and persists its cursor to the `sync_state` table, so it stops cleanly at the function's time limit and the next run resumes. Tune per request with `?batch=`, `?concurrency=`, `?from=`.

For the full ~21M-row gap, run [`scripts/backfill.ts`](scripts/backfill.ts) (`npm run db:backfill`) instead. It is split into two phases so a crash never discards downloaded data:

```bash
# 1. Download the whole range to local gzipped, COPY-ready shards (resumable).
npm run db:backfill -- --phase=fetch

# 2a. Load keeping search online (staging + ON CONFLICT, every index maintained).
npm run db:backfill -- --phase=load --mode=online

# 2b. Or load fast in a maintenance window: drop all 12 secondary indexes,
#     bulk-load with only the primary key, then rebuild the indexes once.
npm run db:backfill -- --phase=load --mode=rebuild --workers=6
```
