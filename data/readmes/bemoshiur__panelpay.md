<div align="center">

# PanelPay

### Open-source Amazon Lightsail reseller panel: prepaid wallet, billing and automatic provisioning

Sell Amazon Lightsail servers, databases, storage, CDN, DNS and domains under your own brand, to customers who pay
in their own currency from a prepaid wallet. Built with TypeScript, Next.js, PostgreSQL and SST on AWS.

[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
![TypeScript](https://img.shields.io/badge/TypeScript-strict-3178c6)
![Next.js](https://img.shields.io/badge/Next.js-16-black)
![AWS](https://img.shields.io/badge/AWS-Lightsail%20%C2%B7%20Route%2053%20%C2%B7%20Lambda-ff9900)
![Status](https://img.shields.io/badge/status-pre--launch-orange)
[![AWS Marketplace: Pro edition coming soon](https://img.shields.io/badge/AWS%20Marketplace-Pro%20edition%20coming%20soon-ff9900)](#choose-your-edition)

<a href="docs/pro-edition.md"><img src="docs/assets/editions-banner.svg" alt="PanelPay editions: free open-source edition under Apache-2.0, and the Pro edition with a one-click AWS CloudFormation install, coming soon to AWS Marketplace" width="100%"></a>

[Website](https://tryaws.now) · **[Pro install guide](docs/pro-edition.md)** · [Documentation](docs/index.md) · [Architecture explained](docs/architecture-explained.md) ·
[For hosting resellers](docs/for-hosting-resellers.md) · [FAQ](docs/faq.md) · [Contributing](CONTRIBUTING.md)

**Created by [S M Moshiur Rahman](https://www.linkedin.com/in/in-moshiur) · [Connect on LinkedIn](https://www.linkedin.com/in/in-moshiur)**

</div>

---

## What is PanelPay?

**PanelPay is a free, open-source control panel and billing system for reselling Amazon Lightsail.** A
customer signs up, tops up a prepaid wallet, and launches a server, a managed database, a storage bucket, a CDN
distribution, a DNS zone or a domain from a simple panel. The platform charges the wallet, writes a
double-entry ledger, creates the resource in your AWS accounts, and renews or suspends it on schedule.

It started as a production system for the Bangladesh market (prices in taka, payments through the EPS gateway,
a Bangla and English panel). The market, currency and payment gateway are configuration and adapters, so the
design works for any region where customers cannot or do not want to pay AWS in dollars with a card.

> **Status: pre-launch.** The platform code is complete and was proven on a staging environment, which has since
> been torn down. It has not taken real customer money in production. Treat it as a serious starting point and
> reference implementation, and read [docs/spec/15-security-gate-before-launch.md](docs/spec/15-security-gate-before-launch.md)
> before you accept payments.

## Choose your edition

|         | **Open source** (this repository)                                             | **PanelPay Pro** on AWS Marketplace                                                                                  |
| ------- | ----------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| Price   | Free, [Apache-2.0](LICENSE)                                                   | $199 for a 36-month contract, billed through your AWS account                                                        |
| Runs on | Your AWS Organization: Lambda, RDS, SQS and more, deployed with SST           | One Amazon EC2 instance in your own AWS account                                                                      |
| Install | Clone, configure and deploy yourself ([Quick start](#quick-start-developers)) | One AWS CloudFormation stack: ready AMI, IAM roles, Amazon Cognito user pools, Amazon S3 invoices bucket, Elastic IP |
| WHMCS   | Addon in [pro/whmcs](pro/whmcs)                                               | Addon included on the AMI                                                                                            |
| Updates | `git pull`                                                                    | Packaged updates while the contract is active; the installed version keeps running after it ends                     |
| Support | [GitHub issues](https://github.com/bemoshiur/panelpay/issues)                 | Vendor support by TiCON System Limited (business@ticonsys.com)                                                       |
| Status  | Source available now                                                          | **Coming soon:** version 1.0.2 is in AWS Marketplace review. The link will appear here when the listing is public.   |

Both editions are built from the same code. The Pro edition packages it for a single EC2 instance and installs
it in minutes, so you do not need to run a multi-account AWS setup yourself.

> **📘 Read the [PanelPay Pro install guide](docs/pro-edition.md)**: what the stack creates, parameters,
> after-launch steps, WHMCS, costs and limits. Template and installer: [pro/cfn](pro/cfn) and
> [pro/box/README.md](pro/box/README.md).

## Who is it for?

- **Hosting resellers and WHMCS sellers** who want to add AWS-backed servers to their offer without writing
  provisioning code. See [For hosting resellers](docs/for-hosting-resellers.md) for an honest comparison.
- **Regional cloud providers and MSPs** who bill in a local currency and need a prepaid, self-service panel.
- **Developers and students** who want to learn how a real multi-account AWS platform is built: STS
  AssumeRole, Lightsail and Route 53 APIs, SQS-driven provisioning, tenant isolation, a double-entry ledger,
  idempotent jobs, infrastructure as code with SST. See [Architecture explained](docs/architecture-explained.md).

## Features

| Area            | What it does                                                                                                                                  |
| --------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| Products        | Lightsail Linux and Windows instances, block disks, managed databases, object storage, load balancers, CDN, containers, static IPs, snapshots |
| Domains and DNS | Domain registration and renewal and DNS zones through Amazon Route 53                                                                         |
| Money           | Prepaid wallet, integer-paisa maths, **append-only double-entry ledger**, VAT invoices, credit notes, refunds to the wallet                   |
| Payments        | EPS hosted checkout with server-to-server verification (adapter pattern for other gateways)                                                   |
| Provisioning    | Operation queue with idempotent jobs, retries, capacity pooling across many AWS accounts, final snapshots before destroy                      |
| Isolation       | Tenant-scoped data access with cross-tenant tests; private-network isolation rules bootstrapped on every Linux instance                       |
| Lifecycle       | Auto-renew, suspend, unpaid grace, retention and deletion with admin approval                                                                 |
| Identity        | Amazon Cognito for customers; separate admin app with TOTP and an IP allowlist                                                                |
| Operations      | Admin console with audit log, price book, FX rate with four-eyes approval, reconciler against AWS usage, runbooks                             |
| Safety          | Every product family behind a feature flag, off by default in production; fail-closed checks                                                  |
| Languages       | Panel messages in English and Bangla (`next-intl`)                                                                                            |

## Architecture at a glance

```
Customer ─▶ CloudFront + WAF ─▶ Next.js panel (apps/web) ──┐
Admin ────▶ CloudFront + WAF ─▶ Next.js admin (apps/admin) ┤  write an operation row,
                                                           │  never call AWS directly (rule R1)
                                                           ▼
                         PostgreSQL (private, RDS Proxy, TLS) ◀── Lambda workers (functions/)
                                                           │      provisioner, scheduler,
                                                           │      reconciler, notifier, ...
                                                           ▼
                                   Pool accounts (Lightsail) and the DNS account (Route 53)
                                   reached only through STS AssumeRole
```

Read the long version with the reasons behind each choice in [Architecture explained](docs/architecture-explained.md).

## Tech stack

| Layer          | Technology                                                                        |
| -------------- | --------------------------------------------------------------------------------- |
| Apps           | Next.js, React, `next-intl` (English and Bangla), self-hosted fonts               |
| Backend        | TypeScript on AWS Lambda, Amazon SQS, Amazon EventBridge Scheduler                |
| Data           | PostgreSQL on Amazon RDS behind RDS Proxy, Drizzle ORM, forward-only migrations   |
| Identity       | Amazon Cognito (customers), TOTP and IP allowlist for admins                      |
| Infrastructure | SST 4 (Pulumi) in `ap-southeast-1`; GitHub Actions with OIDC (no long-lived keys) |
| Payments       | EPS (BDT) today; adapter boundary for others                                      |
| Quality        | Vitest, Playwright, ESLint, Prettier, gitleaks secret scan, SEO/AEO audit         |

## Quick start (developers)

Requirements: Node.js 24, pnpm 10, Docker.

```bash
git clone https://github.com/bemoshiur/panelpay.git
cd panelpay
pnpm install
pnpm db:up && pnpm db:migrate      # local PostgreSQL in Docker
pnpm verify --quick                # lint, typecheck and unit tests of the packages you changed
pnpm test --filter @tc/core        # the pricing, ledger and lifecycle logic, pure and fast
```

The project builds and tests **without** the commercial website theme. To get the full look, bring your own
licensed copy: see [docs/theme.md](docs/theme.md).

To run it on AWS you need your own AWS accounts and a payment-gateway agreement. Start with
[docs/runbooks/single-account-lean.md](docs/runbooks/single-account-lean.md) and
[docs/runbooks/go-live.md](docs/runbooks/go-live.md).

## Repository layout

```
apps/
  web/             customer panel and public site
  admin/           admin app (separate host, TOTP, IP allowlist)
packages/
  core/            pure logic: pricing, ledger, orders, lifecycle, capacity
  db/              schema, migrations, tenant-scoped repositories
  aws/             AWS clients and product adapters (imported only by functions/)
  eps/ notify/ auth/ ui/
functions/         Lambda handlers: provisioner, scheduler, reconciler, notifier, migrator, ...
infra/             SST app, stacks and the CI role templates
verify/            proofs per task and per gate
docs/              specification, runbooks and guides
```

## The rules

Money and customer data are protected by 17 rules that are tested, not just written. The first ones: money is
integer paisa; the ledger is append-only; credit a wallet only after server-to-server verification; every job
is idempotent; the web tier never provisions; fail closed. Read them in [CLAUDE.md](CLAUDE.md) and
[docs/spec/02-rules-that-are-never-broken.md](docs/spec/02-rules-that-are-never-broken.md).

## Documentation

| Read this                                                        | When you want to                                                |
| ---------------------------------------------------------------- | --------------------------------------------------------------- |
| [docs/index.md](docs/index.md)                                   | find your way around                                            |
| [docs/architecture-explained.md](docs/architecture-explained.md) | understand how it works on AWS                                  |
| [docs/for-hosting-resellers.md](docs/for-hosting-resellers.md)   | decide if it fits your hosting business, and compare with WHMCS |
| [docs/faq.md](docs/faq.md)                                       | get quick answers                                               |
| [docs/spec/](docs/spec/)                                         | read the full specification                                     |
| [docs/runbooks/](docs/runbooks/README.md)                        | operate it: deploys, refunds, incidents, restore drills         |

## Important notes before you use it

- **AWS terms.** Reselling AWS services is governed by the AWS Customer Agreement and service terms, and by any
  programme you join. This software does not give you any right to resell AWS. Check with AWS that your
  business model is allowed before you sell.
- **Tax, payments and law.** Invoice formats, VAT rules, KYC and payment rules differ by country. The Bangladesh
  settings are examples and not legal advice. Get local advice.
- **Your own company details.** The company registration number (BIN), trade licence and address on the legal
  pages, in `apps/web/public/facts.json` and on invoices belong to whoever runs the site. In the public copy
  of this repository they are placeholders. Search for `000000000-0000`, `TRAD/DNCC/000000/2000` and
  `Example House`, and replace every hit with your own details before you publish a site or issue an invoice.
- **Not affiliated.** Amazon Web Services, AWS and Amazon Lightsail are trademarks of Amazon.com, Inc. or its
  affiliates. WHMCS is a trademark of WHMCS Limited. This project is independent and is not affiliated with or
  endorsed by either.

## Contributing

Contributions are welcome, from a typo to a new payment gateway. Start with [CONTRIBUTING.md](CONTRIBUTING.md),
look for **good first issue**, and follow the [Code of Conduct](CODE_OF_CONDUCT.md). Report a security problem
privately: see [SECURITY.md](SECURITY.md).

## Credits

PanelPay is created and maintained by **[S M Moshiur Rahman](https://www.linkedin.com/in/in-moshiur)**
([LinkedIn](https://www.linkedin.com/in/in-moshiur)). If this project helps you, please keep the attribution in
[NOTICE](NOTICE), star the repository, and share it.

## License

[Apache License 2.0](LICENSE). The commercial website theme is not included and is not covered by this licence
(see [NOTICE](NOTICE)).

---

<div align="center">

_PanelPay is open source (Apache-2.0), created by [S M Moshiur Rahman](https://www.linkedin.com/in/in-moshiur) · [LinkedIn](https://www.linkedin.com/in/in-moshiur)._

</div>
