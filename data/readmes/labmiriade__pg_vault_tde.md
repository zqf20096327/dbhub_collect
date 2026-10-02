# pg_vault_tde

[![build main](https://img.shields.io/github/actions/workflow/status/labmiriade/pg_vault_tde/ci.yml?branch=main&label=build%20main)](https://github.com/labmiriade/pg_vault_tde/actions/workflows/ci.yml?query=branch%3Amain)
[![build develop](https://img.shields.io/github/actions/workflow/status/labmiriade/pg_vault_tde/ci.yml?branch=develop&label=build%20develop)](https://github.com/labmiriade/pg_vault_tde/actions/workflows/ci.yml?query=branch%3Adevelop)
[![CodeQL](https://img.shields.io/github/actions/workflow/status/labmiriade/pg_vault_tde/codeql.yml?branch=develop&label=CodeQL)](https://github.com/labmiriade/pg_vault_tde/security/code-scanning)
[![packages](https://img.shields.io/github/actions/workflow/status/labmiriade/pg_vault_tde/build-packages.yml?label=packages)](https://github.com/labmiriade/pg_vault_tde/actions/workflows/build-packages.yml)
[![PGXN](https://img.shields.io/badge/PGXN-pg__vault__tde-blue)](https://pgxn.org/dist/pg_vault_tde/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17%20%7C%2018-336791)](#compatibility)
[![License](https://img.shields.io/badge/license-PostgreSQL-blue)](LICENSE)

**Transparent Data Encryption (TDE) for PostgreSQL 17+** — Open-source (PostgreSQL License), plug-and-play, zero core modifications.

pg_vault_tde encrypts every tuple with **AES-256-GCM** at the Table Access
Method layer. Data is encrypted before it reaches the storage manager and
decrypted after it leaves. Encryption keys are managed by **HashiCorp Vault** /
**OpenBao** or a **local PKCS#12 wallet** and cached in shared memory with
automatic rotation.

**Current release: v1.7** — 141 regression tests (44 v1.4 + 20 v1.5 + 36 v1.6 + 41 v1.7), zero compiler warnings on PG 17 + PG 18.

### Commercial Support

Looking for professional support for `pg_vault_tde` in production? At [Miriade](https://miriade.it), we offer dedicated enterprise services, including:

* **24/7 Production Support & SLA Guarantees**
* **Custom Feature Development & Vault Integration**
* **Performance Tuning & Security Audits**
* **Managed Setup & Migration Assistance**

Learn more about our enterprise encryption solutions at [Mircrypt](https://www.miriade.it/en/products/mircrypt-it)

Contact our engineering team at [marketing@miriade.it](mailto:marketing@miriade.it) to discuss your requirements.

### Compatibility

PostgreSQL 17 and 18, 19 planned; OpenSSL 3.x required. Per-major API notes in
[Version Compatibility](doc/pg_vault_tde.md#postgresql-version-compatibility);
packaged (OS, PG) combinations and what CI exercises on each in the
[Support Matrix](doc/pg_vault_tde.md#support-matrix).

---

## Quick Start

> **Already running 1.7.0 or earlier?** Do not upgrade to 1.7.1 or later before
> reading [Upgrading to 1.7.1](#upgrading-to-171). Tables holding out-of-line
> TOAST values must be dumped *before* the new binary is installed.
>
> **Upgrading from 1.7.1?** If `pg_vault_tde_rotate_online()` has run since the
> last restart, act *before* restarting: copy out a rotated table that was being
> read or written — see [`rotate_online()` with concurrent access](#rotate_online-with-concurrent-access) —
> and run `VACUUM FULL` on a rotated table with out-of-line values — see
> [`rotate_online()` and out-of-line values](#rotate_online-and-out-of-line-values).
> A standby promoted while still on 1.7.1 must be restarted before its first write —
> see [Streaming standby and `rotate_online()`](#streaming-standby-and-rotate_online).
> Every table ever rotated needs a `REINDEX` — see [`rotate_online()` and indexes](#rotate_online-and-indexes) —
> and so does every partial index on an encrypted table — see [Partial indexes on encrypted tables](#partial-indexes-on-encrypted-tables).
> Check who created each database's wallet — see [Who may call the key-management functions](#who-may-call-the-key-management-functions).
> Otherwise nothing has to be done before installing 1.7.2, but existing
> encrypted tables need one `VACUUM FULL` afterwards 

[...截断...]

— see
> [Upgrading to 1.7.2](#upgrading-to-172). Rows stay readable either way; until
> they are rewritten, `UPDATE` on some of them can take the backend down.

### 1. Install

```bash
# Build and install into your PostgreSQL instance
git clone https://github.com/labmiriade/pg_vault_tde.git
cd pg_vault_tde

# The PostgreSQL packages below come from the PGDG repository for any major your
# distribution does not ship itself — PG 18 on Debian 13, every major on
# RHEL/Rocky. Set it up first if you have not already:
#   https://www.postgresql.org/download/
# On RHEL/Rocky also run:  dnf -qy module disable postgresql

# On Debian/Ubuntu (PG 18) — server-dev pulls in the clang/llvm PGXS needs for bitcode
apt-get install -y build-essential postgresql-server-dev-18 \
                   libssl-dev libcurl4-openssl-dev pkg-config
make && sudo make install

# On Debian/Ubuntu (PG 17)
apt-get install -y build-essential postgresql-server-dev-17 \
                   libssl-dev libcurl4-openssl-dev pkg-config
make PG_CONFIG=/usr/lib/postgresql/17/bin/pg_config && sudo make install

# On RHEL/Rocky — EPEL and CRB first: postgresqlNN-devel needs perl(IPC::Run)
dnf install -y epel-release
dnf config-manager --set-enabled crb

# On RHEL/Rocky (PG 18) — clang/llvm-devel are NOT pulled in by postgresqlNN-devel,
# and redhat-rpm-config provides the hardening spec file pg_config injects
dnf install -y postgresql18-devel openssl-devel libcurl-devel \
               gcc make redhat-rpm-config clang llvm-devel
make PG_CONFIG=/usr/pgsql-18/bin/pg_config && make install

# On RHEL/Rocky (PG 17)
dnf install -y postgresql17-devel openssl-devel libcurl-devel \
               gcc make redhat-rpm-config clang llvm-devel
make PG_CONFIG=/usr/pgsql-17/bin/pg_config && make install
```

**Or via [PGXN](https://pgxn.org/dist/pg_vault_tde/)** (same OS build
dependencies as above are still required — `pgxn install` just runs the
build for you):

```bash
pip install pgxnclient   # or: apt-get install pgxnclient / dnf install pgxnclient
pgxn install pg_vault_tde
```

See [wiki: Installation](https://github.com/labmiriade/pg_vault_tde/wiki/Installation)
for package-based (`.deb`/`.rpm`) installs and full per-OS prerequisites.

### 2. Configure PostgreSQL

Add to `postgresql.conf`:

```
shared_preload_libraries = 'pg_vault_tde'
```

> **Check the WAL resource manager id first.** pg_vault_tde registers a custom WAL
> resource manager under id **161**, reserved for it on the PostgreSQL *Custom WAL
> Resource Managers* wiki. Extensions that follow the registry never use it, but an
> unregistered one — typically in-house or proprietary — can. On every node that
> will load pg_vault_tde or replay its WAL (primary, standbys, PITR restore hosts),
> this must return **no rows** before you add it:
>
> ```sql
> SELECT rm_id, rm_name FROM pg_get_wal_resource_managers()
> WHERE rm_id = 161 OR rm_name = 'pg_vault_tde';
> ```
>
> If it returns one, the server will refuse to start once pg_vault_tde is preloaded
> (`failed to register custom resource manager "pg_vault_tde" with ID 161`). After the
> restart the same query must return exactly `161 | pg_vault_tde`. Any role can run it.

Restart PostgreSQL and create the extension in your database:

```sql
CREATE EXTENSION pg_vault_tde;
```

### 3. Configure Key Access


#### a) HashiCorp Vault / OpenBao

`kms_provider` has no built-in default — it must be set explicitly. Set GUC
parameters in `postgresql.conf` (or `ALTER SYSTEM`) to point at your Vault /
OpenBao instance:

```ini
pg_vault_tde.kms_provider          = 'vault'
pg_vault_tde.vault_url            = 'https://vault.example.com:8200'
pg_vault_tde.vault_namespace      = ''          # leave empty for community edition
pg_vault_tde.vault_token          = 'hvs.TOKEN' # or use AppRole (1.1)
pg_vault_tde.vault_transit_mount  = 'transit'
pg_vault_tde.vault_key_name       = 'pg-tde-dek'
pg_vault_tde.vault_ca_cert        = '/etc/ssl/vault/ca.pem'
pg_vault_tde.vault_timeout_ms     = 5000
p