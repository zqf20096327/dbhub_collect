# CD | Tidbits | Drift Detection

> **Bite-sized how-to** | ~15 min setup

---

## What is Drift Detection?

In most teams, staging and production are supposed to stay in sync — but they drift apart silently. A failed production deployment, a skipped approval, or a one-off hotfix can leave your environments running different artifact versions without anyone realising.

Harness CD surfaces this automatically. When a service is deployed across an **Environment Group**, the Services dashboard tracks the artifact version running in each environment and flags any mismatch as drift — right there on the service page, without digging through pipeline logs.

**How it works:**

1. You group related environments (e.g. Staging and Production) into an **Environment Group**.
2. You deploy the same service to both environments via a CD pipeline.
3. If the environments fall out of sync — different artifact versions, different last deployment times — Harness shows a **Drift Detected** warning on the service.
4. You remediate by re-deploying to bring the lagging environment back in line.

---

## What does this Tidbit demonstrate?

A full drift detection cycle using a Java Spring Boot e-commerce application deployed to Kubernetes:

1. **Baseline run** — deploy to both Staging and Production. Both environments are on the same artifact version.
2. **Create drift** — run the pipeline again, approve Staging, reject Production. Staging advances to a newer version; Production stays behind.
3. **Detect** — navigate to the Services dashboard. Harness shows the Drift Detected warning with a per-environment comparison table.
4. **Remediate** — run the pipeline again and approve both stages. Drift clears.

---

## Prerequisites

Before you start, make sure you have:

- A Harness project with CD enabled
- A Kubernetes cluster with a Harness Kubernetes connector configured
- A Docker Hub account and a Harness Docker Hub connector
- A GitHub connector pointing at this repo

---

## Project Structure

```
cd-tidbits-drift-detection/
├── .harness/
│   └── pipeline.yaml          — Full CI + CD pipeline (Build → Staging → Production)
├── k8s/
│   ├── deployment.yaml        — Kubernetes Deployment manifest
│   ├── service.yaml           — Kubernetes Service manifest
│   └── values.yaml            — Harness artifact expression for image injection
├── src/                       — Java Spring Boot application source code
├── Dockerfile                 — Two-stage Docker build
└── pom.xml                    — Maven build configuration
```

---

## Step 1 — Import the Pipeline

1. Open `.harness/pipeline.yaml` in this repository and update the placeholders at the top of the file:
   - `YOUR_PROJECT_ID` → your Harness project identifier
   - `YOUR_ORG_ID` → your Harness org identifier
   - Commit the changes
2. Go to **Deployments → Pipelines → Import from Git**
3. Select your GitHub connector, point it to this repository, and select `.harness/pipeline.yaml`
4. Hit **Import**
5. Once imported, open the Build stage → Build and Push step and update:
   - `YOUR_DOCKER_CONNECTOR` → your Docker Hub connector identifier
   - `YOUR_DOCKERHUB_USERNAME` → your Docker Hub username

---

## Step 2 — Set Up Service, Environment, and Infrastructure

**Service**
1. Go to **Deployments → Services → New Service**
2. Name: `appservice`, Deployment Type: **Kubernetes**
3. Add Manifest → K8s Manifest → point to the `k8s/` folder in this repo
4. Add Primary Artifact → Docker Registry → image: `<your-username>/harness-ecommerce-app-demo`

**Environments**
1. Create two environments: `Staging` (Pre-Production) and `production` (Production)
2. Add an Infrastructure Definition to each, pointing to your Kubernetes cluster and specifying the namespace:
   - Staging → namespace: `staging`
   - Production → namespace: `production`

---

## Step 3 — Create an Environment Group

1. Go to **Deployments → Environments → Environment Groups**
2. Click **New Environment Group**
3. Name it `ecommerce-environments`
4. Add both **Staging** and **Production** environments to the group
5. Save

The environment group is what tells Harness to track this service across both environments and surface drift when they fall out of sync.

---

## Step 4 — Establish a Baseline

Run the pipeline. When the approval steps appear, approve **both** Staging and Production.

Once the pipeline completes, both environments are running the same artifact version — this is your baseline.

---

## Step 5 — Create Drift

Run the pipeline again. This time:

- **Approve** the Staging approval step → Staging deploys successfully
- **Reject** the Production approval step → Production stays on the previous version

Staging is now ahead of Production. The environments have drifted.

---

## Step 6 — Detect Drift

1. Go to **Deployments → Services**
2. Click into your service (`harness-ecommerce-app-service`)
3. On the Summary tab you will see the **Environment Group card** for `ecommerce-environments`
4. Hover over the warning triangle on the artifact — the **Drift Detected** tooltip appears with a per-environment comparison table showing the last deployment time for Staging vs Production

---

## Step 7 — Remediate

Run the pipeline one more time and approve **both** approval steps.

Once Production is updated to the same artifact version as Staging, navigate back to the service — the drift warning is gone.

---

## Common Issues & Tips

**Drift Detected warning not appearing**
- Make sure both environments are added to the same Environment Group. Drift detection only works within an environment group.
- Check that at least two pipeline runs have completed — one to both environments, one to staging only.

**Pipeline not picking up the correct artifact tag**
- The `image_tag` pipeline variable is set to `<+pipeline.sequenceId>` by default. Make sure the Docker Hub image was pushed successfully in the Build stage before checking deployment tags.

**Namespace not found on first run**
- The Create Namespace shell script step handles this automatically. If it fails, verify that your Kubernetes connector has permissions to create namespaces.

---

## Resources

- [Monitor Deployments and Services in CD Dashboards](https://developer.harness.io/docs/continuous-delivery/monitor-deployments/monitor-cd-deployments/)
- [Environment Groups](https://developer.harness.io/docs/continuous-delivery/x-platform-cd-features/environments/create-environment-groups/)
- [Harness CD Pipeline YAML Reference](https://developer.harness.io/docs/platform/pipelines/harness-yaml-quickstart/)
