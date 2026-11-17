# harnesslang

A language for agent harnesses, compiled to each platform's durability
guarantees. A program says what the harness does: the model, the tools and
their effect classes, the state and the turn loop. A target says where it
runs and what that place promises when it crashes. The compiler proves the
program against the target and emits code for it, for
[nanocode](https://github.com/nanocodexyz/nanocode) and harnesses like it.

## Why compile per platform

An agent harness sends things that cannot be taken back: a shell command, a
comment, a payment. After a crash it must not send them again, and it must
admit when it cannot know whether they were sent. How to get that differs by
host. A JSONL file can lose its unsynced tail or tear its last line. SQLite
commits a transaction. A Postgres session can have a second owner once its
lease expires. A Durable Object's output gate holds outgoing requests until
its writes commit. A Vercel Workflow step runs at least once and is recorded
when it returns. Written by hand, each host gets its own durability code and
its own bugs. harnesslang states the rule once, in the language (an external
effect's result has a type that includes `unknown`), and lowers it to what
each host offers: a group commit and `fsync`, a transaction, a fenced
transaction, the output gate, a step that reads its attempt number.

## Example

```hl docs/snippets/readme.hl
harness agent

const steps_max: u64 = 8
const calls_max: u64 = 4
const history_max: u64 = 256

tool read(path: text) -> text effect none
tool bash(command: text) -> text effect external
model think calls calls_max
state { history: list<entry, history_max> }

on ask(question: text) -> text
  requires len(history) + 1 + steps_max * (1 + calls_max) <= history_max
{
  push history user(question)
  loop step below steps_max {
    let reply = think(history)
    push history assistant(reply)
    match reply {
      answer(words) => { return words }
      calls(requested) => {
        for call in requested {
          match dispatch(call) {
            ok(output) => { push history result(call, output) }
            failed(error) => { push history error(call, error) }
            unknown => { push history unknown(call) }
          }
        }
      }
    }
  }
  return "no answer within steps_max"
}
```

`dispatch` has type `maybe<text>`, so leaving out the `unknown` arm is a
compile error. `requires` reserves the room one turn can use, so no `push` can
find the list full. Every loop and list is bounded by a named constant, so
the worst case is a number the compiler checks against each platform:

```console
$ hl check --target cloudflare docs/snippets/readme.hl | grep -E 'worst|ok for'
  handler ask: worst case 40 effects, 75 journal records, 40 outbound requests
  proved handler ask on cloudflare: worst_case: 75 journal records per run on the plan's longest path, as hl check counts (step below steps_max (8) x call below calls_max (4))
  proved handler ask on cloudflare: worst_case: 40 outbound requests <= 10000 outbound requests per invocation (step below steps_max (8) x call below calls_max (4))
docs/snippets/readme.hl: ok for cloudflare
$ hl sim --target server-postgres --seeds 0..100 docs/snippets/readme.hl
ok target=server-postgres mutation=none seeds=0..100 (100 seeds): turns=244 runs=655 crashes=375 power_losses=0 torn_writes=0 takeovers=55 fenced=36 dispatches=927 unknown=136
```

## What it proves

`hl check` and `hl prove` prove, for every handler on every target and every
path, crash and rerun paths included:

- **Durable before external.** An external effect runs only after its call
  record, and every record before it, is durable. Recovery never runs an
  external call a crash left open again; it reports it `unknown`.
- **Finished once.** Every path, traps included, finishes in exactly one
  status, acknowledged only after the status is durable.
- **No traps in your code.** No `u64` arithmetic overflows and no `push` finds
  its list full, given the handler's `requires`.
- **Invariants.** Each `invariant` holds in the zero state and wherever a turn
  can end.
- **Within limits.** The worst case of outbound requests fits the platform's
  limit.

Every property has a planted bug the prover must catch, and `hl sim` runs each
target's fault model (crashes, torn and lost writes, lease takeovers, retried
steps) by seed against the same invariants, each with its own planted bug.
What the proofs assume and leave out is in
[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md#proofs).

## Targets

| Target | Runs in | Journal | Emits |
| --- | --- | --- | --- |
| `native-jsonl` | a process | an append-only JSONL file, CRC-32 per line | Rust, std only |
| `native-sqlite` | a process | SQLite | Rust, std only, over a host `Sql` |
| `server-postgres` | a server pool | Postgres, fenced by owner epoch | Rust, std only, over a host `Sql` |
| `cloudflare` | a Durable Object | the object's SQLite | a JavaScript Worker and Durable Object |
| `vercel` | a Vercel Function | a Workflow run's event log | a JavaScript workflow and step |

The compiler and every program it emits use only their language's standard
library and the platform's own API.

## Status

Built: the parser, checker and prover; the replay interpreter; the simulator
with every target's faults and planted bugs; code generation for all five
targets; an oracle that folds harnesslang journals with nanocode's own
`nanocode-turnlog`; a kill -9 drill of the generated `native-jsonl` code;
`hl-host` (`hosts/native/`), the fixed native host, running nanocode's Claude harness written in harnesslang
(`examples/claude_code.hl`) and run as a coding agent against the Anthropic
API, starting subagents (`examples/claude_code_child.hl`) as child sessions;
with an OpenAI model it runs Codex's harness (`examples/codex_agent.hl`)
against the Responses API.
Not built yet: splitting a handler over
Cloudflare's request limit (`hl check` refuses it instead). The platform
limits in `src/target/` come from summaries of vendor documentation and are
marked unverified in `DECISIONS.md`.

## Code mode

Code mode lets the model answer with a JavaScript cell that calls the
harness's tools as nested calls, journaled so that a nested external call is
never dispatched twice. It is specified in [docs/CODE_MODE.md](docs/CODE_MODE.md)
and runs on every target: the simulator, the prover, the compiled WebAssembly
on every fixed host and the nanocode oracle cover it.

## Use

    cargo build --release
    target/release/hl check examples/agent.hl
    target/release/hl prove --target vercel examples/reviewer.hl
    target/release/hl sim --target cloudflare --seeds 0..1000 examples/agent.hl
    target/release/hl emit --format wat --target native-jsonl examples/agent.hl
    scripts/check.sh
    cargo build --release --manifest-path hosts/native/Cargo.toml
    hosts/native/target/release/hl-host run --instruction task.md --cwd . --model claude-haiku-4-5 --journal output/run

- [docs/LANGUAGE.md](docs/LANGUAGE.md): the language reference and a tutorial
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md): the design, journal and proofs
- [docs/CODE_MODE.md](docs/CODE_MODE.md): code mode
- `DECISIONS.md`: what each change established, with measurements

## Deploy

`hl deploy`, `status`, `monitor`, `logs`, `rollback`, `secrets` and `destroy` ship a
harness and watch it without wrangler or the Vercel CLI: they call the
Cloudflare and Vercel REST APIs with `CLOUDFLARE_API_TOKEN` and
`CLOUDFLARE_ACCOUNT_ID` or `VERCEL_TOKEN` (and `VERCEL_TEAM_ID`). `hl deploy
FILE` ships what `hl emit` writes; `hl deploy --bundle DIR` ships a prebuilt
directory, its main module named by `DIR/hl-bundle.json`. The native targets
install versioned copies under `.hl/deploy/` with the same commands. Against
the fake of both APIs in `oracle/deploy/`, which checks every request against
the providers' pinned OpenAPI specs:

```console
$ scripts/deploy-drill.sh --demo
> hl deploy --target cloudflare --name demo --out output/deploy-demo/cloudflare --bundle docs/snippets/deploy
deploy cloudflare demo: 1 file, 241 bytes, digest 40b7aa88e20c (from docs/snippets/deploy)
  migration hl-v1: new SQLite-backed class HarnessObject
  version a0000000-0000-4000-8000-000000000001 serves 100% (deployment d0000000-0000-4000-8000-000000000002)
  url https://demo.hl-fake.workers.dev
  wrote output/deploy-demo/cloudflare
> echo sk-demo | hl secrets set API_KEY ...
secrets cloudflare demo: set API_KEY (a new version serves it)
> hl status --target cloudflare --name demo --out output/deploy-demo/cloudflare
status cloudflare demo
  url https://demo.hl-fake.workers.dev
  version a0000000-0000-4000-8000-000000000003 (#2, uploaded 2026-11-14T00:00:04.000Z) serves 100% (deployment d0000000-0000-4000-8000-000000000004)
  versions: 2
  secrets: API_KEY
> hl logs --target cloudflare --name demo --out output/deploy-demo/cloudflare --follow --events 1
tail cloudflare demo: following (tail 00000000000000000000000000000005)
2026-11-14T00:00:06.000Z ok POST https://demo.hl-fake.workers.dev/sessions/s1/turn
  log turn 1 answered
> hl monitor --target cloudflare --name demo --out output/deploy-demo/cloudflare
monitor cloudflare demo
  url https://demo.hl-fake.workers.dev
  version a0000000-0000-4000-8000-000000000003 serves 100% (deployment d0000000-0000-4000-8000-000000000004)
  last 60 minutes: 1 events, 0 errors (0.0% failed)
  recent 1:
    2026-11-14T00:00:06.000Z log turn 1 answered
> hl rollback --target cloudflare --name demo --out output/deploy-demo/cloudflare
rollback cloudflare demo: version a0000000-0000-4000-8000-000000000001 (#1) serves 100% (deployment d0000000-0000-4000-8000-000000000006), was a0000000-0000-4000-8000-000000000003
  the Durable Object's storage is not rolled back: the older code reads the journal as it is now
  secrets belong to versions: the serving version has the secrets it was uploaded or last changed with
> hl destroy --target cloudflare --name demo --out output/deploy-demo/cloudflare --yes
destroy cloudflare demo: deleted the script, its versions and its Durable Objects' storage
```

`hl deploy FILE` puts a bearer token in front of every route: the first
deploy draws 32 random bytes, sets them as the `HL_AUTH_TOKEN` secret in the
same request that creates the script or project, and writes them to
`OUT/auth-token` (mode 600); requests without `Authorization: Bearer TOKEN`
get 401, and a deployment without the secret answers 503 rather than serve.
`hl secrets set HL_AUTH_TOKEN` rotates it. A `--bundle` ships as it is.
`hl monitor` shows the serving version, the error rate over `--minutes` and
the latest turns in one round trip.

`hl deploy --endpoints` lists every operation it calls, with its operation ID
in the pinned specs.

## License

[MIT](LICENSE-MIT) or [Apache-2.0](LICENSE-APACHE).
