<div align="center">

<img src="src-tauri/icons/128x128@2x.png" alt="Avenqor icon" width="128" height="128">
<br>
<img src="Avenqor-logo.png" alt="Avenqor icon" width="200" height="200">
</br>

**A local-first project manager for Windows and Android.**
Organize workspaces, projects, tasks, deadlines, and documents in one place, on your own computer or phone, with no account and no internet.

![Version](https://img.shields.io/badge/version-1.1.0-4a3de0)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Android-0078D6)
![License](https://img.shields.io/badge/license-Apache%202.0-blue)
![Tauri](https://img.shields.io/badge/Tauri-2-24C8DB)
![React](https://img.shields.io/badge/React-19-61DAFB)
![TypeScript](https://img.shields.io/badge/TypeScript-6-3178C6)
![SQLite](https://img.shields.io/badge/SQLite-local-003B57)

</div>

<p align="center">
  <img src="docs/screenshots/dashboard.png" alt="Avenqor Dashboard" width="860">
</p>

> **Version 1.1.0** adds the **Android version** to the Windows program of version 1.0.0. The Windows features below were tested by the developer on Windows 10; the Android version was tested by the developer on one Android phone (see [docs/MOBILE.md](docs/MOBILE.md)). The dated test logs are in [docs/DEVELOPMENT_STATUS.md](docs/DEVELOPMENT_STATUS.md) and [docs/MOBILE.md](docs/MOBILE.md). Avenqor is a one-person project, so expect rough edges and please report them as [issues](https://github.com/andra-gs/Avenqor/issues).

## Contents

- [Download](#download)
- [What is Avenqor?](#what-is-avenqor)
- [Features](#features)
- [Your data stays with you](#your-data-stays-with-you)
- [For programmers](#for-programmers)
- [Getting started](#getting-started)
- [Roadmap](#roadmap)
- [Documentation](#documentation)
- [License](#license)

## Download

All downloads are on the **[latest release page](https://github.com/andra-gs/Avenqor/releases/latest)**, under "Assets". Both files are **not** code-signed by a company (a certificate costs money), so Windows and Android show a warning; the steps below explain it. Each release page lists the SHA-256 checksum of every file.

### Windows

File named like `Avenqor_1.1.0_x64-setup.exe`.

1. Run the downloaded file. It installs Avenqor for your Windows user only, so no administrator password is needed.
2. Windows may show **"Windows protected your PC"** (SmartScreen). Click **More info**, then **Run anyway**. You can compare the file's SHA-256 checksum, given on the release page, with the result of `Get-FileHash .\Avenqor_1.1.0_x64-setup.exe` in PowerShell.
3. Start Avenqor from the Start menu. Your data is saved on your computer (see [Your data stays with you](#your-data-stays-with-you)).

Requirements: Windows 10 (version 1803 or later) or Windows 11, 64-bit. **Uninstalling** keeps your data unless you tick the option to delete the application data. To move to another computer, use **Settings, Backup and restore**.

### Android

File named like `Avenqor_1.1.0_android-arm64.apk`. It is not in the Google Play Store.

1. Download the file on the phone, or copy it there from a computer.
2. Open it. Android asks you to allow installing apps from this source (the browser or the file manager you used): allow it. This setting is "Install unknown apps" in the phone's settings.
3. Android or Google Play Protect may warn that the app is from an unknown developer. This is expected for an app outside the Play Store. Choose to install anyway.
4. Open Avenqor. The data stays on the phone, in the app's private storage.

Requirements: Android 7.0 or newer, on a phone with a 64-bit ARM processor (most phones made in recent years). The Android version was tested by the developer on one phone only, so other phones may behave differently. **Updating:** install a newer APK over the old one; your data stays (the file is always signed with the same key). **Uninstalling the app deletes its data**, so export a backup first (Settings, Data). **Phone and computer do not share data**: there is no synchronization. To move your work between them, export a backup on one and restore it on the other.

## What is Avenqor?

Avenqor is a desktop app for people who juggle several pieces of work at once: university students with group assignments, programming students and small dev teams, independent developers, and content creators with production workflows.

Work is organized in three levels:

```
Workspace  →  Project  →  Tasks (and their checklists, notes, labels, documents)
```

For example, the workspace **Informatics Group** can hold the projects **Final Semester Project** and **Portfolio Website**. Each project has its own board, tasks, deadlines, documents, and activity.

Avenqor works **fully offline**. Nothing is sent anywhere, and no account is needed. It is a single-user app today: data on one computer is not shared with other computers, and the app does not pretend otherwise.

## Features

Every item below is implemented and has been tested by the developer.

### Dashboard and workspaces

See your workspaces, recent projects, the tasks assigned to you, and recent activity at a glance. Create, rename, and delete workspaces; each shows its projects and activity.

### Projects and tasks

Create, edit, archive, restore, and delete projects. Tasks have a title, description, status, priority, and deadline. Project **progress is calculated** from the tasks in Done, never typed in. Each task page also has:

<p align="center">
  <img src="docs/screenshots/task.png" alt="Task page with checklist, notes, and labels" width="760">
</p>

- a **checklist** (add, tick, edit, remove),
- **notes** (newest first, editable),
- **labels** with colors, defined per project.

### Kanban board

Four columns: To Do, In Progress, Review, Done. **Drag a card** to another column, or use the arrow buttons. Priorities, deadlines, and labels show on each card, and every move is saved right away.

<p align="center">
  <img src="docs/screenshots/board.png" alt="Kanban board" width="860">
</p>

### Calendar, deadlines, and My Tasks

A month calendar shows task deadlines, with overdue ones in red. An upcoming-deadline list sits next to it. **My Tasks** lists everything assigned to you across all active projects, with a status filter.

<p align="center">
  <img src="docs/screenshots/calendar.png" alt="Calendar with deadlines" width="860">
</p>

### Project documents

Keep notes, requirements, meeting notes, API references, and UI/UX decisions next to the work. Documents are plain text, searchable by title, and can be filtered by type and project.

<p align="center">
  <img src="docs/screenshots/documents.png" alt="Documents page" width="860">
</p>

### Activity history

Important changes (creating, editing, moving, archiving, deleting) are recorded locally. The Dashboard, the workspace page, and the project page show the newest 8, with a link to the full list.

### Search and filters

One search box in the top bar (`Ctrl+K`) finds workspaces, projects, tasks, and the text of documents. On a project page you can filter the task list by status, priority, and label.

### Deadline reminders

Optional: once a day Avenqor shows a Windows notification for your tasks that are due today or overdue. Reminders appear only while the app is open, and Windows shows notifications for installed apps.

### Backup and restore

Export all your data to one readable JSON file, and restore it later. A restore **replaces everything**, so Avenqor first requires you to save a safety backup of your current data, and it checks the file completely before it changes anything. A file that is damaged or not made by Avenqor is refused with a clear message.

<p align="center">
  <img src="docs/screenshots/backup.png" alt="Backup and restore in Settings" width="760">
</p>

### Interface

Clean light theme, DM Sans font, indigo accent (one accent color for every progress bar), a collapsible sidebar, and a custom title bar that shows where you are (for example *Workspace / Project / Board*). The window works down to 960x600. On a phone (a screen narrower than 768 px) the sidebar is replaced by a bottom navigation bar with a Menu page, the top bar has two rows, and lists and forms fit the screen width.

## Your data stays with you

- All data is stored in one SQLite file, `avenqor.db`, in `%APPDATA%\io.github.andra-gs.avenqor` on Windows. It is **not** in the installation folder, so uninstalling or updating the program does not touch it.
- Avenqor makes no network requests for its features. (The first *build* from source downloads packaging tools; running the app does not.)
- On Android the database lives in the app's private storage on the phone. Data on the phone and on a computer is separate: nothing is synchronized.
- A backup file contains your workspaces, projects, tasks, checklists, notes, labels, documents, and activity history. It does not contain program settings, because there are none yet, and it is not encrypted: store it somewhere you trust.

## For programmers

### Stack

| Layer | Choice |
|---|---|
| Desktop shell | [Tauri 2](https://tauri.app) (Rust) with Microsoft Edge WebView2 |
| Interface | React 19, TypeScript, Vite, React Router (hash routing) |
| Styling | Tailwind CSS 4, with all colors, sizes, and radii defined once as design tokens |
| Database | SQLite through the official Tauri SQL plugin, with numbered migrations |
| Files | Tauri dialog and fs plugins, used only for backups |

### Architecture in one picture

```
Page  →  Feature (sections)  →  Hook  →  Service  →  Repository  →  SQLite
                                          rules,       only SQL
                                          validation
```

- **Pages compose, hooks fetch.** A page arranges sections; data comes from hooks. Components never touch the database.
- **Services** hold the business rules (validation, UUIDs, progress). **Repositories** are the only code that writes SQL, always with parameters.
- **Base components** (`src/components/ui`) accept no `className`, so the look of the app can only change in one component or in `src/styles/tokens.css`. Changing the accent color in that single file recolors every screen.
- **Activity history is written by SQLite triggers**, not by app code, so a change and its history entry are saved atomically.
- **Restore is one SQL script** (`BEGIN IMMEDIATE … COMMIT`) sent in one call, because the SQL plugin may use a different connection per call. Backup files are treated as untrusted input.
- **Least privilege:** the permission file lists only what the app needs, and the frontend can reach only files the person picks in the system file windows.

Data conventions: UUID text IDs, deadlines as `YYYY-MM-DD`, timestamps as UTC ISO 8601, and no stored progress. The database has 11 tables (schema version 6): profiles, workspaces, workspace members, projects, tasks, checklist items, notes, labels, task labels, documents, and the activity log. Workspace members and the local profile are already in place so that roles (owner, admin, member, guest) can be supported when collaboration arrives.

Details: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) and [docs/DATABASE_SCHEMA.md](docs/DATABASE_SCHEMA.md).

### Project layout

```
src/
  app/ assets/ components/ features/ pages/ hooks/ services/ repositories/ lib/ styles/ types/
src-tauri/
  src/            Rust entry point and plugin registration
  migrations/     numbered SQL migrations (never edited after release)
  capabilities/   Tauri permissions
docs/             documentation
```

## Getting started

If you only want to use Avenqor, [download the installer](#download). The rest of this section is for running it from source.

### Prerequisites (Windows)

From the [Tauri prerequisites](https://v2.tauri.app/start/prerequisites/):

1. **Microsoft C++ Build Tools** with the **"Desktop development with C++"** workload (installing the Build Tools alone is not enough; use Visual Studio Installer, Modify).
2. **Microsoft Edge WebView2** (already part of Windows 10 1803+ and Windows 11).
3. **Rust**, installed with `rustup`, using the MSVC toolchain (`rustup default stable-msvc`). The SQL plugin needs Rust 1.90 or newer.
4. **Node.js** LTS with npm.

Check what you have in PowerShell:

```powershell
node -v
npm -v
rustc --version
cargo --version
rustup show
```

If `npm` says "running scripts is disabled on this system", run this once and try again:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

### Run in development

```powershell
git clone https://github.com/andra-gs/Avenqor.git
cd Avenqor
npm install
npm run tauri dev
```

The first run compiles all Rust dependencies (about 18 minutes on the developer's computer); later runs are faster. Close the window and press `Ctrl+C` to stop.

### Build a Windows release

```powershell
npm run tauri build
```

The first build took about 34 minutes and downloads the WiX and NSIS packaging tools from GitHub. Output is in `src-tauri\target\release\`: the program `project-manager.exe`, an MSI installer in `bundle\msi\`, and an NSIS installer in `bundle\nsis\`. The NSIS installer (`-setup.exe`) was installed, tested, and uninstalled on the developer's computer (reported 2026-11-01); the MSI installer was not tested.

### Build the Android app

Android needs extra tools (Android Studio, the Android SDK and NDK, Java, and four Rust targets) and a signing key for release builds. The full steps, with the commands, are in [docs/MOBILE.md](docs/MOBILE.md). In short, after the setup:

```powershell
npm run tauri android build -- --apk --target aarch64
```

This builds a release APK; without a signing key (`keystore.properties`, which is never committed) the file is named `...-unsigned.apk` and cannot be installed. Use the debug build (`--debug`) with a USB cable for testing. Do not use `npm run tauri android dev`: on the developer's phone it showed a white screen (see MOBILE.md).

### Useful commands

| Command | What it does |
|---|---|
| `npm run tauri dev` | Starts the desktop app with live reload |
| `npm run build` | Type-checks (`tsc`) and builds the frontend; must pass before every commit |
| `npm run tauri build` | Builds the release program and installers |

There is no automated test suite yet. Features are tested by hand and the results are logged with dates in [docs/DEVELOPMENT_STATUS.md](docs/DEVELOPMENT_STATUS.md).

## Roadmap

| Phase | Goal | State |
|---|---|---|
| 0 | Environment and project setup | Done |
| 1 | Interface foundation | Done |
| 2 | SQLite, workspaces, projects, tasks | Done |
| 3 | Board, calendar, task details, documents, activity | Done |
| 4 | Backup and restore, search and filters, validation review, local notifications | Done |
| 5 | GitHub integration | Future |
| 6 | Online accounts, sync, shared workspaces | Future |
| 7 | Web, iOS, and AI assistance (Android came earlier, as version 1.1) | Future |

**Version 1.0** (Windows) is Phase 4 plus release preparation. **Version 1.1** adds the Android version (same code base, recorded in [docs/MOBILE.md](docs/MOBILE.md)). After that, a bigger update: documents as files and folders, and a whiteboard for each workspace (details in [docs/PROJECT_OVERVIEW.md](docs/PROJECT_OVERVIEW.md)). GitHub and online features are later phases.

Known limitations today: no subtasks, no templates, reminders only while the app is open, and single-user only. The database folder on Windows is in Roaming (see Known issues in the status file). On Android: the icon in the status bar for notifications may still show the old icon, dragging a board card by touch was not tried (use the arrow buttons), and iOS is not supported.

## Documentation

| File | What it covers |
|---|---|
| [CLAUDE.md](CLAUDE.md) | Project instructions and development rules |
| [docs/PROJECT_OVERVIEW.md](docs/PROJECT_OVERVIEW.md) | Goals, target users, MVP scope, roadmap, future plans |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | How the application is structured, and why |
| [docs/DATABASE_SCHEMA.md](docs/DATABASE_SCHEMA.md) | SQLite tables and migrations |
| [docs/DEVELOPMENT_STATUS.md](docs/DEVELOPMENT_STATUS.md) | What is done, tested, broken, and next |
| [docs/MOBILE.md](docs/MOBILE.md) | The Android version: decisions, setup, plan |
| [docs/BRAND.md](docs/BRAND.md) | Brand identity notes (in Indonesian) |

## About

Avenqor is built by [Andra](https://github.com/andra-gs) as a learning project, together with Claude (Anthropic) as an AI development partner. The developer reports that no registration of the name Avenqor was found in Indonesia or internationally (stated 2026-11-01; not checked by Claude, and not legal advice).

## License

Avenqor is released under the **[Apache License 2.0](LICENSE)** (chosen by the developer on 2026-11-04). In plain words, and not legal advice: anyone may use, copy, modify, and share Avenqor, including in their own or commercial projects, **as long as they give credit**. Concretely, you must keep the [LICENSE](LICENSE) text and the copyright and attribution notices in the [NOTICE](NOTICE) file with every copy or derived work, and you must mark files you changed. The license does not give anyone the right to use the name "Avenqor" or its logo as the name of their own product. The software is provided "as is", without warranty.

Avenqor uses open-source libraries (for example Tauri, React, and the DM Sans font), each under its own license. Copies of Avenqor published before this date (versions 1.0.0 and 1.1.0) were released before the license was added; the license applies to the code in this repository from now on.
