# Tidbyt NYC Rentals 🏙️

**Author:** Rosie Domenech  
**Date:** April 2026  
**Description:** Live NYC apartment rental listings pulled from Craigslist RSS, scrolling across your Tidbyt 64x32 LED display. Filter by borough and number of listings.

---

## Preview

![NYC Rentals Preview](nycapts.gif)

---

## Features

- 🏙️ Live listings from Craigslist NYC
- 🗺️ Filter by borough: All NYC, Manhattan, Brooklyn, Queens, Bronx
- 🔄 Refreshes every 30 minutes
- 📋 Shows 3, 5, or 8 listings cycling through
- 🔢 Listing counter (e.g. 2/5)
- No API key required

---

## Setup

```bash
git clone https://github.com/RosieDomenech/tidbyt-nyc-rentals.git
cd tidbyt-nyc-rentals
pixlet serve nycapts.star
```

### Push to Tidbyt
```bash
pixlet render nycapts.star
pixlet push \
  --api-token YOUR_API_TOKEN \
  --installation-id nyc-rentals \
  YOUR_DEVICE_ID \
  nycapts.webp
```

---

## Configuration

| Option | Values | Default |
|---|---|---|
| Borough | All NYC, Manhattan, Brooklyn, Queens, Bronx | All NYC |
| Listings | 3, 5, 8 | 5 |
