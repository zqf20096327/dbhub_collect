# Texins Flying Club — Tidbyt Flight Tracker

🌐 **Live Web Dashboard & Virtual Tidbyt:** [**https://houston88.github.io/tidbyt-housty-flight-tracker/**](https://houston88.github.io/tidbyt-housty-flight-tracker/)

Tracks the four Texins Flying Club aircraft out of McKinney National Airport (`KTKI`) using the FlightAware AeroAPI v4:

| N-Number | Aircraft Type | Real Livery Scheme | Primary Accent |
| :--- | :--- | :--- | :--- |
| **`N121DB`** | 1972 Piper Arrow II | White upper, Royal Cobalt Blue swept tail & belly, Gold swoop | Royal Blue (`#3b82f6`) |
| **`N3QZ`** | 1973 Cessna 182P Skylane | White fuselage, Scarlet Red wingtip, stripe & tail bars, Navy nose | Scarlet Red (`#ef5350`) |
| **`N4135W`** | 1999 Piper Archer III | Crisp White upper cabin & mid-tail, Deep Blue lower fuselage & upper tail | Aviation Blue (`#60a5fa`) |
| **`N6833C`** | 1965 Piper Cherokee 180 | Crisp White fuselage & tail with Navy Blue cap/belly & Silver pin-striping | Ice Silver (`#cbd5e1`) |

## Previews

| Airborne Live Telemetry View | 4-Plane Parked Status Board |
| :---: | :---: |
| ![Airborne View](preview_airborne.gif) | ![Parked Status Board](preview_live_board.gif) |
| *Displayed automatically when any club aircraft is airborne (shows route, times, speed/heading, altitude, and nearest city).* | *Displayed when all four aircraft are on the ground, with scrolling route/time/location summaries for each plane.* |

## Features
- **Custom Pixel-Art Silhouettes**: Distinct side-profile sprites for each aircraft type (16×8 for the airborne detail card and 10×6 mini icons for the 4-plane status board).
- **Smart Display Modes**:
  - **`auto` (Default)**: Prioritizes actively airborne aircraft with a full 64×32 live telemetry card (3-letter `FROM->TO` route, local departure & arrival times, groundspeed in knots + compass heading, altitude, and nearest city). When all 4 aircraft are parked, displays a compact 4-plane status board.
  - **`board`**: Always displays the 4-plane compact status board.
  - **`cycle`**: Cycles full-screen detail cards for all 4 aircraft.
  - **`demo`**: Renders a simulated airborne flight (`N121DB` en route `TKI -> ADS`) for previewing without using API credits.
- **API Key Configuration**:
  - Stored locally in `.env` (`FLIGHTAWARE_API_KEY=...`, gitignored).
  - Exposed as an in-app Tidbyt setting (`api_key`) via `get_schema()`.

## Usage (`pixlet v0.34.0`)

### 1. Render with `.env` API Key
```bash
make render
# or directly:
source .env && pixlet render texins_flights.star api_key="$FLIGHTAWARE_API_KEY"
```

### 2. Interactive Browser Preview & In-App Settings (`pixlet serve`)
```bash
make serve
# Opens http://127.0.0.1:8080 where you can paste your AeroAPI key and switch Display Modes
```

### 3. Render Magnified Animated GIF Previews
```bash
make demo
make cycle
```

## Running on Your Home Tidbyt

Tidbyt devices display pre-rendered WebP graphics pushed via the Tidbyt Cloud API. Because flight status updates dynamically, you render the applet with your AeroAPI key and push the rendered WebP to your Tidbyt.

### Step 1: Retrieve Your Tidbyt Credentials
From the **Tidbyt Mobile App**:
1. **Device ID**: Tap **Settings** (gear icon) -> Select your device -> tap **Device Settings** / **Get Device ID** (e.g. `humble-porcupine-4829`).
2. **API Key**: Tap **Settings** -> **General** (or Developer/Account) -> **Get API Key** (or create a token).

### Step 2: Add Credentials to `.env`
Add the following to your local `.env` file (which is gitignored):
```bash
FLIGHTAWARE_API_KEY=your_flightaware_key
TIDBYT_DEVICE_ID=your_device_id
TIDBYT_API_KEY=your_tidbyt_api_key
```

### Step 3: Push to Your Tidbyt

```bash
# Push and display immediately on your screen:
make push

# Or push silently to your normal app rotation:
make push-bg
```

### Step 4: Automating Regular Updates

To keep flight telemetry fresh throughout the day:

#### Option A: GitHub Actions + Live GitHub Pages Dashboard (Cloud — Hourly 7 AM to 9 PM CT)
This repository includes [`.github/workflows/update-tidbyt.yml`](.github/workflows/update-tidbyt.yml), which runs every hour between **7:00 AM and 9:00 PM Central Time** (`America/Chicago`) and stays off overnight.

To prevent duplicate API charges, each hourly run calls [`scripts/fetch_fleet_status.py`](scripts/fetch_fleet_status.py) **once**, and reuses that single snapshot (`fleet_b64`) to:
1. Render and push `texins_flights.webp` to your physical Tidbyt (`pixlet push -b`).
2. Render lightweight 64×32 `.webp` animations (`live.webp`, `board.webp`, `cycle.webp`, `demo.webp`) scaled up sharply in the browser via CSS `image-rendering: pixelated` with **zero extra FlightAware API calls**.
3. Publish the hybrid web dashboard ([`site/index.html`](site/index.html) + `fleet_status.json` + `.webp` files) to **GitHub Pages** (`https://houston88.github.io/tidbyt-housty-flight-tracker/`).

To enable GitHub Pages on your repo:
1. Go to your repository on GitHub -> **Settings** -> **Pages**.
2. Under **Build and deployment -> Source**, select **GitHub Actions**.
3. Ensure your three secrets (`FLIGHTAWARE_API_KEY`, `TIDBYT_DEVICE_ID`, `TIDBYT_API_KEY`) are set under **Settings -> Secrets and variables -> Actions**.

#### Option B: Local Cron Job (Linux / macOS / Raspberry Pi)
Add a crontab entry (`crontab -e`) to update every hour from 7 AM to 9 PM:
```bash
0 7-21 * * * cd /home/houston/repos/tidybit-housty-flight-tracker && make push-bg > /dev/null 2>&1
```

#### Option C: Background Loop Script
Run a simple background loop while your machine is on:
```bash
while true; do
  make push-bg
  sleep 3600  # wait 1 hour
done
```

