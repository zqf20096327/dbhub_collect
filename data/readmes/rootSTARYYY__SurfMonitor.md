<p align="center">
  <img src="build/icon.png" alt="Surf Monitor Logo" width="72" />
</p>

<h1 align="center">Surf Monitor (v4.2.1)</h1>

<p align="center">
  A local-first Windows desktop infrastructure, website, and remote Linux VPS monitoring suite built with <strong>Electron 33</strong>, <strong>React 18</strong>, <strong>TypeScript</strong>, <strong>Vite</strong>, <strong>Tailwind CSS</strong>, <strong>Recharts</strong>, and <strong>SQLite (<code>better-sqlite3</code>)</strong>.
</p>

<p align="center">
  <img src="screenshots/panel.png" alt="Surf Monitor Overview Dashboard" width="900" />
</p>

---

## Key Features

### Website, Protocol & Dependency Monitoring
- **Three-State Health Classification (`UP`, `DEGRADED`, `DOWN`)**: Separates network reachability from HTTP application health using configurable expected status code expressions (`200-399` default), JSONPath/text/latency assertions, and retries.
- **Multi-Protocol Checks**: HTTP/HTTPS (`GET`, `HEAD`, `POST`, `PUT`, `PATCH`, `DELETE`, `OPTIONS`), SSL/TLS certificate expiry, DNS record resolution, TCP port checks, ICMP ping, keyword matching, local heartbeat receiver (`127.0.0.1:45821`), content diffing, and domain RDAP expiry.
- **Website Intelligence**: Redirect chain analyzer, security header grading, and broken-link crawler with SSRF protection.
- **Groups, Services & Dependency Map**: Organize monitors into groups, model service dependencies with cycle detection, and inspect root-cause propagation.
- **Maintenance Windows**: Schedule immediate or future maintenance windows (`30m`, `1h`, `4h`, `24h`, or custom) per monitor or globally, with live countdowns and early termination.

### Remote Linux Infrastructure, Docker, systemd & PM2
- **Authenticated Localhost Agent (`agent/surf-agent.mjs`)**: Binds strictly to `127.0.0.1:47200` on the remote Linux VPS and communicates exclusively over an SSH `forwardOut` tunnel with constant-time Bearer token verification.
- **1-Click SSH Installer & Upgrader (`agent/install.sh`)**: Installs the unprivileged `surfagent` systemd service, Docker socket access, and `/usr/local/bin/surf-pm2-helper` with least-privilege `/etc/sudoers.d/surf-monitor-agent` rules directly from **Add Server** or **Server Details → Update Agent**.
- **Multi-User PM2 Monitoring & Control**: Automatically discovers PM2 installations across `root` and regular Linux users, collects CPU/memory/uptime/restart metrics, streams redacted `stdout`/`stderr` logs, detects unexpected stops or restart spikes, and supports allowlisted `start`, `stop`, and `restart` actions with audit logging.
- **Server Editing**: Update host, SSH port, username, poll interval, thresholds, or credentials on existing servers without recreating them.

### Notifications & SMTP Overhaul
- **Channels**: Discord webhooks, Telegram bots, Custom Webhooks, Windows Desktop notifications, and **SMTP Email**—all credentials encrypted at rest using Electron `safeStorage`.
- **SMTP Provider Presets**: Built-in presets for **Brevo** (`smtp-relay.brevo.com:587`), **Gmail** (`smtp.gmail.com:587`), **Outlook / Office 365** (`smtp.office365.com:587`), and **Custom SMTP**, supporting `STARTTLS`, `Implicit TLS/SSL` (port 465), unauthenticated relays, **Test Connection**, and **Send Test Email**.

### Licensing & Desktop Integration
- **100% Free & Local-First**: No license keys, trials, or external accounts required—with a 5-slide first-launch introduction and personalized greeting.
- **Native Splash & System Tray**: 10-stage startup progress splash screen, Windows AppUserModelId notification identity (`com.surfmonitor.app`), minimize-to-tray, WAL backups, and JSON/CSV exports.

---

## Screenshots

### Monitors & Heartbeats
| Monitors | Heartbeat Monitors |
| :---: | :---: |
| ![Monitors](screenshots/monitor.png) | ![Heartbeat Monitors](screenshots/heartbeatmonitors.png) |

### Remote Servers & Telemetry
| Remote Servers | Server Details |
| :---: | :---: |
| ![Remote Servers](screenshots/servers.png) | ![Server Details](screenshots/serverdetail.png) |

### PM2 Process Monitoring & Log Viewer
| PM2 Processes | PM2 Process Details & Logs |
| :---: | :---: |
| ![PM2 Processes](screenshots/pm2.png) | ![PM2 Process Details](screenshots/pm2details.png) |

### Settings & Configuration
<p align="center">
  <img src="screenshots/settings.png" alt="Surf Monitor Settings" width="850" />
</p>

---

## Tech Stack & Architecture

| Layer | Technology |
| --- | --- |
| Desktop Shell | Electron 33 (`contextIsolation: true`, `nodeIntegration: false`, `sandbox: true`) |
| Frontend | React 18, TypeScript, Vite, Tailwind CSS, Lucide Icons, Recharts |
| Persistence | SQLite (`better-sqlite3`, WAL mode, foreign keys, 31 tables) |
| Remote Tunnel | `ssh2` SFTP + `forwardOut` + `agent/surf-agent.mjs` |
| Email Transport | `nodemailer` with TLS verification & error classification |
| Testing | Vitest, ESLint 9, TypeScript (`tsc`) |

---

## Getting Started (Windows)

```powershell
npm install
npm run typecheck
npm run lint
npm test
npm run dev
```

> **Note:** `postinstall` runs `electron-builder install-app-deps` to compile `better-sqlite3` for Electron. If you switch Node or Electron versions, run `npm run rebuild`.


---

## Building the Windows Installer

```powershell
npm run build:win
```

Outputs the NSIS installer (`Surf Monitor-Setup-4.2.1.exe`) into `release\`, using `build\icon.ico` and `build\icon.png`.
