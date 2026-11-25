# Workbench

Workbench is a cross-platform local development environment built with Tauri v2, Rust, and SvelteKit. It provides a native desktop interface for managing local web servers, language runtimes, databases, `.test` HTTPS domains, and development workspaces.

## Features

- **Local Services**: Install, start, stop, and monitor Caddy (with local HTTPS and reverse proxy support), Apache HTTP, MariaDB, Redis, and phpMyAdmin. Includes live log streaming, configurable ports, local site routing, and system tray controls.
- **Runtime Version Manager**: Download and switch between multiple versions of PHP, Composer, Node.js, and Flutter, alongside `rustup` toolchain management.
- **Fast PATH Shims (`workbench-shim`)**: A native Rust shim resolver that routes CLI invocations to your global default, a per-project `.workbench.toml` pin, or an existing host binary.
- **PHP Configuration**: Inspect PHP installations, toggle extensions, and edit `php.ini` settings directly from the interface.
- **Database Administration**: Connect to local or remote MariaDB/MySQL servers to inspect schemas, create or drop databases and users, manage grants, and import/export SQL dumps.
- **Project Discovery and Storage Hibernation**: Scan workspace directories for Laravel, PHP, SvelteKit, Node.js, Flutter, and Rust projects. Reclaim disk space by hibernating idle projects (removing rebuildable artifacts such as `node_modules`, `vendor`, and build caches) and waking them back up on demand, plus inspect and clean global ecosystem caches.
- **Shell Integration**: Non-destructive `PATH` integration for `zsh`, `bash`, `fish`, and PowerShell, with a clean uninstall option that removes Workbench files and shell blocks without touching your projects.

## Tech Stack

- **Desktop Shell and Backend**: [Tauri v2](https://v2.tauri.app/) (Rust, Tokio, SQLite via `rusqlite`)
- **Frontend**: [SvelteKit](https://kit.svelte.dev/) (Svelte 5, TypeScript, Tailwind CSS v4)
- **Shim Resolver**: Standalone Rust binary (`src-tauri/crates/workbench-shim`)

## Project Structure

```text
.
├── manifests/                  # Bundled runtime and service download manifests
│   ├── runtimes.json
│   └── services.json
├── src/                        # SvelteKit frontend (routes, stores, components)
├── src-tauri/
│   ├── crates/workbench-shim/  # Native PATH shim binary
│   ├── src/
│   │   ├── commands.rs         # Tauri IPC command handlers
│   │   ├── config.rs           # Global config (~/.workbench/config.toml)
│   │   ├── databases/          # MariaDB/MySQL inspection, grants, import/export
│   │   ├── db.rs               # Local SQLite persistence for cleanup stats
│   │   ├── runtimes/           # Runtime installer, rustup, PHP ini/extensions
│   │   ├── services/           # Process supervisor, logs, Caddy/Apache configs
│   │   ├── shell.rs            # Shell profile integration and host tool detection
│   │   ├── storage/            # Workspace scanner, project hibernation, global caches
│   │   └── telemetry.rs        # Real-time CPU, memory, and network host telemetry
│   ├── Cargo.toml
│   └── tauri.conf.json
├── static/                     # Static frontend assets
└── package.json
```

## Supported Platforms

| Platform | Target |
| :--- | :--- |
| macOS (Apple Silicon) | `aarch64-apple-darwin` (`.dmg`, `.app`) |
| Linux (64-bit) | `x86_64-unknown-linux-gnu` (`.deb`, `.rpm`, `.AppImage`) |
| Windows (64-bit) | `x86_64-pc-windows-msvc` (`.msi`) |

### Quick Install on macOS

Because Public Beta builds are ad-hoc signed rather than Apple Developer ID notarized, macOS Gatekeeper may flag browser-downloaded `.dmg` files as *"damaged and can't be opened"*.

**Option 1 — One-line terminal installer (recommended, bypasses browser quarantine):**

```bash
curl -fsSL https://raw.githubusercontent.com/aquinasm/workbench/main/install.sh | sh
```

**Option 2 — After dragging `Workbench.app` from the `.dmg` to `/Applications`:**

```bash
xattr -cr /Applications/Workbench.app
```

## Getting Started

### Prerequisites

- [Node.js](https://nodejs.org/) (v20+ recommended)
- [Rust](https://rustup.rs/) (stable toolchain)
- Tauri v2 platform prerequisites (see the [Tauri prerequisites guide](https://v2.tauri.app/start/prerequisites/))

### Development

```bash
# Install frontend dependencies
npm install

# Run the desktop app in development mode
npm run tauri dev
```

### Type Checking and Testing

```bash
# Run Svelte and TypeScript checks
npm run check

# Run Rust tests across the workspace
cargo test --manifest-path src-tauri/Cargo.toml
```

### Production Build

```bash
# Build platform installers (dmg, AppImage, nsis)
npm run tauri build
```

## Configuration

Workbench stores its configuration, shims, and managed runtimes in:

- **macOS / Linux**: `~/.workbench`
- **Windows**: `%LOCALAPPDATA%\Workbench`

You can override this location by setting the `WORKBENCH_HOME` environment variable.

### Per-Project Runtime Pins

To pin specific runtime versions for a project, add a `.workbench.toml` file in the project root (or configure it from the project detail view in the app):

```toml
[runtimes]
php = "8.4.4"
node = "22.14.0"
```

## Keyboard Shortcuts

| Shortcut | Action |
| :--- | :--- |
| `Cmd/Ctrl + K` | Open command palette |
| `Cmd/Ctrl + R` | Rescan workspaces and global caches |
| `Cmd/Ctrl + 1` – `7` | Switch between Dashboard, Services, Runtimes, Projects, Databases, Storage, and Settings |

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

## Security

If you discover a security vulnerability, please follow the reporting process in [SECURITY.md](SECURITY.md) instead of opening a public issue.

## License

This project is licensed under the [MIT License](LICENSE).
