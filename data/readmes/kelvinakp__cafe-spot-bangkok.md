# Cafe Spot Bangkok (CSC452)

Flutter + Express + TiDB + Vercel final project.

## Structure

```text
MP-project/
  backend/              Express API
  cafe_spot_bangkok/    Flutter app
  project.md            Requirements
  README.md
```

## Run backend

```powershell
cd backend
npm install
npm start
```

API: http://localhost:3000  
Needs `backend/.env` with TiDB `DATABASE_URL` (see `.env.example`).  
Seed DB with `seed.sql` in DBeaver if tables are empty.

## Run Flutter

```powershell
cd cafe_spot_bangkok
flutter pub get
flutter run
```

Login: any email with `@`, password ≥ 6 chars.  
Demo saves: `demo@gmail.com` / `123456`

## Features

- Explore Bangkok cafes (read + filters)
- My Saves CRUD by category
- Splash → Login → Tabs
- Deploy API to Vercel for marks
