# ClickHouse Homebrew Tap

Run [ClickHouse](https://clickhouse.com/) as a service on macOS with standard
[Homebrew](https://brew.sh) commands.

This tap is a **service wrapper only**. It ships no ClickHouse binary. It
writes the config files, creates the data and log directories, and provides
`brew services` integration.

## Installation

### 1. Install the ClickHouse binary

The binary is installed separately. The official installer downloads it into
the current directory:

```bash
curl https://clickhouse.com/ | sh
```

Then move it somewhere on your `PATH`.

Alternatively, download a stable release build directly:

```bash
# Apple silicon
curl -L -o clickhouse https://github.com/ClickHouse/ClickHouse/releases/latest/download/clickhouse-macos-aarch64
# Intel
curl -L -o clickhouse https://github.com/ClickHouse/ClickHouse/releases/latest/download/clickhouse-macos

chmod +x clickhouse
```

> **The `clickhouse` cask is deprecated.** It fails the macOS Gatekeeper
> check and will be **disabled on 2026-09-01**. Use one of the methods above
> rather than `brew install --cask clickhouse`.

### 2. Install the service wrapper

```bash
brew install pavsap/clickhouse/clickhouse-server
```

Equivalently:

```bash
brew tap pavsap/clickhouse
brew install clickhouse-server
```

### 3. Trust the tap

Homebrew 6 requires non-official taps to be trusted, otherwise `brew upgrade`
skips them with a warning:

```bash
brew trust pavsap/clickhouse
```

This is local, per-machine configuration stored in `~/.homebrew/trust.json`.

## Usage

### Service Management

```bash
# Basic service control
brew services start|stop|restart clickhouse-server

# Check service status
brew services info clickhouse-server

# Manual start (without a background service)
clickhouse-server
```

`clickhouse-server` is a small wrapper installed by this tap. It resolves the
`clickhouse` binary from your `PATH` at run time and starts it with this tap's
config. Extra arguments are passed straight through.

### Test Installation

```bash
# Test local queries
clickhouse client -q 'SELECT 1'
clickhouse client -q 'SELECT version()'

# Test connectivity
curl 'http://localhost:8123/ping'
curl 'http://localhost:8123/?query=SELECT%201'
```

### Configuration

Default configuration files:
- `/opt/homebrew/etc/clickhouse-server/config.xml`
- `/opt/homebrew/etc/clickhouse-server/users.xml`

Data directory:
- `/opt/homebrew/var/lib/clickhouse`

Log files, all under `/opt/homebrew/var/log/clickhouse-server/`:

| File | Written by |
|---|---|
| `clickhouse-server.log` | ClickHouse itself, per `config.xml` |
| `clickhouse-server.err.log` | ClickHouse itself, per `config.xml` |
| `clickhouse.log` | the service, capturing stdout |
| `clickhouse.err.log` | the service, capturing stderr |

If the service fails to start, check `clickhouse.err.log` first. That is
where the wrapper's own errors land.

### Environment overrides

| Variable | Effect |
|---|---|
| `CLICKHOUSE_BINARY` | Use this binary instead of searching `PATH` |
| `CLICKHOUSE_CONFIG` | Load this config instead of the tap's `config.xml` |

## Security

Default configuration:
- Empty password for default user
- Access restricted to localhost (127.0.0.1 and ::1)
- Default ports:
  - HTTP: 8123
  - Native: 9000
  - Interserver: 9009

⚠️  Consider changing default passwords in production environments.

## Upgrading

Configuration files are not overwritten on upgrade. To use new configurations:
1. Backup existing files
2. Remove them
3. Reinstall the formula

## Troubleshooting

### Common Issues

1. `clickhouse binary not found on PATH`:

   The wrapper could not locate a `clickhouse` binary. Install one (see
   Installation above), or point at an existing one:
```bash
export CLICKHOUSE_BINARY=/path/to/clickhouse
```

2. Permission issues:
```bash
sudo chown -R $(whoami) /opt/homebrew/var/lib/clickhouse
sudo chown -R $(whoami) /opt/homebrew/var/log/clickhouse-server
```

3. Port conflicts:
Edit ports in config.xml and restart the service.

## Releasing

The formula uses a git `url` with a `tag`, so it needs no `sha256` and a
release is a single atomic step: bump the tag in the formula, then tag that
same commit:

```bash
# edit Formula/c/clickhouse-server.rb: tag: "v1.4"
git commit -am "clickhouse-server 1.4"
git tag v1.4
git push origin main v1.4
```

Push the branch and tag together so `main` never names a tag that is not yet
on the remote.

Do not switch back to an `archive/refs/tags/*.tar.gz` url. That needs a
`sha256` which cannot be computed until the tag exists, which forces a
follow-up commit that the tag itself does not contain.

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the Apache License 2.0. See the
[LICENSE](LICENSE) file for details.

## Acknowledgments

- [Homebrew](https://brew.sh/)
- [ClickHouse](https://clickhouse.com/)
