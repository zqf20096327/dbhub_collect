# Beankeeper

The accounting runtime for AI agents. Your assistant manages your books -- `bk` makes sure it can't mess them up.

A CLI backed by SQLCipher-encrypted SQLite, with an embeddable Rust library underneath.

## Why Beankeeper?

AI assistants can already categorise expenses, reconcile bank feeds, and generate financial reports. The missing piece is a backend that makes those operations *safe* -- one where the agent physically cannot produce an unbalanced ledger, silently duplicate a transaction, or corrupt the audit trail.

hledger, ledger-cli, and beancount are built around plain-text files a human edits by hand. That's the right design for manual bookkeeping. `bk` is built for when an agent is doing it.

### The backing store is a database, not a file

SQLite (optionally encrypted with SQLCipher) is the source of truth, not a `.journal` file. That means the agent can post transactions, query balances, and generate reports through a stable CLI contract without worrying about file locking, merge conflicts, or parse errors.

### The agent cannot create an unbalanced transaction

The CLI’s private transaction writer requires a validated `Transaction` and proof
that its company’s posting date falls in an open period. `JournalEntry` checks
entry currency as entries are added, and `JournalEntry::post()` requires at least
two entries with equal debit and credit totals. Account lookup, journal
validation, and the period check run in the savepoint that writes the posting.
Balance and closed-period failures return `VALIDATION` (exit code 3).

### Retries are safe

Agents retry. Import scripts fail mid-batch. `--reference` takes a non-empty string (a bank reference number, a statement row hash, whatever), trims surrounding whitespace, and stores it verbatim as a key unique per company. Subsequent posts with the same reference in that company are rejected with the existing transaction ID, or skipped with `--on-conflict skip`. Retrying a referenced post does not create duplicates.

### The agent gets structured feedback, not text to parse

JSON command responses use the same envelope, except for successful `export` output, which uses the file format described below:

```json
{ "ok": true,  "meta": { "command": "txn.post", "company": "acme", "timestamp": "..." }, "data": { ... } }
{ "ok": false, "meta": { "command": "txn.post", "company": "acme", "timestamp": "..." }, "error": { "code": "NOT_FOUND", "message": "..." } }
```

Monetary JSON fields retain integer minor units and add decimal-string companions,
for example `"amount": 180000, "amount_display": "1800.00"` for USD.
`txn list` and `audit log` keep their data arrays and expose
`meta.pagination` with filtered totals and `has_more`; table mode warns on stderr
when more rows exist. Audit pages default to 50 rows and accept up to 100. For
the next page, pass `meta.pagination.next_offset` to `--offset` with the same
filters. MCP tools expose the same amounts and put pagination in the tool
result’s `_meta.pagination`.

Named error codes (`NOT_FOUND`, `VALIDATION`, `DATABASE`, etc.), `meta.command` in dot notation, consistent field presence. The agent can handle `bk` output reliably without parsing human-readable text or guessing at shapes.

A successful `bk export --output-format json` writes a standalone `{"beankeeper_export": {"version": 1, "companies": [...]}}` object, without `ok`, `meta`, or `data`, even with `--json`. Read its companies with `jq '.beankeeper_export.companies'`.

### The audit trail is tamper-evident

Database triggers reject changes to posted financial fields, entry details, and audit records, including deletion and replacement. Transaction metadata and entry clearance status remain mutable for correlation, reversals, and reconciliation. Supported mutations append an actor, timestamp, and before/after snapshots in the same atomic operation.

Every new posting, including imports and reversals, stores `posted_by` and a `create` audit record containing its imm

[...截断...]

utable transaction and entry details. Set the actor label with `--actor NAME` or `BK_ACTOR` on the CLI or MCP server. Both use the verified agent URI as the actor when a token is present and no label is configured. `bk txn show` displays the poster; JSON transaction output includes `posted_by`. Legacy transactions have an unknown poster (`null` in JSON).

`bk verify` checks every company in one ledger snapshot. It reports currency-by-currency
debit and credit totals, row counts, named checks, and the SHA-256 audit-chain head
after recomputing every row hash. Use `bk --json verify` or the MCP `verify` tool for
the same structured evidence. Failures identify the first failed check and the
affected record where available (`DATABASE`, exit code 4).
See [verification and its limits](docs/audit-integrity.md#verification-and-limits).

These protections detect tampering against the stored chain; they are not signatures or an external trust anchor. Someone with unrestricted database access can remove triggers and rewrite the ledger, hashes, and sequence together, or restore an older complete database. See [audit integrity](docs/audit-integrity.md) for the format, migration behavior, and limits.

### Verified agent identity and capability enforcement

`bk key init` creates a local trust root inside an encrypted ledger.
`bk agent issue --name claude --public-key "$AGENT_PUBLIC_KEY" --ttl 8h` issues
an attestation. Supply it with `--agent-token` or `BK_AGENT_TOKEN` to record its
verified `agent_uri` and `token_jti` on new postings and audit rows. `txn show`,
`audit log --agent URI`, and JSON `meta.agent` expose attribution; `agent list`
and `agent revoke URI_OR_JTI` manage issued tokens. Stdio MCP uses one process
token; HTTP accepts a bearer token per request and always requires verification.
Both recheck every call. Invalid, expired or revoked supplied tokens return
`UNAUTHORIZED` (exit 6 for CLI, HTTP 401 at the HTTP boundary).

With enforcement off, writes without a token can record an unverified client
hint from known runtime environment markers. The hint records only allowlisted
marker names and leaves the actor label independent. See it in `bk audit log`
and MCP `audit_log`. Use `--quiet` to suppress the stderr notice on CLI
commands or when launching a stdio MCP server.

Enforcement defaults to off. CLI 0.24.0 adds `bk policy show` and
`bk policy set --enforce on|off`. Bootstrap by issuing a token with
`ledger/read,ledger/admin`, saving it, then enabling as a named actor. Once on,
all reads and mutations require tokens. Missing credentials return `UNAUTHORIZED`
(exit 6); insufficient grants return `FORBIDDEN` (exit 7). Policy changes require
`ledger/admin` and append `policy_change` audit records.

| Grant | Operations |
| --- | --- |
| `ledger/read` | Lists, shows, reports, export, verify, audit, agent list, policy show, loan schedule |
| `ledger/post` | Posting/import/attachments/annotations, investment trades, security writes, loan pay, schedule writes, rule writes |
| `ledger/propose` | Propose, list and withdraw owned pending requests |
| `ledger/approve` | List all proposals, approve or reject |
| `ledger/reverse` | Reverse postings and undo eligible audit receipts |
| `ledger/reconcile` | txn clear/reconcile |
| `ledger/budget` | budget set/delete |
| `ledger/admin` | Company/account writes, key init, agent issue/revoke, agent limit set/clear, policy set, backup/restore |

Grants are siblings: admin does not imply posting, and post does not imply
reverse. Issue the union needed; bare `ledger` grants are rejected. Stdio MCP
filters tools by startup grants; HTTP filters discovery per request. Both recheck
every call, and `--read-only` remains a ceiling.
Tokens are bearer credentials without proof of private-key possession or signed
writes. Back up before schema v18 upgrades: existing hashes remain intact, but
older binaries cannot append the new v3 audit format. `init --force` requires an
admin to disable enforcement first. S