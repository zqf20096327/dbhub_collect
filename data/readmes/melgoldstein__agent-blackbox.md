# agent-blackbox

**Find the tool response that changed the decision.**

[![CI](https://github.com/melgoldstein/agent-blackbox/actions/workflows/ci.yml/badge.svg)](https://github.com/melgoldstein/agent-blackbox/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](pyproject.toml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

A local recorder and replay debugger for tool-using AI workflows. Record nested calls, inspect their evidence, replace a response at a checkpoint, and compare the resulting decisions. Python, SQLite, and a browser. No hosted service or API key required for the demo.

![The debugger showing a recorded inventory investigation](docs/overview.jpg)

## Quickstart (30 Seconds)

With Python 3.11+ and Git installed, in an activated virtual environment:

```bash
git clone https://github.com/melgoldstein/agent-blackbox.git
cd agent-blackbox
python -m pip install .
blackbox demo
blackbox serve
```

Open **http://127.0.0.1:8765**. Select the recorded run, inspect `inventory.lookup`, then choose **Create fork and compare**. The corrected response is prefilled. Initial dependency downloads may take longer than 30 seconds.

| Evidence | Original run | Forked run |
| --- | --- | --- |
| Available inventory | 0 units | 24 units |
| Evidence age | 48 hours | 0 hours |
| Decision | Expedite 20 units | Allocate existing stock |
| External purchases issued | None | None |

The included agent is a deterministic decision workflow that deliberately trusts stale inventory. It demonstrates a failure you can reproduce exactly; it does not pretend to be an autonomous model.

## Three execution modes

| Mode | What executes | External calls |
| --- | --- | --- |
| Playback: `inspect`, browser | Read stored events | None |
| Offline replay | Registered workflow from initial state; recorded responses substituted | No live fallback |
| Fork | Registered workflow from nearest preceding checkpoint; one response replaced; remaining responses replayed | No live fallback |

Replay is supported for **explicit, versioned workflow implementations**, not arbitrary Python stack frames. Model responses are recorded evidence, not deterministic model execution. Direct recording works independently of workflow registration.

## CLI walkthrough

`demo` prints JSON including its `id`. Substitute that ID for `RUN_ID` below. Event 3 is the inventory response in a fresh demo; other recordings have their own event numbers.

```bash
blackbox list
blackbox inspect RUN_ID
blackbox replay RUN_ID --offline
blackbox fork RUN_ID --replace-event 3 --response examples/corrected-stock.json
blackbox compare RUN_ID FORK_ID
blackbox export RUN_ID > trace.json
```

Each replay/fork returns a new run ID. Run the complete sequence without manual ID substitution:

```bash
python examples/capture_demo.py
```

This writes original, replay, fork, and comparison JSON under `.blackbox/demo/`. View those recordings with:

```bash
blackbox --db .blackbox/demo/traces.sqlite serve
```

## Instrument a tool

```python
from agent_blackbox import Recorder


def lookup_inventory(sku: str) -> dict:
    return {"sku": sku, "available": 24, "age_hours": 0}


with Recorder("inventory-investigation") as recorder:
    with recorder.span("investigate-shortage"):
        stock = recorder.call("inventory.lookup", lookup_inventory, sku="PUMP-042")
```

Use `async with Recorder(...)` and `await recorder.acall(...)` for async tools. Context-local parent spans isolate concurrent asyncio tasks. Await all child tasks before exiting the recorder. Arguments and results must be JSON-serializable; tool return values are passed through unchanged while persisted snapshots are redacted.

[Workflow integration](docs/integration.md) explains checkpoints, registration, and the replay contract. [Trace format](docs/trace-format.md) documents the versioned JSON export.

## Optional real-model recording

```bash
python -m pip install '.[openai]'
```

Set `OPENAI_API_KEY` and `BLACKBOX_MODEL` in your environment, then:

```python
import os
from agent_blackbox import Recorder
from agent_blackbox.adapters.openai import respond

with Recorder("model-observation", capture_models=True) as recorder:
    response = recorder.model(
        "openai.responses",
        respond,
        model=os.environ["BLACKBOX_MODEL"],
        input="Give a one-sentence inventory freshness check.",
    )
```

The optional adapter stores output text, model identity, and provider-reported token counts. It does not store reasoning items or invent cost estimates. This integration is tested with a stub SDK response; live provider behavior and billing require your credentials and are not part of the offline verification.

## Measured recording overhead

Windows 10, Python 3.12.14, AMD64; 500 samples after 50 warmups. Same in-memory lookup callback on both paths. Recorder construction is excluded; the recorded path includes validation, redaction, and two durable SQLite transactions per call.

| Path | Median | p95 |
| --- | ---: | ---: |
| Uninstrumented callback | 0.100 us | 0.200 us |
| Recorded callback | 8,794.750 us | 9,376.800 us |

**Added median latency: 8.795 ms.** This version favors inspectable interrupted runs over throughput. Tiny baseline timings approach timer resolution; the absolute recording cost is more useful than a speed ratio. Results depend on storage, antivirus, and system load; this is one machine, not a universal guarantee.

```bash
python benchmarks/recording.py
```

[Raw measurements](benchmarks/windows-python312.json) retain workload and environment details.

## Boundaries that matter

- Redaction runs before persistence, using sensitive key names, two common token prefixes, and configured literal secrets. It is not a general DLP system. Redacted recordings are playback-only.
- Offline replay never calls functions through `Recorder.call`, `acall`, or `model`. Workflow implementations are trusted Python code: this is not an OS sandbox and cannot stop direct network or filesystem access inside your own workflow.
- Only completed, compatible runs can replay. Changed arguments, missing responses, version mismatches, and invalid replacements fail explicitly.
- SQLite records are editable by their owner. No immutability or tamper-evidence claim is made.
- The debugger binds to loopback, checks Host and write Origins, and renders payloads as text. It has no remote authentication; do not expose it through a public proxy.
- There are no automatic LangChain/LangGraph integrations, arbitrary process recovery, streamed-token interception, or distributed tracing in this release.

## Development

```bash
python -m pip install -e '.[dev]'
python -m pytest -q
python -m ruff check .
python -m ruff format --check .
python -m build
```

CI tests Python 3.11-3.13 on Linux and Windows, builds the distribution, and installs the wheel into a separate environment to verify CLI and packaged browser assets.

Read the [architecture](docs/architecture.md), [troubleshooting](docs/troubleshooting.md), and [contributing guide](CONTRIBUTING.md). MIT licensed. Created by [Mel Goldstein](https://melgoldstein.com/).
