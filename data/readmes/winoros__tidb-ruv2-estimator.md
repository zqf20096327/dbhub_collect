# TiDB RU Estimator

English | [简体中文](README.zh-CN.md)

Estimate new RU consumption for a selected period using statement statistics and system metadata collected through a TiDB SQL connection.

Reports include total RU, a sensitivity range, a time series, SQL Top 20 lists, and contributions by engine, plan shape, and resource group. The default workflow reads system tables. Saved data can be analyzed offline.

## Get started

You need Python 3.11+, uv, and a TiDB account with access to statement summary.

```sh
uv sync --extra mysql
uv run ru-estimator run \
  --host YOUR_TIDB_HOST --port 4000 --user YOUR_SQL_USER \
  --start '2026-10-26T00:00:00+08:00' \
  --end '2026-10-27T00:00:00+08:00'
```

Enter your password when prompted. Open the `report.md` path printed when the run finishes.

The tool uses [bundled RU coefficients](src/tidb_ru_estimator/data/default-ru-coefficients.json). Override them with `--coefficients FILE`. Report language follows your system locale; use `--language en` or `--language zh` to select it explicitly.

See [QUICKSTART](QUICKSTART.md) for connection settings, output files, and offline commands.

## Reports

- RU center estimate and sensitivity range.
- RU time series grouped by summary window.
- RU Top 20 by digest and SQL executions Top 20.
- RU contributions by engine, plan shape, and resource group.
- System information, validation status, and diagnostics.

RU values use two decimal places and thousands separators. JSON retains full precision. Keep the Markdown and SVG files together when moving or sharing a report.

## Estimation scope

The default model covers TiDB/TiKV point reads, scans, common joins, aggregation, sorting, and some window plans. TiFlash and some operators are not yet supported; affected records appear in diagnostics.

Estimates use the historical records collected. If only part of the workload can be modeled, the report shows that subtotal. If no records can be modeled, it provides diagnostics.

## Documentation

| Document | Contents |
| --- | --- |
| [QUICKSTART](QUICKSTART.md) | Installation, commands, options, and output files |
| [Estimation model](sampling/APPROXIMATION.md) | Formulas, assumptions, and validation |
| [Statement filtering](sampling/STATEMENT_EXCLUSIONS.md) | Statement classification and exclusions |
| [Point-read sampling](sampling/README.md) | Sampling and estimation for a selected digest |
| [Batch point reads](sampling/BATCH_POINT.md) | BatchPointGet inputs and estimation |
| [Transactional reads](sampling/STATEFUL_LOOKUP.md) | Get/BatchGet sequences within transactions |

## Development

```sh
uv sync --extra mysql
uv run pytest -q
uv run ruff check src tests
uv run ruff format --check src tests
```
