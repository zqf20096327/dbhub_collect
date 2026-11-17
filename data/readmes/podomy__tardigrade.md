Tardigrade

License: GNU Affero General Public License v3.0 or later (/LICENSE)

Tardigrade is a distributed SQL database, developed in the open. It is
a CP system: serializable transactions, Raft replication per range,
PostgreSQL wire compatible. It survives minority-partition outages by
refusing work rather than diverging.

Documentation

  Changelog - /CHANGELOG
  Contributing - /CONTRIBUTING
  Commit message format - /COMMITS
  Contributor license agreement - /CLA
  Upstream technical docs - /docs/: CockroachDB-authored design notes,
    RFCS, and tech notes, retained for reference

Contributing

Tardigrade takes no pull requests. Propose first, patch second,
both by email to contact@podomy.com.

1. RFC: send a request for comments describing the problem and
   the approach. Wait for agreement before writing any code.
2. Patch: build the change as commits following /COMMITS,
   export them with git format-patch, and send them with
   git send-email. That mailed diff is the change; there is
   no PR queue behind it.

  Commit message format - /COMMITS
  Contributor license agreement - /CLA
  Contributing - /CONTRIBUTING

License

Tardigrade is distributed under the GNU Affero General Public License
v3.0 or later. See /LICENSE.
