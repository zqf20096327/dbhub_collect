# BITEX E-Commerce

## Full Stack E-Commerce Website (+ Dashboard) with Next.js 16: React, Typescript, Tailwindcss, Prisma, PostgreSQL, NextAuth, Redux

![Fullstack E-Commerce Website](https://res.cloudinary.com/drokemaoa/image/upload/v1709638892/bitexPoster.png)

## Overview

Bitex is a full-stack E-Commerce project developed with Next.js 16, featuring a range of technologies including React, Typescript, Tailwindcss, Prisma, PostgreSQL, NextAuth, and Redux.

⚠️ `Note:` This project is a personal endeavor created for portfolio purposes and is not associated with any real business or project.

---

## 📦 Monorepo

This repository is now structured as a **Turborepo monorepo** managed with `pnpm` workspaces. The Next.js storefront lives in `apps/store`, and shared code is published under `packages/*`.

---

## 🗄️ Looking for the original MongoDB version?

> ### 🧭 `main` is now **Turborepo + PostgreSQL**
>
> The original **single-package, MongoDB** codebase has been **preserved unchanged** on a dedicated branch:
>
> ### 👉 Branch: [`legacy/mongo-monolith`](https://github.com/HosseinNamvar/bitex/tree/legacy/mongo-monolith)
>
> Check it out locally with:
>
> ```shell
> git checkout legacy/mongo-monolith
> ```
>
> Use this branch if you want to see the project as it was **before** the monorepo restructure and the Postgres migration. It is kept for historical / portfolio reference and is **not** receiving new updates.

---

## 🔗 Live Version

[https://bitex.namvar.dev](https://bitex.namvar.dev) ⤴️

---

### 🖥️ Admin Dashboard Features

#### 🔐 Authentication

- Credential authentication for Dashboard using NextAuth.

#### 📁 Category Management

- Advanced category management, including combining categories.
- Add, update, and delete categories and subcategories.
- Dedicated **specifications** for every category.

#### 🏭 Brands and Products

- Add and delete products with category-specific specifications.
- Add, update, and delete brands.

#### 📋 Traffic Report

- Reports on user page visits.

---

### 🛍️ E-Commerce Store Features

#### 🎨 UI Features

- Full responsiveness
- CSS animations and effects
- Skeleton loadings (without using external library )to have seamless page navigation experience.
- Custom made UI Components (no external library):

  - Price range slider
  - CheckBox
  - DropDownList
  - Popups
  - Button

- Interactive Homepage Slider

  - Crafted from scratch without using any Library
  - Supports both Mouse Drag and `TouchInput`

- Shopping cart management with **Redux**.
- Product gallery to showcase items attractively.
- Dynamically Loading Categories (List) from Database

#### 🔍 Filter and Sort

- Advanced filters products by Price, Brand, and Availability.
- Sorting options in product list page (sort by name and price).

#### ⚙️ Backend

- Interaction with PostgreSQL database using Prisma ORM.
- Relational schema with Prisma migrations (see `apps/store/prisma/migrations/`).
- Server-side form data validation using ZOD.

## 🚀 Getting Started

### 💾 Cloning the repository

```shell
git clone https://github.com/HosseinNamvar/bitex.git
```

### 📥 Install packages

From the repository root (pnpm workspaces):

```shell
pnpm install
```

### 🛠️ Setup .env file

Create `apps/store/.env` with:

```shell
DATABASE_URL=        # PostgreSQL connection string, e.g. postgresql://user:pass@host:5432/bitex
NEXTAUTH_SECRET=
CLOUDINARY_URL=      # Hosting address for product images
```

#### ⬆️ Setup Prisma

Apply the committed Postgres migrations:

```shell
pnpm --filter bitex-store exec prisma migrate deploy
```

For local development against a fresh database, you can use:

```shell
pnpm --filter bitex-store exec prisma migrate dev
```

#### 🚀 Start the app

From the repo root (runs through Turborepo):

```shell
pnpm dev
```
