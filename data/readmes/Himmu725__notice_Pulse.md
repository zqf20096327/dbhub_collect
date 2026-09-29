# NoticePulse 📋

A full-stack Notice Board built with **Next.js (Pages Router)**, **Prisma**, **TiDB Cloud (MySQL)**, and deployed on **Vercel**.

## Live Demo
🔗 https://noticepulse.vercel.app

## Features
- ✅ Create, read, update, and delete notices
- 🔴 Urgent notices always sort above Normal (via Prisma `orderBy`)
- 🏷️ Category badges: Exam, Event, General
- 📱 Fully responsive (mobile + desktop)
- 🛡️ Server-side input validation on all API routes
- 🖼️ Optional image URL per notice (bonus)
- 🗑️ Delete confirmation modal

## Tech Stack

| Layer       | Technology                        |
|-------------|-----------------------------------|
| Framework   | Next.js 14, Pages Router          |
| ORM         | Prisma                            |
| Database    | TiDB Cloud (MySQL-compatible)     |
| Hosting     | Vercel (Hobby tier)               |
| Styling     | Tailwind CSS                      |

## Running Locally

### Prerequisites
- Node.js 18+
- Free [TiDB Cloud](https://tidbcloud.com) account

### Steps

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/noticepulse.git
cd noticepulse

# 2. Install dependencies
npm install

# 3. Set up environment variables
cp .env.example .env
# Edit .env and add your TiDB Cloud DATABASE_URL

# 4. Push schema to database
npx prisma db push

# 5. Start dev server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

## API Routes

| Method | Route                | Description              |
|--------|----------------------|--------------------------|
| GET    | `/api/notices`       | Fetch all (Urgent first) |
| POST   | `/api/notices`       | Create a notice          |
| GET    | `/api/notices/:id`   | Fetch one notice         |
| PUT    | `/api/notices/:id`   | Update a notice          |
| DELETE | `/api/notices/:id`   | Delete a notice          |

## One Thing I Would Improve With More Time

I would replace the image URL input with a proper **drag-and-drop file upload** using Cloudinary or Vercel Blob. This gives users a real upload experience and avoids broken external image links. I'd also add pagination for large notice lists.

## AI Usage

Used Claude (Anthropic) as an assistant for:
- Schema design advice (enums vs strings for Category/Priority)
- Confirming Prisma `orderBy` behaviour for Urgent-first sorting in MySQL
- Debugging TiDB Cloud SSL connection string format
- README structure template (all content filled in manually)

All architecture decisions and implementation are my own.
