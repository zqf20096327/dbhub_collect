# fundkeep-indexer

Indexes events from the [fundkeep-contract](https://github.com/fundkeep-web/fundkeep-contract) Soroban contract into SQLite, and serves them over a small REST API for [fundkeep-app](https://github.com/fundkeep-web/fundkeep-app)'s dashboard and activity feed.

This is the read side of the topology: the frontend writes directly to the chain via RPC (see `@fundkeep/sdk`), and reads goal/activity history from here instead of re-deriving it from raw events client-side.

**Live Testnet service:** [fundkeep-indexer.onrender.com/health](https://fundkeep-indexer.onrender.com/health) · **Contract:** [`CBYUM...DDFAH`](https://stellar.expert/explorer/testnet/contract/CBYUMUNDBGT5JTYX62SSFH5NTK2ELLRT2PP3LLZOI757JB4BULDDDFAH) · **App:** [fundkeep.vercel.app](https://fundkeep.vercel.app)

## How it works

A poller calls the Soroban RPC's `getEvents` on an interval, starting from a saved cursor (or a recent ledger window on first run), decodes the four event types `fundkeep-contract` publishes (`goal_created`, `deposit`, `unlock`, `withdraw`), and upserts them into two SQLite tables: `goals` (current state per goal) and `activity` (an append-only log). A small Express API reads from those tables.

## Requirements

- Node.js v22.12+

## Setup

```bash
npm install
cp .env.example .env   # fill in CONTRACT_ID at minimum
npm run dev
```

## API

| Endpoint | Description |
|---|---|
| `GET /health` | `{ ok, lastLedger }` |
| `GET /api/goals/:owner` | All indexed goals for a Stellar address |
| `GET /api/activity/:owner?limit=100` | Activity log for a Stellar address, newest first |

## Environment Variables

See [`.env.example`](.env.example). `CONTRACT_ID` is the only required one; everything else has a sane default for testnet.

## Scripts

```bash
npm run dev        # tsx watch mode
npm run build       # compile to dist/
npm start            # run the compiled build
npm test              # vitest
npm run typecheck      # tsc --noEmit
```

## Deploying

The committed [`render.yaml`](render.yaml) is the authoritative Render Blueprint. It uses Node 22, a health check, the verified contract allowlist, restrictive production CORS and a persistent disk for SQLite. The disk is required: without it, both indexed data and the ledger cursor reset on every deploy.
