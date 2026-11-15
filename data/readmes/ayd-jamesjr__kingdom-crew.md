# Kingdom Crew Fellowship Website

A digital platform for **Kingdom Crew Fellowship at the University of Lay Adventists of Kigali (UNILAK), Rwamagana Campus**.

The project combines a responsive multi-page website with an optional Node.js/Express API, a TiDB Cloud (MySQL-compatible) database, and a server-side AI assistant integration.

> **Project category:** Fellowship & Community — this is a fellowship project, distinct from academic coursework and client projects.

## Overview

The frontend presents fellowship information and community resources. When the backend and external services are configured, the application can also load published events, save contact inquiries, and provide an AI-powered assistant.

## Features

### Website frontend
- Multi-page website: Home, About, Activities, Events, Gallery, Bible, and Contact
- Responsive navigation and page styling
- Configurable social links, events, and gallery content
- Bible reader that retrieves passage text from Bible API
- Client-side form validation

### Backend and integrations
- Node.js and Express server
- TiDB Cloud database connection using `mysql2`
- API endpoint for published events
- Contact inquiry endpoint with input validation and parameterized SQL
- AI assistant endpoint using an OpenAI-compatible API provider
- Rate limiting and security headers
- Health endpoint for checking service configuration

**Backend-dependent features require valid environment variables and configured external services.** The static frontend can be previewed separately, but contact submissions, database-backed events, and AI responses need the backend.

## Technology Stack

| Area | Technologies |
|---|---|
| Frontend | HTML5, CSS3, vanilla JavaScript |
| Backend | Node.js, Express |
| Database | TiDB Cloud / MySQL-compatible |
| Database driver | mysql2 |
| AI integration | OpenAI-compatible chat completions API |
| Security middleware | Helmet, express-rate-limit |
| Configuration | dotenv |
| Hosting option | Render |

## Project Structure

```text
kingdom-crew/
├── public/
│   ├── index.html
│   ├── about.html
│   ├── activities.html
│   ├── events.html
│   ├── gallery.html
│   ├── bible.html
│   ├── contact.html
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   ├── config.js
│   │   ├── main.js
│   │   └── scriptures.js
│   └── images/
├── src/
│   ├── config/
│   │   └── db.js
│   └── server.js
├── schema.sql
├── .env.example
├── .gitignore
├── package.json
└── package-lock.json
```

## Run Locally

### Requirements

- Node.js 18 or later
- npm
- A code editor such as Visual Studio Code

### 1. Clone the repository

```bash
git clone https://github.com/ayd-jamesjr/kingdom-crew.git
cd kingdom-crew
```

### 2. Install dependencies

```bash
npm install
```

### 3. Configure environment variables

Copy `.env.example` to `.env` and add the values for the services you intend to use.

On macOS/Linux:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

At minimum, the server can be started with the example configuration, but database-backed and AI features will remain unavailable until their settings are configured.

### 4. Start the server

```bash
npm start
```

Open [http://localhost:3000](http://localhost:3000).

For development with Node's watch mode:

```bash
npm run dev
```

### Frontend-only preview

You can preview the static website by opening `public/index.html` directly or using the Live Server extension in Visual Studio Code. API-backed functionality will not work in a frontend-only preview.

## Database Setup — TiDB Cloud

The repository includes `schema.sql` for the current database structure.

1. Create or select a TiDB Cloud cluster.
2. Open the TiDB SQL Editor and run the contents of `schema.sql`.
3. Add the connection details to your local `.env` file:
   - `DATABASE_HOST`
   - `DATABASE_PORT`
   - `DATABASE_USER`
   - `DATABASE_PASSWORD`
   - `DATABASE_NAME`
4. Restart the server.
5. Check [http://localhost:3000/api/health](http://localhost:3000/api/health) to confirm the server's reported configuration.

The current schema defines two tables:

- `inquiries` — contact form submissions
- `events` — fellowship events, including a clearly labelled demo row

Remove or replace the demo event before using the database for real fellowship information. Only publish event details that have been confirmed by fellowship leadership.

## AI Assistant Configuration

The backend can connect to an OpenAI-compatible chat completions API. Configure these variables in `.env`:

- `AI_API_KEY`
- `AI_BASE_URL`
- `AI_MODEL`
- `AI_FALLBACK_MODEL` (optional)

The example environment file includes a Groq configuration as a starting point. Provider availability, model names, pricing, and usage limits can change; check the provider's current documentation and terms before relying on a particular model.

The API key must remain on the server. **Never put it in files under `public/` or commit it to GitHub.**

## Deployment

The Express server serves the frontend from `public/` and exposes the API routes, so the full application can be deployed as a Node.js web service on a compatible platform such as Render.

Typical Render settings:

- **Build command:** `npm install`
- **Start command:** `npm start`

Add the required database and AI settings as service environment variables in the hosting dashboard. Do not upload your local `.env` file. After deployment, verify the health endpoint and test the features that depend on external services.

A static hosting service can serve the frontend, but the API must still be deployed separately and configured for cross-origin requests if the frontend and backend use different origins.

## Security and Responsible Use

- Keep `.env` and all real credentials out of version control.
- Keep AI provider keys on the server, never in browser JavaScript.
- Use HTTPS for deployed services.
- The contact endpoint validates submitted fields, applies a request limit, and uses parameterized SQL.
- Confirm the privacy notice, consent wording, data retention, and access process before collecting real visitor information.
- Have fellowship leadership review public contact details, meeting information, events, and faith-related content before publishing them.
- Treat AI responses as informational assistance, not official fellowship statements or pastoral care.

## Current Scope and Future Development

The current repository includes the website frontend, Express API foundation, database schema for inquiries and events, and an AI assistant integration point.

The following larger-platform features are **not implemented in this version**:

- Member accounts and authentication
- Admin dashboard
- Member directory
- Community feed

These can be considered for future phases after the existing foundation has been tested and the requirements have been agreed with fellowship leadership.

## Project Classification

**Fellowship & Community Project — Kingdom Crew, UNILAK Rwamagana Campus**

This project is presented separately from personal projects, client work, and UNILAK academic coursework.

---

*Built to support fellowship connection, communication, and community.*
