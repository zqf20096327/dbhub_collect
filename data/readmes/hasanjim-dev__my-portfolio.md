# Muntasir Hasan Jim — Portfolio

My personal portfolio website, built to showcase my projects, skills, and certificates.

🔗 **Live site:** [muntasirhasanjim.vercel.app](https://muntasirhasanjim.vercel.app)

## Features

- Responsive, single-page design with smooth-scroll navigation
- Sections: Home, About, Skills, Projects, Certificates, Contact
- Category-based Skills section (Frontend, Backend, Database, Tools)
- Animated particle background
- Typewriter effect for role/title text
- Contact form with email notifications
- Resume (PDF) download
- Image upload for projects/certificates via Cloudinary
- Admin panel with login (bcrypt-hashed password) for managing content

## Tech Stack

**Frontend:** React, Vite, React Router, React Icons, tsparticles, Typewriter Effect
**Backend:** Node.js, Express
**Database:** MySQL (hosted on Aiven)
**Image Storage:** Cloudinary (via Multer)
**Deployment:** Vercel (frontend) + Render (backend) + Aiven (MySQL database)

## Getting Started

### Frontend

```bash
git clone https://github.com/hasanjim-dev/my-portfolio.git
cd my-portfolio
npm install
npm run dev
```

### Backend

```bash
cd backend
npm install
npm start
```

Create a `.env` file inside `backend/` with your own MySQL (Aiven), Cloudinary, and mail credentials — see `.env.example` if provided, or ask the repo owner for the required variable names. **Never commit your `.env` file.**

## Folder Structure

```
my-portfolio/
├─ public/                  # Static assets (favicon, icons, resume PDF)
├─ src/
│  ├─ assets/               # Images used in the UI (hero image, logos)
│  ├─ components/           # Navbar, Home, About, Skills, Projects,
│  │                        # Certificates, Contact, Footer, Admin, AdminLogin,
│  │                        # ParticleBackground
│  ├─ App.jsx               # Routes (/, /admin-login, /admin) and page layout
│  ├─ App.css               # Component/section styling
│  ├─ index.css             # Global styles (resets, root variables)
│  └─ main.jsx               # React entry point
├─ backend/
│  ├─ server.js             # Express server & API routes
│  ├─ uploads/              # Temp storage for uploaded images (pre-Cloudinary)
│  ├─ .env                  # Backend secrets (MySQL/Aiven, Cloudinary, mail) — not committed
│  └─ package.json
├─ vercel.json              # SPA rewrite rules for Vercel
├─ vite.config.js
└─ package.json
```

## Contact

- Email: hasanjim2345@gmail.com
- LinkedIn: [muntasir-hasan-jim](https://linkedin.com/in/muntasir-hasan-jim-1804b643a)
