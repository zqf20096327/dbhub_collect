# rag-accordion-demo

Reproducible evidence that **retrieval-aware prompt design** — not Q&A conversion in itself — is what makes synthetic Q&A beat raw markdown in RAG.

## TL;DR

| KB | Source | Accuracy (n=3) |
|---|---|---|
| `mdx_direct` | Raw markdown | **72%** |
| `naive_facts` | Q&A from a generic prompt | **75%** |
| `best_facts` | Q&A from a retrieval-aware prompt | **92%** |

Three knowledge bases, same source document, same embedding model, same chatbot LLM, same questions, three independent runs. Naive Q&A conversion gives you **+3 pt over raw markdown — but that's run variance, not a retrieval gain**: the genuine fixes and breaks cancel exactly (Q2/Q6 fixed, Q4/Q12 broken), and the residual +3 pt traces to a single question where the raw-markdown baseline happened to wobble on one run (see [results/summary.md](results/summary.md)). The real gain (**+17 pt over naive, +20 pt over raw markdown**) comes from the prompt design (chiefly Rules 4–5). Documented in [prompt_engineering.md](prompt_engineering.md).

Full numbers and per-question breakdown: [results/summary.md](results/summary.md).

## The accordion pattern

To produce one line of JSONL per Q&A fact from any document, this repo uses a two-stage StructFlow pipeline:

```
document ─► Stage 1 (segmenter)     ─► {sections: [...]}
            Splits the document into self-contained sections.

            Flatten sections         ─► one section per JSONL line
            (Stage 1 output expanded for Stage 2 input)

            Stage 2 (extractor)      ─► {facts: [...]} per section
            Creates Q&A pairs from each section.

            Flatten facts            ─► one fact per JSONL line
            (Stage 2 output expanded for the final KB)
```

The "accordion" name comes from the shape: `1 doc → N sections → M facts`, with a flatten step after each Stage to expand array outputs into line-per-record JSONL (sections.jsonl for Stage 2's input; facts.jsonl for the final KB). Stage 1 and Stage 2 are both [StructFlow](https://gw.portal.ldxhub.io) jobs.

The mechanism is format-agnostic — Stage 1's segmentation rule is the only thing that needs to know your input. This demo segments markdown by `## / ###` headings, but the same pattern works on HTML sections, PDF chapters, DOCX heading styles, or any structured text. For PDF/DOCX/XLSX/PPTX, pair it with LDX hub's [ExtractDoc](https://gw.portal.ldxhub.io) to extract clean text first, then feed that into Stage 1.

**The prompts are what matter.** See [prompts/](prompts/) for the four prompts used (Stage 1 segmenter, Stage 2 best, Stage 2 naive, and the chatbot system prompt that drives answer generation against the attached KB).

## The five prompt design rules

What separates `best_facts` (92%) from `naive_facts` (75%):

1. **Self-contained answers** — each fact stands alone, no cross-references
2. **Developer-friendly question phrasing** — `How do I...?`, `What is the default value of...?`
3. **Exact preservation of technical identifiers** — API names, endpoint paths, parameter names, enum values stay verbatim
4. **Service-specific facts for cross-category information** — when a section discusses statuses, errors, or behaviors tied to a specific service, generate a service-scoped fact with the service name in both question and answer (this is what resolves Q12; Q4 is resolved by Rule 5)
5. **Deliberate keyword design** — 3–7 short terms per fact (service names, parameters, concepts)

*In this validation, Rules 4 and 5 produced the entire +17 pt gain over naive (Q12 and Q4 respectively); Rules 1–3 measured zero net contribution because the Stage 2 model already satisfied them at temperature 0. They are robustness insurance for when the model, temperature, or input changes — see [prompt_engineering.md](prompt_engineering.md) for the full attribution.*

Each rule is explained, with examples and the failure mode it prevents, in [prompt_engineering.md](prompt_engineering.md).

## Tech stack

- **Document AI**: [LDX hub](https://gw.portal.ldxhub.io) (StructFlow — accordion implementation)
- **RAG platform**: Dify Cloud
  - Vector storage: TiDB Cloud Starter ([PingCAP case study](https://www.pingcap.com/case-study/dify-consolidates-massive-database-containers-into-one-unified-system-with-tidb/))
  - Embedding: OpenAI `text-embedding-3-large`
  - Retrieval: Hybrid Search (Weighted Score, 0.7 semantic / 0.3 keyword)
- **LLMs**:
  - Chatbot: OpenAI GPT-5.5 (per-query, premium quality)
  - Stage 2 Q&A generation: Google Gemini 3.5 Flash (batch, cost-efficient)

Cross-vendor by design — LDX hub treats LLMs as swappable, so picking the right model per phase is the boring default.

## Repository contents

```
.
├── README.md                  ← you are here
├── prompt_engineering.md      ← the five rules, with examples
├── test_questions.md          ← 12 validation questions
├── prompts/
│   ├── stage1_segmenter.md    ← document segmentation prompt
│   ├── stage2_best.md         ← retrieval-aware Q&A prompt
│   ├── stage2_naive.md        ← generic Q&A prompt (baseline)
│   └── chatbot_system.md      ← chatbot system prompt (answer generation)
├── data/
│   ├── test_en_full.mdx       ← source document (LDX hub portal intro + API ref; internal links like `/signup` and `/api` are preserved as-is from the portal and do not resolve inside this repository)
│   ├── sections.jsonl         ← Stage 1 output, flattened (53 sections, Stage 2 input format)
│   ├── facts_best.txt         ← 82 Q&A facts from stage2_best.md
│   └── facts_naive.txt        ← 78 Q&A facts from stage2_naive.md
├── workflows/
│   └── dify-accordion.yml     ← Dify Workflow template (Stage 1 + Stage 2 + flatten)
└── results/
    ├── summary.md             ← final aggregate, key findings
    ├── mdx_direct/            ← raw-markdown KB runs 1–3
    ├── best_facts/            ← best-prompt KB runs 1–3
    └── naive_facts/           ← naive-prompt KB runs 1–3
```

## Reproducing the validation

1. **Generate the facts**: import `workflows/dify-accordion.yml` into Dify and feed `data/test_en_full.mdx` as input. The workflow ships with `prompts/stage2_best.md` already baked into the Stage 2 system prompt — to reproduce the naive baseline, swap it for `prompts/stage2_naive.md` before running. Output is JSONL — rename to `.txt` for Dify Knowledge upload.
2. **Build the three KBs**: in Dify Cloud, create one Knowledge Base per source (`test_en_full.mdx`, `facts_best.txt`, `facts_naive.txt`) using the chunking and retrieval settings in [results/summary.md](results/summary.md).
3. **Run the questions**: feed the 12 questions from [test_questions.md](test_questions.md) into a Chatbot app, switching the attached KB between runs. Expected per-question pattern matches [results/summary.md](results/summary.md).

## About LDX hub

[LDX hub](https://gw.portal.ldxhub.io) is a document AI gateway that exposes five services through a single API: **StructFlow** (structured generation), **RefineLoop** (XLIFF translation refinement), **RenderOCR** (OCR conversion with layout), **CastDoc** (PDF-to-Office without OCR), and **ExtractDoc** (plain-text extraction). The accordion pattern in this repo is one StructFlow use case among many.

If you want to skip building the workflow yourself, the [LDX hub Dify plugin](https://marketplace.dify.ai/plugins/ldxhub-io/ldxhub) and [n8n nodes](https://www.npmjs.com/package/n8n-nodes-ldxhub) cover StructFlow as a one-step block. MCP access is also available for use from Claude Desktop and other MCP clients.

## Dependencies

The Dify workflow ([`workflows/dify-accordion.yml`](workflows/dify-accordion.yml)) uses two community plugins, both installed automatically when the workflow is imported into Dify:

- **[ldxhub-io/ldxhub](https://marketplace.dify.ai/plugins/ldxhub-io/ldxhub)** — StructFlow tool. Source: [`ldxhub-io/dify-nodes-ldxhub`](https://github.com/ldxhub-io/dify-nodes-ldxhub) (MIT).
- **[kurokobo/file_tools](https://github.com/kurokobo/dify-plugin-collection)** — converts the in-memory string output of each `Code` node into a Dify `File` object that the next StructFlow node can consume (Apache 2.0).

## License

MIT.
