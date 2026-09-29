# SCS Tidbit — Basic SBOM Generation from a Repository (CycloneDX & SPDX)

> **Harness University Tidbit.** A 5–10 minute, self-paced micro-lesson backed by an executable repo.
> **Skill:** Add an **SSCA Orchestration** step to a CI pipeline to automatically generate a Software Bill of Materials (SBOM) directly from your **source code repository** in either CycloneDX or SPDX format — with zero extra tooling to install.

---

## What this skill accomplishes

An SBOM is an ingredient list for your software: every open-source library, version, and license your repository contains. Scanning the source repo (instead of a built image) lets you catch dependency risks earlier — before a container is even built — and works for any language or project that lacks a Dockerfile.

The **SCS SSCA Orchestration** step generates the SBOM automatically after your code is checked out. Harness:

1. Runs **cdxgen** to scan the repository's `package.json` manifest
2. Produces a signed SBOM in CycloneDX-JSON or SPDX-JSON format
3. Stores the SBOM in the Harness platform (downloadable from Execution details)
4. Tracks **SBOM Drift** — components added, removed, or version-bumped vs. a base branch

---

## How it works

```
Pipeline: scs_basic_sbom
└── Stage: Generate SBOM from Repository (CI)
    └── Step: SscaOrchestration
        ├── Mode:        Generation
        ├── Tool:        cdxgen
        ├── Format:      CycloneDX-JSON
        ├── Artifact:    Repository (cloned_codebase: /harness)
        └── SBOM Drift:  compare against main branch
```

cdxgen walks the checked-out workspace, detects `package.json`, and produces a complete SBOM covering all declared npm dependencies.

---

## Sample application

This repo includes a `sample-app/` directory — a minimal Node.js app — so you have something meaningful to scan right away:

```
sample-app/
  package.json       # Node.js deps: express, axios, lodash, uuid, dotenv
  index.js           # Simple Express API
```

cdxgen detects the `package.json` manifest and includes all declared packages in the SBOM.

---

## SBOM format comparison

| Factor | SPDX | CycloneDX |
|--------|------|-----------|
| Maintainer | Linux Foundation | OWASP |
| Best for | License compliance, IP audits | Security scanning, vulnerability tracking |
| Vulnerability support | Relies on external tools | Native VEX, hashing, dependency trees |
| Formats | JSON, XML, YAML, RDF, Tag/Value | JSON, XML, protobuf |
| Choose when | Legal team needs detailed license data | Security team needs CVE correlation |

**This tidbit uses CycloneDX** — the better choice when you want to cross-reference your SBOM with vulnerability databases (NVD, OSV).

---

## Repo layout

```
.harness/
  pipeline.yaml     # CI pipeline with SscaOrchestration step
sample-app/
  package.json      # Node.js manifest (what cdxgen scans)
  index.js          # Sample Express app
.gitignore
README.md
```

---

## Prerequisites

1. **Harness account** with **Supply Chain Security (SCS)** module enabled.
2. **Harness Cloud** build infrastructure (used in this pipeline).
3. A **Git connector** pointing to this repository.

> No registry connector needed — this pipeline does not build or push a Docker image.

---

## Step 1 — Understand the SscaOrchestration step fields

| Field | Value | Why |
|-------|-------|-----|
| **mode** | `generation` | Generate a new SBOM (vs. `ingestion` for pre-existing SBOMs) |
| **tool.type** | `cdxgen` | Best choice for artifact (repository) scanning; understands package manifests natively |
| **tool.spec.format** | `cyclonedx-json` | Security-focused format; swap to `spdx-json` if needed |
| **source.type** | `repository` | Artifact type: scanning a repository, not a container image |
| **source.spec.url** | Your GitHub repo URL | URL of the artifact (repository) cdxgen fetches and scans |
| **source.spec.variant** | `main` | Branch of the artifact to scan |
| **source.spec.cloned_codebase** | `/harness` | Local path where the artifact is cloned — no change needed |
| **sbom_drift.spec.variant** | `main` | Base branch to compare against for drift detection |
| **resources.limits** | 500Mi / 0.5 CPU | Prevents the cdxgen container from being OOM-killed on large repos |

---

## Step 2 — Import the pipeline

1. Go to **Software Supply Chain Assurance → Pipelines** (or **Continuous Integration → Pipelines**)
2. Click **Create a Pipeline → Import from YAML**
3. Paste the contents of `.harness/pipeline.yaml`
4. Replace the `# REPLACE:` placeholders:
   - `orgIdentifier` — your Harness org identifier
   - `projectIdentifier` — your Harness project identifier
   - `connectorRef` — your Git connector (e.g. `account.github_connector`)
   - `repoName` — your repository name (e.g. `my-org/my-repo`)
   - `source.spec.url` — URL of the artifact (your GitHub repo)
   - `source.spec.variant` — artifact branch to scan (default: `main`)
   - `sbom_drift.spec.variant` — base branch for drift comparison (default: `main`)
5. **Save**

---

## Step 3 — Run and view the SBOM

1. Click **Run → Run Pipeline**
2. Fill in the runtime inputs (org, project, connector, repo) if prompted
3. Wait for the SscaOrchestration step to finish (green)
4. Click the step in the execution view → **Supply Chain tab** to see:
   - SBOM quality score
   - Component list (name, version, license, PURL) — npm packages from `sample-app/package.json`
   - Attestation status
   - Drift report (added / removed / version-bumped components vs. base branch)

You can also download the raw SBOM JSON from the execution page.

---

## Image vs. Repository scanning — when to use each

| | Repository scan | Image scan |
|---|---|---|
| **When** | During CI, on every commit | After image is built and pushed |
| **What it sees** | Package manifests (declared deps) | Installed packages inside the image layer |
| **Catches** | Dep drift, license issues early | OS packages, transitive runtime deps |
| **Tool** | cdxgen | Syft |
| **Requires registry** | No | Yes |

Use **repo scanning** to shift left and catch issues before a build. Use **image scanning** for a complete runtime inventory after a build.
