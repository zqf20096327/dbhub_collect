# IDP | Tidbits | Workflows — Know What Workflow Actions Are

> **Bite-sized how-to** | ~20 min setup

---

## What is a Workflow Action?

A workflow in Harness IDP is a self-service automation that developers trigger from the portal. Under the hood, every workflow is made up of **actions** — individual steps that execute in sequence.

An action can:
- Fetch a template and populate it with variables
- Create a GitHub repository
- Trigger a Harness pipeline
- Register a service in the IDP catalog
- Create a secret, open a PR, send a notification, and more

**Actions are the building blocks.** When you chain them together, you get a workflow that turns a developer's form input into automated infrastructure changes — without waiting for a DevOps team.

---

## What does this Tidbit demonstrate?

- **The Workflow Library** — 22 pre-built workflow templates organized by category (Deployment, Governance, Infrastructure, Service Lifecycle, Team People), each showing what's possible with workflow actions
- **Key workflow action types** — `fetch:template`, `publish:github`, `harness:trigger-pipeline`, `catalog:register` and others explained with use cases
- **A live workflow** — "Create New Microservice" that chains two actions:
  1. `fetch:template` — populates a skeleton with the developer's inputs
  2. `publish:github` — creates a GitHub repository under `harness-community`

**The demo:** A developer fills in a form (service name, description, owner) → clicks Execute → a GitHub repo is created automatically with a populated README, Express service starter, and `catalog-info.yaml` ready for catalog registration.

---

## Repository Structure

```
idp-tidbits-workflows-service-scaffold/
├── template.yaml              — workflow definition (2 actions, 2 parameter pages)
├── skeleton/
│   ├── catalog-info.yaml      — Harness IDP catalog entity (auto-populated)
│   ├── README.md              — generated README with service details
│   ├── package.json           — Node.js package
│   └── src/index.js           — basic Express service with /health endpoint
└── README.md
```

---

## Prerequisites

- A Harness account with the IDP module enabled
- A GitHub connector with write access to your target organization
- The GitHub Git Integration configured in Harness IDP
- The workflow registered in Harness IDP

---

## Step 1 — Set Up the GitHub Connector and Git Integration

The workflow uses GitHub in two places:
- **fetch:template** — reads the skeleton files from this repo
- **publish:github** — creates the new service repo in your GitHub org

Both require a GitHub connector with the right permissions.

**Create a GitHub Connector:**
1. Go to **Project Settings → Connectors → + New Connector → GitHub**
2. Name it (e.g., `idp-gh-connector`)
3. Select **Username and Token** authentication
4. Enter your GitHub username and a Personal Access Token with `repo` scope
5. Test the connection → Save

**Configure the Git Integration in IDP:**
1. Go to **IDP → Configure → Git Integrations**
2. Click **+ New Git Integration**
3. Select **Third-party Git provider**
4. Choose the GitHub connector you just created
5. Enter your repo URL to **Validate Permissions** — you should see "Great! You have necessary permissions for GitHub"
6. Save

> **Note:** Only one GitHub git integration is allowed per host. If one already exists, edit it to use the new connector instead of creating a new one.

---

## Step 2 — Understand Workflow Actions

Before building, explore what actions are available. In Harness IDP:

1. Go to **Workflows → Library**
2. Browse the 22 pre-built templates across 5 categories
3. Click **Preview & Install** on any template to see its actions

Key action types you'll encounter:

| Action | Purpose | Used for |
|---|---|---|
| `fetch:template` | Populate a skeleton with form values | Service scaffolding |
| `fetch:plain` | Copy files as-is without substitution | Boilerplate files |
| `publish:github` | Create a new GitHub repository | Scaffolding |
| `publish:github:pull-request` | Open a PR on an existing repo | Config changes |
| `catalog:register` | Register a service in IDP catalog | Onboarding |
| `harness:trigger-pipeline` | Trigger a Harness CI/CD pipeline | Deployment workflows |
| `harness:create-secret` | Create a Harness secret | Secret management |
| `debug:log` | Log output during execution | Testing/debugging |

---

## Step 3 — Register the Workflow

1. Go to **IDP → Create → Workflow** (Platform Engineer section)
2. Switch to **YAML** mode
3. Paste the contents of `template.yaml`
4. Click **Convert and proceed** if prompted → **Save**

The workflow **CreateNewMicroservice** will appear in your Workflows list.

---

## Step 4 — Execute the Workflow

1. Go to **IDP → Workflows → CreateNewMicroservice → Execute**
2. Fill in **Service Details:**
   - Service Name: `Payment Service`
   - Description: `Handles all payment processing`
   - Owner: select a group
   - Lifecycle: `Experimental`
3. Fill in **Repository:**
   - Repository Name: `payment_service` *(use underscores, not hyphens)*
4. Click **Execute**

The workflow runs two actions:
- **Fetch Skeleton Template** — pulls the `skeleton/` folder and fills in all variables
- **Create GitHub Repository** — creates `harness-community/payment_service` with the populated files

---

## Step 5 — Register the Service in Catalog

After the workflow succeeds:

1. Go to **IDP → Create → Component → Import from Git**
2. Select your GitHub connector
3. Repository: `harness-community/payment_service`
4. Branch: `main`
5. YAML Path: `catalog-info.yaml`
6. Click **Import**

The service appears in the IDP catalog with its description, owner, lifecycle, and scorecard.

---

## Key Concept — Why Actions Matter

A single workflow can chain as many actions as needed:

```
fetch:template  →  publish:github  →  harness:trigger-pipeline  →  catalog:register
      ↓                  ↓                       ↓                        ↓
Fill skeleton    Create repo          Run CI/CD pipeline          Register in catalog
```

This means a developer can go from "I need a new service" to "service is deployed and tracked" in one click — without touching Terraform, GitHub, or Harness directly.

---

## Step 5 — View Execution History

Every workflow execution is tracked. Go to **IDP → Workflows → Execution History** to see:

- **Execution ID** — unique identifier for each run
- **Started by** — who triggered the workflow
- **Status** — Success, Failed, or In Progress
- **Duration** — how long the workflow took
- **Actions** — how many actions ran and their individual status

Click any execution to drill into the action logs — see exactly what each step did, what values were passed, and any errors that occurred. This is your audit trail and debugging tool in one place.

---

## Resources

- [Harness IDP Documentation](https://developer.harness.io/docs/internal-developer-portal/)
- [Workflow Actions Reference](https://developer.harness.io/internal-developer-portal/use-idp/self-service-workflows/create-workflow/custom-actions)
- [Workflow Library](https://developer.harness.io/internal-developer-portal/use-idp/self-service-workflows/workflow-library/overview)
