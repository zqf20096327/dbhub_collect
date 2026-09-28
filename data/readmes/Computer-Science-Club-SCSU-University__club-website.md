# CS Club Website

A modern, full-stack web platform for university Computer Science Club management and public engagement. Built with Next.js, Django REST Framework, and PostgreSQL.

## 🏗️ Architecture

This is a **monorepo** containing three main applications:

- **`apps/public-website/`** - Public-facing Next.js website
- **`apps/officers-hub/`** - Officer management dashboard (Clerk-authenticated)
- **`apps/backend/`** - Django REST API backend
- **`packages/ui/`** - Shared UI components library

### Tech Stack

- **Frontend**: Next.js 15, React 19, TypeScript, Tailwind CSS
- **Backend**: Django 5.x, Django REST Framework, PostgreSQL
- **Authentication**: Clerk (officers-hub), Public API (web)
- **UI Components**: shadcn/ui, Aceternity UI
- **Build System**: Turbo (monorepo), pnpm
- **Deployment**: TBD (GitHub Actions planned)

## 🚀 Quick Start

### Prerequisites

- **Docker Desktop** (includes Docker and Docker Compose)
- **Node.js** >= 20 (for local development outside Docker)
- **pnpm** (package manager)

### 1. Clone & Setup

```bash
git clone <repository-url>
cd club-website

# Install dependencies and setup database
pnpm setup

# Optional: Create .env file only if you need to override defaults
# cp env.example .env
```

### 2. Run the Application

```bash
# Start all services (frontend, backend, database)
pnpm dev

# Or run in detached mode
pnpm dev:detached

# View logs
pnpm logs
```

### 3. Stop Services

```bash
# Stop all services
pnpm cleanup

# Stop and remove volumes (deletes database data)
pnpm cleanup:volumes
```

### 🌐 Access Points

Once running, access the applications at:
- **Public Website**: http://localhost:3000
- **Officers Hub**: http://localhost:3001 (requires Clerk authentication)
- **Django API**: http://localhost:8000/api

### 🛠️ Useful Commands

```bash
# Database operations
pnpm db:migrate          # Run database migrations
pnpm db:makemigrations   # Create new migrations
pnpm db:shell            # Access PostgreSQL shell

# Django operations
pnpm api:shell           # Access Django shell

# Development
pnpm logs                # View all service logs
pnpm logs api            # View specific service logs
```

## 📁 Project Structure

```
cs-club-website/
├── apps/
│   ├── public-website/        # Public Next.js website
│   │   ├── app/               # App router pages
│   │   ├── components/        # React components
│   │   ├── hooks/            # Custom React hooks
│   │   └── lib/              # Utilities & API client
│   ├── officers-hub/          # Officer dashboard
│   │   ├── app/              # Protected dashboard pages
│   │   ├── components/       # Dashboard components
│   │   ├── hooks/           # Officer-specific hooks
│   │   └── middleware.ts    # Clerk authentication
│   └── backend/              # Django REST API
│       ├── api/             # Main API app
│       │   ├── models/      # Database models
│       │   ├── services/    # Business logic
│       │   ├── views/       # API endpoints
│       │   ├── serializers/ # Data transformation
│       │   └── permissions/ # Access control
│       └── backend/         # Django settings
├── packages/
│   ├── ui/                   # Shared component library
│   ├── eslint-config/       # Shared ESLint config
│   └── typescript-config/   # Shared TypeScript config
└── db/
    └── schema.sql           # Database schema reference
```

## 🔧 Environment Configuration

**No configuration required!** The project includes sensible defaults for all environment variables in `docker-compose.yml`, including test Clerk authentication keys.

### Optional: Custom Configuration

Only create a `.env` file if you need to override the defaults (e.g., using your own Clerk keys):

```bash
# Copy the example file
cp env.example .env

# Edit with your custom values
# Most commonly changed: Clerk authentication keys
```

See `env.example` for all available configuration options. The most common customization is adding your own Clerk keys from https://dashboard.clerk.com.

## 🎯 Features

### Public Website (`apps/public-website`)
- ✅ **Events**: Browse upcoming CS Club events
- ✅ **Announcements**: Latest club news and updates
- ✅ **Officers**: Meet the current leadership team
- ✅ **About**: Club information and mission
- ✅ **RSVP System**: Public event registration
- ✅ **Responsive Design**: Mobile-first approach
- ✅ **Dark/Light Mode**: System-aware theming

### Officers Hub (`apps/officers-hub`)
- ✅ **Authentication**: Clerk-based officer login
- ✅ **Dashboard**: Overview of club metrics
- ✅ **Event Management**: Create, edit, delete events
- ✅ **Announcement Management**: Publish club updates
- ✅ **Officer Management**: Manage team profiles
- ✅ **RSVP Tracking**: View event registrations
- ✅ **Protected Routes**: Officer-only access

### Backend API (`apps/backend`)
- ✅ **REST API**: Clean, documented endpoints
- ✅ **Authentication**: Clerk JWT verification
- ✅ **Public Endpoints**: Events, announcements, officers
- ✅ **Officer Endpoints**: CRUD operations
- ✅ **Database**: PostgreSQL with proper schema
- ✅ **Clean Architecture**: Services, models, views separation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Follow the existing code style and architecture
4. Test your changes thoroughly
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Development Guidelines

- **Separation of Concerns**: Keep business logic in services, UI logic in components
- **Type Safety**: Use TypeScript throughout, avoid `any` types
- **Responsive Design**: Mobile-first approach with Tailwind CSS
- **Accessibility**: Follow WCAG guidelines
- **Performance**: Optimize images, lazy load components, minimize bundle size

## 🤝 Contributing

We welcome contributions from everyone! Whether you're fixing bugs, adding features, or improving documentation, your help is appreciated.

Please read our [Contributing Guide](CONTRIBUTING.md) for detailed instructions on how to get started.

### Quick Start for Contributors

```bash
# Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/club-website.git
cd club-website

# Set up the development environment
pnpm setup

# Start developing
pnpm dev
```

### Looking for something to work on?

Check out our [open issues](https://github.com/your-org/club-website/issues), especially those tagged with:
- `good first issue` - Perfect for beginners
- `help wanted` - We need your help!
- `documentation` - Help improve our docs

## ✨ Contributors

Thanks to all our amazing contributors! 🎉

<a href="https://github.com/Computer-Science-Club-SCSU-University/club-website/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Computer-Science-Club-SCSU-University/club-website" />
</a>

Made with [contrib.rocks](https://contrib.rocks).

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- CS Club members and officers for their continuous support
- Our university for providing resources and guidance
- The open-source community for amazing tools and libraries

---
