# Bix SQL Agent

Bix SQL Agent is a full-stack demo that turns natural-language questions into SQL queries against a bundled SQLite copy of the Northwind dataset. The FastAPI backend assembles a LangChain SQL agent, streams intermediate reasoning, and returns synthesized answers, while a React/Vite front end renders the chat experience with live tool-call traces.

## Features
- FastAPI service that exposes synchronous and Server-Sent Events (SSE) chat endpoints.
- LangChain SQL agent configured for SQLite with optional domain hints and reasoning controls.
- In-memory session store that preserves multi-turn chat context per client.
- React/Vite single-page UI with streaming updates, tool-call trace viewer, and local session persistence.
- Bundled `northwind.db` sample database for immediate experimentation.

## Architecture
- **Backend:** `server.py` builds a LangChain ReAct agent (`create_react_agent_compat`) on top of `langchain-openai` and `langgraph`, exposing `/ask` and `/ask/stream`.
- **Agent helpers:** `agent_utils.py` inspects the installed LangGraph version to select the correct modifier arguments and configures `ChatOpenAI` from environment variables.
- **Frontend:** `frontend/src/App.jsx` renders the chat UI, subscribes to SSE updates, and gracefully falls back to the non-streaming REST endpoint.

## Prerequisites
- Python 3.10+ and Node.js 18+.
- An OpenAI API key with access to a GPT-4.1/GPT-5 tier model (configurable via `OPENAI_MODEL`).

## Backend Setup
```bash
python -m venv .venv
.venv\Scripts\activate  # On Windows PowerShell use: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create a `.env` file in the project root:
```
OPENAI_API_KEY=sk-...
# Optional overrides
OPENAI_MODEL=gpt-5-mini
OPENAI_REASONING_EFFORT=medium
SQL_AGENT_HINTS=Focus on the Northwind sales tables.
```

Start the FastAPI server:
```bash
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

The server automatically loads `northwind.db` from the repository root. To target a different SQLite database, edit the `SQLDatabase.from_uri` call in `server.py`.

## Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

During development the Vite proxy is expected to forward `/api` requests to `http://localhost:8000`. If you deploy the backend elsewhere, set `VITE_API_BASE` in `.env` or inline when building.

## API Reference
- `GET /health` → returns `{"status": "ok"}` for readiness checks.
- `POST /ask` → accepts `{ "question": "...", "session_id": "optional" }` and returns `{ "answer": "..." }`.
- `GET /ask/stream?question=...&session_id=...` → SSE stream that emits `start`, `tool_call`, `message`, and `final` events with incremental agent reasoning.

Example `curl` request:
```bash
curl -X POST http://localhost:8000/ask ^
  -H "Content-Type: application/json" ^
  -d "{\"question\": \"Which employee sold the most units?\"}"
```

## Customization Ideas
- Swap in your own SQLite database by updating the connection URI.
- Provide domain-specific instructions via the `SQL_AGENT_HINTS` environment variable.
- Change the default assistant greeting or styling inside `frontend/src/App.jsx`.
- Plug in alternative LangChain-compatible LLMs by adjusting `create_chat_openai_from_env`.

## Contributing
Issues and pull requests are welcome. Please run formatting and linting tools locally before submitting changes. If you add new dependencies, remember to update `requirements.txt` or the front-end `package.json`.

## Bix Tech Nearshore Dev (Sponsored)
Need a senior team to help you ship production-grade AI products faster? [Bix Tech](https://bix-tech.com/) offers vetted nearshore engineers, product managers, and designers who overlap with U.S. time zones. Reach out to start a project or augment your current squad.


