# Non-Traditional Teams — a Harness University Tidbit

A bite-sized how-to on modeling **cross-functional squads, tribes, vendors, and
matrix reporting** in Harness AI DLC Insights (AIDI), starting from a developer
records CSV.

Traditional teams follow a manager and their reports. This tidbit is for the
other shape: people who sit in one reporting line but ship with another squad,
share a tribe, or work through a vendor.

The key thing to understand up front: **non-traditional teams are CSV
attributes plus Org Tree levels.** You still do not create teams by hand. You
import people, group on the attributes that define the team, and AIDI derives
leaf-node teams for you.

---

## What you'll learn

1. How to import a developer CSV that is rich enough for matrix and
   cross-functional grouping
2. How **reporting manager** and **most common manager** differ — and when to
   use each
3. How to create Org Trees by **squad**, **tribe**, **location**, **business
   unit**, **department**, or **vendor**

**Time to complete:** ~15 minutes.

---

## The mental model

```
Developer records (CSV with extra attributes)
        ↓
    Org Tree          ← group by squad / tribe / vendor / location / …
        ↓
  Teams (auto)        ← every leaf node becomes a Team
        ↓
Insights dashboards   ← scoped to that non-traditional cut
```

| Piece | Who creates it |
|-------|----------------|
| **Developer records** | You — CSV upload from your HRIS, plus the extra columns this tidbit uses |
| **Org Tree** | You — levels and filters that cut across reporting lines |
| **Teams** | **Auto-derived.** Every leaf node in the Org Tree is a Team |

Use **one tree for the real reporting chain** (manager email) and **other trees
for non-traditional lenses**. Do not force squads into the manager tree.

---

## Repository layout

```
aidlc-tidbits-non-traditional-teams/
├── README.md
└── developers-sample.csv    91 fictional people, ready to import
```

Emails are `@acmecloud.io`. Nothing in this file is a real person or customer.

---

## Prerequisites

- A Harness account with **AI DLC Insights (SEI)** enabled
- Admin access (**AIDI Admin** role)
- Integrations connected for Issue Management (Jira), Source Code Management (GitHub), and CI/CD (Harness)

No secrets or tokens are stored in this repo.

---

## Sample data at a glance

The sample has **91 rows**: one CTO root (**ava collins**), four VPs, five
directors, ten engineering managers, and ICs across engineering, product,
design, and docs. Every name and email is dummy data.

The org-tree grouping you will use most is **Business Unit → Department → Team**.
The canonical path in this file is **Engineering → Payments → Checkout**.
Engineering also has two sibling departments (**Platform**, **Data**). Two dummy
BUs (**Product**, **Operations**) sit beside Engineering so a BU-level tree is
not a single node.

| Column | What it is for |
|--------|----------------|
| `name`, `email` | Developer identifier; join key to Jira and GitHub |
| `manager name`, `manager email` | **Reporting manager** — the HR / org-chart line |
| `most common manager`, `most common manager email` | Who they actually work with most. Differs from reporting manager for **24** people (matrix) |
| `location` | Region: `AMER`, `EMEA`, or `APAC` only |
| `site` | Remote site aligned to region (`amer-remote`, `emea-remote`, `apac-remote`) |
| `business unit` | `Engineering` (primary), plus dummy `Product` and `Operations` |
| `department` | Under Engineering: `Payments`, `Platform`, `Data`. Dummy BUs use `Experience` and `Reliability` |
| `team` | Delivery team, e.g. `Checkout` under Payments. Also `Risk`, `Core`, `Identity`, `Metrics`, `Assist`, and dummy teams |
| `squad` | Cross-functional delivery unit (e.g. `payments-checkout`, `platform-iam`) |
| `tribe` | Cluster of squads: `platform tribe`, `payments tribe`, `insights tribe`, `growth tribe` |
| `vendor` | Empty for employees; `Vendor A`, `Vendor B`, or `Vendor C` for contractors |
| `role`, `sub role`, `sub-team`, `job-function`, `start date`, `executive`, `status` | Standard AIDI fields so you can still build a classic reporting tree |

Reporting lines stay intact: **one empty `manager email`** (the CTO). Re-upload
keeps the tree in sync.

---

## Step 1 — Import developer records

**Account Management → Developers → Import CSV**

Upload [`developers-sample.csv`](developers-sample.csv).

At minimum AIDI needs `Name`, `Email`, and `Manager Email`. Everything else is
optional **until you want a non-traditional team**. Then the grouping attribute
must already be a column.

After import, confirm custom columns appear as Org Tree level and filter
options: `squad`, `tribe`, `location`, `business unit`, `department`, `vendor`,
and `most common manager`.

---

## Step 2 — Group by attribute (Org Tree)

**Org Tree → + Create Org Tree**

This is how you model standing cross-functional groups.

1. **Name** it for the lens, e.g. `Acme Squads` or `Acme Vendors`.
2. **Levels** — pick the attribute that *is* the team boundary, not manager
   email. Examples with this CSV:

   | Levels | What you get |
   |--------|----------------|
   | `Business Unit` → `Department` → `Team` | **Engineering → Payments → Checkout** (plus Platform/Data teams, and dummy Product / Operations BUs) |
   | `Tribe` → `Squad` | Four tribes, then squad-level leaf teams that cut across reporting lines |
   | `Vendor` | Three contractor populations plus employees (empty vendor) |
   | `Location` | `AMER` / `EMEA` / `APAC` |
   | `Most common manager` | Matrix view — people grouped by who they work with, not who they report to |
   | `Manager Email` | Classic org chart only. **No further levels** are allowed beneath it |

3. **Data filters** — carve a subset, e.g. `Role` equals engineer **and**
   `Tribe` equals checkout tribe. Multiple filters combine with AND. Check
   **Developer Records** preview before continuing.
4. **Profiles** — attach Efficiency, Productivity, and Business Alignment.
5. **Default integrations** — Issue Management, SCM, and CD.
6. **Save Org Tree**.

Keep a separate tree for manager email if leadership still needs the reporting
hierarchy.

> Changing a profile on an Org Tree re-interprets metrics for **every** team
> under it. Change deliberately.

---

## Step 3 — Configure teams and read Insights

Every **leaf node** is still a Team. Open **Team Settings**:

- **Integrations** are mandatory before the rest of the config unlocks.
- **Developer identifiers** must be set or coding days and PR metrics stay
  blank.

Then open **Insights**, pick the Org Tree that matches the question:

| Question | Tree to use |
|----------|-------------|
| How is Checkout shipping? | `Business Unit` → `Department` → `Team`, open **Engineering / Payments / Checkout** |
| How is checkout shipping by squad? | `Tribe` → `Squad`, open `payments-checkout` |
| How is Vendor B performing? | Tree leveled on `Vendor` |
| How is AMER vs EMEA vs APAC? | Tree leveled on `Location` |
| Who actually manages this person's work? | Tree leveled on `Most common manager` |
| Classic span of control | Tree leveled on `Manager Email` |

---

## Best practices

**Put the grouping attribute in the CSV first.** Squad, tribe, vendor, and
most-common-manager teams cannot exist until those columns exist.

**Use multiple Org Trees instead of one compromised tree.** Reporting chain in
one; squads, vendors, and geography in others.

**Reporting manager is HR truth; most common manager is delivery truth.** When
they disagree, that person is matrixed. Decide which lens the dashboard is for.

**Vendors need the same identity mappings as employees.** Empty `vendor` means
FTE in this sample; `Vendor A` / `Vendor B` / `Vendor C` are the three partner
options.

**Expect design, docs, and product to look quiet** on Efficiency and
Productivity. Business Alignment still works because it runs on tickets.

**Do not over-nest.** `Business Unit` → `Department` → `Team` is the intended
tree for this file (`Engineering` → `Payments` → `Checkout`). `Tribe` → `Squad`
is the cross-functional alternative. Adding location under every team usually
just adds clicks.

---

## Troubleshooting

| Symptom | Likely cause |
|---------|--------------|
| Cannot group by squad / tribe / vendor | Column missing from the CSV, or not mapped on import |
| Squad teams still look like reporting teams | Org Tree levels are still `Manager Email` |
| Matrix contributors missing from a squad | They have the wrong `squad` or `most common manager` value in the CSV |
| Vendor tree has a huge "empty" team | Employees have a blank `vendor`; filter them out if you only want partners |
| A whole branch missing | That manager's email is not a row in the CSV |
| Two disconnected trees | More than one row has an empty `manager email` |
| A team's dashboards are empty | Integrations not saved in **Team Settings** |

---

## Source documentation

- [Key concepts in AI DLC Insights](https://developer.harness.io/ai-dlc-insights/new-to-ai-dlc-insights/key-concepts)
- [Create Org Trees](https://developer.harness.io/software-engineering-insights/use-software-engineering-insights/setup-sei/setup-org-tree)
- [Configure Teams](https://developer.harness.io/software-engineering-insights/use-software-engineering-insights/setup-sei/setup-teams)
- [Manage developer records](https://developer.harness.io/software-engineering-insights/use-software-engineering-insights/setup-sei/manage-developers)
- [View Insights](https://developer.harness.io/ai-dlc-insights/use-ai-dlc-insights/view-insights)

---

## A note on the data

Everything in this repository is fictional. The names, the `@acmecloud.io`
email addresses, and the org structure are generated sample data. No customer
information and no credentials are included, and none are needed to follow along.
