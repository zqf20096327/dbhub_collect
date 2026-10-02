# OpenADS

📖 **Docs**:
[English](https://fivetechsoft.github.io/OpenADS/en/)
· [Español](https://fivetechsoft.github.io/OpenADS/es/)
· [Português](https://fivetechsoft.github.io/OpenADS/pt/)

🤝 **Contributing:** [`CONTRIBUTING.md`](CONTRIBUTING.md)

A free and open-source implementation compatible with Advantage Database Server (ADS), discontinued by SAP.

The goal is to provide a *drop-in* replacement for the Advantage Client Engine (`ace32.dll` / `ace64.dll` / `libace.so`) so existing applications — particularly Harbour/Clipper apps using `contrib/rddads` — keep working without recompilation.

### One API, many backends — DBF today, any database tomorrow

OpenADS **presents as ADS** — your application talks to the same ACE
entry points it always did — but that ADS surface is just the front
door. Behind it, the very same API can be served by different storage
engines:

| Backend | Connection | Use it for |
|---------|-----------|------------|
| **DBF / ADT** (native xBase, CDX/NTX/ADI indexes) | local path or `tcp://` | the default — your existing `.dbf` data, unchanged |
| **SQLite** | `AdsConnect60("sqlite://…")` | a single-file SQL database, zero server |
| **PostgreSQL** | `postgresql://…` | a scalable, concurrent, server-class RDBMS |
| **MariaDB / MySQL** | `mariadb://…` | the MySQL ecosystem |
| **Microsoft SQL Server** | `mssql://…` | native TDS 7.4, optional TLS |
| **ODBC** | `odbc://…` | anything else with a driver |

Because the application only ever sees the ADS API, **you run on DBF
today and switch to PostgreSQL, MSSQL, or SQLite tomorrow if you
outgrow flat files — without rewriting your business logic.** The same
Harbour/Clipper/FiveWin code, the same `USE` / `dbSeek` / `tDatabase`
calls, now backed by a real database when you need concurrency, scale,
or central administration. OpenADS is a *scalable suite*, not a single
file format: keep your legacy investment, change the engine under it on
your own schedule. See [`docs/OPENADS_PLUS.md`](docs/OPENADS_PLUS.md)
and the per-backend cookbooks under [`cookbook/orm/`](cookbook/orm/).

### Independence, provenance, and trademarks

- **Independent implementation.** OpenADS is an independent
  open-source project. It is not affiliated with, sponsored by, or
  endorsed by SAP SE. "Advantage Database Server", "ADS", and any
  related marks, logos, and product names are the property of their
  respective owners and are referenced here solely to describe
  compatibility — their use does not imply any affiliation or
  endorsement.
- **No SAP-owned binaries required.** The OpenADS DLL is a
  drop-in replacement; running an application against
  `ace32.dll` / `ace64.dll` / `libace.so` produced by this project
  does **not** require any DLL, `.so`, or other binary owned by SAP.
  The only runtime dependencies are the host operating system's
  standard libraries (e.g. `KERNEL32.dll` and the Microsoft Visual
  C++ / Universal CRT runtime on Windows; `libc` / `libstdc++` on
  Linux).
- **Provenance — clean-room.** This codebase is written from
  publicly observable behavior of the original Advantage Client
  Engine and from the **public** Harbour `contrib/rddads` source
  (which is the call site OpenADS targets). It is **not** derived
  from leaked internal manuals or from disassembly / reverse
  engineering of SAP-owned binaries that would violate the
  Advantage SDK / ACE EULA. The implementation has been generated
  by an AI assistant (Anthropic Claude) under direct human
  supervision; every milestone is reviewed, tested, and committed
  by a human maintainer.
- **Purpose — non-commercial preservation.** OpenADS is a
  community-driven open-source project pursued **without economic
  benefit to its maintainers**. Its only goal is to provide a
  compatibility path for legacy applications affected by SAP's
  discontinuation of Advantage Database Server, so the existing
  Harbour / Clipper code base that depends on the ACE entry points
  can keep running. The project does not 

[...截断...]

sell, license, sublicense,
  or otherwise monetise the software; redistribution is permitted
  by the Apache License 2.0 (see [`LICENSE`](LICENSE)) but the
  upstream maintainers receive no fee for the work.
- **No warranty, no support contract.** OpenADS is provided **AS
  IS**, without warranty of any kind, express or implied (see the
  Apache License 2.0 §7 and §8). There is no service-level
  agreement, no commercial support channel, and no representation
  of fitness for any particular purpose.
- **Downstream responsibility.** Users who deploy OpenADS as a
  drop-in replacement for the Advantage Client Engine remain solely
  responsible for ensuring that **their own** use of related
  third-party tooling (Harbour, Clipper, original Advantage
  installations, application code, fixtures) complies with whatever
  licenses, EULAs, or service agreements apply to those components.
  The project ships no SAP-owned binary and asserts no permission
  on behalf of any third-party rightsholder.

## Status

**Harbour rddtst.prg: 442 / 442 PASS (100%)** (2026-05-08). The
canonical Harbour RDD compatibility harness (`harbour/tests/rddtest/
rddtst.prg`, the same suite that DBFCDX is benchmarked against)
runs end-to-end through `contrib/rddads` linked to OpenADS'
`ace64.dll` with **zero failures** on Windows MSVC64. Validated
fixture (`tools/harbour_patch/adscl52_ads.prg`) is regenerated by
`rddmktst` against the ADS RDD itself, so the inlined expected
values reflect ADS-engine behaviour rather than DBFCDX's. For
context: native DBFCDX scores 369 / 442 against its own DBFCDX-
generated baseline; OpenADS clears every line of the regenerated
ADS-flavoured baseline. The session that closed the last gap is
recorded across 28 incremental commits ending at `28be1be`.

**Current release: [v1.09.68](https://github.com/FiveTechSoft/OpenADS/releases/tag/v1.09.68) (2026-09-20).**
OpenADS has broad compatibility coverage, but support varies by API and
backend. Before production deployment, review [`TODO.parity.md`](TODO.parity.md)
and [`docs/known-issues.md`](docs/known-issues.md), test the exact workload,
and apply normal database security and backup controls. In particular,
documented Data Dictionary and access-control parity gaps make untrusted or
multi-user deployments experimental until those gaps are closed. `openads_serverd` serves the OpenADS wire
protocol; clients connect with
`AdsConnect60("tcp://host:port/path.add", ...)` and no application code
changes. Docs:
[English](https://fivetechsoft.github.io/OpenADS/en/) ·
[Español](https://fivetechsoft.github.io/OpenADS/es/) ·
[Português](https://fivetechsoft.github.io/OpenADS/pt/) —
including [migrating from ADS](https://fivetechsoft.github.io/OpenADS/en/migrating-from-ads/)
(CDX rollback / error 7017 caveat). `docs/wire-protocol.md` is the
formal spec for non-C++ clients (Python, Go, Rust, Harbour AEP).

Cross-platform CI runs on Ubuntu, macOS, and Windows. Check the current
[Actions results](https://github.com/FiveTechSoft/OpenADS/actions/workflows/ci.yml)
before relying on a branch or release; this document does not claim that the
latest run is green.

Release timeline:

| Tag       | Date       | Highlights |
|-----------|------------|-----------|
| **v1.8.2** | 2026-07-08 | **CI green on Linux/macOS** — NTXPL852 test fixture fixes Clang build; POSIX release ZIPs/tarballs ship again. Same engine as v1.8.1. |
| **v1.8.1** | 2026-07-08 | **`OrdScope` string key padding** — `setScopeTop`/`setScopeBottom` on character fields (work-order filters) honour scoped `GotoTop`/`Skip` on local and remote. |
| **v1.8.0** | 2026-07-08 | **NTXPL852 / PL852 OEM collation** — Polish CP-852 index sort (Ł between L and M); CDX bulk `REINDEX`; 19 new unit tests. |
| **v1.7.0** | 2026-07-08 | **REMOTE `AdsSetScope` / `OrdScope`** — `GotoTop`/`Skip` honour scoped key ranges over `tcp://` (Harbour labour-item / work-order filters). Docs: CDX rollback warning (SAP ACE error 7017). |
| **v1.6.5** | 2026-07-07 | **RE