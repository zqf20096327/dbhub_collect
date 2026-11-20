# Boxloft

A warehouse app for resellers and small 3PLs. You scan items into named boxes, see what Amazon and the stores are bringing in, and pick and pack what sold.

It came out of a real resale warehouse with 2 people on the floor. Most of the hard parts are done: a ledger that never loses a unit, two people saving at once without overwriting each other, marketplace syncs, and a stock audit that checks what you bought against what sold. You connect your own accounts and point your coding agent at `CLAUDE.md` for the rest.

## What it does

- **Boxes, not bins.** Every box has a name written on it (A31). The letter is the market: A for Amazon, E for eBay, W for Walmart, L for local. Scan a box, scan items, done. Each scan saves at once and has its own Undo.
- **Loose on a shelf, or in another building.** Put away takes a place as well as a box: one tap per building or named shelf, or "+ New place". A place has its own page, where you add items the same way as on a box page.
- **No barcode? Take a photo.** On a box or place page, a photo of the item finds its match (needs a photo key, see AI below). One tap puts it away, and the photo becomes the item's photo when it has none.
- **Receive.** Scan a UPC and a new item fills in from the catalog (title, photo, size). Pick the order it came from and the cost and date fill in. Items bought on 5 orders go in as one save.
- **Arriving.** Amazon orders, store orders from your Gmail, and Walmart orders, by expected date, with tracking. Scan the carrier label on a box that showed up and it lists what's inside.
- **Orders.** Amazon (SP-API) and eBay sales sync every 15 minutes. Walmart sales, and anything else, come in as a CSV file (Orders, Import orders). Each order shows the photo, the box to pick from and the ship box that fits. Orders the marketplace already shipped get scanned out by themselves.
- **Stock audit.** Per ASIN: bought, minus sent back, minus sold on Amazon, is what should be on your shelves. Scan the boxes and it tells you what's missing.
- **Listings.** What's in your A boxes that isn't listed, what's listed with 0 in a box, what Amazon won't let you sell.
- **Labels.** 4x6 box labels and 2x1 unit labels from the browser (Rollo or any label printer). Phones send labels to a print queue, and the computer with the printer prints them.
- **Two people at once.** A save from a screen that showed old numbers is refused with who changed it. Nothing double counts.

## What it doesn't do

- It doesn't buy shipping labels. You buy them where you do now (Seller Central, eBay, Pirate Ship), and the app scans the order out.
- It doesn't make or edit listings, and it doesn't push stock counts to any marketplace. It reads them.
- It doesn't sync Walmart sales or listings yet. The Walmart card saves your keys and tests them; import Walmart sales as CSV.
- It's US only: amazon.com, the eBay US site, US dollars.

## Before you start

You need a Mac or Linux computer. On Windows, use WSL (Windows Subsystem for Linux) and run every command below inside it.

- **Python 3.11 or newer.** Check with `python3 --version`. Get it from [python.org/downloads](https://www.python.org/downloads/).
- **Node 20 or newer.** Check with `node --version`. Get it from [nodejs.org](https://nodejs.org/).
- **git.** Check with `git --version`. On a Mac, running it the first time offers to install it.

What it costs to run:

- A small Linux server: about $6 a month (1 CPU, 1 GB of memory).
- A domain name, about $10 to $20 a year.
- Keepa is optional and paid (see keepa.com for its API plans). Without it, barcode lookup uses UPCitemdb's free tier, about 100 lookups a day.
- AI is optional and billed per call by the provider you pick.

## Try it on your computer

On this repo's GitHub page, click the green **Code** button and copy the HTTPS address. Then, in a terminal:

```bash
git clone <the address you copied> boxloft
cd boxloft
python3 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt
cd web && npm ci && npm run build && cd ..
BOXLOFT_DATA=./data BOXLOFT_PUBLIC_URL=http://localhost:5101 .venv/bin/python scripts/setup.py admin "Your Name" --demo
BOXLOFT_DATA=./data BOXLOFT_DEV=1 .venv/bin/python backend/server.py
```

`setup.py` prints a one-use link and your username (`admin` here). Open the link, set a password of 10 or more characters, and you're in. `--demo` puts 5 sample boxes with a few items in them; the other pages (orders, purchases, audit) start empty.

The last command runs the server. Leave that terminal window open while you use the app. Ctrl+C stops it.

The link starts with `BOXLOFT_PUBLIC_URL`, so its port has to match the server's (`BOXLOFT_PORT`, default 5101).

`BOXLOFT_DEV=1` lets the sign-in cookie work over plain HTTP, and it also makes the server listen on every network interface (0.0.0.0), so other devices on your network can reach it. That's handy for trying it on a phone at home. Don't use it on public Wi-Fi, and leave it off on a server.

Run the tests with `.venv/bin/python -m pytest -q tests`: about 600 pass and a few skip, in about a minute. The skips need private sample pages or a case the demo data doesn't have.

## Put it on a server

Phones need HTTPS for the camera scanner, and Amazon and eBay only send you back to an HTTPS address. So the real thing needs a server with a domain name.

1. **Rent a server.** Any provider works (DigitalOcean, Hetzner, Linode, AWS Lightsail). Pick Ubuntu 24.04, 1 GB of memory. Note its public IP address.
2. **Point a name at it.** At the company where you bought your domain, add a DNS record: type `A`, name `wms` (or whatever you like), value = the server's IP. That makes `wms.yourdomain.com`. It can take up to an hour to work.
3. **Open the ports.** Your provider's firewall must let in TCP 22 (SSH), 80 and 443. On the server itself: `ufw allow 22,80,443/tcp && ufw enable`.
4. **Install Docker.** Sign in with `ssh root@<server IP>`, then run `curl -fsSL https://get.docker.com | sh`.
5. **Start the app:**

```bash
git clone <the repo's address> boxloft && cd boxloft
cp .env.example .env
nano .env          # set BOXLOFT_PUBLIC_URL=https://wms.yourdomain.com and DOMAIN=wms.yourdomain.com, your name and time zone
docker compose up -d --build
docker compose exec app python3 scripts/setup.py admin "Your Name"
```

Caddy gets the HTTPS certificate for `DOMAIN` by itself. Open the link `setup.py` printed.

We haven't run the Docker path ourselves yet, so tell us what breaks. The original runs without Docker: Python 3.12, Caddy (`deploy/Caddyfile`) and the systemd unit in `deploy/boxloft.service`.

To update later: `git pull && docker compose up -d --build`.

## Back up and restore

Everything lives in one data folder (`BOXLOFT_DATA`; `/data` inside Docker): `wms.db`, `auth.db`, `photos/`, `secrets/` and `backups/`. Every night at 3:15 AM the app checks the ledger and copies both databases into `backups/` (the last 30 days).

Those copies sit on the same server. Copy the folder somewhere else every day:

```bash
docker compose cp app:/data ./boxloft-backup-$(date +%F)          # Docker
rsync -a root@<server IP>:/var/lib/boxloft/ ./boxloft-backup/    # without Docker, from your own computer
```

The nightly copies don't include `secrets/connections.json` (your marketplace keys) or the photos. A full copy of the folder has both. Keep it private: the keys file is plain text.

To restore: stop the app (`docker compose stop app`), put `wms.db` and `auth.db` back in the data folder, delete any `wms.db-wal`, `wms.db-shm`, `auth.db-wal` and `auth.db-shm` next to them, and start it again. Then run `python3 scripts/manage.py check` (Docker: `docker compose exec app python3 scripts/manage.py check`); it prints `"ok": true` when the ledger adds up.

## Settings

Everything about your business comes from the environment. See `.env.example`.

| Variable | What it is | Default |
|---|---|---|
| `BOXLOFT_APP_NAME` | Name in the header and on labels | Boxloft |
| `BOXLOFT_SITE_NAME` | The building where boxes sit on shelves | Main warehouse |
| `BOXLOFT_PLACE` | Town under the name in the sidebar | empty |
| `BOXLOFT_TZ` | Your time zone. "Today" and every time shown use it | America/New_York |
| `BOXLOFT_PUBLIC_URL` | The address people open | http://localhost:5101 |
| `BOXLOFT_TZ_LABEL` | Short label after times | ET, CT, MT, PT for US zones |
| `BOXLOFT_PORT` | Port the server listens on | 5101 |
| `BOXLOFT_DATA` | Data folder | ./data |
| `BOXLOFT_STATIC` | Built web app folder | web/dist |
| `BOXLOFT_DEV` | 1 = plain-HTTP cookie and listen on 0.0.0.0 (trying it only) | off |
| `KEEPA_API_KEY` | Barcode and ASIN lookup (1 Keepa token per new code, cached forever) | none: UPCitemdb's free tier |

AI settings are in the AI section below.

## Connect your accounts

An admin does all of this in the app under **Settings, Connections**. Each card shows the addresses to copy into the marketplace's developer site, a form for the keys, and a Test button that makes one read-only call. Keys are saved in `DATA/secrets/connections.json` (mode 600), never in the database or its backups.

Amazon and eBay need the app on its public HTTPS address first. They won't send you back to `localhost`.

### Amazon (SP-API)

You need a Professional seller account and an approved developer profile.

1. In Seller Central: **Apps and Services, Develop Apps**. The first time, fill in the developer profile. Pick "private developer" (an app for your own account only). Amazon takes from a day to a few weeks to approve it.
2. **Add new app client.** API type: SP API. Roles: Orders, Reports, Inventory and Order Tracking, Product Listing (Amazon's role names change now and then; pick the closest).
3. Edit the app and paste the 2 addresses from the app's Amazon card: **OAuth Login URI** (`https://<your address>/api/amazon/login`) and **OAuth Redirect URI** (`https://<your address>/api/amazon/callback`).
4. Copy 3 values onto the Amazon card: the App ID (starts with `amzn1.sp.solution.`), the LWA Client ID (starts with `amzn1.application-oa2-client.`) and the LWA Client Secret (starts with `amzn1.oa2-cs.v1.`, shown under "View" next to LWA credentials). Save, then **Connect Amazon** and approve on Amazon's page.

Orders sync every 15 minutes; listings, buyer returns and selling approval every hour.

### eBay

1. Make an account at [developer.ebay.com](https://developer.ebay.com). Under **Application Keysets**, create a Production keyset.
2. eBay asks how you handle account deletion notices before the keyset works. Pick the notification option and paste 2 values from the app's eBay card: **Account deletion endpoint** and **Verification token** (the app makes the token; copy it from the card). eBay checks the endpoint right away, so the app must be online.
3. **User Tokens, Get a Token from eBay via Your Application, Add eBay Redirect URL.** That makes a RuName: eBay's name for "where to send the seller after they approve the app". Set its "Your auth accepted URL" to the card's **Auth accepted URL**. eBay also wants a privacy policy URL; any page of yours works.
4. Copy the App ID (Client ID), Cert ID (Client Secret) and RuName (looks like `Your_Name-YourApp-PRD-abcdef`) onto the card. Save, then **Connect eBay**.

### Walmart Marketplace

In Walmart Seller Center, **Settings, API Key Management**, make a Client ID and Client Secret and paste them. For now this only tests the connection. Walmart sales go in as CSV (Orders, Import orders).

### Gmail (store orders)

Turn on 2-step sign-in on the Google account, make an app password, and paste it with the address and the last 4 digits of the card you buy inventory with. The app reads order, shipping and cancellation emails (read-only IMAP), keeps only orders paid with that card, and puts each one on Arriving for a person to approve. It needs an AI key (below).

An app password can read the whole mailbox. Use a mailbox that gets your store orders and not much else, if you can.

## AI (optional)

Two jobs use AI, both on a short leash. For store emails, code finds the candidate order numbers, amounts and item lines first, and the model only picks among them, so it can't invent a number. For photos, one picture of a box gives name, brand and barcode digits; digits are used only when their check digit passes.

| Provider | Key | Store emails | Photos |
|---|---|---|---|
| Anthropic | `ANTHROPIC_API_KEY` (and `pip install anthropic`) | yes | yes |
| OpenAI | `OPENAI_API_KEY`, plus `BOXLOFT_AI_MODEL` | yes | yes |
| TypeSafe | `TYPESAFE_API_KEY` | yes | no |
| Gemini | `GEMINI_API_KEY` | no | yes |

With no key, store emails aren't read and New product takes a typed name. Everything else works.

Picking: `BOXLOFT_AI_PROVIDER` (store emails) and `BOXLOFT_PHOTO_PROVIDER` (photos) name a provider; left empty, the first key that's set wins (emails: TypeSafe, Anthropic, OpenAI; photos: Gemini, Anthropic, OpenAI). `BOXLOFT_AI_MODEL` overrides the Anthropic model (default claude-opus-5-5) and is required for OpenAI. `GEMINI_MODEL` and `OPENAI_BASE_URL` (any OpenAI-compatible server) are there too. The Anthropic and OpenAI paths are covered by tests with a fake model; the original warehouse runs on TypeSafe and Gemini.

## The Chrome extension (optional)

Amazon's API doesn't tell a buyer when their purchases arrive. The extension in `extension/` does: on a computer that stays on, it reads your own Amazon Your Orders pages, each package's Track page, and your Walmart order pages, and sends them to your server, which parses them (`backend/pages.py`).

It's not on the Chrome Web Store. Load it yourself:

1. Open `extension/manifest.json` and add your address to the `host_permissions` list, with `/*` on the end:

   ```json
   "host_permissions": ["https://www.amazon.com/*", "https://www.walmart.com/*", "https://wms.yourdomain.com/*"],
   ```

2. In Chrome go to `chrome://extensions`, turn on Developer mode (top right), click **Load unpacked** and pick the `extension` folder. After any later edit to its files, click the reload arrow on its card there.
3. In the app: **Settings, Amazon sync**, make a token (it starts with `bl_` and shows once).
4. Click the puzzle-piece icon in Chrome's toolbar and pin the extension. Click its icon, paste your address and the token, Save, then Sync now. Stay signed in to Amazon in that Chrome.

Its own safety rules live in the extension (`sync.js`), so your server can't loosen them: a fixed list of URL patterns it will open, a fixed pace, at most 1,500 Amazon pages per run, and it stops a site on any sign-in, captcha or robot-check page. It never clicks or buys. The server adds 2 more: runs at least 2 hours apart, and none from 10 PM to 6 AM (`backend/pagesync.py`).

**Read this before you use it.** It reads pages of your own signed-in accounts with your own browser. Amazon's and Walmart's terms limit automated access to their sites, and an account flag is your risk. Keep the pace as it is.

## Security notes

- Marketplace keys and the Gmail app password sit in plain text in `DATA/secrets/connections.json` on the server (mode 600). Anyone with root on the server can read them.
- Sign-in locks after 5 wrong tries from one address for 15 minutes. Passwords are hashed (PBKDF2, 600,000 rounds). Sessions last 30 days.
- The server listens on 127.0.0.1 only and trusts the proxy in front of it for the visitor's address. Keep Caddy (or your proxy) on the same machine.
- Found a hole? See `SECURITY.md`.

## Words you'll see

| Word | Meaning |
|---|---|
| FBA / FBM | Fulfilled by Amazon (Amazon holds and ships the stock) / fulfilled by merchant (you ship it) |
| 3PL | A warehouse that stores and ships another business's stock |
| ASIN | Amazon's 10-character item number (B0...) |
| SP-API | Amazon's Selling Partner API, the one for sellers |
| LWA | Login with Amazon, the sign-in that SP-API apps use |
| RuName | eBay's name for the address a seller returns to after approving your app |
| IMAP | The standard way to read email from a server |
| Caddy | The web server in front of the app; it gets the HTTPS certificate |
| systemd | Linux's service manager, which keeps the app running without Docker |
| venv | A Python folder of packages just for this project (`.venv`) |

## Working on it with a coding agent

`CLAUDE.md` holds the rules that keep the numbers right: the append-only ledger, how undo works, the 409 check for stale screens, and which queries count "units still coming". Point your agent at it before any change, and run the tests after. The comments name Alex (the owner) and Sam (floor staff), the 2 people the app was built around, and the dates are when each rule was learned.

## License

MIT. See `LICENSE`.
