<p align="center">
  <img src="site/img/icon.png" width="96" height="96" alt="Hourmint app icon">
</p>

<h1 align="center">Hourmint</h1>

<p align="center">
  Free, open source time tracker for Mac.<br>
  Track client work from the menu bar, keep an honest work log, and turn your hours into PDF invoices with a detailed timesheet.<br>
  Local-first. No account. Your data stays on your Mac.
</p>

<p align="center">
  <a href="https://github.com/abdurrahmanriyad/hourmint/releases/latest"><img src="https://img.shields.io/github/v/release/abdurrahmanriyad/hourmint?label=release&color=059669" alt="Latest release"></a>
  <a href="https://github.com/abdurrahmanriyad/hourmint/releases"><img src="https://img.shields.io/github/downloads/abdurrahmanriyad/hourmint/total?color=059669" alt="Downloads"></a>
  <img src="https://img.shields.io/badge/macOS-13%2B-18181b?logo=apple" alt="macOS 13 or later">
  <a href="LICENSE"><img src="https://img.shields.io/github/license/abdurrahmanriyad/hourmint?color=18181b" alt="MIT licence"></a>
</p>

<p align="center">
  <a href="https://github.com/abdurrahmanriyad/hourmint/releases/latest/download/Hourmint.dmg"><b>Download for Mac</b></a>
  &nbsp;|&nbsp;
  <a href="https://hourmint.abdur.tech">Website</a>
  &nbsp;|&nbsp;
  <a href="CONTRIBUTING.md">Contribute</a>
</p>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="site/img/hero-dark.webp">
  <img src="site/img/hero.webp" alt="The Hourmint timer in the macOS menu bar, its popover open below it, and the work log window behind">
</picture>

## Features

- **Menu bar timer.** The elapsed time sits next to your clock. Start, stop or switch projects from a small popover.
- **Survives everything.** Quit, restart or sleep your Mac and the running timer is still right.
- **Honest work log.** Day, week and custom views with totals per client and project. Manual and edited entries are labelled.
- **Timesheets and PDF invoices.** Pick the hours to bill, group them the way your client likes, and export a PDF with every entry attached. Hours already on an invoice are locked, so nothing is billed twice.
- **Any currency, any rate.** Each client has its own currency and hourly rate, with per-project overrides. Invoices keep the rate they were made with.
- **Rounding, tax and discounts.** Your own invoice numbering, like `INV-{YYYY}-{0001}`.
- **Idle detection and reminders.** Hourmint notices when you walk away, nudges you if you forget to start, and warns you about a timer that has run for hours.
- **Backups built in.** A daily backup, plus export to CSV or JSON at any time.
- **Private by design.** No account, no cloud, no analytics. The only network request is the update check against GitHub Releases.

## See it in action

From a running timer to the work log to a finished invoice:

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="site/img/tour-dark.webp">
  <img src="site/img/tour.webp" alt="A tour of Hourmint: the Today screen with a running timer, the weekly work log, and a new invoice for Acme Robotics built from logged hours, with its live preview">
</picture>

## Install

1. Download [Hourmint.dmg](https://github.com/abdurrahmanriyad/hourmint/releases/latest/download/Hourmint.dmg) (macOS 13 or later, Apple Silicon and Intel).
2. Open it and drag Hourmint to your Applications folder.
3. Open Hourmint. It isn't notarized by Apple yet, so the first time macOS says it can't verify the developer. Go to **System Settings > Privacy & Security** and click **Open Anyway**.

Updates install from inside the app after that.

## Contributing

Bug reports, ideas and pull requests are welcome. And if Hourmint saves you time, a star on GitHub helps other freelancers find it.

- Found a bug? [Open an issue](https://github.com/abdurrahmanriyad/hourmint/issues/new/choose), or use **Report a problem** in the app's Settings.
- Want to help? Look for issues labelled [good first issue](https://github.com/abdurrahmanriyad/hourmint/labels/good%20first%20issue) or [help wanted](https://github.com/abdurrahmanriyad/hourmint/labels/help%20wanted).
- Have a question or an idea? Start a [discussion](https://github.com/abdurrahmanriyad/hourmint/discussions).

Hourmint is built with [Tauri 2](https://tauri.app) (Rust), React, TypeScript and SQLite. [CONTRIBUTING.md](CONTRIBUTING.md) explains how to run it locally, how the code is laid out and how to send a change.

```sh
npm install
npm run app        # the native app with hot reload
npm run test:all   # typecheck, frontend tests and Rust tests
```

## Licence

[MIT](LICENSE). The bundled Noto Sans fonts are under the SIL Open Font License (`src/assets/fonts/OFL.txt`).
