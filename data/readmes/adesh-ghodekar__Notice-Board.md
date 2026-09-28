# College Notice Board

A full-stack Notice Board built with Next.js (Pages Router), Prisma and MySQL.
Admins can create, edit, delete, and pin notices; the public list is
responsive, filterable, and always shows Urgent notices first.

## Features

- Public notice list with search, category/priority filters, sorting and pagination.
- Urgent notices always sort above Normal ones — done in the database via Prisma `orderBy`, not in the browser.
- Admin-only create/edit form (one shared form component for both flows).
- Delete requires a confirmation dialog.
- Optional notice image (rendered as a card banner when a valid `http(s)` URL is provided).
- Admin dashboard for managing notices and other admin accounts.
- Credentials-based admin login (NextAuth) with hashed passwords (bcrypt).
- All writes go through `pages/api/` routes with server-side validation — the API rejects bad input even if the browser is bypassed (e.g. via curl/Postman).

## 🛠 Tech Stack

Frontend
- Next.js
- React
- Tailwind CSS

Backend
- Next.js API Routes
- Prisma ORM
- TiDB Cloud

Authentication
- NextAuth
- bcrypt

Deployment
- Vercel

## Folder structure

```
notice-board/
│
├── components/
│   ├── admin/          # AdminTable, DashboardCard - admin-only building blocks
│   ├── common/          # LoadingSpinner, EmptyState, ConfirmDialog - shared UI
│   ├── layout/           # Navbar
│   └── notice/           # NoticeCard, NoticeForm (+ NoticeFormPage), StatsCards, filters, pagination
│
├── hooks/
│   └── useRequireAuth.js # client-side "redirect to /login if no session" guard
│
├── lib/
│   ├── prisma.js         # Prisma client singleton
│   └── auth.js            # NextAuth config + requireAdmin() API guard
│
├── pages/
│   ├── admin/             # dashboard, manage notices, manage admins
│   ├── api/                # notices, admins, auth API routes
│   ├── notices/            # create / edit pages (thin wrappers over NoticeFormPage)
│   ├── login.js
│   ├── index.js             # public notice list
│   ├── _app.js
│   └── _document.js
│
├── prisma/
│   ├── schema.prisma
│   ├── migrations/
│   └── seed.js              # creates a default admin account
│
├── public/
├── styles/
├── utils/
│   ├── constants.js         # category/priority/sort option lists (single source of truth)
│   └── validateNotice.js    # shared server-side validation for create + update
│
├── .env.example
├── .gitignore
├── package.json
└── README.md
```

## Running locally

1. **Install dependencies**
   ```bash
   npm install
   ```

2. **Set up environment variables**

   Copy `.env.example` to `.env` and fill in real values:
   ```bash
   cp .env.example .env
   ```
   - `DATABASE_URL` — a free hosted MySQL database (e.g. [TiDB Cloud](https://tidbcloud.com)).
   - `NEXTAUTH_URL` — `http://localhost:3000` for local dev.
   - `NEXTAUTH_SECRET` — generate one with `openssl rand -base64 32`.

3. **Run migrations and seed a default admin**
   ```bash
   npx prisma migrate deploy
   npx prisma db seed
   ```
   This creates an admin with:
   - Username: `admin`
   - Email: `admin@college.com`
   - Password: `admin123`

   Change this password (or create a new admin and delete this one) before deploying anywhere public.

4. **Start the dev server**
   ```bash
   npm run dev
   ```
   Open [http://localhost:3000](http://localhost:3000).

## Screenshots

Login page
<img width="1632" height="885" alt="Screenshot 2026-07-09 143157" src="https://github.com/user-attachments/assets/fa3edf01-a254-4d1e-b826-84500db736f3" />
Home page
<img width="1727" height="910" alt="Screenshot 2026-07-09 143354" src="https://github.com/user-attachments/assets/45647fc1-e066-48f0-b42a-613cd9e7c0ec" />
Admin Dashboard
<img width="1722" height="777" alt="Screenshot 2026-07-09 143524" src="https://github.com/user-attachments/assets/096af1e3-2cf7-4a92-a7f3-772dc6427a12" />
Manage notice
<img width="1706" height="902" alt="Screenshot 2026-07-09 143604" src="https://github.com/user-attachments/assets/3b119019-f628-44e0-8b6f-3b022a4167da" />

## Deploying to Vercel

1. Push this repository to a public GitHub repo.
2. Import it into Vercel (Hobby/free tier).
3. Add the same three environment variables from `.env` in the Vercel project settings (set `NEXTAUTH_URL` to your Vercel deployment URL).
4. Deploy. `prisma generate` runs automatically via the `postinstall` script.
5. Run `npx prisma migrate deploy` once against the production database (locally, pointed at the prod `DATABASE_URL`, or via a one-off Vercel deployment hook) before the first deploy.

## One thing I'd improve with more time

Image uploads currently rely on the admin pasting an external image URL. With
more time I'd add real file uploads (e.g. to a free tier of Cloudinary or
Vercel Blob) with server-side size/type checks, instead of trusting a link.

## Where and how AI was used

AI tools (Claude and ChatGPT) were used throughout development: scaffolding the initial
Next.js/Prisma/NextAuth setup, writing individual components and API routes,
and later restructuring the project into the folder layout above (extracting
shared components like `NoticeForm`/`NoticeFormPage`, `AdminTable`,
`ConfirmDialog`, and centralizing validation in `utils/validateNotice.js` to
remove duplication between the create and update API routes). All AI-assisted
code was reviewed, tested locally, and adjusted by hand before committing.
