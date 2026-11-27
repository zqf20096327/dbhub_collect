<img width="2256" height="382" alt="cover-company_1" src="https://github.com/user-attachments/assets/ae9509c8-b8d8-4608-b3df-6971618f8da5" />


# Verilays

An agent's "done" is a self-report. Verilays is an open-source tool that checks your database to see if what the agent claimed actually happened.

[Demo](#demo) · [Use it on your agent](#use-it-on-your-agent) · [Running it on your servers](#running-it-on-your-servers) · [How it works](#how-it-works) · [Statuses](#statuses) · [What's next](#whats-next)

Your agent tells a customer "you're booked for Tuesday at 10:00". The tool returned success, the trace looks fine, and nothing reached the database. Or it landed at 11:00. Or it landed twice. Verilays records what each tool claimed, reads the record back from your own Postgres, and tells you which of these happened.

```
                verified  mismatch  missing  failed  ambiguous
create_booking         4         1        1       1          1

Needs attention
e54edf4d  missing      room=noop start_time=10:00  not found after 0:00:40
75a021a2  mismatch     room=wrong start_time=10:00  start_time: expected 10:00, got 11:00:00
6b909e47  duplicate    room=dup start_time=10:00  duplicate of 1a88226b, 0s later
496a4779  ambiguous    room=overwritten start_time=10:00  changed after verified: start_time 10:00 → 12:00:00
970b8ac4  failed       room=raises start_time=10:00  RuntimeError('booking API down')
```

That's real output from the demo below.

## Demo

Needs only Docker. From a clean checkout:

```
docker compose run --build --rm demo
```

It starts Postgres and runs a booking agent through eight scenarios while the worker checks every 3 seconds. After the 40-second deadline it prints `verilays report`. About a minute in all.

| scenario | what the tool does | outcome |
|---|---|---|
| happy path | writes the row | `verified` |
| silent no-op | returns `{"id": 999}`, writes nothing | `missing` at the deadline |
| wrong values | saves 11:00 instead of 10:00 | `mismatch`, with the diff |
| late write | returns the id now, writes the row 15s later | `verified` on a later check |
| duplicate | the same booking twice | the second is listed as a duplicate |
| overwritten | writes the row; someone moves it to 12:00 after it was verified | `ambiguous` |
| tool raises | raises `RuntimeError` | `failed`; the agent gets the same exception |
| store down | works, but the action store can't be reached | not recorded; a warning is logged |

## Use it on your agent

**Let your coding agent do it.** Add the skill, then ask Claude Code, Cursor or Codex to add Verilays to your agent. It finds the tools that change something, wraps them, starts the worker, and runs one action through until it comes back `verified`.

```
npx skills add yinoni/verilays
```

Or by hand:

**1. Install it**, and start the action store (Verilays' own table, in a Postgres you run):

```
pip install git+https://github.com/yinoni/verilays
docker compose up -d postgres        # in this repo; the store is on localhost:55432
```

**2. Wrap the tool.** For a tool that inserts into a Postgres table:

```python
import verilays

verilays.init("postgresql://verilays:verilays@localhost:55432/verilays")

@verilays.action.postgres(table="orders", lookup_field="id",
                          fields_to_compare=["customer", "amount"], deadline="2m")
def create_order(customer, amount):
    ...
    return {"id": new_id}
```

The tool must return a dict holding `lookup_field` (`{"id": 42}`), or take it as an argument (`cancel_order(id)`) when it doesn't return it. Each name in `fields_to_compare` must be both a tool argument and a column. The worker then finds the row `orders.id = 42` and checks that its `customer` and `amount` match what the agent passed.

When a column is named differently from the argument, map it, column first: `fields_to_compare={"customer_id": "customer", "amount_cents": "amount"}`. The same goes for the lookup: `lookup_field={"id": "order_id"}` when the tool returns `{"order_id": 42}`.

The action is recorded under the function's name, `create_order`. If your agent knows the tool by another name, pass it first: `@verilays.action.postgres("place_order", table=...)`.

If your tools write to more than one database, name each one with `db`: `db="crm"` checks the database in `VERILAYS_POSTGRES_CRM` instead of `VERILAYS_POSTGRES`.

`deadline` is how long the write may take to show up: `"10s"`, `"5m"` or `"1h"` (default `"1m"`). Until then, a row that isn't there yet stays `pending` and is checked again, so a late write still ends up `verified`. Set it longer than your slowest write (a queue, a slow API, a webhook): a deadline that's too short turns a late write into `missing`.

For a delete tool, pass `exists=False`: the action is verified once the row is gone, and a row still there at the deadline is a mismatch.

For a value the tool sets that isn't one of its arguments, pass `expected={"status": "cancelled"}`. A field in both `fields_to_compare` and `expected` is checked against `expected`.

A wrong setting, like `lookup_field=5` or `deadline="5 min"`, never breaks your tool: it still runs, isn't checked, and a warning says why (`create_order runs but is not checked: lookup_field must be str | dict, got 5`). The same happens when `fields_to_compare` names an argument the tool doesn't take, such as a typo or a renamed argument.

**3. Run the worker.** It reads the URL of the database to check from `VERILAYS_POSTGRES`:

```
export VERILAYS_DSN=postgresql://verilays:verilays@localhost:55432/verilays
VERILAYS_POSTGRES=postgresql://user:pass@localhost:5432/shop verilays worker --every 10
```

**4. Run your agent, then read the report:**

```
verilays report
```

### Using LangGraph?

A LangGraph node takes one argument, the graph's state, so use `verilays.langgraph` instead of `verilays.action`. It's the same decorator, but `fields_to_compare` names keys of the state instead of arguments:

```python
@verilays.langgraph.postgres(table="bookings", lookup_field={"id": "booking_id"},
                             fields_to_compare=["customer", "time"])
def create_booking(state):
    booking_id = db.insert(state["customer"], state["time"])
    return {"booking_id": booking_id}
```

The state can be a dict, a `TypedDict`, a dataclass or a Pydantic model. Only the checked keys are saved. For a node that writes outside Postgres, use `@verilays.langgraph(system=..., verify=fn)`, which saves the whole state as the arguments.

### Using Langfuse?

When a tool runs inside a Langfuse trace, its action is linked to that trace and tool call. Install the extra and give the worker your Langfuse keys:

```
pip install "verilays[langfuse] @ git+https://github.com/yinoni/verilays"
export LANGFUSE_PUBLIC_KEY=pk-lf-... LANGFUSE_SECRET_KEY=sk-lf-... LANGFUSE_BASE_URL=https://cloud.langfuse.com
```

Each verdict then shows up in Langfuse as a `verilays` score on the tool call, with a line saying what happened: `Missing: we didn't find the record in the system before the deadline`.

On a `mismatch`, that line includes the real values from your database (`start_time: expected 10:00, got 11:00:00`), so they're sent to Langfuse too.

### Running it on your servers

In production you run two things: a Postgres for the action store, and the worker container. Copy [`.env.example`](.env.example) to `.env` and fill it in:

```
VERILAYS_DSN=postgresql://verilays:verilays@postgres:5432/verilays
VERILAYS_POSTGRES=postgresql://readonly:password@your-db-host:5432/shop
```

Then a `docker-compose.yml` next to it:

```yaml
services:
  postgres:
    image: postgres:16
    environment:
      POSTGRES_USER: verilays
      POSTGRES_PASSWORD: verilays
      POSTGRES_DB: verilays
    volumes: [verilays-store:/var/lib/postgresql/data]
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "verilays"]
      interval: 2s

  verilays-worker:
    build: https://github.com/yinoni/verilays.git#main
    command: verilays worker --every 10
    env_file: .env
    restart: unless-stopped
    depends_on:
      postgres: {condition: service_healthy}

volumes:
  verilays-store:
```

```
docker compose up -d
docker compose exec verilays-worker verilays report
```

Your agent calls `verilays.init(...)` with the same store, at an address it can reach (expose `postgres`'s port, or use a Postgres you already run and drop the `postgres` service). Inside the container, `localhost` is the container itself: a database on the host is `host.docker.internal` (on Linux, also add `extra_hosts: ["host.docker.internal:host-gateway"]` to the worker).

With a custom `verify=` check, the worker needs your code: build your own image on top of this one with your module copied in, and add `--app myagent.tools` to the command.

## How it works

1. The decorator runs your tool unchanged, then records the tool name, a deadline and what the worker needs to check: for `action.postgres`, only the lookup field and the compared fields. A custom `verify=` check also saves the tool's arguments and result.
2. The worker picks up pending actions and looks the record up in your database. It opens that connection read-only, so Postgres refuses any write from it even if the user in the URL could write. A read-only user is still a good idea.
3. It keeps checking until the deadline. Found with the right values is `verified`, different values is `mismatch`, and still not there at the deadline is `missing`.

If Verilays can't record a call, your tool still runs and returns as normal. It never breaks your agent.

Everything runs in your infrastructure: the action store is your Postgres, and the worker is your container (`Dockerfile`, configured with env vars only). Nothing is sent to us. If you turn on Langfuse, verdicts go to your own Langfuse project.

## Statuses

| status | meaning |
|---|---|
| `pending` | not found yet; checked again until the deadline |
| `verified` | the write is there, with the right values |
| `mismatch` | the write is there, with different values (the report shows the diff) |
| `missing` | still not found at the deadline |
| `ambiguous` | verified, then changed or deleted before the deadline |
| `failed` | the tool raised; the agent got the same exception |
| `expired` | the check itself kept failing until the deadline, so we never found out |
| `check_error` | the worker is set up wrong (e.g. a missing `VERILAYS_POSTGRES`); retried when it restarts |

An action with the same `fields_to_compare` values as one inside `duplicate_window` (default `1m`) is listed as a duplicate of it.

## What it doesn't do (yet)

- **Postgres only.** For anything else, write the check yourself (below).
- **It only sees actions that go through a wrapped tool.** If the agent never calls the tool, there's nothing to check.
- **It checks that the record matches what the agent passed, not whether it was the right action.**
- **A row that already existed with the same values reads as `verified`.**
- **The tool has to return the lookup key** (`{"id": 42}`).

### Not Postgres?

Write the check yourself and pass it as `verify=`. It gets the tool's arguments, its result and the action's row, and returns a `CheckResult`:

```python
from verilays.checks import CheckResult

def order_exists(params, result, row):
    order = shop_api.get_order(result["id"])
    if order is None:
        return CheckResult.not_found()
    if order["amount"] != params["amount"]:
        return CheckResult.mismatch(diff={"amount": {"expected": params["amount"], "got": order["amount"]}})
    return CheckResult.verified()

@verilays.action(system="shop-api", verify=order_exists, deadline="2m")
def create_order(customer, amount): ...
```

The worker has to import that function, so point it at your module: `verilays worker --app myagent.tools --every 10`.

## What's next

What we plan to build is in the [issues](../../issues): checks for more systems, more ways to catch a bad action, and more ways to see the results. Give a 👍 to the ones you want, and we build the most wanted first.

Something Verilays missed, or caught? A system it should check? [Open an issue](../../issues). We read every one.

Want to build one yourself? [CONTRIBUTING.md](CONTRIBUTING.md) shows how, and issues labelled `good first issue` are a good place to start.

## License

[Apache-2.0](LICENSE)
