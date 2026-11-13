# DEBRIEF

<p align="center">
  <img src="docs/assets/debrief-banner.svg" alt="DEBRIEF — find what's been following you" width="100%">
</p>

<p align="center">
  <strong>Your phone and your Kismet rig already heard every tracker, hotspot and gadget that crossed your path today.</strong><br>
  DEBRIEF goes back through those logs and shows you which ones <em>kept showing up</em> — at the coffee shop, at work, down your street.
  Offline. No accounts. Nothing uploaded.
</p>

<p align="center">
  <img alt="python" src="https://img.shields.io/badge/python-3%20·%20stdlib%20only-55F5A0?style=flat-square">
  <img alt="license" src="https://img.shields.io/badge/license-MIT-55F5A0?style=flat-square">
  <img alt="inputs" src="https://img.shields.io/badge/reads-SWIVEL%20·%20Kismet%20·%20WigleCSV-4DA6FF?style=flat-square">
  <img alt="offline" src="https://img.shields.io/badge/runs-offline-4DA6FF?style=flat-square">
  <img alt="accounts" src="https://img.shields.io/badge/accounts-none-4DA6FF?style=flat-square">
  <img alt="tests" src="https://img.shields.io/badge/tests-131%20passing-55F5A0?style=flat-square">
</p>

---

## 🧩 How the pieces fit — in plain English

Three parts, one picture:

- **SWIVEL** (the phone app) hears the Bluetooth and Wi-Fi right around you as you go about your day, and writes it all down.
- **Kismet** (optional, on a laptop) hears *more* Wi-Fi, from farther off — a second set of ears.
- **DEBRIEF** (this tool) pours both logs into **one database**, matches up anything that *both* heard, and keeps a **running history across every outing** — so it can answer the one question that matters: **what keeps showing up wherever you go?**

You don't need Kismet to start — your phone alone is plenty. Kismet just makes the picture sharper.

---

## 👣 See what's been following you

Every AirTag, Tile, car hotspot and Bluetooth gadget near you is **broadcasting all the time.** Run [SWIVEL](https://github.com/officialtomblack/SWIVEL) on your phone (and Kismet on a laptop, if you have one) and you've got a log of everything that was around you — every place you went.

DEBRIEF reads those logs and asks the question that matters: **did the same device turn up in more than one place?** Your neighbour's router stays put. A tracker slipped into your bag doesn't.

<p align="center">
  <img src="docs/assets/debrief-following.svg" alt="One morning, three stops: a Find My tag appears at every stop and a car hotspot at two; DEBRIEF flags both as followed while everything else stays unflagged" width="100%">
</p>

- 🏷️ **Trackers, called out by name.** Apple **Find My** (AirTags and Find My accessories) and **Tile** are recognised from their Bluetooth adverts — even when the address is randomized.
- 📍 **"Followed" flag.** A device is flagged when the **same address shows up at two or more places more than 200 m apart, over more than 5 minutes.** All three numbers are yours to tune (`--follow-distance`, `--follow-min-span`, `--cluster-distance`).
- 🗓️ **Regulars.** `run` keeps adding every capture you feed it to one database, so you can ask which devices turned up on **more than one day** — a gadget that's there on Monday *and* Thursday is worth a second look.
- 🧾 **Receipts for every flag.** Click any device in the report and DEBRIEF shows *why*: how many places, how many sightings, and the exact rule that fired.

> **Read the flag, not your fears.** "Followed" means *this device's address appeared at several of your places* — not that a person is tracking you. Your own phone, earbuds and car will be flagged too (they really do go everywhere you go). Trackers rotate their Bluetooth address on a schedule, so a single tag can show up as more than one device across a long day. DEBRIEF marks this signal **low confidence**, on purpose.
>
> **It will cry wolf — by design.** DEBRIEF would rather flag something that turns out to be nothing than stay quiet about a tag in your bag. A false alarm costs you a minute of checking; a missed tracker costs a lot more. If nothing's wrong, even better.

---

## ✨ What else it digs up

| 🎯 | Signal | What DEBRIEF tells you |
|---|---|---|
| 🧲 | **Trackers** | `is_tracker` / `tracker_type`: Find My, Tile — matched by advert signature, never by guessing. |
| 👣 | **Followed** | `followed_flag`: the same device at ≥2 of your places, far apart, over time. |
| 👯 | **Evil-twin hints** | `security_conflict`: a Wi-Fi network seen **open** one moment and **WPA2** the next — a classic fake-hotspot trick. |
| 🚨 | **Kismet IDS alerts** | `kismet_ids_alerts`: deauth floods and other attacks Kismet caught, pinned to the device. |
| 📡 | **Confirmed by two radios** | `seen_by_both_within_window`: the phone *and* Kismet heard it within the same minute — not a glitch. |
| 📷 | **Near a mapped camera** | `near_alpr`: metres to the nearest known ALPR / Flock camera from OpenStreetMap, from your capture's own GPS. |
| 🏭 | **Who made it** | `oui_vendor`, `oui_device_type`, `device_class`, `advertised_services` — vendor and device type, **withheld** whenever the address can't honestly support it. |
| 🔍 | **Fingerprints** | `probed_ssids` (the networks a phone keeps hunting for — near-unique) and `device_cluster_id` (one device across its rotating addresses). |
| 🌐 | **IP addresses** | `observed_ip` from SWIVEL's subnet sweep or Kismet's cleartext traffic — and it always says which. |

Every column is documented in **[docs/FIELD-REFERENCE.md](docs/FIELD-REFERENCE.md)**.

---

## 🚀 Try it in 60 seconds — no capture needed

DEBRIEF ships with a **synthetic demo**: a made-up morning walk across three stops, with a Find My tag and a Tile tagging along, a car hotspot that turns up twice, an evil-twin café network and a Kismet log of the last stop. Every address, name and coordinate in it is invented.

```bash
git clone https://github.com/officialtomblack/DEBRIEF.git && cd DEBRIEF
python3 swivel_enhance.py fetch           # once: download the public reference registries (IEEE, Bluetooth SIG, …)
python3 demo/make_demo.py                 # write the synthetic demo capture
python3 swivel_enhance.py run demo/demo_walk.ndjson demo/demo_office.kismet --db out/demo.db --fresh
python3 swivel_enhance.py report out/demo.db --out out/demo_report.html   # open it in your browser
```

<p align="center">
  <img src="docs/assets/debrief-report.png" alt="The DEBRIEF report on the synthetic demo: the Find My tracker ranked first, flagged followed at 3 places, with its evidence expanded" width="100%">
</p>

The tracker floats to the top, flagged **followed** at **3 places** — and the expanded row shows every field with **where it came from and how sure DEBRIEF is.**

---

## 🛰️ Use it on your own captures

**1. Capture.** Run [SWIVEL](https://github.com/officialtomblack/SWIVEL) while you go about your day. Optional: run Kismet on a laptop at the same time — DEBRIEF merges the two.
**2. Copy the logs into one folder.** From SWIVEL, tap **EXPORT** and copy the session off the phone (`.ndjson`, `.json` or WigleCSV); from Kismet, the `.kismet` file it wrote. Drop them in the same folder.
**3. Fold them in** — the easy way or by hand, below.

### 🔁 Your everyday routine — one command

Grab the starter script **[`debrief-run.sh`](debrief-run.sh)**, open it, and edit the **two path lines** at the top (where you cloned DEBRIEF, and your captures folder). From then on, your whole routine after any outing is:

```bash
./debrief-run.sh          # fold everything new, then open the report
./debrief-run.sh -n       # dry-run: show what it would do, change nothing
```

It folds every new capture in your folder into one database — already-folded files are skipped automatically, so **running it again is always safe** — and opens the ranked report. Drop new files in, run it again, and the picture of *what keeps showing up* gets sharper every outing. (If your phone is plugged in and you built the debug app, it even pulls new sessions off the phone for you; if not, it just folds the folder.)

### Or run it by hand

```bash
python3 swivel_enhance.py run session.ndjson capture.kismet --kismet-window 60
#   -> out/swivel.db, out/swivel_devices.csv, out/swivel_clusters.geojson, out/swivel_summary.txt
python3 swivel_enhance.py report out/swivel.db     # ranked HTML report, no coordinates in it
datasette out/swivel.db -m datasette_metadata.json --static assets:datasette-assets \
  --setting facet_time_limit_ms 3000 --setting sql_time_limit_ms 5000   # optional: browse + map in your browser
```

**`run` accumulates.** Every run adds the new captures to the same database (files already ingested are skipped by content hash) and re-scores everything. `--fresh` starts over.

---

## 🔎 Ask your data anything

The output is one plain SQLite file. Open it with `sqlite3 out/swivel.db` (or `python3 -m sqlite3 out/swivel.db` on Python 3.12+, or browse it in Datasette) and paste:

```sql
-- 👣 Who's following you: devices that turned up at more than one of your places.
-- Leans toward false alarms on purpose — better to check a scare that was nothing than miss a real tag.
SELECT radio, address, coalesce(device_name, tracker_type, oui_vendor) AS what,
       json_array_length(location_clusters) AS places, sessions_seen, last_seen
FROM devices
WHERE (followed_flag = 1                                                 -- the tool's rule: 2+ places >200 m apart, >5 min
       OR (is_tracker = 1 AND json_array_length(location_clusters) >= 2)) -- any tracker at 2+ places, even close together
  -- AND address NOT IN ('AA:BB:CC:DD:EE:FF')                            -- uncomment + fill in to hide your own gear
ORDER BY is_tracker DESC, places DESC, sessions_seen DESC;
```

```sql
-- 🧲 Every tracker, most recent first
SELECT tracker_type, address, sighting_count, sessions_seen, first_seen, last_seen
FROM devices WHERE is_tracker = 1 ORDER BY last_seen DESC;
```

```sql
-- 🗓️ Regulars: devices heard on more than one day (UTC)
SELECT d.radio, d.address, coalesce(d.device_name, d.oui_vendor, d.advertised_company) AS what,
       count(DISTINCT substr(s.ts_utc, 1, 10)) AS days
FROM devices d JOIN sightings s ON s.address = d.address AND s.radio = d.radio
GROUP BY d.radio, d.address HAVING days >= 2 ORDER BY days DESC;
```

```sql
-- 👯 Evil-twin hints: networks seen both open and secured
SELECT address, device_name, security_modes FROM devices WHERE security_conflict = 1;
```

```sql
-- 📷 Devices you heard within 150 m of a mapped ALPR camera (run `fetch --alpr-bbox S,W,N,E` first)
SELECT address, coalesce(device_name, oui_vendor) AS what, near_alpr AS metres_to_camera
FROM devices WHERE near_alpr <= 150 ORDER BY near_alpr;
```

---

## 🧭 How it works

<p align="center">
  <img src="docs/assets/debrief-how-it-works.svg" alt="SWIVEL phone logs, Kismet captures and WigleCSV go into DEBRIEF, which merges, enriches offline, scores and audits, producing a SQLite database, CSV, GeoJSON map and HTML report" width="100%">
</p>

1. **Merge.** The same MAC heard by the phone and by Kismet becomes **one device**, with every raw sighting kept underneath it.
2. **Enrich — offline.** Vendors, device types, Bluetooth services and tracker signatures come from public registries you download **once** (`fetch`). No lookups while it runs.
3. **Score and flag.** Places, "followed", trackers, evil-twin hints, two-radio confirmation, camera proximity — then an `info_score` so the richest devices rise to the top. Empty rotating-address noise is set aside (never deleted).
4. **Audit itself.** Every run re-checks its own hard rule and **exits with an error** if it ever broke it.

Deep dive: **[docs/TECHNICAL.md](docs/TECHNICAL.md)**.

---

## 🎖️ Evidence, not proof

Most tools that "detect" things overpromise. DEBRIEF does the opposite — on purpose.

- **The hard rule:** a randomized or locally-administered address **never gets a vendor.** A random address carries no maker information, so DEBRIEF refuses to invent one. Enforced when each sighting is read, **re-audited on every run**, and pinned by tests (including a check that the tests themselves fail against the old tool).
- **Every enriched field carries its own `_source` and `_confidence`.** A blank means *"not determined"* — never a guess — and the `_source` usually says why (e.g. `withheld:ble_strict`, `no_registry_match`).
- **Nothing is silently dropped.** Raw sightings are immutable (the database blocks edits); duplicates and malformed rows are labelled, not deleted.
- **Your capture files are read-only.** A `.kismet` is opened immutably. Raw in, enriched copy out.

---

## 🔒 Your data stays yours

- 🔌 **Offline by default.** `run` and `report` never touch the network.
- 🙋 **Two lookups, both opt-in.** `wigle` and `beacondb` look up **Wi-Fi access points only** (fixed infrastructure) — never a phone, a Bluetooth device, a randomized address or your GPS. WiGLE also needs your own API token; no token, nothing sent. `--dry-run` tells you how many lookups *would* go out, and sends nothing.
- 🗂️ **Outputs stay local.** Everything lands in `out/`, which git ignores. The HTML report contains **no coordinates at all** — places appear only as a count.
- 🧪 **The demo is fake.** Nothing in this repository came from a real capture.

---

## ✅ Verification status (the honest version)

- ✔️ **131 automated tests pass** (`python3 -m unittest discover -s tests`, last run 2026-11-05) — parsing, merging, every enrichment, the followed/cluster logic, the report, and the hard-rule regression.
- ✔️ **Used on real captures:** 11 capture files, 221,539 sightings, 21,338 devices — **0** randomized addresses given a vendor.
- ✔️ **The demo reproduces the screenshot above:** 2 trackers, 3 followed devices, 12 two-radio confirmations, 1 evil-twin hint, 1 IDS alert.
- ⏳ **Not yet field-verified:** the "followed" flag against a real planted tracker over a full day; `device_cluster_id` needs Kismet probe data, which most captures don't have.

---

## 🧰 Requirements

- **Python 3** (developed on 3.12) — standard library only. PyYAML from your system packages for the Bluetooth SIG files.
- **Optional:** [Datasette](https://datasette.io) to browse the database with a map; Kismet for the second radio.

---

## 📜 Part of the SWIVEL family

**[SWIVEL](https://github.com/officialtomblack/SWIVEL)** hears it. **DEBRIEF** tells you what it meant.

Maintained by [**@officialtomblack**](https://github.com/officialtomblack) — questions or bug reports: [theredwake.sh@protonmail.com](mailto:theredwake.sh@protonmail.com). Licensed under the **MIT License** — see [LICENSE](LICENSE).

For **authorized, personal** security research. DEBRIEF describes **devices, not people.**

<p align="center"><sub>DEBRIEF reads the airwaves you already captured. It never transmits. Your data never leaves your hands.</sub></p>
