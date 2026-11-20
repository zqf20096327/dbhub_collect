# NomiFlow

### Modern Payroll & Workforce Management Platform

NomiFlow is a multi-tenant SaaS platform designed to simplify payroll processing and employee management for businesses in Panama. It automates complex salary calculations, tax deductions, employee administration, and payroll reporting while maintaining compliance with Panamanian labor regulations.

Built with **.NET 9, React 19, TypeScript, and PostgreSQL**, NomiFlow provides a scalable architecture for managing multiple organizations, securing business data, and streamlining payroll operations.

---

## ✨ Key Features

### 💰 Advanced Payroll Processing
- Automated Social Security (CSS) contributions based on Panama's Law 462.
- Educational Insurance calculations.
- Progressive Income Tax (ISR) calculations with dependent deductions.
- Configurable professional risk contributions.
- Automated overtime calculations with 8 payment categories.
- 13th-month salary calculations.
- Employee termination settlements and prorated benefits.
- Configurable payroll tax rules and calculation parameters.

### 👥 Employee Management
- Complete employee profiles and employment records.
- Department and position management.
- Salary and employment contract history.
- Employee absences and vacation requests.
- Employee loans, salary advances, and recurring deductions.
- Centralized employee information management.

### 📊 Payroll Workflow
- Structured payroll lifecycle: Draft → Calculated → Approved → Paid.
- Automated salary calculations and deductions.
- Loan amortization and prorated payments.
- Vacation balance calculations and request workflows.
- Detailed payroll history and audit tracking.

### 📈 Reports & Analytics
- PDF salary receipts and payslips.
- Regulatory Social Security reports.
- Income tax declarations.
- Excel exports for accounting and financial workflows.
- Payroll summaries and business reporting.

### 🏢 Multi-Tenant Architecture
- Multiple companies managed through one platform.
- Tenant-based data isolation.
- Role-based access control with 29 granular permissions.
- Custom roles and permission management.
- Secure employee and company data access.
- Email invitations and subscription-based feature limits.

### 🔌 B2B API Platform
- RESTful API endpoints for external integrations.
- SHA-256 API key authentication.
- Request rate limiting and monthly usage quotas.
- Idempotency keys to prevent duplicate operations.
- Automated API usage notifications and quota alerts.

### 💳 Subscription Management
- Integrated Stripe subscription billing.
- Multiple subscription tiers: Free, Starter, Professional, and Enterprise.
- Plan-based employee, user, and business limits.
- Automated subscription lifecycle management.
- Stripe webhook integration.

---

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Backend | C#, .NET 9, ASP.NET Core Web API |
| Frontend | React 19, TypeScript 5.9, Vite 7 |
| UI & Styling | Tailwind CSS 3.4, Lucide React |
| Database | PostgreSQL 16 |
| ORM | Entity Framework Core 9 |
| Authentication | ASP.NET Core Identity, JWT |
| API Documentation | Swagger / OpenAPI |
| State Management | React Context API |
| Data Visualization | Recharts |
| PDF Generation | QuestPDF |
| Excel Generation | ClosedXML |
| Payments | Stripe |
| Email Services | Brevo |
| Testing | xUnit, Moq, FluentAssertions |
| Infrastructure | Docker, DigitalOcean, CapRover |

---


### Architecture Principles

- **Domain:** Contains core business entities, rules, and interfaces.
- **Application:** Handles business workflows, services, DTOs, and payroll calculations.
- **Infrastructure:** Implements database access, repositories, and external integrations.
- **Web:** Provides REST APIs, authentication, middleware, and frontend hosting.

Dependencies flow inward, keeping business logic independent of infrastructure and presentation technologies.

---

## 🔐 Security & Authorization

- JWT Bearer authentication with refresh token support.
- Secure password and identity management.
- Tenant-aware authorization and data isolation.
- Custom roles and 29 granular system permissions.
- Separate authentication for B2B API clients.
- SHA-256 API key hashing.
- Audit trails for important data modifications.
- Soft-delete policies to preserve historical records.

---

## 🚀 Getting Started

### Prerequisites

Make sure you have the following installed:

- [.NET 9 SDK](https://dotnet.microsoft.com/download/dotnet/9.0)
- [Node.js 20+](https://nodejs.org/)
- [PostgreSQL 16](https://www.postgresql.org/)
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/Coretech001/NomiFlow.git
cd NomiFlow
```

### 2. Configure the Database

Create a PostgreSQL database named `PaglyDB`.

Configure your connection string in:

```text
src/UI/Pagly.Web/appsettings.json
```

Alternatively, configure the environment variable:

```text
ConnectionStrings__DefaultConnection
```

### 3. Apply Database Migrations

```bash
dotnet ef database update \
  --project src/Infrastructure/Pagly.Infrastructure \
  --startup-project src/UI/Pagly.Web
```

### 4. Install Frontend Dependencies

```bash
cd src/UI/Pagly.Web/ClientApp
npm install
```

### 5. Start the Backend

From the repository root:

```bash
dotnet run --project src/UI/Pagly.Web
```

Backend API:

```text
http://localhost:5039
```

Swagger documentation:

```text
http://localhost:5039/swagger
```

### 6. Start the Frontend

Open another terminal:

```bash
cd src/UI/Pagly.Web/ClientApp
npm run dev
```

Frontend application:

```text
http://localhost:5173
```

---

## 💳 Subscription Plans

NomiFlow supports four subscription tiers with different usage limits and features.

| Feature | Free | Starter | Professional | Enterprise |
|---|:---:|:---:|:---:|:---:|
| Employees | 5 | 25 | 100 | Unlimited |
| Users | 1 | 3 | 10 | Unlimited |
| Businesses | 1 | 1 | 3 | Unlimited |
| Excel Reports | ❌ | ✅ | ✅ | ✅ |
| PDF Reports | ❌ | ❌ | ✅ | ✅ |
| B2B API | ❌ | ❌ | ✅ | ✅ |
| Monthly Price | $0 | $29.99 | $79.99 | $199.99+ |

*Pricing and feature limits are based on the project's documented configuration.*

---

## 🚢 Deployment

The application uses Docker for containerization and CapRover on DigitalOcean for deployment.

Deployment workflow:

1. Push changes to the `master` branch.
2. GitHub webhook triggers the deployment process.
3. Docker builds the application.
4. Database migrations are applied during application startup.
5. The updated application is deployed through CapRover.

Production configuration is managed through environment variables for database connections, JWT authentication, Stripe, Brevo, and API rate limits.

---

## 🗺️ Development Roadmap

### Completed
- [x] Clean Architecture implementation.
- [x] Multi-tenant architecture and data isolation.
- [x] Custom role and permission management.
- [x] Panama payroll calculation engine.
- [x] Overtime and 13th-month salary calculations.
- [x] PDF and Excel reporting.
- [x] Stripe subscription integration.
- [x] Email invitation system.
- [x] B2B API platform.
- [x] Automated deployment pipeline.
- [x] Audit trails and health checks.

### In Progress
- [ ] Comprehensive unit and integration test coverage.
- [ ] Employee self-service portal.

### Planned
- [ ] Banking integration for payroll disbursement.
- [ ] Mobile application using .NET MAUI.
- [ ] Advanced executive dashboards.
- [ ] AI-powered payroll anomaly detection.

---

## 📚 Documentation

Additional technical documentation is organized into the following areas:

- `docs/architecture/` — System architecture and frontend conventions.
- `docs/payroll/` — Payroll calculations and business rules.
- `docs/compliance/` — Panamanian regulations and compliance.
- `docs/multi-tenant/` — Tenant isolation and architecture.
- `docs/roles-permisos/` — Roles and permissions.
- `docs/api-platform/` — B2B API documentation.
- `docs/integrations/` — Stripe, Brevo, and email integrations.
- `docs/deploy/` — Deployment and infrastructure guides.
- `docs/security/` — Authentication and security practices.
- `docs/qa/` — Testing and quality assurance.

---

## 🎯 Project Goals

NomiFlow aims to provide businesses with a centralized and reliable payroll management solution by combining automated calculations, employee administration, regulatory compliance, and secure multi-tenant infrastructure.

The platform is designed to reduce manual administrative work, improve payroll accuracy, and make complex workforce operations easier to manage.

---

**NomiFlow — Payroll Management, Simplified.**

Built with .NET, React, TypeScript, and PostgreSQL.
