# commerce-simulator

Realistic, continuously changing commerce data for a fictional consumer goods brand, spread
across several source systems in plain Postgres.

Use it to test and evaluate analytics, BI and AI platforms against data that behaves like a
real business: sell-in and sell-out, imperfect keys between systems, documents that change
state, seasonality, promotions and planted business stories with ground truth.

Improvements are welcome: open an issue or a pull request.

The simulated company is **Northvale Consumer Care GmbH**, a German skincare manufacturer with
three brands (Velmora, Cutara, Sorell) selling in Germany, Austria and Switzerland through its
own web shop, two drugstore chains, a perfumery chain and a marketplace. Everything is fictional. All parameters are synthetic
defaults, not market data.

> Status: **phase 2** (retail reality). The web shop, warehouse, SAP-style ERP (with trade
> deductions), marketing stack and retailer and marketplace feeds are generated for all five
> channels, with five planted scenarios and data quality noise recorded in `truth`. The digital
> shelf, a readable English ERP naming profile and platform guides follow in phase 3. See
> [docs/SPEC.md](docs/SPEC.md).

## Quick start (Docker)

```bash
cp .env.example .env        # fill in the three passwords (>= 16 chars, all different; openssl rand -base64 24)
docker compose up -d
docker compose logs -f generator
```

On first start the generator creates the schemas and backfills 24 months of history. With the
default volume this takes about 18 minutes with the stack limited to 2 vCPU and 2 GB RAM (an
estimate: phase 1 measured 13 minutes there, and the phase-2 backfill takes about 1.4 times as
long on the same development machine, 13.4 against 9.5 minutes); slower disks take longer. On a
2 vCPU / 2 GB cloud VM (AWS t4g.small, gp3 disk, 2 GB swap) the v0.2.0 backfill measured about
46 minutes, with at least 635 MB of memory available throughout and no OOM kill. It then keeps
running live, with the simulation clock equal to wall time. Only Postgres is published
(port 5432, SSL required for remote connections).

Connect your BI tool as `bi_reader` (password `CPGSIM_READER_PASSWORD`) to database `cpgsim`.
That role can read the business schemas and nothing else.

## What is in the database

| Schema | Stands in for | Conventions |
| --- | --- | --- |
| `shop` | Web shop platform: customers, addresses, orders, order lines, payments, refunds, promotions, subscriptions | UUID keys, `timestamptz` in UTC, statuses as words |
| `wms` | Warehouse and shipping: shipments, carrier events, returns, daily stock levels, stock movements | Integer keys, two-letter status codes, local Berlin time without time zone |
| `erp` | SAP-style ERP: `mara`, `makt`, `mbew`, `kna1`, `knmt`, `tcurr`, `vbak`/`vbap`, `konv`, `likp`/`lips`, `vbrk`/`vbrp`, trade promotion agreements `kona`/`zkona_item`, deductions `zdeduct`/`zdeduct_item`/`zdeduct_clr` | Ten-digit document numbers, SAP field names, amounts in document currency plus EUR |
| `mkt` | Marketing stack: campaigns, daily spend, web sessions, last-click attributions, influencer codes (15 % off a customer's first web order, never combined with another promotion) | Text keys, dates; daily facts exported once a day after the day closes |
| `feeds` | Retailer sell-out (weekly; the perfumery per retail month), marketplace daily sales, traffic and inventory, feed loads | Flat file-like rows in each sender's own codes and layout, a load id per delivery, insert-only (restatements are new loads) |
| `shelf` | Digital shelf | Arrives in phase 3 |
| `sim`, `truth` | Simulator state and ground truth for planted scenarios | Never granted to `bi_reader` |

The systems do not share keys. The shop order UUID reaches the ERP only as a reference on the
sales document (`vbak.bstnk`, about 1 % missing or truncated). The warehouse references the ERP
delivery number, never the shop order. Web customers appear in the ERP as one collective account
per country. Retailers and the marketplace report their own article numbers, mapped through
`erp.knmt` (about 95 % complete). For the missing 5 % the EDI order lines (`vbap.kdmat` next to
`matnr`) and the brand's promotion agreements still show the article, so the mapping can be
recovered from the order history; feeds and deduction claim items carry the article only. Joining
the systems is part of what a platform is tested on.

At the default 315 web orders a day, a 24-month backfill writes about 10.9 million rows (3.6 GB
including indexes, plus up to 2 GB of Postgres WAL). Live mode adds about 13,800 to 15,300 rows a
day, about 1.6 GB a year.

## Loading it into a BI tool

Every business table follows one contract, so a standard query-based incremental load works
without custom logic:

- every table has a primary key;
- `created_at` and `updated_at` (`timestamptz`) are set from the simulation clock, and
  `updated_at` moves on every change and is indexed;
- nothing is ever deleted: cancellations are states, withdrawn rows carry `is_deleted` and
  `deleted_at`;
- daily snapshot tables (`wms.stock_levels_daily`) and the four `feeds` tables are insert-only:
  load them in full or append by `load_id` (a restated sell-out period is a new load).

Load incrementally with `WHERE updated_at > :last_watermark` on a 5 to 15 minute schedule.
A change committed by the generator is visible at the end of its 30-second tick.

Use the **largest `updated_at` already loaded** (per table) as the watermark. In live mode,
including the catch-up after the generator was down, `created_at` and `updated_at` carry the
time of the commit that wrote the row (business columns such as `placed_at` keep the simulated
event time), so that watermark never misses a row. If your tool can only use the time its last
load started, subtract an overlap of a minute and upsert on the primary key. The history
written by the initial backfill is stamped with simulated event times.

## Planted scenarios

Scenarios are time-bounded business stories that a platform should be able to surface by
joining sources. Each one records exactly what it did in the `truth` schema.

| Scenario | Story |
| --- | --- |
| `carrier_decay` | Swiftbox deliveries in Bavaria get 2.5 times slower and fail three times as often from a set week |
| `promo_margin_trap` | 25 % off plus free shipping on Velmora grows orders but loses money once shipping and returns are costed |
| `hero_oos_substitution` | A quality block takes a hero SKU out of stock for three weeks; a sibling absorbs 40 % of its demand, retailers' sell-out dips |
| `influencer_cohort_churn` | A boosted influencer campaign buys customers who rarely order again (CAC versus lifetime value) |
| `retailer_overstock` | Mylo orders 30 % above its sell-out for a quarter, then cuts orders and claims clearance deductions |

Data quality noise (duplicate customers, malformed postcodes, statuses set in error, duplicate
carrier scans, DST local times, missing order references, unmapped articles, sell-out
restatements, free-text return reasons, GDPR erasures) is planted at low configurable rates and
recorded in `truth` the same way (`sim truth <defect>`).

Switch a scenario on live, for example during a demo, and it shows up in the BI tool after the
next incremental load:

```bash
docker compose exec generator sim scenario enable promo_margin_trap
docker compose exec generator sim truth promo_margin_trap
```

## Command line

| Command | What it does |
| --- | --- |
| `sim init` | Creates schemas, tables, indexes and grants |
| `sim reset --seed N` | Drops all simulated data and the clock, keeps the structure (refuses while a generator is running; `--force` stops it) |
| `sim backfill --months 24` | Runs backfill mode up to now (`--start`, `--until` for fixed windows) |
| `sim run` | Runs live mode until stopped; catches up first if behind |
| `sim start` | Container entrypoint: init, backfill if new, then run |
| `sim status` | Clock, queue depth, rows written in the last hour, active scenarios, config changes |
| `sim scenario list / enable <id> / disable <id>` | Lists scenarios or switches one on or off from now |
| `sim truth <scenario or defect id>` | Prints what a scenario or data quality defect planted |

## Configuration

One YAML file, [config/default.yaml](config/default.yaml), describes the business and is
validated at start-up. Pass a private overlay with `--overlay /path/to/private.yaml` (or
`CPGSIM_OVERLAY` in `.env`). It is deep-merged on top, and it is where prospect-specific settings
and scenarios belong. Keep overlays outside this repository.

The same seed, config and history start produce the same business, whatever the tick length,
batching or restarts. A demo can therefore be reset and replayed exactly:

```bash
docker compose stop generator
docker compose run --rm generator reset --yes      # add --seed N for another business
docker compose up -d generator                     # backfills again, then runs live
```

Only one generator may write to a database; a second one (or `sim backfill` next to a running
container) refuses to start. Changing the business config of a running simulation is logged and
recorded (`sim status`); tick and backfill settings may change freely.

## Running without Docker

Requires Python 3.12 and a Postgres 14+ database.

```bash
python3.12 -m venv .venv && .venv/bin/pip install -e '.[dev]'
export CPGSIM_DSN=postgresql://sim_writer:...@localhost:5432/cpgsim
.venv/bin/sim init
.venv/bin/sim backfill --months 24
.venv/bin/sim run
```

An administrator creates the roles first with [sql/roles.sql](sql/roles.sql). Tests run with
`.venv/bin/pytest`. Database tests need `CPGSIM_TEST_DSN` pointing at a scratch database.

## Compatibility

Anything with a Postgres connector and query-based incremental loads, for example Incorta,
Microsoft Fabric or Databricks. Platform-specific notes live under `examples/`: [Incorta](examples/incorta/README.md) (load plans, queries and [joins](examples/incorta/joins.md)).

## Documentation

- [docs/SPEC.md](docs/SPEC.md): what the simulator generates and why
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md): engine, module contracts and per-system conventions

## Licence

Apache-2.0, see [LICENSE](LICENSE).

## About

Maintained by the Data & AI team at [Runibex](https://runibex.com). We have spent years
building commerce platforms for large B2C, B2B and B2B2C businesses, and this simulator
distils what that work taught us about how commerce data actually behaves across systems.
We use it in our own work and share it in case it is useful in yours. If you would like to
collaborate, get in touch.
