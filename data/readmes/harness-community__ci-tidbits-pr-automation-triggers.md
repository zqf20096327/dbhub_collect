# Harness University Tidbit — PR Automation & Triggers

A bite-sized how-to on automating a Harness pipeline with **Git triggers**,
**branch targeting**, and **path-based filters**.

In this Tidbit you build one pipeline that provisions an **AWS S3 bucket** with
Terraform, and wire up two Git triggers so that:

| Git event | What fires | Terraform step that runs |
|---|---|---|
| **Open / update a PR → `main`** | PR trigger | `terraform plan` (preview only) |
| **Merge the PR (push → `main`)** | Push trigger | `terraform apply` (creates the bucket) |
| **Change a file outside `terraform/`** | *(nothing)* | Pipeline is skipped by the **path filter** |

This mirrors a real GitOps flow: reviewers see the plan on the PR, and
infrastructure is only mutated once the change is merged.

---

## What you'll learn

- Configure a **Pull Request** webhook trigger scoped to a target branch (`main`).
- Configure a **Push** webhook trigger that fires on merge.
- Use a **`changedFiles` path filter** so triggers only fire for changes under
  `terraform/` — a mono-repo best practice.
- Use **conditional execution** (`<+trigger.event>`) so a single pipeline runs
  `plan` on a PR and `apply` on a merge.

---

## Repository layout

```
.
├── terraform/                # ← changes HERE trigger the pipeline
│   ├── main.tf               #   S3 bucket + public-access block
│   ├── variables.tf          #   region + bucket name (edit bucket_name!)
│   └── outputs.tf
├── app/                      # ← the "other" dir; changes here are IGNORED
│   ├── notes.txt
│   └── README.md
└── .harness/
    ├── pr_automation_terraform_pipeline.yaml   # the pipeline
    ├── trigger_pr_to_main.yaml                 # PR trigger → plan
    └── trigger_merge_to_main.yaml              # push/merge trigger → apply
```

---

## Prerequisites

1. A **Harness** account with a project (Continuous Integration/Delivery module enabled).
2. A **GitHub connector** in Harness pointing at *your fork* of this repo, with
   API access enabled (needed for PR/push webhook triggers and the `changedFiles`
   condition).
3. An **AWS connector** or delegate credentials that let Terraform create an S3
   bucket. The Terraform steps inherit AWS credentials from your delegate /
   connector at runtime — **do not** hard-code keys in the YAML.
4. A Harness **Delegate** with Terraform available (or use the Harness-hosted
   infrastructure that ships Terraform).

---

## Setup

### 1. Fork and clone

Fork this repo into your own GitHub org so you can open PRs against it, then
create the Harness GitHub connector against your fork.

### 2. Edit the bucket name

S3 bucket names are **globally unique**. Open `terraform/variables.tf` and set
`bucket_name` to something unique to you:

```hcl
variable "bucket_name" {
  default = "my-unique-harness-tidbit-bucket-2026"
}
```

### 3. Import the pipeline

In Harness → **Pipelines → New Pipeline → Import from Git**, or paste the YAML
from `.harness/pr_automation_terraform_pipeline.yaml` into the YAML editor.

The YAML uses `<+input>` for the codebase/Git connector and `folderPath: terraform`.
Fill in your connector when prompted. Look for the commented lines
(`# repoName: <+input>`) — uncomment and set `repoName` if your GitHub connector
is account- or org-level rather than repo-level.

### 4. Create the two triggers

Add both triggers from `.harness/` (Pipeline Studio → **Triggers → New Trigger →
paste YAML**). Swap `<+input>` connector references for your GitHub connector.

- **`trigger_pr_to_main.yaml`** — event `Pull Request`, actions Open/Reopen/Synchronize,
  conditions `targetBranch == main` **AND** `changedFiles Regex ^terraform/.*`.
- **`trigger_merge_to_main.yaml`** — event `Push`, conditions `targetBranch == main`
  **AND** `changedFiles Regex ^terraform/.*`.

When you save a trigger, Harness registers the webhook in GitHub automatically.
If it doesn't, copy the webhook URL from the trigger list and add it manually in
GitHub → **Settings → Webhooks** (content type `application/json`).

---

## How the pipeline decides plan vs. apply

A single Custom stage holds both Terraform steps. Each step has a `when`
condition on the trigger event:

```yaml
# Terraform Plan
when:
  stageStatus: Success
  condition: <+trigger.event> == "PR"     # only on pull requests

# Terraform Apply
when:
  stageStatus: Success
  condition: <+trigger.event> == "PUSH"   # only on merge (push to main)
```

`<+trigger.event>` resolves to `PR` or `PUSH`, so the PR run previews the change
and the merge run applies it.

---

## Demo script (for the video)

1. **PR triggers plan.** Create a branch, tweak `terraform/main.tf` (e.g. add a
   tag), and open a PR to `main`. → The pipeline runs and executes **only the
   Terraform Plan** step. Show the plan output in the run.
2. **Merge triggers apply.** Merge the PR. → A new run starts from the push
   event and executes **only the Terraform Apply** step. The S3 bucket is
   created — show it in the AWS console.
3. **Path filter ignores other changes.** Edit `app/notes.txt`, open a PR. →
   **No pipeline run.** The `changedFiles` filter kept it from firing, because
   nothing under `terraform/` changed.

---

## Clean up

To avoid AWS charges, destroy the bucket when you're done (run a Terraform
Destroy step, or `terraform destroy` locally with the same variables).

---

## Notes

- No secrets are committed. AWS credentials come from your delegate/connector.
- `secretManagerRef: harnessSecretManager` uses the built-in Harness secret
  manager for the Terraform plan file — no setup required.
- GitHub PR actions include `Synchronize` so pushing new commits to an open PR
  re-runs the plan.
