<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/logo-dark.svg">
  <img src="docs/assets/logo-light.svg" alt="tidbit" width="280">
</picture>

### Capture anything into structured Markdown notes and training-ready JSONL.

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-3776AB.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org)
[![Mypy: strict](https://img.shields.io/badge/mypy-strict-2a6db4.svg?style=flat-square)](http://mypy-lang.org)
[![Tests: 207](https://img.shields.io/badge/tests-207%20passing-brightgreen.svg?style=flat-square)](#reliability)
[![MCP: server](https://img.shields.io/badge/MCP-server-8b5cf6.svg?style=flat-square)](https://modelcontextprotocol.io)

<br>

<img src="docs/assets/hero.svg" alt="Terminal demo: tidbit captures a research paper into a Markdown note and a JSONL log entry" width="100%">

</div>

<br>

You define a YAML schema with the fields you care about. You point `tidbit` at a URL, a PDF, an ebook, a screenshot, or your clipboard. It hands back a Markdown note with exactly those fields filled in by an LLM, plus a JSONL log line containing the raw source and the extracted fields, ready for downstream tooling, retrieval, or fine-tuning.

No database. No server. No background daemon. One command, plain files, your choice of model.

```bash
pipx install tidbit
export ANTHROPIC_API_KEY=sk-ant-...
tidbit capture https://example.com/paper --preset research-paper
```

---

## Why

You read a paper. You paste it into an LLM. You get a summary. You close the tab. Two weeks later you need the methodology section and the specific numbers. Gone.

`tidbit` fixes that without becoming yet another note-taking app. You stay in your existing editor (Obsidian, Logseq, vim, VS Code, whatever) and `tidbit` becomes the layer that turns ephemeral content into structured Markdown that fits the workflow you already have.

It does two things at once, from a single capture:

> **Builds your knowledge base.** Define `for research papers, extract title, authors, methodology, findings, limitations` once in a YAML file. Every paper you capture afterwards has the same shape. Two hundred notes later you can grep across all of them by field because they all match.

> **Builds a training dataset.** Every capture also writes a JSONL row containing the raw input and the extracted fields. Over time this becomes a domain-specific dataset of `(content, structured output)` pairs. Use it for evals, retrieval, or fine-tuning a small local model on your exact extraction patterns.

You don't have to choose between the two. You get both for free, on every capture.

---

## Quick start

```bash
# 1. Install
pipx install tidbit

# 2. Pick any one backend
export ANTHROPIC_API_KEY=sk-ant-...                  # Claude (recommended)
export OPENAI_API_KEY=sk-...                         # OpenAI
export OPENAI_BASE_URL=http://localhost:11434/v1     # Ollama (local, free)
export GROQ_API_KEY=gsk-...                          # Groq (fast)

# 3. Capture
tidbit capture https://example.com/blog-post
tidbit capture ~/Downloads/paper.pdf --preset research-paper
tidbit capture ~/Books/novel.epub --preset book
tidbit capture clipboard

# 4. Or capture everything at once
tidbit batch ~/Downloads/conference-papers/ --preset research-paper
```

That's it. Nothing else to install or configure.

---

## What it captures

| Input | How it's processed |
|---|---|
| **URL** | Trafilatura local extraction (default), or `--reader jina` for the hosted Jina Reader fallback on JS-heavy pages |
| **PDF** | pdfplumber for clean multi-column extraction (academic papers), pypdf fallback, embedded metadata included in the prompt |
| **EPUB** | ebooklib + BeautifulSoup, full Dublin Core metadata, per-chapter markers preserved |
| **Image** | PIL with downscale pipeline (max 2000px long edge, max 5MB), routed to your backend's vision model |
| **Clipboard** | Auto-detects text vs image (pyperclip + PIL.ImageGrab) |
| **stdin** | `curl https://… \| tidbit pipe --preset tech-article` |
| **Folder** | `tidbit batch ~/Downloads/papers --preset research-paper` |

Scanned PDFs with no embedded text and DRM-protected EPUBs are not extracted directly. For scanned PDFs, screenshot the page and use the image path. Your vision model will read it. `tidbit` will not attempt to circumvent DRM.

---

## More than just capture

`tidbit` is built around a small set of commands you can compose with the rest of your shell:

```bash
# Preview what an extraction would look like, no API call, no cost
tidbit capture https://example.com --dry-run

# Browse what's currently in your inbox
tidbit inbox

# Show what you've captured recently
tidbit recap --since 7d

# Promote a captured note from the inbox into your real vault
tidbit promote note.md --to ~/Notes/research/papers.md
```

The inbox-and-promote workflow is what keeps `tidbit` from quietly polluting your vault. Captures land in an inbox folder. You review them. You promote the ones worth keeping, into the file in your vault where they actually belong. Everything else stays in the inbox until you decide what to do with it. The JSONL log captures every attempt regardless.

---

## Presets define what you extract

A preset is a small YAML file. The schema is the contract: the LLM has to fill it in or the capture fails loudly.

```yaml
name: research-paper
description: Academic papers and preprints

schema:
  title: string
  authors: list[string]
  methodology: string
  findings: list[string]
  limitations: string?
  tags: list[string]

prompt_hint: |
  Focus on the actual claims and contributions.
  Skip marketing language and acknowledgements.
  If the content is not a research paper, set title
  to "not_a_research_paper" and leave other fields empty.

vault:
  inbox: ~/Notes/inbox
  jsonl: ~/Notes/tidbit-log.jsonl
```

The bundled presets cover most common cases:

`general`  ·  `research-paper`  ·  `tech-article`  ·  `book`  ·  `tutorial`  ·  `tool-review`  ·  `security-finding`  ·  `pentest-finding`  ·  `threat-intel`

Create your own with `tidbit preset new <name>`. Every capture validates the LLM's output against the schema and retries with a stricter, schema-aware prompt before giving up.

---

## What you actually get

A captured note in your inbox folder, ready for any Markdown editor:

```markdown
---
preset: research-paper
source: https://example.com/paper
captured_at: 2026-04-09T10:14:22Z
source_hash: a3f8b2c1
title: Efficient Attention via Dynamic Sparsity
authors:
  - Maria Chen
  - James Park
  - Jordan Lee
tags:
  - attention
  - efficiency
  - transformers
---

# Efficient Attention via Dynamic Sparsity

## Methodology
We introduce a learned routing mechanism that selects a sparse subset of
key-value pairs for each query token, reducing attention compute from
quadratic to near-linear in sequence length…

## Findings
- 3.2× speedup on long-context benchmarks at comparable quality
- Routing overhead amortizes after sequence length 2k
- Compatible with FlashAttention kernels without modification

## Limitations
Routing decisions are fixed at inference time; the paper does not
explore dynamic re-routing during generation…

## Raw source
<the full extracted text appears here, so you can always see what the LLM read>
```

And one row appended to `~/Notes/tidbit-log.jsonl`:

```json
{"preset":"research-paper","source":"https://example.com/paper","captured_at":"2026-04-09T10:14:22Z","source_hash":"a3f8b2c1","raw_content":"Efficient Attention via Dynamic Sparsity\nMaria Chen, James Park, Jordan Lee\n\nAbstract: …","extracted":{"title":"Efficient Attention via Dynamic Sparsity","authors":["Maria Chen","James Park","Jordan Lee"],"methodology":"We introduce a learned routing mechanism…","findings":["3.2x speedup on long-context benchmarks at comparable quality","Routing overhead amortizes after sequence length 2k","Compatible with FlashAttention kernels without modification"],"limitations":"Routing decisions are fixed at inference time…","tags":["attention","efficiency","transformers"]}}
```

The Markdown is for you. The JSONL is for your tools.

---

## MCP server

`tidbit` ships an MCP server so AI assistants can capture into your structured notes mid-conversation.

```json
{
  "mcpServers": {
    "tidbit": { "command": "tidbit", "args": ["mcp"] }
  }
}
```

Drop that into Claude Desktop, Cursor, Cline, Continue, Windsurf, or any other MCP client. Then in your conversation:

> Save this article with the research-paper preset.

Same presets, same vault, same JSONL log as the CLI. Captures land in the same inbox, ready to be promoted or grepped like any other note.

---

## What `tidbit` is not

Not a bookmark manager. Not a read-it-later app. Not a RAG system. Not a note-taking app.

You give it content and a schema. It gives you structured Markdown and a JSONL record. What you do with those files is up to you. `tidbit` is for when capture needs to be programmable: a cron job, a `curl` pipe, a folder of PDFs, a Cursor session, or a Claude Desktop conversation.

---

## Reliability

`tidbit` treats every LLM response as untrusted. Every extraction is:

- **Validated against the preset schema.** Required fields must be present, list fields must be lists, type mismatches surface as a structured error and trigger one stricter retry with a schema-aware prompt before failing loudly. No silent type coercion, no missing fields written to disk.
- **Atomically written.** Temp file plus rename, so a crash mid-write never leaves a half-written note in your inbox.
- **Deduplicated by content hash.** Re-running `tidbit capture` on the same URL never creates a duplicate. The dedup discriminator is the preset, so the same article under two different presets correctly produces two notes.
- **Logged on failure.** Bad responses get written to `~/.config/tidbit/failed/` for debugging, so you never lose the input when something goes wrong.
- **Size-guarded.** PDFs and EPUBs that would blow the model's context window are rejected with a clear message instead of producing a garbage extraction.

Strict types, 207 tests, mypy `--strict` clean, ruff clean, zero warnings. About 4,000 lines of source and 3,000 lines of tests.

---

## Install

```bash
# Recommended
pipx install tidbit

# Or, into your active environment
pip install --user tidbit
```

From source:

```bash
git clone https://github.com/phanii9/Tidbit && cd Tidbit
pip install -e ".[dev]"
pytest && mypy --strict src/tidbit && ruff check src tests
```

Requires Python 3.10 or newer. No system-level dependencies.

---

## Roadmap

- [ ] YouTube transcript capture as a built-in extractor
- [ ] Defuddle as an opt-in URL backend for JS-heavy pages
- [ ] Preset gallery and community sharing
- [ ] Eval harness for measuring extraction quality on golden inputs
- [ ] Long-form chunking for books and long PDFs

**Permanent non-goals:** chat interface over notes, RAG framework, vector database, multi-user mode, cloud-hosted SaaS, browser extension, mobile app. `tidbit` stays a CLI plus an MCP server that produces plain files. Everything else is somebody else's tool.

---

## Contributing

Issues, feature requests, and pull requests welcome. The codebase is small, strictly typed, and aggressively tested. Bug reports with a reproducible example are the highest-leverage contribution you can make.

## License

[MIT](LICENSE)
