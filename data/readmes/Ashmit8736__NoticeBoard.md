# Reno Platforms Notice Board — Web Development Assignment

A responsive, state-of-the-art Notice Board web application built with **Next.js (Pages Router)**, **Prisma ORM**, and **Tailwind CSS**. It supports end-to-end Create, Read, Update, and Delete (CRUD) operations with strict server-side validation and advanced database-level functionality like Search, Pagination, and Priority sorting.

---

## 🚀 Features & Evaluation Criteria Handled

### Full CRUD via API Routes (`/api/notices`):
- **GET `/api/notices`**: Fetches notices with advanced **Search** (by title/body) and **Pagination** (skip/take). Sorts automatically by `createdAt` (descending) so the newest notices always appear at the top.
- **POST `/api/notices`**: Creates a new notice with robust server-side validation (ensuring title, body, and dates are present).
- **GET `/api/notices/[id]`**: Retrieves a single notice by ID for editing.
- **PUT `/api/notices/[id]`**: Updates an existing notice with strict server-side validation.
- **DELETE `/api/notices/[id]`**: Deletes a notice by ID after user confirmation via a custom modal dialog.

### Advanced Capabilities:
- **Real-Time Search & Pagination:** Features a debounced search bar and a "Load More" pagination system to ensure high performance with large datasets.
- **Single Reusable Add / Edit Form:** One component (`components/NoticeForm.jsx`) handles both creation and editing. When editing, it automatically loads and populates the notice's current values.
- **Responsive & Premium Glassmorphism Design:** A beautiful, responsive grid layout for desktop, tablet, and phone screens featuring a vibrant mesh background and translucent "frosted glass" UI elements.
- **Lazy Loading:** All notice images use native `loading="lazy"` to optimize bandwidth and page speed.

---

## 🛠 Required Tech Stack Used

- **Framework:** Next.js (Pages Router under `pages/`)
- **Database Access / ORM:** Prisma ORM (`@prisma/client`)
- **Database:** TiDB Cloud Serverless (MySQL Compatible)
- **Styling:** Tailwind CSS (v4) with custom Glassmorphism UI
- **Deployment:** Vercel

---

## 📦 How to Run the Project Locally (Step-by-Step)

Follow these instructions to set up and run the project on your local computer from scratch.

### Prerequisites
1. **Node.js**: Ensure you have Node.js (v18 or higher) installed on your system.
2. **Git**: Ensure Git is installed to clone the repository.
3. **TiDB Cloud Account**: A free TiDB Serverless cluster for the database.

### Step 1: Clone the Repository
Open your terminal or command prompt and run:
```bash
git clone https://github.com/Ashmit8736/NoticeBoard.git
cd NoticeBoard
```

### Step 2: Install Dependencies
Install all the required Node packages (Next.js, Prisma, Tailwind, etc.):
```bash
npm install
```

### Step 3: Set up Environment Variables
In the root directory of the project, create a new file named `.env`. Open this file and add your TiDB Cloud database connection string. It should look exactly like this:
```env
DATABASE_URL="mysql://<username>:<password>@<host>:4000/<database>?sslaccept=strict"
```
*(Replace the `<username>`, `<password>`, `<host>`, and `<database>` with your actual TiDB credentials).*

### Step 4: Push Database Schema
Tell Prisma to create the necessary tables in your TiDB database based on the schema:
```bash
npx prisma db push
```

### Step 5: Start the Development Server
Run the local development server:
```bash
npm run dev
```

### Step 6: View the Application
Open your web browser and navigate to:
[http://localhost:3000](http://localhost:3000)

---

## ☁️ Deploying to Vercel

This project is fully configured for zero-downtime deployment on Vercel.

1. Create a new project in [Vercel](https://vercel.com) and import this GitHub repository.
2. In the **Environment Variables** section of the Vercel deployment settings, add:
   - **Key:** `DATABASE_URL`
   - **Value:** Your full TiDB connection string (same as the `.env` file).
3. We have already added a `postinstall` script in `package.json` (`"postinstall": "prisma generate"`). Vercel will automatically generate the Prisma client during the build step.
4. Click **Deploy**.

---

## 💡 One Thing I Would Improve With More Time

With more time, I would implement **Role-Based Access Control (RBAC) & Authentication**. 

Currently, anyone who visits the live URL can create, edit, or delete notices. By integrating a solution like **NextAuth.js**, I would ensure that only authenticated faculty, administrators, or authorized staff can manage notices. Regular students and visitors would only have "read-only" access to view the dashboard and read the notices. This is a critical security requirement for a real-world institutional notice board.

---

## 🤖 Where and How AI Was Used

AI (Google DeepMind / Gemini) was utilized extensively as an AI pair programmer throughout the development lifecycle:

1. **Architecture & API Routes:** AI was used to scaffold the Next.js API route handlers (`/api/notices`) and implement robust server-side validation.
2. **Advanced Features:** Consulted AI to design and implement complex logic like Debounced Database Searching and "Load More" Pagination to ensure the app scales efficiently.
3. **UI/UX & Glassmorphism Design:** Used AI to brainstorm and implement the premium "Glassmorphism" design system using Tailwind CSS, including the vibrant mesh background, translucent frosted glass containers, hover animations, and the custom urgent/category badges.
4. **Debugging:** Relied on AI to debug deployment issues (e.g., adding Vercel `postinstall` scripts for Prisma) and Prisma sorting logic to ensure the newest notices consistently appear at the top of the feed.
