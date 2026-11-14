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
`hl-agent` (`agent/`), nanocode's Claude harness written in harnesslang
(`examples/claude_code.hl`) and run as a coding agent against the Anthropic
API, starting subagents (`examples/claude_code_child.hl`) as child sessions.
Not built yet: splitting a handler over
Cloudflare's request limit (`hl check` refuses it instead). The platform
limits in `src/target/` come from summaries of vendor documentation and are
marked unverified in `DECISIONS.md`.

## Code mode

Code mode lets the model answer with a JavaScript cell that calls the
harness's tools as nested calls, journaled so that a nested external call is
never dispatched twice. It is specified in [docs/CODE_MODE.md](docs/CODE_MODE.md)
and runs on every target: the simulator, the prover, both generated backends
and the nanocode oracle cover it.

## Use

    cargo build --release
    target/release/hl check examples/agent.hl
    target/release/hl prove --target vercel examples/reviewer.hl
    target/release/hl sim --target cloudflare --seeds 0..1000 examples/agent.hl
    target/release/hl emit --target native-jsonl examples/agent.hl
    scripts/check.sh
    cargo build --release --manifest-path agent/Cargo.toml
    agent/target/release/hl-agent run --instruction task.md --cwd . --model claude-haiku-4-5 --journal output/run

- [docs/LANGUAGE.md](docs/LANGUAGE.md): the language reference and a tutorial
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md): the design, journal and proofs
- [docs/CODE_MODE.md](docs/CODE_MODE.md): code mode
- `DECISIONS.md`: what each change established, with measurements

## License

[MIT](LICENSE-MIT) or [Apache-2.0](LICENSE-APACHE).
