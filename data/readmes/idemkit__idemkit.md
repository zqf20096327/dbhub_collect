# idemkit

[![PyPI](https://img.shields.io/pypi/v/idemkit.svg)](https://pypi.org/project/idemkit/)
[![npm](https://img.shields.io/npm/v/idemkit.svg)](https://www.npmjs.com/package/idemkit)
[![Python CI](https://github.com/idemkit/idemkit/actions/workflows/ci-python.yml/badge.svg)](https://github.com/idemkit/idemkit/actions/workflows/ci-python.yml)
[![TypeScript CI](https://github.com/idemkit/idemkit/actions/workflows/ci-typescript.yml/badge.svg)](https://github.com/idemkit/idemkit/actions/workflows/ci-typescript.yml)
[![License: Apache 2.0](https://img.shields.io/badge/license-Apache_2.0-blue.svg)](./LICENSE)
[![Dependencies](https://img.shields.io/badge/dependencies-0-brightgreen.svg)](#install)

**idemkit makes an operation safe to retry.** Send the same request twice and the second one does not run. It gets the first result back instead. Works on HTTP endpoints, queue consumers, and ordinary function calls, in Python and TypeScript.

## 💸 The problem

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/double-charge-dark.svg">
  <img src="assets/double-charge-light.svg" width="100%"
       alt="Two bank notifications seconds apart, each charging the card $100.00 for the same order under different reference numbers, and a support message asking for a refund.">
</picture>

The customer paid once. Their connection dropped before the response came back, the app retried, and the payment provider processed the second request as a separate transaction. Two reference numbers, one order.

## 🩹 The fix everyone writes first

```python
async def charge(key, body):
    if await redis.get(key):                      # seen this key? replay
        return await redis.get(f"{key}:result")
    result = await do_charge(body)                # real money leaves here
    await redis.set(key, "done")
    await redis.set(f"{key}:result", result)
    return result
```

## 🕳 Why it doesn't hold

| What goes wrong                                                              | Customer gets          |
| ---------------------------------------------------------------------------- | ---------------------- |
| Both retries reach the `get` before either reaches the `set`, so both charge | Charged twice          |
| The worker dies after charging and before `set(key)`, so the retry recharges | Charged twice          |
| The same key comes back with a different amount                              | Someone else's receipt |

A load test will find the first one if you go looking for it. The other two need a process to die at a particular moment, which is hard to arrange on purpose and happens on its own during any deploy.

The version that survives production needs four things the snippet above doesn't have:

| You need           | So that                                                                                        |
| ------------------ | ---------------------------------------------------------------------------------------------- |
| 🔒 An atomic claim | It's written and checked in one step, and two callers can never both win it                    |
| ⏱ A lease          | A worker that dies releases the key by itself, instead of blocking it forever                  |
| 🛡 A fencing token  | That worker wakes up an hour later and its write bounces, rather than clobbering a good result |
| ⏳ A way to wait   | A duplicate waits for the call in progress and gets its result, instead of an error            |

Four hundred lines or so, most of them for cases you can't reproduce on demand. Worth writing once and then never again.

## ✅ What idemkit does

```python
@idempotent(backend=RedisBackend.from_url("redis://..."),
            config=MethodConfig(key_fields=["order_id"]))
async def charge(*, order_id, amount):
    return await do_charge(order_id, amount)   # runs once per order_id
```

- **One run, even in a dead heat.** No read-then-write gap where both duplicates see "not done".
- **A dead worker can't wedge the key or double-run.** Its lease expires and its late write is rejected.
- **Duplicates wait and replay.** A retry that arrives mid-flight gets the result, not a conflict.
- **A reused key with a changed body is rejected,** not answered with the wrong stored response.
- **Failures aren't cached forever.** A decline releases the key, so an honest retry runs for real.
- **Tested against real infrastructure.** The same conformance vectors run on Redis, Postgres, Mongo, and DynamoDB, plus property-based model checking and fault injection.

<a id="install"></a>

## 🚀 Install

<details open>
<summary><b>Python</b></summary>

```bash
pip install "idemkit[asgi]" fastapi
```

```python
from fastapi import FastAPI
from idemkit import IdempotencyMiddleware, InMemoryBackend

app = FastAPI()
app.add_middleware(IdempotencyMiddleware, backend=InMemoryBackend())

@app.post("/charge")
async def charge():
    return {"charged": True}   # runs once per Idempotency-Key; retries replay it
```

Swap `InMemoryBackend` for `RedisBackend` or `PostgresBackend` and add a `scope` for production. Full guide: [python/README.md](./python/README.md).

</details>

<details open>
<summary><b>TypeScript / Node</b></summary>

```bash
npm install idemkit
```

```ts
import express from "express";
import { InMemoryBackend } from "idemkit";
import { idempotency } from "idemkit/express";

const app = express();
app.use(idempotency({ backend: new InMemoryBackend() }));
app.use(express.json());

app.post("/charge", (req, res) => {
  res.status(201).json({ charged: true }); // runs once per Idempotency-Key
});
```

Full guide: [typescript/README.md](./typescript/README.md).

</details>

Now send the same request twice and watch the second one skip your handler:

```console
$ curl -isX POST localhost:8000/charge -H 'Idempotency-Key: k1' -d '{}' | head -1
HTTP/1.1 201 Created

$ curl -isX POST localhost:8000/charge -H 'Idempotency-Key: k1' -d '{}' | grep -i replayed
idempotency-replayed: true          # same response, and charge() never ran
```

Neither package has runtime dependencies. The Redis client, the Postgres driver, the web framework: all yours, and idemkit imports only the one you ask for.

## 🎯 Three places a retry turns into a duplicate

| Your duplicate is                    | Deduped on            | You add                             |
| ------------------------------------ | --------------------- | ----------------------------------- |
| a client retrying `POST` / `PATCH`   | the `Idempotency-Key` | one line of middleware              |
| a broker redelivering a message      | the broker message id | `IdempotentConsumer`                |
| a function called again (agent, job) | the arguments         | `@idempotent` / `idempotent(fn, …)` |

- **Frameworks:** Express · FastAPI · Fastify · Flask · Django · Hono · Next.js · Bun
- **Brokers:** SQS · Kafka · RabbitMQ · BullMQ · Pub/Sub
- **Stores:** In-memory · Redis · Postgres · Mongo · DynamoDB

## 📚 Going deeper

The idea behind all this started with [Why an idempotency key isn't an idempotency guarantee](https://www.infoworld.com/article/4191741/why-an-idempotency-key-isnt-an-idempotency-guarantee.html). Handing the client a key is the easy half. The half that stops the double charge is the protocol behind it, and that protocol is usually folklore passed between teams. Here it's a written [spec](./spec/idemkit-unified-spec.md) with [conformance vectors](./spec/conformance.yaml) any implementation can be checked against.

- **Python:** [guide](./python/README.md) · [examples](./python/examples/) · [correctness](./python/docs/correctness.md)
- **TypeScript:** [guide](./typescript/README.md) · [examples](./typescript/examples/) · [correctness](./typescript/docs/correctness.md)

Both packages derive the same key and write the same record, so a Python service and a Node service can point at one Redis and dedupe against each other.

Worth being clear about the limit: this is effectively-once, not exactly-once. If your code charges a card and the process dies before idemkit can record it, no library can tell you afterwards whether the money moved. What idemkit does is narrow that window and then tell you when you land in it, so you can reconcile instead of guess.

Stable at 1.0, semantic versioning, Apache-2.0. Bug reports, spec feedback, and ports to other languages are all welcome.
