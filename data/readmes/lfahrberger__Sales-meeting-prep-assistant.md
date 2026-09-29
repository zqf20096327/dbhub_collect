# Sales Meeting Prep and Follow-Up Assistant

## Project Overview

Sales Meeting Prep and Follow-Up Assistant is a production-ready MVP designed for sales teams that need a lightweight way to capture meeting information, preserve account context, and generate polished follow-up materials quickly.

## Business Problem

Sales representatives often manage meeting notes across disconnected tools, which makes it difficult to retain account history, prepare thoughtful follow-up, and maintain consistent communication after customer conversations.

## Solution Summary

This application provides a simple workflow:

1. Capture key meeting details in a structured form
2. Store those details in a relational database
3. Generate AI-powered summaries and follow-up content from the meeting record
4. Review past meetings in a clean history view

## Key Features

- Business-style landing page with clear navigation
- New Meeting form with required validation
- Relational database storage for meetings and generated outputs
- Meeting History view with clickable meeting records
- Search and filter controls on Meeting History
- Meeting Detail page with original notes and generated AI content
- AI generation for executive summary, customer pain points, next steps, and follow-up email
- Environment-based configuration for database and LLM credentials
- TiDB Cloud-friendly database setup using MySQL-compatible connectivity
- Loading and error states for key routes
- Vercel deployment configuration with basic security headers

## Tech Stack

- Next.js App Router
- React
- TypeScript
- MySQL-compatible database access via `mysql2`
- OpenAI SDK for LLM integration
- Zod for validation

## Setup Instructions

### 1. Install dependencies

```bash
npm install
```

### 2. Configure environment variables

Copy `.env.example` to `.env.local` and update the values.

Required variables:

- `DATABASE_URL` or the individual `DB_*` settings
- `LLM_API_KEY`

Optional variable:

- `LLM_MODEL` (defaults to `gpt-4.1-mini`)

### 3. Start the development server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

## Environment Variables

```env
DATABASE_URL=mysql://username:password@host:4000/database_name?ssl={"rejectUnauthorized":true}
DB_HOST=localhost
DB_PORT=3306
DB_NAME=sales_meeting_prep
DB_USER=root
DB_PASSWORD=your_password
DB_SSL=false
LLM_API_KEY=your_llm_api_key
LLM_MODEL=gpt-4.1-mini
```

## Notes on Connecting to TiDB Cloud

TiDB Cloud is MySQL compatible, so it can be used directly with this application.

1. Create a TiDB Cloud cluster and database.
2. Add an IP allowlist entry for your local machine or deployment platform.
3. Copy the MySQL connection string.
4. Set `DATABASE_URL` in `.env.local`.
5. Ensure SSL is enabled for production and TiDB Cloud usage.

Example:

```env
DATABASE_URL=mysql://USER:PASSWORD@HOST:4000/sales_meeting_prep?ssl={"rejectUnauthorized":true}
```

## How to Run Locally

1. Install Node.js 20+.
2. Install project dependencies with `npm install`.
3. Create `.env.local` from `.env.example`.
4. Point the app to a MySQL-compatible database.
5. Add your `LLM_API_KEY`.
6. Run `npm run dev`.
7. Open `http://localhost:3000`.

## Deployment Option: Vercel

This project includes a simple `vercel.json` for a clean Next.js deployment with basic security headers.

1. Push the project to GitHub.
2. Import the repository into Vercel.
3. Confirm the root directory is `sales-meeting-prep-assistant` if the repository contains other folders.
4. Add the same environment variables in the Vercel project settings.
5. Ensure your TiDB Cloud allowlist permits Vercel access.
6. Deploy.

Recommended production environment variables:

```env
DATABASE_URL=mysql://USER:PASSWORD@HOST:4000/sales_meeting_prep?ssl={"rejectUnauthorized":true}
LLM_API_KEY=your_llm_api_key
LLM_MODEL=gpt-4.1-mini
```

## Future Improvements

- Editable meeting records
- Exportable CRM-ready summaries
- Team collaboration and shared account views
- CRM integrations such as Salesforce or HubSpot
