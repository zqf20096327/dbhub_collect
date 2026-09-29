# AI Career and PDF Knowledge Base

A local-first FastAPI application for career analysis and cited PDF retrieval. Uploaded PDFs are validated by magic bytes, hashed for duplicate detection, stored outside the web root, extracted page by page, chunked at paragraph boundaries, and indexed in persistent SQLite. Search blends normalized TF-IDF cosine similarity with exact-term and phrase matching. Answers are extractive and refuse unsupported questions.

## Run locally

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:PYTHONPATH = '.'
uvicorn backend.api:app --reload --port 8001
```

Open `frontend/index.html` after the API starts. Configure limits and storage in `.env` using `.env.example`. The basic pipeline is CPU-only and does not require a paid API. Optional OCR uses PyMuPDF, Pillow, and Tesseract; install the Tesseract executable separately and ensure it is on `PATH`.

Linux/macOS setup is available as `bash setup.sh`. Docker runs the backend with `docker compose up --build`; mount `./data` to preserve the SQLite database and uploaded files.

## API

- `POST /documents/upload` accepts one or more multipart `files`.
- `GET /documents`, `GET /documents/{id}`, `DELETE /documents/{id}` manage the knowledge base.
- `POST /documents/{id}/process` retries failed processing; `GET /documents/{id}/status` reports progress.
- `GET /documents/{id}/pages/{page}` and `GET /documents/{id}/chunks/{chunk_id}` expose provenance.
- `POST /search` accepts `{ "query": "...", "document_ids": [] }`.
- `POST /chat` returns an extractive answer, sources, and document/page/section/chunk citations.
- `GET /health`, `/health/embedding`, and `/health/vector-db` provide health checks.

The original `/analyze`, `/resume`, `/roadmap`, and `/upload-resume` career endpoints remain available.

## Verification

```powershell
$env:PYTHONPATH = '.'
python scripts/test_embeddings.py
pytest -q
python scripts/test_pipeline.py path\to\document.pdf "maximum temperature"
```

`test_embeddings.py` verifies finite persisted vector generation and similarity retrieval. OCR and table extraction require PDFs containing those structures plus the optional OCR/runtime packages; `pypdf` preserves page text and metadata, while complex table geometry is not silently represented as invented cells.

## Production notes

This deployment intentionally has no unauthenticated internet exposure, rate limiter, external LLM, or distributed queue. Put FastAPI behind an authenticated reverse proxy for shared use, add a worker queue for long-running OCR, and configure a hosted/local reranker or LLM only when its grounding and citation contract has been tested. Uploaded PDFs are never executed.
