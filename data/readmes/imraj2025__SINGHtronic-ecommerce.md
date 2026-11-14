<div align="center">
  <img src="public/logo%20v1%20svg.svg" alt="SINGHtronic Logo" width="260" />

  # SINGHtronic — Full-Stack Electronics E-Commerce & Admin Platform

  **A production-grade B2C electronics storefront and enterprise admin dashboard built with Next.js 15, Node.js/Express, Prisma ORM, and Serverless MySQL (TiDB Cloud).**

  [![Live Demo](https://img.shields.io/badge/Live_Storefront-Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://singhtronic-ecommerce.vercel.app)
  [![Backend API](https://img.shields.io/badge/REST_API-Render-46E3B7?style=for-the-badge&logo=render&logoColor=black)](https://singhtronic-ecommerce.onrender.com/api/products)
  [![Next.js](https://img.shields.io/badge/Next.js_15-black?style=for-the-badge&logo=next.js&logoColor=white)](https://nextjs.org/)
  [![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
  [![Prisma](https://img.shields.io/badge/Prisma_ORM-2D3748?style=for-the-badge&logo=prisma&logoColor=white)](https://www.prisma.io/)
  [![TiDB Cloud](https://img.shields.io/badge/MySQL-TiDB_Cloud-DC143C?style=for-the-badge&logo=mysql&logoColor=white)](https://tidbcloud.com/)
</div>

---

## Overview

**SINGHtronic** is a full-stack e-commerce web application engineered with a decoupled architecture:
- **Customer Storefront:** Dynamic server-rendered catalog (`Next.js App Router`), multi-parameter filtering (category, price range in INR, customer ratings, stock status), real-time search, persistent cart and wishlist (`Zustand`), and user notifications.
- **Enterprise Admin Dashboard (`/admin`):** Role-Based Access Control (`NextAuth.js`) governing full CRUD workflows for products, categories, merchants, customer orders, user accounts, and batch CSV inventory uploads.
- **Hardened REST API (`/server`):** Express.js service featuring rate limiting (`express-rate-limit`), input sanitization, structured request logging, and strict CORS validation.

---

## Live Deployment Architecture

| Layer | Technology | Hosting Provider | Production Endpoint |
| :--- | :--- | :--- | :--- |
| **Frontend & SSR** | Next.js 15, React, TypeScript, Tailwind CSS, DaisyUI | **Vercel** | [singhtronic-ecommerce.vercel.app](https://sing-htronic-ecommerce-amber.vercel.app/) |
| **Backend REST API** | Node.js, Express.js, Rate Limiter, CORS | **Render** | [singhtronic-ecommerce.onrender.com](https://singhtronic-ecommerce.onrender.com/api/products) |
| **Database & ORM** | MySQL (TLS/SSL Strict), Prisma ORM | **TiDB Cloud** | AWS Regional Serverless Cluster |

---

## Key Features

### Storefront Experience
- **Dynamic Catalog & SSR:** Server-rendered featured products and category views with `no-store` cache invalidation for real-time inventory accuracy.
- **Multi-Faceted Search & Filtering:** Filter by product category (`/shop/[[...slug]]`), dynamic price ceiling, minimum star rating, stock availability, and sort order.
- **Persistent State Management:** Client-side cart, wishlist, pagination, sorting, and notification stores powered by **Zustand**.
- **Authentication & Session Security:** Credentials and OAuth-ready authentication via **NextAuth.js**, protected routes via Next.js middleware, and automatic idle session timeout handling.

### Admin Dashboard (`/admin`)
- **Product & Inventory CRUD:** Create, update, and delete products with custom slugs, stock status, category mapping, and gallery images.
- **Batch CSV Upload Engine:** Upload multi-row CSV catalogs with validation, batch history tracking, and rollback support (`/admin/bulk-upload`).
- **Order & Merchant Management:** Track customer order lifecycles, line items, and multi-merchant associations.
- **User & Role Administration:** Manage registered accounts and elevate privileges between `user` and `admin` roles.

---

## Project Structure

```text
SINGHtronic-ecommerce/
├── app/                        # Next.js App Router pages, layouts & API routes
│   ├── (dashboard)/admin/      # Protected Admin Dashboard routes (Products, Orders, Users, CSV Upload)
│   ├── _zustand/               # Zustand global stores (cart, wishlist, notifications, pagination, sort)
│   ├── api/                    # NextAuth ([...nextauth]) & user registration routes
│   ├── cart/ & checkout/       # Shopping cart and checkout workflows
│   ├── product/[productSlug]/  # Dynamic product detail pages
│   └── shop/[[...slug]]/       # Category & filtered catalog views
├── components/                 # Reusable UI & dashboard components
├── hooks/                      # Custom React hooks (notifications, session timeout)
├── lib/                        # API client, environment config, & input sanitizers
├── prisma/                     # Root Prisma schema & migrations for NextAuth/SSR
├── public/                     # Static product assets, icons, & SINGHtronic vector branding
└── server/                     # Standalone Node.js + Express REST API
    ├── controllers/            # Route handlers (products, orders, categories, merchants, bulk-upload)
    ├── middleware/             # Rate limiting & request validation
    ├── prisma/                 # Backend Prisma schema
    ├── routes/                 # Express routers
    └── utills/                 # Database seeding script (insertDemoData.js)
```

---

## Local Development Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/imraj2025/SINGHtronic-ecommerce.git](https://github.com/imraj2025/SINGHtronic-ecommerce.git)
cd SINGHtronic-ecommerce
```

### 2. Configure Environment Variables
Create a `.env` file in the **root** directory:
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:3001
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your_nextauth_secret_key
DATABASE_URL="mysql://USER:PASSWORD@HOST:4000/test?sslaccept=strict"
```

Create a `.env` file in the **`/server`** directory:
```env
NODE_ENV=development
PORT=3001
FRONTEND_URL=http://localhost:3000
DATABASE_URL="mysql://USER:PASSWORD@HOST:4000/test?sslaccept=strict"
```

### 3. Install Dependencies & Seed the Database
```bash
# Install root frontend dependencies
npm install --legacy-peer-deps
npx prisma generate

# Install backend dependencies & push schema
cd server
npm install
npx prisma generate
npx prisma db push

# Seed initial merchant, categories, and 30 electronics products
cd utills
node insertDemoData.js
```

### 4. Run the Application
Open two terminals:
```bash
# Terminal 1: Start Express Backend (Port 3001)
cd server
node app.js

# Terminal 2: Start Next.js Frontend (Port 3000)
npm run dev
```
Visit `http://localhost:3000` for the storefront or `http://localhost:3000/admin` for the admin dashboard.

---

## Author

**Rajan Singh**
- GitHub: [@imraj2025](https://github.com/imraj2025)