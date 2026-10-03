<img src="assets/logo.svg" alt="claude-skills logo" width="88" align="right" />

# claude-skills for business

[![License: MIT](https://img.shields.io/github/license/fdtaljaard/claude-skills)](LICENSE)
[![Latest release](https://img.shields.io/github/v/release/fdtaljaard/claude-skills)](https://github.com/fdtaljaard/claude-skills/releases)
[![Claude Code plugin marketplace](https://img.shields.io/badge/Claude%20Code-plugin%20marketplace-5A4FE5)](#installing-a-skill)

A public collection of [Agent Skills](https://agentskills.io/specification) for Claude, by Francois Taljaard — reference-backed assistants for ERP consultants and integrators (Sage 300, Sage 200 Evolution, Sage X3, SAP Business One).

> **The point of these skills: no guessing.** Every material claim — a table or field, an enum value, a version requirement, an SDK class or method — comes from a **bundled reference** (data dictionaries, release notes, SDK class/enum references extracted from the vendors' own files) or a fresh fetch of the vendor's official docs, and is **cited**. Field names, enum values and version facts are exactly what a language model otherwise guesses plausibly and wrongly, so each skill is built to look them up and show its source.

## Skills

| Skill | What it does |
|---|---|
| [`sage300-assistant`](skills/sage300-assistant) | Sage 300 (Accpac) ERP assistant for consultants and integrators: verified T-SQL views/queries from bundled AOM data dictionaries, version/upgrade guidance and release notes, and C# against the `ACCPAC.Advantage` .NET library. |
| [`sage200-assistant`](skills/sage200-assistant) | Sage 200 Evolution (Pastel Evolution) ERP assistant for consultants and integrators: C# development against the `Pastel.Evolution` .NET SDK — connecting via `DatabaseContext`, the record load/set/`Save()` pattern, posting transactions, and generating correct code from a bundled class and enum reference (152 types, 41 enums) extracted from the shipped SDK CHM. More capabilities to follow. |
| [`sapb1-assistant`](skills/sapb1-assistant) | SAP Business One ERP assistant for consultants and integrators: object type number, table and primary key lookup from a bundled list of all B1 object types, verified SQL views/queries from bundled B1 10.0 and 9.3 data dictionaries (tables, columns, indexes, valid values, parent-table links), C# development against the DI API (`SAPbobsCOM`) from a bundled DI API 10.0 class and enum reference, and Service Layer (REST / OData v4) integration guidance (session handling, query options, ETags, batch, SQLQueries, FP 2602 webhooks) summarised from SAP's documentation. More capabilities to follow. |
| [`sagex3-assistant`](skills/sagex3-assistant) | Sage X3 ERP assistant for consultants and integrators: verified SQL views/queries and table/field lookup from a bundled Sage X3 **V11** table dictionary (every table with abbreviation, keys/indexes, columns, data types, dimensions, local-menu enum values and foreign-key link expressions) compiled from Sage's online help; versions and upgrades — V12 release/patch naming and lifecycle, platform prerequisites per release, upgrade paths and procedures, and per-release notes 2023 R2 → 2026 R1 with the tables whose definition changed. More capabilities to follow. |

## Installing a skill

These skills run inside **[Claude Code](https://www.claude.com/product/claude-code)** — Anthropic's assistant that you use through the Claude desktop app or the `claude` command. You don't need to write any code to install or use them. You add this collection once, then install whichever skill you need.

**Step 1 — Add this collection (do this once).** In Claude Code, type:

```
/plugin marketplace add fdtaljaard/claude-skills
```

This just tells Claude where to find the skills. You only ever do it once.

**Step 2 — Install the skill you want.** Type one of:

```
/plugin install sage300-assistant@fdtaljaard-skills
/plugin install sage200-assistant@fdtaljaard-skills
/plugin install sapb1-assistant@fdtaljaard-skills
/plugin install sagex3-assistant@fdtaljaard-skills
```

(Pick the one for the system you work with — Sage 300, Sage 200 Evolution, SAP Business One, or Sage X3.)

**Step 3 — Just ask your question in plain English.** There's no special command to "turn it on" — the skill switches itself on whenever your question is about that product. For example: *"I need a Sage 300 view of open sales orders with the customer name and total."* Claude looks the answer up in the bundled reference and shows its working.

**Keeping it current.** To get the latest version later, type `/plugin marketplace update fdtaljaard-skills`. To remove a skill, type `/plugin uninstall <skill-name>@fdtaljaard-skills`.

<details>
<summary><b>Other ways to install (for developers)</b></summary>

**With the [skills CLI](https://agentskills.io):**

```bash
npx -y skills add fdtaljaard/claude-skills --skill sage300-assistant --agent claude-code
```

**Manually** — copy the skill folder into your Claude skills directory (`~/.claude/skills/` for all projects, or `<project>/.claude/skills/` for one):

```bash
git clone https://github.com/fdtaljaard/claude-skills.git
cp -r claude-skills/skills/sage300-assistant ~/.claude/skills/
```

Each skill's `SKILL.md` describes when it triggers and how it works; `MAINTENANCE.md` covers how it is built and kept up to date.

</details>

## Layout

```
skills/
  <skill-name>/
    SKILL.md        # entry point loaded on activation
    references/     # bulk reference material, read on demand
    scripts/        # maintenance tooling (not needed at runtime)
```

## Contributing

Issues and pull requests are welcome — corrections to a reference, a new skill, or a new capability on an existing one. See [CONTRIBUTING.md](CONTRIBUTING.md) for how skills are structured and the bar a change should meet (every claim verifiable and cited), and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for how we work together. To report a problem with the data a skill returns, or a security concern, see [SECURITY.md](SECURITY.md).

## License

The code and original content in this repository are released under the [MIT License](LICENSE). Reference material derived from Sage's documentation and product metadata remains subject to Sage's own terms (see the disclaimer below).

## Disclaimer

Sage 300 and Accpac are trademarks of their respective owners. This project is independent and not affiliated with or endorsed by Sage. Reference material bundled with `sage300-assistant` is derived from Sage's published documentation and product metadata for use as a lookup aid; always verify against official Sage documentation before acting on it in a production system.

Sage 200 Evolution and Pastel Evolution are trademarks of their respective owners. `sage200-assistant` is independent and not affiliated with or endorsed by Sage. Its SDK reference is extracted from the shipped `Pastel.Evolution.chm` and XML documentation for SDK version **11.0.0.10 only** (other versions are not included), and Sage's own terms apply to that material. It documents the `Pastel.Evolution` object SDK, not the Evolution ODBC/SQL layer or the Connector/API web service. Verify against Sage's own documentation, and on the client's installed SDK, before relying on any of it — the SDK binds to a licensed Evolution install of a matching version.

Sage X3 is a trademark of its respective owner. `sagex3-assistant` is independent and not affiliated with or endorsed by Sage. Its table dictionary is a compact extraction of facts (table and column names, types, keys, local-menu values, link expressions) from the "Table dictionary" pages of Sage's public online help for **Sage X3 V11 only** (`online-help.sagex3.com/erp/11/`), not a copy of those pages; Sage's own terms apply to that material. Other versions (V12 and later, V9/V10 patches), folder-specific customizations, activity-code-dependent columns and local-menu changes are not included. Confirm against Sage's own documentation, and on the client's folder, before relying on any of it.

SAP and SAP Business One are trademarks of SAP SE. `sapb1-assistant` is independent and not affiliated with or endorsed by SAP. Its object type list is compiled from community websites, its B1 10.0 schema dictionary and DI API reference are compiled from SAP's own SDK help (`REFDB.chm`, `REFDI.chm`) and SAP's terms apply to them, its 9.3 schema dictionary comes from erpref.com (a third party; the schema IP belongs to SAP), and its Service Layer references are prose summaries of SAP Help Portal pages (sources and caveats are in `skills/sapb1-assistant/references/objects/INDEX.md`, `skills/sapb1-assistant/references/dictionary/INDEX.md`, `skills/sapb1-assistant/references/diapi/INDEX.md` and `skills/sapb1-assistant/references/servicelayer/INDEX.md`). The schema dictionaries cover SAP Business One **10.0 and 9.3 only**; other releases (including later feature packs) and client-specific user-defined tables and fields are not included. Confirm against SAP's own documentation, and on the client's database, before relying on any of it.
