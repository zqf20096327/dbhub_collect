# Rust BT Sniffer

English | [简体中文](README.zh-CN.md)

**Tune into the public BitTorrent DHT network — and walk away with magnet links that actually download.**

BitTorrent has no central server: it's a peer-to-peer market where everyone trades directly, and the public DHT acts as the shared directory. A magnet link is just a shopping list — the file names, the sizes, and directions to the people sharing them. Rust BT Sniffer sits at the market and:

1. **Listens.** It records the magnet links being traded on the DHT — over a thousand per minute, no trackers, no accounts, no crawling. (Each link is just a short fingerprint of a torrent, never the files themselves.)
2. **Reads the label.** For every link it finds the people sharing it, downloads the `.torrent` metadata, verifies the hashes, and files it into a full-text-searchable library.
3. **Checks the goods are real.** This is the part most tools skip. Plenty of "hot" torrents are 99% ads: the ad file is seeded but the actual files have zero seeders, so you only ever download the ads. The built-in dead-torrent filter analyzes the peers' bitfields and spot-checks pieces by downloading them, and keeps the dead ones out of your library.

The result: a database of *usable* magnets — searchable through a built-in web dashboard, exposed as a REST API, running as a single ~18 MB binary with no dependencies.

![WebUI dashboard](screenshot.png)
*WebUI dashboard: live stat cards, inbound rate and bandwidth charts, CPU / memory usage, runtime status.*

## What it's for

- **Finding what's out there** — a live, filterable map of what the DHT is talking about right now, not a stale index.
- **Building a magnet library** — every collected torrent gets its metadata (name, files, sizes, trackers) and lands in a local SQLite library with Chinese / Japanese / English full-text search.
- **Not wasting bandwidth on dead torrents** — the integrity probe rejects "ad-only" torrents and forged bitmaps before they enter your library, so you don't spend a night downloading files nobody is seeding.

## Features

- **Single binary, pure Rust** — one statically-linked executable; the WebUI is embedded, no runtime dependencies. Windows + Linux.
- **Dual-stack passive DHT sniffing** — IPv6-first (BEP-32) with IPv4 (BEP-5); collects infohashes from inbound `get_peers` / `announce_peer`; BEP-42 node IDs; BEP-51 `sample_infohashes` active sampling (on by default, configurable); routing tables persist across restarts.
- **BTv1 / BTv2 metadata fetching** — v1 via BEP-9/BEP-10 `ut_metadata`, v2 via BEP-52; multi-peer racing, hash verification before storage; hybrid magnets get both `btih` and `btmh`.
- **Dead-torrent filter** — two-stage integrity probe: v1 bitfield-coverage analysis (zero extra connections) flags ad-only torrents whose real files have no seeders; v2 spot-check sampling actually downloads a few pieces and verifies SHA-1 to expose forged all-ones bitmaps. Insufficient evidence never kills a torrent — the filter is deliberately pass-biased. Design: [docs/probe-plan.md](docs/probe-plan.md).
- **SQLite storage + FTS5 full-text search** — WAL mode, batched single writer; trigram index for CJK; whitelisted query syntax (`AND`/`OR`/`NOT`, `"phrase"`, `cat:` `ext:` `size:` `files:` `after:` `before:`) with BM25 ranking and snippets.
- **Embedded WebUI** — live dashboard (1 Hz SSE), search, torrent detail, heat ranking, settings page with config hot reload, dark/light theme, mobile adaptation.
- **REST API + readiness probe** — everything is JSON; `/api/health` returns 200 / 503 for monitoring.
- **Token auth & security hardening** — loopback always token-free; empty-token LAN mode; public clients rejected; per-IP rate limiting (IPv6 aggregated by /64), bounded search input, Host allowlist (anti DNS-rebinding), CSRF checks.
- **Outbound proxy channel** (off by default) — SOCKS5 (TCP CONNECT + UDP ASSOCIATE) / HTTP CONNECT with built-in split routing: only non-mainland-China addresses go through the proxy, for international DHT bootstrap and fetching.
- **UDP trackers (BEP-15)** — `udp://` tracker URLs work out of the box (direct or SOCKS5 UDP relay) and feed the routing table on cold start.
- **Storage-driven maintenance** — 20 GB database cap by default, evicting lowest-heat entries first; optional time retention; periodic cleanup / vacuum / FTS optimize / WAL checkpoint; automatic backups (`[backup]`, off) and alert webhooks (`[alert]`, off).
- **Ops niceties** — per-peer/IP fetch quota (`[peer_quota]`, off), public search-only listener (`[web.public]`, off), public connectivity self-checks (`[selfcheck]`, off), TP-Link router WAN IPv6 tracking (`[router]`, off), rolling file logs (`[log]`, off), offline database merge (`sniffer merge`), synthetic benchmark seeding (`sniffer bench-seed`).

## How It Works

Think of the DHT as a giant shared phone book with no owner: every BitTorrent client holds a slice of it and answers questions. The sniffer joins this network and (mostly) listens — it records the infohashes other nodes ask about and announce. New infohashes pass a Bloom-filter dedup and a bounded queue, then metadata workers connect to the torrent's peers and download just the `.torrent` info dictionary (**never file content**) via the BEP-9 extension protocol — racing several peers and verifying hashes before writing. The dead-torrent filter runs on each successful fetch: peers' bitfields reveal which pieces are claimed to exist, and spot-check sampling turns claims into verified evidence. Everything lands in a single SQLite database that the WebUI and REST API search.

```
        Mainline DHT network (IPv6 + IPv4)
          │  inbound get_peers / announce_peer (passive sniffing)
          │  BEP-51 sample_infohashes (active sampling, optional)
          ▼
   bounded infohash queue ──▶ Bloom dedup + DB primary-key dedup
          ▼
   metadata fetch workers  (collect_peers → race fetch → hash verify, BTv1/v2)
          ▼
   dead-torrent filter  (bitfield coverage → spot-check sampling)
          ▼
   SQLite (WAL, single writer) + FTS5 index
          ├──▶ embedded WebUI (dashboard / search / settings)
          └──▶ REST API

Outbound traffic to non-CN addresses is routed through the proxy channel
(SOCKS5 / HTTP CONNECT) for international bootstrap and fetching.
```

## Quick Start

Requirements: a stable Rust toolchain (**1.85+**, the MSRV of clap 4.6).

```bash
git clone https://github.com/yuunnn-w/Rust-BT-Sniffer
cd Rust-BT-Sniffer
cargo build --release                      # binary: target/release/sniffer (sniffer.exe on Windows)
cp config.example.toml config.toml         # Windows: copy config.example.toml config.toml
./target/release/sniffer serve             # reads ./config.toml; built-in defaults if missing
```

- The server reads `config.toml` from the working directory; if missing it starts with built-in defaults (a WARN is logged). `config.example.toml` is the fully annotated default reference.
- WebUI: <http://127.0.0.1:8080> (default bind `0.0.0.0:8080`; loopback and LAN clients are token-free).
- CLI search: `sniffer search <keyword>` (same whitelisted query syntax as the WebUI).
- Other subcommands: `sniffer merge --source <db>` (offline-merge another machine's database, service must be stopped), `sniffer bench-seed <N> [--bench]` (seed synthetic records, optionally run the search benchmark). See `sniffer --help`.
- On Windows the DHT needs the inbound UDP port allowed through the firewall (default 5000), otherwise sniffing yields nothing — see [deploy/windows-firewall.md](deploy/windows-firewall.md).

## Configuration

Every key has a built-in default; [config.example.toml](config.example.toml) documents each one with comments, defaults, and hot-reload flags (hot keys apply on save from the settings page, non-hot keys need a restart). The core sections:

| Section | What it controls | Default highlights |
|---|---|---|
| `[net]` | UDP listen port, dual-stack switches | `port = 5000`, IPv4+IPv6 |
| `[web]` / `[web.public]` | WebUI + REST API bind, tokens, public search-only listener | `0.0.0.0:8080`; public listener off |
| `[dht]` | BEP-51 sampling, routing-table persistence | sampling on (30 s / 96 nodes) |
| `[limits]` | outbound UDP PPS, routing capacity, queue size | 800 PPS, 8192 nodes/table |
| `[metadata]` | fetch workers/concurrency, probe_* dead-torrent filter keys | 64 workers, 50 fetch PPS |
| `[store]` | SQLite path, write batch, low-disk guard, page cache | `sniffer.db` |
| `[dedup]` | Bloom filter sizing | 20M entries (~24 MB), hard cap 64M |
| `[maintenance]` / `[backup]` / `[alert]` | retention & storage cap, backups, webhooks | 20 GB cap; backup & alert off |
| `[proxy]` | SOCKS5 / HTTP CONNECT outbound channel + CN split routing | off |
| `[bootstrap]` / `[tracker]` | DHT bootstrap nodes, DoH resolvers, tracker seeding | built-in lists |

## Performance

Measured on Windows 11 x86_64 (Intel Core Ultra 7 258V, 8 logical cores, 32 GB RAM), rustc 1.97.0, `--release --offline`:

| Item | Measured |
|---|---|
| Clean release build | 220 s (`cargo build --release --offline`) |
| Binary size | 13.5 MB (14,138,880 B) |
| Test suite | 336 passed / 0 failed (3 ignored), `cargo test --offline` |
| Test wall time | 117 s incl. building test binaries; 58 s re-run with binaries cached |
| Threads | 53–55 |
| Working set (120 s run) | ~29 MB right after startup; 61–76 MB during the initial crawl; ~70–76 MB steady |
| Private memory (120 s run) | ~40 MB at startup; ~57–60 MB steady |
| CPU (120 s run) | ~55–65% of one core during the bootstrap crawl (≈7–8% of an 8-core machine) |
| Outbound DHT queries | 69,634 in 120 s (~580/s; limit 800/s, 0 dropped by the token bucket) |
| Routing table | 8192 nodes (v4, at capacity cap) + 68 nodes (v6) after 120 s |
| Inbound queries | 954 in 120 s (68 v4 / 886 v6) |
| Infohashes collected | 2,629 new in 120 s; BEP-51 sampling saw 2,523 hashes (2,303 new) |
| Metadata fetches | 3 ok / 468 failed (both direct channels hit the cooldown — proxy-less test network, see [FAQ](#faq)) |

Notes: this is a **120-second cold-start window** on a consumer laptop — the bootstrap crawl and tracker ping bursts dominate CPU and traffic; long-run steady state is quieter. No inbound firewall rule was added for the test port, so passive inbound sniffing is underrepresented here.

### Linux server measurements

Measured on a 5-core x86_64 Linux server (10.8 GiB RAM, Ubuntu Server), rustc 1.98.0, same `--release --offline` build, run as an isolated instance (separate ports and database) alongside the production service:

| Item | Measured |
|---|---|
| Clean release build | 97 s (5 cores parallel) |
| Binary size | 17.7 MB (17,691,344 B) |
| RSS over a 120 s cold start | ~16 MB right after startup → ~60 MB during the crawl → ~70 MB steady at the end |
| Peak RSS (VmHWM) | 70 MB |
| CPU (120 s run) | ~5% of one core on average; higher during the bootstrap crawl |
| Peak thread count | ~200 (mostly idle blocking-pool stacks, not paged into RAM) |
| Outbound DHT queries | 63,502 in 120 s (~529/s; limit 800/s, token bucket dropped 0) |
| Routing table | 8192 nodes (v4, at capacity) + 83 nodes (v6) after 120 s |
| Inbound queries | 964 in 120 s (75 v4 / 889 v6) |
| Infohashes collected | 2,416 new in 120 s |
| Metadata fetches | 6 ok / 407 failed (proxy-less network — both direct channels stayed in cooldown, see [FAQ](#faq)) |
| Queue overflow | 0 (depth stayed well below the 10,000 cap) |

Notes: same 120-second cold-start window on a server; the bootstrap crawl and BEP-51 sampler dominate the early phase. A long-running production instance on the same host measured ~82 MB RSS after 2.5 minutes, queue depth 1,556/10,000, zero drops. Values are consistent with the Windows measurements above — the fixed costs (Bloom filter, routing tables) dominate the footprint.

## FAQ

**What's a DHT? Why do you get 2,400 magnets in two minutes without a tracker?**
The DHT is the BitTorrent network's own shared directory — a distributed hash table run collectively by every client, with no owner and no single point of failure. Clients look each other up in it. The sniffer joins as a normal node and listens to the traffic: it sees the infohashes other nodes are asking about and announcing. That's why no trackers, accounts, or crawling are involved.

**What's a magnet link? Have you downloaded the files?**
A magnet link is a compact identifier for a torrent (a 20-byte infohash plus optional names). No — the program never downloads file content. At most it fetches the `.torrent` info dictionary (names, sizes, piece layout) from peers, which is what a BitTorrent client would download first anyway. The database holds magnets and metadata, not files.

**What does "dead torrent" mean, and how is it detected?**
A torrent whose real files nobody is seeding — the classic "ad-only" setup: one small ad file is widely shared, the actual files have zero seeders, and you end up downloading nothing but ads. Stage 1 (v1) analyzes the peers' bitfields during the metadata handshake — zero extra connections. If at least `probe_min_peers` (2) consistent bitfields show real-file coverage below `probe_file_threshold` (0.30) and un-downloadable bytes exceed `probe_dead_ratio` (0.50), it's rejected and not retried for `probe_dead_ttl_secs` (24 h). Stage 2 (v2, `probe_max_samples` = 8) actually downloads a few claimed pieces and verifies their SHA-1, catching forged all-ones bitmaps. The design is deliberately pass-biased: insufficient evidence never kills a torrent. Stage 1 dead torrents are dropped before any sampling budget is spent. Full design: [docs/probe-plan.md](docs/probe-plan.md).

**Will I be detected or tracked for running this?**
Sniffing is passive: inbound queries arrive at your port and are recorded; your node participates in the DHT like any client. If you advertise a public address or enable active sampling / self-checks, your node makes outbound DHT requests like every client does — nothing distinguishes it from a normal BitTorrent client. The WebUI can run token-free on loopback only.

**What memory should I expect?**
The Bloom dedup filter dominates: it is sized from the live database row count at startup (floor 20M entries ≈ 24 MB, hard cap 64M ≈ 77 MB). The infohash queue is bounded (10,000), fetch concurrency is capped (64 workers / 50 PPS), and SQLite page cache is adaptive (4–64 MB). A fresh 2-minute run measured ~70–76 MB working set on Windows and ~70 MB on Linux; expect well under 200 MB on a populated database.

**Why do metadata fetches keep timing out / entering "cooldown" without a proxy?**
The fetch path has two direct-connection channels (CN / non-CN) with automatic health tracking: after 12 consecutive timeouts a channel cools down and is skipped, with a few probe connections released periodically (every 600 s) to detect recovery. This protects the fetch budget when direct international connectivity is poor. Enabling `[proxy]` routes non-CN traffic through your proxy instead. The cooldown only affects metadata fetching, not sniffing itself.

**Does it work behind NAT / without a public IP?**
Yes — sniffing and fetching work fine; only the public-search address display and the public self-checks degrade. The address chain's external probe level shows your NAT egress IP.

**Why is my sniffing rate zero on Windows?**
The inbound UDP port (default 5000) must be allowed through Windows Firewall, and many ISP modems also filter inbound IPv6 — see [deploy/windows-firewall.md](deploy/windows-firewall.md) for the rules and a troubleshooting checklist.

## Deployment

**Linux (systemd)**: unit file at [deploy/sniffer.service](deploy/sniffer.service). One-time install:

```bash
sudo useradd -r -s /usr/sbin/nologin sniffer
sudo mkdir -p /opt/sniffer   # put the sniffer binary and config.toml here
sudo chown -R sniffer:sniffer /opt/sniffer
sudo cp deploy/sniffer.service /etc/systemd/system/sniffer.service
sudo systemctl daemon-reload && sudo systemctl enable --now sniffer
```

The unit sets `LimitNOFILE=65536`, `MemoryHigh=1G`, `MemoryMax=2G`, `OOMScoreAdjust=-100` — headroom far above the measured steady-state footprint. Logs go to journald (`journalctl -u sniffer -f`). To restart or upgrade, use `systemctl restart sniffer`, **not** the WebUI hot-restart (`POST /api/control/restart` spawns a child process outside systemd's supervision).

**Windows**: see [deploy/windows-firewall.md](deploy/windows-firewall.md) — firewall rules for the inbound UDP port, plus Task Scheduler / NSSM autostart recipes.

**Firewall / IPv6 in general**: the DHT needs inbound UDP (e.g. `sudo ufw allow 5000/udp`); the optional public search listener (`[web.public]`, default 8081) needs inbound TCP, and for IPv6 typically router/modem-side forwarding as well.

## Contributing

Issues and PRs are welcome. Code comments are primarily in Chinese. Before submitting, please run:

```bash
cargo test
cargo clippy --all-targets -- -D warnings
```

## Disclaimer

> **This project is for learning and research purposes only.** Users must comply with the laws and regulations of their country or region. The DHT network is a public protocol: all sniffed information is data already publicly propagated on the network. The program only records infohashes and torrent metadata; it does not download, store, or distribute any file content. The authors assume no liability for how users use this software.

## License

GPL-3.0-only — see [LICENSE](LICENSE).
