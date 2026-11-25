# OpenGaussConnector

`OpenGaussConnector` is the managed .NET data provider for [openGauss](https://www.opengauss.org), the
open-source relational database. It implements the ADO.NET provider model — connections, commands, data
readers, transactions, batches, data sources and a connection string builder — and ships the plugin
packages the upstream driver is known for.

The provider is a port of the openGauss ADO.NET driver (snapshot `ba5e8ba`, 2023-11-07) onto a new package
identity and the modern .NET target set. All public ADO.NET type names are preserved
(`OpenGaussConnection`, `OpenGaussCommand`, `OpenGaussDataReader`, `OpenGaussParameter`,
`OpenGaussConnectionStringBuilder`, `OpenGaussFactory`, `PostgresException`, …) and live in the
`OpenGaussConnector` namespace.

## Status

Version `0.1.0` is a pre-release used for the first milestone: the core provider, the data source and
dependency injection integration, the five extension packages and the migrated test suites all build,
and the offline test entry passes. Nothing has been published to NuGet yet, and no package has been run
against a live server in this repository's history — see the [development progress](docs/opengauss-connector-progress.md)
document for what has and has not been verified.

## Packages

Every package is built for `netstandard2.0`, `netstandard2.1`, `net8.0`, `net9.0` and `net10.0`.

| Package | Purpose |
| --- | --- |
| `OpenGaussConnector` | The ADO.NET provider: connections, commands, readers, transactions, batches, data sources |
| `OpenGaussConnector.DependencyInjection` | `IServiceCollection` integration (`AddOpenGaussConnection`, `AddOpenGaussDataSource`, keyed data sources) |
| `OpenGaussConnector.GeoJSON` | PostGIS `geometry`/`geography` mapped to GeoJSON.NET types |
| `OpenGaussConnector.Json.NET` | `json`/`jsonb` serialized with Newtonsoft.Json |
| `OpenGaussConnector.NetTopologySuite` | PostGIS `geometry`/`geography` mapped to NetTopologySuite types |
| `OpenGaussConnector.NodaTime` | Date and time types mapped to NodaTime types |
| `OpenGaussConnector.OpenTelemetry` | Tracing for commands through the provider's `ActivitySource` |

## Quickstart

```csharp
using OpenGaussConnector;

var connectionString = "Host=myserver;Port=5432;Database=mydb;Username=myuser;Password=mypass";

await using var connection = new OpenGaussConnection(connectionString);
await connection.OpenAsync();

await using var command = new OpenGaussCommand("SELECT name FROM cities WHERE population > @min", connection);
command.Parameters.Add(new OpenGaussParameter("min", 100000));

await using var reader = await command.ExecuteReaderAsync();
while (await reader.ReadAsync())
{
    Console.WriteLine(reader.GetString(0));
}
```

An `OpenGaussDataSource` can replace the process-wide pool on .NET 8 and later: it owns its own pool and
hands out closed connections whose connection string cannot change.

```csharp
await using var dataSource = new OpenGaussDataSourceBuilder(connectionString).Build();
await using var connection = await dataSource.OpenConnectionAsync();
```

Dependency injection:

```csharp
services.AddOpenGaussDataSource(connectionString); // singleton data source, .NET 8+
services.AddOpenGaussConnection(connectionString); // transient connections, all targets
```

Extensions are registered on the type mapper at startup:

```csharp
OpenGaussConnection.GlobalTypeMapper
    .UseNodaTime()
    .UseGeoJson()
    .UseNetTopologySuite()
    .UseJsonNet();

services.AddOpenTelemetry().WithTracing(builder => builder.AddOpenGauss());
```

## Building

The repository uses the .NET SDK installed on the machine (no `global.json`), central package management
and a `.slnx` solution.

```powershell
dotnet build OpenGaussConnector.slnx -c Release
./eng/Test-Offline.ps1        # tests that need no server
./eng/Verify-Packages.ps1     # packs the seven packages, inspects them and consumes them
./eng/Verify-UpstreamFidelity.ps1   # compares the source tree with the pinned upstream snapshot
```

Tests that need a server read the connection string from `OPENGAUSS_TEST_DB` (`NPGSQL_TEST_DB` is still
accepted as a fallback):

```powershell
$env:OPENGAUSS_TEST_DB = 'Host=127.0.0.1;Port=15432;Username=gaussdb;Password=...;Database=postgres'
dotnet test tests/OpenGaussConnector.Tests -c Release
```

## Continuous integration

[`.github/workflows/ci-cd.yml`](.github/workflows/ci-cd.yml) runs on Windows and Linux:

| Trigger | What runs |
| --- | --- |
| Pull request to `master` | Restore, build, and the offline tests on both operating systems |
| Push to `master` | The same, plus pack, inspect and consume the seven packages from `eng/Verify-Packages.ps1` |
| Push a tag `v0.1.0` or `0.1.0` | The same, plus publish the packages to NuGet and create the GitHub release |

`<Version>` in `Directory.Build.props` is the only version source, and a tag that disagrees with it fails the
run before anything is packed. Publishing uses NuGet trusted publishing: the workflow exchanges a GitHub OIDC
token for a short-lived key, so no long-lived API key is stored, and the repository variable `NUGET_USER`
holds the nuget.org profile name.

Tests that need a live server are not part of the pipeline because the runners have no openGauss instance;
run them locally with `OPENGAUSS_TEST_DB` as shown above.

## Documentation

Start at [docs/README.md](docs/README.md). The [driver design](docs/opengauss-connector-design.md) explains
the porting strategy and the acceptance criteria; the [feature matrix](docs/opengauss-connector-feature-matrix.md)
tracks each capability against JDBC and server evidence; the [development progress](docs/opengauss-connector-progress.md)
document records what is done, what is pending and how verification results are logged.

## License

Mulan Permissive Software License v2 (Mulan PSL v2). See [LICENSE](LICENSE). The provider is derived from
the openGauss ADO.NET driver, which is distributed under the same license.
