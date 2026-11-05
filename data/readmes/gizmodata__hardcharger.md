<p align="center">
  <a href="https://gizmodata.com">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/gizmodata/hardcharger/main/docs/assets/hardcharger-banner-dark.png">
      <img src="https://raw.githubusercontent.com/gizmodata/hardcharger/main/docs/assets/hardcharger-banner-light.png" alt="Hardcharger™" width="600">
    </picture>
  </a>
</p>

<p align="center">
  <a href="https://github.com/gizmodata/hardcharger/actions/workflows/server.yml"><img src="https://github.com/gizmodata/hardcharger/actions/workflows/server.yml/badge.svg" alt="CI"></a>
  <a href="https://pypi.org/project/hardcharger/"><img src="https://img.shields.io/pypi/v/hardcharger?logo=pypi&amp;label=PyPI%20server" alt="PyPI version"></a>
  <a href="https://pypi.org/project/hardcharger/"><img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&amp;logoColor=white" alt="Python 3.10 or later"></a>
  <a href="https://pypi.org/project/hardcharger/"><img src="https://img.shields.io/pepy/dt/hardcharger.svg" alt="PyPI downloads"></a>
  <a href="https://docs.hardcharger.gizmodata.com"><img src="https://img.shields.io/badge/docs-Hardcharger-2563eb.svg" alt="Hardcharger documentation"></a>
  <a href="https://hub.docker.com/r/gizmodata/hardcharger"><img src="https://img.shields.io/badge/dockerhub-image-green.svg?logo=Docker" alt="Docker Hub image"></a>
  <a href="https://github.com/gizmodata/hardcharger/pkgs/container/hardcharger"><img src="https://img.shields.io/badge/github--package-container--image-green.svg?logo=Docker" alt="GitHub container image"></a>
  <a href="https://github.com/gizmodata/hardcharger/releases/latest"><img src="https://img.shields.io/badge/release-binaries-orange.svg?logo=GitHub" alt="Release binaries"></a>
  <a href="https://github.com/gizmodata/chargewire"><img src="https://img.shields.io/badge/protocol-Chargewire-31a8db.svg" alt="Chargewire protocol"></a>
  <a href="https://duckdb.org"><img src="https://img.shields.io/badge/engine-DuckDB%202.0-fff000.svg?logo=duckdb&logoColor=black" alt="DuckDB 2.0"></a>
  <a href="https://arrow.apache.org"><img src="https://img.shields.io/badge/wire%20format-Apache%20Arrow-f15a24.svg" alt="Apache Arrow"></a>
  <br>
  <a href="https://pypi.org/project/adbc-driver-hardcharger/"><img src="https://img.shields.io/badge/PyPI%20client-adbc--driver--hardcharger-blue.svg?logo=PyPI" alt="PyPI: adbc-driver-hardcharger (client)"></a>
  <a href="https://github.com/gizmodata/hardcharger-adbc"><img src="https://img.shields.io/badge/ADBC%20driver-hardcharger--adbc-blue.svg?logo=Python" alt="ADBC driver"></a>
  <a href="https://github.com/gizmodata/hardcharger-jdbc"><img src="https://img.shields.io/badge/JDBC%20driver-hardcharger--jdbc-red.svg?logo=openjdk" alt="JDBC driver"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-Apache%202.0-brightgreen.svg" alt="Apache 2.0 license"></a>
  <a href="https://join.slack.com/t/gizmodatacommunity/shared_invite/zt-42jk7kdti-SJp7qk7d6XYCIKfBG~4HrA"><img src="https://img.shields.io/badge/Slack-GizmoData%20Community-4A154B?logo=slack" alt="Slack community"></a>
  <a href="https://gizmodata.com"><img src="https://img.shields.io/badge/by-GizmoData%E2%84%A2-f15a24.svg" alt="by GizmoData™"></a>
</p>

<h3 align="center">Fast, secure, remote DuckDB. Every feature included.</h3>

---

## 🏎️ What is Hardcharger?

**Hardcharger™** puts [DuckDB 2.0](https://duckdb.org) on the network. Clients connect over
[**Chargewire**](https://github.com/gizmodata/chargewire), an open HTTP protocol that moves
[Apache Arrow](https://arrow.apache.org) record batches straight from DuckDB to your
application: no gRPC, no Flight, no sidecars.

It is the successor to [GizmoSQL](https://github.com/gizmodata/gizmosql), rebuilt from
scratch for DuckDB 2.0, and it is free: no editions, no license keys. Everything that was
Enterprise in GizmoSQL is in every Hardcharger build.

- 🦆 **DuckDB 2.0 inside.** A standalone server on D

[...截断...]

uckDB's v2 C API, not an extension.
- ⚡ **Chargewire on the wire.** A query and its first rows come back in one HTTP round trip.
  Large results stream as Arrow IPC, compressed with LZ4 or zstd when asked, and can be resumed. Bulk ingest
  streams Arrow straight into a table.
- 🔐 **Security in the core, not bolted on.** Token sign-in, TLS and mTLS, and role-based
  access control checked inside DuckDB against each statement's own plan. Also row
  policies, column masking, tenants, SSO (OIDC/JWKS) and a tamper-evident audit log.
- 🔭 **Observable.** Instrumentation into a DuckDB file or PostgreSQL, catalog logging (also
  into DuckLake), a Prometheus `/metrics` endpoint, query profiles and `KILL SESSION`.
- 🧩 **Configured your way.** Flags, `HARDCHARGER_*` environment variables, or a YAML file.
- 🌐 **Ready to scale out.** Results are already described as partitions with locations,
  so distributed query execution can arrive without a protocol change.

## 🖥️ Desktop app (v2.1.0+)

Run Hardcharger from a native app for macOS 15+ on Apple silicon or Windows: start and
stop the server, open its SQL workspace, manage settings, and follow the logs. Closing
the window leaves the server running in the macOS menu bar or Windows system tray;
**Quit Hardcharger** stops it.

<p align="center">
  <img src="docs/assets/desktop-preview-light.png" alt="Hardcharger desktop dashboard design preview, light theme: server controls, database information and the SQL workspace button" width="49%">
  <img src="docs/assets/desktop-preview-dark.png" alt="Hardcharger desktop dashboard design preview, dark theme" width="49%">
</p>

The dashboard images show the design preview with sample data. The app runs the same
`hardcharger-server` executable shipped in the command-line packages and opens its built-in
web UI in a separate window. It also bundles the `hardcharger` CLI. Pick the desktop app
for an interactive computer, or the command-line packages for terminals, automation,
containers and operating-system services. Both remain supported.

For v2.1.0+, desktop release artifacts use the **`Hardcharger-desktop-…`** prefix:
the macOS `.dmg` is signed and notarized, and the Windows `.msi` is signed. The existing
Windows `Hardcharger-windows-…msi` installs the command-line tools. Linux users continue
to use the command-line packages or Docker; a Linux desktop package is follow-up work.
See the [desktop guide](docs/desktop-app.md) for installation, network sharing, certificates,
settings import/export, and the difference between closing and quitting.

<a id="built-in-web-ui"></a>

## 🌐 Built-in web UI

<p align="center">
  <img src="docs/assets/web-ui-query-light.png" alt="Hardcharger's web UI, light theme: the schema browser with the server and its catalogs, two editor tabs, and a query's results" width="49%">
  <img src="docs/assets/web-ui-query-dark.png" alt="Hardcharger's web UI, dark theme" width="49%">
</p>

Hardcharger has a web UI compiled into the server binary: nothing extra to install, and it is
served on the server's own port and TLS certificate. It is off by default; `--web-ui` turns it on
(or `HARDCHARGER_WEB_UI=true`, or `web_ui: true` in the YAML file).

```bash
openssl req -x509 -newkey ec -pkeyopt ec_paramgen_curve:prime256v1 -nodes -days 30 -subj /CN=localhost -addext subjectAltName=DNS:localhost -keyout server.key -out server.pem
HARDCHARGER_ADMIN_PASSWORD='change-me' hardcharger-server --web-ui --tls-cert server.pem --tls-key server.key --database demo.duckdb
# open https://localhost:31337/ui and sign in as hardcharger / change-me (the certificate is self-signed)
```

- ✍️ **SQL editor**: up to 20 tabs, each with its own session (its own transaction, temporary
  tables and settings). Ctrl/⌘+Enter runs the statement at the cursor (a bar in the margin
  marks it) or exactly the selection; ⇧ runs all, with a result tab per result set and
  Messages. Cancel stops the statement on the server and says how far a script got. An open
  or failed tran