# Byte-Sized Knowledge

A platform for publishing dense, interactive reference guides on any topic. Each guide is a self-contained encyclopedia with diagrams, examples, and structured navigation — packaged into a fast, searchable, shareable site.

The current guides cover software engineering (system design, design patterns, databases, cloud architecture, AI), but the platform is topic-agnostic. A guide on history, medicine, law, finance, or anything else fits the same structure.

## Features

- **Interactive encyclopedias** — self-contained guides with diagrams, code, and structured navigation
- **Command palette** (`Cmd/Ctrl + K`) — searches across all guides and every concept inside them
- **Deep links** — every concept has a shareable URL: `/topics/[slug]?concept=[id]`
- **Knowledge cards** — auto-generated OG images for rich social media previews
- **Favourites** — save concepts to a personal revision list, persisted in `localStorage`
- **Dark mode** — manual toggle + system preference, no flash on load
- **SEO-ready** — sitemap, `robots.txt`, JSON-LD structured data, per-concept meta tags

## Current Guides

| Guide | Concepts |
|---|---|
| 🏗️ System Design Encyclopedia | 39 |
| 🧩 Design Patterns Encyclopedia | 23 |
| 🐘 PostgreSQL Internals | 11 |
| ☁️ Cloud Architecture Patterns | 24 |
| 🤖 AI/LLM Encyclopedia | 25 |
| ⚙️ Production AI Agents Encyclopedia | 13 |

## Getting Started

Requires **Node.js ≥ 18**.

```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

```bash
npm run build   # production build
npm run start   # serve the production build
```

## Project Structure

```
app/                         # Next.js App Router pages + API routes
  layout.tsx                 # Root layout: header, dark mode, skip link
  page.tsx                   # Home page
  favorites/page.tsx         # Saved concepts page
  topics/[slug]/page.tsx     # Guide page with JSON-LD + per-concept metadata
  api/og/[topic]/[concept]/  # Edge route: generates OG knowledge cards
  sitemap.ts                 # Dynamic sitemap
  robots.ts                  # robots.txt

components/
  encyclopedias/             # Guide files (*.jsx) + next/dynamic wrappers
  TopicGrid.tsx              # Home page card grid with live search filter
  TopicViewer.tsx            # Guide page shell: accessible tablist + breadcrumb
  TopicRenderer.tsx          # Lazy-load drawer for encyclopedias
  SearchBar.tsx              # Cmd+K command palette
  FavoriteButton.tsx         # Heart icon — save/unsave a concept
  SharePopover.tsx           # Share a concept: copy URL + OG preview
  ThemeToggle.tsx            # Dark/light mode toggle

data/
  topics.ts                  # Guide metadata (id, title, description, subtopics)
  searchIndex.ts             # All concepts across all guides

hooks/
  useFavorites.ts            # localStorage favourites with cross-tab sync
  useTheme.ts                # Dark mode preference (localStorage + system)

lib/
  conceptUtils.ts            # Concept ↔ subtopic resolution + URL helpers
  favorites.ts               # Pure localStorage read/write helpers
  ogColors.ts                # Guide → hex palette for OG image generation
```

## URL Scheme

| URL | Description |
|---|---|
| `/` | Home — guide grid with search |
| `/topics` | All guides |
| `/topics/[slug]` | A guide (e.g. `/topics/system-design`) |
| `/topics/[slug]?concept=[id]` | Deep link to a specific concept |
| `/favorites` | Saved concepts |
| `/api/og/[slug]/[id]` | OG knowledge card image (1200×630 PNG) |
| `/sitemap.xml` | Full sitemap |
| `/robots.txt` | Robots file |

## Deep Links

Every concept has a shareable URL. Use the share icon on any concept row to copy it. When opened, the page auto-selects the matching tab, opens the guide drawer, and navigates to that concept:

```
/topics/postgres-internals?concept=8
/topics/system-design?concept=load-balancing
/topics/ai-llm?concept=21
```

## OG Image API

```
GET /api/og/[slug]/[conceptId]
```

Returns a 1200×630 PNG knowledge card with the concept title, description, and guide branding. Automatically referenced in `og:image` and `twitter:card` metadata for any concept deep-link.

## Favourites

Stored in `localStorage["byte-sized-knowledge-favorites"]` as a JSON array. Exportable from `/favorites` as a `.json` file. The nav badge updates live across browser tabs.

## Adding a Guide

See `CLAUDE.md` for the step-by-step process. In short: add the encyclopedia file, register it in `data/topics.ts` and `data/searchIndex.ts`, create a `next/dynamic` wrapper, and add it to `TopicRenderer`'s map.

## Tech

- [Next.js 16](https://nextjs.org) — App Router, SSG, Edge API routes
- [React 19](https://react.dev)
- [Tailwind CSS v4](https://tailwindcss.com)
- [TypeScript 5](https://www.typescriptlang.org)
- [`next/og`](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/opengraph-image) — OG image generation
