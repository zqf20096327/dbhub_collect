# one-quote-a-day

**One quote a day.** A white page with a single sentence about overcoming in
the middle. At midnight, in your own time zone, it changes.

**[quoteaday.vercel.app](https://quoteaday.vercel.app)** · **[Download the Android app](https://github.com/ferrnd/one-quote-a-day/releases/latest/download/one-quote-a-day.apk)** · source in [`android/`](android)

- 1,000 quotes, translated by hand into 10 languages
- the same quote for everyone on the same day, planned for the next 400 years
- two colours only: ink and paper, swapping at night
- no framework, no tracking, works offline

Underneath it is a deliberately over-engineered machine: a SQLite database
compiled by Python into a 10 MB file of hand-written **WebAssembly Text**, whose
runtime does the calendar math, the pseudo-random schedule and the string
storage. JavaScript only reads the clock and paints the text.

---

## Contents

- [Features](#features)
- [Languages](#languages)
- [How it works](#how-it-works)
- [The schedule](#the-schedule)
- [Building](#building)
- [Testing](#testing)
- [Android app](#android-app)
- [Deploying](#deploying)
- [Security](#security)
- [Project layout](#project-layout)
- [License](#license)

## Features

| | On the site | In the app |
| --- | --- | --- |
| Quote of the day | slides down at midnight | same, plus a daily notification at the hour you pick |
| Past days | <kbd>←</kbd> <kbd>→</kbd> or swipe | swipe |
| Archive | click **DAY N** to read every day so far, with a countdown to the next | tap **DAY N** |
| Copy | click the quote | tap the quote |
| Search | right-click the quote or the author | tap the author |
| Favorites | long-press (phone) or middle-click (computer) | long-press |
| Share | WhatsApp, Facebook, X, Telegram, Discord, Instagram, email, link, square image | Android share sheet, image or text, save to gallery |
| Night | white on black from 21:00 to 06:00, or always light or dark | same, and the launcher icon follows |
| Settings | theme, text size, animations, background lights, counter, copy format, search engine, language | the same, plus notifications |

Append `?date=YYYY-MM-DD` to preview another day, or `?theme=day|night` to force
a theme. Day 1 is 2026-11-16.

## Languages

English · Português (Brasil) · Español · Français · Italiano · Deutsch ·
Nederlands · 日本語 · 中文（简体） · 한국어

Every quote is translated by hand to carry its meaning rather than its words,
proverbs become their local equivalents, and every author's name is written the
way readers of that language know it (ウィンストン・チャーチル, 温斯顿·丘吉尔,
윈스턴 처칠). The interface follows the browser or phone language unless one is
picked in Settings. Japanese, Chinese and Korean are set in Noto Serif behind
Cormorant Garamond, upright, with their own line breaking.

Translations live in the database like everything else; see
[CONTRIBUTING.md](CONTRIBUTING.md) for how to add a language.

## How it works

```
 database/schema.sql ─┐
 database/seeds/*.sql ┴─► sqlite3 ─► catalog ─┬─► schedule (PCG32 + Fisher-Yates)
                                              │            │
 src/wat/*.wat ───────────────────────────────┴─► watgen ◄─┘
                                                     │
                                       generated/quotes.wat   (10 MB of WAT)
                                                     │  wabt
                                              docs/quotes.wasm (1.3 MB)
                                                     │
 web/ ──────────────────────────────────────► docs/  ─► Vercel
                                                     │
                     python -m tools.qotd android ──► android/app/src/main/assets/quotes.json
```

1. **`database/schema.sql`** is a normalised SQLite schema (themes, authors,
   quotes, locales, translations, dedications, calendar) with `STRICT` tables,
   `CHECK` constraints and intake views whose `INSTEAD OF` triggers let seeds
   insert readable rows and fail loudly on a typo.
2. **`database/seeds/*.sql`** hold the data, one commit per quote and per
   translation.
3. **`python -m tools.qotd wat`** compiles the database in memory, validates it
   (integrity, foreign keys, contiguous ids, complete translations), computes
   the schedule and writes `generated/quotes.wat`: the hand-written fragments in
   `src/wat/` plus data segments for every record, string and day.
4. **`node tools/assemble.mjs`** assembles it into `docs/quotes.wasm` with wabt.
5. **`python -m tools.qotd site`** stages `web/` into `docs/`, stamps
   cache-busting hashes and draws the Open Graph image with a pure-Python PNG
   rasteriser.
6. In the browser, `app.js` instantiates the module, asks it for the entry of
   the local date in the chosen language, decodes the UTF-8 straight out of
   linear memory and sleeps until the next local midnight.

The module's linear memory:

| Region      | Contents                                                              |
| ----------- | --------------------------------------------------------------------- |
| header      | 128 bytes: magic `QOTD`, format, counts, pointers, FNV-1a of the pool |
| records     | 16 bytes per quote per language: text and author pointer/length      |
| locales     | code and native name of each language                                 |
| pool        | every string, interned, UTF-8                                         |
| schedule    | one `u16` quote index per day for 146,097 days                        |
| dedications | `(day, record)` pairs pinned to a date                                |

The start function validates the header and recomputes the pool checksum, so a
corrupted module refuses to instantiate instead of showing garbage.

## The schedule

Time is cut into blocks of N days, N being the number of quotes. Each block
shows every quote exactly once, in an order given by a Fisher-Yates shuffle
driven by PCG32 seeded with the block number. If a block would open with the
quote that closed the previous one, its first two days swap, so no quote ever
appears two days in a row.

Adding quotes never rewrites days already planned: the `calendar` table records
the launch day and how many quotes existed then. Those keep their original
order, newer quotes follow in a shuffled run of their own, and only then does
the rotation include everything.

The table embedded in the module covers 2000-01-01 to 2399-12-31, exactly one
Gregorian cycle. Outside it the module recomputes the identical schedule on the
fly. Both paths are tested against each other, against the Python reference
and, in the Android app, against a Kotlin port. Every day in the generated WAT
is annotated, so the calendar can be audited with `grep`:

```sh
grep "2026-12-25" generated/quotes.wat
```

## Building

Requirements: Python 3.10+ (standard library only) and Node.js 20+.

```sh
npm ci            # installs wabt, the only dependency
npm run build     # database -> WAT -> wasm -> docs/
npm run serve     # http://localhost:8000
```

| Command | What it does |
| --- | --- |
| `npm run stats` | quotes per theme |
| `npm run today` | today's quote, from the Python reference |
| `npm run today -- 2027-01-01` | any other day |
| `npm run build:db` | writes `build/quotes.sqlite` for ad-hoc queries |
| `python -m tools.qotd android` | exports the catalog and golden schedule for the app |

## Testing

```sh
npm test
```

- **`tests/python`**: PCG32 reference vectors, calendar math against `datetime`
  over four centuries, schedule invariants, database constraints, every
  translation, the generated WAT and the Android export being up to date.
- **`tests/js`**: the shipped `quotes.wasm` itself: calendar math against
  `Date`, the embedded table against the live algorithm, no repeats in 400
  years, trap behaviour, a corrupted binary, every language, and midnight/DST
  handling in the clock.
- **`android/`**: the Kotlin schedule against the Python golden file, and the
  whole app driven under Robolectric with screenshots of every screen.

CI runs the full build, fails if the committed `generated/` or `docs/` differ
from a fresh build, then runs both suites.

## Android app

`android/` is a native app in Kotlin and Jetpack Compose, without a WebView. It
ships the same catalog as the site and computes the schedule itself. On top of
the site it has a daily notification (armed with `AlarmManager`, re-armed after
reboots and clock changes) and a launcher icon that turns black with white
quotes at night.

Requirements: JDK 17+ and the Android SDK (platform 35).

```sh
python -m tools.qotd android     # export quotes.json and the golden schedule
node android/tools/strings.mjs   # interface strings, generated from web/i18n.js
cd android && ./gradlew test assembleDebug
```

The APK lands in `android/app/build/outputs/apk/debug/`; screenshots from the
tests in `android/app/build/screens/`. Icons are drawn by
`python android/tools/icons.py`.

## Deploying

The site is static: `vercel.json` serves `docs/` with no build step.

```sh
vercel deploy --prod
```

## Security

There is no server code, database or login online, only static files on
Vercel's CDN, which also absorbs denial-of-service traffic. Every response
carries a strict Content-Security-Policy (only this origin's scripts and Google
Fonts), `X-Frame-Options: DENY`, HSTS, a Permissions-Policy that turns off
camera, microphone, location and the rest, and cross-origin isolation headers.

## Project layout

```
database/        schema and seeds, the source of truth
src/wat/         the hand-written WebAssembly Text runtime
tools/qotd/      the Python build pipeline
tools/           the wabt assembler script
web/             page, styles, clock, translations, service worker
generated/       the generated WAT module (committed)
docs/            the deployable site (committed)
android/         the native Android app
tests/           Python and Node test suites
```

## License

Code is MIT licensed. The quotes are short excerpts, each attributed to its
author. Cormorant Garamond and Cinzel are under the SIL Open Font License.
