# Flappy Boi

A polished, modern take on the classic Flappy Bird experience built with React, TypeScript, Vite, Tailwind CSS, and Supabase.

Flappy Boi brings the nostalgic arcade loop to the browser with smooth canvas-based gameplay, dynamic day/night visuals, sound effects, configurable settings, and a live leaderboard powered by Supabase.

## ✨ Features

- Responsive Flappy Bird gameplay with tap/click/keyboard controls
- Smooth animated canvas rendering
- Day/night cycle that shifts the atmosphere every 10 points
- Sound effects and game settings
- Local best-score tracking
- Public leaderboard with Supabase integration
- Clean, mobile-friendly UI built with Tailwind CSS

## 🛠️ Tech Stack

- React + TypeScript
- Vite
- Tailwind CSS
- Supabase
- Lucide Icons

## 🚀 Getting Started

### 1. Install dependencies

```bash
npm install
```

### 2. Start the development server

```bash
npm run dev
```

Open the local Vite URL in your browser to play.

## 🔧 Environment Setup

Create a local environment file named `.env` in the project root and add your Supabase credentials:

```env
VITE_SUPABASE_URL=https://your-project-ref.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key
```

You can also use the newer style names:

```env
NEXT_PUBLIC_SUPABASE_URL=https://your-project-ref.supabase.co
NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY=your-publishable-key
```

A sample file is included at [.env.example](.env.example).

## 🗄️ Supabase Setup

The app expects a `scores` table for the leaderboard.

Run the following SQL in your Supabase SQL Editor:

```sql
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS scores (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  player text NOT NULL,
  score integer NOT NULL,
  created_at timestamptz DEFAULT now()
);

ALTER TABLE scores ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "anon_select_scores" ON scores;
CREATE POLICY "anon_select_scores" ON scores FOR SELECT
  TO anon, authenticated USING (true);

DROP POLICY IF EXISTS "anon_insert_scores" ON scores;
CREATE POLICY "anon_insert_scores" ON scores FOR INSERT
  TO anon, authenticated WITH CHECK (true);

DROP POLICY IF EXISTS "anon_delete_scores" ON scores;
CREATE POLICY "anon_delete_scores" ON scores FOR DELETE
  TO anon, authenticated USING (true);

CREATE INDEX IF NOT EXISTS scores_score_desc_idx ON scores (score DESC);
```

## 📁 Project Structure

```text
src/
  components/
    FlappyBird.tsx
    Leaderboard.tsx
  lib/
    supabase.ts
  App.tsx
  main.tsx
supabase/
  migrations/
    20260722103945_create_scores_table.sql
```

## ▶️ Available Scripts

- `npm run dev` — start the local development server
- `npm run build` — build the project for production
- `npm run preview` — preview the production build locally
- `npm run typecheck` — run TypeScript checks
- `npm run lint` — lint the codebase

## 🎮 How to Play

- Click, tap, or press the spacebar to flap
- Avoid the pipes
- Survive as long as you can and beat your best score
- Enter your name after a good run to appear on the leaderboard

## 🌟 Notes

This project is designed as a fun browser game with a lightweight online leaderboard, making it a great foundation for arcade-style web apps or personal portfolio projects.

