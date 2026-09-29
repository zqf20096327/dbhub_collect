# Tidbyt NYC Emergency Alerts 🚨

**Author:** Rosie Domenech  
**Date:** April 2026  
**Description:** Live NYC emergency alerts from the official Notify NYC system scrolling on your Tidbyt 64x32 LED display. Updates every 5 minutes.

---

## Preview

![NYC Alerts Preview](nycalerts.gif)

---

## Features

- 🚨 **Live alerts** from the official Notify NYC / Everbridge RSS feed
- 🇬🇧 **English only** — filters out multilingual duplicates automatically
- 🎨 **Color coded by category:**
  - 🟠 Orange: Infrastructure (gas, water, power)
  - 🟡 Yellow: Traffic disruptions
  - 🔵 Blue: MTA / Transit
  - 🔴 Red: Emergency / Safety
  - 🟢 Green: Public health / All clear
- 📋 Cycles through multiple alerts (3, 5, or 8)
- ⏱️ Refreshes every 5 minutes
- No API key required

---

## Alert Types Covered

- 🔥 Fires and emergencies
- 🚇 MTA subway and bus disruptions
- 🚗 Major traffic incidents and road closures
- ⚡ Power outages (Con Edison)
- 💧 Water condition alerts
- 🌪️ Weather emergencies
- 🔍 Silver Alerts / missing persons
- 🏗️ Planned infrastructure work

---

## Setup

```bash
git clone https://github.com/RosieDomenech/tidbyt-nyc-alerts.git
cd tidbyt-nyc-alerts
pixlet serve nycalerts.star
```

### Push to Tidbyt
```bash
pixlet render nycalerts.star
pixlet push \
  --api-token YOUR_API_TOKEN \
  --installation-id nycalerts \
  YOUR_DEVICE_ID \
  nycalerts.webp
```

---

## Data Source

Official [Notify NYC](https://a858-nycnotify.nyc.gov/notifynyc/) emergency alerts via the [Everbridge RSS feed](https://feeds.everbridge.net/feeds/453003085617722/rss/rss.xml). Updated in real time by NYC Emergency Management (NYCEM).
