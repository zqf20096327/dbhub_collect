# OpenVitals — own your wearable data

A local-first system to pull your own biometrics off your wearable. It currently supports the
**WHOOP 4.0**: live heart rate and HRV straight off the strap over Bluetooth, sleep, Strain
and Recovery estimated from the strap, your WHOOP history from the official API as an
archive, a localhost dashboard, and encrypted local and cloud backups. No membership is
needed for the strap side. Everything stays on your machine unless you turn the cloud parts on.

> **Your device, your data.** This is personal interoperability and backup — not for any
> device you don't own. It's **not a medical device** (fitness/self-tracking only), and it's
> reverse-engineered (a firmware update can change the protocol). WHOOP's own scores come
> from its cloud through the API and stop where your membership stopped. Current Strain,
> Sleep and Recovery are **estimates** computed from the strap. Each is versioned and shown
> only when the data behind it passes its checks.
>
> OpenVitals is an independent project. It is not affiliated with, endorsed by, or sponsored
> by WHOOP, Inc. "WHOOP" is a trademark of WHOOP, Inc. and is used here only to name the
> device the software works with.

## What it does
Details, commands and the method behind each number are in **`whoop-tools/README.md`**.

**Collecting**
- **Always-on daemon** (`daemon.py`): connects when the strap is near, reads what it stored
  while away, streams live heart rate, and reads storage again every 5 minutes. After the Mac
  sleeps it reconnects by itself, and restarts itself if macOS Bluetooth is stuck.
- **Store and forward**: the strap records every second on its own. Raw frames are saved
  before they are acknowledged, so a crash does not lose data.
- **WHOOP archive**: your scored history through the official API (OAuth), kept as a dated
  archive behind a calendar.

**Computed from the strap**
- **Sleep** (`sleep.py`): falling asleep, waking and wake-ups from wrist movement and heart
  rate. Checked against a sleep lab (PhysioNet sleep-accel, 31 nights, held-out): falling
  asleep off by about 7 min, time asleep by 43 min, 86% of 30 s epochs right. It still counts
  about 3 wake-ups too many a night, and the check used Apple Watch recordings, not this strap.
- **Strain, Sleep need, Sleep performance, Recovery** (`scores.py`): versioned models.
  `generic-v1` is the default for anyone. `calibrate.py` fits your own model on your WHOOP
  archive and uses it only where it does at least as well. `v1` is frozen and applies only to
  the archive it was fitted on (errors on its held-out days: strain 0.5 on workouts and 1.3 on
  whole days, sleep performance 4.9 points, recovery 7.1 points and the right zone on 86% of days).
- **Breathing rate** during sleep, from beat intervals. About 1.1 breaths/min off per
  recording on held-out public recordings (chest sensors, not this strap).
- **Energy (kcal)** (`energy.py`): from heart rate and your body data, which stays in the
  local database. A rough estimate, about 16–18% off.
- **Skin temperature** as a nightly change from your usual (not calibrated to °C), **steps**
  and **on/off wrist**.
- **Stress monitor** (`stress.py`): 0–3 every 5 minutes while you are still and awake,
  against your own calm. It cannot tell coffee, talking or standing up from stress.
- **Health alerts** (`alerts.py`): resting HR up, HRV down, short sleep, breathing rate up,
  very low recovery. Each needs 3 clean nights in a row.
- **Coverage**: how much of each day has heart rate, and why the longest gap is there.

**On the strap**
- **Battery**: the strap's own reading (GetBatteryLevel), plus the Bluetooth Battery Level
  value, which is most likely the slide-on battery pack (not proven).
- **Silent alarm and buzz** (`alarm.py`): a fixed wake time kept on the strap, and a test
  buzz. Verified on a real strap.

**Around it**
- **Dashboard** on localhost: Heart, Today, Archive, Device. Works offline.
- **Telegram** (optional): a morning message with a recommendation, nudges (battery, strap
  missing), `/status` and `/now`.
- **Phone app** (optional): the same dashboard on your own Cloudflare Worker, behind a
  password, with passkey sign-in.
- **Backups**: encrypted local snapshots, Cloudflare D1 sync, and raw frames archived to
  Cloudflare R2 (encrypted, verified, then removed locally).

## Not built yet
- Sleep stages (deep, REM).
- Blood oxygen (SpO2): the data the strap stores cannot support it.
- Automatic workout detection and training load.
- A sleep planner ("go to bed by…").
- A journal (caffeine, alcohol) and what moves your recovery.
- A smart alarm that picks the wake time from how rested you are. Today the alarm is a fixed time.
- WHOOP 5.0/MG (a different protocol).
- A Linux install (the launchd services are Mac only).

## Give it to an AI (easiest path)
1. Clone this repo and open it in an AI coding agent (e.g. Claude Code) on the Mac with the
   strap nearby.
2. Point the agent at **`skills/reverse-engineer-whoop/SKILL.md`** (or copy that folder to
   `~/.claude/skills/` to make it a first-class skill), then say:
   > "Use the reverse-engineer-whoop skill to help me own my WHOOP 4.0 data."
3. The agent follows the skill: finds the strap by BLE service UUID, proves the command
   path, streams live HR, drains history, wires up the WHOOP API, and stands up the
   dashboard + backups.

## Do it yourself
```bash
cd whoop-tools
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python whoop.py selftest        # prove the protocol frame builder
.venv/bin/python daemon.py                # hold the strap while it's nearby: drain + live HR; Ctrl-C to stop
# official API: copy .env.example -> .env, add dev-app creds, then:
.venv/bin/python whoop_api.py login && .venv/bin/python whoop_api.py sync
.venv/bin/python dashboard.py             # http://localhost:8787
```
Full setup, backups, and the always-on background service are in **`whoop-tools/README.md`**.

The strap records one sample a second on its own. `daemon.py` connects whenever the strap
is near the laptop, collects what it stored while you were away, and streams live in
between, so the heart-rate record has no gaps even though the laptop is not always there.

## Preview with demo data (fill-in template)
This repo ships **synthetic demo data only** — a fictional "Demo User", no real person's
biometrics. See the dashboard populated before connecting anything:
```bash
cd whoop-tools
.venv/bin/python seed_demo.py                              # (re)generate data/whoop-demo.db
WHOOP_DB=data/whoop-demo.db .venv/bin/python dashboard.py  # http://localhost:8787
```
When you run the real pipeline it creates your **own** `whoop.db` (gitignored) and fills it
from your strap + API. The demo DB is just the template so you know what "done" looks like.

## The dashboard
A local, offline app (`whoop-tools/static/`, vendored Chart.js, light/dark theme):

- **Heart** (full screen, the landing view): a 3D heart that beats on the strap's real beat
  timing, metric callouts tied to the mesh, an exploded mode (`E`), full screen (`F`),
  drag to rotate, a live pulse strip and a timeline.
- **Today**: only what the strap recorded today (live monitor, heart rate over the day,
  daytime HRV from RR intervals), compared against your archive baseline.
- **Archive**: WHOOP cloud history behind a calendar. Every page is labelled with the day
  you're viewing: recovery, vitals, trends, sleep, activity and workouts for that day.
- **Device**: strap battery, **heart rate coverage** per day (how much of the day has heart
  rate, how much is still on the strap, and why the longest gap is there), stored record
  counts, decoded firmware log, and a **Resync** button that runs one collector cycle (or asks
  the running daemon to drain now).

## Keeping coverage high
Strain, Sleep and Recovery are only shown when the strap recorded enough of the day (85%) or
night. The morning Telegram message says when strain was held back and where the biggest
gap was. How the data gets in:

- The strap records every second on its own, worn or not near the Mac, and keeps days of
  it (the exact capacity is not measured yet). When the Mac sees the strap again, the daemon reads everything stored and fills the
  gaps. So **the Mac being asleep or you being out of range does not lose data**; it only
  delays it until the next connection.
- What does lose data:
  - **The strap is off your wrist or charging.** It records nothing then. Charge it while
    you sit at the desk (about an hour), not overnight or while you are out.
  - **Another app reads the strap first.** The WHOOP phone app (or any second copy of this
    daemon) takes the stored history and the strap then deletes it. Log out of the WHOOP app
    on your phone, or turn its Bluetooth off, and run only one daemon.
  - **The strap's memory fills up.** That takes days away from the Mac. Open the Mac near
    the strap at least once every couple of days.
- What makes data arrive sooner (so the morning message and today's numbers are complete):
  - Keep the Mac within about 10 m of the strap: the bedroom at night is ideal.
  - Plugged in, let the Mac stay awake with the screen off: System Settings > Battery >
    Options > "Prevent automatic sleeping on power adapter when the display is off" (or run
    `caffeinate -s` in a terminal). Leave the lid open: a closed lid puts a MacBook to sleep
    unless an external display is attached.
  - Leave Bluetooth on. After a wake the daemon reconnects by itself (and restarts itself if
    macOS Bluetooth is stuck), usually within two minutes.
- The Device page shows each day's coverage. "Still on the strap" means it will fill in at
  the next sync; "nothing stored" means the strap was off your wrist, charging, or another
  app read it.

Screenshots below use the synthetic demo data:

![Heart view](skills/reverse-engineer-whoop/images/02-dashboard.png)
![Today](skills/reverse-engineer-whoop/images/03-trends-sleep.png)
![Archive day](skills/reverse-engineer-whoop/images/04-activity-device.png)

## Do it yourself with an agent
Point your coding agent (Claude Code, Codex, Cursor) at
[`skills/reverse-engineer-whoop/SKILL.md`](skills/reverse-engineer-whoop/SKILL.md). It walks
from a blank machine to a running system in seven phases, each with a "done when" check, and
`skills/reverse-engineer-whoop/scripts/doctor.py` tells it what's done and what's next.
Setup, protocol, data model, dashboard, troubleshooting and the optional Cloudflare backup
are in `skills/reverse-engineer-whoop/resources/`.

## What's here
- `whoop-tools/` — the working system (BLE protocol, always-on daemon, API sync, decode,
  sleep, scores, stress, alerts, alarm, dashboard, Telegram, encrypted backups, Cloudflare
  D1 sync and Worker, launchd services).
- `whoop-tools/templates/` + `import_data.py` — **device adapter**: no WHOOP 4.0? Fill the
  CSV templates from any wearable's export (Oura, Garmin, Apple Health, Fitbit…) and import
  them into the same dashboard. Mapping guide + agent prompt in `templates/README.md`.
- `skills/reverse-engineer-whoop/` — a portable skill + `resources/PROTOCOL.md`
  (verified protocol + command table) and `resources/WALKTHROUGH.md` (the end-to-end path).

## Architecture
```
 WHOOP 4.0 strap ──BLE──►  whoop.py / daemon.py ───────────────┐
 WHOOP API (OAuth) ──────►  whoop_api.py ─────────────────────┤──►  SQLite (whoop.db)
                                                              │        │
                                      decode.py (raw→tables) ─┘        ├─► dashboard.py (localhost)
                                                                       ├─► backup.py (encrypted local)
                                                                       ├─► cloud_sync.py (Cloudflare D1)
                                                                       └─► archive.py (raw frames → Cloudflare R2, then removed locally)
```
