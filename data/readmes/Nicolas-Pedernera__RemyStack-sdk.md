![RemyStack](./assets/banner.png)

  <img src="https://img.shields.io/badge/status-early%20access-B08D3E" alt="Status"/>
</p>

<p align="center">
  <a href="https://remy-stack-admin.vercel.app">Live demo</a> ·
  <a href="#installation">Installation</a> ·
  <a href="#quickstart">Quickstart</a> ·
  <a href="#supported-connectors">Connectors</a> ·
  <a href="#roadmap">Roadmap</a>
</p>

---

## Table of Contents

- [Why RemyStack](#why-remystack)
- [How it works](#how-it-works)
- [Live demo](#live-demo)
- [Supported connectors](#supported-connectors)
- [Installation](#installation)
- [Quickstart](#quickstart)
- [Configuration](#configuration)
- [Roadmap](#roadmap)
- [Website](#website)
- [Contributing](#contributing)
- [License](#license)

## Why RemyStack

B2B companies in Latin America — fintechs, logtechs, healthtechs — spend weeks wiring up payment gateways and country-specific e-invoicing APIs by hand, with no standard way to monitor failures, retries, or contract changes. When an external API breaks, most teams find out when a customer complains.

RemyStack is a thin orchestration layer that sits between your backend and the third-party APIs you depend on. You send an event through the SDK; RemyStack handles delivery, retries with backoff, and gives you a live view of what succeeded, what's pending, and what failed — and why.

It's built **by developers, for developers**: no business-user automation UI, no drag-and-drop workflows. Just an SDK, a clear event model, and a monitoring dashboard your engineering team will actually use.

## How it works

```
Your backend  →  RemyStack SDK  →  Orchestration engine (queues + retries)  →  Connector  →  External API
                                              ↓
                                     Monitoring dashboard
                                (live status, retries, logs)
```

- Events are queued and retried automatically (backoff: 1 → 5 → 15 → 30 → 60 min) if a connector call fails.
- Every tenant is isolated — this repo (the SDK) only talks to the API with your tenant's API key, nothing else.
- The orchestration engine and dashboard are closed source; this repo is the client library you integrate into your own backend.

## Live demo

You can see a real (demo) tenant running live at **[remy-stack-admin.vercel.app](https://remy-stack-admin.vercel.app)** — event status, retry counts, and connector health, updated in real time.

> This is a demo environment for evaluation. Production access is by pilot invite — see [Website](#website) below.

## Supported connectors

| Category | Connectors |
| --- | --- |
| Payments | Mercado Pago, Stripe, PayPal, dLocal |
| E-invoicing | Facturapi (México), CUCU / SIN (Bolivia) |

More connectors are added as pilot customers need them — see [Roadmap](#roadmap).

## Installation

```bash
npm install @remystack/sdk
```

## Quickstart

```ts
import { RemyStackClient } from "@remystack/sdk";

const client = new RemyStackClient({
  apiKey: process.env.REMYSTACK_API_KEY!,
});

await client.sendEvent({
  connector: "mercadopago",
  type: "payment.created",
  payload: {
    orderId: "1234",
    amount: 1500,
    currency: "BOB",
  },
});
```

RemyStack queues the event, retries automatically on failure, and surfaces delivery status on your dashboard — no polling, no manual retry logic in your codebase.

## Configuration

| Option    | Type   | Required | Description                          |
| --------- | ------ | -------- | -------------------------------------- |
| `apiKey`  | string | Yes      | Your tenant's API key                  |
| `baseUrl` | string | No       | Override the default API endpoint      |

## Roadmap

- [x] Core SDK — event submission, retries, per-tenant auth
- [x] 6 production connectors (payments + e-invoicing)
- [x] Monitoring dashboard
- [ ] Public API reference docs
- [ ] Additional LatAm e-invoicing connectors (Colombia, Peru, Chile)
- [ ] Public observability metrics (Grafana-style)

## Website

- **Now:** live demo dashboard at [remy-stack-admin.vercel.app](https://remy-stack-admin.vercel.app)
- **Coming soon:** [remystack.com](https://remystack.com) — marketing site + public docs

## Contributing

This repo (the SDK) is open for issues and PRs. Found a bug, or a connector you'd like to see supported? [Open an issue](https://github.com/Nicolas-Pedernera/RemyStack-sdk/issues).

## License

MIT — see [LICENSE](./LICENSE).

## Capturas

**Pantalla de conexión al core-engine**
![Conectar al motor](./assets/connect.png)

**Dashboard de monitoreo en tiempo real**
![Monitor de eventos](./assets/dashboard.png)
