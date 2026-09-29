# TiDB as the governed fact layer beneath Amazon Bedrock AgentCore

A working reference implementation: an EV charger fleet diagnostic agent running on
**AgentCore Runtime**, using **TiDB** as the memory substrate — episodic, semantic and
procedural memory in one ACID cluster, with no separate vector store.

This repository exists to make one architectural argument concrete.

## Three layers of governance

AWS ships two governance primitives for agents. Both stop short of the same boundary.

| Layer | Governs | Primitive | Where it acts |
|---|---|---|---|
| Utterance | what the model **says** | **Bedrock Guardrails** — content filters, denied topics, PII redaction, contextual grounding and automated reasoning checks | input and output of the model call |
| Action | what the agent **may do** | **Policy in AgentCore** — Cedar, deterministic, default-deny, every decision logged to CloudWatch | intercepts the tool call *before* invocation, at the Gateway |
| **Fact** | what the agent **knows** | **TiDB** ← this repository | after the write |

The Guardrails documentation is explicit that it does not address data at rest, audit trails,
or post-inference persistence. Policy governs whether a tool call is permitted, not whether the
fact it produced is true, who authored it, whether later evidence superseded it, or whether it
can be corrected or erased on request.

That third row is what this substrate provides: mutable, correctable, provenance-ranked facts
with an audit trail, joinable to business data in a single SQL statement.

## What it is not

It is not an alternative to AgentCore Memory. AgentCore Memory owns the conversation layer and
is good at it. The two are composed, not compared — see
[`memory_strategy/`](memory_strategy/README.md), which implements the **self-managed strategy**
extension point AWS documents and leaves empty. AWS's own guidance assigns extraction and
*"consolidat[ing] memory records ... to remove duplicates and resolve conflicts with existing
records"* to the customer pipeline. This is that pipeline.

## Memory tiers

| Tier | Table | Contents |
|---|---|---|
| Episodic | `agent_reasoning` | every checkpoint: observation, hypothesis, evidence refs, confidence, resolution — with supersession tracking |
| Semantic | `outage_catalog`, `charger_windows` | vector embeddings colocated with structured facts; hybrid vector + FULLTEXT retrieval |
| Procedural | `fleet_memory` | validated fleet-wide patterns, scoped and confidence-ranked |

Confidence is **derived, not self-reported**. `verified_confirmations` is incremented only by
`agent/verify_outcome.py` on an adjudicated field outcome, and is tracked separately from
agent-authored counters. The routing shortcut gates on the verified counter alone, so an agent
cannot talk its way into being trusted. `pending_refs` and `adjudicated_refs` carry the
platform-stamped linkage and the per-reference idempotency record; neither is ever
model-supplied.

## Cost behaviour

Context assembly runs five tiers of SQL before the model is called, so the agent starts briefed
rather than exploring. When a high-confidence verified pattern matches, routing takes a shortcut:
a cheaper model and 3 tool rounds instead of 15. The saving is model substitution and round
reduction — measurable in dollars and latency per investigation, and it improves as the fleet's
verified memory grows.

## Quickstart

```bash
cp .env.example .env          # fill in TiDB credentials
pip install -r requirements.txt

python -c "import pathlib,os,pymysql"   # sanity check
mysql < schema.sql                       # idempotent
python seed/seed_charger_registry.py
python seed/seed_outage_catalog.py
python seed/stream_telemetry.py --minutes 60
python embedding/embedding_service.py --poll --once   # fill NULL vectors

python agent/run_agent.py --auto          # investigate the top anomaly
python agent/dispatch.py --top 5          # concurrent fleet dispatch
```

Deploying to AgentCore Runtime: see [`agentcore/README.md`](agentcore/README.md). Secrets are
**Secrets Manager ARNs only** — never literals in `agentcore.json`.

## Layout

```
tool_handlers.py       substrate: pooling, hybrid search, memory ops, agent loop, custodial duties
text_bander.py         deterministic text builders for embedding
observability.py       per-role token accounting, routing signal, timings
agent/                 run_agent.py (CLI + run_investigation), dispatch.py, verify_outcome.py
runtime/main.py        AgentCore Runtime entrypoint + Secrets Manager resolution
seed/                  registry, outage catalog and telemetry seeding
tool_definitions.json  the agent's tool surface
adapters/ev_charger/   [Phase 2] where the domain layer moves when lib/ is split out
migrations/            schema v3 (derived confidence), v4 (counter split), v5 (verification link)
agentcore/             deployment config — ARNs only, targets eu-central-1
mcp_server/            [Phase 4] TiDB memory ops as Gateway MCP tools
jobs/                  [Phase 2] custodial duty CLI — the missing scheduler
memory_strategy/       [Phase 4] AgentCore Memory self-managed strategy pipeline
infra/                 [Phase 2-4] EventBridge, Lambda trigger, Cedar policies, IAM
eval/                  [Phase 2] evaluation harness
```

Directories marked `[Phase N]` contain a README stating intent and constraints, not stubbed code.
See [`ARCHITECTURE.md`](ARCHITECTURE.md) for the target deployment and
[`AGENT_LIFECYCLE.md`](AGENT_LIFECYCLE.md) for the memory lifecycle in detail.

## Honest status

| Claim | State |
|---|---|
| Runs on AgentCore Runtime | Previously deployed and invoked successfully; being redeployed in eu-central-1 from this repo |
| Derived confidence, counter split, verification loop | Implemented (schema v3-v5) |
| Deduplication, reconciliation, write control | Implemented, enforced on write |
| Decay, compaction | Implemented, **not yet scheduled** — see [`jobs/`](jobs/README.md) |
| Semantic recall of agent-authored facts | `reasoning_vec` is currently written by the polling embedding service, not at insert. Phase 2 moves it inline. |
| Gateway / MCP / Cedar policy integration | **Not built** — Phase 4, see [`mcp_server/`](mcp_server/README.md) |

Related: [`ev_charger_anomaly_detection`](https://github.com/bernard-kavanagh/ev_charger_anomaly_detection)
(the substrate this is built from) and
[`network_incident`](https://github.com/bernard-kavanagh/network_incident) (multi-agent
topology on the same foundation).
