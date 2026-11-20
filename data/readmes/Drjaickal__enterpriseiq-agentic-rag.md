# EnterpriseIQ — Agentic RAG Knowledge Intelligence

<p align="center">
  <strong>Turn documents into a searchable, evidence-grounded knowledge base.</strong><br/>
  Upload PDF, DOCX and TXT files. Ask natural-language questions. Retrieve relevant passages and generate answers grounded in those documents.
</p>

<p align="center">
  <a href="https://enterpriseiq-agentic-rag.vercel.app/">Live application</a> ·
  <a href="https://enterpriseiq-agentic-rag.onrender.com/health">API health</a> ·
  <a href="https://github.com/Drjaickal/enterpriseiq-agentic-rag">Source code</a>
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.x-3776AB?logo=python"/>
  <img alt="FastAPI" src="https://img.shields.io/badge/API-FastAPI-009688?logo=fastapi"/>
  <img alt="PostgreSQL" src="https://img.shields.io/badge/Database-PostgreSQL-4169E1?logo=postgresql"/>
  <img alt="pgvector" src="https://img.shields.io/badge/Vector%20Search-pgvector-336791"/>
  <img alt="Gemini" src="https://img.shields.io/badge/LLM-Google%20Gemini-8E75B2"/>
  <img alt="Render" src="https://img.shields.io/badge/Backend-Render-46E3B7"/>
  <img alt="Vercel" src="https://img.shields.io/badge/Frontend-Vercel-000000"/>
  <img alt="Status" src="https://img.shields.io/badge/Project-Actively%20Improving-blue"/>
</p>

---

## Contents
- [Overview](#what-is-enterpriseiq)
- [Why EnterpriseIQ?](#why-build-it)
- [Capabilities](#core-capabilities)
- [Architecture and data flow](#architecture)
- [Document ingestion](#how-document-ingestion-works)
- [Question answering](#how-question-answering-works)
- [Database design](#database-design)
- [Technology stack](#technology-stack)
- [API reference](#api-reference)
- [Local setup](#run-locally)
- [Configuration](#environment-configuration)
- [Deployment](#deployment)
- [Engineering challenges and findings](#engineering-challenges-and-findings)
- [Known limitations](#known-limitations-and-current-work)
- [Roadmap](#roadmap)
- [Learning outcomes](#learning-outcomes)

## What is EnterpriseIQ?

EnterpriseIQ is a document-grounded question-answering application built around a Retrieval-Augmented Generation (RAG) pipeline. Users upload business or personal documents and ask questions in natural language. The backend extracts text, splits it into passages, converts passages into vector embeddings, stores them in PostgreSQL with pgvector, retrieves relevant passages for a question, and asks a language model to answer using that retrieved context.

**Project status:** deployed and actively improving. This repository contains a working RAG foundation. Advanced features in the roadmap are not claimed as completed.

## Why build it?

Traditional document search often depends on exact words. A user may ask “Where will I be based?” while a document says “work location”. Semantic retrieval can connect related meanings even when wording differs.

EnterpriseIQ demonstrates the end-to-end path from raw files to grounded answers:

1. Ingest common document formats.
2. Extract text and available source metadata.
3. Split long text into retrieval-sized chunks.
4. Embed chunks into 768-dimensional vectors.
5. Store text, metadata and vectors in PostgreSQL/pgvector.
6. Embed a user's question and retrieve the closest passages.
7. Generate an answer constrained to the retrieved context.
8. Return source identifiers and similarity information.

It is valuable for learning because each stage is visible and replaceable. It is a production-minded foundation because it uses an API boundary, relational storage, vector retrieval, configurable model providers, input validation and cloud deployment. Real production use still requires the security, reliability, evaluation and storage work documented below.

## Core capabilities

| Capability | Current implementation |
|---|---|
| PDF ingestion | PyMuPDF extracts text page by page and records page numbers |
| DOCX ingestion | python-docx extracts paragraphs and table rows |
| TXT ingestion | UTF-8 with CP1252 fallback |
| Recursive chunking | Paragraph, line and space separators |
| Chunk overlap | Default 1,000-character chunks; 150-character overlap |
| Embeddings | Gemini or Ollama, selected through environment variables |
| Vector storage | PostgreSQL + pgvector; 768-dimensional vectors |
| Retrieval | Cosine-distance nearest-neighbour search; configurable top-k |
| Generation | Gemini or Ollama, selected through environment variables |
| Grounding | Prompt instructs model to use supplied document context only |
| Sources | Document ID, chunk index and similarity in response |
| Duplicate detection | SHA-256 content hash |
| API | FastAPI health, stats, document listing, upload and chat routes |

## Architecture

### High-level system architecture

```mermaid
flowchart LR
    U[User] --> FE[EnterpriseIQ Web UI]
    FE -->|HTTPS / JSON / multipart| API[FastAPI Backend]
    API --> ING[Document Ingestion]
    API --> CHAT[Question Answering]
    ING --> EXT[PDF / DOCX / TXT Extractors]
    EXT --> CH[Recursive Chunker]
    CH --> EMB[Embedding Provider]
    EMB --> VS[(PostgreSQL + pgvector)]
    CHAT --> QEMB[Query Embedding]
    QEMB --> VS
    VS --> RET[Top-K Relevant Chunks]
    RET --> PROMPT[Grounded Prompt Builder]
    PROMPT --> LLM[Gemini or Ollama LLM]
    LLM --> ANS[Answer + Source References]
    ANS --> FE
```

### Backend modules

| Module | Responsibility |
|---|---|
| `apps/api/app/main.py` | FastAPI app, CORS, validation, upload and chat routes |
| `ai_engine/ingestion/document_processor.py` | Loader selection, SHA-256 hash and metadata |
| `ai_engine/ingestion/*_loader.py` | Format-specific text extraction |
| `ai_engine/chunking/recursive_chunker.py` | Recursive splitting and overlap |
| `ai_engine/ingestion/ingestion_service.py` | Ingestion orchestration and embedding selection |
| `ai_engine/embeddings/gemini_embeddings.py` | Gemini embedding client |
| `ai_engine/embeddings/ollama_embeddings.py` | Ollama embedding client |
| `ai_engine/embeddings/vector_store.py` | Document/chunk persistence and vector search |
| `ai_engine/retrieval/semantic_search.py` | Query embedding and relevant-chunk retrieval |
| `ai_engine/agents/rag_agent.py` | Context construction, generation and source-number validation |
| `database/models.py` | SQLAlchemy document and chunk models |
| `database/connection.py` | SQLAlchemy engine and database sessions |

## How document ingestion works

The API accepts PDF, DOCX and TXT files and enforces a 20 MB upload limit. It strips directory components from the original filename and stores the upload under a generated filename.

```mermaid
flowchart TD
    A[Upload file] --> B{Extension allowed?}
    B -- No --> E[HTTP 400]
    B -- Yes --> C{Empty or over 20 MB?}
    C -- Invalid --> F[HTTP 400 / 413]
    C -- Valid --> D[Save upload]
    D --> G[Select format loader]
    G --> H[Extract text and metadata]
    H --> I[Compute SHA-256]
    I --> J{Content already exists?}
    J -- Yes --> K[Return already_exists]
    J -- No --> L[Recursive chunking]
    L --> M[Select Gemini or Ollama]
    M --> N[Generate 768-D embeddings]
    N --> O[Store document and chunks]
    O --> P[Commit transaction]
    P --> Q[Return ingestion result]
```

### Ingestion details

1. `.pdf`, `.docx` and `.txt` are routed to dedicated loaders.
2. PDF extraction processes each non-empty page and preserves its page number.
3. DOCX extraction collects non-empty paragraphs and table rows. DOCX page numbers are not currently available.
4. TXT extraction tries UTF-8, then CP1252.
5. SHA-256 of the file bytes becomes the document ID/content hash.
6. Recursive chunking prioritizes paragraph breaks, then line breaks, then spaces. Defaults: 1,000 characters and 150 characters of overlap.
7. The selected embedding provider converts each chunk to a 768-dimensional vector.
8. The document and chunk rows are committed to PostgreSQL. A failed commit triggers rollback.

Duplicate detection is content-based: renaming an identical file does not create a new logical document.

## How question answering works

A RAG system has two distinct model tasks:

- **Embedding model:** converts the question into a vector so the database can find semantically similar passages.
- **Generation model (LLM):** receives the question and retrieved passages, then writes the answer.

The LLM does not search the database itself in this implementation. Retrieval happens in the backend before generation.

```mermaid
sequenceDiagram
    actor User
    participant UI as Web UI
    participant API as FastAPI
    participant Search as Semantic Search
    participant Embed as Embedding Model
    participant DB as PostgreSQL / pgvector
    participant LLM as Generation Model

    User->>UI: Ask a question
    UI->>API: POST /api/v1/chat
    API->>API: Validate question and top_k
    API->>Search: semantic_search(question, top_k)
    Search->>Embed: Embed the question
    Embed-->>Search: 768-dimensional query vector
    Search->>DB: Order chunks by cosine distance
    DB-->>Search: Top-k matching chunks
    Search-->>API: Text, metadata, similarity
    API->>LLM: Question + retrieved context + grounding rules
    LLM-->>API: Answer with [Source N] labels
    API->>API: Remove invalid source numbers
    API-->>UI: Answer, sources, model, retrieved count
    UI-->>User: Display answer
```

### Retrieval and generation, step by step

1. The API validates a non-empty question up to 4,000 characters. `top_k` is constrained to 1–10.
2. `semantic_search` selects Gemini or Ollama using `EMBEDDING_PROVIDER`.
3. The embedding client converts the question into a 768-dimensional vector.
4. `VectorStore.search` calculates cosine distance between the query and stored chunk vectors, orders by nearest distance and returns top-k rows.
5. The RAG agent builds labelled context blocks such as `[Source 1: Document ... - Chunk ...]`.
6. The system prompt instructs the generation model to use only supplied context, avoid inventing facts, acknowledge missing information and cite factual statements.
7. Gemini or Ollama generates the answer.
8. The backend removes citation labels whose source numbers are outside the retrieved source range.
9. The API returns the answer, source metadata, model and retrieved-chunk count.

**Citation caveat:** validating source numbers prevents references to non-existent sources, but does not independently prove that a citation supports its sentence. Citation entailment needs a separate evaluation layer.

## Database design

The current schema contains two primary tables:

```mermaid
erDiagram
    DOCUMENTS ||--o{ DOCUMENT_CHUNKS : contains
    DOCUMENTS {
        varchar id PK
        varchar filename
        varchar file_type
        varchar content_hash UK
        timestamptz created_at
    }
    DOCUMENT_CHUNKS {
        varchar id PK
        varchar document_id FK
        integer chunk_index
        text content
        vector_768 embedding
        json metadata_json
    }
```

- `documents.id` is the SHA-256 content hash.
- `documents.content_hash` is unique.
- `document_chunks.document_id` references the parent document.
- Each chunk stores text, index, a 768-dimensional embedding and JSON metadata.
- The ORM relationship is configured with delete-orphan cascading.

The vector query uses cosine distance and returns similarity as `1 - distance`.

## Technology stack

| Layer | Technology |
|---|---|
| API | Python, FastAPI, Pydantic |
| ORM | SQLAlchemy |
| Database | PostgreSQL |
| Vector extension | pgvector |
| Embedding providers | Google Gemini Embeddings, Ollama |
| Generation providers | Google Gemini, Ollama |
| PDF parser | PyMuPDF |
| DOCX parser | python-docx |
| HTTP client | httpx |
| Local database | Docker Compose + pgvector PostgreSQL image |
| Frontend hosting | Vercel |
| Backend hosting | Render |
| Database hosting | Neon PostgreSQL |

## API reference

Base backend URL: `https://enterpriseiq-agentic-rag.onrender.com`

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | API identity and running status |
| GET | `/health` | Health check |
| GET | `/api/v1/stats` | Document and indexed-chunk counts |
| GET | `/api/v1/documents` | List stored documents |
| POST | `/api/v1/documents/upload` | Upload and ingest a file |
| POST | `/api/v1/chat` | Ask a question over indexed documents |

### Chat request

```json
{
  "question": "What is the role mentioned in the offer letter?",
  "top_k": 3
}
```

### Upload request

Send multipart/form-data with a `file` field. Supported extensions: PDF, DOCX and TXT. Maximum file size: 20 MB.

### Chat response shape

```json
{
  "status": "success",
  "question": "What is the role mentioned in the offer letter?",
  "answer": "The retrieved document states ... [Source 1]",
  "sources": [
    {
      "source_id": "Document <document-id> - Chunk 0",
      "document_id": "<document-id>",
      "chunk_index": 0,
      "similarity": 0.82
    }
  ],
  "model": "<configured-generation-model>",
  "retrieved_chunks": 3
}
```

Values above are illustrative. Actual source IDs, similarity, model names and answers depend on runtime data and configuration.

## Run locally

### Prerequisites

- Python 3.10+ (use a version supported by installed dependencies)
- Git
- Docker Desktop for local PostgreSQL/pgvector, or a PostgreSQL database with pgvector enabled
- Gemini API key for Gemini mode, or a running Ollama server for local mode

### 1. Clone

```bash
git clone https://github.com/Drjaickal/enterpriseiq-agentic-rag.git
cd enterpriseiq-agentic-rag
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv apps/api/.venv
.\apps\api\.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
python -m venv apps/api/.venv
source apps/api/.venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r apps/api/requirements.txt
```

### 4. Start local PostgreSQL with pgvector

```bash
docker compose up -d postgres
```

The compose file exposes PostgreSQL on port 5432. Its example development password must never be reused in a public or production environment.

### 5. Configure environment variables

Create a `.env` file in the repository root. See the configuration section. Never commit this file.

### 6. Initialize the database

```powershell
python -m database.init_db
```

### 7. Start the API

Run from the repository root:

```powershell
$env:PYTHONPATH = "."
uvicorn apps.api.app.main:app --reload --host 127.0.0.1 --port 8000
```

Interactive API docs: `http://127.0.0.1:8000/docs`  
Health endpoint: `http://127.0.0.1:8000/health`

## Environment configuration

Set variables in local `.env` or in your hosting provider's environment-variable settings. Never paste API keys into source code, screenshots, issues or commits.

| Variable | Purpose | Example / default |
|---|---|---|
| `DATABASE_URL` | PostgreSQL connection string | Required |
| `EMBEDDING_PROVIDER` | Embedding backend | `gemini` or `ollama` |
| `GEMINI_API_KEY` | Gemini authentication | Required for Gemini |
| `GEMINI_EMBEDDING_MODEL` | Gemini embedding model | `gemini-embedding-001` |
| `OLLAMA_EMBEDDING_MODEL` | Ollama embedding model | `nomic-embed-text` |
| `OLLAMA_BASE_URL` | Ollama server URL | `http://localhost:11434` |
| `GENERATION_PROVIDER` | Generation backend | `gemini` or `ollama` |
| `GEMINI_GENERATION_MODEL` | Gemini generation model | Configure a model available to your API key |
| `OLLAMA_GENERATION_MODEL` | Ollama generation model | `qwen2.5:3b` |

Example local Gemini configuration (use placeholders locally; do not commit real secrets):

```dotenv
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST:5432/DATABASE
EMBEDDING_PROVIDER=gemini
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
GEMINI_EMBEDDING_MODEL=gemini-embedding-001
GENERATION_PROVIDER=gemini
GEMINI_GENERATION_MODEL=YOUR_AVAILABLE_GEMINI_MODEL
```

For Ollama mode, set the provider variables to `ollama`, configure its base URL, and ensure the selected models are installed and reachable from the backend.

## Deployment

The current public deployment is split across services:

| Component | Hosting |
|---|---|
| Web application | [Vercel](https://enterpriseiq-agentic-rag.vercel.app/) |
| FastAPI backend | [Render](https://enterpriseiq-agentic-rag.onrender.com) |
| PostgreSQL + pgvector | Neon |

Render build command:

```bash
pip install -r apps/api/requirements.txt
```

Render start command:

```bash
PYTHONPATH=. uvicorn apps.api.app.main:app --host 0.0.0.0 --port $PORT
```

Configure environment variables in the hosting dashboard. The frontend must point its API base URL to the deployed backend (for example, `NEXT_PUBLIC_API_URL`). Do not commit `.env`.

**Free-tier note:** free hosting plans may sleep, have resource limits or change their terms. External model APIs may have quotas, rate limits and temporary availability errors. This project does not guarantee zero-cost or uninterrupted operation.

## Engineering challenges and findings

These are real engineering lessons from implementing and deploying the project.

### 1. A hosted backend cannot assume a local model server exists

The original ingestion path instantiated the Ollama embedding client directly. A cloud host without an Ollama service listening at `localhost:11434` returned a connection-refused error during upload.

**Finding and fix:** ingestion now selects its embedding client from `EMBEDDING_PROVIDER`, matching the provider-selection pattern used by semantic retrieval. Local Ollama development and hosted Gemini embeddings can use the same ingestion interface.

### 2. Embedding dimensions must match end to end

The Gemini embedding client requests 768 dimensions. The database column is `Vector(768)`, and vector search rejects query vectors whose length is not 768.

**Finding:** ingestion vectors, query vectors and the database vector column must share the same model/dimensionality contract. A future model or dimension change requires a re-embedding and migration plan.

### 3. Database schema readiness is separate from API health

A web process can start while expected database tables are missing. A successful health response alone does not prove schema initialization or vector queries are healthy.

**Finding:** database initialization and database-aware readiness checks belong in a reliable deployment workflow.

### 4. Model availability is an external dependency

A valid API key and correct application code do not guarantee that a hosted model is available at every moment. The generation provider can return temporary 503/UNAVAILABLE errors during high demand.

**Finding:** verify model IDs against the provider account and current availability. Production hardening should add bounded retries with backoff, configurable fallback, timeouts and clear user-facing errors. A fallback should only be enabled when its model and quota are configured.

### 5. Retrieval quality depends on chunking and metadata

Very large chunks can dilute relevance; very small chunks can lose context. Overlap helps preserve context across boundaries but increases vector count.

**Finding:** chunk size, overlap, top-k and source metadata should be evaluated against representative questions rather than selected only by intuition.

### 6. Grounding instructions are not a complete guarantee

The prompt limits answers to retrieved context and asks for citations. The code also strips invalid source numbers.

**Finding:** prompt constraints and citation-number checks improve traceability, but an evaluation suite is still needed to measure factual correctness, citation precision, retrieval recall and unsupported-answer rates.

## Known limitations and current work

This section separates implemented behaviour from future work.

- **Gemini 503 errors:** generation can be temporarily unavailable. Configurable fallback and retry handling are planned, not yet implemented.
- **Temporary local upload storage:** uploads are written to `storage/uploads`. This is not durable object storage on ephemeral hosting. Managed object storage or a Drive integration is future work.
- **No API authentication/authorization:** inspected routes do not yet enforce login, tenant isolation or per-document permissions. Do not use this deployment for confidential multi-customer data until access control is implemented and tested.
- **No OCR pipeline:** scanned/image-only PDFs may yield little or no extracted text.
- **DOCX page mapping:** paragraphs and tables are extracted without page-level source locations.
- **Synchronous processing:** ingestion and model calls run in the request path. Larger workloads may need background jobs and a queue.
- **Vector-only retrieval:** current semantic search uses pgvector cosine distance. Hybrid keyword/vector retrieval and cross-encoder reranking are roadmap items, not current features.
- **No formal RAG evaluation suite:** retrieval and answer quality need repeatable datasets and metrics.
- **Syntactic citation validation:** invalid source numbers are removed, but citation entailment is not independently checked.
- **No rate limiting in inspected routes:** add quotas, throttling and stronger upload protections before broad public use.
- **Frontend model label may be static:** the UI has displayed a Qwen/Ollama label even when hosted environment variables select Gemini. The UI should derive provider status from a backend configuration endpoint.
- **No autonomous tool-using agent loop:** the current question-answering path is retrieval followed by generation. Planning, tool selection and multi-step agent execution remain future work.

## Roadmap

### Reliability and correctness
- [ ] Verify configured model IDs at startup and expose provider status safely.
- [ ] Add bounded retries, exponential backoff, timeouts and configurable model fallback.
- [ ] Add database readiness checks and structured logs.
- [ ] Return richer source metadata, including filename and page number where available.
- [ ] Add citation-support validation.

### Retrieval quality
- [ ] Add hybrid keyword + vector retrieval.
- [ ] Add cross-encoder reranking.
- [ ] Add metadata filters and configurable similarity thresholds.
- [ ] Evaluate chunk size, overlap and top-k using a labelled question set.
- [ ] Add retrieval and generation evaluation metrics.

### Product and enterprise capabilities
- [ ] Add authentication and role-based access control.
- [ ] Add tenant/workspace isolation and per-document permissions.
- [ ] Add durable object storage (for example, Google Cloud Storage; Drive integration can be explored for personal/workspace workflows).
- [ ] Move ingestion to background jobs.
- [ ] Add document versioning, deletion and re-indexing.
- [ ] Add usage analytics, rate limits and audit logs.

### Platform engineering
- [ ] Add automated tests and CI checks.
- [ ] Add Docker packaging for the API.
- [ ] Add monitoring, tracing and error reporting.
- [ ] Add load tests and deployment health gates.

## Learning outcomes

This project provides hands-on experience with:

- Retrieval-Augmented Generation architecture.
- Embedding models and vector dimensionality.
- Semantic similarity and cosine-distance retrieval.
- PostgreSQL, pgvector, SQLAlchemy and relational modelling.
- Document parsing, recursive chunking and metadata design.
- Prompt construction, context grounding and source references.
- FastAPI request validation and API design.
- Environment-based provider configuration.
- Debugging cloud-only failures versus local development.
- Deploying a multi-service application with Vercel, Render and Neon.

## Contributing

Contributions and suggestions are welcome. Before opening a pull request:

1. Reproduce the issue and include minimal steps.
2. Add or update tests for changed behaviour.
3. Keep secrets and local environment files out of commits.
4. Update this README when API behaviour, configuration or architecture changes.

For bugs or feature ideas, open a GitHub issue with expected behaviour, actual behaviour and relevant sanitized logs.

---

<p align="center">
  <strong>EnterpriseIQ — make every document queryable, and every answer traceable.</strong><br/>
  Built by
  <a href="https://github.com/Drjaickal">Avijit Acharya</a>
  ·
  <a href="https://www.linkedin.com/in/avijit-acharya-532a76209/">LinkedIn</a>
</p>
