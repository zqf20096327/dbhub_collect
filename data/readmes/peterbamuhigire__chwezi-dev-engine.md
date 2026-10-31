# Chwezi Dev Engine

Chwezi Dev Engine is the engineering catalogue of the Chwezi skill engines: 167 routed `SKILL.md` files that tell an AI coding agent, or the engineer directing one, how to design, build, review, secure and operate production software. It covers system and API architecture, relational databases, distributed systems, application and infrastructure security, Python, TypeScript/JavaScript, PHP, Java, C#/.NET, Kotlin and Swift, web, Android, iOS and cross-platform mobile clients, AI and agent systems, multi-tenant SaaS and ERP platforms, DevOps and cloud delivery, game development, GIS, and the product and commercial decisions around software. A root baseline, [`world-class-engineering`](skills/sdlc-meta/world-class-engineering/SKILL.md), applies to every change: small, explained changes, explicit failure handling, evidence scaled to risk, and a verify-before-done gate. The engine applies published standards where the work calls for them, including the OWASP Top 10 2025, OWASP ASVS 5.0.0, the OWASP Top 10 for LLM Applications and API Security Top 10, ISO/IEC 27001:2022, SOC 2 Trust Services Criteria, PCI DSS v4.0.1, the NIST AI RMF, ISO/IEC 42001:2023, the EU AI Act, GDPR and Uganda's Data Protection and Privacy Act 2019, WCAG 2.2 AA, OpenAPI 3.1, RFC 9457, SLSA v1.2, PSR-12, ISO/IEC/IEEE 29119 and the C4 model. Accounting treatment (IFRS/IAS) is owned by the separate [Chwezi Accounting Doctrine](https://github.com/peterbamuhigire/chwezi-accounting-doctrine) engine; this engine implements it in software.

The engine produces working engineering artefacts rather than advice: architecture records and C4 diagrams whose claims are pinned to a commit and checked by `verify_diagram_evidence.py`; OpenAPI contracts; database schemas and migration plans; threat models, authorisation matrices, Data Protection Impact Assessments and severity-rated security audit reports; test strategies and Release Evidence Bundles; CI/CD pipelines, Terraform, Docker and Kubernetes configurations; traceable requirements with acceptance criteria and SDLC document sets; AI feature specifications, evaluation harnesses and cost models; game design and production plans; implementation-status audits with completion blueprints; CodeTour onboarding walkthroughs; and validated Word and Excel deliverables. It serves software engineers, technical leads, architects, product owners, QA and delivery reviewers, and the consultants of Chwezi Core Systems, working through Claude Code, Codex or any agent that can read Markdown. Repository tests check the catalogue count, evidence sections and routing fixtures on every change.

## Installation

This repository was formerly named `skills-web-dev`, and an older clone may still sit in a folder of that name; every command below works from whatever the folder is called. What the October 2026 improvement passes did, and what they did not establish, is summarised under [Quality and improvement](#quality-and-improvement); read the validation records there before treating an example as production proof.

**Prerequisites.** Git. Node.js 18 or later for the standalone installer and the hook tests (CI uses Node 24; the checks in this file were last run on Node 22). Python 3.11 or later for the Codex model-policy helper. For the validators and tests, `pip install -r requirements-ci.txt` installs pytest 9.0.3 and PyYAML 6.0.2; CI runs them on Python 3.12, and the 2026-10-31 run on Linux used Python 3.14 with PyYAML 6.0.3. Commands below use `python3`; on Windows use `python` or `py -3`.

**Claude Code plugin (recommended).** The repository is its own marketplace (`.claude-plugin/marketplace.json`, marketplace `chwezi-engineering`, plugin `engineering`):

```text
/plugin marketplace add peterbamuhigire/chwezi-dev-engine
/plugin install engineering@chwezi-engineering
```

The plugin manifest (`.claude-plugin/plugin.json`) ships the 165 skills under `skills/`, plus `agents/`, `hooks/` and `rules/`. The two project-initialis

[...截断...]

ation skills in `00-meta-initialization/` are read from a clone.

**Codex portable package.** Root `plugin.json` uses the portable Agent Plugins format and the repo-scoped catalog lives at `.agents/plugins/marketplace.json`. It discovers the root `skills/` directory; the two `00-meta-initialization/` workflows remain documented clone-based entrypoints. Codex and Claude keep separate host catalogs. Adding the repo marketplace changes the user's Codex marketplace state. This repository does not automatically edit that state or submit a public listing.

**Standalone installer (no plugin system, or project-local scope).** `install.sh` and `install.ps1` delegate to `scripts/install-engine.js`, which copies skills, agents, hooks and rules into `~/.claude` (`--scope user`, the default) or `./.claude` (`--scope project`) and records every file it writes in `.chwezi/install-state.json` inside that target folder:

```sh
git clone https://github.com/peterbamuhigire/chwezi-dev-engine.git
cd chwezi-dev-engine
bash install.sh --scope project --dry-run   # print the plan, write nothing
bash install.sh --scope project
```

Run the wrapper with `bash`: the file is tracked without its executable bit, so `./install.sh` fails with "Permission denied" on a fresh Linux clone. On Windows PowerShell, run `.\install.ps1 --scope project` (the same flags pass through to the Node installer; not run in the October 2026 passes). `node scripts/install-engine.js uninstall --engine <name>`, `doctor` and `list-installed` manage an existing install; `<name>` is the folder the engine was cloned into (`chwezi-dev-engine` for the clone above), and `list-installed` prints it. Uninstall removes only files the installer recorded. On 2026-10-31 a real install into an empty home folder, `doctor`, a dry-run uninstall and a real uninstall all exited 0, and the uninstall left only the install-state record.

**Codex.** Point Codex at the clone; it reads [`AGENTS.md`](AGENTS.md) as the router. Before substantive work, run the bounded model-policy check described in [`.codex/README.md`](.codex/README.md):

```text
python3 <engine-root>/.codex/ensure_model_policy.py --runtime codex --check
```

Run `--apply` only if the check reports drift (it exits 1 and prints `DRIFT` when the Codex configuration is missing or differs). Claude Code skips this step; `--runtime claude --check` prints `NOT_APPLICABLE` and exits 0.

If an offline `debug prompt-input` check must enumerate the entire plugin skill
manifest, use the measured invocation documented in [the October 2026
validation record](docs/kaizen/2026-10-engine-kaizen/04-validation-record.md):

```sh
codex -m gpt-6-luna -c model_reasoning_effort="high" -c skills.max_context_tokens=10000 debug prompt-input
```

This invocation-level budget affects the initial skill list. The checked default
loaded 130 of 165 declared plugin skill paths; the explicit budget loaded all
165 in the isolated offline run. It does not alter persistent user settings.

**Manual route.** Clone the repository, then have the agent read [`CLAUDE.md`](CLAUDE.md) (which imports `AGENTS.md`), the [skill routing index](docs/skill-routing-index.md), and only the `SKILL.md` files the task needs. Expose `skills/` and `00-meta-initialization/` to the working agent; [docs/USING-IN-A-PROJECT.md](docs/USING-IN-A-PROJECT.md) covers submodule, sibling-clone and read-only-mount wiring.

**Verify.** Run from the repository root. These are the steps of the CI workflow (`.github/workflows/skill-guardrails.yml`), in its order, plus `git diff --check` from [`CONTRIBUTING.md`](CONTRIBUTING.md). Each exited 0 on the current tree on Linux (Fedora, Python 3.14.8, Node 22.23.1) on 2026-10-31.

```sh
python3 -m pip install -r requirements-ci.txt
python3 -X utf8 scripts/skill_catalog_guardrails.py
python3 -X utf8 -m unittest tests/test_skill_catalog_guardrails.py
python3 -X utf8 -m pytest tests -q -p no:cacheprovider
python3 -X utf8 scripts/routing_smoke_test.py --min-rank1 89 --lint-fi