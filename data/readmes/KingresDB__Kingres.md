<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="kingres/brand/svg/kingres-db-horizontal-color-dark.svg">
    <img src="kingres/brand/svg/kingres-db-horizontal-color-light.svg" alt="KingresDB" width="420">
  </picture>
</p>

KingresDB
=========

KingresDB (short name `kingres`) is a database derived from PostgreSQL.  It
adds sharding, a tamper-evident ledger with a standalone verifier, a cluster
control plane with a REST API and a web console, and analytics extensions
(approximate aggregates, time partitioning, columnar storage).  Most of the
new behaviour is in extensions (`contrib/kingres_*`) and in the `kingres/`
directory; the rest of this tree is the PostgreSQL source it is based on.  It
is built for PostgreSQL 18 (this branch) and for PostgreSQL 19 (branch
`kingres-19`), from one source of each extension.

**Status.**  There is no release yet.  The first release will be 0.1.0.  It
contains every phase of the roadmap except phase 8 (a global snapshot and a
multi-node ledger), which is future roadmap, and phase 15 (management of
third-party extensions), which comes after the first release.  Sharding,
query pushdown, table lifecycle, elasticity, distributed schemas, high
availability, the ledger with its verifier, signing and anchoring, the control
plane and the console, analytics, configuration from the console and the export
and import of tables and databases are built.  The README of the project states
the exact state of every phase, and
[kingres/docs/guide/limitations.md](kingres/docs/guide/limitations.md) lists what
KingresDB does not do.  Failover is new in this release: test your recovery
procedure before you rely on it.

- [kingres/README.md](kingres/README.md): the status of every phase, the
  repository map and the documentation.
- [Wiki](https://github.com/KingresDB/Kingres/wiki): a guide to the design, the
  components, building, installing and development.
- [LICENSE](LICENSE): KingresDB's own code is under AGPL-3.0-only; PostgreSQL's
  code keeps its licence ([COPYRIGHT](COPYRIGHT)).
- [Contributing](.github/CONTRIBUTING.md), [security
  policy](.github/SECURITY.md) and [code of
  conduct](.github/CODE_OF_CONDUCT.md).

KingresDB is derived from PostgreSQL.  It is not PostgreSQL, and it is not
endorsed by the PostgreSQL project.  The original PostgreSQL README follows
unchanged.

PostgreSQL Database Management System
=====================================

This directory contains the source code distribution of the PostgreSQL
database management system.

PostgreSQL is an advanced object-relational database management system
that supports an extended subset of the SQL standard, including
transactions, foreign keys, subqueries, triggers, user-defined types
and functions.  This distribution also contains C language bindings.

Copyright and license information can be found in the file COPYRIGHT.

General documentation about this version of PostgreSQL can be found at
<https://www.postgresql.org/docs/18/>.  In particular, information
about building PostgreSQL from the source code can be found at
<https://www.postgresql.org/docs/18/installation.html>.

The latest version of this software, and related software, may be
obtained at <https://www.postgresql.org/download/>.  For more information
look at our web site located at <https://www.postgresql.org/>.
