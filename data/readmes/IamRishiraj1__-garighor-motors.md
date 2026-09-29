# গাড়ি ঘর — GariGhor Motors

**A full-stack car dealership platform with an AI assistant that doesn't just chat — it captures qualified leads directly into PostgreSQL.**

[![Live Site](https://img.shields.io/badge/Live-garighor--motors.vercel.app-C98A3D?style=for-the-badge)](https://garighor-motors.vercel.app)
[![Try Demo](https://img.shields.io/badge/No%20Login%20Needed-Try%20Portfolio%20Demo-14181F?style=for-the-badge)](https://garighor-motors.vercel.app)

Built end-to-end as a production-ready reference implementation: a public customer site, a private dealer admin console, and an AI front-desk assistant with structured, database-backed lead capture — designed to be handed to a non-technical business owner and actually run.

---

## 🚗 What this is

Most dealership chatbots just answer questions and the conversation disappears. This one is different: when a customer says *"I want to book a test drive,"* the backend forces the AI to return a strict, typed JSON response — not free text — validates it independently in code, and writes a structured lead directly into Postgres. No manual transcription, no lost enquiries, no single point of failure if the AI itself has a bad moment.

**Try it yourself, no signup required:**
- Browse the live site → [garighor-motors.vercel.app](https://garighor-motors.vercel.app)
- Open the chat bubble (bottom-right) and ask about a car, or say you'd like a test drive
- Scroll to the footer → **"✦ Try Portfolio Demo"** for a full sandboxed dealer console — no credentials needed, safe to click around

---

## ✨ Key Features

### Customer site
- Full inventory catalog — search, filter by brand/body/fuel/price, sort by mileage/year/price
- Car detail pages with auction-grade specs, features list, and a real enquiry/test-drive form
- Wishlist that self-heals — stale saved IDs are reconciled against live inventory automatically
- Real authentication — bcrypt-hashed passwords, JWT sessions, not a demo login
- AI assistant grounded in **live inventory data** — it only discusses cars that actually exist, at their actual prices

### AI lead-capture pipeline
- Google Gemini API with `responseSchema` forcing typed JSON on every turn — no regex-parsing of free text
- Code-enforced contact validation (independent of what the model decided) before anything touches the database
- Duplicate-lead prevention, scoped by source, with a 10-minute dedup window
- Automatic retry with exponential backoff on transient Gemini `503` errors
- **Graceful fallback architecture** — if the AI is unavailable, the chat widget surfaces a structured 4-step booking wizard that posts to the *same* `/api/leads` endpoint. The AI is an interface, not a single point of failure.

### Dealer admin console
- Full inventory CRUD with Cloudinary-backed photo uploads
- Leads inbox with pipeline management (new → contacted → closed) and source tagging (form / AI / demo)
- Mobile-responsive — sidebar collapses to a horizontal tab bar under 780px
- Dynamic homepage hero image, editable from the dashboard

### Portfolio demo console
- Public, credential-free sandbox at the same URL — inventory edits are browser-only (never touch the real database), while the AI chat and booking wizard are **100% real**, writing to an isolated `source: "demo"` slice of the same production database

### Production-grade infrastructure
- Automated daily backups (`pg_dump` + Cloudinary manifest), tested via a real restore into an isolated Neon database branch — not just configured and assumed to work
- Uptime monitoring keeping the free-tier backend warm
- CI/CD: push to `main` auto-deploys frontend (Vercel) and backend (Render)

---

## 🏗️ Architecture

```
┌─────────────┐      ┌──────────────────┐      ┌─────────────────┐
│   React     │─────▶│  Express API     │─────▶│  PostgreSQL      │
│  (Vercel)   │◀─────│  (Render)        │◀─────│  (Neon, serverless)
└─────────────┘      └──────────────────┘      └─────────────────┘
                              │
                 ┌────────────┴────────────┐
                 │                         │
          ┌──────▼──────┐          ┌───────▼────────┐
          │  Gemini AI   │          │  Cloudinary     │
          │ (structured  │          │ (photo storage) │
          │   output)    │          └────────────────┘
          └──────────────┘
```

**The lead-capture fallback, specifically:**

```
             ┌── Gemini AI ─────────────────────┐
Customer ────┤                                  ├──→ POST /api/leads ──→ PostgreSQL
             └── Fallback Booking Form ─────────┘                           │
                                                                             ↓
                                                                      Admin Dashboard
```

Both paths converge on the same validated backend endpoint. The LLM is the conversational interface; the backend is the single source of truth.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | React 18, Vite, Lucide React icons, CSS-in-JS |
| **Backend** | Node.js, Express.js, Prisma ORM |
| **Database** | PostgreSQL (Neon, serverless, free tier) |
| **AI** | Google Gemini (`gemini-3.6-flash`) with structured JSON output |
| **Auth** | JWT + bcrypt |
| **Media storage** | Cloudinary |
| **Hosting** | Vercel (frontend) · Render (backend) |
| **Monitoring** | UptimeRobot |
| **Backups** | Custom `pg_dump`-based Node script + Windows Task Scheduler |

No component library, no CSS framework, no ORM alternative evaluated and discarded lightly — every dependency choice is one I can defend in an interview.

---

## 📁 Project Structure

```
garighor-motors/
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Entire client app — routing, all pages, all components
│   │   ├── main.jsx         # React entry point
│   │   └── index.css        # Minimal global reset
│   └── README.md            # Frontend-specific setup
│
├── backend/
│   ├── prisma/
│   │   └── schema.prisma    # Car, Lead, User, Setting models
│   ├── src/
│   │   ├── index.js         # Express app entry, mounts all routes
│   │   ├── lib/prisma.js    # Shared Prisma client
│   │   ├── middleware/
│   │   │   ├── auth.js          # JWT verification + admin gate
│   │   │   ├── asyncHandler.js  # Prevents unhandled rejections from crashing the server
│   │   │   ├── rateLimit.js     # Per-IP rate limiting
│   │   │   └── upload.js        # Multer, local disk or Cloudinary driver
│   │   └── routes/
│   │       ├── auth.js      # Register / login / session restore
│   │       ├── cars.js      # Inventory CRUD
│   │       ├── leads.js     # Enquiries + AI/demo lead capture
│   │       ├── chat.js      # Gemini integration, structured output, fallback logic
│   │       ├── uploads.js   # Photo upload → Cloudinary URL
│   │       └── settings.js  # Site-wide settings (hero image)
│   ├── scripts/
│   │   ├── backup.js        # pg_dump + rotation
│   │   └── restore.js       # Restore into a target database
│   └── README.md            # Backend-specific setup + deployment guide
│
└── README.md                 # You are here
```

---

## 🚀 Getting Started

Each service has its own detailed setup guide:

- **[Backend setup →](./backend/README.md)** — database, environment variables, migrations, deployment
- **[Frontend setup →](./frontend/README.md)** — local dev, build, environment variables

Quick version:

```bash
# Backend
cd backend
npm install
cp .env.example .env      # fill in your DATABASE_URL, JWT_SECRET, GEMINI_API_KEY, etc.
npx prisma migrate dev
npm run seed               # optional — creates a demo admin + sample inventory
npm run dev                 # http://localhost:4000

# Frontend (separate terminal)
cd frontend
npm install
echo "VITE_API_URL=http://localhost:4000/api" > .env.local
npm run dev                 # http://localhost:5173
```

---

## 🐛 Notable Engineering Decisions (a.k.a. things that broke and got fixed properly)

- **Async errors could crash the whole server.** Express 4 doesn't catch errors thrown inside `async` route handlers — a single bad request could take down the entire process. Fixed with an `asyncHandler` wrapper on every route.
- **A schema change with no migration.** Added a Prisma model, wrote the whole feature around it, forgot to run `prisma migrate dev`. The live endpoint 404'd for a day before being caught by actually testing it, not just reading the code.
- **Migrations running on every cold start.** `prisma migrate deploy` was in Render's Start Command, adding latency to every wake-up from sleep. Moved to the Build Command — now runs once per deploy, not once per request.
- **The AI accepted an incomplete email as valid.** Gemini set `triggerBooking: true` when a user typed a clearly broken email. Fixed with independent, code-level validation that overrides the model's own (possibly wrong) confirmation.
- **A single point of failure in lead capture.** If Gemini returned an error mid-conversation, the lead was just... gone. Fixed by separating the LLM (interface) from the backend (source of truth) — a structured booking form now exists as a fully independent path to the same database write.

Full write-up with code snippets: **[Case study →](https://garighor-motors.vercel.app)**

---

## 📄 License

This project is available for portfolio and educational reference. If you'd like to use this architecture for a real business, feel free to reach out.

---

## 👤 Author

**Rishiraj**
Full-Stack Developer & AI Automation
[LinkedIn](https://linkedin.com/in/iamrishiraj1) · [GitHub](https://github.com/IamRishiraj1) · [Live Demo](https://garighor-motors.vercel.app)

*Built as a portfolio piece to demonstrate handover-ready, production-grade full-stack development — not a tutorial project.*
