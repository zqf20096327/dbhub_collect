# THE ASCENT

[![CI](https://github.com/AliMoharramy/ascent-study/actions/workflows/ci.yml/badge.svg)](https://github.com/AliMoharramy/ascent-study/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
![Node 22](https://img.shields.io/badge/node-22-339933)
![PostgreSQL 17](https://img.shields.io/badge/PostgreSQL-17-336791)

<p align="center">
  <img src="docs/images/hero.webp" alt="The Today screen of THE ASCENT in its dark and cream themes: a focus timer, three quest tiers, a coach card and a countdown to the exam" width="900">
</p>

**A self-hosted, gamified study + habit engine.** One mission, the nearest boss, nothing else on the screen: it turns a
months-long exam campaign into a climb — quests, XP, rivals, bosses, loot, rest and review — while an event-sourced
ledger keeps every number honest and replayable.

It was built by one person for **one national entrance exam**, and ships with a single sample exam configuration (exam
date, subjects, chapters, week grid) that you replace with your own. The UI is **Persian (RTL)** with Jalali dates and
English headings. The app works fully **without any AI key**; remote AI is an optional, guarded, cost-capped extra.

> **Status:** used by its author for their own exam preparation; maintained on a best-effort basis. It is a *reference implementation*
> you can run as-is for the same exam, or fork and adapt. Making the exam fully configurable (dates, subjects,
> week grid) is the main open roadmap item — see [Adapting it to another exam](#adapting-it-to-another-exam).

## Highlights

- **Transactional by design:** one PostgreSQL database, per-user advisory locks, idempotent retries, atomic first-run
  setup — no lost updates under concurrent requests (see [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)).
- **Honest numbers:** every mutation is an event; XP / score / gold ledgers are projections you can rebuild and diff
  (`npm run replay`).
- **Safe to run for months:** verified, encrypted backups, an atomic restore and a restore drill.
- **Deploy anywhere:** Vercel + Neon (free tiers work), or Docker Compose on your own server.
- **Calm by default:** no guilt, no streak-shaming; penalties start only after you confirm your baseline week.
- **Native Windows focus widget:** a lightweight Rust + Slint companion with server-synced focus sessions, task titles, and opt-in AI suggestions. See [`desktop/windows-widget/README.md`](desktop/windows-widget/README.md) for setup and packaging.
- **~400 automated tests** (unit, PostgreSQL integration/concurrency) plus a page-level smoke test in CI.

## A look around

Everything below runs on the built-in **demo data** (three weeks of sample study history — see
[Try it with demo data](#try-it-with-demo-data)), so you can see the numbers move without entering a thing.

| | |
|---|---|
| ![Today: focus timer, quests, coach](docs/images/today-night.webp)<br>**Today** — one mission, the nearest boss, a timer. | ![World map with realms and cleared chapters](docs/images/map-night.webp)<br>**Map** — every chapter is a node; two spaced, solid tests clear it. |
| ![Habit Lab with streak grids](docs/images/habits-night.webp)<br>**Habit Lab** — tiny / standard / stretch tiers, a calm streak grid, identity votes. | ![Forge: error notebook with causes](docs/images/forge-night.webp)<br>**Forge** — turn every mistake into a one-line lesson and a review. |
| ![Plan: 25-week load calendar](docs/images/plan-night.webp)<br>**Plan** — capacity-aware weeks, triage and a burn-gap check. | ![Character sheet with attributes and achievements](docs/images/character-night.webp)<br>**Character** — XP, attributes and achievements. Numbers you can replay and audit. |

<details>
<summary>The same screens in the cream (light) theme, plus Arena and Review</summary>

| | |
|---|---|
| ![Today, cream theme](docs/images/today-cream.webp) | ![Map, cream theme](docs/images/map-cream.webp) |
| ![Arena: rival, duels and bosses](docs/images/arena-night.webp) | ![Weekly and nightly reviews](docs/images/review-night.webp) |

</details>

> The interface is Persian (RTL) with Jalali dates; screenshots are taken with the English headings you see in the app.

## Try it with demo data

No account, no typing — one command gives you a separate database with three weeks of realistic sample history
(focus blocks, tests, a few Chapter Clears, habit streaks, error notes, reviews), generated through the same services
the UI uses:

```bash
make demo         # Node 22 + Docker; then sign in as  demo / demo-password-123  at http://localhost:3100
```

Without `make`: `npm run db:migrate && npm run demo:seed` against an **empty local** database (the script refuses to
touch a non-local one, or one that already has an account). To regenerate the screenshots above after a UI change, run
the app against that database and `npm run screenshots -- --base http://localhost:3000`.

## Quick start

```bash
git clone https://github.com/AliMoharramy/ascent-study.git
cd ascent-study
make dev          # needs Node 22 + Docker; PostgreSQL, migrations, seed and a dev user are created for you
# open http://localhost:3100  (login: see `make login`)
```

**Deploy your own:** [![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FAliMoharramy%2Fascent-study&project-name=ascent-study&repository-name=ascent-study&env=DATABASE_URL,SETUP_TOKEN,CRON_SECRET,OFFSITE_KEY&envDescription=Pooled%20PostgreSQL%20URL%2C%20and%20three%20random%20secrets%20(see%20the%20launch%20guide)&envLink=https%3A%2F%2Fgithub.com%2FAliMoharramy%2Fascent-study%2Fblob%2Fmain%2Fdocs%2Flaunch-guide.md) — you still need a PostgreSQL database (Neon's free plan works) and to run `npm run db:migrate` once; follow [`docs/launch-guide.md`](docs/launch-guide.md).

Details: [Quick start](#quick-start-1), [Deployment](#deployment) (Vercel + Neon, step by step: [`docs/launch-guide.md`](docs/launch-guide.md)),
and a Persian end-user guide: [`docs/user-guide-fa.md`](docs/user-guide-fa.md).

> **Before you expose it to the internet:** set `SETUP_TOKEN`, `CRON_SECRET` and `OFFSITE_KEY` (see
> [Configuration](#configuration--secrets)). The first visitor of a fresh server can otherwise create the one account.

## Adapting it to another exam

Today the exam is encoded in a few places — `src/lib/campaign.ts` (`EXAM_DATE`, `PROJECT_START`, `WEEK1_START`,
`TOTAL_WEEKS`), the reference data in `docs/seed/` (subjects, chapters, coefficients, mock exams) and the Persian
copy. To adapt it today: change those constants, replace the seed YAML files (`npm run seed:validate` checks them), and
re-run `npm run db:seed`. Turning this into configuration (env/DB instead of constants, seed "packs", i18n) is the
biggest piece of planned work and a great place to contribute — see [CONTRIBUTING.md](CONTRIBUTING.md).

## Project links

- Contributing: [`CONTRIBUTING.md`](CONTRIBUTING.md) · [Code of Conduct](CODE_OF_CONDUCT.md) · [Security policy](SECURITY.md) · [Changelog](CHANGELOG.md) · [Windows widget](desktop/windows-widget/README.md)
- Architecture (English): [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) · design docs (Persian): [`docs/README.md`](docs/README.md) · decisions: [`docs/adr.md`](docs/adr.md)
- Operations & recovery: [`docs/runbook.md`](docs/runbook.md) · deployment: [`docs/deploy.md`](docs/deploy.md)
- Licenses & third-party content: [`LICENSE`](LICENSE) (MIT, code) · [`NOTICE`](NOTICE) · [`public/art/LICENSE.md`](public/art/LICENSE.md) (artwork, CC BY 4.0)

---

## Contents

1. [Status & roadmap](#status--roadmap) (full list: [`ROADMAP.md`](ROADMAP.md))
2. [Feature tour](#feature-tour)
3. [Core game concepts](#core-game-concepts)
4. [Quick start (detailed)](#quick-start-1)
5. [Makefile reference](#makefile-reference)
6. [npm scripts reference](#npm-scripts-reference)
7. [Configuration & secrets](#configuration--secrets)
8. [Data model & integrity](#data-model--integrity)
9. [Scheduled jobs](#scheduled-jobs)
10. [Backup, restore & recovery](#backup-restore--recovery)
11. [Testing & CI](#testing--ci)
12. [Project structure](#project-structure)
13. [Art & design system](#art--design-system)
14. [Deployment](#deployment)
15. [Troubleshooting](#troubleshooting)
16. [Documentation map](#documentation-map)
17. [Conventions](#conventions)

---

## Status & roadmap

**R0–R5 are complete** (tracked as issues #1–#115 in the original private tracker; those numbers appear throughout the docs and ADRs).

| Release | Scope | State |
|---|---|---|
| R0 | Substrate: event store, projections/replay, migrations, seeds, auth, config | ✅ done |
| R1 | Core loop: Today, quests, capacity/triage/planner, rollover, onboarding, focus mode | ✅ done |
| R2 | Campaign: world map, rival & duels, bosses, arena, forge, plan, council, shop, codex + tools/ops (#61–#74) | ✅ done |
| R3 | Life pillars: habits, bonds, builder hour, loot, story, review rounds, ghost league, streaks (#75–#91) | ✅ done |
| R4 | Intelligence & wellness: guarded AI adapter, insights, predictions, wrapped, what-if, error mining, burnout radar, Archie coach, ICS/Anki export, exam-day playbook, Experiment Lab (#92–#105) | ✅ done |
| R5 | Final ascent: animations/sound/calm mode, offline sync, second-theme polish + a11y AA + visual regression, Web Push/Telegram, perf & security pass, final-week kit, cheat-sheet PDF, share card + monthly PDF, freeze docs (#106–#115) | ✅ done |

**Open backlog (#116–#124)** — optional future work, not blockers: IDEA epics (browser extension for detour capture,
voice/local-AI coach, companion pet, mobile widgets, chapter cinematics, post-exam prestige),
display-only Focus Energy (#122), real candidate course-session data (#123), and server deployment (#124).

Deployment is **prepared for local, Docker, and Vercel + managed PostgreSQL (Database V2)**, but has not been deployed; see [Deployment](#deployment).
Every Function and tool reads and writes one transactional PostgreSQL database; Blob holds only encrypted backups. **Build Freeze** starts 7 Esfand 1405 (2027-02-26, ADR-0020): after it, only study
features and bug fixes ship — no new mechanics before the exam.

## Feature tour

### R1 — Core loop
Event store with projection/replay · three-tier missions (Core from Planner, Fixed, Pillars, Comeback, Shield, Life
Event) · nightly rollover · capacity / triage / planner · Today v1 (bento) · Surge / Idle / manual entry / Undo ·
error analysis · Idea Vault + Detour friction · Habit Lab · nightly review · Baseline Report · XP pop / level-up ·
daily goal · onboarding · layered nav bar · feature flags · shortcuts + Focus mode.

### R2 — Campaign
World map with Clear rule · Shadow Rival + duels · bosses · Arena (mock-exam banks; dropped linear-algebra counts as
an *intentional skip*, not a weakness) · Forge (errors, spaced-repetition cards, artifacts) · Weekly Council · Plan UI
(calendar, load ratio, burn gap, rebalance, reset week) · sleep & body program · Gold / shop / achievements · Codex +
Decision Log. Tools & ops (#61–#74): config editor with rollback/import/export · exam simulator with exact negative
marking and suspect flags · territory fog · combo meter · command palette (⌘K) · 5-minute review deck · escape-pattern
report + anti-goal · exam weight map · encrypted offsite backup + replay CLI · Hall of Fame.

### R3 — Life pillars (#75–#91)
Habit lifecycle + contracts + 12-week heatmap + identity votes · exploration slot (≤10% cap) · light bonds + weekly
mission + night book · Builder Hour with 6-hour bank · loot + pity + trait radar · editable story chapters + rival
events · TOC review rounds ×3 + monthly review + Spark Log · detour ledger · 10-runner Ghost League · quest board +
monthly challenge · Streak Society (7/30/60/100) + checkpoint/legendary nodes.
Extras (#86–#91): vertical Path view synced with the map · skill tree + gem avatar · sleep debt + mood/energy check-in
+ wind-down · five mastery levels + pretest + interleaving + rounds 2/3 · encrypted time capsule sealed until exam day
(Summit badge) · final-week Boss Rush + free season pass + weekly challenge card.

### R4 — Intelligence & wellness (#92–#105)
AI adapter with an aggregates-only privacy guard and monthly cost / daily call caps (full functionality without AI) ·
weekly review + structured error analysis · narrative + gentle anomaly warnings · net-% prediction with confidence
interval + energy peak + weakness hunter · sleep CSV import with preview + habit shaping + prereq warnings · anchor
reminders (≤5/day, no blame) · six-slide Weekly Wrapped · what-if + rank estimate with an explicitly hypothetical curve
(T-DATA-04) · error mining + per-question timing + skip trainer with expected-value scoring · burnout radar + buddy
report · Archie coach chat + plan negotiator · ICS / Anki export · exam-day playbook + pre-exam sleep · Experiment Lab.

### R5 — Final ascent (#106–#115)
Animations, sound and **calm mode** (a single flag strips confetti/springs/sounds/mascot art to simple fades) ·
**offline mode** with an IndexedDB outbox + sync queue (six mutation types, ADR-0015) · second-theme (Cream) polish,
**WCAG 2.1 AA** contrast across both themes, and **pixelmatch visual regression** · opt-in **Web Push + Telegram**
anchor reminders · **performance & security pass** (≤200 KB gzip initial JS, TTFB budget, CSRF/lockout/headers) ·
**Final Ascent** exam-week kit (auto ≤7 days out): review-only last-7-days plan, printable playbook, pre-exam sleep,
anxiety toolkit (box breathing, grounding — no XP) · **cheat-sheet builder** (print A4 from Forge artifacts) ·
shareable result card + monthly PDF report · final docs/runbook + Build Freeze announcement.

### Pages & shortcuts

Primary navigation (mobile bottom bar): **Today · Map · Arena · Forge · Sheets**. Everything else lives under **More**
(and on the desktop vertical rail).

| Route | Page |
|---|---|
| `/today` | Daily cockpit: focus timer, Core/Fixed/Pillar/Comeback quests, test log (live net %), quest board, loot chest, 4-layer progress, safety net, nightly check-in |
| `/map` · `/map/[id]` | World map (4 realms / 8 subjects, fog, exam hot spots) + vertical Path · node detail (Clear progress, history, errors, lessons) |
| `/arena` · `/arena/exam` | Shadow Rival MP gap, weekly duel, bosses, mock-exam banks, challenge card, Boss Rush · timed exam simulator (−⅓ marking) |
| `/forge` | Errors · spaced-repetition Review · Artifacts (Markdown cheat-sheets) · Coach |
| `/sheets` | Print A4 per-subject cheat-sheets built from your own Forge artifacts |
| `/plan` | 25-week capacity, scenarios, triage, drag calendar, rebalance, Rest Day Pass, `.ics` export, forecast / what-if / rank |
| `/coach` | Archie local chat + plan negotiation ("nothing moves until you approve"); remote AI is enabled for the fresh profile once provider settings are supplied |
| `/habits` | Habit Lab: anchors, 12-week heatmap, lifecycle, scorecard, identity votes |
| `/life` | Exploration · Bonds · Builder Hour · Ghost League · Story · Escapes · Monthly |
| `/review` | Nightly · Weekly Council · review rounds · Monthly · Experiment Lab · AI Coach · Wrapped |
| `/rest` | Sleep program (wake −20 min/week → 05:30), Mi Band CSV import, wind-down, sleep debt, burnout radar, buddy report |
| `/final` | Exam-week kit: review-only last-7-days plan, printable playbook, pre-exam sleep, anxiety toolkit |
| `/ideas` | Idea Vault (park ≤30 s) + Detour Ledger ("study first" friction) + Builder Hour |
| `/character` | "Me": level/title/XP, attribute radar, Gold/SS, achievements, Hall of Fame, streak medals, loot pity, Reward Shop, Gems + Skill Tree, avatar, Season Pass, Time Capsule |
| `/courses` · `/courses/[id]` | Video library (lesson import, speed, progress, test sources, mastery + interleaving) · course detail |
| `/codex` | In-app docs reader, Persian full-text search, Decision Log |
| `/settings` | Theme, backups, Day-0 CSV import, feature flags, daily goal, money budget, Replay, reminders, Push/Telegram, versioned config editor |
| `/deck` · `/run` · `/baseline` | 5-minute review deck (Anki export) · mini-run result · Baseline Week report |
| `/report/monthly` · `/playground` | Printable A4 monthly report · UI component playground (dev) |
| `/focus` · `/offline` · `/onboarding` · `/login` | Fullscreen focus clock · offline outbox/sync · 4-step setup (≤2 min) · auth (5 wrong attempts → 15-min lock) |

Shortcuts: `?` help · `S` surge (×1.2, 90 min) · `Space` timer · `T` log test · `N` idea · `F` focus mode · `U` undo
(10 min) · `G`+letter navigation · `Ctrl/Cmd+K` command palette.

---

## Core game concepts

The loop: **Plan → Today** (quests + focus + tests) **→ Forge** (errors / review / artifacts) **→ Arena** (rival /
bosses / mocks) **→ Review → Rest**. The screen always shows one mission and the nearest boss — never a wall of stats.

### Currencies

| Currency | Behaviour | Earned from | Used for |
|---|---|---|---|
| **XP** | Never decreases; drives Level | study + pillars (rates/caps below) | level & title |
| **SS** (Season Score) | Can go negative; daily floor −40, weekly −120 (Reset Week −50) | weekly study XP + boss net % − miss penalties | league standing |
| **Gold** | Spendable | Standard day 10, Stretch +5, weekly boss 50, duel 100, region boss 150, daily goal +10, surplus non-study XP 1:1 | Reward Shop |
| **Gems** | Skill-tree currency | chapter clear 2, boss win 5, duel win 2, streak milestone 10, perfect run 3 | Skill Tree (tiers 10 / 25 / 60) |
| **MP** (Mastery Points) | Shadow Rival gap | tier-weighted chapter mastery | racing the Shadow |

### XP rates (per day, after caps)

| Activity | XP | Daily cap |
|---|---|---|
| Focus | 1 per 5-min block (Surge ×1.2 up to 90 min; manual entry after 24 h ×0.5) | 72 |
| Video lesson | 5 | 40 |
| Tests | 0.6 / correct + 0.1 / wrong (interleaved ×1.1) | 80 |
| Error analysed | 1.0 | 40 |
| Review card | 2 | 30 |
| Forge artifact | 8 | 24 |
| Chapter Clear | 60 × tier (M 1 / S 0.7 / C 0.4) | — |
| Pillar quest | 10 (sleep on time 15) | 35 |
| Mini-trial / Weekly boss / Mock exam | 20 + 2×net % / 80 + 2×net % / 60 + 3×net % (+100 for beating the Shadow) | — |

Non-study XP (Forge, Pillars) may be at most **30%** of the week's level-counting XP; the surplus converts to Gold 1:1.
A **Seed** quest is 25% of Standard XP; **Stretch** is ×1.25. Every award carries a `ruleKey` + reason so the UI can
always answer "why?".

### Levels & titles

Total XP to reach level *L* = `120·L + 6·L·(L+1)`; the next level costs `120 + 12·(L+1)` (ADR-0004). Titles:
Wanderer → Initiate (6) → Scholar (11) → Adept (16) → Strategist (21) → Warden (26) → Champion (31) → Ascendant (36) →
Summit-Bound (41).

### Quests & the safety net

At most **5 active quests/day** ("three, never five"): **Core** (from the Planner; Seed/Standard/Stretch), **Fixed**
(daily anchors), **Pillars** (habits/life), **Comeback** (after a miss). Misses cost SS — Core −20, Fixed −6, Pillar −4,
skipped weekly boss −40 — floored per day/week. A **Shield** (1 per 5 Standard-day streak, max 3, use within 24 h) or a
**Life Event** (≤2/week) forgives the day's penalties; the Comeback quest refunds 50% of a missed day's penalty.
**Undo** reverses a focus/test log within 10 minutes. Streak medals never reset (≥80% over 30 days keeps the streak).

### Clear rule (chapter mastery)

A map node is **Cleared** only after **≥2 sessions, ≥2 days apart, ≥5 questions, ≥60% net** — watching video alone never
clears a chapter. Tiers **M/S/C** weight exam importance (3/2/1 in triage).

### Shadow Rival, bosses & loot

The **Shadow Rival** paces at 0.85–1.10× your plan (+5%/week); the Arena shows the MP gap and a "Why?" breakdown, and
rests shrink the gap if you fall ≥20% behind for 2 weeks. **Bosses**: Weekly (Friday, 25 q / 60 min, threshold 40→55%
by level), Mini-Trial (biweekly, 25 q / 60 min), Region (40 q / 100 min @ 45%). **Loot**: 60% nothing / 25% codex /
10% cosmetic / 5% shield, with a guaranteed drop after 7 dry chests (pity).

### Plan: capacity & triage

25-week capacity under cautious/base/optimistic scenarios (0.55 / 0.65 / 0.8 focus factor, 10% reserve, 45 fixed
min/day). **Triage** ranks chapters by exam weight (M/S/C = 3/2/1) × headroom (1 − baseline accuracy `a0`) ÷ estimated
hours, then selects enough to cover **≥70% of must-have** and **≥90% of should-have** weighted marks; it re-runs every
14 days. The Planner turns that into ≤5 daily quests, and the Coach negotiates changes — nothing moves without approval.

### Honesty & anti-gaming

Every mutation is an **event**; XP/SS/Gold/Gems are *projections* rebuilt by `npm run replay` (the anti-gaming backbone).
Anomaly guards flag impossible days (>200 tests, >14 focus hours, perfect accuracy on <50 tests, >40% manual entries).
Assumed exam data is always flagged, never silently official; rank estimates use an explicitly hypothetical curve
(T-DATA-04). Rest and wellness are a **mirror, never a penalty**.

---

## Quick start

### Prerequisites

- **Node.js 22** (CI is pinned to 22).
- npm 10+ · GNU Make 4+ (optional but recommended; on Windows use the MSYS2/Git-Bash `make`).
- **Docker** — local development and tests use a disposable PostgreSQL 17 container (`docker compose`).

### Option A — `make dev` (recommended)

```bash
make dev
```

One command does everything, against an **isolated local PostgreSQL** container (`ascent_dev`, bound to 127.0.0.1) —
never a production database:

1. `npm ci` if dependencies are missing,
2. start PostgreSQL (`docker compose up -d --wait postgres`),
3. apply all pending migrations (`npm run db:migrate`, direct connection, advisory-locked),
4. import the reference seed (idempotent),
5. create the test user if absent (idempotent),
6. start Next.js on **http://localhost:3100**.

**Test login:** username `test` · password `test-password-123` (print anytime with `make login`).
A fresh dev DB lands on onboarding after sign-in.

Overrides: `make dev PORT=3000 PG_PORT=54329 DEV_USER=me DEV_PASSWORD='…'`.
Stop the database (data is kept in a Docker volume): `make db-stop`. Start from scratch: `docker compose down -v`.

### Option B — manual npm

```bash
docker compose up -d --wait postgres
export DATABASE_URL=postgresql://ascent_dev:local-dev-only@127.0.0.1:54329/ascent_dev   # local container only
export DIRECT_DATABASE_URL=$DATABASE_URL
npm ci && npm run db:migrate && npm run db:seed
npm run dev          # http://localhost:3000
```

With an empty database the site shows a **First-run setup** form to create your account (creation is atomic: two
simultaneous requests make exactly one account). Alternatively: `npm run user:create -- <username> "<display name>"`
(password via `ASCENT_PASSWORD` env or prompt). Sign-in locks for 15 minutes after 5 wrong attempts.

### Production build

```bash
npm run build && npm start     # serves on :3000
```

### Quality gates (same as CI)

```bash
npm test                 # vitest — pure domain/unit tests, no database needed
npm run test:pg          # integration + concurrency tests on isolated PostgreSQL schemas (TEST_DATABASE_URL, disposable DB only)
npm run typecheck        # tsc --noEmit (strict)
npm run lint             # eslint
npm run seed:validate    # docs/seed/*.yaml schema + id-reference checks (runs in CI)
npm run perf:budget      # initial JS ≤ 200 KB gzip on /today (NFR-02, runs in CI)
npm run art:validate     # public/art batch-1 presence, dimensions, size caps (local gate)
npm run visual           # pixelmatch visual regression vs baselines (needs an isolated QA server)
```

---

## Makefile reference

| Target | What it does |
|---|---|
| `make` / `make help` | Print the target list |
| `make dev` | deps → start local PostgreSQL → migrate → seed → ensure test user → serve on `$(PORT)` |
| `make demo` | Like `dev`, but in a separate `ascent_demo` database seeded with three weeks of sample data (`demo` / `demo-password-123`) |
| `make login` | Print URL + test username |
| `make db-stop` | Stop the local PostgreSQL container (data kept) |
| `make test` / `make test-pg` / `make lint` / `make typecheck` / `make build` | Pass-through to the npm scripts (`test-pg` starts the local database first) |
| `make start` / `make stop` | Build and launch the Windows widget detached / stop its process |

| Variable | Default | Meaning |
|---|---|---|
| `PORT` | `3100` | Dev server port (kept away from a possibly-running `:3000`) |
| `PG_PORT` | `54329` | Host port of the local PostgreSQL container |
| `DEV_USER` / `DEV_PASSWORD` | `test` / `test-password-123` | Credentials ensured by `user:ensure` |

Windows notes: this MSYS `make` build strips leading `VAR=value` assignments from recipes, so the Makefile passes the
database environment through an explicit `sh -c` wrapper — do not "simplify" it back.

## npm scripts reference

| Script | Purpose |
|---|---|
| `dev` / `build` / `start` | Next.js dev (`:3000`) / production build / production serve (`:3000`) |
| `test` / `test:watch` / `test:pg` | Vitest unit run / watch / PostgreSQL integration suite |
| `lint` / `format` / `typecheck` | ESLint / Prettier write / `tsc --noEmit` |
| `db:migrate` | Apply pending PostgreSQL migrations (forward-only, advisory-locked, checksum-verified; needs `DIRECT_DATABASE_URL`) |
| `db:seed` | Idempotent import of `docs/seed/*.yaml` (subjects, chapter weights, course sessions, exam structure, test sources) |
| `user:create -- <user> "<name>"` | Create a user from CLI (password: `ASCENT_PASSWORD` or prompt) |
| `user:reset-password` | Reset the single user's password, clear the lockout, sign everyone out (`ASCENT_NEW_PASSWORD`) |
| `user:ensure -- [user] [password]` | Idempotent dev user (defaults `DEV_USER`/`DEV_PASSWORD` or `test`/`test-password-123`) |
| `seed:validate` / `art:validate` | Validate seed YAML (CI) / art assets (local) |
| `perf:budget` | Assert initial JS ≤ 200 KB gzip on `/today` (NFR-02); runs in CI |
| `visual` | Visual regression (pixelmatch) of 5 main pages × Night/Cream vs committed baselines; run against an isolated QA server (`--base http://localhost:3103`, `--update` to re-baseline) |
| `demo:seed` | Fill an **empty local** database with three weeks of realistic sample data (refuses non-local databases) |
| `screenshots` | Regenerate `docs/images/*` (README gallery, hero, social preview) from a running app with demo data; needs Chrome/Edge |
| `icons:gen` | Generate app/PWA icons from source art |
| `telegram:bot` | Telegram bot helper for the opt-in reminder channel (chat-id discovery / polling) |
| `backup` | One verified backup file in `BACKUP_DIR` (30 kept) |
| `restore -- <file> [--drill] [--replace] [--migrate]` | Verified, atomic restore into `RESTORE_DATABASE_URL`; `--drill` = rehearse into an empty database |
| `offsite` | AES-256-GCM encrypted copy in `OFFSITE_DIR` (8 kept); restore it with `restore` |
| `replay` | Rebuild XP/SS/Gold/Gems ledgers from the event log and report diffs |

## Configuration & secrets

Copy [`.env.example`](.env.example) to `.env` (never commit `.env`). Next.js loads it for the server; CLI scripts read
the same variables from the process environment.

| Variable | Default | Notes |
|---|---|---|
| `DATABASE_URL` | — | **Pooled** PostgreSQL URL used by the app at runtime (verified TLS required for remote hosts) |
| `DIRECT_DATABASE_URL` | — | **Direct** (non-pooler) URL for `db:migrate`, restore and dumps; never set on Vercel Runtime |
| `TEST_DATABASE_URL` | — | Disposable database for `test:pg`; refused if it equals `DATABASE_URL` |
| `RESTORE_DATABASE_URL` | — | Explicit restore target (a scratch database for drills) |
| `DB_POOL_MAX` | `4` | Connections per instance (1–10) |
| `BACKUP_DIR` | `./data/backups` | Local/Docker nightly backups (30 kept); not used on Vercel |
| `OFFSITE_DIR` | `./data/offsite` | Encrypted weekly copies (8 kept) |
| `OFFSITE_KEY` | empty | Passphrase/64-hex for AES-256-GCM backups. **Required for Vercel's nightly backup and for offsite copies.** Store it separately from the copies — losing it makes them unrecoverable |
| `CAPSULE_KEY` | empty | Time-capsule encryption key. Empty = per-user local key in the DB `kv` table; set a passphrase to keep it out of the DB. Store separately from backups |
| `AI_KEY` | empty | The **only** place an AI key may live — never in the config DB or backups. Remote AI is enabled in the fresh profile but uses the deterministic local provider until both this key and a base URL are set |
| `AI_BASE_URL` | empty | Optional OpenAI-compatible endpoint; can also be set in the config editor |
| `TELEGRAM_BOT_TOKEN` | empty | Bot token for Telegram reminders (read from env, never stored in the config DB). Telegram also needs the chat id saved in Settings. **Web Push needs no env key** — VAPID keys are generated once per user and kept in their `kv` store |
| `TZ` | `Asia/Tehran` | Timezone for game-day boundaries and cron jobs |
| `DISABLE_JOBS` | unset | `true` skips cron scheduling (useful in tests/CI) |
| `CRON_SECRET` | empty | Vercel only: guards `/api/cron/*`; Vercel cron sends it as a Bearer header |
| `SETUP_TOKEN` | empty | **Set it on any internet-reachable server.** When set, creating the first account also requires this value, so a stranger cannot claim a fresh deployment |
| `COOKIE_SECURE` | auto | `false` for plain-HTTP local/Docker smoke runs; secure cookies in production |
| `DEV_USER` / `DEV_PASSWORD` | `test` / `test-password-123` | Used by `user:ensure` |
| `ASCENT_PASSWORD` | — | Password for `user:create` (else interactive prompt) |
| `ASCENT_NEW_PASSWORD` | — | Used by `npm run user:reset-password` |
| `MIGRATIONS_PG_DIR` / `SEED_DIR` / `DOCS_DIR` | repo paths | Override locations of migrations / seed YAML / codex docs |

The game-day boundary is compiled at 04:00 Tehran (`src/lib/time.ts`). The AI model and cost caps are configured in
**Settings → config editor**; `AI_BASE_URL` is an environment fallback. `DISABLE_JOBS`, `COOKIE_SECURE` and the
`DEV_*`/`ASCENT_*` vars are read by code but not listed in `.env.example`.

**Feature flags** (per user, Settings → config editor) gate optional surfaces. Default **ON**: `rival`, `bosses`,
`loot`, `shop`, `sleepProgram`, `ghostLeague`, `mascots`, `fog`, `bossRush`, `seasonPass`, `challengeCards`,
`anomalyAlerts`. Default **OFF**: `ai`, `sounds`, `calm`. Every default is a working offline experience; `calm` mode
strips confetti/springs/sounds/mascot art to simple fades.

**Reminders & notifications** (per user): `reminders` default on (tone `playful`, ≤5/day, shared cap across channels,
gentle — never guilt or streak-shaming); `notifications.push` and `notifications.telegram` default **off** and are
strictly opt-in. The 15-minute dispatcher only sends for users who enabled a channel.

## Data model & integrity

- **PostgreSQL** via Drizzle ORM (`node-postgres`); schema in [`src/db/schema.ts`](src/db/schema.ts), constraints, foreign keys
  and indexes in [`src/db/migrations-pg/`](src/db/migrations-pg). One database is the single source of truth.
- **Forward-only migrations** tracked in `_migrations` with checksums and a session advisory lock; applied only by
  `npm run db:migrate` (never at boot, build or cold start) — see [`docs/deploy.md`](docs/deploy.md) §3.
- **Transactions:** each domain operation runs in one transaction holding a per-user advisory lock
  (`withUserTransaction`), so an event, its projections and its ledgers commit atomically and concurrent requests for
  the same user serialize. Retries are idempotent through `UNIQUE (user_id, client_request_id)` plus a request gate.
- **First-run setup** is atomic: a singleton unique index guarantees exactly one account.
- **Event sourcing:** every mutation appends to the event log; XP / SS / Gold / Gems ledgers are *projections*.
  `npm run replay` rebuilds them from events and reports any drift — the anti-gaming backbone.
- **Reference seeds** ([`docs/seed/`](docs/seed)): a sample exam configuration — subjects, chapters, courses, chapter
  weights, exam structure and test-bank rows. Imports are idempotent upserts; re-seeding never clobbers user toggles
  (e.g. purchased banks). Third-party facts inside these files are covered by [`NOTICE`](NOTICE).
- **Exam honesty:** anything that is not officially published ships as a clearly **flagged assumption** (a visible
  "counts are an assumption — not official" chip and a per-subject assumed table), and the app never presents it as
  fact. When official data lands, only the YAML changes and the flag clears.
- **Jalali calendar** implemented dependency-free in [`src/i18n/`](src/i18n); game day rolls over at 04:00 Tehran.

## Scheduled jobs

Registered once per server process ([`src/jobs/boot.ts`](src/jobs/boot.ts)); skipped on Vercel and when `DISABLE_JOBS=true` (Vercel uses `vercel.json` crons → `/api/cron/*`). Boot never connects to the database or runs migrations:

| Job | Schedule (Tehran) | Behaviour |
|---|---|---|
| Nightly backup | 03:30 daily (local/Docker; on Vercel the 00:00 UTC cron) | Verified archive; local: `BACKUP_DIR`, Vercel: encrypted in private Blob; 30 kept, event logged |
| Reminder dispatch | every 15 min | Opt-in anchor reminders via Web Push / Telegram, ≤5/day shared cap, deduped per day; only for users who enabled a channel |

The **game day rolls over at 04:00 Tehran** — a derived boundary computed on read ([`src/lib/time.ts`](src/lib/time.ts)),
not a cron job; quest rollover, streaks and sleep debt settle against it. The nightly backup runs at 03:30, just before
that boundary.

## Backup, restore & recovery

```bash
npm run backup                          # verified archive now (BACKUP_DIR)
npm run offsite                         # encrypted copy now (needs OFFSITE_KEY)
RESTORE_DATABASE_URL=<scratch-url> npm run restore -- <file> --drill --migrate   # rehearsal into an EMPTY database
RESTORE_DATABASE_URL=<target-url>  npm run restore -- <file> --replace           # real restore (back up first)
npm run replay                          # verify ledgers against the event log
```

A backup is one gzip-JSON archive taken in a single read-only `REPEATABLE READ` transaction (consistent while the app
writes), with per-table row counts and SHA-256, the migration journal, and no login sessions. A restore is one
transaction that truncates, inserts in foreign-key order and re-checks every table against the archive — any mismatch
rolls everything back. Full procedures: [`docs/runbook.md`](docs/runbook.md). **Keep `OFFSITE_KEY` and `CAPSULE_KEY`
outside the backup set** — they are the only things backups cannot recover.

## Testing & CI

- `npm test`: pure domain engines (XP, score, levels, capacity, triage, planner, mastery, rival, boss, review, sleep,
  habits, pillars, combo, fog, exam, achievements) and Jalali calendar — no database needed.
- `npm run test:pg`: services, projections, migrations, backup/restore round-trips, idempotency and **concurrency**
  (simultaneous study logs, retries, first-run setup, login lockout, reward claims) on isolated PostgreSQL schemas.
- CI ([`.github/workflows/ci.yml`](.github/workflows/ci.yml)) on every PR and push to `main`, **Node 22**:
  - `check` (with a PostgreSQL 17 service): seed validation → lint → typecheck → unit tests → `test:pg` → production
    build without database credentials → **initial-JS perf budget** (≤200 KB gzip).
  - `docker`: image build + smoke test against PostgreSQL (explicit `db:migrate`, `db:seed`, `/healthz`, unauthenticated
    API returns 401, first-run setup page, 93 chapters seeded) + `docker compose config` validation.
  - [`migrate.yml`](.github/workflows/migrate.yml): manual, approval-gated production migration.
- Local-only gates (not in CI): `art:validate` (asset spec) and `visual` (pixelmatch regression, needs a QA server).
- Gates are never weakened to pass; a red gate is a blocker, not a suggestion.

## Project structure

```
app/(app)/        pages: today, map (+[id]), arena (+exam), forge, sheets, plan, coach,
                  habits, life, review, rest, final, ideas, character, courses (+[id]),
                  codex, deck, run, baseline, report/monthly, playground, settings
app/              focus, login, offline, onboarding (outside the (app) shell) · root redirect
app/api/          route handlers (auth, quests, tests, focus, plan, habits, forge,
                  ideas, arena, rest, reviews, shop, codex, undo, insights, wrapped, notify, personal-tasks, …)
desktop/          native Windows focus widget (Rust + Slint; see desktop/windows-widget/README.md)
src/domain/       pure, unit-tested game logic (xp, score, levels, quests, capacity,
                  triage, planner, mastery, rival, boss, review, sleep, habits, pillars, …)
src/events/       event store + projections (XP/SS/Gold/Gems ledgers, replay)
src/server/       services: auth, config, seed, reference, backup, offsite, ai, notify, …
src/config/       default game config + Zod schema (single source of tunable numbers)
src/db/           Drizzle schema + reversible SQL migrations (0001…0010)
src/jobs/         boot + cron (nightly backup, weekly offsite, reminder dispatch)
src/i18n/         dependency-free Jalali calendar
src/ui/           color-block components + icons
src/lib/          time/game-day helpers, utils
scripts/          tsx dev/ops tools · scripts/ops/ in-container shell scripts
docs/             design docs 01–13, ADRs, runbook, deploy, research, seed YAML
public/art/       batch-1 art (27 assets + style reference) + LICENSE.md provenance register
data/             SQLite DBs + backups (git-ignored)
```

## Art & design system

- Style contract: [`docs/art-brief.md`](docs/art-brief.md) (scene/mascot specs, dimensions, WebP size caps);
  character bible: [`docs/mascot-bible.md`](docs/mascot-bible.md) — **Hero** (yellow hoodie), **Shade** (purple rival
  shadow), **Archie** (guide); flat vector, thick outlines, glossy medals.
- `npm run art:validate` enforces presence, dimensions and byte caps for all **27 batch-1 assets**; every file's
  tool, date, prompt reference and originality is recorded in [`public/art/LICENSE.md`](public/art/LICENSE.md).
- UI: color-block cards, **Night/Cream** themes (WCAG 2.1 AA contrast in both), fonts Bebas Neue (display) + Nunito
  (body) + Vazirmatn (Persian), RTL-first layouts with `lang="fa" dir="rtl"` on Persian text. Accent colors used as
  text have theme-aware `*-ink` token variants so they stay legible on Cream.

## Deployment

Prepared but **not deployed yet**. Production = **Vercel Functions + one managed PostgreSQL** (`DATABASE_URL` pooled,
`DIRECT_DATABASE_URL` for operators only). Release order: fresh backup → `npm run db:migrate` (direct URL, never at
build) → deploy → staging checklist. Blob holds only encrypted nightly backups. Self-hosting: `docker compose --profile
selfhost up -d --build` (PostgreSQL + app + Caddy).

Everything — env table, release process, rollback policy, backup/restore drill, staging checklist — is in
[`docs/deploy.md`](docs/deploy.md) and [`docs/runbook.md`](docs/runbook.md). Production starts with a **fresh account**;
local SQLite data is not imported.

**Moving all data:** Settings → *Move all data* exports/imports a verified archive (e.g. Vercel → local). Import takes a
verified safety backup first and replaces everything in one transaction.

## Troubleshooting

| Symptom | Cause & fix |
|---|---|
| `ECONNREFUSED 127.0.0.1:54329` | Local PostgreSQL is not running: `make dev` starts it; or `docker compose up -d --wait postgres` (Docker Desktop must be running) |
| `PostgreSQL migrations require a direct connection` | You passed a pooler URL to `db:migrate`/`restore`; use `DIRECT_DATABASE_URL` |
| `EADDRINUSE :::3000` / `:::3100` | Another instance holds the port. Stop it, or `make dev PORT=3101` |
| `make` ignores `VAR=value` prefixes / exports | MSYS make quirk on Windows — the Makefile already wraps env in `sh -c`; don't "simplify" it back |
| Sign-in locked | 5 wrong attempts → 15-minute lockout; wait, or `npm run user:reset-password` |
| Vercel backup cron returns 500 | `OFFSITE_KEY` missing or Blob store not linked; backups never run unencrypted |
| Telegram reminders silent | `TELEGRAM_BOT_TOKEN` unset or chat id missing — set the token in env and the chat id in Settings; both channels are opt-in |
| First-run setup instead of login | The targeted DB has no users yet — create one via the form or `user:create` / `user:ensure` |
| Persian text garbled in GitHub CLI bodies | Use `--body-file` (or `--comment "$(cat file)"`); heredocs corrupt UTF-8 Persian on Windows shells |

## Documentation map

| Doc | Content |
|---|---|
| [`docs/README.md`](docs/README.md) | Index of the design program |
| `docs/01…13-*.md` | Vision & psychology · exam domain & data · capacity & triage · game design · habit engine · feature spec · architecture & data model · UI/UX spec · implementation plan · decisions & open items · Duolingo analysis · UI style analysis · ideas backlog |
| [`docs/adr.md`](docs/adr.md) | Architecture decision records (ADR-0001…) |
| [`docs/runbook.md`](docs/runbook.md) | Operations, backup/restore, password reset |
| [`docs/deploy.md`](docs/deploy.md) | Vercel + PostgreSQL / Docker deployment, env table, release & rollback policy |
| [`docs/research/`](docs/research) | Exam-data research incl. T-DATA-02 coefficients verification |
| [`docs/seed/`](docs/seed) | Reference YAML: subjects, chapters, courses, exam structure, test sources |
| [`docs/art-brief.md`](docs/art-brief.md) · [`docs/mascot-bible.md`](docs/mascot-bible.md) | Art production contract & characters |

## Conventions

- One changeset per branch/PR; conventional commits (`feat:`, `fix:`, `chore:`…); CI must be green before merge.
- Issues are closed **by hand after merge** with evidence comments; PR bodies avoid auto-closing keywords for
  externally-gated work.
- Persian GitHub text goes through `--body-file`; UI strings stay RTL-correct.
- Secrets only in env (`.env`, never committed); keys stored apart from backups.
- Tests and CI gates are never weakened; assumptions in reference data are always flagged, never silently official.

---

*Personal project — art assets are AI-generated with a full provenance register (`public/art/LICENSE.md`); code and
design docs are private to the owner.*

## License

Source code and documentation text: [MIT](LICENSE). Artwork: CC BY 4.0 ([`public/art/LICENSE.md`](public/art/LICENSE.md)).
Third-party facts in `docs/seed/` and `docs/research/` are **not** covered — read [`NOTICE`](NOTICE).
