# IaCM | Tidbits | Plan/Apply Pipeline — Build a Simple Plan and Apply Pipeline

> **Bite-sized how-to** | ~20 min setup

---

## What is Harness IaCM?

Infrastructure as Code Management (IaCM) is Harness's module for managing Terraform-based infrastructure. It connects your Terraform code in a Git repository to your cloud accounts through isolated **workspaces**, repeatable **pipelines**, and shared **connectors** — giving you state management, drift detection, cost estimation, and policy enforcement all in one place.

At the core of every IaCM workflow is the provision pipeline: **init → plan → apply**. Harness runs these as structured pipeline steps with full logs, approvals, and audit trails — so infrastructure changes are visible, reviewed, and repeatable.

**How a provision pipeline works:**

1. A developer or platform engineer triggers the pipeline.
2. The **init** step initializes the Terraform working directory and downloads providers.
3. The **plan** step runs `terraform plan` — showing exactly what will be created, changed, or destroyed.
4. An optional **approval** step pauses the pipeline for a human review before anything changes.
5. The **apply** step runs `terraform apply` — provisioning the actual infrastructure.
6. The workspace **Resources** tab shows all provisioned resources and outputs.

---

## What does this Tidbit demonstrate?

A complete Plan/Apply pipeline using Harness IaCM — **no cloud account needed**. This Tidbit uses the **Harness Terraform provider** to provision a Harness pipeline from within Harness itself.

1. **Set up connectors** — a GitHub connector for the Terraform code.
2. **Create a workspace** — link the connector, point to this repository, set Terraform version.
3. **Add workspace variables** — set Harness account ID, API key, org, project, and pipeline name.
4. **Import the pipeline** — load `.harness/pipeline.yaml` via Import from Git.
5. **Run the pipeline** — init runs, plan shows **1 resource to add**, approval gate pauses for review, apply provisions it.
6. **Verify** — "Provisioned by IaCM" appears in Deployments → Pipelines.

---

## How the Terraform provisions a Harness pipeline

The Terraform in this repository uses the `harness/harness` provider to create one resource — a Harness pipeline. Here is the core of `main.tf`:

```hcl
terraform {
  required_providers {
    harness = {
      source  = "harness/harness"
      version = "~> 0.30"
    }
  }
}

resource "harness_platform_pipeline" "demo_pipeline" {
  identifier = var.pipeline_identifier
  name       = var.pipeline_name
  org_id     = var.org_id
  project_id = var.project_id

  yaml = <<-EOT
    pipeline:
      name: ${var.pipeline_name}
      identifier: ${var.pipeline_identifier}
      stages:
        - stage:
            name: Hello Stage
            type: Custom
            spec:
              execution:
                steps:
                  - step:
                      type: ShellScript
                      name: Hello from IaCM
                      spec:
                        script: echo "This pipeline was provisioned by Harness IaCM using Terraform!"
  EOT
}
```

**What the plan step shows** — a diff of one resource to create:
```
# harness_platform_pipeline.demo_pipeline will be created
+ resource "harness_platform_pipeline" "demo_pipeline" {
    + identifier = "provisioned_by_iacm"
    + name       = "Provisioned by IaCM"
    ...
  }

Plan: 1 to add, 0 to change, 0 to destroy.
```

**What the apply step produces:**
```
pipeline_id   = "provisioned_by_iacm"
pipeline_name = "Provisioned by IaCM"
pipeline_url  = "https://app.harness.io/ng/account/.../pipelines/provisioned_by_iacm"
```

- `init`: Downloads the Harness provider and initializes the workspace backend
- `plan`: Shows the pipeline diff — nothing applied yet
- `apply`: Creates the pipeline in Deployments → Pipelines — visible immediately in the UI

---

## Prerequisites

Before you start, make sure you have:

- A Harness account with the IaCM module enabled
- A Harness API key with pipeline create/edit permissions
- A GitHub Personal Access Token with `repo` scope
- A Harness delegate running (for connector connectivity)

**Create a Harness API key:**
1. Go to your user profile in Harness
2. Go to the **API Keys** tab → **+ New API Key** → name it `iacm-terraform-key` → **Save**
3. Click **+ New Token** under the key → name it → **Generate**
4. Copy the token — you'll add it as a workspace secret variable

> See the [Harness API Key quickstart](https://developer.harness.io/harness-platform/use-harness-platform/automation/api/api-quickstart#create-a-harness-api-key-and-token) for a detailed walkthrough.

---

## Project Structure

```
iacm-tidbits-plan-apply-pipeline/
├── .harness/
│   └── pipeline.yaml    — IaCM provision pipeline (init → plan → approval → apply)
├── main.tf              — Harness provider + pipeline resource
├── variables.tf         — harness_account_id, harness_api_key, org_id, project_id, pipeline_name
├── outputs.tf           — pipeline_id, pipeline_name, pipeline_url
└── README.md
```

---

## Step 1 — Create the GitHub Connector

1. Go to **Project Settings → Connectors → + New Connector → GitHub**
2. Name: `iacm-github-connector`
3. Authentication: **Username and Token**
4. Enter your GitHub username and a Personal Access Token with `repo` scope
5. Connectivity Mode: **Connect through a Harness Platform**
6. Test the connection → Save

---

## Step 2 — Create the Workspace

1. Go to **Infrastructure → Workspaces → + New Workspace → Start from scratch**
2. Fill in:
   - **Name:** `iacm-plan-apply-demo`
   - **Git Connector:** `iacm-github-connector`
   - **Repository:** `harness-community/iacm-tidbits-plan-apply-pipeline`
   - **Branch:** `main`
   - **Folder Path:** *(leave blank)*
3. Under **Provisioner:**
   - **Workspace Type:** Terraform
   - **Terraform Version:** `1.5.7`

> **Note:** No cloud connector needed — the Harness provider authenticates via the API key set in workspace variables.

4. Click **Create**

---

## Step 3 — Add Workspace Variables

The Terraform configuration requires five variables. Set them in the workspace so Harness injects them into every pipeline run.

1. Open the workspace → **Variables** tab → **+ Add Variable**
2. Add the following:

| Variable | Value | Type | Secret? |
|---|---|---|---|
| `harness_account_id` | `<+account.identifier>` | Terraform | No |
| `harness_api_key` | Your API key token | Terraform | **Yes** |
| `org_id` | `<+org.identifier>` | Terraform | No |
| `project_id` | `<+project.identifier>` | Terraform | No |
| `pipeline_name` | `Provisioned by IaCM` | Terraform | No |

> **Tip:** Mark `harness_api_key` as a **Secret** variable so the token never appears in logs.
> `<+account.identifier>`, `<+org.identifier>`, and `<+project.identifier>` are built-in Harness expressions that resolve at runtime — no need to look up or hardcode any IDs.

---

## Step 4 — Import the Pipeline

1. Open `.harness/pipeline.yaml` on GitHub and update the one placeholder:
   - `YOUR_WORKSPACE_ID` → the identifier of the workspace you just created
   - Commit and push the change
2. Go to **Infrastructure → Pipelines → Import from Git**
3. Select `iacm-github-connector`, repo: `harness-community/iacm-tidbits-plan-apply-pipeline`, file: `.harness/pipeline.yaml`
4. Click **Import**

> **Note:** `projectIdentifier` and `orgIdentifier` in the pipeline YAML are automatically set by Harness during import based on the current project context — no need to update them manually.

---

## Step 5 — Run the Pipeline

1. Go to **Infrastructure → Pipelines → IaCM Plan Apply Pipeline → Run**
2. Watch the execution:
   - **init** — Terraform initializes, Harness provider downloads
   - **plan** — diff appears: 1 Harness pipeline to create
   - **Approve Apply** — pipeline pauses; review the plan and click **Approve**
   - **apply** — the new pipeline is created in your Harness project
3. After apply, go to **Deployments → Pipelines** — "Provisioned by IaCM" appears
4. Check the workspace **Resources** tab to see the managed resource and the output URL

---

## Common Issues & Tips

**init fails with provider download error**
- The delegate needs outbound internet access to reach `registry.terraform.io`. Verify network policies allow it.

**plan fails with authentication error**
- Double-check the `harness_api_key` workspace variable is set correctly and the token has pipeline create/edit permissions. Verify `harness_account_id` matches your actual account ID in Account Settings → Overview.

**apply fails with "pipeline already exists"**
- A pipeline with the same `pipeline_identifier` already exists in that project. Change the `pipeline_identifier` workspace variable to something unique (e.g. `provisioned_by_iacm_v2`).

**Terraform version constraint error**
- Harness IaCM supports Terraform up to v1.5.7 (MPL license). Set the workspace Terraform version to `1.5.7`. Terraform v1.6.0+ (BSL license) is not supported — use OpenTofu for newer versions.

---

## Resources

- [Harness IaCM Documentation](https://developer.harness.io/infrastructure-as-code-management)
- [Get Started with Terraform on IaCM](https://developer.harness.io/infrastructure-as-code-management/new-to-iacm/get-started/terraform-get-started)
- [Provision a Workspace](https://developer.harness.io/infrastructure-as-code-management/platform/workspaces/provision-workspace)
- [Harness Terraform Provider](https://developer.harness.io/docs/platform/resource-development/terraform/harness-terraform-provider/)
