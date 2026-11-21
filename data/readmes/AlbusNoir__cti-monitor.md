# CTI Monitor

A lightweight, automated Cyber Threat Intelligence (CTI) collector and Discord push-notification ticker built with Python, `uv`, SQLite, and Apprise. It polls ~60 structured vulnerability feeds, ransomware leak trackers, vendor PSIRTs, threat research blogs, government CERTs, and breaking security news, enriches headlines with CISA KEV and FIRST EPSS data, deduplicates overlapping coverage, tracks meaningful article updates, and routes alerts into dedicated Discord channels.

## How It Works

1. **Source Ingestion (`feeds.json`):** Polls curated RSS, Atom, and JSON endpoints using `curl_cffi` (Chrome TLS impersonation) and `feedparser` with per-source timeouts and category routing.
2. **Two-Tier Deduplication & Update Tracking (`cti_monitor.db`):**
   * **Exact Item & Update Tracking (`seen_items`):** Stores every seen item ID, its latest title, and escalation state in SQLite. Trivial CMS edits are ignored, while meaningful headline changes (`< 85%` similarity or a newly added `CVE-YYYY-NNNN`) trigger a `🔄 [Updated]` alert.
   * **Channel-Scoped Headline Deduplication (`posted_headlines`):** Normalizes titles and extracts CVEs/tokens over a rolling 36-hour window per channel. If multiple news outlets report the exact same story in `#firehose`, only the first headline posts while primary-source advisories in `#vendor-psirts-vulns` or `#active-exploitation` still post normally.
3. **CVE Enrichment (`kev_cache.json` + FIRST EPSS):** Automatically extracts `CVE-YYYY-NNNN` identifiers from incoming headlines, cross-references them against a locally cached copy of the CISA Known Exploited Vulnerabilities (KEV) catalog, and queries the FIRST EPSS API for exploitation probability scores.
4. **Dynamic Keyword & Late Escalation Routing (`keywords.json`):** Evaluates headlines against active-exploitation keywords, retrospective exclusion rules (`ignore_escalation_keywords`), vendor watchlists, KEV matches, and EPSS thresholds. High-priority matches, including previously seen articles whose CVE is later added to CISA KEV or updated to confirm active exploitation, are cross-posted once to `#active-exploitation`.
5. **Notification Delivery (`webhooks.json` + Apprise):** Formats clean, embed-suppressed Markdown links (`<URL>`) and delivers them to Discord (or any Apprise-supported provider).
6. **Health Monitoring (`#bot-status`):** Tracks per-feed HTTP status, consecutive failures, and recovery events in SQLite, alerting after 3 consecutive failures and generating a daily health digest.

## Repository Structure

* `cti_monitor.py` - Main collector, enrichment engine, deduplicator, update tracker, and health reporter.
* `feeds.json` - Master registry of intelligence sources, categories, and target channels.
* `keywords.json` - Dynamic keyword escalation rules, ignore filters, vendor watchlists, and EPSS thresholds.
* `webhooks.example.json` - Template for configuring Apprise notification URLs.
* `webhooks.json` - Live Apprise notification URLs *(ignored by Git)*.
* `cti_monitor.db` - Local SQLite deduplication, update state, and feed health database *(ignored by Git)*.
* `kev_cache.json` - Local cache of CISA KEV CVE IDs *(ignored by Git)*.

## Setup Guide (Ubuntu 24.04 LTS)

> **Platform Note:** These instructions target **Ubuntu 24.04 LTS** (x86_64 or ARM64). On RHEL/Rocky/Oracle Linux, replace `apt` commands with `dnf` equivalents.

### 1. Install `uv` and Sync Dependencies
Install `uv` into your user profile using the official standalone installer, then clone the repository and sync the isolated virtual environment:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.local/bin/env
git clone <your-repo-url> ~/cti-monitor
cd ~/cti-monitor
uv sync
```

### 2. Configure Webhooks (`webhooks.json`)
Copy the example template to `webhooks.json`, replace the placeholders with your Discord webhook credentials formatted for Apprise (`discord://WebhookID/WebhookToken`), and lock down file permissions:

```bash
cp webhooks.example.json webhooks.json
chmod 600 webhooks.json
nano webhooks.json
```

### 3. Seed the Database (`--init`)
Run an initial seed pass so existing articles are recorded in SQLite without flooding your Discord channels, then verify feed health:

```bash
uv run cti_monitor.py --init
uv run cti_monitor.py --health-report
```

### 4. Schedule with Cron
Verify your `uv` binary path (`which uv`), then add two entries via `crontab -e` to poll every 10 minutes and post a daily health digest at 13:00 UTC (8:00 AM EST):

```cron
*/10 * * * * /home/ubuntu/.local/bin/uv run --project /home/ubuntu/cti-monitor /home/ubuntu/cti-monitor/cti_monitor.py >> /home/ubuntu/cti-monitor/cron.log 2>&1
0 13 * * * /home/ubuntu/.local/bin/uv run --project /home/ubuntu/cti-monitor /home/ubuntu/cti-monitor/cti_monitor.py --health-report >> /home/ubuntu/cti-monitor/cron.log 2>&1
```

## Managing Feeds & Keywords

### Adding or Tuning Feeds (`feeds.json`)
Each object in `feeds.json` follows this schema:
```json
{
  "name": "Example Security Blog",
  "url": "https://example.com",
  "type": "rss",
  "category": "vendor-research",
  "channel": "threat-research",
  "enabled": true
}
```
* **`type`:** Use `"rss"` for standard RSS/Atom feeds or `"cisa_kev"` for the official CISA KEV JSON endpoint.
* **`channel`:** Must match a key defined in `webhooks.json` (`active-exploitation`, `vendor-psirts-vulns`, `threat-research`, `gov-cert-advisories`, or `firehose`).
* **Muting Noisy Feeds:** Set `"enabled": false` to stop polling a source without removing it from the registry.

### Tuning Escalation Rules (`keywords.json`)
`keywords.json` is reloaded dynamically on every run:
* **`escalate_keywords`:** Case-insensitive phrases that cross-post matching headlines into `#active-exploitation`.
* **`ignore_escalation_keywords`:** Prevents retrospective roundups (e.g., `"patch tuesday"`, `"roundup"`, `"webinar"`) from triggering escalation alerts.
* **`watch_vendors` & `escalate_watch_vendors`:** Adds a vendor badge (`🏷️`) to matching posts; set `escalate_watch_vendors` to `true` during active vendor incidents to forward all mentions to `#active-exploitation`.
* **`auto_escalate_kev_cves` & `epss_threshold_percent`:** Automatically badges and escalates headlines mentioning CVEs present in CISA KEV or exceeding your EPSS probability threshold.

## Day-to-Day Operations & Troubleshooting

* **Check Feed Health Manually:** `uv run cti_monitor.py --health-report`
* **Inspect Failing Feeds in SQLite:**
  ```bash
  sqlite3 cti_monitor.db "SELECT source_name, consecutive_failures, last_status, last_error FROM feed_health WHERE consecutive_failures > 0;"
  ```
* **Inspect Suppressed Duplicates:** `grep "\[DEDUPED\]" ~/cti-monitor/cron.log | tail -n 20`
* **Cloudflare / WAF Blocks:** Requests use `curl_cffi` with Chrome TLS fingerprinting. If a site blocks datacenter IP ranges outright, disable it in `feeds.json` or route it via a Google News RSS query (`site:example.com`).
* **Resetting History:** Delete `cti_monitor.db` and re-run `uv run cti_monitor.py --init`.
