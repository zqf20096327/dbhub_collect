# Invoice Management System - TanStack Start + Cloudflare

A modern invoice management system built with TanStack Start, Cloudflare D1, and feature-based architecture.

## 🚀 Getting Started

### Install the dependencies

```bash
pnpm i
```

### Start the development server

```bash
pnpm dev
```

### Build for Production

```bash
pnpm build
```

### Preview the production build

```bash
pnpm preview
```

### Deploy to Cloudflare

```sh
pnpm run deploy
```

## 🏗️ Project Architecture

### Feature-Based Organization

This project uses a **feature-based architecture** where each business domain is organized as a self-contained feature with its own components, hooks, services, and types.

```
src/
├── features/           # Business features (main application logic)
├── components/         # Shared UI components (shadcn/ui)
├── routes/            # TanStack Router pages
├── lib/               # Shared utilities & configurations
├── hooks/             # Global hooks
└── utils/             # Helper functions
```

## 🎯 How to Determine Features

### 1. **Business Domain Approach** (Recommended)

Think about the main business domains/capabilities your app provides:

#### Current Features:
- **`auth/`** - User authentication & authorization
- **`invoices/`** - Invoice creation, management, payments
- **`customers/`** - Customer management, Telegram integration
- **`products/`** - Product/service catalog
- **`dashboard/`** - Analytics, reports, overview
- **`settings/`** - User preferences, company settings
- **`notifications/`** - Email/Telegram notifications

#### Future Features:
- **`reports/`** - Advanced reporting & analytics
- **`billing/`** - Subscription management
- **`integrations/`** - Third-party API integrations
- **`mobile/`** - Mobile-specific components

### 2. **Feature Identification Questions**

Ask yourself:
- ✅ **Does this have its own data model?** (Users, Invoices, Products)
- ✅ **Does this have unique business rules?** (Invoice calculations, auth flows)
- ✅ **Would this be a separate microservice?** (In a distributed system)
- ✅ **Does this have 3+ related components?** (List, Form, Detail views)

### 3. **Feature Structure Template**

```
src/features/[feature-name]/
├── components/          # Feature-specific UI components
│   ├── [FeatureName]List.tsx
│   ├── [FeatureName]Form.tsx
│   ├── [FeatureName]Detail.tsx
│   └── index.ts        # Barrel export
├── hooks/              # Feature-specific hooks
│   ├── use[FeatureName].ts
│   ├── use[FeatureName]Query.ts
│   └── index.ts
├── services/           # API calls & business logic
│   ├── [featureName]Service.ts
│   └── index.ts
├── types/             # Feature-specific TypeScript types
│   ├── [featureName].types.ts
│   └── index.ts
├── utils/             # Feature-specific utilities
│   └── [featureName]Utils.ts
└── index.ts           # Main feature export
```

## 📁 Current Feature Examples

### Auth Feature
```typescript
// src/features/auth/
├── components/
│   ├── LoginForm.tsx           # Login form UI
│   ├── RegisterForm.tsx        # Registration form
│   ├── AuthProvider.tsx        # Auth context provider
│   └── ProtectedRoute.tsx      # Route protection
├── hooks/
│   ├── useAuth.ts              # Auth state management
│   ├── useLogin.ts             # Login business logic
│   └── useRegister.ts          # Registration logic
├── services/
│   └── authService.ts          # Auth API calls
└── types/
    └── auth.types.ts           # User, Session types
```

### Invoice Feature (Planned)
```typescript
// src/features/invoices/
├── components/
│   ├── InvoiceList.tsx         # Invoice listing
│   ├── InvoiceForm.tsx         # Create/edit invoice
│   ├── InvoiceDetail.tsx       # Invoice viewer
│   ├── InvoiceItems.tsx        # Line items management
│   └── PaymentTracker.tsx      # Payment status
├── hooks/
│   ├── useInvoices.ts          # Invoice CRUD
│   ├── useInvoiceCalculations.ts # Tax/total calculations
│   └── usePayments.ts          # Payment tracking
├── services/
│   ├── invoiceService.ts       # Invoice API
│   └── paymentService.ts       # Payment processing
└── types/
    ├── invoice.types.ts        # Invoice, InvoiceItem types
    └── payment.types.ts        # Payment types
```

## 🔧 Creating a New Feature

### 1. Use the Feature Generator (Recommended)
```bash
# Create new feature scaffold
pnpm create:feature <feature-name>
```

### 2. Manual Creation
```bash
# Create feature directory
mkdir -p src/features/my-feature/{components,hooks,services,types}

# Create barrel exports
touch src/features/my-feature/{components,hooks,services,types}/index.ts
touch src/features/my-feature/index.ts
```

### 3. Feature Integration
```typescript
// 1. Create route in src/routes/
export const Route = createFileRoute('/my-feature')({
  component: MyFeaturePage,
})

function MyFeaturePage() {
  return <MyFeatureList /> // Import from feature
}

// 2. Export from feature
// src/features/my-feature/index.ts
export { MyFeatureList } from './components'
export { useMyFeature } from './hooks'
```

## 🗄️ Database Integration

### D1 Database Setup
```typescript
// Access D1 in server functions
import { env } from 'cloudflare:workers'

export async function getInvoices() {
  const db = env.INVOICE_DB // D1 binding
  return await db.prepare("SELECT * FROM invoices").all()
}
```

### Drizzle ORM Integration
```typescript
// src/lib/db.ts
import { drizzle } from 'drizzle-orm/d1'
import { invoices } from './schema'

export function createDB(d1: D1Database) {
  return drizzle(d1, { schema })
}
```

## 📋 Feature Checklist

When creating a new feature, ensure:

- [ ] **Components** - UI components with proper TypeScript
- [ ] **Hooks** - Business logic separated from UI
- [ ] **Services** - API calls and external integrations
- [ ] **Types** - Full TypeScript coverage
- [ ] **Tests** - Unit tests for hooks and services
- [ ] **Documentation** - Feature-specific README if complex
- [ ] **Route Integration** - Properly connected to TanStack Router
- [ ] **Database Schema** - D1/Drizzle schema if data-driven

## 🚀 Deployment

### Cloudflare Bindings

Access Cloudflare resources in server functions:

```typescript
import { env } from 'cloudflare:workers'

// D1 Database
const invoices = await env.INVOICE_DB.prepare("SELECT * FROM invoices").all()

// KV Storage
const cached = await env.MY_KV.get("key")

// R2 Storage
const file = await env.MY_BUCKET.get("file.pdf")
```

### Environment Variables
```bash
# .dev.vars (local development)
CLOUDFLARE_ACCOUNT_ID=your-account-id
CLOUDFLARE_DATABASE_ID=your-db-id
```

## 📖 Additional Resources

- [TanStack Start Docs](https://tanstack.com/start)
- [Cloudflare D1 Docs](https://developers.cloudflare.com/d1/)
- [Drizzle ORM Docs](https://orm.drizzle.team/)
- [Feature-Driven Architecture](https://feature-sliced.design/)
