# Wintodo

![Wintodo — Native WinUI 3 replacement for Microsoft To Do](docs/releases/launch-banner.png)

**A free, native Windows 11 task manager** built with **WinUI 3** and **.NET 10 Native AOT** (`x64` and `ARM64`). Wintodo preserves the fast, familiar workflow of Microsoft To Do while storing your tasks locally in SQLite and syncing over open standards (**iCalendar `VTODO`**, **CalDAV**) — no proprietary cloud, no Electron, no WebView2, no ads or telemetry.

**[Get Wintodo free on Microsoft Store →](https://apps.microsoft.com/detail/9PF4DX2BSF0X)** *(Windows 11 24H2+, x64 & ARM64 · Published by Univera LLC)*

## Highlights

- **Familiar Microsoft To Do experience:** *My Day*, *Important*, *Planned*, *All*, *Completed*, custom lists and list groups, steps (subtasks), due dates, repeat schedules (`RRULE`), notes, file attachments, full keyboard shortcuts (`Ctrl+N`, `Ctrl+F`, `Space`), and multi-step `Ctrl+Z` undo.
- **Built-in Microsoft To Do import:** One-time, strictly **read-only** import wizard — pick which lists to copy (tasks, steps, notes, due dates, attachments) without touching your originals.
- **Open standards, zero lock-in:** Use 100% locally with no account at all, sync with any **CalDAV** server (Nextcloud Tasks, Radicale, Fastmail, etc. — credentials kept in Windows `PasswordVault`), or import/export standard **iCalendar (`.ics` / `VTODO`, RFC 5545)** files anytime.
- **Native Windows 11 integration:** Mica backdrop, Light / Dark / High Contrast themes, OS-scheduled reminder notifications (`ScheduledToastNotification`, fire even when closed), taskbar badge, Jump List, and Windows Share target.
- **Private by default:** No vendor task server, no account system of our own, no analytics or advertising. See [Privacy Policy](docs/releases/PRIVACY.md).

## Measured performance (Windows 11 x64, Native AOT)

All numbers are measured — no estimates. Full tables and methodology live in [docs/PERF.md](docs/PERF.md).

| Metric | Measured result |
|---|---|
| **Live Store v1.0.0.0 idle memory** | **86.8 MB** Task Manager memory (`Private Working Set`), 1 process, **18 threads** *(182.2 MB Total Working Set)* |
| **Memory scaling (0 → 20,000 tasks)** | `142.7 MB` → `180.5 MB` Total Working Set *(+38 MB for 20,000 tasks across 20 lists)* |
| **10,000-task list scroll** | **119.37 fps**, **0** dropped frames, **0 B** per-frame callback allocations |
| **10,000-task SQLite queries & FTS5 search** | **1.5–2.7 ms** smart-list queries · **2.3–6.7 ms** worst warm FTS5 search |
| **Self-contained MSIX package size** | **56.6 MiB** (`x64`) · **55.0 MiB** (`ARM64`) · `21.3 MiB` Native AOT executable |

## Build and run

Prerequisites: the exact .NET SDK pinned in [`global.json`](global.json), WinApp CLI 0.7+, Windows 11 with Developer Mode enabled.

```powershell
dotnet build Wintodo.sln -p:Platform=x64 -warnaserror
dotnet test  Wintodo.sln -p:Platform=x64
.\BuildAndRun.ps1
```

Details: [docs/guides/build-and-run.md](docs/guides/build-and-run.md).

## Licence

Wintodo is distributed under the [Wintodo Source-Available Licence 1.0](LICENSE.md):

- Free to inspect, modify, and self-build for personal or internal business use.
- Free unbranded community redistributions are permitted with matching source and notices.
- The individual author retains the **Wintodo** brand and commercial licensing rights; **Univera LLC** publishes the official Microsoft Store release.

## Documentation

| You want | Read |
|---|---|
| How the code is organised | [ARCHITECTURE.md](ARCHITECTURE.md) |
| Product scope, milestones, budgets | [PLAN.md](PLAN.md) |
| Measured performance log | [docs/PERF.md](docs/PERF.md) |
| Privacy policy | [docs/releases/PRIVACY.md](docs/releases/PRIVACY.md) |
| Current progress & release history | [docs/PROGRESS.md](docs/PROGRESS.md) |
| Full documentation index | [docs/README.md](docs/README.md) |
| Rules for AI coding agents | [AGENTS.md](AGENTS.md) |
