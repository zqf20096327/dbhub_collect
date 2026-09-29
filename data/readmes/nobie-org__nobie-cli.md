<p align="center">
  <a href="https://nobie.com/cli"><img src="https://nobie.com/favicons/nobie-logo.svg" width="88" alt="Nobie CLI"></a>
</p>

<h1 align="center">Nobie CLI <sup>Beta</sup></h1>

<p align="center">
  <strong>Run any Microsoft Excel workbook from the command line—and get the right answer.</strong>
</p>

<p align="center">
  <a href="https://nobie.com/cli">Documentation</a> ·
  <a href="https://nobie.com/install.sh">Install</a> ·
  <a href="https://github.com/nobie-org/nobie-cli/issues">Issues</a>
</p>

Nobie correctly recalculates every `.xlsx` workbook supported by the Microsoft Excel application. No other third-party spreadsheet engine does. Nobie CLI puts that engine in the terminal.

Other spreadsheet libraries read and write cells. Nobie runs the workbook and returns the answers. A financial model, forecast, pricing tool, or operating plan can run in a shell, CI job, service, or coding agent without the Microsoft Excel application and without being rebuilt in code.

Nobie also reads, edits, renders, and serves `.xlsx` files. Formulas, tables, styles, conditional formatting, charts, and layout stay in the workbook.

## Install

The installer supports macOS and Linux on ARM64 and x86-64:

```sh
curl -fsSL https://nobie.com/install.sh | sh
nobie version
```

The installer asks you to accept the [Nobie Desktop App License Terms](https://nobie.com/desktop-app-license-terms). For a noninteractive install:

```sh
curl -fsSL https://nobie.com/install.sh | sh -s -- --accept-license
```

On macOS this installs `Nobie.app` and the `nobie` command. On Linux it installs the `nobie` binary.

## Quick start

Recalculate an existing workbook and save the result to a new file:

```sh
nobie calc recalc model.xlsx --save-to recalculated.xlsx
```

Or create a workbook and put a small pricing model in it:

```sh
nobie workbook new pricing.xlsx

nobie script run pricing.xlsx --max-tokens 1000 --overwrite <<'NOBIE'
set Sheet1!A1:B1 to {"Unit price", 20}
set Sheet1!A2:B2 to {"Quantity", 3}
set Sheet1!A3:B3 to {"Total", formula "=B1*B2"}
NOBIE
```

Read the result:

```console
$ nobie range read pricing.xlsx Sheet1!A1:B3 --format csv
Unit price,20
Quantity,3
Total,60
```

The script runs as one transaction. If a statement fails, the workbook is left unchanged. Use `--save-to another.xlsx` instead of `--overwrite` to keep the original file.

## Serve a workbook over HTTP

`nobie serve` maps JSON request fields to input cells and output cells back to JSON:

```sh
nobie serve pricing.xlsx \
  --input quote.quantity=Sheet1!B2 \
  --output quote.total=Sheet1!B3
```

```console
$ curl -sS http://127.0.0.1:8000/api/quote \
    -H 'content-type: application/json' \
    -d '{"quantity":5}'
{"total":"100"}
```

The workbook still owns the formula. The HTTP API only supplies inputs and returns results.

## More than cells

Nobie has commands for sheets, ranges, tables, conditional formats, charts, styles, column widths, row heights, frozen panes, and calculation mode. Cell and range reads can return human-readable text, JSON, JSON Lines, XML, CSV, or TSV.

It can also render a range to PNG or print a workbook to PDF:

```sh
nobie range render model.xlsx Summary!A1:H30 --out summary.png
nobie workbook print model.xlsx --out model.pdf
```

For repeated jobs, open the workbook once and use its `@name` handle in later commands. Direct file writes require an explicit choice: `--save-to PATH` keeps the original, while `--overwrite` replaces it.

Run `nobie --help` for the command list and `<command> --help` for details:

```sh
nobie --help
nobie chart create --help
```

## Coding agents

Nobie can describe the command set installed on the machine:

```sh
nobie skill
nobie script skill
nobie script schema --list
```

`nobie skill` includes the command reference. The script schema lists the statements understood by that version of the CLI.

## Repository and license

This repository contains Nobie CLI documentation and [issues](https://github.com/nobie-org/nobie-cli/issues), not the CLI source.

Microsoft and Excel are trademarks of the Microsoft group of companies. Nobie is not affiliated with or endorsed by Microsoft.

Nobie CLI is licensed, not sold. Its use is governed by the [Nobie Desktop App License Terms](https://nobie.com/desktop-app-license-terms).

Copyright © 2026 Nobie, Inc. All rights reserved.
