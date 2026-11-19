<div align="center">

<img src="assets/images/KPLogooo.png" alt="KasuPilot logo" width="110" />

# KasuPilot

**An offline-first personal finance app for India: salary cycles, cards, loans and bank SMS, with all data kept on your phone.**

[![Latest release](https://img.shields.io/github/v/release/manojrajm/KaasuPilot?color=00F0FF&label=release&logo=github)](https://github.com/manojrajm/KaasuPilot/releases)
![Platform](https://img.shields.io/badge/platform-Android-3DDC84?logo=android&logoColor=white)
![Expo SDK](https://img.shields.io/badge/Expo%20SDK-58-000020?logo=expo)
![React Native](https://img.shields.io/badge/React%20Native-0.88-61DAFB?logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-strict-3178C6?logo=typescript&logoColor=white)
![Data](https://img.shields.io/badge/data-on--device%20only-0B1530)

[**Download the APK**](https://github.com/manojrajm/KaasuPilot/releases/latest) · [Features](#features) · [Architecture](#architecture) · [Getting started](#getting-started) · [Security & privacy](#security--privacy)

<br />

<img src="assets/images/mockups/hero_mockup_showcase.png" alt="KasuPilot screens: home, SMS review, loans" width="100%" />

</div>

---

## Table of contents

1. [Overview](#overview)
2. [Screenshots](#screenshots)
3. [Install the app](#install-the-app)
4. [Features](#features)
5. [Architecture](#architecture)
6. [Tech stack](#tech-stack)
7. [Project structure](#project-structure)
8. [Getting started](#getting-started)
9. [Testing and quality](#testing-and-quality)
10. [Build and release](#build-and-release)
11. [Data model](#data-model)
12. [Security & privacy](#security--privacy)
13. [SMS ingestion pipeline](#sms-ingestion-pipeline)
14. [Troubleshooting](#troubleshooting)
15. [Known limitations](#known-limitations)
16. [Roadmap](#roadmap)
17. [Contributing](#contributing)
18. [Author](#author) · [License](#license)

---

## Overview

KasuPilot answers three questions every day:

| Question | Where it is answered |
|---|---|
| **How much do I have left this salary cycle?** | Home: the salary card shows *available balance = carried balance + salary + extra income − expenses* |
| **What do I owe, and when is the next EMI due?** | Loans: cockpit, due-date calendar and EMI reminders |
| **Where is my money going?** | Transactions ledger, spending donut and 50/30/20 envelopes |

All data lives in an on-device SQLite database. There is no backend, no account and no analytics.
The only network traffic is the app checking for its own JavaScript updates (see [Security & privacy](#security--privacy)).

> **Status:** personal-use build in a field-testing period. It is distributed as a sideloaded APK and is
> not published on Google Play.

---

## Screenshots

| Live bank SMS review | Spending analytics and ledger |
|:---:|:---:|
| <img src="assets/images/mockups/mockup_sms_radar.png" width="320" alt="Bank SMS review" /><br /><sub>Bank alerts parsed on the device, then confirmed with one tap.</sub> | <img src="assets/images/mockups/mockup_transactions.png" width="320" alt="Ledger and spending donut" /><br /><sub>Spending donut by category, with search by merchant or person name.</sub> |

| Loans and EMI | Profile and data controls |
|:---:|:---:|
| <img src="assets/images/mockups/mockup_loans.png" width="320" alt="Loans cockpit" /><br /><sub>Due-date calendar, prepayment simulator, one-tap EMI booking.</sub> | <img src="assets/images/mockups/mockup_profile.png" width="320" alt="Profile and security" /><br /><sub>Security settings, backup export, and developer support via UPI.</sub> |

| Add an expense | Add income |
|:---:|:---:|
| <img src="assets/images/mockups/mockup_expense.png" width="320" alt="Add expense" /><br /><sub>Account picker, categories and recipient tagging.</sub> | <img src="assets/images/mockups/mockup_income.png" width="320" alt="Add income" /><br /><sub>Extra income is added to the current salary cycle.</sub> |

---

## Install the app

1. Download the latest `.apk` from [GitHub Releases](https://github.com/manojrajm/KaasuPilot/releases/latest) on your phone.
2. Open the file and tap **Install**. If asked, allow *Install unknown apps* for your browser or file manager.
3. If Google Play Protect warns about the app, choose **More details → Install anyway**. This applies to
   this install only; there is no need to switch Play Protect off.
4. **Android 13 and later:** SMS permission may be greyed out for sideloaded apps. Go to
   *Settings → Apps → KasuPilot → ⋮ → Allow restricted settings*, then *Permissions → SMS → Allow*
   (both receive and read).
5. Allow **Notifications**, then set *Battery → No restrictions* for KasuPilot. On Xiaomi, Oppo, Vivo and
   Realme phones, also turn **Autostart** on. Without these, the phone may stop the app from receiving SMS.
6. Open the app once, then create your PIN.

**Updating:** install the new APK over the old one. Do not uninstall, because uninstalling deletes all data.

---

## Features

### Home
- **Salary balance card:** your real salary card in the bank's colours, with the available balance for the
  current cycle, a usage bar and the days to the next salary.
- **Automatic salary credit:** the configured salary is posted on salary day every month, and never twice.
- **Cycle rollover:** when a cycle ends with money left, choose *add to this month* or *move to savings*.
- Spending velocity gauge, next-EMI cockpit, alerts, live SMS radar and recent activity.

### Cards
- Add your own cards for **SBI, Indian Bank, HDFC, ICICI, Axis** or any other bank, as debit or credit.
- Card faces drawn from the bank's colours, with chip, contactless mark and a **VISA / Mastercard / RuPay** logo;
  tap to flip to the CVV side.
- Card numbers are checked with the **Luhn** algorithm, and the network is detected from the number.
- Number, expiry and CVV are kept in the hardware keystore and shown only after biometric or PIN
  verification, then hidden again after 30 seconds.

### Loans and EMI
- Add or edit loans: principal, rate, tenure, first EMI date, the bank's exact EMI, instalments already paid,
  outstanding amount, processing fee and the paying account.
- Amortisation schedule, prepayment simulator (reduce tenure or EMI), Snowball vs Avalanche payoff,
  loan health score (0–100) and a month-by-month due-date calendar.
- **Pay EMI** splits interest and principal, advances the schedule and writes the ledger debit in one
  database transaction. The same instalment cannot be paid twice.
- Local EMI reminders.

### Bank SMS (Android)
- A native receiver and a headless JavaScript task read bank SMS, including while the app is closed.
- **Inbox scan:** the **🔄 Scan inbox** button reads your last 20 SMS and adds any bank transaction that was
  missed. The app also catches up automatically on every launch and return to the foreground.
- A pure on-device parser handles SBI, Indian Bank, HDFC, ICICI, Axis and UPI messages: amount,
  debit or credit, merchant or person name, account last four digits, reference number and balance.
- **Receipt merging:** a merchant receipt (for example a Jio recharge) and the bank debit for the same
  payment become one transaction, so the expense is counted once.
- Duplicate protection by reference number. Unknown formats are rejected, and an unmatched account is
  flagged instead of guessed.
- Review sheet: confirm, edit merchant, category or account, or ignore.

### Security and profile
- App lock with fingerprint or face, a PIN fallback and an animated lock screen. Auto-lock is immediate,
  1 minute or 5 minutes.
- Screenshot blocking and a hidden preview in the recent-apps list.
- Profile photo from the gallery or camera, stored privately inside the app.

### Analytics and export
- Spending donut and category breakdown, plus 50/30/20 envelope budgeting.
- CSV export of the ledger and a PIN-protected `.kasuvault` backup (see the [backup caveat](#security--privacy)).

---

## Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│ PRESENTATION   src/app (Expo Router screens) · src/components (UI)      │
├────────────────────────────────────────────────────────────────────────┤
│ APPLICATION    src/hooks: use-cases that subscribe to repositories      │
│                and build view models (useHomeDashboard, useLoans, …)    │
├────────────────────────────────────────────────────────────────────────┤
│ DOMAIN         src/domain: pure TypeScript, no React, Expo or database  │
│                money · loans · budget · cards · sms · profile           │
├────────────────────────────────────────────────────────────────────────┤
│ DATA           src/data/repositories → src/data/db/client (SQLite)      │
│                versioned migrations via PRAGMA user_version              │
├────────────────────────────────────────────────────────────────────────┤
│ SERVICES       src/services: keystore, biometrics, notifications,       │
│                SMS ingestion and inbox scan, backup, profile photo      │
├────────────────────────────────────────────────────────────────────────┤
│ NATIVE         plugins/ (config plugin + Kotlin SMS receiver)           │
│                modules/sms-inbox (Expo module that reads the SMS inbox) │
└────────────────────────────────────────────────────────────────────────┘
```

**Dependency rules**

1. `src/domain` never imports React, React Native, Expo or the database. It takes plain data and returns
   plain data, so it runs in plain Node for tests.
2. Screens never run SQL. They call hooks, and hooks call repositories.
3. Side effects live only in `src/services` and the repositories.
4. Repositories expose `subscribe(callback)`. Hooks reload on change, so every screen stays in sync.

---

## Tech stack

| Area | Choice |
|---|---|
| Framework | Expo SDK 58, React Native 0.88 (New Architecture), React 19 with React Compiler |
| Language | TypeScript (strict) |
| Navigation | Expo Router (file-based, typed routes) |
| Database | `expo-sqlite` (WAL, foreign keys, migrations) |
| Secrets | `expo-secure-store` (Android Keystore) |
| Authentication | `expo-local-authentication`, salted PIN hash via `expo-crypto` |
| UI and motion | `react-native-reanimated` 4, `react-native-svg`, `expo-haptics`, `expo-linear-gradient` |
| Notifications | `expo-notifications` (local, scheduled) |
| Files and media | `expo-image-picker`, `expo-file-system`, `expo-clipboard` |
| Privacy | `expo-screen-capture` |
| Native Android | Kotlin `BroadcastReceiver`, `HeadlessJsTaskService` and an Expo module |
| Delivery | EAS Build (APK) and EAS Update (over-the-air JavaScript updates) |

---

## Project structure

```
Kasupilot/
├── index.ts                 # app entry: registers the background SMS task, then loads the router
├── app.json                 # Expo config: name, icons, permissions, plugins, update channel
├── eas.json                 # build profiles and update channels
├── metro.config.js          # wasm and COOP/COEP headers (expo-sqlite on web)
├── modules/
│   └── sms-inbox/           # local Expo module (Kotlin): reads recent SMS from the inbox
├── plugins/
│   ├── withSmsReceiver.js   # config plugin: manifest entries and Kotlin sources
│   └── native-android/      # SmsBroadcastReceiver.kt, SmsHeadlessTaskService.kt
├── scripts/
│   ├── test-sms-parser.mts  # SMS parser test corpus (npm run test:sms)
│   └── make_icons.py        # regenerates the app icon set
├── assets/images/           # icons, mockups, splash video
└── src/
    ├── app/                 # screens: index, transactions, loans, loan-form, cards/, profile, explore
    ├── components/          # home · cards · loans · security · transaction · profile · ui
    ├── domain/              # money · loans · budget · cards · sms · profile · types.ts
    ├── data/
    │   ├── db/client.ts         # connection and migrations
    │   └── repositories/        # account · card · loan · salary · settings · transaction · profile
    ├── hooks/               # use-cases for screens
    ├── services/            # lock · cardVault · notifications · smsIngestion · smsInboxScanner · backup · …
    └── utils/               # date (local-time calendar maths) · id
```

---

## Getting started

### Prerequisites
- Node.js 22.18 or later (the SMS test script runs TypeScript directly), and npm
- An Android phone or emulator
- An [Expo account](https://expo.dev) to build the APK

### Run in development
```bash
npm install
npx expo start            # press "a" for Android
```

> Expo Go runs the UI, ledger, cards, loans and lock screen. **Background SMS capture and the inbox scan
> need a real build** (EAS APK or `npx expo run:android`), because they use custom native code.

> Add packages with `npx expo install <package>` so versions match SDK 58. See [`AGENTS.md`](AGENTS.md).

### Scripts

| Command | Purpose |
|---|---|
| `npm run typecheck` | TypeScript check (`tsc --noEmit`) |
| `npm run lint` | ESLint through Expo |
| `npm run test:sms` | Run the SMS parser test corpus |
| `npx expo-doctor` | Dependency and configuration health check |

---

## Testing and quality

- **SMS parser:** `npm run test:sms` runs 19 real-format messages through the parser. They cover Indian Bank,
  SBI, HDFC, ICICI and Axis, a Jio recharge receipt, salary and refunds, ATM withdrawals, and messages that
  must be rejected (OTPs, failed payments, requests, due reminders, offers).
- **Adding a bank format:** add the message and its expected fields to `scripts/test-sms-parser.mts`, see it
  fail, fix `src/domain/sms/parser.ts`, and run the suite again.
- **Before every commit:** `npm run typecheck` must report 0 errors.
- Domain maths (EMI, salary cycles) is not yet covered by automated tests; see the [roadmap](#roadmap).

---

## Build and release

### Build an APK

```bash
npx eas-cli@latest login
npx eas-cli@latest build -p android --profile preview
```

| Profile | Output | Update channel | Use |
|---|---|---|---|
| `preview` | `.apk` | `preview` | Install on a phone for testing |
| `development` | `.apk` with dev client | `development` | Debugging with Metro |
| `production` | `.aab` | `production` | Play Store (not used) |

- The finished build shows a download link and a QR code, and is also listed under **expo.dev → project → Builds**.
- Increase `android.versionCode` in `app.json` for every APK, and keep the same signing keystore so the new
  APK installs over the old one with the data intact.
- Build a new APK when a **native** change is made: a native package, a Kotlin file, permissions, the app
  icon or `app.json` identity fields.

### Ship JavaScript-only changes over the air

```bash
npx eas-cli@latest update --branch preview --environment preview --platform android --message "What changed"
```

- The phone downloads the update when the app opens and applies it on the next launch. Close and reopen the
  app twice to see it.
- An update only reaches APKs with the same **runtime version** (`runtimeVersion` policy `appVersion`).
  Do not change `version` in `app.json` unless a new APK is also being built.
- If the upload times out, run the same command again. Files already uploaded are kept.

### Publish a release
1. Build the `preview` APK and test it on a phone.
2. Create a GitHub release with a version tag and attach the `.apk`.
3. In the notes, list the highlights, install steps and known limitations.

---

## Data model

All money is stored as **integer paise**. Interest rates are stored as **basis points** (8.50 % = 850).

| Table | Purpose |
|---|---|
| `accounts` | Cards (debit or credit) and the built-in Cash account. Balance = opening balance + confirmed ledger |
| `transactions` | The ledger. A unique `source_ref` makes automatic entries idempotent: `salary:<date>`, `emi:<loan>:<n>`, `sms:rrn:<ref>` |
| `loans` | Loan register: principal, outstanding, rate, tenure, instalments paid, EMI, due day, paying account |
| `settings` | JSON settings: `profile`, `security`, `experience`, `salaryState`, `smsScan` |

Card numbers, expiry and CVV are **not** stored in SQLite. See the next section.

---

## Security & privacy

### What is stored where

| Asset | Protection |
|---|---|
| Ledger, loans, settings | SQLite file in the app's private storage. It is not encrypted at database level |
| Card number, expiry, CVV | `expo-secure-store` (hardware-backed keystore, `WHEN_UNLOCKED_THIS_DEVICE_ONLY`); shown only after biometric or PIN |
| App PIN | Salted SHA-256 hash in the keystore. Five wrong attempts trigger a 30-second lockout |
| Screen | Screenshots blocked and the recent-apps preview hidden (configurable). Always blocked on card screens |
| Backup file | PBKDF2-SHA256 key from the PIN plus a SHA-256 counter-mode keystream |

> ⚠️ **Backup strength.** The backup key comes from a 4-digit PIN, so anyone holding the `.kasuvault` file
> can try all 10 000 PINs offline. Keep backups in private locations only, and do not send them over chat or
> email. A passphrase-based AES-256-GCM format is on the [roadmap](#roadmap).

Storing the CVV is a deliberate choice for this personal-use build. It would not be acceptable in a
Play Store or PCI-scoped product.

### Network use
The app has no backend, account or analytics. The one network call is **EAS Update**: on launch the app asks
Expo's servers whether a new JavaScript bundle exists for its channel and downloads it if so. No ledger,
card or SMS data is sent.

### Permissions

| Permission | Why |
|---|---|
| `RECEIVE_SMS` | Read bank SMS as they arrive, including while the app is closed |
| `READ_SMS` | The **Scan inbox** catch-up reads recent messages. Only bank transactions are kept; OTPs and personal messages are discarded |
| `RECEIVE_BOOT_COMPLETED` | Restore EMI reminders after a restart |
| `POST_NOTIFICATIONS` | EMI reminders and new-transaction alerts |
| Camera and photos | Only when you choose a profile photo |
| Biometrics | App lock and card reveal |

---

## SMS ingestion pipeline

```
Bank SMS arrives
   │
   ▼  SmsBroadcastReceiver.kt    joins multi-part SMS; app open → JS event, app closed → headless task
   ▼  index.ts                   registers the headless task at startup, before any screen loads
   ▼  smsBackgroundReceiver.ts   task KasuPilotSmsReceiverTask
   ▼  smsIngestion.ts            receipt/debit merge, duplicate check, account matching
   ▼  domain/sms/parser.ts       sender → bank, direction, amount, counterparty, reference, balance
   ▼  transactions (pending_review)
   ▼  SMS review sheet           confirm · edit · ignore → confirmed ledger entry

Catch-up path:  modules/sms-inbox → smsInboxScanner.ts → the same smsIngestion.ts
                (on app launch, on return to foreground, and from the "Scan inbox" button)
```

Unknown formats are left unparsed instead of guessed, and an unmatched bank or card is flagged for you to
resolve. Both capture paths use the same duplicate key, so a message seen twice is recorded once.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| SMS permission is greyed out | *Settings → Apps → KasuPilot → ⋮ → Allow restricted settings*, then allow SMS |
| Bank SMS is missed while the app is closed | Set *Battery → No restrictions* and enable *Autostart*; then use **🔄 Scan inbox** |
| A bank SMS shows "Unknown Merchant" | The format is not recognised yet. Open an issue with the SMS text (hide account numbers) |
| An OTA update does not appear | Close and reopen the app twice, and check that the phone has internet and the APK's `versionCode` is current |
| "Scan inbox" button is missing | The installed APK predates the inbox module. Install the latest APK |
| Data is gone after an update | The old app was uninstalled. Always install the new APK over the old one |

---

## Known limitations

- Background SMS capture depends on the phone: some manufacturers stop apps aggressively. The inbox scan
  is the safety net.
- iOS cannot read SMS, so iOS would rely on manual entry. The app is Android-only today.
- Credits that arrive without an SMS (for example some government refunds) must be added manually.
- Paying a credit-card bill from a debit card is currently recorded as two expenses until a *transfer*
  transaction type exists.
- Two identical payments within 30 minutes may be merged into one by the receipt matcher.
- Transactions cannot be edited or back-dated yet.

---

## Roadmap

1. **Ledger correctness:** transfer transaction type, transaction edit, back-dated entries.
2. **Backup:** passphrase-based AES-256-GCM format, automatic weekly backups and a monthly report to share.
3. **Reconciliation:** enter the real bank balance and book the difference.
4. **Tests and CI:** unit and property tests for `domain/`, and a CI workflow.
5. Credit-card statement cycle, recurring entries and category budgets.
6. Person view: totals sent to and received from one person.
7. Tamil UI, home-screen widget, voice entry and receipt OCR.

---

## Contributing

Issues and pull requests are welcome.

- Follow the [architecture rules](#architecture), and keep `src/domain` free of React, Expo and database imports.
- Store money as integer paise, and compute month and salary-cycle boundaries in local time (`src/utils/date.ts`).
- Write migrations forward-only, each in one transaction with its `user_version` bump.
- In hooks, set state only in async callbacks (lint rule `react-hooks/set-state-in-effect`).
- Use [Conventional Commits](https://www.conventionalcommits.org): `feat:`, `fix:`, `chore:`, `docs:`.
- Run `npm run typecheck` and `npm run test:sms` before opening a pull request.
- For a bad SMS parse, open an issue with the message text, the sender header and the expected result.
  Remove account numbers and names first.

Further reading: [`ARCHITECTURE.md`](ARCHITECTURE.md) (product and technical specification) and
[`AGENTS.md`](AGENTS.md) (rules for coding agents working in this repository).

---

## Author

**Manoj Raj** · [GitHub @manojrajm](https://github.com/manojrajm)

If KasuPilot is useful to you, star the repository, or support development through the UPI option inside the
app's profile screen.

## License

See [`LICENSE`](LICENSE).
