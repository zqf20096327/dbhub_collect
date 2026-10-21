# BossAlign

> **The Human Feedback Alignment Engine for AI Agents.**
> Turn human feedback into persistent, scoped rules. Stop agents from repeating the same mistakes.

[![CI](https://github.com/davidmercer0620-ai/bossalign/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/davidmercer0620-ai/bossalign/actions/workflows/ci.yml)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

BossAlign (蛔虫引擎) is a small, framework-independent layer between agent memory and agent behavior. It stores corrections as **proposed rules with evidence, scope, and exclusions**, then retrieves and checks only the rules that fit a new task. The same API can hold programming, workplace, writing, design, and interpersonal preferences; the core does not assign meaning to roles such as manager, partner, or employee.

Unlike a chat-history memory, BossAlign is designed to remember what should be repeated, where it applies, and where it must not be generalized. A system check is never presented as user approval.

| Ordinary conversation memory | BossAlign |
| --- | --- |
| Saves statements or summaries | Converts feedback into a rule proposal with its source |
| Often retrieves by broad similarity | Matches declared project, task, audience, objective, and task ID fields |
| Can spread a local correction to unrelated tasks | Stores explicit negative boundaries and returns uncertainty when context is missing |
| Usually has no rule lifecycle | Keeps draft, confirmed, and inactive states plus version history |
| May say an output “passes” | Reports deterministic evidence and coverage; never claims human approval |

## Quickstart

Python 3.9+; the core package has no runtime dependencies. From a clone:

```bash
git clone https://github.com/davidmercer0620-ai/bossalign.git
cd bossalign
python -m pip install -e .
```

Try the local synthetic demo. It uses the real SDK and a temporary SQLite database; it makes no model call and does not simulate a person's approval.

```bash
bossalign demo
```

### Python SDK

```python
from bossalign import BossAlign, TaskContext

with BossAlign("bossalign.sqlite3") as align:
    proposal = align.ingest(
        "For consumer onboarding copy, avoid 'guaranteed zero downtime'. "
        "Do not apply this to technical incident reports.",
        reviewer="reviewer-1",
        context={
            "applicable_scope": {
                "project": "sample-app",
                "task_type": "consumer_copy",
                "audience": "consumer",
            },
            "negative_boundaries": [{"task_type": "technical_incident_report"}],
            "deterministic_checks": ["guaranteed zero downtime"],
            "conflict_key": "downtime_claim",
            "effect": "avoid",
        },
    )
    print(proposal.status)  # draft: stored, but not active

    rule = align.confirm_rule(proposal.rule_id)  # explicit confirmation step
    task = TaskContext(
        project="sample-app",
        task_type="consumer_copy",
        audience="consumer",
    )
    selection = align.retrieve(task, reviewer="reviewer-1")
    report = align.check(task, "This copy promises guaranteed zero downtime.", reviewer="reviewer-1")

    print([item.rule_id for item in selection.active_rules])
    print(report.status)  # violations_found
    print(report.violations[0].evidence)  # exact matched phrase
    print(report.user_approved)  # False
```

Feedback events, rule records, and version snapshots are stored in SQLite. A new `BossAlign("bossalign.sqlite3")` instance can retrieve the same confirmed rules after restart. A material `update_rule()` creates another version and returns a confirmed rule to `draft`; it must be confirmed again. `revoke_rule()`/`deactivate_rule()` stops retrieval while retaining history. `delete_rule()` removes the rule, its source events, and version snapshots.

### Preference owner, context, and privacy

Rules can identify whose preference is represented independently of who submitted the feedback. Use `attribution="direct"`, `"third_party"`, or `"ai_inference"`; transferred reports and AI inferences remain drafts until the named preference owner confirms them. Scope may include the generic `interaction_context` field, such as `workplace`, `code_review`, or `personal_relationship`; those values are supplied by the application and have no special behavior in the core.

For an attributed rule, confirm with `align.confirm_rule(rule_id, confirmed_by="person-1")`; the SDK will not treat the submitter as the preference owner by default.

`confirmed_by` is an identity label, not authentication. An integrating application must authenticate the person before it submits a confirmation.

`valid_until` makes a rule temporary; a rule without an expiry remains in force until it is updated, revoked, or deleted. Supply a current explicit boundary in `TaskContext.current_overrides` to report a conflict and keep the stored rule out of `effective_rules`. A past preference never overrides a current refusal.

Sensitive feedback is local-first. `sensitive=True` requires explicit storage consent; the SDK stores a minimized directive and omits the original source text by default. Retaining source text requires an explicit `retain_source_text=True`. A provider that may send data off-device also requires `allow_external_processing=True`. The provider is not called when either consent check fails.

The SDK cannot identify or redact every sensitive detail. Supply a minimized directive and non-identifying scope values; do not place raw personal identifiers in the rule fields.

```python
with BossAlign("bossalign.sqlite3") as align:
    proposal = align.ingest(
        "Sensitive source text supplied by the person.",
        reviewer="agent",
        preference_owner="person-1",
        attribution="direct",
        sensitive=True,
        consent_to_store_sensitive=True,
        context={
            "directive": "Ask before offering advice.",  # minimized persisted rule
            "applicable_scope": {
                "interaction_context": "personal_relationship",
                "task_type": "venting",
            },
        },
    )
```

### Fictional interpersonal feedback cases

The public cases in [`examples/communication_feedback_cases.json`](examples/communication_feedback_cases.json) distinguish expression, advice-seeking, a temporary request for space, and a changed boundary. They test how the core handles structured provider results; they are not evidence that the offline parser understands emotional nuance.

| Feedback type | Expected handling |
| --- | --- |
| “I need to vent; please just listen.” | Store as a non-rule event; do not create a persistent preference |
| “Can you help me decide what to say?” | Treat as an advice request, not as a lasting preference |
| “I need space tonight; please do not message me until tomorrow.” | Keep the time-limited boundary only through its expiry |
| “Ask before calling me.” | Store as a scoped boundary update that can replace a prior rule after confirmation |

BossAlign is not a psychological assessment, mind-reading, or emotional persuasion system. It does not diagnose people, infer consent from past behavior, or generate relationship scripts.

### Before / after: keeping a correction in its lane

History: “For consumer onboarding copy, avoid ‘guaranteed zero downtime’. Do not apply this to technical incident reports.”

| New task | Ordinary broad memory | BossAlign result |
| --- | --- | --- |
| Consumer onboarding copy in `sample-app` | May repeat the phrase, or retrieve a vague “avoid claims” memory | Applies the confirmed rule; exact configured phrase checks can flag the phrase |
| Technical incident report in `sample-app` | May incorrectly remove a useful incident detail | Excludes the rule because `task_type` matches a negative boundary |
| Task with no audience or project context | May apply based on vague similarity | Returns uncertainty; it does not force the rule onto the task |

The offline provider does **not** understand arbitrary semantics. It recognizes a small set of instruction/preference cues and checks only exact phrases explicitly configured for deterministic checking. For broader language interpretation, configure an OpenAI-compatible provider; its findings remain model inferences and still require human review.

## CLI

The database path is selected with `--db` before the command, or with `BOSSALIGN_DB`.

```bash
# Store a proposal. Supply structured scope; otherwise it will not be activated.
bossalign --db ./memory.sqlite3 ingest \
  --reviewer reviewer-1 \
  --raw "Avoid 'guaranteed zero downtime' in consumer copy." \
  --context-json '{"applicable_scope":{"project":"sample-app","audience":"consumer"},"negative_boundaries":[{"task_type":"technical_incident_report"}],"deterministic_checks":["guaranteed zero downtime"]}'

# Confirm only after reviewing the stored proposal
bossalign --db ./memory.sqlite3 rules confirm --rule-id RULE_ID

bossalign --db ./memory.sqlite3 rules list --reviewer reviewer-1
bossalign --db ./memory.sqlite3 rules update --rule-id RULE_ID --directive "Keep the measurement context"
bossalign --db ./memory.sqlite3 rules deactivate --rule-id RULE_ID
bossalign --db ./memory.sqlite3 rules revoke --rule-id RULE_ID --reason "Updated brand guidelines"
bossalign --db ./memory.sqlite3 rules reject --rule-id RULE_ID --reason "Unverified hypothesis"
bossalign --db ./memory.sqlite3 rules supersede --rule-id OLD_ID --new-rule-id NEW_ID
bossalign --db ./memory.sqlite3 rules delete --rule-id RULE_ID
bossalign --db ./memory.sqlite3 check --file draft.md \
  --task-context '{"project":"sample-app","task_type":"consumer_copy","audience":"consumer"}' \
  --reviewer reviewer-1
bossalign --db ./memory.sqlite3 export --preview
bossalign --db ./memory.sqlite3 export --out export.json
bossalign --db ./memory.sqlite3 replay --file steps.json
bossalign --db ./memory.sqlite3 sanitize --file draft.md --out clean.md
```

Commands: `ingest`, `rules`, `check`, `export`, `replay`, `demo`, `sanitize`, and `calibrate`. Check exit codes are `0` for no reported issue/no applicable rule, `1` for a reported violation or model finding requiring review, and `2` when evaluation is uncertain or cannot run. `calibrate` exits `0` on success, `1` when a candidate policy is rejected by the gate, and `2` when the evidence is insufficient.

For sensitive CLI ingestion, pass `--sensitive --consent-to-store-sensitive`. Use `--allow-external-processing` only when you explicitly authorize a configured remote provider to receive the feedback. Source text is not retained for sensitive feedback unless `--retain-source-text` is also supplied.

## LLM provider

The SDK accepts a provider object. The included adapter uses the OpenAI Chat Completions-compatible request shape and Python's standard library; no vendor SDK is required.

```python
import os
from bossalign import BossAlign
from bossalign.providers import OpenAICompatibleProvider

provider = OpenAICompatibleProvider(
    base_url=os.environ.get("BOSSALIGN_BASE_URL", "https://api.openai.com/v1"),
    model=os.environ["BOSSALIGN_MODEL"],
    api_key=os.environ["BOSSALIGN_API_KEY"],
)
align = BossAlign("memory.sqlite3", provider=provider)
```

The adapter returns a proposal; the SDK still stores it as `draft`. The provider can also return review findings, which are labelled `llm_inference`, include output evidence, and require human judgment. No real provider call is made unless an application explicitly configures and invokes one.

For CLI parsing/review, set `BOSSALIGN_PROVIDER=openai`, `BOSSALIGN_API_KEY`, and `BOSSALIGN_MODEL`; set `BOSSALIGN_BASE_URL` for a compatible endpoint. Listing rules, sanitizing, and the synthetic demo do not need provider credentials.

## Calibration

V0.2 could store and check rules but could not measure whether applying them was
the right call. V0.3 adds a closed loop: record a human verdict, measure the
decisions, derive a threshold from the measurements, and gate any policy change
behind the same pool.

```python
from bossalign import BALANCED_POLICY, BossAlign, TaskContext

with BossAlign("memory.sqlite3") as align:
    task = TaskContext(project="sample-app", task_type="consumer_copy")
    align.record_outcome(task, "missed", note="rule should apply without the audience key")
    print(align.calibration_report().to_dict())

    recommendation = align.derive_threshold(target_precision=0.9, min_support=20)
    decision = align.propose_bump(BALANCED_POLICY, memo="recover partial-context decisions")
    print(decision.accepted, decision.regressions)
```

Verdicts are `correct`, `wrong_apply`, `missed`, `correct_skip`, and `irrelevant`.
The first four carry ground truth; the last is excluded. Metrics are precision,
recall, decision coverage, over-generalization rate, a Wilson interval, and
Brier/ECE helpers for confidence quality.

A policy change is promoted only when it clears every limit: enough support, at
least one new outcome since the active version, **no regression on any previously
correct decision**, precision at or above target, coverage at or above the floor,
and over-generalization at or below the ceiling. Accepted and rejected versions
are both kept, with their memo and decision record.

`strict` remains the default and reproduces V0.2 behaviour exactly; `balanced`
and `permissive` are candidates that must earn promotion on your own outcomes.
Full methodology, metric definitions, and the worked example are in
[`docs/calibration.md`](docs/calibration.md).

## Benchmark

Run the public suites locally:

```bash
python benchmarks/run.py          # JSON report
python benchmarks/run.py --gate   # exit 1 unless the promotion gate is met
```

Two sections:

- **Functional regression** — 4 fictional cases (software development, content
  writing, product design, data analysis): 4 feedback events, 8 scope decisions,
  12 output checks. It reports extraction accuracy, scope accuracy,
  error-generalization rate, and violation precision/recall.
- **Decision quality** — 66 labelled tasks across six projects and 24 rules,
  scored under three policies, with the upgrade gate evaluated in both directions:

| Policy | Precision | Recall | Coverage | Over-generalization | Gate |
| --- | --- | --- | --- | --- | --- |
| `strict` | 1.000 | 0.500 | 0.545 | 0.000 | baseline |
| `balanced` | 1.000 | 1.000 | 0.818 | 0.000 | accepted |
| `permissive` | 0.857 | 1.000 | 0.909 | 0.200 | rejected |

Both suites make zero model calls. They are synthetic fixtures that check
decision behaviour and promotion gating; they are not a language benchmark or a
model comparison.

The separate interpersonal communication fixture is exercised by unit tests; it
is not counted in these metrics.

## Architecture

```text
Feedback -> Parser Proposal -> SQLite Event Store (Audit Log + Provenance)
                                       |
                   Preference Lifecycle: PROPOSED -> CONFIRMED
                                       |
Task Context -> Scope Engine V2 (Multi-dimensional constraints + Exclusions)
                                       |
                   Conflict Resolver (Multi-actor / Temporal / Authority)
                                       |
Grounded Facts (Evidence Retriever) + Configured Checks -> CheckReport
                                       |
              Safe State Export (Strict Whitelist Projection)
                                       |
     Human Verdict -> Calibration Pool -> Decision Policy -> Rule-set Version Gate
```

The last line is V0.3: decisions are recorded, measured, and only then allowed to
change how the engine decides. See [Calibration](docs/calibration.md).

The SDK, CLI, and demo share the same event store, lifecycle engine, boundary engine, conflict resolver, and checker. SQLite is the local runtime storage. Data privacy is enforced by default-deny architecture, field-whitelisted exports, and local physical isolation. The presentation sanitizer is strictly a tag stripping utility.

## Current limits

- Offline parsing is heuristic and English/Chinese cue-based, not general semantic extraction.
- The offline provider does not recognize emotional intent reliably. Structured intent labels from an application or configured provider remain proposals until the preference owner confirms them.
- Scope matching uses normalized exact values, not embeddings or fuzzy matching.
- Partial-context decisions are opt-in through a policy object; the default stays strict. A relaxed policy must clear the gate on your own outcomes before it becomes the active version.
- Confidence is never updated automatically. `derive_threshold()` and the gate use recorded verdicts; without verdicts there is nothing to calibrate.
- Unstructured negative boundaries are treated as uncertain; supply condition objects such as `{"audience":"technical"}`.
- Deterministic output checks look for configured exact phrases. They do not prove semantic compliance.
- LLM provider compatibility is defined by the OpenAI Chat Completions request shape; no third-party client has been integration-tested here.
- The calibration corpus is synthetic. A passing gate shows that a policy is measurable and non-regressive on that pool, not that it generalizes to your domain.
- MCP is deferred until the V0.3 SDK and core behavior have broader validation. No MCP client compatibility is claimed.
- The benchmark is a small fictional regression set, not evidence of production reliability or broad accuracy.

## FAQ

**Does BossAlign call a model by default?** No. The default provider is deterministic and offline. Set up a provider explicitly for model-assisted parsing or review.

**Does a `no_deterministic_violations_found` result mean the draft is approved?** No. It means only that the configured exact-phrase checks did not find a match. `user_approved` remains `false`.

**Can it generate or rewrite content?** V0.2 does not generate drafts. Use your existing agent to write content, then pass that output and its task context to `check()`.

**Where is memory stored?** In the SQLite file passed to `BossAlign`, or by default at `~/.bossalign/memory.sqlite3`. Storage is local. If you explicitly configure and invoke an external Provider, the input to that provider call is sent to that service.

**What happens when context is missing?** BossAlign returns uncertainty and does not force a scoped rule onto the task.

**Does it include MCP support?** No. MCP is deferred; no MCP client compatibility is claimed.

## Development

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
ruff check bossalign tests benchmarks
python -m bossalign demo
python benchmarks/run.py --gate
```

See [CONTRIBUTING.md](CONTRIBUTING.md), [Architecture](docs/architecture.md),
[Calibration](docs/calibration.md), and the [Chinese README](README_CN.md). Licensed under MIT; see [LICENSE](LICENSE).
