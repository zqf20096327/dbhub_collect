# CI Tidbit — Governance Policies with OPA (Policy as Code)

Enforce CI guardrails centrally with **Harness Policy as Code**: write an OPA
**Rego** policy, group it into a **Policy Set**, bind that set to the **Pipeline**
entity on the **On Save** event, and Harness will evaluate every pipeline save
*before it can be stored*. This tidbit teaches one atomic skill: **apply an OPA
policy that (1) requires a mandatory security/scan step and (2) blocks a risky
`curl … | sh` command**, then watch a compliant pipeline save successfully and a
violating pipeline get blocked at save time.

> This is the **CI** governance tidbit. A separate CD tidbit covers governance
> for deploy stages (approval gates). Here the rules are CI-specific: scan steps
> and risky shell commands.

---

## What you'll learn

- The Policy as Code model: **Policy** (one Rego rule) → **Policy Set** (group +
  entity + event + severity) → **enforcement** (On Save / On Run).
- How to write a Rego `deny` rule against the expanded **pipeline** payload.
- How a Policy Set on **On Save / Error and exit** blocks a non-compliant pipeline before it can be saved.
- Where to read the **policy evaluation** result for any run.

## How it works

```
 Pipeline saved in Harness UI
          │
          ▼
 Harness OPA server evaluates Policy Set "CI Governance"  ◄── policies/ci_governance.rego
          │
   ┌──────┴───────┐
 PASS            DENY (severity = Error)
   │               │
 Save succeeds  Save rejected, pipeline cannot be stored
 (runs normally) (Policy Set Evaluations panel shows why)
```

The policy receives the full pipeline YAML as JSON under `input.pipeline`. Two
independent `deny` rules (see [`policies/ci_governance.rego`](policies/ci_governance.rego)):

1. **Mandatory scan** — every CI stage must have a step whose name/identifier
   contains `scan` or `security`.
2. **Block risky commands** — no `Run` step may pipe a remote script into a
   shell (`curl … | sh`, `wget … | bash`).

## Repo contents

| Path | Purpose |
|------|---------|
| `policies/ci_governance.rego` | OPA/Rego policy source — copy the entire file into Harness to create a Policy |
| `.harness/governance_pipeline_success.yaml` | **Compliant** pipeline — satisfies both rules, runs to Success |
| `.harness/governance_pipeline_violation.yaml` | **Violating** pipeline — breaks both rules, rejected at run time (no steps execute) |

## Prerequisites

- A Harness account with **Policy as Code / Governance** enabled (Enterprise tier; not available on Free).
- Permissions: ability to create **Policies** and **Policy Sets** at your chosen scope (Account / Org / Project).
- Your **Project ID** and **Org ID** (found in Project/Org Settings in Harness).
- Infrastructure: No Kubernetes, delegate, or STO license needed — this runs on **Harness Cloud** (managed runners).
- Harness terminology: New to Harness? **Scope** = Account (global) / Org (organization) / Project (team's work container).

## Step-by-step

### 1. Fork / clone this repo

Clone or fork this repo to your GitHub account (you'll need to push it to import pipelines into Harness later).

```bash
git clone https://github.com/harness-community/ci-tidbits-governance-opa
cd ci-tidbits-governance-opa
```

### 2. Update the pipeline YAMLs with your Harness details

Both pipeline YAML files need your organization and project IDs. Open them and replace the marked lines:

**File: `.harness/governance_pipeline_success.yaml`**
- Line 4: `projectIdentifier: <+project.identifier>` → your actual project ID (e.g., `my_project`)
- Line 5: `orgIdentifier: <+org.identifier>` → your actual org ID (e.g., `my_org`)

**File: `.harness/governance_pipeline_violation.yaml`**
- Line 4: `projectIdentifier: <+project.identifier>` → your actual project ID (same as success pipeline)
- Line 5: `orgIdentifier: <+org.identifier>` → your actual org ID (same as success pipeline)


### 3. Create the Policy in Harness

In Harness UI: **Account Settings** (or Org/Project Settings) → **Security and Governance** → **Policies** → **+ New Policy**.

- **Policy Name**: `Tidbit CI Governance OPA`
- **Policy Type**: `Inline`
- **Paste entire contents** of [`policies/ci_governance.rego`](policies/ci_governance.rego) into the editor
- **Save**

**Important:** Do NOT change the first line `package pipeline` — Harness requires this exact package name to route policy evaluations correctly.

### 4. Create and enforce the Policy Set

Back on the **Security and Governance** page → **Policy Sets** tab → **+ New Policy Set**.

- **Policy Set Name**: `Tidbit CI Governance OPA Set`
- **Entity Type**: `Pipeline` (what does this policy apply to?)
- **Deployment Type**: `All` (keep default)
- **Event**: `On Save` (evaluate the policy when a pipeline is saved; violations are caught at edit time before anyone can run the pipeline)
- **Continue** → **+ Add Policy** → select your policy (`Tidbit CI Governance OPA`) → Severity: **Error and exit** → **Apply** → **Finish**
- Back in the Policy Sets list, confirm the **Enforced** toggle is **ON** (blue)

**Scope note:** This Policy Set applies to **all** pipelines of type `Pipeline` in your scope. If you create it at **Project** level, it only affects that project's pipelines. Recommended for first tests.

### 5. Import and save the compliant pipeline

In Harness: **Pipelines** → **+ New** → **+ Import from YAML**.

- Copy the full contents of `.harness/governance_pipeline_success.yaml`
- Paste into the editor → **Import / Save**
- Expected outcome on save:
  - ✓ **Policy Evaluations** tab shows **PASSED** (both rules satisfied)
  - ✓ Pipeline is saved successfully
  - ✓ Run it — all steps execute: Install dependencies → Security scan → Success
  - ✓ The scan runs `pip-audit` on the sample dependency list

### 6. Import and save the violation pipeline (the guardrail test)

In Harness: **Pipelines** → **+ New** → **+ Import from YAML**.

- Copy the full contents of `.harness/governance_pipeline_violation.yaml`
- Paste into the editor → attempt to **Import / Save**
- **Expected outcome (this is the teaching moment):**
  - ✗ Save is **rejected immediately** (status: Policy Violation)
  - ✗ **Policy Set Evaluations** panel displays both deny messages:
    ```
    CI stage 'risky_build' must contain a security/scan step
      (identifier or name containing 'scan' or 'security').
    Run step 'risky_install' contains a risky 'pipe remote script to shell'
      command (e.g. curl | sh). Blocked by CI governance policy.
    ```
  - ✗ **Pipeline cannot be saved** — the policy blocks it before it ever reaches a runner.

**Fix the violation:** Remove the `curl | sh` command from the YAML, add a scan step named "security_scan", and try to save again — it will now pass.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| **"Policy as Code" not visible in Harness** | Not on Enterprise tier or no Governance permission | Use an account with Policy as Code licensed and assigned to you |
| **Compliant pipeline gets blocked anyway** | Scan step name doesn't contain "scan" or "security" | Rename the step or its identifier to include one of those keywords. Rule is exact: check the YAML identifier field. |
| **Violating pipeline saves successfully (shouldn't)** | Policy Set not enforced or wrong severity | Check: (1) Policy Set **Enforced** toggle is ON, (2) Severity is **Error and exit** (not Warn), (3) Event is **On Save** |
| **Org / project identifier errors on import** | YAML has placeholder IDs like `<+project.identifier>` | Replace with actual IDs. Find them: **Project Settings** (bottom-left) → Identifier; or **Org Settings** → Identifier |
| **Policy evaluation not shown on save** | Policy Set not attached to your project's Pipeline entity | Verify: **Security and Governance** → **Policy Sets** → your set → **Enforced** ON and Event is **On Save**. Try scope: Project level first, not Account. |

## Make it stricter (optional)

- Add `On Run` to the Policy Set as well for defence in depth — violations are
  caught both at save time and at run time.
- Extend Rule 2 to block other patterns (e.g. `chmod 777`, hardcoded secrets,
  `latest` image tags).
- Require a *specific* native scan step type (e.g. an STO `Aqua`/`Snyk` step)
  instead of a name match, if you have the STO module.
