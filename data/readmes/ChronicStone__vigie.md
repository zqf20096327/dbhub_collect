<p align="center">
  <a href="https://vigie.chronicstone.dev"><img src=".github/cover.png" alt="Vigie: self-hosted telemetry for Node apps, on OpenTelemetry and ClickHouse" width="100%"></a>
</p>

<p align="center">
  <a href="https://vigie.chronicstone.dev/docs/getting-started/introduction"><b>Docs</b></a> ·
  <a href="https://vigie.chronicstone.dev/docs/getting-started/quickstart">Quickstart</a> ·
  <a href="https://vigie.chronicstone.dev/docs/definitions/overview">Definitions API</a> ·
  <a href="https://vigie.chronicstone.dev/docs/features/mcp">MCP</a> ·
  <a href="https://vigie.chronicstone.dev/docs/self-hosting/deploy">Self-hosting</a>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-D9685C" alt="MIT license"></a>
  <img src="https://img.shields.io/badge/OpenTelemetry-native-425CC7" alt="OpenTelemetry native">
  <img src="https://img.shields.io/badge/storage-ClickHouse-FAFF69?labelColor=333" alt="ClickHouse">
</p>

**Vigie** watches a running app and tells you what is wrong in plain sentences: which requests fail and why, which background jobs are stuck, which provider is refusing calls, and what to do about it. Logs, traces, tasks, issues, alerts, a status page and MCP, in one small process you run yourself. Your telemetry never leaves your machines.

Adonis and NestJS connect with one command. Anything that speaks OpenTelemetry works too, in any language.

## Quickstart

```sh
bunx @vigiejs/cli --seed
```

Vigie is now on `http://localhost:5310`, with a day of demo telemetry from a made-up shop. ClickHouse comes from an installed binary, Docker, or a download. No sign-in on your machine.

Then connect your app:

```sh
node ace add @vigiejs/adonis      # Adonis
npx @vigiejs/nestjs init          # NestJS
```

The installer finds Vigie, sets up traces, writes `VIGIE_URL` and `VIGIE_KEY`, and sends a test event. On a server, it opens a page where someone signed in allows the app, so nobody copies a key.

Anything else: `OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318`. A log record with `method`, `status` and `durationMs` is a request; one with `task.kind` is a background task. [The full contract](https://vigie.chronicstone.dev/docs/connect/any-stack).

<p align="center">
  <img src=".github/screen-overview.png" alt="Vigie overview: traffic, what needs you, slowest routes" width="100%">
</p>

## What you get

- **Requests** as one wide event each: route, status, duration, user and your own fields, joined to the trace, the queries and the outgoing calls.
- **Tasks** with every attempt and why it failed, skipped or will retry. What is stuck, what runs late, which worker died.
- **Issues** grouped by cause, with the why and the fix in plain words.
- **Processes** across several jobs, such as "from payment to parcel", with the instances stuck at each step.
- **Alerts** on error rates, latency, stuck tasks, metrics, silence or any SQL, to Slack, Discord, email, webhooks or Linear.
- **A status page** that says in a sentence what is wrong and what still works, with 90 days of history.
- **MCP** with more than a hundred tools, so agents read the same screens you do.
- **Secrets masked at ingest**, before anything is stored.

<p align="center">
  <img src=".github/screen-process.png" alt="A process: orders from payment to parcel, with the stuck and failed ones" width="100%">
</p>

## Your app, in code

Everything specific to your app lives in `definitions/`, typed TypeScript next to your app's code. It reloads when you save and deploys with the app.

```ts
// definitions/processes/acme.ts
import { defineProcess, step } from '@vigiejs/sdk'

export const fulfilment = defineProcess({
  id: 'order-fulfilment',
  title: 'Order fulfilment',
  subject: 'order',
  sla: '4h',
  steps: [
    step.task('paynest.payment.ingest', { label: 'Payment confirmed by Paynest', expectWithin: '30m' }),
    step.task('parcelo.ship', { label: 'Shipment created at Parcelo', expectWithin: '15m' }),
  ],
})
```

| Define | With |
|---|---|
| How an event reads | `defineLogRenderer` |
| Why an error happens, and the fix | `defineErrorRenderer` |
| A flow across several tasks | `defineProcess` |
| A screen, a dashboard | `definePage`, `defineDashboard` |
| Alerts and uptime checks | `defineAlert`, `defineMonitor` |
| The public status page | `defineStatusPage` |
| An MCP tool | `defineTool` |
| Secrets in your paths | `defineRedactor` |

[Every definition, with examples](https://vigie.chronicstone.dev/docs/definitions/overview). The ones in [`definitions/`](definitions) here describe Acme, a made-up shop, and power the demo data.

## On a server

```sh
git clone https://github.com/ChronicStone/vigie.git && cd vigie
deploy/install.sh --domain vigie.example.com
```

Docker, ClickHouse and HTTPS from Caddy. It prints the setup code for the first owner and the first ingest key. Leave out `--domain` to keep it private on `127.0.0.1`, behind Tailscale or an SSH tunnel. [Deploy guide](https://vigie.chronicstone.dev/docs/self-hosting/deploy).

## Packages

| Package | |
|---|---|
| [`@vigiejs/cli`](.) | The server, the app and the `vigie` command: `bunx @vigiejs/cli --seed` |
| [`@vigiejs/sdk`](packages/sdk) | Types for your `definitions/`: `npm i -D @vigiejs/sdk` |
| [`@vigiejs/adonis`](packages/adonis) | `node ace add @vigiejs/adonis` |
| [`@vigiejs/nestjs`](packages/nestjs) | `npx @vigiejs/nestjs init` |

## Develop

```sh
bun install
bun run dev -- --seed       # Vigie itself, with hot reload
bun run typecheck
bun run test                # unit
bun run test:integration    # needs CLICKHOUSE_URL and a build
```

The docs and the landing page live in [`site/`](site): `cd site && bun install && bun run dev`.

Built with Bun, TanStack Start, Base UI, Better Auth, ClickHouse and SQLite.

## License

[MIT](LICENSE)
