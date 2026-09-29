# Notice Board

A CRUD Notice Board built with Next.js (Pages Router) and Prisma, per the Reno Platforms web development assignment.

**Live app:** https://reno-notice-board-swart.vercel.app

## Tech stack

- **Framework:** Next.js, Pages Router
- **Database access:** Prisma
- **Database:** MySQL-compatible (TiDB Cloud recommended free tier; Neon/Supabase also work with the `postgresql` provider swapped in)
- **Styling:** Tailwind CSS
- **Hosting:** Vercel (free/Hobby tier)

## Features

- Notices list as responsive cards (phone and desktop), each with Edit and Delete (Delete requires confirmation).
- One shared form for both creating and editing a notice.
- Fields: `title`, `body`, `category` (Exam / Event / General), `priority` (Normal / Urgent), `publishDate`, and an optional `imageUrl`.
- Full CRUD through API routes under `pages/api/notices`, using GET, POST, PUT, and DELETE with appropriate status codes.
- Server-side validation in the API routes (`lib/validateNotice.ts`) — required fields and date validity are enforced there, not just in the browser.
- Urgent notices always sort above Normal ones, done via Prisma's `orderBy: [{ priority: "desc" }, { publishDate: "desc" }]` in the database query, not by sorting in the browser.

## Running locally

1. **Install dependencies**

   ```bash
   npm install
   ```

2. **Set up a database**

   Create a free hosted MySQL-compatible database (e.g. [TiDB Cloud](https://tidbcloud.com) Serverless tier). Copy `.env.example` to `.env` and set `DATABASE_URL` to your connection string:

   ```bash
   cp .env.example .env
   ```

3. **Push the schema**

   ```bash
   npx prisma db push
   ```

4. **Run the dev server**

   ```bash
   npm run dev
   ```

   Open [http://localhost:3000](http://localhost:3000).

## Deploying

1. Push this repo to a public GitHub repository.
2. Import it into [Vercel](https://vercel.com) (Hobby/free tier).
3. Add a `DATABASE_URL` environment variable in the Vercel project settings, pointing at the same hosted database (or a separate production instance).
4. Deploy. Vercel runs `prisma generate && next build` automatically via the `build` script in `package.json`.

## One thing I'd improve with more time

Image upload is currently a plain URL field rather than a real upload flow — there's no free, credit-card-free object storage tier that fits neatly into a Vercel serverless deploy without extra setup, so I decided a URL input was the more honest scope for the time available. With more time I'd add actual file upload (e.g. to Vercel Blob or Cloudinary's free tier) with client-side preview and server-side size/type validation.

## Where and how AI was used

AI tools (primarily Claude Code) were used as a development assistant during this assignment. I used AI to:

- Scaffold parts of the Next.js and Prisma setup.
- Generate initial implementations for some CRUD API routes and React components.
- Explain Prisma queries, API design, and Next.js Pages Router concepts.
- Suggest improvements for validation, error handling, and code organization.
- Help debug issues related to Prisma, deployment, and TypeScript.
