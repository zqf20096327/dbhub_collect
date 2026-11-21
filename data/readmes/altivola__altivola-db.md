# altivola-db

A light database client that runs on your own computer. One app for **PostgreSQL**, **MySQL/MariaDB**, **SQLite**,
**SQL Server**, **MongoDB**, **Redis** and **Cloudflare D1**, plus an MCP server so AI agents can query your databases.

## Download

|                           |                                                                                                                                             |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| **macOS** (Apple Silicon) | [**altivola-db-macos-arm64.dmg**](https://github.com/altivola/altivola-db/releases/latest/download/altivola-db-macos-arm64.dmg)             |
| **Windows** (x64)         | [**altivola-db-windows-x64-setup.exe**](https://github.com/altivola/altivola-db/releases/latest/download/altivola-db-windows-x64-setup.exe) |

The apps are not signed yet, so the first open needs one extra step:

- **macOS:** drag the app to Applications, then right-click it and pick **Open**.
- **Windows:** if SmartScreen warns, click **More info**, then **Run anyway**.

After that the app updates itself.

## Or run it with Docker

```sh
docker run -d --name altivola-db -p 127.0.0.1:7789:7789 -v altivola-db-data:/data \
  --add-host host.docker.internal:host-gateway ghcr.io/altivola/altivola-db:latest
```

Then open http://localhost:7789.

## Use it with AI agents

```sh
claude mcp add altivola-db -- docker exec -i altivola-db altivola-db mcp
```

## More

Connection URLs, shortcuts, dump and import, the CLI, MCP setup for the desktop app and development:
see the [guide](docs/guide.md).

[MIT](LICENSE)
