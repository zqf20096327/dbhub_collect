# GaussDB Routine Wrapper Generator

This directory contains an offline generator that reads one `gsql` export result file and emits C# wrappers for GaussDB procedures and functions.

The workflow is:

1. Provision representative routines or point the export at an existing database.
2. Run one `input.sql` with `gsql`.
3. Capture one `output.result`.
4. Run the Python generator.
5. Add the generated `.cs` files to a .NET project and call the wrappers.

## Directory layout

- `sql/routine_scenarios.sql`
  Creates representative procedures, functions, overloads, enums, composites, and fallback cases in schema `routine_codegen`.
- `sql/input.sql`
  Exports all metadata required by the generator in one sectioned result file.
- `samples/output.result`
  Sample metadata export captured from the test database.
- `tool/generate_gaussdb_routines.py`
  Generator entry point.
- `tool/gaussdb_routine_codegen/`
  Parser, metadata model, type mapping, and C# rendering logic.
- `generated/routine_codegen/`
  Example generated output for the sample metadata file.

## Reference documentation

The SQL shapes used here were aligned with the local GaussDB product documentation requested in this change:

- `D:\code\DOCUMENT\云数据库 GaussDB 开发指南（集中式_V2.0-8.x）.pdf`

In practice, the scenario SQL uses the GaussDB Oracle-compatible procedure syntax and standard function syntax that worked against the target database during validation.

## 1. Provision the sample routines

Run:

```powershell
& 'D:\Software\dws_9.1.1_gsql_for_windows\x64\gsql.exe' `
  -d hdx_test `
  -h 120.46.16.223 `
  -U root `
  -p 8000 `
  -W "Gauss_234net," `
  -f 'D:\code\gaussdb-routine-wrapper-generator\sql\routine_scenarios.sql'
```

This resets schema `routine_codegen` and recreates:

- IN-only procedures
- OUT / INOUT procedures
- scalar-returning functions
- table-returning functions
- composite-returning functions
- enum-mapped types
- overloads
- default-parameter ambiguity cases
- unsupported scalar and `record` fallback cases

## 2. Export metadata with one input SQL file

Run:

```powershell
& 'D:\Software\dws_9.1.1_gsql_for_windows\x64\gsql.exe' `
  -d hdx_test `
  -h 120.46.16.223 `
  -U root `
  -p 8000 `
  -W "Gauss_234net," `
  -f 'D:\code\gaussdb-routine-wrapper-generator\sql\input.sql' |
  Set-Content -Encoding UTF8 'D:\code\gaussdb-routine-wrapper-generator\samples\output.result'
```

`input.sql` emits four required sections into one file:

- `@@SECTION|ROUTINES`
- `@@SECTION|TYPES`
- `@@SECTION|COMPOSITE_FIELDS`
- `@@SECTION|ENUM_LABELS`

The generator validates that all four section markers exist. If one is missing, generation fails with a format-contract error instead of silently emitting partial code.

## 3. Generate C# wrappers

Run:

```powershell
python D:\code\gaussdb-routine-wrapper-generator\tool\generate_gaussdb_routines.py `
  --input D:\code\gaussdb-routine-wrapper-generator\samples\output.result `
  --output-dir D:\code\gaussdb-routine-wrapper-generator\generated\routine_codegen `
  --namespace EfScaffoldTest.Generated `
  --schema routine_codegen
```

Generated files:

- `GeneratedGaussDbDtos.cs`
- `GeneratedGaussDbRuntimeHelpers.cs`
- `GeneratedGaussDbRoutines.cs`

### Optional: run through the provided shell script

For Git Bash / WSL / Linux-style shells, you can run the wrapper script directly:

```bash
bash D:/code/gaussdb-routine-wrapper-generator/generate_gaussdb_routines.sh
```

This uses the default paths:

- input: `samples/output.result`
- output: `generated/routine_codegen`
- namespace: `EfScaffoldTest.Generated`
- schema: `routine_codegen`

### Optional: generate only specific routines

By default, the generator emits all routines in the selected schema.

You can also generate only the routines you need.

Generate one specific routine by name:

```powershell
python D:\code\gaussdb-routine-wrapper-generator\tool\generate_gaussdb_routines.py `
  --input D:\code\gaussdb-routine-wrapper-generator\samples\output.result `
  --output-dir D:\code\gaussdb-routine-wrapper-generator\generated\single_routine `
  --namespace EfScaffoldTest.Generated `
  --routine routine_codegen.get_employee_name
```

Generate one specific overload by signature:

```powershell
python D:\code\gaussdb-routine-wrapper-generator\tool\generate_gaussdb_routines.py `
  --input D:\code\gaussdb-routine-wrapper-generator\samples\output.result `
  --output-dir D:\code\gaussdb-routine-wrapper-generator\generated\single_overload `
  --namespace EfScaffoldTest.Generated `
  --routine "routine_codegen.format_employee(numeric, boolean)"
```

Generate from a routine list file:

```powershell
python D:\code\gaussdb-routine-wrapper-generator\tool\generate_gaussdb_routines.py `
  --input D:\code\gaussdb-routine-wrapper-generator\samples\output.result `
  --output-dir D:\code\gaussdb-routine-wrapper-generator\generated\selected_routines `
  --namespace EfScaffoldTest.Generated `
  --routine-list D:\code\gaussdb-routine-wrapper-generator\samples\routine_list.txt
```

The shell script supports the same filters:

```bash
bash D:/code/gaussdb-routine-wrapper-generator/generate_gaussdb_routines.sh \
  --routine routine_codegen.get_employee_name
```

```bash
bash D:/code/gaussdb-routine-wrapper-generator/generate_gaussdb_routines.sh \
  --routine "routine_codegen.format_employee(numeric, boolean)"
```

```bash
bash D:/code/gaussdb-routine-wrapper-generator/generate_gaussdb_routines.sh \
  --routine-list D:/code/gaussdb-routine-wrapper-generator/samples/routine_list.txt
```

Routine selector forms:

- `name`
- `schema.name`
- `name(type1, type2)`
- `schema.name(type1, type2)`

Matching behavior:

- `name` or `schema.name`
  Matches all exported overloads with that name.
- `name(type1, type2)` or `schema.name(type1, type2)`
  Matches one specific overload by input parameter types.

If a selector does not match any exported routine, the generator fails fast with a clear error message.

## 4. Consume the generated code

`EfScaffoldTest10` links the generated files directly:

```xml
<Compile Include="..\gaussdb-routine-wrapper-generator\generated\routine_codegen\*.cs"
         Link="Generated\%(Filename)%(Extension)" />
```

That project validates representative wrappers against the real GaussDB database.

Run:

```powershell
dotnet run --project D:\code\EfScaffoldTest10\EfScaffoldTest.csproj --framework net10.0
```

Validated in this change:

- `UpdateEmployeeNameAsync`
- `GetEmployeeNameAsync`
- `AdjustEmployeeBonusAsync`
- `GetEmployeeCompAsync`
- `EmployeeCountAsync`
- `EmployeeNameAsync`
- `GetEmployeeSummaryAsync`
- `ListEmployeesAsync`
- `SumNumbersAsync`
- `EchoPayloadAsync`
- `MakeLocationPointFallbackAsync`
- fallback stubs for ambiguous/defaulted overloads and `record`

## Supported routine categories

The generator currently emits:

- `procedure` with `IN` parameters only
  Uses `ExecuteSqlInterpolatedAsync`.
- `procedure` with `OUT` / `INOUT`
  Uses `DbCommand` plus reader materialization into DTOs.
- scalar-returning `function`
  Uses `ExecuteScalarAsync` with provider-aligned type conversion.
- `RETURNS TABLE`
  Generates row DTOs and list materialization.
- composite-returning `function`
  Generates DTOs from exported composite field metadata.
- enum-backed types
  Generates C# enums with `EnumMember`.

## Fallback behavior

The generator does not silently skip unsupported shapes.

It emits explicit fallback wrappers for:

- unsupported scalar database types
  Example: `point` returns `object?`.
- unsupported `SETOF` row shapes
  Returns `List<Dictionary<string, object?>>`.
- `record` return types
  Emits a stub that throws `NotSupportedException` because offline metadata does not contain a reliable column definition list.
- ambiguous overloads caused by trailing default parameters
  Emits a stub that throws `NotSupportedException` instead of generating a wrapper that will fail at runtime with an overload-resolution error.

## Type mapping notes

The generator includes a curated type map for common GaussDB types used in customer wrappers, including:

- `numeric` -> `decimal`
- `varchar` / `character varying` -> `string`
- `integer` -> `int`
- `bigint` -> `long`
- `boolean` -> `bool`
- `date` -> `DateOnly`
- `timestamp` -> `DateTime`
- `timestamptz` -> `DateTimeOffset`
- `jsonb` -> `string`
- common arrays such as `integer[]`, `numeric[]`, and `text[]`

Custom enums and composite types are resolved from exported type metadata.

## net9 / net10 note

The generated source is intentionally kept to common C# and EF Core APIs so it can be consumed by both `net9` and `net10` projects.

Validation completed in this repository during this change:

- `net10` real compile and database execution in `EfScaffoldTest10`

Not executed in this session:

- `net9` runtime validation against a built GaussDB EF Core provider package

## Known limitations

- `record` return values cannot be made executable from `pg_proc`-style offline metadata alone.
- Some GaussDB-specific object types still fall back to `object?`.
- Ambiguous overloads introduced by default parameters are surfaced explicitly as stubs.
- The generator currently expects the documented `input.sql` format contract and section markers.
