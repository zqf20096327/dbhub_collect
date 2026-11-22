# SceneLingo 🎬

A Telegram bot for useful expressions with matching short movie clips and explanations. Subscribers choose a CEFR level, learning language, explanation language and delivery interval inside Telegram.

> Learn languages by watching movies — expressions for your level, zero self-hosting.

> **Multilingual rollout is experimental.** Clip availability varies by language, automatic audio verification is imperfect, and free-tier rate limits and worker duration can delay or prevent delivery. Telegram has no send idempotency key. Durable per-slot claims prevent blind replay; interrupted or timed-out sends are marked uncertain, so delivery is not guaranteed exactly once. Test your setup before enabling production delivery.

## How it works

```
cron-job.org (every 10 minutes)
    │  POST → GitHub API (repository_dispatch)
    ▼
GitHub Actions (free ephemeral runner)
    │
    ▼
daily_job.py
    ├─ Neon Postgres   → due subscribers and their preferences
    ├─ Expressions     → curated candidates or transcript-first selection by CEFR level
    ├─ Clip.Cafe       → search and download a clip with a matching audio track
    ├─ Groq Whisper    → verify spoken language and phrase (best effort)
    ├─ Groq Qwen       → localized explanation and example
    ▼
Telegram Bot API       → send to each due subscriber
```

Use `/start` for guided setup: bot interface language (Arabic or English) → learning language → CEFR level → explanation language → delivery interval → review and confirm. Delivery starts only after confirmation. Use `/level` to pick A2–C2, `/learn` for the learning language, `/explain` for the explanation language, and `/interval` to choose a preset from 30 minutes to 24 hours. `/today` shows the most recent expression for the selected level and learning language; `/stop` unsubscribes. Both language menus offer English, Chinese, Hindi, Spanish, French, Arabic, Portuguese, Russian, German and Japanese. Intervals offer preset buttons (half an hour to 24 hours) only; typed numbers are not accepted. `/language` changes the bot interface language without changing learning or explanation preferences. Existing intervals below 30 minutes are raised to 30. Existing subscribers retain their subscription and default to English, Egyptian Arabic and 180 minutes. CEFR labels are approximate.

## Stack

| Tool | Role |
| --- | --- |
| cron-job.org | External HTTP POST every 10 minutes |
| GitHub Actions | Free ephemeral worker |
| Python + python-telegram-bot | The bot |
| Neon (Postgres) | Database |
| Clip.Cafe | Movie quote search and short clips |
| Groq API (`qwen/qwen3.8-27b`, Whisper) | Expressions, explanations and audio verification |

## Setup

### 1. Create the Telegram bot

Chat with [@BotFather](https://t.me/BotFather) → `/newbot` → copy the `BOT_TOKEN`.

### 2. Create the database

- Sign up at [Neon](https://neon.tech) (free, no credit card) → create a project → copy the **connection string** (`DATABASE_URL`).
- Run the schema once:
  ```bash
  pip install -r requirements.txt
  DATABASE_URL=postgresql://... python -m db
  ```

### 3. Get a Groq API key

- Sign up at [Groq](https://console.groq.com) → API Keys → create key (`GROQ_API_KEY`).

### 4. Configure

```bash
cp .env.example .env
# fill in BOT_TOKEN, DATABASE_URL, GROQ_API_KEY
```

### 5. Handle /start for free (Vercel, browser-only)

`bot.py` uses polling and needs a running process. For 24/7 free hosting
that works entirely from a phone browser:

1. Open [vercel.com](https://vercel.com) → sign in with GitHub → **Add New → Project**
   → import this repo. Framework preset: **Other**.
2. Add environment variables: `BOT_TOKEN`, `DATABASE_URL`.
3. Deploy. Then open this URL in your browser:

```
https://api.telegram.org/bot<TOKEN>/setWebhook?url=https://<your-app>.vercel.app/api/telegram
```

Telegram replies `{"ok":true,...}` — done. The function in `api/telegram.js`
handles the Telegram controls and talks to Neon over TLS. The webhook and scheduled job apply additive migrations automatically.

### 5b. Legacy Cloudflare Worker (does not support levels)

```bash
npm i -g wrangler
wrangler login
wrangler secret put BOT_TOKEN
wrangler secret put DATABASE_URL
wrangler deploy
```

This legacy worker does not implement level selection; use the Vercel webhook above for this version.

For local testing you can still run `python bot.py` (polling) instead.

### 6. Run locally (optional)

The `imageio-ffmpeg` dependency supplies FFmpeg when no system binary is available. A system `ffprobe`, if installed, is used for the stream-language precheck; otherwise the bundled FFmpeg inspects the stream.

```bash
pip install -r requirements.txt
python daily_job.py  # sends to subscribers whose delivery time is due
```

### 7. Automate with GitHub Actions

1. Push this repo to GitHub (public repo → free Actions minutes).
2. Add secrets: **Settings → Secrets and variables → Actions** → `BOT_TOKEN`, `DATABASE_URL`, `GROQ_API_KEY`.
3. Merge the workflow into the default branch. You can also trigger it manually from the **Actions** tab.

### 8. Schedule via cron-job.org

Create a free job on [cron-job.org](https://cron-job.org) scheduled every 10 minutes that POSTs directly to the current repository URL (update it after any repository rename):

```
https://api.github.com/repos/revolover00/scenelingo/dispatches
```

with headers `Authorization: Bearer <PAT>`, `Accept: application/vnd.github+json`, and `Content-Type: application/json`, and body `{"event_type": "daily-word"}`.
The PAT needs `repo` scope (classic) or repository Contents read and write permission (fine-grained). The workflow must exist on the default branch and be enabled. Store the token only in the scheduler, not in the repository. This polling interval is not a delivery-time guarantee: Actions queueing, source availability, verification and rate limits can delay or prevent messages.

## Environment variables

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| `BOT_TOKEN` | ✅ | — | Telegram bot token |
| `DATABASE_URL` | ✅ | — | Neon Postgres connection string |
| `GROQ_API_KEY` | ✅ | — | Groq API key |
| `GROQ_MODEL` | | `qwen/qwen3.8-27b` | Groq model |
| `WORDS_FILE` | | `words.txt` | Word bank (one word per line) |
| `CLIP_BEFORE` | | `2` | Seconds before the word |
| `CLIP_AFTER` | | `3` | Seconds after the word |
| `SEND_DELAY` | | `0.2` | Seconds between sends |

## Project structure

```
bot.py               # Telegram bot, /start etc. (polling, for local use)
worker.js            # Cloudflare Worker webhook — free 24/7 /start hosting
daily_job.py         # Daily broadcast pipeline
phrases.py           # CEFR-labelled expressions and topics
clip_cafe.py         # Movie quote search and clip download
yarn_clips.py        # Legacy Yarn integration
youtube_free.py      # Legacy InnerTube search
clipper.py           # yt-dlp + FFmpeg clip cutting
groq_meaning.py      # Groq meanings (with retries)
words.py / words.txt # Word bank
db.py / schema.sql   # Neon Postgres layer
config.py            # Env config
tests/               # pytest suite
.github/workflows/daily.yml  # daily broadcast
.github/workflows/test.yml   # CI tests on push
```

## Testing

```bash
pip install -r requirements.txt -r requirements-dev.txt
python -m pytest -q
npm ci
node --test tests/telegram.test.js
```

## Notes

- Clip.Cafe integration parses public pages and HLS playlists, which may change or become unavailable. A localized audio track is combined with the video when available; otherwise the original MP4 is checked.
- English expressions use a curated bank, with generated candidates after it is exhausted. Other languages prefer expressions selected from a verified transcript, then fall back to generated candidates. Clips are only sent after best-effort audio verification. Some language/level combinations may have no usable clip.
- Serialized Actions runs and a pre-send settings check reduce races, but Telegram sends and database updates cannot be atomic. Long-running jobs can delay individual schedules; provider free tiers impose usage limits.
- Clips are short excerpts from Clip.Cafe for educational use.

## License

Copyright © 2026 SceneLingo. **All rights reserved for new original material
covered by the current [LICENSE](LICENSE).**

Copying, modification, redistribution, hosting and commercial or non-commercial
use of that restricted material require prior written permission, except where
applicable law or platform terms provide otherwise. This is not an open-source
license.

**Previously MIT-licensed material remains available under MIT**, including its
commercial-use permissions. This change is not retroactive and does not restrict
that material merely because it is included in a newer version. The historical
notice is preserved in [LEGACY-MIT.txt](LEGACY-MIT.txt).

Public GitHub viewing and forking permissions remain governed by GitHub's terms.
Third-party content remains subject to its owners' rights and licenses.
See [Rights and attribution](OWNERSHIP.md).

### Starting with a different Telegram bot

Each bot now stores subscriptions and expression history in its own Postgres schema,
`bot_<numeric Telegram bot ID>`. Token rotation for the same bot retains its data;
a different bot starts with an empty subscription list. Public/legacy tables are
not deleted or imported. Both the webhook and scheduled sender use this isolation.

Update `BOT_TOKEN` in Vercel and GitHub Actions, deploy, then run **Configure Telegram
bot** with the new bot's numeric ID. The setup verifies the GitHub token belongs to
that bot before initializing its schema or registering the production webhook.
Users must open the new bot, press `/start`, and confirm setup before delivery.
Never put tokens in source files or workflow inputs.

### Private administration dashboard

Production URL: `https://scenelingoo.vercel.app/`. The root and `/dashboard` require
HTTP Basic authentication over HTTPS (username `admin`). Store only a SHA-256 hash
of a strong random password in the sensitive production variable
`DASHBOARD_PASSWORD_HASH`; never use the bot token as a dashboard password. Missing
configuration fails closed. All data responses use `private, no-store`. The dashboard
is read-only: opening it cannot trigger content generation or broadcasts. It shows
aggregate counts, active language/level/interval cohorts, due counts, recent expressions,
and the last 30 scheduler outcomes with counters for newly recorded runs. No subscriber IDs or names are returned.

Run history starts with this release. `completed` is a run outcome, not a delivery
count, token usage figure, or guarantee of delivery. Details of errors remain in
GitHub Actions; secrets and raw exception messages are not copied to the dashboard.
The scheduler rechecks demand before clip search, explanation generation, and sending.
No content generation occurs for empty or no-longer-due groups. One verified clip
is shared per learning-language/level group and one explanation per requested
explanation language, irrespective of delivery interval.

The old Vercel domain is retained for compatibility. New webhook setup uses
`https://scenelingoo.vercel.app/api/telegram`.

### Lesson captions

Lesson generation returns validated JSON (`meaning`, `usage`, `example`,
`translation`) rather than a free-form caption. A separate renderer owns the
localized headings, spacing, source attribution and Telegram caption budget.
The verified expression is preserved exactly; the practice example is explicitly
labeled as new, not a movie quote. The prompt forbids invented scene details.
Malformed or missing fields fail closed instead of sending broken lessons.
Presentation limits count UTF-16 units, including emoji, and omit a source link
when it cannot fit rather than cutting the expression or lesson block in half.
This uses one explanation request per requested explanation-language cohort,
not one request per subscriber, with no additional generation on idle runs.

### Half-hour clock slots

The 30-minute option is due at each :00 and :30 boundary, starting at the next
strictly future slot, rather than 30 minutes after subscription or delivery.
Both the webhook and worker load `scheduling.sql` for the same SQL function.
Longer intervals retain elapsed-time scheduling. Future unaligned 30-minute
preferences are migrated; already-overdue work remains due. Manual send-now
is an explicit override, and the following automatic due time uses clock slots.
The external cron should run at minutes `0,30` (`0,30 * * * *`), not just at a
30-minute offset from when the cron was created. Queueing and clip preparation
can delay actual delivery. No catch-up burst is sent after missed slots.
When initializing the database manually, apply `schema.sql` then `scheduling.sql`
in the bot's isolated schema; `db.init_db()` does both automatically.


## Reliable SceneLingo delivery

Production now uses `reliable_delivery.py`, backed by bot-local tables from
`reliability.sql` (loaded automatically by Python initialization and the webhook).
The older `run_due_subscribers` helper remains for compatibility and tests; the
production entry point uses the durable worker instead.

- A session advisory lock prevents concurrent workers for the same bot.
- A unique `(chat_id, due_at)` claim is committed before any Telegram upload.
  Receipts are saved before schedules advance. A terminated worker's unresolved
  claims become **uncertain**, never silently resent. Uncertain sends advance
  the schedule conservatively on recovery. This can skip a delivery; it is not
  an exactly-once guarantee, and uncertainty needs operator review.
- Only explicit Telegram rate-limit refusals are retried (up to 3 calls, waits
  capped at 60 seconds). Exhausted refusals cool down at least 15 minutes with
  at most 3 slot claims. Network timeouts are ambiguous and are not auto-retried.
  Blocked users are deactivated; permanent rejections advance the schedule.
- Successfully uploaded verified clips are retained as bot-specific Telegram
  `file_id` references, not binary files in Git or the database. Reusable captions
  are stored by explanation language. Cache selection excludes content already
  sent or potentially sent to any intended recipient. No level/language is
  silently downgraded if verified content is unavailable. The cache grows only
  through actual requested deliveries; this is NOT a prefilled content library.
- The dashboard reports durable delivery states, classified send errors, cache
  counts, saves, feedback, run counters and reported API token usage. API usage
  counts SDK operations, not each internal HTTP retry; missing token counts are
  null, not fabricated. No USD cost or quality guarantee is implied.
- Below new clips: save the expression or report an unclear explanation/clip.
  Only a recorded recipient may act on that lesson. `/saved` shows up to 10 saved
  expressions; `/review` starts a self-assessed recall exercise. Remembered items
  double their review spacing up to 30 days; difficult items return after one day.
  Reviews are user-initiated, not unsolicited reminder broadcasts or AI grading.

Display/package branding is **SceneLingo** (`scenelingo`). Existing GitHub repository
URLs, the live `scenelingoo.vercel.app` domain and Telegram username are deliberately
preserved so deployment, cron and existing links continue working. Renaming those
external resources is a separate migration, not a text replacement.

### Operator checklist

Run `npm test` and `python -m pytest -q`, then initialize using the existing
**Configure Telegram bot** workflow after deployment. The browser integration
workflow checks private access, real database aggregates, rendering and mobile
layout without broadcasting. For a real Telegram test, use an explicit manual
send to opted-in recipients only. Monitor uncertain receipts and content failures;
never bulk-reset claims to force retries. Historical commit messages on shared
branches have not been rewritten. Copyright permissions and human review of
content remain operator responsibilities.


## Ten-minute preparation window

Keep the external cron at **every 10 minutes**. Each serialized worker run sends
currently due lessons first, then prepares lessons due within the next 10 minutes.
Preparation checks the current subscription and settings, reuses verified content
and explanations where possible, and never sends Telegram messages or advances a
schedule. A partial media assignment survives explanation failure, allowing the
next tick to retry the missing explanation rather than select another clip.

Prepared slots are keyed by recipient and exact due time, with a settings version.
Delivery only uses a matching, ready assignment and rechecks eligibility before
sending. Stopped or changed subscriptions cannot bypass the normal preflight.
Missing/expired preparations use the existing verified on-demand pipeline, so a
new subscription or missed preparation tick does not permanently block delivery.
Existing delivery claims and uncertainty rules still apply.

For this small deployment, verified clip bytes use a **temporary Postgres buffer**,
shared by lesson, not per user: at most **20 MiB per clip and 80 MiB total**, with a
24-hour expiry. Cleanup runs on each worker invocation and removes expired media
and media already reusable via Telegram file ID. Old slot assignments are cleaned
after their due time plus 24 hours. These are application limits, NOT reserved
provider capacity: database quotas, backups, WAL and network overhead still apply.
No new storage credentials, public clip URLs or binary files in Git are needed.
Larger clips or a full buffer fail preparation visibly and retain the existing
on-demand delivery fallback. At larger scale migrate this buffer to object storage.

Logs report prepared slots and preparation failures; failures cause a failed run
and are retried on later ticks. The dashboard's delivery counts are NOT counts of
prepared slots. No early upload to an admin/staging Telegram chat is performed.

**Timing limits:** this is lookahead preparation, not a real-time scheduler.
GitHub runner startup/queues can delay both phases; a due time between cron ticks
can wait until the next tick. Overlapping invocations share the existing workflow
concurrency group and database lock. Do not promise second-accurate delivery.


### Scheduler fallback

The delivery workflow also has a native GitHub Actions schedule every ten minutes.
The external `daily-word` dispatch remains supported. Both paths share workflow
concurrency and the database worker lock; native schedules can be delayed and do
not guarantee exact delivery times. The native schedule runs from the default
branch and depends on GitHub Actions being enabled.


### Webhook authentication and operational checks

POST updates require Telegram's `X-Telegram-Bot-Api-Secret-Token` header. The value
is derived consistently by Python and JavaScript using HMAC-SHA256 with a
versioned, domain-separated message and the existing bot token; it is not the bot
token itself. Do not log it. Token rotation requires webhook re-registration.
Configure Telegram bot registers the secret while preserving pending updates.
For rollout, first run its webhook-only repair mode from the new revision, then
deploy the authenticated receiver. Profile-only mode still never changes webhooks.

Each delivery workflow also checks the expected webhook URL, authenticated endpoint
health and rejection of unauthenticated updates. A recent Telegram delivery error
with pending updates fails the check. It does not automatically overwrite webhook
changes during routine delivery. GitHub failed-run notifications depend on the
repository/account notification settings; there is no separate SMS/email service.

Preparation counts, failures, duration and current media buffer usage are visible
in the private dashboard. Preparation logs are retained for 30 days. A stale-run
warning appears after 30 minutes without a recorded run; a recent manual run is
not proof that the external cron or GitHub scheduler is working automatically.

The browser integration workflow also runs a disposable-schema Postgres lifecycle
check: prepare synthetic fixture content, delete its local file, reject early
sending, shift only the fixture's clock to due, restore persisted media and simulate
one send. No subscriber data is changed and no Telegram call is made. This tests
storage and routing, not audio quality or actual Telegram transport.


### Private subscriber administration

The authenticated dashboard now includes a read-only subscriber directory, with
50-row pages and parameterized search by stored name, username or Telegram ID.
It shows stored first name/username, subscription status, language/level/interval
preferences, setup state via status, subscription/settings timestamps, next due
time and last recorded delivery outcome/error/expression. Telegram IDs are strings
to preserve precision. There is no phone number, email, read receipt or other
uncollected profile information. Names are currently refreshed by `/start` and may
be stale or absent. Access requires the same private admin authentication; never
share credentials or screenshots containing user data publicly.

### Shared lesson library across delivery intervals

Production chooses the **oldest unseen reusable lesson for each recipient** within
their learning language and level. A 30-minute subscriber can advance through the
library while hourly/daily subscribers consume those same lessons at their own due
times. This is a per-person backlog, not a group-wide exclusion: a fast subscriber
having seen lesson A no longer forces everyone else to skip A and generate more.

The library uses existing Telegram file IDs or unexpired prepared media. Captions
are reused separately by explanation language. Recorded sent/uncertain/sending
lessons are excluded per recipient; pinned retries and prepared-slot assignments
take priority. Normal subscription/settings/due-time checks and delivery claims
still apply. If no matching reusable lesson exists, verified on-demand generation
remains the fallback. This reduces redundant media/AI work, not the number of cron
checks or Telegram sends. It does not create missing verified content or reduce
quality/level to fill a gap.
