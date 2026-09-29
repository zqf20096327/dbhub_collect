# rupi-c: Lightspeed SQLite

Adapting CompCert's verified semantics to compile SQLite — a
Rupicola-style verified pipeline in Rocq where **proof search IS the
compilation**.

## North star

One derivation

```rocq
Deriving asm Such That (c_to_asm_refinement source asm)
```

in which *every* intermediate function and program is an evar, assembled
construct-by-construct by applying `Qed`'d combinator lemmas over the
source's Csyntax AST. No pass is ever run; nothing is normalised with
`vm_compute`; the assembly emerges from the proof. The combinator
libraries are function-agnostic, so the next SQLite function is compiled
by pointing the driver at its Csyntax and letting the combinator walk
run. Target: all 2627 compiled SQLite functions.

The witness `R` is an `Asm.program` produced by CompCert semantics:

```rocq
Compiler.transf_c_program source = OK R
```

Full plan: [`plan-perconstruct.md`](plan-perconstruct.md).

## The core pattern

For each pass `P : src-IR -> tgt-IR`, a per-construct ("gap combinator")
library is:

1. A **spec relation** `tr_P` whose constructors are the compilation
   rules, one per source construct (CompCert ships some: `SimplExprspec`,
   `RTLgenspec`, `Selectionproof`; the rest are built here).
2. A **refinement lemma** `tr_P_fundef -> match_prog`, so that building
   `tr_P` IS proving the gap. Equation-based passes get a `Certified<P>`
   module with a spec-based `match_prog` (see `theories/SQLite/
   CertifiedSimplExpr.v`, `CertifiedAllocproof.v`, `CertifiedLinearize.v`).
3. A **combinator layer**: `apply`-able lemmas that pick the constructor,
   emit the fragment into the evar, and leave continuation goals — the
   compiler's degrees of freedom (registers, CFG nodes, temp names,
   linearisation order) become evars the prover instantiates.

## Current state

- **Frontier — Phase 1 (SimplExpr, per-construct)**:
  [`theories/SQLite/MutexEndG1PC.v`](theories/SQLite/MutexEndG1PC.v)
  derives `sqlite3MutexEnd`'s Clight function as an *evar* by applying
  the `SimplExprspec` constructors directly over its Csyntax
  (`dvar_val`, `dcall_val`, `dassign_eff`, the `dfnptr` tactic). No
  `transl_*` pass runs, nothing normalises; the single fresh temporary
  (`me_t`) is chosen by the prover. This file is the template the rest
  of the codebase is being refactored toward.
- **Baseline — whole-function chain (to be replaced)**: gaps 1–10
  derived by proof search over whole functions with per-def reduction
  (`MutexEndG*.v`, plus complete chains for a no-op and
  `sqlite3_libversion_number`: `NoopDeriv*.v`, `LibVersionDeriv*.v`,
  composed in `DerivationGaps.v` and `DeriveMutexEndAsm.v`). Kept as the
  regression baseline until the per-construct chain fully replaces it.
- **Backend certificates**: allocation (`CertifiedAllocSolution.v`,
  `CertifiedAllocproof.v`), linearize (`CertifiedLinearize.v`), and the
  relational pipeline (`CertifiedPipeline.v`) close backend gaps without
  trusting opaque oracles.
- Two functions verified end-to-end `Csyntax -> Asm`, dumped to real
  arm64 and linked into a working SQLite build
  (`scripts/dump_noop_asm.sh`, `scripts/dump_libversion_asm.sh`,
  `scripts/link_verified_asm.sh`).

## Roadmap (from `plan-perconstruct.md`)

| Phase | Gap | Content |
|-------|-----|---------|
| 0 | — | Generic program/function combinator drivers, evar-choice helpers |
| 1 | Csyntax → Clight | SimplExpr per-construct — **done** (`MutexEndG1PC.v`) |
| 2 | CminorSel → RTL | `CertifiedRTLgen`: real instruction emission as proof search |
| 3 | frontend | SimplLocals, Cshmgen, Cminorgen, Selection per-construct |
| 4 | Mach → Asm | Stacking/Asmgen per-instruction combinators |
| 5 | RTL → LTL | Register allocation as the prover's choice (hardest; certificate fallback kept) |
| 6 | LTL → Linear | Linearisation order as a proof choice |
| 7 | — | Single `Deriving asm Such That (c_to_asm_refinement source asm)`; delete all baked `tf_N`/`p_N` |

## Hard rule

No unverified assembly lanes. `Abort` means pending: it must not feed
benchmarks, linking, or baselines. Assembly is an artifact only when the
corresponding Rocq proof closes with `Qed`. All SQLite contexts reduce
to concrete `Csyntax.program` sources (`theories/SQLite/generated/`).

## Layout

```
theories/SQLite/   proof chain: per-construct (G1PC), baseline (G*), certificates
theories/Lightspeed/  the Deriving plugin (witness dump on Qed)
proofgen/          SQLite function inventory + proof-stub generation
agents/            restartable proof loop, obligation slices
scripts/           Csyntax export, proof compilation, asm dump + link
bench/             clang/gcc/CompCert lanes, speedtest1 + testrunner harness
patches/           local CompCert fixes (aarch64 stack alignment)
examples/          plugin smoke tests
plan*.md           plan-perconstruct.md (direction), plan.md (history/frontier log)
```

Submodules: [CompCert](https://github.com/AbsInt/CompCert),
[sqlite](https://github.com/sqlite/sqlite),
[rupicola](https://github.com/mit-plv/rupicola).

## Verified-build result

SQLite compiled entirely with the locally built CompCert
(`sqlite/build-compcert4`) passes the full Tcl suite:

```text
0 errors out of 1034771 tests
```

Speedtest1 O3 baselines (2026-08-04, macOS arm64):

```text
clang: main 0.101s, mix1 0.206s, json 0.037s, cte 0.020s, orm 0.091s, fp 0.055s, rtree 0.157s
gcc:   main 0.107s, mix1 0.213s, json 0.038s, cte 0.019s, orm 0.100s, fp 0.054s, rtree 0.145s
```

## Build notes

- CompCert needed an AArch64 `Asmexpand.ml` fix (large stack frames left
  `sp` misaligned before `stp` → SIGBUS); see `patches/`.
- Apple SDK `math.h` needs a shim for CompCert; SQLite rebuilt with
  `SQLITE_ENABLE_MATH_FUNCTIONS`.
- The Tcl harness needs Tcl ≥ 8.6 (Homebrew `tcl-tk`).
- Restart checks:

```sh
scripts/export_sqlite_csyntax.sh
python3 proofgen/sqlite_proofgen.py --check
scripts/compile_sqlite_proofs.sh
```
