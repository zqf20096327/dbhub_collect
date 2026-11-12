# OceanBase for Flow Steward

Connect OceanBase to Flow Steward for reusable Dataset queries and workflow-driven data changes over its MySQL-compatible interface. The Dataset connector tests access, inspects typed table schemas, validates saved SQL against selected resources, previews results, runs saved queries and infers their output schema. Use application lookups and reporting extracts to supply data to subsequent workflow steps while keeping Dataset queries read-only.

A separate workflow action runs one INSERT, UPDATE or DELETE with named parameters and an optional parameter schema. Use it to save workflow output or change existing application records in the configured OceanBase database, subject to the server's SQL support and the database user's permissions. Parameter values are supplied separately from SQL, allowing reusable statements to accept different workflow inputs.

Configure the host, port, database and user and store a nonempty password in secrets. This package targets OceanBase's MySQL-compatible endpoint and does not provide an Oracle-mode interface. Reads return at most 100 rows and 480 KiB. SQL support is a restricted subset; schema administration, transaction scripts and database triggers are outside the connector's operation set.

## Runtime and operation requirements

Connect **OceanBase** datasets and run parameterized workflow writes. This repository contains one installable OceanBase extension, version **1.3.6**, with separate Linux AMD64 and ARM64 archives. No other database can be selected or installed from this package.

## Set up a OceanBase connection

Create a project connection using these settings:

| Setting | Meaning |
| --- | --- |
| `host` | OceanBase host. Required. |
| `port` | OceanBase port. Required. |
| `database` | OceanBase database. Required. |
| `user` | OceanBase user. Required. |

Store the OceanBase user password in the connection secrets. The pinned source requires a nonempty password; datasets may alternatively use their password environment secret. Resolved dataset secret environment values are forwarded to the native process; direct environment overrides retain their established precedence. Dataset advanced environment exposes only the named OCEANBASE_ source variables; password overrides remain in secrets. Writer connections use the explicit settings above.

Use an OceanBase MySQL-compatible endpoint and the user identity expected by that endpoint. This package does not offer an Oracle-mode interface.

## Read datasets and write from workflows

Datasets support connection testing, typed schema introspection, saved SQL, visual-query resource scope validation, bounded previews and execution. Read queries use the native read-only path and are capped at 100 rows and 480 KiB inline output. No trigger surface is exposed.

`execute_write` runs one INSERT, UPDATE or DELETE on the selected OceanBase project connection. Provide `connection_ref`, SQL with named `:parameters`, a `params` object and optional JSON `param_schema`. Values stay separate from SQL and use native driver binding. The server must support the supplied SQL syntax.

The host resolves matching project configuration and secrets, account/project scope, execution context and a durable external-effect claim. Test mode suppresses writes before a driver starts. Writes execute once; uncertain dispatched failures return `retryable: false` and require checking the database before a manual retry. Workflow writes do not make dataset queries writable.

The bounded SQL subset refuses raw dollar characters and backslashes in read SQL; write SQL also refuses raw dollar characters. Put those values in bound parameters. A top-level read LIMIT accepts one integer literal with an optional integer OFFSET. The existing SQL safety guards are unchanged; 1.3.0 adds database-specific settings validation and preserves native payloads.

## Upgrade compatibility

The visible name is OceanBase. The legacy extension ID `flowsteward.data-connector-mcp-toolbox-oceanbase`, project connection type `toolbox_sql_writer`, dataset connector IDs and action IDs remain unchanged so existing installations and workflows can upgrade. These are internal compatibility identifiers, not a second database selector.

## Technical implementation and packaging

Google MCP Toolbox is implementation tooling, pinned to tag `v1.16.0`, commit `06ea49d9a487a72c22419b5a8d5c22c11f0d7485`. Its fixed native build registers only this repository's OceanBase interfaces. Installation and runtime download no drivers. Native binaries are rebuilt with Go 1.27.4 and the reviewed module baseline; toolbox-provenance.json records exact patches, dependencies and binary digests.

To package the existing verified binaries:

```sh
python3 scripts/package_extension.py --runtime-target linux-amd64
python3 scripts/package_extension.py --runtime-target linux-arm64
```

`scripts/build_toolbox.sh` is the optional pinned implementation rebuild; it cannot select another database. `toolbox-provenance.json`, `THIRD_PARTY.yml` and root `SHA256SUMS` describe the native payloads. Each installer ZIP contains exactly one executable for its target and target/native metadata. The byte-exact Apache-2.0 license is in `LICENSE`; implementation notices are in `NOTICE`.

## Verification limits

Manifest isolation checks cover friendly names, database-specific fields, credential separation and the exact shipped SQL profiles. Contract tests cover scope/ref checks, parameter separation, test-mode suppression, output bounds and unknown write outcomes. No live OceanBase credentials were supplied; compile and contract evidence does not establish a successful authenticated database connection.

## Automated CI and releases

Pushes to `main` and pull requests run the shared extension build workflow. The checked-in `.github/release-config.json` selects both Linux targets, the repository's package script and test inputs. Missing native payloads and published-only inventory are restored from checksum-pinned release archives; tracked source files are preserved. The source packager retains its provenance checks.

After the versioned release commit is on `main`, publish by pushing its version tag:

```sh
git tag v1.3.6
git push origin v1.3.6
```

The release workflow runs the shared checks, builds the target archives and publishes the GitHub release and checksums. Do not move an existing tag. To rerun a release for an existing tag, dispatch the same workflow:

```sh
gh workflow run release.yml --repo Flow-Steward/ext-data-oceanbase --ref main -f tag=v1.3.6
```

The manifest, descriptor (when present), package version and tag must identify the same release. Release publication uses the workflow token; no additional repository secret is required by these callers.

### Standalone CI coverage

The release recipe lists the standalone test files and individual test nodes explicitly, including package, source and provenance contracts. The shared runner clears repository pytest addopts so packaged contract checks are not silently deselected. This scope does not claim live provider or database verification.

The following integration coverage requires a separate environment and is not part of standalone CI:

- `tests/test_packaged_toolbox_postgres_integration.py`: Creates and queries a disposable external PostgreSQL database using FS_TOOLBOX_INTEGRATION_DSN/FS_DB_DSN.
- `tests/test_projected_dataset_postgres_e2e.py`: Creates and queries a disposable external PostgreSQL database using FS_TOOLBOX_INTEGRATION_DSN/FS_DB_DSN.
