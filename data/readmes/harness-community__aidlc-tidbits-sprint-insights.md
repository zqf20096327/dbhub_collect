# Sprint Insights — a Harness University Tidbit

A bite-sized how-to on configuring **Sprint Insights** in Harness AI DLC
Insights (AIDI): start from an existing organization and teams, set Sprint
settings in the **Efficiency Profile**, then read the **Sprint Metrics**
dashboard.

The key thing to understand up front: **the Efficiency Profile defines how you
measure sprint activity, and the Sprint Metrics dashboard is where those
measurements show up for the teams in your Org Tree.** You do not build a
separate sprint dashboard. You configure Summary Cards, Delivery Analysis, and
Sprint Boundary Grace Periods once, save the profile, and Insights reflects it.

---

## What you'll learn

1. How Sprint settings live in the **Efficiency Profile** (alongside DORA)
2. How to configure **Summary Cards**, **Delivery Analysis**, and **Sprint
   Boundary Grace Periods**
3. How those settings appear on the **Sprint Metrics** dashboard for an Org
   Tree and its teams
4. How to read planning, delivery, scope-change, velocity, and predictability
   metrics — including Sprint Details and work-item drill-down

**Time to complete:** ~15 minutes.

---

## The mental model

```
Org Tree and teams
        ↓
Efficiency Profile → Sprints   ← Summary Cards, Delivery Analysis, grace periods
        ↓
Insights → Sprint Metrics      ← scoped to the selected Org Tree
```

| Piece | Who creates it |
|-------|----------------|
| **Org Tree and teams** | Already in place for this tidbit (example: Raj Org) |
| **Efficiency Profile (DORA + Sprints)** | You — tune which sprint metrics to show and how boundaries work |
| **Sprint Metrics dashboard** | **Pre-built.** Insights reflects the saved Sprint configuration |

The overall flow is simple: teams sit under the Org Tree, the Efficiency
Profile defines how sprint activity is measured, and the Sprint Metrics
dashboard brings those measurements together so you can understand how teams
plan and deliver sprint work.

---

## Repository layout

```
aidlc-tidbits-sprint-insights/
└── README.md
```

This tidbit is configuration-and-read only. It uses an organization you already
have in Insights.

---

## Prerequisites

- A Harness account with **AI DLC Insights (SEI)** enabled
- Admin access (**AIDI Admin** role)
- An existing **Org Tree** with teams (this walkthrough uses **Raj Org**)
- An **Efficiency Profile** with DORA already in place
- Issue management connected so sprint boundaries and work items can be read

No secrets or tokens are stored in this repo.

---

## The example org

This walkthrough uses **Raj Org** with multiple teams under it.

On the **Insights** page, the organization is at the top. Teams in this Org
Tree include:

- Others
- Data
- Reliability
- Payments
- Experience
- Platform

When you select an Org Tree, **Sprint Metrics are scoped to the teams and
repositories within that Org Tree.** That is the team-level view of sprint
performance.

---

## Step 1 — Open the Efficiency Profile (Sprints)

Start from the existing organization and teams, then open the **Efficiency
Profile**.

DORA configuration is already in place. Open the **Sprints** section. This is
where you configure the metrics you want for sprint **planning**,
**delivery**, and **predictability**.

There are three main areas:

1. **Summary Cards**
2. **Delivery Analysis**
3. **Sprint Boundary Grace Periods**

Go through them one by one.

---

## Step 2 — Configure Summary Cards

**Summary Cards** give a quick view of the key sprint metrics.

| Metric | What it shows |
|--------|----------------|
| **Sprint Commit** | Amount of work that was planned at the start of the sprint |
| **Sprint Creep** | Additional work that was added after the sprint started |
| **Sprint Size** | Total size of the sprint at the sprint end date |
| **Average Sprint Size** | Average size of the sprint across multiple sprints |
| **Scope Creep %** | Ratio of work added after the sprint started compared to the original sprint commitment |

Together these show how the sprint was planned, how the scope changed, and how
much work the team was dealing with.

---

## Step 3 — Configure Delivery Analysis

**Delivery Analysis** is how the team delivered against the sprint scope.

| Metric | What it shows |
|--------|----------------|
| **Committed Work Delivered** | Work delivered against the original sprint commitment |
| **Creep Work Delivered** | Additional work that was added after the sprint started and was delivered |
| **Total Work Delivered** | Overall work delivered against the final sprint scope |

You can enable these metrics and customize their display names based on how you
want them to appear in the dashboard. This is how you see not just what was
planned, but also what was actually delivered.

---

## Step 4 — Configure Sprint Boundary Grace Periods

**Sprint Boundary Grace Periods** define a small time window around the start
of a sprint.

In this example, **Sprint Start Grace Period** is set to **two days**. Work
completed within those two days **before** the sprint starts can still be
counted toward the planned sprint work.

Example: if a sprint starts on January 1st, work completed on December 30th or
31st can be included. That accounts for work finished just before the official
sprint start date.

---

## Step 5 — Save the Efficiency Profile

Once the Sprint metrics you want are configured, **save the Efficiency
Profile**. The Sprint configuration is then ready. It becomes part of the
Sprint Metrics view in Insights.

---

## Step 6 — Open Sprint Metrics in Insights

Go back to the **Insights** page.

1. Select **Raj Org** (or your Org Tree) at the top.
2. Confirm the teams under that tree (Others, Data, Reliability, Payments,
   Experience, Platform in this example).
3. Within **Efficiency**, switch from **DORA** to **Sprint Metrics**.

That is the Sprint Insights dashboard.

### How you can view the data

At the top, choose how you want to view the data:

- **Story Points** (used in this example)
- **Work Item Count**

You can also enable **Show trendline** to see how the metrics are changing over
time.

---

## Step 7 — Read the Sprint Metrics dashboard

### Planning metrics (top)

These help you understand the original sprint plan and how the scope changed:

- Sprint Commit
- Sprint Creep
- Sprint Size
- Average Sprint Size

### Delivery metrics

These help you understand what happened to the planned and additional work
during the sprint:

- Delivered Commit
- Missed Commit
- Delivered Creep
- Work Delivered

### Context around delivery and scope change

- Sprint Velocity
- Total Delivered Work vs Committed Work
- Churn Rate
- Work Removal Rate

### Predictability metrics

These show how consistently the team delivers against its sprint commitments.

Together, these metrics give a broader picture of sprint **planning**,
**execution**, and **delivery**.

### Sprint Details

As you scroll down, **Sprint Details** gives a more detailed view of sprint
activity over time.

- Compare committed work with delivered work across different sprints.
- Use the sprint-level view to analyze the performance of specific sprints.
- Drill into the underlying work items to see which items were delivered,
  which were missed, and which were added after the sprint started.

That context sits behind the numbers on the dashboard.

---

## Recap

1. Start with the Org Tree and teams.
2. Open the Efficiency Profile and go to the **Sprints** section.
3. Configure **Summary Cards**, **Delivery Analysis**, and **Sprint Boundary
   Grace Periods**.
4. Save the profile — that configuration becomes part of the Sprint Metrics
   view in Insights.
5. For Raj Org and its teams, you can see sprint planning, delivery, scope
   changes, velocity, and predictability metrics in one place.

With this setup, you move from the team structure to the actual sprint data
and understand **commitment**, **delivery**, **scope changes**, and
**predictability** across sprints.

---

## Source documentation

- [Key concepts in AI DLC Insights](https://developer.harness.io/ai-dlc-insights/new-to-ai-dlc-insights/key-concepts)
- [View Insights](https://developer.harness.io/ai-dlc-insights/use-ai-dlc-insights/view-insights)
- [Sprint metrics reference (Agile metrics)](https://developer.harness.io/software-engineering-insights/use-software-engineering-insights/analytics-and-reporting/efficiency/agile-metrics)
- [Create a Sprint metrics Insight (classic SEI tutorial)](https://developer.harness.io/software-engineering-insights/use-software-engineering-insights/setup-sei/create-and-manage-dashboards/insight-tutorials/agile-insights)
