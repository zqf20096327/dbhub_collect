# Tidbyt CISA KEV Alert Ticker 🛡️

**Author:** Rosie Domenech  
**Date:** April 2026  
**Description:** Shows the top 3 most recent CISA Known Exploited Vulnerabilities (KEV) simultaneously on your Tidbyt 64x32 LED display. Each CVE scrolls in its own color-coded row. Updates every hour from the official CISA KEV catalog.

---

## Preview

![CISA KEV Preview](cisakev.gif)

---

## Features

- 🛡️ **Live data** from the official CISA KEV catalog
- 📋 **3 simultaneous rows** — CVE ID, vendor, product, patch deadline
- 🔴 **Red** = known ransomware campaign use
- 🟡 **Yellow / Cyan / White** = standard KEV entries
- 💀 **Ransomware-only toggle** — filter to show only ransomware-linked CVEs
- 🔄 Updates every hour
- No API key required

---

## Setup

```bash
git clone https://github.com/RosieDomenech/tidbyt-cisa-kev.git
cd tidbyt-cisa-kev
pixlet serve cisakev.star
```

### Push to Tidbyt
```bash
pixlet render cisakev.star
pixlet push \
  --api-token YOUR_API_TOKEN \
  --installation-id cisakev \
  YOUR_DEVICE_ID \
  cisakev.webp
```

---

## Color Coding

| Color | Meaning |
|---|---|
| 🔴 Red header + rows | Known ransomware campaign use |
| 🟡 Yellow | Row 1 — most recent KEV |
| 🔵 Cyan | Row 2 |
| ⬜ White | Row 3 |

---

## Data Source

Official [CISA KEV Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) — updated regularly by CISA with vulnerabilities that are actively being exploited in the wild.
