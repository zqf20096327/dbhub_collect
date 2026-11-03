# opengauss-oracle-fdw

**Oracle Foreign Data Wrapper for openGauss** — based on [oracle_fdw](https://github.com/laurenz/oracle_fdw) 2.2.0, with the official openGauss adaptation patches plus an additional patch that lets non-UTF-8 Oracle data (e.g. GBK bytes in a US7ASCII database) pass through without corruption.

*This is a community-maintained project and is **not** an official openGauss or Huawei project.*

[中文说明](README.zh-CN.md)

---

## What is this?

[oracle_fdw](https://github.com/laurenz/oracle_fdw) is the well-known PostgreSQL foreign data wrapper for Oracle, written by Laurenz Albe (upstream license: permissive BSD-style, see [LICENSE](LICENSE)).

openGauss ships its own adaptation of oracle_fdw (sources and patches published in [openGauss-third_party](https://atomgit.com/opengauss/openGauss-third_party) under Mulan PSL v2), but there is **no standalone public repository** of the patched, buildable source tree — you normally have to extract it from the openGauss source tree and third-party build system.

This repository fills that gap and adds one practical enhancement:

| Patch | Source | What it does |
|---|---|---|
| `opengauss_oracle_fdw-2.2.0_patch.patch` | openGauss official | main openGauss adaptation |
| `gsc.patch` | openGauss official | global syscache adaptation |
| `opengauss_oracle_fdw-2.2.0_patch_20221230.patch` | openGauss official | join push-down interface adaptation |
| `opengauss-reltargetlist.patch` | openGauss official | reltargetlist adaptation |
| **`0001-openGauss-CN-PATCH-1`** | **this repo** | skip the forced UTF-8 verification so that non-UTF-8 Oracle data (e.g. GBK bytes in a US7ASCII database) is stored raw and can be converted on the openGauss side |

The source tree in this repository is **complete and build-ready**: upstream oracle_fdw 2.2.0 + all four official openGauss patches + CN-PATCH-1 applied. All patches are kept under [`patches/`](patches) for traceability.

## Why CN-PATCH-1 (non-UTF-8 / GBK support)?

Many legacy Oracle installations in China use database character set **US7ASCII** while the actual data is **GBK bytes** (written by clients that claim US7ASCII). When openGauss (a UTF-8 database) reads such columns through oracle_fdw:

1. By default the OCI session uses the database encoding (UTF-8); Oracle then converts the GBK bytes and turns them into the replacement character (U+FFFD) — **irreversibly destroyed**.
2. Even with a raw-byte OCI session (`nls_lang` FDW option), the openGauss adaptation patch rejects non-UTF-8 bytes with `invalid byte sequence for encoding "UTF8"`.

CN-PATCH-1 disables that verification (a 3-line, clearly marked change in `convertTuple`, see [the patch](patches/0001-openGauss-CN-PATCH-1-skip-utf8-verify.patch)), so the original bytes reach the `varchar` column **bit-exact** (verified with `octet_length`). The data is then converted **on the openGauss side only**:

```sql
-- ① make OCI transfer bytes untouched (FDW-level option, openGauss adaptation)
ALTER FOREIGN DATA WRAPPER oracle_fdw OPTIONS (ADD nls_lang 'AMERICAN_AMERICA.US7ASCII');

-- ② display: raw bytes -> GBK decoding (view on the foreign table)
CREATE OR REPLACE VIEW v_ora_emp AS
SELECT empno,
       convert_from(substring(ename::bytea FROM 1 FOR octet_length(ename)), 'GBK') AS ename
FROM ora_emp;                      -- ora_emp is the foreign table

-- ③ consistency check: byte-wise equality (bytea = bytea)
SELECT v.empno,
       CASE WHEN substring(v.ename::bytea FROM 1 FOR octet_length(v.ename))
                 = convert_to(l.ename, 'GBK')
            THEN 'MATCH' ELSE 'DIFF' END
FROM ora_emp v JOIN local_emp l USING (empno);
```

Full write-up, caveats (e.g. never cast `::bytea` without `substring` + `octet_length`, encoding detection via `DUMP(col,1016)`) and rollback notes: [README.zh-CN.md](README.zh-CN.md) § US7ASCII, and the deployment package document [`README-内网部署.md`](docs/README-内网部署.md).

*Impact on regular UTF-8 Oracle databases: none. The skipped verification only mattered for invalid byte sequences; well-formed UTF-8 data behaves exactly as before (verified against an AL32UTF8 Oracle 11g).*

### Performance notes for large tables

* The `substring + convert_from` conversion itself is cheap (C-level, tens of nanoseconds per character). For a million rows with two Chinese columns it is a few seconds of CPU — rarely the bottleneck.
* The real costs of a large foreign-table query are OCI row transfer (network round trips) and any filtering that **cannot be pushed down** to Oracle. Therefore:
  1. Never put converted columns in `WHERE` — conditions on them cannot be pushed down and force a full table transfer. Filter by numeric/date/key columns only (e.g. primary-key ranges).
  2. Never use a converted column as the JOIN key — the join would have to happen on the openGauss side after transferring the whole foreign table. Join on numeric keys; convert Chinese columns only for display/comparison.
  3. For repeated checks on a large table, **materialize once** into a local temp table (bytea columns), then run local joins — the conversion cost is paid a single time:
     ```sql
     CREATE TEMP TABLE ora_snap AS
     SELECT empno, substring(ename::bytea FROM 1 FOR octet_length(ename)) AS ename_b
     FROM ora_emp WHERE empno BETWEEN :lo AND :hi;   -- slice large tables by key range
     SELECT s.empno, CASE WHEN s.ename_b = convert_to(l.ename,'GBK') THEN 'MATCH' ELSE 'DIFF' END
     FROM ora_snap s JOIN local_emp l ON l.empno = s.empno;
     ```
  4. Raise the table option `prefetch` (default 100) to e.g. 10000 to reduce fetch round trips.
* GUI clients (DBeaver etc.) **cannot** `SELECT *` directly from the raw foreign table — the JDBC driver decodes `varchar` as UTF-8 and throws `Illegal UTF-8 sequence` on GBK bytes. Always query through the conversion view. This error actually confirms that bytes arrived intact.

## Compatibility

| Item | Verified |
|---|---|
| openGauss | 6.0.2 / 6.0.3 (single build covers both; built on official tag v6.0.3) |
| Oracle client | Instant Client 11.2.0.4 (x86_64, Basic+SDK) |
| Oracle server | 11.2.0.4 (AL32UTF8 and US7ASCII+GBK both verified end-to-end, incl. JOIN) |
| OS | Kylin Linux Advanced Server V10 (Lance/Halberd) x86_64, glibc 2.28 |
| Build flags | `-march=x86-64 -mtune=generic` (no `-march=native`; max GLIBC symbol GLIBC_2.14) |

## Build

This tree is meant to be built **inside the openGauss source tree** (openGauss has no PGXS for contrib modules): copy/symlink it to `contrib/oracle_fdw`'s expected location (`dependency/oracle_fdw` under the server source root or a third-party binarylibs directory), run `./configure` on the server tree, then `make -C contrib/oracle_fdw`. See the step-by-step guide: [docs/BUILD-kylinV10.md](docs/BUILD-kylinV10.md) (Kylin V10, gcc 7.3, offline build without binarylibs).

Prebuilt binaries are **not** published here; build reproducibly from this source instead.

## Repository layout

```
├── oracle_fdw.cpp / oracle_utils.cpp / oracle_gis.cpp / oracle_fdw.h   # patched, build-ready source
├── Makefile / oracle_fdw.control / oracle_fdw--*.sql                   # extension files
├── README.oracle_fdw / UPSTREAM.md / CHANGELOG / TODO                  # upstream documentation
├── patches/
│   ├── oracle_fdw-ORACLE_FDW_2_2_0.tar.gz        # pristine upstream 2.2.0
│   ├── upstream-opengauss/                        # the four official openGauss patches
│   └── 0001-openGauss-CN-PATCH-1-skip-utf8-verify.patch   # the non-UTF-8 enhancement
├── docs/
│   ├── BUILD-kylinV10.md                          # offline build guide
│   └── README-内网部署.md                          # production deployment handbook (CN)
└── LICENSE                                        # upstream BSD-style license
```

## License & attribution

- Upstream oracle_fdw (c) Magistrat der Stadt Wien / Cybertec Schönig & Schönig GmbH — permissive BSD-style license, see [LICENSE](LICENSE). Retained in full, including all copyright headers.
- Official openGauss adaptation patches — from [openGauss-third_party](https://atomgit.com/opengauss/openGauss-third_party), licensed under **Mulan PSL v2**.
- `CN-PATCH-1` and this repository layout — © zhangqxgz, released under the same permissive terms as upstream oracle_fdw.

Trademarks: *Oracle* is a trademark of Oracle Corporation; *openGauss* is a trademark of its respective owners. This project is independent community work.

## Related

- Deployment package (Kylin V10, glibc 2.28, x86_64, openGauss 6.0.2/6.0.3, IC 11.2.0.4): built from this source, incl. verify script and Chinese deployment handbook.
- Upstream oracle_fdw: https://github.com/laurenz/oracle_fdw
