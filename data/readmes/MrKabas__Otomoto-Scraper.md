# Otomoto Scraper

A scraper for **otomoto.pl** car listings. It collects make, model, year, mileage, price, the
full technical specification and — most importantly — the **equipment list** (air conditioning,
rain sensor, cruise control, ACC, parking sensors, camera, navigation, LED headlights, alloy
wheels, heated seats and ~50 more).

Listing descriptions are deliberately skipped: they are the largest part of the payload and
carry no structured data.

Data goes into **SQLite**, with export to **CSV / Parquet / JSON**.

---

## How it works

Otomoto exposes a public GraphQL endpoint at `https://www.otomoto.pl/graphql`. The scraper uses
two queries:

1. **Listing** — `advertSearch(criteria, page, sortBy)` returns 32 adverts per page
   (`id`, title, URL, creation date, price, location, seller type).
2. **Details** — `advertDetails(id: { type: HASH_ID, value: "<id>" })` returns **~150
   parameters** with Polish labels, including the complete equipment list. Up to **12 adverts
   per request** (GraphQL aliases).

Requests are throttled to **5 req/s** (configurable), with retries, backoff and DataDome
anti-bot handling.

> **Why 12 and not 20?** Otomoto's parser rejects any document with 13 or more `advertDetails`
> aliases (`GRAPHQL_PARSE_FAILED`). The limit applies to the alias count, not to the document
> size, so trimming the selection set does not help. The default batch is 10; `--batch` is
> clamped to 12.

---

## Installation

```bash
npm install
npm run init          # creates data/otomoto.db
```

Requires Node.js ≥ 20 (tested on 22.14) on Windows, Linux or macOS.

---

## Quick start

```bash
# 1. today's listings only (~2 900 ads, ~1.5 min)
npm run crawl -- today

# 2. database statistics
npm run stats

# 3. export cars with AC and a rain sensor under 50k PLN
npx tsx src/cli.ts export --format csv --where "has_ac = 1 AND has_rain_sensor = 1 AND price_pln < 50000"
```

> **npm caveat (npm 11):** npm parses *every* `--flag` on the command line as its own config,
> even after `--`. It expands `--format` to `--format-package-lock` and silently drops `--out`,
> `--since`, `--where` and friends, so `npm run export -- --format parquet` quietly writes a
> default CSV. Reliable options:
>
> - `npm run crawl -- today` — positional ranges work,
> - `npm run export:parquet` — the format is baked into the script,
> - `npx tsx src/cli.ts export --format parquet --out export/cars.parquet` — any flags,
> - `npm run export -- -- --format parquet` — the extra `--` stops npm from parsing.

---

## Date ranges

```bash
npm run list -- today          # today (from local midnight, Europe/Warsaw)
npm run list -- week           # this week (from Monday)
npm run list -- month          # this month (from the 1st)
npm run list -- 7d             # rolling 7 days
npm run list -- 30d            # rolling 30 days
npm run list -- 2026-10-15     # from a given day
npm run list -- last-run       # only ads newer than the previous run

npx tsx src/cli.ts list --from 2026-10-01 --to 2026-10-31   # explicit range
npx tsx src/cli.ts list --updated-since 2d                  # only ads changed recently
```

Both forms are equivalent: `npm run list -- today` and `npx tsx src/cli.ts list --since today`.

Ranges are computed in the **Europe/Warsaw** time zone and converted to UTC, because the API
only accepts full ISO-8601 timestamps (e.g. `2026-11-01T00:00:00Z`). Epoch numbers and other
formats are silently ignored by Otomoto.

`--since last-run` uses `crawl_state.list.max_created_at`, saved after every crawl, so a daily
run only downloads what is new.

---

## Commands

| Command | Description |
|---|---|
| `npm run init` | create the database and tables |
| `npm run list -- [range]` | fetch the listing (fast, no details) |
| `npm run details` | fetch parameters and equipment for `listed` ads |
| `npm run crawl -- [range]` | `list` + `details` in one run |
| `npm run update` | incremental: new ads since `last-run` + retry failures |
| `npm run recompute` | rebuild equipment flags from stored parameters (no network) |
| `npm run export:csv` / `:parquet` / `:json` | full dump in the chosen format |
| `npx tsx src/cli.ts export [options]` | CSV / Parquet / JSON with an SQL filter |
| `npm run stats` | data coverage, equipment statistics, top makes |

### `list` / `crawl` options

| Option | Default | Description |
|---|---|---|
| `[range]` / `--since <when>` | — | `today`, `week`, `month`, `7d`, `30d`, `YYYY-MM-DD`, `last-run` |
| `--from` / `--to` | — | explicit date range |
| `--updated-since <when>` | — | filter on the modification date instead of creation date |
| `--max-pages <n>` | all | page limit (for testing) |
| `--concurrency <n>` | 4 | parallel page requests |
| `--rps <n>` | 5 | requests per second |
| `--dry-run` | — | only count the adverts |

### `details` options

| Option | Default | Description |
|---|---|---|
| `--limit <n>` | all | advert limit |
| `--batch <n>` | 10 | adverts per GraphQL request (max 12) |
| `--concurrency <n>` | 4 | parallel requests |
| `--refresh` | — | re-fetch already enriched adverts |
| `--retry-errors` | — | retry failed adverts (max 3 attempts) and vanished ones (max 2) |

### `export`

```bash
# full dump with a ready-made script (default filename export/otomoto-YYYY-MM-DD.*)
npm run export:csv
npm run export:parquet
npm run export:json

# anything with flags - call the CLI directly
npx tsx src/cli.ts export --format csv     --out export/cars.csv
npx tsx src/cli.ts export --format parquet --out export/cars.parquet
npx tsx src/cli.ts export --format json    --out export/cars.json

npx tsx src/cli.ts export --format csv --where "make = 'BMW' AND year >= 2020 AND has_4wd = 1"
npx tsx src/cli.ts export --format csv --where "price_pln < 40000 AND mileage_km < 150000" --delimiter ";"
```

`--where` is raw SQL applied to the `v_ads` view (all `ads` columns plus every equipment flag).
CSV files are UTF-8 with a BOM so Excel opens Polish characters correctly.

Measured sizes on a fully enriched database (2 893 adverts, 103 columns):

| Format | Size | Per row |
|---|---|---|
| CSV | 1.8 MB | ~635 B |
| Parquet (snappy) | 0.37 MB | ~128 B |
| SQLite source | 47.6 MB | ~16.9 KB |

Extrapolated to the full catalogue (~235 000 adverts): **~150 MB CSV**, **~30 MB Parquet**,
**~4 GB SQLite**. Photos (`photos`, ~4.6M rows) and raw parameters (`ad_params`, ~15.7M rows)
are *not* part of `v_ads` and would add roughly 2 GB of CSV on their own.

---

## Data model

### `ads` — one advert (46 columns)

| Group | Columns |
|---|---|
| identity | `id`, `url`, `title`, `created_at`, `updated_at`, `first_seen`, `last_seen`, `status` |
| basics | `make`, `model`, `generation`, `year`, `mileage_km`, `price_pln`, `currency` |
| technical | `fuel_type`, `gearbox`, `transmission`, `engine_cc`, `engine_power_km` |
| body | `body_type`, `door_count`, `seats`, `color`, `color_type`, `country_origin` |
| condition | `new_used`, `damaged`, `registered_pl`, `first_owner`, `no_accident`, `service_aso`, `imported` |
| seller | `seller_type` (`firma` / `prywatny`), `seller_id`, `seller_name`, `city`, `region`, `district` |
| media | `photo_count` (the URLs live in `photos`) |
| bookkeeping | `state`, `attempts`, `last_error`, `enriched_at` |

`vin` and `first_registration` exist for completeness but are always `NULL`: the API returns
those values encrypted, so they cannot be decrypted.

### `ad_params` — every raw parameter (EAV)

`ad_id`, `key`, `label`, `type`, `value`, `value_label`. This holds **all ~150 parameters**
exactly as returned (227 distinct keys observed), with nothing lost. Keys are stable, e.g.
`rain_sensor`, `air_conditioning_type`, `price_amount`.

### `ad_features` — convenient 0/1 flags (57 columns)

51 boolean flags plus 5 descriptive text columns and `airbags_count`:

`has_ac`, `ac_type`, `has_rain_sensor`, `has_cruise`, `cruise_type`, `has_adaptive_cruise`,
`has_front_sensors`, `has_rear_sensors`, `has_camera`, `has_navi`, `has_bluetooth`, `has_usb`,
`has_touchscreen`, `has_wireless_charging`, `has_sound_system`, `has_leather`, `has_heated_seats`,
`has_heated_steering`, `has_sport_seats`, `has_multifunction_sw`, `has_alloy_wheels`,
`alloy_wheels_type`, `has_towbar`, `has_sunroof`, `has_tinted_windows`,
`has_heated_windshield`, `has_blind_spot`, `has_lane_assist`, `has_sign_recognition`,
`has_distance_control`, `has_adaptive_lights`, `headlights_type`, `has_led_lights`,
`has_led_daytime`, `has_fog_lights`, `has_cornering_lights`, `has_esp`, `has_abs`, `has_isofix`,
`airbags_count`, `has_start_stop`, `has_tire_pressure`, `has_electric_brake`, `has_hill_hold`,
`has_4wd`, `drive_type`, `has_keyless`, `has_electric_mirrors`, `has_folding_mirrors`,
`has_heated_mirrors`, `has_imported`, `has_vin`, `has_registration`, `has_service_record`,
`is_damaged`, `is_original_owner`, `is_no_accident`

> **Note:** Otomoto only returns a parameter when the seller ticked it, so `0` means "not
> declared in this advert", not "the car does not have it". Coverage varies from ~10% to ~100%
> depending on the feature.

Coverage measured on 2 838 enriched adverts: AC 68%, rain sensor 46%, cruise control 51%
(ACC 13%), rear sensors 44%, navigation 36%, leather 23%, heated seats 39%, alloy wheels 46%,
LED 23%, towbar 14%, 4x4 22%, sunroof 10%, ~3.3 airbags on average.

### Other tables

- `photos` — every photo (`ad_id`, `position`, `url`)
- `price_history` — price changes (one row per change)
- `dict_params` — `key → Polish label` dictionary, built automatically
- `crawl_runs`, `crawl_state` — run history and checkpoints
- the queue is `ads.state` itself (`listed` → `enriched` / `error` / `gone`)

### Advert states (`ads.state`)

| State | Meaning |
|---|---|
| `listed` | known from the listing, details not fetched yet |
| `enriched` | parameters, equipment and photos stored |
| `error` | 3 failed attempts (network/API) — `--retry-errors` retries |
| `gone` | the advert disappeared from the API between listing and details |

---

## Performance

Measured on a full day crawl (2 888 adverts, batch 10, 5 req/s): **1 min 21 s**
(23 s listing + 58 s details, 42 MB transferred, 47 MB database).

| Range | Adverts | Time (5 req/s) |
|---|---|---|
| today | ~2 900 | ~1.5 min |
| this week | ~34 700 | ~16 min |
| this month | ~143 000 | ~1 h |
| full catalogue | ~235 000 | ~1 h 50 min |

Transfer: ~14 KB per advert (details + photos) ≈ **3 GB** for the full catalogue.
Database: ~16 MB per 1 000 adverts ≈ **4 GB** for the full catalogue.

To go faster: `--batch 12` (the API maximum) cuts the request count by ~20%, and `--rps 10`
halves the crawl time (at a higher risk of hitting DataDome).

---

## Configuration (environment variables)

| Variable | Default | Description |
|---|---|---|
| `OTOMOTO_RPS` | `5` | requests per second |
| `OTOMOTO_BATCH` | `10` | adverts per GraphQL request (clamped to 12) |
| `OTOMOTO_CONCURRENCY` | `4` | parallel requests |
| `OTOMOTO_RETRIES` | `5` | retry attempts |
| `OTOMOTO_TIMEOUT` | `30000` | request timeout in ms |
| `OTOMOTO_DB` | `data/otomoto.db` | database path |
| `OTOMOTO_DEBUG` | — | `1` enables debug logs |

---

## Resilience

- **Rate limiting** — a global slot-based limiter in the client, never above `rps`.
- **Retries** — 429/5xx/network errors use exponential backoff with jitter.
- **DataDome** — challenge detection, automatic 15–120 s cooldown, User-Agent rotation and
  cookie persistence. After the retries are exhausted a clear error is raised.
- **Resuming** — state lives in `ads.state`; an interrupted crawl never duplicates rows
  (`ON CONFLICT(id)`).
- **Per-advert errors** — stored in `ads.last_error` with an attempt counter; `--retry-errors`
  retries them.
- **Vanished adverts** — when `advertDetails` answers with an empty object, the advert is
  marked `gone` instead of writing rows with a `NULL` id, so the data stays consistent.
- **Schema changes** — `recompute` rebuilds the equipment flags from stored parameters, so a
  mapping fix needs no re-download. Legacy columns (`raw_json`, `has_roof_rails`) are dropped
  automatically when the database is opened.

---

## Known limitations

- **12 adverts per request** — the GraphQL parser rejects 13+ aliases regardless of document
  size, so `--batch` is clamped to 12.
- **VIN, phone and registration number** are returned encrypted by the API and cannot be read
  (they are stored in `ad_params` as unreadable strings). `has_vin` therefore only means "the
  advert carries a VIN parameter" and is true for ~100% of adverts, which makes it a poor
  filter.
- **Descriptions** are not fetched (by design).
- **Equipment** comes from the seller's declaration — a missing entry does not mean the car
  lacks the feature.
- **The API is not public** and may change; all queries live in one file (`src/queries.ts`),
  so the schema is easy to update.

---

## Legal notes

The data is publicly available and `robots.txt` does not disallow `/osobowe` or `/oferta`.
The scraper runs at a moderate rate (5 req/s), does not bypass any protection and does not
publish sellers' contact details. Before commercial use, check Otomoto's terms of service and
your GDPR obligations (personal data of individuals).

---

## License

Released under the [MIT License](LICENSE). You are free to use, copy, modify, merge, publish,
distribute, sublicense and sell copies of this software, provided the copyright notice and the
license text are included. The software is provided "as is", without warranty of any kind.

Source files carry an `SPDX-License-Identifier: MIT` header so the license is detectable by
tooling such as `reuse`, GitHub's license scanner or license auditors.
