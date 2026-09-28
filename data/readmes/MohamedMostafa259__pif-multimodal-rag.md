# PIF-Multimodal-RAG

A modular, multilingual, and multimodal Retrieval-Augmented Generation (RAG) system tailored for the financial analysis of Public Investment Fund (PIF) annual reports.

The framework builds upon the design principles of M3DocRAG, extending it with domain-specific adaptations for financial document understanding in both **Arabic** and **English**.

## Demo

Watch the full demo on YouTube: [PIF-Multimodal-RAG Demo](https://youtu.be/wtyusISywdY)

[![PIF-Multimodal-RAG Demo](https://img.youtube.com/vi/wtyusISywdY/0.jpg)](https://www.youtube.com/watch?v=wtyusISywdY)

## Features

- Modular FastAPI backend ([src/main.py](src/main.py)), with [Celery](src/celery_app.py) for background tasks, like reports indexing into the vector DB.
- Vector database integration (Qdrant) for dense retrieval ([src/stores/vectordb/providers/qdrant_provider.py](src/stores/vectordb/providers/qdrant_provider.py)).
- PDF ingestion and caching ([assets/pif-annual-reports/](assets/pif-annual-reports/)).
- Web frontend ([webapp/README.md](webapp/README.md)) for interactive analysis.
- Prometheus metrics ([src/utils/metrics.py](src/utils/metrics.py)).
- Dockerized deployment ([docker/docker-compose.yml](docker/docker-compose.yml)).

## Quick Start

1. **Run [Kaggle Notebook](https://www.kaggle.com/code/mohamedmostafa259/m3docrag-lite-multi-modal-document-rag-server):**  
   - This notebook requires your **NGROK_AUTHENTICATION** and **HF TOKEN** tokens.
   - After running the notebook, copy the generated ngrok URL.
   - For Docker deployment (recommended), paste the URL into `docker/env/.env.app` as `KAGGLE_NGROK_API_URL`. For quick local development, put it in your root `.env` file.

2. Download the [reports](https://www.kaggle.com/datasets/mohamedmostafa259/pif-annual-reports) in [assets/pif-annual-reports/](assets/pif-annual-reports/)

3. **Set Environment Variables:**  
   - Edit `docker/env/.env.app` (for Docker) or `.env` (for local dev).

4. **Start Services:**  
   ```
   docker compose -f docker/docker-compose.yml up -d --build
   ```
   Open [http://localhost](http://localhost) for the UI. The API is proxied at `/api/v1/*`.

## Directory Structure

- [src/](src/): Backend source code ([src/README.md](src/README.md))
- [webapp/](webapp/): React frontend ([webapp/README.md](webapp/README.md))
- [assets/](assets/): PDF reports and cached images ([assets/README.md](assets/README.md))
- [docker/](docker/): Docker configs ([docker/README.md](docker/README.md))
- [tests/](tests/): Unit and integration tests

## Key Files

- [src/main.py](src/main.py): FastAPI app entrypoint
- [src/celery_app.py](src/celery_app.py): Celery worker setup
- [src/controllers/rag_controller.py](src/controllers/rag_controller.py): RAG orchestration
- [src/routes/generation.py](src/routes/generation.py): Answer and compare endpoints
- [src/models/asset_model.py](src/models/asset_model.py): Asset DB model
- [src/stores/vectordb/providers/qdrant_provider.py](src/stores/vectordb/providers/qdrant_provider.py): Qdrant integration

## License

See [LICENSE](LICENSE).

---

For more details, see the linked READMEs in each subdirectory.
