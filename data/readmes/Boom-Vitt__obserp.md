<!-- BBN:HEADER:START -->
<p align="center">
  <img src="site/assets/wordmark.png" width="420" alt="obserp" />
</p>
<!-- BBN:HEADER:END -->

<div align="center">

# obserp

Open-source, self-hosted ERP for Thai SMEs, with AI and OCR on your own machine.

[![Desktop CI](https://github.com/Boom-Vitt/obserp/actions/workflows/boombignose-desktop.yml/badge.svg?branch=main)](https://github.com/Boom-Vitt/obserp/actions/workflows/boombignose-desktop.yml)
[![ERP E2E](https://github.com/Boom-Vitt/obserp/actions/workflows/erp-e2e.yml/badge.svg?branch=main)](https://github.com/Boom-Vitt/obserp/actions/workflows/erp-e2e.yml)
[![License](https://img.shields.io/badge/license-AGPL--3.0%20%7C%20Commercial-blue?style=flat-square)](./LICENSE)
[![Release](https://img.shields.io/github/v/release/Boom-Vitt/obserp?style=flat-square)](https://github.com/Boom-Vitt/obserp/releases/latest)
[![GitHub stars](https://img.shields.io/github/stars/Boom-Vitt/obserp?style=flat-square)](https://github.com/Boom-Vitt/obserp/stargazers)

[Website](https://boom-vitt.github.io/obserp/) · [Download](https://github.com/Boom-Vitt/obserp/releases/latest) · [Documentation](./docs) · [Issues](https://github.com/Boom-Vitt/obserp/issues)

</div>

obserp brings sales, purchasing, inventory, projects, and finance into one database, with business data on the customer's own machine or server. Thai VAT, withholding tax (WHT), THB amounts, and the `Asia/Bangkok` time zone are built in. Local AI and OCR help read documents and prepare suggestions for a person to review and confirm before saving. The product name is **obserp**. Release tags keep the `boombignose-v*` prefix.

As of **12 November 2026**, the latest published release verified is [boombignose-v1.5.4](https://github.com/Boom-Vitt/obserp/releases/tag/boombignose-v1.5.4). The version source and mobile AI Agent have merged, and release publication is tracked in [#190](https://github.com/Boom-Vitt/obserp/issues/190). The source statements and roadmap below describe [main at 482d5700](https://github.com/Boom-Vitt/obserp/tree/482d5700d7516d97719af7f9e65d3a64cf749b90). A merge does not prove inclusion in the latest installer or complete physical-device acceptance.

## Features

| Module | Available in current source |
| --- | --- |
| Dashboard and CRM | Cash, revenue, unpaid invoices, pipeline, clients, contacts, deals, and follow-up activities |
| Sales and payments | Quotes, invoices, deposits, subscriptions, receipts, WHT, and finance period locks |
| Purchasing and products | Vendors, RFQs, purchase orders, partial receipts, vendor bills, returns, and a product catalog |
| Inventory | Multiple warehouses, stock movements, deliveries, returns, transfers, physical counts, and replenishment |
| Expenses and projects | Claims with separate approval, tasks, milestones, timesheets, and time billing |
| Reports and month-end close | VAT, receivables aging, calendar, accountant packs, and CSV export to your accounting software |
| AI and OCR | Permission-scoped ERP chat, Thai and English images and PDFs, form suggestions, and review worklists. A download is refused when the on-machine hardware estimate says the model will not fit. That estimate is not a measured quality or speed result. See [Local model hardware](./docs/LOCAL_MODEL_HARDWARE.md) and [Local AI models](./docs/local-ai-models.md). |
| Teams and automation | Owner, admin, accountant, and member roles, organization scope, invitation links, audit log, and n8n outbox/webhooks |
| Company world and telesale | 2D/3D company views, mini-games, activity-based ranking, and a telephone desk with caller matching and local recording |
| iOS mobile app | Flutter QR pairing over a private tailnet, native AI chat, and OCR review |
| Thai ERP benchmark | [`evals/thai_erp_bench`](./evals/thai_erp_bench/README.md) runs five frozen synthetic fixtures against a loopback server you already started. An absent scorer is recorded as pending, not as a pass. |

Call recording requires appropriate authorization and lawful data handling. The network 3D view supports investigation. It is not DLP or proof that data cannot leak. See the [security boundaries](./.github/SECURITY.md#current-source-security-boundaries).

An owner or admin can issue a full tax invoice or an abbreviated tax invoice inside the app, with a frozen snapshot and a PDF. Nothing is sent to the Revenue Department. See [what a statutory tax invoice still needs](./docs/thai/tax-invoice-gaps.md). Saving a workspace business type writes an audit row. The encrypted data layer enforces the selected profile's consent and retention rules on reads and writes. Selecting a profile does not complete privacy controls across all ERP modules. [`lib/fhir/r4-mapper.ts`](./lib/fhir/r4-mapper.ts) maps typed clinic records to FHIR R4 JSON. The [patient registry](./docs/CLINIC_PATIENT_REGISTRY.md) stores encrypted profiles with clinical-role access, HN numbering and read auditing. There is no FHIR HTTP API. `POST /api/privacy` stores a purpose-scoped consent and an AES-256-GCM payload for an opaque subject id. It does not encrypt existing CRM, finance, staff, recording, or attachment columns. See [the privacy data layer](./docs/PRIVACY_DATA_LAYER.md).

Payroll, a manufacturing module, a FHIR API, and submission of e-Tax Invoice or e-Receipt data to the Revenue Department are not implemented. Team chat, the private-network drive, meetings, multi-role access, and the synthetic Thai ERP dataset and benchmark runner are on `main`. They are not a claim about release 1.5.4. This pull request is still open and is not in that release.

| Work | Pull request |
| --- | --- |
| Ticket board, sprints, and notifications | [#399](https://github.com/Boom-Vitt/obserp/pull/399) |

## Architecture

- Go/Wails provides the native desktop window and supervises the local stack. A separate Go CLI supports a headless server.
- Next.js 16, React 19, and TypeScript run the web application and application logic. PostgreSQL uses Supabase Auth and PostgREST.
- ERP, Auth, REST, PostgreSQL, and Ollama bind to loopback, such as `127.0.0.1`. Mobile access uses a private Tailscale tailnet and an HTTPS entry point to ERP only, with normal login and the MFA policy. A pairing QR provides connection details, not a session or role.
- Business access checks workspace membership, capability, and Postgres RLS. Server-only service-role paths must enforce their own authorization and scope. Money is stored as integer satang.
- The Flutter iOS app connects to the customer's self-hosted ERP. Go hot paths under [#213 Option B](https://github.com/Boom-Vitt/obserp/issues/213) are planned and require profiling first. This RFC has not moved the application core.

Read the [local architecture](./docs/boombignose/ARCHITECTURE_LOCAL.md) and the [desktop, headless deployment, and recovery runbook](./docs/boombignose/BUNDLE.md#headless-server-installation-and-private-access).

### Local AI and OCR

Chat and OCR use Ollama on loopback without a cloud fallback. An administrator explicitly downloads model weights. Weights are neither bundled in installers nor downloaded at startup. AI and OCR produce suggestions to compare with the original evidence. They do not approve, post accounts, pay, or file tax automatically.

Detailed [model guidance and recorded limits](./docs/local-ai-models.md) are retained from the previous README. Model versions, licenses, platform limits, and installation authority are documented in the [catalog](./boombignose/internal/bundle/ollama_models.json), [Ollama runbook](./docs/boombignose/BUNDLE.md#ollama), and [OCR privacy and limits](./docs/PDPA_SECURITY_NOTES.md#local-ai-ocr-and-attachments). Model downloads can contact external registries. Operators must review model terms and secure any independently managed daemon.

## Install

Choose an artifact and verify `SHA256SUMS` from [the latest GitHub Release](https://github.com/Boom-Vitt/obserp/releases/latest). Installers are named `obserp-*` and release tags keep the `boombignose-v*` prefix. Releases up to `boombignose-v1.5.4` were published under the earlier name, as `BoomBigNose-*` files; their in-app updater validates legacy repository and payload names as well as those filenames. A verified automatic rename bridge is still pending [#500](https://github.com/Boom-Vitt/obserp/issues/500), so install the first `obserp-*` release once by hand. See the [update and bridge runbook](./docs/boombignose/UPDATE.md#remaining-release-bridge-work-for-500). Your data directory is not touched. On macOS, drag the old `BoomBigNose.app` to the Trash after `obserp.app` opens. The Linux archive contains the binary named `obserp`.

| Platform | Release artifacts |
| --- | --- |
| [Windows x64](https://github.com/Boom-Vitt/obserp/releases/latest) | `obserp-windows-x64-setup.exe` |
| [macOS Apple Silicon](https://github.com/Boom-Vitt/obserp/releases/latest) | `obserp-macos-arm64.dmg` |
| [Linux amd64](https://github.com/Boom-Vitt/obserp/releases/latest) | `obserp-linux-amd64.tar.gz` or `obserp-linux-amd64.AppImage`, requires WebKitGTK 4.1 |

Windows can show SmartScreen warnings. The macOS DMG is signed with a Developer ID and notarized by Apple. Check the selected release notes. Since 0.3.0, desktop installers bundle Node, PostgreSQL, Auth, PostgREST, and Ollama. Desktop installation does not require Docker.

### Developer quick start

Use Node.js 22+, pnpm, Docker, and the Supabase CLI from the dev dependencies. The reset command below is for a separate, disposable development stack only.

```sh
git clone https://github.com/Boom-Vitt/obserp.git
cd obserp
pnpm install
pnpm exec supabase start
pnpm exec supabase db reset
cp .env.example .env.local
pnpm exec supabase status
pnpm dev
```

`supabase/config.toml` sets the Auth site URL to `http://127.0.0.1:3100`. Run `PORT=3100 pnpm dev` and set `NEXT_PUBLIC_APP_URL` to the same origin so confirmation links match. Fill `.env.local` with the values from `pnpm exec supabase status` before running `pnpm dev`. The fake seed account is `demo@boombignose.org`. See [`supabase/seed.sql`](./supabase/seed.sql). Never use the seed or demo-login settings in production.

Run `pnpm lint`, `pnpm typecheck`, `pnpm test`, and `pnpm build`. `pnpm e2e` requires the [isolated test stack](./docs/testing/erp-gates.md). See [`.env.example`](./.env.example) for environment variables.

## Roadmap

Status is checked against PRs merged into `main` and [open milestones](https://github.com/Boom-Vitt/obserp/milestones) on 12 November 2026. ✅ Done means merged source, not certification or acceptance on every device. Milestone dates are adjustable targets.

| Phase | Status | Scope and evidence |
| --- | --- | --- |
| 1. Core ERP | ✅ Done | Sales, purchasing, inventory, projects, finance, and reports. [#1](https://github.com/Boom-Vitt/obserp/pull/1), [#2](https://github.com/Boom-Vitt/obserp/pull/2), [#154](https://github.com/Boom-Vitt/obserp/pull/154) |
| 1. Desktop 1.5.x | ✅ Done | Windows, macOS, and Linux installers. [#154](https://github.com/Boom-Vitt/obserp/pull/154), [#158](https://github.com/Boom-Vitt/obserp/pull/158), [#164](https://github.com/Boom-Vitt/obserp/pull/164), and Releases |
| 1. AI and OCR | ✅ Done | Chat, ERP read tools, and OCR review. [#134](https://github.com/Boom-Vitt/obserp/pull/134), [#140](https://github.com/Boom-Vitt/obserp/pull/140), [#155](https://github.com/Boom-Vitt/obserp/pull/155), [#174](https://github.com/Boom-Vitt/obserp/pull/174) |
| 1. Company world | ✅ Done | 2D/3D modes and module zones. [#165](https://github.com/Boom-Vitt/obserp/pull/165), [#173](https://github.com/Boom-Vitt/obserp/pull/173) |
| 1. Telesale | ✅ Done | Telephone desk and local recording. [#176](https://github.com/Boom-Vitt/obserp/pull/176) |
| 1. Mini-games and ranking | ✅ Done | Mini-games and rankings from ERP activity. [#175](https://github.com/Boom-Vitt/obserp/pull/175) |
| 1. Mobile | ✅ Done | iOS pairing, Thai theme, native AI chat, and OCR. [#136](https://github.com/Boom-Vitt/obserp/pull/136), [#161](https://github.com/Boom-Vitt/obserp/pull/161), [#178](https://github.com/Boom-Vitt/obserp/pull/178) |
| 1. Access and language | ✅ Done | MFA AAL2 and login rate limiting [#172](https://github.com/Boom-Vitt/obserp/pull/172), Thai default locale [#143](https://github.com/Boom-Vitt/obserp/pull/143) |
| 2. Governance | ✅ Done | PR template, security policy, CODEOWNERS, and issue routing. [#188](https://github.com/Boom-Vitt/obserp/pull/188) |
| 2. QA matrix | ✅ Done | Installed release workflow for Windows, macOS, and Linux, scheduled every six hours. [#184](https://github.com/Boom-Vitt/obserp/pull/184). Workflow presence does not establish a passing latest run. |
| 2. v1.5.4 and mobile AI Agent | ✅ Done | [#190](https://github.com/Boom-Vitt/obserp/issues/190), PRs [#180](https://github.com/Boom-Vitt/obserp/pull/180), [#181](https://github.com/Boom-Vitt/obserp/pull/181), and the [v1.5.4 milestone](https://github.com/Boom-Vitt/obserp/milestone/1) |
| 2. QA 24/7 operations | 🚧 In progress | Linux harness [#195](https://github.com/Boom-Vitt/obserp/issues/195), macOS isolation [#196](https://github.com/Boom-Vitt/obserp/issues/196), dispatch [#197](https://github.com/Boom-Vitt/obserp/issues/197), cross-OS feature verification [#198](https://github.com/Boom-Vitt/obserp/issues/198) |
| 2. Releases and security scanning | ✅ Done | PR-tested installer promotion [#238](https://github.com/Boom-Vitt/obserp/pull/238), tracked by [#215](https://github.com/Boom-Vitt/obserp/issues/215); CodeQL and Dependabot [#189](https://github.com/Boom-Vitt/obserp/pull/189) |
| 2. Unified CRM inbox | ✅ Done | [#177](https://github.com/Boom-Vitt/obserp/pull/177) merged. See the [inbox setup and limits](./docs/crm-inbox.md). |
| 3. e-Tax Invoice | 📋 Planned | Output [#200](https://github.com/Boom-Vitt/obserp/issues/200), email delivery [#201](https://github.com/Boom-Vitt/obserp/issues/201), INET integration [#212](https://github.com/Boom-Vitt/obserp/issues/212) |
| 3. Correctness and performance | 📋 Planned | Write API idempotency [#214](https://github.com/Boom-Vitt/obserp/issues/214), profiling and Go hot paths [#213](https://github.com/Boom-Vitt/obserp/issues/213) |
| 3. FDE toolkit | 📋 Planned | Migration, parallel operation, and reconciliation. [#216](https://github.com/Boom-Vitt/obserp/issues/216) |
| 3. Compliance groundwork | 🚧 In progress | Draft plans [#246](https://github.com/Boom-Vitt/obserp/pull/246), [#247](https://github.com/Boom-Vitt/obserp/pull/247); planned SBOM/provenance [#202](https://github.com/Boom-Vitt/obserp/issues/202), control matrix [#203](https://github.com/Boom-Vitt/obserp/issues/203), DR drill [#204](https://github.com/Boom-Vitt/obserp/issues/204), ISO/IEC 29110 readiness [#205](https://github.com/Boom-Vitt/obserp/issues/205) |

## Security and compliance

See the [compliance roadmap](./docs/compliance/ROADMAP.md) for the current plan and owner checklist.

### In place on main

- The [SECURITY.md policy](./.github/SECURITY.md) and [GitHub private vulnerability reporting](https://github.com/Boom-Vitt/obserp/security/advisories/new) are available. Report vulnerabilities privately.
- [#172](https://github.com/Boom-Vitt/obserp/pull/172) adds MFA AAL2 enforcement and login rate limiting. AAL2 checks apply to users with verified MFA factors. Enrollment is not mandatory for every account.
- Internal services bind to loopback. Business data uses Postgres RLS with role and workspace checks.
- Fixes from `govulncheck`, `staticcheck`, and `gofmt` merged in [#156](https://github.com/Boom-Vitt/obserp/pull/156). Those past check results do not certify that the current product has no vulnerabilities.
- Governance [#188](https://github.com/Boom-Vitt/obserp/pull/188), the QA matrix [#184](https://github.com/Boom-Vitt/obserp/pull/184), and CodeQL/Dependabot configuration [#189](https://github.com/Boom-Vitt/obserp/pull/189) are merged. These checks do not establish certification or vulnerability-free software.

Operators remain responsible for network exposure, disk and backup encryption, and data access. Session cookies are JavaScript-readable. Service-role bypasses RLS, so privileged paths require separate authorization. Read the [current security boundaries](./.github/SECURITY.md#current-source-security-boundaries) and [PDPA notes](./docs/PDPA_SECURITY_NOTES.md).

### Certification plan

Read the [compliance index](./docs/compliance/README.md), [ISO/IEC 27001 plan](./docs/compliance/ISO27001-PLAN.md) from [#246](https://github.com/Boom-Vitt/obserp/pull/246), and [ISO/IEC 29110 readiness drafts](./docs/compliance/iso29110/README.md) from [#247](https://github.com/Boom-Vitt/obserp/pull/247). The [PDPA drafts](./docs/compliance/pdpa/README.md) are also preparation documents. Registration, appointments, policy approval, audit contracts, and applications remain with the owner through [checklist #250](https://github.com/Boom-Vitt/obserp/issues/250). Draft documents do not establish certification or completed controls.

**obserp does not currently hold any certification. All certification work below is planned or in progress.**

Company registration under [#206](https://github.com/Boom-Vitt/obserp/issues/206) is a prerequisite to certification applications in this plan. Preparation phases follow [Compliance 30d](https://github.com/Boom-Vitt/obserp/milestone/4), [Compliance 90d](https://github.com/Boom-Vitt/obserp/milestone/5), and [Compliance later](https://github.com/Boom-Vitt/obserp/milestone/6). They are not promised certification dates.

| Standard or target | Purpose | Target phase | Issue |
| --- | --- | --- | --- |
| ISO/IEC 29110 | Prepare project management and software implementation records for very small entities | 📋 Planned · Compliance 90d | [#205](https://github.com/Boom-Vitt/obserp/issues/205), assessment application [#207](https://github.com/Boom-Vitt/obserp/issues/207) |
| ISO/IEC 27001:2022 groundwork | Prepare a control matrix, SBOM/provenance, and disaster-recovery drill evidence | 🚧 In progress · draft matrix/policy; SBOM and DR drill remain planned | [#203](https://github.com/Boom-Vitt/obserp/issues/203), [#202](https://github.com/Boom-Vitt/obserp/issues/202), [#204](https://github.com/Boom-Vitt/obserp/issues/204) |
| e-Tax Invoice output to Revenue Department specifications | Prepare output, delivery, and INET service provider integration | 📋 Planned · Compliance 30d, subject to required agreements and testing | [#200](https://github.com/Boom-Vitt/obserp/issues/200), [#201](https://github.com/Boom-Vitt/obserp/issues/201), [#212](https://github.com/Boom-Vitt/obserp/issues/212) |
| CAC SME | Prepare the business's anti-corruption process and evidence | 📋 Planned · Compliance later, owner-led | [#208](https://github.com/Boom-Vitt/obserp/issues/208) |
| ETDA e-Tax service provider | Consider assessment if operating an e-Tax service directly | 📋 Planned · Compliance later | [#209](https://github.com/Boom-Vitt/obserp/issues/209) |

Only if a hosted cloud service is offered later, consider ISO/IEC 27017, ISO/IEC 27018, ISO/IEC 27701, CSA STAR, SOC 2 Type II, ISO 22301, and ISO/IEC 20000-1. These are future considerations. This README claims no certification or audit result.

## Forward Deployed Engineering (FDE)

FDE is a service model in which engineers work on-site or alongside the customer to move a legacy system onto obserp. AI helps interpret data and suggest mappings while the old system and obserp run side by side for human review before cutover.

1. **Discovery**. Review workflows, data sources, access, and acceptance criteria with the customer.
2. **Data mapping**. AI suggests field and record mappings. A person reviews and approves them before import.
3. **Parallel run**. Operate the old system and obserp together within the agreed scope. Keep evidence and differences.
4. **Daily reconciliation**. Compare the trial balance, accounts receivable (AR), accounts payable (AP), and stock each day. Assigned reviewers investigate differences.
5. **Cutover**. Switch after the agreed criteria are met, with backups, a recovery point, and a verifiable rollback plan.

The [FDE migration toolkit #216](https://github.com/Boom-Vitt/obserp/issues/216) is **Planned**. This process does not claim that a complete migration toolkit exists or that AI can certify accounting balances.

## Editions and scope

| Edition | License and scope |
| --- | --- |
| Community | [AGPL-3.0-only](./LICENSE) or [Commercial](./COMMERCIAL-LICENSE.md), with the core modules |
| Pro | [`ee/LICENSE`](./ee/LICENSE), covering the client portal, accounting-software export, multiple workspaces, and hosted provisioning |

Community is the default. Pro lives in [`ee/`](./ee/), builds with `BBN_EDITION=pro`, and requires a commercial agreement for production use. See the [open-core boundary](./docs/OPEN_CORE_BOUNDARY.md). obserp does not yet provide complete statutory accounting. Tax filing, payroll, and manufacturing are outside the current scope. e-Tax Invoice remains planned.

## Contributing and community

- Read [CONTRIBUTING.md](./CONTRIBUTING.md). Run lint, typecheck, test, and build before opening a PR.
- Read and affirm the [CLA.md](./CLA.md) for your contribution.
- Use the [issue templates](https://github.com/Boom-Vitt/obserp/issues/new/choose), [Discussions](https://github.com/Boom-Vitt/obserp/discussions), and [master tracker #210](https://github.com/Boom-Vitt/obserp/issues/210).
- Report vulnerabilities privately under [SECURITY.md](./.github/SECURITY.md). Keep customer data and secrets out of public issues. Use fake test data.

## License

Community is dual-licensed under [AGPL-3.0-only](./LICENSE) or a separately agreed [Commercial license](./COMMERCIAL-LICENSE.md). Pro in [`ee/`](./ee/) is commercial source-available software under [`ee/LICENSE`](./ee/LICENSE), with a commercial agreement required for production. [`bignose/`](./bignose/LICENSE) is a separate proprietary product. Names and logos are reserved under [TRADEMARK.md](./TRADEMARK.md). Third-party licenses are listed in [NOTICE](./NOTICE).

Copyright © 2026 BoomBigNose AI Co., Ltd.

<!-- BBN:FOOTER:START -->
[Maintained by the obserp project](https://github.com/Boom-Vitt/obserp/)
<!-- BBN:FOOTER:END -->
