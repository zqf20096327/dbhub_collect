# Scope Recall

Scope Recall `4.0.6` lets your assistants find earlier conversations and show where an answer came from.
You can keep memory on one computer or share a store across your own agents. Capture and text search work without a model budget.

## Quick start

1. Install the published package with Python 3.11–3.14 using `python -m pip install -U "hermes-scope-recall[codex]"`.
2. Run `scope-recall setup`, review the hosts and store it found, and confirm the plan.
3. Approve the integration in your host and open a new session. Tell it a distinctive test phrase, finish the turn, then ask for that phrase in a second session.

To install from source, run `python -m pip install -U ".[codex]"` from the repository root.

| Host | Setup and host-specific approval |
|---|---|
| Antigravity | [Set up capture and recall](docs/install/antigravity.md) |
| Claude Code | [Setup](docs/install/claude-code.md) |
| Codex | [Setup and hook review](docs/install/codex.md) |
| Hermes | [Setup and local identity](docs/install/hermes.md) |
| Cherry Studio | [Connect a read-only MCP entry](docs/install/cherry-studio.md) |
| WorkBuddy | [Setup and MCP approval](docs/install/workbuddy.md) |
| DeepSeek Harness | [Setup and plugin check](docs/install/dsh.md) |

Cherry Studio can search an existing store through MCP. Use another connected host to capture the test phrase.

## Using your store

- [Installation and upgrades](docs/install.md) covers host approval, model settings and verification. [Shared stores](docs/shared-store.md), [remote entries](docs/remote-entries.md) and [Docker](docs/docker.md) cover other ways to connect.
- Run `scope-recall ui` to review evidence, correct or mute a memory, or control what gets recorded. See [the local interface](docs/ui.md) and [private mode](docs/private-mode.md).
- [Import](docs/import.md), [export](docs/export.md) or [back up and restore](docs/backup-restore.md) your conversations. [Migration instructions](maintenance/AGENT_WORKFLOW.md) cover older installations.
- [Host identity and data access](docs/host-integration.md#data-and-host-boundaries), [claim evidence](docs/claim-mutation-contract.md), [profile and entity views](docs/profile-entity.zh-CN.md) and [evidence paths](docs/trace.zh-CN.md) describe how to inspect a result.
- [Background work](docs/background-work.md), [task handoffs](docs/host-integration.md#task-handoffs) and [development and benchmarks](CONTRIBUTING.md) cover operation and contribution.
