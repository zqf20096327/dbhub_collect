# mpdbx — MpEngineDB Explorer

A single Windows executable (~7.9 MB, no install, no runtime), with Python and PowerShell editions, that turns a **copy** of Microsoft Defender's
engine database (`Scans\mpenginedb.db` + `-wal`) and `Scans\History\{Store,Results}` into correlated, decoded
forensic records: process first starts, executions of binaries without an embedded certificate, OriginalFileName
renames, file hashes, scan/AMSI provenance, rolling queues (threats, host network context, RDP), CFA folders and more.

It is not a table browser: rows from different tables are joined into **locations, process runs, file content and
events**, every link shows **the rule that made it and how strong it is** (● exact, ◐ partial, ○ heuristic), and
every row shows **where it came from** (DB, WAL-only, WAL-modified, removed by the WAL).

![mpdbx Findings page](docs/findings.png)

## Download
From the [latest release](https://github.com/Mihir-Choudhary/mpdbx/releases/latest) take one of:

| File | Run | Needs |
|---|---|---|
| `mpdbx.exe` | double-click, or `mpdbx open <Scans>` | Windows 10/11 |
| `mpdbx.ps1` | `Unblock-File mpdbx.ps1`, then `powershell -ExecutionPolicy Bypass -File mpdbx.ps1 [<Scans>]` | stock Windows PowerShell 5.1 |
| `mpdbx.py` | `python3 mpdbx.py [<Scans>]` | Python 3.8+ with tkinter (Windows, macOS, Linux); standard library only |

Check each file against `SHA256SUMS.txt` in the release. Every edition is a single self-contained file: no installer,
nothing written to the registry. The exe is not code-signed, so Windows SmartScreen may warn the first time you run it.
The script editions read the DB and WAL only; see [Other editions](#other-editions-same-layout-same-rules).

## Acquire a consistent copy first
The database is SYSTEM-only and locked while Defender runs. Take everything **from one VSS snapshot** so the DB and
its WAL belong together. (`esentutl /y … /vss` makes a *separate* snapshot per call, so a DB and a WAL copied with two
calls can be inconsistent.)

Collect from `C:\ProgramData\Microsoft\Windows Defender\Scans\`:

| File | Needed |
|---|---|
| `mpenginedb.db` | required |
| `mpenginedb.db-wal` | required: often the newest hours of activity, and rows the WAL deleted (`-shm` is not needed) |
| `History\Store\*`, `History\Results\*` | recommended: file-scan provenance (~1 h) and scan runs |
| `mpengine.dll` of the active platform (`…\Definition Updates\{GUID}\`) | optional: only if a future engine changes the DB key |
| MFTECmd CSV of `$MFT` + system volume serial (`vol C:`) | optional: resolves FileHashes MFT references to paths |

From an elevated PowerShell (one snapshot, copy, delete the snapshot):
```
$s = (Get-CimInstance Win32_ShadowCopy -Filter "ID='$((Invoke-CimMethod -ClassName Win32_ShadowCopy -MethodName Create -Arguments @{Volume='C:\'}).ShadowID)'")
$src = $s.DeviceObject + '\ProgramData\Microsoft\Windows Defender\Scans'
robocopy $src D:\case\Scans mpenginedb.db mpenginedb.db-wal /B /COPY:DT
robocopy "$src\History" D:\case\Scans\History /E /B /COPY:DT
$s | Remove-CimInstance
Get-FileHash D:\case\Scans\* , D:\case\Scans\History\*\* -Algorithm SHA256
```
Copy raw bytes only: never open the live database with SQLite or another tool that may checkpoint it (that merges and
empties the WAL). Keep the `Scans\…` layout; mpdbx opens the `Scans` folder.

## Open
- Double-click `mpdbx.exe`, then **Open ▾ → Scans folder…** (or **mpenginedb.db file…**), or drag it onto the window.
- `mpdbx open D:\case\Scans [--tab findings|timeline|files|evidence]`

Decryption, WAL replay and SQLite all run **in memory**; nothing is written unless you export or save bookmarks,
and exports refuse to overwrite any input file.

## Using it
1. **Findings** (home) — one card per first question: unsigned programs run outside system folders, renamed
   executables, threat detections, RDP logons, rows found only in the WAL, then an overview (programs started,
   signature hits, file hashes, host context). Each card shows a count and examples; click it to open exactly those events.
2. **Timeline** — **Quick views** on the left (All activity, Red flags, Programs run, Unsigned programs, Renamed
   executables (any folder), File scans, Detections & signatures (threats + LowFi), Found only in the WAL). Routine background records (module loads,
   file hashes, cache expiries) are hidden until you tick **Show routine events** or type a search. **More filters** opens the detailed
   filters (event type, location, provenance, link strength, source table, time). Drag on the histogram to zoom to a
   time range. Columns: Time · What · Name · Details · Path · Source; WAL rows are tinted, ▲ marks red flags.
3. Click a row → the **detail panel** opens: decoded fields (with a raw toggle), where the row came from, related
   records with the rule that links them (● exact ◐ partial ○ heuristic), events nearby in time, one-click pivots
   (same location, same process run, same hash, ±time window) and bookmarks with tag and note.
4. **Files & processes** — every typed view (locations, process runs, file hashes, renamed binaries, queues, RDP,
   host context, CFA folders, …) and every raw table, decoded where a decoder applies.
5. **Evidence** — input hashes, WAL report (frames validated/applied, where the checksum chain stopped), per-table
   DB-only vs DB+WAL counts, the volume map (confirm it to make it exact), MFT CSV binding, warnings.

Search box: type any name, path, hash or PID; the **?** next to it lists examples you can click.
Settings (⋮): time zone, theme, compact rows, detail panel, bookmarks. Export ▾: this list as CSV/JSON, an HTML
report (findings + bookmarks), or everything.

Keys: `Ctrl+F` search · `Ctrl+1/2/3/4` tabs · `Alt+←/→` back/forward · `Enter` follow first related ·
`Ctrl+B` bookmark · `Ctrl+C` copy row (TSV) · `Ctrl+E` export current list.

## Other editions (same layout, same rules)
For machines where an exe cannot be run, or that are not Windows, `mpdbx.ps1` (source: `ports/powershell/`) uses
Windows' own `winsqlite3.dll`, and `mpdbx.py` (source: `ports/python/`) needs only Python with tkinter
(`apt install python3-tk` on Debian/Ubuntu).

Both editions show Findings / Timeline / Files & processes / Evidence, decrypt and replay the WAL in memory with the
same rules, and have a no-GUI mode (`mpdbx.py info|export <Scans> --out DIR`, `mpdbx.ps1 <Scans> -Info | -Export DIR`).
They do not read `Scans\History` (Store/Results), MFT CSVs or bookmarks; those stay in the exe.
`python ports/tests/edge_cases.py` runs the malformed-input, export-guard and search checks for both editions.
`python ports/verify_ports.py <Scans> ...` checks that both editions produce exactly the exe's DB/WAL events and the same
export files (verified on the reference copies and the WAL edge-case fixtures).

Notes: the PowerShell edition compiles its engine (C#, embedded in the script) with `Add-Type`, which writes short-lived
files under `%TEMP%` on the analysis machine.
On Python < 3.11, or a Windows build whose `winsqlite3.dll` lacks `sqlite3_deserialize`, the decrypted image is written
to a private temporary file that is deleted on exit.
`ports/powershell/mpdbx.ps1` is generated: edit `mpdbx.src.ps1` / `engine.cs` and run `python ports/powershell/build.py`.

## Search syntax
| Term | Meaning |
|---|---|
| `text` / `"two words"` | free text over summaries, fields and paths |
| `path:c:\users\*` `name:*.exe` | path / file name (glob; no wildcard = substring) |
| `sha256:` `sha1:` `md5:` | digest (prefix or glob) |
| `pid:4120` | process ID |
| `type:nocert*` | event type |
| `src:db` `src:walonly` `src:walmod` `src:removed` | provenance |
| `loc:system` `loc:outside` | location class |
| `nocert:yes` | locations with a no-embedded-cert execution |
| `after:2026-10-19` `before:2026-10-19T17:00+05:30` | time (display zone unless an offset is given) |
| `/regex/` | regular expression over the search text |
| `-term` | negate |

## Command line (same exe)
```
mpdbx info   <path>
mpdbx export <path> --out DIR [--format csv|json] [--force]
mpdbx report <path> --out FILE.html [--bookmarks F.mpdbx.json] [--force]
mpdbx diff   <pathA> <pathB> --out FILE.csv|FILE.html [--force]
options: --key-dll mpengine.dll  --tz Z|+HH:MM  --volmap N=X  --mft FILE --mft-vsn XXXX-XXXX --mft-drive X
exit codes: 0 ok · 2 usage · 3 input unreadable · 4 decrypt failed · 5 output refused
```

## What the labels mean
- **Process first start** — BackupProcessInfo: first start of an image in its ~7-day window; the time equals kernel
  process creation (ms). Images with a valid Microsoft embedded signature are not recorded.
- **No-cert execution** — first execution of an image **without an embedded certificate** (catalog-signed files count).
- **OriginalFileName set** — the PE OriginalFileName Defender recorded at file creation; differs from the file name → rename.
- **File hashed** — FileHashes row: MD5/SHA1/SHA256 by MFT reference (the table's SHA1/MD5 column names are swapped;
  shown correctly). Bind an MFTECmd CSV in Evidence to see paths.
- **File scan (Store)** — `Scans\History\Store` record (~1-hour cache): file, acting process (PID + start). Its time is
  an estimate (cache expiry − 1 h) and marked ≈.
- **Outside system dirs** — not under `X:\Windows`, `X:\Program Files`, `X:\Program Files (x86)` (writability not claimed).

## Limits
Validated on one Windows 11 build (Defender platform 4.18.260x). Store scan times are estimates; Results fields beyond
GUID/start/end are shown raw; RDP queue decoders come from another host's dump and fall back to key/value.

## Build from source
Requires Rust 1.99+ with the `x86_64-pc-windows-msvc` target.
```
cargo build --release          # builds target\release\mpdbx.exe (static CRT, size-optimised)
cargo test                     # unit, fixture and headless UI tests
```
The test fixtures are synthetic databases generated by `tests/gen_fixtures.py`; no real evidence is included.
Tests marked `#[ignore]` run against local acquisitions that are not part of this repository: set `MPDBX_COPIES`
to the folder holding them (`live\...`, `vss9\...`) and run `cargo test -- --ignored`.

## Credits
The engine database codec builds on public research: dobin's
[Defender Internals](https://blog.deeb.ch/posts/defender-ai-introspection/) write-up and
[DefRev](https://github.com/dobin/DefRev/blob/main/analysis-1/bm_metastore/mpenginedb_decrypt.py) for the
mpenginedb page encryption, and Fox-IT's
[Windows Defender quarantine research](https://www.fox-it.com/nl/research/reverse-reveal-recover-windows-defender-quarantine-forensics/)
for the shared RC4 key and container format. The key is built in; `--key-dll mpengine.dll` finds it in a copy of
Defender's `mpengine.dll` instead.

## License
[MIT](LICENSE). Design notes: [docs/design.md](docs/design.md).
