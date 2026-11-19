<p align="center">
  <img src="docs/icon.png" width="128" height="128" alt="Trace icon">
</p>

<h1 align="center">Trace</h1>

<p align="center">
  A free, open-source alternative to Timing: an activity tracker for macOS that keeps everything on your Mac.
</p>

<p align="center">
  <b>English</b> · <a href="README.zh-CN.md">简体中文</a>
</p>

<p align="center">
  <a href="https://github.com/lxyeternal/Trace/releases/latest">Download</a> ·
  <a href="#features">Features</a> ·
  <a href="#privacy">Privacy</a> ·
  <a href="#install">Install</a> ·
  <a href="#build-from-source">Build from source</a>
</p>

![A tour of Trace: overview, lanes, timeline, projects, records, focus and reports](docs/tour.gif)

Trace sits in the menu bar and records which app, window, file and web page is in front of you, and for how long. There are no timers to start and nothing to fill in. At the end of the day it shows where the time went, down to the single file or page.

## Why Trace

[Timing](https://timingapp.com) set the standard for automatic time tracking on the Mac, and it is a paid app. Trace is a free, open-source alternative: it records your day in the same hands-off way, it costs nothing, the source is here to read and change, and your records never leave your Mac unless you turn on sync yourself.

## Features

### The day in lanes

One lane per tag or app, with sound and calls underneath, so you can see what happened at the same time: coding with music on, or a meeting that ran in the background. Below that, every app that was open gets a lane of its own, solid while its window was on screen and faint while it was open out of sight. Only the app in front counts towards tracked time. Trace notes which apps are playing sound or using the microphone, never what is played or said. No keyboard or mouse does not mean you are away: while you are on a call, or the app in front is playing sound, the time still counts.

![The day as parallel lanes, with sound, calls and every open app below](docs/screenshots/lanes.png)

### A detailed timeline

Expand the day level by level: tag › app › file or site › page. The day runs top to bottom on the right; click a session or drag across any stretch of it, and the outline sums up only that period.

![Timeline with a drill-down outline and the day laid out top to bottom](docs/screenshots/timeline.png)

### Projects, found for you

Trace works out which project each file belongs to from the folder it is in (a git repository, a Swift package, an Obsidian vault, or simply the folder inside Documents), so you can see time per project without setting anything up.

![Time grouped by project](docs/screenshots/projects.png)

### Every record, one by one

Switch to Records to read the day stay by stay. Sessions group the records that belong together, and a brief glance at another app does not split a session. Select a record to see its file path or URL, how often you came back to it, and its tags.

![Records grouped into sessions, with an inspector for the selected record](docs/screenshots/records.png)

### Tags that apply themselves

Eight built-in tags (Development, Office, Study, Communication, Entertainment, Games, Design, Browsing) work from the first launch, based on the category each app declares to macOS and a short list of well-known apps and sites. Add your own tags, give them rules on the app, file path, URL or window title, or tag a single record by hand. Rules are applied when reading, so changing one re-tags your whole history.

| Tags | Rules |
|---|---|
| ![Preset and custom tags](docs/screenshots/tags.png) | ![Rules and untagged activity](docs/screenshots/rules.png) |

### Focus, goals and sessions

The Focus page keeps three things together:

- **Sessions.** Press Start, pick a tag, and from then until you stop, everything you do counts as that tag, whatever the rules say. Good for a game, a study block, or anything the rules cannot guess. A session can be open-ended or timed; a timed one ends by itself and tells you. Delete a session and its records go back to their own tags.
- **Goals.** Give a tag a daily target, at least or at most so much, and follow it as a ring with a streak.
- **How focused the day was.** Time in deep work (25 minutes or more of focus work in one go), how often you switched apps each hour, and which apps pulled you away most.

![The Focus page: start a session, goals, and the day's focus](docs/screenshots/focus.png)

### Reports

A week, a month or a year at a glance: a short review in plain sentences of what changed since the period before, time per day stacked by tag, the hours you are usually active, and the projects, sites and files you spent the most time on. The year view adds a calendar with one square per day. Any period can be exported as CSV.

![Weekly report with a review, daily totals and a heat map](docs/screenshots/reports.png)

![A year with one square per day](docs/screenshots/year.png)

### Several Macs, one picture

Sync is optional and off by default. Turn on **Sync with iCloud** in Settings and Trace keeps its records in a `Trace` folder in iCloud Drive: there is nothing to set up, and every Mac signed in to the same iCloud account that turns it on joins in. Each Mac writes its own records and reads the others'. Any other synced folder (Dropbox, a network drive) works too. Tags and rules are shared, and you can look at all Macs together or one at a time. The files are plain text, so the folder doubles as a backup.

### Made for the Mac

Native SwiftUI, light and dark appearance, English, Simplified Chinese and Russian (switchable without restarting), and launch at login. The menu bar panel shows today's total, the app in front, and what else is going on: a call, sound, windows on screen and apps open out of sight. Closing the window leaves Trace recording in the menu bar.

<p align="center">
  <img src="docs/screenshots/menu.png" width="300" alt="The menu bar panel">
</p>

| Dark appearance | Simplified Chinese |
|---|---|
| ![Overview in dark appearance](docs/screenshots/overview-dark.png) | ![Overview in Simplified Chinese](docs/screenshots/zh/overview.png) |

## Privacy

- **Local by default.** Everything is stored in one SQLite file at `~/Library/Application Support/Trace/trace.sqlite`. Trace makes no network connections and has no account.
- **Sync only if you turn it on.** With a sync folder set, your records are also written there as readable files, and whatever syncs that folder carries them. Anyone who can open the folder can read them. Turn sync off and Trace stops writing to it.
- **No keystrokes, no screenshots.** Trace reads the name of the app in front and, through the macOS Accessibility API, the title, document path and page address of its focused window. Nothing else.
- **URLs without the sensitive part.** Query strings, fragments and credentials are removed before a URL is stored.
- **You choose what is recorded.** Window titles, file paths, web addresses, sound and calls, and the list of open apps can each be turned off, and any app can be excluded completely.
- **Your data is yours.** Export it as CSV or erase it from Settings at any time.

## Install

Requires macOS 14 or later, on Apple silicon or Intel.

1. Download the `.dmg` from the [latest release](https://github.com/lxyeternal/Trace/releases/latest).
2. Open it and drag Trace to Applications.
3. Start Trace. It asks for **Accessibility** access (System Settings › Privacy & Security › Accessibility); without it Trace still records which app is in front, but not window titles, file paths or URLs.

Releases are signed with a Developer ID certificate and notarized by Apple, so they open without a security warning.

## Build from source

Needs Xcode 16 or later.

```bash
git clone https://github.com/lxyeternal/Trace.git
cd Trace
scripts/bundle.sh
open build/Trace.app
```

The default build is ad-hoc signed, so macOS asks for Accessibility access again after every rebuild. To avoid that, put the name of one of your signing certificates (see `security find-identity -v -p codesigning`) in a file named `.codesign-identity` in the repository root; the file is ignored by git.

Useful commands:

| Command | What it does |
|---|---|
| `swift test` | Runs the unit tests of the core library. |
| `open -n build/Trace.app --args --demo` | Opens Trace with made-up data, without recording anything. |
| `scripts/release.sh` | Builds a universal app and packages it as a DMG and a zip. |
| `swift scripts/make-icon.swift` | Redraws the app icon. |

## How it works

| Part | Where | What it does |
|---|---|---|
| Capture | `Sources/Trace/Capture` | Reads the frontmost app from `NSWorkspace`, the focused window through the Accessibility API, idle time from `CGEventSource`, and which apps play sound or use the microphone from Core Audio, every two seconds. Every ten seconds it also notes which apps are open and whether a window of theirs is on screen, from the window list (owner and frame only, no titles or contents). |
| Storage | `Sources/TraceCore/EventStore.swift` | SQLite via [GRDB](https://github.com/groue/GRDB.swift). Consecutive identical samples extend one event, so there is one row per stay. Idle time is not stored; it appears as gaps. |
| Tagging | `Sources/TraceCore/Tagging.swift` | Rules match on app, app category, file path, URL or window title. Tags added or removed by hand on a single record override the rules. |
| Sync | `Sources/TraceCore/SyncEngine.swift` | Each Mac writes one file per day into its own subfolder of the sync folder and reads the other Macs' files, so two Macs never edit the same file. For tags and rules the most recent edit wins. |
| Analysis | `Sources/TraceCore/Analyzer.swift`, `Insights.swift` | Day summary, sessions, the drill-down outline, lanes, focus, projects, reports, reviews and CSV export. |
| Interface | `Sources/Trace/Views` | SwiftUI. Colours and shared controls live in `Theme.swift`. |

`TraceCore` has no user interface and is covered by unit tests; the app target adds capture and the interface on top of it.

## Adding a language

Copy `Resources/zh-Hans.lproj` to `Resources/<code>.lproj`, translate the right-hand side of each line, then add the code to `CFBundleLocalizations` in `Support/Info.plist` and to `AppLanguage` in `Sources/Trace/Localization.swift`. The English text is the key, so nothing else needs to change.

## Known limitations

- A silent video or a long read without touching the keyboard or mouse counts as away once the idle time has passed. On a call, or with sound playing in the app in front, it does not; background music counts only if you turn that on in Settings.
- Sound and calls are recognised by which app uses the speakers or the microphone. An app that keeps the microphone open without a call, such as a dictation tool, shows up as a call; exclude it in Settings.
- Private browsing windows are not detected and are recorded like any other window. Exclude the browser or turn off web addresses if that matters to you.
- Page addresses depend on what each browser exposes to the Accessibility API. Safari and Chromium-based browsers (Chrome, Edge, Arc, Brave) are covered; others may only report the window title.

- With sync on, time is not de-duplicated across Macs: if two Macs are in use at the same moment (for example over remote desktop), both count, and their sessions are shown side by side. Tags added by hand to a single record stay on the Mac where they were added.

## Contributing

Issues and pull requests are welcome. Please run `swift test` before opening a pull request, and keep new interface text in both `en` and `zh-Hans`.

## License

[GPL-3.0](LICENSE). You may use, change and share Trace freely, also at work. If you distribute it or a version based on it, you must do so under the same license and make the source available.

Versions up to 0.2.1 were released under the MIT license.
