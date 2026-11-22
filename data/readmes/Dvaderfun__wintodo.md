<p align="center">
  <img src="docs/plans/assets/store-icon-glide.svg" width="112" height="112" alt="">
</p>

<h1 align="center">Wintodo</h1>

<p align="center">
  <strong>A free, native task manager for Windows 11.</strong><br>
  Plan your day offline. Keep your lists on your PC or sync them with your own CalDAV server.
</p>

<p align="center">
  <a href="https://apps.microsoft.com/detail/9pf4dx2bsf0x?referrer=appbadge&amp;mode=full">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://get.microsoft.com/images/en-us%20dark.svg">
      <img src="https://get.microsoft.com/images/en-us%20light.svg" width="200" alt="Download Wintodo from the Microsoft Store">
    </picture>
  </a>
</p>

<p align="center">
  <a href="docs/releases/INSTALLATION.md#windows-and-architecture"><img src="https://img.shields.io/badge/Windows_11-24H2%2B-137D9C" alt="Requires Windows 11 24H2 or later"></a>
  <a href="docs/releases/INSTALLATION.md#windows-and-architecture"><img src="https://img.shields.io/badge/architecture-x64_%C2%B7_ARM64-087F89" alt="Supported architectures: x64 and ARM64"></a>
  <a href="LICENSE.md"><img src="https://img.shields.io/badge/licence-source--available-126C64" alt="Wintodo Source-Available Licence"></a>
</p>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/releases/store/artwork/captures/day-dark.png">
  <img src="docs/releases/store/artwork/captures/day-light.png" alt="Wintodo’s My Day view gathers six tasks from three lists, with stars and due dates beside the tasks.">
</picture>

## Highlights

- **Plan across lists.** Pull tasks into *My Day*, star what matters, and open *Planned* to see what’s due. Add steps, notes, files, and repeat schedules to any task.
- **Bring your lists along.** Choose which Microsoft To Do lists to copy in a one-time import. Your originals stay untouched. You can also import and export iCalendar (`.ics`) files.
- **Stay on the keyboard.** Press `Ctrl+N` to add a task, `Ctrl+F` to find one, and `Space` to mark it complete. Use `Ctrl+Z` to undo multiple changes.
- **Use Windows reminders.** Get reminders even when Wintodo is closed, add tasks through Windows Share, or jump to a list from the taskbar. Light, dark, and high contrast themes are supported.
- **Work without an account.** Wintodo stores tasks locally in SQLite, with optional CalDAV sync. There are no ads or analytics. Read the [privacy policy](docs/releases/PRIVACY.md).

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

Wintodo uses WinUI 3 and .NET 10 Native AOT. To build it, use the .NET SDK pinned in [`global.json`](global.json), WinApp CLI 0.7+, and Windows 11 with Developer Mode enabled.

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
