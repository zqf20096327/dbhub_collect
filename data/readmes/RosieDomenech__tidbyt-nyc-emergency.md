# Tidbyt NYC Emergency Alerts 🚨

**Author:** Rosie Domenech  
**Date:** April 2026  
**Description:** Live NYC emergency alert ticker for your Tidbyt 64x32 LED display. Pulls real-time notifications from the official NYC Open Data Notify NYC API — updated every 5 minutes.

---

## Preview

![NYC Emergency Alerts Preview](nycalerts.gif)

---

## Features

- 🚨 **Live Notify NYC data** — official NYC Open Data API
- 🔄 **Updates every 5 minutes**
- 🎨 **Color coded by type:**
  - 🔴 Red — Emergency Activity
  - 🟠 Orange — Public Health
  - 🟡 Yellow — Transportation
  - 🔵 Cyan — Planned Events
  - 🟢 Green — All Clear
- 🗂️ **Filterable** by alert category
- 📋 Shows 3, 5, or 10 alerts

---

## Data Source

Live alerts from [NYC Open Data — Notify NYC](https://data.cityofnewyork.us/resource/8vv7-7wx3.json) — the official NYC emergency notification system covering:
- Emergency Activity (NYPD, FDNY, OEM)
- Public Health alerts
- Transportation disruptions
- Planned events affecting the public
- Weather emergencies

---

## Setup

```bash
git clone https://github.com/RosieDomenech/tidbyt-nyc-emergency.git
cd tidbyt-nyc-emergency
pixlet serve nycalerts.star
```

### Push to your Tidbyt
```bash
pixlet render nycalerts.star
pixlet push \
  --api-token YOUR_API_TOKEN \
  --installation-id nyc-emergency \
  YOUR_DEVICE_ID \
  nycalerts.webp
```
