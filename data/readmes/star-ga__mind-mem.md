<h1 align="center">
  <img src="https://raw.githubusercontent.com/star-ga/mind-mem/main/assets/logo.png" alt="MIND-Mem logo" width="140"><br>
  MIND-Mem
</h1>
<p align="center">
  <strong>Replayable memory for AI agents. Governed recall with canonical, hash-anchored audit evidence.</strong>
</p>
<p align="center">
  Built on the MIND substrate &bull; Governed-write &bull; Deterministic recall &bull; 107 MCP tools<br>
  <sub>MIND Language Profile: <code>default</code> (full tensor stdlib + Q16.16 + heap) &mdash; see <a href="https://github.com/star-ga/mind/blob/main/docs/roadmap.md#phase-106--library-output--c-abi-mindc-026--030">Phase 10.6</a></sub><!-- mind-profile: default -->
</p>
<p align="center">
  <a href="https://pypi.org/project/mind-mem/"><img src="https://img.shields.io/pypi/v/mind-mem?style=flat-square&color=blue&label=PyPI" alt="PyPI"></a>
  <a href="https://pypi.org/project/mind-mem/"><img src="https://img.shields.io/pypi/pyversions/mind-mem?style=flat-square" alt="Python Versions"></a>
  <a href="https://github.com/star-ga/mind-mem/blob/main/LICENSE"><img src="https://img.shields.io/pypi/l/mind-mem?style=flat-square" alt="License"></a>
  <a href="https://github.com/star-ga/mind-mem/releases"><img src="https://img.shields.io/github/v/release/star-ga/mind-mem?style=flat-square&color=green&label=Release" alt="Release"></a>
  <img src="https://img.shields.io/badge/MIND-substrate-orange?style=flat-square" alt="MIND Substrate">
  <img src="https://img.shields.io/badge/deterministic-byte--identical-brightgreen?style=flat-square" alt="Byte-identical Determinism">
  <img src="https://img.shields.io/badge/governed--write-propose→apply-purple?style=flat-square" alt="Governed Write">
  <img src="https://img.shields.io/badge/MCP-compatible-blueviolet?style=flat-square" alt="MCP Compatible">
  <img src="https://img.shields.io/badge/core_deps-zero-brightgreen?style=flat-square" alt="Zero Core Dependencies">
  <a href="https://github.com/star-ga/mind-mem/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/star-ga/mind-mem/ci.yml?branch=main&style=flat-square&label=CI" alt="CI"></a>
  <a href="https://github.com/star-ga/mind-mem/actions/workflows/release.yml"><img src="https://img.shields.io/github/actions/workflow/status/star-ga/mind-mem/release.yml?style=flat-square&label=Release" alt="Release"></a>
  <img src="https://img.shields.io/badge/test_functions-12%2C605-brightgreen?style=flat-square" alt="Test functions: 12,605">
  <img src="https://img.shields.io/badge/MCP_tools-107-blue?style=flat-square" alt="MCP Tools: 107">
  <img src="https://img.shields.io/badge/clients-20-blueviolet?style=flat-square" alt="AI Clients: 20">
  <img src="https://img.shields.io/badge/backends-markdown_%7C_postgres_%7C_encrypted-teal?style=flat-square" alt="Storage: Markdown + Postgres + Encrypted">
  <img src="https://img.shields.io/badge/audit-cross--model_%2B_SAST_%2B_SoW-darkgreen?style=flat-square" alt="Cross-model consensus audit + SAST (CodeQL/bandit/trivy) + external-audit SoW published">
</p>

<p align="center"><sub>
  <strong>Current release:</strong> <code>v5.0.4</code> (candidate; publication pending) &mdash; corrects lifecycle ranking, graph admission and release gates, and adds source-only training preparation &mdash;
  <a href="CHANGELOG.md">see CHANGELOG</a>
  (single source of truth; per-version detail tables below may lag the changelog)
</sub></p>

---

MIND-Mem is a deterministic AI memory system: recall is defined by the **query, admitted corpus, configuration, scoring instant, and execution providers**. With those inputs held constant, its canonical audit/evidence encoding is byte-identical across replay; ranking scores themselves remain standard floating-point. The Q16.16 fixed-point audit chain is embedded in every applied decision.

`scoring_instant` is a UTC date and is the honest part of that claim: recency ranking is load-bearing for a coding agent, so it is not deleted, it is *named

[...截断...]

*. Omit it and it resolves to today in UTC — the one clock read on the whole path, taken once at the boundary, never inside the scoring loop. Its resolved value is bound into the recall attestation, so any attested run replays exactly by passing that date back.

Built on the MIND substrate. Governed-write (`propose → review → approve_apply`). 107 MCP tools as the surface — but the differentiator is the substrate underneath. On the same workspace, recall uses the query, admitted corpus, configuration, `scoring_instant`, and execution providers. With those inputs held constant, the canonical audit/evidence encoding is byte-identical across replay; ranking scores remain standard floating-point, so this does not promise universal cross-provider result identity.

Most memory layers ship tools. That is table-stakes. MIND-Mem ships a substrate: Q16.16 fixed-point encoding in the audit-hash preimage, a governance pipeline that rejects every unreviewed write, and an audit chain where every applied proposal is hash-anchored. The scoring path itself is pure Python (`mind_kernels.py`): the wheel ships MIND-language kernel *sources* under `mind/` and no compiled kernel, and the optional native `libmindmem.so` is built from `lib/kernels.c` (C99). The substrate claim is the encoding, the gate and the chain — not the kernels, which are not compiled yet. The same query on the same workspace with the same admitted corpus, configuration, scoring instant and execution providers produces repeatable ranked recall; that recall's canonical audit/replay encoding is byte-identical under those held-constant conditions. That property is what makes MIND-Mem suitable as a canonical memory layer across heterogeneous agent stacks.

> **If your agent runs for weeks, it will drift. MIND-Mem prevents silent drift.**
>
> MIND-Mem powers the Memory Plane of the [MIND Cognitive Kernel](https://mindlang.dev/docs/cognitive-kernel) — the deterministic AI runtime architecture.

### 30-Second Demo

```bash
pip install mind-mem
mind-mem-init ~/my-workspace        # Create workspace
mind-mem-recall -q "API decisions" --workspace ~/my-workspace  # Hybrid BM25F search
mind-mem-scan ~/my-workspace        # Detect drift & contradictions
```

Output:
```
[1.204] D-20260215-001 (decision) — Use async/await for all API endpoints
        decisions/DECISIONS.md:11
[1.094] D-20260210-003 (decision) — REST over GraphQL for public API
        decisions/DECISIONS.md:20
```

<sub>Current release: **v5.0.4** (candidate; publication pending) — corrects lifecycle ranking and graph admission, strengthens release validation, and adds source-only training preparation. See [CHANGELOG.md](CHANGELOG.md) for candidate changes and published release history.</sub>

### Substrate Properties

| Property                | What it means                                                                     |
| ----------------------- | --------------------------------------------------------------------------------- |
| **Byte-identical replay** | Replay fixes the query, admitted corpus, configuration, `scoring_instant`, execution providers and dependencies. Canonical Q16.16 audit encoding produces identical bytes and hashes for identical preimages. Ranking uses floating-point scores; provider behavior, access-state updates and receipt metadata can change the inputs and results. |
| **Governed-write**      | Nothing reaches the source of truth without `propose → review → approve_apply`. No silent mutations. Ever. |
| **Auditable**           | Every apply logged with timestamp, receipt, and DIFF. Full traceability from signal to decision. |
| **Deterministic**       | No ML in the retrieval core. Q16.16 fixed-point encoding in the audit-hash preimage. The same preimage produces the same hash. |
| **Local-first**         | The default retrieval path stores data locally. External storage and model providers are optional and must be configured. |
| **No vendor lock-in**   | Plain Markdown files. Move to any 