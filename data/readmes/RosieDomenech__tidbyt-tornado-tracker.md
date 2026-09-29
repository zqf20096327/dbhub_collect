# Tidbyt Tornado Tracker 🌪️

**Author:** Rosie Domenech  
**Date:** April 2026  
**Description:** Live US tornado warning and watch tracker for Tidbyt. Cycles between a pixel-art US map showing affected states and a scrolling ticker of active alerts. Powered by the official NOAA/NWS API — no API key required.

---

## Preview

![Tornado Tracker Preview](tornado.gif)

---

## Features

- 🗺️ **US Map** — all 48 continental states plotted as pixel dots
- 🔴 **Red dots** = active Tornado Warning
- 🟡 **Yellow dots** = active Tornado Watch  
- ⚫ **Gray dots** = no active alerts
- ✅ **ALL CLEAR** when no alerts are active
- 📡 **Live NOAA/NWS data** refreshed every 5 minutes
- 📜 **Scrolling ticker** cycling through all affected areas

---

## Setup

```bash
git clone https://github.com/RosieDomenech/tidbyt-tornado-tracker.git
cd tidbyt-tornado-tracker
pixlet serve tornado.star
```

### Push to Tidbyt
```bash
pixlet render tornado.star
pixlet push \
  --api-token YOUR_API_TOKEN \
  --installation-id tornado-tracker \
  YOUR_DEVICE_ID \
  tornado.webp
```

---

## Data Source

Live alerts from the [NOAA/NWS Alerts API](https://api.weather.gov/alerts/active), filtered for Tornado Warnings and Tornado Watches. Updates every 5 minutes.

---

## Legend

| Color | Meaning |
|---|---|
| 🔴 Red | Tornado Warning (imminent threat) |
| 🟡 Yellow | Tornado Watch (conditions favorable) |
| ⚫ Gray | No active alerts |
