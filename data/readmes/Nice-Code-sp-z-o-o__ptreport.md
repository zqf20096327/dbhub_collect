<div align="center">

# ptreport

### Free, open-source penetration test report generator

Write findings, collect evidence and export professional PDF reports – on your own machine.<br>
No cloud, no accounts, no licence fees.

[![License: Apache 2.0](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-3776AB.svg?logo=python&logoColor=white)](pyproject.toml)
[![Platform: Linux | macOS](https://img.shields.io/badge/platform-Linux%20%7C%20macOS-555.svg)](#install)
[![CI](https://github.com/Nice-Code-sp-z-o-o/ptreport/actions/workflows/ci.yml/badge.svg)](https://github.com/Nice-Code-sp-z-o-o/ptreport/actions/workflows/ci.yml)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

[Quick start](#quick-start) · [Features](#features) · [Screenshots](#screenshots) ·
[Burp extension](#burp-suite-extension) · [Documentation](#documentation) · [Contributing](#contributing)

![ptreport: CVSS calculator and screenshot editor](docs/media/ptreport-demo.gif)

</div>

## Why ptreport?

- **Free and open source.** Apache 2.0. No seats, no subscriptions, no "community edition" limits.
- **Your data stays with you.** Client findings never leave your machine: one SQLite file, no telemetry, works
  offline. Ideal when contracts or NDAs forbid cloud tools.
- **A report your client can read.** A clean, professional PDF out of the box (LaTeX, English or Polish), with
  your logo and colours – or your own LaTeX template.
- **Built for the way pentesters work.** Send requests straight from **Burp Suite**, import **Nessus, Nmap, ZAP,
  OpenVAS and Burp** scans, score with **CVSS 4.0 / 3.1**, pick a **CWE** from the full MITRE catalogue, reuse
  write-ups from a template library, and run retests.
- **One command to install, one command to run.** Python + a self-contained LaTeX engine; nothing else to set up.

## See it in action

[![Watch the 2-minute demo video](docs/media/demo-poster.png)](docs/media/ptreport-demo.mp4)

A 2-minute walkthrough: findings, CVSS, evidence, the screenshot editor, PDF preview, templates, scanner import
and sending a request from Burp. *All data shown is made up (fictional "Acme" client, `.example` domains).*

## Quick start

```bash
git clone https://github.com/Nice-Code-sp-z-o-o/ptreport.git
cd ptreport
./install.sh      # virtualenv + pinned, hash-checked dependencies + LaTeX engine
ptreport          # opens http://127.0.0.1:5055 in your browser
```

Create a report, add findings (or start from a template / import a scan), click **Preview PDF**. Details:
[Install](#install), [Run](#run).

## Features

**Findings**
- Automatic numbering with your own format (`ACME-001`, `2026/ACME/01` …)
- Clickable **CVSS 4.0 / 3.1 / 3.0 / 2.0** calculator; **CWE** autocomplete over the full MITRE CWE 5.0 catalogue
- Description, impact, technical details, PoC, remediation, references – Markdown-style text with tables
- Nine statuses: *Open, Partially fixed, Not fixed, Fixed, Risk accepted, Won't fix, False positive, Not a bug,
  Cannot verify*; confidence; per-finding history
- **Template library** in English and Polish (12 common vulnerabilities to start with); save your own

**Evidence**
- Raw **HTTP request / response** pairs (pasted, imported or sent from Burp)
- **Code evidence** (decompiled functions, disassembly, source excerpts) and **binary / firmware** targets for
  reverse engineering
- **Screenshots** with a built-in **editor**: crop, arrows, boxes and *irreversible* pixelation of secrets; the
  original is kept
- **Evidence files** of any type (.pcap, .har, logs, scripts …) with a server-side **SHA-256** printed in the
  report, so the client can verify every file

**Reports and export**
- **PDF via LaTeX** (Tectonic, bundled by the installer), live preview in the browser, custom templates, branding
- Standalone **HTML**, **Markdown**, LaTeX sources and a **JSON** backup / restore
- Report structure editor, CWE grouping, wording overrides, version history, **English and Polish** report text
- **Retest reports** with a retest summary; report duplication; private **working notes** per report

**Integrations**
- **Burp Suite extension**: right-click a request → *Send to ptreport* (new or existing finding, CWE, severity)
- **Scanner import**: Burp, Nessus, Nmap, OWASP ZAP, OpenVAS / Greenbone – with a review step
- **CLI** for scripts (`ptreport report list`, `ptreport import-scan`, `ptreport export 3 --format pdf`)
- **JSON API** with a bearer token
- **AI agents** (pentest-ai, Decepticon, reverse-engineering agents …): a built-in **MCP server**
  (`ptreport mcp`), scoped integration tokens and **SARIF / ptai proof capsule** import. Everything an agent sends
  lands in a per-report **AI queue** and reaches the report only when you accept it ([details](docs/integrations.md))
- Optional **AI writing assistant** using a *local* Ollama model (off by default, loopback only)

**Security by design**: binds to 127.0.0.1, CSRF protection, strict CSP, hardened XML parsing (no XXE), uploads never
rendered, LaTeX without shell escape. See [SECURITY.md](SECURITY.md).

## Screenshots

| | |
|---|---|
| ![Report overview with findings, CVSS, CWE, targets and statuses](docs/screenshots/report.png) | ![CVSS 3.1 calculator on a finding](docs/screenshots/cvss-calculator.png) |
| **Report overview**: severity bar, findings with CVSS, CWE, targets and status | **CVSS calculator**: the vector and score update as you click |
| ![HTTP evidence on a finding](docs/screenshots/http-evidence.png) | ![Screenshot editor with box, arrow and pixelated area](docs/screenshots/screenshot-editor.png) |
| **HTTP evidence**: raw requests and responses (from Burp or pasted) | **Screenshot editor**: arrows, boxes, irreversible pixelation, crop |
| ![PDF preview in the browser](docs/screenshots/pdf-preview.png) | ![Template library](docs/screenshots/templates.png) |
| **PDF preview** of the LaTeX report | **Finding templates** in English and Polish |
| ![Scanner import review](docs/screenshots/scan-import.png) | ![Send to ptreport dialog in Burp Suite](docs/screenshots/burp-send-dialog.png) |
| **Scanner import** with a review step | **Burp Suite extension**: send a request to a new or existing finding |

**The generated PDF** – cover, summary of findings, and a finding with evidence and a screenshot:

![Pages of a generated PDF report](docs/screenshots/pdf-pages.png)

## Documentation

[Install](#install) · [Run](#run) · [Writing findings](#writing-findings) ·
[Report structure, CWE groups, wording](#report-structure-cwe-groups-wording) · [PDF and LaTeX templates](#pdf-and-latex-templates) ·
[AI writing assistant](#ai-writing-assistant-local-ollama) · [AI agents](#ai-agents-mcp-sarif-ptai) · [Command line](#command-line) ·
[Burp Suite extension](#burp-suite-extension) · [API](#api-for-the-burp-extension) · [Security model](#security-model) ·
[Development](#development)

## Install

```bash
./install.sh
```

Requires Python 3.10+ and `curl`. On Kali, Debian or Ubuntu you may first need `sudo apt install python3-venv`.
The installer also downloads **Tectonic** (a self-contained LaTeX engine, pinned version with a SHA-256 check)
into `~/.local/share/ptreport/tectonic` and typesets a sample report once, so LaTeX packages are cached and
PDF export then works offline. If Tectonic is not available, ptreport uses `xelatex`/`lualatex` from the system.
The script creates an isolated virtualenv in `~/.local/share/ptreport/venv`, installs pinned,
**hash-verified** dependencies from `requirements.lock`, and links `ptreport` into `~/.local/bin`.

Uninstall with `./install.sh --uninstall`. Your data is kept.

## Run

```bash
ptreport
```

This opens <http://127.0.0.1:5055/> in your browser. Options:

| Option | Description |
|---|---|
| `--port 8080` | Use a different port |
| `--data-dir PATH` | Use a different database/secret location (default `~/.local/share/ptreport/data`; you can also set `PTREPORT_DATA_DIR`) |
| `--no-browser` | Don't open the browser |
| `--show-api-token` | Print the API token for the Burp extension and exit |
| `--host 0.0.0.0 --allow-host my-laptop.lan` | Expose on the LAN. **Not recommended:** there is no login screen |

## Writing findings

- **Finding IDs**: the format is set in **Settings → Finding IDs** as a template: `{prefix}` (the report's
  prefix), `{n}` or `{n:4}` (the number, zero padded), `{year}` (year of testing), e.g. `{prefix}-{n:4}` gives
  `SEC-0002`. You can also set the first number and the default prefix for new reports. A report can override the
  format in its details, and a single finding can have its own ID (e.g. when copying an existing report).
- **Numbering**: a new finding gets the next number. Reorder with ↑/↓, or click
  **Renumber by severity** (Critical first, then by CVSS score). Deleting a finding closes the gap.
- **CVSS**: pick a version and click the metrics, or paste a vector; the version is detected
  automatically. The server computes the score and its CVSS rating (None/Low/Medium/High/Critical).
- **Severity is yours**: it is always set by the tester and never derived from CVSS, so it can reflect context
  (chained issues, compensating controls). Reports show both: your severity and, separately, the CVSS score with
  its rating. An empty severity is pre-filled from the CVSS rating as a suggestion only.
- **Text fields** are plain text with fenced code blocks (```` ``` ````) and `` `inline code` ``.
  Payloads like `<script>` are always shown as text, never executed.
- **Tables**: write a Markdown pipe table in any text field:

  ```
  | Port | Service |
  |------|:-------:|
  | 443  | https   |
  ```

  `:---:` centres a column, `---:` aligns it right, `\|` is a literal pipe inside a cell.
- **Templates** (top menu): search by title, tag or CWE and filter by language. On a new finding pick
  **Start from a template**; it fills the form and nothing is saved until you create the finding. **Save as
  template** on a finding copies its saved write-up (no targets, evidence or screenshots) into the library, in the
  report's language. The starter set is installed once; templates you delete stay deleted.
- **Scanner import** (report → **Import scan**): upload the file (format detected automatically, informational
  issues left out unless you tick them), review the findings and targets found, tick what to keep. Targets that
  are already in the report (same address) are reused; imported findings start as "Open" with a history entry
  naming the scanner. XML is parsed with entity declarations rejected (no XXE, no entity expansion).
- **Screenshot editor** (finding → Screenshots → **Edit**): pick a tool in the toolbar and drag on the image.
  **Arrow** and **Box** use one of four colours (red, accent, yellow, white) and an S/M/L stroke; **Pixelate**
  replaces the region with large flat blocks (the hidden text cannot be recovered from the saved image — use it for
  tokens, cookies and personal data); **Crop** selects a rectangle, **Apply crop** (or Enter) cuts it. Undo/redo
  with the buttons or Ctrl+Z / Ctrl+Shift+Z (Ctrl+Y); A / B / P / C switch tools; Esc or Cancel closes without
  saving. **Save** uploads the result as a PNG (JPEG if a PNG would exceed 10 MB); the server checks it is a real
  PNG/JPEG within the upload limit and no larger than the original. The thumbnail then shows **Edited**, an
  *original* link and **Restore original**, which brings the upload back and discards the edit. Exports
  (HTML/Markdown/PDF) show the edited image; the original stays in ptreport, in JSON backups and in duplicated or
  retest reports (it is **not** gone from ptreport — delete the screenshot to remove both).
- **Retest**: on a report, **Create retest report** copies targets, findings (with evidence, screenshots and files),
  structure and CWE texts into a new report linked to the original, with a **Retest summary** section first. Set
  *Retest result* (fixed / partially fixed / not fixed / not tested), date and notes on each finding; a change is
  logged in its history. **Duplicate report** makes an independent copy.
- **Files** (evidence of any type): on a saved finding, **Files → Add files** takes one or more files (or drop
  them on the form) with an optional description. Limits: 25 MB per file, 100 MB and 50 files per finding, no empty
  files. The name is cleaned (directories, control and right-to-left characters, characters Windows does not allow,
  leading dots removed; at most 180 characters). The MIME type comes from the extension via a fixed table, never
  from the browser. Each row shows the size, the first 12 characters of the SHA-256 (full value on hover, copy
  button), the upload time and an editable description. **Download** always saves the file (`Content-Disposition:
  attachment`, `nosniff`, sandbox CSP); HTML, SVG, XML, JavaScript, PDF and other types that a browser could render
  are sent as `application/octet-stream`. The response carries `Repr-Digest: sha-256=...` too. Reports list the
  files (name, size, full SHA-256) after the HTTP evidence; the bytes themselves stay out of HTML/Markdown/PDF and
  travel in the JSON export (base64, with the SHA-256, verified on import: a mismatch rejects the import). Duplicate
  and retest copies keep the files.
- **PDF**: **Preview PDF** opens the PDF typeset from the LaTeX template; Export → PDF downloads it.

## Report structure, CWE groups, wording

- **Report → Report structure** sets the order, titles, level (section/subsection), numbering and page breaks of
  the sections, and lets you add text sections (e.g. "Future directions", an appendix), charts (findings by
  severity, per target, CVSS versus severity) and tables of findings. Built-in sections can be switched off.
- Text fields support `## Heading`, `### Subheading`, `- list items`, `**bold**`, `` `code` ``, fenced code
  blocks and links; headings become numbered subsections in the PDF.
- **Group findings by CWE** (report details) lays out the findings section per CWE: a description of the
  weakness, its findings, then one mitigation for the group (findings without a CWE form the last group).
- **CWE library** (Settings): the full MITRE CWE catalogue (names, descriptions, potential mitigations) is built
  in, works offline and is refreshed with `scripts/update_cwe.py`. Write your own description and mitigation per
  CWE; reports grouped by CWE use, in this order: the report's own text, your library entry, MITRE's text (can be
  switched off). CWE data is (c) MITRE, terms in `src/ptreport/data/CWE-LICENSE.txt`.
- **Report language** is chosen when a report is created (English or Polish headings); Settings sets the default.
- **Settings → Report wording** renames severities, statuses and headings per language (e.g. "New" instead of
  "Open").
- **Preview PDF** shows the real PDF typeset from the LaTeX template.

## PDF and LaTeX templates

**Export → PDF (LaTeX)** typesets the report with the active template; **Export → LaTeX sources** gives a
zip with `report.tex` and its assets to tweak and compile yourself (`tectonic report.tex`).

The default template ("Corporate Band") has a cover with a band in your brand colour and your logo, a
confidentiality label on the cover and in every footer, a severity bar chart, zebra tables, a card per finding
and framed HTTP request/response blocks. **Settings → Branding** sets the colour and the logo; the
confidentiality label (e.g. `TLP:AMBER`) is a field of each report. The template starts with an
`EDIT HERE` block (colour, fonts, logo, label, severity colours), so a downloaded copy is easy to rebrand.

Templates are Jinja with LaTeX-friendly delimiters: `\VAR{report.title}` prints a value and
`\BLOCK{for f in findings} ... \BLOCK{endfor}` controls the flow; lines starting with `%#` are template
comments. Everything printed with `\VAR` is **escaped for LaTeX automatically**, so report content can
never inject LaTeX commands, also in custom templates. Raw HTTP messages and code blocks are written to
files and loaded with `\VerbatimInput`, so they are never parsed as TeX. Templates run in Jinja's sandbox,
and LaTeX always runs without shell escape. In **Settings → PDF template** you can download the default,
upload your own (it is test-rendered before saving) and switch back to the default.

## AI writing assistant (local Ollama)

Optional and **off by default**. It talks only to an [Ollama](https://ollama.com) server on this machine.

1. Install Ollama and a small model, e.g. `ollama pull qwen2.5:3b` (3–8B models are fine on a laptop GPU).
2. **Settings → AI assistant**: tick *Enable*, keep the URL `http://127.0.0.1:11434`, click **Load models**, pick
   one, click **Test connection**, then **Save**.
3. On a finding, an **Assist** menu appears next to Description, Impact, Technical details and Remediation:
   **Draft from title/CWE**, **Improve wording**, **Translate to English / Polish** (the report's language is
   marked) and **Shorten**.
4. The suggestion opens in a dialog as editable plain text. **Replace field**, **Insert** (at the cursor, or at the
   end), **Copy** or **Discard**. Nothing changes until you click, and nothing is saved until you save the finding.

Safety: the URL must be `http(s)` on `127.0.0.1`, `::1` or `localhost` (checked when saving and again on every
request; redirects are not followed and proxy variables are ignored). Prompts contain only the fields of the
finding you are editing (title, CWE, severity, the four texts above), never other reports. Model output is treated
as untrusted text and never rendered as HTML. Requests are rate limited, limited to 20,000 characters per field,
and time out after 120 s. All prompts are in `src/ptreport/ai.py`.

## AI agents (MCP, SARIF, ptai)

ptreport can be the system of record for AI pentest agents. **Nothing an agent sends reaches a report without
you accepting it**: results become *proposals* in the report's **AI queue** (report page → **AI queue**), where
you accept them as new findings, merge them into existing ones (a duplicate hint points at likely matches) or
reject them. Accepted findings start as *Open*, keep their origin (tool, version, run, verdict, model) behind a
small **AI** badge, and get a history entry.

```bash
claude mcp add ptreport -- ptreport mcp --report 3     # MCP server over stdio (Codex / Cursor: see the docs)
ptreport import-ai 3 pentest.sarif --dry-run           # SARIF 2.1.0, ptai proof capsules, proposal JSON
ptreport scope 3 --format md                           # the engagement brief to start an agent from
```

- **MCP tools**: `list_reports`, `get_report`, `get_scope`, `search_cwe`, `list_templates`, `list_proposals`
  and `propose_finding` / `propose_http_evidence` / `propose_code_evidence` / `propose_file` /
  `propose_retest_result`, which only ever create proposals (`--read-only` hides them).
- **Integration tokens** (Settings → Integrations) with the scopes `read` and `propose` for agents that use the
  API (`POST /api/v1/reports/<id>/proposals`); shown once, stored hashed, revocable.
- **Imports** (report → **Import AI results**): SARIF from pentest-ai, Semgrep, CodeQL …, pentest-ai proof
  capsules (the capsule is attached as an evidence file with its SHA-256), and the documented
  **ptreport proposal JSON v1**. In a retest report, results that match a finding are offered as "not fixed";
  nothing is ever marked fixed because it is missing.

The proposal schema, MCP setup for Claude Code / Codex / Cursor, recipes for Decepticon, pentest-ai retests and
reverse-engineering agents, and the security notes are in **[docs/integrations.md](docs/integrations.md)**.

## Command line

`ptreport` on its own starts the web app (above). With a command it works on the same database directly, so you
can script it or use it next to the running app (the database is in WAL mode and every change is one transaction).
`--data-dir` works with every command, before or after it. `ptreport <command> --help` lists all options.

```bash
ptreport report list                      # table: id, title, client, language, period, findings by severity
ptreport report list --json               # the same as JSON, for scripts
ptreport report create --title "ACME web app" --client ACME --assessor "Jan Kowalski" \
    --language en --prefix ACME --start-date 2026-11-01 --end-date 2026-11-10    # prints the new id
ptreport report show 3                    # summary plus the findings table (--json too)

ptreport import-scan 3 burp-issues.xml --dry-run   # what would be created; changes nothing
ptreport import-scan 3 burp-issues.xml             # asks "Import into report #3? [y/N]"
ptreport import-scan 3 scan.nessus --yes --include-info   # no prompt (needed in scripts / without a terminal)

ptreport export 3 --format pdf            # ./ACME_web_app.pdf (same name as the web download)
ptreport export 3 --format md -o notes/   # into a directory; -o FILE for a name, -o - for stdout
ptreport export 3 --format json -o backup.json --force    # --force replaces an existing file
ptreport import-json backup.json          # restores the backup as a new report, prints its id

ptreport import-ai 3 pentest.sarif --dry-run      # SARIF / ptai capsule / proposal JSON -> AI queue
ptreport scope 3 --format md              # engagement brief for agents (JSON by default)
ptreport mcp --report 3                   # MCP server on stdin/stdout for agent clients
```

`report create` checks its input like the web form (e.g. no digits in assessor names, end date not before the
start date) and uses the default prefix and language from Settings when you leave them out. `import-scan` takes
everything the file contains (the web review page with all boxes ticked) and reuses targets already in the report;
`--format` is `auto` (default), `burp`, `nessus`, `nmap`, `zap` or `openvas`. `export --format` is `pdf`, `html`,
`md`, `json` or `tex` (LaTeX sources as .zip).

Exit codes: `0` success, `1` error (unknown report, invalid input, file exists, failed PDF...), `2` wrong usage.
Errors go to stderr.

## Burp Suite extension

Right-click any request or response in Burp (Proxy history, Repeater, Target, Logger, Intruder results ...) and
choose **Send to ptreport**. A dialog asks for:

- the **report** (the last one used is preselected),
- **New finding** (title, **CWE** with search over the whole MITRE catalogue, severity, target) or **Add to an
  existing finding**,
- the evidence title and whether to include the response.

![Sending a request from Burp to ptreport](docs/media/burp-send-to-ptreport.gif)

| | |
|---|---|
| ![Send to ptreport in Burp's context menu](docs/screenshots/burp-context-menu.png) | ![Send to ptreport dialog](docs/screenshots/burp-send-dialog.png) |

![Confirmation after sending](docs/screenshots/burp-sent.png)

Selecting several requests adds each one as a separate HTTP evidence item. A target matching the request's host is
preselected, or created from it. Afterwards you can open the finding in ptreport.

**Build and load** (JDK 17+; no Gradle needed):

```bash
./burp-extension/build.sh          # -> burp-extension/dist/ptreport-burp.jar
```

In Burp: *Extensions → Installed → Add → Java* and pick `ptreport-burp.jar`. Then open the **ptreport** tab in
Burp, paste the API token (`ptreport --show-api-token`, or Settings → API in ptreport) and click *Test
connection*. The build downloads the Montoya API (PortSwigger's official extension API, compile-time only; Burp
provides it at runtime) from Maven Central and checks its SHA-256. The token is kept in Burp's user settings, not in
project files.

## API (for the Burp extension)

Base URL: `http://127.0.0.1:5055/api/v1`, header `Authorization: Bearer <token>`.
The token is shown under **Settings** and can be regenerated there.

| Method | Path | Purpose |
|---|---|---|
| GET | `/ping` | Health / version |
| GET | `/reports` | List reports |
| GET | `/reports/{id}` | Report details |
| GET/POST | `/reports/{id}/targets` | List / create targets |
| GET/POST | `/reports/{id}/findings` | List / create findings (optional inline `evidence` list) |
| GET | `/findings/{id}` | Finding with evidence |
| POST | `/findings/{id}/evidence` | Attach a raw HTTP request/response |
| POST | `/findings/{id}/attachments` | Attach a screenshot: `{"caption": "...", "data_base64": "..."}` |
| GET | `/findings/{id}/files` | Evidence files of a finding (name, size, MIME type, SHA-256, description, download URL) |
| POST | `/findings/{id}/files` | Upload evidence files: `multipart/form-data`, one or more `file` parts, optional `description` |
| GET | `/templates?language=en&q=xss` | Finding template library |
| GET | `/cwe?q=xss` | MITRE CWE catalogue (`{"id": "CWE-79", "name": ...}`) |
| GET/POST | `/reports/{id}/notes` | List / add working notes |
| POST | `/findings/{id}/code-evidence` | Add code evidence: `{"title", "location", "language", "code", "note"}` |
| GET | `/reports/{id}/scope` | Engagement scope for agents (`?format=md` for a Markdown brief) |
| GET/POST | `/reports/{id}/proposals` | AI queue: list (`?status=`) / queue proposals (see [docs/integrations.md](docs/integrations.md)) |

```bash
TOKEN=$(ptreport --show-api-token)
curl -s -H "Authorization: Bearer $TOKEN" -F file=@login.pcap -F file=@burp.har -F description='Login traffic' \
  http://127.0.0.1:5055/api/v1/findings/1/files
curl -s -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d '{"title":"IDOR in /api/orders/{id}","cvss_version":"3.1",
       "cvss_vector":"CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N","cwe":"639",
       "evidence":[{"title":"Order of another user","request":"GET /api/orders/2 HTTP/1.1\r\nHost: shop\r\n\r\n"}]}' \
  http://127.0.0.1:5055/api/v1/reports/1/findings
```

Validation errors return `422 {"error":"validation_failed","errors":{field: message}}`.

Integration tokens (Settings → Integrations) only reach the endpoints of their scopes: `read` (reports,
targets, findings, scope, proposals, CWE, templates) and `propose` (queueing proposals); everything else needs
the main token and answers `403` otherwise.

## Security model

The tool stores sensitive client data, so it protects itself even though it only runs on localhost:

- Listens on `127.0.0.1` only by default. The database folder is `0700`, and the secrets are `0600`.
- A **Host header allow-list** blocks DNS-rebinding attacks from malicious pages open in your browser.
- Every browser form has **CSRF tokens**. Session cookies are `SameSite=Strict` and `HttpOnly`.
- A strict **CSP** (`script-src 'self'`, no inline scripts) plus `X-Frame-Options: DENY`, `nosniff`, and `no-referrer`.
- **Validation** happens server-side on every write path (forms, API, import). Client-side checks only help with UX.
- All SQL uses bound parameters. All user content is HTML-escaped. Reference links are only made for `http(s)`.
- The API uses a random bearer token, compared in constant time. The API sends no CORS headers.

## Development

```bash
uv venv && uv pip install -e ".[dev]"     # or: python -m venv .venv && pip install -e ".[dev]"
.venv/bin/pytest                           # tests
uvx ruff check src tests                   # lint
uvx pip-audit -r requirements.lock --require-hashes   # dependency audit
.venv/bin/ptreport --data-dir ./data       # run against a throwaway DB
```

To regenerate the lock file after changing dependencies:
`uv pip compile pyproject.toml --generate-hashes --python-version 3.10 -o requirements.lock`

### Dependencies

Two runtime dependencies are pinned in `requirements.lock`:

- **Flask**: web framework. It brings Werkzeug, Jinja2 and MarkupSafe.
- **cvss** (Red Hat Product Security): the official FIRST scoring algorithms for CVSS 2.0, 3.x and 4.0.
  CVSS 4.0 scores come from a macro-vector lookup table, which is error-prone to re-implement.
  The CVSS specifications are stable, so infrequent releases are expected. The repository is maintained
  and not archived.

### Layout

```
src/ptreport/
  cli.py            entry point (`ptreport`)
  app.py            Flask app factory, error handling
  db.py             SQLite connection + schema migrations (PRAGMA user_version)
  repo.py           all SQL (parameterised)
  validation.py     server-side validation for forms / API / import
  cvss_service.py   CVSS scoring + calculator metric definitions
  cwe.py            MITRE CWE catalogue (search, names, mitigations)
  ai.py             optional local AI assistant (Ollama, loopback only)
  security.py       Host allow-list, CSRF, API token, security headers
  views.py          browser UI
  api.py            JSON API v1
  export.py         HTML / Markdown / JSON export, JSON import
  importers.py      scanner parsers (Burp, Nessus, Nmap, ZAP, OpenVAS), hardened XML loading
  proposals.py      AI intake queue: proposal validation, duplicate hints, accept / merge / reject
  ai_import.py      SARIF / ptai capsule / proposal JSON imports into the AI queue
  mcp.py            MCP server (stdio, JSON-RPC 2.0) for agent clients
  scope.py          engagement scope for agents (JSON, Markdown brief)
  latex.py          LaTeX rendering + PDF compilation (Tectonic)
  data/             MITRE CWE catalogue, starter finding templates
  rendering.py      safe rich-text rendering, report labels (EN/PL)
  templates/ static/
tests/              pytest suite
```

## Contributing

Issues and pull requests are welcome; see [CONTRIBUTING.md](CONTRIBUTING.md) and the
[code of conduct](CODE_OF_CONDUCT.md). Changes are listed in [CHANGELOG.md](CHANGELOG.md).

**Security issues:** please report them privately as described in [SECURITY.md](SECURITY.md).

## License

ptreport is released under the [Apache License 2.0](LICENSE) (see also [NOTICE](NOTICE)). It ships the MITRE CWE List (CWE Terms of Use) and
the Hanken Grotesk and JetBrains Mono fonts (SIL Open Font License 1.1); details and the licenses of
dependencies are in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

Burp Suite is a trademark of PortSwigger Ltd. and CWE is a trademark of The MITRE Corporation; ptreport is not
affiliated with or endorsed by them.
