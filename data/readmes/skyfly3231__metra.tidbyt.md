# Metra Departure Board (Tidbyt)

A compact 64x32 [Pixlet](https://github.com/tidbyt/pixlet) app for Tidbyt
showing the next several Metra trains for one line, station, and direction.
A GitHub Action fetches live data and pushes an updated render to your
device on a schedule, so it stays current without your machine running.

```
[■] UP-NW      IRVING P
 6m   5:42pm      OK
31m   6:07pm     +5m
66m   6:42pm      OK
```

## How it's structured

- **`app/metra_board.star`** -- the Pixlet app. Pure display logic; it
  never talks to the network itself. Without live data it falls back to
  realistic demo values, so it always renders something sensible on its own.
- **`scripts/fetch_metra.py`** -- fetches Metra's GTFS-Realtime feed and
  writes a small `config.json` of plain values (`train_0_time`,
  `train_0_wait`, `train_0_status`, ...) that get passed into the Pixlet
  app. This is Python, not Starlark, on purpose: Pixlet's Starlark runtime
  has no protobuf module and its HTTP client isn't built for raw binary, so
  decoding Metra's protobuf feed reliably from inside the `.star` file
  isn't practical. Python (with Google's official bindings) does the
  decode; Pixlet just renders the results.
- **`scripts/render_preview.py`** -- renders the app with the real
  `pixlet` binary and generates `preview/preview.html`, a browser preview
  that draws the actual output as round LEDs (closer to what the physical
  display looks like) instead of square image pixels.
- **`.github/workflows/sync.yml`** -- runs on a schedule, fetches fresh
  Metra data, renders the app, and pushes it to your Tidbyt.

## One-time setup

### 1. Get a Metra API token
Apply at [metra.com/developers](https://metra.com/developers) (approval is
typically ~1 business day). You'll get either an `api_token`, or a
username/password pair -- `scripts/fetch_metra.py` supports both; check
which one your approval email gives you.

### 2. Find your station's `stop_id` and your line's `route_id`
These come from Metra's static GTFS schedule
(`https://metra.com/metra-gtfs-api` links to the current `schedule.zip`).
Unzip it and look in `stops.txt` for your station's `stop_id`, and
`routes.txt` for your line's `route_id` (e.g. `UP-NW`, `BNSF`, `MD-N`).
I couldn't confirm exact values for your specific station from here, so
this lookup is on you -- but it's a five-minute CSV skim.

### 3. Get a Tidbyt API token and device ID
In the Tidbyt mobile app: **Settings → Get API Key** for the token, and
your device ID is visible on the same device settings screen.

### 4. Configure the repo
Go to your repo's **Settings → Secrets and variables → Actions**.

Add as **secrets** (sensitive):
| Name | Value |
|---|---|
| `METRA_API_TOKEN` | your Metra token (if you got one) |
| `METRA_API_USER` / `METRA_API_PASS` | your Metra username/password (if you got those instead) |
| `TIDBYT_API_TOKEN` | your Tidbyt API token |
| `TIDBYT_DEVICE_ID` | your Tidbyt device ID |

Add as **variables** (not sensitive, easy to tweak). Values below are set up
for the Rock Island Line, 99th St (Beverly Branch) inbound to LaSalle St:
| Name | Value |
|---|---|
| `METRA_ROUTE_ID` | `RI` |
| `METRA_STOP_ID` | *(confirm from `stops.txt` -- Metra's site uses `99TH-BEV` for this station, but check the actual GTFS stop_id before trusting it)* |
| `METRA_DIRECTION_ID` | `1` (try this first; if the trains that come back look like outbound/evening instead of inbound/morning, switch to `0` -- GTFS direction_id isn't documented by Metra) |
| `METRA_MAX_TRAINS` | `3` |
| `METRA_TIMEZONE` | `America/Chicago` |
| `METRA_LINE_NAME` | `RI` |
| `METRA_LINE_COLOR` | `#CC0000` (Metra's "Rocket Red" for Rock Island) |
| `METRA_STATION_NAME` | `99th St` |
| `METRA_DESTINATION_LABEL` | `LaSalle St` |

### 5. Run it
The workflow runs daily at 11:00 UTC by default (see the commented
alternative cron in `sync.yml` for a tighter commute-hours schedule). You
can also trigger it manually from the **Actions** tab with "Run workflow".

## Previewing changes before you push

```bash
python3 scripts/render_preview.py app/metra_board.star --out preview/preview.html
open preview/preview.html   # or just open the file in a browser
```

This uses the real demo data baked into the app by default. To preview
specific values (e.g. to check how a long delay looks), pass config
key=value pairs the same way `pixlet render` accepts them:

```bash
python3 scripts/render_preview.py app/metra_board.star \
  train_count=2 train_0_time=5:42pm train_0_wait=1m train_0_status=+12m \
  --out preview/preview.html
```

## Testing with real data locally

```bash
export METRA_API_TOKEN=xxxx   # or METRA_API_USER / METRA_API_PASS
export METRA_STOP_ID=99TH-BEV   # confirm against stops.txt first
export METRA_ROUTE_ID=RI
export METRA_DIRECTION_ID=1
python3 scripts/fetch_metra.py
cat config.json
```

## Known unknowns

A few things depend on your specific Metra credentials and station, which
I had no way to verify without a live token:
- Whether your approval gives you an `api_token` or a username/password pair.
- The exact `tripUpdates` endpoint path -- `scripts/fetch_metra.py` uses
  the one documented at metra.com/metra-gtfs-api; double check against
  whatever reference your approval email links to.
- Which `direction_id` (0 or 1) matches your commute direction.

If any of these are off, `fetch_metra.py` prints the error it hit and the
app falls back to demo data rather than pushing a broken render.
