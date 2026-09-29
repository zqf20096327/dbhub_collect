# Sleeper Fantasy Football Draft Tracker for Tidbyt

A Tidbyt app that displays live Sleeper fantasy football draft information on a physical Tidbyt device.

The app was originally built for a live dynasty rookie draft and is designed to provide an at-a-glance view of the current draft state without requiring the Sleeper app to remain open on a phone or computer.

## Features

The live app automatically retrieves Sleeper draft data and displays the appropriate screen based on the current state of the draft.

### Pre-Draft Screen

Before the draft begins, the app displays:

* The team holding the first pick
* The draft start time
* A pre-draft status message
* The team avatar when available

### On-the-Clock Screen

While a draft is active, the app displays:

* The current pick number
* The fantasy team currently on the clock
* The team avatar
* A live countdown timer
* An on-the-clock status message

### Pick-Confirmed Screen

After a player is selected, the app temporarily displays:

* The completed pick number
* The selected player
* The player position and NFL team
* A confirmation message
* The selecting team's avatar

After the confirmation period ends, the display returns to the next on-the-clock screen.

### Draft-Complete Screen

Once the draft is finished, the app displays a completion screen instead of continuing to show an active draft timer.

### Traded Pick Handling

The app checks Sleeper's traded-pick data so that the displayed team reflects the current owner of a draft pick rather than only the roster originally assigned to that draft slot.

### Avatar Fallback

The app attempts to retrieve each team's Sleeper avatar. If an image cannot be loaded, the app falls back to a basic placeholder rather than crashing.

## Repository Structure

```text
sleeper-tidbyt/
├── app/
│   └── sleeper_draft.star
│
├── live-app/
│   └── sleeper_live.star
│
├── replay-app/
│   └── sleeper_replay.star
│
├── api-test/
│   └── sleeper_api_test.star
│
├── api-list-test/
│   └── list_drafts.star
│
├── api-list-old-test/
│   └── list_user_drafts.star
│
├── run_live.ps1
└── .gitignore
```

### `live-app/sleeper_live.star`

The main live version of the app.

It retrieves the current Sleeper league, draft, roster, user, pick, and traded-pick data before rendering the correct Tidbyt screen.

### `replay-app/sleeper_replay.star`

A historical replay version used for testing draft behavior without waiting for a real draft.

It can reveal a configurable number of historical picks and simulate how recently the latest pick occurred. This makes it possible to test:

* Pre-draft behavior
* On-the-clock behavior
* Pick-confirmation screens
* Countdown resets
* Draft-complete behavior

### `app/sleeper_draft.star`

An early static layout prototype used while designing the screen structure and visual style.

### API Test Files

The API test folders contain small Starlark scripts used during development to inspect Sleeper API responses and confirm the required endpoint behavior before integrating the data into the live app.

## Requirements

To run the app, you need:

* A Tidbyt device
* The Pixlet CLI installed
* Pixlet authenticated with your Tidbyt account
* A Sleeper fantasy football league
* A Sleeper league ID
* Your Tidbyt device ID
* PowerShell if using the included live refresh script

## Configuration

### 1. Set the Sleeper League ID

Open:

```text
live-app/sleeper_live.star
```

Find:

```python
LEAGUE_ID = "YOUR_SLEEPER_LEAGUE_ID"
```

Replace the placeholder with the Sleeper league ID for the draft you want to track.

### 2. Set the Draft Start Time

Sleeper may not always provide a usable draft start-time value through the draft response.

Inside:

```text
live-app/sleeper_live.star
```

set:

```python
DRAFT_START_TEXT = "8:00 PM"
```

to the time you want displayed on the pre-draft screen.

### 3. Set the Tidbyt Device ID

Open:

```text
run_live.ps1
```

Find:

```powershell
$DeviceId = "YOUR_TIDBYT_DEVICE_ID_HERE"
```

Replace the placeholder with your Tidbyt device ID.

### 4. Confirm the Installation ID

The default installation ID is:

```powershell
$InstallationId = "sleeperdraft"
```

The installation ID should contain only letters and numbers.

### 5. Adjust the Refresh Frequency

The PowerShell script currently renders and pushes the latest draft state every few seconds:

```powershell
$RefreshSeconds = 3
```

You may adjust this value based on your preferred refresh cadence.

## Running the Live App

From the repository root, run:

```powershell
.\run_live.ps1
```

The script will continuously:

```text
Render the latest Sleeper draft state
        ↓
Push the generated WebP to the Tidbyt
        ↓
Wait for the configured refresh interval
        ↓
Repeat
```

Stop the loop with:

```text
Ctrl + C
```

## Local Preview

To preview the live Starlark app locally:

```powershell
pixlet serve .\live-app\sleeper_live.star
```

Then open the local Pixlet preview in a browser.

For historical testing, preview the replay app instead:

```powershell
pixlet serve .\replay-app\sleeper_replay.star
```

## Sleeper API Data Used

The app retrieves data from Sleeper API endpoints related to:

* League information
* Draft information
* Draft picks
* League users
* Rosters
* Traded draft picks

The data is used to determine:

* Whether the draft has started
* Whether the draft has completed
* Which team is currently on the clock
* Whether the current pick was traded
* Which player was most recently selected
* How much time remains on the current pick

## Development Notes

This project was built for a real live fantasy football draft and successfully displayed:

* The pre-draft screen
* The active on-the-clock screen
* A countdown that refreshed throughout the draft
* Completed-pick confirmations
* The draft-complete state

The primary issue observed during the live draft was that several rapid-fire selections could cause pick-confirmation screens to be replaced before every pick was displayed for the intended amount of time.

## Planned Improvements

Future improvements may include:

* A queue for rapid-fire pick-confirmation screens
* Cleaner configuration separation for local settings
* Additional replay controls for testing
* Improved fallback behavior for missing avatar data
* More polished local setup instructions
* Screenshots or GIFs demonstrating the physical Tidbyt output

## Security Notes

Do not commit:

* Tidbyt API tokens
* Personal credentials
* Private configuration files
* Real device IDs unless intentionally shared
* Sleeper league IDs unless the league data is safe to expose publicly

Generated WebP preview files are excluded through `.gitignore`.

## Related Project

A separate season-long Sleeper fantasy football Tidbyt app is also under development. That project is designed to display standings, weekly matchup scoreboards, pinned matchups, and future scoring alerts during the NFL season.

## License

This project is intended for personal and educational use.
