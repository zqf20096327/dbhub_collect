# MeetIQ — AI Meeting Intelligence Platform

MeetIQ turns meeting recordings into an auditable, searchable workspace. It accepts real audio and video recordings, produces speaker-aware transcripts, extracts grounded meeting intelligence, and keeps every result tied to the user-owned meeting and its original timestamps.

> **Portfolio release:** this repository contains the actual application source, tests, migrations, validation scripts, documentation, and privacy-safe screenshots. It does not include runtime secrets, media uploads, production credentials, or deployment exports.

> **Configuration:** see [Environment Configuration](docs/ENVIRONMENT.md) before running the project. It lists every required managed runtime variable, scope, and safe configuration guidance without including credentials.

## Overview

Recordings alone are difficult to revisit: decisions disappear in long conversations, follow-ups lack ownership, and a transcript without timestamps or speakers is hard to trust. MeetIQ preserves the source recording, creates a diarized transcript, then derives summaries, decisions, action items, questions, sentiment, and semantic answers grounded in the stored transcript.

## Product Preview

The images below are real hosted-preview captures from validated MeetIQ workflows. They have been cropped only to exclude signed-in account identity; no content or UI state has been recreated.

| Dashboard and secure upload | Completed processing timeline |
| --- | --- |
| ![MeetIQ dashboard, meeting library, and secure recording upload](docs/screenshots/dashboard-upload-library.png) | ![MeetIQ completed meeting processing timeline from upload through embedding generation](docs/screenshots/workspace-processing-timeline.png) |

| Meeting workspace | Intelligence and analysis entry points |
| --- | --- |
| ![MeetIQ completed meeting workspace](docs/screenshots/completed-meeting-workspace.png) | ![MeetIQ workspace tabs for overview, transcript, decisions, action items, search, analytics, and speaker mapping](docs/screenshots/workspace-overview-speaker-mapping.png) |

## Key Features

| Area | Implemented capability |
| --- | --- |
| Media ingestion | Secure upload for MP3, WAV, M4A, MP4, and MOV, with server-side size, extension, and MIME validation before S3-compatible object storage. |
| Speech intelligence | Real Deepgram prerecorded speech-to-text, timestamped utterances, and speaker diarization. |
| Workspace | Speaker name mapping, timestamp-seekable transcript, executive summary, decisions, action items, questions, sentiment, analytics, and PDF export. |
| Semantic retrieval | Cached local multilingual embeddings, TiDB native `VECTOR(384)`, server-side `VEC_COSINE_DISTANCE`, ownership filtering, and timestamp-grounded sources. |
| Reliability | Callback-driven analysis continuation, stale-job detection, atomic database leases, bounded backoff, idempotent retries, and terminal failure states. |
| Security | Server-side secrets, OAuth-backed sessions, protected procedures, and ownership checks for every meeting and artifact access path. |

## Technology Stack

| Layer | Technology |
| --- | --- |
| Frontend | React 19, TypeScript, Vite, Tailwind CSS, Radix/shadcn-style components, tRPC React Query, and Recharts. |
| Backend | Node.js, Express, tRPC, Zod, Multer, and Drizzle ORM. |
| Persistence | Managed TiDB/MySQL-compatible database with native `VECTOR(384)` and `VEC_COSINE_DISTANCE`. |
| Storage and identity | S3-compatible object storage with signed URLs, OAuth session authentication, and signed server cookies. |
| AI and ML | Deepgram prerecorded transcription and diarization; built-in LLM gateway; Transformers.js and ONNX multilingual embeddings. |
| Delivery and quality | PDFKit reports, Vitest, TypeScript, pnpm, and Vite production builds. |

## Architecture

![MeetIQ architecture](docs/architecture/meetiq-architecture.png)

The source diagram is maintained in [Mermaid](docs/architecture/meetiq-architecture.mmd). The application pipeline is:

```text
Upload → S3-compatible storage → Deepgram transcription + diarization
      → transcript persistence → grounded LLM analysis
      → local multilingual embeddings → TiDB VECTOR(384)
      → VEC_COSINE_DISTANCE semantic retrieval → analytics + PDF export
```

The React client communicates with the Express/tRPC server. Media records, processing jobs, speakers, transcript segments, intelligence artifacts, analytics inputs, and vector chunks are persisted in a TiDB/MySQL-compatible schema. Deepgram callbacks advance work without requiring an open browser session; a protected scheduled endpoint is prepared for durable stale-job recovery after production publication.

## AI Pipeline

| Component | Responsibility |
| --- | --- |
| **Deepgram** | Asynchronous prerecorded-media transcription with smart formatting, utterance timestamps, diarization, callback delivery, Arabic recovery, and request correlation. |
| **Grounded LLM** | Structured JSON extraction of a summary, topics, decisions, action items, questions, and segment sentiment; grounded answers for semantic-search results. |
| **Local embedding model** | `Xenova/paraphrase-multilingual-MiniLM-L12-v2` via Transformers.js and ONNX. The 384-dimensional model is singleton-loaded, cached, and does not require a paid embedding API. |
| **TiDB vector retrieval** | Persists local vectors in native `VECTOR(384)` and ranks candidates with `VEC_COSINE_DISTANCE` inside the ownership-filtered database query. |
| **PDFKit** | Produces a structured meeting report from stored intelligence, participation data, and transcript content. |

## Semantic Search

MeetIQ does **not** use PostgreSQL or pgvector. A question is embedded locally with the same multilingual model used for transcript chunks. The vector is passed to TiDB, where `VEC_COSINE_DISTANCE` retrieves the closest `VECTOR(384)` chunks after user and meeting ownership predicates are applied. The LLM receives only retrieved, timestamped transcript content and returns an answer with source references, keeping semantic results traceable to the original conversation.

## Reliability and Background Processing

The normal path persists a job, sends Deepgram a short-lived signed media URL, accepts its nonce-correlated callback, persists diarized turns, and launches analysis continuation on the server. The durable recovery path covers callbacks or analysis runs that never finish:

| Control | Behavior |
| --- | --- |
| Conservative stale thresholds | `Transcribing` becomes eligible after 15 minutes; audio extraction, speaker detection, analysis, and embedding stages become eligible after 10 minutes. |
| Atomic claim | A conditional TiDB update assigns a 110-second lease token and increments the recovery attempt counter, so concurrent Heartbeats cannot process the same job. |
| Safe recovery | Transcription-stage jobs are resubmitted using their persisted callback origin. Analysis-stage failures reuse the existing transcript instead of retranscribing media. |
| Bounded retries | Transient failures back off for 1, 2, then 4 minutes. Recovery stops after three attempts and records `STALE_RECOVERY_EXHAUSTED`. |
| Durable trigger | An authenticated every-minute Heartbeat is prepared, but is intentionally activated only after the first production publication. |

## Security

Secrets are read only on the server. The client does not receive Deepgram, database, OAuth-server, or built-in LLM gateway credentials. Meeting lists, workspaces, media redirects, reports, retries, speaker mapping, action changes, and semantic retrieval all enforce user/meeting ownership in server code. See [Security Model](docs/SECURITY.md).

## Testing and Validation

The latest validation ran **25 automated tests across 11 test files**, a zero-error TypeScript check, and a production build with the local embedding model warmed for runtime use. The suite includes provider configuration, callback parsing, intelligence validation, action workflow, TiDB vector behavior, stale-job policy, and lease/retry worker behavior. GitHub Actions repeats the type check, tests, and production build on pushes and pull requests. The credential-authentication check runs when `DEEPGRAM_API_KEY` is configured; secret-free clones still run the complete deterministic suite.

Real end-to-end validation also covered MP4 and MOV processing, a private Arabic-language recording, and a public 17-minute 22-second four-party AMI meeting. The AMI run persisted 211 transcript segments, four speakers, two decisions, six action items, four questions, and 11 native vectors. A real missed-callback simulation was recovered through a fresh Deepgram submission, callback persistence, automatic continuation, embedding generation, and a final `Completed` job state. Full evidence is retained in [`validation/`](validation/).

## Project Structure

```text
client/                         React 19 interface: meetings library and workspace
  src/pages/                    Home, meeting workspace, and UI states
  src/components/               Reusable product and UI components
server/                         Express server, tRPC contracts, and pipeline services
  services/                     Deepgram, intelligence, embeddings, processing, PDF modules
  _core/                        OAuth, storage, LLM, scheduling, and runtime integrations
drizzle/                         TiDB schema, relations, and ordered SQL migrations
shared/                          Shared constants, types, and errors
scripts/                         Build warming and real validation utilities
docs/                            API, security, deployment, architecture, screenshots
tests/                           Tests are co-located with their service or component source
validation/                     Recorded non-secret validation outcomes
```

The repository preserves the implemented architecture rather than adding cosmetic `frontend/`, `backend/`, or worker directories that do not exist in the running system.

## Environment Variables

Use the variable names in [Environment Configuration](docs/ENVIRONMENT.md) with a private local secret manager or deployment secret store. Do not commit real values. `DEEPGRAM_API_KEY` is required for transcription; `MEETIQ_EMBEDDING_MODEL` is optional and defaults to the multilingual local model. No OpenAI embedding credential is required or used.

## Local Development

### Prerequisites

- Node.js 22 or later and pnpm 10.
- A TiDB/MySQL-compatible database with the versioned schema migrations applied.
- S3-compatible storage, a Deepgram project key, OAuth configuration, and an LLM gateway appropriate to the runtime environment.

### Install and run

```bash
pnpm install
pnpm run dev
```

The development command runs the Express server and Vite-integrated React client. Apply the ordered SQL files in `drizzle/` using the database migration workflow for your environment before starting against a new database. Configure secrets privately using the names documented in `docs/ENVIRONMENT.md`.

### Verify and build

```bash
pnpm check
pnpm test
pnpm build
```

`pnpm build` builds the client and server and warms the local embedding model cache. Some scripts in `scripts/` call real configured services; use them only in a controlled environment with explicit authorization.

## API and Deployment Documentation

- [API Reference](docs/API.md)
- [Security Model](docs/SECURITY.md)
- [Deployment Notes](docs/DEPLOYMENT.md)
- [Architecture Diagram Source](docs/architecture/meetiq-architecture.mmd)

## Known Limitations

MeetIQ accepts files up to 50 MB and buffers an upload in request memory before storage. The platform uses diarization labels and user-supplied mapping, not voice-biometric identity recognition. TiDB native vector storage and exact cosine-distance retrieval are implemented, but an approximate vector index is not provisioned in the current managed configuration. A cold instance still incurs ordinary local-model initialization time even though the model is warmed during build.

## Roadmap

- Evaluate TiDB vector indexing options when the managed environment supports a suitable index path at production scale.
- Add provider adapters for additional speech-to-text services while preserving the existing processing contract.
- Expand meeting analytics with cross-meeting trends and team-level reporting.
- Add production observability dashboards, alerting, and recovery runbooks.
- Evolve the one-minute Heartbeat into a scalable worker topology for higher-volume workloads.

## References

[1] [Xenova/paraphrase-multilingual-MiniLM-L12-v2 model documentation](https://huggingface.co/Xenova/paraphrase-multilingual-MiniLM-L12-v2)

[2] [Transformers.js Node.js inference documentation](https://huggingface.co/docs/transformers.js/en/tutorials/node)

[3] [Deepgram prerecorded callbacks](https://developers.deepgram.com/docs/callback)
