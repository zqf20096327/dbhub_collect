<a id="top"></a>

<p align="center"><img src="web/public/favicon.svg" width="96" alt="Hati logo"></p>
<h1 align="center">Hati</h1>
<p align="center">A shared expense splitter with live balances.</p>

<p align="center">
  <a href="https://github.com/Jevoel16/Hati/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/Jevoel16/Hati/ci.yml?branch=main&label=CI&style=flat" alt="CI status"></a>
  <img src="https://img.shields.io/badge/version-1.0.0-blue?style=flat" alt="Version 1.0.0">
  <img src="https://img.shields.io/badge/platform-web-lightgrey?style=flat" alt="Platform: web">
  <img src="https://img.shields.io/badge/React-19-blue?style=flat" alt="React 19">
</p>

<p align="center"><img src="docs/images/hero.png" width="100%" alt="Group page: the amount you are owed with Add expense and Record payment on the left, everyone's balance and the fewest payments to settle up with Show QR buttons on the right"></p>

<p align="center">
  <a href="#about">About</a> · <a href="#screenshots">Screenshots</a> · <a href="#features">Features</a> · <a href="#tech-stack">Tech Stack</a> · <a href="#architecture">Architecture</a> · <a href="#getting-started">Getting Started</a> · <a href="#configuration">Configuration</a> · <a href="#usage">Usage</a> · <a href="#more">More</a>
</p>

---

## About

Hati (Filipino for "to split") is for housemates, project groups and friends who share costs and are tired of tracking them in a group chat. Everyone in a group records what they paid, Hati works out who owes whom to the centavo, and every member sees the balances change the moment an expense is added. It keeps records only and never moves money. Built as the ITE183 final project; the reasoning behind its main choices is in [docs/decisions.md](docs/decisions.md).

## Screenshots

<details>
<summary><b>Screenshots</b></summary>

<table>
  <tr>
    <td width="50%" align="center"><b>Pay with a QR</b><br><a href="docs/images/payment-qr.png"><img src="docs/images/payment-qr.png" width="100%" alt="Payment dialog: Dana Lim pays you 3,399.84 pesos, with a choice between GCash and Landbank above the QR code, and Share and Download buttons"></a></td>
    <td width="50%" align="center"><b>Your groups</b><br><a href="docs/images/groups.png"><img src="docs/images/groups.png" width="100%" alt="Groups list beside the forms to start a group or join one by code or by scanning a QR code"></a></td>
  </tr>
  <tr>
    <td width="50%" align="center"><b>Sign in</b><br><a href="docs/images/sign-in.png"><img src="docs/images/sign-in.png" width="100%" alt="Sign-in page with Google and GitHub buttons with their logos, a theme switch, and an email and password form"></a></td>
    <td width="50%" align="center"><b>Expenses</b><br><a href="docs/images/expenses.png"><img src="docs/images/expenses.png" width="100%" alt="Expenses tab listing each expense with its date, category, who paid, your share and the amount"></a></td>
  </tr>
  <tr>
    <td width="50%" align="center"><b>Dark mode</b><br><a href="docs/images/dark-mode.png"><img src="docs/images/dark-mode.png" width="100%" alt="Group balances in dark mode"></a></td>
    <td width="50%" align="center"><b>Phone (light and dark)</b><br><a href="docs/images/phone.png"><img src="docs/images/phone.png" width="100%" alt="Group balances at phone width, in light mode on the left and dark mode on the right"></a></td>
  </tr>
</table>

</details>

## Features

- Groups you join with an invite link, a code or by scanning its QR code, with admins and members
- A currency for each group, picked when it is created (Philippine peso by default, or USD, EUR, JPY, SGD, KRW or HKD), with no conversion
- Expenses split equally, by exact amounts or by percentage
- Each member's balance, and the fewest payments that settle the whole group
- Balances and an activity feed that update live, with no refresh
- Payment QRs in peso groups: save up to 5 InstaPay QRs (GCash, Maya, Landbank or any bank), and the people who owe you pick one and get it with the exact amount filled in
- Recorded payments that adjust everyone's balance
- Spending summary by category and by month, and any month downloaded as a CSV expense report
- Sign-in with Google or GitHub, plus a public demo account
- A username and password chosen on first sign-in
- A short guided tour for first-time users (start a group, add an expense, read balances, settle up) that can be skipped or replayed from the account page
- A layout that uses the full width on desktop and phones, a system, light or dark theme switch and full keyboard access
- Landing page with How it works, Features and Questions pages linked from its footer

## Tech Stack

| Layer     | Tools                                                                          |
| --------- | ------------------------------------------------------------------------------ |
| Front end | React 19.3.1, React Router 7.18.5, Vite 8.3.8, plain CSS                       |
| QR codes  | qrcode-generator 2.0.4 (drawing), jsQR 1.4.0 (camera and photo scanning)       |
| Back end  | Node.js 26.13.1, Express 5.3.0, ws 8.23.0, Zod 4.6.7, TypeScript 6.0.3         |
| Database  | MySQL 8 locally, TiDB Cloud deployed, through mysql2 3.24.6                    |
| Hosting   | Vercel (static site, API and WebSocket in one function), TiDB Cloud            |
| Analytics | Vercel Web Analytics through @vercel/analytics 2.0.1                           |
| Tooling   | node:test through tsx 4.23.15, ESLint 10.15.0, Prettier 3.10.1, GitHub Actions |

## Architecture

```mermaid
flowchart LR
  browser["Browser<br/>landing pages + React app"] -->|"pages"| static["Vercel static files"]
  browser <-->|"REST /api/* and WebSocket /api/ws"| fn["One Vercel Function<br/>Express + ws"]
  fn -->|mysql2| db[("TiDB Cloud")]
  fn --> oauth["Google / GitHub OAuth"]
  cron["Vercel Cron, daily"] --> fn
```

- The site, API and WebSocket share one origin, so the session cookie is first-party and there is no CORS.
- On the server, routes call services and services call the data layer; the money math is pure functions in `server/src/domain`.
- Every write also adds a row to `group_events`; each instance polls it every second and tells its sockets "this group changed", and the browser refetches.
- Amounts are whole numbers in the group currency's smallest unit (centavos, yen) everywhere, so shares and balances always add up exactly.

The full write-up, with the request path, live updates, auth, data model and front end: [docs/architecture.md](docs/architecture.md).

## Getting Started

You need Node.js 26 and MySQL 8 (Workbench) with an empty `hati` database and a user for it.

```bash
npm install
cp .env.example .env   # then fill in DATABASE_URL and JWT_SECRET
npm run migrate
npm run seed
npm run dev
```

Open http://localhost:5173 and use "Open the demo".

## Configuration

All settings are environment variables; [.env.example](.env.example) lists them for local, development and production use.

<details>
<summary>Environment variables</summary>

| Variable                                   | Required   | Purpose                                                          |
| ------------------------------------------ | ---------- | ---------------------------------------------------------------- |
| `NODE_ENV`                                 | no         | `development`, `test` or `production`                            |
| `PORT`                                     | no         | API port for local development (default 3000)                    |
| `APP_URL`                                  | yes        | Public address of the site; used for OAuth callbacks and SEO     |
| `DATABASE_URL`                             | yes        | `mysql://` connection string (MySQL 8 locally, TiDB deployed)    |
| `TEST_DATABASE_URL`                        | tests only | A MySQL or TiDB server where tests may create and drop databases |
| `JWT_SECRET`                               | yes        | At least 32 random characters; signs the session cookie          |
| `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET` | no         | Turns on Google sign-in                                          |
| `GITHUB_CLIENT_ID`, `GITHUB_CLIENT_SECRET` | no         | Turns on GitHub sign-in                                          |
| `CRON_SECRET`                              | production | At least 16 characters; protects the daily maintenance route     |

</details>

## Usage

1. Sign in with Google or GitHub and choose a password, or open the demo.
2. Create a group and send its invite link or QR code to the others; they can scan it from Join a group.
3. Optionally add the InstaPay QR of each wallet or bank you use on the Account page, so people who owe you can pay the exact amount.
4. Add expenses as they happen and pick how each one is split.
5. Check the Balances tab for the fewest payments that settle up, use Show QR to pick one of the payee's QRs and pay or share it, and record each payment once it is made.

Guides: [Architecture](docs/architecture.md) · [API reference](docs/api.md) · [Deploying to Vercel](docs/deploy.md) · [Security](docs/security.md) · [State machines](docs/state-machines.md) · [Performance](docs/performance.md)

## More

<details>
<summary>Project structure</summary>

```
api/       Vercel Function entry (re-exports the server)
server/    Express API: routes -> services -> data layer, plus pure money logic
web/       React app and the static landing page
docs/      Decisions, API, security, state machines, deployment
docker/    Dockerfiles for the web, API and database containers
```

</details>

<details>
<summary>Scripts</summary>

| Script              | What it does                                     |
| ------------------- | ------------------------------------------------ |
| `npm run dev`       | API on port 3000 and web app on port 5173        |
| `npm run build`     | Builds the web app into `public/`                |
| `npm start`         | Runs the API without watching for changes        |
| `npm test`          | Unit tests, plus API tests when a test DB is set |
| `npm run typecheck` | Type-checks the server and the web app           |
| `npm run lint`      | ESLint                                           |
| `npm run format`    | Prettier                                         |
| `npm run migrate`   | Applies database migrations                      |
| `npm run seed`      | Creates or resets the demo account               |

</details>

<p align="right"><a href="#top">Back to top</a></p>
