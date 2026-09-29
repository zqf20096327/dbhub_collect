# Whoop for Tidbyt

A custom [Tidbyt](https://tidbyt.com) widget that displays your [Whoop](https://www.whoop.com) fitness data with recovery, sleep, and strain rings.

![Tidbyt Display](https://img.shields.io/badge/display-64x32-orange) ![License](https://img.shields.io/badge/license-MIT-green) ![Refresh](https://img.shields.io/badge/refresh-hourly-blue)

## Features

- **Recovery Ring** — Color-coded (green/yellow/red) based on your recovery score
- **Sleep Ring** — Shows sleep performance percentage
- **Strain Ring** — Shows daily strain as a percentage of max (21)
- **Scrolling Stats** — Recovery %, sleep duration, strain score, and HRV
- **Hourly Auto-Refresh** — GitHub Actions workflow refreshes data and pushes to your Tidbyt every hour
- **Auto Token Refresh** — Whoop OAuth tokens are refreshed automatically

## Setup

### Prerequisites

- A [Whoop](https://www.whoop.com) device with active membership
- A [Tidbyt](https://tidbyt.com) (Gen 1 or Gen 2)
- [Pixlet](https://github.com/tidbyt/pixlet) CLI installed (`brew install tidbyt/tidbyt/pixlet`)

### 1. Create a Whoop Developer App

1. Go to [developer.whoop.com](https://developer.whoop.com)
2. Create a team and app
3. Select scopes: `read:recovery`, `read:cycles`, `read:sleep`
4. Set redirect URI to `https://localhost:3000/callback`
5. Note your **Client ID** and **Client Secret**

### 2. Get Your Whoop OAuth Tokens

Run the included OAuth helper:

```bash
python3 oauth_helper.py
```

This opens your browser for Whoop authorization and saves tokens to `.whoop_tokens.json`.

### 3. Get Your Tidbyt Credentials

In the Tidbyt mobile app, go to **Settings > General**:
- Note your **Device ID**
- Tap **Get API Key** for your API token

### 4. Configure GitHub Secrets

Add these secrets to your GitHub repo (Settings > Secrets and variables > Actions):

| Secret | Description |
|---|---|
| `WHOOP_CLIENT_ID` | Your Whoop app Client ID |
| `WHOOP_CLIENT_SECRET` | Your Whoop app Client Secret |
| `WHOOP_REFRESH_TOKEN` | Refresh token from step 2 (auto-updated by workflow) |
| `TIDBYT_DEVICE_ID` | Your Tidbyt Device ID |
| `TIDBYT_API_KEY` | Your Tidbyt API token |
| `GH_PAT` | GitHub Personal Access Token with `repo` scope (needed to update refresh token) |

### 5. Enable the Workflow

The GitHub Actions workflow runs automatically every hour. You can also trigger it manually from the Actions tab.

## Local Development

```bash
# Preview with demo data
pixlet serve whoop.star

# Preview with live data
pixlet render whoop.star auth_token="YOUR_ACCESS_TOKEN"
open whoop.webp

# Push to Tidbyt once
pixlet push --api-token YOUR_TIDBYT_KEY --installation-id whoopTracker YOUR_DEVICE_ID whoop.webp
```

## How It Works

1. **GitHub Actions** runs the workflow every hour
2. The workflow **refreshes the Whoop OAuth token** (tokens expire hourly)
3. **Pixlet renders** the Starlark widget, which fetches recovery/sleep/strain data from the Whoop API
4. The rendered image is **pushed to the Tidbyt** device via the Tidbyt API
5. The new refresh token is **saved back to GitHub Secrets** for the next run

## Widget Layout

```
┌──────────────────────────────────┐
│   (R)      (S)      (D)         │  <- Recovery / Sleep / Strain rings
│   26       76       20          │  <- Values inside rings
│    R        S        D          │  <- Labels
│                                  │
│  26% Recovery  6h54m Sleep ...  │  <- Scrolling marquee
└──────────────────────────────────┘
  64 x 32 pixels
```

## API Limitations

- **No battery level** — The Whoop API does not expose device battery data
- **Read-only** — Only summary metrics are available (no raw sensor data)
- **Rate limits** — 100 requests/minute, 10,000 requests/day

## License

MIT
