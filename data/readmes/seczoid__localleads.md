<div align="center">

<img src="static/favicon.svg" width="72" alt="LocalLeads logo">

# LocalLeads

**Find every local business on Google Maps, get their emails, and let your AI agent do the rest.**

A self-hosted lead machine written in Rust. Pick from Google Maps' own business categories, search whole states or countries area by area, read each business's website for emails, socials and phone numbers, rotate through hundreds of checked proxies, and drive all of it from Claude, Codex or Cursor over MCP. One binary, one SQLite file, no API keys, no monthly bill.

[![Website](https://img.shields.io/badge/website-localleads.run-00b368.svg)](https://www.localleads.run/)
[![License: AGPL-3.0](https://img.shields.io/badge/license-AGPL--3.0-22c55e.svg)](LICENSE)
[![Rust](https://img.shields.io/badge/rust-2024-f74c00.svg?logo=rust)](https://www.rust-lang.org)
[![Docker](https://img.shields.io/badge/docker-ready-2496ed.svg?logo=docker&logoColor=white)](docs/SELF_HOSTING.md)
[![MCP](https://img.shields.io/badge/MCP-44_tools-8b5cf6.svg)](#-built-for-ai-agents-mcp)
[![Docker image](https://github.com/seczoid/localleads/actions/workflows/docker.yml/badge.svg)](https://github.com/seczoid/localleads/actions/workflows/docker.yml)

**[🌐 localleads.run](https://www.localleads.run/)** · [Features](#-features) · [Quick start](#-quick-start) · [MCP](#-built-for-ai-agents-mcp) · [Self-hosting](#-self-hosting-with-https) · [Docs](docs/SELF_HOSTING.md)

<sub>Proxies we recommend: <a href="https://fas.st/t/R1CJJibL"><b>ProxyScrape</b></a> residential.<br>Affiliate link: signing up through it supports the project at no extra cost to you.</sub>

<a href="https://www.localleads.run/"><img src="docs/images/hero.png" alt="The Searches page with a search running: Google Maps done, websites being read for emails" width="900"></a>

<sub>See every feature, how it compares with Outscraper, Apify and Scrap.io, and the one-line install at <a href="https://www.localleads.run/"><b>www.localleads.run</b></a>.</sub>

</div>

---

## ✨ Why LocalLeads

- **Whole regions, not 120 results.** Google Maps stops at about 120 results per lookup. LocalLeads splits a state, a city or a whole country into ZIP codes or towns, busiest first, so you get what Maps actually has, not the first page. Any country works.
- **Emails, not just listings.** Every lead with a website gets its site read: home, contact, about and team pages. Out come emails (even obfuscated and Cloudflare-protected ones), the people behind them, socials, extra phones and the tech the site runs.
- **Proxies that actually work.** A built-in proxy checker tests hundreds of proxies against Google Maps at once, groups them, and fails over mid-search when one dies.
- **Your agent can run it.** A full MCP server with 44 tools: "find 500 roofers in Austin with emails and export them" just works.
- **Yours.** Runs on your laptop or your VPS. Your data stays in one SQLite file you own. No API key, no per-lead pricing.
- **Fast and light.** Rust, Tokio and SQLite. Reads 64 websites at a time, keeps the leads table quick at millions of rows, and idles at a few MB of RAM.

## 🚀 Features

### 🔎 Google Maps search at scale

<img src="docs/images/new-search.png" alt="The New search form with the Google Maps category list open" width="900">

- **Google Maps categories built in:** start typing and pick from 4,000+ categories Google Maps itself uses ("Roofing contractor", "Dentist", "HVAC contractor"…), closest matches first, or browse them by industry and add a whole group at once. Anything else, like a brand name, is searched exactly as typed. One search can cover many business types, each searched in every area.
- **Every country:** a whole country, some states or provinces, single cities, ZIP or postal codes, or your own list of places. The US ships with 40,000+ ZIP codes; every other country comes with its states, towns of 1,000+ people and, for about a hundred countries, postal codes.
- **Area-by-area splitting:** big areas are broken into ZIP codes, cities or states, busiest first, to get past Google's per-lookup cap.
- **Three search modes:** text search, a Google Maps URL, or a list of place IDs.
- **Filters** for rating, review count, has website, has phone and more, applied as results come in.
- **Global de-duplication:** each business is stored once and linked to every search that found it, so overlapping areas never create repeats.
- **Fine control:** maximum results, results per area, skip the first N, language and region, exact-match keywords, retries, and requests at once (10 without proxies, 100 to 300 with them).
- **Preview first:** the summary shows how many lookups a search will make before you start it.

### 📡 Live progress

<img src="docs/images/search-live.png" alt="A search's page: Google Maps and Websites progress above its newest leads" width="900">

- Two progress bars update in real time: **Google Maps** (leads saved, areas searched, repeats skipped) and **Websites** (sites read, emails found, speed and time left).
- Once Google Maps is done, every lead's website is read for emails, as many at once as the search itself ran.
- Pause, resume or stop a search; **Continue** carries a stopped one on from the areas it already finished, and **Run again** starts a fresh copy. If the server restarts, updates or crashes, running searches carry on by themselves. Each search keeps an activity log of every step, retry and failure.

### 📧 Email and contact enrichment

<img src="docs/images/lead-detail.png" alt="Everything found for one lead" width="900">

For every lead with a website, LocalLeads reads up to 8 pages: the home page first, then links that look like contact, about or team pages, then common paths like `/contact` if nothing turned up. It picks up:

- `mailto:` links, plain addresses, and ones hidden as `name [at] domain (dot) com`
- Cloudflare-protected emails and emails in structured data (JSON-LD)
- **Names and job titles** next to an address, from team pages
- **Socials:** Facebook, Instagram, LinkedIn, X, YouTube and TikTok
- Extra phone numbers, the site title, and whether the site runs Google Tag Manager or a Facebook Pixel

Then it ranks them: emails on the company's own domain first, a real person's address ahead of `info@`. That one becomes the lead's **best email**.

**Google place details** (optional): reviews broken down by star, review topics, owner information, photos and opening hours.

**Email verification** (only in builds made with `--features verify`; the release downloads and Docker image leave it out): asks each address's mail server whether the mailbox exists, without sending anything. It checks the 5 best emails per lead and labels each one:

| Verdict | Meaning |
| --- | --- |
| ✅ Safe | The server confirmed the mailbox |
| ⚠️ Risky | Catch-all domain, role or disposable address |
| ❔ Unverified | The server wouldn't say |
| ❌ Invalid | No such mailbox; never picked as the best email |

### 📋 Leads browser and exports

<img src="docs/images/leads-browse.png" alt="The leads table filtered to one search and leads with an email, with the Category filter open showing counts" width="900">

- **One table for every lead,** narrowed to one or more searches with the Search filter.
- **Filters with live counts:** search, category, state, city, phone and website, email found, rating.
- **Instant search** across name, address, phone, website and email.
- **Server-side paging,** so the table stays fast with millions of rows.
- **Bulk actions** on selected rows or everything that matches: export, delete, or find emails again. Deletes can be undone for an hour.
- **Clean CSV exports:** one row per business with readable columns (Name, Phone, Email, Email status, Website, Google Maps URL, Hours, socials…), the best email first and opening hours written out. Pick the columns you want, or switch to the full **Outscraper format** (raw fields, one row per email) for tools that expect it. JSON keeps the raw Maps data. Download, or write big exports straight to disk.
- **Lead detail:** every email and the page it came from, socials, phones, the site's tech, reviews, hours and coordinates.

### 🛡️ Proxy checker and manager

<img src="docs/images/proxies.png" alt="The proxies page with group tabs, the health bar and each proxy's status, latency and last error" width="900">

Google limits how fast one connection can search. LocalLeads has a complete proxy toolkit built in:

- **Paste or import** proxies in any common format: `http://user:pass@host:port`, `socks5://…`, `host:port`. Big files import in the background, de-duplicated.
- **Health checks** test every proxy against Google Maps at once and mark it healthy, slow or failed, with its latency and last error.
- **Tunable checker:** test URL, timeout, retries, slow threshold, expected page content, exit-IP check, and how many checks run at once.
- **History** of every check per proxy: when, status, latency, exit IP.
- **Groups** let a search use only some proxies, like a residential pool.
- **Failover:** a proxy that fails mid-search is set aside, and the request retries through another.
- **Bulk tools:** enable, disable, delete, or prune everything that keeps failing.

HTTP, HTTPS and SOCKS5 are supported. Only Google lookups go through proxies; websites are read directly.

**Where to get proxies.** Free proxy lists rarely last on Google Maps. Residential proxies hold up best, and we recommend [ProxyScrape](https://fas.st/t/R1CJJibL)'s rotating residential pool (120M+ IPs in 190+ countries, with a free start). Paste the proxy address from their dashboard into **Add proxies** and you're set. *That's an affiliate link; it helps fund LocalLeads.*

### 🤖 Built for AI agents (MCP)

<img src="docs/images/mcp.png" alt="The Agents page: API keys, then the setup command for Claude Code and ten other agents" width="900">

LocalLeads includes a **Model Context Protocol** server. Everything the dashboard does, an agent can do: **44 tools** covering searches, categories, leads, exports, enrichment, proxies, groups, backups and the server log.

- **11 clients set up for you:** Claude Code, Codex, Cursor, Claude Desktop, VS Code (Copilot), Windsurf, Gemini CLI, Zed, Cline, opencode, and any other MCP client. The Agents page shows the exact command or config for each, with your paths and API key filled in.
- **Two ways to connect:** stdio (the agent launches `localleads mcp`) or Streamable HTTP at `/mcp`. Both share the dashboard's live state, so searches an agent starts show up on screen in real time.
- **API keys:** create one per agent, see when each was last used, revoke any of them instantly. Keys are stored only as hashes.
- **Safe by default:** delete tools are marked destructive, so agents ask first, and every delete returns an undo id that `undo_delete` honours for an hour.

Things you can just ask:

> *"Find 500 roofers in Austin, TX with websites and emails, and tell me when it's done."*
>
> *"Show me the dentists from my last search rated 4.5+ that have an email, as a table."*
>
> *"Export every lead with a verified email from the plumbers search to CSV on my desktop."*
>
> *"Check all my proxies and remove the ones that keep failing."*

<details>
<summary><b>All 44 tools</b></summary>

| Area | Tools |
| --- | --- |
| Searches | `search_options` `find_cities` `find_categories` `preview_search` `create_search` `rerun_search` `continue_search` `list_searches` `get_search` `pause_search` `resume_search` `stop_search` `delete_search` |
| Leads | `browse_leads` `lead_facets` `lead_lists` `get_lead` `enrich_leads` `export_leads` `delete_leads` |
| Proxies | `list_proxies` `proxy_status` `add_proxies` `import_proxy_file` `check_proxies` `cancel_proxy_check` `set_proxies_enabled` `delete_proxies` `prune_proxies` `proxy_history` `get_checker_settings` `update_checker_settings` |
| Groups | `list_proxy_groups` `create_proxy_group` `rename_proxy_group` `delete_proxy_group` `assign_proxies_to_group` `remove_proxies_from_group` |
| App | `overview` `app_info` `list_notices` `server_log` `undo_delete` `backup_database` |

</details>

### 🔐 Self-hosting with HTTPS

- **One-command setup:** paste one line on your Mac or server and LocalLeads is installed and running, with HTTPS set up on a server. Run it again to update. See the [Quick start](#-quick-start).
- **Accounts:** first-run setup creates your account (Argon2id password hash); sign out and change your password from Settings.
- **Hardened for the internet:** a one-time setup code so no stranger can claim a fresh install, sign-in lockout after repeated failures, `Secure` cookies, a Content-Security-Policy and other security headers, and a host allowlist.
- **Small footprint:** one binary in a slim image that idles at a few MB of RAM, runs as an unprivileged user, has a health check and shuts down cleanly.

### 🧰 And also

- **Searches home** with totals, anything running, and every search with its phone and website coverage.
- **Undo** for deletes: searches, leads, proxies and groups come back with one click for an hour.
- **System page** with the server's own log, live, filterable and downloadable.
- **Updates from the dashboard:** an **Update and restart** card when a new version is out.
- **Backups:** one-click consistent snapshots while searches run, and restore from the command line.
- **Built-in docs** page with a walkthrough of every screen.
- **Dark and light themes.**
- **JSON API** (`/api/stats`, `/api/jobs`, `/api/leads`) for scripts, using an API key or your session.

## ⚡ Quick start

Pick where you want LocalLeads to run:

| Where | Good for | Takes |
| --- | --- | --- |
| **[On your Mac](#on-your-mac)** | Trying it out and using it yourself | 1 minute |
| **[On your Windows PC](#on-your-windows-pc)** | The same, on Windows | 1 minute |
| **[On a server (VPS)](#on-a-server-vps)** | Opening it from any computer or phone, with searches that keep running when your computer is off | 5 minutes |

### On your Mac

1. Open **Terminal**: press `⌘ Space`, type `Terminal`, press Enter.
2. Copy this line, paste it into Terminal, and press Enter:

   ```bash
   curl -fsSL https://raw.githubusercontent.com/seczoid/localleads/main/setup.sh | bash
   ```

3. When it asks you something, press **Enter** to accept the suggested answer.
4. When it says **LocalLeads is running**, open **[http://localhost:7878](http://localhost:7878)** in your browser and create your account.

That's it. LocalLeads starts again by itself whenever you log in, so you only do this once.

### On your Windows PC

1. Download **[localleads for Windows](https://github.com/seczoid/localleads/releases/latest/download/localleads-x86_64-pc-windows-msvc.zip)**.
   On a Windows laptop with an ARM chip (Snapdragon, Surface Pro X), take **[this one](https://github.com/seczoid/localleads/releases/latest/download/localleads-aarch64-pc-windows-msvc.zip)** instead.
2. Right-click the downloaded file and choose **Extract All**.
3. Open the new folder and double-click **localleads.exe**.
   If you see "Windows protected your PC", click **More info**, then **Run anyway**.
4. A black window opens. Leave it open while you use LocalLeads; closing it stops LocalLeads.
5. Open **[http://localhost:7878](http://localhost:7878)** in your browser and create your account.

### On a server (VPS)

Any Linux server works; Ubuntu or Debian is easiest. You'll need the login your server provider gave you.

1. Log in to your server. Your provider shows you how; it usually looks like `ssh root@203.0.113.7`.
2. Copy this line, paste it, and press Enter:

   ```bash
   curl -fsSL https://raw.githubusercontent.com/seczoid/localleads/main/setup.sh | bash
   ```

3. It asks **Where will you open LocalLeads?**
   - **No domain name?** Press **Enter**. You'll open LocalLeads at your server's address, like `https://203.0.113.7`.
   - **Have a domain** (like `leads.yourcompany.com`)? First, at the company you bought it from, add an **A record** that points it at your server's IP address. Then type **2** and enter the domain.

   For every other question, press **Enter**.
4. At the end it shows **the address to open** and a **setup code**. Open the address, type the code, and create your account.

Good to know:

- **"Your connection is not private"?** That's expected when you use the server's address instead of a domain. Click **Advanced**, then **Proceed**. You only see it once per browser. With a domain, you never see it.
- **The page won't load?** Many providers have their own firewall. In your provider's control panel, allow ports **80** and **443**.
- Everything LocalLeads needs, including the web server that handles HTTPS, is installed for you.

### Update, change settings or uninstall

- **From the dashboard:** when a new version is out, an **Update and restart** card appears in the sidebar. It downloads the release, checks it against the release's checksums, backs up your database and restarts. Running searches pause for a few seconds and carry on afterwards. A version that fails to start is set aside and the one before it keeps running. Set `LOCALLEADS_UPDATES=off` to turn the checks off.
- **Mac or server:** run the same command again. It shows a menu: update, change settings, or uninstall. Your leads are kept.
- **Windows:** download the new version the same way and replace `localleads.exe`. Your leads are stored separately, so they're kept.

### Connect your AI agent

In LocalLeads, open **Agents** in the sidebar, create an API key, choose your agent (Claude, Codex, Cursor and 8 more), and copy what it shows into your agent. Full details: **[docs/MCP.md](docs/MCP.md)**.

<details>
<summary><b>On the command line instead</b></summary>

Register LocalLeads with Claude Code, Codex and Cursor in one go. This also creates an API key:

```bash
localleads mcp install --write
```

For Claude Code over HTTP:

```bash
claude mcp add --scope user --transport http localleads https://leads.example.com/mcp \
  --header "Authorization: Bearer ll_your_api_key"
```

</details>

### For developers and advanced setups

<details>
<summary><b>What the setup command does</b></summary>

1. Downloads the latest release built for your machine and checks its SHA-256.
2. Asks where you'll open LocalLeads.
3. On a Linux server opened by domain or IP, sets up HTTPS with [Caddy](https://caddyserver.com). If Caddy is missing, it installs it with the system's package manager: Caddy's own repository on Debian/Ubuntu (apt) and Fedora/RHEL (dnf), the regular package on Arch (pacman) and openSUSE (zypper), or Caddy's official binary anywhere else. If Caddy already serves other sites, LocalLeads is added next to them and the Caddyfile is backed up first. On a Mac, Caddy is never installed.
4. Runs LocalLeads as a service that starts on boot (systemd on Linux, launchd on macOS). On Linux it runs as its own unprivileged user in a hardened unit.
5. Opens ports 80 and 443 in ufw or firewalld if one is on, then prints the address and a one-time setup code.

If ports 80 and 443 are already taken (say by nginx), it tells you what's using them and offers other ports, or putting LocalLeads behind that web server. On a [Coolify](https://coolify.io) server it routes Let's Encrypt's check through Coolify's proxy, so the IP still gets a trusted certificate.

| Choice | You get | Needs |
| --- | --- | --- |
| **The server's IP** (default on Linux) | `https://203.0.113.7` with a Let's Encrypt certificate for the IP, renewed on its own (self-signed if Let's Encrypt can't reach the server) | Nothing |
| **Your domain** | `https://leads.example.com` with a Let's Encrypt certificate, renewed on its own | A DNS `A` record pointing at the server |
| **Only this machine** (default on macOS) | `http://localhost:7878` | Nothing |
| **Behind your own web server** | LocalLeads on `127.0.0.1`, plus a ready-made nginx, Caddy or Apache config to paste in | Your nginx, Traefik, Caddy, ... |

Data lives in `/var/lib/localleads` on Linux and `~/.localleads/data` on macOS.

To read the script before running it:

```bash
curl -fsSLO https://raw.githubusercontent.com/seczoid/localleads/main/setup.sh && less setup.sh && bash setup.sh
```

Supported: Linux with systemd and glibc 2.28+ (Ubuntu 20.04+, Debian 10+, RHEL/Rocky/Alma 8+, Fedora, Arch, openSUSE) on x86_64 or ARM64, and macOS 12+ on Apple silicon or Intel.

</details>

<details>
<summary><b>Setup options, and installing without questions</b></summary>

For scripts and cloud-init, put options after `bash -s --`:

```bash
curl -fsSL https://raw.githubusercontent.com/seczoid/localleads/main/setup.sh | sudo bash -s -- --domain leads.example.com --yes
```

| Option | What it does |
| --- | --- |
| `--domain NAME` | Serve at your domain with Let's Encrypt HTTPS (Linux) |
| `--ip [ADDRESS]` | Serve at the server's IP with Let's Encrypt HTTPS for the IP (Linux) |
| `--local` | Only this machine, at `http://localhost:PORT` |
| `--proxy URL` | Behind your own web server; `URL` is the address people open |
| `--port N` | Port LocalLeads listens on, on `127.0.0.1` (default 7878) |
| `--edge` | Install the newest build of `main` instead of the latest release |
| `--version vX.Y.Z` | Install a specific release |
| `--binary PATH` | Install a `localleads` binary you built yourself |
| `--no-firewall` | Leave ufw and firewalld alone |
| `-y`, `--yes` | Don't ask; use the defaults and the options given |
| `--update` | Update an existing install |
| `--uninstall` | Remove it; add `--delete-data` to also delete the data (Caddy stays) |

</details>

<details>
<summary><b>All downloads</b></summary>

Every release on the **[Releases page](https://github.com/seczoid/localleads/releases)** has builds for Linux (x86_64, ARM64), macOS (Apple silicon, Intel) and Windows (x86_64, ARM64), with a `SHA256SUMS` file. Unpack one and run:

```bash
./localleads --open          # Windows: localleads.exe --open
```

The newest build of `main` is always on the [edge pre-release](https://github.com/seczoid/localleads/releases/tag/edge).

</details>

<details>
<summary><b>Docker</b></summary>

The repo's `compose.yaml` runs LocalLeads behind Caddy (images: `ghcr.io/seczoid/localleads`):

```bash
git clone https://github.com/seczoid/localleads.git
cd localleads
cp .env.example .env    # set DOMAIN=leads.example.com
docker compose up -d --build
docker compose logs localleads    # the one-time setup code
```

Open `https://leads.example.com`, enter the code and create your account. Update with `git pull && docker compose up -d --build`.

On your own computer, without Compose:

```bash
git clone https://github.com/seczoid/localleads.git
cd localleads
docker build -t localleads .
docker run -d --name localleads -p 127.0.0.1:7878:7878 -v localleads-data:/data localleads
docker logs localleads
```

Then open [http://127.0.0.1:7878](http://127.0.0.1:7878) and create your account with the setup code from the log.

Backups, restores, all settings, and running behind your own nginx or Traefik are covered in **[docs/SELF_HOSTING.md](docs/SELF_HOSTING.md)**.

</details>

<details>
<summary><b>Build from source</b></summary>

**1. Install the build tools.**

- macOS:

  ```bash
  xcode-select --install
  brew install cmake
  ```

- Debian / Ubuntu:

  ```bash
  sudo apt-get install -y build-essential cmake clang libclang-dev pkg-config
  ```

- Rust 1.88 or newer:

  ```bash
  curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
  ```

**2. Build and install.**

```bash
git clone https://github.com/seczoid/localleads.git
cd localleads
cargo install --path .
```

Add `--features verify` for email verification (mail-server checks). It's left out of the release builds.

**3. Run it.**

```bash
localleads --open
```

The dashboard opens at [http://127.0.0.1:7878](http://127.0.0.1:7878). Create your account on the first visit.

</details>

## ⚙️ Command line

```text
localleads [OPTIONS] [COMMAND]

Commands:
  mcp                 MCP server over stdio for AI agents
  mcp install         Print or (--write) apply the setup for Claude Code, Codex and Cursor

Options:
  --db <PATH>          SQLite database path               [env: LOCALLEADS_DB]
  --bind <ADDR>        Listen address (127.0.0.1:7878)     [env: LOCALLEADS_BIND]
  --public-url <URL>   Public address, e.g. https://leads.example.com
                                                           [env: LOCALLEADS_PUBLIC_URL]
  --behind-proxy       Trust X-Forwarded-* from a reverse proxy
                                                           [env: LOCALLEADS_BEHIND_PROXY]
  --restore <PATH>     Restore a SQLite backup before starting
  --open               Open the dashboard in your browser

Environment:
  LOCALLEADS_UPDATES=off   Don't look for new versions on GitHub
```

Examples:

```bash
# Another database and port
localleads --db ~/leads/roofers.sqlite --bind 127.0.0.1:7879

# Restore a backup, then start
localleads --restore ~/Downloads/localleads-backup.sqlite

# MCP over stdio with an API key
LOCALLEADS_API_KEY=ll_your_api_key localleads mcp
```

## 🏗️ How it's built

| Layer | Tech |
| --- | --- |
| Server | Rust 2024, [axum](https://github.com/tokio-rs/axum), Tokio |
| UI | Server-rendered [Askama](https://github.com/askama-rs/askama) templates, [htmx](https://htmx.org), [Alpine.js](https://alpinejs.dev), DataTables, [Hugeicons](https://hugeicons.com) |
| Storage | SQLite in WAL mode (one writer, a pool of readers) |
| Scraping | Google Maps' web search responses parsed directly; websites read with browser-like TLS ([webclaw](https://github.com/0xMassi/webclaw)) |
| Email checks | [check-if-email-exists](https://github.com/reacherhq/check-if-email-exists) (optional `verify` feature) |
| MCP | [rmcp](https://github.com/modelcontextprotocol/rust-sdk), stdio and Streamable HTTP |
| Deploy | Multi-stage Docker image, Caddy for HTTPS, multi-arch images built in GitHub Actions |

Everything (searches, leads, proxies, settings, your account) lives in a single SQLite file. Static assets are compiled into the binary, so there's nothing else to deploy.

## 🧪 Development

```bash
cargo run                      # debug build on http://127.0.0.1:7878
cargo test --features verify   # unit and integration tests
cargo clippy --all-targets --features verify
cargo fmt
```

Pull requests are welcome. For larger changes, please open an issue first to talk it through.

### Releasing

Every push to `main` rebuilds the [edge pre-release](https://github.com/seczoid/localleads/releases/tag/edge) for all six platforms. To cut a real release, bump `version` in `Cargo.toml`, commit, and push a matching tag:

```bash
git tag v0.2.0
git push origin v0.2.0
```

The [Release workflow](.github/workflows/release.yml) builds Linux, macOS and Windows binaries, writes `SHA256SUMS`, and publishes "LocalLeads v0.2.0" with install instructions and notes generated from the commits since the last tag. `setup.sh` installs it on the next run. The tag push also publishes the Docker image as `:0.2.0` and `:latest`.

## ⚖️ Responsible use

LocalLeads reads public Google Maps listings and public business websites. Google can change its responses, show consent pages or rate-limit requests at any time; LocalLeads reports those as failures and doesn't try to bypass them. You're responsible for following the laws that apply to you (for example GDPR, CAN-SPAM and CASL) and the terms of the sites you access. Use the data to reach businesses respectfully.

## 📄 License

[GNU AGPL-3.0](LICENSE) © seczoid

You can use, change and self-host LocalLeads freely. If you share a changed version, or run one as a service that other people use over a network, you must publish your full source code under the same license.
