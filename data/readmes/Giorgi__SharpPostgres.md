# SharpPostgres

A proof-of-concept toolkit for building PostgreSQL extensions in C# with Native AOT - no C shim, just `[UnmanagedCallersOnly]` exports that Postgres loads as a C extension, and `DirectPInvoke` for callbacks into the running backend.

```csharp
[PgFunction("cs_add_one_int4", SqlName = "cs_add_one", Volatility = PgVolatility.Immutable)]
public static int CsAddOne(int x) => checked(x + 1);
```

The source generator turns that into the matching `pg_finfo_*` + wrapper pair - a small generated function that decodes PG's `FunctionCallInfo` arguments, forwards to the C# method, and encodes the return value as a Datum. The generator also derives STRICTness from C# nullable annotations and emits the `CREATE FUNCTION` SQL. Writing a new function is one method with one attribute.

## Status

Experimental. The foundation is solid (114 integration tests pass against `postgres:18`), but several pieces remain:

- No `PG_TRY` / `PG_CATCH` interop. Error reporting itself works correctly: NOTICE / WARNING / ERROR with proper SQLSTATE all flow to the client, and the connection stays healthy after an ERROR (PG aborts the statement, cleans up its memory contexts, returns the error). What doesn't run is C# `finally` / `Dispose` - PG's `siglongjmp` skips over the managed stack frames. Workaround: don't hold external resources (HttpClient, FileStream, etc.) across calls that might raise.
- Limited type catalog (no arrays, `bytea`, `timestamptz`, `interval`, custom types).
- Limited toolkit coverage (no aggregates, triggers, hooks, GUCs, SPI, background workers).

## Motivation

I wanted to see how far .NET 10 Native AOT could go for building Postgres extensions, which are usually written in C or Rust. The project is a result of that exploration: how much of the pgrx-equivalent surface can you build with `[UnmanagedCallersOnly]`, `DirectPInvoke`, and a Roslyn source generator?

## Example: a JSON Schema validator extension

`SharpPostgres.JsonSchemaCheck` is the real-life example. Two SQL functions backed by `JsonSchema.Net`, with an internal cache so each schema literal is parsed once per backend.

```csharp
using SharpPostgres;

[assembly: PgExtension("0.1.0",
    Comment = "JSON Schema validation for Postgres, written in C# (Native AOT)")]

namespace SharpPostgres.JsonSchemaCheck;

public static partial class Exports
{
    [PgFunction("json_schema_check", Volatility = PgVolatility.Immutable)]
    public static bool JsonSchemaCheck(string schemaText, string instanceText) =>
        JsonSchemaValidation.Matches(schemaText, instanceText);

    [PgFunction("jsonb_schema_check", Volatility = PgVolatility.Immutable)]
    public static bool JsonbSchemaCheck(string schemaText, [PgJsonb] string instanceText) =>
        JsonSchemaValidation.Matches(schemaText, instanceText);
}
```

That's the whole extension's surface. The source generator emits:

- `Pg_magic_func` + `_PG_init` ABI exports
- `pg_finfo_json_schema_check` + `json_schema_check` wrappers
- `pg_finfo_jsonb_schema_check` + `jsonb_schema_check` wrappers
- `json_schema_check.control` (PG's extension control file)
- `json_schema_check--0.1.0.sql` (CREATE FUNCTION DDL)

Use it from SQL:

```sql
CREATE EXTENSION json_schema_check;
SELECT json_schema_check('{"type":"number"}', '42');                      -- true
SELECT jsonb_schema_check('{"type":"string"}', '"hello"'::jsonb);         -- true
```

For a wider tour of toolkit features - scalar SRFs, composite SRFs with several projection shapes, error reporting, `[PgRawDatum]` Datum-passthrough, collation forwarding, materialize-mode SETOFs - see `SharpPostgres.Demos/`. Its functions are deliberately small and synthetic (a `cs_split_text`, a `cs_generate_series`, a `cs_type_kitchen` that returns rows of every supported scalar type, etc.); the goal is breadth of coverage rather than realism. The integration test suite drives that extension end-to-end.

## Project layout

| Project | Purpose |
|---|---|
| `SharpPostgres.Toolkit` | Runtime library: ABI structs, P/Invokes against the PG backend, `SrfBuilder`/`SrfDescriptor`, `PostgresJsonb` (binary jsonb walker), `PostgresText` helpers, `PostgresError` (ereport wrapper). Pure library; AOT-compatible. |
| `SharpPostgres.SourceGenerator` | Roslyn analyzer. Emits wrappers + SQL DDL from `[PgFunction]`, `[PgSrf]`, `[PgCompositeSrf]`, `[PgExtension]` attributes. Targets `netstandard2.0` (Roslyn requirement). |
| `SharpPostgres.SchemaWriter` | Console helper. Reads the `GeneratedSchema` constants from a built extension assembly via `MetadataLoadContext` and writes `.control` + versioned `.sql` files to the project's `extension/` folder. Invoked from each extension's MSBuild `EmitSchema` target. |
| `SharpPostgres.Demos` | Synthetic sample extension. ~30 functions covering scalar UDFs, scalar SETOFs, composite SETOFs, error reporting, every projection shape. Exercised by the integration tests. |
| `SharpPostgres.JsonSchemaCheck` | Real-life example: JSON Schema validation. References `JsonSchema.Net`. Standalone extension `json_schema_check`. |
| `SharpPostgres.Benchmarks` | BenchmarkDotNet comparison between `jsonb_schema_check` and `pg_jsonschema`'s `jsonb_matches_compiled_schema`. |
| `SharpPostgres.IntegrationTests` | TUnit + Testcontainers. Spins up `postgres:18`, mounts both extensions' `.so` + `.control` + `.sql`, runs 114 tests across both. |

## Supported features

What the toolkit + generator handle today:

**Attributes**

- `[PgFunction]` - scalar UDFs (in: scalar types; out: scalar)
- `[PgSrf]` - Set-Returning Functions returning `IEnumerable<T>` for T in supported scalar types (including nullable variants `IEnumerable<T?>` / `IEnumerable<string?>`)
- `[PgCompositeSrf]` - SRFs returning composite records via `SrfBuilder.Define(...).Project(...)`
- `[PgExtension]` - assembly-level marker; gates module-level exports + drives SQL DDL emission

**Parameter and column types**

- `short`, `int`, `long`, `bool`, `float`, `double`, `decimal`
- `string` (text), `string` + `[PgJsonb]` (jsonb)
- `Guid` (uuid), `DateTime` (timestamp)
- Nullable variants for all of the above
- `[PgCollation] uint` - receive the COLLATE Oid (not a SQL arg slot)
- `[PgRawDatum("text")] nuint` / `[return: PgRawDatum("...")]` - raw Datum passthrough for zero-allocation forwarding to PG built-ins

**Generated code per extension**

- PG calling-convention wrappers (`pg_finfo_X` + `X`)
- `Pg_magic_func` + `_PG_init` (gated on `[assembly: PgExtension]`)
- `[ModuleInitializer]` wiring for composite SRF descriptors
- `CREATE FUNCTION` DDL with auto-derived signatures
- `<extension>.control` file
- Auto-snake_case for SQL parameter names; `[PgArgName("override")]` for explicit names
- STRICT derived from C# parameter nullability (any `T?` → non-STRICT)
- Volatility from `Volatility = PgVolatility.Immutable | Stable | Volatile` (default Volatile)

**Error reporting**

- `PostgresError.RaiseWarning(msg)`, `RaiseError(msg)`, `RaiseMessage(severity, msg, detail, hint, sqlstate, source)` - wrap PG's `errstart` / `errcode` / `errmsg_internal` / `errfinish` plumbing
- NOTICE / WARNING messages flow to the client via the standard protocol channel (visible in psql, Npgsql's `Notice` event, etc.)
- `ERROR` triggers PG's `siglongjmp` out of the C# stack, aborts the statement, and returns the error to the client with the SQLSTATE you supplied
- The connection stays healthy after an `ERROR` - subsequent queries on the same connection work normally. Integration tests verify this end-to-end: fire an ERROR mid-statement, run another query, check the result
- Caveat (see [Status](#status)): the longjmp skips C# `finally` / `Dispose`, so don't hold external resources across calls that might raise

**Composite SRFs**

- ValuePerCall mode (default) - per-row tuple construction via `heap_form_tuple`
- Materialize mode (`Materialize = true`) - Tuplestore-backed; required for WITH HOLD cursors and other materialize-only contexts
- Projection shapes accepted: anonymous-type init (`r => new { x = r.A }`), inferred names (`r => new { r.A }`), computed columns (`r => new { sum = r.A + r.B }`), constant columns (`r => new { tag = "fixed" }`), single-member access (`r => r.X`)

## Comparison to pgrx

| Feature | SharpPostgres | pgrx |
|---|:-:|:-:|
| Scalar UDFs | yes | yes |
| Set-Returning Functions (scalar + composite) | yes | yes |
| Error reporting via `ereport` | yes | yes |
| Source-generator codegen | yes (Roslyn) | yes (proc-macros) |
| SQL DDL emission (`.sql` + `.control`) | yes | yes |
| `PG_TRY` / `PG_CATCH` (siglongjmp interop) | no | yes |
| SPI (run SQL from extension code) | no | yes |
| Custom types | no | yes |
| Aggregates / triggers / operators | no | yes |
| Hooks framework | no | yes |
| Background workers | no | yes |
| Custom GUCs | no | yes |
| Arrays as parameter / return type | no | yes |


## Benchmarks

[`SharpPostgres.Benchmarks`](SharpPostgres.Benchmarks) compares `jsonb_schema_check` against `pg_jsonschema`'s `jsonb_matches_compiled_schema` (the cached-schema variant; both implementations cache the parsed schema per backend, so this is apples-to-apples).

Representative numbers on PG 18 + recent Windows hardware, 20,000 inserts into a table with a CHECK constraint:

- **Small payload** (`{a: int, b: text}`): pg_jsonschema ~53 ms, json_schema_check ~81 ms - **1.5× slower**

The gap is probably at the **validator library** layer: `JsonSchema.Net` evaluation cost vs `jsonschema-rs` evaluation cost. 

## Build, test, deploy

Requirements: .NET 10 SDK, Docker Desktop (for integration tests; on Windows/macOS it's also used to do cross-OS Linux AOT publishes).

```bash
dotnet build SharpPostgres.slnx -c Release
dotnet run --project SharpPostgres.IntegrationTests -c Release
```

The build target chain publishes both extension `.so` files to `artifacts/linux-x64/` (via Docker on non-Linux hosts, native on Linux). The integration tests bind-mount those `.so` + each extension's `extension/` folder into a `postgres:18` container and run `CREATE EXTENSION`.

To install into your local Windows PG 18:

```powershell
.\deploy.ps1                              # builds + installs json_schema_check
.\deploy.ps1 -Extension Demos             # builds + installs sharppostgres_demos
.\deploy.ps1 -Extension All               # both
```

Requires elevated PowerShell (copies into Program Files, restarts the `postgresql-x64-18` service).

CI runs on `ubuntu-latest` via `.github/workflows/ci.yml` - native publish, no Docker needed for build, Testcontainers handles PG.

## Architecture notes

- **Native AOT, no C shim.** The published `.so` / `.dll` exports the C symbols PG expects from a loaded extension (`pg_finfo_X`, `X`, `Pg_magic_func`, `_PG_init`) directly from C# via `[UnmanagedCallersOnly]`. PG calls in, the wrappers decode args + bridge to managed methods, the toolkit's `DirectPInvoke` against `postgres.exe` (Windows) / undefined-symbol resolution at `dlopen` (Linux) reaches back into the running backend for callbacks (palloc, ereport, jsonb iteration, numeric conversion, tuplestore, etc.).
- **Source generator does the boilerplate.** ABI wrappers, finfo records, module-level exports, SQL DDL - all derived from attributes on user code. User extension code is just methods with attributes.
- **STRICT is derived from C# nullable annotations**, not a separate knob. `int` parameter → STRICT; `int?` → non-STRICT. The single source of truth lives where the developer naturally writes it.

Foundational gaps still open:

- `PG_TRY` / `PG_CATCH` interop - without it, any C# code that holds external resources (HttpClient, FileStream, native handle) across a PG call that might `ereport(ERROR)` will leak on the longjmp. The biggest remaining safety + feature blocker.
- SPI access (run SQL from within an extension) - unblocks the entire class of extensions that look things up in other tables.
- Hooks (executor, planner, ProcessUtility) - unblocks audit / monitoring / planner-extension territory.
