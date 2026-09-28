<p align="center">
  <a href="README.md"><img src="https://img.shields.io/badge/English-0969da?style=flat-square" alt="English"></a>
  <a href="README.zh-CN.md"><img src="https://img.shields.io/badge/%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87-c8102e?style=flat-square" alt="简体中文"></a>
  <a href="README.ja.md"><img src="https://img.shields.io/badge/%E6%97%A5%E6%9C%AC%E8%AA%9E-8250df?style=flat-square" alt="日本語"></a>
</p>

# Phone Record Manager

A local Windows desktop application for recording phone-number bindings and managing manual number-replacement work without automating access to third-party accounts.

[![Last commit](https://img.shields.io/github/last-commit/NextWeb4/phone-record-manager?style=flat-square)](https://github.com/NextWeb4/phone-record-manager/commits/main)
[![Repository size](https://img.shields.io/github/repo-size/NextWeb4/phone-record-manager?style=flat-square)](https://github.com/NextWeb4/phone-record-manager)
[![GitHub stars](https://img.shields.io/github/stars/NextWeb4/phone-record-manager?style=flat-square)](https://github.com/NextWeb4/phone-record-manager)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
[![MIT License](https://img.shields.io/github/license/NextWeb4/phone-record-manager?style=flat-square)](LICENSE)

## Overview

Phone Record Manager v1.2.0 is built with Python, PySide6, and SQLite. It keeps its database on the local Windows account, provides Chinese and English interface modes, and treats phone-number replacement as a checklist that the user completes manually.

> **Security boundary:** the master password controls access through the application, but it does not encrypt the SQLite database or individual records. A process or operating-system account that can read the database can read its contents. Protect the Windows account and disk, and use encrypted application backups for sensitive exports.

The application does not provide cloud synchronization, sign in to websites, submit SMS codes, modify third-party profiles, scrape provider dashboards, or bypass captchas, rate limits, or account-security checks.

## Capabilities

| Area | What the application provides |
| --- | --- |
| Local access | First-run master-password setup, PBKDF2-HMAC-SHA256 verification, explicit uninitialized/configured/corrupt states, and a 1-1440 minute idle-lock interval |
| Phone numbers | Multiple numbers, binding counts, and independent active, replacing, paused, cancelled, or abnormal lifecycle states |
| Registrations | Create, edit, search, sort, soft-delete, and restore website/app records with account, URL, recovery email, tags, and notes |
| Templates | Common website/app templates plus fully custom records |
| Replacement work | Manual tasks, item status, batch number replacement, history, and guards against conflicting active tasks or deleted records |
| Data transfer | Streamed and bounded CSV import, CSV export, and authenticated encrypted backup import/export using `cryptography.fernet` |
| Desktop experience | Light/dark themes, Chinese/English navigation and settings, single-instance startup, operation history, and privacy-limited rotating diagnostics |

Normal record edits and batch changes cannot silently bypass an active replacement task. The repository enforces replacement, deletion, and phone-status invariants in its service/repository layers and validates them again during backup restoration.

## Requirements and Compatibility

- **Operating system:** the application UI, PowerShell packaging, executable metadata, and MSI target Windows x64.
- **Release Python:** CI and release builds use CPython 3.12.7.
- **Pinned packages:** `requirements.txt` fixes wheel versions and SHA-256 hashes, including `PySide6_Essentials==6.11.1`, `shiboken6==6.11.1`, `cryptography==49.0.0`, and `pyinstaller==6.21.0`.
- **Storage:** SQLite comes from Python's standard library. The current user needs write access to the application data directory.
- **MSI builds:** WiX Toolset CLI 5.0.2 is installed by CI. A local MSI build requires WiX on `PATH`; source execution and a portable-only build do not.

The Windows package deliberately installs `PySide6_Essentials` and `shiboken6`, not the PySide6 meta package or `PySide6_Addons`. The packaging hooks exclude unused Qt PDF, Virtual Keyboard, Network, and Mesa OpenGL components.

## Install and Run

### Use a release package

Download one of the assets from [GitHub Release v1.2.0](https://github.com/NextWeb4/phone-record-manager/releases/tag/v1.2.0):

- `phone-record-manager-windows-v1.2.0.zip`: extract it and run `手机号记录管理器.exe`;
- `phone-record-manager-windows-v1.2.0.msi`: Windows installer;
- `SHA256SUMS.txt`: SHA-256 values for the ZIP and MSI.

The release is not code-signed. Verify the downloaded ZIP or MSI against `SHA256SUMS.txt` before running it, especially when Windows reports an unknown publisher.

### Run from source

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install --require-hashes -r requirements.txt
.venv\Scripts\python -m phone_record_manager
```

Use a CPython 3.12 Windows environment that matches the release toolchain. The application entry point and PyInstaller entry point both delegate to `phone_record_manager.app`.

## Typical Workflow

1. On first launch, create a master password containing at least eight characters.
2. Add a phone number, choose its lifecycle state, and add the websites/apps bound to it.
3. Find records with full-text search, status filters, and table sorting; soft-delete or restore them as needed.
4. Create a replacement task before moving registrations to another active number, then update each manual work item.
5. Set the idle-lock interval, theme, and Chinese/English interface language in Settings.
6. Export an encrypted backup, store its password separately, and verify restoration before removing an older data copy.

Login URLs in records are restricted to valid HTTP/HTTPS addresses. Opening a stored link remains a user action; the application does not submit credentials or verification codes.

## Local Data and Recovery

The default data location is:

```text
%LOCALAPPDATA%\PhoneRecordManager\phone_records.sqlite3
```

Development or test runs can use an isolated directory:

```powershell
$env:PHONE_RECORD_MANAGER_HOME="D:\Temp\PhoneRecordManagerData"
.venv\Scripts\python -m phone_record_manager
```

The same data directory can contain `runtime-errors.log`, a rotating diagnostic file limited to exception type and code locations. It must not contain exception messages, phone numbers, passwords, backup paths, or business fields.

- CSV is useful for review and migration but is unencrypted; protect and delete temporary CSV copies.
- Encrypted backups provide authenticated encryption. Losing the backup password makes that backup unrecoverable.
- Export uses a same-directory temporary file, flushes it, and atomically replaces the target. The live SQLite file and its `-wal`, `-shm`, and `-journal` sidecars cannot be export targets.
- Restore validates table/field shape, value types, primary keys, soft-delete state, references, and replacement-workflow invariants before replacing data in one transaction.
- If the four master-password settings are incomplete or malformed, startup fails closed. There is no unauthenticated password-reset path.

Read [Backup and Restore](docs/BACKUP_AND_RESTORE.md) before a migration and [Security Model](docs/SECURITY_MODEL.md) before handling real personal data.

## Test and Validate

```powershell
python -m unittest discover -s tests
python -m compileall -q phone_record_manager scripts tests
python -m pip check
```

The nine test modules cover lifecycle and single-instance behavior, database schema, diagnostics, CSV/encrypted transfer, packaging entry points, password hashing, phone/registration services, replacement workflows, and offscreen UI behavior.

Windows CI also parses every `scripts/*.ps1` file, installs dependencies with `--require-hashes`, builds the portable ZIP and MSI, and starts the packaged executable in an isolated `PHONE_RECORD_MANAGER_HOME`. No separate lint or formatter command is declared.

## Build and Release

Build only the PyInstaller directory package:

```powershell
.\scripts\build_exe.ps1
```

Build a portable ZIP without requiring WiX:

```powershell
.\scripts\build_release.ps1 -SkipMsi
```

Build the complete local release after placing WiX Toolset CLI on `PATH`:

```powershell
.\scripts\build_release.ps1
```

The full build runs tests, creates the PyInstaller directory package, copies license/source-offer material, audits the Qt inventory and private artifacts, generates the ZIP and MSI, validates the MSI, and writes checksums.

```text
release-assets\phone-record-manager-windows-v1.2.0.zip
release-assets\phone-record-manager-windows-v1.2.0.msi
release-assets\SHA256SUMS.txt
```

The default build fails if WiX or the MSI is unavailable; use `-SkipMsi` explicitly for portable-only verification. The release workflow accepts a new `v<major>.<minor>.<patch>` tag only when it matches `phone_record_manager.__version__`, publishes from the verified tag commit, and refuses to overwrite an existing Release.

## Project Structure

| Path | Responsibility |
| --- | --- |
| `phone_record_manager/app.py` | QApplication setup, data directory, single-instance lock, database lifecycle, login, and main window |
| `phone_record_manager/ui/` | PySide6 windows, dialogs, pages, icons, formatting, and light/dark themes |
| `phone_record_manager/services/` | Authentication, registrations, replacement work, settings, logging, and import/export workflows |
| `phone_record_manager/db/` | SQLite schema, connections, repositories, statistics, operation history, and backup persistence |
| `phone_record_manager/security/` | Password hashing and sensitive-field definitions |
| `phone_record_manager/diagnostics.py` | Privacy-limited rotating unhandled-error log |
| `tests/` | Standard-library `unittest` and offscreen Qt regression suites |
| `scripts/` | Version metadata, PyInstaller, MSI, checksum, privacy, and release orchestration |
| `packaging_hooks/` | Audited PyInstaller collection/exclusion rules for Qt |
| `installer/phone_record_manager.wxs` | WiX x64 MSI definition |
| `docs/` | Backup, security, and v1.2.0 code-audit evidence |

## Security Notes

- The master password is an application access gate, not database encryption. Use Windows device encryption or BitLocker and keep the data directory out of shared/cloud-synchronized folders.
- Password configuration fails closed when its algorithm, iteration count, Base64, salt, or digest structure is invalid.
- Backup restoration validates all input before any existing rows are deleted or replaced.
- CSV and backup outputs cannot alias the live database through normalized paths, symbolic links, or hard links.
- Spreadsheet-like exports must retain formula-injection defenses for cells beginning with `=`, `+`, `-`, or `@`.
- Release checksums prove file integrity, not publisher identity; current packages remain unsigned.

## Status and Limitations

- The repository is active and documents the v1.2.0 Windows release path.
- Phone-number replacement is deliberately manual; there is no account automation or remote recovery.
- The application UI supports Chinese and English. The three README languages do not imply a Japanese application interface.
- Availability depends on the user's local disk and backup practice; the project does not provide cloud synchronization.
- A single SQLite connection is owned by the Qt main thread. Large imports, PBKDF2 work, or backup restoration may temporarily block the interface.
- Automatic locking protects the visible session but can close active modal windows; unsaved form input may be lost.

## Maintenance and Contributions

- Keep presentation in `phone_record_manager/ui/`, workflow validation in `phone_record_manager/services/`, persistence in `phone_record_manager/db/`, and password/sensitive-field policy in `phone_record_manager/security/`; do not put SQL in UI classes.
- Redirect development data with `PHONE_RECORD_MANAGER_HOME` and add focused failure-path tests for schema, authentication, import/export, restoration, registration, replacement, settings, or lifecycle changes.
- Dependency and packaging changes must preserve hash-locked installation, Qt license/source-offer material, the audited plugin inventory, portable/MSI checksums, CI startup smoke, and the local-only network boundary.
- Keep all three README versions, `RELEASE_NOTES.md`, `THIRD_PARTY_NOTICES.md`, `QT_SOURCE_OFFER.md`, version metadata, and workflow asset names synchronized.

## Author

- HaoXiang Huang
- [Rays688888@Gmail.com](mailto:Rays688888@Gmail.com)
- <https://nextweb4.github.io/>
- <https://github.com/NextWeb4>

## License and Third-Party Components

Application source is released under the [MIT License](LICENSE). The Windows package also contains separately licensed runtime components documented in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) and [`THIRD_PARTY_LICENSES/`](THIRD_PARTY_LICENSES).

Qt/PySide6 is distributed under LGPL-3.0-only for this package. Qt shared libraries remain separate and replaceable under `_internal/PySide6`; corresponding-source locations, the three-year written offer, and replacement notes are in [QT_SOURCE_OFFER.md](QT_SOURCE_OFFER.md).

