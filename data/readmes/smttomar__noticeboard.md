# Notice Board

A full-stack notice board app for publishing announcements, exams, events, and urgent updates. It is built with **Next.js Pages Router**, **Prisma**, **MySQL**, and **Tailwind CSS**, with admin-only create, edit, and delete actions.

Live demo: https://noticeboard-puce.vercel.app/

## Features

- Public notice listing with responsive cards
- Search by notice title or body
- Urgent notices pinned at the top
- Category support: `Exam`, `Event`, and `General`
- Priority support: `Normal` and `Urgent`
- Optional notice image URL
- Light and dark theme toggle
- Admin login and logout
- Admin-only create, edit, and delete flows
- Server-side validation for notice mutations
- Open Graph and Twitter preview image metadata

## Tech Stack

| Concern | Technology |
| --- | --- |
| Framework | Next.js 14, Pages Router |
| UI | React, Tailwind CSS, React Icons |
| Database ORM | Prisma |
| Database | MySQL-compatible database |
| Auth | Signed HTTP-only role cookie |
| Hosting | Vercel |

## Requirements

Install these before starting:

- Node.js 18 or newer
- npm
- Git
- A MySQL-compatible database URL

Good hosted database options include TiDB Cloud, PlanetScale, Railway MySQL, Aiven MySQL, or any regular MySQL server.

## Setup From GitHub

### 1. Clone the repository

```bash
git clone https://github.com/your-username/noticeboard.git
cd noticeboard
```

Replace `your-username` with the GitHub account or organization that owns the repo.

### 2. Install dependencies

```bash
npm install
```

### 3. Create the environment file

Create a `.env` file in the project root:

```env
DATABASE_URL="mysql://USER:PASSWORD@HOST:PORT/DATABASE"
ADMIN_EMAIL="admin@example.com"
ADMIN_LOGIN_PASSWORD="change-this-password"
ADMIN_SESSION_SECRET="change-this-long-random-secret"
NEXT_PUBLIC_SITE_URL="http://localhost:3000"
```

Environment variable details:

| Variable | Required | Purpose |
| --- | --- | --- |
| `DATABASE_URL` | Yes | MySQL connection string used by Prisma |
| `ADMIN_EMAIL` | Yes | Email address for the admin user created by the seed script |
| `ADMIN_LOGIN_PASSWORD` | Yes | Password used on `/login` for admin access |
| `ADMIN_SESSION_SECRET` | Recommended | Secret used to sign the admin session cookie |
| `NEXT_PUBLIC_SITE_URL` | Recommended | Absolute site URL used for OG and Twitter preview images |

For local development, `NEXT_PUBLIC_SITE_URL` can stay as `http://localhost:3000`. For production, set it to your deployed site URL, for example `https://noticeboard-puce.vercel.app`.

### 4. Push the Prisma schema to the database

```bash
npx prisma db push
```

This creates the `Notice` and `User` tables, plus the required enums.

### 5. Create the admin user

```bash
npm run create-admin
```

The script uses `ADMIN_EMAIL` and `ADMIN_LOGIN_PASSWORD` from `.env`. It creates the admin user if missing, or updates the existing user to the `admin` role.

### 6. Start the development server

```bash
npm run dev
```

Open http://localhost:3000 in your browser.

### 7. Log in as admin

1. Go to http://localhost:3000/login
2. Enter the email from `ADMIN_EMAIL`
3. Enter the password from `ADMIN_LOGIN_PASSWORD`
4. After login, use **New Notice** to create notices

## Common Scripts

| Command | Description |
| --- | --- |
| `npm run dev` | Start the local development server |
| `npm run build` | Generate Prisma client and build the Next.js app |
| `npm run start` | Start the production build locally |
| `npm run lint` | Run Next.js lint checks |
| `npm run db:push` | Push the Prisma schema to the configured database |
| `npm run create-admin` | Create or update the admin user |

## Deploy To Vercel

### 1. Push the code to GitHub

```bash
git add .
git commit -m "Initial notice board setup"
git push origin main
```

### 2. Import the repo in Vercel

1. Open https://vercel.com
2. Click **Add New Project**
3. Import your GitHub repository
4. Keep the framework preset as **Next.js**

### 3. Add production environment variables

In Vercel project settings, add:

```env
DATABASE_URL="mysql://USER:PASSWORD@HOST:PORT/DATABASE"
ADMIN_EMAIL="admin@example.com"
ADMIN_LOGIN_PASSWORD="use-a-strong-production-password"
ADMIN_SESSION_SECRET="use-a-long-random-production-secret"
NEXT_PUBLIC_SITE_URL="https://your-vercel-domain.vercel.app"
```

Use your real Vercel domain or custom domain for `NEXT_PUBLIC_SITE_URL`. This matters because social preview images need absolute URLs.

### 4. Prepare the production database

Run these commands locally with the production `DATABASE_URL` in your `.env`:

```bash
npx prisma db push
npm run create-admin
```

This creates the production tables and admin account before you use the deployed app.

### 5. Deploy

Click **Deploy** in Vercel. Vercel runs `npm install`, `postinstall`, and the build command automatically.

After deployment, open:

```text
https://your-vercel-domain.vercel.app
https://your-vercel-domain.vercel.app/login
```

## Open Graph Image

The app serves its preview image from:

```text
/public/og-image.png
```

The metadata is generated in `pages/_app.js` and uses `NEXT_PUBLIC_SITE_URL` to produce full URLs such as:

```text
https://your-domain.com/og-image.png
```

After changing the OG image or metadata, redeploy and refresh link previews in the social platform debugger because WhatsApp, LinkedIn, Facebook, and X can cache old previews.

## API Routes

| Method | Route | Access | Description |
| --- | --- | --- | --- |
| `GET` | `/api/notices` | Public | List all notices |
| `POST` | `/api/notices` | Admin | Create a notice |
| `GET` | `/api/notices/[id]` | Public | Get one notice |
| `PUT` | `/api/notices/[id]` | Admin | Update a notice |
| `DELETE` | `/api/notices/[id]` | Admin | Delete a notice |
| `POST` | `/api/auth/login` | Public | Log in as admin |
| `POST` | `/api/auth/logout` | Public | Clear the login cookie |

Notice mutation routes validate input on the server and return `422` with field-level errors for invalid data.

## Data Model

The app stores two main records:

| Model | Purpose |
| --- | --- |
| `Notice` | Notice title, body, category, priority, event date, optional image, timestamps |
| `User` | Admin/user account record used for login authorization |

Supported notice categories:

```text
Exam
Event
General
```

Supported notice priorities:

```text
Normal
Urgent
```

## Project Structure

```text
noticeboard/
├── components/
│   ├── NoticeCard.jsx
│   └── NoticeForm.jsx
├── lib/
│   ├── auth.js
│   ├── notices.js
│   ├── prisma.js
│   ├── theme.js
│   └── useNoticeTheme.js
├── pages/
│   ├── api/
│   │   ├── auth/
│   │   └── notices/
│   ├── notices/
│   ├── _app.js
│   ├── _document.js
│   ├── index.js
│   └── login.js
├── prisma/
│   └── schema.prisma
├── public/
│   ├── logo.svg
│   └── og-image.png
├── scripts/
│   └── create-admin.js
├── styles/
│   └── globals.css
├── next.config.js
├── package.json
└── README.md
```

## Troubleshooting

### Admin login says it is not configured

Set `ADMIN_LOGIN_PASSWORD` in `.env`, restart the dev server, and try again.

### Admin login says invalid credentials

Run:

```bash
npm run create-admin
```

Then log in with `ADMIN_EMAIL` and `ADMIN_LOGIN_PASSWORD`.

### Database tables are missing

Run:

```bash
npx prisma db push
```

Make sure `DATABASE_URL` points to the database you are trying to use.

### OG image does not appear in previews

Check that `NEXT_PUBLIC_SITE_URL` is set to the public deployed URL, redeploy the app, and ask the social platform to scrape the URL again.

### Vercel deployment builds but the app errors

Confirm the production `DATABASE_URL`, `ADMIN_LOGIN_PASSWORD`, and `ADMIN_SESSION_SECRET` are set in Vercel, then run `npx prisma db push` against the production database.
