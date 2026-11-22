# Pentworks

Pentworks is an offline, terminal-based workspace for documenting security assessments. Organize projects, targets and findings, write Markdown notes, attach evidence, and generate a project report. Active project and target selections are stored in SQLite.

## Install

Requires Python 3.14 or later. Installation needs access to the dependencies on PyPI or a local wheelhouse. After installation, Pentworks runs offline.

```sh
python -m venv .venv
# Activate on Windows PowerShell
.\.venv\Scripts\Activate.ps1
# On macOS or Linux, run: source .venv/bin/activate
python -m pip install .
pentworks --help
pentworks version
```

From the source checkout you can also run `python main.py --help`.

## Quick start

On a fresh workspace, the first project, target and finding each have ID `1`. In an existing workspace, use the corresponding `list` commands to find the IDs. Use an existing local file for the attachment.

```sh
pentworks project create "Demo assessment" --description "Internal application review"
pentworks project use 1
pentworks target add demo.example --description "Demo application"
pentworks target use 1
pentworks finding add "Verbose error responses" low --endpoint /example --description "The response includes internal diagnostic details."
pentworks note add "Review notes" --finding 1
pentworks evidence add screenshot.png --finding 1
pentworks dashboard
pentworks report generate
```

### Working with records

```sh
pentworks project list
pentworks target status
pentworks finding list
pentworks finding show 1
pentworks finding status 1 confirmed
pentworks note list --finding 1
pentworks note edit 1
pentworks note rename 1 "Follow-up notes"
pentworks note search "follow-up"
pentworks evidence list --finding 1
pentworks evidence show 1
```

Findings have severity `info`, `low`, `medium`, `high`, or `critical`, and status `open`, `confirmed`, `fixed`, or `false_positive`. Notes can be scoped with `--project`, `--target`, or `--finding ID`. Editing uses `VISUAL`, then `EDITOR`, then Notepad on Windows or `vi` on Unix-like systems.

Evidence imports copy the source file. `evidence show` hashes the stored copy and returns a nonzero exit code if it is missing, unreadable, or has changed. Deletion commands ask for confirmation and accept `--yes` for scripts. Removing a project, target, or finding also removes its associated records and files. Pentworks reports failed file cleanup and retries it on a later workspace command.

## Workspace and existing data

```text
~/.pentworks/
  pentworks.db  Projects, targets, findings, metadata and active selections
  notes/       Markdown files
  evidence/    Stored copies of attached files
  reports/     Generated Markdown reports
```

Set `PENTWORKS_HOME` to select a different workspace. Set `PENTWORKS_DB` to an absolute database path when the database lives elsewhere. Back up the database and workspace files together while Pentworks is closed.

A source checkout with a legacy `pentworks.db` alongside `database.py` keeps using that database unless either environment variable is set. An installed wheel cannot discover other checkouts automatically. Point the installed command at your existing database before running workspace commands. For example, in PowerShell:

```powershell
$env:PENTWORKS_DB = 'D:\Pentworks\pentworks.db'
pentworks project list
```

Keep `PENTWORKS_HOME` unset if your existing notes and attachments are already under the default workspace. The schema update adds indexes and cleanup bookkeeping in place while preserving previous records. For an installed command on Unix-like systems, use `export PENTWORKS_DB=/absolute/path/to/pentworks.db`.

## Limitations and roadmap

Pentworks supports one active context per database. Reports are Markdown snapshots with relative links to local files, so keep the workspace layout when moving a report with its attachments. The local workspace uses the filesystem permissions of your operating system. Files orphaned by versions before v0.1.0 are retained for manual review.

Future releases may add finding filters, structured exports, and workspace backup tools.

## Development

```sh
python -m pip install -e ".[dev]"
python -m pytest
python -m build
```
