<p align="center">
  <img src="frontend/public/favicon.svg" alt="helaasvrij" height="160">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=black" alt="React">
  <img src="https://img.shields.io/badge/TypeScript-3178C6?logo=typescript&logoColor=white" alt="TypeScript">
  <img src="https://img.shields.io/badge/Vite-646CFF?logo=vite&logoColor=white" alt="Vite">
  <img src="https://img.shields.io/badge/Tailwind%20CSS-4-06B6D4?logo=tailwindcss&logoColor=white" alt="Tailwind CSS">
  <br>
  <img src="https://img.shields.io/badge/.NET-10-512BD4?logo=dotnet&logoColor=white" alt=".NET 10">
  <img src="https://img.shields.io/badge/ASP.NET%20Core-10-512BD4?logo=dotnet&logoColor=white" alt="ASP.NET Core 10">
  <img src="https://img.shields.io/badge/EF%20Core-10-512BD4?logo=dotnet&logoColor=white" alt="EF Core 10">
  <img src="https://img.shields.io/badge/PostgreSQL-17-4169E1?logo=postgresql&logoColor=white" alt="PostgreSQL 17">
  <img src="https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/MCP-000000?logo=modelcontextprotocol&logoColor=white" alt="MCP">
</p>

A private dashboard that helps people in Belgium land a position. Connect GitHub, upload a CV and see exactly what each posting wants from you, with every gap turned into an action tied to your own projects. The search runs like a Jira project: backlog, sprints, board, calendar and an activity log per position.

## <img src="https://api.iconify.design/octicon/rocket-24.svg?color=%232F81F7" width="22" height="22" alt="Rocket"> Getting started

You need:

- Docker with Docker Compose (your user in the `docker` group, or use `sudo`)
- Node.js 22+ with npm, only for frontend development and the MCP server
- .NET 10 SDK, only for backend builds and tests

Run commands from the repo root unless stated otherwise.

```sh
git clone https://github.com/DenysHerasymchuk/internship-coach.git
cd internship-coach
cp .env.example .env
```

Open `.env` and replace `CHANGE_ME` with a database password of your choice. Never commit `.env`.

Other keys in `.env` (all optional for a first start, the app runs without them):

- `R33_API_KEY`: route33 LLM key. Without it every AI feature (profile extraction, gap matrix, drafts, interview prep, chat) answers with an error.
- `GITHUB_TOKEN`: raises the GitHub ingest limit from 60 to 5,000 requests per hour (no scopes needed).
- `GITHUB_CLIENT_ID`, `GITHUB_CLIENT_SECRET`: "Sign in with GitHub" (see below).
- `ADZUNA_APP_ID`, `ADZUNA_APP_KEY`: search real postings on the Find positions page.

### 🐳 Run everything (Docker)

```sh
docker compose up --build
```

| What | URL |
| --- | --- |
| App | http://localhost:5173 |
| API health | http://localhost:5080/api/health |
| Swagger | http://localhost:5080/swagger |

Register an account on the login page, or sign in with GitHub.

First walk-through: Profile (add a GitHub username, paste CV text, confirm items), Postings (add a posting, Analyse), Gap plan (tick a gap to re-scan), Documents (CV, cover letter, recruiter message), Interview prep.

Stop with `Ctrl+C`, or `docker compose down` (add `-v` to also delete the database).

### 🎨 Frontend development (hot reload)

Keep the Docker stack running for the API, then in a second terminal:

```sh
cd frontend
npm install
npm run dev -- --port 5174
```

Open http://localhost:5174. Calls to `/api` are proxied to the API on port 5080.

### 🔐 GitHub sign-in (optional)

Email and password work without this. To enable "Sign in with GitHub":

1. On GitHub open Settings, Developer settings, OAuth Apps, New OAuth App.
2. Homepage URL `http://localhost:5173`. Authorization callback URL `http://localhost:5173/api/auth/github/callback`.
3. Generate a client secret and put both values in `.env`:

   ```
   GITHUB_CLIENT_ID=your-client-id
   GITHUB_CLIENT_SECRET=your-client-secret
   ```

4. Restart: `docker compose up -d api`.

For the Vite dev server (port 5174) create a second OAuth App with callback `http://localhost:5174/api/auth/github/callback` and use its keys in a local `.env`. Without the keys, the GitHub button returns to the login page with an error message.

### 🤖 AI fallback with Claude Code

route33 is always tried first. With `LLM_FALLBACK=claude-cli` in `.env`, a failed route33 call (no key, 401/403, 429, 5xx, timeout, network error) is retried once through the Claude Code CLI (`claude -p`, billed to the Claude subscription you log in with). Sonnet answers Smart calls, Haiku answers Cheap calls; the CLI runs with no tools. The API log says which transport answered, never the content.

The CLI is installed in the API image. Log in once; the login lives in the `jobs-data` volume (`docker compose down -v` deletes it):

```sh
docker compose up -d --build api
docker compose exec api claude
```

With `dotnet run` on the host, set `COACH_Llm__Fallback=ClaudeCli` and your own `claude` is used. Optional: `COACH_Llm__ClaudeCli__TimeoutSeconds` (default 120) and `COACH_Llm__ClaudeCli__Command` (default `claude`).

### 🧪 Build and test

```sh
dotnet build backend/InternshipCoach.slnx
dotnet test backend/InternshipCoach.slnx
cd frontend && npm run build
cd ../mcp && npm install && npm test
CLAUDE_CLI_SMOKE=1 dotnet test backend/InternshipCoach.slnx --filter ClaudeCliSmokeTests   # one real local call
```

### 🔌 Assistant and MCP

The chat button on every page and the MCP server share one tool catalog (`GET /api/tools`). Changes the assistant proposes run only after you confirm. To drive the app from Claude Code or Claude Desktop, create a personal access token in Settings > Account and follow `/connect-claude` or [mcp/README.md](mcp/README.md).

### 🔖 Save to helaasvrij

Settings > Preferences has a draggable "Save to helaasvrij" bookmark. Click it on a LinkedIn or Indeed job page and the position opens prefilled in the add form. The server never fetches LinkedIn itself.

### 🌍 Environments

| Environment | URL |
| --- | --- |
| Local (Docker) | http://localhost:5173 |
| Local (Vite) | http://localhost:5174 |
| API | http://localhost:5080 |

## <img src="https://api.iconify.design/octicon/book-24.svg?color=%232F81F7" width="22" height="22" alt="Book"> Documentation

| Read this | For |
| --- | --- |
| [CLAUDE.md](CLAUDE.md) | Idea, principles, pages, stack, layout and commands |
| [mcp/README.md](mcp/README.md) | MCP server setup and tools |
