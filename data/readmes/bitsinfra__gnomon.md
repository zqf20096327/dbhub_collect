# Gnomon

**Git for Postgres data, built for agents.** Give an agent its own branch of your real database,
as nothing more than a connection string. See every field it changed, merge it into main when it's
right, and undo it if it wasn't.

Gnomon runs inside the Postgres you already have. One extension, no copies, no second database.

```sql
create extension gnomon;
select gnomon.track('orders');                    -- history starts now, no backfill

select gnomon.create_branch('agent/refunds');
select gnomon.use('agent/refunds');

-- Every query from here on runs on the branch
update orders set status = 'refunded' where id = 4182;

select * from gnomon.diff('agent/refunds');       -- every row and field it changed
select gnomon.merge('agent/refunds');             -- three-way, type-aware, conflicts as rows
select gnomon.undo_merge(1);                      -- and back
```

- **Documentation:** <https://gnomon.bitsinfra.com/>
- **Install:** `create extension gnomon` on PostgreSQL 15-18, self-hosted or managed (RDS, Aurora,
  Supabase). See [Installation](docs/installation.md).
- **New here?** The [tutorial](docs/tutorial.md) takes ten minutes.

## A branch of production, in an instant

A branch reads everything from main and keeps only what it changes, so it opens instantly and
copies nothing, however big your database is. Give one to every agent run, every pull request and
every test.

Your application doesn't change. A branch is a connection string: point a session at it, and the
queries it already runs read and write the branch instead of main.

| Where | How |
|---|---|
| A session | `select gnomon.use('feature')` |
| One transaction (behind a pooler) | `select gnomon.begin('feature')` |
| A connection string | `gnomon branch url feature` |
| With the C module | `SET gnomon.branch = 'feature'` |
| A past moment | `select gnomon.use('main', '2026-10-31 23:59')` |

Schema changes come along too. Run a migration on a branch to add a column, rename one or create a
table, and main stays as it is until the merge, which brings the new shape and its data across
together.

## Review data like code

Every branch comes with a diff: each row and field it changed, before and after. Review it in your
browser, comment on a single row and settle conflicts side by side. When an agent is done, Gnomon
opens the review and sends you the link.

Add checks written in SQL, and Gnomon runs them on the merged result before the merge is allowed to
land. An approval covers what you saw: if the branch changes afterwards, it comes back to you.

## Merges that understand your data

When main and a branch change the same value, Gnomon doesn't just pick a side. Counts add up, JSON
merges key by key and text merges line by line. Anything that truly clashes becomes a conflict, for
a person to settle or for a query to resolve.

Branches merge into each other too, not only into main, and a single transaction can be picked from
one branch onto another. Undo works the same way: take back one transaction, everything an agent
did this afternoon, or a whole merge.

## Any moment, exactly as it was

Gnomon keeps the history of every table you track. Read the whole database as it was at any moment,
with the queries you already have, and get the same answer every time. When an agent makes a
decision, you can see exactly what it saw.

```sql
-- The open invoices at the end of October
select gnomon.use('main', '2026-10-31 23:59');
select sum(amount) from invoices where status = 'open';
```

The same history streams out as it happens, to Kafka, NATS or a webhook, and into dbt as snapshots
that keep deleted rows. Older history can move to object storage, and Gnomon brings it back when a
query reaches that far.

When a check that used to pass starts failing, `gnomon bisect` finds the transaction that broke it:
who made it, when and why.

## Safe to hand to an agent

One command gives an agent a database role, a branch of its own and a connection string. That's all
it needs, whatever it's built with. It reads and writes its branch, and the database refuses the
rest, main included, even when the agent asks for it by name.

```bash
# A database role, a branch of its own and a connection string
gnomon agent create support-bot
```

- **It merges only what you allow.** Merging is for the people you choose, or for an agent within
  rules you write: at most twenty rows, only these tables, every check passing. Postgres enforces
  them, whatever the agent is told.
- **Nothing leaves before you approve.** Emails, webhooks and payments an agent queues stay on its
  branch until the merge.
- **Every change has a name on it.** Each change records the agent, the run and the reason it gave.
- **Replay what it saw.** Gnomon records the moment of every read, so a replay returns exactly the
  rows the agent read.
- **Try a few ways at once.** Start several attempts from the same moment, compare their changes
  and checks, and keep the best one.
- **Stop it, and take it back.** One command locks an agent out, closes its branches and undoes
  what it merged, newest first.
- **Ready for your agents.** The Gnomon MCP server, on the agent's machine or over HTTP, lets it
  explore the schema, try a change without keeping it, and rewind its branch to a checkpoint.

## Build it into your product

The TypeScript and Python SDKs give each task your agents take on a run: a branch of its own, with
limits already set. Merge it, send it for review, or let it go.

```ts
import { Gnomon } from "@bitsinfra/gnomon";
import { nodePostgres } from "@bitsinfra/gnomon/pg";

const gnomon = new Gnomon({
  app: nodePostgres(appPool),   // your application's own login
  runs: nodePostgres(runsPool), // one login shared by every agent run
});

// A branch for this task, discarded unless it's merged or submitted
await using run = await gnomon.startRun({
  task: "Refund order 4182",
  actor: "support-bot",
});
await run.sql("update orders set status = 'refunded' where id = 4182");

const { checks, changes } = await run.summary();
if (checks.passed && changes.rows <= 20) await run.merge();
else await run.submit({ title: "Refund order 4182" });
```

Runs can't read each other's branches, even when they share one database login. Bring the agent
framework you already use: the Anthropic SDK, the Claude Agent SDK, the Vercel AI SDK, the OpenAI
Agents SDK, LangChain or any MCP client gets the same few tools, bound to one run. They work
through your drivers and ORMs, from node-postgres and Prisma to psycopg and Django. And in your
tests, each test gets its own branch of one seeded database.

```bash
npm install @bitsinfra/gnomon      # TypeScript
pip install gnomon-postgres  # Python
```

## What is in the box

| Part | Path | What it does |
|---|---|---|
| SQL core | [src/sql](src/sql) | The extension: history, branches, merges, review, valid time, retention, archiving. Installs on managed Postgres. |
| C module | [src/c](src/c) | Optional: `SET gnomon.branch` alone routes, real row locks, `ON CONFLICT` and `TRUNCATE` on branches, stale-read detection, faster writes and point reads. |
| CLI, MCP server, review app | [cli](cli) | One Go binary: `gnomon branch/diff/merge/bisect/agent/migrate/serve/mcp/daemon/archive`. |
| SDKs | [sdk/ts](sdk/ts), [integrations/python](integrations/python) | `@bitsinfra/gnomon` and `gnomon-postgres`: a run per task, review, typed diffs, test helpers. One [specification](sdk/spec/SPEC.md) and conformance suite. |
| GitHub Action | [action](action) | A database branch per pull request, migrations on it, the changes as a comment. |
| Integrations | [integrations](integrations) | Python, Node, Ruby, Go, Java, Elixir, .NET, PHP; PostgREST and Supabase; a dbt package. |
| Examples, container | [examples](examples), [docker](docker) | The tutorial's shop database and a ready-made image. |

## Documentation

Everything is at <https://gnomon.bitsinfra.com/>, and the same pages live in [docs](docs):

- [Installation](docs/installation.md) and the [tutorial](docs/tutorial.md)
- [Concepts](docs/concepts.md): branches, coordinates, merges
- [Agents](docs/agents.md), [runs and the SDKs](docs/sdk.md), [the MCP server](docs/mcp.md)
- [Branches](docs/branches.md), [schema changes](docs/schema-changes.md), [review](docs/review.md), [merges](docs/merges.md)
- [History and time travel](docs/history.md), [the change feed](docs/feed.md)
- [SQL reference](docs/sql-reference.md), [CLI reference](docs/cli.md), [errors](docs/errors.md)
- [Operations](docs/operations.md), [security](docs/security.md), [benchmarks](docs/benchmarks.md)
- [llms.txt](llms.txt) for coding agents

## License

Gnomon is open source under the [PostgreSQL License](LICENSE). Contributions are welcome: see
[CONTRIBUTING.md](CONTRIBUTING.md). Report security issues privately, as described in
[SECURITY.md](SECURITY.md).
