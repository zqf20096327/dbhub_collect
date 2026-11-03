<div align="center">

# 🧾 MyInvois Middleware Gateway

### *One clean REST API in front of Malaysia's MyInvois. Free for every developer.*

**Free, open-source middleware gateway for Malaysia's LHDN MyInvois e-invoicing system.** A production-ready REST API layer between your applications (ERP, POS, web dashboard) and the official MyInvois API. It handles token and session management, digital signing, document submission, status polling, `Retry-After` and rate-limit handling, a 10-minute duplicate guard, multi-tenant companies, credit, debit and refund notes, and consolidated B2C invoices, so you integrate once and ship.

<br />

![MyInvois Middleware Gateway](asset/social-preview.png)

<br />

## 🧊 Designed & Developed by KLCube Network Agency

### Zahid Aramai, Founder & Lead Developer

[![KLCube Network Agency](https://img.shields.io/badge/KLCube-Network_Agency-F97316?style=for-the-badge&logoColor=white)](#-designed--developed-by-klcube-network-agency)
[![Lead Developer](https://img.shields.io/badge/Lead_Developer-Zahid_Aramai-1E293B?style=for-the-badge)](#-designed--developed-by-klcube-network-agency)
[![SSM Registration](https://img.shields.io/badge/SSM_Reg._No.-201603293248_(002580717--P)-2563EB?style=for-the-badge)](#-designed--developed-by-klcube-network-agency)

<br />

[![Node.js](https://img.shields.io/badge/Node.js-22-339933?style=for-the-badge&logo=node.js&logoColor=white)](https://nodejs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org)
[![Fastify](https://img.shields.io/badge/Fastify-5.x-000000?style=for-the-badge&logo=fastify&logoColor=white)](https://fastify.dev)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![Redis](https://img.shields.io/badge/Redis-7-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io)
[![Prisma](https://img.shields.io/badge/Prisma-5.x-2D3748?style=for-the-badge&logo=prisma&logoColor=white)](https://www.prisma.io)

[![CI](https://github.com/zahidaramai/MyInvoice-SDK-Middleware/actions/workflows/ci.yml/badge.svg)](https://github.com/zahidaramai/MyInvoice-SDK-Middleware/actions/workflows/ci.yml)
[![OpenAPI Lint](https://github.com/zahidaramai/MyInvoice-SDK-Middleware/actions/workflows/openapi-lint.yml/badge.svg)](https://github.com/zahidaramai/MyInvoice-SDK-Middleware/actions/workflows/openapi-lint.yml)
[![Generate SDKs](https://github.com/zahidaramai/MyInvoice-SDK-Middleware/actions/workflows/gen-sdks.yml/badge.svg)](https://github.com/zahidaramai/MyInvoice-SDK-Middleware/actions/workflows/gen-sdks.yml)
[![Changesets](https://github.com/zahidaramai/MyInvoice-SDK-Middleware/actions/workflows/changesets.yml/badge.svg)](https://github.com/zahidaramai/MyInvoice-SDK-Middleware/actions/workflows/changesets.yml)
[![Release](https://github.com/zahidaramai/MyInvoice-SDK-Middleware/actions/workflows/release.yml/badge.svg)](https://github.com/zahidaramai/MyInvoice-SDK-Middleware/actions/workflows/release.yml)

![Status](https://img.shields.io/badge/status-open_source-success?style=flat-square)
![Document Types](https://img.shields.io/badge/document_types-9_validated-blue?style=flat-square)
![SDKs](https://img.shields.io/badge/generated_SDKs-4-orange?style=flat-square)
![Models](https://img.shields.io/badge/prisma_models-10-informational?style=flat-square)
![Node](https://img.shields.io/badge/node-%3E%3D20-339933?style=flat-square&logo=node.js&logoColor=white)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)
![Made in Malaysia](https://img.shields.io/badge/made%20in-Malaysia-CC0001?style=flat-square)

[**Repository**](https://github.com/zahidaramai/MyInvoice-SDK-Middleware) · [**OpenAPI Spec**](openapi/openapi.yaml) · [**Author**](https://zahidaramai.com/) · [**Disclaimer**](DISCLAIMER.md)

> **Disclaimer**: This is an unofficial community project and is not affiliated with LHDN (Lembaga Hasil Dalam Negeri Malaysia). See [DISCLAIMER.md](DISCLAIMER.md) for full terms.

</div>

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Tech Stack](#-tech-stack)
- [Features](#-features)
- [API Reference](#-api-reference)
  - [Authentication](#authentication-endpoints)
  - [Submission Endpoints](#submission-endpoints)
  - [Document Endpoints](#document-endpoints)
  - [Management Endpoints](#management-endpoints)
  - [Session, Submission and TIN Endpoints](#session-submission-and-tin-endpoints)
  - [Health & Monitoring](#health--monitoring)
  - [Generated SDKs](#generated-sdks)
- [Digital Signing (v1.1)](#-digital-signing-v11)
- [Permissions & Roles](#-permissions--roles)
- [Data Model & Reference Codes](#-data-model--reference-codes)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Available Scripts](#-available-scripts)
- [Quality & Verification](#-quality--verification)
- [Scope](#-scope)
- [Environment Variables](#-environment-variables)
- [Deployment](#-deployment)
- [Security & Troubleshooting](#-security--troubleshooting)
- [Contributing, Resources & License](#-contributing-resources--license)

---

## 🎯 Overview

Malaysia's MyInvois e-invoicing mandate asks every business to talk to the LHDN API: authenticate, sign, submit, poll, respect rate limits and handle rejections. This gateway does that plumbing once, behind one documented REST API, so your ERP, POS or dashboard only sends JSON invoices. It is **free for everyone** under the MIT licence, whether you are a solo developer, an SME or a software house. A key use case is **consolidated B2C invoicing** (daily sales without a buyer ID), alongside B2B, B2C with NRIC, and draft-first workflows.

| | |
|---|---|
| **Project** | MyInvois Middleware Gateway (`myinvois-middleware`) |
| **Licence** | MIT, free open-source software |
| **Author** | [Zahid Aramai](https://zahidaramai.com/) · KLCube Network Agency |
| **Target API** | LHDN MyInvois (SANDBOX and PROD, selected by `MYINVOIS_ENV`) |
| **Document formats** | v1.0 (unsigned) and v1.1 (digitally signed) |
| **Document types** | 9 types validated (see below) |
| **Multi-tenant** | Companies with stored MyInvois credentials, or ERP on-behalf mode |
| **Default port** | `3000`, base path `/api/v1` |
| **SDKs** | TypeScript, Python, Java, C# / .NET generated from `openapi/openapi.yaml` |
| **Reference timezone** | Malaysia (MYT, UTC+8) |

### Validated with Both v1.0 and v1.1

This middleware has been **validated against the MyInvois Sandbox and Production APIs** with all 9 document types in both **v1.0 (unsigned)** and **v1.1 (digitally signed)** formats:

| Document Type | v1.0 | v1.1 (Signed) |
|---------------|:----:|:-------------:|
| Invoice (01) | Validated | Validated |
| Credit Note (02) | Validated | Validated |
| Debit Note (03) | Validated | Validated |
| Refund Note (04) | Validated | Validated |
| Self-billed Invoice (11) | Validated | Validated |
| Self-billed Credit Note (12) | Validated | Validated |
| Self-billed Debit Note (13) | Validated | Validated |
| Self-billed Refund Note (14) | Validated | Validated |
| Consolidated Invoice | Validated | Validated |

### Architecture

```
┌─────────────────┐     ┌──────────────────────────┐     ┌─────────────────┐
│                 │     │    MyInvois Gateway       │     │                 │
│  Your Dashboard │────>│  ┌──────────────────┐    │────>│  MyInvois API   │
│  (React/Vue)    │     │  │ JWT Auth         │    │     │  (LHDN)         │
│                 │     │  │ RBAC             │    │     │                 │
└─────────────────┘     │  │ Rate Limiting    │    │     └─────────────────┘
                        │  │ Digital Signing  │    │
┌─────────────────┐     │  │ JSON -> UBL 2.1  │    │
│  POS System     │────>│  │ Error Normalizer │    │
│                 │     │  └──────────────────┘    │
└─────────────────┘     └────────────┬─────────────┘
                                     │
                        ┌────────────▼─────────────┐
                        │  Background Workers       │
                        │  - Auto Status Poller     │
                        │  - Monthly Consolidation  │
                        └────────────┬─────────────┘
                                     │
          ┌──────────────────────────┼──────────────────────────┐
          │                          │                          │
   ┌──────▼──────┐           ┌───────▼───────┐          ┌──────▼──────┐
   │  PostgreSQL │           │    Redis      │          │  Prometheus │
   │  (Prisma)   │           │  (BullMQ +    │          │  (Metrics)  │
   │  10 models  │           │   Rate Limit) │          │             │
   └─────────────┘           └───────────────┘          └─────────────┘
```

---

## 🧱 Tech Stack

| Layer | Technology | Notes |
|-------|-----------|-------|
| **Runtime** | [Node.js](https://nodejs.org) 22 | CI runs Node 22; `engines.node` is `>=20` |
| **Language** | [TypeScript 5.x](https://www.typescriptlang.org) | ESM monorepo (`"type": "module"`) |
| **API framework** | [Fastify 5](https://fastify.dev) | `apps/gateway`, CORS, correlation IDs, error normalizer |
| **Database** | [PostgreSQL 16](https://www.postgresql.org) | Via Prisma, 10 models |
| **ORM** | [Prisma 5](https://www.prisma.io) | Schema and migrations in `packages/storage/prisma` |
| **Queue and cache** | [Redis 7](https://redis.io) + [BullMQ](https://bullmq.io) | Background worker and rate limiting |
| **Monorepo** | [pnpm](https://pnpm.io) 9 workspaces | `packageManager` pinned to `pnpm@9.15.1` |
| **Testing** | [Vitest](https://vitest.dev), [MSW](https://mswjs.io), [Testcontainers](https://testcontainers.com) | Unit, route, integration, E2E, contract tests |
| **Metrics** | Prometheus | `/metrics` endpoint |
| **SDK generation** | [OpenAPI Generator](https://openapi-generator.tech) v7.10.0 | Docker-based, deterministic |
| **Linting** | ESLint, Prettier, [Spectral](https://stoplight.io/open-source/spectral) | Spectral lints the OpenAPI spec in CI |
| **Releases** | [Changesets](https://github.com/changesets/changesets) | Version and publish workflow |

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **4 Submission Types** | Consolidated B2C, JustSave (draft), B2B (buyer TIN+BRN), B2C (buyer NRIC) |
| **JWT Authentication** | Access + Refresh tokens with role-based access control |
| **Multi-Tenant Companies** | Full company management with MyInvois credential storage |
| **User Management** | Users, Roles, Companies CRUD with permission gating |
| **Document Operations** | List, Status, PDF, Cancel, QR Code, Share Links |
| **Digital Signing v1.1** | X.509 PKCS#12 certificate signing per LHDN specification |
| **Auto Status Polling** | Background polling for submission status updates |
| **Monthly Consolidation** | Scheduled consolidation of draft B2C invoices |
| **Draft Management** | Save, edit, update, and submit draft invoices |
| **Rate Limiting** | Built-in LHDN rate limit enforcement (12/100/300 RPM) |
| **ERP On-Behalf Mode** | Single ERP credentials for multiple suppliers |
| **POS Integration** | Dedicated POS adapter with QR e-invoice registration |
| **S3 Certificate Loading** | Load P12 certificates from AWS S3 or local paths |
| **Prometheus Metrics** | Built-in `/metrics` endpoint for monitoring |
| **Error Normalization** | Consistent error envelope with correlationId tracking |
| **4 Generated SDKs** | TypeScript, Python, Java, C# clients from OpenAPI spec |

### Engineering guarantees

- **Token and session management**: MyInvois tokens are handled by a token manager in `packages/myinvois-client`, and gateway sessions are exposed under `/v1/sessions`.
- **`Retry-After` handling**: rate-limited responses (HTTP 429) carry a `Retry-After` header on the submission, TIN and auth routes, and the gateway respects it when talking to LHDN.
- **10-minute dedupe**: an idempotency window (`IDEMPOTENCY_WINDOW_MINUTES: 10`, stored in the `IdempotencyWindow` model) stops duplicate submissions.
- **TIN validation cache**: results are cached in the `TinValidateCache` model, with `idValue` hashed using `TIN_HASH_SALT`.
- **Consistent errors**: every error uses one envelope with a `correlationId` for tracing.
- **Auth throttling**: login (5 per minute per IP), refresh (10 per minute per IP) and POS token generation (250 per minute per user) are rate limited.

---

## 📡 API Reference

### Base URL

```
http://localhost:3000/api/v1
```

All endpoints below are relative to the base URL. All endpoints except `/auth/login` require a JWT bearer token:

```
Authorization: Bearer <access_token>
```

The full contract lives in [`openapi/openapi.yaml`](openapi/openapi.yaml).

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/login` | Login with email/password |
| POST | `/auth/logout` | Invalidate tokens |
| POST | `/auth/refresh` | Exchange refresh token for new access token |
| GET | `/auth/me` | Get current authenticated user |
| POST | `/auth/switch-company` | Switch active company context |
| POST | `/auth/pos-token` | Generate a long-lived POS token (needs `manage:companies`) |

#### Login Response

```json
{
  "accessToken": "eyJhbGciOiJIUzI1NiIs...",
  "refreshToken": "eyJhbGciOiJIUzI1NiIs...",
  "expiresIn": 900,
  "user": {
    "id": "abc123",
    "email": "admin@example.com",
    "name": "Admin",
    "role": "Admin"
  }
}
```

### Submission Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/klcubelhdn/submit-consolidate` | Consolidated B2C invoice (daily sales) |
| POST | `/klcubelhdn/submit-justsave` | Save invoice as draft (no LHDN submission) |
| POST | `/klcubelhdn/submit-buyer` | B2B invoice (with buyer TIN + BRN) |
| POST | `/klcubelhdn/submit-personal` | B2C invoice (with buyer NRIC) |

#### Legacy Unified Endpoint

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/documents/submit` | Unified submission with flags |

#### Submission Request Format

```json
POST /api/v1/klcubelhdn/submit-buyer
{
  "companyId": "uuid-of-company",
  "documentVersion": "1.1",
  "invoices": [{
    "invoiceNumber": "INV-2026-001",
    "invoiceDate": "2026-01-21T10:00:00Z",
    "amount": 100.00,
    "discount": 0,
    "rounding": 0,
    "taxAmount": 8.00,
    "total": 108.00,
    "buyer": {
      "tin": "C25235029040",
      "name": "Buyer Company Sdn Bhd",
      "idType": "BRN",
      "idValue": "20170104319",
      "address": "123 Main Street",
      "city": "Kuala Lumpur",
      "state": "14",
      "postalCode": "50000",
      "phone": "0123456789",
      "email": "buyer@example.com"
    },
    "items": [{
      "description": "Professional Services",
      "quantity": 1,
      "unitPrice": 100.00,
      "discount": 0,
      "taxCode": "01",
      "taxRate": 8,
      "taxAmount": 8.00,
      "total": 108.00
    }]
  }]
}
```

### Document Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/documents` | List documents (with filters, pagination) |
| GET | `/documents/:uuid/status` | Get document status from MyInvois |
| GET | `/documents/:uuid/pdf` | Download PDF |
| POST | `/documents/:uuid/cancel` | Cancel submitted document |
| GET | `/documents/:uuid/qr` | Generate QR code (PNG) |
| GET | `/documents/:uuid/links` | Get all shareable links |
| POST | `/documents/:trackingId/submit` | Submit a saved draft |
| PUT | `/documents/:trackingId` | Update draft invoice data |
| DELETE | `/documents/:trackingId` | Delete draft invoice |
| GET | `/klcubelhdn/invoices/:trackingId` | Get full invoice details |

#### List Documents

```
GET /api/v1/documents?companyId=xxx&status=VALID&page=1&limit=20
```

#### Document Status Values

| Status | Description |
|--------|-------------|
| `DRAFT` | Saved locally, not submitted |
| `PENDING` | Queued for submission |
| `SUBMITTED` | Sent to MyInvois, awaiting validation |
| `VALID` | Accepted by LHDN |
| `INVALID` | Rejected by LHDN |
| `CANCELLED` | Cancelled after validation |

### Management Endpoints

#### Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users` | List all users (paginated) |
| POST | `/users` | Create user |
| GET | `/users/:id` | Get user by ID |
| PUT | `/users/:id` | Update user |
| DELETE | `/users/:id` | Delete user |
| PUT | `/users/:id/role` | Assign role to user |
| POST | `/users/:userId/companies/:companyId` | Link user to company |
| DELETE | `/users/:userId/companies/:companyId` | Unlink user from company |

#### Roles

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/roles` | List all roles (paginated) |
| GET | `/roles/all` | Get all roles (for dropdowns) |
| GET | `/roles/permissions` | Get available permissions |
| POST | `/roles` | Create role |
| GET | `/roles/:id` | Get role by ID |
| PUT | `/roles/:id` | Update role |
| DELETE | `/roles/:id` | Delete role |

#### Companies

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/companies` | List companies (paginated) |
| GET | `/companies/all` | Get all companies (for dropdowns) |
| POST | `/companies` | Create company |
| GET | `/companies/:id` | Get company details |
| PUT | `/companies/:id` | Update company |
| DELETE | `/companies/:id` | Delete company |
| PUT | `/companies/:id/credentials` | Set MyInvois API credentials |

#### POS Integration

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/pos/invoice` | Register invoice for public QR sharing |

#### Public Routes (No Auth)

Mounted at `/public` (outside `/api/v1`).

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/public/invoice/:invoiceId` | Public e-invoice registration page |
| POST | `/public/invoice/:invoiceId/submit` | Submit the public registration form |

### Session, Submission and TIN Endpoints

Lower-level routes that sit outside the `/api/v1` prefix and mirror the MyInvois flow directly.

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/v1/sessions` | Create a MyInvois session |
| GET | `/v1/sessions/:sessionId` | Read a session |
| DELETE | `/v1/sessions/:sessionId` | End a session |
| POST | `/v1/submissions` | Create a submission |
| GET | `/v1/submissions/:trackingId` | Read a submission |
| POST | `/v1/submissions/:trackingId/poll` | Poll a submission now |
| GET | `/v1/tin/validate` | Validate a taxpayer TIN (cached) |
| POST | `/v1/documents/:uuid/cancel` | Cancel a document |
| POST | `/v1/documents/:uuid/reject` | Reject a document |
| GET | `/v1/documents/:uuid/details` | Document details |

### Health & Monitoring

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Basic health check |
| GET | `/healthz` | Kubernetes liveness probe |
| GET | `/readyz` | Readiness probe (DB + Redis) |
| GET | `/metrics` | Prometheus metrics |
| GET | `/version` | Version info |

### Generated SDKs

Auto-generated client SDKs from the OpenAPI specification (`openapi/openapi.yaml`, generator config in `openapi-generator/`):

| Language | Location |
|----------|----------|
| TypeScript | `sdks/typescript/` |
| Python | `sdks/python/` |
| Java | `sdks/java/` |
| C# / .NET | `sdks/dotnet/` |

Regenerate locally with `pnpm gen:sdk` (needs Docker). The `Generate SDKs` workflow also regenerates them when the spec or generator configs change on `main`.

---

## 🔏 Digital Signing (v1.1)

Documents submitted with `documentVersion: "1.1"` are automatically signed using X.509 certificates per LHDN specification.

### Certificate Setup

**Option 1: Local PKCS#12 File**
```env
SIGNING_ENABLED=true
SIGNING_DEFAULT_VERSION=1.1
SIGNING_PKCS12_PATH=/path/to/certificate.p12
SIGNING_PKCS12_PASSPHRASE=your-password
```

**Option 2: AWS S3**
```env
SIGNING_PKCS12_PATH=s3://your-bucket/certificates/signing.p12
SIGNING_PKCS12_PASSPHRASE=your-password
```

**Option 3: PEM Files**
```env
SIGNING_CERT_PATH=/path/to/cert.pem
SIGNING_KEY_PATH=/path/to/key.pem
SIGNING_KEY_PASSPHRASE=your-password
```

Base64 variants (`SIGNING_PKCS12_BASE64`, `SIGNING_CERT_BASE64`, `SIGNING_KEY_BASE64`) and a second certificate pair for zero-downtime rotation (`SIGNING_CERT_PATH_2`, `SIGNING_KEY_PATH_2`) are documented in `.env.example`.

### Signing Process

1. Gateway receives document with `documentVersion: "1.1"`
2. Calculates document hash (SHA-256)
3. Signs hash with RSA-SHA256 using private key
4. Injects UBL XAdES signature into document
5. Submits signed document to MyInvois

---

## 🛡️ Permissions & Roles

Role-based access control with **6 permissions**:

| Permission | Description | Endpoints |
|------------|-------------|-----------|
| `submit:invoice` | Submit invoices to LHDN | `/klcubelhdn/*`, `/documents/submit` |
| `read:documents` | View documents and statuses | `/documents`, `/documents/:uuid/*` |
| `cancel:documents` | Cancel submitted documents | `/documents/:uuid/cancel` |
| `manage:users` | User CRUD operations | `/users/*` |
| `manage:roles` | Role CRUD operations | `/roles/*` |
| `manage:companies` | Company CRUD operations | `/companies/*` |

### Default Roles (Pre-seeded)

| Role | Permissions |
|------|-------------|
| **Admin** | All 6 permissions |
| **Invoice Manager** | `submit:invoice`, `read:documents`, `cancel:documents` |
| **Viewer** | `read:documents` |

Custom roles can be created via the API using any combination of the 6 permissions.

---

## 🗄️ Data Model & Reference Codes

### Database Models

| Model | Purpose |
|-------|---------|
| `User` | Platform user accounts |
| `Role` | Roles with permission arrays |
| `Company` | Multi-tenant company entities with MyInvois credentials |
| `UserCompany` | User-Company many-to-many linking |
| `RefreshToken` | JWT refresh token tracking |
| `Invoice` | Invoice storage with full lifecycle |
| `Submission` | Gateway submission tracking |
| `SubmissionDocument` | Individual documents within submissions |
| `IdempotencyWindow` | 10-minute deduplication window |
| `TinValidateCache` | TIN validation result caching |

### Tax Codes

| Code | Description |
|------|-------------|
| 01 | Sales Tax (SST) |
| 02 | Service Tax |
| 03 | Tourism Tax |
| 04 | High-Value Goods Tax |
| 05 | Sales Tax on Low Value Goods |
| 06 | Not Applicable |
| E | Tax Exemption |

### State Codes

| Code | State |
|------|-------|
| 01 | Johor |
| 02 | Kedah |
| 03 | Kelantan |
| 04 | Melaka |
| 05 | Negeri Sembilan |
| 06 | Pahang |
| 07 | Pulau Pinang |
| 08 | Perak |
| 09 | Perlis |
| 10 | Selangor |
| 11 | Terengganu |
| 12 | Sabah |
| 13 | Sarawak |
| 14 | Kuala Lumpur |
| 15 | Labuan |
| 16 | Putrajaya |
| 17 | Not Applicable |

---

## 📂 Project Structure

```
MyInvoice-SDK-Middleware/
├── apps/
│   ├── gateway/                 # REST API (Fastify)
│   │   ├── src/
│   │   │   ├── adapters/        # KLCubeLHDN + POS adapters
│   │   │   ├── auth/            # JWT authentication
│   │   │   ├── management/      # User/Role/Company CRUD
│   │   │   ├── polling/         # Auto status poller + consolidation
│   │   │   ├── public/          # Public QR registration
│   │   │   ├── config/          # Signing, S3 loader
│   │   │   ├── plugins/         # Fastify plugins
│   │   │   └── routes/          # Core v1 routes
│   │   ├── prisma/              # Gateway seed script
│   │   └── test/                # Gateway tests
│   └── worker/                  # Background job processor (BullMQ)
├── packages/
│   ├── contracts/               # Shared TypeScript types
│   ├── core/                    # Rate limiter, error normalization
│   ├── myinvois-client/         # Typed MyInvois API client + token manager
│   ├── signing/                 # X.509 signing (v1.1)
│   └── storage/                 # Prisma ORM + PostgreSQL (schema, migrations, seed)
├── sdks/                        # Generated client SDKs
│   ├── typescript/
│   ├── python/
│   ├── java/
│   └── dotnet/
├── openapi/                     # OpenAPI 3.0.3 spec (openapi.yaml)
├── openapi-generator/           # Per-language SDK generator configs
├── docker/                      # Docker Compose (dev + prod), nginx
├── scripts/                     # SDK generation, seed and signing debug scripts
├── load/                        # k6 smoke test
├── test/                        # E2E, integration, MSW and OpenAPI contract tests
├── asset/                       # Social preview image
├── .github/workflows/           # CI, OpenAPI lint, SDK generation, changesets, release
├── .env.example                 # Development environment template
├── .env.production.template     # Production environment template
├── .env.sandbox.example         # Sandbox environment template
└── Dockerfile                   # Multi-stage production build
```

---

## 🚀 Getting Started

### Prerequisites

- Node.js 22+ (CI runs Node 22; the workspace `engines.node` is `>=20`)
- pnpm 9+
- Docker (for local PostgreSQL and Redis)

### 1. Clone & Install

```bash
git clone https://github.com/zahidaramai/MyInvoice-SDK-Middleware.git
cd MyInvoice-SDK-Middleware
pnpm install
```

### 2. Start Infrastructure

```bash
docker compose -f docker/docker-compose.yml up -d
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your MyInvois credentials and database settings
```

### 4. Run Migrations & Seed

```bash
pnpm --filter @myinvois/storage prisma migrate dev
pnpm --filter @myinvois/storage prisma db seed
```

### 5. Start Gateway

```bash
pnpm --filter @myinvois/gateway dev
```

Gateway available at `http://localhost:3000`

### 6. Test Login

```bash
curl -X POST http://localhost:3000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"admin123"}'
```

The seeded `admin@example.com` account is for local development only. Change or remove it before any shared or production use.

---

## 📜 Available Scripts

### Workspace (repository root)

| Script | Description |
|--------|-------------|
| `pnpm install` | Install all dependencies |
| `pnpm build` | Build all packages |
| `pnpm lint` | Lint all packages |
| `pnpm typecheck` | Typecheck all packages |
| `pnpm test` | Run all tests |
| `pnpm check` | Lint, build and test |
| `pnpm format` / `pnpm format:check` | Prettier write / check |
| `pnpm gen:sdk` | Regenerate the four SDKs from the OpenAPI spec (Docker) |
| `pnpm changeset` / `pnpm version-packages` / `pnpm ci:publish` | Changesets release flow |

### Gateway and worker

| Script | Description |
|--------|-------------|
| `pnpm --filter @myinvois/gateway dev` | Start gateway (hot reload) |
| `pnpm --filter @myinvois/worker dev` | Start background worker (hot reload) |
| `pnpm --filter @myinvois/worker start` | Run the built worker (`node dist/index.js`) |

### Database (`@myinvois/storage`)

| Script | Description |
|--------|-------------|
| `pnpm --filter @myinvois/storage prisma migrate dev` | Run migrations |
| `pnpm --filter @myinvois/storage prisma generate` | Generate client |
| `pnpm --filter @myinvois/storage prisma db seed` | Seed database |
| `pnpm --filter @myinvois/storage prisma studio` | Open Prisma Studio |

The package also exposes `db:migrate`, `db:generate`, `db:push`, `db:studio` and `db:seed` shortcuts.

### Testing and OpenAPI

```bash
# Run all tests
pnpm test

# Run with coverage
pnpm test -- --coverage

# Run linting + build + tests
pnpm check

# Run specific test file
pnpm --filter @myinvois/gateway test -- signing.test.ts

# Lint the OpenAPI spec
npx @stoplight/spectral-cli lint openapi/openapi.yaml --ruleset .spectral.yaml

# k6 smoke test
k6 run -e BASE_URL=http://localhost:3000 load/k6-smoke.js
```

---

## ✅ Quality & Verification

| Area | Evidence |
|------|----------|
| **Sandbox and production validation** | All 9 document types validated in v1.0 and v1.1 against the MyInvois Sandbox and Production APIs |
| **CI** | `ci.yml` runs `pnpm check` (lint, build, test) on every push and pull request to `main`, on Node 22 with a PostgreSQL 16 service |
| **OpenAPI** | Spectral lint workflow plus a contract test suite in `test/openapi/` |
| **Load** | k6 smoke test in `load/k6-smoke.js` |
| **Releases** | Changesets and a tag-driven `release.yml` (`v*.*.*`) |

### Test Structure

| Type | Location |
|------|----------|
| Unit tests | `packages/*/test/` |
| Route tests | `apps/gateway/src/routes/**/*.test.ts` |
| Integration tests | `test/integration/` |
| E2E tests | `test/e2e/` |
| Negative tests | `apps/gateway/test/negative/` |
| Contract tests | `test/openapi/` |

---

## 🧭 Scope

**Delivered**

- REST gateway for MyInvois: auth, signing, submission, polling, document operations, multi-tenant companies, POS adapter, health and metrics.
- Credit, debit and refund notes, self-billed documents and consolidated B2C invoices, in v1.0 and v1.1.
- Generated SDKs for TypeScript, Python, Java and C# / .NET, plus the OpenAPI 3.0.3 spec.

**Out of scope**

- This is not an official LHDN product and gives no tax, legal or accounting advice (see [DISCLAIMER.md](DISCLAIMER.md)).
- No bundled front-end dashboard. Bring your own UI.
- No hosted service: you run the gateway, database and Redis yourself.

---

## 🔑 Environment Variables

Names and purpose only. Copy `.env.example` (or `.env.production.template` for production) to `.env` and fill in your own values.

> **Never commit `.env` or any real secret, certificate, passphrase or credential to version control.**

### Required Environment Variables

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | PostgreSQL connection string |
| `REDIS_URL` | Redis connection string |
| `JWT_SECRET` | Access token signing key (64 hex chars) |
| `JWT_REFRESH_SECRET` | Refresh token signing key (64 hex chars) |

### Optional Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | 3000 | Server port |
| `NODE_ENV` | development | Environment mode |
| `LOG_LEVEL` | debug | Logging level (debug/info/warn/error) |
| `JWT_ACCESS_EXPIRY` | 15m | Access token TTL |
| `JWT_REFRESH_EXPIRY` | 7d | Refresh token TTL |
| `MYINVOIS_ENV` | SANDBOX | MyInvois environment (SANDBOX/PROD) |
| `SIGNING_ENABLED` | false | Enable v1.1 document signing |
| `SIGNING_DEFAULT_VERSION` | 1.0 | Default document version |
| `SIGNING_PKCS12_PATH` | - | Path to P12 certificate |
| `SIGNING_PKCS12_PASSPHRASE` | - | P12 passphrase |
| `ERP_MODE` | false | Enable ERP intermediary mode |
| `ENABLE_MONTHLY_CONSOLIDATION` | false | Enable monthly draft consolidation |
| `METRICS_ENABLED` | true | Enable Prometheus metrics |

### Other variables in `.env.example`

| Variable | Purpose |
|----------|---------|
| `HOST` | Bind address (default `0.0.0.0`) |
| `MYINVOIS_CLIENT_ID`, `MYINVOIS_CLIENT_SECRET_1`, `MYINVOIS_CLIENT_SECRET_2` | Primary MyInvois credentials (second secret for rotation) |
| `MYINVOIS_SUPPLIER_TIN`, `MYINVOIS_SUPPLIER_ID_TYPE`, `MYINVOIS_SUPPLIER_ID_VALUE` | Supplier taxpayer identity for submission |
| `ERP_MYINVOIS_CLIENT_ID`, `ERP_MYINVOIS_CLIENT_SECRET`, `ERP_MYINVOIS_ENV` | ERP on-behalf credentials and environment |
| `METRICS_ROUTE` | Metrics path (default `/metrics`) |
| `TIN_HASH_SALT` | Salt for hashing `idValue` in the TIN cache |
| `SIGNING_PKCS12_BASE64`, `SIGNING_CERT_BASE64`, `SIGNING_KEY_BASE64` | Base64 certificate inputs |
| `SIGNING_CERT_PATH`, `SIGNING_KEY_PATH`, `SIGNING_KEY_PASSPHRASE` | PEM certificate, key and key passphrase |
| `SIGNING_CERT_PATH_2`, `SIGNING_KEY_PATH_2` | Second pair for certificate rotation |
| `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` | Used by the production Docker Compose file |

### Generate Secure Secrets

```bash
openssl rand -hex 32
```

---

## ☁️ Deployment

### Option 1: Docker Compose

```bash
cp .env.production.template .env
# Edit .env with production values

docker compose -f docker/docker-compose.prod.yml up -d
docker compose exec gateway npx prisma migrate deploy
```

The production stack defines `gateway`, `postgres` and `redis` services; an nginx config is in `docker/nginx/`.

### Option 2: AWS Elastic Beanstalk

The gateway ships a `Procfile` (`web: node dist/server.js`) in `apps/gateway/`. The earlier `scripts/deploy-eb.sh` helper and the AWS EB and Docker deployment guides were removed from the tree in commit `357167c`; they remain in git history.

### Option 3: Docker (Standalone)

```bash
docker build -t myinvois-gateway .
docker run -p 3000:3000 --env-file .env myinvois-gateway
```

### CI/CD

| Workflow | File | Trigger |
|----------|------|---------|
| CI | `ci.yml` | Push and pull request to `main` |
| OpenAPI Lint | `openapi-lint.yml` | Spec or `.spectral.yaml` changes |
| Generate SDKs | `gen-sdks.yml` | Manual, or spec and generator config changes on `main` |
| Changesets | `changesets.yml` | Push to `main` |
| Release | `release.yml` | Tags matching `v*.*.*` |

### Environment matrix

| Environment | `MYINVOIS_ENV` | Signing |
|-------------|----------------|---------|
| Local development | `SANDBOX` | Off by default (`SIGNING_ENABLED=false`) |
| Production | `PROD` | Enable with `SIGNING_ENABLED=true` for v1.1 |

---

## 🔐 Security & Troubleshooting

### Best Practices

1. Use strong JWT secrets (64+ hex characters)
2. Enable HTTPS in production (via reverse proxy or load balancer)
3. Restrict database access to minimum required
4. Enable database encryption at rest
5. Rotate secrets regularly
6. Monitor application logs for anomalies

Report vulnerabilities privately as described in [SECURITY.md](SECURITY.md).

### CORS

Currently allows all origins. To restrict, modify `apps/gateway/src/app.ts`:

```typescript
cors({
  origin: ["https://your-domain.com"],
  methods: ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
  allowedHeaders: ["Content-Type", "Authorization"],
  credentials: true,
})
```

### Common Issues

| Issue | Solution |
|-------|----------|
| **401 Unauthorized** | Token expired - use `/auth/refresh` for new token |
| **403 Forbidden** | Missing permissions or user not linked to company |
| **429 Too Many Requests** | Rate limit hit - respect `Retry-After` header |
| **Certificate Errors** | Verify `SIGNING_PKCS12_PATH` and passphrase |
| **Database Connection** | Check `DATABASE_URL` and PostgreSQL is running |

### Debug Commands

```bash
# Local dev with verbose logging
LOG_LEVEL=debug pnpm --filter @myinvois/gateway dev

# Test health
curl http://localhost:3000/health

# Docker logs
docker compose logs -f gateway
```

---

## 📄 Contributing, Resources & License

### Contributing

Free software gets better with your help. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/my-feature`)
3. Ensure tests pass (`pnpm check`)
4. Commit your changes
5. Push to the branch
6. Open a Pull Request

### Resources

**External references**

- [MyInvois SDK Documentation](https://sdk.myinvois.hasil.gov.my/)
- [Submit Documents API](https://sdk.myinvois.hasil.gov.my/einvoicingapi/02-submit-documents/)
- [Get Submission API](https://sdk.myinvois.hasil.gov.my/einvoicingapi/06-get-submission/)
- [Standard Error Response](https://sdk.myinvois.hasil.gov.my/standard-error-response/)
- [JSON Digital Signature](https://sdk.myinvois.hasil.gov.my/signature-creation-json/)

**Project documentation**

- [OpenAPI Specification](openapi/openapi.yaml)
- [Changelog](CHANGELOG.md)
- [Contributing Guide](CONTRIBUTING.md)
- [Security Policy](SECURITY.md)
- [Disclaimer](DISCLAIMER.md)

### Developer

**Zahid Aramai**, Full-Stack Developer & System Architect

| | |
|---|---|
| **Website** | [zahidaramai.com](https://zahidaramai.com/) |
| **Email** | hello@zahidaramai.com |
| **GitHub** | [@zahidaramai](https://github.com/zahidaramai) |

### License

Released under the **MIT License**, free for personal and commercial use. See [LICENSE](LICENSE) for details.

---

<div align="center">

## 🧊 Designed & Developed by **KLCube Network Agency**

### **Zahid Aramai**, Founder & Lead Developer

📋 **SSM Registration No. 201603293248 (002580717-P)**

[![KLCube Network Agency](https://img.shields.io/badge/KLCube-Network_Agency-F97316?style=for-the-badge)](https://zahidaramai.com/)
[![Zahid Aramai](https://img.shields.io/badge/Developer-Zahid_Aramai-1E293B?style=for-the-badge)](https://zahidaramai.com/)
[![SSM 201603293248](https://img.shields.io/badge/SSM-201603293248_(002580717--P)-2563EB?style=for-the-badge)](https://zahidaramai.com/)

<br />

Free and open-source software, built in Malaysia for developers everywhere.

© 2026 **KLCube Network Agency** · Zahid Aramai · SSM 201603293248 (002580717-P)

*One integration. Every invoice. Free for everyone.*

</div>
