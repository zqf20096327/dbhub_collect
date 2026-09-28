# oddb.org
* https://github.com/zdavatz/oddb.org

## Description
Open Drug Database for Switzerland. See the live version at http://ch.oddb.org

## Features/Problems
* **SDIF Interactions**: Drug interaction checking uses the [SDIF (Swiss Drug Interactions Finder)](https://github.com/zdavatz/sdif) SQLite database (`data/sqlite/interactions.db`). Four sources: EPha.ch curated ATC-to-ATC interactions, substance-level matches, ATC class-level keyword matching in Swissmedic FachInfo text, and CYP enzyme-mediated interactions. Each interaction shows its source (EPha.ch or Swissmedic FI) with type badge (Wirkstoff, ATC-Klasse, CYP). Route indicators (topisch, i.v., s.c., etc.) and approved combination therapy hints are displayed next to drug names. FI results display a "Gegenrichtung hat höhere Einstufung" hint when their severity is below the pair maximum across all interaction types. EPha results show the hint only for asymmetric EPha ratings between directions.
* Twitter share and mail/notify icons have been removed from drug search result lists.
* The `desitin` flavor was retired in August 2026 on request. Unlike just-medical it was still in use — 1206 requests from 459 distinct addresses in that month — so visitors now get the gcc default: the urls keep working, the branding and the desitin-specific result ordering do not. `LookandfeelDesitin`, its css theme and the desitin branches in `State::Global` and `Util::ResultSort` remain in the tree, so restoring the `WRAPPERS` entry revives it.
* The `just-medical` flavor was retired in August 2026: its hostname no longer resolves and the path flavor served no requests. Removing its `LookandfeelFactory::WRAPPERS` entry is what retires it — sessions asking for it fall back to `gcc`. The med-drugs xls export to `med-drugs@just-medical.com` is a separate thing and is unaffected.
* Some email-Addresses are still hardcoded. That needs to be fixed and placed into etc/oddb.yml
* If you install oddb.org via gem please also see these [instructions](http://dev.ywesee.com/Niklaus/Index).

## Requirements
* `git clone https://github.com/rbenv/ruby-build.git "$(rbenv root)"/plugins/ruby-build`
* `rbenv install 3.4.5`
* Linux: `sudo apt-get install apache2 daemontools daemontools-run pkg-config libmagickwand-dev libpq-dev libmagickcore-dev graphicsmagick uuid-dev`
* macOS: `brew install libpq graphicsmagick ossp-uuid` (use `bundle config build.pg --with-pg-config=$(brew --prefix libpq)/bin/pg_config` for the pg gem)
* `bzcat 22:00-postgresql_database-ch_oddb-backup.bz2 | su -c psql -l postgres -p 5433 ch_odd`
* see Guide.txt

## Useful commands
### Reparse compositions of 5 digit Swissmedic Numbers ([issue #139](https://github.com/zdavatz/oddb.org/issues/139))
`sudo -u apache bundle exec ruby jobs/import_swissmedic_only update_compositions 67685 60134`
### Reparse all compositions
`sudo -u apache bundle exec ruby jobs/import_swissmedic_only update_compositions`
### Check all packages
`sudo -u apache bundle exec ruby jobs/import_swissmedic_only check`
### Reparse FachInfo/PatInfo text for a specific IKSNR
`bundle exec ruby jobs/update_textinfo_swissmedicinfo --skip --target=both 62822 --reparse`
### Find and delete objects nothing can reach
`bundle exec ruby jobs/verify_chapter_reachability <ids.txt>` walks the live objects and checks a list of supposedly unreachable ids against them — run this before deleting anything.
`bundle exec ruby jobs/delete_unreachable_objects` counts what is unreachable per class; `--upto=<n>`, `--extent=<class>` or `--all` plus `--apply` deletes it, logging every id. `ChangeLogItem`, `Array` and `Hash` are never touched.
### Check the Fachinfo references
`bundle exec ruby jobs/repair_fachinfo_references` reports registrations whose `@fachinfo` points at something that cannot be a Fachinformation; `--apply` clears the reference. It asks the database rather than the objects — a registration legitimately references `Hash`, `Company`, `Indication`, `Fachinfo`, `Patent`, `Reg

[...截断...]

istration` and `MiniFi` and nothing else — because the broken value is an `ODBA::Stub` *declaring* `ODDB::Fachinfo` while resolving to something else, so `is_a?` says yes and only `respond_to?` tells the truth by fetching the object. Runs monthly from cron and exits non-zero on a find.

### Check the compositions for dead agents
`bundle exec ruby jobs/repair_dead_bag_agents` walks all registrations and reports `ActiveAgent`s that no longer resolve, plus compositions whose `@active_agents` is nil; `--apply` removes them and writes an undo log. It leaves `@inactive_agents` alone — nil is the normal state on 6885 older compositions and no damage.

### Check the pointer index
`bundle exec ruby jobs/repair_pointer_index` reports rows of the `oddb_persistence_pointer` index that do not lead to the object the pointer names; `--apply` deletes them and writes an undo log. Two sorts: rows whose target is an `Array` or `Hash` — those are the dangerous ones, `find_by_pointer` hands them out — and rows whose target no longer exists, which are inert leftovers of earlier repairs. Dry by default, exits non-zero on a find.

### Deactivate registrations Swissmedic no longer lists
`bundle exec ruby jobs/deactivate_vanished_registrations` reports registrations that are still active but have dropped out of the Packungen lists **and are no longer in `Präparateliste-latest.xlsx`**; `--apply` deactivates them with the date of the first list that missed them. The Präparateliste is required — without it an export authorisation, which has no Swiss package and so never appears in the Packungen list, cannot be told from one that was struck off.

### Correct the de-registration dates
`bundle exec ruby jobs/fix_deregistration_dates` compares `inactive_date` against the Swissmedic Packungen lists in `data/xls` and reports what is wrong; `--apply` writes it and logs every change for undo.

### Check the Patinfo sequence lists
`bundle exec ruby jobs/repair_patinfo_sequences` walks every Patinfo and reports those whose `@sequences` is not a list; `--apply` restores it from the sequences that point back and writes an undo log. It walks all ~14 500 objects rather than filtering on `object_connection`, which costs about a minute and is the only way to get a number that holds — an edge does not say which ivar it came from, and a nil or dangling `@sequences` has no usable edge at all. Dry by default, exits non-zero on a find.

### Rebuild the RSS archives
`bundle exec ruby jobs/build_fachinfo_year_feeds --apply` writes `fachinfo-<year>.rss` from the documents' change logs (about fifteen minutes for 6287 Fachinfos; runs nightly from `jobs/update_fachinfo_rss_feeds`).
`bundle exec ruby jobs/build_patinfo_year_feeds --apply` does the same for the patient information — `patinfo-<year>.rss` plus a small `patinfo.rss` with the newest fifty changes (19 minutes for 6427 Patinfos; runs nightly from `jobs/update_patinfo_rss_feeds`).
`bundle exec ruby jobs/build_price_archives --apply` rebuilds the monthly price archives from the packages' price history.
`bundle exec ruby jobs/split_rss_archives <channel>.rss --apply` cuts an existing feed into monthly files.
Each of the three is dry by default and writes only with `--apply`.

**Note:** The `fiparse` daemon (DRb on port 10002) runs as a separate process managed by daemontools (`/etc/service/fiparse`). After making code changes to `ext/fiparse/src/`, restart the daemon with `sudo svc -h /etc/service/fiparse` for changes to take effect.

### Fachinfo Table Rendering
Tables from swissmedicinfo are parsed by `detect_table?` in `ext/fiparse/src/textinfo_html_parser.rb`. Tables with percentage-width styles are rendered as preformatted text; others are rendered as HTML tables with proper `colspan`/`rowspan` support. The view (`src/view/chapter.rb`) only emits `colspan`/`rowspan` attributes when > 1 to avoid invalid `colspan="0"` in the output.

### Swiyu Login
The app uses [Swiyu](https://www.eid.admin.ch/en/swiyu) wallet-based authe