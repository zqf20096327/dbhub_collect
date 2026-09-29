# overnight-compute

SQLite-backed compute leases for running multiple coding agents on one shared machine overnight.

I made this because I was tired of telling a pile of agents "you get the GPU for the next two hours, then you get it after that" and hoping they would not step on each other. `overnight-compute` gives them a tiny shared queue, lease, heartbeat, and early-handoff protocol.

## Install

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
mkdir -p ~/.local/bin
curl -fsSL https://raw.githubusercontent.com/Infatoshi/overnight-compute/main/bin/overnight-compute -o ~/.local/bin/overnight-compute
chmod +x ~/.local/bin/overnight-compute
overnight-compute init
```

Make sure `~/.local/bin` is on `PATH`.

The CLI is a standalone Python script launched through `uv`.

## Quick Start

Schedule a 12-hour queue with six 2-hour slots:

```bash
overnight-compute schedule-chain --start now --slot 2h \
  pretrain-a pretrain-b pretrain-c pretrain-d pretrain-e pretrain-f
```

Each agent should wrap expensive commands:

```bash
overnight-compute run --agent pretrain-a -- uv run pytest
```

For manual multi-step work:

```bash
nvidia-smi
overnight-compute wait --agent pretrain-a
# do expensive work
overnight-compute heartbeat --agent pretrain-a --ttl 30m
overnight-compute release --agent pretrain-a --status done
```

Check the queue:

```bash
overnight-compute status
```

## Pasteable Agent Prompt

```text
I am going to sleep for 12 hours. You need to operate autonomously, coordinate compute with other agents, and make useful progress without asking me questions unless you are truly blocked by something only I can resolve.

First, create your own overnight-compute agent name. Make it specific to the experiment or workstream you are actually going to run, not generic. Use lowercase letters, numbers, and hyphens only. Keep it short but descriptive.

Before any GPU work or long CPU work:
1. Run `nvidia-smi`.
2. Check the queue with `overnight-compute status`.
3. If you are not already scheduled, schedule yourself into the overnight queue using your descriptive agent name. Choose a reasonable remaining slot without overwriting other agents. If unsure, use a 2-hour slot starting after the latest scheduled job.
4. Run `overnight-compute wait --agent YOUR_DESCRIPTIVE_AGENT_NAME`.
5. Only begin expensive work after it says `acquired`.

Prefer wrapping long commands with:

  overnight-compute run --agent YOUR_DESCRIPTIVE_AGENT_NAME -- COMMAND ...

If doing manual multi-step compute, heartbeat every few minutes while compute is active:

  overnight-compute heartbeat --agent YOUR_DESCRIPTIVE_AGENT_NAME --ttl 30m

When your useful overnight work is complete:

  overnight-compute release --agent YOUR_DESCRIPTIVE_AGENT_NAME --status done

If you hit a real blocker:

  overnight-compute release --agent YOUR_DESCRIPTIVE_AGENT_NAME --status failed --detail "short reason"

Your mission for the next 12 hours:
- Take over the assigned workstream autonomously.
- Profile before optimizing.
- Make minimal, targeted changes based on evidence.
- Run bounded sweeps where useful.
- Measure before and after. Do not claim speedups without measurements.
- Keep compute coordinated through `overnight-compute` so you do not step on other agents.
- Stay awake by using sleep/timer loops while waiting for leases or long jobs.
- Do not revert unrelated user changes.
- Run relevant tests or smoke checks before declaring work complete.

Hard invariant:
You may use expensive compute only while you own the overnight-compute lease.
```

## Commands

```bash
overnight-compute --help
overnight-compute instructions
overnight-compute schedule --agent NAME --start now --duration 2h
overnight-compute schedule-chain --start now --slot 2h NAME1 NAME2 NAME3
overnight-compute wait --agent NAME
overnight-compute run --agent NAME -- COMMAND ...
overnight-compute heartbeat --agent NAME --ttl 30m
overnight-compute release --agent NAME --status done
overnight-compute status
overnight-compute events
```

## Notes

- Source of truth is a local SQLite database at `~/.local/state/overnight-compute/overnight-compute.sqlite`.
- A running lease blocks other agents until it is released or expires.
- Later agents can start early when earlier agents mark `done`, `failed`, or `skipped`.
- This is machine-local coordination, not a cluster scheduler.
