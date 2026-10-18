# SupportFlow — IT Helpdesk & Ticket Management System

SupportFlow is a full-stack IT helpdesk and ticket management system designed to manage support requests across **Employee**, **Technician**, and **Administrator** roles.

The platform provides ticket creation and assignment, controlled ticket workflows, SLA tracking, public replies, internal notes, attachments, notifications, knowledge-base management, dashboards, analytics, reports, audit logging, and production deployment.

---

## Live Application

**Frontend**

```text
https://supportflow-bao6.vercel.app
```

**Backend API**

```text
https://supportflow-iota.vercel.app/api/v1
```

**Health Check**

```text
https://supportflow-iota.vercel.app/api/v1/health
```

---

## Project Highlights

- Full-stack helpdesk and ticket management workflow
- Employee, Technician, and Administrator roles
- JWT authentication with refresh-token sessions
- Role-based access control and resource-level authorization
- Ticket creation, assignment, reassignment, unassignment, and self-assignment
- Controlled ticket status transitions
- Public replies and Technician/Admin internal notes
- Ticket attachments with Cloudinary storage
- SLA response and resolution tracking
- Realtime notifications using Socket.IO
- Persistent notification storage with REST recovery
- Knowledge Base with article search and feedback
- Role-specific dashboards and analytics
- Technician workload and SLA metrics
- CSV and PDF report exports
- Audit logging
- Password change and password-reset workflows
- Production deployment using Vercel and TiDB Cloud

---

## Screenshots

### Admin Dashboard

![SupportFlow Admin Dashboard](docs/screenshots/02-admin-dashboard.png)

### Employee Dashboard

![SupportFlow Employee Dashboard](docs/screenshots/03-employee-dashboard.png)

### Create Ticket

![SupportFlow Create Ticket](docs/screenshots/04-create-ticket.png)

### Ticket Details

![SupportFlow Ticket Details](docs/screenshots/05-ticket-details.png)

### Technician Dashboard

![SupportFlow Technician Dashboard](docs/screenshots/06-technician-dashboard.png)

### User Management

![SupportFlow User Management](docs/screenshots/07-admin-user-management.png)

### Knowledge Base

![SupportFlow Knowledge Base](docs/screenshots/09-knowledge-base.png)

### Reports & Analytics

![SupportFlow Reports and Analytics](docs/screenshots/10-reports-analytics.png)

---

## User Roles

### Employee

Employees can:

- Create support tickets
- View their own tickets
- Track ticket status
- Add public replies
- Upload allowed attachments
- View notifications
- Browse the Knowledge Base
- Close or reopen eligible tickets
- Submit ticket feedback

### Technician

Technicians can:

- View support queues
- View assigned tickets
- Self-assign eligible tickets
- Update ticket status
- Add public replies
- Add internal notes
- Resolve tickets
- View SLA information
- View workload information
- Receive realtime notifications

### Administrator

Administrators can:

- Manage users and roles
- Activate or deactivate users
- View all tickets
- Assign, reassign, and unassign tickets
- Manage ticket categories
- Manage SLA policies
- Manage Knowledge Base content
- View analytics and reports
- Export report data
- Review audit logs

---

## Ticket Workflow

The main ticket lifecycle is:

```text
OPEN
  ↓
ASSIGNED
  ↓
IN_PROGRESS
  ↔
WAITING_FOR_USER
  ↓
RESOLVED
  ↓
CLOSED
```

Reopened tickets follow:

```text
RESOLVED
  ↓
REOPENED
  ↓
IN_PROGRESS
```

Ticket status changes are validated by the backend to prevent invalid workflow transitions.

### Workflow Diagram

![SupportFlow Ticket Workflow](docs/diagrams/supportflow-ticket-workflow.png)

---

## System Architecture

SupportFlow uses a separated frontend/backend architecture.

```text
Users
  │
  ▼
React + Vite + Tailwind CSS
Frontend on Vercel
  │
  ├── HTTPS REST API
  │
  └── Socket.IO
  ▼
Node.js + Express.js
Backend on Vercel
  │
  ├── TiDB Cloud
  │     └── MySQL-compatible relational database
  │
  ├── Cloudinary
  │     └── Attachment storage
  │
  └── Brevo SMTP
        └── Transactional email
```

### Architecture Diagram

![SupportFlow Architecture](docs/diagrams/supportflow-architecture.png)

---

## Database Design

SupportFlow uses a relational database model built around users, tickets, assignments, ticket history, communication, attachments, notifications, SLA policies, Knowledge Base content, feedback, and audit logging.

Main database tables include:

- `users`
- `refresh_tokens`
- `password_reset_tokens`
- `ticket_categories`
- `ticket_priorities`
- `sla_policies`
- `tickets`
- `ticket_assignments`
- `ticket_status_history`
- `ticket_comments`
- `ticket_attachments`
- `notifications`
- `knowledge_base_categories`
- `knowledge_base_articles`
- `article_feedback`
- `ticket_feedback`
- `audit_logs`

### ER Diagram

![SupportFlow ER Diagram](docs/diagrams/supportflow-er-diagram.png)

---

## Technology Stack

### Frontend

- React
- Vite
- JavaScript
- Tailwind CSS
- React Router
- Axios
- TanStack Query
- Recharts
- Socket.IO Client

### Backend

- Node.js
- Express.js
- MySQL2
- JWT
- bcryptjs
- Socket.IO
- Nodemailer
- Multer
- Cloudinary
- express-validator
- Helmet
- CORS
- Morgan
- cookie-parser

### Database

- TiDB Cloud
- MySQL-compatible SQL
- SQL migrations and seed scripts

### Production Services

- Vercel — frontend and backend hosting
- TiDB Cloud — production relational database
- Cloudinary — attachment storage
- Brevo SMTP — transactional email

### Development Tools

- Git
- GitHub
- Postman
- VS Code

For more details, see:

[Technology Stack Documentation](docs/TECH_STACK.md)

---

## Authentication & Security

SupportFlow includes:

- JWT access tokens
- Refresh-token sessions
- HttpOnly refresh-token cookies
- Secure cookies in production
- SameSite cookie configuration
- bcrypt password hashing
- Role-based access control
- Resource ownership checks
- Protected routes
- Password change workflow
- Password reset workflow
- Session revocation
- Request validation
- Parameterized SQL queries
- CORS origin restrictions
- Helmet security headers
- Upload validation
- Rate limiting
- Sanitized production errors
- Audit logging
- Environment-variable-based secrets

There is no public signup flow. User accounts are managed through controlled application workflows.

---

## SLA Management

SupportFlow supports priority-based SLA policies.

Default SLA targets:

| Priority | Response Time | Resolution Time |
|---|---:|---:|
| Critical | 30 minutes | 4 hours |
| High | 1 hour | 8 hours |
| Medium | 4 hours | 24 hours |
| Low | 8 hours | 48 hours |

Ticket-specific SLA information is preserved so existing tickets are not unintentionally affected by later policy changes.

---

## Notifications

SupportFlow provides persistent and realtime notification delivery.

The notification flow is:

```text
Application Event
      │
      ▼
Notification saved to database
      │
      ▼
Socket.IO event emitted
      │
      ▼
Authenticated user receives update
```

The database remains the source of truth. If a realtime event is missed, the frontend can recover persisted notifications through REST refetching.

---

## Knowledge Base

The Knowledge Base includes:

- Article categories
- Article creation and management
- Article search
- Suggested support content
- View tracking
- Helpful/unhelpful feedback

---

## Analytics & Reports

SupportFlow includes role-specific analytics and reporting for areas such as:

- Ticket status distribution
- Ticket priority distribution
- Ticket category distribution
- Technician workload
- SLA compliance
- Ticket volume
- Resolution performance
- Recent activity

Supported report exports include:

```text
CSV
PDF
```

---

## Project Structure

```text
supportflow/
│
├── client/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── ...
│
├── server/
│   ├── src/
│   ├── package.json
│   └── ...
│
├── docs/
│   ├── screenshots/
│   ├── diagrams/
│   ├── API.md
│   ├── DEPLOYMENT.md
│   ├── DEMO_ACCOUNTS.md
│   ├── FEATURES.md
│   ├── SETUP.md
│   └── TECH_STACK.md
│
├── README.md
└── ...
```

---

## Local Installation

Detailed installation instructions are available in:

[Local Setup Guide](docs/SETUP.md)

### Basic Setup

Clone the repository:

```bash
git clone https://github.com/kmaperera/supportflow.git
cd supportflow
```

Install backend dependencies:

```bash
cd server
npm install
```

Create the backend environment file based on the provided example configuration.

Run the required database migrations and seed scripts according to the setup guide.

Start the backend:

```bash
npm run dev
```

In another terminal, install frontend dependencies:

```bash
cd client
npm install
```

Create the frontend environment file and configure the local API base URL.

Start the frontend:

```bash
npm run dev
```

Use the actual `.env.example` files and project scripts as the source of truth for environment-variable names and available commands.

---

## API Documentation

The backend uses the base path:

```text
/api/v1
```

Detailed API documentation is available here:

[SupportFlow API Documentation](docs/API.md)

---

## Demo Accounts

Dedicated demo-account information is documented here:

[Demo Accounts](docs/DEMO_ACCOUNTS.md)

Administrator credentials are intentionally not published because the Administrator role includes sensitive system-management permissions.

---

## Feature Documentation

A detailed feature reference is available here:

[SupportFlow Features](docs/FEATURES.md)

---

## Deployment

SupportFlow is deployed using the following production architecture:

| Component | Service |
|---|---|
| Frontend | Vercel |
| Backend | Vercel |
| Database | TiDB Cloud |
| File Storage | Cloudinary |
| Email | Brevo SMTP |
| Realtime | Socket.IO |

Detailed deployment notes are available here:

[Deployment Documentation](docs/DEPLOYMENT.md)

---

## Production URLs

**Application**

```text
https://supportflow-bao6.vercel.app
```

**API**

```text
https://supportflow-iota.vercel.app/api/v1
```

**Health Check**

```text
https://supportflow-iota.vercel.app/api/v1/health
```

---

## Production Considerations

SupportFlow is deployed as a portfolio application using serverless infrastructure.

A few production characteristics are important to understand:

- TiDB Cloud requires secure TLS database connections.
- Realtime notifications use Socket.IO and persist notifications before emitting them.
- REST/database state remains the reliable source of truth if a realtime event is missed.
- Socket.IO rooms are process-local in the current Vercel deployment, so cross-instance realtime delivery is best-effort.
- The current rate limiter is process-local/in-memory, which is suitable for this portfolio deployment but would normally be replaced by a shared store for horizontally scaled production systems.

For a larger production environment, shared realtime infrastructure and distributed rate limiting would be appropriate improvements.

---

## Documentation

| Document | Description |
|---|---|
| [FEATURES.md](docs/FEATURES.md) | Detailed feature list |
| [TECH_STACK.md](docs/TECH_STACK.md) | Technology-stack documentation |
| [SETUP.md](docs/SETUP.md) | Local installation and setup |
| [API.md](docs/API.md) | REST API documentation |
| [DEPLOYMENT.md](docs/DEPLOYMENT.md) | Production deployment guide |
| [DEMO_ACCOUNTS.md](docs/DEMO_ACCOUNTS.md) | Demo-account information |

---

## Project Goals

SupportFlow was developed as an individual full-stack project to demonstrate practical software-development skills including:

- Requirements and workflow design
- Relational database design
- REST API development
- Authentication and authorization
- Complex business-rule implementation
- React frontend development
- Realtime communication
- File and email integrations
- Analytics and reporting
- Security controls
- Testing with Postman
- Production deployment
- Debugging cloud-environment issues

---

## Future Improvements

Possible future improvements include:

- Shared Socket.IO infrastructure using Redis or another adapter
- Distributed rate limiting
- Expanded automated integration and end-to-end testing
- CI/CD pipeline improvements
- Centralized production monitoring and observability
- Additional notification channels
- Advanced SLA and reporting options

---

## Author

**Malith Perera**

Computer Science Undergraduate

GitHub:

```text
https://github.com/kmaperera
```

Portfolio:

```text
https://malithperera.dev
```

---

## Repository

```text
https://github.com/kmaperera/supportflow
```

---

## License

This project was developed as an individual academic and portfolio project.

If a formal open-source license is added later, this section should be updated accordingly.
