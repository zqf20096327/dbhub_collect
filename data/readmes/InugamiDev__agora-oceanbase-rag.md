![CI](https://github.com/InugamiDev/agora-oceanbase-rag/actions/workflows/ci.yml/badge.svg) ![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg) ![Next.js 15](https://img.shields.io/badge/Next.js-15-black?logo=next.js)

# Agora ConvoAI + OceanBase Vector RAG

A multi-use-case voice AI showcase that combines Agora's Conversational AI Engine with OceanBase native vector search for Retrieval-Augmented Generation.

Pick a persona: customer support, sales consultant, or real estate advisor. Each persona speaks through Agora RTC and uses a separate logical knowledge collection stored in one OceanBase `documents` table.

## Stack

- Next.js 15 App Router and React 19
- Agora RTC, RTM, and Conversational AI Engine
- OceanBase 4.3.x+ native vector storage and HNSW vector indexes
- OpenAI `text-embedding-3-small` and `gpt-4o-mini`
- Agora-managed Deepgram STT and MiniMax TTS
- Three.js and React Three Fiber for the 3D avatar

## Architecture

```text
User voice -> Agora RTC -> CAI Agent
                       -> Deepgram STT
                       -> /api/chat
                       -> OpenAI embedding
                       -> OceanBase VECTOR(1536) search
                       -> GPT-4o-mini with retrieved context
                       -> MiniMax TTS
                       -> Agora RTC audio + Agora RTM text
                       -> client-side avatar lip sync
```

## Project Structure

```text
src/lib/
  agora.ts             Agora token generation
  embeddings.ts        OpenAI embeddings
  oceanbase.ts         OceanBase connection, upsert, vector search
  viseme-engine.ts     Text-to-viseme conversion

scripts/
  setup-oceanbase.ts   Create database, table, and vector index
  seed-data.ts         Embed and insert sample documents
```

The UI, Agora lifecycle routes, avatar components, hooks, and viseme engine are carried over from the sibling Couchbase demo. Only the vector backend changed.

## Prerequisites

- Node.js 18+
- Agora account and a project with Conversational AI enabled
- OpenAI API key
- OceanBase Cloud account, or OceanBase Community Edition for local/self-hosted testing

No Deepgram or MiniMax keys are required for the default flow because Agora provides managed STT and TTS.

## OceanBase Cloud Setup

1. Go to [cloud.oceanbase.com](https://cloud.oceanbase.com) and create an OceanBase Cloud tenant.
2. Create or choose a MySQL-compatible tenant.
3. Create a database user with permission to create databases, tables, and indexes.
4. Copy the public host, port, username, and password into `.env`.
5. Set `OCEANBASE_TLS=true` for OceanBase Cloud unless your tenant connection guide says otherwise.

The setup script creates the `knowledge_base` database, a single `documents` table with `VECTOR(1536)`, a collection B-tree index, and an HNSW vector index.

## OceanBase Community Edition Alternative

For local testing, run OceanBase CE with the MySQL-compatible port exposed:

```bash
docker run -p 2881:2881 oceanbase/oceanbase-ce:latest
```

Then set:

```env
OCEANBASE_HOST=127.0.0.1
OCEANBASE_PORT=2881
OCEANBASE_USER=root@test
OCEANBASE_PASSWORD=
OCEANBASE_DATABASE=knowledge_base
OCEANBASE_TABLE=documents
OCEANBASE_TLS=false
```

Confirm your image version is OceanBase 4.3.x or newer because native vector support is required.

## Environment Variables

Copy `.env.example` to `.env` and fill in:

| Variable | Purpose |
| --- | --- |
| `AGORA_APP_ID` | Server-side Agora App ID |
| `AGORA_APP_CERTIFICATE` | Server-side Agora App Certificate |
| `NEXT_PUBLIC_AGORA_APP_ID` | Client-side Agora App ID |
| `OCEANBASE_HOST` | OceanBase host |
| `OCEANBASE_PORT` | MySQL-compatible OceanBase port, usually `2881` |
| `OCEANBASE_USER` | OceanBase user, for example `root@test` |
| `OCEANBASE_PASSWORD` | OceanBase password |
| `OCEANBASE_DATABASE` | Database created by setup, default `knowledge_base` |
| `OCEANBASE_TABLE` | Documents table, default `documents` |
| `OCEANBASE_TLS` | `true` for OceanBase Cloud, `false` for local CE |
| `OPENAI_API_KEY` | Embeddings and LLM completions |
| `NEXT_PUBLIC_APP_URL` | Public URL Agora CAI can call for `/api/chat` |

For local RAG testing with Agora CAI, expose the app with a public tunnel such as ngrok and set `NEXT_PUBLIC_APP_URL` to that HTTPS URL. If the agent cannot reach your local app, it will fall back to the non-RAG LLM path.

## Getting Started

```bash
npm install
cp .env.example .env
# fill in Agora, OceanBase, and OpenAI credentials
npm run setup
npm run seed
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) and pick a use case.

## Data Model

This demo uses one table and stores persona routing in the `collection` column:

```sql
CREATE TABLE documents (
  id VARCHAR(64) PRIMARY KEY,
  collection VARCHAR(64) NOT NULL,
  text TEXT NOT NULL,
  source VARCHAR(128),
  chunk_index INT,
  embedding VECTOR(1536),
  INDEX idx_collection (collection)
);

CREATE VECTOR INDEX idx_documents_embedding
ON documents(embedding)
WITH (distance=cosine, type=hnsw);
```

The logical collections are `customer_support`, `sales`, and `real_estate`.

## How RAG Works Here

1. The user speaks through Agora RTC.
2. The CAI agent transcribes speech to text.
3. `/api/chat` embeds the latest user message.
4. OceanBase ranks matching rows with `cosine_distance(embedding, VECTOR('[...]'))`.
5. The app converts distance to a higher-is-better score with `1 - distance`.
6. Relevant chunks are injected into the LLM context.
7. The answer streams back to the CAI agent for speech synthesis.

## Scripts

| Command | Description |
| --- | --- |
| `npm run dev` | Start Next.js dev server |
| `npm run build` | Production build |
| `npm run start` | Run production build |
| `npm run setup` | Create OceanBase database, table, and vector index |
| `npm run seed` | Embed and insert sample knowledge documents |

## Troubleshooting

| Issue | Fix |
| --- | --- |
| `VECTOR` type is unknown | Use OceanBase 4.3.x or newer and a MySQL-compatible tenant |
| Vector index creation fails | Confirm the tenant supports native vector indexes; rerun `npm run setup` after table creation |
| RAG returns no hits | Run `npm run seed`, verify `OCEANBASE_DATABASE` and `OCEANBASE_TABLE`, and confirm the selected persona collection has rows |
| OceanBase Cloud connection fails | Set `OCEANBASE_TLS=true`, check allowlists/firewalls, and verify host/port/user format |
| Local CE connection fails | Confirm the Docker container is healthy and port `2881` is published |
| Agent does not call RAG | Set `NEXT_PUBLIC_APP_URL` to a public HTTPS URL reachable by Agora CAI |
| OpenAI embedding errors | Verify `OPENAI_API_KEY` and account quota |

## Notes

OceanBase vector constructor binding is implemented as `VECTOR(<escaped JSON array string>)` in `src/lib/oceanbase.ts` because direct parameter binding for vector expressions is not consistently documented across MySQL-compatible drivers. Non-vector values remain parameterized through `mysql2`.
