# Tidbyt GitHub Status

A Tidbyt app that displays real-time GitHub operational status. Shows color-coded status with component-level detail.

> **Screenshot placeholder:** Preview the app locally with `pixlet serve github_status.star`.

## Features

- Real-time GitHub status from the [githubstatus.com API](https://www.githubstatus.com/api)
- Color-coded display for status at a glance: green / yellow / red
- Component-level outage details with a scrolling marquee
- Active incident display
- 60-second cache for API efficiency

## Prerequisites

- macOS, Linux, or Windows
- Pixlet CLI (`brew install tidbyt/tidbyt/pixlet`)
- A Tidbyt device (optional for pushing; not required for local preview)

## Quick Start

```sh
# Local preview
pixlet serve github_status.star
# Then open http://localhost:8080

# Render to image
pixlet render github_status.star

# Push to device
pixlet push --api-token YOUR_TOKEN YOUR_DEVICE_ID github_status.webp
```

## Using run.sh

Use the helper script for common preview and deployment workflows:

- `./run.sh --serve` for local preview
- `./run.sh -d DEVICE_ID -t TOKEN` for a one-time push
- `./run.sh -d DEVICE_ID -t TOKEN --loop 60` for continuous updates
- Environment variables: `TIDBYT_DEVICE_ID`, `TIDBYT_API_TOKEN`

## Docker

Run as a container on any machine — no Pixlet install needed on the host.

```sh
# 1. Copy and fill in your credentials
cp .env.example .env
# Edit .env with your TIDBYT_DEVICE_ID and TIDBYT_API_TOKEN

# 2. Build and run
docker compose up -d

# View logs
docker compose logs -f

# Stop
docker compose down
```

You can get your device ID and API token from the Tidbyt mobile app under Settings → General → Get API key.

## How It Works

The app fetches live operational data from the GitHub Status API at `githubstatus.com`. It maps the current overall status into clear visual colors:

- **Green** for normal operation
- **Yellow** for degraded performance or partial disruption
- **Red** for major outages or critical incidents

The display presents the current GitHub status first, then highlights affected components and active incidents. When outage details are longer than the available screen space, they scroll in a marquee so the full message remains readable on the Tidbyt display.

To reduce unnecessary API requests, responses are cached for 60 seconds before refreshing.

## Note on Audio Alerts

Tidbyt Gen 2 includes a speaker, but there is currently no public API for custom apps to play sounds. Audio alert support will be added when the API becomes available.

## API Reference

GitHub Status API: https://www.githubstatus.com/api

## License

MIT
