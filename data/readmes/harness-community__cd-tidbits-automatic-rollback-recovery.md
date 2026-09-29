# CI/CD Tidbit — Automatic Rollback with Harness

Learn how to configure **Automatic Rollback & Recovery** for Kubernetes deployments using Harness Continuous Delivery.

In this hands-on tidbit, you'll start with a sample application in GitHub, connect it to Harness, configure the required Service and Environment, import a pipeline from Harness Configuration-as-Code, deploy a healthy version, intentionally introduce a deployment failure, and watch Harness automatically restore the previous successful release.

---

## What this skill accomplishes

Automatic Rollback helps protect deployments when a newly released version fails to reach a healthy state.

Harness continuously monitors the Kubernetes deployment during rollout. If the deployment fails, a configured **Stage Rollback** failure strategy can automatically execute the rollback steps and restore the previous successful release.

In this tidbit you will:

* Connect a GitHub repository to Harness.
* Build and push a Docker image using Harness CI.
* Configure a Harness Kubernetes Service and Environment.
* Deploy the application using a Kubernetes Rolling Deployment.
* Configure **Stage Rollback** for automatic recovery.
* Intentionally introduce a deployment failure.
* Observe Harness detecting the failed rollout.
* Automatically restore the previous healthy release.
* Verify the recovered application and Kubernetes deployment.

---

## What you will build

You will create a two-stage CI/CD pipeline.

### Build Stage

The Build stage:

1. Clones the application repository.
2. Builds the Docker image.
3. Pushes the image to Docker Hub.

### Deploy Stage

The Deploy stage:

1. Uses the Docker image produced by the Build stage.
2. Applies the Kubernetes manifests.
3. Performs a Kubernetes Rolling Deployment.
4. Monitors the deployment until it reaches a healthy state.
5. Automatically rolls back when the deployment fails.

The deployment uses:

* Kubernetes Deployment
* Kubernetes Service
* Docker Hub Artifact
* Harness Service
* Harness Environment
* Kubernetes Infrastructure
* Stage Rollback Failure Strategy
* Kubernetes Rolling Rollback

---

## Architecture

```text
                         GitHub Repository
                                |
                                v
                     +----------------------+
                     |      Harness CI      |
                     |                      |
                     | Clone → Build → Push |
                     +----------+-----------+
                                |
                                v
                         +-------------+
                         |  Docker Hub  |
                         | Docker Image |
                         +------+------+
                                |
                                v
                     +----------------------+
                     |      Harness CD      |
                     |                      |
                     | Kubernetes Rolling   |
                     |     Deployment       |
                     +----------+-----------+
                                |
                                v
                     +----------------------+
                     |   Healthy Release    |
                     |          ✅          |
                     +----------+-----------+
                                |
                         New Version
                                |
                                v
                     +----------------------+
                     | Deployment Failure   |
                     |          ❌          |
                     +----------+-----------+
                                |
                                v
                     +----------------------+
                     | Harness Detects      |
                     | Deployment Failure  |
                     +----------+-----------+
                                |
                                v
                     +----------------------+
                     |   Stage Rollback     |
                     +----------+-----------+
                                |
                                v
                     +----------------------+
                     | Kubernetes Rolling   |
                     |      Rollback        |
                     +----------+-----------+
                                |
                                v
                     +----------------------+
                     | Previous Healthy     |
                     | Release Restored ✅  |
                     +----------------------+
```

---

# Prerequisites

Before starting, make sure you have:

* A Harness account.
* A Harness project.
* A GitHub account and repository access.
* A GitHub connector in Harness.
* A Docker Hub account.
* A Docker Hub connector in Harness.
* A Kubernetes cluster.
* A Kubernetes connector/delegate.
* Permission to create Services, Environments, and Pipelines in the Harness project.

This example uses:

* **GitHub** — source code and Harness pipeline configuration.
* **Docker Hub** — container image registry.
* **Kubernetes** — deployment target.
* **Harness CI/CD** — build, deployment, health monitoring, and rollback.

---

# Repository Structure

```text
cd-tidbits-automatic-rollback-recovery/

├── app/
│   ├── Dockerfile
│   └── index.html
│
├── k8s/
│   ├── deployment.yaml
│   ├── namespace.yaml
│   └── service.yaml
│
├── .harness/
│   └── pipeline.yaml
│
└── README.md
```

### `app/`

Contains the sample application and Dockerfile used to build the container image.

### `k8s/`

Contains the Kubernetes resources required to deploy the application.

### `.harness/`

Contains the Harness pipeline configuration as code.

The pipeline YAML is included in the repository so the complete pipeline can be imported and reproduced instead of being created manually from scratch.

---

# Step 1 — Clone the Repository

Clone the repository locally:

```bash
git clone https://github.com/harness-community/cd-tidbits-automatic-rollback-recovery.git

cd cd-tidbits-automatic-rollback-recovery
```

You can also fork the repository into your own GitHub account and work from your fork.

---

# Step 2 — Configure Harness Connectors

Before importing the pipeline, configure the required connectors in your Harness project.

Navigate to:

```text
Harness
  → Project Settings
  → Connectors
```

Create and test the following connectors:

### GitHub Connector

Used to:

* Clone the application repository.
* Read the Kubernetes manifests.
* Read the Harness pipeline configuration.

Select **Test Connection** and verify that the connector is healthy.

### Docker Hub Connector

Used to:

* Build and push the Docker image.
* Retrieve the image during deployment.

Verify the connector using **Test Connection**.

### Kubernetes Connector / Delegate

Used by Harness to communicate with the Kubernetes cluster and execute the deployment.

Verify that the Kubernetes Delegate is running and available.

---

# Step 3 — Configure the Harness Service

The Harness Service defines **what is being deployed**.

Navigate to:

```text
Project
  → Services
  → New Service
```

Create a Service named:

```text
rollback-demo
```

Select:

```text
Deployment Type: Kubernetes
```

Configure the Kubernetes manifests to use the GitHub repository.

Set the manifest path to:

```text
k8s
```

The Service should reference the Kubernetes manifests from this repository.

---

## Configure the Artifact

Inside the `rollback-demo` Service, configure the primary artifact source.

Use:

```text
Artifact Type: Docker Registry
```

Configure the Docker Hub connector and repository used by the Build stage.

For this example, the Docker image repository is:

```text
pes2ug19cs219/harness-rollback
```

If you fork this repository or use your own Docker Hub account, replace this with your own image repository.

---

# Step 4 — Configure the Harness Environment

The Environment defines **where the application is deployed**.

Navigate to:

```text
Project
  → Environments
  → New Environment
```

Create an environment named:

```text
dev
```

Add a Kubernetes infrastructure definition.

Configure it to point to your Kubernetes cluster.

Select the appropriate Kubernetes connector/delegate.

Your final structure should look similar to:

```text
Environment
└── dev
    └── Kubernetes Infrastructure
        └── Kubernetes Cluster
```

---

# Step 5 — Import the Harness Pipeline

The complete Harness pipeline is included in:

```text
.harness/pipeline.yaml
```

This is the Configuration-as-Code version of the pipeline used in the demonstration.

Instead of manually rebuilding the pipeline, import this YAML into Harness.

Navigate to:

```text
Project
  → Pipelines
  → Create Pipeline
  → Import From Git
```

Select your GitHub connector.

Point it to:

```text
cd-tidbits-automatic-rollback-recovery
```

Select the branch:

```text
main
```

Set the pipeline YAML path to:

```text
.harness/pipeline.yaml
```

Import the pipeline.

---

# Step 6 — Update Environment-Specific Values

After importing the pipeline, review the YAML and update any values that are specific to your Harness account.

Typical values that may need to be changed include:

```text
organization identifier
project identifier
GitHub connector reference
Docker Hub connector reference
GitHub repository
Docker image repository
Kubernetes infrastructure
```

Make sure the Service referenced by the pipeline is:

```text
rollback-demo
```

And the Environment is:

```text
dev
```

Save the pipeline after making the required changes.

---

# Step 7 — Understand the Pipeline

The pipeline contains two stages.

```text
Build
  |
  v
Deploy
```

### Build

The Build stage:

```text
Clone Repository
        |
        v
Build Docker Image
        |
        v
Push Image to Docker Hub
```

### Deploy

The Deploy stage:

```text
Select Artifact
        |
        v
Kubernetes Rolling Deployment
        |
        v
Wait for Healthy State
```

The Deploy stage also contains the rollback configuration.

---

# Step 8 — Configure Automatic Rollback

Open the Deploy stage.

Navigate to:

```text
Deploy
  → Failure Strategy
```

Configure:

```text
Failure Type: All Errors
Action: Stage Rollback
```

The stage rollback uses the Kubernetes Rolling Rollback step to restore the previous successful deployment.

The resulting flow is:

```text
Deployment Failure
        |
        v
Stage Rollback
        |
        v
Kubernetes Rolling Rollback
        |
        v
Previous Release Restored
```

---

# Step 9 — Deploy the First Healthy Version

Run the pipeline for the first time.

The expected flow is:

```text
Build
  ↓
Docker Image Created
  ↓
Image Pushed to Docker Hub
  ↓
Deploy
  ↓
Kubernetes Rolling Deployment
  ↓
Healthy Application
```

The pipeline should complete successfully.

---

# Step 10 — Verify the Healthy Deployment

Verify the Kubernetes pods:

```bash
kubectl get pods -n rollback-demo
```

Check the ReplicaSets:

```bash
kubectl get rs -n rollback-demo
```

Check the deployment history:

```bash
kubectl rollout history deployment rollback-demo -n rollback-demo
```

The application should be running successfully.

If using the local Kubernetes setup from the demo, you can access it using:

```bash
kubectl port-forward svc/rollback-demo 8080:80 -n rollback-demo
```

Then open:

```text
http://localhost:8080
```

---

# Step 11 — Introduce a Deployment Failure

Now we'll intentionally break the next deployment.

For example, modify the Kubernetes deployment so the container cannot start successfully.

One example is an invalid container command:

```yaml
command:
  - /bin/does-not-exist
```

Commit and push the change:

```bash
git add .

git commit -m "Introduce deployment failure for rollback demo"

git push
```

Run the Harness pipeline again.

---

# Step 12 — Observe the Failed Deployment

During the deployment, Harness will:

1. Build the new Docker image.
2. Push the image to Docker Hub.
3. Start the Kubernetes Rolling Deployment.
4. Monitor the new pods.
5. Wait for the deployment to reach a healthy state.

Because the new version contains an intentional failure, the new pods will not become healthy.

The deployment eventually fails.

---

# Step 13 — Observe Automatic Rollback

Because the Deploy stage is configured with:

```text
Stage Rollback
```

Harness automatically starts the rollback process.

The execution flow becomes:

```text
Rolling Deployment
        |
        v
New Version Fails
        |
        v
Harness Detects Failure
        |
        v
Stage Rollback
        |
        v
Kubernetes Rolling Rollback
        |
        v
Previous Version Restored
```

No manual `kubectl rollout undo` command is required.

---

# Step 14 — Verify the Rollback

Check the pods:

```bash
kubectl get pods -n rollback-demo
```

Check the ReplicaSets:

```bash
kubectl get rs -n rollback-demo
```

Check deployment history:

```bash
kubectl rollout history deployment rollback-demo -n rollback-demo
```

You should see the previous healthy deployment restored.

Verify the deployment status:

```bash
kubectl rollout status deployment rollback-demo -n rollback-demo
```

Finally, verify the application:

```bash
kubectl port-forward svc/rollback-demo 8080:80 -n rollback-demo
```

Open:

```text
http://localhost:8080
```

The application should be available again.

---

# Expected Result

The complete workflow should look like:

```text
Build
  ✅
   |
   v
Deploy Healthy Version
  ✅
   |
   v
Introduce Bad Version
   |
   v
Rolling Deployment
  ❌
   |
   v
Harness Detects Failure
   |
   v
Stage Rollback
  🔄
   |
   v
Previous Version Restored
  ✅
```

---

# Try It Yourself

After completing the main demonstration, try introducing different failure scenarios.

### Invalid Container Command

```yaml
command:
  - /bin/does-not-exist
```

### Invalid Image

Use an image that does not exist or cannot be pulled.

### Readiness Probe Failure

Configure a readiness probe to check an endpoint that does not exist.

### Application Startup Failure

Introduce an application configuration or startup error.

For each scenario, observe how Harness handles the failed rollout and executes the configured rollback.

---

# Troubleshooting

## Pipeline Cannot Find the Pipeline YAML

Verify:

```text
.harness/pipeline.yaml
```

exists in the selected branch and that the GitHub connector has access to the repository.

---

## Connector Not Found

Verify the connector references in the imported pipeline match the connectors created in your Harness project.

---

## Image Cannot Be Found

Verify:

* Docker Hub repository name.
* Docker Hub connector.
* Image tag.
* Repository permissions.

---

## Deployment Does Not Become Healthy

Check:

```bash
kubectl get pods -n rollback-demo

kubectl describe deployment rollback-demo -n rollback-demo

kubectl describe pods -n rollback-demo

kubectl get events -n rollback-demo
```

Pay particular attention to:

* Readiness probes.
* Image pull errors.
* Container startup errors.
* Kubernetes resource availability.

---

## Rollback Does Not Execute

Verify:

* The Deploy stage has a **Stage Rollback** failure strategy.
* A Kubernetes Rolling Rollback step is configured.
* A previous successful deployment exists.
* Kubernetes has multiple deployment revisions.

Check:

```bash
kubectl rollout history deployment rollback-demo -n rollback-demo
```

---

# What This Tidbit Intentionally Does NOT Cover

This tidbit focuses specifically on **Automatic Rollback & Recovery**.

It does not cover:

* Blue-Green Deployments
* Canary Deployments
* Progressive Delivery
* Traffic Shifting
* Approval Gates
* GitOps
* Continuous Verification
* Production deployment strategies

---

# Configuration-as-Code

The Harness pipeline used in this demonstration is available in:

```text
.harness/pipeline.yaml
```

This allows you to:

* Review the complete pipeline definition.
* Import the pipeline into your own Harness project.
* Version-control pipeline changes.
* Reproduce the demonstration without manually rebuilding the pipeline.

The pipeline includes the Build stage, Deploy stage, artifact configuration, Kubernetes Rolling Deployment, and rollback configuration.

---

# Reference

* [Harness Continuous Delivery Documentation](https://developer.harness.io/docs/continuous-delivery/)
* [Harness Kubernetes CD Quickstart](https://developer.harness.io/docs/continuous-delivery/deploy-srv-diff-platforms/kubernetes/kubernetes-cd-quickstart/)
* [Harness Failure Strategies](https://developer.harness.io/docs/platform/pipelines/failure-handling/define-a-failure-strategy-on-stages-and-steps/)
* [Harness Kubernetes Rolling Deployments](https://developer.harness.io/docs/continuous-delivery/deploy-srv-diff-platforms/kubernetes/kubernetes-rolling-deploy/)
* [Harness Kubernetes Rollback](https://developer.harness.io/docs/continuous-delivery/deploy-srv-diff-platforms/kubernetes/kubernetes-rollback/)
* [Kubernetes Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)

---

## Repository

**GitHub:**
https://github.com/harness-community/cd-tidbits-automatic-rollback-recovery
