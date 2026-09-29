# Tidbyt Hourly Weather

A sleek hourly weather forecast display for Tidbyt devices with smooth temperature curves and color-coded visualization.

## Features

- **12-hour temperature graph** with cubic spline interpolation for smooth curves
- **Color-coded temperature bars** from blue (cold) to orange (hot)
- **Current temperature** display with daily high/low range
- **Scrolling detailed forecast** at the bottom
- **Smart caching** (10 minutes) to minimize API calls

## Quick Start

### 1. Install Pixlet

**macOS:**
```bash
brew install tidbyt/tidbyt/pixlet
```

**Linux:**
```bash
wget https://github.com/tidbyt/pixlet/releases/download/v0.17.0/pixlet_0.17.0_linux_amd64.tar.gz
tar -xzf pixlet_0.17.0_linux_amd64.tar.gz
sudo apt install libwebp-dev  # Ubuntu/Debian
```

### 2. Configure Your Location

Currently set for Seattle. To change:

1. Get your city's lat/lon coordinates
2. Visit: `https://api.weather.gov/points/LAT,LON`
3. Copy the `forecastHourly` URL from the response
4. Update `HOURLY_WEATHER_URL` in `weather.star`

### 3. Deploy

```bash
# Login and get device ID
pixlet login
pixlet devices

# Test locally (optional)
pixlet serve weather.star

# Deploy to device
pixlet render weather.star
pixlet push <device-id> --installation-id "Weather" weather.webp
```

## Files

- `weather.star` - Main Tidbyt app (Starlark)
- `weather.py` - API testing helper

## Data Source

Uses the free National Weather Service API (US only, no API key required).

## Temperature Colors

- Blue (≤0°C) → Gray → Green (mild) → Orange/Red (≥30°C)
- Bars scaled relative to daily temperature range