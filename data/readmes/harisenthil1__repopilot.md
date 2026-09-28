# RepoPilot

**An AI code agent that understands a repository, proposes code changes, waits for human approval, and validates patches inside an isolated Docker sandbox.**

RepoPilot combines code-aware retrieval, structured LLM outputs, LangGraph workflows, human-in-the-loop approval, and automated testing to create a controlled software-engineering agent.

Instead of sending an entire repository to an LLM, RepoPilot parses source code into symbols, indexes those symbols with embeddings in PostgreSQL + pgvector, retrieves relevant code for a task, generates a targeted patch, and validates the approved change against the repository's test suite.

## Features

- Clone and inspect GitHub repositories through a FastAPI API
- Parse Python source code into classes, functions, methods, and async functions using the AST
- Generate semantic embeddings for code symbols with SentenceTransformers
- Store and search code embeddings using PostgreSQL + pgvector
- Perform metadata-filtered retrieval by file and symbol type
- Analyze coding tasks with a LangGraph agent
- Generate structured, file-level patch plans with OpenAI
- Validate proposed edits against exact source snippets
- Generate unified diffs without modifying the canonical repository
- Pause execution for human approval using persistent LangGraph interrupts
- Apply approved patches only inside disposable run sandboxes
- Install dependencies and execute repository tests inside Docker
- Run tests without network access and with restricted container permissions
- Detect failed patches, retrieve additional failure-related context, and generate repairs
- Require another human approval before executing repaired patches
- Persist run attempts, test output, patches, and execution scores

## Architecture

```text
                         GitHub Repository
                                │
                                ▼
                       Repository Ingestion
                                │
                                ▼
                         Canonical Workspace
                                │
                                ▼
                         Python AST Scanner
                                │
                                ▼
                     Symbol-Aware Code Chunks
                                │
                                ▼
                       SentenceTransformers
                                │
                                ▼
                     PostgreSQL + pgvector
                                │
                                ▼
                         Semantic Retrieval
                                │
                                ▼
                          LangGraph Agent
                       ┌────────┴────────┐
                       │                 │
                       ▼                 ▼
                 Task Analysis      Code Context
                       │                 │
                       └────────┬────────┘
                                ▼
                     Structured Patch Plan
                                │
                                ▼
                         Unified Diff
                                │
                                ▼
                    Human Approval Interrupt
                                │
                         approved / rejected
                                │
                                ▼
                    Disposable Run Workspace
                                │
                                ▼
                      Restricted Docker Run
                                │
                                ▼
                              pytest
                         ┌──────┴──────┐
                         │             │
                       PASS           FAIL
                         │             │
                         ▼             ▼
                       Score      Failure Retrieval
                         │             │
                         ▼             ▼
                     Complete      Repair Patch
                                       │
                                       ▼
                              Human Approval Again
                                       │
                                       └──────► Retry
```

## Example

RepoPilot was tested against the Flask repository with the task:

> Add a concise docstring to Flask's main CLI entry point explaining that it invokes the Flask command line interface. Do not change its behavior.

The agent retrieved the relevant CLI implementation, generated the following patch, and paused for approval:

```diff
--- a/src/flask/cli.py
+++ b/src/flask/cli.py
@@ -1120,6 +1120,7 @@

 def main() -> None:
+    """Invoke the Flask command line interface."""
     cli.main()
```

After approval, RepoPilot created an isolated copy of the repository, applied the patch, built the project inside Docker, and executed the repository's test suite.

```text
........................................................................ [ 14%]
........................................................................ [ 29%]
........................................................................ [ 43%]
........................................................................ [ 58%]
........................................................................ [ 73%]
........................................................................ [ 87%]
...........................................................              [100%]

491 passed in 13.17s
```

The run completed with:

```text
attempt:        1
status:         passed
test exit code: 0
score:          100
```

This is an example integration run, not a benchmark or guarantee for arbitrary repositories.

## Retry and Repair Loop

A failed patch does not immediately terminate an agent run.

When repository tests fail, RepoPilot:

1. Persists the failed attempt and test output.
2. Builds a retrieval query using the original task and failure information.
3. Retrieves additional code related to the failure.
4. Sends the original plan, repository context, and test failure to the repair model.
5. Generates a complete revised patch against the original repository state.
6. Validates the revised patch locally.
7. Pauses again for human approval.
8. Runs the revised patch in a fresh sandbox if approved.

Retries are bounded by a configurable maximum attempt count.

The retry workflow is covered by a deterministic LangGraph test that forces attempt 1 to fail and attempt 2 to pass.

```text
Attempt 1
   │
   ▼
Tests fail ──► Score 25
   │
   ▼
Retrieve failure context
   │
   ▼
Generate repaired patch
   │
   ▼
Human approval
   │
   ▼
Attempt 2
   │
   ▼
Tests pass ──► Score 95
   │
   ▼
Completed
```

## Safety Model

RepoPilot intentionally separates **patch generation** from **patch execution**.

The original cloned repository remains unchanged during an agent run. Approved edits are applied to a disposable copy under `run_workspaces/`.

Several additional controls are applied before generated code can execute:

- Every generated file path is validated to remain inside the repository.
- An `original_snippet` must exist exactly once before an edit can be applied.
- Patch generation happens in memory before any file is modified.
- Every initial patch requires explicit human approval.
- Every repaired patch requires a new human approval.
- Tests run inside Docker rather than directly on the host.
- The repository is mounted read-only while tests execute.
- Test containers run without network access.
- Linux capabilities are dropped.
- `no-new-privileges` is enabled.
- CPU, memory, and process limits are applied.
- Temporary writable storage is isolated from the repository source.

Dependency installation occurs in a separate setup step before the network-isolated test execution.

## Tech Stack

| Layer | Technology |
|---|---|
| API | FastAPI |
| Agent orchestration | LangGraph |
| LLM | OpenAI API |
| Structured generation | Pydantic |
| Code parsing | Python AST |
| Embeddings | SentenceTransformers |
| Vector search | pgvector |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Checkpointing | LangGraph PostgreSQL Checkpointer |
| Sandboxing | Docker |
| Dependency environment | uv |
| Validation | pytest |

## Project Structure

```text
repopilot/
├── app/
│   ├── routers/
│   │   ├── repositories.py
│   │   └── runs.py
│   ├── services/
│   │   ├── analysis_agent.py
│   │   ├── checkpointing.py
│   │   ├── code_scanner.py
│   │   ├── embeddings.py
│   │   ├── execution.py
│   │   ├── indexer.py
│   │   ├── llm.py
│   │   ├── patch_agent.py
│   │   ├── patches.py
│   │   └── repository.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
├── tests/
│   ├── test_code_scanner.py
│   ├── test_patches.py
│   ├── test_retry_loop.py
│   └── test_scoring.py
├── compose.yaml
├── pytest.ini
├── requirements.txt
├── .env.example
└── README.md
```

`workspace/` and `run_workspaces/` are generated locally and excluded from version control.

## Getting Started

### Prerequisites

You will need:

- Python 3.13+
- Docker
- Git
- An OpenAI API key

### 1. Clone RepoPilot

```bash
git clone <your-repository-url>
cd repopilot
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS / Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env`.

```env
DATABASE_URL=postgresql+psycopg://repopilot:repopilot_dev@localhost:5432/repopilot
LANGGRAPH_DATABASE_URL=postgresql://repopilot:repopilot_dev@localhost:5432/repopilot?sslmode=disable
OPENAI_API_KEY=your-api-key
OPENAI_MODEL=your-model-name
```

Never commit `.env`.

### 5. Start PostgreSQL

```bash
docker compose up -d
```

The included PostgreSQL image provides the `pgvector` extension used for semantic code search.

### 6. Start RepoPilot

```bash
python -m uvicorn app.main:app --reload --reload-dir app
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## API Workflow

A typical RepoPilot workflow looks like this.

### 1. Import a repository

```http
POST /repositories
```

```json
{
  "url": "https://github.com/pallets/flask.git"
}
```

RepoPilot clones the repository and returns a repository ID.

### 2. Index the repository

```http
POST /repositories/{repository_id}/index
```

RepoPilot extracts Python symbols, generates embeddings, and stores them in pgvector.

### 3. Search the repository

```http
GET /repositories/{repository_id}/search?q=error+handling
```

Optional metadata filters can restrict results by file or symbol type.

### 4. Analyze a task

```http
POST /repositories/{repository_id}/analyze
```

The analysis endpoint retrieves relevant code and returns a structured description of target files, symbols, proposed changes, and uncertainties.

### 5. Start an agent run

```http
POST /repositories/{repository_id}/runs
```

```json
{
  "task": "Add a concise docstring to Flask's main CLI entry point without changing behavior.",
  "retrieval_limit": 8,
  "max_attempts": 3
}
```

The agent retrieves code, analyzes the task, generates a patch, and enters:

```text
awaiting_approval
```

### 6. Review and approve the patch

```http
POST /runs/{run_id}/approve
```

Or reject it:

```http
POST /runs/{run_id}/reject
```

Approval resumes the persisted LangGraph workflow.

### 7. Inspect the run

```http
GET /runs/{run_id}
```

### 8. Inspect execution attempts

```http
GET /runs/{run_id}/attempts
```

Attempt history includes the exact patch that was tested, exit codes, logs, status, and test-based score.

## Scoring

RepoPilot uses a deliberately simple execution score rather than presenting an opaque model-generated quality metric.

```text
First-attempt pass     100
Second-attempt pass     95
Third-attempt pass      90
Tests failed            25
Test timeout            10
Setup failure            0
```

The score represents **execution outcome and repair efficiency**, not a universal measurement of code quality.

## Tests

Run RepoPilot's test suite with:

```bash
python -m pytest -q
```

The test suite currently covers:

- AST symbol extraction
- Repository path validation and path traversal prevention
- Test-based execution scoring
- LangGraph failure → repair → approval → retry behavior

`pytest.ini` restricts test discovery to RepoPilot's own `tests/` directory so tests inside cloned repositories are not accidentally collected.

## Current Limitations

RepoPilot is intentionally scoped as a portfolio-scale code agent rather than a full IDE replacement.

Current limitations include:

- Code-aware symbol extraction is Python-first.
- Repository ingestion currently targets GitHub repositories over HTTP/HTTPS.
- Automated dependency setup currently expects Python projects using `pyproject.toml` and `uv.lock`.
- Repository-wide semantic search depends on the quality of symbol extraction and embedding retrieval.
- Complex changes may require code outside the retrieved context.
- RepoPilot proposes patches but does not automatically commit or push code.
- Generated code remains dependent on LLM quality and should always be reviewed before approval.

## Design Goals

RepoPilot was built around four principles:

**Ground changes in repository code.**  
The model receives retrieved source symbols instead of being asked to reason about a repository it has not seen.

**Make agent actions inspectable.**  
Analysis, proposed edits, diffs, test logs, attempts, and scores are persisted rather than hidden behind a single agent response.

**Keep execution separate from generation.**  
An LLM may propose code, but deterministic validation and human approval decide whether that code reaches the execution environment.

**Use tests as feedback.**  
A failed patch becomes additional context for another retrieval and repair cycle rather than merely producing a failed run.

