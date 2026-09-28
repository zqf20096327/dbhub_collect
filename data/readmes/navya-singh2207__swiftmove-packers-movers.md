# SwiftMove Packers & Movers

Multi-page marketing site + Express API for quotes, tracking, auth, contact, and Gemini-powered chat.

```
.
├── *.html, css/, js/     # Static website
├── frontend/             # Floating chat widget
├── backend/              # Node.js + Express API
└── render.yaml           # Render Blueprint for the API
```

---

## Quick start

### 1. Backend API

```bash
cd backend
cp .env.example .env
# Edit .env with TiDB + Gemini + JWT values
npm install
npm run dev
```

API: `http://localhost:5000` (or the `PORT` in `.env`)

### 2. Frontend (static site)

From the project root:

```bash
python3 -m http.server 8080
```

Open `http://localhost:8080`. The chat widget defaults to `http://localhost:5001` — either match that in `.env` `PORT`, or set:

```html
<script>window.SWIFTMOVE_API_URL = 'http://localhost:5000';</script>
```

before loading `frontend/js/chat-widget.js`.

### 3. Database schema

Apply `backend/schema.sql` to your TiDB/MySQL database (creates `swiftmove` tables for users, quotes, shipments, contacts, chat_history).

---

## Environment variables

Copy `backend/.env.example` → `backend/.env`. Never commit `.env`.

| Variable | Required | Description |
|----------|----------|-------------|
| `PORT` | No | HTTP port (default `5000`; Render sets this automatically) |
| `HOST` | No | Bind address (default `0.0.0.0` for cloud hosts) |
| `NODE_ENV` | No | `development` or `production` |
| `CORS_ORIGIN` | Recommended in prod | Comma-separated allowed origins, e.g. `https://yoursite.com` |
| `DB_HOST` | **Yes** | TiDB Cloud host, e.g. `gateway01....tidbcloud.com` |
| `DB_PORT` | **Yes** | Usually `4000` |
| `DB_USER` | **Yes** | TiDB username |
| `DB_PASSWORD` | **Yes** | TiDB password |
| `DB_NAME` | **Yes** | Database name (e.g. `swiftmove`) |
| `DB_SSL_CA` | No | Path to CA cert if needed; omit on Render to use system CAs |
| `DB_SSL_REJECT_UNAUTHORIZED` | No | Default `true` (TLS required for TiDB Cloud) |
| `JWT_SECRET` | **Yes** | Secret for signing auth tokens |
| `JWT_EXPIRES_IN` | No | Token lifetime (default `7d`) |
| `GEMINI_API_KEY` | **Yes** (for chat) | Google AI Studio / Gemini API key |
| `GEMINI_MODEL` | No | Default `gemini-2.0-flash` (override if your key supports `gemini-1.5-flash`) |

### TiDB Cloud notes

- TiDB requires TLS (`minVersion: TLSv1.2`).
- Locally on macOS you can set `DB_SSL_CA=/etc/ssl/cert.pem`.
- On **Render**, leave `DB_SSL_CA` empty so Node uses the system certificate store.
- Ensure your TiDB Cloud cluster allows connections from Render egress IPs (or allow public access during setup).

### Gemini notes

- Create a key at [Google AI Studio](https://aistudio.google.com/apikey).
- Free-tier quotas may return HTTP **429**; the API maps this to a friendly error.

---

## npm scripts (`backend/`)

| Script | Command | Purpose |
|--------|---------|---------|
| `npm start` | `node server.js` | Production server |
| `npm run dev` | `node --watch server.js` | Auto-restart on file changes |
| `npm run check` | DB ping | Verify TiDB connection using `.env` |

---

## API endpoints

Base URL: `http://localhost:5000/api` (local) or `https://<your-service>.onrender.com/api` (Render).

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `GET` | `/health` | — | Health check |
| `GET` | `/check` | — | Simple OK probe |
| `POST` | `/quote` | — | Create quote (`name`, `email`, `phone`, `from_city`, `to_city`, `item_details`) |
| `GET` | `/track/:trackingId` | — | Shipment status by tracking ID |
| `POST` | `/contact` | — | Contact form (`name`, `email`, `message`) |
| `POST` | `/auth/register` | — | Register user (rate limited) |
| `POST` | `/auth/login` | — | Login → JWT (rate limited) |
| `GET` | `/admin/quotes` | Bearer + **admin** | List all quotes |
| `POST` | `/chat` | — | Chatbot (`message`, optional `tracking_id`, `session_id`) (rate limited) |

### Auth header

```http
Authorization: Bearer <jwt_token>
```

Admin routes require `role: "admin"` on the user (set in the database after register).

### Example: create quote

```bash
curl -X POST https://<your-service>.onrender.com/api/quote \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Rahul Sharma",
    "email": "rahul@example.com",
    "phone": "9876543210",
    "from_city": "Mumbai",
    "to_city": "Delhi",
    "item_details": "2 BHK home shifting"
  }'
```

### Example: chat

```bash
curl -X POST https://<your-service>.onrender.com/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"What packing services do you offer?"}'
```

---

## Deploy on Render

### Option A — Blueprint (`render.yaml`)

1. Push this repo to GitHub.
2. In Render: **New** → **Blueprint** → select the repo.
3. Fill in sync:false env vars: `DB_*`, `GEMINI_API_KEY`, `CORS_ORIGIN`.
4. Deploy. Health check uses `/api/health`.

### Option B — Manual Web Service

1. **New Web Service** → connect repo.
2. **Root Directory:** `backend`
3. **Build Command:** `npm install`
4. **Start Command:** `npm start`
5. **Health Check Path:** `/api/health`
6. Add environment variables from the table above (`JWT_SECRET` can be generated in the Render UI).

### After deploy

1. Point the chat widget at your API:

```html
<script>window.SWIFTMOVE_API_URL = 'https://swiftmove-api.onrender.com';</script>
```

2. Set `CORS_ORIGIN` to your frontend origin(s).
3. Confirm schema is applied on TiDB (`npm run check` locally against prod credentials, or hit `/api/health` after deploy).

### Render-specific behavior already configured

- Binds `0.0.0.0` and uses `process.env.PORT`
- `trust proxy` enabled for rate limiting behind Render’s load balancer
- SSL works without a CA file path (system CAs)
- Request body limited to 100kb

---

## Security

- Passwords hashed with bcrypt
- JWT for protected routes
- Global input sanitization + parameterized SQL
- Rate limits on `/api/auth` and `/api/chat`
- `.env` gitignored — only `.env.example` is committed

---

## Frontend images

Photographs load from Unsplash CDN (`js/image-urls.js`). Replace with licensed brand photos when going live.
