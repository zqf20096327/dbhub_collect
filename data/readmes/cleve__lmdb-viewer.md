# lmdb-viewer

LMDB viewer re-implemented in Python with Flet.

The app opens an LMDB directory, reads the default database, lists key/value pairs, supports refresh, and filters rows by key or value.

## Features

- Open an LMDB directory from a native folder picker
- Browse key/value pairs in a two-column table
- Search by key or value
- Refresh rows from disk without reopening the app
- Safe text decoding for non-UTF-8 LMDB content using replacement characters

## Requirements

- Python 3.11+
- An LMDB environment directory to inspect

## Install

```sh
poetry install
```

Poetry manages the project environment, so you do not need to create a separate `.venv` manually.

## Run

```sh
poetry run python app.py
```

## Package

Flet can package the app as a desktop binary. On Linux, build on Linux; on Windows, build on Windows; on macOS, build on macOS.

Basic Linux desktop build:

```sh
poetry install
poetry run flet build linux
```

Linux desktop prerequisites reported by `flutter doctor`:

```sh
sudo apt-get update
sudo apt-get install -y clang cmake ninja-build libgtk-3-dev mesa-utils
```

Or use the helper script in this repository:

```sh
bash scripts/install_linux_build_deps.sh
```

Build artifacts are written under `build/<target>`. This repository includes a Poetry-managed `pyproject.toml` with Flet metadata, the Python entry module, and the app icon under `assets/icon.png`.

Notes:

- The first `flet build` may download Flutter automatically.
- Desktop packaging can require platform-native build dependencies.
- Packaged builds exclude `.git`, optional in-project virtualenvs, and sample data.
- A GitHub Actions workflow is included at `.github/workflows/build-linux.yml` to produce a Linux artifact in CI.

## Project Layout

- `app.py`: entry point
- `lmdb_viewer/database.py`: LMDB access and filtering
- `lmdb_viewer/app.py`: Flet user interface
- `pyproject.toml`: Poetry and Flet project metadata
- `assets/icon.png`: icon used for packaged builds
- `scripts/install_linux_build_deps.sh`: installs Linux desktop build prerequisites

## Notes

- The current implementation targets the default LMDB database, matching the original app behavior.
