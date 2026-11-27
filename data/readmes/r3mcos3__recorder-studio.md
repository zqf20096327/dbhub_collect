# Recorder Studio

[![Open your Home Assistant instance and open this repository in the Marketplace.](https://my.home-assistant.io/badges/marketplace_repository.svg)](https://my.home-assistant.io/redirect/marketplace_repository/?owner=r3mcos3&repository=recorder-studio&category=integration)

**Take control of what Home Assistant records, from a modern sidebar panel instead of YAML.**

Home Assistant's `recorder` stores the state history of every entity in a database. Over time a handful of noisy
entities (uptime counters, link quality, signal strength, …) can account for most of it. Recorder Studio shows you
exactly which entities take up how much of the database, lets you stop recording them with a toggle, and cleans up the
history that is no longer wanted.

> **SQLite only.** This integration manages Home Assistant's SQLite database. If you use (or want to use) **MariaDB or PostgreSQL**, or want the recorder database run for you, see the **[Recorder Studio DB add-on](https://community.home-assistant.io/t/recorder-studio-db-an-add-on-that-runs-mariadb-postgresql-or-sqlite-for-your-recorder-with-recorder-studio-built-in/1035261)**: it contains everything on this page and runs SQLite, MariaDB or PostgreSQL.

![Overview](docs/images/overview.png)

## Features

- **Per device / per entity recording control.** Switch recording on or off for a whole device or a single entity,
  review the changes, then save them in one go. The result is written to a generated `recorder_studio.yaml`.
- **See what fills your database.** Total, current and obsolete records, the top entities, and **each entity's and
  device's share of the database in percent**.
- **See how big the database is.** The total size (database + WAL + SHM) is always shown next to the title. After an
  analysis you also get the size per table (states, attributes, statistics, events, …) including indexes, and how much
  unused space a repack would return to the disk.
- **Suggestions.** A list of entities that look like noise (diagnostic or technical values, big share of the database),
  with the space excluding them would save. One click queues the exclusion; entities with long-term statistics get a
  warning, and you can hide suggestions you do not want.
- **Growth and trend.** Records written in the last 24 hours (the real ingest rate, unaffected by purges), the busiest
  entities, a chart of the database size over time and, when the file keeps growing, a forecast of when the disk is full.
- **Size per entity.** Besides record counts, an estimate of the space each entity and device takes, including its
  attribute data, with sorting by size.
- **Alerts.** Raises a Repairs alert when the disk runs low, is filling up or the database grows fast. It checks every few
  hours, also while the panel is closed.
- **Search and filter.** Search by entity id, name, device or platform; filter by domain or status (recorded, excluded,
  excluded but still has history); sort by name or by share of the database.
- **Safe maintenance.** Every purge dialog shows how old your latest Home Assistant backup is. Purge by retention, purge the history of excluded entities, purge a single entity or a whole
  device, repack the database, restart Home Assistant. Every destructive action shows its estimated impact and asks for confirmation;
  bulk purges require typing `PURGE`.
- **Orphaned exclusions.** Finds excluded entities that no longer exist and have no history, with a one-click clean-up.
- **Guided migration.** Finds existing recorder settings by itself (inline in `configuration.yaml`, the file it includes,
  GUI Recorder, packages or any other YAML file), or takes a file path or pasted YAML, and switches `configuration.yaml`
  to the generated file, with a diff preview and an automatic backup.
- **Follows your theme.** Light and dark, responsive down to phone width, keyboard accessible.

![Entities](docs/images/entities.png)

*(Screenshots from a real Home Assistant installation.)*

## Requirements

- Home Assistant 2024.11 or newer, with the default **SQLite** recorder.
- An admin user (the panel and its API are admin-only).
- No Node or Python tooling: the panel is plain JavaScript with [Lit](https://lit.dev) bundled in.

## Installation

### Marketplace / HACS (recommended)

Home Assistant 2026.11 and newer have the **Marketplace** built in (it replaced HACS); older versions use [HACS](https://hacs.xyz).

1. Open the Marketplace (**Settings > Marketplace**, or HACS on older versions) and search for **Recorder Studio**
   (it is in the default catalog), or click the button at the top of this page.
2. Download **Recorder Studio** and restart Home Assistant.
3. Go to **Settings > Devices & services > Add integration** and choose **Recorder Studio**.
4. Open **Recorder Studio** in the sidebar. Later updates show up as an update entity under **Settings > Updates**.

### Manual

Copy the `custom_components/recorder_studio/` folder into `<config>/custom_components/`, restart Home Assistant and
continue with step 3 above.

## First steps

1. **Open the panel.** The data is live: the panel analyses the database by itself when it opens and then keeps
   the record counts and sizes up to date in the background (read-only). The per-table sizes read every page of the
   file, so they are refreshed every 10 minutes; *Re-analyse* on the Overview tab forces a full refresh.
2. **Check the situation.** The Migration tab tells you whether `configuration.yaml` already includes
   `recorder_studio.yaml`. If not, a blue banner offers a *Set up* shortcut.
3. **Migrate** once (see [Migration](#migration)).
4. **Pick what to stop recording** on the Entities tab, save. It applies right away, no restart (only the first activation and a changed database URL or commit interval need one).
5. **Clean up** the history you no longer want on the Maintenance tab.

## The tabs

| Tab | What it does |
| --- | --- |
| **Overview** | Total / current / obsolete records, database size split into file / WAL / SHM, records or estimated size per entity, composition chart, suggestions, growth and trend, the busiest entities of the last 24 hours, size per table and reclaimable space. *Obsolete* means records that still exist for entities that are now excluded. |
| **Entities** | Device tree with a recording toggle per device and per entity, records and share per row, search, filters and sorting. Changes stay pending until you press **Save changes** (a bar at the bottom shows how many). A trash button on every entity and every device purges its history (the impact is shown first). |
| **Maintenance** | Purge by retention, purge excluded entities, repack, restart Home Assistant. |
| **Orphans** | Excluded entities that no longer exist anywhere and have no history. Remove them in bulk; nothing is deleted from the database. |
| **Migration** | Import an existing recorder config from any of the detected sources, a file or pasted YAML, and get the exact `configuration.yaml` change to apply yourself. |
| **Settings** | Retention (`purge_keep_days`), auto purge, auto repack, commit interval, optional manual rules and the alert thresholds. |

### Manual rules

Individual entities are managed with the toggles. For broader rules, the Settings tab accepts a small YAML block:

```yaml
exclude:
  entity_globs:
    - sensor.*_uptime
  domains:
    - update
  event_types:
    - call_service
include:
  domains: []
  entity_globs: []
```

Only `exclude.{domains,entity_globs,event_types}` and `include.{domains,entity_globs}` are accepted. Anything else
(including `entities`, which the toggles own) is rejected with a message and never written.

## Maintenance

![Maintenance](docs/images/maintenance.png)

> **Purges are permanent and cannot be undone. Make a full Home Assistant backup first.**

- **Purge by retention** calls `recorder.purge` with your `purge_keep_days` and deletes everything older.
- **Purge one entity or a device** (trash buttons on the Entities tab) calls `recorder.purge_entities` with
  `keep_days: 0` for exactly the entities shown in the dialog. A device purge always covers all entities of that device,
  even when a search filter is active. If some of them are still recorded, the dialog says so.
- **Purge excluded entities** calls `recorder.purge_entities` with `keep_days: 0` for all currently excluded
  entities, ignoring retention. The dialog shows the entities, records and approximate size first.
- **Repack** calls `recorder.purge` with `repack: true` (so retention is applied too). It needs free disk space of
  roughly the database size and can block the recorder for several minutes.
- **Restart Home Assistant** is only needed for the first activation, a changed database URL or commit interval. Home Assistant validates the
  configuration first and refuses to restart on errors.

Purges are queued by the recorder. After a purge the panel keeps re-analysing until the records are gone, and the live updates take over after that.

## Suggestions, growth and alerts

![Suggestions](docs/images/suggestions.png)

- **Suggestions** are a heuristic, not a verdict. Only sensors, binary sensors, updates, numbers, selects, text, buttons,
  events, images and the sun are ever suggested; lights, switches, climate, locks, covers and the like never are.
  Diagnostic entities and names such as *uptime*, *linkquality* or *rssi* score highest. Entities with a `state_class`
  feed long-term statistics (and possibly the Energy dashboard), so they are shown with a warning and are not counted in
  the "could save" total; energy, battery, temperature and similar device classes are not suggested unless they are
  diagnostic. Excluding goes through the normal pending-changes bar and applies live like any other exclusion.
- **Growth** uses the real number of records written in the last 24 hours. The size chart needs a few days of history:
  one snapshot per day is kept (about 13 months at most), also while the panel is closed. The forecast only appears while
  the file is really growing.
- **Size per entity** is an estimate: the entity's share of the `states` table plus its attribute data. The attribute
  measurement is the slowest query Recorder Studio runs, so it is repeated at most once an hour, is aborted after 20
  seconds and is read-only like everything else.
- **Alerts** appear under **Settings > System > Repairs**: *disk space is low* (free space below your percentage),
  *the database is filling the disk* (forecast of 30 days or less) and *the database is growing fast* (more than your
  percentage in a week). They clear by themselves. Thresholds are on the Settings tab and apply without a restart.
- The **backup check** in purge dialogs reads the list of Home Assistant backups. If that cannot be read it says so and
  never blocks the purge.

## How it works

1. Your choices are stored in `.storage/recorder_studio.data` and rendered to **`recorder_studio.yaml`** in your
   config folder (written atomically, so Home Assistant never reads a half-written file).
2. `configuration.yaml` contains `recorder: !include recorder_studio.yaml`. The Migration tab sets this up.
3. Changes to the filter, retention, auto purge and auto repack are applied **to the running recorder** (no restart). The database URL and commit interval are only read at start-up; the panel tells you when a restart is pending.
4. Statistics are read with a strictly **read-only** SQLite connection. Anything that changes data goes through the
   official `recorder.*` services.

Nothing is written at startup; installing the integration alone changes nothing on disk.

## Migration

Open **Migration** (or click *Set up* in the banner). Two steps, each with its own confirmation:

1. **Import** the existing exclusions into Recorder Studio. The tab lists every place in your configuration folder that
   holds recorder settings (an inline `recorder:` block in `configuration.yaml`, the file it includes, GUI Recorder's
   `gui_recorder.yaml`, and other YAML files up to three folders deep such as `packages/`). You can also enter a path
   inside the configuration folder or paste YAML (a `recorder:` block or bare options such as `exclude:`). Files are only
   read, never modified; `secrets.yaml`, `.storage` and `custom_components` are skipped. Unsupported options are listed as
   warnings instead of being dropped silently, and values that use YAML tags such as `!secret` are never imported as
   plain text. Importing replaces your current exclusions, or, with the checkbox, adds to them, so you can combine
   several sources.
2. **Activate (by hand).** Recorder Studio never edits `configuration.yaml`. A diff shows exactly which lines to
   remove (the old `recorder:` block) and which to add, and a button copies
   `recorder: !include recorder_studio.yaml`. Apply it in your own editor.

Then restart Home Assistant. To go back at any time, point the include at the old file.

> If the recorder settings came from a file other than `configuration.yaml` (for example a package), that file is not
> changed. Remove its `recorder:` section yourself after activating, otherwise Home Assistant reports a duplicate
> recorder configuration. The panel shows this note next to the source.

![Migration](docs/images/migration.png)

### Coming from GUI Recorder

Import from `gui_recorder.yaml`, make the include change in `configuration.yaml`, restart, and check that the Migration tab shows *Active*. After that you
can uninstall GUI Recorder. Keep `gui_recorder.yaml` for a while as a fallback; it is inert once
`configuration.yaml` no longer includes it.

## Uninstalling

Removing the integration does not touch your database or `recorder_studio.yaml`. Because
`recorder: !include recorder_studio.yaml` is plain Home Assistant YAML, your recording behaviour keeps working
without the integration. To leave `configuration.yaml` tidy, copy the content of `recorder_studio.yaml` (below the
two comment lines) into an inline `recorder:` block and remove the include.

## Safety

- Every destructive action shows its impact and needs confirmation; bulk purges need `PURGE` typed.
- All websocket commands are admin-only; destructive ones also require an explicit `confirm: true`.
- `configuration.yaml` is backed up before it is changed, and files are written atomically.
- Optional **read-only mode**: set `READ_ONLY_MODE = True` in `custom_components/recorder_studio/const.py` to refuse
  every write action while statistics and lists keep working.

## Troubleshooting

| Problem | What to try |
| --- | --- |
| Panel does not appear | Add the integration under *Devices & services*, then hard-refresh (Ctrl+Shift+R). The panel is admin-only. |
| The panel is missing and the log mentions a non-SQLite database | The recorder uses another database backend, so there is no panel. Use the [Recorder Studio DB add-on](https://community.home-assistant.io/t/recorder-studio-db-an-add-on-that-runs-mariadb-postgresql-or-sqlite-for-your-recorder-with-recorder-studio-built-in/1035261) instead. |
| Panel or icon looks outdated | Hard-refresh the browser. After updating the files, restart Home Assistant. |
| Banner says the file is not active | `configuration.yaml` does not include `recorder_studio.yaml`; use *Set up* on the Migration tab. |
| Statistics are empty or old | The panel updates them every 30 seconds while it is open and visible. A first analysis on a very large database can take a moment; *Re-analyse* forces it. |
| Changes have no effect | Check that `configuration.yaml` includes `recorder_studio.yaml` (Migration tab, *Active*). If the panel still asks for a restart, the log says why (`Could not apply the recorder configuration live`). |
| No trend chart yet | One snapshot is saved per day; the chart needs a few days, the forecast a few more. |
| Size per entity looks off | It is an estimate. The attribute part is measured once an hour; right after a restart it is based on record counts. |

## Limitations

- SQLite only. For MariaDB or PostgreSQL use the [Recorder Studio DB add-on](https://community.home-assistant.io/t/recorder-studio-db-an-add-on-that-runs-mariadb-postgresql-or-sqlite-for-your-recorder-with-recorder-studio-built-in/1035261).
- Purging works per entity, per device, for all excluded entities, or by retention. It needs a recent analysis, because
  the confirmation dialog shows the impact first. Entities without a device cannot be purged as a group.
- Live apply relies on two recorder internals (the `entity_filter` attribute and the listener stop/start the recorder also runs around backups). If a Home Assistant update changes them, Recorder Studio falls back to asking for a restart; it never leaves the recorder without its listeners.
- The per-table sizes need SQLite's `dbstat` module; if your SQLite build lacks it, that card is simply hidden.
- Re-enabling recording for an entity that one of your manual domain/glob rules excludes is not supported; remove or
  narrow the rule instead.

## Development

```bash
uv venv .venv && uv pip install --python .venv/bin/python pytest pyyaml
.venv/bin/python -m pytest                    # pure core, fast, no Home Assistant needed
uv venv .venv-ha --python 3.13 && uv pip install --python .venv-ha/bin/python pytest-homeassistant-custom-component
.venv-ha/bin/python -m pytest tests_ha        # the Home Assistant glue (websocket API, alerts, config flow)
python3 scripts/build_preview.py   # rebuilds preview/preview.html
```

- `custom_components/recorder_studio/core/` is pure Python with no Home Assistant imports (rules, YAML rendering,
  SQLite analysis, migration, device tree) and is unit-tested against a synthetic SQLite database.
- The Home Assistant glue is `service.py`, `websocket_api.py`, `panel.py`, `storage.py` and `config_flow.py`.
- The panel is a single [Lit](https://lit.dev) module (`frontend/recorder-studio-panel.js`), vendored in
  `frontend/vendor/`, with no build step.
- **UI preview without Home Assistant:** open `preview/preview.html` in a browser (one file, fake data, writes
  nothing). Deep links: `preview.html#analyze&tab=entities&open=all&theme=dark&phone`.

## Credits and license

Independent re-implementation inspired by the functionality of
[GUI Recorder](https://github.com/martinandersen84/gui-recorder) (MIT); no code was copied. Panel built with
[Lit](https://lit.dev) (BSD-3-Clause, vendored). Released under the [MIT license](LICENSE).
