<div id="top"></div>

<div align="center">

<img src="./assets/safai-logo.png" alt="Safai Logo" width="460" />

# SafaiOS - Civic Waste Intelligence & Municipal Operating System

**The Intelligence Behind Cleaner Cities.**  
*Detect. Act. Verify.*

<br />

[![CI](https://github.com/TheVicky1/Safai_OS/actions/workflows/ci.yml/badge.svg)](https://github.com/TheVicky1/Safai_OS/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-00c853.svg?style=for-the-badge)](LICENSE)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![YOLO11s](https://img.shields.io/badge/YOLO-11s-00599C.svg?style=for-the-badge&logo=ultralytics&logoColor=white)](https://github.com/ultralytics/ultralytics)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.x-EE4C2C.svg?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org/)
[![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL_17-3ECF8E.svg?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com/)
[![RLS Protected](https://img.shields.io/badge/RLS-100%25_Protected-blueviolet.svg?style=for-the-badge)](#database-foundation--security)
[![Test Suite](https://img.shields.io/badge/Tests-151_Passing-success.svg?style=for-the-badge&logo=pytest&logoColor=white)](#validation--quality-gates)
[![Contributions Welcome](https://img.shields.io/badge/Contributions-Welcome-0e8a16.svg?style=for-the-badge)](#contributing)

<br />

> 🌍 **Civic Cleanliness Through Verified Accountability**: SafaiOS unites computer vision, municipal operations, and dual-actor proof-of-work cleanup verification to eliminate urban litter dumps and restore civic trust.

<br />

[About](#about) · [Foundational Principles](#foundational-principles) · [Core Features](#core-features) · [AI & Vision Engine](#ai--computer-vision-engine) · [Database Foundation & Security](#database-foundation--security) · [System Architecture](#system-architecture) · [Quick Start](#quick-start) · [Validation & Quality Gates](#validation--quality-gates) · [Project Structure](#project-structure) · [Contributing](#contributing) · [Documentation](#documentation)

</div>

---

<a id="about"></a>
<div align="center">
  <h2>About</h2>
</div>

Urban centers across the globe struggle with an insidious sanitation bottleneck: **the accountability gap**.

Municipal authorities struggle with blind spots across sprawling streets. Citizens report open waste dumps only to see reports vanish into administrative voids. Sanitary drivers are dispatched without verifiable route priorities. Most critically, traditional civic systems suffer from **ghost cleanups** - where tasks are marked closed without visual proof, leaving waste uncollected and citizens disillusioned.

**SafaiOS** solves this breakdown.

SafaiOS is an open-source, server-authoritative **Civic Waste Intelligence & Municipal Operating System**. Built on a high-throughput edge computer vision backbone (**YOLO11s**) and a hardened database layer (**PostgreSQL 17 / Supabase** with Row-Level Security on 100% of tables), SafaiOS automates the entire waste remediation lifecycle:

1. **Instant AI Detection**: High-resolution waste localization and classification across five material categories.
2. **Deterministic Dispatch**: Direct assignment of verified incidents to sanitary drivers and municipal fleets.
3. **Proof-of-Work Verification**: Strict before-and-after photographic evidence and dual-actor verification.
4. **Civic Incentive Ledger**: Idempotent Safai Coins reward issuance upon confirmed cleanup verification.
5. **Municipal Accountability**: Tamper-proof, append-only audit logging and real-time operational telemetry.

---

<a id="foundational-principles"></a>
<div align="center">
  <h2>Foundational Principles</h2>
</div>

### 1. Verifiable Proof of Cleanup
No incident is ever marked resolved based on claims alone. Drivers must submit photographic proof linked to their active assignment. The reporting citizen verifies the cleanup. If the citizen denies the work or fails to respond within seven days, the task escalates to municipal administrative review.

### 2. Strict Anti-Fraud & Self-Verification Ban
A cleanup performer can **never** verify their own work, regardless of any assigned administrative or citizen roles. If a citizen reports a dump and performs the cleanup themselves, verification is routed to an authorized municipal administrator.

### 3. Server-Authoritative Workflow Governance
Client applications (Citizen, Driver, Admin) are strictly presentation layers. Clients cannot directly modify incident statuses, alter reward balances, manipulate AI results, or delete audit logs. Every state transition is executed through server-validated commands.

### 4. Zero Data Leakage Computer Vision
Our vision engine is trained on the curated **SafaiOS_Dataset_v10k** dataset containing 10,000+ audited waste images. Strict geographic and source-split isolation guarantees zero cross-split leakage, benchmarked on real-world Indian street waste distributions.

### 5. Idempotent Civic Reward Ledger
Safai Coins are awarded only upon verified incident closure. Every reward transaction is tied to a unique idempotency key and incident record, strictly preventing double-crediting or balance tampering.

---

<a id="core-features"></a>
<div align="center">
  <h2>Core Features</h2>
</div>

SafaiOS provides a complete municipal operating framework across citizens, sanitation drivers, and city administrators:

| Subsystem | Capabilities | Status |
| :--- | :--- | :--- |
| **YOLO11s Detection Engine** | Real-time object detection at 768px (`E002` baseline & `E004` CoarseDropout) classifying 5 material categories with class-specific NMS. | Available |
| **Citizen Reporting Pipeline** | Geotagged camera capture, client-side draft validation, automated AI pre-analysis, and private upload isolation. | Available |
| **Municipal Dispatch Center** | Real-time incident intake, duplicate candidate screening, driver availability tracking, and single-active-assignment enforcement. | Available |
| **Driver Execution Interface** | Route navigation, assignment acceptance, on-site arrival markers, and photographic cleanup evidence submission. | Available |
| **Dual-Actor Verification Engine** | Citizen before-and-after visual inspection, approval/denial controls, and automated 7-day administrative escalation. | Available |
| **Anti-Fraud Security System** | Disqualification of cleanup performers from self-verification; strict reporter conflict rerouting to municipal admins. | Available |
| **Safai Coins Ledger** | Append-only financial credit/debit transaction ledger with unique incident idempotency constraints. | Available |
| **Duplicate Assessment Engine** | Automated spatio-temporal and visual similarity assessment between incident candidates without unverified auto-deletion. | Available |
| **Tamper-Proof Audit Logging** | Comprehensive append-only security logs capturing actor identity, action type, before/after states, and request IDs. | Available |
| **Private Scoped Storage** | User-isolated folder scoping (`storage.objects`) for `incident-media` and `cleanup-evidence` with incident-bound RLS policies. | Available |
| **Multi-Role RBAC** | Strict role separation across `CITIZEN`, `DRIVER`, `ADMIN`, `VIEWER` (read-only), and `SUPERADMIN`. | Available |
| **Automated Notifications** | Event-driven status updates across incident submission, driver assignment, evidence review, and reward distribution. | Available |

---

<a id="ai--computer-vision-engine"></a>
<div align="center">
  <h2>AI & Computer Vision Engine</h2>
</div>

The visual core of SafaiOS is engineered for real-world environmental complexity: varying daylight, heavy shadows, overlapping garbage heaps, soiled materials, and occluded street litter.

```
+-----------------------------------------------------------------+
|                    SafaiOS AI Vision Pipeline                   |
+-----------------------------------------------------------------+
|                                                                 |
|   [ Incoming Citizen Image ]                                    |
|               |                                                 |
|               v                                                 |
|   [ Preprocessing & Letterbox Resizing to 768x768 ]              |
|               |                                                 |
|               v                                                 |
|   [ YOLO11s Detection Backbone & Feature Pyramid Network ]      |
|               |                                                 |
|               v                                                 |
|   [ Postprocessing & Class-Specific NMS (conf=0.25, iou=0.60) ] |
|               |                                                 |
|               v                                                 |
|   [ Waste Taxonomy Mapping & Density Stratification ]           |
|               |                                                 |
|               v                                                 |
|   [ Server-Authoritative ai_analysis_results Entry ]            |
+-----------------------------------------------------------------+
```

### Approved Real-World Waste Taxonomy

| Class ID | Material Identifier | Real-World Target Scope |
| :---: | :--- | :--- |
| **0** | `plastic_bottle` | PET water/soda bottles, detergent bottles, rigid plastics |
| **1** | `plastic_wrapper_bag` | Single-use polythene bags, chip packets, packaging films |
| **2** | `paper_cardboard` | Corrugated boxes, packaging cartons, newspapers, paper cups |
| **3** | `glass_bottle_container` | Beverage bottles, broken glass containers, food jars |
| **4** | `metal_can` | Aluminium beverage cans, tin food containers, aerosol cans |

### Model Evolution & Experiments

- **`E001` - Baseline Verification**: Validated input resolution scaling and baseline anchor configuration.
- **`E002` - Production YOLO11s Model**: Trained at 768px input resolution on `SafaiOS_Dataset_v10k` with confidence threshold `0.25` and NMS IoU `0.60`. Checkpoint SHA-256: `8bd30b05a0b4a84d95c5e71f213b967d255144a8fe57791ef110b920fc86d073`.
- **`E003` - High-Resolution Evaluation Protocol**: Rigorous performance evaluation across fine-grained scale tiers.
- **`E004` - CoarseDropout Occlusion Invariance**: Specialized training protocol injecting rectangular occlusion masks during training to maximize recall on heavily clustered and partially buried street litter.

### Dataset Engineering (`SafaiOS_Dataset_v10k`)

The model family is trained on a dedicated dataset constructed with extreme rigor:
- **10,000+ Curated Images**: Sourced from real-world street photography and verified open repositories.
- **Zero Cross-Split Contamination**: Deterministic split allocation ensuring no image or near-duplicate spans train, validation, and locked test splits.
- **Independent Indian Benchmark Set**: Dedicated evaluation set reflecting challenging municipal street environments in India.

---

<a id="database-foundation--security"></a>
<div align="center">
  <h2>Database Foundation & Security</h2>
</div>

SafaiOS operates on **PostgreSQL 17** via **Supabase**, adhering to a zero-trust database security model.

### 16 Relational Entities & Guardrails

The database schema establishes 15 core entities plus the supporting evidence-media junction:

1. `profiles`: User identities linked 1-to-1 with `auth.users`, protected from client privilege mutation.
2. `user_roles`: Server-governed roles (`CITIZEN`, `DRIVER`, `ADMIN`, `VIEWER`, `SUPERADMIN`) with active-role uniqueness.
3. `admin_permissions`: Granular capability flags for administrative accounts.
4. `incidents`: Central reporting records with coordinates, narrative, lifecycle state, and timestamps.
5. `incident_media`: Metadata for original citizen photographs and driver evidence with SHA-256 hashing.
6. `ai_analysis_results`: Immutable records of detector runs, checkpoint hashes, and bounding box coordinates.
7. `duplicate_assessments`: Spatio-temporal match scores between incident pairs for administrator review.
8. `driver_assignments`: Historical dispatch records enforcing at most one active driver assignment per incident.
9. `cleanup_evidence`: Driver cleanup statements and submission timestamps bound to active assignments.
10. `cleanup_evidence_media`: Many-to-many junction linking cleanup evidence to authorized media records.
11. `verification_decisions`: Append-only audit of citizen or admin approval/denial determinations.
12. `citizen_feedback`: Post-resolution citizen satisfaction ratings (1-5) and commentary.
13. `safai_coin_accounts`: User ledger accounts tracking Safai Coin balances.
14. `safai_coin_transactions`: Immutable transaction ledger enforcing idempotency on reward credits.
15. `audit_logs`: Append-only system-wide security log capturing actor ID, entity states, and request IDs.
16. `notifications`: Event-driven user alert records with delivery and read receipt timestamps.

### Strict Incident Lifecycle Flow

```text
DRAFT (Citizen report + YOLO11s pre-scan)
  │
  ▼
SUBMITTED
  │
  ▼
ADMIN_REVIEW (Duplicate assessment logged; no automated closure)
  │
  ▼
ASSIGNED (Dispatched to single active sanitary driver)
  │
  ▼
CLEANUP_IN_PROGRESS (Driver en route / on site)
  │
  ▼
AWAITING_CITIZEN_VERIFICATION (Driver submits cleanup evidence)
  ├── Citizen Approves ───────────────► CLOSED ──► Idempotent Safai Coins Minted
  ├── Citizen Denies ─────────────────► AWAITING_ADMIN_REVIEW
  └── No Response in 7 Days ──────────► AWAITING_ADMIN_REVIEW
                                          │
                                          ├── Admin Approves ──► CLOSED ──► Idempotent Safai Coins Minted
                                          └── Admin Rejects  ──► RESOLUTION_REQUIRED (Rework / Reassign)
```

### Row-Level Security (RLS) Policy Matrix

- **100% Table Coverage**: RLS is explicitly enabled on all 16 public tables.
- **Citizen Isolation**: Citizens can only query their own reports and evidence submitted for their incidents.
- **Driver Isolation**: Drivers can only view assignments explicitly assigned to their driver profile.
- **Read-Only Viewer**: The `VIEWER` role is strictly read-only and cannot execute mutations across any table.
- **Hardened Search Paths**: All PL/pgSQL trigger and helper functions enforce explicit `set search_path = public` or `set search_path = public, auth` to neutralize search path hijacking.
- **Private Storage**: Storage buckets `incident-media` and `cleanup-evidence` are private; object reads require incident authorization or administrative privileges.

---

<a id="system-architecture"></a>
<div align="center">
  <h2>System Architecture</h2>
</div>

SafaiOS enforces clean boundaries between client presentation, server business logic, computer vision inference, and durable data storage:

```
+-------------------------------------------------------------------------+
|                       Presentation Layer (UI Apps)                      |
|   - Citizen Mobile / Web App      - Sanitary Driver Field App           |
|   - Municipal Admin Portal        - Public Viewer Dashboard             |
+-------------------------------------------------------------------------+
                                     │
                             HTTPS / JSON APIs
                                     │
+-------------------------------------------------------------------------+
|                  Server-Authoritative Application Layer                 |
|   - Incident Lifecycle Controller    - Dispatch & Assignment Engine     |
|   - Verification & Anti-Fraud Guard  - Duplicate Screening Service      |
|   - Safai Coins Transaction Manager  - 7-Day Autonomous Sweeper         |
+-------------------------------------------------------------------------+
                  │                                   │
         Python IPC / REST                     Supabase Client
                  │                                   │
+-----------------------------------+   +---------------------------------+
|     AI Computer Vision Engine     |   |    Database & Storage Layer     |
|   - YOLOInferenceEngine (E002)    |   |   - PostgreSQL 17               |
|   - Letterbox 768px Preprocessor  |   |   - Row-Level Security (RLS)    |
|   - Class-Specific NMS Postprocess|   |   - Private Storage Buckets     |
|   - Bounding Box Normalizer       |   |   - pgTAP Automated Test Suite  |
+-----------------------------------+   +---------------------------------+
```

---

<a id="quick-start"></a>
<div align="center">
  <h2>Quick Start</h2>
</div>

### Prerequisites

- **Python**: `3.11.x`
- **Docker Desktop**: With Linux engine / WSL 2 enabled
- **Supabase CLI**: `v2.x` installed
- **Git**: Installed and configured

### 1. Clone the Repository

```bash
git clone https://github.com/TheVicky1/Safai_OS.git
cd Safai_OS
```

### 2. Configure Python Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate

# Upgrade pip and install dependencies in editable mode
pip install --upgrade pip
pip install -e ".[dev]"
```

### 3. Configure Local Environment Variables

```bash
cp .env.example .env
```

Review `.env` to verify your local test configurations.

### 4. Start Local Supabase Stack

```bash
# Start local containers (Postgres 17, Storage, Auth, Studio)
supabase start

# Apply database foundation migration and seeds
supabase db reset
```

The Supabase local development stack will be available at:
- **Studio Dashboard**: [http://localhost:54323](http://localhost:54323)
- **API Gateway**: [http://localhost:54321](http://localhost:54321)
- **Local PostgreSQL**: `postgresql://postgres:postgres@localhost:54322/postgres`

---

<a id="validation--quality-gates"></a>
<div align="center">
  <h2>Validation & Quality Gates</h2>
</div>

SafaiOS enforces strict automated verification gates across both computer vision and database subsystems:

### Run Python ML & Core Regression Suite

Execute the full suite of **151 unit and regression tests**:

```bash
pytest tests/ -v
```

This validates:
- Dataset pipeline integrity, label bounds, and split leak isolation.
- YOLO bounding box conversions, greedy matching, and IoU calculations.
- Class-specific non-maximum suppression (NMS) and confidence filtering.
- Inference engine lazy-loading and model export routines.
- `E004` CoarseDropout data augmentation protocols.

### Run Database pgTAP Authorization Tests

Verify database constraints, active assignment uniqueness, RLS citizen/driver isolation, and self-verification prevention:

```bash
supabase test db
```

Exercises the comprehensive 24-point test suite in `supabase/tests/database_foundation.test_test.sql`.

### Run Database Linting

Ensure SQL migrations adhere to production security standards (search path safety, RLS enablement, key constraints):

```bash
supabase db lint --level error --fail-on error
```

---

<a id="project-structure"></a>
<div align="center">
  <h2>Project Structure</h2>
</div>

```text
Safai_OS/
├── .github/
│   └── workflows/
│       └── ci.yml               # Automated CI (Database validation + Python pytest)
├── Application/                 # Municipal application specifications & roadmap
│   ├── Admin/                   # Municipal Admin portal architecture
│   ├── AI/                      # Vision detector and reasoning specifications
│   ├── Backend/                 # Server-authoritative workflow boundaries
│   ├── Citizen/                 # Citizen reporting interface design
│   ├── Documentation/           # Master architecture sign-offs & contracts
│   └── Driver/                  # Driver dispatch and execution interface
├── assets/
│   └── safai-logo.png           # Official 3D emerald-gold Safai logo
├── configs/                     # Training and evaluation YAML configs
├── data/                        # Dataset manifest specifications & splits
├── docs/                        # Canonical engineering documentation and specifications
│   ├── README.md                # Master documentation hub and navigation sitemap
│   ├── ARCHITECTURE.md          # Computer vision pipeline and edge architecture specification
│   ├── DATA_MODEL.md            # Relational database schema and RLS security policies
│   ├── API.md                   # Edge detection REST API contracts and payload schemas
│   ├── DEVELOPMENT.md           # Developer environment setup, tooling, and contributing guide
│   ├── DEPLOYMENT.md            # Hardware tiers, ONNX/TensorRT export, and production runbook
│   ├── CI_PIPELINE.md           # GitHub Actions CI workflows and automated quality gates
│   ├── SECURITY.md              # Threat model, RBAC matrix, and audit policies
│   ├── TESTING.md               # 151 Python tests, 24 pgTAP tests, and test runbooks
│   ├── EVALUATION_METHODOLOGY.md# Stratified evaluation metrics and operating points
│   └── ROADMAP.md               # Strategic product and engineering milestone roadmap
├── models/                      # Model definitions and export scripts
├── reports/                     # Forensic audit logs, QA reports & milestone summaries
│   ├── evaluations/             # Validation batch figures and prediction logs
│   └── experiments/             # Experiment protocols and error analysis (E001-E004)
├── scripts/                     # Dataset acquisition, training, and evaluation scripts
├── src/
│   └── safaios/                 # Core Python package (engine, dataset, utils)
├── supabase/
│   ├── config.toml              # Local Supabase configuration (PostgreSQL 17)
│   ├── migrations/              # Production database foundation migrations
│   └── tests/                   # pgTAP security, RLS, and authorization tests
├── tests/                       # Automated Python test suite (151 tests)
├── .env.example                 # Example local environment configuration
├── pyproject.toml               # Python package configuration and build dependencies
└── requirements.txt             # Frozen dependency manifest
```

---

<a id="contributing"></a>
<div align="center">
  <h2>Contributing</h2>
</div>

Contributions to SafaiOS are warmly welcomed! Whether you are optimizing computer vision inference, refining Supabase security policies, expanding test coverage, or designing civic interfaces, your help makes cities cleaner.

### 8-Step Contributor Quickstart

1. **Explore Open Issues**: Check out our open issues for bug reports, enhancements, and feature requests.
2. **Claim an Issue**: Comment on an issue so the maintainers can assign it to you.
3. **Fork & Clone**: Fork the repository to your GitHub account and clone it locally.
4. **Create a Feature Branch**:
   ```bash
   git checkout -b feature/issue-number-short-description
   ```
5. **Implement Changes**: Adhere to clean code practices and preserve existing test coverage.
6. **Verify Quality Gates**:
   - Run `pytest tests/ -v` (all 151 tests must pass).
   - Run `supabase test db` (all pgTAP authorization tests must pass).
   - Run `supabase db lint --level error --fail-on error`.
7. **Commit Changes**: Use clear, conventional commit messages:
   ```bash
   git commit -m "feat(security): enforce driver evidence timestamp bounds"
   ```
8. **Open a Pull Request**: Submit your pull request to the `main` branch with a clear description of changes.

---

<a id="documentation"></a>
<div align="center">
  <h2>Documentation Index</h2>
</div>

| Document | Focus & Specification | Target Audience |
| :--- | :--- | :--- |
| 📚 [**Master Documentation Hub**](docs/README.md) | Central documentation directory, sitemap, and navigation hub | All Contributors |
| 🏗️ [**Technical Architecture**](docs/ARCHITECTURE.md) | Vision pipeline, 768px letterbox resizing, edge topology, and waste taxonomy | CV Engineers, Architects |
| 🗄️ [**Relational Data Model**](docs/DATA_MODEL.md) | 16 PostgreSQL database entities, PostGIS coordinates, and storage bucket RLS | Backend Developers, DBA |
| 🔌 [**Edge Detection API**](docs/API.md) | `/v1/detect` and batch contracts, Pydantic schemas, and latency SLAs | API Consumers, Mobile/Web |
| 💻 [**Developer Setup Guide**](docs/DEVELOPMENT.md) | Local environment, Python venv, CPU PyTorch setup, and Supabase CLI | All Contributors |
| 🚀 [**Production Deployment**](docs/DEPLOYMENT.md) | Jetson Orin/Nano, TensorRT 10.x FP16 export, systemd service, and Docker | DevOps, Edge Engineers |
| ⚙️ [**CI & Quality Gates**](docs/CI_PIPELINE.md) | GitHub Actions CI workflows, the 7 automated quality gates, and rulesets | Maintainers, Contributors |
| 🛡️ [**Security & RBAC Architecture**](docs/SECURITY.md) | Threat model, role predicates, self-verification denial, and ledger rules | Security Engineers, Auditors |
| 🧪 [**Testing Runbook**](docs/TESTING.md) | 151 Python tests, 24 pgTAP database tests, secret scanner, and link audits | QA, Test Automation |
| 📊 [**Evaluation Methodology**](docs/EVALUATION_METHODOLOGY.md) | Operational operating points (`conf=0.25`, `iou=0.60`) and scale stratification | Data Scientists, Evaluators |
| 🗺️ [**Product Roadmap**](docs/ROADMAP.md) | Strategic milestone tracking across Foundation, Dispatch, and Governance | Product Leads, Community |
| 📋 [**Final Architecture Sign-Off**](Application/Documentation/FINAL_ARCHITECTURE_SIGNOFF.md) | Approved product decisions, lifecycle state machine, and boundaries | System Architects |
| 🤖 [**ML Integration Contract**](Application/Documentation/ML_INTEGRATION_CONTRACT.md) | Checkpoint hashes, YOLO11s hyperparameters, and inference schemas | ML Engineers |
| 🏛️ [**Contributors Hall of Fame**](CONTRIBUTORS.md) | Permanent recognition of community contributors, live sync badges, and inductees | All Contributors |

---

<div align="center">
  <h2>Contributors & Community</h2>
</div>

SafaiOS is built with care by an open-source community dedicated to autonomous municipal intelligence, computer vision innovation, and cleaner, greener cities.

<div align="center">

[![Contributors Count](https://img.shields.io/github/contributors/TheVicky1/Safai_OS?style=for-the-badge&color=00c853)](https://github.com/TheVicky1/Safai_OS/graphs/contributors)

[![SafaiOS Contributors](https://contrib.rocks/image?repo=TheVicky1/Safai_OS)](https://github.com/TheVicky1/Safai_OS/graphs/contributors)

*A huge thank you to all open-source developers who contribute to SafaiOS!*

👉 [**View all contributors on GitHub**](https://github.com/TheVicky1/Safai_OS/graphs/contributors) • [**Contributors Hall of Fame**](CONTRIBUTORS.md)

</div>

---

<div align="center">
  <h2>License</h2>
</div>

SafaiOS is open-source software licensed under the **[MIT License](LICENSE)**.

---

<div align="center">

**Detect. Act. Verify.**

[⬆ Back to top](#top)

</div>
