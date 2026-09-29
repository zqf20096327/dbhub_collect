🚨 CivicResilience Agent – Hackathon MVP

An AI-powered full-stack agent for incident reporting, analysis, and routing. Built fast, demo-ready, and fully extensible.


---

📂 Project Structure

backend/   → FastAPI API (ingest, analyze, route, feedback, incidents)
frontend/  → React + Vite demo UI
tests/     → pytest integration tests


---

⚡ Quickstart (Local Dev)

1. Backend

cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

2. Frontend (new terminal)

cd frontend
npm install
npm run dev


---

🔑 Environment Variables

OPENAI_API_KEY (optional) → embeddings + LLM features

AUTHORITY_WEBHOOK (optional) → forward routed incidents

DB_PATH (optional) → SQLite path (default: civicresilience.db)



---

✅ Tests

pip install pytest
pytest tests/test_backend.py


---

🗄️ Database Notes

Default: local SQLite (civicresilience.db)

TiDB Integration: placeholder adapter at

backend/app/tidb_adapter.py

Swap in real TiDB client calls for production or cloud deployment.



---

🛠️ Built For

⚡ Hackathon speed

📦 Easy extension

🌍 Real-world civic resilience use cases

