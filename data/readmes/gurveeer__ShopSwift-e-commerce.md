# 👜 ShopSwift E-Commerce Platform

Modern e-commerce solution built with React, TypeScript, and SQLite

## Features

- 🛍️ Product browsing with category filters
- 🔐 JWT-based user authentication
- 🛒 Persistent shopping cart
- 📊 Admin dashboard with inventory management
- 🚀 Vite-powered frontend
- 🎨 Tailwind CSS styling

## UI

**Homepage - Product Browsing**

![Homepage with product listings](image/README/1742975262057.png) 


![1742975336838](image/README/1742975336838.png)

**Admin Dashboard**

![1742975391718](image/README/1742975391718.png)

![1742975434887](image/README/1742975434887.png)

![1742975457095](image/README/1742975457095.png)

## Technologies

- Architecture: Clean Architecture with separation between presentation, application, and infrastructure layers
- API Layer: RESTful endpoints with JWT authentication middleware
- State Management: Global store using React Query for server state and Zustand for UI state

## Project Structure

```
├── client/            # React frontend
├── server/            # Express backend
├── shared/            # Shared types and utilities
├── migrations/        # Database schema versions
└── attached_assets/   # Design documents & resources
```

- Frontend: React 18, TypeScript, Vite
- State Management: React Query
- UI: Shadcn UI, Lucide Icons
- Backend: Node.js, Express
- Database: SQLite (Drizzle ORM)

## Installation

```bash
cd client
npm install
cd ../server
npm install
```

## Environment Variables

| Variable     | Description               | Required | Default                 |
| ------------ | ------------------------- | -------- | ----------------------- |
| VITE_API_URL | Backend API base URL      | Yes      | http://localhost:5000   |
| DATABASE_URL | SQLite database path      | Yes      | file:../database.sqlite |
| JWT_SECRET   | Secret for signing tokens | Yes      | -                       |
| NODE_ENV     | Runtime environment       | No       | development             |

1. Create `.env` file:

```env
VITE_API_URL=http://localhost:5000
DATABASE_URL=file:../database.sqlite
JWT_SECRET=your_secure_secret
```

## Database Setup

```bash
npm run migrate
```

## API Endpoints

### Authentication

- `POST /api/auth/register` User registration
- `POST /api/auth/login` User authentication
- `GET /api/auth/me` Get current user

### Products

- `GET /api/products` List all products
- `GET /api/products/:id` Get product details
- `POST /api/products` Create new product (admin)

### Orders

- `POST /api/orders` Create new order
- `GET /api/orders` List user orders
- `GET /api/orders/:id` Get order details

```bash
# Frontend
cd client
npm run dev

# Backend
cd ../server
npm start
```

## Admin Access

1. Register with admin email pattern (username: admin, Password: admin123)
2. Navigate to `/admin`

## Deployment

1. **Production Build**

```bash
cd client && npm run build
cd ../server && npm run build
```

2. **Docker Setup**

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
CMD ["node", "dist/server.js"]
```

3. **Hosting Recommendations**

- Frontend: Vercel/Netlify
- Backend: Railway/Render
- Database: Supabase/AWS RDS

## Contributing

### Development Workflow

1. Create feature branch from `develop`
2. Write tests for new features
3. Update TypeScript definitions
4. Document API changes
5. Submit PR with Linter checks passing

### Code Standards

- Type Safety: Strict TypeScript enforcement
- Formatting: Prettier with project settings
- Testing: 80% coverage minimum
- Documentation: JSDoc for complex functions

PRs welcome! Please follow existing code patterns and add tests for new features.
