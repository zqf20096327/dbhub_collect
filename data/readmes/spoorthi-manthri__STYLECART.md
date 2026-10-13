# STYLECART — React frontend (Spring Boot edition)

This is the STYLECART clothing shopping and tailor customization frontend. Supabase has been removed. Persistent actions are configured to use your Java Spring Boot REST API and TiDB/MySQL-compatible database.

## Technology
- React + TypeScript + Vite
- React Router
- Tailwind CSS
- Java Spring Boot REST API (separate backend project)
- TiDB Cloud / MySQL-compatible database (configured by the backend)

## Run the website in IntelliJ IDEA

1. Extract this ZIP to a folder, for example `E:\\STYLECART\\stylecart-frontend`.
2. Open that folder in IntelliJ IDEA. Open the folder that contains `package.json` (not its parent folder).
3. Install Node.js LTS if it is not already installed: https://nodejs.org/
4. Open IntelliJ's Terminal in the frontend folder and run:

   ```bash
   npm install
   npm run dev
   ```

5. Open the local URL Vite prints, usually `http://localhost:5173`.

To create a production build, run `npm run build`.

## Connect to Java Spring Boot

During local development, the frontend uses Vite’s `/api` proxy to `http://localhost:8081`, avoiding browser CORS issues. If your backend uses another URL, copy `.env.example` to `.env.local`, set `VITE_API_BASE_URL` to the full API base URL, then restart Vite.

The frontend currently expects these REST endpoints:

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/products` | List products; sample products appear if the API is offline or returns an empty list |
| POST | `/api/auth/register` | Register with `{ "name": "...", "email": "...", "password": "..." }` |
| POST | `/api/auth/login` | Login with `{ "email": "...", "password": "..." }` |
| POST | `/api/orders` | Save a checkout order |
| POST | `/api/tailor-requests` | Save a tailor/alteration request |

For register/login, the expected response is `{ "user": { "id": 1, "email": "person@example.com", "name": "Person" }, "token": "optional-jwt-token" }`. The `token` is optional unless your backend uses authenticated endpoints. Error responses may return a `message` or `error` field.

**Important:** this ZIP contains the frontend, not the Java backend. If your existing backend uses different endpoint paths or request/response fields, update `src/api/client.ts` to match it, or add the corresponding Spring Boot controllers/services/entities. Product browsing can display sample data without the backend, but login, order placement, and tailor request submission require the matching Java endpoints to be running. The UI will show an error rather than falsely confirming a database write.

## Features included
- Home page and clothing category browsing
- Browse by fabric/material
- Product cards with size/color choices
- Cart with quantity updates and totals
- Checkout with delivery details, preferred date/time and Cash on Delivery
- Separate tailor service request form for alterations and custom stitching
- Login and registration UI wired to Spring Boot endpoints
- Responsive navigation and styling

## Notes
- Supabase package, client, environment file, and migration folder have been removed.
- Tailor reference images currently preview locally in the browser only. File upload/storage is not connected; the selected image is not sent to the backend.
- Do not commit `.env.local`, database passwords, API secrets, or JWT secrets to GitHub.
- The cart is currently maintained in frontend state; persistent server-side cart APIs can be connected separately.
