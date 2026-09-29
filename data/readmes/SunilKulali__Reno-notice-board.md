# Reno-notice-board

A notice board app built with the Next.js Pages Router, Prisma, and a hosted MySQL-compatible database. Notices support full create, read, update, and delete, with urgent notices always ordered above normal ones at the database level.

## Tech stack

- Framework: Next.js (Pages Router)
- ORM: Prisma
- Database: MySQL-compatible, hosted (TiDB Cloud free tier recommended)
- Styling: Tailwind CSS

## Design notes

The board is designed as a physical notice board with pinned, slightly tilted paper cards on a chalkboard-textured background. Urgent notices use a red-pin ink stamp instead of a simple colored badge, which fits the school or college context of the project.

## Running locally

1. Clone and install dependencies

   ```bash
   git clone <your-repo-url>
   cd notice-board
   npm install
   ```

2. Set up a free hosted database

   - Create a MySQL-compatible database such as TiDB Cloud.
   - Copy `.env.example` to `.env` and paste your connection string into `DATABASE_URL`.

3. Push the schema

   ```bash
   npx prisma db push
   ```

4. Run the dev server

   ```bash
   npm run dev
   ```

   Open https://reno-notice-board-eta.vercel.app/.

## Deploying

1. Push this repo to a public GitHub repository.
2. Import it into Vercel.
3. Add the `DATABASE_URL` environment variable in the Vercel project settings.
4. Deploy. The Vercel build runs `prisma generate` automatically via the `postinstall` script.

## API routes

| Route | Method | Purpose |
| --- | --- | --- |
| `/api/notices` | `GET` | List all notices, urgent-first |
| `/api/notices` | `POST` | Create a notice |
| `/api/notices/[id]` | `GET` | Fetch a single notice |
| `/api/notices/[id]` | `PUT`/`PATCH` | Update a notice |
| `/api/notices/[id]` | `DELETE` | Delete a notice |

All required-field and date validation happens server-side in `lib/validateNotice.js`, independent of the client-side form checks.

## One thing to improve with more time

Image storage is currently handled as base64 strings in the database rather than dedicated object storage. That keeps the app simple and free-tier friendly, but a real product would benefit from storing just a URL in object storage such as Cloudinary or Vercel Blob.



