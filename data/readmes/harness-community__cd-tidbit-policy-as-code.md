# CD | Tidbits | Policy as Code

> **Bite-sized how-to** | ~10 min setup

---

## What is Policy as Code?

Harness Policy as Code lets you define governance rules as code using **Open Policy Agent (OPA)** and enforce them automatically across your pipelines. Instead of relying on teams to manually follow deployment standards, policies are evaluated at save or run time — and pipelines that violate them are blocked before they can cause problems.

**How it works:**

1. You write policies in **Rego** — OPA's policy language.
2. You group them into a **Policy Set** and attach it to pipelines.
3. Harness evaluates the policies whenever a pipeline is saved or run.
4. Any violation produces a clear error message and blocks the action.

---

## What does this Tidbit demonstrate?

Three real-world deployment governance policies applied to a Java Spring Boot e-commerce application:

**Policy 1 — Require Approval** — Every deployment stage must have a HarnessApproval or JiraApproval step before any deployment step runs. Prevents unreviewed changes from reaching any environment.

**Policy 2 — Block Latest Tag** — Deployment stages must not use `latest` as the image tag. Pinning to a specific version ensures deployments are reproducible and prevents unintended changes from being promoted silently.

**Policy 3 — Require Staging Before Production** — A production deployment stage must be preceded by a staging stage in the same pipeline. Ensures every change is validated in a lower environment before reaching production.

---

## Prerequisites

Before you start, make sure you have:

- A Harness CD pipeline with at least one Deployment stage
- A Kubernetes cluster with a Harness Kubernetes connector
- A Docker Hub account and a Harness Docker connector
- A GitHub connector pointing at this repo
- Harness Policy Engine enabled in your project

---

## Project Structure

```
cd-tidbits-policy-as-code/
├── .harness/
│   └── pipeline.yaml              — Full CI + CD pipeline (Build → Staging → Production)
├── ecommerce-app/                 — Java Spring Boot e-commerce application
│   ├── src/                       — Application and test source code
│   ├── Dockerfile                 — Two-stage Docker build
│   └── pom.xml                    — Maven build configuration
├── k8s/
│   ├── deployment.yaml            — Kubernetes Deployment manifest
│   ├── service.yaml               — Kubernetes Service manifest
│   └── namespace.yaml             — Kubernetes Namespace manifest
└── policies/
    ├── require-approval.rego          — Policy 1: Require approval before deployment
    ├── block-latest-tag.rego          — Policy 2: Block use of latest image tag
    └── require-staging-before-prod.rego — Policy 3: Require staging before production
```

---

## Step 1 — Import the Pipeline

1. Go to your Harness project → **Deployments → Pipelines → Import Pipeline**
2. Select your GitHub connector, point it to this repository, and select `.harness/pipeline.yaml`
3. Update the following placeholders in the YAML:
   - `<YOUR_PROJECT_ID>` — your Harness project identifier
   - `<YOUR_ORG_ID>` — your Harness org identifier
   - `<YOUR_DOCKER_CONNECTOR>` — your Docker Hub connector identifier
   - `<YOUR_DOCKERHUB_USERNAME>` — your Docker Hub username

---

## Step 2 — Set Up Service, Environment, and Infrastructure

**Service**
1. Go to **Deployments → Services → New Service**
2. Name: `harness-ecommerce-app`, Deployment Type: **Kubernetes**
3. Add Manifest → K8s Manifest → point to the `k8s/` folder in this repo
4. Add Primary Artifact → Docker Registry → image: `<your-username>/harness-ecommerce-app-demo`

**Environments**
1. Create two environments: `Staging` (Pre-Production) and `production` (Production)
2. Add an Infrastructure Definition to each pointing to your Kubernetes cluster

---

## Step 3 — Create the OPA Policies

Go to **Project Settings → Policies → New Policy** and create the following three policies.

**Policy 1 — Require Approval**

```rego
package pipeline

deny[msg] {
  stage := input.pipeline.stages[_].stage
  stage.type == "Deployment"
  not has_approval(stage)
  msg := sprintf(
    "Deployment stage '%s' is missing an approval step. Add a HarnessApproval or JiraApproval step before deploying.",
    [stage.name]
  )
}

has_approval(stage) {
  step := stage.spec.execution.steps[_].step
  step.type == "HarnessApproval"
}

has_approval(stage) {
  step := stage.spec.execution.steps[_].step
  step.type == "JiraApproval"
}
```

**Policy 2 — Block Latest Tag**

```rego
package pipeline

deny[msg] {
  stage := input.pipeline.stages[_].stage
  stage.type == "Deployment"
  tag := stage.spec.serviceConfig.serviceDefinition.spec.artifacts.primary.spec.tag
  tag == "latest"
  msg := sprintf(
    "Deployment stage '%s' uses the 'latest' image tag. Pin to a specific version tag.",
    [stage.name]
  )
}
```

**Policy 3 — Require Staging Before Production**

```rego
package pipeline

deny[msg] {
  stage := input.pipeline.stages[_].stage
  stage.type == "Deployment"
  is_production(stage)
  not has_staging_stage
  msg := sprintf(
    "Production stage '%s' requires a staging deployment stage to run first.",
    [stage.name]
  )
}

is_production(stage) {
  contains(lower(stage.name), "prod")
}

is_production(stage) {
  contains(lower(stage.spec.environment.environmentRef), "prod")
}

has_staging_stage {
  stage := input.pipeline.stages[_].stage
  stage.type == "Deployment"
  contains(lower(stage.name), "staging")
}

has_staging_stage {
  stage := input.pipeline.stages[_].stage
  stage.type == "Deployment"
  contains(lower(stage.spec.environment.environmentRef), "staging")
}
```

---

## Step 4 — Create a Policy Set

1. Go to **Project Settings → Policies → Policy Sets → New Policy Set**
2. Fill in:
   - **Name:** `CD Deployment Governance`
   - **Entity Type:** Pipeline
   - **Event:** On Save
3. Add all three policies with **Action: Error and exit**
4. Click **Save**

---

## Step 5 — Test the Policies

**Trigger a violation** — remove the approval step from the production stage and try to save the pipeline. You should see:

```
Policy Evaluation failed.
Deployment stage 'Deploy to Production' is missing an approval step.
Add a HarnessApproval or JiraApproval step before deploying.
```

**Fix the violation** — add the approval step back. All three policies should now pass and the pipeline saves successfully.

---

## Common Issues & Tips

**Policy evaluates but doesn't block**
- Check that the Policy Set action is set to **Error and exit**, not **Warn**.
- Confirm the Policy Set is applied to the correct entity type (Pipeline) and event (On Save or On Run).

**Rego policy not matching**
- Use the **Test Policy** button in the policy editor to paste in a sample pipeline YAML and verify the deny rule fires.
- Check field paths carefully — `input.pipeline.stages[_].stage` is the correct path for Harness pipeline stages.

**Approval step not detected**
- Make sure the step type is exactly `HarnessApproval` or `JiraApproval` — Rego matching is case-sensitive.

---

## Resources

- [Harness Policy as Code Overview](https://developer.harness.io/docs/platform/governance/policy-as-code/harness-governance-overview/)
- [OPA Rego Language Reference](https://www.openpolicyagent.org/docs/latest/policy-language/)
- [Harness Pipeline YAML Reference](https://developer.harness.io/docs/platform/pipelines/harness-yaml-quickstart/)
