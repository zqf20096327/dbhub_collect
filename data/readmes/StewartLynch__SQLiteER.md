# SQLiteER

[![Latest Release](https://img.shields.io/github/v/release/StewartLynch/SQLiteER?label=release)](https://github.com/StewartLynch/SQLiteER/releases/latest)
[![Download DMG](https://img.shields.io/badge/download-DMG-blue)](https://github.com/StewartLynch/SQLiteER/releases/latest/download/SQLiteER.Installer.dmg)
![Platform](https://img.shields.io/badge/platform-macOS-lightgrey)
![Minimum macOS](https://img.shields.io/badge/macOS-15.0%2B-brightgreen)
![Xcode](https://img.shields.io/badge/Xcode-27%2B-blue)
![Swift](https://img.shields.io/badge/Swift-5-orange)
![License](https://img.shields.io/badge/license-All%20rights%20reserved-lightgrey)

![image-20260613105812812](assets/image-20260613105812812.png)

A native macOS app that turns any SQLite database — including **Core Data**, **SwiftData** and **SQLiteData** stores — into a clean,
interactive entity-relationship diagram you can rearrange and export.

Drag a database file onto the window and SQLiteER reads its schema, lays out every table as a card,
and draws the relationships between them with crow's-foot cardinality notation. Then drag the cards to
taste and export the result as a PNG or PDF.

## Download

Grab the latest installer from the [GitHub Releases page](https://github.com/StewartLynch/SQLiteER/releases/latest), or download the current DMG directly:

[Download SQLiteER.Installer.dmg](https://github.com/StewartLynch/SQLiteER/releases/latest/download/SQLiteER.Installer.dmg)

## Features

- **Open any SQLite file** — `.sqlite`, `.sqlite3`, `.db`, `.mdb`, `.sdb`, or `.store` — via the Open button
  (⌘O) or drag-and-drop.
- **Core Data aware.** Core Data uses a private `Z`-prefixed schema and never declares foreign keys.
  SQLiteER detects a Core Data store and translates it back into clean entity and attribute names,
  hiding the internal bookkeeping tables/columns.
- **Relationship detection** from three sources:
  - **Foreign keys** declared in the schema (teal lines, `FK`).
  - **Inferred joins** from naming conventions like `customerId → customers` (dashed orange,
    `inferred`).
  - **Core Data relationships** — to-one links and `Z_<N>` many-to-many join tables (purple, `rel`).
- **Crow's-foot cardinality.** Each line shows `one` (bar) or `many` (foot) at each end, so 1:1, 1:N,
  and N:M are readable at a glance. One-to-one is detected from single-column `UNIQUE` indexes.
- **Interactive canvas** — drag tables, zoom (35%–160%), and reset the layout (⌘R).
- **Export** the diagram as **PNG** or **PDF** (⌘E).

## Requirements

- macOS 15.0 or later
- Xcode 27 or later (to build)

## Building & Running

Open `SQLiteER.xcodeproj` in Xcode and run (⌘R). The app builds and launches as **SQLiteER**.

> Note: the Xcode project file and source folder are still named `SQLiteER` on disk; only the
> product name (`SQLiteER`) is user-facing.

## How It Works

The app keeps a strict separation between *reading* a database and *drawing* it. Everything downstream
keys off plain table and column names, so the renderer never needs to know where the schema came from.

| File | Responsibility |
|------|----------------|
| `SQLiteERApp.swift` | App entry point and default/minimum window sizing. |
| `ContentView.swift` | Main window: sidebar, toolbar, drop target, file import/export, and the `@Observable` workspace state. |
| `SchemaModels.swift` | Value types for the schema (`DatabaseSchema`, `TableSchema`, `ColumnSchema`, `TableRelationship`). |
| `SQLiteSchemaLoader.swift` | Reads schema via the SQLite3 C API; handles standard **and** Core Data stores; infers relationships and cardinality. |
| `DiagramLayout.swift` | Pure layout math — card placement and connector geometry. |
| `ERDiagramView.swift` | Renders the cards, relationship lines, crow's-foot markers, and drag handling. |
| `DiagramExporter.swift` | Renders the diagram to PNG/PDF with `ImageRenderer`. |

### Reading Notes

- Databases are copied to a temporary location (with their `-wal`/`-shm` sidecars) before reading, so
  the original file is never modified and WAL-pending changes are visible.
- For Core Data stores, entity names come from the authoritative `Z_PRIMARYKEY` table; a relationship
  is only drawn for an **INTEGER** column that matches an entity (so a same-named text attribute, like
  a denormalized `country` string, is correctly *not* treated as a link).

## Tech Stack

- **SwiftUI** for the UI and, via `ImageRenderer`, for export.
- **The raw SQLite3 C API** for read-only schema introspection (no third-party dependencies).
- **The Observation framework** (`@Observable`) for state, in line with the project's preference for
  Swift Concurrency over Combine.

## License

Copyright © 2026 CreaTECH Solutions. All rights reserved.
