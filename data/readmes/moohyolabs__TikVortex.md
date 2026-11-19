<div align="center">

<img src="tikvortex/assets/icon.png" width="112" alt="TikVortex icon">

# TikVortex

**Download TikTok videos, photo slideshows and highlights in their original quality - no watermark.**

By **[moohyo labs](https://github.com/moohyolabs)** · a desktop app for Windows (with a command line for everything else), built on the
[Ez-TikTok-Downloader](https://github.com/AlexRabbit/Ez-TikTok-Downloader) engine by AlexRabbit.

[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-8b5cf6?style=flat-square)](LICENSE)
![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-ec4899?style=flat-square)
![Windows](https://img.shields.io/badge/Windows-10%20%7C%2011-a855f7?style=flat-square)

<img src="docs/screenshots/download-dark.jpg" width="900" alt="TikVortex download page, dark theme">

</div>

---

## Contents

- [Features](#features)
- [Install](#install)
- [Using the app](#using-the-app)
- [Command line](#command-line)
- [Settings and files](#settings-and-files)
- [Building a release](#building-a-release)
- [Troubleshooting](#troubleshooting)
- [Credits](#credits)
- [Licence](#licence)
- [Disclaimer](#disclaimer)

## Features

**Downloading**
- Original-quality video through TikWM's Original Downloader, with automatic fallback to the compressed copy if the original isn't ready - and an automatic retry in original quality at the end of every batch.
- Paste anything: links, short links, bare post IDs, `@usernames`, several accounts at once, a saved creator group, or a `.txt` / `.url` file. Drag and drop works on the window and on Mini Mode.
- Photo slideshows saved image by image, full size.
- Parallel downloads, an optional speed limit, and pause / stop.
- **Force** re-download: replaces a file in place and keeps its date and folder; if the original still isn't available, your existing copy is kept.
- Unfinished queues can be resumed after a restart.

**Organising**
- Creator groups: one creator with several accounts, downloaded as one timeline into one folder.
- Folder layout by creator group, by account, or everything in one folder.
- Drag-and-drop file-name builder (post ID is always kept, so existing files are still recognised).
- Post or download dates written into the files (MP4 and JPEG metadata) so photo apps show them in posting order, plus tools to re-order and fix dates on older downloads.

**The app**
- **Library** of everything you've downloaded: search, sort (date posted, date downloaded, size, creator), filter by videos / photos / compressed / duplicates, cards that fill the width at 3-9 per row, video length on every card, muted previews on hover (with the time counting up), creator chips with post counts, a **creator gallery**, an **Info** panel (one post's details, or a summary of several), and multi-select (click, Ctrl, Shift, drag a box, Ctrl+A) with open, show in folder, copy links, re-download and Recycle Bin.
- **Watchlist**: TikVortex checks the creators (or creator groups) you watch for new posts, every hour to once a day, and downloads them automatically or lets you know - also while it sits in the tray.
- **Highlights**: browse a creator's highlights collection by collection (or all at once), preview video stories on hover, and pick the ones to download.
- Light, dark and follow-Windows themes, six colour themes (Vortex, Aurora, Sunset, Ocean, Midnight, Sakura) and adjustable glass.
- Command bar (**Ctrl+K**), clipboard watching, tray icon, finish notifications and sound, always-on-top **Mini Mode** (**Ctrl+M**), TikWM status indicator, and keyboard shortcuts throughout.
- Creators' profile pictures in the sidebar, library and group editor (fetched once and cached); pick a creator group's picture in Tools.
- One copy of the app at a time - launching it again (or dropping links on it) hands them to the running window.
- Optional check for new releases on GitHub at launch.

<p align="center">
  <img src="docs/screenshots/library-dark.jpg" width="440" alt="Library page, dark theme">
  <img src="docs/screenshots/watchlist-light.jpg" width="440" alt="Watchlist page, light theme">
  <img src="docs/screenshots/library-light.jpg" width="440" alt="Library page, light theme">
  <img src="docs/screenshots/settings-dark.jpg" width="440" alt="Settings page, dark theme">
</p>

## Install

### Windows - ready-made app
1. Download `TikVortex-<version>-windows.zip` from the [Releases](../../releases) page.
2. Unzip it anywhere you can write to (for example `Documents\TikVortex`).
3. Run **`TikVortex.exe`**.

Your settings (`config.json`), download cache and the `profiles` folder are created next to the app, so the whole folder is portable.

> Windows SmartScreen may warn about an unsigned app the first time. Choose **More info → Run anyway**.

### From source (Windows, macOS, Linux)
Requires Python 3.10 or newer.

```bash
git clone https://github.com/moohyolabs/TikVortex.git
cd TikVortex
pip install -r requirements.txt     # or run "Install dependencies.bat"
```

Start it with **`TikVortex.bat`** or **`TikVortex.pyw`** on Windows (no Command Prompt window stays open), or `python3 -m tikvortex` on macOS / Linux.

## Using the app

| Page | What it does |
|---|---|
| **Download** | Paste or drop links, IDs, `@users`, a group name or a `.txt`. **Clipboard** adds copied TikTok links automatically; **Force** re-downloads things you already have. The queue shows progress, quality and any posts needing attention (with **Retry original**). |
| **Library** | Everything in your download folder. Right-click or use the selection bar for bulk actions. |
| **Highlights** | Type `@username`, open a collection (or **Show all stories**), pick stories, **Download selected**. You can also paste a highlight post ID. |
| **Watchlist** | Opened from **View all** in the sidebar, a watched creator, Ctrl+6, the command bar or the tray. Add a `@username`, profile link or group; choose how often to check and whether new posts download automatically. |
| **Tools** | Re-order a folder or creator group by post date (keep the current dates or pick a start date and time, with a preview), fix dates on older downloads, bulk force re-download, creator-group editor, certificate check, and shortcuts to the log and folders. |
| **Settings** | Download folder, folder layout, file names, quality and date options, profile-listing fallback, TikTok session ID and cookies, theme, glass, moving background, sound, tray, notifications, start with Windows and what to do with failed links. |

**Shortcuts:** Ctrl+V paste & queue · Ctrl+Enter start · Ctrl+1–6 switch page (6 = Watchlist) · Ctrl+K command bar · Ctrl+M Mini Mode · Esc clear selection.

The sidebar shows the batch in progress, your watchlist (with a count of new posts waiting) and recent batches. The **Online** pill shows whether TikWM is responding - hover it for details.

## Settings and files

Everything lives next to the app (or the folder in `TIKVORTEX_HOME`, if set):

| File | Purpose |
|---|---|
| `config.json` | All settings. The app writes it for you. |
| `link_cache.json` | Which posts you've already fetched. |
| `profiles/` | Your downloads (change it in Settings). |
| `sessionid.txt` | Optional: your TikTok session ID, for posts only visible when logged in. Set it in **Settings → TikTok session ID**. **Keep it private.** |
| `cookies.txt` | Optional: cookies for yt-dlp and gallery-dl, for restricted profiles. Choose it in **Settings → Cookies**. |
| `log.txt` | Log of everything the app did - useful when something goes wrong. |
| `.tikvortex/` | Thumbnails, covers, profile pictures, saved post details and the unfinished-queue file. Safe to delete (Settings → Cache → Clear clears the pictures). |

## Building a release

On Windows, run **`build.bat`**. It installs the build tools, renders the icon, runs PyInstaller with `TikVortex.spec` and writes:

- `dist\TikVortex\` - the app folder (`TikVortex.exe` and docs)
- `dist\TikVortex-1.0.0-windows.zip` - ready to upload

Pushing a tag such as `v1.0.0` to GitHub runs the same build in GitHub Actions (`.github/workflows/release.yml`) and attaches the zip to a release.

`tools/make_icon.py` regenerates the icon.

## Troubleshooting

- **Videos come out "Compressed".** TikWM sometimes takes longer to prepare the original. They're retried at the end of the batch; you can also press **Retry original** later, or raise *Wait for original file* in Settings.
- **"Certificate has expired" errors.** TikWM's file server has had an expired certificate. Use **Tools → Check TikWM certificate**, and if it confirms the problem, turn on *Accept TikWM's expired certificate* in Settings (it only applies to `*.tokcdn.com`).
- **Profiles won't list.** Profiles are listed through TikWM first, then yt-dlp (bundled), then gallery-dl if *Settings → Try gallery-dl for profiles* is on (its slow method opens the profile page itself, so it often works when the others are blocked). If all of them fail, add `cookies.txt` or paste the post links instead.
- **TikWM refused (HTTP 403).** TikWM allows about one request a second, so it can refuse while a big batch is running. Watchlist checks wait for downloads to finish for this reason; anything else can simply be retried a minute later.
- **Highlights won't load.** They're listed through a third-party service that is sometimes unavailable. Try again later, or paste the post IDs instead.
- **Slideshow fallback / gallery-dl.** gallery-dl isn't bundled with the Windows app. To use it, put `gallery-dl.exe` next to `TikVortex.exe` or on your PATH.

## Credits

Thank you to:

| Project | Author | Used for | Licence |
|---|---|---|---|
| [Ez-TikTok-Downloader](https://github.com/AlexRabbit/Ez-TikTok-Downloader) | **AlexRabbit** | The original download engine this project is built on (now `tikvortex/core/`), the cache format and the idea behind it all | Unlicense (public domain) |
| [TikWM](https://www.tikwm.com/) | TikWM | The service that provides original-quality, watermark-free files | Third-party web service |
| [omar-thing.site](https://omar-thing.site/) | omar-thing | Listing highlight stories (used through its public viewer - please respect its terms) | Third-party web service |
| [yt-dlp](https://github.com/yt-dlp/yt-dlp) | yt-dlp contributors | Listing a profile's posts (bundled) | Unlicense |
| [gallery-dl](https://github.com/mikf/gallery-dl) | Mike Fährmann | Optional last resort for slideshows and profile listing (run as a separate program, not bundled) | GPL-2.0 |
| [Qt](https://www.qt.io/) / [PySide6](https://doc.qt.io/qtforpython/) | The Qt Company | The desktop interface | LGPL-3.0 |
| [QtAwesome](https://github.com/spyder-ide/qtawesome) | Spyder project | Icon fonts in Qt | MIT |
| [Phosphor Icons](https://phosphoricons.com/) | Helena Zhang & Tobias Fried | Interface icons | MIT |
| [Material Design Icons](https://pictogrammers.com/library/mdi/) | Pictogrammers | Download icon | Apache-2.0 |
| [Geist](https://vercel.com/font) | Vercel & basement.studio | Interface font (bundled) | SIL OFL 1.1 - see `tikvortex/assets/fonts/Geist-OFL.txt` |
| [Inter Display](https://rsms.me/inter/) | Rasmus Andersson / The Inter Project Authors | TikVortex wordmark and page titles (bundled) | SIL OFL 1.1 - see `tikvortex/assets/fonts/Inter-OFL.txt` |
| [Requests](https://requests.readthedocs.io/) | Kenneth Reitz & contributors | HTTP | Apache-2.0 |
| [truststore](https://github.com/sethmlarson/truststore) | Seth Larson | Using Windows' own certificate store | MIT |
| [PyInstaller](https://pyinstaller.org/) | PyInstaller team | Building the Windows app | GPL-2.0 with bootloader exception |

TikVortex itself - the name, icon, interface design and app code (`tikvortex/`) - is made by
**[moohyo labs](https://github.com/moohyolabs)**.

## Licence

Copyright © 2026 moohyo labs.

TikVortex is free software: you can redistribute it and/or modify it under the terms of the
**GNU General Public License, version 3** (or, at your option, any later version), as published
by the Free Software Foundation. It comes **without any warranty**. See [LICENSE](LICENSE) for the full text.

Bundled fonts stay under the SIL Open Font License 1.1.
The original Ez-TikTok-Downloader code was released into the public domain by its author, which allows it to be
included here under the GPL.

## Disclaimer

TikVortex is an independent project. It is **not affiliated with, endorsed by or connected to TikTok, ByteDance,
TikWM or omar-thing.site**. "TikTok" is a trademark of its owner and is used here only to describe what the app works with.

Use it for content you have the right to download - your own videos, or content for personal, offline viewing - and respect creators, copyright and the terms of the services involved. Don't re-upload other people's work.
