# MeterVanta

**AI Cost Intelligence & Usage-Based Billing Platform**

> **Control AI costs. Monetize usage. Protect your margins.**

If your product uses AI services such as ChatGPT (OpenAI), Claude (Anthropic) or Gemini (Google), every request costs you money, and those costs grow with every customer. MeterVanta shows you exactly what that AI spending is, who and what it's for, and helps you charge your customers for it.

_Know what your AI costs. Know what your AI earns._

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/screenshots/overview-dark.png">
  <img alt="The MeterVanta overview: spending today, this month and over the last 30 days, a month-end forecast, and each project's budget" src="docs/screenshots/overview-light.png">
</picture>

## What it does

- **Shows where your AI money goes.** See your AI spending by customer, by product feature and by AI agent, with the exact cost of every request.
- **Keeps spending under control.** Set monthly budgets and get an email, Slack or webhook alert at 80% and 100%. AI agents can ask MeterVanta before each step and stop before they go over budget.
- **Turns AI usage into revenue.** Create pricing plans with a monthly fee, included usage and a markup, then charge each customer for what they used. Invoices can be drafted in Stripe for you to review and send.
- **Shows which customers are worth it.** See each customer's revenue next to what their AI usage costs you, month by month.
- **Gives customers their own statement.** Send a customer a private link to a read-only page showing what they owe. They never see your costs.
- **Keeps your data yours.** You run MeterVanta on your own server or cloud account. It never sees your users' conversations, only how much each request used.

## Who it's for

| If you are…                                | MeterVanta helps you…                                                          |
| ------------------------------------------ | ------------------------------------------------------------------------------ |
| A software company with AI features        | Know what each customer's AI use costs, and bill them for it                   |
| An agency running AI agents for clients    | Track spending per client and keep every project within budget                 |
| A team building AI apps for others         | Show clients exactly what their AI usage costs, with a statement they can read |
| An enterprise team with a shared AI budget | See which teams and features use it, and get warned before it runs out         |

## A look inside

| See where spending goes                                                                                                                                                                                                                                             | See what each customer earns                                                                                                                                                                                                                  |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <picture><source media="(prefers-color-scheme: dark)" srcset="docs/screenshots/breakdown-dark.png"><img alt="Cost by customer: each customer's AI cost, share, requests and cost per resolved support ticket" src="docs/screenshots/breakdown-light.png"></picture> | <picture><source media="(prefers-color-scheme: dark)" srcset="docs/screenshots/revenue-dark.png"><img alt="Revenue and AI cost per customer for a month, and the difference between them" src="docs/screenshots/revenue-light.png"></picture> |
| **Spending over time**                                                                                                                                                                                                                                              | **Your customer's statement**                                                                                                                                                                                                                 |
| <picture><source media="(prefers-color-scheme: dark)" srcset="docs/screenshots/spend-dark.png"><img alt="Daily AI spending over 90 days, and spending by provider" src="docs/screenshots/spend-light.png"></picture>                                                | <picture><source media="(prefers-color-scheme: dark)" srcset="docs/screenshots/portal-dark.png"><img alt="A customer's read-only statement: what they owe, their plan and their charges" src="docs/screenshots/portal-light.png"></picture>   |

<sub>Screenshots use sample data.</sub>

## How it works

1. **Connect your app.** Your developer adds a few lines of code, so that after each AI request your app tells MeterVanta how much it used and for which customer.
2. **MeterVanta works out the cost.** It prices every request with the AI provider's published rates, and keeps a dated record of every price it used.
3. **You see, control and bill it.** Use the dashboard to watch spending, set budgets and alerts, and charge customers for their usage.

## Getting started

A developer installs MeterVanta once. After that, everyone on your team uses it from a web browser.

1. **Install it.** Put it on [Vercel](https://vercel.com) with a hosted database, or on your own server. See the [deployment guide](docs/DEPLOYMENT.md).
2. **Connect your app.** Follow the [quickstart](docs/QUICKSTART.md) and the [integration guide](docs/INTEGRATION.md).
3. **Invite your team.** Add colleagues from the **Team** page as admins, members or read-only viewers.
4. **Optional: start billing.** Set up plans and customers. See the [billing guide](docs/BILLING.md).

## Common questions

**Which AI services does it work with?**
OpenAI, Anthropic (Claude) and Google (Gemini) are fully supported. Others, such as Mistral, can report their usage too.

**Does it see our users' conversations?**
No. Only usage figures are sent, such as how much text the AI read and wrote (measured in "tokens"), never the content itself.

**Does it charge our customers automatically?**
It works out each customer's charges and can create draft invoices in Stripe. You review and send them, so nothing goes out without you.

**What does it cost?**
MeterVanta itself is free and open source, under the MIT license. You only pay for wherever you host it. Free hosting plans are enough to try it out; for business use, choose a paid plan, since Vercel's free plan is for non-commercial use.

**Is our data safe?**
It runs on your own account, so your data stays with you. Passwords and keys are stored securely, sign-in supports your company's single sign-on, and an audit log records who changed what.

## For developers

| Guide                                      | What's in it                                                       |
| ------------------------------------------ | ------------------------------------------------------------------ |
| [Quickstart](docs/QUICKSTART.md)           | A recorded, priced request in about ten minutes                    |
| [Integration guide](docs/INTEGRATION.md)   | Connecting a real app, with a go-live checklist                    |
| [Technical reference](docs/REFERENCE.md)   | Installation, every dashboard page, the APIs, data model and tests |
| [Deployment](docs/DEPLOYMENT.md)           | Docker Compose, or Vercel with hosted Postgres                     |
| [Billing](docs/BILLING.md)                 | Plans, charges, credit, Stripe invoicing and the customer portal   |
| [Architecture](docs/ARCHITECTURE.md)       | How it fits together, and why                                      |
| [Cost accounting](docs/COST-ACCOUNTING.md) | How each request's cost is calculated and checked                  |
| [Demos](docs/DEMOS.md)                     | Runnable sample scenarios                                          |
| [Release notes](docs/RELEASE_NOTES.md)     | What's in each version                                             |

Contributions are welcome: see [CONTRIBUTING.md](CONTRIBUTING.md). Licensed under the [MIT License](LICENSE).
