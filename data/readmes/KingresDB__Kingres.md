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

**Status.**  There is no release and no beta yet.  The first release will
contain every phase of the roadmap except phase 8, which is future roadmap.
Sharding, the ledger and its verifier, the control plane and the console are
built; query pushdown, table lifecycle, high availability, signing and
anchoring of the ledger, and analytics are still in progress; elasticity
(phase 10) and distributed schemas (phase 11) are designed and not built yet.
Many parts have
been independently reviewed and their findings fixed; some fixes have not been
reviewed again, and some findings are open.  In particular, failover must not
be relied on yet, and nothing should be treated as anchored outside the
database until an open finding in the anchoring is fixed.  The README of the
project states the exact state of every phase.

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
