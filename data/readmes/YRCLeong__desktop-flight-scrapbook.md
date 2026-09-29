# Flight Scrapbook Desktop

Flight Scrapbook Desktop is a local-first desktop app for aviation enthusiasts who want to keep a personal archive of their flight history. It is a C#/.NET desktop rewrite of the Android beta, using Avalonia for the cross-platform UI and SQLite for local persistence.

The app is not a real-time tracker and does not try to imitate travel credentials. Souvenir exports are memory artwork only and intentionally avoid boarding-pass, barcode, QR-code, or airline-logo behavior.

## Features

- Local SQLite flight archive with no account, backend, or cloud dependency.
- Demo seed catalog for airports, airlines, aircraft types, and 30+ sample flights.
- Manual flight entry with local catalog validation and great-circle distance calculation.
- Official CSV template import with row-level validation.
- Flight list filtering by search text, year, airline, aircraft, and favorites.
- Overview statistics, rankings, yearly summaries, and achievements.
- Offline 2D route map rendered in Avalonia.
- Offline Cesium globe page hosted through Avalonia WebView when available.
- Souvenir PNG exports through SkiaSharp, with recent export history, open-file/open-folder actions, and copy-path support.

## Requirements

- .NET 10 SDK 10.0.300 or newer 10.0 feature band.
- Windows 10/11, macOS, or Linux supported by Avalonia.

This repository includes `global.json` so local development uses .NET 10 when installed.

## Run

```powershell
dotnet restore FlightScrapbook.DesktopApp.slnx
dotnet run --project src/FlightScrapbook.Desktop/FlightScrapbook.Desktop.csproj
```

## Test

```powershell
dotnet test FlightScrapbook.DesktopApp.slnx
```

The test suite covers core math/import/stats behavior, SQLite persistence, ViewModel actions, PNG export, and an Avalonia headless smoke test.

## Publish

```powershell
.\scripts\publish.ps1 -Runtime win-x64
.\scripts\publish.ps1 -Runtime linux-x64
.\scripts\publish.ps1 -Runtime osx-x64
```

Published files are written to `publish/<runtime>`.

## Data Location

The desktop app stores user data under the current user's local application data directory in `FlightScrapbookDesktop`. Exports are written to an `exports` folder under that directory.

## Project Structure

- `src/FlightScrapbook.Core`: domain models, geodesic math, CSV import, statistics, achievements, and export artifact specs.
- `src/FlightScrapbook.Data`: SQLite schema, seed data persistence, import batches, and repository implementation.
- `src/FlightScrapbook.Desktop`: Avalonia UI, ViewModels, offline map/globe controls, path service, and PNG export service.
- `tests/FlightScrapbook.Tests`: automated tests for core, data, desktop ViewModel, export, and smoke behavior.

## Changelog

See `CHANGELOG.md` for release notes.

## License

MIT. See `LICENSE`.
