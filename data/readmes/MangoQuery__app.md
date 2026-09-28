<p align="center">
  <img src="logo/mango-app-icon-256.png" width="128" height="128" alt="Mango icon">
</p>

<h1 align="center">Mango</h1>

<p align="center">
  <strong>A fast, native MongoDB GUI — built with <a href="https://github.com/PerryTS">Perry</a></strong>
</p>

<p align="center">
  <em>MongoDB, finally fast.</em>
</p>

<p align="center">
  <img src="screenshots/query-browser.png" width="49%" alt="Query browser">
  &nbsp;
  <img src="screenshots/document-editor.png" width="49%" alt="Document editor">
</p>

---

Mango is a native desktop MongoDB client written in TypeScript and compiled to native ARM64/x86_64 using [Perry](https://github.com/PerryTS). No Electron, no JVM, no runtime overhead — just a small, fast binary that talks directly to your database.

## Features

- **Connection management** — Save, edit, and delete connection profiles. Connect via host/port or full connection string (SCRAM-SHA-256, TLS).
- **Database & collection browser** — Query any collection with custom filters, sort, and projection.
- **Document viewer** — Browse query results as formatted JSON.
- **Document editing** — Edit documents inline and save changes back to MongoDB.
- **Document CRUD** — Insert, update, delete, and duplicate documents.
- **Index listing** — View indexes with key, uniqueness, and size info.
- **Dark & light mode** — Follows system preference automatically.
- **Cross-platform** — Targets macOS (AppKit), iOS (UIKit), Android (Views), Linux (GTK4), Windows (Win32), and the **browser** (WebAssembly + DOM via Perry's `--target web`).

## Getting Started

### Prerequisites

- [Perry](https://github.com/PerryTS) compiler
- [Bun](https://bun.sh) (for type-checking and running tests)
- A running MongoDB instance

### Build

```bash
# Install type-checking dependencies
bun install

# Compile to native binary
perry compile src/app.ts --output mango

# Run
./mango
```

### Run in the browser (WebAssembly)

```bash
# Compile to a single self-contained HTML+WASM file (~4 MB)
perry compile src/app.ts --target web -o dist/mango.html

# Serve over HTTP (file:// won't work — fetch() hits CORS errors)
python3 -m http.server 8765 -d dist
open http://localhost:8765/mango.html
```

The web build is the same source code, compiled by Perry to WebAssembly with a JavaScript bridge that maps every Perry widget to a DOM element. SQLite-backed connection storage degrades to an in-memory transient store on web; the Hone code editor's native bindings degrade to no-ops; and you'll need to point at a Mango Server proxy (see below) if you want to talk to MongoDB from the browser. Everything else (UI, navigation, query builder, document viewer, dark/light mode, i18n) works the same as the native builds.

### Mango Server (proxy for the web build)

The browser cannot speak MongoDB's wire protocol directly. The companion server in `src/serve.ts` is a small native binary that exposes every `MangoClient` operation over an authenticated REST API and forwards each call to the MongoDB the user picks at session start.

```bash
# Build the native binary (~6.5 MB)
npm run build:serve

# Run it
./mango-serve \
  --host mango.example.com \
  --port 3000 \
  --tokens alice-token,bob-token \
  --allow-origin https://mango.example.com
```

| Flag             | Default       | Purpose                                                                    |
| ---------------- | ------------- | -------------------------------------------------------------------------- |
| `--host`         | `localhost`   | Bind address. `localhost` binds 127.0.0.1; anything else binds 0.0.0.0.    |
| `--port`         | `3000`        | HTTP port.                                                                 |
| `--tokens`       | *(empty)*     | Comma-separated bearer tokens. Without any, the server 401s everything.    |
| `--allow-origin` | *(same-host)* | Comma-separated CORS origins. Defaults to same-origin only.                |
| `--allow-local`  | *off*         | Permit MongoDB URIs to loopback / RFC1918 hosts. Self-hosted demos only.   |
| `--html`         | `mango.html`  | Path to the compiled web build, served at `GET /`. Optional.               |

The `MANGO_TOKENS` env variable appends to `--tokens` — handy in container deployments.

**How users connect.** Each user pastes the server URL and their bearer token into the **Proxy URL** / **Proxy token** fields in the web build's connection screen. Both are persisted to `localStorage`. Once the `/healthz` indicator turns green, they create a connection profile (with a normal `mongodb://` URI) and Mango forwards each request through the proxy.

**Security model.** The proxy is designed for public, multi-tenant deployment:

- **Auth.** Every API call requires `Authorization: Bearer <token>`. Tokens are flat strings the operator distributes out-of-band; the server uses a constant-time compare.
- **Sessions.** Opaque session IDs are tied to the creating token. 30 minute idle TTL, 24 hour hard TTL, in-memory only — restart drops them all.
- **Rate limit.** Per-token token bucket: 100 req/s, 1000 req/min.
- **SSRF guard.** MongoDB URIs are rejected if any host is loopback, RFC1918, link-local, or `0.0.0.0`. Use `--allow-local` for self-hosted demos where you want the proxy to dial `mongodb://localhost`.
- **Body / response caps.** 4 MB request body; 16 MB serialized response, max 10 000 documents per query.
- **TLS.** The server itself speaks HTTP. Put Caddy / nginx / a load balancer in front for TLS termination, especially in public deployment — bearer tokens and MongoDB URIs are sent on the wire.

### Development

```bash
# Type-check
perry check

# Run tests
bun test
```

## Project Structure

```
src/
  app.ts                  # Entry point — screens, navigation, UI
  serve.ts                # Mango Server: REST proxy for the web build
  data/
    connection-store.ts   # SQLite CRUD for saved connections
    mongo-client.ts       # Native MongoDB client wrapper
    web-mongo-client.ts   # fetch() client used by the web build
    bson-json.ts          # Extended-JSON helpers ($oid / $date roundtrip)
    preferences.ts        # User preferences (theme, page size, etc.)
    database.ts           # SQLite database helper
  theme/
    colors.ts             # Mango color palette (light/dark)
    typography.ts         # Platform-specific font families
tests/                    # Unit and integration tests
logo/                     # App icons and brand assets
perry.config.ts           # Perry build configuration
perry.toml                # Perry project manifest
```

## How It Works

Perry compiles TypeScript to native machine code via SWC (parsing) and LLVM (codegen). Platform UI is rendered through native frameworks — AppKit on macOS, UIKit on iOS, GTK4 on Linux, etc. MongoDB access uses Perry's built-in `mongodb` package, which wraps the Rust MongoDB driver directly in the compiled binary.

The result is a ~7 MB self-contained binary with sub-100 MB RAM usage and instant cold start.

## License

[MIT](LICENSE) — Skelpo GmbH
