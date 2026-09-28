# Next.js 16 + Pulumi AWS Production Starter Template

A production-ready, full-stack TypeScript starter template with Next.js 16 frontend/backend, AWS infrastructure managed by Pulumi, PostgreSQL with Drizzle ORM, and complete SaaS features including authentication, payments, monitoring, and email.

## ✨ Features

This starter template provides everything you need to build and deploy a modern SaaS application:

- **🚀 Full-stack TypeScript** - End-to-end type safety from database to frontend
- **⚡ Next.js 16** - App Router, React Server Components, and Server Actions
- **🔐 Authentication** - Better Auth with email/password and OAuth (Google, GitHub, Apple)
- **💳 Payments** - Stripe integration with subscription management and webhooks
- **🗄️ Database** - PostgreSQL 16 with Drizzle ORM and migrations
- **☁️ Infrastructure** - AWS resources managed with Pulumi (VPC, RDS, ECS, S3, CloudFront, SES)
- **📊 Monitoring** - Sentry error tracking, PostHog analytics, and CloudWatch logs
- **📧 Email** - React Email templates with AWS SES integration
- **🌍 Internationalization** - Multi-language support with next-intl
- **📝 Blog** - MDX-based blog system with dynamic routing
- **🔔 Real-time** - Server-Sent Events (SSE) support
- **🔍 SEO** - Dynamic sitemap and robots.txt generation
- **🧪 Testing** - Vitest for unit/integration tests, Playwright for E2E tests
- **🎨 UI Components** - shadcn/ui with Tailwind CSS 4

## Tech Stack

### Frontend
- Next.js 16 (App Router)
- React 19
- TypeScript 5.7+
- Tailwind CSS 4
- shadcn/ui components
- Lucide React icons

### Backend
- Next.js 16 API Routes
- tRPC 11 for type-safe APIs
- Better Auth for authentication
- Stripe for payments
- React Email for transactional emails

### Database
- PostgreSQL 16
- Drizzle ORM
- Drizzle Kit for migrations

### Infrastructure
- Pulumi (TypeScript) for IaC
- AWS (VPC, RDS, ECS, S3, CloudFront, SES, etc.)

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** 20.0.0 or higher
- **pnpm** 9.0.0 or higher (package manager)
- **Docker** & **Docker Compose** (for local development)
- **Git** (for version control)

### Optional (for deployment)

- **AWS account** with appropriate permissions
- **Pulumi CLI** ([Installation guide](https://www.pulumi.com/docs/get-started/install/))
- **Stripe account** (test mode for development, production for deployment)

## Getting Started

### 1. Clone and Install

```bash
git clone <repo-url>
cd typescript-starter
pnpm install
```

### 2. Environment Variables

Create a `.env.local` file in the `apps/web` directory with the following variables:

```bash
cd apps/web
touch .env.local
```

**Required variables:**

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Authentication
BETTER_AUTH_SECRET=your-secret-key-min-32-characters-long
BETTER_AUTH_URL=http://localhost:3000

# Application
NEXT_PUBLIC_APP_URL=http://localhost:3000
NODE_ENV=development
```

**Optional variables (for full functionality):**

```env
# OAuth Providers (optional)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
APPLE_CLIENT_ID=your-apple-client-id
APPLE_CLIENT_SECRET=your-apple-client-secret

# Stripe (optional, for payments)
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# AWS SES (optional, for emails)
AWS_SES_REGION=us-east-1
AWS_SES_FROM_EMAIL=noreply@yourdomain.com
AWS_SES_FROM_NAME=Your App Name

# Redis (optional, for rate limiting)
UPSTASH_REDIS_REST_URL=https://...
UPSTASH_REDIS_REST_TOKEN=...

# Monitoring (optional)
SENTRY_DSN=https://...
NEXT_PUBLIC_SENTRY_DSN=https://...
NEXT_PUBLIC_POSTHOG_KEY=phc_...
NEXT_PUBLIC_POSTHOG_HOST=https://app.posthog.com
```

> **Note:** Generate `BETTER_AUTH_SECRET` using: `openssl rand -base64 32`

### 3. Start Local Services

Start PostgreSQL and Redis using Docker Compose:

```bash
# From the project root
docker-compose up -d
```

This will start:
- **PostgreSQL 16** on port `5432`
- **Redis 7** on port `6379`

Verify services are running:

```bash
docker ps
```

You should see both `postgres` and `redis` containers running.

### 4. Database Setup

Set up the database schema and seed initial data:

```bash
# Navigate to the web app
cd apps/web

# Generate database migrations from schema
pnpm db:generate

# Apply migrations to the database
pnpm db:migrate

# (Optional) Seed the database with sample data
pnpm db:seed
```

> **Tip:** Use `pnpm db:studio` to open Drizzle Studio, a visual database browser.

### 5. Start Development Server

Start the development server:

```bash
# From the project root
pnpm dev
```

Or from the web app directory:

```bash
cd apps/web
pnpm dev
```

The application will be available at [http://localhost:3000](http://localhost:3000).

> **Note:** The dev server uses Turbopack by default for faster builds. If you encounter issues, you can run without Turbopack by modifying the `dev` script in `apps/web/package.json`.

## 📁 Project Structure

```
typescript-starter/
├── apps/
│   └── web/                          # Next.js application
│       ├── app/                      # App Router (Next.js 16)
│       │   ├── [locale]/            # Internationalized routes
│       │   │   ├── (auth)/          # Authentication routes
│       │   │   ├── (dashboard)/     # Protected dashboard routes
│       │   │   ├── (marketing)/     # Public marketing pages
│       │   │   └── blog/            # Blog pages (MDX)
│       │   ├── api/                 # API routes
│       │   │   ├── auth/           # Auth endpoints
│       │   │   ├── trpc/           # tRPC handler
│       │   │   ├── sse/            # Server-Sent Events
│       │   │   └── webhooks/       # Webhook handlers
│       │   ├── sitemap.ts          # Dynamic sitemap
│       │   └── robots.ts            # Dynamic robots.txt
│       ├── components/              # React components
│       │   ├── ui/                  # shadcn/ui components
│       │   ├── auth/               # Auth components
│       │   ├── dashboard/          # Dashboard components
│       │   └── todos/              # Todo components
│       ├── lib/                     # Utilities and configurations
│       │   ├── i18n/               # Internationalization
│       │   ├── auth.ts             # Auth configuration
│       │   ├── db.ts               # Database client
│       │   ├── trpc.ts             # tRPC setup
│       │   └── stripe.ts           # Stripe integration
│       ├── server/                  # Server-side code
│       │   ├── db/                 # Database schema & queries
│       │   ├── trpc/               # tRPC routers & procedures
│       │   └── services/           # Business logic services
│       ├── emails/                  # React Email templates
│       ├── content/                 # MDX blog posts
│       ├── messages/                # i18n translation files
│       ├── drizzle/                 # Database migrations
│       ├── tests/                   # Test files
│       │   ├── e2e/                # Playwright E2E tests
│       │   ├── integration/        # Integration tests
│       │   └── unit/               # Unit tests
│       └── scripts/                 # Utility scripts
│
├── packages/
│   └── infrastructure/              # Pulumi infrastructure as code
│       ├── database.ts             # RDS configuration
│       ├── compute.ts              # ECS configuration
│       ├── network.ts              # VPC configuration
│       └── ...
│
├── docker-compose.yml               # Local development services
├── turbo.json                       # Turborepo configuration
├── pnpm-workspace.yaml              # pnpm workspace config
└── README.md                        # This file
```

## 🛠️ Development

### Available Scripts

Run these commands from the project root or from `apps/web`:

#### Development
```bash
pnpm dev              # Start development server (with Turbopack)
pnpm build            # Build for production
pnpm start            # Start production server (after build)
```

#### Database
```bash
pnpm db:generate      # Generate migrations from schema changes
pnpm db:migrate       # Apply migrations to database
pnpm db:push          # Push schema directly (dev only, no migrations)
pnpm db:studio        # Open Drizzle Studio (visual DB browser)
pnpm db:seed          # Seed database with sample data
```

#### Testing
```bash
pnpm test             # Run unit and integration tests (Vitest)
pnpm test:ui          # Run tests with interactive UI
pnpm test:coverage    # Run tests with coverage report
pnpm test:e2e         # Run end-to-end tests (Playwright)
pnpm test:e2e:ui      # Run E2E tests with Playwright UI
```

#### Code Quality
```bash
pnpm lint             # Lint code with Biome
pnpm lint:fix         # Fix linting issues automatically
pnpm format           # Format code with Biome
pnpm type-check       # Type check with TypeScript
```

#### Email Development
```bash
pnpm email:dev        # Start email preview server
```

#### Docker
```bash
pnpm docker:build     # Build Docker image
pnpm docker:run       # Run Docker container
```

### Database Management

**Drizzle Studio** - Visual database browser:

```bash
pnpm db:studio
```

Opens a web interface at `http://localhost:4983` where you can:
- Browse tables and data
- Run queries
- Edit records
- View relationships

### Email Preview

Preview React Email templates locally:

```bash
pnpm email:dev
```

This starts a development server where you can preview all email templates.

### Type Safety

This project uses **end-to-end type safety**:
- Database schema → TypeScript types (Drizzle)
- API routes → Type-safe clients (tRPC)
- Environment variables → Validated at runtime (Zod)
- Component props → TypeScript interfaces

Run `pnpm type-check` to verify type safety across the entire codebase.

## 🚀 Deployment

This project uses **Pulumi** for infrastructure as code on **AWS**. For detailed deployment instructions, see the [Deployment Guide](./docs/DEPLOYMENT.md).

### Quick Start

1. **Install Pulumi CLI**: [Installation guide](https://www.pulumi.com/docs/get-started/install/)

2. **Configure AWS credentials**:
   ```bash
   aws configure
   ```

3. **Initialize and deploy infrastructure**:
   ```bash
   cd packages/infrastructure
   pulumi stack init production
   pulumi config set aws:region us-east-1
   pulumi preview  # Review changes
   pulumi up       # Deploy
   ```

### What Gets Deployed

- **VPC** - Isolated network environment
- **RDS PostgreSQL** - Managed database
- **ECS Fargate** - Containerized application
- **Application Load Balancer** - Traffic distribution
- **S3 + CloudFront** - Static asset hosting
- **AWS SES** - Email delivery
- **Secrets Manager** - Secure environment variables

See [docs/DEPLOYMENT.md](./docs/DEPLOYMENT.md) for complete deployment guide.

## 🧪 Testing

This project includes comprehensive testing setup. For detailed testing documentation, see the [Testing Guide](./docs/TESTING.md).

### Quick Start

```bash
# Run all tests
pnpm test

# Run E2E tests
pnpm test:e2e

# Run with coverage
pnpm test:coverage
```

### Test Structure

- **Unit Tests** (`tests/unit/`) - Test individual functions and utilities
- **Integration Tests** (`tests/integration/`) - Test API endpoints and tRPC procedures
- **E2E Tests** (`tests/e2e/`) - Test full user flows with Playwright

See [docs/TESTING.md](./docs/TESTING.md) for complete testing guide.

## 📚 Documentation

- **[API Documentation](./docs/API.md)** - Complete tRPC API reference
- **[Deployment Guide](./docs/DEPLOYMENT.md)** - Step-by-step AWS deployment
- **[Testing Guide](./docs/TESTING.md)** - Testing strategies and examples

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Run quality checks**:
   ```bash
   pnpm lint
   pnpm type-check
   pnpm test
   ```
5. **Commit your changes**: `git commit -m 'Add amazing feature'`
6. **Push to your branch**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

### Code Style Guidelines

- **Linting**: Use Biome (configured in `biome.json`)
- **TypeScript**: Follow strict mode, avoid `any` types
- **Naming**: Use meaningful, descriptive names
- **Formatting**: Run `pnpm format` before committing
- **Testing**: Add tests for new features
- **Documentation**: Update docs for significant changes

## 🔧 Troubleshooting

### Database Connection Issues

**Problem**: Cannot connect to PostgreSQL

**Solutions**:
- Verify Docker containers are running: `docker ps`
- Check `DATABASE_URL` in `.env.local` matches docker-compose.yml
- Ensure database exists: `docker exec -it postgres psql -U user -d dbname`
- Restart containers: `docker-compose restart`

### Build Errors

**Problem**: Build fails with cryptic errors

**Solutions**:
- Clear Next.js cache: `rm -rf apps/web/.next`
- Clear Turbo cache: `pnpm clean`
- Reinstall dependencies: `rm -rf node_modules && pnpm install`
- Check Node.js version: `node --version` (should be 20+)

### Type Errors

**Problem**: TypeScript errors in IDE or build

**Solutions**:
- Run type check: `pnpm type-check`
- Restart TypeScript server in your IDE
- Ensure all dependencies are installed: `pnpm install`
- Check `tsconfig.json` paths are correct

### Port Already in Use

**Problem**: Port 3000 is already in use

**Solutions**:
- Find process using port: `lsof -i :3000` (macOS/Linux) or `netstat -ano | findstr :3000` (Windows)
- Kill the process or change port in `package.json`: `next dev -p 3001`

### Environment Variables Not Loading

**Problem**: Environment variables are undefined

**Solutions**:
- Ensure `.env.local` is in `apps/web/` directory
- Check variable names match `env.ts` schema
- Restart dev server after changing `.env.local`
- Verify no typos in variable names

### Migration Issues

**Problem**: Database migrations fail

**Solutions**:
- Check database connection: `pnpm db:studio`
- Verify migration files in `apps/web/drizzle/`
- Reset database (dev only): `pnpm db:push` (drops and recreates)
- Check for conflicting migrations

### Still Having Issues?

- Check the project's GitHub Issues for similar problems
- Review the [Deployment Guide](./docs/DEPLOYMENT.md) for production issues
- Ensure all prerequisites are installed correctly

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Next.js](https://nextjs.org/) - The React framework
- [Drizzle ORM](https://orm.drizzle.team/) - TypeScript ORM
- [tRPC](https://trpc.io/) - End-to-end typesafe APIs
- [Better Auth](https://www.better-auth.com/) - Authentication library
- [Pulumi](https://www.pulumi.com/) - Infrastructure as code
- [shadcn/ui](https://ui.shadcn.com/) - UI components
- [Turborepo](https://turbo.build/) - Monorepo build system

---

**Built with ❤️ using modern web technologies**

