# Teams & Dashboards — a Harness University Tidbit

A bite-sized how-to on getting **Teams** and **Dashboards** working in Harness
AI DLC Insights (SEI), starting from a developer records CSV.

The key thing to understand up front: **you do not create teams, and you do not
build dashboards.** You import people, create an **Org Tree**, and AI DLC
Insights derives the teams and populates three pre-built dashboards for you.

---

## What you'll learn

1. How to import developer records from a CSV
2. How to create an Org Tree — and why that is the only structure you build by hand
3. How teams are auto-derived, and the team settings you still must configure
4. The three out-of-the-box dashboards and what each one answers

**Time to complete:** ~15 minutes.

---

## The mental model

```
Developer records (CSV)
        ↓
    Org Tree          ← the only thing you build
        ↓
  Teams (auto)        ← every leaf node becomes a Team
        ↓
Insights dashboards   ← three, pre-built
```

| Piece | Who creates it |
|-------|----------------|
| **Developer records** | You — CSV upload from your HRIS |
| **Profiles** (Efficiency, Productivity, Business Alignment) | Already exist. You select them on the Org Tree |
| **Org Tree** | You — levels, filters, profiles, default integrations |
| **Teams** | **Auto-derived.** Every leaf node in the Org Tree is a Team |
| **Dashboards** | **Pre-built.** Three out-of-the-box Insights |

Everything on the Insights page is automatically scoped by your Org Tree,
Teams, and Profiles, so a developer, a team lead, and an executive each see the
level relevant to them.

---

## Repository layout

```
sei-tidbits-dashboards-and-teams/
├── README.md
└── developers-sample.csv    102 fictional developers, ready to import
```

Emails are `@acmecloud.io`. Nothing in this file is a real person or customer.

---

## Prerequisites

- A Harness account with **AI DLC Insights (SEI)** enabled
- Admin access (**AIDI Admin** role)
- Integrations connected for Issue Management (Jira), Source Code Management (GitHub), and CI/CD (Harness)

No secrets or tokens are stored in this repo.

---

## Step 1 — Import developer records

**Account Management → Developers → Import CSV**

Upload [`developers-sample.csv`](developers-sample.csv).

At minimum a developer CSV needs `Name`, `Email`, and `Manager Email`.
Optionally `Site`, `Role`, and `Team` — these become the attributes you can
build Org Tree levels and filters from, so it pays to include them.

The sample has 102 rows: one CTO root (**priya raman**), ten managers, and 91
individual contributors across `platform`, `payments`, `data`, `security`,
`experience`, `ai`, `sre`, `product`, `design`, and `docs`.

Two fields do the structural work:

- **`email`** — the developer identifier, and the join key to Jira and GitHub
- **`manager email`** — the reporting field the tree is built from

Re-uploading an updated CSV keeps the tree in sync. AIDI detects new hires,
reporting changes, and team moves, then rebuilds the tree automatically.

---

## Step 2 — Create the Org Tree

**Org Tree → + Create Org Tree**

This is the one structure you build by hand.

1. **Name** it, e.g. `Acme Cloud Engineering`.
2. **Levels** — how developers are grouped as you descend. With this CSV:
   - `Team` → 10 teams (one per team value)
   - `Team` → `Sub-team` → 19 teams (squad level)
   - `Department` → `Site` → `Team` for a cross-sectional view

   If you pick **Manager Email** as a level, no further levels are allowed
   beneath it — it produces the full reporting chain on its own.
3. **Data filters** — narrow which developer records are included, e.g.
   `Role` equals engineer. Multiple filters combine with AND. Check the
   **Developer Records** preview before continuing.
4. **Profiles** — select the **Efficiency**, **Productivity**, and
   **Business Alignment** profiles. These already exist; you are attaching, not
   authoring. Every team in the tree inherits them.
5. **Default integrations** — Issue Management, SCM, and CD for the whole tree.
   Teams can override later.
6. **Save Org Tree**.

You can create multiple Org Trees. Use one for the real reporting chain and
others for different lenses, such as business unit or geography.

> Changing a profile on an Org Tree re-interprets metrics for **every** team
> under it. Change deliberately.

### A brief word on profiles

You do not build a DORA profile from scratch. The **Efficiency** profile is
where DORA lives — Lead Time for Changes, Deployment Frequency, Change Failure
Rate, and MTTR, plus Sprint settings. Open it only when you need to tune how a
metric is calculated, for example which pipeline counts as a production
deployment. For a first run, the defaults are fine.

---

## Step 3 — Teams are created for you

**Teams**

Every **leaf node** in the Org Tree automatically becomes a Team. There is no
"create team" button, and you should not look for one.

What you *do* have to do is configure each team, because auto-derived teams
have no context about where their data lives.

Open a team to reach **Team Settings**:

- **Integrations** — select Issue Management, SCM, and Continuous Deployment.
  **This is mandatory.** You cannot complete the rest of the configuration
  until integrations are saved. You can attach multiple SCMs to one team.
- **Developer identifiers** — each developer's per-tool usernames. Without
  these, coding days and PR activity cannot be attributed.

Which integrations a team needs depends on the profile:

| Metric | Requires |
|--------|----------|
| Lead Time for Changes, MTTR | Issue Management |
| Deployment Frequency, Change Failure Rate | Continuous Deployment |
| Coding days, PR metrics | Source Code Management |

Once saved, AIDI starts attributing data and dashboards typically update within
minutes. Large syncs take longer.

---

## Step 4 — Read the three out-of-the-box dashboards

**Insights**, then pick your Org Tree from the dropdown at the top. Navigate the
tree to scope any dashboard to the organization, a sub-group, or a single team.

AI DLC Insights ships three pre-built dashboards. You do not create these.

### Efficiency

Throughput and stability — DORA Metrics plus Sprint Insights.

| Metric | What it shows |
|--------|----------------|
| Deployment Frequency | How often code is successfully deployed to production |
| Lead Time for Changes | Time for code to go from commit to production |
| MTTR | Mean time to recovery after a production failure |
| Change Failure Rate | Percentage of deployments causing a production failure |

### Productivity

How developers are working across pull requests, reviews, and commits.

| Metric | What it shows |
|--------|----------------|
| PR Velocity per Dev | Pull requests completed per developer |
| PR Cycle Time | Time for a PR to go from open to merged |
| Work Completed per Dev | Work completed per developer over time |
| Coding Days per Dev | Days a developer actively contributes code |
| Comments per PR | Average number of comments on pull requests |
| Average Time to First Comment | How long a PR waits for its first response |

### Business Alignment

How engineering output maps to product and business goals — work items grouped
into categories such as Strategic Work, Tech Debt, and Customer Commitments.

---

## Best practices

**Get the CSV attributes right before building the tree.** The Org Tree can
only group and filter on what the developer records contain. Adding `Site`,
`Role`, and `Team` up front saves a re-import later.

**Let leaf nodes land where a real manager owns the work.** That is your
natural team boundary, and it is what becomes a Team.

**Do not over-nest.** Every extra level is a level someone has to click
through to find their numbers.

**Configure integrations on every team.** An unconfigured team is the single
most common reason a dashboard looks empty. Integrations are mandatory for a
reason.

**Use multiple Org Trees instead of compromising one.** If two groups need
genuinely different measurement standards, build a second tree rather than
bending one profile to fit both.

**Expect non-engineering teams to look quiet.** The sample includes `design`,
`docs`, and `product`. They have little or no commit activity, so Efficiency
and Productivity will be sparse. Business Alignment still works, because it
runs on tickets.

---

## Troubleshooting

| Symptom | Likely cause |
|---------|--------------|
| A team's dashboards are empty | Integrations not selected and saved in **Team Settings** |
| Coding days and PR metrics blank | Developer identifiers not set for that team |
| Deployment Frequency / Change Failure Rate blank | No Continuous Deployment integration on the team |
| Lead Time or MTTR blank | No Issue Management integration on the team |
| A whole branch missing from the tree | That manager's email is not a row in the CSV |
| Two disconnected trees | More than one row has an empty `manager email` |
| Same person appears twice | Duplicate or case-variant email |
| Teams are too coarse or too granular | Change the Org Tree **levels** — leaf nodes are the teams |
| Metrics shifted after a change | A profile on the Org Tree was changed; it applies to all teams |

---

## Source documentation

- [Key concepts in AI DLC Insights](https://developer.harness.io/ai-dlc-insights/new-to-ai-dlc-insights/key-concepts)
- [Create Org Trees](https://developer.harness.io/software-engineering-insights/use-software-engineering-insights/setup-sei/setup-org-tree)
- [Configure Teams](https://developer.harness.io/software-engineering-insights/use-software-engineering-insights/setup-sei/setup-teams)
- [Manage developer records](https://developer.harness.io/software-engineering-insights/use-software-engineering-insights/setup-sei/manage-developers)
- [View Insights](https://developer.harness.io/ai-dlc-insights/use-ai-dlc-insights/view-insights)
- [Troubleshooting AI DLC Insights](https://developer.harness.io/ai-dlc-insights/troubleshooting-and-resources)

---

## A note on the data

Everything in this repository is fictional. The names, the `@acmecloud.io`
email addresses, and the org structure are generated sample data. No customer
information and no credentials are included, and none are needed to follow along.
