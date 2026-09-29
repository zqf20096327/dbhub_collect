# AI CHATBOT by Utkarsh

A responsive, black-themed AI chatbot with Groq-powered answers and persistent MySQL/TiDB conversation memory.

## Project structure

```text
AI-PROJECT/
├── frontend/             React + Vite interface (deploy to Vercel)
├── backend/              FastAPI + Groq + SQLAlchemy API (deploy to Render)
├── render.yaml           Render Blueprint
└── README.md
```

## Run locally

### 1. MySQL

Create an empty database:

```sql
CREATE DATABASE ai_chatbot CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Tables are created automatically when the backend starts.

For a quick local preview, `DATABASE_URL` may be omitted and the app will use a local SQLite file. Render/TiDB should always receive the production MySQL URL.

### 2. Backend

Copy `backend/.env.example` to `backend/.env` and fill in your values. For local MySQL, use:

```env
GROQ_API_KEY=your_real_key
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/ai_chatbot
DB_SSL=false
FRONTEND_URL=http://localhost:5173
```

If the username or password contains `@`, `:`, `/`, or another URL-reserved character, URL-encode it.

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API runs at `http://localhost:8000`; API documentation is at `http://localhost:8000/docs`.

### 3. Frontend

Copy `frontend/.env.example` to `frontend/.env`, then:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

## Deploy

### TiDB Cloud

1. Create a TiDB Serverless cluster and database.
2. Copy the connection host, port, username, password, and database name.
3. Build the SQLAlchemy URL in this format:
   `mysql+pymysql://USERNAME:PASSWORD@HOST:4000/DATABASE`
4. TiDB Cloud uses TLS, so keep `DB_SSL=true`.

### Render (backend)

1. Push this project to GitHub and create a Render Blueprint using `render.yaml`, or create a Python Web Service with root directory `backend`.
2. Add `GROQ_API_KEY`, `DATABASE_URL`, and `FRONTEND_URL` in Render's environment settings.
3. Set `FRONTEND_URL` to your final Vercel URL, such as `https://your-app.vercel.app`.
4. Deploy and copy the Render service URL.

### Vercel (frontend)

1. Import the same GitHub repository in Vercel.
2. Set the root directory to `frontend`; Vercel will detect Vite automatically.
3. Add `VITE_API_URL` with the Render backend URL, such as `https://ai-chatbot-utkarsh-api.onrender.com`.
4. Deploy. If the Vercel domain changes, update `FRONTEND_URL` on Render and redeploy the backend.

## Environment variables

| Service | Variable | Purpose |
|---|---|---|
| Backend | `GROQ_API_KEY` | Groq API authentication |
| Backend | `GROQ_MODEL` | Model name; defaults to `qwen/qwen3-32b` |
| Backend | `DATABASE_URL` | MySQL/TiDB SQLAlchemy connection URL |
| Backend | `DB_SSL` | Set `true` for TiDB Cloud |
| Backend | `FRONTEND_URL` | Allowed frontend origin(s), comma-separated |
| Frontend | `VITE_API_URL` | Public Render backend URL |

Never commit a real `.env` file. The included `.gitignore` excludes all `.env` secrets.
