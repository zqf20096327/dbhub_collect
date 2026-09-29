# SCS | Tidbits | Multi-Artifact Governance

> **Bite-sized how-to** | ~30 min setup


## What is Multi-Artifact Governance?

Modern software ships as multiple artifact types — a container image for runtime and a JAR file for shared libraries. Governing only one means blind spots in the other.

Harness SCS (Supply Chain Security) lets you apply the same SBOM-based policies to both container and non-container artifacts in a single pipeline. The policy evaluates every component in each artifact's SBOM and flags violations — giving you complete coverage regardless of artifact type.


## What does this Tidbit demonstrate?

A two-stage CI pipeline that governs both artifact types:

1. **Build and Generate SBOM** — builds the Spring Boot JAR, builds and pushes the Docker image, generates an SBOM for the Docker image (cdxgen), and ingests the pre-generated CycloneDX SBOM for the Maven JAR
2. **Enforce SBOM Policies** — applies the same policy set to both artifacts and surfaces violations


## Key Concepts

**SBOM (Software Bill of Materials)** — an inventory of all components, libraries, and dependencies in an artifact. Harness SCS uses SBOMs as the basis for policy evaluation.

**SscaOrchestration step** — generates or ingests an SBOM for an artifact. Supports two modes:
- **Generation mode** — Harness generates the SBOM automatically using cdxgen or Syft (for container images)
- **Ingestion mode** — you supply a pre-generated SBOM file (required for non-container artifacts like JARs)

**SscaEnforcement step** — evaluates the artifact's SBOM against a policy set and reports violations.

**Policy Set** — a collection of OPA-based policies attached to an entity type (SBOM). Each policy defines allow/deny rules based on component name, version, license, supplier, or purl.

**CycloneDX Maven Plugin** — generates a CycloneDX SBOM (`bom.json`) during `mvn package`. Used to produce the SBOM for the non-container Maven JAR artifact.


## Prerequisites

Before you start, make sure you have:

- A Harness account with the SCS module enabled
- A Harness CI pipeline with a build infrastructure — Harness Cloud or a Kubernetes cluster with a Harness delegate
- A Docker Hub connector configured in Harness
- A GitHub connector pointing to this repository


## Step 0 — Set Up Connectors

Connectors are how Harness communicates with external systems. Before running the pipeline, configure two connectors in **Project Settings → Connectors → + New Connector**:

**GitHub Connector**
- Select **GitHub** as the connector type
- Enter your GitHub repository URL and credentials (personal access token or OAuth)
- Test the connection
- Note the **connector identifier** — you will need it for the pipeline YAML

**Docker Hub Connector**
- Select **Docker Registry** as the connector type
- Provider: Docker Hub
- Enter your Docker Hub username and access token
- Test the connection
- Note the **connector identifier** — you will need it for the pipeline YAML

> **Note:** The Docker Hub connector serves two purposes in this pipeline — it pulls container images used in pipeline steps (e.g., the Maven build image) and it pushes the built Docker image to your registry.


## Project Structure

```
scs-tidbits-multi-artifact-governance/
├── .harness/
│   └── pipeline.yaml                    — CI pipeline (Build + SBOM + Enforce)
├── src/
│   └── main/java/com/harness/ecommerce/
│       ├── EcommerceApplication.java
│       └── HealthController.java
├── pom.xml                              — Maven build with CycloneDX plugin
└── Dockerfile                           — Two-stage Docker build
```


## Step 1 — Create an SBOM Policy

1. Go to **Project Settings → Security and Governance → Policies → + New Policy**
2. Name: `block-high-risk-licenses`
3. In the Rego editor, use the Harness sample library — search **SBOM** and select a sample
4. Modify the deny list rules as needed (name, version, license conditions)
5. Save the policy

> **Note:** The policy package must be `package sbom` — not `package main`. Using the Harness sample library ensures the correct structure automatically.


## Step 2 — Create a Policy Set

1. Go to **Project Settings → Security and Governance → Policies → Policy Sets → + New Policy Set**
2. Name: `multi-artifact-policy-set`
3. **Entity Type:** SBOM
4. **Event:** On Step
5. Click **+ Add Policy** → select `block-high-risk-licenses` → set severity to **Error and exit**
6. Save and note the **Policy Set identifier**
7. Toggle the policy set to **Enforced: Yes**


## Step 3 — Update the Pipeline Placeholders

Open `.harness/pipeline.yaml` and replace:

| Placeholder | Value |
|---|---|
| `YOUR_PROJECT_ID` | Your Harness project identifier |
| `YOUR_ORG_ID` | Your Harness org identifier |
| `YOUR_DOCKERHUB_CONNECTOR` | Your Docker Hub connector identifier |
| `YOUR_DOCKERHUB_USERNAME` | Your Docker Hub username |
| `YOUR_POLICY_SET_ID` | The policy set identifier from Step 2 |

Commit and push.


## Step 4 — Import and Run the Pipeline

1. Go to **Pipelines → Import From Git** → select your GitHub connector → import `.harness/pipeline.yaml`
2. Click **Run Pipeline** → set branch to `main` → Run


## Pipeline Walkthrough

The pipeline has two stages. **Stage 1** builds the artifacts and generates SBOMs for both. **Stage 2** enforces the governance policy against both artifact types. The sections below walk through what each step does and why.


## Stage 1: Build and Generate SBOM

This stage is responsible for building the artifacts and getting their SBOMs into Harness SCS. It has four steps — the first two build the artifacts, and the last two handle SBOM generation and ingestion for each artifact type.

**Step 1 — Maven Build and Generate SBOM (Run step)**
Runs `mvn package` using the `maven:3.9-eclipse-temurin-17` container. The CycloneDX Maven plugin generates a CycloneDX SBOM at `/harness/target/bom.json` with all 41 compile-time dependencies.

**Step 2 — Build and Push Docker Image**
Builds the Docker image from the Dockerfile and pushes to Docker Hub tagged with `latest` and the pipeline sequence ID.

**Step 3 — Generate SBOM - Docker Image (SscaOrchestration, generation mode)**
Harness uses cdxgen to scan the Docker image and generate an SBOM automatically. The SBOM is stored in Harness SCS and scored.

**Step 4 — Ingest SBOM - Maven JAR (SscaOrchestration, ingestion mode)**
Harness ingests the pre-generated `bom.json` from the Maven build. The `artifactFile` field identifies the JAR as a distinct non-container artifact. SBOM drift is detected by comparing against the last ingested SBOM.

> **Why ingestion mode for JAR?** SBOM auto-generation is only supported for container images. For non-container artifacts (JARs, Helm charts, YAML manifests), you must generate the SBOM externally and ingest it. The CycloneDX Maven plugin handles this during the Maven build.


## Stage 2: Enforce SBOM Policies

**Step 1 — Enforce Policy - Docker Image (SscaEnforcement)**
Evaluates the Docker image SBOM against the policy set. Violations are recorded and visible in **SCS → Artifacts → Policy Violations**.

**Step 2 — Enforce Policy - Maven JAR (SscaEnforcement)**
Evaluates the Maven JAR SBOM against the same policy set. Both artifacts share the same governance rules.

Both steps use a `failureStrategies: Ignore` so the pipeline completes even when violations are found — allowing you to see violations for both artifacts in the same run.


## Viewing Policy Violations

After the pipeline runs:

1. Go to **Supply Chain Security → Artifacts → YOUR_DOCKERHUB_USERNAME/scs-ecommerce-app**
2. Click on the build tag to open the artifact overview
3. The **Overview** tab shows the SBOM Violations summary — Allow list violations and Deny list violations
4. On the right side, the **Chain of Custody** section shows the full event history:
   - **SBOM generated** — for both the Docker image and Maven JAR
   - **SBOM policy enforcement - failed** — click **View violations** to see the full list of components that violated the policy rules including component name, ecosystem, license, and the specific rule violated


## Resources

- [Generate SBOM for Artifacts](https://developer.harness.io/docs/software-supply-chain-assurance/open-source-management/generate-sbom-for-artifacts/)
- [Ingest SBOM for Non-Container Artifacts](https://developer.harness.io/docs/software-supply-chain-assurance/open-source-management/ingest-sbom-data/)
- [Create SBOM Policies](https://developer.harness.io/docs/software-supply-chain-assurance/open-source-management/create-sbom-policies/)
- [Enforce SBOM Policies](https://developer.harness.io/docs/software-supply-chain-assurance/open-source-management/enforce-sbom-policies/)
