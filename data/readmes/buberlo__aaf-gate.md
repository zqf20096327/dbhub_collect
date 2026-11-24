# aaf-gate

## Community-owned project / Maintainers wanted

This repository is published under the [Apache License 2.0](LICENSE) as a foundation for others to build on. Konrad Kern is not actively maintaining it; the repo remains under his GitHub account with no archive and no org transfer planned for now. You may use, fork, modify, and sell derivatives under the license terms. Contributors who show sustained, high-quality work can request write or maintainer access as described in [GOVERNANCE.md](GOVERNANCE.md). Spirit: here is the idea—build on it.

Deterministic policy gate, kill switch, call limits and tamper-evident audit for existing AI agent runtimes. **Not an agent of its own.** Models, providers and the agent loop are not reimplemented. The primary runtime is [Hermes Agent](https://github.com/NousResearch/hermes-agent) (pinned at v0.23.1 for the Mac mini appliance track). Adapters can target other runtimes later.

Core version **1.0.0rc1** (v1 candidate). See [CHANGELOG.md](CHANGELOG.md), [docs/v1/STATUS.md](docs/v1/STATUS.md) and [docs/v1/INSTALLATION-AND-OPERATIONS.md](docs/v1/INSTALLATION-AND-OPERATIONS.md).

## What it does

aaf-gate sits in front of tool calls and applies a deterministic policy per tool class:

- **read** — allow or deny reads (for example Gmail search)
- **draft** — allow or deny drafts (for example a reply draft; sending is out of scope)
- **internal_write** — allow or deny internal writes (for example labels); unattended internal writes stay blocked

It also provides:

- a **kill switch** (`gate-stop` / `gate-resume` / `gate-status`) that stops further work for a principal
- **call limits** per time window and tool class (tool-call counts, not model-token cost)
- an append-only, hash-chained **audit log** in SQLite
- **backup and restore** with a chain anchor (`gate-backup` / `gate-restore`)
- versioned, locked **industry templates** and example customer profiles
- a **device acceptance pack** for a Mac mini appliance (track A)

Pilot 1 scope: read Gmail, categorize, and draft a reply. No send.

## Architecture

```text
tool call
  → gate            (class decision)
  → GateKeeper      (policy, limits, kill switch, audit)
  → hermes_adapter  (Hermes hook mapping)
  → gatesocket      (Unix socket)
  → Hermes plugin aaf-gate 0.5.0 (pre_tool_call / post_tool_call)
```

Python standard library only in `core/`. No third-party Python dependencies.

## Status

This is a **v1 candidate (1.0.0rc1)**. It is implemented and unit-tested locally. It is **not production-ready**, **not yet device-accepted**, and it makes **no compliance claims**.

| | |
|---|---|
| Implemented and unit-tested locally | yes (`Ran 719 tests`, `OK`, Python stdlib) |
| Tested on the target Mac mini | no |
| Google Gmail Developer Preview access | not granted yet |
| Production | no |
| Send mail, computer use, own agent loop | not included |

Start values for the call-limit window are assumptions in the Pilot 1 policy (3600 s; read 160, draft 40, internal_write 80) and will be reset after a pilot week from recorded `gate_calls`.

## Quickstart

```bash
cd core
python3 -m unittest discover -s tests -q
python3 -m framework.cli version
```

`version` prints `core_version`, `schema_version` and `ok` as JSON. Further commands (`python3 -m framework.cli <command>`):

| Command | Arguments |
|---|---|
| `verify-install` | `package` `target` [`--package-hash`] |
| `verify-plugin` | `installed` (`--digest` \| `--package`) |
| `plugin-digest` | `dir` |
| `gate-serve` | `--db` `--socket` `--principal` [`--server` gmail] [`--mode` 0600] [`--group`] [`--unattended`] |
| `gate-plist` | `--label` `--python` `--workdir` `--db` `--socket` `--principal` `--user` [`--group`] [`--server` gmail] [`--mode` 0600] [`--unattended`] [`--log`] |
| `verify-launchd` | `installed` `--package` |
| `verify-hooks` | `home` |
| `verify-relay` | [`--home`] [`--system-root` /] |
| `pin-audit` | `source` `config` |
| `verify-hermes-dump` | `dump_file` `--package` |
| `verify-hermes-probe` | `probe_file` `--package` |
| `verify-device` | `--package` `--installed` `--package-hash` [`--managed-dir` /etc/hermes] `--hermes-home` `--plugin` `--launchd` `--dump` [`--home`] [`--system-root` /] [`--profile`] [`--allowed-profile`] [`--audit-anchor`] |
| `gate-init` | `--db` `--principal` `--tenant` [`--package`] [`--kind` agent] |
| `gate-audit` | `--db` `--tenant` [`--limit` 50] [`--summary`] [`--since`] [`--until`] [`--anchor`] |
| `gate-principal-add` | `--db` `--principal` `--tenant` `--role` |
| `gate-stop` | `--db` `--principal` |
| `gate-resume` | `--db` `--principal` |
| `gate-status` | `--db` `--tenant` |
| `gate-backup` | `--db` `--out` |
| `gate-restore` | `--backup` `--db` [`--expect-anchor`] |
| `pilot-baseline` | `--summary` `--timesheet` [`--min-samples` 5] [`--require-clean`] |
| `version` | — |

Device installation, operation, backup and the acceptance probes are described in [docs/v1/INSTALLATION-AND-OPERATIONS.md](docs/v1/INSTALLATION-AND-OPERATIONS.md). That guide has not been executed on a device yet.

## Repository layout

```text
core/          Python core (stdlib), CLI, tests
adapters/      Runtime adapters (Hermes plugin: adapters/hermes/aaf-gate/)
templates/     Versioned industry templates
profiles/      Synthetic example profiles
docs/v0.4/     Product direction
docs/v0.5/     Notes on implemented increments
docs/v1/       Honest status and install/operations guide
docs/adr/      Architecture decisions
CHANGELOG.md
LICENSE        Apache-2.0
```

## License

Copyright 2026 Konrad Kern. Licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE).

Hermes Agent is a separate project by Nous Research, licensed under MIT. This repository contains adapter and plugin code that talks to Hermes hooks; it does not vendor the Hermes source tree.
