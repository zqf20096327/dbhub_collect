# ACTC — Agent Commerce Transaction Coordinator

Saga-based distributed transaction middleware for [UCP](https://ucp.dev) + [AP2](https://github.com/google-agentic-commerce/AP2) agent checkout flows.

## Problem

Agent commerce involves three independent state machines controlled by different parties:

| Protocol | State Machine | Controller |
|----------|--------------|------------|
| UCP | `incomplete → ready_for_complete → completed / canceled` | Merchant |
| AP2 | `IntentMandate → CartMandate → PaymentMandate → Receipt` | Agent Platform |
| Payment Rail | `pending → authorized → captured / declined / refunded` | Payment Processor |

When any leg times out, crashes, or returns ambiguous results, these states tear apart:
- **Money captured, no order** — payment went through but UCP completion timed out
- **Order created, payment declined** — UCP shows completed but the card was rejected
- **Mandates dangling** — SD-JWT+kb signed but checkout was canceled

ACTC coordinates these three protocols using the Saga pattern with crash recovery, ensuring every transaction reaches a consistent terminal state.

## Install

```bash
npm install actc-core
```

Requires Node.js 18+. Single runtime dependency: `better-sqlite3`.

## Quick Start

```typescript
import { ACTC } from 'actc-core';
import { DefaultUCPAdapter } from 'actc-core/adapters/ucp-adapter';
import { DefaultAP2Adapter } from 'actc-core/adapters/ap2-adapter';

const actc = new ACTC(ucpAdapter, ap2Adapter, paymentRailAdapter, {
  persistence: 'sqlite',
  sqlitePath: './actc.db',
});

await actc.initialize(); // runs crash recovery

const result = await actc.executeCheckout({
  merchantEndpoint: 'https://merchant.com/ucp/v1',
  merchantProfileUrl: 'https://merchant.com/.well-known/ucp',
  lineItems: [{ id: 'item_1', title: 'Widget', quantity: 2, price: 2500 }],
  signingKeyId: 'platform_key_001',
  correlationId: 'order_12345',
});

if (result.context.finalStatus === 'confirmed') {
  // Both sides consistent — order placed, payment captured
}
```

## Architecture

```
ACTC SDK (embedded in your process)
├── Saga Engine          Forward execution + backward compensation
├── Recovery Engine      Crash recovery on startup
├── Reconciliation Engine  Periodic cross-protocol state comparison
├── WAL (Hash Chain)     Tamper-evident audit log
├── Idempotency Manager  Exactly-once execution
└── Persistence          SQLite (default) / pluggable backend
         │
    ┌────┴────┐    ┌────┴────┐    ┌────┴────┐
    │  UCP    │    │  AP2    │    │ Payment │
    │ Adapter │    │ Adapter │    │  Rail   │
    └─────────┘    └─────────┘    └─────────┘
```

### 6-Step Checkout Saga

| # | Step | Timeout | Compensate |
|---|------|---------|------------|
| 1 | Create UCP checkout session | 15s | Cancel session |
| 2 | Verify readiness + merchant JWS auth | 60s | Cancel session |
| 3 | Generate AP2 mandates (SD-JWT+kb) | 10s | No-op (expire naturally) |
| 4 | Complete checkout | 90s | **Check actual state first**, then cancel or forward |
| 5 | Verify payment outcome | 30s | Refund if captured + order failed |
| 6 | Finalize | 5s | No-op |

Step 4's compensation is the critical safety mechanism — it queries the actual UCP state before deciding whether to cancel, wait, or acknowledge completion.

## Adapters

ACTC never calls external APIs directly. You provide adapter implementations:

```typescript
// Use the built-in HTTP adapter for UCP
const ucpAdapter = new DefaultUCPAdapter({
  resolvePublicKey: async (url) => fetchMerchantJwk(url),
});

// Use the built-in JSON-RPC adapter for AP2
const ap2Adapter = new DefaultAP2Adapter({
  credentialProviderEndpoint: 'http://localhost:8002/rpc',
});

// Implement PaymentRailAdapter for your payment processor
class StripeAdapter implements PaymentRailAdapter {
  async queryPaymentState(params) { /* ... */ }
  async cancelPayment(params) { /* ... */ }
  async refundPayment(params) { /* ... */ }
}
```

## Safety Guarantees

- **Crash recovery**: Incomplete sagas resume automatically on restart
- **Idempotency**: Every step bound to a unique key — safe to retry
- **WAL hash chain**: SHA-256 linked entries detect tampering via `verifyIntegrity(sagaId)`
- **Poisoned state**: If compensation fails, saga enters `Poisoned` status for manual review
- **No secrets stored**: ACTC never holds payment processor API keys or raw card numbers

## Testing

```bash
npm test              # 44 unit + integration tests
npm run test:e2e      # 29 E2E tests against live HTTP mock servers
npm run test:all      # everything
```

## API

```typescript
const actc = new ACTC(ucpAdapter, ap2Adapter, paymentAdapter, config);

await actc.initialize();                          // setup + crash recovery
await actc.executeCheckout(params);               // full 6-step saga
await actc.getSagaState(sagaId);                  // query by saga ID
await actc.getSagaByCorrelation(correlationId);   // query by external ID
await actc.reconcile();                           // manual reconciliation run
await actc.verifyIntegrity(sagaId);               // WAL hash chain check
await actc.cleanupIdempotencyRecords();           // expire old keys
await actc.shutdown();                            // graceful stop
```

## License

Apache-2.0
