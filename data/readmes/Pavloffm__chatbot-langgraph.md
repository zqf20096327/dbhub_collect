# Chatbot LangGraph

**A local AI assistant with persistent conversations, streamed replies, and
optional web search with source links.** React handles the chat interface;
FastAPI, LangGraph, Ollama, and PostgreSQL handle the backend and message state.

![A looping preview of a chat response showing web search progress and source links](docs/images/chat-demo.gif)

*Search progress and source links in action.*

[Download the full 30-second demo (MP4, 3.1 MB)](https://raw.githubusercontent.com/Pavloffm/chatbot-langgraph/main/docs/videos/demo_chatbot.mp4)
· [View a still screenshot](docs/images/chat-preview.png). The screenshot uses
simulated conversations and mocked authentication.

**Local prototype, not a hosted service.** Running the app requires a Clerk
development instance with an invited account, PostgreSQL, and Ollama.

## What's implemented

- **Conversations you can return to.** PostgreSQL stores titles and ownership;
  LangGraph checkpoints preserve message state across restarts.
- **Answers with visible context.** Replies stream as they are generated. When
  optional web search runs, the UI shows its progress and links to returned sources.
- **Readable, navigable UI.** Browse previous chats, jump between messages,
  and read or copy Markdown, code, tables, and maths on desktop or mobile.
- **Server-enforced access.** FastAPI verifies Clerk session tokens and
  checks conversation ownership instead of trusting a signed-in browser.

**Stack:** React · TypeScript · FastAPI · LangGraph · Ollama · PostgreSQL · Clerk
· optional SearXNG.

## How it works

```text
React + Clerk → FastAPI (token verification, streamed NDJSON)
                    ├── PostgreSQL (conversation metadata and ownership)
                    └── LangGraph + PostgreSQL checkpointer
                              ├── Ollama (local model)
                              └── SearXNG (optional web search)
```

The backend streams text, search progress, completion, and errors as
newline-delimited JSON. A tool-capable model decides whether to search; if
enabled, one bounded SearXNG request returns up to five results. The app works
without SearXNG. Per-conversation advisory locks prevent overlapping
generations, and bounded database pools limit resource use.

## Run locally

You will need Python 3.12, [uv](https://docs.astral.sh/uv/), Node.js 24,
Docker, a running Ollama model (`gemma4:e4b`), and a Clerk development application.
The model must support tool calling if you enable web search. See the
[backend setup](backend/README.md) and [frontend setup](frontend/README.md) for
configuration and troubleshooting.

1. Copy `backend/.env.example` to `backend/.env`. Replace the sample database
   passwords and update both database URLs to match. Supply your
   `CLERK_SECRET_KEY` in that local file, and set
   `CLERK_AUTHORIZED_PARTIES=http://localhost:5173`. Remove `SEARXNG_BASE_URL`
   if you are not running SearXNG. Never commit credentials.
2. Add `VITE_CLERK_PUBLISHABLE_KEY` from the same Clerk development instance to
   `frontend/.env.local`. Configure that instance for your local origin and invite
   your test account. Start Ollama with the model named above.
3. In separate terminals, run:

   ```sh
   cd backend
   docker compose --env-file .env up -d --wait postgres
   uv run --env-file .env alembic upgrade head
   uv run --env-file .env python -m backend.checkpoint_setup
   uv run --env-file .env uvicorn backend.main:app --reload
   ```

   ```sh
   cd frontend
   npm ci
   npm run dev
   ```

Open `http://localhost:5173`. Web search is optional; see
[SearXNG configuration](backend/README.md#optional-local-web-search).

## Verification and limits

The [GitLab pipeline](docs/GIT_WORKFLOW.md#gitlab-ci) runs linting, type checks,
unit tests, a frontend build, documentation checks, and a history-based secret
scan. Backend tests mock external services; frontend unit and browser tests also
cover mocked authentication and chat interactions. Real Clerk sign-in, Ollama,
PostgreSQL, and SearXNG still require local integration checks. Dependency audits
are advisory, not a clean bill of health; see [security notes](docs/SECURITY.md).

This is not configured for public deployment. Production use needs HTTPS,
production authentication settings, rate limiting, and an operational review.
The [backend README](backend/README.md) documents the API and failure behavior;
the [frontend README](frontend/README.md) documents the UI and test setup.
