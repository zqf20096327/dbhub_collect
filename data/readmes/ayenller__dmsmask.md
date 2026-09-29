# dmsmask

Full-load migration from **MySQL HeatWave to TiDB with column masking**, using
AWS DMS native Data Masking.

Masking happens inside DMS while the rows are in flight. The source database is
never modified — no masked views, no `ALTER`, no type coercion — and the
plaintext never lands on disk or in a log.

**Which columns get masked is declared by you in `masking.yaml`. Nothing is
inferred.** The tool's job is different: to refuse to let a declared choice fail
silently, then generate every configuration file, run the migration, and prove
the result.

---

## Quick start

```bash
./setup.sh                        # create .venv and install dependencies (once)
cp config.example.yaml config.yaml
$EDITOR config.yaml               # ARNs, endpoints, credentials

./migrate.py scaffold             # list every column, annotated with legal actions
$EDITOR masking.yaml              # change `keep` to `hash` on the columns you want masked

./migrate.py all                  # generate → preflight → apply-ddl → run → verify
```

`masking.yaml` is the only place that needs human input.

---

## Two routes

Set `route:` in `config.yaml`.

### `direct` — DMS writes straight into TiDB

```
HeatWave ──▶ AWS DMS ──▶ TiDB
              masking
```

Fewer moving parts, one fewer place for data to sit. Best when DMS and TiDB are
in the same region and the dataset is small enough that row-by-row `INSERT`
throughput is not a concern.

### `s3` — DMS writes Parquet to S3, TiDB imports from there

```
HeatWave ──▶ AWS DMS ──▶ S3 ──▶ TiDB
              masking       (IMPORT INTO)
```

Preferred across regions, and whenever you need evidence.

| | `direct` | `s3` |
|---|---|---|
| Cross-region throughput | Row-by-row `INSERT`, slow | Bulk physical import, **much faster** |
| Re-running after a failure | Whole task restarts | Files persist; re-run only the import |
| **Proving the masking worked** | Only once it is in the database | **Before it reaches the database** — inspect the Parquet files |
| Moving parts | Fewer | One extra hop, plus bucket policy and lifecycle rules to get right |
| TiDB Cloud tier | Any | Starter/Essential support S3 import; the Role ARN must be registered in the console first |

The S3 route's decisive advantage is the file-level checkpoint. Because
`hash-mask` output is reproducible (see [Verification](#verification)), every
masked value can be compared against the source *before* anything is loaded —
evidence that survives an audit, not just a "looks like a hash" spot check.

Step-by-step guides:

- **[S3-ROUTE.md](S3-ROUTE.md)** — the S3 route using this tool
- **[S3-ROUTE-MANUAL.md](S3-ROUTE-MANUAL.md)** — the same route by hand, with no
  tooling beyond the `aws` CLI and a MySQL client

---

## Declaring what to mask

```bash
./migrate.py scaffold
```

Every line of the generated `masking.yaml` states the column's DMS internal type
and **exactly which actions that type accepts**, so the choice can be made
without cross-referencing the AWS documentation:

```yaml
columns:
  # ===== customers =====
  customers.id: keep          # bigint unsigned -> UINT8    class B | allowed: digits-randomize
  customers.field_01: keep    # varchar(191)    -> WSTRING  class A | allowed: hash, digits-mask, digits-randomize
  customers.field_05: keep    # date            -> DATE     class C | allowed: none (drop only)
  customers.properties: keep  # json            -> CLOB     class C | allowed: none (drop only)
```

Change the ones you want masked. Anything left at `keep`, or omitted entirely, is
migrated as-is.

```yaml
columns:
  customers.field_01: hash    # full name
  customers.field_02: hash    # email
  customers.properties: drop  # json cannot be masked
  users.email: hash
  users.password: hash
```

### Actions

| Action | Meaning |
|---|---|
| `hash` | SHA256, 64 uppercase hex characters. **Deterministic** — equal inputs stay equal, so joins and unique keys survive |
| `digits-mask` | Every digit becomes a fixed character. Length unchanged |
| `digits-randomize` | Every digit becomes a random digit. Length and format unchanged, so the value stays plausible — **weak masking** |
| `drop` | Column excluded from the migration; the target table has no such column |
| `keep` | Migrated as-is, in plaintext |

---

## Validation

`./migrate.py check` — and the first step of `all` — validates the spec against
the real schema and **reports every problem at once** rather than one per run:

```
FAIL users.password: unknown action 'obfuscate'. Valid actions: digits-mask,
     digits-randomize, drop, hash, keep
FAIL users.account_ids: `hash` is not possible. DMS maps json to its internal
     type CLOB (class C), which no masking action supports.
     Options: set it to `drop` to exclude the column, or ALTER the source column
     to TEXT/VARCHAR first, which makes it class A and fully maskable.
FAIL users.id: `hash` is not possible. DMS maps bigint unsigned to its internal
     type UINT8 (class B), which only supports: digits-randomize.
     Note that digits-randomize preserves length and format, so it is weak masking.
FAIL users.nonexistent: column `nonexistent` does not exist in `users`
```

This layer exists to catch the class of mistake DMS would **accept and then
silently ignore**.

### Type admission

Whether a column can be masked depends on the type DMS maps it to internally, not
on the MySQL type name:

| Class | DMS internal type | Available actions |
|---|---|---|
| **A** | `WSTRING` / `STRING` | all three, including `hash` |
| **B** | `NUMERIC` / `INT1-8` / `UINT1-8` | `digits-randomize` only |
| **C** | `CLOB` / `NCLOB` / `BLOB` / `BYTES` / `DATE` / `DATETIME` / `REAL4` / `REAL8` / `BOOLEAN` | **none** |

> The easiest trap to fall into: `TEXT` maps to `WSTRING` (**maskable**) while
> `MEDIUMTEXT` and `LONGTEXT` map to `NCLOB` (**not maskable**). Same family,
> opposite behaviour. The tool checks the exact type of every column rather than
> asking whether something "looks like a text field".

A sensitive class C column has two options only: `drop` it, or `ALTER` the source
column to `TEXT` first so that it becomes class A.

### Cross-table consistency (warnings, not errors)

Two problems that are invisible in a single table and obvious across a schema:

- **The same column name masked in one table and left in plaintext in another.**
  If both hold the same data, the plaintext copies defeat the masking.
- **A foreign key masked on only one side.** `hash` is deterministic, so joins do
  survive masking — but only when both sides get the same action.

Both are reported with the affected tables listed. They are warnings, because the
spec may well be intentional.

---

## Commands

| Command | What it does |
|---|---|
| `scaffold` | Write `masking.yaml` listing every column with its type, class and legal actions. `--maskable-only` lists only columns DMS can actually mask |
| `check` | Validate `masking.yaml` against the schema |
| `generate` | Render the DMS mapping and task settings, the TiDB DDL, the verification SQL and the spec report |
| `preflight` | Check AWS identity, DMS engine version, endpoint connectivity, source type drift, target readiness |
| `apply-ddl` | Create the target tables on TiDB (DMS never creates secondary indexes) |
| `run` | Create and start the DMS task, then follow it to completion |
| `verify` | Table statistics, row-count reconciliation, plaintext residue scan |
| `rehearse` | Local dry run with **no AWS involved**: copies source to target applying the same masking semantics, to validate the spec and the DDL |
| `all` | generate → preflight → apply-ddl → run → verify |

### Generated artefacts

```
generated/
  table-mapping.json       DMS selection + transformation rules
  task-settings.json       DMS replication task settings
  tidb-schema.sql          target DDL
  verify.sql               reconciliation and residue queries
  spec-report.md           every column action, LOB inventory, warnings — for sign-off

# route: s3 only
  stage-to-tidb-naming.sh  rename DMS output to the {db}.{table} form TiDB resolves by
  import-into.sql          IMPORT INTO statements pointing at the staged prefix
```

---

## What the target DDL changes

`tidb-schema.sql` is not a copy of the source DDL:

- **Hashed columns are widened to `CHAR(64)`.** A source `varchar(50)` copied
  verbatim would silently truncate the SHA256 and produce wrong data with no error.
- **`utf8mb4_0900_ai_ci` is remapped to `utf8mb4_bin`** — TiDB does not support
  the former. Sorting and comparison semantics change, so the report names every
  affected table.
- **Dropped columns are removed along with any index that referenced them**;
  composite indexes lose just that column.
- **Foreign keys are omitted by default.** A parallel full load does not load
  parents before children. Re-add them afterwards if the application needs them.
- **HeatWave's `RAPID_COLUMN=...` column comments are stripped.**
- **`FULLTEXT` and `SPATIAL` indexes are omitted** (unsupported in TiDB) and
  listed in the report.
- Nullability is always written out explicitly: `TIMESTAMP NULL DEFAULT NULL` and
  `TIMESTAMP DEFAULT NULL` do not mean the same thing under every setting of
  `explicit_defaults_for_timestamp`.

---

## Safety constraints

| Constraint | Why |
|---|---|
| DMS engine version **≥ 3.5.4**, preflight aborts otherwise | **Below this version the masking rules are accepted and then ignored** — plaintext reaches the target with no error anywhere. The only silent failure mode in the whole pipeline |
| `DataMaskingErrorPolicy = STOP_TASK` | Other policies skip the offending row, which means the unmasked original lands on the target |
| Log severity never above `LOGGER_SEVERITY_DEFAULT` | `DETAILED_DEBUG` writes row values into CloudWatch — plaintext PII into logs |
| `schema-name` is never `%` | A wildcard pulls in `mysql` and `sys` and fails the task |
| Target tables must be empty | A full load into a non-empty table produces duplicates or primary key conflicts |
| Source type drift aborts the run | The schema file is a snapshot. If `phone` is really a `BIGINT`, full masking silently degrades to weak masking |
| AWS identity must own the configured ARNs | A cross-account ARN otherwise surfaces as `Invalid value <arn>`, which reads like a malformed ARN rather than the permission problem it is |

---

## Verification

Three independent signals, because none is sufficient alone:

1. **DMS table statistics** — catches a table left `SUSPENDED` while the task as a
   whole still reported success.
2. **Row counts** — catches missing rows, against a baseline recorded before the
   task started (the source may keep writing during a full load).
3. **Plaintext residue scan** — catches masking that never happened, which the
   first two would both report as fine.

`verify` exits non-zero if any of them fails, and `all` stops there.

### Exact-value verification

DMS `hash-mask` is equivalent to **`UPPER(SHA2(value, 256))` over the UTF-8
bytes** — confirmed empirically, including for non-ASCII input. So the expected
value of every masked cell can be computed from the source:

```python
want = hashlib.sha256(source_value.encode("utf-8")).hexdigest().upper()
assert want == masked_value
```

That is a stronger claim than "the format looks right": every value is provably
correct. On the S3 route this can be done against the Parquet files before
anything reaches the database.

Two invariants worth checking alongside it:

- **Determinism** — two source rows holding the same value must still hold the
  same value after masking.
- **Cardinality** — `hash` is injective, so `COUNT(DISTINCT col)` must match the
  source. A unique key with an unchanged distinct count is proof the constraint
  survived.

---

## Connections and credentials

`source` and `target` each take an `ssl_mode`, matching the mysql client flag:
`disabled` | `required` | `verify-ca` | `verify-identity`. HeatWave normally needs
`verify-identity` with `ssl_ca` pointing at its CA bundle.

Keep passwords out of the config file:

```bash
export DMSMASK_SOURCE_USER=... DMSMASK_SOURCE_PASSWORD=...
export DMSMASK_TARGET_USER=... DMSMASK_TARGET_PASSWORD=...
```

When the DMS resources live in a different AWS account than your default profile,
set `aws.profile`. Preflight verifies that the active credentials actually own the
configured ARNs before anything else runs.

`config.yaml` is gitignored; `config.example.yaml` contains no secrets.

---

## Limitations

- **Full load only, no CDC.** The source should be quiesced during the load, or
  the row-count baseline taken at start time treated as the reference.
- **Class B columns can only be weakly masked.** A phone number stored as `BIGINT`
  keeps its digit count and format under `digits-randomize` — the result is still
  a plausible phone number. Full masking requires changing the source column to
  `VARCHAR`/`TEXT`.
- **Class C columns cannot be masked at all** — drop them, or change the source
  column type.
- `rehearse` approximates `digits-mask` and `digits-randomize`; its `hash` output
  is byte-identical to what DMS produces.
- The tool does not create DMS replication instances or endpoints, and does not
  configure networking (PrivateLink, VPC endpoints, IP allowlists).

---

## Validation status

`tests/` (29 cases, `./.venv/bin/python -m pytest tests/ -q`) covers type
admission, DDL parsing, spec validation and its error messages, LOB policy,
consistency warnings, DDL generation, task settings, the S3 staging script, the
scaffold, and TLS mode parsing.

Beyond the unit tests, the pipeline has been exercised end to end:

- A real 130-table / 1283-column schema parses completely; column counts match the
  generated target DDL table for table.
- All 262 generated DDL statements execute on TiDB v8.5.3 and on MySQL 8.0.44.
- Both routes ran against live AWS DMS. On the S3 route, 155 masked values were
  compared cell by cell against `UPPER(SHA2(source, 256))` with zero mismatches.
- Injecting plaintext residue and a row-count shortfall each made `verify` fail
  with a non-zero exit code.

---

## License

MIT — see [LICENSE](LICENSE).
