# TeknoParrot Manager

![TeknoParrot Manager](images/banner.png)

TeknoParrot Manager is a Windows PowerShell tool for managing TeknoParrot arcade libraries on Windows. It registers extracted games, propagates controls, deploys lightgun crosshairs, applies ReShade and dgVoodoo2 compatibility fixes, and exports libraries to LaunchBox.

TeknoParrot Manager is made for beginners and is also useful if you already know TeknoParrot. It hides complexity, not detail. Repeatable bulk steps (AutoSync, Register, Propagate Controls) save manual work. Where it changes your files it says so, makes a backup first, and shows what it did under Details and in the log. It keeps four things apart: games found, games registered, a game that launches, and controls that are set up. See [Advanced users](docs/ADVANCED-USERS.md).

Canonical links: [GitHub repository](https://github.com/Jumpstile/teknoparrot-manager) | [Releases](https://github.com/Jumpstile/teknoparrot-manager/releases) | [Issue tracker](https://github.com/Jumpstile/teknoparrot-manager/issues)

This guide is for v1.0 RC9.3.

**Jump to:** [Quick Start](QUICKSTART.md) | [Full user guide](docs/USER-GUIDE.md) | [Changelog](TeknoParrot-Manager-CHANGELOG.txt) | [Troubleshooting](docs/TROUBLESHOOTING.md) | [Start Here (first game in 10 minutes)](docs/START-HERE.md)

## Download

Release page of the latest published release: [v1.0 RC9.3](https://github.com/Jumpstile/teknoparrot-manager/releases/tag/v1.0-RC9.3).

1. Download the ZIP file from the release page.
2. Extract the whole package to a short folder outside Program Files, for example `C:\TPM`. Keep all the folders.
3. Double-click **`TeknoParrot-Manager.bat`**.

TeknoParrot Manager does not install TeknoParrot. Install TeknoParrot first. [Start Here](docs/START-HERE.md) shows how.

## What it does

These are the main things TeknoParrot Manager can do:

**Set up your games**

- **AutoSync (menu 1).** Unpacks your game ZIPs and adds the games to TeknoParrot in one run. It works from a network drive or a local folder and leaves unchanged games alone. It backs up your TeknoParrot settings (UserProfiles) first.
- **Register only (menu 2).** Adds games you already extracted. It finds each game, picks the right game path, and never overwrites a game that is already added. One exception: if an already-added game's saved path points into another game's folder, TeknoParrot Manager fixes it to the game's own folder. It backs up first and writes the change to the log.
- **LaunchBox integration (menu 3).** Adds your registered games to LaunchBox, fills in details and playlists, groups the versions of a game, links art, and keeps LaunchBox in step with TeknoParrot. It opens the LaunchBox choices any time, without registering or extracting anything first. If you have no LaunchBox yet, it tells you so and how to continue.
- **Matches hard-to-name games.** It uses folder names, game codes and an optional community game list to work out which game is which.

**Controls, picture and fixes**

- **Propagate Controls (menu 4).** Set up one game of each control type. TeknoParrot Manager copies those controls to similar games that have none. It never invents a binding.
- **Crosshair setup (menu 5).** Gives lightgun games custom player 1 and player 2 crosshairs.
- **ReShade setup (menu 6).** Adds picture effects (shaders) to the games you pick. You can also use bezel pictures you already have.
- **dgVoodoo2 setup (menu 7).** Fixes older games that crash or show a black screen on old graphics settings.
- **GPU fix setup (menu 8).** Detects AMD, NVIDIA or Intel and applies the matching fix.
- **Force feedback setup (menu 9).** Sets up the native FFB Blaster (membership) or a free third-party plugin for wheel games. The plugin comes in the newest release, with each game's own settings file. It lists your game controllers by name (Xbox, PlayStation, wheel). It recognizes old plugin files and upgrades them after a backup. It always asks first.
- **BepInEx setup (menu

[...截断...]

 10).** Installs or updates BepInEx for the games that need it, after you approve.
- **Region setup (menu 11).** Pick the country your games start in, choose which games, confirm, and switch back to automatic any time.
- **Postgres setup (menu 12).** Sets up the local PostgreSQL database that some Incredible Technologies games need.
- **Required game patches (menu 13).** Finds a required fix, checks it against your own ZIP, backs up first, installs it, verifies it, and can undo it.

**Check, protect and update**

- **Library health check (menu 14).** Reports what is registered, broken or missing, without changing anything. It knows the TeknoDOS game type.
- **Restore backup (menu 15).** Puts profiles, LaunchBox library files or Postgres databases back from an earlier copy.
- **Check for Updates (menu 16).** Downloads a new release, checks it, installs it, and puts everything back if something goes wrong. Available from RC8.1.
- **Create Support Package (menu 17).** Gathers safe logs and reports into one ZIP to attach to a bug report.

**For beginners**

- **Plain-language screens.** Short messages and one clear next step. Press **D** on a screen for the technical details.
- **Preview mode.** Shows the planned changes without making them.

The [full user guide](docs/USER-GUIDE.md) describes every feature step by step.

## Quick start

**Before you start:**

1. Install TeknoParrot into its own folder, such as `C:\TeknoParrot`. Never use the installer's default `C:\Windows\system32`.
2. Open `TeknoParrotUi.exe` yourself, one time. Click OK, OK, and Accept and Continue on the pop-up windows. You may use Skip Setup.
3. Keep your games as ZIP files (for AutoSync) or already extracted into folders.

**Your first run:**

1. Double-click **`TeknoParrot-Manager.bat`** and answer each first-run question. If you are not sure, pick the first choice.
2. At the main menu, type **1** (AutoSync) and press Enter. It unpacks your games and adds them to TeknoParrot.
3. Open TeknoParrot and start one game. Test one game after each run.
4. Stuck? Type **17** to make a support package, or see [Troubleshooting](docs/TROUBLESHOOTING.md).

The normal backup protects UserProfiles (TeknoParrot's saved game settings) only. It is not a whole-game backup.

**The main menu** (type a number and press Enter):

| # | Mode | What it does |
| --- | --- | --- |
| 1 | **AutoSync** | Extract your game ZIPs, then register the games |
| 2 | **Register only** | Register games you already extracted |
| 3 | **LaunchBox integration** | Add your registered games to LaunchBox, fill in details and playlists, link art, keep LaunchBox in step. Works any time, even before you register anything |
| 4 | **Propagate Controls** | Copy known controls to similar games that have none, set up games with your controller layout, check controls, learn your arcade buttons |
| 5 | **Crosshair setup** | Pick and deploy custom crosshairs to lightgun games |
| 6 | **ReShade setup** | Add visual post-processing to game folders |
| 7 | **dgVoodoo2 setup** | Fix some old DX8, DirectDraw, and Glide game crashes or black screens |
| 8 | **GPU fix setup** | Apply the AMD / NVIDIA / Intel fix to registered games |
| 9 | **Force feedback (FFB) setup** | Native FFB Blaster (membership) or a free third-party plugin |
| 10 | **BepInEx setup** | Install or update after you approve, using stable x64/x86 releases |
| 11 | **Region setup** | Pick the country your games start in, choose which games, confirm |
| 12 | **Postgres setup** | Set up the local PostgreSQL database some Incredible Technologies games need |
| 13 | **Required game patches** | Find, check, back up, install, verify, or undo a required fix from your local ZIP |
| 14 | **Library health check** | Report what is registered, broken, or missing, without changing anything |
| 15 | **Restore backup** | Put profiles, LaunchBox library files, or Postgres databases back from an earlier copy |
| 16 | **Check for Updates** | Check GitHub for a newer r