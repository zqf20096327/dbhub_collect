# chainreconciler

[![ci](https://github.com/q133ss/chainreconciler/actions/workflows/ci.yml/badge.svg)](https://github.com/q133ss/chainreconciler/actions/workflows/ci.yml)

Recover the outcome of a transaction you already sent, using only its chain id
and hash.

An RPC can time out after the node accepted the transaction, or a service can
restart before it writes the result down. Re-sending is unsafe: the first copy
may still land. `chainreconciler` keeps an observation on disk before the send,
then reads the chain until it has a final answer.

The library is read-only. Signing, sending, nonce management, and retries stay
in the calling application. It needs read access to an RPC and a writable
SQLite file.

## Install

The package is not published to npm yet. Install it from this repository;
npm runs the build through the `prepare` script:

```bash
npm install github:q133ss/chainreconciler
```

For development, clone the repository and run `npm ci` as shown in
[Development](#development).

Requires Node.js 22.12 or newer.

## How it works

1. Before sending, call `await reconciler.track({ chainId, hash })`. The
   observation is committed to SQLite first, so a crash after this point is
   recoverable.
2. Send the transaction with your own client. The library never sends it.
3. On startup and on an application timer, call `await reconciler.runDue()`.
   It checks a bounded batch of observations whose retry time has come.
4. Read the answer with `await reconciler.get(ref)`. Another process using the
   same SQLite file sees the same observation, with no second `track` call.

A network adapter decides what "final" means (confirmation count, finalized
tag, or another rule). The reconciler never guesses finality from block depth.

## Result states

| State       | Meaning                                                                  | Polled again? |
| ----------- | ------------------------------------------------------------------------ | ------------- |
| `pending`   | Not found yet, not final yet, or the RPC failed temporarily              | Yes           |
| `confirmed` | Final receipt, execution succeeded; block number and result are stored   | No            |
| `failed`    | Final receipt, execution reverted; block number and reason are stored    | No            |
| `unknown`   | The watch deadline passed without a final answer; the stop reason is kept | No            |

`unknown` does not mean the transaction failed. It can be a successful
transaction that was never confirmed during the watch window, for example
while the RPC was unavailable.

A receipt for another hash or chain is rejected; the observation stays
`pending` with a diagnostic reason and the original deadline. The same applies
to short-lived RPC errors.

## Example

The complete runnable version is in
[`examples/recovery.ts`](examples/recovery.ts). Run it with `npm run example`.

```ts
import { Reconciler, SqliteStore, type ChainReader } from 'chainreconciler';

const dbFile = './transactions.db';
const ref = { chainId: '8453', hash: '0xabc...' };

// A fake RPC adapter. Replace this with your real read client.
const mempoolReader: ChainReader = {
  async lookup() {
    return { kind: 'pending', reason: 'transaction is in the mempool' };
  },
};

const firstStore = new SqliteStore(dbFile);
const first = new Reconciler({
  store: firstStore,
  reader: mempoolReader,
  watchForMs: 10 * 60_000,
  initialRetryMs: 1_000,
});

// Process #1: persist the observation before sending.
await first.track(ref);

try {
  await sendWithYourClient(ref); // may throw "RPC timeout"
} catch (error) {
  console.error('send outcome unknown:', error);
}

await first.runDue(); // still pending
await first.close(); // process exits or crashes

// Process #2: reopen the same file. No second track() call.
const secondStore = new SqliteStore(dbFile);
const finalReader: ChainReader = {
  async lookup(lookedUp) {
    // A real adapter fetches the receipt by lookedUp.hash and applies its
    // own finality rule before returning `final`.
    return {
      kind: 'final',
      receipt: {
        chainId: lookedUp.chainId,
        hash: lookedUp.hash,
        blockNumber: 12_345_678,
        success: true,
        result: { status: 'success' },
      },
    };
  },
};

const restarted = new Reconciler({
  store: secondStore,
  reader: finalReader,
  watchForMs: 10 * 60_000,
});

console.log(await restarted.get(ref)); // status: 'pending'
await restarted.runDue();
console.log(await restarted.get(ref)); // status: 'confirmed'
```

## Writing an adapter

`ChainReader.lookup` receives the canonical `{ chainId, hash }` and an options
object with an `AbortSignal` and the RPC timeout:

```ts
const reader: ChainReader = {
  async lookup(ref, { signal }) {
    const receipt = await rpc.getTransactionReceipt(ref.hash, { signal });

    if (receipt === null) {
      return { kind: 'notFound' };
    }

    const depth = (await rpc.getBlockNumber({ signal })) - receipt.blockNumber + 1;
    if (depth < FINALITY_CONFIRMATIONS) {
      return {
        kind: 'pending',
        reason: `${depth}/${FINALITY_CONFIRMATIONS} confirmations`,
      };
    }

    return {
      kind: 'final',
      receipt: {
        chainId: ref.chainId,
        hash: ref.hash,
        blockNumber: receipt.blockNumber,
        success: receipt.status === 'success',
        reason: receipt.revertReason,
        result: receipt.logs, // must be JSON-serializable
      },
    };
  },
};
```

Adapters should return `notFound` only when the node really does not know the
transaction. An RPC exception or timeout should be thrown; the reconciler
records it as a transient error and retries with backoff.

## Configuration

```ts
const reconciler = new Reconciler({
  store,
  reader,
  clock, // optional; useful in tests
  watchForMs: 24 * 60 * 60_000,
  initialRetryMs: 15_000,
  maxRetryMs: 5 * 60_000,
  retryFactor: 2,
  rpcTimeoutMs: 10_000,
  batchSize: 100,
});
```

| Option          | Default | Description                                      |
| --------------- | ------- | ------------------------------------------------ |
| `watchForMs`    | 24 h    | How long an observation may stay unresolved      |
| `initialRetryMs`| 15 s    | Delay before the second attempt                  |
| `maxRetryMs`    | 5 min   | Upper bound for the exponential retry delay      |
| `retryFactor`   | 2       | Backoff multiplier                               |
| `rpcTimeoutMs`  | 10 s    | Per-lookup deadline; also passed to the adapter  |
| `batchSize`     | 100     | Maximum observations handled by one `runDue` call |

`SqliteStore` accepts `:memory:` for tests or a file path for durable
observations. It enables WAL mode and uses a composite primary key on
`(chain_id, hash)`, plus an index on `(status, next_attempt_at)`.

## Concurrency and idempotency

- `track` is idempotent. A repeated call returns the existing observation and
  does not move its deadline, reset attempts, or discard a final receipt.
- Workers update an observation only if the stored status is `pending` and the
  version still matches the one they read. If two workers race, the stale
  response is discarded and counted as `skipped`.
- The same hash on different chains is two independent observations.
- SQLite serializes writers across processes. Keep the database on a local
  filesystem; WAL is not intended for network shares.

Call `runDue()` once on startup and then from a timer controlled by your
application:

```ts
await reconciler.runDue();

const timer = setInterval(() => {
  reconciler.runDue().catch((error) => {
    console.error('reconciliation batch failed', error);
  });
}, 5_000);
timer.unref();
```

## Development

```bash
npm ci
npm run lint
npm run typecheck
npm test
npm run build
npm run example
```

## License

MIT
