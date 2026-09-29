# xsukax X RSS Generator

[![PHP](https://img.shields.io/badge/PHP-8.0%2B-777BB4?logo=php\&logoColor=white)](https://www.php.net/)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite\&logoColor=white)](https://www.sqlite.org/)
[![RSS](https://img.shields.io/badge/RSS-2.0-F26522?logo=rss\&logoColor=white)](https://www.rssboard.org/rss-specification)
[![License](https://img.shields.io/badge/License-GPL--3.0-blue.svg)](LICENSE)
[![Self Hosted](https://img.shields.io/badge/Self--Hosted-Yes-success)](#installation)

A lightweight, self-hosted **RSS 2.0 feed generator for public X (formerly Twitter) profiles**, built entirely as a single PHP application with SQLite caching.

**xsukax X RSS Generator** fetches publicly accessible X profile HTML, extracts posts and media, stores them locally, and exposes the results as standards-compatible RSS feeds that can be consumed by RSS readers, automation platforms, monitoring systems, and other feed-aware applications.

No Composer packages, X API credentials, external database server, or cURL dependency are required.

---

## Table of Contents

* [Overview](#overview)
* [Features](#features)
* [How It Works](#how-it-works)
* [Prerequisites](#prerequisites)
* [Installation](#installation)

  * [Quick Installation](#quick-installation)
  * [Debian / Ubuntu](#debian--ubuntu)
  * [Local Development](#local-development)
* [Configuration](#configuration)
* [Usage](#usage)

  * [Web Interface](#web-interface)
  * [Direct RSS URL](#direct-rss-url)
  * [RSS Reader](#rss-reader)
  * [Manual Cache Refresh](#manual-cache-refresh)
* [Project Structure](#project-structure)
* [Caching and Storage](#caching-and-storage)
* [Production Deployment](#production-deployment)
* [Security](#security)
* [Troubleshooting](#troubleshooting)
* [Limitations](#limitations)
* [Contributing](#contributing)
* [License](#license)
* [Author / Maintainers](#author--maintainers)
* [Contact / Support](#contact--support)
* [Disclaimer](#disclaimer)

---

# Overview

**xsukax X RSS Generator** provides a simple way to follow public X profiles through RSS without requiring access to the official X API.

The application:

1. Accepts an X username.
2. Retrieves the corresponding public X profile page.
3. Parses available posts from the returned HTML.
4. Extracts post text, timestamps, links, and supported images.
5. Stores retrieved data in a local SQLite database.
6. Reuses cached data to reduce unnecessary requests.
7. Generates a valid RSS 2.0 document.
8. Serves the feed through a stable URL suitable for RSS clients.

The project is intentionally designed around **minimal deployment complexity**. The application logic, HTML interface, RSS renderer, caching system, parser, rate limiter, and database initialization all live inside a single `index.php` file.

### Design Goals

The project focuses on:

* Simple self-hosting
* Minimal dependencies
* No official X API requirement
* No API keys or OAuth configuration
* RSS standards compatibility
* Local data caching
* Graceful handling of upstream failures
* Lightweight deployment
* Reasonable security defaults
* Easy maintenance when X markup changes

> [!IMPORTANT]
> This project parses publicly available X HTML rather than using an official API. Changes to X's HTML structure, anti-bot systems, or access policies may temporarily affect feed generation.

---

# Features

## RSS Generation

* Generates standard **RSS 2.0** feeds from public X profiles.
* Supports direct feed URLs.
* Includes standard RSS fields such as:

  * `title`
  * `link`
  * `description`
  * `pubDate`
  * `guid`
* Includes an Atom `rel="self"` link for canonical feed identification.
* Uses `content:encoded` for rich post content.
* Produces plain-text descriptions for compatibility with simpler RSS readers.

## Public X Profile Parsing

* Fetches public X profile HTML directly.
* Does not require:

  * X API credentials
  * API keys
  * OAuth
  * Developer accounts
* Extracts:

  * Post text
  * Post URLs
  * Post IDs
  * Publication timestamps
  * Supported post images
* Handles media-only posts.
* Uses several timestamp detection strategies when necessary.
* Restricts embedded media URLs to supported X image CDN locations.

## Image Support

Post images can be included in generated feeds through `content:encoded`.

Images are rendered responsively to improve compatibility with:

* Desktop RSS readers
* Mobile RSS applications
* Feed aggregators
* Web-based RSS clients

The generator intentionally keeps rich media in a single RSS content field to reduce duplicate image rendering in readers that process multiple RSS content representations.

## SQLite Caching

* Zero-configuration SQLite storage.
* Database schema is created automatically.
* Per-profile cache.
* Default cache lifetime: **300 seconds / 5 minutes**.
* Cached posts remain available when appropriate if a later X refresh fails.
* Automatic post de-duplication.
* Existing cached posts can be refreshed with updated content.
* HTTP validators such as `ETag` and `Last-Modified` are reused when available.

## HTTP Caching

Generated RSS responses support:

* `ETag`
* `If-None-Match`
* HTTP `304 Not Modified`
* `Cache-Control`
* `stale-if-error`

This can significantly reduce bandwidth when RSS readers repeatedly request unchanged feeds.

## Built-In Rate Limiting

Basic request limiting is included to reduce abuse and unnecessary upstream requests.

Default settings:

```text
60 requests / 60 seconds / client IP
```

When the limit is exceeded, the application returns:

```text
HTTP 429 Too Many Requests
```

with an appropriate `Retry-After` response header.

## Web Interface

A lightweight responsive web interface is included.

Users can:

* Enter an X username.
* Choose the maximum number of feed items.
* Open the generated RSS feed.
* Force an immediate cache refresh.
* See refresh success or failure information.

The interface automatically supports browser light and dark color schemes.

## Browser-Friendly XML Handling

The application includes special handling for browsers such as Firefox and Safari, which may otherwise download or delegate RSS documents instead of displaying XML directly.

RSS clients still receive the normal RSS MIME type.

## Security Features

Built-in protections include:

* Strict input validation
* PDO prepared statements
* CSRF protection for GUI actions
* HTTP-only session cookies
* `SameSite=Lax` session cookies
* Content Security Policy
* `X-Frame-Options: DENY`
* `X-Content-Type-Options: nosniff`
* `Referrer-Policy: no-referrer`
* HTML output escaping
* TLS peer verification for upstream HTTPS requests
* Controlled Host header validation
* External entity/network protection during DOM parsing
* Restricted remote image sources
* Error display disabled for RSS output
* SQLite database permissions set to `0600` when possible

---

# How It Works

The basic data flow is:

```text
RSS Reader / Browser
        |
        v
    index.php
        |
        +---- Validate username and feed limit
        |
        +---- Check SQLite cache
        |
        +---- Cache still fresh?
        |          |
        |          +---- Yes --> Use cached posts
        |          |
        |          +---- No
        |                |
        |                v
        |        Fetch public X profile
        |                |
        |                v
        |          Parse profile HTML
        |                |
        |                v
        |        Extract posts and media
        |                |
        |                v
        |          Update SQLite cache
        |
        v
    Generate RSS 2.0
        |
        v
 Browser / RSS Reader
```

No background process or cron job is required.

Feeds are refreshed when requested and the configured cache interval has expired.

---

# Prerequisites

## Required Software

The server must provide:

* **PHP 8.0 or newer**
* **PDO**
* **PDO SQLite (`pdo_sqlite`)**
* **DOM**
* **libxml**
* SQLite support
* HTTPS outbound connectivity to `x.com`
* PHP sessions
* A writable application directory for SQLite database creation

The following PHP configuration must also be enabled:

```ini
allow_url_fopen = On
```

The project deliberately uses PHP's native HTTPS stream wrapper, so **cURL is not required**.

## Recommended Environment

For production deployments:

* PHP 8.1+
* Nginx or Apache
* PHP-FPM
* HTTPS
* Current CA certificates
* A dedicated web-server user
* Proper file permissions

## Verify Requirements

Check your PHP version:

```bash
php -v
```

Check the required extensions:

```bash
php -r '
foreach (["pdo_sqlite", "dom", "libxml"] as $extension) {
    echo $extension . ": " .
        (extension_loaded($extension) ? "OK" : "MISSING") .
        PHP_EOL;
}
'
```

Check `allow_url_fopen`:

```bash
php -r 'echo "allow_url_fopen=" . ini_get("allow_url_fopen") . PHP_EOL;'
```

Expected result:

```text
allow_url_fopen=1
```

---

# Installation

## Quick Installation

Clone the repository:

```bash
git clone https://github.com/xsukax/xsukax-X-RSS-Generator.git
cd xsukax-X-RSS-Generator
```

Ensure the main application file is named:

```text
index.php
```

Verify its PHP syntax:

```bash
php -l index.php
```

If everything is correct:

```text
No syntax errors detected in index.php
```

Place the project inside your web server's document root or configure a dedicated virtual host for it.

---

## Debian / Ubuntu

Install PHP and the required extensions:

```bash
sudo apt update
sudo apt install php php-cli php-fpm php-sqlite3 php-xml
```

Verify the modules:

```bash
php -m | grep -Ei 'PDO|sqlite|dom|libxml'
```

Clone the project:

```bash
cd /var/www
sudo git clone https://github.com/xsukax/xsukax-X-RSS-Generator.git xrss
```

Ensure the PHP/web-server process can create the SQLite database in the application directory.

For example, if PHP runs as `www-data`:

```bash
sudo chown -R www-data:www-data /var/www/xrss
sudo chmod 750 /var/www/xrss
```

Adjust permissions according to your own deployment model and security policy.

---

## Local Development

PHP's built-in development server can be used for testing:

```bash
git clone https://github.com/xsukax/xsukax-X-RSS-Generator.git
cd xsukax-X-RSS-Generator
php -d allow_url_fopen=1 -S 127.0.0.1:8000
```

Open:

```text
http://127.0.0.1:8000/
```

> [!WARNING]
> PHP's built-in web server is intended for development and testing. Use Nginx, Apache, or another production-grade web server for public deployments.

---

# Configuration

Configuration is intentionally kept simple.

Application settings are defined as constants near the beginning of `index.php`.

Example:

```php
const APP_NAME = 'xsukax X RSS Generator';
const DB_FILE = __DIR__ . '/.xsukax-x-rss.sqlite';

const DEFAULT_LIMIT = 20;
const MIN_LIMIT = 1;
const MAX_LIMIT = 100;

const CACHE_TTL = 300;
const FETCH_TIMEOUT = 12;
const MAX_HTML_BYTES = 12_000_000;

const RATE_WINDOW = 60;
const RATE_MAX_REQUESTS = 60;
```

## Configuration Reference

| Setting             |                  Default | Description                                    |
| ------------------- | -----------------------: | ---------------------------------------------- |
| `APP_NAME`          | `xsukax X RSS Generator` | Application name                               |
| `DB_FILE`           |   `.xsukax-x-rss.sqlite` | SQLite database location                       |
| `DEFAULT_LIMIT`     |                     `20` | Default number of RSS items                    |
| `MIN_LIMIT`         |                      `1` | Minimum allowed feed size                      |
| `MAX_LIMIT`         |                    `100` | Maximum allowed feed size                      |
| `CACHE_TTL`         |                    `300` | Seconds between normal upstream fetch attempts |
| `FETCH_TIMEOUT`     |                     `12` | X HTTP request timeout                         |
| `MAX_HTML_BYTES`    |               `12000000` | Maximum accepted profile response size         |
| `USER_AGENT`        |     Application-specific | HTTP User-Agent sent to X                      |
| `RATE_WINDOW`       |                     `60` | Rate-limit window in seconds                   |
| `RATE_MAX_REQUESTS` |                     `60` | Requests allowed per client per window         |

After changing PHP constants, no database migration is normally required.

---

## X HTML Selectors

The X-specific HTML selectors are deliberately kept together:

```php
const POST_SELECTOR = 'article';
const STATUS_LINK_SELECTOR = 'a[href*="/status/"]';
const CONTENT_SELECTOR = 'div[dir="auto"]';
const TIME_SELECTOR = 'time[datetime]';
const IMAGE_SELECTOR = 'img[src]';
```

If X changes its frontend markup, these selectors may need to be updated.

This centralized design makes parser maintenance easier.

---

## php.ini

Make sure:

```ini
allow_url_fopen = On
display_errors = Off
log_errors = On
```

Restart PHP-FPM or your web server after modifying `php.ini`.

Example:

```bash
sudo systemctl restart php8.4-fpm
```

Use the PHP-FPM version installed on your own server.

---

# Usage

## Web Interface

Navigate to the application URL:

```text
https://rss.example.com/
```

Enter:

* **Username** — an X username, with or without `@`
* **Limit** — number of posts to include

The supported limit range is:

```text
1 - 100
```

Click:

```text
Open RSS
```

to open the generated feed.

### Example

Username:

```text
xsukax
```

Limit:

```text
20
```

The resulting feed will use a URL similar to:

```text
https://rss.example.com/index.php?x=xsukax&l=20
```

---

## Direct RSS URL

Feeds can be accessed without the GUI.

Format:

```text
index.php?x=USERNAME&l=LIMIT
```

Example:

```text
https://rss.example.com/index.php?x=xsukax&l=20
```

If `index.php` is configured as the default directory index, this may also work:

```text
https://rss.example.com/?x=xsukax&l=20
```

### Parameters

| Parameter | Required | Description             |
| --------- | -------- | ----------------------- |
| `x`       | Yes      | X username              |
| `l`       | No       | Maximum items to return |

If `l` is omitted, the application uses:

```text
20
```

The accepted range is:

```text
1 - 100
```

A leading `@` in the username is automatically removed.

Valid username characters are:

```text
A-Z
a-z
0-9
_
```

---

## Command-Line Testing

You can test a feed with `curl`:

```bash
curl -i "http://127.0.0.1:8000/?x=xsukax&l=10"
```

Save the generated RSS:

```bash
curl \
  "http://127.0.0.1:8000/?x=xsukax&l=20" \
  -o xsukax.xml
```

Inspect the output:

```bash
head -n 30 xsukax.xml
```

---

## RSS Reader

Copy your generated URL:

```text
https://rss.example.com/?x=xsukax&l=20
```

and add it to your preferred RSS client.

The feed can be used with software such as:

* FreshRSS
* Miniflux
* Feedly
* NetNewsWire
* NewsBlur
* Thunderbird
* Feedbro
* Other RSS 2.0-compatible applications

---

## Manual Cache Refresh

The normal feed endpoint respects `CACHE_TTL`.

To bypass the normal cache interval:

1. Open the web interface.
2. Enter the X username.
3. Select a feed limit.
4. Click **Refresh cache now**.

A manual refresh bypasses the normal cache TTL and attempts a fresh profile retrieval immediately.

The interface reports:

* Number of parsed items
* Number of newly added items
* Number of updated cached items
* Refresh errors, if any

If a refresh fails but older data exists, cached posts remain available.

---

# Project Structure

The project intentionally has a minimal structure:

```text
xsukax-X-RSS-Generator/
├── index.php
├── README.md
├── LICENSE
└── .xsukax-x-rss.sqlite       # Generated automatically at runtime
```

Recommended optional `.gitignore`:

```text
.xsukax-x-rss.sqlite
.xsukax-x-rss.sqlite-journal
*.log
```

The generated SQLite database should **not** be committed to Git.

---

## `index.php`

The single application file contains:

```text
Configuration
│
├── Generic helpers and validation
├── Browser/RSS content-type handling
├── SQLite database initialization
├── Per-IP rate limiting
├── HTTPS profile fetching
├── CSS-selector-to-XPath conversion
├── X HTML parsing
├── Post and image extraction
├── Timestamp detection
├── Cache management
├── Post de-duplication
├── RSS 2.0 generation
├── GUI session handling
├── CSRF protection
├── Security headers
├── Web interface rendering
└── Request router
```

This architecture makes deployment straightforward and avoids framework scaffolding.

---

# Caching and Storage

## SQLite Database

The application automatically creates:

```text
.xsukax-x-rss.sqlite
```

inside the application directory.

The database contains three main tables:

### `users`

Stores per-profile metadata such as:

* Username
* Last fetch attempt
* Last successful fetch
* Last fetch error
* HTTP ETag
* HTTP Last-Modified value
* Last update time

### `items`

Stores cached X posts:

* Post ID
* Username
* Title
* Link
* Content
* Publication date
* Fetch timestamp
* Source HTML fragment

### `rate_limits`

Stores temporary per-IP request counters used by the built-in rate limiter.

---

## Cache Behavior

The default cache lifetime is:

```text
300 seconds
```

or:

```text
5 minutes
```

During that period, repeated feed requests use cached content instead of repeatedly fetching the X profile.

After expiration, the application attempts to refresh the source.

When available, upstream HTTP validators are used:

```text
If-None-Match
If-Modified-Since
```

If X responds with:

```text
304 Not Modified
```

the existing cache remains valid without reparsing identical content.

---

## Generated Feed ETag

The RSS feed itself also receives an ETag calculated from feed state.

RSS readers sending:

```http
If-None-Match: "..."
```

can receive:

```http
HTTP/1.1 304 Not Modified
```

instead of downloading the complete feed again.

---

# Production Deployment

## Nginx Example

A simplified Nginx configuration might look like:

```nginx
server {
    listen 80;
    server_name rss.example.com;

    root /var/www/xrss;
    index index.php;

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    location ~ \.php$ {
        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        fastcgi_pass unix:/run/php/php8.4-fpm.sock;
    }

    # Never expose SQLite files.
    location ~* \.(sqlite|sqlite3|db)(-journal)?$ {
        deny all;
        return 404;
    }

    # Protect hidden files while allowing ACME challenges.
    location ~ /\.(?!well-known).* {
        deny all;
        return 404;
    }
}
```

Adjust the PHP-FPM socket for your installed PHP version.

For production, add TLS using your preferred certificate provider.

---

## Apache Protection

When using Apache, make sure the SQLite database cannot be downloaded.

An `.htaccess` or VirtualHost rule can include:

```apache
<FilesMatch "\.(sqlite|sqlite3|db)(-journal)?$">
    Require all denied
</FilesMatch>
```

The application database contains cached source content and request metadata and should never be publicly downloadable.

---

## Reverse Proxy Considerations

The application's rate limiting intentionally uses PHP's `REMOTE_ADDR` and does not automatically trust arbitrary `X-Forwarded-For` values.

This avoids IP spoofing through untrusted proxy headers.

If the application runs behind a trusted reverse proxy, configure the proxy/web server's **real-IP mechanism** so PHP receives the correct trusted client address.

Do not modify the application to blindly trust user-controlled `X-Forwarded-For` headers.

---

# Security

Security reports are welcome and should be handled responsibly.

## Built-In Security Controls

The project includes several defensive measures:

### Input Validation

X usernames are restricted to:

```text
letters
digits
underscores
```

Feed limits must be integers between:

```text
1 and 100
```

### SQL Safety

Database operations use PDO prepared statements where applicable.

The feed limit is validated and converted to an integer before being incorporated into the SQLite `LIMIT` clause.

### CSRF Protection

GUI POST actions include randomly generated CSRF tokens.

Tokens are compared using:

```php
hash_equals()
```

to prevent timing-sensitive comparisons.

### Session Security

GUI sessions use:

* HTTP-only cookies
* `SameSite=Lax`
* Secure cookies when HTTPS is detected

### HTTP Security Headers

The GUI sends headers including:

```http
X-Content-Type-Options: nosniff
Referrer-Policy: no-referrer
X-Frame-Options: DENY
Content-Security-Policy: ...
Cache-Control: no-store
```

### Upstream TLS Verification

HTTPS requests use TLS certificate and hostname verification.

### DOM Parser Hardening

HTML parsing uses libxml with network access disabled for parser-triggered external resources.

### Database Permissions

When the SQLite file is created, the application attempts to apply:

```text
0600
```

permissions.

Web-server-level protection is still strongly recommended.

---

## Production Security Checklist

Before exposing the generator publicly:

* [ ] Use a currently supported PHP version.
* [ ] Enable HTTPS.
* [ ] Keep PHP and system packages updated.
* [ ] Keep `display_errors` disabled.
* [ ] Enable PHP error logging.
* [ ] Block direct HTTP access to SQLite files.
* [ ] Do not commit `.xsukax-x-rss.sqlite` to Git.
* [ ] Restrict application directory permissions.
* [ ] Allow only the PHP/web-server user to modify runtime data.
* [ ] Keep the default rate limiter enabled.
* [ ] Configure trusted proxy IP handling correctly.
* [ ] Monitor PHP and web-server error logs.
* [ ] Review parser selectors after upstream X frontend changes.
* [ ] Back up the SQLite database if cached feed history is important.

---

## Reporting a Vulnerability

Please **do not publicly disclose exploitable security vulnerabilities in a normal GitHub issue**.

Preferred reporting method:

1. Use GitHub's **Security Advisories / private vulnerability reporting** feature for this repository, if available.
2. Include:

   * Affected version or commit
   * Description of the vulnerability
   * Reproduction steps
   * Potential impact
   * Suggested mitigation, if known
3. Allow reasonable time for investigation and remediation before public disclosure.

If private vulnerability reporting is not available, open a minimal issue requesting a private communication channel **without publishing exploit details**.

---

# Troubleshooting

## `PDO SQLite extension (pdo_sqlite) is required`

Install SQLite support.

Debian / Ubuntu:

```bash
sudo apt install php-sqlite3
```

Then restart PHP-FPM or Apache.

---

## `DOM and libxml extensions are required`

Install PHP XML support:

```bash
sudo apt install php-xml
```

Restart PHP afterward.

---

## `allow_url_fopen must be enabled`

Locate the active PHP configuration:

```bash
php --ini
```

Set:

```ini
allow_url_fopen = On
```

Restart the relevant PHP service.

---

## SQLite Database Cannot Be Created

Ensure the PHP process can write to the application directory.

Check:

```bash
ls -ld .
```

and identify the PHP-FPM user:

```bash
ps aux | grep php-fpm
```

Then correct ownership or permissions appropriately.

---

## Feed Contains No Posts

Possible causes include:

* X changed its HTML structure.
* X returned a different page layout.
* The profile does not expose posts publicly.
* X blocked or challenged the server IP.
* The profile does not exist.
* Network access to X failed.
* Cached data does not yet exist.

Check the PHP error log and application refresh message.

---

## X Returns an HTTP Error

The application may report an error such as:

```text
X returned HTTP 403
```

or:

```text
X returned HTTP 429
```

This originates from the upstream X service.

Possible causes include:

* Network restrictions
* Temporary blocking
* Rate limiting
* Anti-automation measures
* Changed access behavior

The generator does not attempt to bypass X access controls.

---

## Feed Works in an RSS Reader but Looks Different in a Browser

This may be normal.

Browsers and RSS readers interpret XML and RSS MIME types differently. Firefox and Safari in particular have changed their built-in RSS behavior over time.

The application contains browser-specific handling intended to make top-level XML viewing more convenient while preserving the correct RSS content type for feed clients.

---

## Incorrect or Missing Images

Only supported X-hosted post/card image URLs are intentionally included.

Profile avatars, emoji assets, and unrelated third-party image URLs are excluded.

If X changes its media structure, image extraction logic may require an update.

---

# Limitations

Because this project works from public HTML rather than an official API, several limitations should be understood.

### X Markup Can Change

The parser depends on elements available in X's public HTML.

A significant frontend change can require selector updates.

### Server-Side Requests May Be Restricted

X may apply:

* Rate limits
* Geographic restrictions
* Authentication requirements
* Bot detection
* Temporary access restrictions

The application does not attempt to circumvent such controls.

### Public Profiles Only

The project is intended for information that is already publicly accessible.

It does not provide access to:

* Private accounts
* Protected posts
* Direct messages
* Authenticated account data

### Not a Complete X API Replacement

The generator is focused on converting publicly available profile posts into RSS. It is not intended to reproduce the full functionality of the official X API.

---

# Contributing

Contributions are welcome.

Bug fixes, compatibility improvements, documentation improvements, parser updates, security hardening, and performance enhancements are all encouraged.

## Development Workflow

### 1. Fork the repository

Use GitHub's **Fork** button.

### 2. Clone your fork

```bash
git clone https://github.com/YOUR-USERNAME/xsukax-X-RSS-Generator.git
cd xsukax-X-RSS-Generator
```

### 3. Create a branch

For a feature:

```bash
git checkout -b feature/my-feature
```

For a bug fix:

```bash
git checkout -b fix/parser-problem
```

### 4. Make your changes

Keep changes:

* Focused
* Readable
* Backward compatible when practical
* Consistent with the existing single-file architecture

### 5. Validate PHP syntax

```bash
php -l index.php
```

### 6. Test both interfaces

Verify:

* Normal GUI loading
* CSRF-protected forms
* Direct RSS generation
* Cache hits
* Forced cache refreshes
* Invalid usernames
* Invalid limits
* RSS XML validity
* SQLite initialization
* HTTP error handling
* Mobile layout

### 7. Commit

Use meaningful commit messages.

Example:

```bash
git commit -m "Fix X post image extraction"
```

### 8. Push

```bash
git push origin fix/parser-problem
```

### 9. Open a Pull Request

Describe:

* What changed
* Why it changed
* How it was tested
* Any compatibility considerations

---

## Coding Guidelines

Contributors should:

* Use PHP strict typing where appropriate.
* Follow the existing code style.
* Prefer PSR-12-compatible formatting.
* Validate all external input.
* Escape HTML output.
* Use parameterized database operations.
* Avoid introducing unnecessary dependencies.
* Keep X-specific selectors centralized.
* Preserve RSS 2.0 compatibility.
* Preserve the project's lightweight architecture.
* Document configuration changes.
* Avoid suppressing security-related failures.
* Never commit generated SQLite data.

Large architectural changes should be discussed in an issue before implementation.

---

# License

This project is licensed under the:

**GNU General Public License v3.0 (GPL-3.0)**

You are free to:

* Use the software
* Study the software
* Modify the software
* Distribute copies
* Distribute modified versions

subject to the terms and conditions of the GPL-3.0 license.

Modified or redistributed versions must comply with the GPL's source-code and licensing requirements.

See:

```text
LICENSE
```

for the complete license text.

SPDX identifier:

```text
GPL-3.0-only
```

---

# Author / Maintainers

## Primary Author

**xsukax**

GitHub:

```text
https://github.com/xsukax
```

Repository:

```text
https://github.com/xsukax/xsukax-X-RSS-Generator
```

The project is maintained as part of the xsukax collection of lightweight, self-hosted, and open-source utilities.

---

# Contact / Support

For bug reports, feature requests, compatibility problems, or general questions, use the repository's GitHub Issues page:

```text
https://github.com/xsukax/xsukax-X-RSS-Generator/issues
```

Before opening an issue:

1. Confirm you are using a supported PHP version.
2. Confirm `pdo_sqlite`, `dom`, and `libxml` are enabled.
3. Confirm `allow_url_fopen` is enabled.
4. Test whether the server itself can reach `https://x.com/`.
5. Check the PHP error log.
6. Search existing issues for similar reports.

When reporting a problem, include:

```text
PHP version:
Operating system:
Web server:
PHP SAPI:
Relevant error:
Steps to reproduce:
Expected behavior:
Actual behavior:
```

Do not post confidential server information, credentials, session cookies, or other secrets.

---

# Disclaimer

This project is an independent open-source utility and is **not affiliated with, endorsed by, sponsored by, or operated by X Corp.**

"X", "Twitter", and related names and trademarks belong to their respective owners.

The project accesses publicly available web content. Users are responsible for ensuring that their deployment and use of the software complies with:

* Applicable law
* X's applicable terms and policies
* Hosting-provider rules
* Network-access restrictions
* Content and privacy requirements in their jurisdiction

The software does not attempt to bypass authentication, access private accounts, or defeat technical access controls.

Because X can change its frontend implementation at any time, uninterrupted compatibility cannot be guaranteed.

---

## ⭐ Support the Project

If you find **xsukax X RSS Generator** useful:

* Star the repository
* Report bugs
* Suggest improvements
* Submit pull requests
* Share the project with other RSS and self-hosting users

Repository:

```text
https://github.com/xsukax/xsukax-X-RSS-Generator
```

---

**xsukax X RSS Generator**
*Public X profiles → clean, self-hosted RSS feeds.*
