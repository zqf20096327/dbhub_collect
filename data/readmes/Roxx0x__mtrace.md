# mtrace

[![test](https://github.com/Roxx0x/mtrace/actions/workflows/test.yml/badge.svg)](https://github.com/Roxx0x/mtrace/actions/workflows/test.yml)
![python](https://img.shields.io/badge/python-3.9%2B-blue)
![license](https://img.shields.io/badge/license-MIT-green)

A cognitive memory architecture for agents. Not a store with a similarity search bolted on — a memory that **decays, strengthens with use, associates, consolidates, and forgets**, which is what "memory" means everywhere except in most agent frameworks.

Most agent memory is a vector database with a nicer name: embed the text, sort by cosine, done. That retrieves the most *similar* thing regardless of whether it's important, recent, still relevant, or connected to what the agent is thinking about. mtrace scores availability the way the memory literature says to — relevance is one term, not the whole score — and then does the parts a database can't: it lets memories fade, distils episodes into lessons, and wires related memories so recalling one surfaces the rest.

sqlite, standard library, runs offline with nothing installed.

## Quickstart

```
pip install "git+https://github.com/Roxx0x/mtrace"
```

```python
from mtrace import Memory

m = Memory("agent.db")

m.remember("deployed v2.3 to production at 14:00")
m.remember("v2.3 caused a spike in 500s on payments", importance=8)
m.remember("rolled back to v2.2, errors cleared in 4 minutes")
m.remember("chatted about the weather")          # low importance, will fade

# retrieval is relevance × importance × recency, then spreading activation
for item in m.recall("what went wrong with payments"):
    print(item)

# turn the incident's episodes into one durable lesson
m.consolidate()

# later: evict what's faded and unimportant; the lesson and the weather part ways
m.forget()
```

`python examples/agent_session.py` runs the full lifecycle — remember, recall, consolidate, forget — offline.

## What it actually does

Four things a vector store doesn't:

- **Activation, not just similarity.** Every memory has a base-level activation (ACT-R; Anderson & Schooler, 1991) that rises with use and decays as a power law of time. Retrieval combines relevance, importance (1–10 poignancy, per Generative Agents), and recency — normalised and weighted, so importance on a 1–10 scale can't swamp cosine on a 0–1 scale.
- **Association and spreading.** New memories auto-link to the ones they resemble; the association graph builds itself. At recall, activation spreads one hop across those links, so pulling one memory surfaces its neighbours. Retrieving memories together strengthens their link (Hebb).
- **Consolidation.** Clustered episodes get distilled into semantic memories with provenance back to their sources — the agent-side of what sleep does for a brain, "reflection" in the Generative Agents sense.
- **Forgetting.** Episodes fade on an Ebbinghaus curve and get evicted when retention drops — unless they're important or well-connected. A store that only grows is a log, and it rots the same way an over-full context does.

The maths, with citations, is in [docs/the-math.md](docs/the-math.md). The full picture is [docs/architecture.md](docs/architecture.md).

## Where it sits

| | vector store / RAG | storage layer (mem0, graphiti) | **mtrace** |
|---|---|---|---|
| retrieval | cosine similarity | similarity + filters | relevance × importance × recency + spreading |
| memories strengthen with use | no | no | yes (reinforcement) |
| memories fade / get forgotten | no | rarely | yes (forgetting curve) |
| associations between memories | no | graph edges (manual/extracted) | self-building + Hebbian |
| episodes → distilled facts | no | some | consolidation with provenance |
| dependencies | vector db + model | db + model | none (model optional) |

It's not a competitor to a vector database — it's the activation model that sits on top of one. Swap the built-in lexical embedder for real embeddings and you keep the whole architecture; you just get semantic relevance feeding the same scoring.

## CLI

```
mtrace remember "the friday deploy caused an outage" --tag incident
mtrace recall "production outage"
mtrace consolidate
mtrace forget --dry-run
mtrace inspect 1          # activation breakdown: base-level, recency, retention, links
```

`inspect` prints the numbers most systems hide — why a memory is or isn't available right now.

## Pluggable where it counts

Two interfaces, one method each, both with a working default:

- **`Embedder`** — built-in is a dependency-free hashed bag-of-words (lexical). Plug a sentence-transformer or an embeddings API for semantic recall.
- **`Scorer`** — built-in rates importance by a heuristic. Plug an LLM for real poignancy scoring.

Consolidation's synthesiser is pluggable the same way (extractive by default, LLM optional). The architecture doesn't change when you plug them in — the defaults are the floor, not a mock.

## Install and test

```
git clone https://github.com/Roxx0x/mtrace && cd mtrace
pip install -e ".[dev]"
pytest
```

Python 3.9+, standard library. The only optional dependency is `anthropic`, for the LLM backends.

## References

Built on known results, not invented here: Atkinson & Shiffrin (multi-store), Anderson & Schooler / ACT-R (activation), Ebbinghaus (forgetting), Miller (working-memory capacity), and Park et al., *Generative Agents* (the relevance/importance/recency retrieval and reflection). Full list in [docs/references.md](docs/references.md).

MIT.
