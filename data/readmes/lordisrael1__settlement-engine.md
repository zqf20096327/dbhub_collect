# Reconciliation Engine

[![CI](https://github.com/lordisrael1/settlement-engine/actions/workflows/ci.yml/badge.svg)](https://github.com/lordisrael1/settlement-engine/actions/workflows/ci.yml)

A payment reconciliation engine for Nigerian fintech, built on
[`pay-normalize`](https://www.npmjs.com/org/pay-normalize).

It records a payment the moment the provider's webhook arrives, waits for the settled cash,
and partitions every difference between them into **matched**, **explained** or
**exception**, so that a person only reviews a genuine anomaly.

## How it works

Three independent records describe the same money, and only one of them is cash:

    T+0  Webhook                     a customer paid; the provider owes us
           psp_receivable  +10,000
           merchant_revenue -10,000

    T+1  Settlement report           the provider says a payout is coming, less deductions
           Payout PO-1: gross 10,000 - fee 150 - VAT 11.25 = 9,838.75
           Payments are matched to the payout. Nothing is booked.

    T+2  Bank statement              our own bank, about our own account
           A credit of 9,838.75 confirms PO-1, and only now:
           bank_account   +9,838.75      fees_expense   +150.00
           taxes_withheld    +11.25      psp_receivable -10,000.00

A settlement report is the provider describing its own future behaviour. Booking cash on it
would hide four ordinary events: a payout reported and never sent, one the bank returns, one
credited short of a correspondent-bank charge, and one credited twice.

See [docs/DOMAIN-MODEL.md](docs/DOMAIN-MODEL.md) for the full model.

## Quick start

Requires a container runtime.

    docker compose up --build

That starts Postgres and the service, applies migrations under an advisory lock, binds port
8080 and begins draining the webhook inbox.

    curl localhost:8080/health
    # {"status":"ok","database":"reachable",
    #  "inbox":{"pending":0,"failed":0,"deferred":0,"oldestPendingAt":null},
    #  "alerts":[]}

`/health` reaches a verdict rather than only reporting numbers: it answers **503** once a
threshold is breached, with a sentence per breach in `alerts`. That is the last mile — a
queue that grows all weekend, a worker that died, a delivery nobody will retry, and a
reconciliation that has not run since Tuesday are all things an existing uptime monitor can
now find out about without anybody remembering to look
([ADR-0074](docs/adr/0074-the-last-mile-is-a-schedule-and-a-verdict.md)). Use it as a
readiness or alerting target, not as a liveness probe: a degraded service is up, and
restarting it fixes nothing.

    curl -H 'x-api-key: local-dev-key-0123456789' localhost:8080/balances
    curl -X POST -H 'x-api-key: local-dev-key-0123456789' localhost:8080/reconcile/runs
    curl -H 'x-api-key: local-dev-key-0123456789' localhost:8080/exceptions

Webhooks are verified, stored and acknowledged in milliseconds; a worker interprets them
moments later, and the delivery id resolves to the ledger transaction it became:

    curl -X POST localhost:8080/webhooks/paystack \
         -H 'x-paystack-signature: <hmac-sha512 of the raw body>' \
         --data-binary @charge.json
    # {"accepted":true,"deliveryId":"3ceec2a5...","duplicate":false}

    curl -H 'x-api-key: ...' localhost:8080/deliveries/3ceec2a5...
    # {"state":"processed","transactionId":"payment:paystack:charge:PSK_9f3a2c", ...}

The two evidence rails take the file itself, because the bytes are the evidence and their
hash is its identity:

    curl -X POST -H 'x-api-key: ...' --data-binary @settlements.json \
         localhost:8080/ingest/settlement/flutterwave   # a claim; books nothing
    curl -X POST -H 'x-api-key: ...' --data-binary @statement.json \
         localhost:8080/ingest/bank                     # the proof
    curl -X POST -H 'x-api-key: ...' localhost:8080/reconcile/runs

## HTTP API

| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | Database reachability, inbox depth, and a verdict. 503 when a threshold is breached. No authentication. |
| `GET` | `/metrics` | Prometheus exposition: counters, histograms, and per-tenant gauges read from the books. Needs `books.read` — unlike `/health`, this one says how much money is unmatched |
| `POST` | `/webhooks/:source` | 200 accepted · 401 bad signature · 404 unknown source · 503 no secret configured |
| `POST` | `/tenants/:tenant/webhooks/:source` | The same, for a deployment holding several sets of books. The tenant selects which secret must verify the signature; it is not itself a credential |
| `GET` | `/deliveries/:deliveryId` | What became of an accepted webhook, down to the ledger transaction id |
| `GET` | `/balances` | Every account, its meaning, and its balance in kobo |
| `POST` | `/ingest/settlement/:source` | A settlement export, as raw bytes · 501 for a source with no adapter |
| `POST` | `/ingest/bank` | A bank statement, as raw bytes. Recorded at `operator_uploaded`: proves who uploaded it, nothing about where it came from |
| `POST` | `/ingest/bank/feeds/:feedId` | The same bytes over a channel that proves its origin. `X-Feed-Signature` must verify · 401 stores **nothing** |
| `POST` | `/ingest/expectations/:source` | What the merchant's own system says it took. A completeness control and **not** a fourth record: it books nothing, matches nothing and resolves nothing ([ADR-0096](docs/adr/0096-the-merchants-own-system-may-count-but-never-match.md)) |
| `GET` | `/completeness?days` | Payments the merchant recorded that a provider never reported. Empty without a feed, which is the ordinary state |
| `GET` | `/inbox/pressure` | Delivery lag per provider, and whether each is being shed. The number `/health` cannot carry: *whose* queue |
| `POST` | `/reconcile/runs` | Runs allocation and bank confirmation; returns what was concluded and booked, and what the run cost against its budget |
| `GET` | `/reconciliation/summary?from&to` | Matched, explained and exception counts, plus money reported and not yet banked |
| `GET` | `/exceptions`, `/exceptions/:key` | The queue, worst first, with the candidates the matcher rejected |
| `GET` | `/reserves` | Money a PSP withheld and has not returned, oldest first, overdue ones flagged |
| `GET` | `/bank/position` | Our books against the bank's own running balance. Does **not** prove the statement came from the bank |
| `POST` | `/bank/attestations` | Record that a named person compared the books to the bank's portal. Append-only |
| `POST` | `/exceptions/:key/resolve` | Records a maker-checked resolution; an unapproved write-off is a 422 |
| `GET` | `/ingest/anomalies` | Foreign formats that have moved, worst first ([ADR-0067](docs/adr/0067-format-drift-is-a-record-not-a-counter.md)) |
| `POST` | `/ingest/anomalies/:key/acknowledge` | Take ownership of a drift; it stays owned when the next file shows it again |
| `GET` | `/evidence/:id` | Document metadata and its access log. No grant needed — no personal data in any of it |
| `GET` | `/evidence/:id/raw?reason` | The bytes. Needs the `evidence.raw` grant · 400 without a reason · 410 once purged on schedule |
| `POST` | `/evidence/:id/exports` | A sealed copy. Needs `evidence.export`; an original needs a second approver |
| `GET` | `/evidence/exports/:exportId` | Collect it, once. No API key — the token in `X-Recon-Export-Token` is the credential, and the path carries only a hash ([ADR-0088](docs/adr/0088-a-download-token-is-a-credential-not-a-link.md)) |
| `POST` | `/evidence/exports/:id/revocation` | Stop a token working, now. Checked before expiry, so a revoked token that is then presented is recorded as revoked rather than as a timeout |

The full reference, including every error and what causes it, is at `/docs/`.

Management endpoints take either an `Authorization: Bearer` token from the configured identity
provider or an `X-API-Key` for a service principal. Both resolve to the same identity, and
nothing downstream branches on which arrived — except approval, which needs a *person*, because
a second credential is not a second pair of eyes
([ADR-0077](docs/adr/0077-identity-is-federated-and-authorization-is-per-permission.md)).

Webhook endpoints authenticate by the provider's signature over the raw bytes and by nothing
else, because a provider holds no credential of ours
([ADR-0052](docs/adr/0052-two-authentication-rails.md)).

Every management request is served on a connection already pinned to the caller's tenant, so the
isolation is enforced by Postgres rather than by a predicate each handler remembers
([ADR-0076](docs/adr/0076-tenancy-is-a-database-boundary.md)).

## API reference

    docker compose up --build
    open http://localhost:8080/docs/

A [Scalar](https://scalar.com) reference over an OpenAPI 3.1 document, served by the service
itself — `/docs/openapi.json` and `/docs/openapi.yaml` are the document, and the UI bundle is
self-hosted rather than fetched from a CDN, so it renders on a machine with no route out.

Paths, methods, parameters and request-body schemas are generated from the routes. Responses
and the error catalogue are written in [apps/api/src/openapi.ts](apps/api/src/openapi.ts) and
merged in when the document is built — deliberately *not* attached to the routes, because
Fastify's `schema.response` is a serialiser as well as a description and `fast-json-stringify`
drops any property the schema does not name. Documentation must not be able to reshape a
payload that carries money. A test asserts both halves: that every served route is documented,
and that no route compiles a response schema.

## CLI

The same libraries, driven from the command line:

    docker compose run --rm cli node apps/pipeline/dist/main.js <command>

| Command | Description |
|---|---|
| `migrate` | Apply every migration once, checksum-verified |
| `demo` | An end-to-end walkthrough with commentary, against real Postgres |
| `simulate [seed] [--reverse]` | Generate a messy day from a seed and check the books against its declared arithmetic |
| `balances` | Current balances, derived from entries |
| `verify` | Check the balance cache and total conservation |
| `replay [--rebuild]` | Fold the event log from genesis and check every projection against it |
| `ingest-settlement <source> <file>` | Store a provider's report; books nothing |
| `ingest-bank <file> [bank-id]` | Store a bank statement |
| `reconcile [--limit=N]` | Allocation, then bank confirmation. Says in yellow when it read a sample rather than the books. |
| `exceptions` | The queue, worst first |
| `reserves` | Money a PSP withheld and has not returned, oldest first |
| `attest-bank [--balance=<naira>] [--note=...]` | Print our books against the bank's own closing balance; with `--balance`, record that a person checked the portal |
| `evidence-retention [--apply]` | Move every document to the state its retention schedule says. A dry run without `--apply`. |
| `tenants` | Every set of books this database holds, and the trust floor each will book cash from |
| `create-tenant <id> <name>` | Onboard a set of books. Deliberately a command rather than an endpoint: a credential that can create tenants sits outside every tenant, which makes it the most valuable thing in the estate. |
| `check-invariants` | The business rules, as distinct from the arithmetic. **Exits non-zero** on a violation — unlike `exceptions`, because an exception queue is the system working and a violated invariant is the books being wrong. |
| `verify-chain` | Does the audit trail still say what it said? Both verifiers, and every published head. |
| `anchor-log --by=<who> [--reference=<where>]` | Publish the current chain head. Put the printed hash somewhere this database cannot reach, and record where. |
| `recovery-drill` | Every integrity check, per tenant, against a database somebody has just restored. Writes nothing. |

Every command is idempotent: running it twice moves no money. For a clean run, start from
`docker compose down -v`.

## Configuration

Configuration arrives as environment variables; see [.env.example](.env.example).

| Variable | Description |
|---|---|
| `DATABASE_URL` | Postgres connection string, for the **serving** role — one that owns nothing and is not a superuser, or the tenant boundary is not enforced ([ADR-0076](docs/adr/0076-tenancy-is-a-database-boundary.md)) |
| `RECON_MIGRATE_DATABASE_URL` | The **owner's** connection string, used once at boot under an advisory lock. Optional; without it the service migrates with its own connection. |
| `RECON_TENANT` | Whose books this process acts for when nothing more specific says. Default `default`, which is where every row written before tenancy lives. |
| `RECON_API_KEYS` | `principal:secret:grants[:tenant]`, comma-separated. `grants` mixes role names and permission names freely. An **empty grant list is refused** — it used to mean "everything", and reading a balance is no longer the same right as rewriting a fee contract. |
| `RECON_OIDC_ISSUER`, `RECON_OIDC_AUDIENCE`, `RECON_OIDC_JWKS_URI` | The identity provider. All three or none: a partly configured provider accepts tokens against rules nobody finished writing. Without them, approval is refused for want of a human identity. |
| `RECON_OIDC_ROLES_CLAIM`, `RECON_OIDC_TENANT_CLAIM` | Which claims carry roles and the tenant. Defaults `groups` and `recon:tenant`. **The tenant comes from the token, never from the request.** |
| `RECON_OIDC_ROLE_MAP` | `group=role,…`. Maps a directory's own group names onto `auditor`, `support`, `operator`, `approver`, `controller`, `admin`. |
| `RECON_OIDC_MFA_METHODS`, `RECON_OIDC_JWKS_TTL_MS` | Which `amr` values count as a second factor, and how long a key set is reused. Defaults `mfa,otp,hwk,swk,pin` and 10 minutes. |
| `RECON_STEP_UP_KOBO` | Above this, a decision needs a session the provider says presented a second factor. Answered 409, not 403: come back with a factor, nothing has been recorded. Default ₦1,000,000. |
| `RECON_FEED_SECRET_<TENANT>_<REF>` | The signing secret or public key for a registered bank feed. Kept here rather than in `bank_feeds`, so the database holds which key was in force and no key material. |
| `RECON_EVIDENCE_KEY` | The root key evidence is sealed under, as `<key-id>:<base64 of 32 bytes>`. Refuses to start without it, or without `RECON_EVIDENCE_KMS`. |
| `RECON_EVIDENCE_KEYS_RETIRED` | Keys that no longer seal new records but must still unwrap old ones. Also where the local key goes after a KMS cut-over. |
| `RECON_EVIDENCE_KMS` | `aws:<region>:<key-arn>`. Displaces `RECON_EVIDENCE_KEY` — setting both is a startup refusal, because a KMS with a local fallback is one an attacker turns off by breaking a network ([ADR-0087](docs/adr/0087-root-keys-live-somewhere-this-process-cannot-read.md)). Credentials come from the standard AWS variables. |
| `RECON_RETENTION_ORIGINAL_DAYS`, `RECON_RETENTION_REDACTED_DAYS`, `RECON_RETENTION_INBOX_DAYS` | The retention schedule, in days. Defaults 30 / 2192 / 30. |
| `RECON_EXPORT_TTL_MS` | How long an export link lives. Default 15 minutes. |
| `RECON_EXPORT_BIND_PRINCIPAL` | Whether an export may only be collected by the principal it was issued to. Default `false`: the archive key is already a second factor leaking through a different channel, and requiring a management credential makes an export collectable only by somebody who already has access to the system it left. Recorded either way ([ADR-0088](docs/adr/0088-a-download-token-is-a-credential-not-a-link.md)). |
| `RECON_WEBHOOK_SECRET_<SOURCE>` | Per-source webhook signing secret, for the default tenant. A source without one answers 503. |
| `RECON_WEBHOOK_SECRET_<TENANT>_<SOURCE>` | The same, per tenant, for `POST /tenants/{tenant}/webhooks/{source}`. A delivery's tenant is the tenant whose secret signed it — the path is not a credential. |
| `RECON_WEBHOOK_SECRET_<SOURCE>_PREVIOUS` | The outgoing secret during a rotation. Both are tried, so a backlog signed with the old one is not discarded ([ADR-0073](docs/adr/0073-retries-back-off-and-secrets-overlap.md)) |
| `RECON_MERCHANT` | Whose books these are. Fee contracts are negotiated per merchant. |
| `RECON_BANK_ACCOUNT`, `RECON_BANK` | Which of our own accounts an upload is about when the request does not say |
| `RECON_DRAIN_INTERVAL_MS`, `RECON_DRAIN_BATCH`, `RECON_DRAIN_MAX_ATTEMPTS` | Inbox worker tuning. Retries back off exponentially between attempts, so eight of them span minutes rather than seconds. |
| `RECON_RECONCILE_INTERVAL_MS` | Reconcile on a schedule. **0 (the default) means nothing in the process reconciles** — drive `POST /reconcile/runs` from a cron instead, and see the warning the service logs at boot. |
| `RECON_RECONCILE_LIMIT` | How many records one run may consider. A run that hits it says so, and stops clearing exceptions it could not see ([ADR-0075](docs/adr/0075-clearing-is-bounded-by-what-the-run-saw.md)). Default 1000. |
| `RECON_SUBSET_MAX_CANDIDATES`, `RECON_SUBSET_MAX_SIZE`, `RECON_SUBSET_MAX_STEPS` | The bounded subset search. The default of 24 candidates is a *small-batch* bound; raising it is exponential, so raise `MAX_STEPS` with it ([ADR-0070](docs/adr/0070-arithmetic-matching-is-a-small-batch-feature.md)). |
| `RECON_RATE_WEBHOOK_PER_MINUTE`, `RECON_RATE_MANAGEMENT_PER_MINUTE`, `RECON_RATE_MAX_KEYS` | Per-caller request ceiling, **per process**. 0 disables. This is the floor, not the control — see Deployment below. |
| `RECON_RATE_WEBHOOK_SHARED_PER_MINUTE`, `RECON_RATE_MANAGEMENT_SHARED_PER_MINUTE` | The same ceiling across every replica, counted in Postgres. 0 (the default) leaves it off, which is right for one replica and wrong for two — without it the figures above are multiplied by the pod count ([ADR-0089](docs/adr/0089-a-rate-limit-that-survives-a-second-replica.md)). Fails open. |
| `RECON_BACKPRESSURE_MAX_PENDING`, `RECON_BACKPRESSURE_MAX_LAG_SECONDS`, `RECON_BACKPRESSURE_RETRY_AFTER_SECONDS` | When to answer a provider 503 with a `Retry-After` instead of accepting. Both ceilings 0 by default: shedding works only inside a provider retry schedule you know ([ADR-0092](docs/adr/0092-shedding-back-to-a-provider-that-retries.md)). The lag ceiling also drives `/health`'s `source_lagging`. |
| `RECON_BUDGET_MAX_STEPS`, `RECON_BUDGET_MAX_MILLIS`, `RECON_BUDGET_MAX_SEARCHES` | What one reconciliation run may spend, for a tenant with no row in `reconciliation_budgets`. Defaults 2,000,000 / 300,000 / 500 — generous, because a budget that fires on a Tuesday is one somebody raises to infinity ([ADR-0094](docs/adr/0094-a-run-has-a-budget-and-running-out-is-a-finding.md)). |
| `RECON_ALERT_INBOX_PENDING`, `RECON_ALERT_INBOX_FAILED`, `RECON_ALERT_INBOX_AGE_MS`, `RECON_ALERT_OPEN_EXCEPTIONS`, `RECON_ALERT_RECONCILE_AGE_MS`, `RECON_ALERT_ATTESTATION_AGE_MS` | When `/health` stops saying it is fine. Each 0 disables that verdict. Four verdicts have no threshold and cannot be turned off, because each is a fact rather than a level: `invariants_violated`, `audit_chain_broken`, `statement_gap` and `negative_receivable`. |
| `RECON_TRUST_PROXY` | `true` behind a load balancer. Without it every caller shares the balancer's address, and the per-address rate limit becomes a global one. |
| `PORT`, `LOG_LEVEL` | Defaults 8080 and `info` |

### Deployment requirements

Seven things this service does not do for itself, stated as requirements rather than left to
be discovered:

**The service must not connect as a superuser.** Postgres exempts a superuser from every
row-level security policy — not "shows more rows", *ignores* them — so a service connecting that
way has no tenant boundary at all, with every policy present and correct in `pg_policies`. Run
migrations as the owner, serve as a role that owns nothing:

    psql -f docker/10-app-role.sql

The service refuses to start on a multi-tenant database in that state, and warns on a
single-tenant one.

**Backups must name the wildcard.** A logical dump taken with a single tenant set succeeds and
dumps that tenant's rows — a file of the right shape with a fraction of the content. Use
`PGOPTIONS="-c recon.tenant=*" pg_dump …`, anchor the chain head before backing up, and rehearse
the restore. See [docs/DISASTER-RECOVERY.md](docs/DISASTER-RECOVERY.md).

**Reconciliation must be driven.** Set `RECON_RECONCILE_INTERVAL_MS`, or run
`POST /reconcile/runs` from a cron. Not both, and not on more than one replica: every write a
run performs is keyed so a concurrent second run duplicates nothing, but it duplicates the
work. If neither is done, exceptions are never raised and the queue stays empty for the wrong
reason — which is why `/health` reports `reconciliation_stale`.

**Rate limiting belongs at the edge, and a second replica needs the shared limiter.** The
built-in limiter is per-process and in-memory: a restart forgets everything, and an attacker
with a thousand source addresses is a thousand callers. Put a WAF or gateway limit in front of
`/webhooks/:source`, keep `RECON_WEBHOOK_BYTES` tight, and set `RECON_TRUST_PROXY=true` so the
in-process limiter sees real client addresses.

The moment there is more than one replica, also set `RECON_RATE_WEBHOOK_SHARED_PER_MINUTE` and
`RECON_RATE_MANAGEMENT_SHARED_PER_MINUTE`. Without them the per-process figure is multiplied by
the pod count and the number in your environment quietly stops being the limit
([ADR-0089](docs/adr/0089-a-rate-limit-that-survives-a-second-replica.md)).

**Somebody has to compare the books to the bank** — unless a verified feed does it. See *The
trust boundary* below.

**A KMS is where the evidence root key belongs.** `RECON_EVIDENCE_KEY` holds it in the
environment, which is the honest option and not the destination: anything that can read the
environment can read every evidence blob, key use produces no independent audit trail, and
destroying a key is an edit rather than an API call somebody else's logs record. Set
`RECON_EVIDENCE_KMS` and move the old key to `RECON_EVIDENCE_KEYS_RETIRED`, where it can still
*read* what it sealed and never wraps anything new
([ADR-0087](docs/adr/0087-root-keys-live-somewhere-this-process-cannot-read.md)).

**Backpressure and run budgets are off until you set them.** Both are deliberate: shedding
tells a provider to come back later and only works because PSPs retry — which means it stops
working at the edge of a provider's patience — and a run budget that fires on an ordinary
Tuesday is one somebody raises to infinity. Set `RECON_BACKPRESSURE_MAX_LAG_SECONDS` once you
know your providers' retry schedules, and lower `RECON_BUDGET_*` per tenant in
`reconciliation_budgets` if one customer's data shape is consuming the scheduler
([ADR-0092](docs/adr/0092-shedding-back-to-a-provider-that-retries.md),
[ADR-0094](docs/adr/0094-a-run-has-a-budget-and-running-out-is-a-finding.md)).

## The trust boundary

Cash is booked from bank evidence, and **how much that evidence's word is worth is now a value the
database compares before it lets cash move.**

Every document carries a trust level, ordered
([ADR-0079](docs/adr/0079-evidence-carries-a-trust-level.md)):

| | |
|---|---|
| `unverified` | bytes of unknown origin. Nothing reaches this in normal operation. |
| `operator_uploaded` | a named principal presented a file over an authenticated endpoint. Proves who uploaded it. Proves **nothing** about where it came from. |
| `human_attested` | a named person compared it against the bank's own portal, and said on what basis. |
| `feed_verified` | the bytes carried a signature this deployment recomputed against a secret shared only with the bank or its aggregator. |
| `bank_signed` | the bank signed the document itself, so the proof survives leaving this system. |

Each tenant declares the weakest level it will book cash from:

    UPDATE tenants SET minimum_bank_trust = 'feed_verified' WHERE tenant_id = 'acme';

A confirmation below the floor is refused by a **constraint trigger**, so it does not matter that
a write bypasses every line of application code in the repository. A control in a service is a
control until somebody writes a second service.

The default is `operator_uploaded`, which is exactly the position described by
[ADR-0068](docs/adr/0068-the-bank-file-is-the-trust-boundary.md) and preserves existing behaviour
on upgrade. **Raising it is the remediation, and it is a configuration change rather than a
deploy.**

Trust is *appended*, never updated. A statement uploaded on Monday and checked against the portal
on Thursday really is more trustworthy on Thursday, and when it became so is what an auditor asks.

### Two ways to reach the higher rungs

**A person, out of band.** Unchanged from before, and still worth doing:

    docker compose run --rm cli node apps/pipeline/dist/main.js attest-bank --balance=1450320.55

`/health` raises `bank_unattested` when a week passes without one.

**A feed, automatically.** Register one, then deliver over it:

    POST /ingest/bank/feeds/{feedId}
    X-Feed-Signature: <hex hmac-sha256, or base64 ed25519, over the raw bytes>

The signing secret lives in the deployment's own store, keyed by the `secret_ref` recorded on the
feed row — so `bank_feeds` says *which* key was in force without holding any key material, and a
compromise of the database is not a compromise of the thing that makes bank evidence trustworthy.
A delivery whose signature does not verify **stores nothing**: recording it at
`operator_uploaded` would turn a failed provenance check into a successful upload.

A feed also carries balances the bank told us, recorded whether or not they agree with our books.
That is the first number in this system that did not come from our own arithmetic —
`/bank/position` compares the ledger to the *statement's own* running balance, which a fabricated
file supplies and agrees with perfectly.

### What is still true

`verify` proves **internal conservation**: every transaction balances, the entries sum to zero, the
cache agrees with the entries. A fabricated statement that balances passes all of it. "The books
are internally consistent" and "the books match reality" remain different claims — what has
changed is that the second one is now a level the system records and a floor it enforces, rather
than a paragraph.

Nothing here stops somebody with direct database access writing an evidence row at `bank_signed`.
That is what the hash-chained log and its published heads are for
([ADR-0078](docs/adr/0078-a-tamper-evident-audit-trail.md)).

### The bank-file contract

The conversion from a bank's own CSV into the shape `/ingest/bank` accepts lives outside this
repository, because every Nigerian bank exports something different and the per-bank knowledge
belongs where it is maintained ([ADR-0057](docs/adr/0057-bank-evidence-arrives-as-an-upload.md)).
Two clauses of that hand-off are now checked rather than assumed:

**`id` must be unique within the account, forever.** Most Nigerian bank exports have no
per-row id, so a converter synthesises one — and the obvious synthesis, a hash of date, amount
and narration, collides the day two customers pay the same ₦5,000 subscription with the same
narration. **Include the running balance or a within-file sequence**: `${date}:${seq}` is
enough. A repeated id inside one file is refused; a row conflicting with a *different* stored
row is refused and queued as `BANK_LINE_COLLISION`, severity 3. Re-uploading an unchanged file
is still a silent no-op.

**`date` must be ISO-8601** — `YYYY-MM-DD`, read as UTC midnight, or a full timestamp.
`new Date("02/01/2026")` is the 1st of February in every JavaScript engine and a Nigerian
export written DD/MM means the 2nd of January, which is a month of drift into the window that
decides whether a credit can match a payout at all.

## Development

    npm install
    npm run build
    npm test                    # 188 tests; suites needing a database skip themselves

    docker compose up -d postgres
    DATABASE_URL=postgres://recon:recon@localhost:5432/recon npm test    # 371 tests

The database suites need a real Postgres, because the invariants they assert are enforced by
Postgres. Each suite takes its own schema, so they can run concurrently.

CI runs the second command, not the first. A green build with no database would report
success while skipping every trigger-enforced invariant, the replay determinism check, the
exception lifecycle, the durable inbox and all of the HTTP routes — see
[.github/workflows/ci.yml](.github/workflows/ci.yml). Node 22 is the floor: the test script
passes glob patterns to `node --test`, which Node 20 does not expand.

    npm run bench               # measure; see docs/PERFORMANCE.md

Notable coverage: a test that feeds a synthetic PAN through the ingest boundary and asserts
nothing is written; a test that redacts every provider fixture and asserts the canonical
payment is unchanged, so the keep-list stays complete as connectors change; a property test
asserting that across roughly 1,200 random valid
transactions every cached balance equals its recomputed balance and the whole ledger sums to
zero; a test that a settlement report books nothing while an independent bank credit books
everything; an HTTP suite driving every endpoint through the real router via `app.inject()`;
and an end-to-end suite that drives a generated day in six arrival orders and asserts they
all reach identical balances and an identical queue.

Two suites are written as attacks rather than as features. `tenancy.test.ts` asserts isolation
using the queries a route written in a hurry would issue — no tenant predicate anywhere — over a
connection as a role Postgres actually applies policies to, and detects a tampered event *with
the append-only trigger switched off*, because that is precisely the attack an append-only table
cannot defend against. `security.test.ts` asks what a compromised operator can make the books
say: fabricate a statement, promote a file's trust, release a reserve twice, book a resolution
against cash, approve their own write-off with a second key.

## Project structure

    packages/canon         the shared vocabulary; types only, depends on nothing
    packages/ledger-core   the double-entry engine, and the only path to writing money
    packages/ingest        the anti-corruption boundary; no database, no I/O
    packages/reconciler    the matching engine, the exception queue, and the checks that
                           read the books rather than compare two records
    packages/inbox         durable webhook acceptance, and the two things that ration the
                           rail: a shared rate window and lag per provider
    packages/protect       refuse card data, keep only what the matcher reads, encrypt it
                           under a key in configuration or in a KMS — never both
    packages/policy        joins ingest's calendars to the database's fee contracts
    packages/simulator     a seeded generator of provider files with planted anomalies
    apps/api               the Fastify service
    apps/pipeline          the CLI over the same libraries

Dependencies point one way only, toward `canon`. There are no cycles.

## Features

- **Tenant isolation enforced by Postgres**, not by a `WHERE` clause: `tenant_id` on every
  financial fact, inside every natural key, behind `FORCE ROW LEVEL SECURITY`. A route added in
  fourteen months by somebody who has not read the decision record is scoped correctly, because
  the connection is pinned and the policies do the rest
  ([ADR-0076](docs/adr/0076-tenancy-is-a-database-boundary.md)).
- **A tamper-evident audit trail.** Each event's hash covers its content and the hash before it,
  built by a trigger so it covers writers other than this application, verified by two
  independent implementations, and anchored to somewhere the database cannot reach — because a
  history rewritten end to end verifies against itself perfectly
  ([ADR-0078](docs/adr/0078-a-tamper-evident-audit-trail.md)).
- **Evidence with a trust level, and a floor cash may not be booked below.** An uploaded file and
  a signed feed delivery are no longer the same claim, a person's attestation is an appended fact
  with a date on it, and a confirmation below the tenant's floor is refused by a constraint
  trigger ([ADR-0079](docs/adr/0079-evidence-carries-a-trust-level.md)).
- **Money that comes back, from either direction.** A bank reversing a credit and a provider
  withdrawing a claim are different facts with different counterparties to chase, recorded as
  such; a provider's message is a claim rather than a state, and `disputed` is a real answer
  ([ADR-0080](docs/adr/0080-money-can-come-back.md)).
- **Business rules checked as invariants.** A reserve released twice, a promise settled with no
  bank credit behind it, an inflow confirmed by a debit: each of them leaves the books balanced
  and the position wrong, and each is now either refused at the write or found by a sweep that
  `/health` runs ([ADR-0081](docs/adr/0081-domain-invariants-are-checked.md)).
- **A recovery drill that verifies a restore against a published head.** Row counts cannot tell a
  whole restore from one that lost a tenant; a thirty-two byte chain head can
  ([ADR-0082](docs/adr/0082-a-restore-is-verified-by-a-published-head.md)).
- **Root keys that can live somewhere this process cannot read.** A KMS-backed key ring with no
  SDK and no fallback to a local key — because a fallback is what an attacker arranges — and
  retired local keys that can still *read* what they sealed while never wrapping anything new
  ([ADR-0087](docs/adr/0087-root-keys-live-somewhere-this-process-cannot-read.md)).
- **Download tokens treated as bearer credentials.** Out of the URL and into a header, bound to
  the principal they were issued to, revocable before expiry, and with **every** presentation
  recorded — because the pattern that indicates a leak is made entirely of failures, and only
  successes were audited before
  ([ADR-0088](docs/adr/0088-a-download-token-is-a-credential-not-a-link.md)).
- **Metrics and trace context.** Prometheus exposition named for the business rather than the
  schema — `reconciliation_amount_unmatched_ngn`, `reconciliation_bank_confirmation_latency`,
  `ledger_db_lock_wait_seconds` — with per-tenant gauges read from the books at scrape time, and
  W3C trace context on every request and every log line
  ([ADR-0090](docs/adr/0090-a-verdict-is-not-observability.md),
  [ADR-0091](docs/adr/0091-the-service-level-objectives-are-financial.md)).
- **Backpressure that pushes back on a provider that already retries.** Lag per source rather
  than one number across all of them, and a 503 with `Retry-After` once a drain has stopped —
  which is not a lost payment, and is the only reason the mechanism is defensible at all
  ([ADR-0092](docs/adr/0092-shedding-back-to-a-provider-that-retries.md)).
- **Fee contracts that cannot change their mind after pricing something.** A database-computed
  fingerprint of the terms, carried into every decision they priced; immutability from the
  moment a conclusion rests on them; and a supersession chain, so "why did the rate change on 15
  March?" has an answer with a name on it
  ([ADR-0093](docs/adr/0093-a-contract-that-priced-a-decision-is-history.md)).
- **A per-tenant budget on every reconciliation run.** The per-payout search bound was never
  multiplied by anything; ten thousand same-amount payments is what a subscription business
  looks like *and* what an attacker would build, and the result is a run that stops finishing
  while the queue goes quiet ([ADR-0094](docs/adr/0094-a-run-has-a-budget-and-running-out-is-a-finding.md)).
- **Negative receivables found and named.** Clawbacks exceeding what a source still owes us is
  credit exposure with the cash already spent — and it hides behind every other source's
  positive balance in a single `psp_receivable` row, with the books perfectly balanced
  throughout ([ADR-0095](docs/adr/0095-a-receivable-that-goes-negative-is-a-liability.md)).
- **An optional completeness feed.** The merchant's own system may *count* and may never
  *match*: the one input that can answer "were we told everything?", fenced off in the schema
  from every path that books, matches or resolves
  ([ADR-0096](docs/adr/0096-the-merchants-own-system-may-count-but-never-match.md)).
- Signature-verified webhook ingest from four providers, normalised and posted as balanced
  `authorized` transactions that cannot be duplicated, unbalanced or edited.
- Settlement reports parsed into payouts with named deductions — fee, tax, reserve, penalty,
  chargeback — each bound for its own account.
- Bank statements parsed into canonical credit and debit lines.
- Two-stage matching: allocation of payments to payouts, which books nothing, and bank
  confirmation, which books cash and splits each batch deduction across the payments it was
  charged on.
- Dated fee contracts scoped by merchant, source, channel and currency; deadlines from a
  business calendar with a named time zone, cut-offs, weekends and versioned Nigerian
  holiday tables.
- Full lineage: every record traces to the SHA-256 of its source file and to the row inside
  it.
- A durable exception queue that deduplicates across runs, escalates when a window passes,
  closes itself when evidence arrives, and carries the near-misses the matcher rejected — and
  that clears **only what a run actually looked at**, never an item a person has acknowledged
  ([ADR-0075](docs/adr/0075-clearing-is-bounded-by-what-the-run-saw.md)).
- Reserves with a deadline: a withholding becomes a dated obligation the moment it books, a
  release clears it oldest-first, and one past its date is chased. Without this, a PSP that
  returns reserves on schedule and one that never returns any produce identical books
  ([ADR-0071](docs/adr/0071-reserves-carry-a-deadline.md)).
- Partial refunds and partial chargebacks: a ₦3,000 refund against a ₦10,000 charge takes back
  ₦3,000 and leaves the rest waiting for its payout
  ([ADR-0069](docs/adr/0069-partial-refunds-and-chargebacks.md)).
- Same-amount bank credits paired as a *set* where the set is unambiguous even though no
  member of it is — the ordinary Tuesday of a fixed-price business, and otherwise a queue whose
  depth tracks transaction volume
  ([ADR-0072](docs/adr/0072-same-amount-credits-are-paired-as-a-set.md)).
- Maker-checked human resolutions that post their own compensating entries and can never
  touch `bank_account`.
- A data-protection boundary: a delivery or upload carrying a card number or sensitive
  authentication data is refused before it is stored; provider payloads are reduced to the
  fields reconciliation reads in the same transaction that records what they meant; every
  stored document is encrypted per record under a key the database has never seen; and every
  read of a document names a verified principal in an append-only access log.
- An append-only event log written beside the ledger, which `replay` folds from genesis to
  prove the balances can be rebuilt from it.
- A seeded adversarial simulator that generates a messy day, declares in advance what every
  planted anomaly is, and drives it in every arrival order.
- Operational honesty: retries that back off with deterministic jitter, a webhook secret ring
  so a rotation does not discard a backlog, a fixed lock order on the balance cache, a
  per-caller rate ceiling on the unauthenticated rail, and a `/health` that answers 503 rather
  than leaving a number for nobody to read
  ([ADR-0073](docs/adr/0073-retries-back-off-and-secrets-overlap.md),
  [ADR-0074](docs/adr/0074-the-last-mile-is-a-schedule-and-a-verdict.md)).

## Known limits

Stated here rather than left to be discovered. Each one is a real boundary of what this system
claims, not a bug list.

**A deployment with no bank feed still has no proof of provenance.** The trust ladder makes that
*visible and enforceable* rather than fixing it: at the default floor, an uploaded file still books
cash, and the control over a fabricated one is still a person on a schedule. What changed is that
raising the floor is a configuration change, and that the system can now say which rung any
particular inflow was confirmed from. See *The trust boundary* above.

**NGN only.** A webhook in any other currency is `ignored` with a reason, and it is *ignored*
rather than queued — so a Nigerian merchant taking international card payments settled in USD
and converted has those payments silently absent from reconciliation rather than visibly
unmatched. The ledger has one currency, `Money` will not combine two, and multi-currency is a
change to the chart of accounts and every balance, not a configuration flag.

**Arithmetic-only matching is a small-batch feature.** The bounded subset search considers 24
candidates by default. A payout batching more than that is escalated as `BATCH_TOO_LARGE` —
honestly, saying it was never attempted — rather than reported as unmatched. This is survivable
because every PSP with an adapter here ships itemised settlement files, so the reference path
carries the volume ([ADR-0070](docs/adr/0070-arithmetic-matching-is-a-small-batch-feature.md)).

**Three credits against two same-amount payouts still escalates all three.** Set pairing needs
the two sides to be the same size; sizing it correctly when they are not needs the bank's own
running balance to disambiguate.

**One hot row per account.** Every booking for a merchant contends on the `psp_receivable`
balance row, so adding workers stops raising throughput past that point. Lock *ordering* is
fixed, so this costs latency rather than deadlocks — but it is a design property of the cache
and no index fixes it. The options are per-account sharding or dropping the cache to a
periodically-materialised view with `verifyBalances` as the source of truth; both are deferred
([ADR-0053](docs/adr/0053-scaling-decisions-built-and-deferred.md)).

**Without an identity provider, this system will not let you claim maker-checker.** One person
holding two static keys satisfies "a different approver", and no database check can see it — so
approval now requires a *human* identity at `federated` assurance or better, and a static key is
refused with a message saying why. A deployment on keys alone keeps working in every other
respect ([ADR-0077](docs/adr/0077-identity-is-federated-and-authorization-is-per-permission.md)).

**The tenant boundary is void if the service connects as a superuser.** Postgres exempts a
superuser from every row-level security policy — not "shows more rows", ignores them — and
`POSTGRES_USER` creates one. The service refuses to start on a multi-tenant database in that
state and warns on a single-tenant one; `docker/10-app-role.sql` is the three lines that fix it
([ADR-0076](docs/adr/0076-tenancy-is-a-database-boundary.md)).

**A logical backup must name the wildcard.** `pg_dump` run with a single tenant set succeeds and
dumps that tenant's rows: a file of the right shape with a fraction of the content. Use
`PGOPTIONS="-c recon.tenant=*"`. This is the most dangerous consequence of tenancy and is written
up in [docs/DISASTER-RECOVERY.md](docs/DISASTER-RECOVERY.md).

**A hash chain proves less than it looks like.** A history rewritten end to end verifies
perfectly. Only a head published *outside* this database distinguishes the two, so `anchor-log`
without a `--reference` is a promise made to yourself, and the window a rewrite can hide in is the
interval between anchors.

**One tenant's appends are serialised.** The chain's advisory lock means events for a tenant are
written one at a time. It sits beside the `psp_receivable` contention that was already there, so
it narrows nothing that was not already narrow — but it is a real ceiling.

**This system cannot see whether the customer got what they paid for.** "Charged but never
provisioned" and "provisioned but never charged" are outside it by design — the product
database is not a fourth record, and the merchant must cover that with a join on the payment
reference stored here. Worth saying plainly rather than letting a reader assume this is a
complete revenue-integrity check
([ADR-0049](docs/adr/0049-the-product-database-is-not-a-record.md)).

**Reserves withheld before ADR-0071 shipped have no hold rows** and will not be chased by this
mechanism. Backfilling is possible from `entries` and is deliberately not automatic: the
deadline would be derived from a schedule nobody agreed to at the time.

**The completeness feed needs the *provider's* reference, not the merchant's order id.** A
merchant whose orders table holds only its own id cannot use it for per-payment completeness,
and feeding order ids reports a hundred per cent missing every day for an integration that is
working perfectly. The endpoint refuses with that sentence rather than leaving it to be
discovered ([ADR-0096](docs/adr/0096-the-merchants-own-system-may-count-but-never-match.md)).

**Credit exposure is modelled with the PSP as the counterparty, not the merchant.** These books
are the merchant's own, so a clawback that exceeds what a source still owes us means *we* owe
*them* — which is found, reclassified and queued
([ADR-0095](docs/adr/0095-a-receivable-that-goes-negative-is-a-liability.md)). The platform
version of the same shape — a merchant balance we hold, going negative, with reserve, recovery
and collection as first-class states — is not modelled, and would be a larger piece of domain
design than an account and a query.

**Trace ids flow; there is no exporter.** W3C trace context is accepted, generated, logged and
returned, so a gateway that already traces can find this service's log lines. What is not here
is an OTLP exporter, because what it buys over a correlated log line is only useful once there
is a second service to correlate with ([ADR-0090](docs/adr/0090-a-verdict-is-not-observability.md)).

## Roadmap

- **Dashboard.** No UI exists; the queue and the books are reachable over HTTP and from the
  CLI only.
- **Bank feed adapters.** The signed-delivery rail exists and the trust model is enforced
  ([ADR-0079](docs/adr/0079-evidence-carries-a-trust-level.md)); what does not exist is a *poller*
  for any particular open-banking provider. Statement continuity is no longer on this list —
  gaps and balance discontinuities across files that each reconcile perfectly are found at
  ingest, in the response and on `/health`
  ([ADR-0083](docs/adr/0083-a-statement-covers-a-period.md)).
- **An exception queue that classifies and prioritises itself.** Severity ranks by reason code
  today. At a million transactions a day and two tenths of a per cent exceptions, that is two
  thousand items a morning — and the ranking that matters then is amount × age × risk ×
  confidence, with `AUTO_RESOLVABLE` separated from `FRAUD_SUSPECTED` rather than both being
  "severity 3".
- **A settlement state machine.** The lifecycle a payment goes through is currently expressed
  across `transaction_state_changes`, `expected_inflows` and the payout's own status. Making it
  one declared machine would let the database refuse an impossible transition rather than
  leaving it to a matcher that happens not to produce one.
- **Provider sandbox contract tests, nightly.** Fixture-level drift detection exists in both
  directions ([ADR-0085](docs/adr/0085-a-field-that-stops-arriving.md)); what does not is a
  scheduled run against each provider's sandbox, which is the only thing that catches a
  semantic change to a field that still parses.
- **Multi-currency.** NGN is hardcoded through the chart of accounts, `Money`, and every
  balance. A merchant settling in USD needs a currency dimension on accounts and balances, an
  FX rate as dated administered data beside the fee contracts, and a decision about which
  moment the rate is taken at. None of that is a flag.
- **Capacity work.** Partitioning, index shaping, pool sizing and load testing are
  deliberately deferred until there is traffic to measure
  ([ADR-0053](docs/adr/0053-scaling-decisions-built-and-deferred.md)).

The company's own product database is deliberately not a fourth record. "Customer A bought
service X" is a question for that database, joined on the payment reference this system
stores ([ADR-0049](docs/adr/0049-the-product-database-is-not-a-record.md)).

## Documentation

| Document | Contents |
|---|---|
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Module layout, the dependency graph, request flow, where each invariant is enforced, and how it is deployed |
| [docs/DOMAIN-MODEL.md](docs/DOMAIN-MODEL.md) | The chart of accounts, the payment lifecycle, matching stages and reason codes, and the exception lifecycle |
| [docs/PERFORMANCE.md](docs/PERFORMANCE.md) | Measured throughput for parsing, ledger writes and batch matching — including where subset-sum stops finding answers |
| [docs/DISASTER-RECOVERY.md](docs/DISASTER-RECOVERY.md) | RPO/RTO, how to take a backup that is whole, how to restore, and how to prove the restored database is the same books |
| [docs/adr/](docs/adr/README.md) | 82 decision records, each with its context, decision and consequences |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Engineering rules for changing this codebase |
