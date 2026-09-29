# TeslaTidbyt

Displays a live overview of your Tesla fleet on one or more [Tidbyt](https://tidbyt.com) devices.

For each tracked vehicle it shows:
- A car silhouette (Model 3 or Model X shape) in the vehicle's paint colour
- Distance from home in km
- Battery level bar (turns orange below 30%)
- A lightning bolt when charging

## How it works

The script fetches vehicle data from a running instance of [Tesla-Fleet-Collector](https://github.com/WietseWind/Tesla-Fleet-Collector), renders a 64×32 pixel GIF using `sharp`, and pushes it to your Tidbyt device(s) via the Tidbyt API.

## Requirements

- [Bun](https://bun.sh) runtime
- A running [Tesla-Fleet-Collector](https://github.com/WietseWind/Tesla-Fleet-Collector) instance reachable over HTTP — this is your data source. You'll need to set up and host that yourself; it exposes a `/vehicles` endpoint with pre-computed data including battery level, charge state, distance from home, and paint colour.
- One or more Tidbyt devices with their API keys

## Setup

1. Install dependencies:
   ```sh
   bun install
   ```

2. Copy the sample config and fill in your values:
   ```sh
   cp config.sample.json config.json
   ```

3. Edit `config.json`:
   ```json
   {
     "base_url": "https://your-fleet-collector.example.com",
     "vehicles_url": "https://your-fleet-collector.example.com/vehicles",
     "wanted": ["Alice", "Bob"],
     "tidbyts": [
       {
         "device": "your-tidbyt-device-id",
         "apikey": "your-tidbyt-api-key"
       }
     ]
   }
   ```

   - **`base_url`** — base URL of your Tesla-Fleet-Collector instance
   - **`vehicles_url`** — full URL to the `/vehicles` endpoint (typically `base_url + /vehicles`)
   - **`wanted`** — list of vehicle names (matching the `name` field returned by the collector) to display
   - **`tidbyts`** — array of Tidbyt devices to push to; add as many as you like

4. Run:
   ```sh
   bun index.mjs
   ```

   Set up a cron job to refresh on an interval, e.g. every minute.

## Notes

- `config.json` is gitignored — never commit it.
- Vehicle colours are taken from the `skin_color` field returned by the collector and brightened for visibility on the black Tidbyt display.
- Model X vehicles (type `100d`) use a slightly larger silhouette than the default Model 3 shape.
