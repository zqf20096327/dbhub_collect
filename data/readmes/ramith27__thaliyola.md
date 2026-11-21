# Thaliyola

*Thaliyola* (തളിയോല) is Malayalam for the palm-leaf manuscripts Kerala used to write knowledge down and keep it for the next generation.

A shared team knowledge base exposed as a remote [MCP](https://modelcontextprotocol.io) server. Every Claude client on a team reads and writes the same knowledge: systems, metrics, runbooks, project design docs, API contracts and UI/UX specs, plus the findings from past investigations.

The server holds no LLM. Clients (Claude Code, claude.ai, scheduled agents) do the reasoning; Thaliyola stores, searches, validates and versions. Agent-written content goes through human review before it is published.

| Home | Knowledge graph | Project |
|---|---|---|
| ![Home: search, setup checklist and spaces](docs/images/home.png) | ![Knowledge graph](docs/images/graph.png) | ![A project's articles by folder](docs/images/project-frontend.png) |
| **Design system** (inherits from the Library) | **Sessions** asking each other | **Security** |
| ![Design system with inherited and overridden colours and contrast checks](docs/images/design.png) | ![Sessions: who can be asked, listening or busy](docs/images/sessions.png) | ![Security: vulnerabilities needing attention](docs/images/security.png) |
| **Incident** with its timeline | **Pull request briefings** | **What happened lately** |
| ![An incident: severity, status, and a timeline of notes and status changes](docs/images/incident.png) | ![Pull requests briefed, with the PR briefing setting and webhook](docs/images/pulls.png) | ![A project's brief: incidents, decisions, new knowledge](docs/images/brief.png) |
| **Guide**: every feature and command | **On a phone** | **Health** |
| ![Guide: what's switched on and every command](docs/images/guide.png) | <img src="docs/images/design-phone.png" alt="Design system on a phone" width="220"> | ![Admin › System › Health: backups, restore checks, jobs](docs/images/health.png) |

New here? Open **Guide** in the app (`#/guide`) for every feature, whether it's switched on, how to use it and every command, or read [`docs/`](docs/README.md).

## Concepts

**Scopes**

| Scope | Holds |
|---|---|
| `team` | Org-wide systems, metric definitions, runbooks, team decisions |
| one per project | Project overview, design docs, decisions, API contracts, screen specs, project findings |
| `library` | Reusable items shared across projects: UI component specs, design tokens, UX and tech patterns, shared contracts |

A project can declare that it **uses** an item from the library or from another project; that item then appears in the project's context and search results.

**Components.** A project can have several codebases (`backend`, `frontend`, `mobile`, ...). API contracts link the component that provides them to the components that consume them. When a contract or a shared design changes, consumers get an **impact notice** that shows up the next time an agent loads the project context.

**Design knowledge.**
- **Item types:** design tokens, UI component specs, UX patterns and screen specs.
- **Attachments:** screenshots and token files, which can also be embedded in markdown with `![alt](asset:<id>)`.
- **Figma:** frames are linked as source links. Figma stays the visual source of truth; Thaliyola holds the reviewed intent and rules.
- **Wiring:** a screen spec `uses` library UI components and `depends_on` the API contract it calls. A change to either reaches the teams that depend on it as an impact notice.

**Articles and findings.** Articles are curated, long-lived documents written to a template per type. Findings are episodic: incidents, RCAs, known issues, data gotchas, query recipes.

## MCP tools

| Tool | Purpose |
|---|---|
| `search_knowledge` | Hybrid keyword and semantic search over article sections and findings. Defaults to the current project + team + library |
| `get_article` | One article, or one section of it, with relations, source links and entities |
| `get_finding` | One finding with relations, s

[...截断...]

ource links and review history |
| `browse_kb` | Folder tree of articles in a scope |
| `list_projects` | Projects with components and Project admins (with their names) |
| `get_project_context` | Cold-start context for an agent in a project or component: overview, contracts, impact notices, recent decisions, shared items it uses, known issues |
| `list_impact_notices` / `ack_notice` | Upstream contract or shared-design changes a project or component hasn't handled yet |
| `list_review_queue` | Pending and decided proposals (`mine: true` for your own), plus `skill_reviews`: how many skill versions wait for you |
| `get_article_template` | Expected sections for an article type |
| `list_stale_entries` | Entries not verified recently and articles past their review date |
| `list_suggestions` | Recurring root causes to fold into an article (with a suggested target), and unlinked near-duplicate findings |
| `get_asset` | A screenshot, exported frame, token file, spec or PDF attached to an item. Images come back as MCP image content the agent can look at. PDFs (reports, audits, exports) come back as their text with page markers; long ones arrive in parts (`pages: "5-9"`, and `next_pages` says what to read next). `as: "file"` returns the file itself (up to 8 MB), e.g. for a scanned PDF with no text |

**Write tools.** Every write is a proposal that a person reviews before it is published:

| Tool | Purpose |
|---|---|
| `propose_finding` | Capture a confirmed root cause, incident, known issue, data gotcha or query recipe. Returns near-duplicates instead of storing when it finds them |
| `update_finding` | Propose changes to a finding |
| `create_article` | Propose a new article of any type |
| `propose_article_edit` | Propose new text for one section of an article, and/or change its tags: `tags` replaces them all, `add_tags` / `remove_tags` change some (not both at once). A tags-only edit needs no text: **to fix a stale tag, `propose_article_edit` with `add_tags` / `remove_tags`**. Tags are normalised (lower case, hyphens, no duplicates) and reviewed like text. On approval, components consuming a contract and projects using a shared item get an impact notice |
| `promote_finding` | Propose folding a recurring finding into an article section |
| `verify_entry` | Mark an entry still valid (applied immediately; refreshes freshness but never moves an article's review date), or propose that it is superseded |
| `link_entries` | Add a typed link: `uses`, `provided_by`, `consumed_by`, `depends_on`, `related`, `same_root_cause`, `supersedes` |
| `add_source_link` | Attach a Figma frame, PR, Sentry issue or dashboard to an item |
| `upload_asset` | Attach a screenshot (PNG/JPEG/WebP/GIF), token JSON, markdown or PDF. Text files are redacted; images can't be |
| `share_to_library` | Propose publishing a project item to the library. On approval by someone who can review in the library, a copy (with its links and files) is created and the project is linked to it |

**Approval tools.** A person who may review decides through Claude, with exactly the permissions they have in the web app, while **Approvals from Claude** is on (see [Review](#review)):

| Tool | Purpose |
|---|---|
| `get_proposal` | One proposal: the item now (`current`) and what it would become (`proposed`), who wrote it, whether it's stale and whether you may decide it (`can_review`) |
| `review_proposal` | Approve (optionally with `edits`) or reject (with a `reason`) a proposal. Your own proposal written through Claude in the last 10 minutes needs `confirmed_by_user: true` |
| `list_skill_reviews` / `get_skill_version` | Skill versions waiting for review with `can_approve`, flags and import groups / one version's files and diff |
| `review_skill_version` | Approve or reject a skill version; `checked_flags` / `checked_tools` when it has high-risk flags or pre-approved tools. Never one you proposed or whose import you started |
| `approve_skill_import` | Approve an import's low-ri